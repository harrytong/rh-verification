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
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.PlaceRead.exists_local_map_at_place_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.PlaceRead.exists_local_map_at_place_alt"
#print GlobalTheory.PlaceRead.exists_local_map_at_place_alt
#print axioms GlobalTheory.PlaceRead.exists_local_map_at_place_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.PlaceRead.exists_local_map_at_place_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.TwInputs.RealSide.ofPins" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.TwInputs.RealSide.ofPins"
#print GlobalTheory.TwInputs.RealSide.ofPins
#print axioms GlobalTheory.TwInputs.RealSide.ofPins
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.TwInputs.RealSide.ofPins"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "Formalism.IndefR.Links.RealDat3.characterisation_of_weak" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN Formalism.IndefR.Links.RealDat3.characterisation_of_weak"
#print Formalism.IndefR.Links.RealDat3.characterisation_of_weak
#print axioms Formalism.IndefR.Links.RealDat3.characterisation_of_weak
#eval IO.println "RH_STAGE3_DECL_END Formalism.IndefR.Links.RealDat3.characterisation_of_weak"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "Formalism.IndefR.Links.RealDat.thP_of_weak" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN Formalism.IndefR.Links.RealDat.thP_of_weak"
#print Formalism.IndefR.Links.RealDat.thP_of_weak
#print axioms Formalism.IndefR.Links.RealDat.thP_of_weak
#eval IO.println "RH_STAGE3_DECL_END Formalism.IndefR.Links.RealDat.thP_of_weak"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "Formalism.IndefR.Links.OrZero" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN Formalism.IndefR.Links.OrZero"
#print Formalism.IndefR.Links.OrZero
#print axioms Formalism.IndefR.Links.OrZero
#eval IO.println "RH_STAGE3_DECL_END Formalism.IndefR.Links.OrZero"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "Formalism.IndefR.Links.orZero_exists" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN Formalism.IndefR.Links.orZero_exists"
#print Formalism.IndefR.Links.orZero_exists
#print axioms Formalism.IndefR.Links.orZero_exists
#eval IO.println "RH_STAGE3_DECL_END Formalism.IndefR.Links.orZero_exists"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "Formalism.IndefR.Links.RealDat.IsThPW" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN Formalism.IndefR.Links.RealDat.IsThPW"
#print Formalism.IndefR.Links.RealDat.IsThPW
#print axioms Formalism.IndefR.Links.RealDat.IsThPW
#eval IO.println "RH_STAGE3_DECL_END Formalism.IndefR.Links.RealDat.IsThPW"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "Formalism.IndefR.Links.RealDat.ExAt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN Formalism.IndefR.Links.RealDat.ExAt"
#print Formalism.IndefR.Links.RealDat.ExAt
#print axioms Formalism.IndefR.Links.RealDat.ExAt
#eval IO.println "RH_STAGE3_DECL_END Formalism.IndefR.Links.RealDat.ExAt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "Formalism.IndefR.Links.RealDat.ExAt.thF" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN Formalism.IndefR.Links.RealDat.ExAt.thF"
#print Formalism.IndefR.Links.RealDat.ExAt.thF
#print axioms Formalism.IndefR.Links.RealDat.ExAt.thF
#eval IO.println "RH_STAGE3_DECL_END Formalism.IndefR.Links.RealDat.ExAt.thF"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "Formalism.IndefR.Links.RealDat.PThF" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN Formalism.IndefR.Links.RealDat.PThF"
#print Formalism.IndefR.Links.RealDat.PThF
#print axioms Formalism.IndefR.Links.RealDat.PThF
#eval IO.println "RH_STAGE3_DECL_END Formalism.IndefR.Links.RealDat.PThF"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "Formalism.IndefR.Links.UnusedChoiceStatements" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN Formalism.IndefR.Links.UnusedChoiceStatements"
#print Formalism.IndefR.Links.UnusedChoiceStatements
#print axioms Formalism.IndefR.Links.UnusedChoiceStatements
#eval IO.println "RH_STAGE3_DECL_END Formalism.IndefR.Links.UnusedChoiceStatements"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "Formalism.IndefR.Links.UnusedChoiceStatements.ex" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN Formalism.IndefR.Links.UnusedChoiceStatements.ex"
#print Formalism.IndefR.Links.UnusedChoiceStatements.ex
#print axioms Formalism.IndefR.Links.UnusedChoiceStatements.ex
#eval IO.println "RH_STAGE3_DECL_END Formalism.IndefR.Links.UnusedChoiceStatements.ex"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.R3.Holds" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.R3.Holds"
#print GlobalTheory.Mem.R3.Holds
#print axioms GlobalTheory.Mem.R3.Holds
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.R3.Holds"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.R3.Holds.aux" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.R3.Holds.aux"
#print GlobalTheory.Mem.R3.Holds.aux
#print axioms GlobalTheory.Mem.R3.Holds.aux
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.R3.Holds.aux"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.R3.Pins" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.R3.Pins"
#print GlobalTheory.Mem.R3.Pins
#print axioms GlobalTheory.Mem.R3.Pins
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.R3.Pins"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "Formalism.IndefR.Lift.IsThetaP" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN Formalism.IndefR.Lift.IsThetaP"
#print Formalism.IndefR.Lift.IsThetaP
#print axioms Formalism.IndefR.Lift.IsThetaP
#eval IO.println "RH_STAGE3_DECL_END Formalism.IndefR.Lift.IsThetaP"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mass.Levels.measure_comap_finE" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mass.Levels.measure_comap_finE"
#print GlobalTheory.Mass.Levels.measure_comap_finE
#print axioms GlobalTheory.Mass.Levels.measure_comap_finE
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mass.Levels.measure_comap_finE"

/- Conditional facts about the actual imported OrZero definition.
These do not construct ExAt and do not assert a nonzero selected value. -/
namespace RHStage3Realization
 theorem valid_of_exists {X : Type} [Zero X] (p : X → Prop) (x : X)
    (h : Formalism.IndefR.Links.OrZero p x) (hex : ∃ y, p y) : p x :=
  h.1 hex
 theorem zero_of_no_witness {X : Type} [Zero X] (p : X → Prop) (x : X)
    (h : Formalism.IndefR.Links.OrZero p x) (hn : ¬ ∃ y, p y) : x = 0 :=
  h.2 hn
end RHStage3Realization
#print RHStage3Realization.valid_of_exists
#print axioms RHStage3Realization.valid_of_exists
#print RHStage3Realization.zero_of_no_witness
#print axioms RHStage3Realization.zero_of_no_witness
#eval IO.println "RH_STAGE3_REALIZATION_BOUNDARY_ACCEPTED"
#eval IO.println "RH_STAGE3_REALIZATION_END"
