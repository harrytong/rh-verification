#!/usr/bin/env python3
"""Collect public-source evidence for the Nielsen/Chu RH critique.

Python 3.10+, standard library only. Run on Harry's existing Ubuntu checkout:
  python3 collect_rh_critics.py --project ~/rh-verification/riemann-hypothesis

This is a SOURCE evidence collector, not a proof checker or a compiled-term
dependency tracer. It does not execute Lean project code, change the checkout,
build anything, read the whole proof export, or contact the network. Its ZIP
contains selected public Lean source, toolchain source, and verification metadata.
"""

import argparse
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
import zipfile

SOURCE_PIN = "753431bfe28701f6f3937f664fcaf08daa139c03"
MATHLIB_PIN = "0df444a360eaa60ab8c11dca51a86af692955474"
TOOLCHAIN = "leanprover/lean4:v4.33.1"

TOKENS = (
    "anyGeometry", "geoOf", "geoCl", "GeoCl", "geoDegenerate",
    "geoDegenerateNoTau", "algDegenerate", "algJunk", "padDegenerate",
    "padJunk", "mdlJunk", "hypsE", "plugAll", "geoOf_surf", "GeoTiedP",
    "geoTied", "formsTieX", "degree_value_of_determinant", "hExpl6",
    "every_character_of_literature_of_vWin",
    "every_character_of_theta_integrals_local_matching",
    "everyCharacter_of_row", "rhOfAll", "allChi", "claimAll", "critAll",
    "geoOver_stages", "divEx_prov", "divEx_geoCl",
    "memberE_closing_alt_alt", "member_exists_baseLattice_alt",
)
MATCH = re.compile(r"(?<![\w'])((?:" + "|".join(map(re.escape, TOKENS)) + r"))(?![\w'])")
BROAD = "|".join(TOKENS)
MATHLIB_TOKENS = ("RiemannHypothesis", "riemannZeta", "LFunction")
EXTRA_BASENAMES = {
    "Main.lean", "Statements.lean", "MainTheorems.lean",
    "MainTheoremsAll.lean", "MainTheoremsCritical.lean", "MainConclusion.lean",
    "EveryCharacterE.lean", "EveryCharacterOfLiteratureOfWVin.lean",
    "EveryCharacterOfLiteratureOfVWin.lean",
    "SiegelEisensteinSecondTermHypotheses.lean", "GeoTiedP.lean",
    "TupPinsOfMuIsW.lean", "PublishedInputsImplyConclusion.lean",
    "MemberEClosing.lean", "NotGeoClFalse.lean", "OverIx.lean",
    "LinkedBundleConstructionExists.lean",
}
CORE_API = (
    "Lean/Util/CollectAxioms.lean", "Lean/Util/CollectConstants.lean",
    "Lean/Declaration.lean", "Lean/Expr.lean", "Lean/Environment.lean",
    "Lean/MonadEnv.lean", "Lean/Elab/Command.lean",
)


def git(project, *args):
    p = subprocess.run(["git", "-C", str(project), *args],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors="replace").strip() or f"git {args} failed")
    return p.stdout


def unchanged(project):
    diff = git(project, "diff", "--name-only", "HEAD", "--", "src", "lean-toolchain",
               "lakefile.toml", "lake-manifest.json").decode().strip()
    if diff:
        raise RuntimeError("Tracked project inputs differ from HEAD; no source changes made:\n" + diff)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def scan(project, tracked, tokens=TOKENS, root="src"):
    """Use rg first, git grep as fallback; retain only tracked Lean sources."""
    broad = "|".join(map(re.escape, tokens))
    match = re.compile(r"(?<![\w'])((?:" + broad + r"))(?![\w'])")
    if shutil.which("rg"):
        cmd = ["rg", "--no-config", "--no-ignore", "--hidden", "--no-heading",
               "--line-number", "--color", "never", "--glob", "*.lean", "-e", broad, root]
    else:
        cmd = ["git", "grep", "--no-color", "-n", "-I", "-E", "-e", broad, "--", root]
    counts = collections.Counter()
    files = {t: set() for t in tokens}
    rows = []
    with tempfile.TemporaryFile(mode="w+t") as errors:
        proc = subprocess.Popen(cmd, cwd=project, stdout=subprocess.PIPE, stderr=errors,
                                text=True, encoding="utf-8", errors="replace")
        assert proc.stdout is not None
        for line in proc.stdout:
            parts = line.rstrip("\n").split(":", 2)
            if len(parts) != 3 or parts[0] not in tracked:
                continue
            path, lineno, text = parts
            hits = match.findall(text)
            if not hits:
                continue
            counts.update(hits)
            for token in set(hits):
                files[token].add(path)
            rows.append((path, int(lineno), ",".join(sorted(set(hits))), text))
        code = proc.wait()
        errors.seek(0)
        if code not in (0, 1):
            raise RuntimeError("Source search failed: " + errors.read())
    return counts, files, sorted(rows)


