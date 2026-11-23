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

namespace RHStage3ProvenanceFixture
def bodyOnly : Nat := 37
def wrapper : Nat := bodyOnly
theorem witnessed (h : True) : True := h
def unused : Nat := 53
end RHStage3ProvenanceFixture
run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "RHStage3ProvenanceFixture.wrapper" 4096
  liftIO <| RHStage3Provenance.inspect env "RHStage3ProvenanceFixture.witnessed" 4096
  liftIO <| RHStage3Provenance.inspect env "Nat.add" 4096
  liftIO <| RHStage3Provenance.inspect env "RHStage3ProvenanceFixture.wrapper" 0
#eval IO.println "RH_STAGE3_PROVENANCE_FIXTURE_END"
