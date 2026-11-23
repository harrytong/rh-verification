import json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from test_driver import a,HERE

class DescentTests(unittest.TestCase):
    def test_target_and_helper_contract(self):
        cfg=json.loads((HERE/'descent-targets.json').read_text());text=(HERE/'ThetaDescent.lean').read_text()
        self.assertEqual(len(cfg['targets']),8);self.assertEqual(len(set(cfg['targets'])),8)
        self.assertEqual(cfg['targets'],json.loads((HERE/'chain-targets.json').read_text())['descent'])
        helper=(HERE/'ProvenanceHelpers.lean.txt').read_text()
        self.assertEqual(text.count(helper),1);self.assertIn(helper,(HERE/'ProvenanceFixture.lean').read_text())
        for t in cfg['targets']:
            for marker in ['inspect env "'+t+'" 4096','#print '+t+'\n','#print axioms '+t+'\n','RH_STAGE3_DECL_BEGIN '+t+'"','RH_STAGE3_DECL_END '+t+'"']:self.assertEqual(text.count(marker),1)
        self.assertEqual(text.count('import Main\n'),1);self.assertNotIn('RHStage3Search',text)
        self.assertIn('descent',a.RECORDS)

    def run_phase(self,fail_at=None):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);project=p/'project';tc=p/'tc';out=p/'out'
            for x in [project,tc,out]:x.mkdir()
            cfg=json.loads((HERE/'descent-targets.json').read_text());calls=[]
            def logged(argv,log,cid,seconds):
                name=log.stem;calls.append(name)
                if name==fail_at:return 1,'/audit/ThetaDescent.lean:1:0: error: Target not found'
                if name=='positive':return 0,'RH_STAGE3_CONTEXT FIXTURE\nRH_STAGE3_POSITIVE_FIXTURE_END'
                if name=='negative':return 1,'/audit/NegativeFixture.lean:4:19: error: Type mismatch\n True\n False'
                if name=='provenance-fixture':return 0,'RH_STAGE3_PROVENANCE_FIXTURE_END'
                if name=='descent':
                    text=''
                    for t in cfg['targets']:
                        for r in [dict(event='target',target=t,module='Development.Test',kind='theorem',has_body=True)]+[dict(event='references',target=t,location=loc,total=0,retained=0,limit=4096,truncated=False,references=[]) for loc in ['type','body']]:text+='RH_STAGE3_PROVENANCE_JSON\t'+json.dumps(r)+'\n'
                        text+='RH_STAGE3_DECL_BEGIN '+t+'\nsynthetic content\nRH_STAGE3_DECL_END '+t+'\n'
                    return 0,text+'RH_STAGE3_DESCENT_END'
                raise AssertionError(name)
            with patch.object(sys,'argv',['audit_stage3.py','--phase','descent','--project',str(project),'--toolchain',str(tc)]),patch.object(a,'package_files',return_value=[]),patch.object(a,'validate',return_value={}),patch.object(a,'new_output',return_value=out),patch.object(a,'check_resources',return_value={}),patch.object(a.subprocess,'run'),patch.object(a,'command',return_value='sha256:test'),patch.object(a,'run_logged',side_effect=logged),patch.object(a,'validate_provenance_fixture',return_value={}),patch.object(a,'collect_provenance_sources',return_value=dict(total_bytes=0,files=[])):
                rc=a.main()
            m=json.loads((out/'run-metadata.json').read_text());success=fail_at is None
            self.assertEqual(m['phase_completed'],success);self.assertEqual(rc,0 if success else 1)
            self.assertEqual(m['descent_protocol_sha256'],a.sha256(HERE/'DESCENT_PROTOCOL.md'))
            self.assertEqual(m['descent_targets_sha256'],a.sha256(HERE/'descent-targets.json'))
            self.assertEqual(calls,['positive','negative','provenance-fixture']+([] if fail_at=='provenance-fixture' else ['descent']))
            if success:
                self.assertTrue((out/'descent-provenance.json').is_file());self.assertTrue((out/'descent-blocks.json').is_file())
            else:self.assertIn('failure',m)
            self.assertTrue((out/'stage3-evidence.zip').is_file())

    def test_success_outputs(self):self.run_phase()
    def test_fixture_failure_blocks_main(self):self.run_phase('provenance-fixture')
    def test_project_failure_preserves_failure(self):self.run_phase('descent')

if __name__=='__main__':unittest.main()
