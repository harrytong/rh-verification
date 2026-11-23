# Target selection from v0.7 evidence

Input archive SHA-256: a5505fc8e26a31148f41d191f5ea51297ef9b6370eaa6e8db2cf98e0bceb5ea6.

- T.sFin_and_sFinl_of_archCmp_sEta_thetaData: AllStagesAtMemberOfSpecializations.lean:42. FinitenessOfHyp is an import there and was excluded by v0.7's source file cap. Its ownership will be resolved from compiled metadata, not assumed from the filename.
- Up.sFino_of_alt: FiniteLevelAndSecond.lean:118.
- Up.FinitenessStatement, Up.FinitenessListStatement, Up.SpectralFiniteness: v0.7 compiled reference records, with owners SameGaloisLevelExists, SettingsFormsExistList, ExtensionWithOrigin respectively.
- Up.all_stages_of_specializations_alt: AllStagesAtMemberOfSpecializations.lean:32–46.
- Up.sXd_all_alt: AllStagesAtMemberOfSpecializations.lean:42.
- Up.lv3Mv_extensionWithOrigin_and_nEog: OrgOfKept.lean:25–47 and the corresponding compiled reference record.

All names use the GlobalTheory prefix; Up abbreviates HeightCounting.Up. FinitenessOfHyp and SXdAll are explicit source priorities. Owner metadata determines the source modules of all eight targets. Actual constructor identification remains a review task after evidence collection.

This package changes no shared Lean helper or fixture. Construction.lean uses only the established provenance helper and the same inspection/print command pattern. It does not repeat the two capped v0.7 binder searches.
