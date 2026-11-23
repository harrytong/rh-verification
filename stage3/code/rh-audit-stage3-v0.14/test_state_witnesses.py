import json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from test_driver import a,HERE

class StateWitnessTests(unittest.TestCase):
    def test_target_and_helper_contract(self):
        cfg=json.loads((HERE/'state-witness-targets.json').read_text());text=(HERE/'StateWitnesses.lean').read_text()
        self.assertEqual(len(cfg['targets']),25);self.assertEqual(len(set(cfg['targets'])),25)
        self.assertEqual(cfg['targets'],json.loads((HERE/'chain-targets.json').read_text())['state-witnesses'])
        helper=(HERE/'ProvenanceHelpers.lean.txt').read_text()
        self.assertEqual(text.count(helper),1);self.assertIn(helper,(HERE/'ProvenanceFixture.lean').read_text())
        for t in cfg['targets']:
            for marker in ['inspect env "'+t+'" 4096','#print '+t+'\n','#print axioms '+t+'\n','RH_STAGE3_DECL_BEGIN '+t+'"','RH_STAGE3_DECL_END '+t+'"']:self.assertEqual(text.count(marker),1)
        self.assertEqual(text.count('import Main\n'),1);self.assertNotIn('RHStage3Search',text)
        self.assertIn('state-witnesses',a.RECORDS)

    def run_phase(self,fail_at=None):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);project=p/'project';tc=p/'tc';out=p/'out'
            for x in [project,tc,out]:x.mkdir()
            cfg=json.loads((HERE/'state-witness-targets.json').read_text());calls=[]
            def logged(argv,log,cid,seconds):
                name=log.stem;calls.append(name)
                if name==fail_at:return 1,'/audit/StateWitnesses.lean:1:0: error: Target not found'
                if name=='positive':return 0,'RH_STAGE3_CONTEXT FIXTURE\nRH_STAGE3_POSITIVE_FIXTURE_END'
                if name=='negative':return 1,'/audit/NegativeFixture.lean:4:19: error: Type mismatch\n True\n False'
                if name=='provenance-fixture':return 0,'RH_STAGE3_PROVENANCE_FIXTURE_END'
                if name=='state-witnesses':
                    text=''
                    for t in cfg['targets']:
                        for r in [dict(event='target',target=t,module='Development.Test',kind='theorem',has_body=True)]+[dict(event='references',target=t,location=loc,total=0,retained=0,limit=4096,truncated=False,references=[]) for loc in ['type','body']]:text+='RH_STAGE3_PROVENANCE_JSON\t'+json.dumps(r)+'\n'
                        text+='RH_STAGE3_DECL_BEGIN '+t+'\nsynthetic content\nRH_STAGE3_DECL_END '+t+'\n'
                    return 0,text+'RH_STAGE3_STATE_WITNESSES_END'
                raise AssertionError(name)
            with patch.object(sys,'argv',['audit_stage3.py','--phase','state-witnesses','--project',str(project),'--toolchain',str(tc)]),patch.object(a,'package_files',return_value=[]),patch.object(a,'validate',return_value={}),patch.object(a,'new_output',return_value=out),patch.object(a,'check_resources',return_value={}),patch.object(a.subprocess,'run'),patch.object(a,'command',return_value='sha256:test'),patch.object(a,'run_logged',side_effect=logged),patch.object(a,'validate_provenance_fixture',return_value={}),patch.object(a,'pinned_witness_navigation',return_value=dict(groups=[],selected_source_paths=[])),patch.object(a,'collect_provenance_sources',return_value=dict(total_bytes=0,files=[])):
                rc=a.main()
            m=json.loads((out/'run-metadata.json').read_text());success=fail_at is None
            self.assertEqual(m['phase_completed'],success);self.assertEqual(rc,0 if success else 1)
            self.assertEqual(m['state_witness_protocol_sha256'],a.sha256(HERE/'STATE_WITNESS_PROTOCOL.md'))
            self.assertEqual(m['state_witness_targets_sha256'],a.sha256(HERE/'state-witness-targets.json'))
            self.assertEqual(calls,['positive','negative','provenance-fixture']+([] if fail_at=='provenance-fixture' else ['state-witnesses']))
            if success:
                self.assertTrue((out/'state-witness-provenance.json').is_file());self.assertTrue((out/'state-witnesses-blocks.json').is_file())
            else:self.assertIn('failure',m)
            self.assertTrue((out/'stage3-evidence.zip').is_file())

    def test_success_outputs(self):self.run_phase()
    def test_fixture_failure_blocks_main(self):self.run_phase('provenance-fixture')
    def test_project_failure_preserves_failure(self):self.run_phase('state-witnesses')



class NavigationTests(unittest.TestCase):
    def test_pinned_revision_selection_and_no_match(self):
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            def git(*args):
                return subprocess.run(['git',*args],cwd=root,check=True,capture_output=True,text=True).stdout.strip()
            git('init','-q')
            (root/'src/Development').mkdir(parents=True)
            (root/'src/Development/B.lean').write_text('-- exAt := proof\n')
            (root/'src/Development/A.lean').write_text('-- exAt := proof\n')
            git('add','src')
            git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Fixture')
            pin=git('rev-parse','HEAD')
            # Working tree edits must not alter search selection at the pinned revision.
            (root/'src/Development/A.lean').write_text('-- changed\n')
            cfg=dict(groups=[dict(label='assignment',pattern='exAt'),dict(label='absent',pattern='NO_MATCH_HERE')],per_group_file_limit=1,timeout_seconds=10,output_limit_bytes=4096,meaning='fixture')
            with patch.object(a,'SOURCE_PIN',pin):result=a.pinned_witness_navigation(root,cfg)
            first=result['groups'][0]
            self.assertEqual(first['total_matching_files'],2)
            self.assertEqual(first['selected_files'],['Development/A.lean'])
            self.assertEqual(first['omitted_files'],['Development/B.lean'])
            self.assertTrue(first['selection_capped'])
            self.assertEqual(result['groups'][1]['exit_status'],1)
            self.assertEqual(result['groups'][1]['total_matching_files'],0)
            # An output overflow is an explicit error, not partial success.
            cfg['output_limit_bytes']=1
            with patch.object(a,'SOURCE_PIN',pin):
                with self.assertRaisesRegex(RuntimeError,'output cap'):a.pinned_witness_navigation(root,cfg)

    def test_failed_git_is_not_absence(self):
        cfg=dict(groups=[dict(label='bad',pattern='[')],per_group_file_limit=1,timeout_seconds=10,output_limit_bytes=4096,meaning='fixture')
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(RuntimeError,'git failure'):a.pinned_witness_navigation(Path(d),cfg)

if __name__=='__main__':unittest.main()
