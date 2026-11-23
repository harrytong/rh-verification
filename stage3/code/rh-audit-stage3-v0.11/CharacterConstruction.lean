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
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.HeightCountingCharacterData" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.HeightCountingCharacterData"
#print GlobalTheory.HeightCounting.HeightCountingCharacterData
#print axioms GlobalTheory.HeightCounting.HeightCountingCharacterData
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.HeightCountingCharacterData"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Up.StrictHenselianAcyclicLevelNonempty" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Up.StrictHenselianAcyclicLevelNonempty"
#print GlobalTheory.HeightCounting.Up.StrictHenselianAcyclicLevelNonempty
#print axioms GlobalTheory.HeightCounting.Up.StrictHenselianAcyclicLevelNonempty
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Up.StrictHenselianAcyclicLevelNonempty"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.T.stage_c_nonempty_of_prints_third_layer" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.T.stage_c_nonempty_of_prints_third_layer"
#print GlobalTheory.T.stage_c_nonempty_of_prints_third_layer
#print axioms GlobalTheory.T.stage_c_nonempty_of_prints_third_layer
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.T.stage_c_nonempty_of_prints_third_layer"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Up.ChoiceEx.stage_c_nonempty_of_published_inputs" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Up.ChoiceEx.stage_c_nonempty_of_published_inputs"
#print GlobalTheory.HeightCounting.Up.ChoiceEx.stage_c_nonempty_of_published_inputs
#print axioms GlobalTheory.HeightCounting.Up.ChoiceEx.stage_c_nonempty_of_published_inputs
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Up.ChoiceEx.stage_c_nonempty_of_published_inputs"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Up.ChoiceEx.sc_of_sck_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Up.ChoiceEx.sc_of_sck_alt"
#print GlobalTheory.HeightCounting.Up.ChoiceEx.sc_of_sck_alt
#print axioms GlobalTheory.HeightCounting.Up.ChoiceEx.sc_of_sck_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Up.ChoiceEx.sc_of_sck_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.T.stageCExists_of_casselmanWallach" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.T.stageCExists_of_casselmanWallach"
#print GlobalTheory.T.stageCExists_of_casselmanWallach
#print axioms GlobalTheory.T.stageCExists_of_casselmanWallach
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.T.stageCExists_of_casselmanWallach"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.LevCmp.stageCExists_of_harishChandra_serN" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.LevCmp.stageCExists_of_harishChandra_serN"
#print GlobalTheory.LevCmp.stageCExists_of_harishChandra_serN
#print axioms GlobalTheory.LevCmp.stageCExists_of_harishChandra_serN
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.LevCmp.stageCExists_of_harishChandra_serN"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.T.nonGalois_exists_choice_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.T.nonGalois_exists_choice_alt"
#print GlobalTheory.T.nonGalois_exists_choice_alt
#print axioms GlobalTheory.T.nonGalois_exists_choice_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.T.nonGalois_exists_choice_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.ChoiceRead.exists_stC_choice_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.ChoiceRead.exists_stC_choice_alt"
#print GlobalTheory.ChoiceRead.exists_stC_choice_alt
#print axioms GlobalTheory.ChoiceRead.exists_stC_choice_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.ChoiceRead.exists_stC_choice_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.T.local_component_at_place_determined_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.T.local_component_at_place_determined_alt"
#print GlobalTheory.T.local_component_at_place_determined_alt
#print axioms GlobalTheory.T.local_component_at_place_determined_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.T.local_component_at_place_determined_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.ChoiceRead.emtTheta_withE" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.ChoiceRead.emtTheta_withE"
#print GlobalTheory.ChoiceRead.emtTheta_withE
#print axioms GlobalTheory.ChoiceRead.emtTheta_withE
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.ChoiceRead.emtTheta_withE"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Fin3.emtTheta_L_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Fin3.emtTheta_L_alt"
#print GlobalTheory.HeightCounting.Fin3.emtTheta_L_alt
#print axioms GlobalTheory.HeightCounting.Fin3.emtTheta_L_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Fin3.emtTheta_L_alt"

#eval IO.println "RH_STAGE3_CHARACTER_END"
