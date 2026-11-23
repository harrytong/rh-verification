"""Bounded execution utilities adapted from the previously exercised Stage 3 runner."""
from __future__ import annotations


import argparse


from datetime import datetime, timezone


import hashlib


import json


import os


import re


from pathlib import Path


import selectors


import shutil


import subprocess


import sys


import tempfile


import time


import zipfile


HERE = Path(__file__).resolve().parent


SOURCE_PIN = "753431bfe28701f6f3937f664fcaf08daa139c03"


MATHLIB_PIN = "0df444a360eaa60ab8c11dca51a86af692955474"


MAIN_SHA = "9146dfb4148e24d2252e04c50742f3e49dd126dfcc5006d10bf5f873ddf796ad"


STATEMENTS_SHA = "f8e0aed3c2d69390b6dd3bb24e13aa25e043a02ca42f021e3f6e4ec8b57fd6b1"


LEAN_SHA = "e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550"


GIB = 1024**3


LOG_LIMIT = 64 * 1024**2


def now():
    return datetime.now(timezone.utc).isoformat()


def sha256(p):
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def write_json(path, value):
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    temp.replace(path)


def command(argv, cwd=None):
    r = subprocess.run(argv, cwd=cwd, text=True, capture_output=True)
    if r.returncode:
        raise RuntimeError(f"Command failed ({r.returncode}): {argv}\n{r.stderr}")
    return r.stdout.strip()


def package_files():
    rows = []
    for line in (HERE / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        rel = Path(name)
        if rel.is_absolute() or ".." in rel.parts:
            raise RuntimeError("Unsafe package manifest path")
        if sha256(HERE / rel) != digest:
            raise RuntimeError(f"Package checksum mismatch: {name}")
        rows.append(rel)
    if not rows:
        raise RuntimeError("Empty package manifest")
    return rows


def validate(project, toolchain):
    """Read-only checks against prior evidence; no git checkout/reset/build."""
    if command(["git", "rev-parse", "HEAD"], project) != SOURCE_PIN:
        raise RuntimeError("Project revision differs from the audit baseline")
    if command(["git", "diff", "--name-only", "HEAD", "--", "src", "lean-toolchain",
                "lakefile.lean", "lakefile.toml", "lake-manifest.json"], project):
        raise RuntimeError("Tracked project inputs changed")
    if (project / "lean-toolchain").read_text().strip() != "leanprover/lean4:v4.33.1":
        raise RuntimeError("Unexpected proof toolchain")
    ml = project / ".lake/packages/mathlib"
    if command(["git", "rev-parse", "HEAD"], ml) != MATHLIB_PIN:
        raise RuntimeError("Mathlib revision differs from the audit baseline")
    if command(["git", "diff", "--name-only", "HEAD", "--", "Mathlib", "lean-toolchain",
                "lakefile.lean", "lake-manifest.json"], ml):
        raise RuntimeError("Tracked Mathlib inputs changed")
    manifest = json.loads((project / "lake-manifest.json").read_text())
    if [p.get("rev") for p in manifest["packages"] if p["name"] == "mathlib"] != [MATHLIB_PIN]:
        raise RuntimeError("Mathlib manifest pin changed")
    checks = [(project / ".lake/build/lib/lean/Main.olean", MAIN_SHA),
              (project / ".lake/build/lib/lean/Statements.olean", STATEMENTS_SHA),
              (toolchain / "bin/lean", LEAN_SHA)]
    source_rows = json.loads((HERE / "source-manifest.json").read_text())
    checks.extend((project / r["project_path"], r["sha256"]) for r in source_rows)
    for path, digest in checks:
        if sha256(path) != digest:
            raise RuntimeError(f"Input hash changed: {path}")
    return {str(p): digest for p, digest in checks}


def mem_available():
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) * 1024
    raise RuntimeError("Cannot read MemAvailable")


