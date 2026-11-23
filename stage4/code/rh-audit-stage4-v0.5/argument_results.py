"""Coverage checks for v0.5. None of these checks is an RH verdict."""
PREFIX = "Formalism.L2.DIV."
TARGETS = [
    (PREFIX + "wordFacts_of_clauses", PREFIX + "wordFacts_of",
     ["c2", "c3", "tH", "tR"], ["c2", "c3", "tH", "tR"]),
    (PREFIX + "wordFacts_of_face", PREFIX + "wordFacts_of_clauses",
     ["hcl", "tH", "tR"], ["tH", "tR"]),
    (PREFIX + "wordFacts_of_tied", PREFIX + "wordFacts_of_face",
     ["hcl", "tH", "tR"], ["tH", "tR"]),
    (PREFIX + "DivisionPackage.wordFacts", PREFIX + "wordFacts_of_tied",
     ["hcl", "tH", "tR"], ["tH", "tR"]),
    (PREFIX + "DivisionPackageFace.wordFacts", PREFIX + "wordFacts_of_face",
     ["hcl", "tH", "tR"], ["tH", "tR"]),
]
STATUSES = {"definitionally-identical", "not-definitionally-identical"}


def summarize(rows, targets=TARGETS):
    problems = []
    for owner, callee, selected, compared in targets:
        scoped = [r for r in rows if r.get("owner") == owner and r.get("callee") == callee]
        ends = [r for r in scoped if r.get("event") == "argument-calls-end"]
        if (len(ends) != 1 or ends[0].get("status") != "first-match-observed"
                or ends[0].get("scan_capped") is not False or ends[0].get("hits") != 1):
            problems.append({"owner": owner, "reason": "call absent, duplicated, capped or unknown"})
        arg_ends = [r for r in scoped if r.get("event") == "arguments-end"]
        if (len(arg_ends) != 1 or arg_ends[0].get("missing") != []
                or sorted(arg_ends[0].get("found", [])) != sorted(selected)):
            problems.append({"owner": owner, "reason": "selected arguments not completely captured"})
        for param in selected:
            args = [r for r in scoped if r.get("event") == "argument" and r.get("parameter") == param]
            if len(args) != 1:
                problems.append({"owner": owner, "parameter": param, "reason": "argument missing or duplicated"})
                continue
            a = args[0]
            if not a.get("location") or not isinstance(a.get("argument_index"), int):
                problems.append({"owner": owner, "parameter": param, "reason": "argument location/index missing"})
            for field in ("argument", "expected_type"):
                value = a.get(field)
                if not isinstance(value, dict) or not isinstance(value.get("text"), str):
                    problems.append({"owner": owner, "parameter": param, "reason": field + " not recorded"})
            if param in compared:
                comparisons = [r for r in scoped if r.get("event") == "comparison" and r.get("location") == a.get("location")]
                if len(comparisons) != 1 or comparisons[0].get("status") not in STATUSES:
                    problems.append({"owner": owner, "parameter": param, "reason": "argument comparison absent or unknown"})
            if param == "c2":
                binders = [r for r in scoped if r.get("event") == "argument-binder" and r.get("location") == a.get("location")]
                if len(binders) != 1:
                    problems.append({"owner": owner, "parameter": param, "reason": "conditional bound premise not captured exactly once"})
    truncations = [r for r in rows if r.get("event") == "argument" and
                   (r.get("references_truncated") or any(r.get(f, {}).get("truncated") for f in ("argument", "expected_type")))]
    return {"collection_complete": not problems, "coverage_problems": problems,
            "arguments": [r for r in rows if r.get("event") == "argument"],
            "argument_binders": [r for r in rows if r.get("event") == "argument-binder"],
            "comparisons": [r for r in rows if r.get("event") == "comparison"],
            "argument_records_with_truncated_fields": len(truncations),
            "scope": "first stored call at each of five named wrapper edges; no transitive headline specialization",
            "exhaustive_application_coverage": False,
            "claim_verdict": "unresolved; inspect actual supplied proofs and remaining local premises",
            "rh_grh_verdict": "not assessed", "necessity_verdict": "not assessed",
            "comparator_verdict": "not inspected"}


def validate_fixture(rows):
    ns = "RHStage4ArgFixture."
    targets = [(ns + n, ns + "bounded", ["c2", "c3", "tH"], ["c2", "c3", "tH"])
               for n in ("forwarded", "same", "letSame")]
    summary = summarize(rows, targets)
    if not summary["collection_complete"]:
        raise RuntimeError("Argument fixture coverage failed: " + str(summary["coverage_problems"]))
    for short in ("forwarded", "same", "letSame"):
        owner = ns + short
        args = {r["parameter"]: r for r in rows if r.get("event") == "argument" and r.get("owner") == owner}
        for param in ("c2", "c3", "tH"):
            a = args[param]
            comparison = next(r for r in rows if r.get("event") == "comparison" and r.get("owner") == owner and r.get("location") == a["location"])
            expected = "not-definitionally-identical" if short == "forwarded" and param != "tH" else "definitionally-identical"
            if comparison.get("status") != expected:
                raise RuntimeError(f"Argument fixture wrong comparison: {short}/{param}")
        binders = [r for r in rows if r.get("event") == "argument-binder" and r.get("owner") == owner and r.get("location") == args["c2"]["location"]]
        if len(binders) != 1 or "0" not in binders[0].get("type", {}).get("text", ""):
            raise RuntimeError("Nonzero premise was not retained in the argument fixture")
        if short == "forwarded" and any(args[p].get("argument_shape") != "local-reference" for p in ("c2", "c3")):
            raise RuntimeError("Forwarded proof arguments were not recognized")
        if short == "same" and args["c2"].get("argument_shape") != "lambda":
            raise RuntimeError("Constructed conditional proof argument was not recognized")
    absent = [r for r in rows if r.get("owner") == ns + "absent"]
    ends = [r for r in absent if r.get("event") == "argument-calls-end"]
    if (len(ends) != 1 or ends[0].get("status") != "no-call-observed"
            or ends[0].get("hits") != 0 or any(r.get("event") == "argument" for r in absent)):
        raise RuntimeError("Absent argument-call control failed")
    missing = [r for r in rows if r.get("event") == "arguments-end" and r.get("owner") == ns + "missing"]
    if len(missing) != 1 or missing[0].get("missing") != ["not_a_parameter"]:
        raise RuntimeError("Missing parameter control failed")
    return True