def collect(project, out_parent, toolchain):
    project = project.expanduser().resolve(strict=True)
    head = git(project, "rev-parse", "HEAD").decode().strip()
    if head != SOURCE_PIN:
        raise RuntimeError(f"Source commit mismatch: {head}; expected {SOURCE_PIN}. Do not checkout/update during Comparator.")
    unchanged(project)
    if (project / "lean-toolchain").read_text().strip() != TOOLCHAIN:
        raise RuntimeError("Unexpected project Lean toolchain")
    manifest = json.loads((project / "lake-manifest.json").read_text())
    pins = [p["rev"] for p in manifest["packages"] if p["name"] == "mathlib"]
    if pins != [MATHLIB_PIN]:
        raise RuntimeError(f"Unexpected Mathlib manifest pin: {pins}")
    mathlib = project / ".lake/packages/mathlib"
    actual_mathlib = git(mathlib, "rev-parse", "HEAD").decode().strip()
    if actual_mathlib != MATHLIB_PIN:
        raise RuntimeError(f"Mathlib checkout mismatch: {actual_mathlib}")
    def unchanged_mathlib():
        diff = git(mathlib, "diff", "--name-only", "HEAD", "--", "Mathlib",
                   "lean-toolchain", "lakefile.lean", "lake-manifest.json").decode().strip()
        if diff:
            raise RuntimeError("Tracked Mathlib inputs differ from HEAD:\n" + diff)
    unchanged_mathlib()

    tracked = {p for p in git(project, "ls-files", "-z", "--", "src").decode().split("\0")
               if p.endswith(".lean")}
    print(f"Pinned source and Mathlib verified. Scanning {len(tracked):,} tracked Lean files...", flush=True)
    counts, hits, rows = scan(project, tracked)
    mathlib_tracked = {p for p in git(mathlib, "ls-files", "-z", "--", "Mathlib").decode().split("\0")
                       if p.endswith(".lean")}
    print(f"Scanning {len(mathlib_tracked):,} tracked Mathlib files for the final statement definitions...", flush=True)
    ml_counts, ml_hits, ml_rows = scan(mathlib, mathlib_tracked, MATHLIB_TOKENS, "Mathlib")

    parent = out_parent.expanduser().resolve()
    if parent == project or project in parent.parents:
        raise RuntimeError("Output must be outside the proof checkout")
    parent.mkdir(parents=True, exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix="critics-", dir=parent))
    zip_path = out / "source-evidence.zip"
    meta = {"created": datetime.now().astimezone().isoformat(), "source_commit": head,
            "mathlib_commit": actual_mathlib, "lean_toolchain": TOOLCHAIN,
            "tracked_lean_sources": len(tracked), "search_hits_are_not_proof_dependencies": True,
            "mathlib_source_files_omitted_by_cap": [],
            "source_files_omitted_by_cap": [], "toolchain_source_missing": [], "sha256": {}}

    report = ["RH CRITIQUE: SOURCE EVIDENCE ONLY", "",
              "This report does NOT establish compiled proof-term reachability or logical invalidity.",
              "An import/text occurrence is not a theorem dependency. A dependency is not proof of necessity.",
              "The original checkout, build outputs, exports, and Comparator processes are unchanged.",
              "", f"Source: {head}", f"Mathlib: {actual_mathlib}", f"Lean: {TOOLCHAIN}",
              "", "Exact-token textual counts (comments and strings, if any, also count):",
              "token\toccurrences\tfiles"]
    report += [f"{t}\t{counts[t]}\t{len(hits[t])}" for t in TOKENS]

    selected = {p for p in tracked if Path(p).name in EXTRA_BASENAMES}
    selected.add("src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean")
    selected.intersection_update(tracked)
    required = set(selected)
    for token in TOKENS:
        selected.update(hits[token])

    copied = []
    budget = 32 * 1024 * 1024
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        def add(path, name, cap=4 * 1024 * 1024):
            if not path.is_file() or path.is_symlink() or path.stat().st_size > cap:
                return False
            data = path.read_bytes()
            z.writestr(name, data)
            meta["sha256"][name] = hashlib.sha256(data).hexdigest()
            return True

        for rel in sorted(selected, key=lambda p: (p not in required, p)):
            path = project / rel
            size = path.stat().st_size
            if path.is_symlink() or not path.resolve().is_relative_to(project):
                raise RuntimeError(f"Refusing linked source outside the checkout: {rel}")
            if len(copied) >= 800 or size > budget or size > 4 * 1024 * 1024:
                meta["source_files_omitted_by_cap"].append(rel)
                continue
            if add(path, "project/" + rel):
                copied.append(rel)
                budget -= size

        for rel in ("lean-toolchain", "lakefile.toml", "lake-manifest.json", "export-targets.txt", "comparator.json"):
            add(project / rel, "project/" + rel)
        ml_selected = set().union(*ml_hits.values())
        ml_budget = 8 * 1024 * 1024
        ml_copied = 0
        for rel in sorted(ml_selected):
            path = mathlib / rel
            size = path.stat().st_size
            if path.is_symlink() or not path.resolve().is_relative_to(mathlib.resolve()):
                raise RuntimeError(f"Refusing linked Mathlib source: {rel}")
            if ml_copied >= 300 or size > ml_budget or size > 4 * 1024 * 1024:
                meta["mathlib_source_files_omitted_by_cap"].append(rel)
                continue
            if add(path, "mathlib/" + rel):
                ml_copied += 1
                ml_budget -= size
        for rel in CORE_API:
            candidates = [toolchain / "src/lean" / rel, toolchain / "src" / rel]
            found = next((p for p in candidates if p.is_file()), None)
            if found is None or not add(found, "toolchain-source/" + rel):
                meta["toolchain_source_missing"].append(rel)
        for name in ("source-commit.txt", "compiled-headlines.sha256", "solution.export.sha256"):
            add(project.parent / "verification-data" / name, "verification-metadata/" + name)
        for rel in (".lake/build/lib/lean/Main.olean", ".lake/build/lib/lean/Statements.olean"):
            p = project / rel
            if p.is_file():
                meta["sha256"][rel] = digest(p)

        tsv = io.StringIO()
        writer = csv.writer(tsv, delimiter="\t", lineterminator="\n")
        writer.writerow(("file", "line", "tokens", "source_text"))
        writer.writerows(rows)
        z.writestr("source-hits.tsv", tsv.getvalue())
        ml_tsv = io.StringIO()
        ml_writer = csv.writer(ml_tsv, delimiter="\t", lineterminator="\n")
        ml_writer.writerow(("file", "line", "tokens", "source_text"))
        ml_writer.writerows(ml_rows)
        z.writestr("mathlib-hits.tsv", ml_tsv.getvalue())
        report += ["", "Key source locations (up to 4 lines per token):"]
        for token in TOKENS:
            relevant = [r for r in rows if token in r[2].split(",")][:4]
            report += [f"{r[0]}:{r[1]}: {r[3][:300]}" for r in relevant]
        report += ["", f"Full source files copied: {len(copied)}",
                   f"Mathlib source files copied: {ml_copied}",
                   f"Mathlib source files omitted by cap: {len(meta['mathlib_source_files_omitted_by_cap'])}",
                   f"Source files omitted by size/count cap: {len(meta['source_files_omitted_by_cap'])}",
                   "Missing Lean API source: " + (", ".join(meta["toolchain_source_missing"]) or "none"),
                   "", "Next: inspect exact declarations, then trace their types and proof bodies in the compiled environment.",
                   "No conclusion about Nielsen's or Chu's mathematical claims is implied by this collection."]
        unchanged(project)
        unchanged_mathlib()
        report_text = "\n".join(report) + "\n"
        z.writestr("report.txt", report_text)
        z.writestr("metadata.json", json.dumps(meta, indent=2) + "\n")
    (out / "report.txt").write_text(report_text)
    (out / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("\n".join(report[:12 + len(TOKENS)]))
    print(f"\nReport: {out / 'report.txt'}")
    print(f"Evidence ZIP: {zip_path}")
    print(f"ZIP size: {zip_path.stat().st_size:,} bytes")
    print(f"ZIP SHA-256: {digest(zip_path)}")
    print("SOURCE COLLECTION COMPLETED; no Lean verification was run by this collector.")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", type=Path, default=Path.home() / "rh-verification/riemann-hypothesis")
    ap.add_argument("--output", type=Path, default=Path.home() / "rh-verification/critics-audit")
    ap.add_argument("--toolchain", type=Path,
                    default=Path.home() / ".elan/toolchains/leanprover--lean4---v4.33.1")
    args = ap.parse_args()
    try:
        collect(args.project, args.output, args.toolchain.expanduser())
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
