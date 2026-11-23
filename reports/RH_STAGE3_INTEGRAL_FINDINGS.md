# Stage 3 v0.12: theta-integral and class-sum audit

Reviewed 23 November 2026. This report reviews Harry Tong's uploaded evidence from the `integral` phase. It records a successful targeted inspection, not a new independent kernel replay, Comparator result, or RH/GRH verdict.

## Finding

The inspected route connects the theta-lift expression to a genuine integral and then to a finite class sum, under explicit hypotheses. The caller supplies those hypotheses through `RealSide.char`, including `Char3.thP` and `Char3.models`. The remaining question is how the actual upstream construction supplies these fields, and what mathematical content survives in that construction.

In particular, the source definition of `Lift.IsThetaP` requires both integrability and agreement with the integral. This local interface does not consist solely of an unconstrained function named “theta.” However, inspecting an interface and its consumer does not establish that its hypotheses are satisfied non-vacuously in the headline application.

## Evidence and validation

Server run: `/home/harry/rh-verification/critics-audit-stage3/stage3-rc_u_uty`.

Evidence archive SHA-256:

```text
93cba55fe65cdde9f6f7028286f8f1eeedce82d47d2d9ad0a7555fb880ef20b4
```

Pinned project commit: `753431bfe28701f6f3937f664fcaf08daa139c03`.

Pinned Mathlib commit: `0df444a360eaa60ab8c11dca51a86af692955474`.

The review verified all 373 evidence-manifest entries and all 109 package-manifest entries. The 109 package files match the previously delivered v0.12 package. All 33 recorded before/after input hashes agree. All 250 collected source-file hashes match their index. These are integrity checks on the supplied evidence; they are not an independent reproduction of the server's Lean execution or of its Git provenance checks.

The positive fixture, provenance fixture, and integral inspection exited successfully. The negative fixture produced the expected type error. The integral subprocess took 2 minutes 21.67 seconds and reported maximum RSS of 52,090,000 KiB (about 49.68 GiB), with no swaps.

Re-running the original runner's parsers on the uploaded logs reproduced `integral-provenance.json`, `integral-blocks.json`, and `provenance-fixture-result.json` exactly. All 11 requested declarations were present. Each printed axiom list contains only `propext`, `Classical.choice`, and `Quot.sound`, with universe annotations where printed.

The direct-reference lists were not truncated. The pretty-printed declaration blocks contain 546 `⋯` elisions, so they are not complete raw proof-term exports. Two targets are inductive/structure declarations without a value body, as expected.

## What was traced

All source paths below are relative to `src/` at the pinned project commit. Copies are in the archive's `collected-source/` directory. The distinction between compiled-target inspection and additional source reading matters.

### 1. The integral-to-class-sum theorem

Compiled target: `GlobalTheory.LiftUnfold.integral_theta`.

Owner: `Development/AbelianVarietyTheory/Proofs/DivisorProofs/OscillatorModelValuesFourth.lean`.

The theorem relates a `MeasureTheory` integral of the theta integrand over a fundamental domain to a finite weighted sum. Its inputs include a Weil datum, coefficient/form conditions, theta-function and equivariance conditions, measure/fundamental-domain conditions, class representatives, and a nonzero subgroup index.

The proof invokes `GlobalTheory.ClsInt.integral_eq_classSum_of_le` and supplies the invariance conditions. It then identifies the resulting finite sum with the required expression. This is a conditional derivation involving integral unfolding and group actions, rather than an equality established solely by reflexivity.

Additional source reading: `Development/AbelianVarietyTheory/Proofs/DivisorProofs/IntegralEqClassSumOfLe.lean`. This helper was not separately included among the 11 compiled targets. Its general argument uses a left-invariant measure, a fundamental domain, an open subgroup with measure one, representatives, and invariance of the integrand. Its specialized proof obtains the measure-one fact from `GlobalTheory.Mass.Levels.measure_comap_finE hν.1`.

That normalization rules out the zero measure for an instance satisfying these hypotheses. It does not establish that the integrand or its integral is nonzero, and this run did not separately compile a zero-measure exclusion lemma.

### 2. Where the caller obtains its hypotheses

Compiled targets: `GlobalTheory.LiftClassSumTwist.thF_eq_princ` and `GlobalTheory.LiftClassSumTwist.thF_eq_classSum`.

Owner: `Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/ThetaLiftTwistLevelFormEqUnitMulClassSum.lean`.

At `thF_eq_princ`, the source constructs:

```lean
have hC : GlobalTheory.Hk3.Core X.R.toRealDat X.F.lv2 :=
  ⟨X.char.lev, X.char.grp, X.char.fam,
   X.char.models, X.char.chain, X.char.thP⟩
```

The subsequent call to `integral_theta` uses `hC.thP.ωP`, `hC.thP.pt_theta`, `hC.thP.ioP`, and `hC.models.νV`, among other inputs. The identification of the stored lift `thF` with its integral uses `hC.thP.thF`.

The inspected compiled references support this local dependency trace. They do not by themselves establish semantic necessity, nor trace the full construction of the particular `X` used upstream.

The corresponding compiled record/projection targets were `GlobalTheory.Hk3.Core`, `GlobalTheory.Hk3.Core.thP`, `GlobalTheory.TwInputs.RealSide.char`, and `Formalism.IndefR.Links.RealDat3.Char3`. A record projection supplies a field already present in its input; it is not a separate existence proof of that input.

