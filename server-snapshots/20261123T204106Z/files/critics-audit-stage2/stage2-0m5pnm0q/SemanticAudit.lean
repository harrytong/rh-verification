import Lean

/- Read-only stored-syntax analysis. This is not an independent kernel.
   The fixture is imported only in a separate smoke-test process.
   No definition in the imported environment is changed. -/
open Lean
namespace RHStage2

def nameOf (s : String) : Name :=
  (s.splitOn ".").foldl Name.str Name.anonymous

def emit (fields : List (String × Json)) : IO Unit := do
  IO.println ("RH_STAGE2_JSON\t" ++ (Json.mkObj fields).compress)
  (← IO.getStdout).flush

def progress (s : String) : IO Unit := do
  IO.println ("RH_STAGE2_PROGRESS\t" ++ s)
  (← IO.getStdout).flush

def moduleOf (env : Environment) (n : Name) : String :=
  match env.getModuleIdxFor? n with
  | some i => match env.header.moduleNames[i.toNat]? with
    | some m => m.toString
    | none => "<invalid module index>"
  | none => "<no module index>"

def bodyOf : ConstantInfo → Option Expr
  | .defnInfo v => some v.value
  | .thmInfo v => some v.value
  | .opaqueInfo v => some v.value
  | _ => none

def kindOf : ConstantInfo → String
  | .axiomInfo _ => "axiom"
  | .defnInfo _ => "definition"
  | .thmInfo _ => "theorem"
  | .opaqueInfo _ => "opaque"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "constructor"
  | .recInfo _ => "recursor"
  | .quotInfo _ => "quotient-primitive"

def mentions (e : Expr) (n : Name) : Bool := e.getUsedConstants.contains n

/- Drop only explicit, syntactically unused let bindings or lambda arguments.
   No delta unfolding, proof irrelevance, theorem rewriting, eta reduction,
   implicit-argument deletion, or declaration-signature editing is attempted.
   instantiate1 performs the necessary de Bruijn index adjustment. -/
structure TrimState where
  remaining : Nat := 20000
  droppedLets : Nat := 0
  droppedBetaArgs : Nat := 0
  truncated : Bool := false

partial def occursAt (e : Expr) (k : Nat) (depth : Nat := 0) : StateM TrimState Bool := do
  let st ← get
  if st.remaining == 0 || depth > 800 then
    modify fun s => { s with truncated := true }
    -- Conservatively retain a binding when occurrence analysis is incomplete.
    return true
  modify fun s => { s with remaining := s.remaining - 1 }
  match e with
  | .bvar i => return i == k
  | .app f a =>
      if ← occursAt f k (depth + 1) then return true
      occursAt a k (depth + 1)
  | .lam _ t b _ | .forallE _ t b _ =>
      if ← occursAt t k (depth + 1) then return true
      occursAt b (k + 1) (depth + 1)
  | .letE _ t v b _ =>
      if ← occursAt t k (depth + 1) then return true
      if ← occursAt v k (depth + 1) then return true
      occursAt b (k + 1) (depth + 1)
  | .mdata _ b | .proj _ _ b => occursAt b k (depth + 1)
  | _ => return false

partial def trim (e : Expr) (depth : Nat := 0) : StateM TrimState Expr := do
  let st ← get
  if st.remaining == 0 || depth > 800 then
    modify fun s => { s with truncated := true }
    return e
  modify fun s => { s with remaining := s.remaining - 1 }
  match e with
  | .letE _ _ _ b _ =>
      -- hasLooseBVars is a constant-time negative shortcut. occursAt handles
      -- outer variables, so a used outer parameter does not block removal.
      let used ← if !b.hasLooseBVars then pure false else occursAt b 0 (depth + 1)
      if !used then
        modify fun s => { s with droppedLets := s.droppedLets + 1 }
        return ← trim (b.instantiate1 (.sort .zero)) (depth + 1)
      else
        match e with
        | .letE n t v b nd =>
          let t' ← trim t (depth + 1)
          let v' ← trim v (depth + 1)
          let b' ← trim b (depth + 1)
          return .letE n t' v' b' nd
        | _ => return e
  | .app f a =>
      let f' ← trim f (depth + 1)
      match f' with
      | .lam _ _ b _ =>
          let used ← if !b.hasLooseBVars then pure false else occursAt b 0 (depth + 1)
          if !used then
            modify fun s => { s with droppedBetaArgs := s.droppedBetaArgs + 1 }
            return ← trim (b.instantiate1 (.sort .zero)) (depth + 1)
          else
            let a' ← trim a (depth + 1)
            return .app f' a'
      | _ =>
          let a' ← trim a (depth + 1)
          return .app f' a'
  | .lam n t b bi =>
      let t' ← trim t (depth + 1)
      let b' ← trim b (depth + 1)
      return .lam n t' b' bi
  | .forallE n t b bi =>
      let t' ← trim t (depth + 1)
      let b' ← trim b (depth + 1)
      return .forallE n t' b' bi
  | .mdata md b => return .mdata md (← trim b (depth + 1))
  | .proj n i b => return .proj n i (← trim b (depth + 1))
  | _ => return e

