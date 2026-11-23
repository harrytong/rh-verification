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
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.T.sFin_and_sFinl_of_archCmp_sEta_thetaData" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.T.sFin_and_sFinl_of_archCmp_sEta_thetaData"
#print GlobalTheory.T.sFin_and_sFinl_of_archCmp_sEta_thetaData
#print axioms GlobalTheory.T.sFin_and_sFinl_of_archCmp_sEta_thetaData
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.T.sFin_and_sFinl_of_archCmp_sEta_thetaData"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Up.sFino_of_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Up.sFino_of_alt"
#print GlobalTheory.HeightCounting.Up.sFino_of_alt
#print axioms GlobalTheory.HeightCounting.Up.sFino_of_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Up.sFino_of_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Up.FinitenessStatement" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Up.FinitenessStatement"
#print GlobalTheory.HeightCounting.Up.FinitenessStatement
#print axioms GlobalTheory.HeightCounting.Up.FinitenessStatement
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Up.FinitenessStatement"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Up.FinitenessListStatement" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Up.FinitenessListStatement"
#print GlobalTheory.HeightCounting.Up.FinitenessListStatement
#print axioms GlobalTheory.HeightCounting.Up.FinitenessListStatement
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Up.FinitenessListStatement"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Up.SpectralFiniteness" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Up.SpectralFiniteness"
#print GlobalTheory.HeightCounting.Up.SpectralFiniteness
#print axioms GlobalTheory.HeightCounting.Up.SpectralFiniteness
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Up.SpectralFiniteness"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Up.all_stages_of_specializations_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Up.all_stages_of_specializations_alt"
#print GlobalTheory.HeightCounting.Up.all_stages_of_specializations_alt
#print axioms GlobalTheory.HeightCounting.Up.all_stages_of_specializations_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Up.all_stages_of_specializations_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Up.sXd_all_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Up.sXd_all_alt"
#print GlobalTheory.HeightCounting.Up.sXd_all_alt
#print axioms GlobalTheory.HeightCounting.Up.sXd_all_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Up.sXd_all_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Up.lv3Mv_extensionWithOrigin_and_nEog" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Up.lv3Mv_extensionWithOrigin_and_nEog"
#print GlobalTheory.HeightCounting.Up.lv3Mv_extensionWithOrigin_and_nEog
#print axioms GlobalTheory.HeightCounting.Up.lv3Mv_extensionWithOrigin_and_nEog
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Up.lv3Mv_extensionWithOrigin_and_nEog"

#eval IO.println "RH_STAGE3_CONSTRUCTION_END"
