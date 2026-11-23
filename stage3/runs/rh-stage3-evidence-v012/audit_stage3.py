#!/usr/bin/env python3
"""Stage 3 v0.12 integral identity and theta realization. Python 3.10+.

No source mutation, rebuild, export copy, full census, or Comparator control.
See README.md and INTEGRAL_PROTOCOL.md for this increment's scope.
"""
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
RECORDS = {
    "integral": ("ThetaIntegral.lean", ["RH_STAGE3_INTEGRAL_END"]),
    "descent": ("ThetaDescent.lean", ["RH_STAGE3_DESCENT_END"]),
    "character": ("CharacterConstruction.lean", ["RH_STAGE3_CHARACTER_END"]),
    "theta": ("ThetaIdentity.lean", ["RH_STAGE3_THETA_END"]),
    "construction": ("Construction.lean", ["RH_STAGE3_CONSTRUCTION_END"]),
    "extensions": ("Extensions.lean", ["RH_STAGE3_EXTENSIONS_END"]),
    "providers": ("Providers.lean", ["RH_STAGE3_PROVIDERS_END"]),
    "uses": ("ArgumentUses.lean", ["RH_STAGE3_ARGUMENT_USES_END"]),
    "consumers": ("ConsumerImplementations.lean", ["RH_STAGE3_CONSUMER_IMPLEMENTATIONS_END"]),
    "domains": ("DomainBoundary.lean", ["RH_STAGE3_DOMAIN_BOUNDARIES_END"]),
    "witness-chain": ("WitnessChain.lean", ["RH_STAGE3_WITNESS_CHAIN_END"]),
    "height-chain": ("HeightChain.lean", ["RH_STAGE3_HEIGHT_CHAIN_END"]),
    "boundary": ("HeightBoundary.lean", ["RH_STAGE3_HEIGHT_BOUNDARY_THEOREMS_ACCEPTED", "RH_STAGE3_HEIGHT_BOUNDARY_END"]),
    "suppliers": ("SupplierDetails.lean", ["RH_STAGE3_SUPPLIERS_END"]),
    "geometry-general": ("GeometryGeneral.lean", ["RH_STAGE3_SUPPLIER_BASELINE_ACCEPTED", "RH_STAGE3_ARBITRARY_SUPPLIER_ACCEPTED", "RH_STAGE3_GENERAL_SUPPLIER_END"]),
    "geometry": ("GeometryContext.lean", [
        "RH_STAGE3_CONTEXT G1_BEFORE_MONOTONICITY",
        "RH_STAGE3_CONTEXT G2_AFTER_MONOTONICITY",
        "RH_STAGE3_CONTEXT G3_AFTER_OPEN_PACKAGE",
        "RH_STAGE3_CONTEXT G4_AFTER_FUNCTIONAL",
        "RH_STAGE3_CONTEXT G5_BEFORE_FINAL_CONSUMER",
        "RH_STAGE3_GEOMETRY_END", "RH_STAGE3_GEOMETRY_DECLARATIONS_END"]),
    "height": ("HeightContext.lean", [
        "RH_STAGE3_CONTEXT H1_ASSIGNED_HEIGHT",
        "RH_STAGE3_CONTEXT H2_CONSTRUCTED_CONTRACT", "RH_STAGE3_HEIGHT_END"]),
}

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


def provenance_records(text):
    prefix = 'RH_STAGE3_PROVENANCE_JSON\t'
    rows = []
    for line in text.splitlines():
        if line.startswith(prefix):
            try:
                row = json.loads(line[len(prefix):])
            except (ValueError, TypeError) as e:
                raise RuntimeError('Malformed provenance JSON') from e
            if not isinstance(row, dict) or row.get('event') not in {'target', 'references'}:
                raise RuntimeError('Unexpected provenance record')
            if row['event'] == 'references':
                refs = row.get('references')
                if (not isinstance(refs, list) or row.get('retained') != len(refs)
                    or any(type(row.get(k)) is not int or row[k] < 0 for k in ['total','retained','limit'])
                    or row['retained'] != min(row['total'], row['limit'])
                    or type(row.get('truncated')) is not bool
                    or row['truncated'] != (row['total'] > row['limit'])
                    or row.get('location') not in {'type','body'}
                    or any(not isinstance(r,dict) or not isinstance(r.get('name'),str)
                           or not isinstance(r.get('module'),str) or type(r.get('found')) is not bool
                           for r in refs)):
                    raise RuntimeError('Inconsistent provenance reference counts/schema')
            elif (not isinstance(row.get('module'),str) or not isinstance(row.get('kind'),str)
                  or type(row.get('has_body')) is not bool):
                raise RuntimeError('Invalid target metadata')
            if not isinstance(row.get('target'),str):
                raise RuntimeError('Invalid target name')
            rows.append(row)
    if not rows:
        raise RuntimeError('No provenance records')
    return rows

