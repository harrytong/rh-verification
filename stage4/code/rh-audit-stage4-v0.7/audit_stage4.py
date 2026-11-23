#!/usr/bin/env python3
"""Stage 4 v0.7: package-constructor fields and their suppliers. Python 3.10+."""
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import sys
import runtime as rt
import argument_results as ar
import supplier_results as sr
import source_discovery as sd

HERE = Path(__file__).resolve().parent
PREFIX = "RH_STAGE4_JSON\t"
GENERIC = ["GlobalTheory.CovHt.HtTopG.slope_le_height",
           "GlobalTheory.CovHt.HtTopG.height_add_log_nonneg",
           "GlobalTheory.CovHt.FrameCmp.val_le"]
OWNERS = ["GlobalTheory.CovHt.HtTopG.heightAt_eq_of_cover",
          "GlobalTheory.CovHt.FrameCmp.htCmp"]
REQUIRED_CALLS = [(OWNERS[0], GENERIC[0]), (OWNERS[1], GENERIC[2])]

def records(text):
    result = []
    for line in text.splitlines():
        if line.startswith(PREFIX):
            row = json.loads(line[len(PREFIX):])
            if not isinstance(row, dict) or "event" not in row:
                raise ValueError("Malformed audit record")
            result.append(row)
    return result

def validate_fixture(rows):
    expected = {"seed": "not-definitionally-identical",
                "equalSides": "definitionally-identical",
                "equalByHypothesis": "not-definitionally-identical",
                "sameCall": "definitionally-identical",
                "differentCall": "not-definitionally-identical",
                "letCall": "definitionally-identical",
                "firstCall": "not-definitionally-identical"}
    for short, status in expected.items():
        owner = "RHStage4Fixture." + short
        found = [r for r in rows if r.get("event") == "comparison" and r.get("owner") == owner]
        if len(found) != 1 or found[0].get("status") != status:
            raise RuntimeError(f"Fixture failed: {short}; received {found}")
        ends = [r for r in rows if r.get("owner") == owner and r.get("event") in {"generic-end", "calls-end"}]
        expected_end = "first-match-observed" if short == "firstCall" else "completed"
        if len(ends) != 1 or ends[0].get("status") != expected_end:
            raise RuntimeError(f"Fixture did not finish completely: {short}")
    absent = "RHStage4Fixture.noCall"
    if any(r.get("event") == "comparison" and r.get("owner") == absent for r in rows):
        raise RuntimeError("Fixture invented an absent call")
    ends = [r for r in rows if r.get("event") == "calls-end" and r.get("owner") == absent]
    if len(ends) != 1 or ends[0].get("status") != "completed" or ends[0].get("hits") != 0 or ends[0].get("pruned_subtrees", 0) < 1:
        raise RuntimeError("Absent-call pruning control did not pass")
    return True

def summarize(rows):
    problems = []
    for event, owners in [("generic-end", GENERIC), ("calls-end", OWNERS)]:
        for owner in owners:
            ends = [r for r in rows if r.get("event") == event and r.get("owner") == owner]
            allowed = {"completed", "first-match-observed"} if event == "calls-end" else {"completed"}
            if len(ends) != 1 or ends[0].get("status") not in allowed:
                problems.append({"owner": owner, "reason": "missing, duplicate, capped or unknown completion", "records": ends})
    comparisons = [r for r in rows if r.get("event") == "comparison"]
    for owner in GENERIC:
        found = [r for r in comparisons if r.get("owner") == owner and r.get("location") == "generic-conclusion"]
        if len(found) != 1:
            problems.append({"owner": owner, "reason": "generic comparison missing or duplicated"})
    for owner, callee in REQUIRED_CALLS:
        found = [r for r in comparisons if r.get("owner") == owner and r.get("callee") == callee]
        if not found:
            problems.append({"owner": owner, "callee": callee, "reason": "required call site not observed"})
    for row in comparisons:
        if row.get("status") not in {"definitionally-identical", "not-definitionally-identical"}:
            problems.append({"owner": row.get("owner"), "location": row.get("location"),
                             "reason": row.get("status", "missing comparison status")})
    return {"collection_complete": not problems, "coverage_problems": problems,
            "comparisons": comparisons,
            "claim_verdict": "unresolved pending inspection and agreement that these are the criticized comparisons",
            "scope": "named generic boundaries and first observed application per selected caller/callee; not an exhaustive body scan or transitive specialization",
            "exhaustive_application_coverage": False,
            "rh_grh_verdict": "not assessed", "necessity_verdict": "not assessed",
            "comparator_verdict": "not inspected"}

