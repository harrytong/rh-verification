# Stage 3 v0.8: the extension constructor and its theta-proof supplier

Review date: 23 November 2026. This report reviews Harry Tong's uploaded logs and pinned source snapshots. Lean was not rerun in the review environment.

## Main finding

The collected source now identifies an explicit construction of `GlobalTheory.HeightCounting.RealExpansionExtraData`. In `ThirdPlaceSeries/RowsAtStart.lean`, the theorem `GlobalTheory.HeightCounting.Fin3.nonempty_nMore_of_xdAll` constructs the record and assigns:

```lean
geo := GlobalTheory.HeightCounting.Fin3.thetaTie_yStructureLocal_nonempty L l
th := GlobalTheory.T.emtTheta_of_yRel L l Y hY
```

This advances the investigation beyond merely locating a record field or transporting an existing record. The local `.th` proof is supplied by a named theorem, with the level data `l`, reading `Y`, and relation proof `hY` as inputs.

The named theorem delegates to `GlobalTheory.HeightCounting.Fin3.emtTheta_L_alt`. Its implementation is not included in this snapshot. We therefore have not established whether its proof is substantive or vacuous at the relevant inputs. No new RH/Dirichlet-GRH verdict or resolution of the critics' objections follows from this collection.

## Run and evidence validation

Evidence archive: `stage3-evidence(7).zip`.

SHA-256: `d2c2e5b5b612cd06cb0dbea5c5ecacfbbadfd4439c94bcfc3909a1517722c309`.

Server run directory: `/home/harry/rh-verification/critics-audit-stage3/stage3-3n_wvfdf`.

The recorded run completed from 04:15:04 to 04:16:56 EST on 23 November 2026. The construction inspection itself took 1:42.06, exited with status 0, and reported maximum RSS 52,106,476 KiB. Positive and provenance fixtures passed; the negative fixture produced the expected type error.

Review checks:

- All 354 evidence-manifest entries and 89 package-manifest entries match their hashes. Package files match the previously delivered v0.8 manifest.
- All 250 collected source-file hashes match. Their equality to pinned git contents is recorded by the server runner; the upstream repository was not fetched independently during this review.
- The 33 recorded input hashes are unchanged before and after the run.
- The construction provenance, printed-block index, lexical source index, and provenance-fixture result were regenerated with the delivered runner and matched the archived JSON outputs.
- Eight target declarations and 16 direct-reference lists were recorded without reference-list truncation. All eight printed axiom lists contain only `propext`, `Classical.choice`, and `Quot.sound`.

Recorded source pin: `753431bfe28701f6f3937f664fcaf08daa139c03`.

Recorded Mathlib pin: `0df444a360eaa60ab8c11dca51a86af692955474`.

These checks establish internal consistency of the supplied evidence. They are not an independent rerun of the project or a new kernel check. Comparator was neither inspected nor controlled.

## The source route now visible

All file references below are relative to `collected-source/` in the evidence ZIP. `TPS/` abbreviates `Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/`. Except where explicitly identified as compiled-reference evidence, the connections below come from reading the collected source; this run did not extract all of these nested applications from compiled proof terms.

| Step | Evidence location | What it supplies |
| --- | --- | --- |
| Finiteness entry point | `TPS/FinitenessOfHyp.lean:102–103` | `T.sFin_and_sFinl_of_archCmp_sEta_thetaData` delegates to `Fin3.sFin_and_sFinl_of_theta_data_exists`. Its sole direct compiled body reference confirms that delegation. |
| Finiteness branches | Same file, lines 85–95 | Both branches invoke `Fin3.lv3_of_third_alt_alt`, with `extensionWithLaw` or `extensionWithList`. |
| Level construction | Same file, lines 70–83 | Obtains localized data, a reading `Y₁` and `hY₁`, then calls `Fin3.exists_core_and_listPin`. |
| Extension witness | `TPS/RowsAtStart.lean:128–138` | Calls `Fin3.nonempty_nMore_of_xdAll` and packages its result `mo` with the law witness. |
| Record constructor | Same file, lines 95–118 | Constructs `RealExpansionExtraData`, including the explicit `.geo` and `.th` assignments quoted above. |
| Theta-proof wrapper | `TPS/EmtThetaLStatement.lean:14–15` | `T.emtTheta_of_yRel` proves the specified `EMtTheta` proposition by delegating to `Fin3.emtTheta_L_alt`. |

The conditional inputs must be retained when interpreting this route. The finiteness theorem takes published-input, comparison, eta, and theta-data hypotheses. Its source body shows how those hypotheses are passed through the construction; it does not by itself establish how every hypothesis is discharged from a headline root.

