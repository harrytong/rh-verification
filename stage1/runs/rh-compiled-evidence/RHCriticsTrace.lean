import Lean

/- Read compiled declarations only. This program is NOT a kernel checker.
   Runtime imports disable environment extensions and load the private olean view.
   Explicit theorem and opaque values must be traversed, not just definition values.
   Run the isolated smoke fixture before importing the large project. -/

open Lean

namespace RHCriticsAudit

structure Edge where
  target : Nat
  label : String
  extra : Bool
  deriving Inhabited

structure Graph where
  names : Array Name
  index : NameMap Nat
  edges : Array (Array Edge)
  axioms : NameSet
  missing : Array Name

def nameOf (s : String) : Name :=
  (s.splitOn ".").foldl Name.str Name.anonymous

def strArray (xs : Array String) : Json := .arr (xs.map Json.str)

def emit (fields : List (String × Json)) : IO Unit := do
  IO.println ("RH_AUDIT_JSON\t" ++ (Json.mkObj fields).compress)
  (← IO.getStdout).flush

def progress (s : String) : IO Unit := do
  IO.println ("RH_AUDIT_PROGRESS\t" ++ s)
  (← IO.getStdout).flush

abbrev Dep := Name × String × Bool

def exprDeps (e : Expr) (label : String) (extra := false) : Array Dep :=
  e.getUsedConstants.map fun n => (n, label, extra)

def depsOf (ci : ConstantInfo) : Array Dep := Id.run do
  let mut ds := exprDeps ci.type "type"
  match ci with
  | .defnInfo v => ds := ds ++ exprDeps v.value "definition-value"
  | .thmInfo v => ds := ds ++ exprDeps v.value "theorem-proof"
  | .opaqueInfo v => ds := ds ++ exprDeps v.value "opaque-value"
  | .inductInfo v =>
      for n in v.ctors do ds := ds.push (n, "inductive-constructor", true)
      for n in v.all do ds := ds.push (n, "mutual-inductive", true)
  | .ctorInfo v => ds := ds.push (v.induct, "constructor-parent", true)
  | .recInfo v =>
      for n in v.all do ds := ds.push (n, "recursor-inductive", true)
      for r in v.rules do
        ds := ds.push (r.ctor, "recursor-constructor", true)
        ds := ds ++ exprDeps r.rhs "recursor-rule-rhs" true
  | _ => pure ()
  return ds

def kindOf : ConstantInfo → String
  | .axiomInfo _ => "axiom"
  | .defnInfo _ => "definition"
  | .thmInfo _ => "theorem"
  | .opaqueInfo _ => "opaque"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"
  | .quotInfo _ => "quotient-primitive"

def moduleOf (env : Environment) (n : Name) : String :=
  match env.getModuleIdxFor? n with
  | none => "<no imported module index>"
  | some i =>
      match env.header.moduleNames[i.toNat]? with
      | some m => m.toString
      | none => "<invalid module index>"

def nodeJson (env : Environment) (n : Name) : Json :=
  let k := match env.checked.get.find? n with
    | some ci => kindOf ci
    | none => "MISSING"
  Json.mkObj [("name", toJson n.toString), ("kind", toJson k),
    ("module", toJson (moduleOf env n))]

def buildGraph (env : Environment) (roots : Array Name) : IO Graph := do
  let kenv := env.checked.get
  let mut names : Array Name := #[]
  let mut index : NameMap Nat := {}
  let mut edges : Array (Array Edge) := #[]
  let mut axioms : NameSet := {}
  let mut missing : Array Name := #[]
  for n in roots do
    unless index.contains n do
      index := index.insert n names.size
      names := names.push n
  let mut cursor := 0
  let mut edgeCount := 0
  while cursor < names.size do
    let n := names[cursor]!
    let mut es : Array Edge := #[]
    match kenv.find? n with
    | none => missing := missing.push n
    | some ci =>
        if ci.isAxiom then axioms := axioms.insert n
        for (dep, label, extra) in depsOf ci do
          let target := match index.find? dep with
            | some i => i
            | none => names.size
          if target == names.size then
            index := index.insert dep target
            names := names.push dep
          es := es.push { target, label, extra }
    edgeCount := edgeCount + es.size
    edges := edges.push es
    cursor := cursor + 1
    if cursor % 25000 == 0 then
      progress s!"graph: {cursor} expanded, {names.size} discovered, {edgeCount} edges"
    if names.size > 4000000 then
      throw (IO.userError "Graph exceeded 4,000,000 declarations; audit incomplete.")
  emit [("event", toJson "graph-complete"), ("declarations", toJson names.size),
    ("roots", strArray (roots.map Name.toString)),
    ("edges", toJson edgeCount), ("missing", strArray (missing.map Name.toString))]
  return { names, index, edges, axioms, missing }