def validate_provenance_fixture(text):
    rows = provenance_records(text)
    def refs(target, location, limit):
        found = [r for r in rows if r['event']=='references' and r['target']==target
                 and r['location']==location and r['limit']==limit]
        if len(found)!=1:
            raise RuntimeError('Fixture reference record missing or duplicated')
        return found[0]
    wrapper='RHStage3ProvenanceFixture.wrapper'
    body=refs(wrapper,'body',4096)
    if 'RHStage3ProvenanceFixture.bodyOnly' not in [r['name'] for r in body['references']]:
        raise RuntimeError('Fixture lost the definition-body reference')
    if 'Nat' not in [r['name'] for r in refs(wrapper,'type',4096)['references']]:
        raise RuntimeError('Fixture lost the type reference')
    if any(r['name']=='RHStage3ProvenanceFixture.unused' for row in rows
           if row['event']=='references' for r in row['references']):
        raise RuntimeError('Fixture included the unreferenced definition')
    cap=refs(wrapper,'body',0)
    if not cap['truncated'] or cap['retained']!=0:
        raise RuntimeError('Fixture did not expose the intentional reference cap')
    imported=[r for r in rows if r['event']=='target' and r['target']=='Nat.add']
    if len(imported)!=1 or imported[0]['module'].startswith('<'):
        raise RuntimeError('Fixture failed imported-module provenance lookup')
    theorem=[r for r in rows if r['event']=='target' and r['target']=='RHStage3ProvenanceFixture.witnessed']
    if len(theorem)!=1 or theorem[0]['kind']!='theorem' or not theorem[0]['has_body']:
        raise RuntimeError('Fixture failed theorem-body recognition')
    refs('RHStage3ProvenanceFixture.witnessed','body',4096)
    return {'checks':['definition body reference','type reference','unused definition excluded',
                      'cap is explicit','imported module provenance','theorem body available'],
            'meaning':'tool fixture only; no RH statement or necessity check'}

def validate_provenance(text, expected, limit):
    rows=provenance_records(text)
    target_rows=[r for r in rows if r['event']=='target']
    if [r['target'] for r in target_rows] != expected:
        raise RuntimeError('Target provenance is missing, duplicated, extra or out of order')
    if any(r['target'] not in expected for r in rows):
        raise RuntimeError('Unexpected reference target')
    for target in target_rows:
        rr=[r for r in rows if r['event']=='references' and r['target']==target['target']]
        if [r['location'] for r in rr] != (['type','body'] if target['has_body'] else ['type']):
            raise RuntimeError('Missing or duplicate type/body reference record')
        if any(r['limit']!=limit for r in rr):
            raise RuntimeError('Reference budget differs from preregistered value')
    return {'method':'getUsedConstants on stored types and optional bodies; no unfolding',
            'not_established':['argument use','witness discharge','semantic necessity','absence from transitive closure'],
            'any_reference_truncated':any(r.get('truncated',False) for r in rows),
            'records':rows}

USE_FIXTURE_CASES = ['direct','absent','shadowed','outer-under-lambda',
    'binder-domain-only','forall-domain-and-body','let-type-value-body',
    'projection','annotation-inherited','metadata','node-cap','depth-cap']

def use_records(text):
    prefix='RH_STAGE3_USES_JSON\t'
    rows=[]
    for line in text.splitlines():
        if line.startswith(prefix):
            try:
                row=json.loads(line[len(prefix):])
            except (ValueError,TypeError) as e:
                raise RuntimeError('Malformed argument occurrence JSON') from e
            if not isinstance(row,dict) or row.get('event') not in {'binder','end','fixture'}:
                raise RuntimeError('Invalid occurrence event')
            if row['event']=='fixture':
                if not isinstance(row.get('case'),str) or row.get('passed') is not True:
                    raise RuntimeError('Invalid occurrence fixture result')
            else:
                if not isinstance(row.get('target'),str):
                    raise RuntimeError('Invalid occurrence target')
                if row['event']=='binder':
                    for key in ['ordinal','binder_or_let_type_position','other_expression_position',
                                'nodes_visited','node_limit','depth_limit']:
                        if type(row.get(key)) is not int or row[key]<0:
                            raise RuntimeError('Invalid occurrence counter')
                    if (not isinstance(row.get('name'),str) or type(row.get('truncated')) is not bool
                        or row['nodes_visited']>row['node_limit']
                        or row['binder_or_let_type_position']+row['other_expression_position']>row['nodes_visited']):
                        raise RuntimeError('Inconsistent occurrence counts')
                elif (type(row.get('binder_count')) is not int or row['binder_count']<0
                      or row.get('stop') not in {'non-lambda-head','outer-step-cap','binder-cap'}):
                    raise RuntimeError('Invalid occurrence end record')
            rows.append(row)
    if not rows:
        raise RuntimeError('No occurrence records')
    return rows

