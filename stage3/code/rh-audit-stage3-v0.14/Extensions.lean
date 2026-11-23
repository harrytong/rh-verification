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

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.EMtTheta" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.EMtTheta"
#print GlobalTheory.HeightCounting.EMtTheta
#print axioms GlobalTheory.HeightCounting.EMtTheta
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.EMtTheta"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.RealExpansionExtraData" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.RealExpansionExtraData"
#print GlobalTheory.HeightCounting.RealExpansionExtraData
#print axioms GlobalTheory.HeightCounting.RealExpansionExtraData
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.RealExpansionExtraData"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.RealExpansionExtraData.mk" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.RealExpansionExtraData.mk"
#print GlobalTheory.HeightCounting.RealExpansionExtraData.mk
#print axioms GlobalTheory.HeightCounting.RealExpansionExtraData.mk
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.RealExpansionExtraData.mk"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.RealExpansionExtraData.th" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.RealExpansionExtraData.th"
#print GlobalTheory.HeightCounting.RealExpansionExtraData.th
#print axioms GlobalTheory.HeightCounting.RealExpansionExtraData.th
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.RealExpansionExtraData.th"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.RealExpansionExtraData.geo" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.RealExpansionExtraData.geo"
#print GlobalTheory.HeightCounting.RealExpansionExtraData.geo
#print axioms GlobalTheory.HeightCounting.RealExpansionExtraData.geo
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.RealExpansionExtraData.geo"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.defaultExtension" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.defaultExtension"
#print GlobalTheory.HeightCounting.defaultExtension
#print axioms GlobalTheory.HeightCounting.defaultExtension
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.defaultExtension"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Up.extensionWithLaw" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Up.extensionWithLaw"
#print GlobalTheory.HeightCounting.Up.extensionWithLaw
#print axioms GlobalTheory.HeightCounting.Up.extensionWithLaw
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Up.extensionWithLaw"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Up.extensionWithList" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Up.extensionWithList"
#print GlobalTheory.HeightCounting.Up.extensionWithList
#print axioms GlobalTheory.HeightCounting.Up.extensionWithList
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Up.extensionWithList"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.HeightCounting.Up.extensionWithOrigin" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.HeightCounting.Up.extensionWithOrigin"
#print GlobalTheory.HeightCounting.Up.extensionWithOrigin
#print axioms GlobalTheory.HeightCounting.Up.extensionWithOrigin
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.HeightCounting.Up.extensionWithOrigin"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.ClassSumPinLink.pIota_classSumPin_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.ClassSumPinLink.pIota_classSumPin_alt"
#print GlobalTheory.ClassSumPinLink.pIota_classSumPin_alt
#print axioms GlobalTheory.ClassSumPinLink.pIota_classSumPin_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.ClassSumPinLink.pIota_classSumPin_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.ClassSumPinLink.classSumPin_of_read" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.ClassSumPinLink.classSumPin_of_read"
#print GlobalTheory.ClassSumPinLink.classSumPin_of_read
#print axioms GlobalTheory.ClassSumPinLink.classSumPin_of_read
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.ClassSumPinLink.classSumPin_of_read"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Fc.S0.Open0ProofU.open_orbit_of_unramified_exponents_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Fc.S0.Open0ProofU.open_orbit_of_unramified_exponents_alt"
#print GlobalTheory.Fc.S0.Open0ProofU.open_orbit_of_unramified_exponents_alt
#print axioms GlobalTheory.Fc.S0.Open0ProofU.open_orbit_of_unramified_exponents_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Fc.S0.Open0ProofU.open_orbit_of_unramified_exponents_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Fc.StageOneU.member_bundles_large_unramified_exponents_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Fc.StageOneU.member_bundles_large_unramified_exponents_alt"
#print GlobalTheory.Fc.StageOneU.member_bundles_large_unramified_exponents_alt
#print axioms GlobalTheory.Fc.StageOneU.member_bundles_large_unramified_exponents_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Fc.StageOneU.member_bundles_large_unramified_exponents_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_prime_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_prime_alt"
#print GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_prime_alt
#print axioms GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_prime_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_prime_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.Mem.Top.Bl.has3_neo_of_localLanglands_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.Top.Bl.has3_neo_of_localLanglands_alt"
#print GlobalTheory.Mem.Top.Bl.has3_neo_of_localLanglands_alt
#print axioms GlobalTheory.Mem.Top.Bl.has3_neo_of_localLanglands_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.Top.Bl.has3_neo_of_localLanglands_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.T.sFino_and_secondNo_of_sFinl'" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.T.sFino_and_secondNo_of_sFinl'"
#print GlobalTheory.T.sFino_and_secondNo_of_sFinl'
#print axioms GlobalTheory.T.sFino_and_secondNo_of_sFinl'
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.T.sFino_and_secondNo_of_sFinl'"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.T.all_stages_at_member_of_specializations_alt" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.T.all_stages_at_member_of_specializations_alt"
#print GlobalTheory.T.all_stages_at_member_of_specializations_alt
#print axioms GlobalTheory.T.all_stages_at_member_of_specializations_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.T.all_stages_at_member_of_specializations_alt"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Provenance.inspect env "GlobalTheory.T.lv3Mv_extensionWithOrigin_and_NEog" 4096
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.T.lv3Mv_extensionWithOrigin_and_NEog"
#print GlobalTheory.T.lv3Mv_extensionWithOrigin_and_NEog
#print axioms GlobalTheory.T.lv3Mv_extensionWithOrigin_and_NEog
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.T.lv3Mv_extensionWithOrigin_and_NEog"

run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Search.inspect env "GlobalTheory.ClassSumPinLink.pIota_classSumPin_alt" "hN"
run_cmd do
  let env ← getEnv
  liftIO <| RHStage3Search.inspect env "GlobalTheory.ClassSumPinLink.classSumPin_of_read" "hth"
#eval IO.println "RH_STAGE3_EXTENSIONS_END"