def collect_sources(project, out, cfg=None):
    """Bounded source context, validated against git HEAD; no project writes.

    Missing optional sources and caps are recorded, never silently treated as
    absence from a proof closure. This is not a dependency traversal.
    """
    if cfg is None:
        cfg = json.loads((HERE / "source-requests.json").read_text())
    queue = [(s, 0) for s in cfg["roots"]]
    seen, rows, total = set(), [], 0
    while queue:
        rel, depth = queue.pop(0)
        if rel in seen:
            continue
        seen.add(rel)
        p = Path(rel)
        if p.is_absolute() or ".." in p.parts or p.suffix != '.lean':
            raise RuntimeError("Unsafe requested source path")
        row = {"source": 'src/'+rel, "import_depth": depth}
        rows.append(row)
        if len(rows) > cfg['max_files']:
            row['status'] = 'file-count-cap'
            continue
        source = project/'src'/p
        if not source.is_file():
            row['status'] = 'not-found-at-requested-path'
            continue
        if not source.resolve().is_relative_to((project/'src').resolve()):
            raise RuntimeError("Source resolves outside the project src tree")
        if source.stat().st_size > cfg['max_file_bytes']:
            row['status'] = 'file-size-cap'
            continue
        data = source.read_bytes()
        if total + len(data) > cfg['max_total_bytes']:
            row['status'] = 'total-size-cap'
            continue
        tracked = subprocess.run(['git','show',SOURCE_PIN+':src/'+rel], cwd=project,
                                 capture_output=True, timeout=30)
        if tracked.returncode or tracked.stdout != data:
            raise RuntimeError(f"Source differs from pinned git contents: {rel}")
        dest = out/'collected-source'/p
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        total += len(data)
        row.update(status='collected-and-git-verified', bytes=len(data),
                   sha256=hashlib.sha256(data).hexdigest(), evidence_path=str(dest.relative_to(out)))
        if depth < cfg['import_depth']:
            for module in re.findall(r'^import\s+([A-Za-z0-9_\.\u0080-\uffff]+)\s*$', data.decode('utf-8'), re.M):
                if module.startswith(('Development.', 'Formalism.', 'ReciprocityTheory.', 'GroundTheory.', 'CompanionTheory.')):
                    queue.append((module.replace('.', '/')+'.lean', depth+1))
    result = {"meaning": "bounded source context, not a proof closure or use census",
              "configuration": cfg, "total_bytes": total, "files": rows}
    write_json(out/'collected-source-index.json', result)
    return result


def first_error(text):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.search(r'\.lean:\d+:\d+: error', line):
            return {"classification": "unclassified; manual review required",
                    "excerpt": '\n'.join(lines[i:i+35])}
    return None


def check_resources(out, memory_gib, project_phase):
    free = shutil.disk_usage(out).free
    if free < 21 * GIB:
        raise RuntimeError("Less than 21 GiB disk free: keep 20 GiB reserve plus output allowance")
    available = mem_available()
    if project_phase and available < (memory_gib + 16) * GIB:
        raise RuntimeError("Insufficient available RAM for the configured audit limit plus 16 GiB reserve; leave Comparator untouched")
    return {"disk_free_bytes": free, "mem_available_bytes": available}


def new_output(root, project):
    root = root.expanduser().resolve()
    if root == project or project in root.parents or root in project.parents:
        raise RuntimeError("Output must be outside the proof checkout and its ancestors")
    root.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix="stage4-", dir=root))


def docker_command(project, toolchain, out, image, cidfile, filename, seconds, memory_gib, smoke):
    # The fixture has no project mount or project search path.
    paths = [] if smoke else sorted((project / ".lake/packages").glob("*/.lake/build/lib/lean")) + [project / ".lake/build/lib/lean"]
    if any(":" in str(p) or "," in str(p) for p in [project, toolchain, out]):
        raise RuntimeError("Paths containing commas/colons are not supported by this mount/search-path builder")
    args = ["sudo", "-n", "docker", "run", "--rm", "--cidfile", str(cidfile),
            "--name", "rh-audit-" + out.name + "-" + filename.removesuffix(".lean").lower(),
            "--network", "none", "--log-driver=none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges:true", "--user", f"{os.getuid()}:{os.getgid()}",
            "--cpus=2", f"--memory={memory_gib}g", f"--memory-swap={memory_gib}g",
            "--pids-limit=256", "--ulimit", "core=0",
            "--tmpfs", "/tmp:rw,nosuid,nodev,size=1g,mode=1777",
            "--mount", f"type=bind,src={toolchain},dst=/opt/lean,readonly",
            "--mount", f"type=bind,src={out},dst=/audit,readonly",
            "--workdir", "/audit", "--env", "PATH=/opt/lean/bin:/usr/bin:/bin",
            "--env", "LEAN_NUM_THREADS=2", "--env", "LEAN_ABORT_ON_PANIC=1",
            "--env", "LAKE_ARTIFACT_CACHE=false", "--env", "LEAN_PATH=" + ":".join(map(str, paths))]
    if not smoke:
        args += ["--mount", f"type=bind,src={project},dst={project},readonly"]
    args += [image, "/usr/bin/timeout", "--signal=TERM", "--kill-after=10s", str(seconds),
             "/usr/bin/time", "-v", "/opt/lean/bin/lean", "--tstack=400000", "/audit/" + filename]
    return args


