# Stage 3 v0.13: existence witnesses in the theta-realization route

Reviewed 23 November 2026. This report reviews Harry Tong's uploaded server evidence; it does not report a new local Lean run or a completed Comparator run.

## Result

The requested v0.13 realization phase completed successfully. The inspected conversion from a weak, zero-fallback construction to a theta property explicitly consumes an existence witness. The fallback construction alone does not establish that property.

The concrete caller supplies this witness through `x.m.intersectionNumber_baseChange.aux.ex`. The next substantive question is how the upstream `Moved` record is constructed and supplies that field on the route used by the headline proofs.

This is a local result about a particular conversion. It neither establishes that all degenerate constructions are harmless nor demonstrates a flaw in the RH/GRH proof.

## Evidence and validation

| Item | Recorded or checked result |
|---|---|
| Uploaded evidence SHA-256 | `e1e208fd2397101c1cf3c0e13995788ae36c3f1d2999d5398f91a3a8805a1487` |
| Source commit | `753431bfe28701f6f3937f664fcaf08daa139c03` |
| Mathlib commit | `0df444a360eaa60ab8c11dca51a86af692955474` |
| Method | `stage3-targeted-0.13`, phase `realization` |
| Evidence manifest | All 378 listed checksums match |
| Input hashes | Recorded before/after hashes agree |
| Protocol | Evidence copy matches the issued v0.13 protocol |
| Fixtures | Positive and provenance fixtures passed; negative fixture produced the expected type error |
| Project probe | Exit status 0; elapsed 2:02.48 |
| Peak process RSS | 52,120,308 KiB, approximately 49.7 GiB |
| Collection | 17 declaration blocks; 45 provenance records; no recorded constant-reference truncation |
| Source collection | 250 files verified against Git; 67 omitted at the file-count cap |
| Comparator | Not inspected or controlled by this phase |
| Independent kernel check | Not performed by this phase |

The server run began at 18:37:08 UTC and the realization step finished at 18:39:21 UTC on 23 November. The evidence records both `RH_STAGE3_REALIZATION_BOUNDARY_ACCEPTED` and `RH_STAGE3_REALIZATION_END`.

## 1. What the zero fallback actually promises

In `Formalism/LocalToGlobal/IndefiniteReal/LinksW.lean`, line 15, the definition is:

```lean
def OrZero {X : Type} [Zero X] (p : X → Prop) (x : X) : Prop :=
  ((∃ y, p y) → p x) ∧ ((¬ ∃ y, p y) → x = 0)
```

Thus `OrZero p x` provides two conditional guarantees. If a witness of `p` exists, `x` satisfies `p`. If no such witness exists, `x` is zero. The theorem `orZero_exists` constructs an object with this weak guarantee by separating those two cases. It does not establish `∃ y, p y`.

The two v0.13 boundary lemmas, `RHStage3Realization.valid_of_exists` and `RHStage3Realization.zero_of_no_witness`, compiled and each reported no axioms. These are conditional consequences of `OrZero`, not new proofs of the project's existence obligations.

## 2. The stronger theta property consumes existence

The same source defines `ExAt` with explicit existence fields, including `ioP`, `thF`, and `thG`. At lines 161–165, `thP_of_weak` uses these fields:

```lean
theorem thP_of_weak (h : R.IsThPW) (e : R.ExAt) : R.IsThP :=
  ⟨h.ωP, h.vP, h.pt_theta,
   fun i t => (h.ioP i).1 (e.ioP i) t,
   fun i t x => ((h.thF i t).1 (e.thF i t)).1 x,
   fun i t => ((h.thF i t).1 (e.thF i t)).2,
   fun i t => (h.thG i t).1 (e.thG i t)⟩
```

The critical operation is application of the first implication in `OrZero` to an existence proof. For example, `(h.thF i t).1 (e.thF i t)` obtains the actual `PThF` property.

`PThF` includes a theta operator satisfying `Lift.IsThetaP` and a compatibility equation. The collected definition of `IsThetaP` includes an integrability condition and equality to a theta integral. These are formal requirements beyond the fallback guarantee. Their mathematical adequacy remains a separate question.

