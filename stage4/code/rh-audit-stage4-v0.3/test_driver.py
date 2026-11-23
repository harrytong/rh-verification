"""Driver/interpretation tests. These do NOT execute Lean."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import audit_stage4 as audit
import runtime as rt

def fixture_rows():
    rows = []
    for name, status in [("seed", "not-definitionally-identical"),
                         ("equalSides", "definitionally-identical"),
                         ("equalByHypothesis", "not-definitionally-identical"),
                         ("sameCall", "definitionally-identical"),
                         ("differentCall", "not-definitionally-identical"),
                         ("letCall", "definitionally-identical"),
                         ("firstCall", "not-definitionally-identical")]:
        owner = "RHStage4Fixture." + name
        rows += [{"event": "comparison", "owner": owner, "status": status},
                 {"event": "calls-end" if name.endswith("Call") else "generic-end", "owner": owner,
                  "status": "first-match-observed" if name == "firstCall" else "completed"}]
    return rows

def project_rows():
    rows = [{"event": "generic-end", "owner": x, "status": "completed"} for x in audit.GENERIC]
    rows += [{"event": "calls-end", "owner": x, "status": "completed"} for x in audit.OWNERS]
    rows += [{"event": "comparison", "owner": x, "location": "generic-conclusion",
              "status": "not-definitionally-identical"} for x in audit.GENERIC]
    rows += [{"event": "comparison", "owner": owner, "callee": callee,
              "status": "not-definitionally-identical"} for owner, callee in audit.REQUIRED_CALLS]
    return rows

class Tests(unittest.TestCase):
    def test_fixture_success(self):
        self.assertTrue(audit.validate_fixture(fixture_rows()))
    def test_fixture_missing(self):
        with self.assertRaises(RuntimeError): audit.validate_fixture(fixture_rows()[1:])
    def test_fixture_wrong_answer(self):
        rows = fixture_rows(); rows[0]["status"] = "definitionally-identical"
        with self.assertRaises(RuntimeError): audit.validate_fixture(rows)
    def test_fixture_unknown(self):
        rows = fixture_rows(); rows[1]["status"] = "unknown"
        with self.assertRaises(RuntimeError): audit.validate_fixture(rows)
    def test_fixture_duplicate(self):
        rows = fixture_rows(); rows.append(rows[0])
        with self.assertRaises(RuntimeError): audit.validate_fixture(rows)
    def test_record_parsing(self):
        self.assertEqual(audit.records('noise\n'+audit.PREFIX+'{"event":"ok"}\n'), [{"event":"ok"}])
    def test_bad_record(self):
        with self.assertRaises(ValueError): audit.records(audit.PREFIX+'[]')
    def test_no_proof_verdict(self):
        summary = audit.summarize(project_rows())
        self.assertTrue(summary["collection_complete"])
        self.assertEqual(summary["rh_grh_verdict"], "not assessed")
        self.assertTrue(summary["claim_verdict"].startswith("unresolved"))
    def test_missing_call(self):
        self.assertFalse(audit.summarize(project_rows()[:-1])["collection_complete"])
    def test_missing_generic(self):
        rows = [r for r in project_rows() if r.get("location") != "generic-conclusion"]
        self.assertFalse(audit.summarize(rows)["collection_complete"])
    def test_identical_sides_no_verdict(self):
        rows = project_rows()
        for r in rows:
            if r.get("event") == "comparison": r["status"] = "definitionally-identical"
        self.assertEqual(audit.summarize(rows)["rh_grh_verdict"], "not assessed")
    def test_capped_scan(self):
        rows = project_rows(); rows[3]["status"] = "incomplete-cap"
        self.assertFalse(audit.summarize(rows)["collection_complete"])
    def test_exception(self):
        rows = project_rows(); rows[0]["status"] = "unknown"
        self.assertFalse(audit.summarize(rows)["collection_complete"])
    def test_noncomparison(self):
        rows = project_rows(); rows[-1]["status"] = "not-a-direct-comparison"
        self.assertFalse(audit.summarize(rows)["collection_complete"])
    def test_first_match_scope(self):
        rows = project_rows()
        for row in rows:
            if row['event'] == 'calls-end': row['status'] = 'first-match-observed'
        summary = audit.summarize(rows)
        self.assertTrue(summary['collection_complete'])
        self.assertFalse(summary['exhaustive_application_coverage'])
    def test_first_match_without_comparison_not_complete(self):
        rows = [r for r in project_rows() if not r.get('callee')]
        for row in rows:
            if row['event'] == 'calls-end': row['status'] = 'first-match-observed'
        self.assertFalse(audit.summarize(rows)['collection_complete'])
    def test_negative_control_not_timeout(self):
        with self.assertRaises(RuntimeError):
            rt.validate_result("negative",124,"NegativeFixture.lean:1:0: error: Type mismatch",[])
    def test_negative_control_expected(self):
        rt.validate_result("negative",1,"NegativeFixture.lean:1:0: error: Type mismatch",[])
    def test_sorry_rejected(self):
        with self.assertRaises(RuntimeError): rt.validate_result("height",0,"done sorryAx",["done"])
    def test_markers_required(self):
        with self.assertRaises(RuntimeError): rt.validate_result("height",0,"",["done"])
    def test_marker_after_compile_error_is_not_success(self):
        with self.assertRaises(RuntimeError):
            rt.validate_result("comparison-fixture",1,"error: Type mismatch\nRH_STAGE4_FIXTURE_END",["RH_STAGE4_FIXTURE_END"])
    def test_meta_lift_namespace_regression(self):
        helper=(audit.HERE/"ComparisonProbe.lean.txt").read_text()
        self.assertIn("def emitMeta (fields : List (String × Json)) : MetaM Unit :=\n  liftM (emit fields)",helper)
        self.assertNotIn("liftIO",helper)
        self.assertNotIn("open Lean Meta Elab Command",helper)
    def test_command_namespace_opened_after_helper(self):
        with tempfile.TemporaryDirectory() as d:
            audit.assemble(Path(d))
            for filename in ["ComparisonFixture.lean","HeightComparison.lean"]:
                text=(Path(d)/filename).read_text()
                self.assertLess(text.index("end RHStage4"),text.index("open Lean.Elab.Command"))
    def test_output_not_checkout(self):
        with tempfile.TemporaryDirectory() as d:
            project=Path(d)/"proof"
            with self.assertRaises(RuntimeError): rt.new_output(project/"audit",project)
            with self.assertRaises(RuntimeError): rt.new_output(Path(d),project)
    def test_assembly_shared_helper(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d); audit.assemble(out)
            helper=(audit.HERE/"ComparisonProbe.lean.txt").read_text()
            self.assertIn(helper,(out/"ComparisonFixture.lean").read_text())
            self.assertIn(helper,(out/"HeightComparison.lean").read_text())
            self.assertNotIn("import Main",(out/"ComparisonFixture.lean").read_text())
    def test_container_isolation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            cmd=rt.docker_command(p/"proof",p/"lean",p/"out","sha256:test",p/"a.cid","HeightComparison.lean",1800,100,False)
            self.assertIn("--read-only",cmd); self.assertIn("--memory=100g",cmd)
            self.assertIn("--cpus=2",cmd)
            mounts=[cmd[i+1] for i,x in enumerate(cmd) if x=="--mount"]
            self.assertTrue(all(x.endswith(",readonly") for x in mounts))
            self.assertFalse(any("comparator" in x for x in cmd))
    def test_fixture_no_project_mount(self):
        p=Path("/example")
        cmd=rt.docker_command(p/"proof",p/"lean",p/"out","image",p/"a.cid","ComparisonFixture.lean",180,4,True)
        self.assertFalse(any("src=/example/proof" in x for x in cmd))
    def test_only_owned_stop(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"cid";p.write_text("rh-comparator")
            with patch.object(rt.subprocess,"run") as run:
                rt.stop_owned(p);run.assert_not_called()
    def test_disk_guard(self):
        with patch.object(rt.shutil,"disk_usage") as disk:
            disk.return_value.free=20*rt.GIB
            with self.assertRaises(RuntimeError):rt.check_resources(Path("."),100,True)
    def test_memory_guard(self):
        with patch.object(rt.shutil,"disk_usage") as disk,patch.object(rt,"mem_available",return_value=115*rt.GIB):
            disk.return_value.free=64*rt.GIB
            with self.assertRaises(RuntimeError):rt.check_resources(Path("."),100,True)
    def test_archive_excludes_itself(self):
        import zipfile
        with tempfile.TemporaryDirectory() as d:
            out=Path(d);(out/"result.txt").write_text("test")
            rt.archive(out);z=rt.archive(out)
            with zipfile.ZipFile(z) as f:
                self.assertEqual(set(f.namelist()),{"result.txt","EVIDENCE_SHA256SUMS"})

if __name__ == "__main__": unittest.main()
