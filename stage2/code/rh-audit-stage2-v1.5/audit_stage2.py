#!/usr/bin/env python3
"""Stage 2 audit. Python 3.10+; standard library only. See README.md.
No access to or control over the running Comparator is required.
"""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
import tarfile
import time
import re
import difflib

SOURCE_PIN = "753431bfe28701f6f3937f664fcaf08daa139c03"

MATHLIB_PIN = "0df444a360eaa60ab8c11dca51a86af692955474"

MAIN_SHA = "9146dfb4148e24d2252e04c50742f3e49dd126dfcc5006d10bf5f873ddf796ad"

STATEMENTS_SHA = "f8e0aed3c2d69390b6dd3bb24e13aa25e043a02ca42f021e3f6e4ec8b57fd6b1"

LEAN_SHA = "e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550"

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()

def command(args, cwd=None):
    p = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(p.stderr.strip() or f"Command failed: {args}")
    return p.stdout.strip()

def validate(project, toolchain):
    if command(["git", "rev-parse", "HEAD"], cwd=project) != SOURCE_PIN:
        raise RuntimeError("Source HEAD changed. Do not update or checkout the proof while Comparator is running.")
    dirty = command(["git", "diff", "--name-only", "HEAD", "--", "src", "lean-toolchain",
                     "lakefile.toml", "lake-manifest.json"], cwd=project)
    if dirty:
        raise RuntimeError("Tracked project inputs changed:\n" + dirty)
    if (project / "lean-toolchain").read_text().strip() != "leanprover/lean4:v4.33.1":
        raise RuntimeError("Unexpected project toolchain")
    manifest = json.loads((project / "lake-manifest.json").read_text())
    pin = [p["rev"] for p in manifest["packages"] if p["name"] == "mathlib"]
    if pin != [MATHLIB_PIN]:
        raise RuntimeError("Unexpected Mathlib manifest pin")
    ml = project / ".lake/packages/mathlib"
    if command(["git", "rev-parse", "HEAD"], cwd=ml) != MATHLIB_PIN:
        raise RuntimeError("Mathlib checkout changed")
    ml_dirty = command(["git", "diff", "--name-only", "HEAD", "--", "Mathlib",
                        "lean-toolchain", "lakefile.lean", "lake-manifest.json"], cwd=ml)
    if ml_dirty:
        raise RuntimeError("Tracked Mathlib inputs changed:\n" + ml_dirty)
    for name, expected in (("Main", MAIN_SHA), ("Statements", STATEMENTS_SHA)):
        p = project / f".lake/build/lib/lean/{name}.olean"
        if not p.is_file() or sha256(p) != expected:
            raise RuntimeError(f"{name}.olean does not match the previously audited hash")
    if not (toolchain / "bin/lean").is_file():
        raise RuntimeError("Pinned Lean 4.33.1 executable is missing")
    if sha256(toolchain / "bin/lean") != LEAN_SHA:
        raise RuntimeError("Lean executable differs from the compiler recorded in the completed audit")
    return manifest


HERE = Path(__file__).resolve().parent
ROOTS = ["riemannHypothesis", "riemannZeta_eq_zero_re",
         "LFunction_ne_zero_of_half_lt_re", "LFunction_eq_zero_re",
         "LFunction_eq_zero_re_of_isPrimitive"]
OVERIX = Path("src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/OverIx.lean")
ORIGINAL_GEOMETRY = "def anyGeometry : GeoP := fun _ _ _ => True"
MUTATIONS = {
    "benign-beta": "def anyGeometry : GeoP := fun _ _ _ => (fun P : Prop => P) True",
    "restrict-false": "def anyGeometry : GeoP := fun _ _ _ => False",
}


def read_prior(path):
    """Reject incomplete/mismatched evidence before generating requests."""
    records = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    graphs = [r for r in records if r.get("event") == "graph-complete" and
              set(r.get("roots", [])) == set(ROOTS)]
    if len(graphs) != 1 or graphs[0].get("missing") != []:
        raise RuntimeError("Prior graph is absent, ambiguous, or contains missing declarations")
    if not any(r.get("event") == "audit-completed" for r in records):
        raise RuntimeError("Prior audit did not complete")
    expected = {(root, structural) for root in ROOTS for structural in (False, True)}
    summaries = [r for r in records if r.get("event") == "root-summary"]
    actual = {(r["root"], r["include_structural_edges"]) for r in summaries}
    if actual != expected or len(summaries) != 10:
        raise RuntimeError("Prior evidence must have all ten root summaries")
    meta_path = path.parent / "run-metadata.json"
    if not meta_path.is_file():
        raise RuntimeError("Prior run-metadata.json is required beside records.jsonl")
    meta = json.loads(meta_path.read_text())
    if meta.get("source") != SOURCE_PIN or meta.get("mathlib") != MATHLIB_PIN:
        raise RuntimeError("Prior metadata has different source/Mathlib pins")
    if meta.get("main_olean_sha256") != MAIN_SHA or meta.get("statements_olean_sha256") != STATEMENTS_SHA:
        raise RuntimeError("Prior compiled-headline hashes do not match")
    if meta.get("dependency_audit_completed") is not True:
        raise RuntimeError("Prior metadata does not report a completed audit")
    return records, graphs[0], summaries


def requests_from(records):
    pairs = set()
    for row in records:
        if row.get("event") != "reachability" or row.get("reachable") is not True:
            continue
        path = row.get("path", [])
        if not path or path[0]["declaration"]["name"] != row["root"] or \
                path[-1]["declaration"]["name"] != row["target"]:
            raise RuntimeError("Malformed prior witness path")
        for a, b in zip(path, path[1:]):
            pair = (a["declaration"]["name"], b["declaration"]["name"])
            if any("\t" in s or "\n" in s for s in pair):
                raise RuntimeError("Control characters in a declaration name")
            pairs.add(pair)
    if not pairs:
        raise RuntimeError("No witness edges found")
    return sorted(pairs)