structure Walk where
  parents : Array (Option (Nat × String))
  visited : Nat
  axioms : Array Name

def walk (g : Graph) (root : Nat) (extra : Bool) : IO Walk := do
  let mut parents : Array (Option (Nat × String)) := Array.replicate g.names.size none
  parents := parents.set! root (some (root, "root"))
  let mut queue : Array Nat := #[root]
  let mut cursor := 0
  let mut axioms : Array Name := #[]
  while cursor < queue.size do
    let i := queue[cursor]!
    if g.axioms.contains g.names[i]! then axioms := axioms.push g.names[i]!
    for e in g.edges[i]! do
      if (extra || !e.extra) && parents[e.target]!.isNone then
        parents := parents.set! e.target (some (i, e.label))
        queue := queue.push e.target
    cursor := cursor + 1
    if cursor % 250000 == 0 then
      progress s!"reachability: {g.names[root]!}, extra={extra}, visited={cursor}"
  return { parents, visited := cursor, axioms := axioms.qsort Name.lt }

def pathJson (env : Environment) (g : Graph) (w : Walk) (target : Nat) : Json := Id.run do
  let mut current := target
  let mut path : Array Json := #[]
  let mut fuel := g.names.size + 1
  while fuel > 0 do
    fuel := fuel - 1
    let some (p, label) := w.parents[current]! | break
    path := path.push (Json.mkObj [("declaration", nodeJson env g.names[current]!),
      ("edge_from_parent", toJson label)])
    if p == current then break
    current := p
  return .arr path.reverse

def rootNames : Array Name := (#[
  "riemannHypothesis", "riemannZeta_eq_zero_re", "LFunction_ne_zero_of_half_lt_re",
  "LFunction_eq_zero_re", "LFunction_eq_zero_re_of_isPrimitive"
  ] : Array String).map nameOf

def watchNames : Array Name := (#[
  "GlobalTheory.Mem.Top.Bl.anyGeometry",
  "GlobalTheory.Mem.Top.Bl.geoOf",
  "GlobalTheory.Mem.Top.Bl.GeoCl",
  "GlobalTheory.Mem.Top.Bl.geoCl",
  "GlobalTheory.Mem.Top.Bl.OXModel.geoOf_surf",
  "UpperTheory.Lit.hypsE",
  "UpperTheory.Lit.hypsE₂",
  "UpperTheory.Lit.everyE₂",
  "UpperTheory.Top.plugAll",
  "UpperTheory.Top.every_character_of_green_v_win",
  "UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound",
  "UpperTheory.Lit.every_character_of_theta_integrals_local_matching",
  "UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin",
  "UpperTheory.FinalTheorems.everyCharacter_of_row",
  "UpperTheory.FinalTheorems.everyCharacter",
  "GlobalTheory.Mem.Top.DivRec.geoOver_stages",
  "GlobalTheory.Mem.Top.DivRec.exists_divT",
  "GlobalTheory.Mem.Top.DivRec.divEx_prov",
  "GlobalTheory.Mem.Top.DivRec.divEx_of_ox",
  "GlobalTheory.Mem.Top.Closing.divEx_geoCl",
  "GlobalTheory.Mem.Top.Closing.memberE_closing_alt_alt",
  "GlobalTheory.T.member_exists_baseLattice_alt",
  "Formalism.L2.Geo.geoDegenerate",
  "Formalism.L2.Geo.geoDegenerateNoTau",
  "Formalism.L2.Geo.algDegenerate",
  "Formalism.L2.Geo.algJunk",
  "Formalism.L2.Geo.padDegenerate",
  "Formalism.L2.Geo.padJunk",
  "Formalism.L2.Geo.mdlJunk",
  "Formalism.L2.Geo.divXFl",
  "Formalism.L2.Geo.compatibleDivisorData",
  "Formalism.L2.Geo.famFlJ",
  "Formalism.L2.Geo.GeoTiedP.geoTied",
  "Formalism.L2.Geo.GeoTiedP.formsTieX",
  "Formalism.MainNotions.placeRankTwoOne.degree_value_of_determinant",
  "GlobalTheory.EX.OB.LedPart.ht",
  "GlobalTheory.EX.OB.LedPart.pt",
  "Formalism.BasicNotions.DV.hExpl6",
  "SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt",
  "PositivityTheory.Pf1.HilbertSamuelMoriwaki.hsUse_outright",
  "PositivityTheory.Pf1.HilbertSamuelMoriwaki.moriwakiBig_outright",
  "allChi", "rhOfAll", "Formalism.VW.rh_of_every",
  "RiemannHypothesis", "riemannZeta", "DirichletCharacter.LFunction"
  ] : Array String).map nameOf

