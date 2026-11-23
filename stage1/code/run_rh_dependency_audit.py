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
LEAN_SOURCE = 'import Lean\n\n/- Read compiled declarations only. This program is NOT a kernel checker.\n   Runtime imports disable environment extensions and load the private olean view.\n   Explicit theorem and opaque values must be traversed, not just definition values.\n   Run the isolated smoke fixture before importing the large project. -/\n\nopen Lean\n\nnamespace RHCriticsAudit\n\nstructure Edge where\n  target : Nat\n  label : String\n  extra : Bool\n  deriving Inhabited\n\nstructure Graph where\n  names : Array Name\n  index : NameMap Nat\n  edges : Array (Array Edge)\n  axioms : NameSet\n  missing : Array Name\n\ndef nameOf (s : String) : Name :=\n  (s.splitOn ".").foldl Name.str Name.anonymous\n\ndef strArray (xs : Array String) : Json := .arr (xs.map Json.str)\n\ndef emit (fields : List (String × Json)) : IO Unit := do\n  IO.println ("RH_AUDIT_JSON\\t" ++ (Json.mkObj fields).compress)\n  (← IO.getStdout).flush\n\ndef progress (s : String) : IO Unit := do\n  IO.println ("RH_AUDIT_PROGRESS\\t" ++ s)\n  (← IO.getStdout).flush\n\nabbrev Dep := Name × String × Bool\n\ndef exprDeps (e : Expr) (label : String) (extra := false) : Array Dep :=\n  e.getUsedConstants.map fun n => (n, label, extra)\n\ndef depsOf (ci : ConstantInfo) : Array Dep := Id.run do\n  let mut ds := exprDeps ci.type "type"\n  match ci with\n  | .defnInfo v => ds := ds ++ exprDeps v.value "definition-value"\n  | .thmInfo v => ds := ds ++ exprDeps v.value "theorem-proof"\n  | .opaqueInfo v => ds := ds ++ exprDeps v.value "opaque-value"\n  | .inductInfo v =>\n      for n in v.ctors do ds := ds.push (n, "inductive-constructor", true)\n      for n in v.all do ds := ds.push (n, "mutual-inductive", true)\n  | .ctorInfo v => ds := ds.push (v.induct, "constructor-parent", true)\n  | .recInfo v =>\n      for n in v.all do ds := ds.push (n, "recursor-inductive", true)\n      for r in v.rules do\n        ds := ds.push (r.ctor, "recursor-constructor", true)\n        ds := ds ++ exprDeps r.rhs "recursor-rule-rhs" true\n  | _ => pure ()\n  return ds\n\ndef kindOf : ConstantInfo → String\n  | .axiomInfo _ => "axiom"\n  | .defnInfo _ => "definition"\n  | .thmInfo _ => "theorem"\n  | .opaqueInfo _ => "opaque"\n  | .inductInfo _ => "inductive"\n  | .ctorInfo _ => "constructor"\n  | .recInfo _ => "recursor"\n  | .quotInfo _ => "quotient-primitive"\n\ndef moduleOf (env : Environment) (n : Name) : String :=\n  match env.getModuleIdxFor? n with\n  | none => "<no imported module index>"\n  | some i =>\n      match env.header.moduleNames[i.toNat]? with\n      | some m => m.toString\n      | none => "<invalid module index>"\n\ndef nodeJson (env : Environment) (n : Name) : Json :=\n  let k := match env.checked.get.find? n with\n    | some ci => kindOf ci\n    | none => "MISSING"\n  Json.mkObj [("name", toJson n.toString), ("kind", toJson k),\n    ("module", toJson (moduleOf env n))]\n\ndef buildGraph (env : Environment) (roots : Array Name) : IO Graph := do\n  let kenv := env.checked.get\n  let mut names : Array Name := #[]\n  let mut index : NameMap Nat := {}\n  let mut edges : Array (Array Edge) := #[]\n  let mut axioms : NameSet := {}\n  let mut missing : Array Name := #[]\n  for n in roots do\n    unless index.contains n do\n      index := index.insert n names.size\n      names := names.push n\n  let mut cursor := 0\n  let mut edgeCount := 0\n  while cursor < names.size do\n    let n := names[cursor]!\n    let mut es : Array Edge := #[]\n    match kenv.find? n with\n    | none => missing := missing.push n\n    | some ci =>\n        if ci.isAxiom then axioms := axioms.insert n\n        for (dep, label, extra) in depsOf ci do\n          let target := match index.find? dep with\n            | some i => i\n            | none => names.size\n          if target == names.size then\n            index := index.insert dep target\n            names := names.push dep\n          es := es.push { target, label, extra }\n    edgeCount := edgeCount + es.size\n    edges := edges.push es\n    cursor := cursor + 1\n    if cursor % 25000 == 0 then\n      progress s!"graph: {cursor} expanded, {names.size} discovered, {edgeCount} edges"\n    if names.size > 4000000 then\n      throw (IO.userError "Graph exceeded 4,000,000 declarations; audit incomplete.")\n  emit [("event", toJson "graph-complete"), ("declarations", toJson names.size),\n    ("roots", strArray (roots.map Name.toString)),\n    ("edges", toJson edgeCount), ("missing", strArray (missing.map Name.toString))]\n  return { names, index, edges, axioms, missing }\n\nstructure Walk where\n  parents : Array (Option (Nat × String))\n  visited : Nat\n  axioms : Array Name\n\ndef walk (g : Graph) (root : Nat) (extra : Bool) : IO Walk := do\n  let mut parents : Array (Option (Nat × String)) := Array.replicate g.names.size none\n  parents := parents.set! root (some (root, "root"))\n  let mut queue : Array Nat := #[root]\n  let mut cursor := 0\n  let mut axioms : Array Name := #[]\n  while cursor < queue.size do\n    let i := queue[cursor]!\n    if g.axioms.contains g.names[i]! then axioms := axioms.push g.names[i]!\n    for e in g.edges[i]! do\n      if (extra || !e.extra) && parents[e.target]!.isNone then\n        parents := parents.set! e.target (some (i, e.label))\n        queue := queue.push e.target\n    cursor := cursor + 1\n    if cursor % 250000 == 0 then\n      progress s!"reachability: {g.names[root]!}, extra={extra}, visited={cursor}"\n  return { parents, visited := cursor, axioms := axioms.qsort Name.lt }\n\ndef pathJson (env : Environment) (g : Graph) (w : Walk) (target : Nat) : Json := Id.run do\n  let mut current := target\n  let mut path : Array Json := #[]\n  let mut fuel := g.names.size + 1\n  while fuel > 0 do\n    fuel := fuel - 1\n    let some (p, label) := w.parents[current]! | break\n    path := path.push (Json.mkObj [("declaration", nodeJson env g.names[current]!),\n      ("edge_from_parent", toJson label)])\n    if p == current then break\n    current := p\n  return .arr path.reverse\n\ndef rootNames : Array Name := (#[\n  "riemannHypothesis", "riemannZeta_eq_zero_re", "LFunction_ne_zero_of_half_lt_re",\n  "LFunction_eq_zero_re", "LFunction_eq_zero_re_of_isPrimitive"\n  ] : Array String).map nameOf\n\ndef watchNames : Array Name := (#[\n  "GlobalTheory.Mem.Top.Bl.anyGeometry",\n  "GlobalTheory.Mem.Top.Bl.geoOf",\n  "GlobalTheory.Mem.Top.Bl.GeoCl",\n  "GlobalTheory.Mem.Top.Bl.geoCl",\n  "GlobalTheory.Mem.Top.Bl.OXModel.geoOf_surf",\n  "UpperTheory.Lit.hypsE",\n  "UpperTheory.Lit.hypsE₂",\n  "UpperTheory.Lit.everyE₂",\n  "UpperTheory.Top.plugAll",\n  "UpperTheory.Top.every_character_of_green_v_win",\n  "UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound",\n  "UpperTheory.Lit.every_character_of_theta_integrals_local_matching",\n  "UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin",\n  "UpperTheory.FinalTheorems.everyCharacter_of_row",\n  "UpperTheory.FinalTheorems.everyCharacter",\n  "GlobalTheory.Mem.Top.DivRec.geoOver_stages",\n  "GlobalTheory.Mem.Top.DivRec.exists_divT",\n  "GlobalTheory.Mem.Top.DivRec.divEx_prov",\n  "GlobalTheory.Mem.Top.DivRec.divEx_of_ox",\n  "GlobalTheory.Mem.Top.Closing.divEx_geoCl",\n  "GlobalTheory.Mem.Top.Closing.memberE_closing_alt_alt",\n  "GlobalTheory.T.member_exists_baseLattice_alt",\n  "Formalism.L2.Geo.geoDegenerate",\n  "Formalism.L2.Geo.geoDegenerateNoTau",\n  "Formalism.L2.Geo.algDegenerate",\n  "Formalism.L2.Geo.algJunk",\n  "Formalism.L2.Geo.padDegenerate",\n  "Formalism.L2.Geo.padJunk",\n  "Formalism.L2.Geo.mdlJunk",\n  "Formalism.L2.Geo.divXFl",\n  "Formalism.L2.Geo.compatibleDivisorData",\n  "Formalism.L2.Geo.famFlJ",\n  "Formalism.L2.Geo.GeoTiedP.geoTied",\n  "Formalism.L2.Geo.GeoTiedP.formsTieX",\n  "Formalism.MainNotions.placeRankTwoOne.degree_value_of_determinant",\n  "GlobalTheory.EX.OB.LedPart.ht",\n  "GlobalTheory.EX.OB.LedPart.pt",\n  "Formalism.BasicNotions.DV.hExpl6",\n  "SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt",\n  "PositivityTheory.Pf1.HilbertSamuelMoriwaki.hsUse_outright",\n  "PositivityTheory.Pf1.HilbertSamuelMoriwaki.moriwakiBig_outright",\n  "allChi", "rhOfAll", "Formalism.VW.rh_of_every",\n  "RiemannHypothesis", "riemannZeta", "DirichletCharacter.LFunction"\n  ] : Array String).map nameOf\n\ndef reachable (g : Graph) (w : Walk) (n : Name) : Bool :=\n  match g.index.find? n with\n  | some i => w.parents[i]!.isSome\n  | none => false\n\ndef runSmoke (env : Environment) : IO Unit := do\n  let n := fun s => nameOf ("RHCriticsFixture." ++ s)\n  let g ← buildGraph env #[n "root", n "choiceRoot"]\n  if !g.missing.isEmpty then throw (IO.userError "Smoke graph has missing declarations")\n  let some ri := g.index.find? (n "root") | throw (IO.userError "Missing smoke root")\n  let some ci := g.index.find? (n "choiceRoot") | throw (IO.userError "Missing choice root")\n  let direct ← walk g ri false\n  for s in #["fakePremise", "hiddenDef", "viaTheorem", "viaOpaque"] do\n    unless reachable g direct (n s) do\n      throw (IO.userError s!"Smoke missed theorem/opaque dependency: {s}")\n  if reachable g direct (n "irrelevant") then\n    throw (IO.userError "Smoke incorrectly reached an unused theorem")\n  let choiceDirect ← walk g ci false\n  if reachable g choiceDirect (n "fakePremise") then\n    throw (IO.userError "Smoke confused a structural edge with a term reference")\n  let choiceStructural ← walk g ci true\n  unless reachable g choiceStructural (n "fakePremise") do\n    throw (IO.userError "Smoke missed the unused inductive constructor\'s premise")\n  emit [("event", toJson "smoke-passed"),\n    ("checks", strArray #["theorem bodies", "opaque bodies", "definition bodies",\n      "unused theorem excluded", "reference/structural distinction"])]\n\ndef runMain (env : Environment) : IO Unit := do\n  for root in rootNames do\n    unless (env.checked.get.find? root).isSome do\n      throw (IO.userError s!"Headline theorem absent: {root}")\n  for n in watchNames do\n    match env.checked.get.find? n with\n    | none => emit [("event", toJson "watch-declaration"), ("name", toJson n.toString),\n        ("exists", toJson false)]\n    | some ci =>\n        let ds := depsOf ci\n        let dsJson := (ds.extract 0 2000).map fun (dep, label, extra) =>\n          Json.mkObj [("name", toJson dep.toString), ("edge", toJson label),\n            ("structural", toJson extra), ("module", toJson (moduleOf env dep))]\n        emit [("event", toJson "watch-declaration"), ("name", toJson n.toString),\n          ("exists", toJson true), ("declaration", nodeJson env n),\n          ("direct_edges", .arr dsJson), ("direct_edge_count", toJson ds.size),\n          ("direct_edges_truncated", toJson (decide (ds.size > 2000)))]\n  let g ← buildGraph env rootNames\n  for root in rootNames do\n    let some ri := g.index.find? root | throw (IO.userError s!"Missing root index: {root}")\n    for extra in #[false, true] do\n      progress s!"Starting reachability for {root}; include extra edges={extra}"\n      let w ← walk g ri extra\n      emit [("event", toJson "root-summary"), ("root", toJson root.toString),\n        ("include_structural_edges", toJson extra), ("visited", toJson w.visited),\n        ("axioms", strArray (w.axioms.map Name.toString))]\n      for n in watchNames do\n        let hit := reachable g w n\n        let path := match g.index.find? n with\n          | some i => if hit then pathJson env g w i else .arr #[]\n          | none => .arr #[]\n        emit [("event", toJson "reachability"), ("root", toJson root.toString),\n          ("include_structural_edges", toJson extra), ("target", toJson n.toString),\n          ("exists", toJson (env.checked.get.find? n).isSome),\n          ("reachable", toJson hit), ("path", path)]\n  unless g.missing.isEmpty do\n    throw (IO.userError "Referenced declarations are missing; negative results are incomplete.")\n  emit [("event", toJson "audit-completed"),\n    ("meaning", toJson "Syntactic declaration dependency audit completed; no kernel check or mathematical-invalidity verdict.")]\n\nend RHCriticsAudit\n\ndef main (args : List String) : IO UInt32 := do\n  try\n    Lean.initSearchPath (← Lean.findSysroot)\n    let smoke := args == ["smoke"]\n    unless smoke || args == ["main"] do\n      throw (IO.userError "Usage: lean --run RHCriticsTrace.lean smoke|main")\n    RHCriticsAudit.progress (if smoke then "Loading isolated smoke fixture" else\n      "Loading Main compiled declarations; this stage may be quiet and memory intensive")\n    let mod := if smoke then `RHCriticsFixture else `Main\n    let env ← Lean.importModules #[{ module := mod }] {} (loadExts := false)\n    if smoke then RHCriticsAudit.runSmoke env else RHCriticsAudit.runMain env\n    return 0\n  catch e =>\n    IO.eprintln s!"RH_AUDIT_ERROR: {e}"\n    return 1\n'
FIXTURE_SOURCE = 'import Lean\n\n/- Isolated audit-tool test data. This is never imported into the RH project.\n   The artificial axiom tests whether the dependency walker actually reads\n   theorem and opaque bodies; it is not a premise added to the RH proof. -/\nnamespace RHCriticsFixture\n\naxiom fakePremise : True\ndef hiddenDef : True := fakePremise\ntheorem viaTheorem : True := hiddenDef\nopaque viaOpaque : True := viaTheorem\ntheorem root : True := viaOpaque\ntheorem irrelevant : True := True.intro\n\ninductive Choice where\n  | ordinary : Choice\n  | hidden (h : fakePremise = fakePremise) : Choice\n\ntheorem choiceRoot : Nonempty Choice := ⟨Choice.ordinary⟩\n\nend RHCriticsFixture\n'
FINDINGS = "# Nielsen/Chu critique: findings from Harry's pinned source\n\nSource: `753431bfe28701f6f3937f664fcaf08daa139c03`.\nMathlib: `0df444a360eaa60ab8c11dca51a86af692955474`.\nLean: `leanprover/lean4:v4.33.1`.\nEvidence: the uploaded source-evidence.zip, collected 2026-11-22 14:11 EST.\n\nThis document reports source inspection. It does not claim that a compiled\ndependency trace has already run or that mathematical invalidity follows.\n\n## Confirmed source facts\n\n1. `anyGeometry` is defined as `fun _ _ _ => True` in\n   `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/OverIx.lean:19`.\n   The collector finds 162 exact-token textual occurrences in 24 files, including\n   comments/strings if present. This reproduces Chu's 24-file observation.\n2. `GeoCl.base` accepts a proof of the underlying predicate in\n   `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/NotGeoClFalse.lean:22`.\n   Consequently `geoCl anyGeometry D J X` is inhabited by `GeoCl.base True.intro`\n   for every appropriately typed input. This establishes that this particular\n   certificate imposes no restriction. It does not establish that all other\n   hypotheses of a later analytic theorem impose no restriction.\n3. `geoDegenerate`, `algDegenerate`, `padDegenerate`, `mdlJunk`, `geoDegenerateNoTau`,\n   `algJunk`, and `padJunk` exist in\n   `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean`.\n   Many predicates are `True`; many types are `PUnit`; several measures/norms are\n   zero. The model is not literally all zero: `geoDegenerate.inter` uses the\n   integer flag-degree formula, for example. Full field definitions matter.\n4. In that file, `divXFl` at line 829 sets `iMj` to the zero linear map at line\n   860. `compatibleDivisorData` also uses a zero map at line 708. These are\n   distinct constructions, not interchangeable names for one declaration.\n5. `GlobalTheory.EX.OB.LedPart.ht` is defined to equal `DV.hExpl6 ...` at\n   `src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/SetUnipotentTranslate.lean:379`.\n   `LedPart.pt` supplies `h_eq := fun _ => rfl` at line 400. This confirms an\n   identity by construction, not that other estimates about the assigned height\n   are automatic. The formula itself contains sums and logarithmic terms;\n   see `src/Formalism/LocalRingCardinality/KernelPlaceMeanBound.lean:25`.\n6. `geoOf_surf`, `GeoTiedP.geoTied`, `GeoTiedP.formsTieX`, and\n   `degree_value_of_determinant` each have one exact-token textual occurrence\n   in the scanned source: their declaration. This is evidence of no named text\n   calls in those tracked project files. It does not yet certify compiled\n   non-reachability, exclude metaprogram-generated calls, or exclude equivalent\n   arguments proved separately.\n\n## Correction to the proposed top-level chain\n\nThe exact ASCII token `hypsE` has zero occurrences. The older file\n`src/Development/AutomorphicArithmetic/ThetaCorrespondence/FockModels/EveryCharacterE.lean`\ndefines `UpperTheory.Lit.hypsE₂` at line 41 and `everyE₂` at line 67.\n`everyE₂` calls `plugAll` at line 70.\n\nThe final source instead explicitly calls this newer route:\n\n```\nriemannHypothesis\n  -> rhOfAll\n  -> Formalism.VW.rh_of_every allChi\nallChi\n  -> UpperTheory.FinalTheorems.everyCharacter\n  -> UpperTheory.FinalTheorems.everyCharacter_of_row\n  -> UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin\n  -> UpperTheory.Lit.every_character_of_theta_integrals_local_matching\n  -> UpperTheory.Top.every_character_of_green_v_win\n     [given a bundle constructed by\n      UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound]\n```\n\nThis is a source-call outline, not yet the complete compiled dependency path.\nThe new `nonempty_hyps_definite_side_of_closed_bound` ALSO passes\n`geoCl anyGeometry` in its body. This happens in\n`src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/SiegelEisensteinSecondTermHypotheses.lean:60`,\nwith further occurrences at lines 63 and 67. The named-route correction does\nnot make the substantive question disappear. Conversely, an import of the\nolder EveryCharacterE module does not establish use of its theorems.\n\n## Concrete lower-level route worth testing\n\nIn `TupPinsOfMuIsW.lean`, `geoOver_stages` constructs a witness using `divXFl`\nand `famFlJ`; `exists_divT` invokes it. `divEx_prov` invokes `exists_divT`;\n`divEx_of_ox` invokes `divEx_prov`. In\n`PublishedInputsImplyConclusion.lean`, `divEx_geoCl` invokes `divEx_of_ox`\nand upgrades the unrestricted predicate using `geoCl_of`.\n`MemberEClosing.lean`'s `memberE_closing_alt_alt` passes `divEx_geoCl` onward.\nThe compiled audit tests whether this route is reachable from each final root.\n\n## Final statement inspection\n\n`src/Main.lean` types the headline RH theorem as the root `RiemannHypothesis`.\nThe collected pinned Mathlib file\n`Mathlib/NumberTheory/LSeries/RiemannZeta.lean:185` defines it as the familiar\nzeta-zero statement, excluding negative even integers and the pole.\n`src/Statements.lean` defines the Dirichlet statements using\n`DirichletCharacter.LFunction`, which the pinned Mathlib defines through\n`ZMod.LFunction`. This is source-level evidence, separate from the ongoing\nComparator's protected-statement comparison.\n\n## What would constitute a conclusion\n\nA syntactic path to a trivial auxiliary predicate confirms its presence in\nthe stored derivation, not an invalid inference. A predicate's descriptive\nname is not an additional logical premise. A specific gap requires showing\nwhich required implication, interpretation of the final statement, axiom\nrestriction, or kernel rule fails. An unused extraction lemma by itself does\nnot establish such a failure. The semantic adequacy of an intermediate\ngeometric interpretation is also distinct from derivability of the final\nfixed statement under the admitted foundational axioms.\n\nThe next audit reports explicit theorem/opaque-body paths, per-root axiom\nclosures, and expanded inductive dependencies. It is an inspection tool and\ndoes not replace Nanoda or Comparator.\n"


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
