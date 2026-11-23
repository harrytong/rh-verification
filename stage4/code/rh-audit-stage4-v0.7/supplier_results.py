"""Bounded constructor/supplier collection. No automatic claim verdict."""
import argument_results as ar
P = "Formalism.L2.DIV."
OWNER = P + "DivisionPackageFace.ofOpen"
TARGETS = [
    (OWNER, P + "DivisionPackageFace.mk", ["R", "inp", "hTie", "rhs"], ["hTie", "rhs"]),
    (OWNER + "._proof_7", P + "hTie_of", ["hk", "hnum", "hh"], ["hnum", "hh"]),
    (OWNER + "._proof_10", P + "rhs_le_record", ["H", "t", "hC0", "hC1", "hC2", "hCabs", "hLa"],
     ["hC0", "hC1", "hC2", "hCabs", "hLa"]),
]
DECLARATIONS = [P + n for n in ["DivInputs0R", "DivInputs0R.mk", "DivInputsR", "DivInputsR.mk", "DivClausesR", "divClausesR_of",
                "linkDIV_L2R_clauses", "linkDIV_L2R_face", "RecNums.ofNum", "hTie_of", "rhs_le_record", "DivisionPackageFace.ofOpen._proof_7", "DivisionPackageFace.ofOpen._proof_10"]]


def summarize(rows):
    summary = ar.summarize(rows, TARGETS)
    problems = summary["coverage_problems"]
    for name in DECLARATIONS:
        found = [r for r in rows if r.get("event") == "supplier-declaration" and r.get("name") == name]
        if len(found) != 1 or found[0].get("status") != "recorded":
            problems.append({"name": name, "reason": "supplier declaration missing, duplicated or unknown"})
    summary["collection_complete"] = not problems
    summary["supplier_declarations"] = [r for r in rows if r.get("event") == "supplier-declaration"]
    summary["supplier_declarations_with_truncation"] = [r.get("name") for r in summary["supplier_declarations"]
        if r.get("body_references_truncated") or any((r.get(f) or {}).get("truncated") for f in ("type", "body"))]
    summary["scope"] = "first constructor call in DivisionPackageFace.ofOpen and proof-producing calls in its observed _proof_7 and _proof_10 helpers; this constructor still has parameters, not a fully specialized headline package"
    # A character cap is distinct from Lean's pretty-printer elisions.
    def has_elision(value):
        if isinstance(value, dict):
            return any((k == "text" and isinstance(v, str) and "⋯" in v) or has_elision(v)
                       for k, v in value.items())
        if isinstance(value, list):
            return any(has_elision(v) for v in value)
        return False
    summary["records_with_visible_pretty_printer_elisions"] = [
        {k: r[k] for k in ("event", "name", "owner", "callee", "parameter", "location") if k in r}
        for r in rows if has_elision(r)]
    summary["printing_scope"] = "Rendered terms are diagnostic, not complete term serialization; elision-marker detection is not a completeness proof. Comparisons and reference extraction operate on expressions."
    summary["claim_verdict"] = "unresolved pending inspection of supplied inputs and headline specialization"
    return summary


def validate_fixture(rows):
    ns = "RHStage4SupplierFixture."
    targets = [(ns + "make", ns + "Package.mk", ["inp", "hTie", "rhs"], ["inp", "hTie", "rhs"])]
    result = ar.summarize(rows, targets)
    if not result["collection_complete"]:
        raise RuntimeError("Supplier fixture coverage failed: " + str(result["coverage_problems"]))
    for a in result["arguments"]:
        matches = [r for r in result["comparisons"] if r.get("location") == a["location"]]
        expected = "not-definitionally-identical" if a["parameter"] == "inp" else "definitionally-identical"
        if len(matches) != 1 or matches[0].get("status") != expected:
            raise RuntimeError("Supplier fixture comparison failed")
        if a["parameter"] == "inp" and a["argument_shape"] != "local-reference":
            raise RuntimeError("Supplier fixture lost the forwarded input")
    records = [r for r in rows if r.get("event") == "supplier-declaration"]
    ok = [r for r in records if r.get("name") == ns + "make"]
    absent = [r for r in records if r.get("name") == ns + "DeliberatelyAbsent"]
    if len(ok) != 1 or ok[0].get("status") != "recorded" or not ok[0].get("body"):
        raise RuntimeError("Supplier declaration fixture failed")
    if len(absent) != 1 or absent[0].get("status") != "unknown":
        raise RuntimeError("Absent supplier declaration was not reported as unknown")
    return True
