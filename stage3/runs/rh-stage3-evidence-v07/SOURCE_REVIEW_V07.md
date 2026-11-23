# Why these v0.7 targets

Input evidence: v0.6 archive SHA-256 a809a74f9a95d7cd877777872e1c0ff86278e528bb4059ea29ba6c94282e7421, plus previously collected pinned source. The provider findings report distinguishes argument occurrence from necessity.

ClassSumPinOfReadAt.lean (ThirdPlaceSeries), lines 89–95: hN applied to q.x.nx.2 supplies m; m.1.th supplies EMtTheta; the proof transports this through ReadAtAlt to classSumPin_of_readAt_of_pDiv. The corresponding earlier ClassSumDivisibilityBundle.lean implementation applies its hth argument.

SameGaloisLevelExists.lean defines extensionWithLaw as defaultExtension × PLift BkLaw. RootsOfUnityRingLeWittIntegers.lean defines defaultExtension through RealExpansionExtraData, whose fields include th : EMtTheta and a separate geo requirement.

Previously collected OpenOrbitOfUnramifiedExponents.lean supplies hNE by x.1 from extensionWithList. SettingsFormsExistList.lean defines that stronger record by adding ListPin. ExtensionWithOrigin.lean adds OriginData. Those projection conversions leave the underlying construction unresolved.

Previously collected MemberBundlesLargeUnramifiedExponents.lean calls member_exists_baseLattice_alt. Its implementation exists_baseLattice_of_prime_alt in ExistsBaseLatticeOfPrime.lean uses all_stages_at_member_of_specializations_alt, sFino_and_secondNo_of_sFinl', has3_neo_of_localLanglands_alt, and lv3Mv_extensionWithOrigin_and_NEog. Their exact declarations are targeted to retrieve the construction route rather than guessing implementation filenames. Each additional source and declaration still needs review at actual inputs.

Target names are taken from explicit qualified source references or generated structure/projection names. They have not been resolved locally in Lean; the server probe will fail visibly if any differs. This source review is a selection rationale, not an end-to-end proof of witness construction or of the critics' claim.
