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
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.R3.Rw.Moved" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.R3.Rw.Moved"
#print GlobalTheory.Mem.R3.Rw.Moved
#print axioms GlobalTheory.Mem.R3.Rw.Moved
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.R3.Rw.Moved"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.R3.Rw.Moved.mk" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.R3.Rw.Moved.mk"
#print GlobalTheory.Mem.R3.Rw.Moved.mk
#print axioms GlobalTheory.Mem.R3.Rw.Moved.mk
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.R3.Rw.Moved.mk"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.R3.Rw.Moved.intersectionNumber_baseChange" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.R3.Rw.Moved.intersectionNumber_baseChange"
#print GlobalTheory.Mem.R3.Rw.Moved.intersectionNumber_baseChange
#print axioms GlobalTheory.Mem.R3.Rw.Moved.intersectionNumber_baseChange
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.R3.Rw.Moved.intersectionNumber_baseChange"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.R3.Rw.Moved.exAt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.R3.Rw.Moved.exAt"
#print GlobalTheory.Mem.R3.Rw.Moved.exAt
#print axioms GlobalTheory.Mem.R3.Rw.Moved.exAt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.R3.Rw.Moved.exAt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.R3.Rw.St" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.R3.Rw.St"
#print GlobalTheory.Mem.R3.Rw.St
#print axioms GlobalTheory.Mem.R3.Rw.St
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.R3.Rw.St"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.R3.Rw.St.mk" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.R3.Rw.St.mk"
#print GlobalTheory.Mem.R3.Rw.St.mk
#print axioms GlobalTheory.Mem.R3.Rw.St.mk
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.R3.Rw.St.mk"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.R3.Rw.HasBare" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.R3.Rw.HasBare"
#print GlobalTheory.Mem.R3.Rw.HasBare
#print axioms GlobalTheory.Mem.R3.Rw.HasBare
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.R3.Rw.HasBare"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Up.AllSt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Up.AllSt"
#print GlobalTheory.HeightCounting.Up.AllSt
#print axioms GlobalTheory.HeightCounting.Up.AllSt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Up.AllSt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.Top.Bl.Start" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.Top.Bl.Start"
#print GlobalTheory.Mem.Top.Bl.Start
#print axioms GlobalTheory.Mem.Top.Bl.Start
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.Top.Bl.Start"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.Top.Bl.DatEx" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.Top.Bl.DatEx"
#print GlobalTheory.Mem.Top.Bl.DatEx
#print axioms GlobalTheory.Mem.Top.Bl.DatEx
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.Top.Bl.DatEx"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.Top.Bl.UnitaryCaseCondition" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.Top.Bl.UnitaryCaseCondition"
#print GlobalTheory.Mem.Top.Bl.UnitaryCaseCondition
#print axioms GlobalTheory.Mem.Top.Bl.UnitaryCaseCondition
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.Top.Bl.UnitaryCaseCondition"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.R3.Rw.WeightCaseCondition" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.R3.Rw.WeightCaseCondition"
#print GlobalTheory.Mem.R3.Rw.WeightCaseCondition
#print axioms GlobalTheory.Mem.R3.Rw.WeightCaseCondition
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.R3.Rw.WeightCaseCondition"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.T.exists_movedData_state_localisations" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.T.exists_movedData_state_localisations"
#print GlobalTheory.T.exists_movedData_state_localisations
#print axioms GlobalTheory.T.exists_movedData_state_localisations
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.T.exists_movedData_state_localisations"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Fin3.MvLoc.exists_moved_loc" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Fin3.MvLoc.exists_moved_loc"
#print GlobalTheory.HeightCounting.Fin3.MvLoc.exists_moved_loc
#print axioms GlobalTheory.HeightCounting.Fin3.MvLoc.exists_moved_loc
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Fin3.MvLoc.exists_moved_loc"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.TwInputs.RealSide.ofPins" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.TwInputs.RealSide.ofPins"
#print GlobalTheory.TwInputs.RealSide.ofPins
#print axioms GlobalTheory.TwInputs.RealSide.ofPins
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.TwInputs.RealSide.ofPins"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.TwInputs.RealSide.ofPins._proof_1" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.TwInputs.RealSide.ofPins._proof_1"
#print GlobalTheory.TwInputs.RealSide.ofPins._proof_1
#print axioms GlobalTheory.TwInputs.RealSide.ofPins._proof_1
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.TwInputs.RealSide.ofPins._proof_1"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.TwInputs.RealSide.ofPins._proof_2" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.TwInputs.RealSide.ofPins._proof_2"
#print GlobalTheory.TwInputs.RealSide.ofPins._proof_2
#print axioms GlobalTheory.TwInputs.RealSide.ofPins._proof_2
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.TwInputs.RealSide.ofPins._proof_2"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.TwInputs.RealSide.ofPins._proof_3" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.TwInputs.RealSide.ofPins._proof_3"
#print GlobalTheory.TwInputs.RealSide.ofPins._proof_3
#print axioms GlobalTheory.TwInputs.RealSide.ofPins._proof_3
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.TwInputs.RealSide.ofPins._proof_3"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.TwInputs.RealSide.ofPins._proof_4" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.TwInputs.RealSide.ofPins._proof_4"
#print GlobalTheory.TwInputs.RealSide.ofPins._proof_4
#print axioms GlobalTheory.TwInputs.RealSide.ofPins._proof_4
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.TwInputs.RealSide.ofPins._proof_4"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.TwInputs.RealSide.ofPins._proof_5" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.TwInputs.RealSide.ofPins._proof_5"
#print GlobalTheory.TwInputs.RealSide.ofPins._proof_5
#print axioms GlobalTheory.TwInputs.RealSide.ofPins._proof_5
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.TwInputs.RealSide.ofPins._proof_5"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.TwInputs.RealSide.ofPins._proof_6" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.TwInputs.RealSide.ofPins._proof_6"
#print GlobalTheory.TwInputs.RealSide.ofPins._proof_6
#print axioms GlobalTheory.TwInputs.RealSide.ofPins._proof_6
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.TwInputs.RealSide.ofPins._proof_6"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.TwInputs.RealSide.ofPins._proof_7" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.TwInputs.RealSide.ofPins._proof_7"
#print GlobalTheory.TwInputs.RealSide.ofPins._proof_7
#print axioms GlobalTheory.TwInputs.RealSide.ofPins._proof_7
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.TwInputs.RealSide.ofPins._proof_7"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.TwInputs.RealSide.ofPins._proof_8" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.TwInputs.RealSide.ofPins._proof_8"
#print GlobalTheory.TwInputs.RealSide.ofPins._proof_8
#print axioms GlobalTheory.TwInputs.RealSide.ofPins._proof_8
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.TwInputs.RealSide.ofPins._proof_8"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.TwInputs.RealSide.ofPins._proof_9" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.TwInputs.RealSide.ofPins._proof_9"
#print GlobalTheory.TwInputs.RealSide.ofPins._proof_9
#print axioms GlobalTheory.TwInputs.RealSide.ofPins._proof_9
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.TwInputs.RealSide.ofPins._proof_9"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.TwInputs.RealSide.ofPins._proof_10" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.TwInputs.RealSide.ofPins._proof_10"
#print GlobalTheory.TwInputs.RealSide.ofPins._proof_10
#print axioms GlobalTheory.TwInputs.RealSide.ofPins._proof_10
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.TwInputs.RealSide.ofPins._proof_10"

#eval IO.println "RH_STAGE3_STATE_WITNESSES_END"
