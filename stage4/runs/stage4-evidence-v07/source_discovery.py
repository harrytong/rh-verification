"""Bounded literal search of the pinned Git tree, followed by verified copies.

This is source navigation, not a compiled dependency or necessity test.
No checkout edits, subprocess shell, or repository-supplied commands are used.
"""
from pathlib import Path
import subprocess
import runtime as rt

PATTERNS = ["structure DivInputs0R", "divClausesR_of", "DivInputs0R",
            "InpAtAlt", "ptK_of_real_alt", "DivisionPackageFace.ofOpen"]
PRIORITY = [
    "Formalism/LocalToGlobal/Divisibility/RecBridgeMkF.lean",
    "Formalism/LocalToGlobal/Divisibility/RecBridgeNum.lean",
    "Formalism/LocalToGlobal/Divisibility/ConstantGeTwentyEight.lean",
    "Formalism/LocalToGlobal/Divisibility/HeckeCSDICommTrRep.lean",
    "Formalism/LocalToGlobal/Divisibility/RecBridgeSel.lean",
    "Formalism/LocalToGlobal/PtKOfReal.lean",
    "Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/PtKOfReal.lean",
    "Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/DIVRecBridgeSel.lean",
]
MAX_FILES = 80


def paths_from_grep(data):
    prefix = (rt.SOURCE_PIN + ":src/").encode()
    paths = set()
    for entry in data.split(b"\0"):
        if not entry:
            continue
        if not entry.startswith(prefix):
            raise RuntimeError("Unexpected pinned Git grep path prefix")
        rel = entry[len(prefix):].decode("utf-8")
        p = Path(rel)
        if p.is_absolute() or ".." in p.parts:
            raise RuntimeError("Unsafe source-search path")
        if p.suffix == ".lean":
            paths.add(rel)
    return sorted(paths)


def collect(project, out):
    cmd = ["git", "--no-pager", "grep", "-l", "-z", "-F"]
    for pattern in PATTERNS:
        cmd += ["-e", pattern]
    cmd += [rt.SOURCE_PIN, "--", "src"]
    index = {"patterns": PATTERNS, "source_pin": rt.SOURCE_PIN,
             "meaning": "literal source matches only; no compiled-use or absence verdict",
             "limits": {"files": MAX_FILES, "total_bytes": 24*1024**2, "git_seconds": 180},
             "complete": False}
    try:
        result = subprocess.run(cmd, cwd=project, capture_output=True, timeout=180)
        if result.returncode not in (0, 1):
            raise RuntimeError("Git source discovery failed: " + result.stderr.decode(errors="replace")[:2000])
        if len(result.stdout) > 8*1024**2:
            raise RuntimeError("Git path-list output exceeds 8 MiB")
        matched = paths_from_grep(result.stdout)
        ordered = list(dict.fromkeys(PRIORITY + matched))
        chosen = ordered[:MAX_FILES]
        index.update(matched_files=matched, selected_files=chosen, omitted_files=ordered[MAX_FILES:],
                     file_selection_capped=len(ordered)>MAX_FILES)
        dest = out/"supplier-source"
        dest.mkdir()
        collection = rt.collect_sources(project, dest, {"roots": chosen, "import_depth": 0,
                    "max_files": MAX_FILES, "max_file_bytes": 2*1024**2, "max_total_bytes": 24*1024**2})
        index["collection"] = collection
        index["complete"] = not index["omitted_files"] and all(
            r.get("status") == "collected-and-git-verified" for r in collection["files"])
        hits = []
        for r in collection["files"]:
            if r.get("status") != "collected-and-git-verified":
                continue
            path = dest/r["evidence_path"]
            for number, line in enumerate(path.read_text().splitlines(), 1):
                found = [p for p in PATTERNS if p in line]
                if found:
                    hits.append({"source": r["source"], "line": number, "patterns": found,
                                 "text": line[:2000], "text_truncated": len(line)>2000})
                    if len(hits) >= 20000:
                        break
            if len(hits) >= 20000:
                break
        index["hits_capped"] = len(hits) >= 20000
        if index["hits_capped"]:
            index["complete"] = False
        rt.write_json(out/"supplier-source-hits.json", hits)
    except Exception as e:
        index["error"] = str(e)
    rt.write_json(out/"supplier-source-index.json", index)
    return index