### 3. What the theta field actually requires

Additional source reading: `Formalism/LocalToGlobal/IndefiniteReal/LinksChar.lean`, especially lines 305–338.

`RealDat.IsThP` contains seven fields: `ωP`, `vP`, `pt_theta`, `ioP`, `thF_mem`, `thF`, and `thG`. Its `thF` obligation requires existence of a linear theta operator satisfying `Lift.IsThetaP`, together with agreement between that operator and the stored `R.thF` on specified inputs.

Additional source reading: `Formalism/LocalToGlobal/IndefiniteReal/OrthogonalComplementCharacterisation.lean`, lines 164–174. Here `thetaPInt` is defined by an integral, and `IsThetaP` requires:

- `integ`: integrability of the theta integrand on the domain for each specified input;
- `eq`: agreement of the supplied theta operator with that integral.

Thus this interface explicitly includes integrability; the audit must not treat it as merely a use of the integral notation without an integrability obligation. Conversely, these are still obligations supplied by the input record. The run has not yet traced their construction all the way back to the headline witness.

`LinksChar.lean` also defines `models_νV` through `IsMeasDef`. In `LinksDefs.lean:235`, `IsMeasDef` combines `IsMeasLevDef` with a fundamental-domain condition.

### 4. The flat-vector and scalar steps

Compiled target: `GlobalTheory.FlatVecExist.flatVec_existsUnique`, in `Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/FlatVecExistsUnique.lean`.

The inspected source uses `hR.thP.vP` and theta/place-model existence and uniqueness machinery. Its `QGuard R` argument is introduced as `_` at line 91 and is not used in that source proof. This is a local observation about this theorem, not a claim that `QGuard` is unused in the whole route. Other inspected helpers explicitly pass it onward.

Existence and uniqueness of a flat vector do not, by themselves, assert that it is nonzero. This run does not establish nonvanishing of the vector or the resulting class sum in the headline application.

The compiled target `GlobalTheory.FlatLift.flat_eq_unit_smul_om` and the two compiled statement wrappers lead to further explicit helpers:

- `GlobalTheory.T.weilRep_central_acts_by_dilation_unit` leads to `GlobalTheory.TupDil.om_model_eq_unit_smul_dilate`. Its source passes `hC` and `hQG` to `central_uniformiser_acts_by_dilation_tame_kernel`, along with tuple-kernel data and arithmetic conditions.
- `GlobalTheory.T.lift_vector_eq_unit_mul_dilated_flat_datum` leads to `GlobalTheory.LiftFlatModel.lift_eq_model_flat`. Its source uses `exists_reps_pairing`, a residue-twist/Fourier identity, and explicit nonzero/uniformizer conditions to obtain the unit scalar.

The implementation files are respectively `WeilRepCentralActsByDilationUnit.lean` and `LiftVectorEqUnitMulDilatedFlatDatum.lean` in the same `Proofs/InertiaEigenvalues/` directory. Their reading extends the source trace; their full implementations were not additional compiled targets in v0.12.

## Coverage limits and implications for the criticism

The source collector reached its configured 250-file cap. The index records another 208 requests as `file-count-cap`. It was configured for prioritized source references with import depth two. This is bounded context, not a complete source closure. An uncollected declaration cannot be treated as absent or unused.

This result does not refute Nielsen's claim that a route uses `geoCl anyGeometry`. It also does not establish the stronger claim that every alternative proof route is impossible, or that the formal headline theorem is invalid. These remain distinct questions: a declaration is referenced; its content is indispensable in a particular argument; the accepted theorem fails to establish the intended mathematical statement.

Internal use of a `True` predicate is not by itself a formal counterexample. If a sound checker accepts a closed proof of the intended statement under the permitted axioms, such an internal definition cannot independently invalidate that proof. A contrary finding must identify an actual issue with the statement and its definitions, assumptions, or checking/trust boundary. Mathematical explanation and non-vacuity checks remain valuable, but are not interchangeable with that verdict.

## Next targeted work

1. Trace the construction supplying `RealSide.char`, particularly `Char3.thP` and `Char3.models`, in the actual upstream application. Preserve concrete arguments and distinguish construction from projection.
2. Inspect `RealDat.thP_of_weak` and the `ExAt` witness used by `RealDat3.characterisation_of_weak` (`ZeroPartEigenvalueConvention.lean:272–274`). Determine first whether this constructor is the one used on our traced route; do not assume it from its availability.
3. Follow the providers of `IsThetaP.integ`, `IsThetaP.eq`, and the measure normalization. Record any remaining hypotheses and whether relevant index/input domains can be empty. A conditional theorem alone does not resolve that question.
4. Where a later step requires nonvanishing, identify that exact requirement and its supplied proof. Do not impose nonvanishing on every intermediate identity, since valid identities may hold at zero.

These tasks narrow the substantive obligation in the current route. They do not complete Daniel Fairbanks' separate census follow-ups: exhaustive unknown accounting, additional controls, project/library and instance stratification, and preregistered witness-use sampling remain distinct work items unless separately completed and evidenced.

The uploaded run reports no new independent kernel check. It did not inspect or control the running Comparator. No Comparator completion or duration estimate follows from this evidence.
