import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch
from test_driver import a,HERE

class UseTests(unittest.TestCase):
    cfg=dict(max_binders=128,node_limit_per_binder=100000,depth_limit=600)
    def text(self,rows):
        return '\n'.join('RH_STAGE3_USES_JSON\t'+json.dumps(r) for r in rows)
    def rows(self,target='A'):
        return [dict(event='binder',target=target,ordinal=0,name='h',
                     binder_or_let_type_position=0,other_expression_position=1,
                     nodes_visited=3,node_limit=100000,depth_limit=600,truncated=False),
                dict(event='end',target=target,binder_count=1,stop='non-lambda-head')]
    def test_locations_and_limits_are_not_necessity(self):
        r=a.validate_uses(self.text(self.rows()),['A'],self.cfg)
        self.assertFalse(r['any_occurrence_truncated'])
        self.assertIn('semantic necessity',r['not_established'])
        self.assertIn('hypothesis discharge',r['not_established'])
        self.assertEqual(r['records'][0]['other_expression_position'],1)
    def test_no_binder_is_not_a_missing_target(self):
        r=a.validate_uses(self.text([dict(event='end',target='A',binder_count=0,stop='non-lambda-head')]),['A'],self.cfg)
        self.assertFalse(r['any_occurrence_truncated'])
        self.assertIn('all binders exposed',r['not_established'])
    def test_truncated_zero_is_unknown(self):
        rows=self.rows();rows[0].update(truncated=True,other_expression_position=0)
        r=a.validate_uses(self.text(rows),['A'],self.cfg)
        self.assertTrue(r['any_occurrence_truncated'])
        rows[0]['truncated']=False;rows[1]['stop']='outer-step-cap'
        self.assertTrue(a.validate_uses(self.text(rows),['A'],self.cfg)['any_occurrence_truncated'])
    def test_rejects_false_completion_duplicate_budget_order_and_invalid_counts(self):
        good=self.rows()
        variants=[good[:-1],good+[good[-1]],good[::-1],good+[dict(event='fixture',case='x',passed=True)]]
        for key,value in [('ordinal',1),('node_limit',1),('depth_limit',12),
                          ('other_expression_position',4),('truncated',0),('nodes_visited',-1),
                          ('target','B'),('binder_or_let_type_position',True)]:
            rows=json.loads(json.dumps(good));rows[0][key]=value;variants.append(rows)
        for key,value in [('binder_count',2),('stop','complete'),('stop','binder-cap')]:
            rows=json.loads(json.dumps(good));rows[1][key]=value;variants.append(rows)
        for rows in variants:
            with self.assertRaises(RuntimeError):a.validate_uses(self.text(rows),['A'],self.cfg)
        for text in ['','RH_STAGE3_USES_JSON\t{','RH_STAGE3_USES_JSON\t[]']:
            with self.assertRaises(RuntimeError):a.use_records(text)
    def fixture_rows(self):
        return ([dict(event='fixture',case=c,passed=True) for c in a.USE_FIXTURE_CASES]
          +self.rows('RHStage3UsesFixture.identity')
          +[dict(event='end',target='synthetic-outer-cap',binder_count=0,stop='outer-step-cap'),
            dict(event='end',target='synthetic-binder-cap',binder_count=128,stop='binder-cap')])
    def test_fixture_validator_checks_actual_identity_counts_and_every_case(self):
        good=self.fixture_rows()
        self.assertEqual(len(a.validate_use_fixture(self.text(good))['checks']),15)
        for rows in [good[1:],good+[good[0]],good[:-1]]:
            with self.assertRaises(RuntimeError):a.validate_use_fixture(self.text(rows))
        bad=json.loads(json.dumps(good));bad[12]['other_expression_position']=0
        with self.assertRaises(RuntimeError):a.validate_use_fixture(self.text(bad))
    def test_helpers_byte_identical_and_targets_frozen(self):
        helper=(HERE/'ArgumentUseHelpers.lean.txt').read_text()
        prov=(HERE/'ProvenanceHelpers.lean.txt').read_text()
        for name in ['ArgumentUseFixture.lean','ArgumentUses.lean']:
            source=(HERE/name).read_text()
            self.assertEqual(source.count(helper),1)
            self.assertEqual(source.count(prov),1)
        self.assertNotIn('import Main',(HERE/'ArgumentUseFixture.lean').read_text())
        cfg=json.loads((HERE/'use-targets.json').read_text())
        self.assertEqual(cfg['targets'],json.loads((HERE/'chain-targets.json').read_text())['uses'])
        self.assertEqual(len(cfg['targets']),10)
        for target in cfg['targets']:
            self.assertIn('RHStage3Uses.inspect env "'+target+'"',(HERE/'ArgumentUses.lean').read_text())
    def test_fixture_failure_blocks_project_import_and_archives(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);project=p/'project';tc=p/'tc';out=p/'out'
            for x in [project,tc,out]:x.mkdir()
            calls=[]
            def logged(argv,logfile,cidfile,seconds):
                calls.append(logfile.stem)
                if logfile.stem=='positive':return 0,'RH_STAGE3_CONTEXT FIXTURE RH_STAGE3_POSITIVE_FIXTURE_END'
                if logfile.stem=='negative':return 1,'/audit/NegativeFixture.lean:1:0: error: Type mismatch'
                if logfile.stem=='provenance-fixture':return 0,'RH_STAGE3_PROVENANCE_FIXTURE_END'
                if logfile.stem=='use-fixture':return 0,'RH_STAGE3_USE_FIXTURE_END'
                raise AssertionError('project must not start')
            args=['audit_stage3.py','--phase','uses','--project',str(project),'--toolchain',str(tc)]
            with patch.object(sys,'argv',args),patch.object(a,'package_files',return_value=[]),\
                patch.object(a,'validate',return_value={}),patch.object(a,'new_output',return_value=out),\
                patch.object(a,'check_resources',return_value={}),patch.object(a.subprocess,'run'),\
                patch.object(a,'command',return_value='sha256:test'),patch.object(a,'run_logged',side_effect=logged),\
                patch.object(a,'validate_provenance_fixture',return_value={}):
                self.assertEqual(a.main(),1)
            self.assertEqual(calls,['positive','negative','provenance-fixture','use-fixture'])
            self.assertTrue((out/'stage3-evidence.zip').is_file())
            meta=json.loads((out/'run-metadata.json').read_text())
            self.assertFalse(meta['phase_completed'])
    def test_project_probe_keeps_same_sandbox_and_does_not_copy_export(self):
        argv=a.docker_command(Path('/project'),Path('/toolchain'),Path('/evidence'),
                              'sha256:test',Path('/evidence/uses.cid'),'ArgumentUses.lean',1800,100,False)
        self.assertIn('--read-only',argv)
        self.assertIn('type=bind,src=/project,dst=/project,readonly',argv)
        self.assertNotIn('solution.export',' '.join(argv))
        self.assertNotIn('comparator',' '.join(argv))

if __name__=='__main__':unittest.main()
