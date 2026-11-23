# Prior-source basis for v0.10

This is preparation from existing evidence, not the outcome of the new probe.

v0.9 established that Fin3.emtTheta_L_alt uses StrictHenselianAcyclicLevel.c and HeightCountingCharacterData.th. SameGaloisLevelExists.lean defines the former level and its Nonempty obligation; RootsOfUnityRingLeWittIntegers.lean defines the character record.

The v0.8 collected-source files already contain an upstream candidate route. All TPS paths below mean Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/.

- TPS/SeriesCoverOfPrimitive.lean: T.stage_c_nonempty_of_prints_third_layer delegates to Up.ChoiceEx.stage_c_nonempty_of_published_inputs, whose expression applies Up.ChoiceEx.sc_of_sck_alt to T.stageCExists_of_casselmanWallach.
- TPS/LevelComparisonChoicesExistAtAllPlaces.lean: that wrapper delegates to LevCmp.stageCExists_of_harishChandra_serN. It uses T.nonGalois_exists_choice_alt to produce a character-data witness after preparing choice data.
- TPS/NonGaloisExistsChoice.lean: T.nonGalois_exists_choice_alt delegates to ChoiceRead.exists_stC_choice_alt. Its body invokes T.local_component_at_place_determined_alt, extracts e, u, hb, hl, hth, defines a scaled map G using the inverse of u, and constructs HeightCountingCharacterData. The final field is supplied through ChoiceRead.emtTheta_withE, pick_eq, and (hth v hv i).smul_inv.
- The new probe will resolve the exact compiled owners of sc_of_sck_alt, local_component_at_place_determined_alt, and emtTheta_withE; their implementation bodies were not inspected in this preparation. It will also collect the owners' source and bounded import context.

All twelve target names therefore come from inspected declarations or explicit source applications. No claim is made that they form an indispensable route in all five headline proofs. Further source may expose another transport or a stronger upstream obligation.

Frozen evidence anchors:
- v0.8 archive: d2c2e5b5b612cd06cb0dbea5c5ecacfbbadfd4439c94bcfc3909a1517722c309
- v0.9 archive: dbb49c17bb13c9f34cbaa9b0179473a4c9670f98f25f2db2cb4ee75e692a671d
- Project revision: 753431bfe28701f6f3937f664fcaf08daa139c03

This package reuses the existing provenance helper and fixture bytes. It adds no new expression-search algorithm or global traversal.
