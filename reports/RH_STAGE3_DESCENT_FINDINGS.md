# Stage 3 v0.11: theta identity and coefficient descent

Review date: 23 November 2026. This is a review of Harry Tong's uploaded run, compiled-declaration reference records and collected source snapshots. Lean was not rerun in the review environment.

## Finding

The three selected suppliers now have a concrete local explanation. The theta-lift wrapper refers to a proof that combines flat-vector normalization, an integral-to-sum identity and class-sum regrouping. The proportionality theorem proves separate zero and nonzero conclusions by comparing basis coefficients. The unit-existence wrapper refers to an algebraic proof using integrality and the assumption that the level integer is invertible.

One potentially misleading branch is now explained: the local-component construction chooses unit 1 when its complex scalar has no preimage in the coefficient field. In that branch, a nonzero right-hand vector would itself produce such a preimage, contradicting the branch assumption. Thus both vectors are zero for the admissible inputs in that branch. This is a conditional deduction, not evidence that the branch is actually selected at the headline inputs, or that all relevant spaces are zero.

This evidence identifies actual reasoning at the inspected application sites. It does not establish the nonvacuity of every upstream hypothesis, semantic necessity of this route, correctness of all mathematical definitions, or a new RH/GRH verdict. It also does not resolve the Nielsen/Chu criticisms globally.

## Evidence and validation

Evidence archive: `stage3-evidence(10).zip`.

SHA-256: `6529451a52fb9ce02ce165537494c985824ad93ca1c5f742c950a401ae1df762`.

Server run: `/home/harry/rh-verification/critics-audit-stage3/stage3-orgahr7_`.

Method: `stage3-targeted-0.11`, phase `descent`.

Source revision: `753431bfe28701f6f3937f664fcaf08daa139c03`.

Mathlib revision: `0df444a360eaa60ab8c11dca51a86af692955474`.

The recorded run began at 04:42:23 EST and finished at 04:45:04 EST on 23 November 2026. The project Lean command took 2:33.81 and exited 0. Its maximum reported RSS was 52,102,960 KiB, about 49.69 GiB.

Review checks completed:

- All 368 entries in the evidence checksum manifest matched the uploaded bytes.
- All 104 package manifest entries matched. The package manifest is identical to the delivered v0.11 manifest.
- The 33 recorded before/after input hashes are unchanged.
- Positive and provenance fixtures succeeded; the negative fixture produced the intended `True` versus `False` type error.
- The trusted local v0.11 parser reproduced `descent-provenance.json`, `descent-blocks.json` and `provenance-fixture-result.json` from the logs.
- All eight requested targets were recorded, with no reported direct-reference truncation.
- The eight printed axiom reports list only `propext`, `Classical.choice` and `Quot.sound` (including universe annotations where printed).
- All 250 collected source files matched their recorded hashes and sizes, totaling 2,212,438 bytes. The server runner records them as checked against pinned git contents. This review verified the supplied bytes and records; it did not independently fetch that repository revision.

Limitations: 49 source requests hit the file-count cap. The printed declaration log contains 452 `⋯` elisions. Stored constant-reference lists are not full argument-use traces, and collected source is bounded context, not a complete dependency closure. Source-level inspection of an underlying theorem is distinguished below from the direct compiled-reference records obtained for the selected targets.

Comparator was neither inspected nor controlled by this phase. This run performs no new independent-kernel check.

## 1. The theta-lift/class-sum supplier

Selected target:

`GlobalTheory.T.thetaLift_twistLevelForm_eq_unit_mul_classSum`

Its compiled proof-body reference list contains `GlobalTheory.LiftClassSumTwist.thF_eq_classSum`. The source wrapper in `ThetaLiftTwistLevelFormEqUnitMulClassSumStatement.lean`, line 17, delegates to that theorem.

The underlying source, `ThetaLiftTwistLevelFormEqUnitMulClassSum.lean`, makes the following construction in `thF_eq_classSum` (line 165 onward):