def validate_uses(text, expected, cfg):
    rows=use_records(text)
    if any(r['event']=='fixture' for r in rows):
        raise RuntimeError('Fixture records in project output')
    at=0
    for target in expected:
        ordinal=0
        while at<len(rows) and rows[at]['event']=='binder':
            r=rows[at]
            if (r['target']!=target or r['ordinal']!=ordinal
                or ordinal>=cfg['max_binders']
                or r['node_limit']!=cfg['node_limit_per_binder']
                or r['depth_limit']!=cfg['depth_limit']):
                raise RuntimeError('Occurrence binder order or budget mismatch')
            ordinal+=1;at+=1
        if at>=len(rows):
            raise RuntimeError('Missing occurrence terminator')
        r=rows[at]
        if r['event']!='end' or r['target']!=target or r['binder_count']!=ordinal:
            raise RuntimeError('Occurrence terminator mismatch')
        if r['stop']=='binder-cap' and ordinal!=cfg['max_binders']:
            raise RuntimeError('Invalid binder cap')
        at+=1
    if at!=len(rows):
        raise RuntimeError('Extra or reordered occurrence records')
    return {'method':'bounded syntactic de Bruijn occurrence count in each explicit outer lambda remainder',
      'position_labels':['binder_or_let_type_position','other_expression_position'],
      'not_established':['hypothesis discharge','semantic necessity','computational relevance',
                         'all binders exposed','reduction-normalized use','headline validity'],
      'any_occurrence_truncated':any(r.get('truncated',False) or r.get('stop') in {'binder-cap','outer-step-cap'} for r in rows),
      'records':rows}

def validate_use_fixture(text):
    rows=use_records(text)
    cases=[r['case'] for r in rows if r['event']=='fixture']
    if cases!=USE_FIXTURE_CASES:
        raise RuntimeError('Occurrence fixture cases missing, duplicated or reordered')
    ordinary=[r for r in rows if r.get('target')=='RHStage3UsesFixture.identity']
    rendered='\n'.join('RH_STAGE3_USES_JSON\t'+json.dumps(r) for r in ordinary)
    cfg=dict(max_binders=128,node_limit_per_binder=100000,depth_limit=600)
    validated=validate_uses(rendered,['RHStage3UsesFixture.identity'],cfg)
    binders=[r for r in ordinary if r['event']=='binder']
    if (len(binders)!=1 or binders[0]['other_expression_position']!=1
        or binders[0]['binder_or_let_type_position']!=0 or validated['any_occurrence_truncated']):
        raise RuntimeError('Stored theorem identity occurrence fixture failed')
    caps=[r for r in rows if r.get('target') in {'synthetic-outer-cap','synthetic-binder-cap'}]
    if caps!=[dict(event='end',target='synthetic-outer-cap',binder_count=0,stop='outer-step-cap'),
              dict(event='end',target='synthetic-binder-cap',binder_count=128,stop='binder-cap')]:
        raise RuntimeError('Outer occurrence cap fixture failed')
    if len(rows)!=len(cases)+len(ordinary)+len(caps):
        raise RuntimeError('Unexpected occurrence fixture output')
    return {'checks':cases+['stored theorem binder','outer-step cap','binder cap'],
            'meaning':'tool fixture only; synthetic AST cases are not mathematical proofs'}


SEARCH_CASES=['direct','absent','shadowed','outer-binder','annotation-omitted',
              'let-value','projection','metadata','capped','depth-cap-before-hit','application-context','function-context']
