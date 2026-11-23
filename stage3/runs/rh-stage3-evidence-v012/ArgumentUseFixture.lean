import Lean
/- Stored expression references only. No unfolding, reduction, mutation,
   global traversal, or necessity inference. Shared byte-for-byte by fixtures
   and the project probe. Imported metadata APIs follow the Stage 2 runner. -/
open Lean Elab Command
namespace RHStage3Provenance
def nameOf (s : String) : Name :=
  (s.splitOn ".").foldl Name.str Name.anonymous
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
def emit (fields : List (String × Json)) : IO Unit := do
  IO.println ("RH_STAGE3_PROVENANCE_JSON\t" ++ (Json.mkObj fields).compress)
  (← IO.getStdout).flush
def refJson (env : Environment) (n : Name) : Json :=
  Json.mkObj [("name", toJson n.toString), ("module", toJson (moduleOf env n)),
    ("found", toJson ((env.checked.get.find? n).isSome))]
def emitRefs (env : Environment) (target location : String) (e : Expr)
    (limit : Nat) : IO Unit := do
  let refs := e.getUsedConstants
  let kept := refs.toList.take limit
  emit [("event", toJson "references"), ("target", toJson target),
    ("location", toJson location), ("total", toJson refs.size),
    ("retained", toJson kept.length), ("limit", toJson limit),
    ("truncated", toJson (decide (refs.size > limit))),
    ("references", Json.arr (kept.toArray.map (refJson env)))]
def inspect (env : Environment) (target : String) (limit : Nat) : IO Unit := do
  let n := nameOf target
  match env.checked.get.find? n with
  | none => throw (IO.userError ("Target not found: " ++ target))
  | some ci =>
    emit [("event", toJson "target"), ("target", toJson target),
      ("module", toJson (moduleOf env n)), ("kind", toJson (kindOf ci)),
      ("has_body", toJson ((bodyOf ci).isSome))]
    emitRefs env target "type" ci.type limit
    match bodyOf ci with
    | some b => emitRefs env target "body" b limit
    | none => pure ()
end RHStage3Provenance

/- Syntactic occurrence counts in stored bodies; no reduction, unfolding,
   type inference, proof minimization or declaration mutation. -/
namespace RHStage3Uses
open Lean
structure Counts where
  remaining : Nat := 100000
  annotation : Nat := 0
  other : Nat := 0
  truncated : Bool := false
partial def count (e : Expr) (k : Nat) (inAnnotation : Bool := false)
    (depth : Nat := 0) (depthLimit : Nat := 600) : StateM Counts Unit := do
  let st ← get
  if st.remaining == 0 || depth > depthLimit then
    modify fun s => { s with truncated := true }
    return ()
  modify fun s => { s with remaining := s.remaining - 1 }
  match e with
  | .bvar i =>
    if i == k then
      if inAnnotation then
        modify fun s => { s with annotation := s.annotation + 1 }
      else
        modify fun s => { s with other := s.other + 1 }
  | .app f a =>
    count f k inAnnotation (depth + 1) depthLimit
    count a k inAnnotation (depth + 1) depthLimit
  | .lam _ t b _ | .forallE _ t b _ =>
    count t k true (depth + 1) depthLimit
    count b (k + 1) inAnnotation (depth + 1) depthLimit
  | .letE _ t v b _ =>
    count t k true (depth + 1) depthLimit
    count v k inAnnotation (depth + 1) depthLimit
    count b (k + 1) inAnnotation (depth + 1) depthLimit
  | .mdata _ b | .proj _ _ b => count b k inAnnotation (depth + 1) depthLimit
  | _ => pure ()
def result (e : Expr) (fuel : Nat := 100000) (depthLimit : Nat := 600) : Counts :=
  ((count e 0 false 0 depthLimit).run { remaining := fuel }).2
def emit (fields : List (String × Json)) : IO Unit := do
  IO.println ("RH_STAGE3_USES_JSON\t" ++ (Json.mkObj fields).compress)
  (← IO.getStdout).flush
