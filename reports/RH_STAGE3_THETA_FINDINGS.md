# Stage 3 v0.9: theta identity transport and its upstream obligation

Review date: 23 November 2026. This is a review of Harry Tong's uploaded execution logs, compiled-declaration reference records, and pinned source snapshots. Lean was not rerun in this review environment.

## Main finding

The implementation of `GlobalTheory.HeightCounting.Fin3.emtTheta_L_alt` transports an existing theta identity from `l.c.th` to a localized reading. It does not establish that identity from scratch at this point.

The source explicitly uses `hY.eW` to convert the representation-equality premise, then applies `l.c.th`. Compiled body-reference records independently contain the corresponding field projections. This closes the local supplier gap left by v0.8, but moves the mathematical obligation upstream: where is `HeightCountingCharacterData` constructed, and how is its `th : EMtTheta ...` field proved?

This finding establishes neither circular reasoning nor a flaw. Reusing and transporting a previously proved property is ordinary mathematics. It also does not establish that the identity has substantive content at the headline proof's actual inputs. Neither the critics' allegation nor an end-to-end RH/Dirichlet-GRH verdict is settled by this phase.

## Evidence validation

- Uploaded archive: `stage3-evidence(8).zip`.
- SHA-256: `dbb49c17bb13c9f34cbaa9b0179473a4c9670f98f25f2db2cb4ee75e692a671d`.
- Server run: `/home/harry/rh-verification/critics-audit-stage3/stage3-_t9nmjuc`.
- Recorded interval: 04:24:12–04:26:30 EST, 23 November 2026.
- Theta inspection: elapsed 2:11.99, exit 0, maximum RSS 52,112,112 KiB. Positive and provenance fixtures passed; the negative fixture produced the expected type error.
- All 317 evidence-manifest entries and 94 package-manifest entries matched. Archived package contents matched the delivered v0.9 manifest.
- The 33 recorded input hashes were unchanged before and after execution.
- All 209 collected source-file hashes matched; 1,494,475 source bytes were collected, with no exclusions or caps reached in the requested source set. Equality to pinned git contents is recorded by the server runner, not independently checked against a newly fetched upstream repository here.
- Theta provenance, declaration-block index and provenance-fixture JSON were reproduced with the delivered local runner and matched the archived outputs.
- Ten targets were recorded without direct-reference-list truncation. Their printed axiom lists contain only `propext`, `Classical.choice`, and `Quot.sound`.

Source pin: `753431bfe28701f6f3937f664fcaf08daa139c03`.

Mathlib pin: `0df444a360eaa60ab8c11dca51a86af692955474`.

These are evidence-consistency checks, not a new independent kernel check. The printed declarations contain 1,056 `⋯` elision indicators, so they must not be treated as complete serialized proof terms. No Comparator completion is reported or inferred.

## Exact local route

Paths below refer to `collected-source/` in the evidence archive. `TPS/` abbreviates `Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/`; `IW/` abbreviates `Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/`.

| Location | Source observation | Interpretation |
| --- | --- | --- |
| `TPS/RowsAtStart.lean:95–118` | `nonempty_nMore_of_xdAll` constructs `RealExpansionExtraData`, with `th := T.emtTheta_of_yRel L l Y hY`. | A local record is constructed, but its theta field is supplied by another theorem. |
| `TPS/EmtThetaLStatement.lean:14–15` | The wrapper delegates to `Fin3.emtTheta_L_alt`. | Its direct compiled body references confirm this delegation. |
| `TPS/EmtThetaL.lean:17–22` | Introduces the identity's arguments and premises, uses `hY.eW`, and applies `l.c.th`. | The identity is transported from existing level data. |
| `TPS/SameGaloisLevelExists.lean:38–39` | `StrictHenselianAcyclicLevel` extends `ThirdIntermediateLevel` with `c : HeightCountingCharacterData mt b T.k T.psi`. | The theorem's level argument already contains the character-data record. |
| `TPS/RootsOfUnityRingLeWittIntegers.lean:63–75` | `HeightCountingCharacterData` includes `th : EMtTheta Y b.YS ch`. | This is the upstream proof obligation that must be traced to its constructor. |
| `TPS/SameGaloisLevelExists.lean:49` | `StrictHenselianAcyclicLevelNonempty` asserts the relevant character-data record is nonempty. | This names an existence obligation; its definition alone is not a proof of that obligation. |

