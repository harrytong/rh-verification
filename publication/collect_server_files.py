#!/usr/bin/env python3
"""Copy bounded audit evidence and log snapshots; never execute or alter a run."""
import argparse
import datetime as dt
import gzip
import hashlib
import json
import os
from pathlib import Path

MIB = 1024 * 1024
ALLOWED = {'.py', '.lean', '.md', '.txt', '.json', '.jsonl', '.log', '.tsv',
           '.csv', '.diff', '.patch', '.sha256', '.zip', '.yaml', '.yml', '.sh', '.cid'}
NAMES = {'SHA256SUMS', 'EVIDENCE_SHA256SUMS', 'lean-toolchain', 'LICENSE', 'NOTICE', 'vm.max_map_count.before'}
OMIT_DIRS = {'.git', '.lake', '__pycache__', 'node_modules'}

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(MIB), b''): h.update(block)
    return h.hexdigest()

def candidates(base):
    for name in ('critics-audit', 'critics-audit-stage2', 'critics-audit-stage3', 'critics-audit-stage4'):
        root = base / name
        if root.is_dir() and not root.is_symlink():
            for parent, dirs, files in os.walk(root, followlinks=False):
                dirs[:] = sorted(d for d in dirs if d not in OMIT_DIRS and not (Path(parent)/d).is_symlink())
                for name in sorted(files): yield Path(parent)/name
    root = base/'logs'
    if root.is_dir() and not root.is_symlink():
        for path in sorted(root.iterdir()):
            if path.is_file() and path.name.startswith(('main-build-', 'theorem-audit-', 'solution-export-', 'nanoda-', 'comparator-')):
                yield path
    root = base/'verification-data'
    if root.is_dir() and not root.is_symlink():
        for path in sorted(root.iterdir()):
            if path.is_file() and (path.suffix in {'.json', '.sha256'} or path.name == 'vm.max_map_count.before'):
                yield path
    root = base/'tools'
    if root.is_dir() and not root.is_symlink():
        for package in sorted(root.glob('rh-audit-stage*')):
            if not package.is_dir() or package.is_symlink(): continue
            for parent, dirs, files in os.walk(package, followlinks=False):
                dirs[:] = sorted(d for d in dirs if d not in OMIT_DIRS and not (Path(parent)/d).is_symlink())
                for name in sorted(files): yield Path(parent)/name

def copy_snapshot(source, target, initial_size, compress):
    """Copy at most the initial file size, so an appending log cannot grow unbounded."""
    target.parent.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha256(); copied = 0
    with source.open('rb') as src, target.open('wb') as raw:
        dest = gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) if compress else raw
        try:
            while copied < initial_size:
                data = src.read(min(MIB, initial_size-copied))
                if not data: break
                dest.write(data); h.update(data); copied += len(data)
        finally:
            if compress: dest.close()
    return copied, h.hexdigest()

def collect(base, repo, max_input_bytes=4*1024*MIB, max_file_bytes=80*MIB):
    base = base.resolve(); repo = repo.resolve()
    if not (repo/'publication').is_dir() or not (repo/'stage1').is_dir(): raise RuntimeError('Destination must contain the root-level publication payload.')
    if repo == base or base in repo.parents: raise RuntimeError('Use a publication checkout outside the verification directory.')
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = repo/'server-snapshots'/stamp
    if out.exists(): raise RuntimeError('Snapshot already exists; retry in a later second.')
    out.mkdir(parents=True)
    report = {'captured_utc': stamp, 'base': str(base),
              'interpretation': 'Additional server snapshots, not automatically reviewed; no new proof or Comparator verdict.',
              'files': [], 'skipped': [], 'missing_locations': [], 'errors': []}
    for name in ('logs','critics-audit','critics-audit-stage2','critics-audit-stage3','critics-audit-stage4','tools'):
        if not (base/name).is_dir(): report['missing_locations'].append(name)
    # Deduplicate against the reviewed archive and any previous snapshots.
    existing = {}
    for parent, dirs, files in os.walk(repo, followlinks=False):
        dirs[:] = [d for d in dirs if d not in OMIT_DIRS and (Path(parent)/d) != out and not (Path(parent)/d).is_symlink()]
        for name in files:
            p=Path(parent)/name
            if p.is_symlink(): continue
            existing.setdefault((p.stat().st_size, digest(p)), p.relative_to(repo).as_posix())
    total = 0
    try:
        for source in candidates(base):
            rel = source.relative_to(base).as_posix()
            if source.is_symlink():
                report['skipped'].append({'source':rel,'reason':'symlink'}); continue
            if source.suffix not in ALLOWED and source.name not in NAMES:
                report['skipped'].append({'source':rel,'reason':'not an audit text/archive format'}); continue
            before=source.stat(); total += before.st_size
            if total > max_input_bytes: raise RuntimeError('Input byte guard exceeded; nothing is silently declared complete.')
            compress = before.st_size > max_file_bytes
            if compress and source.suffix not in {'.log','.txt','.jsonl','.json','.tsv','.csv'}:
                report['skipped'].append({'source':rel,'reason':'file exceeds publication size guard'});continue
            dest=out/'files'/rel
            if compress:dest=dest.with_name(dest.name+'.gz')
            n,h=copy_snapshot(source,dest,before.st_size,compress)
            after=source.stat()
            key=(n,h)
            unchanged=(n==before.st_size and before.st_size==after.st_size and before.st_mtime_ns==after.st_mtime_ns)
            record={'source':rel,'initial_size':before.st_size,'copied_bytes':n,'uncompressed_sha256':h,
                    'source_unchanged_during_copy':unchanged,'snapshot_only':True}
            if key in existing:
                dest.unlink();record['existing_repo_path']=existing[key]
            else:
                if dest.stat().st_size > 90*MIB:
                    dest.unlink();report['skipped'].append({'source':rel,'reason':'stored snapshot exceeds 90 MiB; use a separate release asset'});continue
                record.update({'path':dest.relative_to(repo).as_posix(),'encoding':'gzip' if compress else 'identity',
                               'stored_sha256':digest(dest),'stored_bytes':dest.stat().st_size})
                if not compress:existing[key]=record['path']
            report['files'].append(record)
    except Exception as exc:
        report['errors'].append(str(exc))
        raise
    finally:
        (out/'COLLECTION_INDEX.json').write_text(json.dumps(report,indent=2)+'\n')
        (out/'README.md').write_text('# Additional server snapshot\n\nCaptured '+stamp+'. See COLLECTION_INDEX.json for hashes, source paths,\n'
            'deduplication references, exclusions and files changing during capture.\n'
            'These files are unreviewed additions. A Comparator log snapshot is not\n'
            'automatically a completed verification result. Source files were only read.\n')
    return report

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--base',type=Path,default=Path.home()/'rh-verification')
    args=ap.parse_args()
    r=collect(args.base,args.repo)
    print('Server files indexed:',len(r['files']))
    print('Skipped:',len(r['skipped']),'; missing locations:',', '.join(r['missing_locations']) or 'none')
    print('No running processes were controlled. See server-snapshots/.')

if __name__=='__main__':main()
