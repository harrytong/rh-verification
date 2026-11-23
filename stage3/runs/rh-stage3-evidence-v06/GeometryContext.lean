import Main
import Development.AutomorphicArithmetic.ThetaCorrespondence.FockModels.EveryCharacterE
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.LocalTypeDictionary.FunctionalsSeparateOfHoweUnramOfSiegelWeil
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.LocalTypeDictionary.TestVectorAtDatumOfJoin
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.LocalTypeDictionary.EvaluationGridOfJoin
import Mathlib
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.CohomologicalCsdTempered
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.BernsteinUnitaryProductIrreducible
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.LiftLambdaBound
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.TopPlug
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.At23OfAll
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.Prm1
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.RowGood
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.ColumnChoiceWithTies
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.CountsIrreducibilityConstants
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.BoundAtTwoThreeFamilyFon
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.Hyps
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.DefiniteSideCondition
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.LeafInfinitePlaceBound
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.FourierCoefficientFitOfJoin
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.ExportSt
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.Realised
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.SurjectiveAndLowWeightOfUnramifiedExponents
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.NormChoiceOfExtension
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.SettingsFormsExistList
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.GeometricWeakTies
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.CoreAltAltBis
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.ExtensionWithAtProperty
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.RowFunAtGridA
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.OpenOrbitOfUnramifiedExponents
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.ExtensionWithOrigin
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.OpenAndLinkedOfStrongerExtension
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.LinkedBundlesL3OfOpen
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.SameGaloisLevelExists
import Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.HypothesesNonemptyOfUnramifiedExponents
import Development.AutomorphicArithmetic.Foundations.LocalLanglands.IsRecTOfIsRec

set_option synthInstance.maxHeartbeats 200000
set_option pp.all true

section
section
open Formalism.BasicNotions Formalism.MainNotions GlobalTheory.EX GlobalTheory.EX.OB GlobalTheory.Mem GlobalTheory.Mem.Top GlobalTheory.Mem.Top.Bl GlobalTheory.Fc GlobalTheory.Mem.LiteralAutomorphy
namespace UpperTheory.Lit
open UpperTheory.Top
theorem stage3_bundle_with_context : _root_.GlobalTheory.Fc.S0.UnitaryGroupThirdPlaceHypotheses → _root_.GlobalTheory.FunPr.ThetaLocalInputs → GlobalTheory.IndefiniteRowSideFullHecke.WeilTensorModels.ThetaIntegralsAgree → GlobalTheory.IndefiniteRowSideFullHecke.WeilTensorModels.LocalMatching → _root_.GlobalTheory.CovTop.CovolumeBoundOfX → ∀ (hL : _root_.UpperTheory.Zero.LLC.RecTExists), (∀ cDep : ℝ, _root_.GlobalTheory.Fc.RL.LinkedAt (_root_.GlobalTheory.Mem.Top.Bl.parametersOfDependence hL cDep) (fun Q L => _root_.GlobalTheory.Fc.R1.SlotNormCondition Q L fun 𝒞 => Formalism.MainNotions.Closed 𝒞 fun Fm _ => _root_.GlobalTheory.NLink.BoundAtTwoThreeFamilyFonAlt Fm)) → Nonempty (_root_.GlobalTheory.Fc.HypsAlt S0.NL _root_.GlobalTheory.Fc.DefiniteSideCondition) := by
  intro P F hA hM hX hL hN
  have C := P.litN
  have hS : GlobalTheory.IndefiniteRowSideFullHecke.LevelPlusSubgroup.FunctionalsSeparate :=
    _root_.UpperTheory.Lit.functionalsSeparate_of_howeUnram_of_siegelWeil F GlobalTheory.Hk3.howeUnram_holds P.siegelWeilUnitaryConvergent
  have hRat : S0.RowRat := GlobalTheory.Mem.LiteralAutomorphy.rowRatW_of_rowTest (_root_.GlobalTheory.T.test_vector_assembly_holds F.siegelSetUnitary F.howeDualityReal
    P.greenCuspidal F C.join C.fe hA hM hS)
  have hFit : _root_.GlobalTheory.BigTop.Fun.ConstantFunctionFits @GlobalTheory.BigTop.Fun.Fld := _root_.GlobalTheory.BigTop.Fun.Close.fourier_coefficient_fit_of_join_alt F C.join C.fe hA hM hS (_root_.GlobalTheory.Fc.S0.ontoX_and_lamLow_of_unitaryGroupHypotheses' P).2
  obtain ⟨CF1, hCF1⟩ := _root_.GlobalTheory.Mem.LiteralAutomorphy.evaluation_grid_of_join F.howeDualityReal hM F C.join C.fe hA
    (_root_.GlobalTheory.WeilConv.twisted_weil_representation_convergence F.siegelSetUnitary F) (_root_.GlobalTheory.T.twisted_local_factors_match F.howeDualityReal F hA hM)
    (_root_.GlobalTheory.T.twisted_square_theta_integrals_eq F hA hM) hS
  obtain ⟨CF0, hCF0⟩ := _root_.GlobalTheory.Fc.StageOne.rowFun_at_gridA_alt P.discreteSeriesCover P.harishChandraModules P.cuspRapidDecay P.casselmanWallach
    P.rayClassFieldSt hFit
  have hEv : EvLgG (GridA (max CF0 CF1)) := hCF1 _ (le_max_right _ _)
  have hOpen1 : _root_.GlobalTheory.Fc.S0.OpenParameterStatements (_root_.GlobalTheory.Mem.Top.Bl.parametersOfDependence hL (max CF0 CF1)) := _root_.GlobalTheory.T.open0_of_unitary_group_hypotheses P hL (max CF0 CF1)
  trace "RH_STAGE3_CONTEXT G1_BEFORE_MONOTONICITY"
  trace_state
  have hMono := _root_.GlobalTheory.Glob.open_and_linked_of_stronger_extension_alt hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL (max CF0 CF1))
    (_root_.GlobalTheory.Mem.LiteralAutomorphy.extensionWithAtProperty hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithOrigin hL (max CF0 CF1)) (GridA (max CF0 CF1))) SExt.none (geoCl anyGeometry)
    (fun _ _ _ _ _ _ _ _ _ _ _ _ _ x => ⟨x.1.1⟩)
  trace "RH_STAGE3_CONTEXT G2_AFTER_MONOTONICITY"
  trace_state
  have hOpenA := hMono.2 hOpen1
  trace "RH_STAGE3_CONTEXT G3_AFTER_OPEN_PACKAGE"
  trace_state
  have hFun := hCF0 (max CF0 CF1) (le_max_left _ _) hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithOrigin hL (max CF0 CF1)) SExt.none (geoCl anyGeometry)
    (fun _ _ _ _ _ _ _ _ _ _ _ _ _ x => ⟨x.1⟩) hOpenA
  trace "RH_STAGE3_CONTEXT G4_AFTER_FUNCTIONAL"
  trace_state
  have hL3 := _root_.GlobalTheory.Glob.CovolRow.linked_bundles_l3_of_open_alt P.discreteSeriesCover P.harishChandraModules P.cuspRapidDecay
    P.casselmanWallach P.rayClassFieldSt hX hL (_root_.GlobalTheory.Mem.LiteralAutomorphy.extensionWithAtProperty hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithOrigin hL (max CF0 CF1)) (GridA (max CF0 CF1)))
    SExt.none (geoCl anyGeometry) (fun _ _ _ _ _ _ _ _ _ _ _ _ _ x => ⟨x.1.1.1⟩) hOpenA
  trace "RH_STAGE3_CONTEXT G5_BEFORE_FINAL_CONSUMER"
  trace_state
  exact _root_.GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt P hRat hL (max CF0 CF1) (GridA (max CF0 CF1)) hEv (hN (max CF0 CF1)) hFun hL3