The central source fragment is:

```lean
intro v i hv y hy n a f h
have h2 := HEq.trans (heq_of_eq h) (hY.eW i _)
exact (by with_unfolding_all exact
  ((l.c.th ((v)) ((i)) ((hv)) ((y)) ((hy)) n ((a)) ((f))
    (((eq_of_heq h2)))) : _))
```

The inequality premise `hv` and index-membership premise `hy` are forwarded to the stored identity. The representation-equality premise `h` is converted through the relation's `eW` component. This body does not explicitly discharge the conclusion by `True.intro` or contradiction. That source observation does not prove the premises are satisfiable at all relevant instantiations.

The compiled body-reference record for `emtTheta_L_alt` includes `Fin3.YRel.eW`, `HeightCountingCharacterData.th`, and `StrictHenselianAcyclicLevel.c`. Together with the source application, this supports the specific transport account. A reference list alone would not identify argument positions or prove semantic necessity.

## How the reading relation is supplied

The wrapper `T.normalisedReadings_related_localizedAdelicData` delegates to `Fin3.yRel_of_pin`; the compiled body-reference record confirms this delegation.

`IW/NormalisedReadingsRelatedLocalizedAdelicData.lean:18–39` constructs the relation's three components under its stated hypotheses. It obtains representation agreement through `CopyRead.repOf_heq`, substitutes the moved-data and reading equalities, and builds the `eW` and `jMt` agreements using the supplied coherence and pinning proofs.

Thus this local route constructs `YRel` from compatibility data, rather than simply taking the resulting `YRel` as a new assumption. It still requires those compatibility inputs. This phase has not traced every one of them back to its headline instantiation.

`YRel` itself, in `IW/TwistDataAgreeAcrossCoefficientsLocalized.lean:73–76`, contains representation, `eW`, and `jMt` heterogeneous equalities. Its text is not a definition returning `True`. Whether these equalities are automatic for the chosen inputs is a separate question.

The geometry field remains distinct: `thetaTie_yStructureLocal_nonempty` transports data from `l.b.geo`. A successful transport of that field cannot substitute for checking the origin of `l.c.th`, or conversely.

## What to investigate next

1. Locate the actual supplier of `StrictHenselianAcyclicLevelNonempty` and the constructor of `HeightCountingCharacterData` used on this route. Record the exact expression assigned to `th`, its hypotheses, and its compiled declaration owner.
2. Follow that theta supplier until reaching its mathematical argument, or an explicitly identified unresolved assumption. If it is another transport, name the original identity rather than calling the obligation discharged.
3. At that construction, inspect the actual place/index types, inequality premise and representation-equality premise. An empty domain or impossible premise must be demonstrated for the specific inputs, not inferred from names or census counts.
4. Connect this construction to the headline use with argument-level evidence. Reachability establishes presence; it does not establish indispensability. Any necessity experiment must retain a valid interface and classify failures before interpreting them.

The appropriate next target is therefore the constructor supplying the original theta identity, not another unrestricted closure traversal.

## Remaining scope and public wording

Daniel Fairbanks' broader requests remain separate: a second same-classifier control, every unknown with reason and budget, the larger-budget `LedPart.pt` probe, project/library and instance/generated stratification, and preregistered witness-use sampling. This targeted phase does not complete them.

Suggested public statement:

> Our latest audit traced the localized theta identity to an identity already stored in the input level data. We identified the exact field and the equality transport used to apply it. The next check is how that original identity is constructed and whether its conditions are substantive at the relevant inputs. This is a concrete refinement of the proof trace, not a verdict that the RH proof is correct or flawed.
