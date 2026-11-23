"""Python-only evidence handling and bounded source-navigation tests."""
from pathlib import Path
import tempfile
import subprocess
import unittest
from unittest.mock import patch
from types import SimpleNamespace
import audit_stage4 as audit
import supplier_results as sr
import source_discovery as sd
import runtime as rt
from test_arguments import successful_rows


def rows():
    result = successful_rows(sr.TARGETS)
    result += [{"event": "supplier-declaration", "name": n, "status": "recorded"}
               for n in sr.DECLARATIONS]
    return result


class SupplierTests(unittest.TestCase):
    def test_coverage(self):
        s = sr.summarize(rows())
        self.assertTrue(s["collection_complete"])
        self.assertEqual(len(s["arguments"]), 14)
        self.assertEqual(len(s["comparisons"]), 9)
        self.assertEqual(len(s["supplier_declarations"]), 13)
        self.assertEqual(s["rh_grh_verdict"], "not assessed")

    def test_helper_owners_are_explicit(self):
        self.assertEqual(sr.TARGETS[1][0], sr.OWNER + "._proof_7")
        self.assertEqual(sr.TARGETS[2][0], sr.OWNER + "._proof_10")

    def test_pretty_elision_reported_without_char_truncation(self):
        r = rows(); r[-1]["body"] = {"text": "f ⋯", "truncated": False}
        s = sr.summarize(r)
        self.assertEqual(len(s["records_with_visible_pretty_printer_elisions"]), 1)
        self.assertEqual(s["supplier_declarations_with_truncation"], [])

    def test_old_owner_does_not_satisfy_helper_scan(self):
        r = rows()
        for x in r:
            if x.get("owner") in (sr.OWNER + "._proof_7", sr.OWNER + "._proof_10"):
                x["owner"] = sr.OWNER
        self.assertFalse(sr.summarize(r)["collection_complete"])

    def test_missing_declaration(self):
        self.assertFalse(sr.summarize(rows()[:-1])["collection_complete"])

    def test_unknown_declaration(self):
        r = rows(); r[-1]["status"] = "unknown"
        self.assertFalse(sr.summarize(r)["collection_complete"])

    def test_duplicate_declaration(self):
        r = rows(); r.append(r[-1])
        self.assertFalse(sr.summarize(r)["collection_complete"])

    def test_truncated_declaration_visible(self):
        r = rows(); r[-1]["body"] = {"text": "partial", "truncated": True}
        self.assertEqual(sr.summarize(r)["supplier_declarations_with_truncation"], [sr.DECLARATIONS[-1]])

    def test_missing_constructor_argument(self):
        r = [x for x in rows() if not (x.get("parameter") == "inp")]
        self.assertFalse(sr.summarize(r)["collection_complete"])

    def test_multiple_callees_same_owner_separate(self):
        r = rows()
        next(x for x in r if x.get("event") == "argument-calls-end" and x.get("callee") == sr.P+"hTie_of")["status"] = "unknown"
        self.assertFalse(sr.summarize(r)["collection_complete"])

    def test_unknown_not_fixture_success(self):
        with self.assertRaises(RuntimeError): sr.validate_fixture([])

    def test_generated_probe_targets(self):
        body = (audit.HERE/"SupplierBody.lean.txt").read_text()
        for owner, callee, selected, compared in sr.TARGETS:
            self.assertIn('"'+owner+'"', body)
            self.assertIn('"'+callee+'"', body)
        for name in sr.DECLARATIONS:
            self.assertIn('"'+name+'"', body)

    def test_identical_helper_in_fixture(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d); audit.assemble_suppliers(out)
            h = (audit.HERE/"SupplierProbe.lean.txt").read_text()
            self.assertIn(h, (out/"SupplierFixture.lean").read_text())
            self.assertIn(h, (out/"PackageSuppliers.lean").read_text())
            self.assertNotIn('import Main', (out/"SupplierFixture.lean").read_text())

    def test_pinned_grep_paths(self):
        data = (rt.SOURCE_PIN+":src/A.lean\0"+rt.SOURCE_PIN+":src/B.lean\0").encode()
        self.assertEqual(sd.paths_from_grep(data), ["A.lean", "B.lean"])

    def test_unpinned_path_rejected(self):
        with self.assertRaises(RuntimeError): sd.paths_from_grep(b"src/A.lean\0")

    def test_traversal_path_rejected(self):
        with self.assertRaises(RuntimeError): sd.paths_from_grep((rt.SOURCE_PIN+":src/../bad.lean\0").encode())

    def test_discovery_timeout_reported(self):
        with tempfile.TemporaryDirectory() as d, patch.object(sd.subprocess, 'run', side_effect=TimeoutError('timeout')):
            s = sd.collect(Path(d), Path(d))
            self.assertFalse(s['complete'])
            self.assertIn('timeout', s['error'])

    def test_discovery_file_cap_visible(self):
        paths = [f"Many/File{i:03}.lean" for i in range(90)]
        output = ''.join(rt.SOURCE_PIN+':src/'+p+'\0' for p in paths).encode()
        with tempfile.TemporaryDirectory() as d, patch.object(sd.subprocess,'run', return_value=SimpleNamespace(returncode=0, stdout=output, stderr=b'')), patch.object(rt,'collect_sources',return_value={"files":[]}):
            s = sd.collect(Path(d),Path(d))
            self.assertTrue(s['file_selection_capped'])
            self.assertFalse(s['complete'])
            self.assertEqual(len(s['selected_files']),80)

    def test_real_git_collection_and_modified_source_rejection(self):
        with tempfile.TemporaryDirectory() as d:
            project = Path(d)/'repo'; project.mkdir()
            (project/'src').mkdir()
            source = project/'src/Fixture.lean'
            source.write_text('structure DivInputs0R where\n  n : Nat\n')
            subprocess.run(['git','init','-q'], cwd=project, check=True)
            subprocess.run(['git','add','src/Fixture.lean'], cwd=project, check=True)
            subprocess.run(['git','-c','user.name=AuditFixture','-c','user.email=audit@example.invalid',
                            'commit','-qm','fixture'], cwd=project, check=True)
            pin = subprocess.check_output(['git','rev-parse','HEAD'], cwd=project, text=True).strip()
            first = Path(d)/'first'; first.mkdir()
            second = Path(d)/'second'; second.mkdir()
            with patch.object(rt,'SOURCE_PIN',pin), patch.object(sd,'PRIORITY',[]):
                good = sd.collect(project,first)
                self.assertTrue(good['complete'])
                self.assertEqual(good['matched_files'], ['Fixture.lean'])
                self.assertEqual((first/'supplier-source/collected-source/Fixture.lean').read_bytes(),source.read_bytes())
                source.write_text('structure DivInputs0R where\n  changed : Bool\n')
                changed = sd.collect(project,second)
                self.assertFalse(changed['complete'])
                self.assertIn('differs from pinned git contents',changed['error'])


if __name__ == '__main__': unittest.main()