def stop_owned(cidfile):
    # No name matching, pkill, Comparator inspection, or process-wide cleanup.
    if cidfile.is_file():
        cid = cidfile.read_text().strip()
        if len(cid) == 64 and all(c in "0123456789abcdef" for c in cid):
            subprocess.run(["sudo", "-n", "docker", "stop", "--time", "5", cid],
                           capture_output=True, timeout=15)


def run_logged(argv, logfile, cidfile, seconds):
    start = time.monotonic()
    size = 0
    last = start
    guard = None
    with logfile.open("wb") as log:
        log.write(("START_UTC " + now() + "\nCOMMAND_JSON " + json.dumps(argv) + "\n").encode())
        log.flush()
        proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        sel = selectors.DefaultSelector()
        sel.register(proc.stdout, selectors.EVENT_READ)
        try:
            while sel.get_map():
                for key, _ in sel.select(timeout=1):
                    data = os.read(key.fileobj.fileno(), 65536)
                    if not data:
                        sel.unregister(key.fileobj)
                        break
                    size += len(data)
                    if size > LOG_LIMIT:
                        guard = "output-limit"
                        raise RuntimeError("64 MiB output limit reached; incomplete evidence retained")
                    log.write(data)
                    log.flush()
                    # Full terms remain in the log, rather than flooding the terminal.
                elapsed = time.monotonic() - start
                if elapsed > seconds + 60:
                    guard = "host-wall-clock-limit"
                    raise RuntimeError("Host wall-clock guard reached; incomplete evidence retained")
                if time.monotonic() - last >= 60:
                    print(f"STAGE4_PROGRESS {logfile.stem}: {elapsed:.0f}s; {size:,} log bytes", flush=True)
                    check_resources(logfile.parent, 0, False)
                    last = time.monotonic()
            rc = proc.wait(timeout=15)
        except BaseException:
            stop_owned(cidfile)
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
            log.write((f"\nGUARD_OR_INTERRUPTION {guard or 'resource/error/interrupt'}\n").encode())
            raise
        finally:
            sel.close()
            proc.stdout.close()
        log.write(f"\nPROCESS_EXIT_STATUS {rc}\nEND_UTC {now()}\n".encode())
    return rc, logfile.read_text(errors="replace")


def validate_result(kind, rc, text, markers):
    if kind == "negative":
        # A startup, OOM or timeout error must not be accepted as the negative fixture.
        if rc != 1 or "NegativeFixture.lean:" not in text or "error:" not in text or "Type mismatch" not in text:
            raise RuntimeError("Negative fixture did not fail with the expected Lean type mismatch")
        return
    if rc != 0:
        raise RuntimeError(f"{kind} exited {rc}; inspect its log (124 indicates the time guard)")
    if any(m not in text for m in markers):
        raise RuntimeError(f"{kind}: required evidence markers missing")
    if "sorryAx" in text or "declaration uses `sorry`" in text:
        raise RuntimeError(f"{kind}: unexpected sorry dependency; do not call the probe successful")


def archive(out):
    paths = sorted(p for p in out.rglob("*") if p.is_file() and p.name not in {"stage4-evidence.zip", "EVIDENCE_SHA256SUMS"})
    (out / "EVIDENCE_SHA256SUMS").write_text("".join(f"{sha256(p)}  {p.relative_to(out)}\n" for p in paths))
    with zipfile.ZipFile(out / "stage4-evidence.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for p in paths + [out / "EVIDENCE_SHA256SUMS"]:
            z.write(p, p.relative_to(out))
    return out / "stage4-evidence.zip"
