import Lean
set_option pp.fullNames true
set_option pp.universes true
/- Shared verbatim by the fixture and project probe. No environment mutation.
   Only selected stored proof bodies are traversed; callees are not expanded.
   Reduction for comparison is bounded by the enclosing Core heartbeat budget. -/
open Lean Meta
namespace RHStage4
def nameOf (s : String) : Name :=
  (s.splitOn ".").foldl Name.str Name.anonymous
def headName (e : Expr) : Option Name :=
  match e.getAppFn with
  | .const n _ => some n
  | _ => none
def bodyOf : ConstantInfo → Option Expr
  | .defnInfo v => some v.value
  | .thmInfo v => some v.value
  | .opaqueInfo v => some v.value
  | _ => none
def emit (fields : List (String × Json)) : IO Unit := do
  IO.println ("RH_STAGE4_JSON\t" ++ (Json.mkObj fields).compress)
  (← IO.getStdout).flush
def emitMeta (fields : List (String × Json)) : MetaM Unit :=
  liftM (emit fields)

def inMeta (env : Environment) (action : MetaM α) : IO α := do
  let hb ← IO.getNumHeartbeats
  let ctx : Core.Context := {
    fileName := "<RH-stage4>"
    fileMap := default
    initHeartbeats := hb
    maxHeartbeats := 10000000
    maxRecDepth := 2000
  }
  let (value, _, _) ← action.toIO ctx { env }
  return value
def clipped (s : String) (limit : Nat := 6000) : Json :=
  Json.mkObj [("text", toJson (String.ofList (s.toList.take limit))),
    ("truncated", toJson (decide (s.length > limit)))]
def printed (e : Expr) : MetaM Json := do
  return clipped (← ppExpr e).pretty
def context : MetaM Json := do
  let mut rows : Array Json := #[]
  for d in (← getLCtx) do
    let letValue ← match d.value? with
      | some v => printed v
      | none => pure Json.null
    rows := rows.push (Json.mkObj [
      ("name", toJson d.userName.toString), ("type", ← printed d.type),
      ("let_value", letValue)])
  return Json.arr rows

-- No propositional hypotheses are rewritten into the sides. Local let values
-- are available for definitional reduction. Non-defeq is not "unprovable".
def comparison (owner location callee : String) (ty : Expr) : MetaM Unit := do
  -- Preserve the relation application before whnf can unfold its instance.
  let direct := #[``Eq, ``LE.le, ``LT.lt].any (fun n => headName ty == some n)
  let b ← if direct then pure ty else withTransparency .reducible <| whnf ty
  let args := b.getAppArgs
  let head := headName b
  let relation := if head == some ``Eq then "Eq"
    else if head == some ``LE.le then "LE.le"
    else if head == some ``LT.lt then "LT.lt" else "other"
  let base := [("event",toJson "comparison"),("owner",toJson owner),
    ("location",toJson location),("callee",toJson callee),
    ("relation",toJson relation)]
  if relation == "other" || args.size < 2 then
    emitMeta (base ++ [("status",toJson "not-a-direct-comparison"),
      ("type", ← printed ty),("reduced_type", ← printed b)])
    return ()
  let lhs := args[args.size - 2]!
  let rhs := args[args.size - 1]!
  if lhs.hasMVar || rhs.hasMVar then
    emitMeta (base ++ [("status",toJson "unknown-metavariables")])
    return ()
  let same ← withTransparency .all <| isDefEq lhs rhs
  emitMeta (base ++ [("status",toJson (if same then "definitionally-identical" else "not-definitionally-identical")),
    ("lhs", ← printed lhs),("rhs", ← printed rhs),
    ("local_context", ← context),
    ("transparency",toJson "all"),
    ("meaning",toJson "identity of sides only; not a necessity or RH verdict")])

structure Scan where
  visited : Nat := 0
  hits : Nat := 0
  capped : Bool := false
  firstMatch : Bool := false
  pruned : Nat := 0