## What the new constructor tells us

`nonempty_nMore_of_xdAll` returns an actual record expression under its stated context and hypotheses. It is not merely a theorem accepting that entire record as an extra argument and passing it onward.

Nevertheless, a field supplied by a theorem can still inherit vacuity or trivial data from its inputs. The next question is about the proof of `emtTheta_L_alt` and the instantiated data, not whether the field has been syntactically filled.

The source also separates the two fields:

- `.geo` is supplied by `thetaTie_yStructureLocal_nonempty`. In `TPS/LocalMultiplicityFamily.lean:56–60`, this theorem obtains `g` from `l.b.geo` and reconstructs a theta-tie witness using its fields. It transports existing geometry data; it does not establish those data independently.
- `.th` is supplied by `emtTheta_of_yRel`. Its displayed type is `YRel L Y → EMtTheta Y (yStructureLocal L l) (characterChoiceLocal L l)` with the other parameters quantified.

Neither assignment is locally written as `True.intro`. That narrow source observation must not be expanded into a claim that all underlying predicates are nontrivial or that `anyGeometry` is harmless throughout the proof.

## The relation and data supplied to the theta theorem

`Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/TwistDataAgreeAcrossCoefficientsLocalized.lean:73–76` defines `YRel` as a proposition with three fields:

1. `rep`: heterogeneous equality of the representations associated with `Y` and the existing reading `x.r.Y`.
2. `eW`: pointwise heterogeneous equality of the corresponding `eW` expressions.
3. `jMt`: pointwise heterogeneous equality of the specified `jMt` expressions.

This identifies the relation's formal content. It is not a literal `True` definition. It may still be easy or automatic for the chosen readings; that is not decided by these fields alone.

`TPS/FinitenessOfHyp.lean:55–60` obtains the reading relation via `GlobalTheory.T.normalisedReadings_related_localizedAdelicData`. Lines 77–78 then pass the resulting `hY₁` into the extension construction. Thus the source supplies a named producer for `hY`, rather than leaving it as an unexplained free assumption at this particular call site. The producer's implementation remains to be reviewed.

`TPS/LocalMultiplicityFamily.lean:21–28` constructs `yStructureLocal` by carrying fields from `l.b.YS`. Line 48 defines `characterChoiceLocal` through `chL L l.c.ch`. These provide concrete next inputs to inspect for the theta identity.

## Transport and similarly named files

`TPS/ExistsSeed.lean:21–25` confirms that `sFino_of_alt` receives a witness from `FinitenessListStatement`, retains `v.nx.2`, and adds origin information. It is a transport step, rather than the initial `.th` constructor.

There is also a separate collected file named `FinitenessOfHyp.lean` under `Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/`. Its `moreD` theorem constructs `NMore` with `th := GlobalTheory.T.motive_theta_of_read_relation L l Y hY` at line 158. That is a distinct declaration and route. The basename alone does not make it the constructor traced through the TPS entry point above.

## Limits and next targets

The inspection log contains 277 `⋯` indicators. Printed bodies are not complete raw proof terms. Source collection retained 250 files totaling 1,480,419 bytes, with seven requested paths excluded by the file-count cap. The lexical index contains 14 matching lines; these are navigation aids, not witness-use classifications.

`TPS/EmtThetaLStatement.lean` imports `TPS/EmtThetaL.lean`. The latter is not in this archive: the statement file was reached at the collection depth boundary, so its imports were not expanded. It is not one of the seven explicitly file-capped paths. The next focused collection should prioritize it and the owner of `normalisedReadings_related_localizedAdelicData`.

The next review should:

1. Inspect `Fin3.emtTheta_L_alt`, its direct proof suppliers, and its axiom dependencies.
2. Inspect how `normalisedReadings_related_localizedAdelicData` constructs `YRel` for the reading used here.
3. Follow the theta identity back into `l.b.YS`, `l.c.ch`, and the relevant stage fields; check the place inequality, index/membership conditions and representation-equality antecedent at these inputs.
4. Extract the relevant compiled constructor/application evidence where feasible, keeping it distinct from source-level tracing and semantic necessity.

Daniel Fairbanks' broader census tasks remain outstanding: a second control through the same classifier, full unknown-reason accounting, the larger-budget `LedPart.pt` probe, project/library and instance/generated strata, and preregistered witness-use sampling. This targeted construction result does not complete those tasks.

**Conclusion:** v0.8 locates an explicit extension-record constructor and identifies the named theorem supplying its `.th` field. The substantive content of that theorem at the actual inputs, and its significance for the headline proof, remain open.
