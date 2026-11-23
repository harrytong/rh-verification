# Stage 3 initial evidence review

Reviewed 23 November 2026. Scope: the uploaded `stage3-evidence.zip` from the `inspect` phase of stage3-targeted-0.1. This is a review of Harry Tong's recorded run and supplied sources, not an independent rerun of Lean.

**Conclusion:** the targeted probes completed successfully and clarify two local constructions. They do not establish that the disputed objects are dispensable, that the critics' objections are correct, or that RH/GRH has been independently verified by this stage.

## Integrity and execution

- Evidence SHA-256: `8a0f1688bf7ba187223a69c6dd3743df3ed7faf0442d38ce45b78afbc97b5509`, matching the terminal report. All entries in `EVIDENCE_SHA256SUMS` were verified.
- Run: `stage3-e04wut0m`, 23 November 2026, approximately 02:05:27–02:08:10 EST.
- Project revision: `753431bfe28701f6f3937f664fcaf08daa139c03`; Mathlib revision: `0df444a360eaa60ab8c11dca51a86af692955474`.
- Recorded before/after hashes agree for the selected source files, Lean executable, `Main.olean`, and `Statements.olean`. This is a check of the recorded selection, not a hash of the whole environment.
- Positive fixture succeeded. Negative fixture produced the expected type error. Geometry and height probes exited with status 0.
- Comparator was not inspected or controlled. This package supplies no new Comparator result or independent kernel verdict.

## 1. Geometry: distinguish the predicate from the compatibility package

The printed definition confirms `anyGeometry := fun _ _ _ => True`. The instrumented geometry theorem still uses `geoCl anyGeometry`; its successful compilation is not a replacement, abstraction, or dependency-elimination result.

The evidence distinguishes two fields with similar names:

1. `OAt Γ.geo` asks for the predicate Γ at the relevant inputs. `OAt` also contains a separate `lam` field.
2. `OpenParameterStatements.geo` has type `LinkedAt p GeometricWeakCompatibility'`. It is one of twelve fields in a larger hypothesis package.

The printed body of `GeometricWeakCompatibility'` contains an existential comparison witness together with `IotaPointSummands`, `ClassSumPin`, `CompatibilityConditions`, and `More`. This syntax alone does not establish that those nested conditions have substantive mathematical content; their definitions and suppliers still require investigation.

There is nevertheless a concrete local use to follow. In `linked_bundles_l3_of_open_alt`, the supplied source combines `o.geo` with other package fields, obtains `hgeo`, chooses a witness `τ` and its properties `hτ`, and passes selected properties into `evW_pRows_of_rows_alt`. The resulting `hrows` is passed to `eventual_L3_of_covolume_alt` together with the separate covolume-bound premise `hCov`.

This identifies a local chain of uses beyond mere membership in a large dependency closure. It does **not** prove logical necessity of `anyGeometry`, nontriviality of the compatibility conditions, or correctness of their connection to the intended geometry.

Evidence locations: `geometry.log` lines 414–467 (final local context), 2657–2664 (`anyGeometry` and `geoCl`), 10234 onward (`linked_bundles_l3_of_open_alt`), and 11764–11835 (the package and compatibility definition). Source: `sources/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/LinkedBundlesL3OfOpen.lean`, lines 30–46.

## 2. Height: two equations about a constructed object

The first new theorem proves, in abbreviated notation,

```lean
p.pt.D.div.h u = p.ht u
```

Its elaborated proof is `Eq.refl`. This confirms that the constructed object's height is definitionally the assigned function.

The second new theorem proves

```lean
p.pt.D.div.h u = DV.hExpl6 p.pt.D p.pt.L p.pt.xa.X C.Csz u
```

Its elaborated proof projects `ExtraAt.h_eq` from `p.pt.xa`. It checks an existing contract of the constructed record. It does not independently establish agreement with an original, externally specified mathematical height.

Both new theorems report only `propext`, `Classical.choice`, and `Quot.sound` as axioms. Neither theorem asserts that the original `D.div.h` is preserved. Establishing whether preservation is required, and whether the downstream proof supplies the necessary connection, remains open.

Evidence locations: `height.log` lines 493–599 (`LedPart.ht` and `LedPart.pt`), 751–788 (assigned-height theorem), and 789–839 (constructed-height contract).

## 3. Limits of the current collection

The geometry log contains 275 occurrences of the rendering elision `⋯`; the height log contains two. The key height equations and their proof forms are visible, but the complete printed terms cannot be treated as lossless dumps. Some generated proof constants referenced by `LedPart.pt` are not expanded either.

This run did not perform the broader census follow-ups: two controls through the same classifier, project/library and instance/non-instance strata, preregistered use samples, complete unknown logging, or a larger-budget classifier retry for `LedPart.pt`. The successful height equations do not resolve its earlier classifier timeout.

## 4. Next targeted questions

1. **Trace the compatibility supplier.** Inspect `open0_of_unitary_group_hypotheses` and `geometric_condition_large_grid_alt`, including the exact premises from which their relevant package fields are built. Unfold the nested compatibility predicates only as needed to identify the mathematical obligations actually discharged.
2. **Trace the height consumer.** Find the first downstream estimate that uses the assigned height and identify any theorem connecting that estimate to the quantity required by the headline statement. Expand relevant generated proof constants and omitted arguments at that boundary.
3. **Keep necessity tests local and explicit.** Any abstraction or replacement experiment must identify which premise is changed, preserve the first error, and distinguish an interface mismatch from a missing mathematical premise. A failed edit alone is not evidence of a flawed proof.
4. **Complete Daniel Fairbanks' comparative requests separately.** Freeze sampling and classification rules before inspecting outcomes, report identical denominators and generated-declaration policies across cohorts, and retain every unknown with its reason and budget.

The most useful next result would be an explicit, checked connection at one of these boundaries, or a precisely isolated mismatch. Additional successful compilation of the unchanged route would not by itself settle that question.
