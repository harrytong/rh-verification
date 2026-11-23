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
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Fc.RL.at_tie_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Fc.RL.at_tie_alt"
#print GlobalTheory.Fc.RL.at_tie_alt
#print axioms GlobalTheory.Fc.RL.at_tie_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Fc.RL.at_tie_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.BigTop.PtAt.nmjT_at_tied_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.BigTop.PtAt.nmjT_at_tied_alt"
#print GlobalTheory.BigTop.PtAt.nmjT_at_tied_alt
#print axioms GlobalTheory.BigTop.PtAt.nmjT_at_tied_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.BigTop.PtAt.nmjT_at_tied_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.T.eventually_onPt_of_pDiv_ties_and_onPt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.T.eventually_onPt_of_pDiv_ties_and_onPt"
#print GlobalTheory.T.eventually_onPt_of_pDiv_ties_and_onPt
#print axioms GlobalTheory.T.eventually_onPt_of_pDiv_ties_and_onPt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.T.eventually_onPt_of_pDiv_ties_and_onPt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Fc.Ind.RowPointSummands" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Fc.Ind.RowPointSummands"
#print GlobalTheory.Fc.Ind.RowPointSummands
#print axioms GlobalTheory.Fc.Ind.RowPointSummands
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Fc.Ind.RowPointSummands"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.CovHt.FrameCmp.htCmp" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.CovHt.FrameCmp.htCmp"
#print GlobalTheory.CovHt.FrameCmp.htCmp
#print axioms GlobalTheory.CovHt.FrameCmp.htCmp
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.CovHt.FrameCmp.htCmp"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.CovHt.HTCmp" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.CovHt.HTCmp"
#print GlobalTheory.CovHt.HTCmp
#print axioms GlobalTheory.CovHt.HTCmp
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.CovHt.HTCmp"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.CovHt.cover_height_comparison" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.CovHt.cover_height_comparison"
#print GlobalTheory.CovHt.cover_height_comparison
#print axioms GlobalTheory.CovHt.cover_height_comparison
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.CovHt.cover_height_comparison"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Fc.Ind.eventual_L3_of_covolume_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Fc.Ind.eventual_L3_of_covolume_alt"
#print GlobalTheory.Fc.Ind.eventual_L3_of_covolume_alt
#print axioms GlobalTheory.Fc.Ind.eventual_L3_of_covolume_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Fc.Ind.eventual_L3_of_covolume_alt"

#eval IO.println "RH_STAGE3_CONSUMER_IMPLEMENTATIONS_END"
