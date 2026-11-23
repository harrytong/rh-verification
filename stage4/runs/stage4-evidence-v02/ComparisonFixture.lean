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

-- Look only at maximal application spines. Recurse into their arguments and
-- nonconstant function heads. Enter lambdas/lets with the real local context.
-- Binder annotations are excluded from call-site evidence.
partial def walk (owner : String) (watch : Array Name) (e : Expr)
    (path : String) (depth : Nat) (ref : IO.Ref Scan) : MetaM Unit := do
  let s ← ref.get
  if s.visited >= 250000 || depth > 600 || s.hits >= 64 then
    ref.modify fun s => { s with capped := true }
    return ()
  ref.modify fun s => { s with visited := s.visited + 1 }
  match e with
  | .lam n t b bi =>
    withLocalDecl n bi t fun x => walk owner watch (b.instantiate1 x) (path ++ "/lambda") (depth+1) ref
  | .letE n t v b _ =>
    walk owner watch v (path ++ "/let-value") (depth+1) ref
    withLetDecl n t v fun x => walk owner watch (b.instantiate1 x) (path ++ "/let-body") (depth+1) ref
  | .app .. =>
    let fn := e.getAppFn
    let args := e.getAppArgs
    if let some n := headName fn then
      if watch.contains n then
        ref.modify fun s => { s with hits := s.hits + 1 }
        comparison owner path n.toString (← inferType e)
    else
      walk owner watch fn (path ++ "/function") (depth+1) ref
    for i in [:args.size] do
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

def calls (env : Environment) (owner : String) (watch : Array String) : IO Unit := do
  let ref ← IO.mkRef ({} : Scan)
  emit [("event",toJson "calls-start"),("owner",toJson owner),("watch",toJson watch)]
  try
    let some ci := env.checked.get.find? (nameOf owner) |
      throw (IO.userError "Owner not found")
    let some b := bodyOf ci | throw (IO.userError "Owner has no stored body")
    inMeta env <| walk owner (watch.map nameOf) b "body" 0 ref
    let s ← ref.get
    emit [("event",toJson "calls-end"),("owner",toJson owner),
      ("status",toJson (if s.capped then "incomplete-cap" else "completed")),
      ("visited",toJson s.visited),("hits",toJson s.hits)]
  catch e =>
    let s ← ref.get
    emit [("event",toJson "calls-end"),("owner",toJson owner),
      ("status",toJson "unknown"),("visited",toJson s.visited),
      ("hits",toJson s.hits),("error",toJson e.toString)]
end RHStage4

open Lean.Elab.Command
namespace RHStage4Fixture
theorem seed (a b : Nat) (h : a ≤ b) : a ≤ b := h
theorem equalSides (a : Nat) : a = a := rfl
theorem equalByHypothesis (a b : Nat) (h : a = b) : a = b := h
theorem sameCall (a : Nat) : a ≤ a := seed a a (Nat.le_refl a)
theorem differentCall (a b : Nat) (h : a ≤ b) : a ≤ b := seed a b h
def alias (a : Nat) : Nat := a
theorem letCall (a : Nat) : a ≤ a :=
  let z := alias a
  seed z a (Nat.le_refl a)
end RHStage4Fixture
run_cmd do
  let env ← getEnv
  liftIO <| RHStage4.generic env "RHStage4Fixture.seed"
  liftIO <| RHStage4.generic env "RHStage4Fixture.equalSides"
  liftIO <| RHStage4.generic env "RHStage4Fixture.equalByHypothesis"
  liftIO <| RHStage4.calls env "RHStage4Fixture.sameCall" #["RHStage4Fixture.seed"]
  liftIO <| RHStage4.calls env "RHStage4Fixture.differentCall" #["RHStage4Fixture.seed"]
  liftIO <| RHStage4.calls env "RHStage4Fixture.letCall" #["RHStage4Fixture.seed"]
#eval IO.println "RH_STAGE4_FIXTURE_END"
