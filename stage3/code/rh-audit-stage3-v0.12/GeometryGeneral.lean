import Main
set_option pp.all true
set_option synthInstance.maxHeartbeats 200000
open Formalism.BasicNotions Formalism.MainNotions GlobalTheory.EX GlobalTheory.EX.OB
open GlobalTheory.Mem GlobalTheory.Mem.Top GlobalTheory.Mem.Top.Bl GlobalTheory.Fc
namespace RHStage3Followup
theorem stage3_open_supplier_baseline : _root_.GlobalTheory.Fc.S0.UnitaryGroupThirdPlaceHypotheses → ∀ (hL : _root_.UpperTheory.Zero.LLC.RecTExists) (cDep : ℝ), _root_.GlobalTheory.Fc.S0.OpenParameterStatements (_root_.GlobalTheory.Mem.Top.Bl.parametersOfDependence hL cDep) := by
  intro P hL cDep
  have hNE : ∀ K B f T w Z Wt p0 t nch n xd c, _root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep K B f T w Z Wt p0 t nch n xd c →
      Nonempty (_root_.GlobalTheory.HeightCounting.Up.extensionWithLaw hL K B f T w Z Wt p0 t nch n xd c) := fun _ _ _ _ _ _ _ _ _ _ _ _ _ x => ⟨x.1⟩
  have hB : ∀ (K : Ctx) (q : WPt (_root_.GlobalTheory.Mem.Top.Bl.parametersOfDependence hL cDep).s K), GlobalTheory.Mem.R3.Rw.BkLaw (q.w.D q.Z) := fun _ q => q.x.nx.2.1.2.down
  have hPA := _root_.GlobalTheory.T.linkedAt_hPA_prmR hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none (geoCl anyGeometry)
  have hDc := _root_.GlobalTheory.T.linkedAt_hDcPtG_prmR hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none (geoCl anyGeometry)
  have hTie := _root_.GlobalTheory.T.linkedAt_tie_of_nonempty_extensionWithLaw P.discreteSeriesCover P.harishChandraModules P.casselmanWallach P.weilRepresentationUnitaryPair
    P.discreteSeriesExists P.harishChandraFinite P.cuspRapidDecay hL _ SExt.none (geoCl anyGeometry) hNE
  have hJ := _root_.GlobalTheory.T.entries_combined_real_alt P.weilRepresentationUnitaryPair P.discreteSeriesExists P.discreteSeriesCover P.harishChandraModules
    P.casselmanWallach P.harishChandraFinite P.cuspRapidDecay hL _ SExt.none (geoCl anyGeometry) hPA hDc hTie
  have hMi := _root_.GlobalTheory.T.main_theorem_published_inputs_third_alt_alt P.harishChandraFinite P.cuspRapidDecay P.discreteSeriesCover P.harishChandraModules P.casselmanWallach
    GlobalTheory.Hk3.howeUnram_holds P.weilRepresentationUnitaryPair P.weilSiegelFormulaUnitary P.siegelWeilUnitaryConvergent
    P.doublingMethod P.unramifiedDoublingGL P.discreteSeriesClassification P.strongApproxSU P.siegelWeilUnitaryConvergent2
    hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none (geoCl anyGeometry)
  have hDiv := _root_.GlobalTheory.T.bk_law_entries_alt P.weilRepresentationUnitaryPair P.discreteSeriesExists P.harishChandraFinite P.cuspRapidDecay
    P.discreteSeriesCover P.harishChandraModules P.casselmanWallach hL _ SExt.none (geoCl anyGeometry) hB hMi.1
  have hLam := _root_.GlobalTheory.T.real_group_inputs_combined_alt_alt P.weilRepresentationUnitaryPair P.discreteSeriesExists P.harishChandraFinite P.cuspRapidDecay
    P.harishChandraAnalyticity P.discreteSeriesClassification P.cuspTraceClass P.dixmierMalliavinFactorisation
    P.flathFactorisation
    P.zelevinskyPolynomialRing P.geometricLemma P.greenCuspidal hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none (geoCl anyGeometry)
  have hKap := _root_.GlobalTheory.T.harish_chandra_inputs_combined_alt_alt P.harishChandraFinite P.cuspRapidDecay P.discreteSeriesCover P.harishChandraModules
    P.casselmanWallach P.harishChandraAnalyticity P.discreteSeriesClassification P.cuspTraceClass
    P.dixmierMalliavinFactorisation P.flathFactorisation P.zelevinskyPolynomialRing P.geometricLemma P.greenCuspidal
    hL _ SExt.none (geoCl anyGeometry) hLam
  have hGood := _root_.GlobalTheory.T.linked_bundles_good_of_local_langlands_alt_alt (GlobalTheory.GreenBridge.green_of_regular P.greenRegularCharacters) P.zelevinskyPolynomialRing hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none (geoCl anyGeometry) hNE
  have hLab := _root_.GlobalTheory.T.good_ft_entries_alt_alt (GlobalTheory.GreenBridge.green_of_regular P.greenRegularCharacters) P.zelevinskyPolynomialRing hL _ SExt.none (geoCl anyGeometry) hNE hGood.1
  have hGeo := _root_.GlobalTheory.T.linkedAt_geometricWeakTies_of_tie P.rayClassFieldSt hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none (geoCl anyGeometry) hNE hDiv hTie
  have hDf := _root_.GlobalTheory.T.weil_unitary_entries' P.weilRepresentationUnitaryPair P.discreteSeriesExists P.harishChandraFinite P.cuspRapidDecay
    hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none (geoCl anyGeometry)
  exact ⟨hPA, hLam, hDiv, hDc, hJ, hTie, hLab, hGood.2, hGeo, hMi.2, hKap, hDf⟩