-- Look only at maximal application spines. Recurse into their arguments and
-- nonconstant function heads. Enter lambdas/lets with the real local context.
-- Binder annotations are excluded from call-site evidence.
partial def walk (owner : String) (watch : Array Name) (e : Expr)
    (path : String) (depth : Nat) (ref : IO.Ref Scan) : MetaM Unit := do
  let s ← ref.get
  if s.firstMatch && s.hits > 0 then return ()
  if s.visited >= 250000 || depth > 600 || s.hits >= 64 then
    ref.modify fun s => { s with capped := true }
    return ()
  ref.modify fun s => { s with visited := s.visited + 1 }
  -- Necessary syntactic condition for a direct application in this subtree.
  -- getUsedConstants may also see binder annotations; that can retain extra
  -- branches but cannot justify inventing a call. No constant bodies unfold.
  let refs := e.getUsedConstants
  if !(watch.any fun n => refs.contains n) then
    ref.modify fun s => { s with pruned := s.pruned + 1 }
    return ()
  match e with
  | .lam n t b bi =>
    withLocalDecl n bi t fun x => walk owner watch (b.instantiate1 x) (path ++ "/lambda") (depth+1) ref
  | .letE n t v b _ =>
    withLetDecl n t v fun x => walk owner watch (b.instantiate1 x) (path ++ "/let-body") (depth+1) ref
    walk owner watch v (path ++ "/let-value") (depth+1) ref
  | .app .. =>
    let fn := e.getAppFn
    let args := e.getAppArgs
    if let some n := headName fn then
      if watch.contains n then
        ref.modify fun s => { s with hits := s.hits + 1 }
        comparison owner path n.toString (← inferType e)
    else
      walk owner watch fn (path ++ "/function") (depth+1) ref
    for i in (List.range args.size).reverse do
      walk owner watch args[i]! (path ++ s!"/arg-{i}") (depth+1) ref
  | .mdata _ b => walk owner watch b (path ++ "/metadata") (depth+1) ref
  | .proj _ _ b => walk owner watch b (path ++ "/projection") (depth+1) ref
  | _ => pure ()

partial def conclusion (target : String) (ty : Expr) : MetaM Unit := do
  match ty with
  | .forallE n t b bi =>
    withLocalDecl n bi t fun x => conclusion target (b.instantiate1 x)
  | .mdata _ b => conclusion target b
  | _ => comparison target "generic-conclusion" "" ty

def generic (env : Environment) (target : String) : IO Unit := do
  emit [("event",toJson "generic-start"),("owner",toJson target)]
  try
    let some ci := env.checked.get.find? (nameOf target) |
      throw (IO.userError "Target not found")
    inMeta env <| conclusion target ci.type
    emit [("event",toJson "generic-end"),("owner",toJson target),("status",toJson "completed")]
  catch e =>
    emit [("event",toJson "generic-end"),("owner",toJson target),
      ("status",toJson "unknown"),("error",toJson e.toString)]

def calls (env : Environment) (owner : String) (watch : Array String)
    (firstMatch : Bool := false) : IO Unit := do
  let ref ← IO.mkRef ({ firstMatch := firstMatch } : Scan)
  emit [("event",toJson "calls-start"),("owner",toJson owner),("watch",toJson watch),
    ("first_match_only",toJson firstMatch),
    ("order",toJson "last-argument-first; let-body-before-let-value")]
  try
    let some ci := env.checked.get.find? (nameOf owner) |
      throw (IO.userError "Owner not found")
    let some b := bodyOf ci | throw (IO.userError "Owner has no stored body")
    let refs := b.getUsedConstants
    emit [("event",toJson "body-references"),("owner",toJson owner),
      ("reference_count",toJson refs.size),
      ("references",toJson ((refs.toList.take 256).map Name.toString)),
      ("references_truncated",toJson (decide (refs.size > 256))),
      ("watched_present",toJson (watch.filter fun n => refs.contains (nameOf n)))]
    inMeta env <| walk owner (watch.map nameOf) b "body" 0 ref
    let s ← ref.get
    emit [("event",toJson "calls-end"),("owner",toJson owner),
      ("status",toJson (if firstMatch && s.hits > 0 then "first-match-observed" else
        if s.capped then "incomplete-cap" else "completed")),
      ("scan_capped",toJson s.capped),
      ("pruned_subtrees",toJson s.pruned),
      ("visited",toJson s.visited),("hits",toJson s.hits)]
  catch e =>
    let s ← ref.get
    emit [("event",toJson "calls-end"),("owner",toJson owner),
      ("status",toJson "unknown"),("visited",toJson s.visited),
      ("pruned_subtrees",toJson s.pruned),
      ("hits",toJson s.hits),("error",toJson e.toString)]