def safe_output(project, output):
    p = output.expanduser().resolve()
    if p == project or project in p.parents or p in project.parents:
        raise RuntimeError("Output must be outside the proof checkout and its ancestors")
    p.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix="stage2-", dir=p))


def write_plan(out, records, graph, summaries):
    pairs = requests_from(records)
    (out / "edge-requests.tsv").write_text("".join(f"{a}\t{b}\n" for a, b in pairs))
    rows = ["# Stage 2: Daniel Fairbanks's review requests", "",
            "This is an experiment plan, not new evidence that RH or GRH is proved or refuted.", "",
            "## Why the old membership table is weak on its own", "",
            f"The prior union contains {graph['declarations']:,} declarations. It was constructed from the five roots.",
            "Each root reaches almost all of that union. This is descriptive closure saturation, not a probability or a statistical significance test.", "",
            "| Root | Structural edges | Reachable | Fraction of union |", "|---|---|---:|---:|"]
    for s in summaries:
        rows.append(f"| `{s['root']}` | {s['include_structural_edges']} | {s['visited']:,} | {s['visited']/graph['declarations']:.6%} |")
    rows += ["", f"The existing paths contain **{len(pairs)} distinct source/target pairs** across **{len({a for a, _ in pairs})} source declarations**.", "",
             "## Run sequence", "",
             "1. `inspect`: compile and run the isolated tool fixture; compile the statement examples; classify all prior witness edges and apply bounded local pruning to their source bodies.",
             "2. `abstraction`: generic GeoCl P interface lemmas and scoped generalization of three literal geometry arguments in the actual bundle proof. Imported dependencies remain unchanged.",
             "3. `census`: fresh Mathlib control and five-root reference union, using syntactic categories. `semantic-census` separately applies the preregistered bounded definitional tests to both cohorts.",
             "4. `pruned-closure`: compare raw and locally pruned union reachability. Types stay unchanged; this is not global proof minimization.",
             "5. `mutation-plan`: estimate storage and write the full-rebuild protocol. It performs no rebuild and changes no proof input.",
             "6. `mutation-build`: only after Comparator/checkers have stopped and space is sufficient. Make an isolated source checkout, build its baseline from fresh project outputs, then apply a definitionally equal control or False restriction and rebuild with Lake.", "",
             "## Interpretation rules", "",
             "An edge may occur in several regions. A binder domain can be a type parameter, an instance, data, or a mathematical hypothesis; its position alone does not classify it as a premise proposition.",
             "A body edge may itself occur in a local binder annotation or unused syntax. These labels do not establish necessity.",
             "The local pruning experiment removes only explicit unused let bindings and explicit beta arguments. It does not minimize proof terms globally or remove arguments to named constants. A broken old witness does not prove absence of another path.",
             "The census is syntactic, with overlapping categories. A zero-notation head is not a verified zero map. An internal Mathlib-origin subset is a cohort, not an independent control. The independent control's actual size must be reported; no size match is assumed.",
             "A successful restricted rebuild shows this modified development builds. A failed rebuild identifies a local incompatibility, not mathematical necessity or invalidity of the original theorem. Independent checking of any successful counterfactual would be a separate step.",
             "Replacing PUnit with Bool or replacing 0 with 1 is not automatically a valid non-degenerate geometry. Such models must satisfy the declared structure laws. No genuine geometric model is manufactured by this package.", ""]
    (out / "stage2-plan.md").write_text("\n".join(rows))
    return pairs


def copy_tools(out):
    for filename in ("Stage2Fixture.lean", "Stage2Audit.lean", "StatementCheck.lean",
                     "GeometryAbstraction.lean", "SemanticFixture.lean", "SemanticExtension.lean",
                     "README.md", "CENSUS_PREREGISTRATION.md", "CHANGELOG.md"):
        shutil.copyfile(HERE / filename, out / filename)
    text = (out / "Stage2Audit.lean").read_text()
    marker = "\nend RHStage2\n\ndef main "
    if text.count(marker) != 1:
        raise RuntimeError("Shared Lean tool boundary is ambiguous")
    prefix = text[:text.index(marker)] + "\nend RHStage2\n\n"
    (out / "SemanticAudit.lean").write_text(prefix + (out / "SemanticExtension.lean").read_text())


def docker_base(args, out, project, toolchain, lean_path, writable_experiment=None):
    cmd = ["sudo", "docker", "run", "--rm", "--name", "rh-audit-stage2",
           "--log-driver=none", "--network", "none", "--read-only", "--cap-drop", "ALL",
           "--security-opt", "no-new-privileges:true", "--user", f"{os.getuid()}:{os.getgid()}",
           f"--cpus={args.cpus}", f"--memory={args.memory_gib}g", f"--memory-swap={args.memory_gib}g",
           "--pids-limit=512", "--ulimit", "core=0", "--tmpfs", "/tmp:rw,nosuid,nodev,size=2g,mode=1777",
           "--mount", f"type=bind,src={project},dst={project},readonly",
           "--mount", f"type=bind,src={toolchain},dst=/opt/lean,readonly",
           "--mount", f"type=bind,src={out},dst=/audit,readonly",
           "--workdir", "/audit", "--env", "PATH=/opt/lean/bin:/usr/bin:/bin",
           "--env", f"LEAN_NUM_THREADS={args.cpus}", "--env", "LEAN_ABORT_ON_PANIC=1",
           "--env", "LAKE_ARTIFACT_CACHE=false", "--env", f"LEAN_PATH={lean_path}"]
    if writable_experiment is not None:
        cmd += ["--mount", f"type=bind,src={writable_experiment},dst=/experiment",
                "--workdir", "/experiment"]
    return cmd + ["rh-lean-check:1"]


