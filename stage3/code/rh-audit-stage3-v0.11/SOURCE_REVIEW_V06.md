# Source basis for supplier targets

Reviewed existing pinned evidence, without a new server run.

Common path: Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/.

1. LinkedTies.lean (v0.3 evidence), lines 32–77:
   GlobalTheory.GeoTies.linked_ties_alt is parameterized by Γ : GeoP.
   It creates ExtensionReading.of RX hE (SXE S) (OX Γ), constructs linkage
   witnesses, and at lines 74–75 obtains hcs from
   GlobalTheory.T.class_sum_divisibility_of_extensionWithLaw and applies hcs.2
   to a divisor-condition proof. Its import list includes
   ClassSumPinOfReadAtStatement.lean, not yet present in the reviewed snapshots.
2. PNmjOfPDivOfClassSumPin.lean (v0.3 evidence), lines 12–16:
   pNmj_of_pDiv_of_classSumPin_alt forwards hpin to
   GlobalTheory.T.lattice_family_adoption_fourth_alt.
3. NmjTAtTied.lean (v0.5 evidence) forwards hPin into the third comparison
   lemma and stores the resulting proof in its certificate.
4. EMEqThPe.lean (v0.5 evidence), lines 90–94 and 50–87:
   eM_eq_thPe_alt forwards hP to at_index_alt; the latter applies hP in a
   rewrite at line 76.

The v0.6 targets are names established by these sources. No unobserved
implementation theorem name is guessed. Compiled provenance will identify
source owners and the supplier wrapper's direct references. ClassSumPin-related
source modules receive explicit collection priority to reduce loss to caps.

This establishes where to look next, not that a Γ argument is necessary or
that the full headline proof has a defect. The targeted search is syntactic
and retains all incompleteness indicators.
