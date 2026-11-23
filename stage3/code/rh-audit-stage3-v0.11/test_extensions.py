import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch
from test_driver import a,HERE

class ExtensionTests(unittest.TestCase):
    def test_frozen_targets_shared_helpers_and_complete_print_markers(self):
        cfg=json.loads((HERE/'extension-targets.json').read_text())
        text=(HERE/'Extensions.lean').read_text()
        self.assertEqual(len(cfg['targets']),18)
        self.assertEqual(len(set(cfg['targets'])),18)
        self.assertEqual(cfg['targets'],json.loads((HERE/'chain-targets.json').read_text())['extensions'])
        for helper in ['ProvenanceHelpers.lean.txt','TargetSearchHelpers.lean.txt']:
            h=(HERE/helper).read_text()
            self.assertEqual(text.count(h),1)
            self.assertEqual((HERE/'TargetSearchFixture.lean').read_text().count(h),1)
        for t in cfg['targets']:
            for s in ['inspect env "'+t+'" 4096','#print '+t+'\n','#print axioms '+t+'\n',
                      'RH_STAGE3_DECL_BEGIN '+t+'"','RH_STAGE3_DECL_END '+t+'"']:
                self.assertEqual(text.count(s),1)
        for r in cfg['searches']:
            self.assertIn('RHStage3Search.inspect env "'+r['target']+'" "'+r['binder']+'"',text)
        self.assertEqual(len(cfg['searches']),2)
        self.assertIn('extensions',a.RECORDS)

    def test_extensions_fixture_failure_stops_before_main(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); project=p/'project';tc=p/'tc';out=p/'out'
            for x in [project,tc,out]:x.mkdir()
            calls=[]
            def logged(argv,log,cid,seconds):
                name=log.stem;calls.append(name)
                if name=='positive':return 0,'RH_STAGE3_CONTEXT FIXTURE\nRH_STAGE3_POSITIVE_FIXTURE_END'
                if name=='negative':return 1,'/audit/NegativeFixture.lean:4:19: error: Type mismatch\n True\n False'
                if name=='provenance-fixture':return 0,'RH_STAGE3_PROVENANCE_FIXTURE_END'
                if name=='search-fixture':return 1,'fixture failed'
                raise AssertionError('project must not start')
            with patch.object(sys,'argv',['audit_stage3.py','--phase','extensions','--project',str(project),'--toolchain',str(tc)]),\
                 patch.object(a,'package_files',return_value=[]),patch.object(a,'validate',return_value={}),\
                 patch.object(a,'new_output',return_value=out),patch.object(a,'check_resources',return_value={}),\
                 patch.object(a.subprocess,'run'),patch.object(a,'command',return_value='sha256:test'),\
                 patch.object(a,'run_logged',side_effect=logged),patch.object(a,'validate_provenance_fixture',return_value={}):
                self.assertEqual(a.main(),1)
            self.assertEqual(calls,['positive','negative','provenance-fixture','search-fixture'])
            meta=json.loads((out/'run-metadata.json').read_text())
            self.assertFalse(meta['phase_completed']);self.assertIn('failure',meta)
            self.assertTrue((out/'stage3-evidence.zip').is_file())
            self.assertEqual(meta['extension_protocol_sha256'],a.sha256(HERE/'EXTENSION_PROTOCOL.md'))

    def test_explicit_source_priority_before_reference_fillers(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);project=p/'project';out=p/'out';out.mkdir();src=project/'src/Development';src.mkdir(parents=True)
            for n in ['Owner','Explicit','Filler']:(src/(n+'.lean')).write_text('-- '+n+'\n')
            result=dict(records=[dict(event='target',module='Development.Owner'),dict(event='references',references=[dict(module='Development.Filler')])],any_reference_truncated=False)
            cfg=dict(source_import_depth=0,max_source_files=2,max_source_file_bytes=100,max_source_total_bytes=300,priority_source_roots=['Development/Explicit.lean'])
            def git(args,**kw):return subprocess.CompletedProcess(args,0,(project/'src'/args[-1].split(':src/',1)[1]).read_bytes(),b'')
            with patch.object(a.subprocess,'run',side_effect=git):x=a.collect_provenance_sources(project,out,result,cfg)
            self.assertEqual([r['source'] for r in x['files']],['src/Development/Owner.lean','src/Development/Explicit.lean','src/Development/Filler.lean'])
            self.assertEqual(x['files'][-1]['status'],'file-count-cap')
            self.assertEqual(x['selection']['explicit_priority_source_roots'],cfg['priority_source_roots'])

    def test_unsafe_explicit_source_path_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            result=dict(records=[],any_reference_truncated=False)
            cfg=dict(source_import_depth=0,max_source_files=2,max_source_file_bytes=100,max_source_total_bytes=300,priority_source_roots=['../outside.lean'])
            with self.assertRaises(RuntimeError):a.collect_provenance_sources(Path(d),Path(d),result,cfg)

    def test_missing_explicit_source_is_recorded_not_success(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);out=p/'out';out.mkdir()
            result=dict(records=[],any_reference_truncated=False)
            cfg=dict(source_import_depth=0,max_source_files=2,max_source_file_bytes=100,max_source_total_bytes=300,priority_source_roots=['Development/Missing.lean'])
            x=a.collect_provenance_sources(p,out,result,cfg)
            self.assertEqual(x['files'][0]['status'],'not-found-at-requested-path')
            self.assertEqual(x['total_bytes'],0)

if __name__=='__main__':unittest.main()
