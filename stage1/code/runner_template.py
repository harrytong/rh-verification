#!/usr/bin/env python3
"""Read-only compiled-declaration audit of the pinned RH/Dirichlet-GRH proof.

Python 3.10+, standard library. Uses the existing rh-lean-check:1 Docker image
and the already-installed Lean 4.33.1 toolchain. No network, builds of the RH
project, export copies, or changes to Comparator. The small isolated fixture
is compiled and tested before the large Main import is attempted.

This tool traces stored syntax, including theorem and opaque proof bodies.
It is not a new proof checker, a necessity analysis, or a refutation verdict.
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

SOURCE_PIN = "753431bfe28701f6f3937f664fcaf08daa139c03"
MATHLIB_PIN = "0df444a360eaa60ab8c11dca51a86af692955474"
MAIN_SHA = "9146dfb4148e24d2252e04c50742f3e49dd126dfcc5006d10bf5f873ddf796ad"
STATEMENTS_SHA = "f8e0aed3c2d69390b6dd3bb24e13aa25e043a02ca42f021e3f6e4ec8b57fd6b1"
LEAN_SOURCE = __EMBED_LEAN__
FIXTURE_SOURCE = __EMBED_FIXTURE__
FINDINGS = __EMBED_FINDINGS__


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
    return manifest


def write_results(out, records, project, status):
    completed = status == 0 and any(r.get("event") == "audit-completed" for r in records)
    smoke = any(r.get("event") == "smoke-passed" for r in records)
    graph = next((r for r in records if r.get("event") == "graph-complete" and
                  "riemannHypothesis" in r.get("roots", [])), {})
    decls = {r["name"]: r for r in records if r.get("event") == "watch-declaration"}
    with (out / "records.jsonl").open("w") as f:
        for row in records:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    rows = ["# RH/Dirichlet-GRH compiled dependency audit", "",
            f"Source commit: `{SOURCE_PIN}`", f"Mathlib commit: `{MATHLIB_PIN}`", "Lean: `4.33.1`", "",
            f"Isolated smoke test passed: **{smoke}**",
            f"Full audit completed: **{completed}**", f"Container exit status: `{status}`", "",
            "This is a stored-syntax dependency audit, not an independent kernel check or a verdict on mathematical validity.",
            "Reference paths follow constants in types and definition/theorem/opaque bodies. Expanded paths also follow inductive declarations and recursor rules.",
            "A syntactic path can pass through unused lets or arguments. Absence of a named lemma does not exclude an inlined or alternative argument.", ""]
    if not completed:
        rows += ["**Incomplete run: do not treat absent paths as negative findings.**", ""]
    if graph:
        rows += [f"Union graph declarations: {graph.get('declarations'):,}",
                 f"Union graph edges: {graph.get('edges'):,}",
                 f"Missing referenced declarations: {graph.get('missing')}", ""]
    for r in records:
        if r.get("event") == "root-summary":
            label = "expanded" if r["include_structural_edges"] else "references"
            rows += [f"- `{r['root']}` ({label}): {r['visited']:,} declarations; axioms: `{', '.join(r['axioms'])}`"]
    rows += ["", "## Watched declarations", "",
             "| Declaration | Present in imported environment | RH reference path | Dirichlet nonvanishing reference path |", "|---|---|---|---|"]
    by_target = {}
    for r in records:
        if r.get("event") == "reachability" and not r["include_structural_edges"]:
            by_target[(r["root"], r["target"])] = r["reachable"]
    for name, d in decls.items():
        def verdict(root):
            v = by_target.get((root, name))
            return "yes" if v is True else ("no" if v is False and completed else "unknown")
        rows.append(f"| `{name}` | {'yes' if d['exists'] else 'no'} | {verdict('riemannHypothesis')} | {verdict('LFunction_ne_zero_of_half_lt_re')} |")
    (out / "dependency-summary.md").write_text("\n".join(rows) + "\n")
    paths = ["# Witness paths", "", "Each arrow is a syntactic dependency, not a claim that a premise is indispensable.", ""]
    modules = set()
    for r in records:
        if r.get("event") == "watch-declaration" and r.get("exists"):
            modules.add(r["declaration"]["module"])
            modules.update(d["module"] for d in r["direct_edges"])
        if r.get("event") != "reachability" or not r["reachable"]:
            continue
        variant = "expanded" if r["include_structural_edges"] else "references"
        paths += [f"## {r['root']} to {r['target']} ({variant})", ""]
        for i, step in enumerate(r["path"]):
            d = step["declaration"]
            modules.add(d["module"])
            paths.append(f"{i + 1}. `{d['name']}` via `{step['edge_from_parent']}`; module `{d['module']}`")
        paths.append("")
    (out / "dependency-paths.md").write_text("\n".join(paths) + "\n")
    source_meta = {"copied": [], "omitted": []}
    budget = 12 * 1024 * 1024
    for module in sorted(modules):
        parts = module.split(".")
        if not all(p and not any(c in p for c in '/\\<>') for p in parts):
            continue
        rel = Path(*parts).with_suffix(".lean")
        choices = [(project / "src" / rel, "project"),
                   (project / ".lake/packages/mathlib" / rel, "mathlib")]
        found = next(((p, label) for p, label in choices if p.is_file() and not p.is_symlink()), None)
        if not found:
            continue
        p, label = found
        size = p.stat().st_size
        if len(source_meta["copied"]) >= 400 or size > budget:
            source_meta["omitted"].append(module)
            continue
        dest = out / "followup-source" / label / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = p.read_bytes()
        dest.write_bytes(data)
        source_meta["copied"].append({"module": module, "path": str(dest.relative_to(out)),
                                      "sha256": hashlib.sha256(data).hexdigest()})
        budget -= len(data)
    (out / "followup-source-index.json").write_text(json.dumps(source_meta, indent=2) + "\n")
    return completed, smoke


def run(args):
    project = args.project.expanduser().resolve(strict=True)
    toolchain = args.toolchain.expanduser().resolve(strict=True)
    validate(project, toolchain)
    if not shutil.which("docker"):
        raise RuntimeError("Docker executable is missing")
    parent = args.output.expanduser().resolve()
    if parent == project or project in parent.parents:
        raise RuntimeError("Output must be outside the proof checkout")
    parent.mkdir(parents=True, exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix="proof-trace-", dir=parent))
    (out / "RHCriticsTrace.lean").write_text(LEAN_SOURCE)
    (out / "RHCriticsFixture.lean").write_text(FIXTURE_SOURCE)
    (out / "source-findings.md").write_text(FINDINGS)
    library_dirs = sorted(p for p in (project / ".lake/packages").glob("*/.lake/build/lib/lean") if p.is_dir())
    library_dirs.append(project / ".lake/build/lib/lean")
    lean_path = ":".join(["/tmp"] + [str(p) for p in library_dirs])
    meta = {"started": datetime.now().astimezone().isoformat(), "source": SOURCE_PIN,
            "mathlib": MATHLIB_PIN, "toolchain": "leanprover/lean4:v4.33.1",
            "main_olean_sha256": MAIN_SHA, "statements_olean_sha256": STATEMENTS_SHA,
            "lean_executable_sha256": sha256(toolchain / "bin/lean"),
            "trace_program_sha256": sha256(out / "RHCriticsTrace.lean"),
            "memory_limit_gib": 112, "cpu_limit": 2, "lean_path": lean_path}
    (out / "run-metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"Audit folder: {out}", flush=True)
    print("Container: rh-critics-audit; CPU limit: 2 logical CPUs; memory limit: 112 GiB.", flush=True)
    print("The running Comparator is left untouched. The initial Main import may be quiet.", flush=True)
    subprocess.run(["sudo", "-v"], check=True)
    command(["sudo", "docker", "image", "inspect", "rh-lean-check:1", "--format", "{{.Id}}"])
    shell = r'''set -euo pipefail
/opt/lean/bin/lean -o /tmp/RHCriticsFixture.olean /audit/RHCriticsFixture.lean
/opt/lean/bin/lean --tstack=400000 --run /audit/RHCriticsTrace.lean smoke
printf '\nSmoke test passed. Starting the pinned compiled-project audit.\n'
/usr/bin/time -v /opt/lean/bin/lean --tstack=400000 --run /audit/RHCriticsTrace.lean main
'''
    cmd = ["sudo", "docker", "run", "--rm", "--name", "rh-critics-audit",
           "--log-driver=none", "--network", "none", "--read-only", "--cap-drop", "ALL",
           "--security-opt", "no-new-privileges:true", "--user", f"{os.getuid()}:{os.getgid()}",
           "--cpus=2", "--memory=112g", "--memory-swap=112g", "--pids-limit=256",
           "--ulimit", "core=0", "--tmpfs", "/tmp:rw,nosuid,nodev,size=1g,mode=1777",
           "--mount", f"type=bind,src={project},dst={project},readonly",
           "--mount", f"type=bind,src={toolchain},dst=/opt/lean,readonly",
           "--mount", f"type=bind,src={out},dst=/audit,readonly", "--workdir", "/audit",
           "--env", "PATH=/opt/lean/bin:/usr/bin:/bin", "--env", "LEAN_NUM_THREADS=2",
           "--env", "LEAN_ABORT_ON_PANIC=1", "--env", f"LEAN_PATH={lean_path}",
           "rh-lean-check:1", "/bin/bash", "-c", shell]
    records = []
    with (out / "audit.log").open("w", buffering=1) as log:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, encoding="utf-8", errors="replace")
        assert proc.stdout is not None
        for line in proc.stdout:
            log.write(line)
            if line.startswith("RH_AUDIT_JSON\t"):
                r = json.loads(line.split("\t", 1)[1])
                records.append(r)
                if r.get("event") in {"graph-complete", "smoke-passed", "root-summary", "audit-completed"}:
                    print(json.dumps(r, ensure_ascii=False), flush=True)
            else:
                print(line, end="", flush=True)
        status = proc.wait()
    validate(project, toolchain)
    complete, smoke = write_results(out, records, project, status)
    meta.update({"finished": datetime.now().astimezone().isoformat(), "container_status": status,
                 "smoke_passed": smoke, "dependency_audit_completed": complete})
    (out / "run-metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    bundle = out / "compiled-dependency-evidence.zip"
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob("*")):
            if p.is_file() and p != bundle:
                z.write(p, p.relative_to(out))
    print(f"\nFull audit completed: {complete}; isolated smoke passed: {smoke}")
    print(f"Summary: {out / 'dependency-summary.md'}")
    print(f"Evidence ZIP: {bundle}")
    print(f"ZIP SHA-256: {sha256(bundle)}")
    print("This is a dependency audit, not an additional RH/GRH kernel-check verdict.")
    return 0 if complete else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", type=Path, default=Path.home() / "rh-verification/riemann-hypothesis")
    ap.add_argument("--toolchain", type=Path,
                    default=Path.home() / ".elan/toolchains/leanprover--lean4---v4.33.1")
    ap.add_argument("--output", type=Path, default=Path.home() / "rh-verification/critics-audit")
    args = ap.parse_args()
    try:
        return run(args)
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