1. Assemble `GlobalTheory.Hk3.Core` from fields of the supplied `RealSide` record `X.char`.
2. Obtain a flat vector using `GlobalTheory.FlatVecExist.flatVec_existsUnique`, with `X.guard` among the inputs.
3. Use `GlobalTheory.T.flatVector_eq_unit_mul_centralTranslate_liftVector` to obtain a central translate and scalar `c0` satisfying `UnitOff` and the flat-vector identity.
4. Identify this flat vector with the principal-level flat vector and choose principal-level class representatives.
5. Return scalar `c0⁻¹`. Establish the identity through `thF_eq_princ`, `classSum_princ` and `classSum_weil`.

`thF_eq_princ` (line 107 onward) opens `hC.thP.thF j t` at line 141. It uses the resulting witnesses and identities, applies `GlobalTheory.LiftUnfold.integral_theta` at line 152, and finishes with `sum_eq_classSum`. `classSum_princ` (line 67 onward) invokes a finer-level coset regrouping theorem and the preceding vector-sum result. These are identifiable proof steps under supplied hypotheses.

The immediate flat-vector source was also collected. `GlobalTheory.FlatLift.flat_eq_unit_smul_om`, in `FlatVectorEqUnitMulCentralTranslateLiftVector.lean` at line 52, obtains a scalar with prescribed prime-ideal behavior, constructs a central element, and calls:

- `GlobalTheory.T.weilRep_central_acts_by_dilation_unit`;
- `GlobalTheory.T.lift_vector_eq_unit_mul_dilated_flat_datum`.

It finishes by composing inverse dilations and cancelling a nonzero scalar product. This description is source inspection of an underlying implementation; v0.11 did not separately print all of these deeper declarations from the compiled environment.

The remaining boundary is explicit: how the relevant `RealSide`/`Hk3.Core` fields, guards and theta-realization properties are supplied at the actual application, and what the integral and dilation suppliers require. A field supplying a proposition is not an extra axiom, but its availability and intended meaning still need to be tracked. Complexity or length of the source does not settle that question.

## 2. Proportionality descends only in the nonzero case

Selected target:

`GlobalTheory.T.chosenField_forms_proportional_of_readings`

Source: `ChosenFieldFormsProportionalOfReadings.lean`, line 77. Its compiled references include the two private lemmas defined in that same file: `tensor_exists_basis_expansion` and `tensor_scalar_relation`.

Suppressing the surrounding parameters, the conclusion has the form

```text
R A = z • R B
  → (B = 0 → A = 0)
    ∧ (B ≠ 0 → ∃ t, ε t = z ∧ A = t • B).
```

This requires a faithful reading and compatible embedding, along with the surrounding setup assumptions. The private proof at lines 42–75 proceeds by finite basis expansions. For the nonzero case it finds a nonzero coefficient β[a0] of B, sets t = α[a0] / β[a0], and uses linear independence and injectivity of ε to establish both conclusions. For the zero case it proves all coefficients of A vanish.

The theorem does not assert B ≠ 0. It does not assert that every complex scalar belongs to the coefficient field. The existence of a preimage for z is conditional on the right-hand vector being nonzero.

## 3. The unit predicate has explicit content

Selected target:

`GlobalTheory.T.exists_integral_unit_of_isUnitAwayFromLevel_embedding`

The compiled wrapper references `GlobalTheory.PlaceRead.unit_of_unitOff`. The implementation is in `ExistsIntegralUnitOfIsUnitAwayFromLevelEmbedding.lean`, line 16 onward.

`GlobalTheory.ConjTwist.UnitOff`, defined in `ConjTupRefl.lean` at line 21, is:

```lean
u ≠ 0 ∧ ∃ n : ℕ,
  IsIntegral ℤ ((N : ℂ) ^ n * u) ∧
  IsIntegral ℤ ((N : ℂ) ^ n * u⁻¹)
```

For an integrally closed domain O, an embedding ε from its fraction field into ℂ, and `IsUnit (N : O)`, the supplier proves that t comes from a unit of O when `UnitOff N (ε t)` holds.

