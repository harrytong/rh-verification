import Lean
import Main
set_option pp.all true
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

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.LiftUnfold.integral_theta" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.LiftUnfold.integral_theta"
#print GlobalTheory.LiftUnfold.integral_theta
#print axioms GlobalTheory.LiftUnfold.integral_theta
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.LiftUnfold.integral_theta"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.LiftClassSumTwist.thF_eq_princ" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.LiftClassSumTwist.thF_eq_princ"
#print GlobalTheory.LiftClassSumTwist.thF_eq_princ
#print axioms GlobalTheory.LiftClassSumTwist.thF_eq_princ
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.LiftClassSumTwist.thF_eq_princ"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.LiftClassSumTwist.thF_eq_classSum" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.LiftClassSumTwist.thF_eq_classSum"
#print GlobalTheory.LiftClassSumTwist.thF_eq_classSum
#print axioms GlobalTheory.LiftClassSumTwist.thF_eq_classSum
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.LiftClassSumTwist.thF_eq_classSum"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Hk3.Core" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Hk3.Core"
#print GlobalTheory.Hk3.Core
#print axioms GlobalTheory.Hk3.Core
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Hk3.Core"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Hk3.Core.thP" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Hk3.Core.thP"
#print GlobalTheory.Hk3.Core.thP
#print axioms GlobalTheory.Hk3.Core.thP
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Hk3.Core.thP"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.TwInputs.RealSide.char" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.TwInputs.RealSide.char"
#print GlobalTheory.TwInputs.RealSide.char
#print axioms GlobalTheory.TwInputs.RealSide.char
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.TwInputs.RealSide.char"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "Formalism.IndefR.Links.RealDat3.Char3" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN Formalism.IndefR.Links.RealDat3.Char3"
#print Formalism.IndefR.Links.RealDat3.Char3
#print axioms Formalism.IndefR.Links.RealDat3.Char3
#eval IO.println "RH_STAGE3_DECL_END Formalism.IndefR.Links.RealDat3.Char3"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.FlatVecExist.flatVec_existsUnique" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.FlatVecExist.flatVec_existsUnique"
#print GlobalTheory.FlatVecExist.flatVec_existsUnique
#print axioms GlobalTheory.FlatVecExist.flatVec_existsUnique
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.FlatVecExist.flatVec_existsUnique"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.FlatLift.flat_eq_unit_smul_om" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.FlatLift.flat_eq_unit_smul_om"
#print GlobalTheory.FlatLift.flat_eq_unit_smul_om
#print axioms GlobalTheory.FlatLift.flat_eq_unit_smul_om
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.FlatLift.flat_eq_unit_smul_om"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.T.weilRep_central_acts_by_dilation_unit" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.T.weilRep_central_acts_by_dilation_unit"
#print GlobalTheory.T.weilRep_central_acts_by_dilation_unit
#print axioms GlobalTheory.T.weilRep_central_acts_by_dilation_unit
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.T.weilRep_central_acts_by_dilation_unit"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.T.lift_vector_eq_unit_mul_dilated_flat_datum" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.T.lift_vector_eq_unit_mul_dilated_flat_datum"
#print GlobalTheory.T.lift_vector_eq_unit_mul_dilated_flat_datum
#print axioms GlobalTheory.T.lift_vector_eq_unit_mul_dilated_flat_datum
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.T.lift_vector_eq_unit_mul_dilated_flat_datum"

#eval IO.println "RH_STAGE3_INTEGRAL_END"