def assemble(out):
    helper = (HERE / "ComparisonProbe.lean.txt").read_text()
    for filename, imports, body in [
        ("ComparisonFixture.lean", "import Lean\n", "FixtureBody.lean.txt"),
        ("HeightComparison.lean", "import Lean\nimport Main\n", "ProjectBody.lean.txt")]:
        (out / filename).write_text(imports + "set_option pp.fullNames true\nset_option pp.universes true\n" + helper + "\nopen Lean.Elab.Command\n" + (HERE/body).read_text())

def assemble_arguments(out):
    helper = (HERE / "ComparisonProbe.lean.txt").read_text() + "\n" + (HERE / "ArgumentProbe.lean.txt").read_text()
    for filename, imports, body in [
        ("ArgumentFixture.lean", "import Lean\n", "ArgumentFixtureBody.lean.txt"),
        ("WordFactsArguments.lean", "import Lean\nimport Main\n", "WordFactsBody.lean.txt")]:
        (out / filename).write_text(imports + "set_option pp.fullNames true\nset_option pp.universes true\n" + helper + "\nopen Lean.Elab.Command\n" + (HERE/body).read_text())


def assemble_suppliers(out):
    helper = "\n".join((HERE/name).read_text() for name in
                         ["ComparisonProbe.lean.txt", "ArgumentProbe.lean.txt", "SupplierProbe.lean.txt"])
    for filename, imports, body in [
        ("SupplierFixture.lean", "import Lean\n", "SupplierFixtureBody.lean.txt"),
        ("PackageSuppliers.lean", "import Lean\nimport Main\n", "SupplierBody.lean.txt")]:
        (out/filename).write_text(imports + "set_option pp.fullNames true\nset_option pp.universes true\n" + helper + "\nopen Lean.Elab.Command\n" + (HERE/body).read_text())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--phase", choices=["smoke", "height", "wordfacts", "suppliers"], default="smoke")
    ap.add_argument("--project", type=Path, default=Path.home()/"rh-verification/riemann-hypothesis")
    ap.add_argument("--toolchain", type=Path, default=Path.home()/".elan/toolchains/leanprover--lean4---v4.33.1")
    ap.add_argument("--output", type=Path, default=Path.home()/"rh-verification/critics-audit-stage4")
    args = ap.parse_args()
    project_phase = args.phase in {"height", "wordfacts", "suppliers"}
    files = rt.package_files()
    project = args.project.expanduser().resolve()
    toolchain = args.toolchain.expanduser().resolve(strict=True)
    hashes = rt.validate(project, toolchain) if project_phase else {}
    if rt.sha256(toolchain/"bin/lean") != rt.LEAN_SHA:
        raise RuntimeError("Fixture/project Lean executable differs from recorded baseline")
    out = rt.new_output(args.output, project)
    for rel in files + [Path("SHA256SUMS")]:
        dest = out/rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(HERE/rel, dest)
    assemble(out)
    assemble_arguments(out)
    assemble_suppliers(out)
    meta = {"started_utc": rt.now(), "method": "stage4-0.7", "phase": args.phase,
            "protocol_sha256": rt.sha256(HERE/"PROTOCOL.md"),
            "followup_protocol_sha256": rt.sha256(HERE/"FOLLOWUP_PROTOCOL.md"),
            "reference_filter_protocol_sha256": rt.sha256(HERE/"REFERENCE_FILTER_PROTOCOL.md"),
            "argument_protocol_sha256": rt.sha256(HERE/"ARGUMENT_PROTOCOL.md"),
            "supplier_protocol_sha256": rt.sha256(HERE/"SUPPLIER_PROTOCOL.md"),
            "helper_followup_protocol_sha256": rt.sha256(HERE/"HELPER_FOLLOWUP_PROTOCOL.md"),
            "package_manifest_sha256": rt.sha256(HERE/"SHA256SUMS"),
            "input_hashes_before": hashes, "source_pin": rt.SOURCE_PIN,
            "mathlib_pin": rt.MATHLIB_PIN, "phase_completed": False, "steps": [],
            "limits": {"cpus": 2, "project_memory_gib": 100, "project_wall_seconds": 1800,
                       "per_action_raw_heartbeats": 10000000, "nodes_per_body": 250000,
                       "depth": 600, "hits_per_body": 64},
            "comparator": "not inspected or controlled"}
    rt.write_json(out/"run-metadata.json", meta)
    print(f"Stage 4 folder: {out}\nPhase: {args.phase}\nComparator is left untouched.", flush=True)
    status = 1
    try:
        meta["resources_before"] = rt.check_resources(out, 100, project_phase)
        if project_phase:
            rt.collect_sources(project, out)
        if args.phase == "suppliers":
            print("STAGE4_SOURCE_DISCOVERY: bounded literal search of the pinned source tree", flush=True)
            discovery = sd.collect(project, out)
            meta["supplier_source_collection_complete"] = discovery["complete"]
        subprocess.run(["sudo", "-v"], check=True)
        image = rt.command(["sudo", "-n", "docker", "image", "inspect", "rh-lean-check:1", "--format", "{{.Id}}"])
        if not image.startswith("sha256:"):
            raise RuntimeError("Cannot pin existing Docker image")
        meta["docker_image_id"] = image
        seq = [("negative", "NegativeFixture.lean", [], True),
               ("comparison-fixture", "ComparisonFixture.lean", ["RH_STAGE4_FIXTURE_END"], True)]
        if args.phase == "height":
            seq.append(("height", "HeightComparison.lean", ["RH_STAGE4_STATEMENT_ACCEPTED",
                "RH_STAGE4_ASSIGNED_HEIGHT_RFL_ACCEPTED", "RH_STAGE4_PROJECT_END"], False))
        if args.phase in {"smoke", "wordfacts", "suppliers"}:
            seq.append(("argument-fixture", "ArgumentFixture.lean", ["RH_STAGE4_ARGUMENT_FIXTURE_END"], True))
        if args.phase == "wordfacts":
            seq.append(("wordfacts", "WordFactsArguments.lean", ["RH_STAGE4_WORDFacts_STATEMENT_ACCEPTED", "RH_STAGE4_WORDFacts_END"], False))
        if args.phase in {"smoke", "suppliers"}:
            seq.append(("supplier-fixture", "SupplierFixture.lean", ["RH_STAGE4_SUPPLIER_FIXTURE_END"], True))
        if args.phase == "suppliers":
            seq.append(("suppliers", "PackageSuppliers.lean", ["RH_STAGE4_SUPPLIER_STATEMENT_ACCEPTED", "RH_STAGE4_SUPPLIER_END"], False))
        for name, filename, markers, smoke in seq:
            rt.check_resources(out, 100, not smoke)
            seconds = 180 if smoke else 1800
            cid = out/(name+".cid")
            cmd = rt.docker_command(project, toolchain, out, image, cid, filename, seconds, 4 if smoke else 100, smoke)
            step = {"name": name, "started_utc": rt.now(), "completed": False}
            meta["steps"].append(step)
            rt.write_json(out/"run-metadata.json", meta)
            print(f"STAGE4_START {name}; full output: {out/(name+'.log')}", flush=True)
            rc, text = rt.run_logged(cmd, out/(name+".log"), cid, seconds)
            step.update(exit_status=rc, first_error=rt.first_error(text))
            rt.write_json(out/"run-metadata.json", meta)
            rt.validate_result(name, rc, text, markers)
            if name == "comparison-fixture":
                validate_fixture(records(text))
            elif name == "argument-fixture":
                ar.validate_fixture(records(text))
            elif name == "supplier-fixture":
                sr.validate_fixture(records(text))
            elif name == "suppliers":
                rows = records(text)
                rt.write_json(out/"supplier-records.json", rows)
                summary = sr.summarize(rows)
                summary["source_discovery_complete"] = meta.get("supplier_source_collection_complete", False)
                rt.write_json(out/"CLAIM_RESULTS.json", summary)
                meta["coverage_complete"] = summary["collection_complete"]
            elif name == "wordfacts":
                rows = records(text)
                rt.write_json(out/"argument-records.json", rows)
                summary = ar.summarize(rows)
                rt.write_json(out/"CLAIM_RESULTS.json", summary)
                meta["coverage_complete"] = summary["collection_complete"]
            elif name == "height":
                rows = records(text)
                rt.write_json(out/"comparison-records.json", rows)
                summary = summarize(rows)
                rt.write_json(out/"CLAIM_RESULTS.json", summary)
                meta["coverage_complete"] = summary["collection_complete"]
            step.update(completed=True, ended_utc=rt.now())
            print(f"STAGE4_COMPLETED {name}", flush=True)
        if project_phase:
            meta["input_hashes_after"] = rt.validate(project, toolchain)
        meta["phase_completed"] = True
        status = 0
    except (Exception, KeyboardInterrupt) as e:
        meta["failure"] = str(e) or type(e).__name__
        print("STAGE4_ERROR: " + meta["failure"], file=sys.stderr)
    finally:
        meta["ended_utc"] = rt.now()
        rt.write_json(out/"run-metadata.json", meta)
        evidence = rt.archive(out)
        print(f"Evidence: {evidence}\nSHA-256: {rt.sha256(evidence)}", flush=True)
    if status == 0:
        print("Requested phase finished. Read CLAIM_RESULTS.json for coverage; no RH/GRH verdict is asserted.")
    return status

if __name__ == "__main__":
    sys.exit(main())