def reachable (g : Graph) (w : Walk) (n : Name) : Bool :=
  match g.index.find? n with
  | some i => w.parents[i]!.isSome
  | none => false

def runSmoke (env : Environment) : IO Unit := do
  let n := fun s => nameOf ("RHCriticsFixture." ++ s)
  let g ← buildGraph env #[n "root", n "choiceRoot"]
  if !g.missing.isEmpty then throw (IO.userError "Smoke graph has missing declarations")
  let some ri := g.index.find? (n "root") | throw (IO.userError "Missing smoke root")
  let some ci := g.index.find? (n "choiceRoot") | throw (IO.userError "Missing choice root")
  let direct ← walk g ri false
  for s in #["fakePremise", "hiddenDef", "viaTheorem", "viaOpaque"] do
    unless reachable g direct (n s) do
      throw (IO.userError s!"Smoke missed theorem/opaque dependency: {s}")
  if reachable g direct (n "irrelevant") then
    throw (IO.userError "Smoke incorrectly reached an unused theorem")
  let choiceDirect ← walk g ci false
  if reachable g choiceDirect (n "fakePremise") then
    throw (IO.userError "Smoke confused a structural edge with a term reference")
  let choiceStructural ← walk g ci true
  unless reachable g choiceStructural (n "fakePremise") do
    throw (IO.userError "Smoke missed the unused inductive constructor's premise")
  emit [("event", toJson "smoke-passed"),
    ("checks", strArray #["theorem bodies", "opaque bodies", "definition bodies",
      "unused theorem excluded", "reference/structural distinction"])]

def runMain (env : Environment) : IO Unit := do
  for root in rootNames do
    unless (env.checked.get.find? root).isSome do
      throw (IO.userError s!"Headline theorem absent: {root}")
  for n in watchNames do
    match env.checked.get.find? n with
    | none => emit [("event", toJson "watch-declaration"), ("name", toJson n.toString),
        ("exists", toJson false)]
    | some ci =>
        let ds := depsOf ci
        let dsJson := (ds.extract 0 2000).map fun (dep, label, extra) =>
          Json.mkObj [("name", toJson dep.toString), ("edge", toJson label),
            ("structural", toJson extra), ("module", toJson (moduleOf env dep))]
        emit [("event", toJson "watch-declaration"), ("name", toJson n.toString),
          ("exists", toJson true), ("declaration", nodeJson env n),
          ("direct_edges", .arr dsJson), ("direct_edge_count", toJson ds.size),
          ("direct_edges_truncated", toJson (ds.size > 2000))]
  let g ← buildGraph env rootNames
  for root in rootNames do
    let some ri := g.index.find? root | throw (IO.userError s!"Missing root index: {root}")
    for extra in #[false, true] do
      progress s!"Starting reachability for {root}; include extra edges={extra}"
      let w ← walk g ri extra
      emit [("event", toJson "root-summary"), ("root", toJson root.toString),
        ("include_structural_edges", toJson extra), ("visited", toJson w.visited),
        ("axioms", strArray (w.axioms.map Name.toString))]
      for n in watchNames do
        let hit := reachable g w n
        let path := match g.index.find? n with
          | some i => if hit then pathJson env g w i else .arr #[]
          | none => .arr #[]
        emit [("event", toJson "reachability"), ("root", toJson root.toString),
          ("include_structural_edges", toJson extra), ("target", toJson n.toString),
          ("exists", toJson (env.checked.get.find? n).isSome),
          ("reachable", toJson hit), ("path", path)]
  unless g.missing.isEmpty do
    throw (IO.userError "Referenced declarations are missing; negative results are incomplete.")
  emit [("event", toJson "audit-completed"),
    ("meaning", toJson "Syntactic declaration dependency audit completed; no kernel check or mathematical-invalidity verdict.")]

end RHCriticsAudit

def main (args : List String) : IO UInt32 := do
  try
    Lean.initSearchPath (← Lean.findSysroot)
    let smoke := args == ["smoke"]
    unless smoke || args == ["main"] do
      throw (IO.userError "Usage: lean --run RHCriticsTrace.lean smoke|main")
    RHCriticsAudit.progress (if smoke then "Loading isolated smoke fixture" else
      "Loading Main compiled declarations; this stage may be quiet and memory intensive")
    let mod := if smoke then `RHCriticsFixture else `Main
    let env ← Lean.importModules #[{ module := mod }] {} (loadExts := false)
    if smoke then RHCriticsAudit.runSmoke env else RHCriticsAudit.runMain env
    return 0
  catch e =>
    IO.eprintln s!"RH_AUDIT_ERROR: {e}"
    return 1
