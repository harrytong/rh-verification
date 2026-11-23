import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("audit_stage3", HERE/"audit_stage3.py")
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

class DriverTests(unittest.TestCase):
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
