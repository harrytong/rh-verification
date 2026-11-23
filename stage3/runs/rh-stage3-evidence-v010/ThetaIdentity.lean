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
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Fin3.emtTheta_L_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Fin3.emtTheta_L_alt"
#print GlobalTheory.HeightCounting.Fin3.emtTheta_L_alt
#print axioms GlobalTheory.HeightCounting.Fin3.emtTheta_L_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Fin3.emtTheta_L_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.T.emtTheta_of_yRel" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.T.emtTheta_of_yRel"
#print GlobalTheory.T.emtTheta_of_yRel
#print axioms GlobalTheory.T.emtTheta_of_yRel
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.T.emtTheta_of_yRel"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.T.normalisedReadings_related_localizedAdelicData" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.T.normalisedReadings_related_localizedAdelicData"
#print GlobalTheory.T.normalisedReadings_related_localizedAdelicData
#print axioms GlobalTheory.T.normalisedReadings_related_localizedAdelicData
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.T.normalisedReadings_related_localizedAdelicData"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Fin3.YRel" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Fin3.YRel"
#print GlobalTheory.HeightCounting.Fin3.YRel
#print axioms GlobalTheory.HeightCounting.Fin3.YRel
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Fin3.YRel"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Fin3.yStructureLocal" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Fin3.yStructureLocal"
#print GlobalTheory.HeightCounting.Fin3.yStructureLocal
#print axioms GlobalTheory.HeightCounting.Fin3.yStructureLocal
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Fin3.yStructureLocal"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Fin3.characterChoiceLocal" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Fin3.characterChoiceLocal"
#print GlobalTheory.HeightCounting.Fin3.characterChoiceLocal
#print axioms GlobalTheory.HeightCounting.Fin3.characterChoiceLocal
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Fin3.characterChoiceLocal"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Fin3.nonempty_nMore_of_xdAll" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Fin3.nonempty_nMore_of_xdAll"
#print GlobalTheory.HeightCounting.Fin3.nonempty_nMore_of_xdAll
#print axioms GlobalTheory.HeightCounting.Fin3.nonempty_nMore_of_xdAll
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Fin3.nonempty_nMore_of_xdAll"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Fin3.thetaTie_yStructureLocal_nonempty" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Fin3.thetaTie_yStructureLocal_nonempty"
#print GlobalTheory.HeightCounting.Fin3.thetaTie_yStructureLocal_nonempty
#print axioms GlobalTheory.HeightCounting.Fin3.thetaTie_yStructureLocal_nonempty
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Fin3.thetaTie_yStructureLocal_nonempty"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.EMtTheta" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.EMtTheta"
#print GlobalTheory.HeightCounting.EMtTheta
#print axioms GlobalTheory.HeightCounting.EMtTheta
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.EMtTheta"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Fin3.exists_base_level_rXs_and_yRel" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Fin3.exists_base_level_rXs_and_yRel"
#print GlobalTheory.HeightCounting.Fin3.exists_base_level_rXs_and_yRel
#print axioms GlobalTheory.HeightCounting.Fin3.exists_base_level_rXs_and_yRel
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Fin3.exists_base_level_rXs_and_yRel"

#eval IO.println "RH_STAGE3_THETA_END"
