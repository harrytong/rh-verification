"""Coverage/guard tests with synthetic records. These do not execute Lean."""
import copy
from pathlib import Path
import tempfile
import unittest
import argument_results as ar
import audit_stage4 as audit


def successful_rows(targets=ar.TARGETS):
    rows = []
    for owner, callee, selected, compared in targets:
        common = {"owner": owner, "callee": callee}
        rows.append(dict(common, event="argument-calls-end", status="first-match-observed", scan_capped=False, hits=1))
        rows.append(dict(common, event="arguments-end", missing=[], found=selected))
        for i, p in enumerate(selected):
            loc = "body/parameter-" + p
            rows.append(dict(common, event="argument", parameter=p, argument_index=i, location=loc,
                             argument={"text": "localProof", "truncated": False},
                             expected_type={"text": "a ≤ b", "truncated": False},
                             references_truncated=False))
            if p in compared:
                rows.append(dict(common, event="comparison", location=loc, status="not-definitionally-identical"))
            if p == "c2":
                rows.append(dict(common, event="argument-binder", location=loc, type={"text": "B ≠ 0", "truncated": False}))
    return rows


class ArgumentTests(unittest.TestCase):
    def test_expected_coverage(self):
        r = ar.summarize(successful_rows())
        self.assertTrue(r["collection_complete"])
        self.assertEqual(len(r["arguments"]), 16)
        self.assertEqual(len(r["comparisons"]), 12)
        self.assertFalse(r["exhaustive_application_coverage"])

    def test_unknown_is_not_completion(self):
        rows = successful_rows(); rows[0]["status"] = "unknown"
        self.assertFalse(ar.summarize(rows)["collection_complete"])

    def test_cap_is_not_completion(self):
        rows = successful_rows(); rows[0]["scan_capped"] = True
        self.assertFalse(ar.summarize(rows)["collection_complete"])

    def test_missing_parameter(self):
        rows = successful_rows(); rows[1]["missing"] = ["c2"]
        self.assertFalse(ar.summarize(rows)["collection_complete"])

    def test_missing_proof_record(self):
        rows = [r for r in successful_rows() if not (r.get("event") == "argument" and r.get("parameter") == "c2")]
        self.assertFalse(ar.summarize(rows)["collection_complete"])

    def test_missing_nonzero_premise_is_incomplete(self):
        rows = [r for r in successful_rows() if r.get("event") != "argument-binder"]
        self.assertFalse(ar.summarize(rows)["collection_complete"])

    def test_comparison_must_match_argument_location(self):
        rows = successful_rows()
        next(r for r in rows if r["event"] == "comparison")["location"] = "unrelated"
        self.assertFalse(ar.summarize(rows)["collection_complete"])

    def test_noncomparison_is_unresolved(self):
        rows = successful_rows()
        next(r for r in rows if r["event"] == "comparison")["status"] = "not-a-direct-comparison"
        self.assertFalse(ar.summarize(rows)["collection_complete"])

    def test_duplicates_rejected(self):
        rows = successful_rows(); rows.append(copy.deepcopy(rows[2]))
        self.assertFalse(ar.summarize(rows)["collection_complete"])

    def test_reflexivity_does_not_invalidate_rh(self):
        rows = successful_rows()
        for r in rows:
            if r["event"] == "comparison": r["status"] = "definitionally-identical"
        result = ar.summarize(rows)
        self.assertTrue(result["collection_complete"])
        self.assertEqual(result["rh_grh_verdict"], "not assessed")
        self.assertEqual(result["necessity_verdict"], "not assessed")

    def test_truncation_is_reported(self):
        rows = successful_rows(); rows[2]["argument"]["truncated"] = True
        self.assertEqual(ar.summarize(rows)["argument_records_with_truncated_fields"], 1)

    def test_missing_printed_type_fails(self):
        rows = successful_rows(); del rows[2]["expected_type"]
        self.assertFalse(ar.summarize(rows)["collection_complete"])

    def test_same_helper_for_fixture_and_project(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d); audit.assemble_arguments(out)
            helper = (audit.HERE / "ArgumentProbe.lean.txt").read_text()
            self.assertIn(helper, (out/"ArgumentFixture.lean").read_text())
            self.assertIn(helper, (out/"WordFactsArguments.lean").read_text())
            self.assertNotIn("import Main", (out/"ArgumentFixture.lean").read_text())

    def test_exact_targets_in_project_probe(self):
        body = (audit.HERE / "WordFactsBody.lean.txt").read_text()
        for owner, callee, selected, compared in ar.TARGETS:
            self.assertIn('"'+owner+'"', body)
            self.assertIn('"'+callee+'"', body)
            self.assertIn('#['+', '.join('"'+p+'"' for p in selected)+']', body)
        self.assertEqual(body.count("RHStage4.argumentCalls env"), 5)

    def test_fixture_failure_stops_project(self):
        # Exercise the actual fixture validator with incomplete evidence.
        with self.assertRaises(RuntimeError): ar.validate_fixture([])


if __name__ == "__main__": unittest.main()
