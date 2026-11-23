# Source basis for v0.11

Prior evidence archive: stage3-evidence(9).zip, SHA-256 1cff7e206078852cc67a4523e029301367dfdb032241b2d82202f4e94dcb2f56.
Project pin: 753431bfe28701f6f3937f664fcaf08daa139c03.

In the collected ThirdPlaceSeries/LocalComponentAtPlaceDetermined.lean:
- GlobalTheory.PlaceRead.exists_local_component_at_place_alt is declared at line 36 and invokes GlobalTheory.T.thetaLift_twistLevelForm_eq_unit_mul_classSum at line 72.
- GlobalTheory.PlaceRead.exists_basisAt_latAt_thetaAt_of_atPlace is declared at line 95; it invokes GlobalTheory.T.chosenField_forms_proportional_of_readings at 147 and GlobalTheory.T.exists_integral_unit_of_isUnitAwayFromLevel_embedding at 151.
- GlobalTheory.PlaceRead.exists_local_map_at_place_alt is declared at line 166 and constructs the AtPlace record used by that supplier.

The first three suppliers' declaration bodies were not located in the bounded v0.10 source set. This probe obtains their exact owner modules directly from Main. The caller implementations are also targets so their direct compiled references can corroborate the source calls.

GlobalTheory.ChoiceRead.ThetaAt is defined in Proofs/InertiaEigenvalues/ChoiceSideWithE.lean, and GlobalTheory.HeightCounting.EMtTheta in Definitions/AutomorphicMembership/SubsetTwistExceptionalPlaces.lean. Both were inspected in prior snapshots. They are included for the conditional identity's exact stored type and definition.

No result of the new probe is asserted here. No new Lean helper logic or mathematical lemma is introduced; the established provenance helper is reused unchanged.