partial def scan (target : String) (e : Expr) (ordinal : Nat := 0)
    (outerFuel : Nat := 256) : IO Unit := do
  if outerFuel == 0 then
    emit [("event",toJson "end"),("target",toJson target),
      ("binder_count",toJson ordinal),("stop",toJson "outer-step-cap")]
    return ()
  match e with
  | .mdata _ b => scan target b ordinal (outerFuel - 1)
  | .lam n _ b _ =>
    if ordinal >= 128 then
      emit [("event",toJson "end"),("target",toJson target),
        ("binder_count",toJson ordinal),("stop",toJson "binder-cap")]
      return ()
    let st := result b
    emit [("event",toJson "binder"),("target",toJson target),
      ("ordinal",toJson ordinal),("name",toJson n.toString),
      ("binder_or_let_type_position",toJson st.annotation),
      ("other_expression_position",toJson st.other),
      ("nodes_visited",toJson (100000 - st.remaining)),
      ("node_limit",toJson (100000 : Nat)),("depth_limit",toJson (600 : Nat)),
      ("truncated",toJson st.truncated)]
    scan target b (ordinal + 1) (outerFuel - 1)
  | _ =>
    emit [("event",toJson "end"),("target",toJson target),
      ("binder_count",toJson ordinal),("stop",toJson "non-lambda-head")]
def inspect (env : Environment) (target : String) : IO Unit := do
  match env.checked.get.find? (RHStage3Provenance.nameOf target) with
  | none => throw (IO.userError ("Use target not found: " ++ target))
  | some ci =>
    match RHStage3Provenance.bodyOf ci with
    | none => throw (IO.userError ("Use target has no stored body: " ++ target))
    | some b => scan target b
end RHStage3Uses

namespace RHStage3UsesFixture
open Lean RHStage3Uses
def checkCase (label : String) (e : Expr) (a o : Nat) (truncated : Bool := false)
    (fuel : Nat := 100000) (depthLimit : Nat := 600) : IO Unit := do
  let st := result e fuel depthLimit
  if st.annotation != a || st.other != o || st.truncated != truncated then
    throw (IO.userError ("Occurrence fixture failed: " ++ label))
  emit [("event",toJson "fixture"),("case",toJson label),("passed",toJson true)]
theorem identity (h : True) : True := h
end RHStage3UsesFixture
run_cmd do
  let env ← getEnv
  liftIO <| do
    let t : Lean.Expr := .sort .zero
    let v : Lean.Expr := .bvar 0
    RHStage3UsesFixture.checkCase "direct" v 0 1
    RHStage3UsesFixture.checkCase "absent" t 0 0
    RHStage3UsesFixture.checkCase "shadowed" (.lam `x t (.bvar 0) .default) 0 0
    RHStage3UsesFixture.checkCase "outer-under-lambda" (.lam `x t (.bvar 1) .default) 0 1
    RHStage3UsesFixture.checkCase "binder-domain-only" (.lam `x v (.bvar 0) .default) 1 0
    RHStage3UsesFixture.checkCase "forall-domain-and-body" (.forallE `x v (.bvar 1) .default) 1 1
    RHStage3UsesFixture.checkCase "let-type-value-body" (.letE `x v v (.bvar 1) false) 1 2
    RHStage3UsesFixture.checkCase "projection" (.proj `Synthetic 0 v) 0 1
    RHStage3UsesFixture.checkCase "annotation-inherited" (.lam `x (.app v v) (.bvar 0) .default) 2 0
    RHStage3UsesFixture.checkCase "metadata" (.mdata {} v) 0 1
    RHStage3UsesFixture.checkCase "node-cap" (.app v v) 0 0 true 1
    RHStage3UsesFixture.checkCase "depth-cap" (.app v v) 0 0 true 100000 0
    RHStage3Uses.inspect env "RHStage3UsesFixture.identity"
    RHStage3Uses.scan "synthetic-outer-cap" v 0 0
    RHStage3Uses.scan "synthetic-binder-cap" (.lam `x t v .default) 128
#eval IO.println "RH_STAGE3_USE_FIXTURE_END"
