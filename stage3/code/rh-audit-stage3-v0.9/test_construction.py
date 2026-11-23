import json,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from test_driver import a,HERE

class ConstructionTests(unittest.TestCase):
    def test_targets_and_shared_helper(self):
        cfg=json.loads((HERE/'construction-targets.json').read_text())
        text=(HERE/'Construction.lean').read_text()
        self.assertEqual(len(cfg['targets']),8)
        self.assertEqual(cfg['targets'],json.loads((HERE/'chain-targets.json').read_text())['construction'])
        helper=(HERE/'ProvenanceHelpers.lean.txt').read_text()
        self.assertEqual(text.count(helper),1)
        self.assertIn(helper,(HERE/'ProvenanceFixture.lean').read_text())
        for target in cfg['targets']:
            for marker in ['inspect env "'+target+'" 4096','#print '+target+'\n','#print axioms '+target+'\n','RH_STAGE3_DECL_BEGIN '+target+'"','RH_STAGE3_DECL_END '+target+'"']:
                self.assertEqual(text.count(marker),1)
        self.assertIn('construction',a.RECORDS)
        self.assertNotIn('RHStage3Search',text)

    def test_focused_source_selection_and_import_context(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);out=p/'out';out.mkdir();src=p/'project/src/Development';src.mkdir(parents=True)
            files={'Owner':'import Development.Child\n','Child':'-- child\n','Finiteness':'-- fin\n','Explicit':'-- explicit\n','Noise':'-- noise\n'}
            for n,t in files.items():(src/(n+'.lean')).write_text(t)
            result=dict(records=[dict(event='target',module='Development.Owner'),dict(event='references',references=[dict(module='Development.Noise'),dict(module='Development.Finiteness')])],any_reference_truncated=False)
            cfg=dict(source_import_depth=2,max_source_files=10,max_source_file_bytes=1000,max_source_total_bytes=10000,source_reference_mode='priority-only',priority_module_fragments=['Finiteness'],priority_source_roots=['Development/Explicit.lean'])
            def git(args,**kw):return subprocess.CompletedProcess(args,0,(p/'project'/args[-1].split(':',1)[1]).read_bytes(),b'')
            with patch.object(a.subprocess,'run',side_effect=git):r=a.collect_provenance_sources(p/'project',out,result,cfg)
            names=[x['source'] for x in r['files']]
            self.assertEqual(names,['src/Development/Owner.lean','src/Development/Explicit.lean','src/Development/Finiteness.lean','src/Development/Child.lean'])
            self.assertEqual(r['selection']['reference_modules_not_seeded'],['Development.Noise'])

    def test_bad_source_mode_rejected(self):
        with self.assertRaises(RuntimeError):a.collect_provenance_sources(Path('.'),Path('.'),dict(records=[]),dict(source_reference_mode='typo'))

    def test_lexical_hits_include_comments_and_record_limits(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d);p=out/'sample.lean'
            p.write_text('-- EMtTheta in a comment\nth := '+ 'x'*1200+'\n'+('def x : EMtTheta := foo\n'*2001))
            c=dict(files=[dict(status='collected-and-git-verified',evidence_path='sample.lean',sha256=a.sha256(p))])
            r=a.construction_source_hits(out,c)
            self.assertEqual(r['records'][0]['line'],1)
            self.assertIn('comments included',r['method'])
            self.assertTrue(r['records'][1]['text_truncated'])
            self.assertTrue(r['truncated']);self.assertEqual(len(r['records']),2000)

    def test_lexical_hits_do_not_read_excluded_sources(self):
        with tempfile.TemporaryDirectory() as d:
            r=a.construction_source_hits(Path(d),dict(files=[dict(status='file-count-cap',source='missing.lean')]))
            self.assertEqual(r['records'],[])
            with self.assertRaises(RuntimeError):a.construction_source_hits(Path(d),dict(files=[dict(status='collected-and-git-verified',evidence_path='../outside')]))

    def run_mock_phase(self, fixture_ok):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);project=p/'project';tc=p/'tc';out=p/'out'
            for x in [project,tc,out]:x.mkdir()
            cfg=json.loads((HERE/'construction-targets.json').read_text());calls=[]
            def logged(argv,log,cid,seconds):
                name=log.stem;calls.append(name)
                if name=='positive':return 0,'RH_STAGE3_CONTEXT FIXTURE\nRH_STAGE3_POSITIVE_FIXTURE_END'
                if name=='negative':return 1,'/audit/NegativeFixture.lean:4:19: error: Type mismatch\n True\n False'
                if name=='provenance-fixture':return (0,'RH_STAGE3_PROVENANCE_FIXTURE_END') if fixture_ok else (1,'fixture failed')
                if name=='construction':
                    logtext=''
                    for t in cfg['targets']:
                        for r in [dict(event='target',target=t,module='Development.Test',kind='theorem',has_body=True)]+[dict(event='references',target=t,location=loc,total=0,retained=0,limit=4096,truncated=False,references=[]) for loc in ['type','body']]:
                            logtext+='RH_STAGE3_PROVENANCE_JSON\t'+json.dumps(r)+'\n'
                        logtext+='RH_STAGE3_DECL_BEGIN '+t+'\nsynthetic content\nRH_STAGE3_DECL_END '+t+'\n'
                    return 0,logtext+'RH_STAGE3_CONSTRUCTION_END'
                raise AssertionError(name)
            collected=dict(total_bytes=0,files=[])
            with patch.object(sys,'argv',['audit_stage3.py','--phase','construction','--project',str(project),'--toolchain',str(tc)]),patch.object(a,'package_files',return_value=[]),patch.object(a,'validate',return_value={}),patch.object(a,'new_output',return_value=out),patch.object(a,'check_resources',return_value={}),patch.object(a.subprocess,'run'),patch.object(a,'command',return_value='sha256:test'),patch.object(a,'run_logged',side_effect=logged),patch.object(a,'validate_provenance_fixture',return_value={}),patch.object(a,'collect_provenance_sources',return_value=collected):
                rc=a.main()
            m=json.loads((out/'run-metadata.json').read_text())
            self.assertEqual(m['phase_completed'],fixture_ok)
            self.assertEqual(m['construction_protocol_sha256'],a.sha256(HERE/'CONSTRUCTION_PROTOCOL.md'))
            self.assertEqual(rc,0 if fixture_ok else 1)
            self.assertEqual(calls,['positive','negative','provenance-fixture']+(['construction'] if fixture_ok else []))
            if fixture_ok:
                self.assertTrue((out/'construction-provenance.json').is_file())
                self.assertTrue((out/'construction-blocks.json').is_file())
                self.assertTrue((out/'construction-source-hits.json').is_file())
            self.assertTrue((out/'stage3-evidence.zip').is_file())

    def test_phase_success_writes_evidence(self):self.run_mock_phase(True)
    def test_phase_fixture_failure_stops_before_project(self):self.run_mock_phase(False)

if __name__=='__main__':unittest.main()