def search_records(text):
    rows=[]
    for line in text.splitlines():
        if not line.startswith('RH_STAGE3_SEARCH_JSON\t'):continue
        try: r=json.loads(line.split('\t',1)[1])
        except (ValueError,TypeError) as e:raise RuntimeError('Invalid search JSON') from e
        if not isinstance(r,dict) or r.get('event') not in {'search','fixture'}:
            raise RuntimeError('Invalid search event')
        if r['event']=='fixture':
            if not isinstance(r.get('case'),str) or r.get('passed') is not True:
                raise RuntimeError('Invalid search fixture')
        else:
            for key in ['target','binder','path']:
                if not isinstance(r.get(key),str):raise RuntimeError('Invalid search text field')
            for key in ['ordinal','visited','node_limit','depth_limit','omitted_annotation_roots']:
                if type(r.get(key)) is not int or r[key]<0:raise RuntimeError('Invalid search counter')
            if (type(r.get('truncated')) is not bool or r['node_limit']!=100000 or r['depth_limit']!=600
                or r['ordinal']>=256 or r['visited']>100000
                or r['omitted_annotation_roots']>r['visited']
                or r.get('status') not in {'found','not-found-in-projection'}
                or (r['status']=='found') != bool(r['path'])):
                raise RuntimeError('Inconsistent search result or budget')
            ctx=r.get('application')
            if ctx is not None:
                if r['status']!='found' or not isinstance(ctx,dict):raise RuntimeError('Invalid search application')
                f=ctx.get('function')
                if (not isinstance(ctx.get('application_path'),str)
                    or ctx.get('occurrence_branch') not in {'argument','function'}
                    or type(ctx.get('selected_child_is_bvar')) is not bool
                    or not isinstance(f,dict) or f.get('head_kind') not in {'constant','bound-variable','projection','lambda','other'}
                    or not isinstance(f.get('head'),str)
                    or type(f.get('preceding_arguments')) is not int or not 0<=f['preceding_arguments']<=1024
                    or type(f.get('spine_truncated')) is not bool):
                    raise RuntimeError('Invalid application context schema')
        rows.append(r)
    if not rows:raise RuntimeError('No search records')
    return rows

def validate_searches(text,expected):
    rows=search_records(text)
    if any(r['event']!='search' for r in rows):raise RuntimeError('Fixture in project search')
    if [dict(target=r['target'],binder=r['binder']) for r in rows]!=expected:
        raise RuntimeError('Search targets missing, duplicated or reordered')
    return {'method':'bounded argument-first first occurrence in annotation-omitting projection',
        'not_established':['full-body absence','necessity','hypothesis discharge','headline validity'],
        'any_search_truncated':any(r['truncated'] for r in rows),
        'records':rows}

def validate_search_fixture(text):
    rows=search_records(text)
    if [r['case'] for r in rows if r['event']=='fixture']!=SEARCH_CASES:
        raise RuntimeError('Missing/duplicate/reordered search fixture')
    hits=[r for r in rows if r['event']=='search']
    if len(hits)!=1:raise RuntimeError('Invalid stored theorem search fixture')
    r=hits[0]
    if (r['target']!='RHStage3SearchFixture.identity' or r['binder']!='h' or r['ordinal']!=0
        or r['status']!='found' or r['path']!='root' or r['application'] is not None
        or r['visited']!=1 or r['omitted_annotation_roots']!=0 or r['truncated']):
        raise RuntimeError('Stored theorem search fixture failed')
    return {'checks':SEARCH_CASES+['stored theorem binder lookup'],
            'meaning':'tool fixture only; no RH or necessity verdict'}


def collect_provenance_sources(project,out,result,cfg):
    # Prefer target owners, then directly referenced project modules in lexical order.
    # Non-project refs stay in provenance evidence; this collector never guesses
    # that a module missing from src is Mathlib or that its proof is irrelevant.
    prefixes=('Development.','Formalism.','ReciprocityTheory.','GroundTheory.','CompanionTheory.')
    roots=[r['module'] for r in result['records'] if r['event']=='target']
    refs=sorted({r['module'] for row in result['records'] if row['event']=='references'
                 for r in row['references']})
    fragments=cfg.get('priority_module_fragments',[])
    prioritized=[m for m in refs if any(fragment in m for fragment in fragments)]
    mode=cfg.get('source_reference_mode','all')
    if mode not in {'all','priority-only'}:
        raise RuntimeError('Unknown source reference selection mode')
    selected_refs=refs if mode=='all' else prioritized
    eligible=[]; skipped=[]
    for module in dict.fromkeys(roots+prioritized+selected_refs):
        if not module.startswith(prefixes):
            skipped.append({'module':module,'reason':'outside configured project module prefixes'})
            continue
        if not re.fullmatch(r'[A-Za-z0-9_\u0080-\uffff]+(?:\.[A-Za-z0-9_\u0080-\uffff]+)*',module):
            raise RuntimeError('Unsafe module-to-source mapping')
        eligible.append(module.replace('.','/')+'.lean')
    # Configure the existing git-verified collector without replacing package inputs.
    owner_paths=[m.replace('.', '/')+'.lean' for m in roots if m.startswith(prefixes)]
    extra_roots=cfg.get('priority_source_roots',[])
    ordered=list(dict.fromkeys(owner_paths+extra_roots+eligible))
    source_cfg=dict(roots=ordered,import_depth=cfg['source_import_depth'],
                    max_files=cfg['max_source_files'],max_file_bytes=cfg['max_source_file_bytes'],
                    max_total_bytes=cfg['max_source_total_bytes'])
    collected=collect_sources(project,out,source_cfg)
    collected['selection']={'target_module_priority':roots,'direct_reference_modules_lexical':refs,
                            'priority_module_fragments':fragments,'prioritized_reference_modules':prioritized,
                            'explicit_priority_source_roots':extra_roots,
                            'source_reference_mode':mode,
                            'reference_modules_not_seeded':[m for m in refs if m not in roots+selected_refs],
                            'skipped_modules':skipped,
                            'reference_lists_truncated':result['any_reference_truncated']}
    write_json(out/'collected-source-index.json',collected)
    return collected