def run_logged(cmd, logfile):
    """Stream full diagnostics and preserve structured records even on failure."""
    records = []
    with logfile.open("w", buffering=1) as log:
        log.write("STARTED " + datetime.now().astimezone().isoformat() + "\n")
        log.write("COMMAND_JSON " + json.dumps(cmd) + "\n")
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, encoding="utf-8", errors="replace")
        assert proc.stdout is not None
        for line in proc.stdout:
            log.write(line)
            if line.startswith("RH_STAGE2_JSON\t"):
                row = json.loads(line.split("\t", 1)[1])
                records.append(row)
                if row.get("event") != "edge-classification":
                    print(json.dumps(row, ensure_ascii=False), flush=True)
            else:
                print(line, end="", flush=True)
        proc.stdout.close()
        status = proc.wait()
        log.write(f"\nPROCESS_EXIT_STATUS {status}\n")
        log.write("FINISHED " + datetime.now().astimezone().isoformat() + "\n")
    logfile.with_suffix(".jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))
    logfile.with_suffix(".first-error.json").write_text(
        json.dumps(first_elaboration_error(logfile.read_text()), indent=2) + "\n")
    if status:
        raise RuntimeError(f"Phase failed with exit {status}. Preserve {logfile}; later phases were not started.")
    return records


def require_smoke(rows):
    if not any(r.get("event") == "smoke-passed" for r in rows):
        raise RuntimeError("Smoke success marker missing; refusing the Main import")


def write_edge_report(out, rows, prior):
    by_pair = {(r["source"], r["target"]): r for r in rows if r.get("event") == "edge-classification"}
    expected = set(requests_from(prior))
    if set(by_pair) != expected or len([r for r in rows if r.get("event") == "edge-classification"]) != len(expected):
        raise RuntimeError("Edge classifier did not reproduce every requested pair exactly once")
    reports = ["# Classified witness paths", "",
               "All direct occurrences are reported. Several regions can apply to one pair.",
               "Binder domains include parameters, instances, data and hypotheses; no proposition inference is performed.",
               "Survival after bounded local pruning is not a test of mathematical necessity.", ""]
    for r in prior:
        if r.get("event") != "reachability" or r.get("reachable") is not True or r.get("include_structural_edges"):
            continue
        reports += [f"## `{r['root']}` → `{r['target']}`", ""]
        for a, b in zip(r["path"], r["path"][1:]):
            s, t = a["declaration"]["name"], b["declaration"]["name"]
            d = by_pair[s, t]
            labels = list(d["signature_regions"])
            if d["raw_body_reference"]:
                labels.append(d["body_region"])
            labels.extend("structural/" + x for x in d["structural_regions"])
            trim = "bounded/incomplete" if d["trim_truncated"] else "complete for implemented local transform"
            reports.append(f"- `{s}` → `{t}`: **{'; '.join(labels)}**. Direct reference after local pruning: `{d['trimmed_direct_reference']}`; {trim}.")
        reports.append("")
    (out / "classified-witness-paths.md").write_text("\n".join(reports) + "\n")
    removed = [r for r in by_pair.values() if r["raw_body_reference"] and not r["trimmed_body_reference"]]
    summary = {"requested_pairs": len(expected), "classified_pairs": len(by_pair),
               "body_references_removed_by_local_pruning": len(removed),
               "sources_with_truncated_pruning": sorted({r["source"] for r in by_pair.values() if r["trim_truncated"]}),
               "global_minimization_performed": False, "necessity_verdict": "not established"}
    (out / "edge-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2), flush=True)


def write_census_report(out, control_rows, project_rows):
    lines = ["# Syntactic census and independent Mathlib control", "",
             "Categories overlap. Counts describe syntax after leading lambdas, without delta unfolding or semantic equivalence tests.",
             "Zero-notation heads are candidates, not confirmed zero maps. Closed lambda bodies are independent of their bound parameters syntactically, not necessarily vacuous in context.",
             "The control is imported in a separate process from Mathlib only. Its roots were selected for reproducibility, not to produce a comparable size or a desired rate.",
             "The Mathlib-origin subset of the RH closure is an internal cohort, not an independent control.", ""]
    sizes = []
    for rows in (control_rows, project_rows):
        complete = [r for r in rows if r.get("event") == "census-complete"]
        if len(complete) != 1 or complete[0].get("missing") != []:
            raise RuntimeError("Census incomplete; do not interpret missing categories as zero")
        end = complete[0]
        sizes.append(end["declarations"])
        lines += [f"## {end['cohort']}", "", f"Roots: `{', '.join(end['roots'])}`",
                  f"Union closure: **{end['declarations']:,} declarations**; axioms: `{', '.join(end['axioms'])}`.", ""]
        for b in rows:
            if b.get("event") != "census-bucket":
                continue
            denom = b["declarations"]
            lines += [f"### {b['bucket']}", "", f"Denominator: {denom:,} declarations.", "",
                      "| Overlapping syntactic category | Count | Fraction of denominator |",
                      "|---|---:|---:|"]
            for cat, count, samples in zip(b["category_labels"], b["counts"], b["samples"]):
                rate = f"{count/denom:.6%}" if denom else "n/a"
                lines.append(f"| {cat} | {count:,} | {rate} |")
            lines.append("")
    lines += ["## Comparison limits", "",
              f"Independent control size: {sizes[0]:,}; headline union size: {sizes[1]:,}.",
              "These are not a size-matched or subject-matched pair. Differences in these raw rates cannot establish unusualness, a flaw, or necessity.",
              "Record/structure fields nested inside a constructor are not counted as if the entire declaration were True or a zero map. Follow-up field-level semantic classification remains open.", ""]
    (out / "census-comparison.md").write_text("\n".join(lines))


def write_pruning_report(out, raw_rows, pruned_rows):
    a = next((r for r in raw_rows if r.get("event") == "census-complete"), None)
    b = next((r for r in pruned_rows if r.get("event") == "census-complete"), None)
    if not a or not b or a.get("missing") or b.get("missing"):
        raise RuntimeError("Both reference union traversals must complete before comparing pruning")
    before = {r["target"]: r["reachable_from_any_root"] for r in raw_rows if r.get("event") == "union-watch"}
    after = {r["target"]: r["reachable_from_any_root"] for r in pruned_rows if r.get("event") == "union-watch"}
    if set(before) != set(after):
        raise RuntimeError("Pruning comparison has mismatched watch lists")
    lines = ["# Bounded local-pruning union reachability", "",
             "Both traversals start from all five headline roots. Membership means reachable from at least one root; it is not a per-root result.",
             "Only explicit unused lets and explicit unused lambda arguments are removed from stored bodies. Types are retained. No named constant's signature is minimized or unfolded.",
             "The transformed expressions are inspected, not installed as new theorems or independently kernel-checked.", "",
             f"Raw reference union: {a['declarations']:,}; locally pruned reference union: {b['declarations']:,}.",
             f"Unused lets removed while traversing pruned bodies: {b['dropped_unused_lets']:,}.",
             f"Explicit unused lambda arguments removed: {b['dropped_unused_explicit_beta_arguments']:,}.",
             f"Bodies whose local transform hit its budget: {b['bodies_with_bounded_pruning']:,}. Those subtrees were retained.", "",
             "| Watched declaration | Raw union | Locally pruned union |", "|---|---|---|"]
    for name in sorted(before):
        lines.append(f"| `{name}` | {before[name]} | {after[name]} |")
    lines += ["", "Continued reachability does not prove necessity. Loss of a reference under these reductions is evidence about the transformed syntax, not a refutation or a global proof minimization result.", ""]
    (out / "pruned-union-comparison.md").write_text("\n".join(lines))


def write_semantic_report(out, control, project):
    lines = ["# Preregistered semantic tests: bounded census", "",
             "Read CENSUS_PREREGISTRATION.md for frozen classes, counting units, scope, and exclusions.",
             "These are Lean MetaM definitional-equality tests under all transparency, not additional independent kernel checks.",
             "Unknown tests are never counted as confirmed nontrivial cases. Anonymous records arbitrarily buried in proof terms are outside the field denominator.", ""]
    for rows in (control, project):
        summaries = [r for r in rows if r.get("event") == "semantic-complete"]
        if len(summaries) != 1 or summaries[0]["missing"]:
            raise RuntimeError("Semantic traversal did not complete")
        s = summaries[0]
        lines += [f"## {s['cohort']}", "",
                  f"Closure declarations: {s['closure_declarations']:,}.",
                  f"Definitions attempted: {s['definitions_attempted']:,}; completed: {s['definitions_completed']:,}; unknown: {s['definitions_unknown']:,}.",
                  f"Record constructor fields visited in completed analyses: {s['constructor_fields_visited']:,}; definitions hitting the record depth bound: {s['definitions_with_record_depth_limit']:,}.", ""]
        for b in rows:
            if b.get("event") != "semantic-bucket":
                continue
            lines += [f"### {b['bucket']}", "", f"Denominator: {b['denominator']:,}.", "",
                      "| Frozen category | Confirmed hits |", "|---|---:|"]
            for label, count in zip(b["category_labels"], b["counts"]):
                lines.append(f"| {label} | {count:,} |")
            lines.append("")
        if s["unknown_examples"]:
            lines += ["### First unknown diagnostics", "", "```text", *s["unknown_examples"], "```", ""]
    lines += ["## Remaining use-role work", "",
              "Value classification does not determine whether an object discharges a required hypothesis, is used as ordinary data, or occurs in irrelevant syntax.",
              "The edge reports classify the selected witness paths, not every application in the full closure. A global witness-versus-ordinary census remains unestablished and must not be fabricated from these counts.",
              "The independent Mathlib closure is not assumed to match the headline closure in size or subject. Do not interpret differences as evidence of invalidity or statistical unusualness.", ""]
    (out / "semantic-census-comparison.md").write_text("\n".join(lines))


ABSTRACTION_SOURCE = Path("src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/SiegelEisensteinSecondTermHypotheses.lean")
ABSTRACTION_NAME = "nonempty_hyps_definite_side_of_closed_bound"


def abstraction_files(project, out):
    text = (project / ABSTRACTION_SOURCE).read_text()
    start_marker = "theorem " + ABSTRACTION_NAME + " :"
    end_marker = "theorem every_character_of_theta_integrals_local_matching"
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise RuntimeError("Pinned abstraction source does not have the expected theorem boundaries")
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    header, original = text[:start], text[start:end]
    if original.count("(geoCl anyGeometry)") != 3:
        raise RuntimeError("Expected exactly three literal geometry arguments in the selected theorem")
    outputs = []
    for label, binders in [
        ("baseline", ""),
        ("arbitrary-P", " (auditGamma : GlobalTheory.Mem.Top.Bl.GeoP)"),
        ("universal-P", " (auditGamma : GlobalTheory.Mem.Top.Bl.GeoP) (auditAll : ∀ D J X, auditGamma D J X)"),
    ]:
        new_name = "stage2_" + ABSTRACTION_NAME + "_" + label.replace("-", "_")
        body = original.replace(start_marker, f"theorem {new_name}{binders} :", 1)
        if label != "baseline":
            body = body.replace("(geoCl anyGeometry)", "(geoCl auditGamma)")
        contents = "import Main\n" + header + body + "\nend UpperTheory.Lit\nend\nend\n"
        contents += f"\n#check UpperTheory.Lit.{new_name}\n#print axioms UpperTheory.Lit.{new_name}\n"
        filename = {"baseline": "AbstractionBaseline.lean", "arbitrary-P": "AbstractionArbitraryP.lean",
                    "universal-P": "AbstractionUniversalP.lean"}[label]
        (out / filename).write_text(contents)
        outputs.append((label, filename))
    (out / "abstraction-design.json").write_text(json.dumps({
        "source": str(ABSTRACTION_SOURCE), "source_sha256": sha256(project / ABSTRACTION_SOURCE),
        "theorem": "UpperTheory.Lit." + ABSTRACTION_NAME,
        "literal_arguments_generalized": 3,
        "global_parameterization": False,
        "imported_dependencies": "unchanged pinned declarations; some may still specialize to anyGeometry",
        "universal_P_probe": "Makes an additional premise available; does not infer a weakest precondition or automatically adapt all imported interfaces",
    }, indent=2) + "\n")
    return outputs


def first_elaboration_error(text):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.search(r"\berror:", line) or line.startswith("error:"):
            end = min(len(lines), i+32)
            for j in range(i+1, end):
                if re.search(r"\berror:", lines[j]):
                    end = j
                    break
            snippet = "\n".join(lines[i:end])
            hint = "manual-review-required"
            if "unsolved goals" in snippet.lower():
                hint = "unresolved-proof-goal; satisfiability-not-established"
            elif "type mismatch" in snippet.lower():
                hint = "type-or-interface-mismatch; premise-status-unresolved"
            return {"line": i+1, "context": snippet, "provisional_category": hint,
                    "reviewed_classification": "pending human review"}
    return {"line": None, "context": "", "provisional_category": "no-elaboration-error-found",
            "reviewed_classification": "not applicable or process-level failure; inspect full log"}


def run_abstractions(out, base, project):
    variants = abstraction_files(project, out)
    results = []
    jobs = [("generic-GeoCl-interface", "GeometryAbstraction.lean")] + variants
    for label, filename in jobs:
        logfile = out / f"probe-{label}.log"
        passed = True
        failure = None
        try:
            run_logged(base + ["/usr/bin/time", "-v", "/opt/lean/bin/lean", "--tstack=400000",
                               f"/audit/{filename}"], logfile)
        except RuntimeError as exc:
            passed = False
            failure = str(exc)
        result = {"probe": label, "source": filename, "source_sha256": sha256(out / filename),
                  "compiled": passed, "failure": failure,
                  "first_error": first_elaboration_error(logfile.read_text()),
                  "global_necessity_or_invalidity_verdict": "not established"}
        results.append(result)
        (out / "abstraction-results.json").write_text(json.dumps(results, indent=2) + "\n")
        if label == "baseline" and not passed:
            raise RuntimeError("Baseline clone did not compile; arbitrary-P probes were not attempted. Review the harness/context first.")
    lines = ["# Scoped geometry abstraction experiments", "",
             "These are local experiments against the original imported environment. They do not globally parameterize Main or modify the original definitions.",
             "The body of the selected theorem is copied from the pinned source. The baseline clone must compile before its three literal geometry arguments are generalized.",
             "A universal-P premise, if present, is merely available to the unchanged copied proof script. Its success/failure does not determine a weakest requirement on P.", ""]
    for r in results:
        lines += [f"## {r['probe']}", "", f"Compiled: **{r['compiled']}**; log: `probe-{r['probe']}.log`.",
                  f"Provisional first-error category: `{r['first_error']['provisional_category']}`.",
                  "Reviewed classification: pending. No interpretation of a failure as necessity or invalidity is automatic.", ""]
        if r["first_error"]["context"]:
            lines += ["```text", r["first_error"]["context"], "```", ""]
    lines += ["## What successful generic lemmas would establish", "",
              "A universal P is sufficient for GeoCl P at every input. Any particular GeoCl P witness has a seed satisfying P somewhere in its constructor derivation. GeoCl False is empty. GeoCl anyGeometry is universal.",
              "These statements explain the generic closure interface. They do not show whether every other premise of the headline theorem has the intended mathematical meaning.", ""]
    (out / "abstraction-report.md").write_text("\n".join(lines))


def transport_files(project, out):
    """Keep the copied proof, explicitly transport its two failed interfaces."""
    abstraction_files(project, out)
    universal = (out / "AbstractionUniversalP.lean").read_text()
    intro = "  intro P F hA hM hX hL hN\n"
    open_boundary = "  have hOpenA := hMono.2 hOpen1\n"
    final_boundary = "  exact _root_.GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt"
    for anchor in (intro, open_boundary, final_boundary):
        if universal.count(anchor) != 1:
            raise RuntimeError("Pinned transport boundary absent or ambiguous: " + anchor.strip())
    universal_binder = "(auditAll : ∀ D J X, auditGamma D J X)"
    if universal.count(universal_binder) != 1:
        raise RuntimeError("Universal-P probe binder does not match")
    q = "_root_.GlobalTheory.Mem.Top.Bl."
    jobs = []
    for label, leaf, back_proof in [
        ("universal-P-transport", "AbstractionUniversalPTransport.lean",
         f"{q}GeoCl.base (auditAll D J X)"),
        ("universal-closure-transport", "AbstractionUniversalClosureTransport.lean",
         "auditClosed D J X"),
    ]:
        text = universal
        if label == "universal-closure-transport":
            text = text.replace(universal_binder,
                f"(auditClosed : ∀ D J X, {q}geoCl auditGamma D J X)", 1)
        old_name = "stage2_" + ABSTRACTION_NAME + "_universal_P"
        new_name = "stage2_" + ABSTRACTION_NAME + "_" + label.replace("-", "_")
        text = text.replace(old_name, new_name)
        equality = (
            f"  have auditClosureEq : {q}geoCl auditGamma = {q}geoCl {q}anyGeometry := by\n"
            "    funext D J X\n"
            "    apply propext\n"
            "    constructor\n"
            "    · intro _\n"
            f"      exact {q}GeoCl.base True.intro\n"
            "    · intro _\n"
            f"      exact {back_proof}\n"
        )
        text = text.replace(intro, intro + equality, 1)
        text = text.replace(open_boundary,
            "  have hOpenA := hMono.2 (by\n"
            "    simpa only [auditClosureEq] using hOpen1)\n", 1)
        text = text.replace(final_boundary,
            "  simp only [auditClosureEq] at hFun hL3\n" + final_boundary, 1)
        (out / leaf).write_text(text)
        diff = difflib.unified_diff((out / "AbstractionBaseline.lean").read_text().splitlines(True),
                                    text.splitlines(True), fromfile="compiled-baseline", tofile=leaf)
        (out / leaf.replace(".lean", ".diff")).write_text("".join(diff))
        jobs.append((label, leaf))
    return jobs


def verify_transport_prior(prior, out):
    if prior is None:
        raise RuntimeError("--abstraction-prior must identify the completed abstraction run")
    prior = prior.expanduser().resolve(strict=True)
    meta_file = prior / "run-metadata.json"
    results_file = prior / "abstraction-results.json"
    meta = json.loads(meta_file.read_text())
    results = json.loads(results_file.read_text())
    if meta.get("phase") != "abstraction" or meta.get("phase_completed") is not True or \
            meta.get("source_pin") != SOURCE_PIN or meta.get("mathlib_pin") != MATHLIB_PIN or \
            meta.get("main_olean_sha256") != MAIN_SHA:
        raise RuntimeError("Prior abstraction metadata is incomplete or has different pins")
    baseline = next((r for r in results if r.get("probe") == "baseline"), None)
    if not baseline or baseline.get("compiled") is not True:
        raise RuntimeError("A successfully compiled prior baseline is required")
    expected = baseline.get("source_sha256")
    if sha256(prior / "AbstractionBaseline.lean") != expected or \
            sha256(out / "AbstractionBaseline.lean") != expected:
        raise RuntimeError("Baseline source differs from the previously compiled baseline")
    (out / "transport-prior.json").write_text(json.dumps({
        "prior_directory": str(prior), "baseline_source_sha256": expected,
        "run_metadata_sha256": sha256(meta_file), "abstraction_results_sha256": sha256(results_file),
        "prior_results": results,
    }, indent=2) + "\n")


def run_transport(out, base, project, prior):
    jobs = transport_files(project, out)
    verify_transport_prior(prior, out)
    results = []
    for label, filename in jobs:
        logfile = out / f"probe-{label}.log"
        passed, failure = True, None
        try:
            run_logged(base + ["/usr/bin/time", "-v", "/opt/lean/bin/lean", "--tstack=400000",
                               f"/audit/{filename}"], logfile)
        except RuntimeError as exc:
            passed, failure = False, str(exc)
        has_sorry = "sorryAx" in logfile.read_text()
        results.append({"probe": label, "source": filename,
                        "source_sha256": sha256(out / filename),
                        "compiled_without_reported_sorryAx": passed and not has_sorry,
                        "process_succeeded": passed, "reported_sorryAx": has_sorry,
                        "failure": failure,
                        "first_error": first_elaboration_error(logfile.read_text()),
                        "global_parameterization": False,
                        "independent_kernel_check_performed": False})
        (out / "transport-results.json").write_text(json.dumps(results, indent=2) + "\n")
    lines = ["# Explicit transport at the two failed abstraction interfaces", "",
             "The prior baseline source must match the already compiled baseline byte for byte. It is not rebuilt here.",
             "Two conditional copies of that proof are tested. Both still replace only its three literal geometry arguments; imported declarations are unchanged.",
             "The universal-P case proves geoCl P = geoCl anyGeometry using its universal-P premise and the base constructor. The closure case assumes universal geoCl P directly, then proves the same equality.",
             "That equality is used explicitly when supplying hOpen1 and before passing hFun/hL3 to the specialized final interface. Neither probe simply invokes the original bundle theorem.", "",
             "| Probe | Process succeeded | Reported sorryAx |", "|---|---|---|"]
    for r in results:
        lines.append(f"| {r['probe']} | {r['process_succeeded']} | {r['reported_sorryAx']} |")
    lines += ["", "## Interpretation", "",
              "Success would show that explicit propositional transport resolves these local interface mismatches under the stated premise. It would not generalize the whole project, identify a weakest geometric condition, or establish global necessity or invalidity.",
              "Universal P implies universal GeoCl P by the base constructor. The converse, or strict weakness of the closure premise in this development, is not established by this test.",
              "Failure must be read from the first diagnostic. A failed declaration's sorryAx output is error recovery in the experimental file, not a new axiom of Main.", ""]
    (out / "transport-report.md").write_text("\n".join(lines))


def allocated_bytes(path):
    return int(command(["du", "-sk", str(path)]).split()[0]) * 1024


def storage_estimate(project, destination):
    # Allocation may differ on another filesystem; this is a conservative
    # estimate, never a guarantee. No full copy of solution.export is made.
    build = allocated_bytes(project / ".lake/build")
    src = allocated_bytes(project / "src")
    reserve = max(20 * 1024**3, build // 4)
    required = build + src + reserve
    free = shutil.disk_usage(destination).free
    return {"existing_project_build_allocated_bytes": build, "source_allocated_bytes": src,
            "reserve_bytes": reserve, "estimated_required_free_bytes": required,
            "current_free_bytes": free, "sufficient_for_estimate": free >= required}


def active_checkers():
    active = []
    for proc in Path("/proc").iterdir():
        if not proc.name.isdigit():
            continue
        try:
            words = (proc / "cmdline").read_bytes().split(b"\0")
            argv = [w.decode(errors="replace") for w in words if w]
            if not argv:
                continue
            executable = Path(argv[0]).name
            if (executable == "lake" and "comparator" in argv[1:]) or \
                    executable in {"leanchecker-paranoid", "nanoda_bin"}:
                active.append({"pid": int(proc.name), "executable": executable})
        except (OSError, PermissionError):
            continue
    return active


def apply_mutation(text, variant):
    if variant not in MUTATIONS:
        raise RuntimeError("Unknown mutation")
    if text.count(ORIGINAL_GEOMETRY) != 1:
        raise RuntimeError("Expected exact pinned anyGeometry definition exactly once")
    return text.replace(ORIGINAL_GEOMETRY, MUTATIONS[variant], 1)


def extract_commit(project, dest):
    dest.mkdir()
    proc = subprocess.Popen(["git", "archive", "--format=tar", SOURCE_PIN], cwd=project,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdout is not None
    succeeded = False
    try:
        with tarfile.open(fileobj=proc.stdout, mode="r|") as archive:
            for member in archive:
                rel = Path(member.name)
                if rel.is_absolute() or ".." in rel.parts or not (member.isdir() or member.isfile()):
                    raise RuntimeError("Unexpected path/type in source archive")
                p = dest / rel
                if member.isdir():
                    p.mkdir(parents=True, exist_ok=True)
                else:
                    p.parent.mkdir(parents=True, exist_ok=True)
                    data = archive.extractfile(member)
                    assert data is not None
                    with p.open("wb") as f:
                        shutil.copyfileobj(data, f)
                    p.chmod(0o755 if member.mode & 0o111 else 0o644)
        succeeded = True
    finally:
        proc.stdout.close()
        if not succeeded and proc.poll() is None:
            proc.terminate()
        status = proc.wait()
    if status:
        raise RuntimeError("git archive did not complete successfully")


def mutation_build(args, out, project, toolchain, manifest, base):
    current = active_checkers()
    if current:
        raise RuntimeError("Mutation rebuild deferred: Comparator or a proof checker is still running: " + json.dumps(current))
    estimate = storage_estimate(project, out)
    (out / "mutation-storage.json").write_text(json.dumps(estimate, indent=2) + "\n")
    if not estimate["sufficient_for_estimate"]:
        raise RuntimeError("Mutation rebuild deferred: insufficient free space for a fresh isolated project build; see mutation-storage.json")
    exp = out / "experiment"
    extract_commit(project, exp)
    package_dir = exp / ".lake/packages"
    package_dir.mkdir(parents=True, exist_ok=True)
    for p in manifest["packages"]:
        name = p["name"]
        if not isinstance(name, str) or Path(name).name != name or name in {".", ".."}:
            raise RuntimeError("Unexpected dependency directory name")
        original = project / ".lake/packages" / name
        if not original.is_dir():
            raise RuntimeError(f"Missing installed dependency: {name}")
        (package_dir / name).symlink_to(original, target_is_directory=True)
    # The original checkout and all reused dependency packages are mounted
    # read-only. Only /experiment and /tmp are writable inside this container.
    def build(label):
        cmd = docker_base(args, out, project, toolchain, "", exp)
        shell = "set -euo pipefail\nunset LEAN_PATH\n/usr/bin/time -v /opt/lean/bin/lake build Main\n"
        build_log = out / f"mutation-{label}-build.log"
        try:
            run_logged(cmd + ["/bin/bash", "-c", shell], build_log)
        finally:
            if build_log.exists():
                (out / f"mutation-{label}-first-error.json").write_text(
                    json.dumps(first_elaboration_error(build_log.read_text()), indent=2) + "\n")
        cmd = docker_base(args, out, project, toolchain, "", exp)
        shell = "set -euo pipefail\nunset LEAN_PATH\n/opt/lean/bin/lake env /opt/lean/bin/lean --tstack=400000 /audit/StatementCheck.lean\n"
        run_logged(cmd + ["/bin/bash", "-c", shell], out / f"mutation-{label}-statement.log")
    meta = {"variant": args.variant, "baseline_passed": False, "modified_build_passed": False,
            "independent_kernel_check_performed": False, "original_source_pin": SOURCE_PIN,
            "workspace": str(exp), "necessity_verdict": "not established"}
    dest = out / "mutation-result.json"
    try:
        build("baseline")
        meta["baseline_passed"] = True
        original = (exp / OVERIX).read_text()
        modified = apply_mutation(original, args.variant)
        (out / "mutation-original-OverIx.lean").write_text(original)
        (out / "mutation-modified-OverIx.lean").write_text(modified)
        (exp / OVERIX).write_text(modified)
        build(args.variant)
        meta["modified_build_passed"] = True
        meta["modified_main_olean_sha256"] = sha256(exp / ".lake/build/lib/lean/Main.olean")
    finally:
        dest.write_text(json.dumps(meta, indent=2) + "\n")


def bundle_results(out):
    bundle = out / "stage2-evidence.zip"
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob("*")):
            if p == bundle or "experiment" in p.relative_to(out).parts or not p.is_file():
                continue
            z.write(p, p.relative_to(out))
    return bundle


def run(args):
    project = args.project.expanduser().resolve(strict=True)
    toolchain = args.toolchain.expanduser().resolve(strict=True)
    manifest = validate(project, toolchain)
    prior_path = args.prior.expanduser().resolve(strict=True)
    prior, graph, summaries = read_prior(prior_path)
    out = safe_output(project, args.output)
    copy_tools(out)
    pairs = write_plan(out, prior, graph, summaries)
    watched = sorted({r["name"] for r in prior if r.get("event") == "watch-declaration"})
    (out / "watch-names.txt").write_text("\n".join(watched) + "\n")
    library_dirs = sorted(p for p in (project / ".lake/packages").glob("*/.lake/build/lib/lean") if p.is_dir())
    library_dirs.append(project / ".lake/build/lib/lean")
    lean_path = ":".join(["/tmp"] + [str(p) for p in library_dirs])
    meta = {"started": datetime.now().astimezone().isoformat(), "phase": args.phase,
            "source_pin": SOURCE_PIN, "mathlib_pin": MATHLIB_PIN,
            "main_olean_sha256": MAIN_SHA, "statements_olean_sha256": STATEMENTS_SHA,
            "prior_records_sha256": sha256(prior_path), "prior_records_path": str(prior_path),
            "requested_edges": len(pairs), "cpus": args.cpus, "memory_gib": args.memory_gib,
            "lean_executable_sha256": sha256(toolchain / "bin/lean"),
            "driver_sha256": sha256(Path(__file__).resolve()),
            "tool_sha256": {p.name: sha256(p) for p in out.iterdir() if p.suffix in {".lean", ".md"}},
            "phase_completed": False, "comparator_result": "not read or changed by this tool"}
    (out / "run-metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"Stage 2 folder: {out}", flush=True)
    print(f"Phase: {args.phase}; {len(pairs)} distinct witness edges.", flush=True)
    print("Comparator is left untouched. Read-only phases use separate processes and a capped container.", flush=True)
    try:
        if args.phase == "plan":
            pass
        elif args.phase == "mutation-plan":
            estimate = storage_estimate(project, out)
            estimate["active_checkers"] = active_checkers()
            (out / "mutation-storage.json").write_text(json.dumps(estimate, indent=2) + "\n")
            print(json.dumps(estimate, indent=2), flush=True)
        else:
            if not shutil.which("docker"):
                raise RuntimeError("Docker is not installed")
            subprocess.run(["sudo", "-v"], check=True)
            command(["sudo", "docker", "image", "inspect", "rh-lean-check:1", "--format", "{{.Id}}"])
            base = docker_base(args, out, project, toolchain, lean_path)
            if args.phase == "mutation-build":
                mutation_build(args, out, project, toolchain, manifest, base)
            else:
                smoke_script = "set -euo pipefail\n/opt/lean/bin/lean -o /tmp/Stage2Fixture.olean /audit/Stage2Fixture.lean\n/opt/lean/bin/lean --tstack=400000 --run /audit/Stage2Audit.lean smoke\n"
                smoke_rows = run_logged(base + ["/bin/bash", "-c", smoke_script], out / "smoke.log")
                require_smoke(smoke_rows)
                if args.phase == "smoke":
                    pass
                elif args.phase == "inspect":
                    run_logged(base + ["/usr/bin/time", "-v", "/opt/lean/bin/lean", "--tstack=400000",
                                       "/audit/StatementCheck.lean"], out / "statement-check.log")
                    rows = run_logged(base + ["/usr/bin/time", "-v", "/opt/lean/bin/lean", "--tstack=400000",
                                              "--run", "/audit/Stage2Audit.lean", "edges", "/audit/edge-requests.tsv"], out / "edge-classification.log")
                    write_edge_report(out, rows, prior)
                elif args.phase == "abstraction":
                    run_abstractions(out, base, project)
                elif args.phase == "abstraction-transport":
                    run_transport(out, base, project, args.abstraction_prior)
                elif args.phase == "census":
                    control = run_logged(base + ["/usr/bin/time", "-v", "/opt/lean/bin/lean", "--tstack=400000",
                                                 "--run", "/audit/Stage2Audit.lean", "control"], out / "census-control.log")
                    project_rows = run_logged(base + ["/usr/bin/time", "-v", "/opt/lean/bin/lean", "--tstack=400000",
                                                      "--run", "/audit/Stage2Audit.lean", "census"], out / "census-headlines.log")
                    write_census_report(out, control, project_rows)
                elif args.phase == "pruned-closure":
                    raw = run_logged(base + ["/usr/bin/time", "-v", "/opt/lean/bin/lean", "--tstack=400000",
                                             "--run", "/audit/Stage2Audit.lean", "census", "/audit/watch-names.txt"], out / "pruning-raw.log")
                    pruned = run_logged(base + ["/usr/bin/time", "-v", "/opt/lean/bin/lean", "--tstack=400000",
                                                "--run", "/audit/Stage2Audit.lean", "pruned", "/audit/watch-names.txt"], out / "pruning-reduced.log")
                    write_pruning_report(out, raw, pruned)
                elif args.phase in {"semantic-smoke", "semantic-census"}:
                    script = "set -euo pipefail\n/opt/lean/bin/lean -o /tmp/SemanticFixture.olean /audit/SemanticFixture.lean\n/opt/lean/bin/lean --tstack=400000 --run /audit/SemanticAudit.lean semantic-smoke\n"
                    smoke_rows = run_logged(base + ["/bin/bash", "-c", script], out / "semantic-smoke.log")
                    if not any(r.get("event") == "semantic-smoke-passed" for r in smoke_rows):
                        raise RuntimeError("Semantic smoke marker missing; refusing the Main import")
                    if args.phase == "semantic-census":
                        control = run_logged(base + ["/usr/bin/time", "-v", "/opt/lean/bin/lean", "--tstack=400000",
                                                     "--run", "/audit/SemanticAudit.lean", "semantic-control"], out / "semantic-control.log")
                        project_rows = run_logged(base + ["/usr/bin/time", "-v", "/opt/lean/bin/lean", "--tstack=400000",
                                                          "--run", "/audit/SemanticAudit.lean", "semantic-main"], out / "semantic-headlines.log")
                        write_semantic_report(out, control, project_rows)
        validate(project, toolchain)
        meta["phase_completed"] = True
    except BaseException as exc:
        meta["failure"] = str(exc)
        raise
    finally:
        meta["finished"] = datetime.now().astimezone().isoformat()
        (out / "run-metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
        bundle = bundle_results(out)
        print(f"Evidence: {bundle}", flush=True)
        print(f"Evidence SHA-256: {sha256(bundle)}", flush=True)
    print("Requested phase completed. This is not a new independent kernel-check verdict.", flush=True)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--phase", choices=["plan", "smoke", "inspect", "abstraction", "abstraction-transport", "census", "semantic-smoke", "semantic-census", "pruned-closure", "mutation-plan", "mutation-build"], default="plan")
    ap.add_argument("--project", type=Path, default=Path.home() / "rh-verification/riemann-hypothesis")
    ap.add_argument("--toolchain", type=Path, default=Path.home() / ".elan/toolchains/leanprover--lean4---v4.33.1")
    ap.add_argument("--prior", type=Path, default=Path.home() / "rh-verification/critics-audit/proof-trace-8tnvwr47/records.jsonl")
    ap.add_argument("--output", type=Path, default=Path.home() / "rh-verification/critics-audit-stage2")
    ap.add_argument("--cpus", type=int, default=2)
    ap.add_argument("--memory-gib", type=int, default=100)
    ap.add_argument("--variant", choices=sorted(MUTATIONS), default="restrict-false")
    ap.add_argument("--abstraction-prior", type=Path,
                    help="Completed abstraction output folder; required for abstraction-transport")
    args = ap.parse_args()
    if not 1 <= args.cpus <= 72 or not 4 <= args.memory_gib <= 112:
        ap.error("Use 1..72 CPUs and 4..112 GiB. Keep defaults while Comparator runs.")
    try:
        return run(args)
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"STAGE2_ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