Existence must not be confused with nonzeroness: these results do not, by themselves, prove the operators or measures are nonzero. A zero object could satisfy the relevant predicate in some context.

## 3. The concrete caller and the next upstream obligation

The source chain is:

| Location | Relevant operation |
|---|---|
| `LocalComponentAtPlaceDetermined.lean:179` | Calls `RealSide.ofPins` with `x.m.intersectionNumber_baseChange` |
| `OfFirstStepLoc.lean:17–25` | Supplies `h.aux.ex` to `RealDat3.characterisation_of_weak` |
| `ZeroPartEigenvalueConvention.lean:272–274` | Uses `RealDat.thP_of_weak` with the existence package |
| `LinksW.lean:161–165` | Applies the explicit existence fields to the weak guarantees |

The first two filenames are under `Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/` and `Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/`, respectively. The remaining two are under `Formalism/LocalToGlobal/IndefiniteReal/`.

Compiled constant-reference records confirm that `exists_local_map_at_place_alt` references both `RealSide.ofPins` and `GlobalTheory.Mem.R3.Rw.Moved.intersectionNumber_baseChange`. They also confirm references from `characterisation_of_weak` to `thP_of_weak`, and from the latter to the `ExAt` projections. Some proof components of `RealSide.ofPins` reside in generated `_proof_n` declarations; its top-level reference record alone is not a complete direct-edge account of those components. The intervening source call above is explicit.

In `Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/ReadPk.lean:162–175`, the `Moved` record contains both:

```lean
intersectionNumber_baseChange : Holds z.R z.F
exAt : z.R.toRealDat.ExAt
```

`Holds` contains `aux : UnusedChoiceStatements R F`, and that package contains `ex : R.toRealDat.ExAt`. Despite the name `UnusedChoiceStatements`, the inspected caller uses its `ex` field. The separately stored `Moved.exAt` is not the field passed by this particular call; the two must not be conflated.

The surrounding theorem is conditional on other inputs and quantifies over states through `AllSt`. Consequently, finding the existence package in a record type is not yet an audit of its construction, nor proof that the state domain is inhabited at the relevant final use.

## 4. Measure normalization: a separate conditional fact

`Development/AbelianVarietyTheory/Proofs/FoundationProofs/MeasureToRealEqMass.lean:163` states that, under `IsMeasLevDef V K μ`, the measure of `K.comap (finE V)` is 1. The collected definition of `IsMeasLevDef` includes Haar/probability-measure conditions in its underlying package.

Mathematically this normalization excludes the zero measure for that `μ` under that hypothesis. This review does not establish that it is the same measure as every `νV` used in a theta integral. Such an identification requires its own proof or explicit definition trace.

## Limits and next tests

The printed declarations contain 479 `⋯` indicators. Full constant-reference lists and collected source help identify dependencies, but they do not make an elided printed proof a complete proof-term inspection. Source collection is also bounded, as reported above.

The next targeted phase should:

1. Locate the constructor or supplier of the concrete `Moved` value, including the proof assigned to `intersectionNumber_baseChange`.
2. Follow its `aux.ex` construction into the individual `ExAt` obligations. Record the assumptions and witnesses used, rather than inferring their content from field names.
3. Trace the relevant `AllSt` instantiation to establish which state is used by the headline route, and distinguish hypothetical state properties from construction of an actual state.
4. Inspect the relevant generated `RealSide.ofPins._proof_n` bodies if a fully compiled direct-edge chain is claimed.
5. Connect any measure-normalization result to the actual theta measure before asserting nonzeroness there.

The separate Daniel Fairbanks follow-ups—additional controls, complete unknown accounting, preregistered use sampling, and project/instance/library stratification—remain separate deliverables. This targeted phase does not complete them.

The supported conclusion is that this particular weak-to-strong conversion retains an explicit existence obligation. It does not permit a bare zero fallback to stand in for that obligation. Whether the upstream construction supplies the intended mathematical content is the next question to resolve.
