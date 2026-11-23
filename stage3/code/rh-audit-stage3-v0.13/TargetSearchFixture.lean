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

/- Targeted first-occurrence search. Binder domains and let types are
explicitly omitted. No reduction or inference; no absence/necessity claim. -/
namespace RHStage3Search
open Lean
structure SearchState where
  remaining : Nat := 100000
  visited : Nat := 0
  omittedAnnotations : Nat := 0
  truncated : Bool := false
  hit : Option String := none
  context : Option Json := none
def headInfo (e : Expr) : Json := Id.run do
  let mut f := e
  let mut args := 0
  let mut stopped := false
  for _ in [:1024] do
    match f with
    | .app g _ => f := g; args := args + 1
    | _ => stopped := true; break
  let (kind, label) := match f with
    | .const n _ => ("constant", n.toString)
    | .bvar i => ("bound-variable", toString i)
    | .proj n i _ => ("projection", n.toString ++ ":" ++ toString i)
    | .lam _ _ _ _ => ("lambda", "")
    | _ => ("other", "")
  return Json.mkObj [("head_kind",toJson kind),("head",toJson label),
    ("preceding_arguments",toJson args),("spine_truncated",toJson (!stopped))]
partial def search (e : Expr) (k : Nat) (path : String := "root")
    (depth : Nat := 0) : StateM SearchState Unit := do
  let st ← get
  if st.hit.isSome then return ()
  if st.remaining == 0 || depth > 600 then
    modify fun s => { s with truncated := true }
    return ()
  modify fun s => { s with remaining := s.remaining - 1, visited := s.visited + 1 }
  match e with
  | .bvar i =>
    if i == k then modify fun s => { s with hit := some path }
  | .app f a =>
    search a k (path ++ "/app.arg") (depth + 1)
    let afterArg ← get
    if afterArg.hit.isSome then
      if afterArg.context.isNone then
        let direct := match a with | .bvar i => i == k | _ => false
        let ctx := Json.mkObj [("application_path",toJson path),
          ("function",headInfo f),("occurrence_branch",toJson "argument"),
          ("selected_child_is_bvar",toJson direct)]
        modify fun s => { s with context := some ctx }
    else
      search f k (path ++ "/app.fn") (depth + 1)
      let afterFn ← get
      if afterFn.hit.isSome && afterFn.context.isNone then
        let direct := match f with | .bvar i => i == k | _ => false
        let ctx := Json.mkObj [("application_path",toJson path),
          ("function",headInfo f),("occurrence_branch",toJson "function"),
          ("selected_child_is_bvar",toJson direct)]
        modify fun s => { s with context := some ctx }
  | .lam _ _ b _ | .forallE _ _ b _ =>
    modify fun s => { s with omittedAnnotations := s.omittedAnnotations + 1 }
    search b (k + 1) (path ++ "/binder.body") (depth + 1)
  | .letE _ _ v b _ =>
    modify fun s => { s with omittedAnnotations := s.omittedAnnotations + 1 }
    search b (k + 1) (path ++ "/let.body") (depth + 1)
    search v k (path ++ "/let.value") (depth + 1)
  | .mdata _ b => search b k (path ++ "/metadata.body") (depth + 1)
  | .proj _ _ b => search b k (path ++ "/projection.body") (depth + 1)
  | _ => pure ()
def result (e : Expr) (fuel : Nat := 100000) : SearchState :=
  ((search e 0).run { remaining := fuel }).2
def emit (fields : List (String × Json)) : IO Unit := do
  IO.println ("RH_STAGE3_SEARCH_JSON\t" ++ (Json.mkObj fields).compress)
  (← IO.getStdout).flush
