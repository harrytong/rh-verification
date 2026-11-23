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