The proof pulls integrality back through the injective embedding, uses integral closure to obtain elements a and b of O representing Nⁿt and Nⁿt⁻¹, and proves a*b = N^(2*n). Since N is a unit, a is a unit. It then constructs the required unit by multiplying a by the appropriate power of N⁻¹.

Consequently this inspected unit supplier is not obtaining an arbitrary unit from an unrestricted scalar. It has explicit hypotheses and uses them in algebraic reasoning. However, a nonzero scalar does not prove that the vector it multiplies, the class sum, or a domain of quantification is nonzero or inhabited.

## 4. Why the caller sometimes chooses unit 1

Source: `ThirdPlaceSeries/LocalComponentAtPlaceDetermined.lean`, lines 147–161.

The caller has a complex identity for each admissible input and obtains the proportionality result above. It then splits on

```text
∃ t : KE c w, ε t = z₁.
```

If a preimage exists, the unit supplier produces a unit from t. For a nonzero B, the scalar supplied by proportionality equals this t by injectivity of ε. For a zero B, A is also zero, so the same scalar identity holds.

If no preimage exists, the caller chooses unit 1. For any admissible input, assuming B ≠ 0 would let the proportionality theorem construct a preimage of z₁, contradicting the branch assumption. Thus B = 0 and A = 0, and the identity with scalar 1 follows.

This explains a concrete use of the zero case. It does not determine which branch is used by the final RH/GRH construction. In particular, it would be incorrect to infer from this branch alone either that the main proof collapses to zero objects or that all degeneracy concerns have been eliminated.

## What this changes, and what remains open

The inspected normalization and descent steps are now supported by exact caller locations, stored wrapper references and implementation source. The strongest new conclusion is local: the apparent fallback to unit 1 is justified by a zero/nonzero dichotomy whose nonzero branch would contradict failure of coefficient descent.

The next focused inspection should prioritize `GlobalTheory.LiftUnfold.integral_theta` and the source of the `hC.thP.thF` witness, alongside the flat-vector dilation suppliers. It should record their stored types and implementations and connect their hypotheses to the actual caller arguments. Repeatedly listing wrappers without making that connection would not answer the semantic question.

This phase also leaves Daniel Fairbanks' broader requests open: a second control through the same classifier; complete accounting of all unknowns and budgets; the larger-budget `LedPart.pt` probe; project/library and instance/generated stratification; and a preregistered sample of witness uses. The targeted investigations do not substitute for those tasks.

## Source locator guide

Paths below are relative to `collected-source/` inside the evidence ZIP. Let `IE/` mean `Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/` and `TPS/` mean `Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/`.

| File | Relevant location |
| --- | --- |
| `IE/ThetaLiftTwistLevelFormEqUnitMulClassSumStatement.lean` | Wrapper, line 17 |
| `IE/ThetaLiftTwistLevelFormEqUnitMulClassSum.lean` | Regrouping at 67; integral step at 107–163; main supplier at 165–185 |
| `IE/ChosenFieldFormsProportionalOfReadings.lean` | Basis expansion at 15; scalar relation at 42; selected theorem at 77 |
| `IE/ExistsIntegralUnitOfIsUnitAwayFromLevelEmbeddingStatement.lean` | Wrapper, line 17 |
| `IE/ExistsIntegralUnitOfIsUnitAwayFromLevelEmbedding.lean` | Unit construction, line 16 onward |
| `IE/FlatVectorEqUnitMulCentralTranslateLiftVector.lean` | Conditional normalization, line 52 onward |
| `Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/ConjTupRefl.lean` | `UnitOff` at 21; `IsFlatVec` at 39 |
| `TPS/LocalComponentAtPlaceDetermined.lean` | Theta supplier call at 72; proportionality/unit branches at 147–161 |

All findings above are bounded to the supplied evidence and the stated local proof steps. No new Comparator result, global nonvacuity result, or RH/GRH verdict is asserted.