end RHStage4

/- Stage 4 v0.5: first stored application, with dependent argument types.
   This file follows ComparisonProbe.lean.txt in both generated probes. -/
namespace RHStage4
partial def argumentConclusion (owner location callee : String) (ty : Expr) : MetaM Unit := do
  match ty with
  | .forallE n t b bi =>
    emitMeta [("event", toJson "argument-binder"), ("owner", toJson owner),
      ("location", toJson location), ("callee", toJson callee),
      ("name", toJson n.toString), ("type", ← printed t)]
    withLocalDecl n bi t fun x => argumentConclusion owner location callee (b.instantiate1 x)
  | .mdata _ b => argumentConclusion owner location callee b
  | _ => comparison owner location callee ty

partial def argumentShape (e : Expr) : String :=
  match e with
  | .mdata _ b => argumentShape b
  | .fvar _ => "local-reference"
  | .lam .. => "lambda"
  | .letE .. => "let"
  | .proj .. => "projection"
  | .const .. => "constant"
  | .app .. => "application"
  | _ => "other"

def inspectArguments (owner path callee : String) (e : Expr)
    (selected compared : Array String) : MetaM Unit := do
  let args := e.getAppArgs
  let mut ty ← inferType e.getAppFn
  let mut found : Array String := #[]
  for i in List.range args.size do
    let bt ← whnf ty
    match bt with
    | .forallE n expected body _ =>
      let a := args[i]!
      let param := n.toString
      if selected.contains param then
        found := found.push param
        let refs := a.getUsedConstants
        let loc := path ++ "/parameter-" ++ param ++ s!"-{i}"
        emitMeta [("event", toJson "argument"), ("owner", toJson owner),
          ("callee", toJson callee), ("location", toJson loc),
          ("parameter", toJson param), ("argument_index", toJson i),
          ("argument_shape", toJson (argumentShape a)),
          ("argument", clipped (← ppExpr a).pretty 24000),
          ("expected_type", ← printed expected),
          ("local_context", ← context),
          ("references", toJson ((refs.toList.take 256).map Name.toString)),
          ("reference_count", toJson refs.size),
          ("references_truncated", toJson (decide (refs.size > 256))),
          ("comparison_requested", toJson (compared.contains param)),
          ("scope", toJson "actual argument at this stored wrapper call; not a transitive headline specialization")]
        if compared.contains param then
          argumentConclusion owner loc callee expected
      ty := body.instantiate1 a
    | _ =>
      throwError "Application telescope ended before argument {i}"
  emitMeta [("event", toJson "arguments-end"), ("owner", toJson owner),
    ("callee", toJson callee), ("location", toJson path),
    ("supplied_argument_count", toJson args.size),
    ("selected", toJson selected), ("found", toJson found),
    ("missing", toJson (selected.filter fun n => !(found.contains n)))]

-- Same bounded traversal policy as the v0.4 scanner. Proof arguments themselves
-- are recorded at the first match; this does not recursively expand constants.
partial def argumentWalk (owner callee : String) (selected compared : Array String)
    (e : Expr) (path : String) (depth : Nat) (ref : IO.Ref Scan) : MetaM Unit := do
  let s ← ref.get
  if s.hits > 0 then return ()
  if s.visited >= 250000 || depth > 600 then
    ref.modify fun s => { s with capped := true }
    return ()
  ref.modify fun s => { s with visited := s.visited + 1 }
  if !(e.getUsedConstants.contains (nameOf callee)) then
    ref.modify fun s => { s with pruned := s.pruned + 1 }
    return ()
  match e with
  | .lam n t b bi =>
    withLocalDecl n bi t fun x => argumentWalk owner callee selected compared
      (b.instantiate1 x) (path ++ "/lambda") (depth+1) ref
  | .letE n t v b _ =>
    withLetDecl n t v fun x => argumentWalk owner callee selected compared
      (b.instantiate1 x) (path ++ "/let-body") (depth+1) ref
    argumentWalk owner callee selected compared v (path ++ "/let-value") (depth+1) ref
  | .app .. =>
    let fn := e.getAppFn
    let args := e.getAppArgs
    if headName fn == some (nameOf callee) then
      ref.modify fun s => { s with hits := s.hits + 1 }
      inspectArguments owner path callee e selected compared
    else if (headName fn).isNone then
      argumentWalk owner callee selected compared fn (path ++ "/function") (depth+1) ref
    for i in (List.range args.size).reverse do
      argumentWalk owner callee selected compared args[i]! (path ++ s!"/arg-{i}") (depth+1) ref
  | .mdata _ b => argumentWalk owner callee selected compared b (path ++ "/metadata") (depth+1) ref
  | .proj _ _ b => argumentWalk owner callee selected compared b (path ++ "/projection") (depth+1) ref
  | _ => pure ()

