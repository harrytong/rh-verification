/- Appended to the shared RHStage2 definitions by the Python runner.
   Semantic tests use fresh MetaM states and loaded environment extensions.
   They do not add or replace declarations in the imported proof. -/
namespace RHStage2Semantic
open Lean Meta

def labels : Array String := #["Prop-valued-definition-definitionally-True",
  "unit-typed-constructor-field", "definitionally-zero-linear-map",
  "definitionally-zero-measure", "unit-valued-definition-auxiliary",
  "unit-type-family-value-auxiliary", "reserved"]

def classifyValue (ty value : Expr) (field : Bool) : MetaM (Array Nat) := do
  withTransparency .all do
    forallTelescopeReducing ty fun xs range => do
      let applied := mkAppN value xs
      let range' ← whnf range
      let mut cats : Array Nat := #[]
      match range' with
      | .sort .zero =>
          if ← isDefEq applied (mkConst `True) then cats := cats.push 0
      | _ => pure ()
      if range'.getAppFn.isConstOf `PUnit || range'.getAppFn.isConstOf `Unit then
        cats := cats.push (if field then 1 else 4)
      let typeHead := range'.getAppFn
      let isLinear := #[`LinearMap, `ContinuousLinearMap].any typeHead.isConstOf
      let isMeasure := typeHead.isConstOf `MeasureTheory.Measure
      if isLinear || isMeasure then
        let z ← mkAppOptM `Zero.zero #[some range, none]
        let z ← instantiateMVars z
        if z.hasMVar then throwError "Unresolved metavariables in the zero comparison"
        if ← isDefEq applied z then cats := cats.push (if isMeasure then 3 else 2)
      match range' with
      | .sort _ =>
          let v' ← whnf applied
          if v'.getAppFn.isConstOf `PUnit || v'.getAppFn.isConstOf `Unit then
            cats := cats.push 5
      | _ => pure ()
      return cats

structure Finding where
  location : String
  categories : Array Nat
  deriving Inhabited

structure Analysis where
  findings : Array Finding := #[]
  constructorFieldsVisited : Nat := 0
  recordDepthBoundReached : Bool := false
  deriving Inhabited

/- Every definition in the reference union is considered. Constructor fields
   are inspected in its reduced outer record and recursively in record-valued
   fields, to depth 4. This is not a census of every anonymous record buried
   inside arbitrary proof terms. That wider denominator is explicitly open. -/
partial def analyzeRecord (ty value : Expr) (path : String) (depth : Nat) : MetaM Analysis := do
  if depth > 4 then return { recordDepthBoundReached := true }
  withTransparency .all do
    forallTelescopeReducing ty fun xs _ => do
      let applied := mkAppN value xs
      let v' ← whnf applied
      let .const ctorName _ := v'.getAppFn | return {}
      let env ← getEnv
      let some (.ctorInfo ctor) := env.checked.get.find? ctorName | return {}
      unless (getStructureInfo? env ctor.induct).isSome do return {}
      let args := v'.getAppArgs
      let mut result : Analysis := {}
      for i in [ctor.numParams:args.size] do
        let arg := args[i]!
        let argTy ← inferType arg
        let location := path ++ s!"/constructor:{ctorName}/arg:{i}"
        let cats ← classifyValue argTy arg true
        result := { result with constructorFieldsVisited := result.constructorFieldsVisited + 1 }
        unless cats.isEmpty do
          result := { result with findings := result.findings.push { location, categories := cats } }
        let nested ← analyzeRecord argTy arg location (depth + 1)
        result := {
          findings := result.findings ++ nested.findings
          constructorFieldsVisited := result.constructorFieldsVisited + nested.constructorFieldsVisited
          recordDepthBoundReached := result.recordDepthBoundReached || nested.recordDepthBoundReached
        }
      return result

def analyzeDefinition (ci : ConstantInfo) : MetaM Analysis := do
  let .defnInfo v := ci | return {}
  let cats ← classifyValue v.type v.value false
  let mut result ← analyzeRecord v.type v.value "definition-value" 0
  unless cats.isEmpty do
    result := { result with findings := result.findings.push { location := "definition-value", categories := cats } }
  return result

def inMeta (env : Environment) (action : MetaM α) : IO α := do
  let hb ← IO.getNumHeartbeats
  let ctx : Core.Context := {
    fileName := "<RH-stage2-semantic>"
    fileMap := default
    initHeartbeats := hb
    maxHeartbeats := 2000000
    maxRecDepth := 2000
  }
  let (value, _, _) ← action.toIO ctx { env }
  return value

def smoke (env : Environment) : IO Unit := do
  for (name, expected) in #[("truthAlias", 0), ("zeroLinear", 2), ("zeroMeasure", 3)] do
    let some ci := env.checked.get.find? (RHStage2.nameOf ("RHStage2SemanticFixture." ++ name)) |
      throw (IO.userError "Semantic fixture declaration missing")
    let a ← inMeta env (analyzeDefinition ci)
    unless a.findings.any (fun f => f.categories.contains expected) do
      throw (IO.userError s!"Semantic fixture missed {name}")
  for name in #["equalityPredicate", "identityLinear"] do
    let some ci := env.checked.get.find? (RHStage2.nameOf ("RHStage2SemanticFixture." ++ name)) |
      throw (IO.userError "Semantic negative fixture declaration missing")
    let a ← inMeta env (analyzeDefinition ci)
    if a.findings.any (fun f => f.categories.contains 0 || f.categories.contains 2) then
      throw (IO.userError s!"Semantic false positive on {name}")
  let some record := env.checked.get.find? `RHStage2SemanticFixture.record |
    throw (IO.userError "Record fixture missing")
  let a ← inMeta env (analyzeDefinition record)
  unless a.findings.any (fun f => f.categories.contains 1) do
    throw (IO.userError "Unit-typed record field fixture not recognized")
  RHStage2.emit [("event", toJson "semantic-smoke-passed")]

def run (env : Environment) (roots : Array Name) (cohort : String) : IO Unit := do
  let mut seen : NameSet := {}
  let mut names : Array Name := #[]
  for n in roots do
    unless (env.checked.get.find? n).isSome do throw (IO.userError s!"Missing semantic root: {n}")
    unless seen.contains n do
      seen := seen.insert n
      names := names.push n
  let mut buckets : Array RHStage2.Bucket := #[]
  let mut cursor := 0
  let mut definitions := 0
  let mut completedDefinitions := 0
  let mut unknown := 0
  let mut fields := 0
  let mut depthLimited := 0
  let mut unknownExamples : Array String := #[]
  let mut missing : Array String := #[]
  while cursor < names.size do
    let n := names[cursor]!
    match env.checked.get.find? n with
    | none => missing := missing.push n.toString
    | some ci =>
        let deps := ci.type.getUsedConstants ++
          match RHStage2.bodyOf ci with
          | some b => b.getUsedConstants
          | none => #[]
        for d in deps do
          unless seen.contains d do
            seen := seen.insert d
            names := names.push d
        match ci with
        | .defnInfo _ =>
            definitions := definitions + 1
            try
              let a ← inMeta env (analyzeDefinition ci)
              completedDefinitions := completedDefinitions + 1
              fields := fields + a.constructorFieldsVisited
              if a.recordDepthBoundReached then depthLimited := depthLimited + 1
              let mut definitionCats : Array Nat := #[]
              for f in a.findings do
                for c in f.categories do
                  unless definitionCats.contains c do definitionCats := definitionCats.push c
                buckets := RHStage2.bump buckets "classified-sites/overlapping-categories" f.categories
                  (Name.str n f.location)
              buckets := RHStage2.bump buckets "definitions/at-least-one-hit" definitionCats n
              buckets := RHStage2.bump buckets ("origin/" ++ RHStage2.originOf env n ++ "/definitions") definitionCats n
            catch e =>
              unknown := unknown + 1
              if unknownExamples.size < 20 then unknownExamples := unknownExamples.push s!"{n}: {e}"
        | _ => pure ()
    cursor := cursor + 1
    if cursor % 5000 == 0 then
      RHStage2.progress s!"Semantic {cohort}: {cursor} declarations; {completedDefinitions} completed definitions; {unknown} unknown"
    if names.size > 2000000 then throw (IO.userError "Semantic union exceeded 2,000,000 nodes")
  for b in buckets do
    RHStage2.emit [("event", toJson "semantic-bucket"), ("cohort", toJson cohort),
      ("bucket", toJson b.key), ("denominator", toJson b.count),
      ("category_labels", toJson labels), ("counts", toJson b.hits), ("samples", toJson b.samples)]
  RHStage2.emit [("event", toJson "semantic-complete"), ("cohort", toJson cohort),
    ("closure_declarations", toJson names.size), ("definitions_attempted", toJson definitions),
    ("definitions_completed", toJson completedDefinitions), ("definitions_unknown", toJson unknown),
    ("constructor_fields_visited", toJson fields), ("definitions_with_record_depth_limit", toJson depthLimited),
    ("unknown_examples", toJson unknownExamples), ("missing", toJson missing),
    ("witness_vs_ordinary_role_classification", toJson "not established globally; do not infer from value classification"),
    ("semantic_tests_are_independent_kernel_checks", toJson false)]
  unless missing.isEmpty do throw (IO.userError "Missing declarations in semantic traversal")
end RHStage2Semantic

unsafe def main (args : List String) : IO UInt32 := do
  try
    Lean.initSearchPath (← Lean.findSysroot)
    let mode := args.headD ""
    unless #["semantic-smoke", "semantic-control", "semantic-main"].contains mode do
      throw (IO.userError "Semantic mode required")
    let mod := if mode == "semantic-smoke" then `SemanticFixture else
      if mode == "semantic-control" then `Mathlib else `Main
    RHStage2.progress s!"Semantic import {mod}; environment extensions are loaded for instance/structure metadata"
    -- Required by Lean's dynamic-import API when loadExts is true. Imports
    -- and analysis run sequentially in this isolated tool process. Imported
    -- compacted regions are retained until this process exits.
    Lean.enableInitializersExecution
    let env ← Lean.importModules #[{ module := mod }] {} (loadExts := true)
    if mode == "semantic-smoke" then RHStage2Semantic.smoke env
    else if mode == "semantic-control" then
      if (env.checked.get.find? `riemannHypothesis).isSome then
        throw (IO.userError "Project theorem unexpectedly present in Mathlib control")
      RHStage2Semantic.run env #[`Nat.exists_infinite_primes, `Real.exp_add,
        `MeasureTheory.integral_add] "independent-Mathlib-control"
    else RHStage2Semantic.run env RHStage2.roots "five-headline-reference-union"
    return 0
  catch e =>
    IO.eprintln s!"RH_STAGE2_SEMANTIC_ERROR: {e}"
    return 1