#check stage3_open_supplier_baseline
#eval IO.println "RH_STAGE3_SUPPLIER_BASELINE_ACCEPTED"
theorem stage3_open_supplier_arbitrary (auditGamma : GeoP) : _root_.GlobalTheory.Fc.S0.UnitaryGroupThirdPlaceHypotheses → ∀ (hL : _root_.UpperTheory.Zero.LLC.RecTExists) (cDep : ℝ), _root_.GlobalTheory.Fc.S0.OpenParameterStatements (_root_.GlobalTheory.Mem.Top.Bl.parametersOfExtension (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none auditGamma) := by
  intro P hL cDep
  have hNE : ∀ K B f T w Z Wt p0 t nch n xd c, _root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep K B f T w Z Wt p0 t nch n xd c →
      Nonempty (_root_.GlobalTheory.HeightCounting.Up.extensionWithLaw hL K B f T w Z Wt p0 t nch n xd c) := fun _ _ _ _ _ _ _ _ _ _ _ _ _ x => ⟨x.1⟩
  have hB : ∀ (K : Ctx) (q : WPt (_root_.GlobalTheory.Mem.Top.Bl.parametersOfExtension (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none auditGamma).s K), GlobalTheory.Mem.R3.Rw.BkLaw (q.w.D q.Z) := fun _ q => q.x.nx.2.1.2.down
  have hPA := _root_.GlobalTheory.T.linkedAt_hPA_prmR hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none auditGamma
  have hDc := _root_.GlobalTheory.T.linkedAt_hDcPtG_prmR hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none auditGamma
  have hTie := _root_.GlobalTheory.T.linkedAt_tie_of_nonempty_extensionWithLaw P.discreteSeriesCover P.harishChandraModules P.casselmanWallach P.weilRepresentationUnitaryPair
    P.discreteSeriesExists P.harishChandraFinite P.cuspRapidDecay hL _ SExt.none auditGamma hNE
  have hJ := _root_.GlobalTheory.T.entries_combined_real_alt P.weilRepresentationUnitaryPair P.discreteSeriesExists P.discreteSeriesCover P.harishChandraModules
    P.casselmanWallach P.harishChandraFinite P.cuspRapidDecay hL _ SExt.none auditGamma hPA hDc hTie
  have hMi := _root_.GlobalTheory.T.main_theorem_published_inputs_third_alt_alt P.harishChandraFinite P.cuspRapidDecay P.discreteSeriesCover P.harishChandraModules P.casselmanWallach
    GlobalTheory.Hk3.howeUnram_holds P.weilRepresentationUnitaryPair P.weilSiegelFormulaUnitary P.siegelWeilUnitaryConvergent
    P.doublingMethod P.unramifiedDoublingGL P.discreteSeriesClassification P.strongApproxSU P.siegelWeilUnitaryConvergent2
    hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none auditGamma
  have hDiv := _root_.GlobalTheory.T.bk_law_entries_alt P.weilRepresentationUnitaryPair P.discreteSeriesExists P.harishChandraFinite P.cuspRapidDecay
    P.discreteSeriesCover P.harishChandraModules P.casselmanWallach hL _ SExt.none auditGamma hB hMi.1
  have hLam := _root_.GlobalTheory.T.real_group_inputs_combined_alt_alt P.weilRepresentationUnitaryPair P.discreteSeriesExists P.harishChandraFinite P.cuspRapidDecay
    P.harishChandraAnalyticity P.discreteSeriesClassification P.cuspTraceClass P.dixmierMalliavinFactorisation
    P.flathFactorisation
    P.zelevinskyPolynomialRing P.geometricLemma P.greenCuspidal hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none auditGamma
  have hKap := _root_.GlobalTheory.T.harish_chandra_inputs_combined_alt_alt P.harishChandraFinite P.cuspRapidDecay P.discreteSeriesCover P.harishChandraModules
    P.casselmanWallach P.harishChandraAnalyticity P.discreteSeriesClassification P.cuspTraceClass
    P.dixmierMalliavinFactorisation P.flathFactorisation P.zelevinskyPolynomialRing P.geometricLemma P.greenCuspidal
    hL _ SExt.none auditGamma hLam
  have hGood := _root_.GlobalTheory.T.linked_bundles_good_of_local_langlands_alt_alt (GlobalTheory.GreenBridge.green_of_regular P.greenRegularCharacters) P.zelevinskyPolynomialRing hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none auditGamma hNE
  have hLab := _root_.GlobalTheory.T.good_ft_entries_alt_alt (GlobalTheory.GreenBridge.green_of_regular P.greenRegularCharacters) P.zelevinskyPolynomialRing hL _ SExt.none auditGamma hNE hGood.1
  have hGeo := _root_.GlobalTheory.T.linkedAt_geometricWeakTies_of_tie P.rayClassFieldSt hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none auditGamma hNE hDiv hTie
  have hDf := _root_.GlobalTheory.T.weil_unitary_entries' P.weilRepresentationUnitaryPair P.discreteSeriesExists P.harishChandraFinite P.cuspRapidDecay
    hL (_root_.GlobalTheory.HeightCounting.Up.extensionWithList hL cDep) SExt.none auditGamma
  exact ⟨hPA, hLam, hDiv, hDc, hJ, hTie, hLab, hGood.2, hGeo, hMi.2, hKap, hDf⟩
#print stage3_open_supplier_arbitrary
#print axioms stage3_open_supplier_arbitrary
#eval IO.println "RH_STAGE3_ARBITRARY_SUPPLIER_ACCEPTED"

-- Empty-domain caution: this is a conditional package at False, not a point.
theorem stage3_open_supplier_false :
    GlobalTheory.Fc.S0.UnitaryGroupThirdPlaceHypotheses →
    ∀ (hL : UpperTheory.Zero.LLC.RecTExists) (cDep : ℝ),
    GlobalTheory.Fc.S0.OpenParameterStatements
      (parametersOfExtension (GlobalTheory.HeightCounting.Up.extensionWithList hL cDep)
        SExt.none (fun _ _ _ => False)) :=
  stage3_open_supplier_arbitrary (fun _ _ _ => False)

theorem stage3_false_closure_empty {D : D7} {J : Formalism.L2.Pj.Core D} {X : DivX D} :
    ¬ GeoCl (fun _ _ _ => False) D J X := by
  intro h
  induction h with
  | base hp => exact hp
  | step N h previous ih => exact ih

#print stage3_open_supplier_false
#print axioms stage3_open_supplier_false
#print stage3_false_closure_empty
#print axioms stage3_false_closure_empty
#eval IO.println "RH_STAGE3_GENERAL_SUPPLIER_END"
end RHStage3Followup