end UpperTheory.Lit
end
end

#check UpperTheory.Lit.stage3_bundle_with_context
#print axioms UpperTheory.Lit.stage3_bundle_with_context

#print UpperTheory.Lit.stage3_bundle_with_context
#eval IO.println "RH_STAGE3_GEOMETRY_END"

#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.Top.Bl.anyGeometry"
#print GlobalTheory.Mem.Top.Bl.anyGeometry
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.Top.Bl.anyGeometry"

#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.Top.Bl.geoCl"
#print GlobalTheory.Mem.Top.Bl.geoCl
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.Top.Bl.geoCl"

#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.Top.Bl.OAt"
#print GlobalTheory.Mem.Top.Bl.OAt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.Top.Bl.OAt"

#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.Top.Bl.OX"
#print GlobalTheory.Mem.Top.Bl.OX
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.Top.Bl.OX"

#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Glob.open_and_linked_of_stronger_extension_alt"
#print GlobalTheory.Glob.open_and_linked_of_stronger_extension_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Glob.open_and_linked_of_stronger_extension_alt"

#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Fc.StageOne.rowFun_at_gridA_alt"
#print GlobalTheory.Fc.StageOne.rowFun_at_gridA_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Fc.StageOne.rowFun_at_gridA_alt"

#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Glob.CovolRow.linked_bundles_l3_of_open_alt"
#print GlobalTheory.Glob.CovolRow.linked_bundles_l3_of_open_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Glob.CovolRow.linked_bundles_l3_of_open_alt"

#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt"
#print GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt"

#eval IO.println "RH_STAGE3_GEOMETRY_DECLARATIONS_END"

#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Fc.S0.OpenParameterStatements"
#print GlobalTheory.Fc.S0.OpenParameterStatements
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Fc.S0.OpenParameterStatements"

#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Fc.S0.GeometricWeakCompatibility'"
#print GlobalTheory.Fc.S0.GeometricWeakCompatibility'
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Fc.S0.GeometricWeakCompatibility'"

#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.Mem.Top.Bl.LamAre"
#print GlobalTheory.Mem.Top.Bl.LamAre
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.Mem.Top.Bl.LamAre"