partial def select (target binder : String) (e : Expr) (ordinal : Nat := 0)
    (fuel : Nat := 256) : IO Unit := do
  if fuel == 0 then throw (IO.userError ("Outer binder search capped: " ++ target))
  match e with
  | .mdata _ b => select target binder b ordinal (fuel - 1)
  | .lam n _ b _ =>
    if n.toString == binder then
      let st := result b
      emit [("event",toJson "search"),("target",toJson target),
        ("binder",toJson binder),("ordinal",toJson ordinal),
        ("status",toJson (if st.hit.isSome then "found" else "not-found-in-projection")),
        ("path",toJson (st.hit.getD "")),
        ("application",st.context.getD Json.null),
        ("visited",toJson st.visited),("node_limit",toJson (100000 : Nat)),
        ("depth_limit",toJson (600 : Nat)),
        ("omitted_annotation_roots",toJson st.omittedAnnotations),
        ("truncated",toJson st.truncated)]
    else select target binder b (ordinal + 1) (fuel - 1)
  | _ => throw (IO.userError ("Explicit binder not found: " ++ target ++ ":" ++ binder))
def inspect (env : Environment) (target binder : String) : IO Unit := do
  match env.checked.get.find? (RHStage3Provenance.nameOf target) with
  | none => throw (IO.userError ("Search target missing: " ++ target))
  | some ci =>
    match RHStage3Provenance.bodyOf ci with
    | none => throw (IO.userError ("Search body missing: " ++ target))
    | some b => select target binder b
end RHStage3Search

namespace RHStage3SearchFixture
open Lean RHStage3Search
def check (label : String) (e : Expr) (hit truncated : Bool)
    (fuel : Nat := 100000) : IO Unit := do
  let st := result e fuel
  if st.hit.isSome != hit || st.truncated != truncated then
    throw (IO.userError ("Target search fixture failed: " ++ label))
  emit [("event",toJson "fixture"),("case",toJson label),("passed",toJson true)]
theorem identity (h : True) : True := h
end RHStage3SearchFixture
run_cmd do
  let env ← getEnv
  liftIO <| do
    let t : Lean.Expr := .sort .zero
    let v : Lean.Expr := .bvar 0
    RHStage3SearchFixture.check "direct" v true false
    RHStage3SearchFixture.check "absent" t false false
    RHStage3SearchFixture.check "shadowed" (.lam `x t v .default) false false
    RHStage3SearchFixture.check "outer-binder" (.lam `x t (.bvar 1) .default) true false
    RHStage3SearchFixture.check "annotation-omitted" (.lam `x v t .default) false false
    RHStage3SearchFixture.check "let-value" (.letE `x t v t false) true false
    RHStage3SearchFixture.check "projection" (.proj `Synthetic 0 v) true false
    RHStage3SearchFixture.check "metadata" (.mdata {} v) true false
    RHStage3SearchFixture.check "capped" (.app v v) false true 1
    let mut deep := t
    for _ in [:601] do
      deep := .proj `Synthetic 0 deep
    RHStage3SearchFixture.check "depth-cap-before-hit" (.app v deep) true true
    let application : Lean.Expr := .app (.app (.const `Synthetic.call []) t) v
    let st := RHStage3Search.result application
    let expected := Json.mkObj [("application_path",toJson "root"),
      ("function",Json.mkObj [("head_kind",toJson "constant"),("head",toJson "Synthetic.call"),
        ("preceding_arguments",toJson (1 : Nat)),("spine_truncated",toJson false)]),
      ("occurrence_branch",toJson "argument"),("selected_child_is_bvar",toJson true)]
    if st.context.map Json.compress != some expected.compress || st.hit != some "root/app.arg" then
      throw (IO.userError "Application context fixture failed")
    RHStage3Search.emit [("event",toJson "fixture"),("case",toJson "application-context"),("passed",toJson true)]
    let fnState := RHStage3Search.result (.app v t)
    let fnExpected := Json.mkObj [("application_path",toJson "root"),
      ("function",Json.mkObj [("head_kind",toJson "bound-variable"),("head",toJson "0"),
        ("preceding_arguments",toJson (0 : Nat)),("spine_truncated",toJson false)]),
      ("occurrence_branch",toJson "function"),("selected_child_is_bvar",toJson true)]
    if fnState.context.map Json.compress != some fnExpected.compress then
      throw (IO.userError "Function position fixture failed")
    RHStage3Search.emit [("event",toJson "fixture"),("case",toJson "function-context"),("passed",toJson true)]
    RHStage3Search.inspect env "RHStage3SearchFixture.identity" "h"
#eval IO.println "RH_STAGE3_SEARCH_FIXTURE_END"