def trimmed (e : Expr) : Expr × TrimState := (trim e).run {}

/- These regions describe all *direct syntactic references* in the stored
   signature. A binder may be a type parameter, instance, data, or hypothesis.
   Nothing here infers that a binder domain is a proposition. -/
partial def typeRegions (e : Expr) (target : Name) (i := 0) : Array String :=
  match e with
  | .forallE n t b _ =>
      let here := if mentions t target then #[s!"binder-domain[{i}]:{n}"] else #[]
      here ++ typeRegions b target (i + 1)
  | .letE n t v b _ =>
      let tHit := if mentions t target then #[s!"signature-let-type:{n}"] else #[]
      let vHit := if mentions v target then #[s!"signature-let-value:{n}"] else #[]
      tHit ++ vHit ++ typeRegions b target i
  | .mdata _ b => typeRegions b target i
  | _ => if mentions e target then #["conclusion-type"] else #[]

def structuralLabels (ci : ConstantInfo) (target : Name) : Array String := Id.run do
  let mut result : Array String := #[]
  match ci with
  | .inductInfo v =>
      if v.ctors.contains target then result := result.push "inductive-constructor"
      if v.all.contains target then result := result.push "mutual-inductive"
  | .ctorInfo v =>
      if v.induct == target then result := result.push "constructor-parent"
  | .recInfo v =>
      if v.all.contains target then result := result.push "recursor-inductive"
      for r in v.rules do
        if r.ctor == target then result := result.push "recursor-constructor"
        if mentions r.rhs target then result := result.push "recursor-rule-rhs"
  | _ => pure ()
  return result