def argumentCalls (env : Environment) (owner callee : String)
    (selected compared : Array String) : IO Unit := do
  let ref ← IO.mkRef ({} : Scan)
  emit [("event", toJson "argument-calls-start"), ("owner", toJson owner),
    ("callee", toJson callee), ("selected", toJson selected), ("compared", toJson compared)]
  try
    let some ci := env.checked.get.find? (nameOf owner) |
      throw (IO.userError "Owner not found")
    let some b := bodyOf ci | throw (IO.userError "Owner has no stored body")
    inMeta env <| argumentWalk owner callee selected compared b "body" 0 ref
    let s ← ref.get
    emit [("event", toJson "argument-calls-end"), ("owner", toJson owner),
      ("callee", toJson callee),
      ("status", toJson (if s.capped then "incomplete-cap" else
        if s.hits == 1 then "first-match-observed" else "no-call-observed")),
      ("visited", toJson s.visited), ("hits", toJson s.hits),
      ("scan_capped", toJson s.capped), ("pruned_subtrees", toJson s.pruned)]
  catch e =>
    emit [("event", toJson "argument-calls-end"), ("owner", toJson owner),
      ("callee", toJson callee), ("status", toJson "unknown"), ("error", toJson e.toString)]
end RHStage4

/- Bounded declaration records. Compiled fields are inspected using the unchanged
   v0.5 argument scanner; this helper records the named supporting declarations. -/
namespace RHStage4
def supplierDeclaration (env : Environment) (target : String) : IO Unit := do
  try
    let some ci := env.checked.get.find? (nameOf target) |
      throw (IO.userError "Declaration not found")
    inMeta env do
      let value ← match bodyOf ci with
        | some b => pure (clipped (← ppExpr b).pretty 80000)
        | none => pure Json.null
      let refs := match bodyOf ci with
        | some b => b.getUsedConstants
        | none => #[]
      emitMeta [("event", toJson "supplier-declaration"), ("name", toJson target),
        ("status", toJson "recorded"), ("type", clipped (← ppExpr ci.type).pretty 24000),
        ("body", value), ("body_reference_count", toJson refs.size),
        ("body_references", toJson ((refs.toList.take 512).map Name.toString)),
        ("body_references_truncated", toJson (decide (refs.size > 512)))]
  catch e =>
    emit [("event", toJson "supplier-declaration"), ("name", toJson target),
      ("status", toJson "unknown"), ("error", toJson e.toString)]
end RHStage4

open Lean.Elab.Command
namespace RHStage4SupplierFixture
structure Package (a b : Nat) where
  inp : a ≤ b
  hTie : b = b
  rhs : b ≤ b
def make (a b : Nat) (h : a ≤ b) : Package a b where
  inp := h
  hTie := rfl
  rhs := Nat.le_refl b
end RHStage4SupplierFixture
run_cmd do
  let env ← getEnv
  liftIO <| RHStage4.argumentCalls env "RHStage4SupplierFixture.make"
    "RHStage4SupplierFixture.Package.mk" #["inp", "hTie", "rhs"] #["inp", "hTie", "rhs"]
  liftIO <| RHStage4.supplierDeclaration env "RHStage4SupplierFixture.make"
  liftIO <| RHStage4.supplierDeclaration env "RHStage4SupplierFixture.DeliberatelyAbsent"
#eval IO.println "RH_STAGE4_SUPPLIER_FIXTURE_END"
