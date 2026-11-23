import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import json
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("audit_stage3", HERE/"audit_stage3.py")
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

class DriverTests(unittest.TestCase):
    def provenance_text(self, records):
        return '\n'.join('RH_STAGE3_PROVENANCE_JSON\t'+json.dumps(r) for r in records)

    def provenance_example(self):
        return [dict(event='target',target='A',module='Development.A',kind='definition',has_body=True),
                dict(event='references',target='A',location='type',total=1,retained=1,limit=4096,truncated=False,
                     references=[dict(name='Nat',module='Init.Prelude',found=True)]),
                dict(event='references',target='A',location='body',total=1,retained=1,limit=4096,truncated=False,
                     references=[dict(name='B',module='Development.B',found=True)])]

    def test_provenance_keeps_location_and_does_not_claim_necessity(self):
        result=a.validate_provenance(self.provenance_text(self.provenance_example()),['A'],4096)
        self.assertEqual(result['records'][1]['location'],'type')
        self.assertEqual(result['records'][2]['location'],'body')
        self.assertIn('semantic necessity',result['not_established'])
        self.assertFalse(result['any_reference_truncated'])

    def test_provenance_rejects_missing_extra_duplicate_and_inconsistent_records(self):
        good=self.provenance_example()
        wrongcounts=json.loads(json.dumps(good));wrongcounts[1]['total']=2
        wrongflag=json.loads(json.dumps(good));wrongflag[1]['truncated']=True
        wrongbudget=json.loads(json.dumps(good));wrongbudget[1]['limit']=42
        missingbody=good[:2]
        extra=good+[dict(good[1],target='other')]
        for rows in [wrongcounts,wrongflag,wrongbudget,missingbody,extra,good+[good[0]],good+[good[2]]]:
            with self.assertRaises(RuntimeError):
                a.validate_provenance(self.provenance_text(rows),['A'],4096)
        with self.assertRaises(RuntimeError): a.provenance_records('RH_STAGE3_PROVENANCE_JSON\t{')
        with self.assertRaises(RuntimeError): a.provenance_records('no evidence')

    def test_provenance_truncation_is_incomplete_not_absence(self):
        rows=self.provenance_example()
        rows[2].update(total=5000,retained=4096,truncated=True,
                       references=[dict(name='X'+str(i),module='Development.B',found=True) for i in range(4096)])
        result=a.validate_provenance(self.provenance_text(rows),['A'],4096)
        self.assertTrue(result['any_reference_truncated'])

    def test_provenance_helper_identical_in_smoke_and_project(self):
        helper=(HERE/'ProvenanceHelpers.lean.txt').read_text()
        for filename in ['ProvenanceFixture.lean','ConsumerImplementations.lean']:
            self.assertEqual((HERE/filename).read_text().count(helper),1)
        self.assertNotIn('import Main',(HERE/'ProvenanceFixture.lean').read_text())
        config=json.loads((HERE/'provenance-targets.json').read_text())
        self.assertEqual(config['targets'],json.loads((HERE/'chain-targets.json').read_text())['consumers'])
        for target in config['targets']:
            self.assertIn('inspect env "'+target+'" '+str(config['reference_limit_per_location']),
                          (HERE/'ConsumerImplementations.lean').read_text())

    def test_provenance_source_priority_git_check_and_cap(self):
        with tempfile.TemporaryDirectory() as d:
            project=Path(d)/'project';out=Path(d)/'out'
            (project/'src/Development').mkdir(parents=True);out.mkdir()
            (project/'src/Development/A.lean').write_text('import Development.C\n')
            (project/'src/Development/B.lean').write_text('-- child B\n')
            (project/'src/Development/C.lean').write_text('-- child C\n')
            result=a.validate_provenance(self.provenance_text(self.provenance_example()),['A'],4096)
            cfg=dict(source_import_depth=1,max_source_files=2,max_source_file_bytes=100,max_source_total_bytes=200)
            def git(args,**kwargs):
                rel=args[-1].split(':src/',1)[1]
                return subprocess.CompletedProcess(args,0,(project/'src'/rel).read_bytes(),b'')
            with patch.object(a.subprocess,'run',side_effect=git):
                collected=a.collect_provenance_sources(project,out,result,cfg)
            self.assertEqual([r['source'] for r in collected['files']],
                             ['src/Development/A.lean','src/Development/B.lean','src/Development/C.lean'])
            self.assertEqual(collected['files'][-1]['status'],'file-count-cap')
            self.assertEqual(collected['selection']['skipped_modules'],
                             [dict(module='Init.Prelude',reason='outside configured project module prefixes')])
            with patch.object(a.subprocess,'run',return_value=subprocess.CompletedProcess([],0,b'mismatch',b'')):
                with self.assertRaises(RuntimeError): a.collect_provenance_sources(project,out,result,cfg)

    def test_provenance_source_mapping_rejects_unsafe_module(self):
        result=a.validate_provenance(self.provenance_text(self.provenance_example()),['A'],4096)
        result['records'][0]['module']='Development.../escape'
        with self.assertRaises(RuntimeError): a.collect_provenance_sources(Path('/tmp'),Path('/tmp'),result,{})

    def test_consumers_stop_before_main_when_provenance_fixture_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); project=p/'project'; tc=p/'tc';out=p/'results'
            project.mkdir();tc.mkdir();out.mkdir()
            calls=[]
            def logged(argv,logfile,cidfile,seconds):
                calls.append(logfile.stem)
                if logfile.stem=='negative':
                    return 1,'/audit/NegativeFixture.lean:1:0: error: Type mismatch'
                if logfile.stem=='positive':
                    return 0,'RH_STAGE3_CONTEXT FIXTURE RH_STAGE3_POSITIVE_FIXTURE_END'
                return 0,'RH_STAGE3_PROVENANCE_FIXTURE_END'  # Missing JSON must fail closed.
            args=['audit_stage3.py','--phase','consumers','--project',str(project),'--toolchain',str(tc)]
            with patch.object(sys,'argv',args),patch.object(a,'package_files',return_value=[]),\
                 patch.object(a,'validate',return_value={}),patch.object(a,'new_output',return_value=out),\
                 patch.object(a,'check_resources',return_value={}),patch.object(a.subprocess,'run'),\
                 patch.object(a,'command',return_value='sha256:test'),patch.object(a,'run_logged',side_effect=logged):
                self.assertEqual(a.main(),1)
            self.assertEqual(calls,['positive','negative','provenance-fixture'])
            self.assertTrue((out/'stage3-evidence.zip').is_file())
            meta=json.loads((out/'run-metadata.json').read_text())
            self.assertFalse(meta['phase_completed'])
            self.assertIn('No provenance records',meta['failure']['message'])

    def test_block_index_detects_elisions_without_claiming_completeness(self):
        text='RH_STAGE3_DECL_BEGIN A\ndef A := ⋯\nRH_STAGE3_DECL_END A\n'
        result=a.declaration_blocks(text,['A'])['blocks'][0]
        self.assertEqual(result['elision_indicators'], {'⋯':1})
        self.assertEqual(result['begin_line'],1)
        self.assertEqual(result['end_line'],3)
        clear=a.declaration_blocks(text.replace('⋯','True'),['A'])['blocks'][0]
        self.assertEqual(clear['elision_indicators'],{})
        self.assertIn('not certified',clear['rendering_completeness'])

    def test_block_index_rejects_missing_duplicate_empty_and_out_of_order(self):
        good='RH_STAGE3_DECL_BEGIN A\ndef A := True\nRH_STAGE3_DECL_END A\n'
        for text,names in [(good,['A','B']), (good+good,['A']),
                           (good.replace('def A := True\n',''),['A']),
                           (good.replace(' A',' B')+good,['A','B']),
                           (good.replace('RH_STAGE3_DECL_END A',''),['A'])]:
            with self.assertRaises(RuntimeError): a.declaration_blocks(text,names)

    def test_recorded_targets_have_matching_probe_commands(self):
        for phase,names in json.loads((HERE/'chain-targets.json').read_text()).items():
            filename,markers=a.RECORDS[phase]
            text=(HERE/filename).read_text()
            for name in names:
                self.assertEqual(text.count('#print '+name+'\n'),1)
                self.assertIn('#print axioms '+name+'\n',text)
                self.assertIn('RH_STAGE3_DECL_BEGIN '+name,text)
                self.assertIn('RH_STAGE3_DECL_END '+name,text)
            for marker in markers: self.assertIn(marker,text)

    def test_generalization_changes_only_declared_inputs(self):
        source = (HERE/'sources/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/OpenOrbitOfUnramifiedExponents.lean').read_text()
        body = source.split('theorem open_orbit_of_unramified_exponents_alt :',1)[1].split('\nend GlobalTheory.Fc.S0.Open0ProofU',1)[0]
        expected = 'theorem stage3_open_supplier_baseline :'+body
        self.assertEqual((HERE/'SupplierBaseline.body.txt').read_text(), expected+'\n')
        actual = (HERE/'GeometryGeneral.lean').read_text()
        self.assertIn(expected, actual)
        expected = expected.replace('stage3_open_supplier_baseline :','stage3_open_supplier_arbitrary (auditGamma : GeoP) :')
        expected = expected.replace('(_root_.GlobalTheory.Mem.Top.Bl.parametersOfDependence hL cDep)',
            '(_root_.GlobalTheory.Mem.Top.Bl.parametersOfExtension (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none auditGamma)')
        expected = expected.replace('(geoCl anyGeometry)', 'auditGamma')
        self.assertIn(expected, actual)
        self.assertNotIn('parametersOfDependence', expected)
        self.assertNotIn('anyGeometry', expected)
        self.assertNotIn('auditAll', expected)

    def test_first_error_preserves_typed_error(self):
        text = 'noise\n/audit/GeometryGeneral.lean:22:1: error(lean.test): Type mismatch\nexpected X\n'
        self.assertIn('expected X', a.first_error(text)['excerpt'])
        self.assertIn('unclassified', a.first_error(text)['classification'])
        self.assertIsNone(a.first_error('docker: error'))

    def test_collected_source_must_match_git(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); project=p/'project'; out=p/'out'
            (project/'src/Development').mkdir(parents=True); out.mkdir()
            (project/'src/Development/A.lean').write_text('import Development.B\n')
            (project/'src/Development/B.lean').write_text('-- child\n')
            cfg=dict(roots=['Development/A.lean'], import_depth=1,max_files=5,max_file_bytes=1024,max_total_bytes=4096)
            (p/'source-requests.json').write_text(json.dumps(cfg))
            def git(args,**kwargs):
                rel=args[-1].split(':src/',1)[1]
                return subprocess.CompletedProcess(args,0,(project/'src'/rel).read_bytes(),b'')
            with patch.object(a,'HERE',p),patch.object(a.subprocess,'run',side_effect=git):
                result=a.collect_sources(project,out)
            self.assertEqual(len(result['files']),2)
            self.assertTrue(all(x['status']=='collected-and-git-verified' for x in result['files']))
            self.assertTrue((out/'collected-source/Development/B.lean').is_file())
            with patch.object(a,'HERE',p),patch.object(a.subprocess,'run',return_value=subprocess.CompletedProcess([],0,b'wrong',b'')):
                with self.assertRaises(RuntimeError): a.collect_sources(project,out)

    def test_collection_caps_and_missing_are_explicit(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);project=p/'project';out=p/'out'
            (project/'src/Development').mkdir(parents=True);out.mkdir()
            (project/'src/Development/Big.lean').write_text('123456')
            cfg=dict(roots=['Development/Missing.lean','Development/Big.lean'],import_depth=1,max_files=5,max_file_bytes=2,max_total_bytes=10)
            (p/'source-requests.json').write_text(json.dumps(cfg))
            with patch.object(a,'HERE',p),patch.object(a.subprocess,'run') as run:
                result=a.collect_sources(project,out)
                run.assert_not_called()
            self.assertEqual([x['status'] for x in result['files']],['not-found-at-requested-path','file-size-cap'])

    def test_collection_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            (p/'source-requests.json').write_text(json.dumps(dict(roots=['../secret.lean'])))
            with patch.object(a,'HERE',p):
                with self.assertRaises(RuntimeError): a.collect_sources(p,p)

    def test_success_requires_exit_zero(self):
        with self.assertRaises(RuntimeError):
            a.validate_result("geometry", 1, "MARK", ["MARK"])

    def test_success_requires_marker(self):
        with self.assertRaises(RuntimeError):
            a.validate_result("geometry", 0, "", ["MARK"])

    def test_no_sorry_success(self):
        with self.assertRaises(RuntimeError):
            a.validate_result("geometry", 0, "MARK sorryAx", ["MARK"])

    def test_negative_accepts_only_expected_error(self):
        a.validate_result("negative", 1, "/audit/NegativeFixture.lean:4:0: error: Type mismatch", [])
        for rc,text in [(0,""), (124,"NegativeFixture.lean: error: Type mismatch"),
                        (137,""), (1,"docker: not found"), (1,"NegativeFixture.lean: error: Unknown identifier")]:
            with self.assertRaises(RuntimeError):
                a.validate_result("negative", rc, text, [])

    def test_fixture_has_no_project_access(self):
        cmd = a.docker_command(Path('/proof'),Path('/tc'),Path('/audit-out'),'sha256:abc',Path('/audit-out/x.cid'),'Fixture.lean',120,4,True)
        self.assertNotIn('type=bind,src=/proof,dst=/proof,readonly',cmd)
        self.assertIn('LEAN_PATH=',cmd)
        self.assertIn('--memory=4g',cmd)

    def test_project_mount_readonly(self):
        cmd = a.docker_command(Path('/proof'),Path('/tc'),Path('/audit-out'),'sha256:abc',Path('/audit-out/x.cid'),'HeightContext.lean',1800,100,False)
        self.assertIn('type=bind,src=/proof,dst=/proof,readonly',cmd)
        self.assertIn('--read-only',cmd)
        self.assertIn('--memory-swap=100g',cmd)
        self.assertNotIn('build',cmd)

    def test_output_cannot_be_in_project(self):
        with self.assertRaises(RuntimeError):
            a.new_output(Path('/tmp/proof/results'),Path('/tmp/proof'))

    def test_low_disk_blocks(self):
        class Usage: free = 20*a.GIB
        with patch.object(a.shutil,'disk_usage',return_value=Usage()):
            with self.assertRaises(RuntimeError):
                a.check_resources(HERE,100,True)

    def test_low_available_memory_blocks_project(self):
        class Usage: free = 64*a.GIB
        with patch.object(a.shutil,'disk_usage',return_value=Usage()), patch.object(a,'mem_available',return_value=110*a.GIB):
            with self.assertRaises(RuntimeError):
                a.check_resources(HERE,100,True)
            a.check_resources(HERE,100,False)

    def test_cleanup_requires_own_cid(self):
        with tempfile.TemporaryDirectory() as d, patch.object(a.subprocess,'run') as run:
            p=Path(d)/'x.cid'
            a.stop_owned(p);run.assert_not_called()
            p.write_text('2634778');a.stop_owned(p);run.assert_not_called()
            p.write_text('a'*64);a.stop_owned(p)
            self.assertEqual(run.call_args.args[0],['sudo','-n','docker','stop','--time','5','a'*64])

    def test_capture_success_and_error(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            rc,text=a.run_logged([sys.executable,'-c','print("hello"); raise SystemExit(7)'],p/'test.log',p/'x.cid',3)
            self.assertEqual(rc,7)
            self.assertIn('hello',text)
            self.assertIn('PROCESS_EXIT_STATUS 7',text)

    def test_output_guard_is_failure(self):
        with tempfile.TemporaryDirectory() as d, patch.object(a,'LOG_LIMIT',100):
            p=Path(d)
            with self.assertRaises(RuntimeError):
                a.run_logged([sys.executable,'-c','print("x"*1024)'],p/'test.log',p/'x.cid',3)
            self.assertIn('output-limit',(p/'test.log').read_text())

    def test_geometry_copy_only_adds_instrumentation(self):
        baseline=(HERE/'GeometryBaseline.lean').read_text()
        actual=(HERE/'GeometryContext.lean').read_text()
        actual=actual.split('\n#print UpperTheory.Lit.stage3_bundle_with_context\n',1)[0]
        actual=actual.replace('stage3_bundle_with_context','stage2_nonempty_hyps_definite_side_of_closed_bound_baseline')
        actual=actual.replace('set_option pp.all true\n','')
        actual='\n'.join(line for line in actual.split('\n') if not line.startswith('  trace ') and line!='  trace_state')
        self.assertEqual(actual.rstrip(),baseline.rstrip())

    def test_snapshot_hashes(self):
        import json
        for row in json.loads((HERE/'source-manifest.json').read_text()):
            self.assertEqual(a.sha256(HERE/row['snapshot_path']),row['sha256'])

    def test_geometry_explicit_occurrences_preserved(self):
        text=(HERE/'GeometryContext.lean').read_text()
        self.assertEqual(text.count('(geoCl anyGeometry)'),3)
        self.assertEqual(text.count('  trace_state'),5)

if __name__=='__main__':
    unittest.main(verbosity=2)