def construction_source_hits(out, collected):
    """Lexical navigation only; never a call graph or argument-use classification."""
    patterns = {
        'record-type-or-constructor': r'\bRealExpansionExtraData(?:\.mk)?\b',
        'theta-obligation': r'\bEMtTheta\b',
        'th-field-assignment': r'\bth\s*:=',
        'finiteness-supplier': r'\bsFin_and_sFinl_of_archCmp_sEta_thetaData\b',
    }
    rows=[];limit=2000;truncated=False
    for entry in collected['files']:
        if entry['status']!='collected-and-git-verified':continue
        rel=Path(entry['evidence_path'])
        if rel.is_absolute() or '..' in rel.parts or not (out/rel).resolve().is_relative_to(out.resolve()):
            raise RuntimeError('Unsafe collected source evidence path')
        for line_no,line in enumerate((out/rel).read_text().splitlines(),1):
            labels=[label for label,pattern in patterns.items() if re.search(pattern,line)]
            if labels:
                if len(rows)>=limit:
                    truncated=True
                    continue
                rows.append(dict(file=str(rel),line=line_no,labels=labels,text=line[:1000],
                                 text_truncated=len(line)>1000,source_sha256=entry['sha256']))
    return dict(method='lexical source navigation, comments included; not proof-use evidence',
                patterns=patterns,limit=limit,truncated=truncated,records=rows,
                scope='only collected source files; absent matches are not absence from the proof')


