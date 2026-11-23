# Target selection for v0.9

All references below are to the collected source in v0.8 evidence. TPS abbreviates Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries. IW abbreviates Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition.

| Target (GlobalTheory prefix) | Grounding |
| --- | --- |
| HeightCounting.Fin3.emtTheta_L_alt | TPS/EmtThetaLStatement.lean:15 delegates to it and imports EmtThetaL. |
| T.emtTheta_of_yRel | TPS/EmtThetaLStatement.lean:14–15. |
| T.normalisedReadings_related_localizedAdelicData | TPS/FinitenessOfHyp.lean:60 supplies YRel via this theorem. IW/FinitenessOfHyp.lean imports NormalisedReadingsRelatedLocalizedAdelicDataStatement. |
| HeightCounting.Fin3.YRel | IW/TwistDataAgreeAcrossCoefficientsLocalized.lean:73–76, within the Fin3 namespace. |
| HeightCounting.Fin3.yStructureLocal | TPS/LocalMultiplicityFamily.lean:21–28. |
| HeightCounting.Fin3.characterChoiceLocal | TPS/LocalMultiplicityFamily.lean:48. |
| HeightCounting.Fin3.nonempty_nMore_of_xdAll | TPS/RowsAtStart.lean:95–118, explicit .th assignment at 113. |
| HeightCounting.Fin3.thetaTie_yStructureLocal_nonempty | TPS/LocalMultiplicityFamily.lean:56–60, uses l.b.geo. |
| HeightCounting.EMtTheta | Definitions/AutomorphicMembership/SubsetTwistExceptionalPlaces.lean:136–143. |
| HeightCounting.Fin3.exists_base_level_rXs_and_yRel | TPS/FinitenessOfHyp.lean:51–60, producer call site. |

The run resolves owners from compiled metadata. Filename guesses are not used as proof of ownership. EmtThetaL was previously beyond the source-depth boundary; this phase gives its target owner and explicit source path priority.

No new Lean traversal/classifier is introduced. The existing provenance helper is reused exactly. The source collector and its selection/cap semantics are unchanged from v0.8.