def inspectEdges (env : Environment) (requestPath : String) : IO Unit := do
  let text ← IO.FS.readFile requestPath
  let mut count := 0
  for line in text.splitOn "\n" do
    unless line.isEmpty do
      let fields := line.splitOn "\t"
      let [source, target] := fields | throw (IO.userError "Malformed edge request")
      let s := nameOf source
      let t := nameOf target
      let some ci := env.checked.get.find? s | throw (IO.userError s!"Missing source: {s}")
      unless (env.checked.get.find? t).isSome do
        throw (IO.userError s!"Missing edge target: {t}")
      let regions := typeRegions ci.type t
      let structural := structuralLabels ci t
      let (rawBody, prunedBody, droppedLets, droppedBeta, truncated) :=
        match bodyOf ci with
        | none => (false, false, 0, 0, false)
        | some b =>
            let (b', st) := trimmed b
            (mentions b t, mentions b' t, st.droppedLets, st.droppedBetaArgs, st.truncated)
      let bodyLabel := match ci with
        | .thmInfo _ => "proof-body"
        | .opaqueInfo _ => "opaque-body"
        | .defnInfo _ => "definition-body"
        | _ => "no-body"
      unless !regions.isEmpty || rawBody || !structural.isEmpty do
        throw (IO.userError s!"Previous witness edge not reproduced: {s} -> {t}")
      emit [("event", toJson "edge-classification"), ("source", toJson source),
        ("target", toJson target), ("source_kind", toJson (kindOf ci)),
        ("source_module", toJson (moduleOf env s)),
        ("signature_regions", toJson regions), ("body_region", toJson bodyLabel),
        ("raw_body_reference", toJson rawBody), ("trimmed_body_reference", toJson prunedBody),
        ("structural_regions", toJson structural),
        ("trimmed_direct_reference", toJson (!regions.isEmpty || prunedBody)),
        ("dropped_unused_lets", toJson droppedLets),
        ("dropped_explicit_unused_lambda_arguments", toJson droppedBeta),
        ("trim_truncated", toJson truncated)]
      count := count + 1
      if count % 10 == 0 then progress s!"Classified {count} witness edges"
  emit [("event", toJson "edges-complete"), ("pairs", toJson count)]

def roots : Array Name := (#["riemannHypothesis", "riemannZeta_eq_zero_re",
  "LFunction_ne_zero_of_half_lt_re", "LFunction_eq_zero_re",
  "LFunction_eq_zero_re_of_isPrimitive"] : Array String).map nameOf

def storedStatements (env : Environment) : IO Unit := do
  for n in roots.push `RiemannHypothesis do
    let some ci := env.checked.get.find? n | throw (IO.userError s!"Missing statement: {n}")
    emit [("event", toJson "stored-statement"), ("name", toJson n.toString),
      ("kind", toJson (kindOf ci)), ("module", toJson (moduleOf env n)),
      ("raw_type_expr", toJson (reprStr ci.type))]
    if n == `RiemannHypothesis then
      let some b := bodyOf ci | throw (IO.userError "RiemannHypothesis is not a definition")
      emit [("event", toJson "stored-RiemannHypothesis-definition"),
        ("raw_value_expr", toJson (reprStr b))]

partial def peelLambdas (e : Expr) (n := 0) : Nat × Expr :=
  match e with
  | .lam _ _ b _ => peelLambdas b (n + 1)
  | .mdata _ b => peelLambdas b n
  | _ => (n, e)

def zeroHead (e : Expr) : Bool :=
  let args : Array Expr := e.getAppArgs
  let numeralIsZero : Bool :=
    match args[1]? with
    | some (Expr.lit (Literal.natVal 0)) => true
    | _ => false
  match e.getAppFn with
  | .const n _ =>
      n == `Zero.zero || (n == `OfNat.ofNat && numeralIsZero)
  | Expr.lit (Literal.natVal 0) => true
  | _ => false

def categoryLabels : Array String := #["body-after-lambdas-is-True",
  "body-after-lambdas-is-False", "body-after-lambdas-is-PUnit-or-Unit",
  "body-after-lambdas-has-zero-notation-head", "body-after-lambdas-is-bare-constant",
  "lambda-body-has-no-loose-bound-variables", "zero-head-and-type-mentions-map-vocabulary"]

