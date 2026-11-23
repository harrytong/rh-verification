"""Driver regressions only. No Lean correctness or proof-validity claim."""
import contextlib
from datetime import datetime
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock
import zipfile

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("audit_stage2", HERE / "audit_stage2.py")
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
PRIOR = HERE / "test-data/records.jsonl"
PINNED_SOURCES = HERE / "test-data/source/project"


class DriverTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_prior_complete_66_pairs(self):
        rows, graph, summaries = a.read_prior(PRIOR)
        pairs = a.requests_from(rows)
        self.assertEqual(len(pairs), 66)
        self.assertEqual(len({s for s, t in pairs}), 45)
        self.assertEqual(graph["declarations"], 1478243)
        self.assertEqual(len(summaries), 10)

    def test_missing_prior_completion_rejected(self):
        rows, _, _ = a.read_prior(PRIOR)
        p = self.root / "records.jsonl"
        p.write_text("\n".join(json.dumps(r) for r in rows if r.get("event") != "audit-completed"))
        with self.assertRaisesRegex(RuntimeError, "did not complete"):
            a.read_prior(p)

    def test_missing_prior_metadata_rejected(self):
        p = self.root / "records.jsonl"
        shutil.copyfile(PRIOR, p)
        with self.assertRaisesRegex(RuntimeError, "metadata"):
            a.read_prior(p)

    def test_pin_mismatch_rejected(self):
        p = self.root / "records.jsonl"
        shutil.copyfile(PRIOR, p)
        meta = json.loads((PRIOR.parent / "run-metadata.json").read_text())
        meta["source"] = "different"
        (self.root / "run-metadata.json").write_text(json.dumps(meta))
        with self.assertRaisesRegex(RuntimeError, "pins"):
            a.read_prior(p)

    def test_malformed_path_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "Malformed"):
            a.requests_from([{"event": "reachability", "reachable": True,
                              "root": "a", "target": "b", "path": []}])

    def test_output_paths_protect_checkout(self):
        project = self.root / "project"
        project.mkdir()
        for path in (project, project / "inside", self.root):
            with self.assertRaises(RuntimeError):
                a.safe_output(project, path)
        out = a.safe_output(project, self.root / "outputs")
        self.assertTrue(out.is_dir())

    def test_exact_mutation_guard(self):
        s = "before\n" + a.ORIGINAL_GEOMETRY + "\nafter\n"
        changed = a.apply_mutation(s, "restrict-false")
        self.assertIn("=> False", changed)
        self.assertNotIn(a.ORIGINAL_GEOMETRY, changed)
        self.assertEqual(changed.count("before"), 1)
        for invalid in ("no definition", s + s):
            with self.assertRaises(RuntimeError):
                a.apply_mutation(invalid, "restrict-false")

    def test_mutation_never_starts_with_comparator(self):
        with mock.patch.object(a, "active_checkers", return_value=[{"pid": 1, "executable": "lake"}]), \
                mock.patch.object(a, "extract_commit") as extract:
            with self.assertRaisesRegex(RuntimeError, "still running"):
                a.mutation_build(None, self.root, self.root, self.root, {}, [])
            extract.assert_not_called()

    def test_mutation_never_starts_without_space(self):
        with mock.patch.object(a, "active_checkers", return_value=[]), \
                mock.patch.object(a, "storage_estimate", return_value={"sufficient_for_estimate": False}), \
                mock.patch.object(a, "extract_commit") as extract:
            with self.assertRaisesRegex(RuntimeError, "insufficient"):
                a.mutation_build(None, self.root, self.root, self.root, {}, [])
            extract.assert_not_called()

    def test_container_readonly_caps(self):
        args = types.SimpleNamespace(cpus=2, memory_gib=100)
        cmd = a.docker_base(args, self.root, self.root / "project", self.root / "lean", "/tmp:libs")
        self.assertIn("--read-only", cmd)
        self.assertIn("--memory=100g", cmd)
        self.assertIn("--memory-swap=100g", cmd)
        self.assertIn("none", cmd)
        self.assertIn("--cpus=2", cmd)
        self.assertFalse(any(x in cmd for x in ("stop", "kill", "update")))
        mounts = [cmd[i+1] for i, x in enumerate(cmd[:-1]) if x == "--mount"]
        self.assertTrue(all(x.endswith(",readonly") for x in mounts))
        self.assertEqual(cmd[cmd.index("--workdir")+1], "/audit")

    def test_smoke_success_required(self):
        with self.assertRaises(RuntimeError):
            a.require_smoke([])
        a.require_smoke([{"event": "smoke-passed"}])

    def test_failed_subprocess_preserves_log(self):
        p = self.root / "failure.log"
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, "exit 3"):
                a.run_logged([sys.executable, "-c", 'print("tool error: intentionally failed");raise SystemExit(3)'], p)
        self.assertIn("PROCESS_EXIT_STATUS 3", p.read_text())
        self.assertTrue(p.with_suffix(".jsonl").exists())

    def test_error_parser_uses_first_error(self):
        r = a.first_elaboration_error("warning\n/audit/A.lean:5:8: error: type mismatch\nfirst\n/audit/A.lean:9:0: error: next\n")
        self.assertEqual(r["line"], 2)
        self.assertEqual(r["reviewed_classification"], "pending human review")
        self.assertIn("interface", r["provisional_category"])

    def test_abstraction_generation_changes_only_three_arguments(self):
        project = self.root / "project"
        dest = project / a.ABSTRACTION_SOURCE
        dest.parent.mkdir(parents=True)
        source = PINNED_SOURCES / a.ABSTRACTION_SOURCE.relative_to("src")
        shutil.copyfile(source, dest)
        variants = a.abstraction_files(project, self.root)
        self.assertEqual(len(variants), 3)
        arbitrary = (self.root / "AbstractionArbitraryP.lean").read_text()
        self.assertEqual(arbitrary.count("(geoCl auditGamma)"), 3)
        self.assertNotIn("(geoCl anyGeometry)", arbitrary)
        self.assertIn("(auditGamma : GlobalTheory.Mem.Top.Bl.GeoP)", arbitrary)
        self.assertNotIn("auditAll", arbitrary)
        self.assertIn("auditAll", (self.root / "AbstractionUniversalP.lean").read_text())
        self.assertEqual(dest.read_text(), source.read_text())

    def test_generated_semantic_program_has_one_main(self):
        a.copy_tools(self.root)
        source = (self.root / "SemanticAudit.lean").read_text()
        self.assertEqual(source.count("\ndef main (args"), 1)
        self.assertIn("loadExts := true", source)
        self.assertIn("classifyValue", source)

    def test_evidence_excludes_experiment_and_itself(self):
        (self.root / "keep.log").write_text("evidence")
        (self.root / "experiment").mkdir()
        (self.root / "experiment/large-build").write_text("excluded")
        p = a.bundle_results(self.root)
        with zipfile.ZipFile(p) as z:
            self.assertEqual(z.namelist(), ["keep.log"])

    def test_inspect_orchestration_simulated(self):
        project = self.root / "project"
        lean = self.root / "lean"
        project.mkdir()
        (lean / "bin").mkdir(parents=True)
        (lean / "bin/lean").write_bytes(b"mock compiler; never executed")
        args = types.SimpleNamespace(project=project, toolchain=lean, prior=PRIOR,
                                     output=self.root / "out", phase="inspect", cpus=2,
                                     memory_gib=100)
        rows, _, _ = a.read_prior(PRIOR)
        pairs = a.requests_from(rows)
        edge_rows = [{"event": "edge-classification", "source": s, "target": t,
                      "signature_regions": [], "body_region": "proof-body",
                      "raw_body_reference": True, "trimmed_body_reference": True,
                      "structural_regions": [], "trimmed_direct_reference": True,
                      "trim_truncated": False} for s, t in pairs]
        calls = []
        def fake_run(cmd, path):
            calls.append(cmd)
            path.write_text("simulated orchestration only\n")
            if path.name == "smoke.log": return [{"event": "smoke-passed"}]
            if path.name == "edge-classification.log": return edge_rows
            return []
        with mock.patch.object(a, "validate", return_value={"packages": []}), \
                mock.patch.object(a, "command", return_value="mock-image"), \
                mock.patch.object(a.shutil, "which", return_value="/usr/bin/docker"), \
                mock.patch.object(a.subprocess, "run"), \
                mock.patch.object(a, "run_logged", side_effect=fake_run), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(a.run(args), 0)
        out = next(args.output.iterdir())
        meta = json.loads((out / "run-metadata.json").read_text())
        self.assertTrue(meta["phase_completed"])
        self.assertEqual(len(calls), 3)
        self.assertTrue((out / "classified-witness-paths.md").is_file())
        self.assertTrue((out / "stage2-evidence.zip").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