def declaration_blocks(text, expected):
    """Index printed targets without claiming complete expressions or necessity."""
    lines = text.splitlines(keepends=True)
    begins, ends = {}, {}
    for i, line in enumerate(lines):
        for prefix, positions in [("RH_STAGE3_DECL_BEGIN ", begins), ("RH_STAGE3_DECL_END ", ends)]:
            if line.strip().startswith(prefix):
                name = line.strip()[len(prefix):]
                positions.setdefault(name, []).append(i)
    rows, previous_end = [], -1
    for name in expected:
        start, finish = begins.get(name, []), ends.get(name, [])
        if len(start) != 1 or len(finish) != 1 or not previous_end < start[0] < finish[0]:
            raise RuntimeError(f"Missing, duplicate, or out-of-order declaration block: {name}")
        body = ''.join(lines[start[0]+1:finish[0]])
        if not body.strip():
            raise RuntimeError(f"Empty declaration block: {name}")
        rows.append({"declaration": name, "begin_line": start[0]+1,
                     "end_line": finish[0]+1,
                     "rendered_block_sha256": hashlib.sha256(body.encode()).hexdigest(),
                     "rendered_block_utf8_bytes": len(body.encode()),
                     "elision_indicators": {s: body.count(s) for s in ['⋯', '…'] if s in body},
                     "rendering_completeness": "not certified, even when no elision indicator is detected"})
        previous_end = finish[0]
    return {"meaning": "index of compiler-rendered declarations and axiom output; not a raw term export",
            "blocks": rows}

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
    return Path(tempfile.mkdtemp(prefix="stage3-", dir=root))

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
                    print(f"STAGE3_PROGRESS {logfile.stem}: {elapsed:.0f}s; {size:,} log bytes", flush=True)
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
    paths = sorted(p for p in out.rglob("*") if p.is_file() and p.name not in {"stage3-evidence.zip", "EVIDENCE_SHA256SUMS"})
    (out / "EVIDENCE_SHA256SUMS").write_text("".join(f"{sha256(p)}  {p.relative_to(out)}\n" for p in paths))
    with zipfile.ZipFile(out / "stage3-evidence.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for p in paths + [out / "EVIDENCE_SHA256SUMS"]:
            z.write(p, p.relative_to(out))
    return out / "stage3-evidence.zip"

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--phase", choices=["smoke", "inspect", "geometry", "height", "followup", "boundary", "suppliers", "geometry-general", "obligations", "domains", "witness-chain", "height-chain", "consumers", "provenance-smoke", "uses", "use-smoke", "providers", "search-smoke", "extensions", "construction", "theta", "character", "descent", "integral"], default="smoke")
    ap.add_argument("--project", type=Path, default=Path.home()/"rh-verification/riemann-hypothesis")
    ap.add_argument("--toolchain", type=Path, default=Path.home()/".elan/toolchains/leanprover--lean4---v4.33.1")
    ap.add_argument("--output", type=Path, default=Path.home()/"rh-verification/critics-audit-stage3")
    ap.add_argument("--memory-gib", type=int, default=100)
    ap.add_argument("--probe-seconds", type=int, default=1800)
    args = ap.parse_args()
    if not 64 <= args.memory_gib <= 100 or not 120 <= args.probe_seconds <= 7200:
        ap.error("memory must be 64..100 GiB; probe-seconds must be 120..7200")
    files = package_files()
    project = args.project.expanduser().resolve(strict=True)
    toolchain = args.toolchain.expanduser().resolve(strict=True)
    hashes = validate(project, toolchain)
    out = new_output(args.output, project)
    for p in files + [Path("SHA256SUMS")]:
        dest = out / p
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(HERE/p, dest)
    meta = {"started_utc": now(), "method_version": "stage3-targeted-0.12", "phase": args.phase,
            "integral_protocol_sha256": sha256(HERE/"INTEGRAL_PROTOCOL.md"),
            "integral_targets_sha256": sha256(HERE/"integral-targets.json"),
            "descent_protocol_sha256": sha256(HERE/"DESCENT_PROTOCOL.md"),
            "descent_targets_sha256": sha256(HERE/"descent-targets.json"),
            "character_protocol_sha256": sha256(HERE/"CHARACTER_PROTOCOL.md"),
            "character_targets_sha256": sha256(HERE/"character-targets.json"),
            "theta_protocol_sha256": sha256(HERE/"THETA_PROTOCOL.md"),
            "theta_targets_sha256": sha256(HERE/"theta-targets.json"),
            "construction_protocol_sha256": sha256(HERE/"CONSTRUCTION_PROTOCOL.md"),
            "construction_targets_sha256": sha256(HERE/"construction-targets.json"),
            "extension_protocol_sha256": sha256(HERE/"EXTENSION_PROTOCOL.md"),
            "extension_targets_sha256": sha256(HERE/"extension-targets.json"),
            "provider_protocol_sha256": sha256(HERE/"PROVIDER_PROTOCOL.md"),
            "provider_targets_sha256": sha256(HERE/"provider-targets.json"),
            "use_protocol_sha256": sha256(HERE/"USE_PROTOCOL.md"),
            "use_targets_sha256": sha256(HERE/"use-targets.json"),
            "consumer_protocol_sha256": sha256(HERE/"CONSUMER_PROTOCOL.md"),
            "provenance_targets_sha256": sha256(HERE/"provenance-targets.json"),
            "domain_protocol_sha256": sha256(HERE/'DOMAIN_PROTOCOL.md'),
            "chain_targets_sha256": sha256(HERE/'chain-targets.json'),
            "followup_protocol_sha256": sha256(HERE/'FOLLOWUP_PROTOCOL.md'),
            "package_manifest_sha256": sha256(HERE/'SHA256SUMS'),
            "input_hashes_before": hashes, "source_pin": SOURCE_PIN, "mathlib_pin": MATHLIB_PIN,
            "phase_completed": False, "steps": [], "comparator": "not inspected or controlled",
            "independent_kernel_verdict": "not performed", "budget": {"cpus": 2, "memory_gib": args.memory_gib,
            "probe_seconds": args.probe_seconds, "log_limit_bytes_per_step": LOG_LIMIT}}
    write_json(out/"run-metadata.json", meta)
    print(f"Stage 3 folder: {out}\nPhase: {args.phase}\nComparator is left untouched.", flush=True)
    status = 1
    try:
        meta["resources_before"] = check_resources(out, args.memory_gib, args.phase not in {"smoke", "provenance-smoke", "use-smoke", "search-smoke"})
        if args.phase in ['followup', 'suppliers', 'geometry-general', 'boundary', 'obligations', 'domains', 'witness-chain', 'height-chain']:
            collected = collect_sources(project, out)
            meta['source_collection'] = {"total_bytes": collected['total_bytes'],
                                         "index": 'collected-source-index.json'}
        subprocess.run(["sudo", "-v"], check=True)
        image = command(["sudo", "-n", "docker", "image", "inspect", "rh-lean-check:1", "--format", "{{.Id}}"])
        if not image.startswith("sha256:"):
            raise RuntimeError("Cannot resolve the existing Docker image ID")
        meta["docker_image_id"] = image
        sequence = [("positive", "Fixture.lean", ["RH_STAGE3_CONTEXT FIXTURE", "RH_STAGE3_POSITIVE_FIXTURE_END"], True),
                    ("negative", "NegativeFixture.lean", [], True)]
        if args.phase in {"consumers", "provenance-smoke", "uses", "use-smoke", "providers", "search-smoke", "extensions", "construction", "theta", "character", "descent", "integral"}:
            sequence.append(("provenance-fixture", "ProvenanceFixture.lean", ["RH_STAGE3_PROVENANCE_FIXTURE_END"], True))
        if args.phase in {"uses", "use-smoke"}:
            sequence.append(("use-fixture", "ArgumentUseFixture.lean", ["RH_STAGE3_USE_FIXTURE_END"], True))
        if args.phase in {"providers", "search-smoke", "extensions"}:
            sequence.append(("search-fixture", "TargetSearchFixture.lean", ["RH_STAGE3_SEARCH_FIXTURE_END"], True))
        if args.phase not in {"smoke", "provenance-smoke", "use-smoke", "search-smoke"}:
            selected = (["geometry", "height"] if args.phase == "inspect" else
                        ["boundary", "suppliers", "geometry-general"] if args.phase == "followup" else
                        ["domains", "witness-chain", "height-chain"] if args.phase == "obligations" else [args.phase])
            for name in selected:
                filename, markers = RECORDS[name]
                sequence.append((name, filename, markers, False))
        for name, filename, markers, smoke in sequence:
            check_resources(out, args.memory_gib, not smoke)
            seconds = 120 if smoke else args.probe_seconds
            cidfile = out/(name + ".cid")
            argv = docker_command(project, toolchain, out, image, cidfile, filename, seconds,
                                  4 if smoke else args.memory_gib, smoke)
            print(f"STAGE3_START {name}; full output: {out/(name+'.log')}", flush=True)
            step = {"name": name, "started_utc": now(), "completed": False}
            meta["steps"].append(step)
            write_json(out/"run-metadata.json", meta)
            rc, text = run_logged(argv, out/(name+".log"), cidfile, seconds)
            step.update({"exit_status": rc, "finished_utc": now()})
            step['first_lean_error'] = first_error(text)
            if name == 'geometry-general':
                step['baseline_accepted_marker'] = 'RH_STAGE3_SUPPLIER_BASELINE_ACCEPTED' in text
                step['arbitrary_accepted_marker'] = 'RH_STAGE3_ARBITRARY_SUPPLIER_ACCEPTED' in text
            step["printer_limit_indicators"] = {s: text.count(s) for s in
                ["⋯", "…", "maximum recursion depth", "maximum number of steps"] if s in text}
            step["rendering_completeness"] = "not independently certified; inspect any elisions before a complete-use claim"
            validate_result(name, rc, text, markers)
            if name == 'provenance-fixture':
                fixture_result=validate_provenance_fixture(text)
                write_json(out/'provenance-fixture-result.json',fixture_result)
            if name == 'use-fixture':
                write_json(out/'use-fixture-result.json',validate_use_fixture(text))
            if name == 'uses':
                cfg=json.loads((HERE/'use-targets.json').read_text())
                result=validate_provenance(text,cfg['targets'],cfg['reference_limit_per_location'])
                write_json(out/'use-provenance.json',result)
                uses=validate_uses(text,cfg['targets'],cfg)
                write_json(out/'argument-occurrences.json',uses)
                collected=collect_provenance_sources(project,out,result,cfg)
                meta['source_collection']={'total_bytes':collected['total_bytes'], 'index':'collected-source-index.json'}
                step['any_occurrence_truncated']=uses['any_occurrence_truncated']
                step['any_reference_truncated']=result['any_reference_truncated']
            if name == 'search-fixture':
                write_json(out/'search-fixture-result.json',validate_search_fixture(text))
            if name in {'providers', 'extensions'}:
                cfg=json.loads((HERE/('extension-targets.json' if name == 'extensions' else 'provider-targets.json')).read_text())
                result=validate_provenance(text,cfg['targets'],cfg['reference_limit_per_location'])
                write_json(out/('extension-provenance.json' if name == 'extensions' else 'provider-provenance.json'),result)
                search_result=validate_searches(text,cfg['searches'])
                write_json(out/'targeted-occurrences.json',search_result)
                collected=collect_provenance_sources(project,out,result,cfg)
                meta['source_collection']={'total_bytes':collected['total_bytes'], 'index':'collected-source-index.json'}
                step['any_search_truncated']=search_result['any_search_truncated']
                step['any_reference_truncated']=result['any_reference_truncated']
            if name == 'integral':
                cfg=json.loads((HERE/'integral-targets.json').read_text())
                result=validate_provenance(text,cfg['targets'],cfg['reference_limit_per_location'])
                write_json(out/'integral-provenance.json',result)
                collected=collect_provenance_sources(project,out,result,cfg)
                meta['source_collection']={'total_bytes':collected['total_bytes'], 'index':'collected-source-index.json'}
                step['any_reference_truncated']=result['any_reference_truncated']
            if name == 'descent':
                cfg=json.loads((HERE/'descent-targets.json').read_text())
                result=validate_provenance(text,cfg['targets'],cfg['reference_limit_per_location'])
                write_json(out/'descent-provenance.json',result)
                collected=collect_provenance_sources(project,out,result,cfg)
                meta['source_collection']={'total_bytes':collected['total_bytes'], 'index':'collected-source-index.json'}
                step['any_reference_truncated']=result['any_reference_truncated']
            if name == 'character':
                cfg=json.loads((HERE/'character-targets.json').read_text())
                result=validate_provenance(text,cfg['targets'],cfg['reference_limit_per_location'])
                write_json(out/'character-provenance.json',result)
                collected=collect_provenance_sources(project,out,result,cfg)
                meta['source_collection']={'total_bytes':collected['total_bytes'], 'index':'collected-source-index.json'}
                step['any_reference_truncated']=result['any_reference_truncated']
            if name == 'theta':
                cfg=json.loads((HERE/'theta-targets.json').read_text())
                result=validate_provenance(text,cfg['targets'],cfg['reference_limit_per_location'])
                write_json(out/'theta-provenance.json',result)
                collected=collect_provenance_sources(project,out,result,cfg)
                meta['source_collection']={'total_bytes':collected['total_bytes'], 'index':'collected-source-index.json'}
                step['any_reference_truncated']=result['any_reference_truncated']
            if name == 'construction':
                cfg=json.loads((HERE/'construction-targets.json').read_text())
                result=validate_provenance(text,cfg['targets'],cfg['reference_limit_per_location'])
                write_json(out/'construction-provenance.json',result)
                collected=collect_provenance_sources(project,out,result,cfg)
                write_json(out/'construction-source-hits.json',construction_source_hits(out,collected))
                meta['source_collection']={'total_bytes':collected['total_bytes'], 'index':'collected-source-index.json'}
                step['any_reference_truncated']=result['any_reference_truncated']
            if name == 'consumers':
                cfg=json.loads((HERE/'provenance-targets.json').read_text())
                result=validate_provenance(text,cfg['targets'],cfg['reference_limit_per_location'])
                write_json(out/'consumer-provenance.json',result)
                collected=collect_provenance_sources(project,out,result,cfg)
                meta['source_collection']={'total_bytes':collected['total_bytes'], 'index':'collected-source-index.json'}
                step['provenance']='consumer-provenance.json'
                step['any_reference_truncated']=result['any_reference_truncated']
            targets = json.loads((HERE/'chain-targets.json').read_text())
            if name in targets:
                blocks = declaration_blocks(text, targets[name])
                write_json(out/(name+'-blocks.json'), blocks)
                step['declaration_blocks'] = name+'-blocks.json'
            step["completed"] = True
            step["meaning"] = "expected type error observed" if name == "negative" else "requested Lean commands completed"
            write_json(out/"run-metadata.json", meta)
            print(f"STAGE3_STEP_COMPLETED {name}: {step['meaning']}", flush=True)
        meta["input_hashes_after"] = validate(project, toolchain)
        meta["phase_completed"] = True
        status = 0
    except (Exception, KeyboardInterrupt) as e:
        meta["failure"] = {"type": type(e).__name__, "message": str(e)}
        print(f"STAGE3_ERROR: {e}\nPreserve the logs. No later probe was started.", file=sys.stderr)
    finally:
        meta["finished_utc"] = now()
        write_json(out/"run-metadata.json", meta)
        bundle = archive(out)
        print(f"Evidence: {bundle}\nSHA-256: {sha256(bundle)}", flush=True)
        if status == 0:
            print("Requested collection completed. No new RH/GRH verdict or necessity verdict is asserted.")
    return status

if __name__ == "__main__":
    raise SystemExit(main())
