# Stage 3 v0.7: extension-record provenance

Review date: 23 November 2026. This report reviews Harry Tong's uploaded run evidence and collected source. Lean was not rerun in the review environment.

## Finding

The `.th` field consumed on the previously traced class-sum route has type `GlobalTheory.HeightCounting.EMtTheta`. Its collected definition is a universally quantified conditional equality involving theta expressions and tensor sums. It is not written as `True`.

This identifies a concrete obligation to investigate. It does **not** establish that the obligation is nonvacuous at the actual inputs, that it is necessary for a headline proof, or that the final theorem matches the intended mathematical statement. The construction of the particular `.th` proof remains unresolved. These results neither invalidate the RH/Dirichlet-GRH proof nor settle the critics' objections.

## Evidence and validation

Evidence archive: `stage3-evidence(6).zip`.

SHA-256: `a5505fc8e26a31148f41d191f5ea51297ef9b6370eaa6e8db2cf98e0bceb5ea6`.

Server run: `/home/harry/rh-verification/critics-audit-stage3/stage3-xxrhc455`, phase `extensions`, method `stage3-targeted-0.7`.

The recorded run lasted from 03:49:33 to 03:52:12 EST on 23 November. The main Lean inspection took 2:27.12 and exited with status 0. The positive, provenance, and search fixtures completed; the negative fixture produced the expected `True` versus `False` type error.

Local review verified all 302 evidence-manifest entries, all 84 package-manifest entries, and the hashes of all 200 collected source files. The recorded before/after hashes for 33 pinned inputs are identical. Five derived JSON outputs were reproduced from the logs with the delivered runner and matched their archived counterparts. This checks evidence consistency, not an independent rerun of the Lean checks or authentication of the upstream repository.

Recorded source commit: `753431bfe28701f6f3937f664fcaf08daa139c03`.

Recorded Mathlib commit: `0df444a360eaa60ab8c11dca51a86af692955474`.

The recorded audit executable is from Lean v4.33.1; the separately running Comparator used the previously reported v4.36.0 judging toolchain. These are distinct operations.

## What the source shows

Paths below are relative to `collected-source/` in the evidence archive. `TPS/` abbreviates `Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/`.

### 1. The theta obligation

`Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/SubsetTwistExceptionalPlaces.lean:136–143` defines `EMtTheta`.

Its structure is: for every place `w` and index `i`, assuming `muAt w ≠ mu0`, for an `x` belonging to the specified index set, and for coefficients and forms satisfying a representation equality, a `thPe` expression equals a finite tensor sum.

There are several possible sources of vacuity or simplification that this definition alone does not resolve: the place inequality, existence of indices, membership of `x`, satisfiability of the representation equality, and the instantiated maps and spaces. A mathematically elaborate printed formula is not evidence that these conditions have substantive content at the inputs used by the proof.

`TPS/RootsOfUnityRingLeWittIntegers.lean:76–97` places this obligation in `RealExpansionExtraData.th`, separately from its `.geo` field, and uses that record for `defaultExtension`.

The prior provider report traced source code obtaining an extension witness and passing `m.1.th` onward. v0.7 identifies the definition of that field's type; it does not yet recover the complete construction of the field's proof.

### 2. The existence supplier is a conditional chain

`TPS/Has3NeoOfSteps.lean:30–35` obtains successive stage witnesses, obtains `sc`, applies the supplied finiteness statement to a structure containing the stage and `sc`, and returns the resulting `v`. In particular:

```lean
obtain ⟨sc⟩ := c P x4 l2
obtain ⟨Z, v, -, -⟩ := fin P x4
  { toStrictHenselianAcyclic := l2, c := sc } S Γ ⟨p4 (p3 p2), sat⟩
exact ⟨Z, ⟨v⟩⟩
```

This shows where the local source obtains its witness. It does not show how the supplied `fin` originally builds that witness or its `.th` field.

`TPS/AllStagesAtMemberOfSpecializations.lean:37–46` assembles stage results from named inputs. At line 42 it obtains `hFin` through:

```lean
GlobalTheory.T.sFin_and_sFinl_of_archCmp_sEta_thetaData
  hW hD hP hL hA hEta
  (GlobalTheory.HeightCounting.Up.sXd_all_alt hL)
```

The file imports `TPS/FinitenessOfHyp.lean`, but that file is explicitly marked `file-count-cap` in this run. Its body must be collected before assigning a construction mechanism to this supplier. The names of the inputs do not establish their mathematical content or how the headline proof discharges them.

### 3. Transport is distinguishable from initial construction

`TPS/FiniteLevelAndSecond.lean:66–71` obtains `v` from a finiteness hypothesis and constructs a new level record retaining `v.nx.2` while adding another property. Its line 118 uses `sFino_of_alt hF` as part of the resulting pair.

`TPS/OrgOfKept.lean:28–37` starts with an existing level record `l`, extracts its extension data, and passes that data into a transport function `hnx` to obtain `e'`. The second branch follows the same pattern. This is evidence of transport from an existing record, not identification of the original `.th` constructor.

## Compiled inspection limits

The archive records 18 target declarations and 34 direct-reference lists from stored types and available bodies, with no reference-list truncation. All 18 printed axiom reports list only `propext`, `Classical.choice`, and `Quot.sound`. These are recorded inspection results, not a new independent kernel verification.

Both targeted argument searches were inconclusive:

| Target | Binder | Nodes visited | Limit reached | Omitted annotation roots |
| --- | --- | ---: | --- | ---: |
| `GlobalTheory.ClassSumPinLink.pIota_classSumPin_alt` | `hN` | 100,000 | Yes | 24 |
| `GlobalTheory.ClassSumPinLink.classSumPin_of_read` | `hth` | 100,000 | Yes | 103 |

Both returned `not-found-in-projection` with `truncated: true`. Neither is an absence result. The search deliberately omits annotations, and its budget was exhausted. Previously inspected source contains uses of these hypotheses; this run adds no positive compiled occurrence for either search.

The rendered inspection log contains 1,538 `⋯` indicators. It must not be treated as a complete printed proof term. Source collection retained 200 files and excluded 474 requested candidates by the file-count cap. Neither the source collection nor the direct-reference lists constitute a complete transitive use analysis.

## Next decisive work

1. Resolve and inspect the exact owner and body of `sFin_and_sFinl_of_archCmp_sEta_thetaData`, prioritizing `FinitenessOfHyp.lean` over broad import collection. Follow the construction until the value supplied for `RealExpansionExtraData.th` is identified, preserving any intervening hypotheses.
2. At that construction and its consumer, record the instantiated parameters of `EMtTheta`. Check the domains and each antecedent before claiming either a genuine constraint or vacuous discharge.
3. Replace the capped broad searches with more focused extraction around the relevant application or constructor. A larger search budget alone does not remove annotation omissions or prove semantic necessity.
4. Keep local construction/use evidence distinct from a theorem-preserving transformation or an end-to-end statement comparison. Those stronger tests are still required for stronger conclusions.

Daniel Fairbanks' broader requests also remain open: full unknown-reason accounting, the targeted larger-budget `LedPart.pt` probe, a second control through the same classifier, project/library and instance/generated strata, and a preregistered use-classification sample. This narrow extension trace does not fulfill those census tasks.

Comparator status was neither inspected nor changed by this run. No new RH/GRH verdict, necessity verdict, or independent-kernel verdict is asserted.