def categories (ci : ConstantInfo) : Array Nat := Id.run do
  let some v := bodyOf ci | return #[]
  let (arity, e) := peelLambdas v
  let fn := e.getAppFn
  let mut cats := #[]
  if fn.isConstOf `True && e.getAppArgs.isEmpty then cats := cats.push 0
  if fn.isConstOf `False && e.getAppArgs.isEmpty then cats := cats.push 1
  if (fn.isConstOf `PUnit || fn.isConstOf `Unit) && e.getAppArgs.isEmpty then
    cats := cats.push 2
  if zeroHead e then cats := cats.push 3
  match e with
  | .const _ _ => cats := cats.push 4
  | _ => pure ()
  if arity > 0 && !e.hasLooseBVars then cats := cats.push 5
  if zeroHead e && (ci.type.getUsedConstants.any fun n =>
      #[`LinearMap, `ContinuousLinearMap, `AddMonoidHom, `MonoidHom, `RingHom].contains n) then
    cats := cats.push 6
  return cats

def originOf (env : Environment) (n : Name) : String :=
  let m := moduleOf env n
  if m == "Mathlib" || m.startsWith "Mathlib." then "Mathlib"
  else if m.startsWith "Init." || m.startsWith "Lean." || m.startsWith "Std." ||
      m == "Init" || m == "Lean" || m == "Std" then "Lean-core"
  else "other-project-or-package"

structure Bucket where
  key : String
  count : Nat := 0
  hits : Array Nat := Array.replicate 7 0
  samples : Array (Array String) := Array.replicate 7 #[]
  deriving Inhabited

def bump (buckets : Array Bucket) (key : String) (cats : Array Nat) (n : Name) : Array Bucket := Id.run do
  let i := (buckets.findIdx? fun b => b.key == key).getD buckets.size
  let mut bs := if i == buckets.size then buckets.push { key } else buckets
  let mut b := bs[i]!
  b := { b with count := b.count + 1 }
  for c in cats do
    b := { b with hits := b.hits.set! c (b.hits[c]! + 1) }
    if b.samples[c]!.size < 12 then
      b := { b with samples := b.samples.set! c (b.samples[c]!.push n.toString) }
  bs := bs.set! i b
  return bs

/- Streaming union closure. Reference edges only, matching the first audit's
   non-structural mode: stored types and explicit definition/theorem/opaque
   bodies. No complete edge graph is retained in memory. -/
def census (env : Environment) (initial : Array Name) (label : String)
    (pruneBodies := false) (watchFile := "") : IO Unit := do
  let mut names : Array Name := #[]
  let mut seen : NameSet := {}
  for n in initial do
    unless (env.checked.get.find? n).isSome do
      throw (IO.userError s!"Census root absent: {n}")
    unless seen.contains n do
      seen := seen.insert n
      names := names.push n
  let mut buckets : Array Bucket := #[]
  let mut cursor := 0
  let mut missing : Array String := #[]
  let mut axioms : Array String := #[]
  let mut droppedLets := 0
  let mut droppedBeta := 0
  let mut truncatedBodies := 0
  while cursor < names.size do
    let n := names[cursor]!
    match env.checked.get.find? n with
    | none => missing := missing.push n.toString
    | some ci =>
        if ci.isAxiom then axioms := axioms.push n.toString
        let cats := categories ci
        buckets := bump buckets "all-kinds/all-origins" cats n
        buckets := bump buckets ("kind/" ++ kindOf ci) cats n
        buckets := bump buckets ("origin/" ++ originOf env n ++ "/" ++ kindOf ci) cats n
        let mut bodyDeps : Array Name := #[]
        match bodyOf ci with
        | some b =>
            if pruneBodies then
              let (b', st) := trimmed b
              bodyDeps := b'.getUsedConstants
              droppedLets := droppedLets + st.droppedLets
              droppedBeta := droppedBeta + st.droppedBetaArgs
              if st.truncated then truncatedBodies := truncatedBodies + 1
            else bodyDeps := b.getUsedConstants
        | none => pure ()
        let ds := ci.type.getUsedConstants ++ bodyDeps
        for d in ds do
          unless seen.contains d do
            seen := seen.insert d
            names := names.push d
    cursor := cursor + 1
    if cursor % 25000 == 0 then progress s!"Census {label}: {cursor} expanded, {names.size} discovered"
    if names.size > 2000000 then
      throw (IO.userError "Census exceeded 2,000,000 declarations; incomplete")
  for b in buckets do
    emit [("event", toJson "census-bucket"), ("cohort", toJson label),
      ("bucket", toJson b.key), ("declarations", toJson b.count),
      ("category_labels", toJson categoryLabels), ("counts", toJson b.hits),
      ("samples", toJson b.samples)]
  emit [("event", toJson "census-complete"), ("cohort", toJson label),
    ("roots", toJson (initial.map Name.toString)), ("declarations", toJson names.size),
    ("missing", toJson missing), ("axioms", toJson axioms),
    ("pruned_bodies", toJson pruneBodies), ("dropped_unused_lets", toJson droppedLets),
    ("dropped_unused_explicit_beta_arguments", toJson droppedBeta),
    ("bodies_with_bounded_pruning", toJson truncatedBodies)]
  unless watchFile.isEmpty do
    let text ← IO.FS.readFile watchFile
    for s in text.splitOn "\n" do
      unless s.isEmpty do
        emit [("event", toJson "union-watch"), ("cohort", toJson label),
          ("target", toJson s), ("reachable_from_any_root", toJson (seen.contains (nameOf s)))]
  unless missing.isEmpty do throw (IO.userError "Incomplete census: missing declarations")

def smoke (env : Environment) : IO Unit := do
  let rawZero : Expr := Expr.lit (Literal.natVal 0)
  let rawOne : Expr := Expr.lit (Literal.natVal 1)
  unless zeroHead rawZero && !zeroHead rawOne do
    throw (IO.userError "Raw literal zero classifier failed")
  unless zeroHead (mkNatLit 0) && !zeroHead (mkNatLit 1) do
    throw (IO.userError "Frontend numeral zero classifier failed")
  -- mkNatLit already wraps a raw literal in OfNat.ofNat at this pin.
  -- The numeric index argument below must itself be RAW, not mkNatLit.
  let ofNatZero := mkAppN (mkConst `OfNat.ofNat [.zero])
    #[mkConst `Nat, rawZero, mkInstOfNatNat rawZero]
  let ofNatOne := mkAppN (mkConst `OfNat.ofNat [.zero])
    #[mkConst `Nat, rawOne, mkInstOfNatNat rawOne]
  unless zeroHead ofNatZero && !zeroHead ofNatOne do
    throw (IO.userError "OfNat zero classifier failed")
  let some ci := env.checked.get.find? `RHStage2Fixture.regions |
    throw (IO.userError "Fixture not imported")
  let rs := typeRegions ci.type `RHStage2Fixture.Marker
  unless rs.contains "binder-domain[0]:h" && rs.contains "conclusion-type" do
    throw (IO.userError "Binder/conclusion classifier failed")
  let marker := mkConst `RHStage2Fixture.fakePremise
  let trueIntro := mkConst `True.intro
  let raw := Expr.letE `unused (mkConst `True) marker trueIntro true
  let (p, st) := trimmed raw
  unless mentions raw `RHStage2Fixture.fakePremise &&
      !mentions p `RHStage2Fixture.fakePremise && st.droppedLets == 1 && !st.truncated do
    throw (IO.userError "Unused-let elimination failed")
  let used := Expr.letE `used (mkConst `True) marker (.bvar 0) false
  let (pUsed, _) := trimmed used
  unless mentions pUsed `RHStage2Fixture.fakePremise do
    throw (IO.userError "Pruner deleted a used let")
  let beta := Expr.app (.lam `unused (mkConst `True) trueIntro .default) marker
  let (pBeta, stBeta) := trimmed beta
  unless !mentions pBeta `RHStage2Fixture.fakePremise && stBeta.droppedBetaArgs == 1 do
    throw (IO.userError "Unused explicit beta argument elimination failed")
  let outer := Expr.letE `unused (mkConst `True) marker (.bvar 1) false
  let (pOuter, _) := trimmed outer
  unless pOuter == Expr.bvar 0 do throw (IO.userError "de Bruijn index adjustment failed")
  let (bounded, boundedSt) := (trim raw).run { remaining := 0 }
  unless bounded == raw && boundedSt.truncated do
    throw (IO.userError "Truncation must retain the original subtree")
  for (n, expected) in #[("alwaysTrue", 0), ("unitType", 2), ("constantNat", 5)] do
    let some d := env.checked.get.find? (nameOf ("RHStage2Fixture." ++ n)) |
      throw (IO.userError "Missing census fixture")
    unless (categories d).contains expected do
      throw (IO.userError s!"Census classifier failed for {n}")
  let some ident := env.checked.get.find? `RHStage2Fixture.identityNat |
    throw (IO.userError "Missing identity fixture")
  if (categories ident).contains 5 then
    throw (IO.userError "Identity function misclassified as closed constant function")
  emit [("event", toJson "smoke-passed"),
    ("meaning", toJson "Tool fixture only; not an RH check")]

end RHStage2

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

def main (args : List String) : IO UInt32 := do
  try
    Lean.initSearchPath (← Lean.findSysroot)
    let mode := args.headD ""
    unless #["semantic-smoke", "semantic-control", "semantic-main"].contains mode do
      throw (IO.userError "Semantic mode required")
    let mod := if mode == "semantic-smoke" then `SemanticFixture else
      if mode == "semantic-control" then `Mathlib else `Main
    RHStage2.progress s!"Semantic import {mod}; environment extensions are loaded for instance/structure metadata"
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
