# Stage 4: mapping the height criticism to the code

Prepared 23 November 2026. This is an AI-assisted review of Harry Tong's recorded server evidence and saved source, together with the primary web statements listed below. It is not a new Lean run, independent kernel replay, or Comparator result.

## Finding

The assigned-height identity is confirmed. The conclusion that this makes the RH proof invalid does not follow from that identity. The next concrete target is the pair of bounds in `Formalism.L2.DIV.WordFacts` and their supplied proofs, rather than another general search for declarations containing “height”. These are closer to Nielsen's description of a height between an automorphic pairing and a main term. This is a candidate match, not confirmation that Nielsen intended this exact declaration.

The newly reviewed consumer `Formalism.L2.DIV.linkDIV_at_words` takes the height identity and a separate height-bound proof as distinct arguments. Its body rewrites using the identity and then invokes that bound. This source fact narrows the question; it does not establish that the supplied bound remains non-reflexive at every concrete instantiation.

## Primary-source attribution

Nielsen's [publication listing](https://philpeople.org/profiles/jenny-lorraine-nielsen/publications?app=philpeople&order=viewings), retrieved on 23 November, alleges that assigned height and copied lattice data collapse an important inequality to reflexivity. It also acknowledges the Mathlib theorem type while characterizing the result as a tautology. No exact inequality identifier or complete application is supplied in the retrieved passage. The PhilArchive record and PDF returned HTTP 403, so this review does not claim to have read or identified a version of the current full paper.

Her [DEV comment](https://dev.to/startigerjln/comment/3m23n) identifies `setDiv` and `hExpl6` and asserts that the intended independent geometric realization is absent. Its older route description should not replace the route established by the compiled audit.

Chu's [article](https://dev.to/frankchu/grh-proofs-geometry-is-fun-true-in-24-files-2n2b) explicitly excludes the height equation and lattice witness from his verified findings. Attribute the height-invalidity allegation to Nielsen; do not describe it as an independently reproduced finding by Chu.

These pages are mutable; this report assigns no paper version or revision date.

## Completed v0.4 result

Evidence SHA-256:

```text
670b0f7c58eef765cfb9a1af6c88c3678b3e760337f7240cc45a56e3c5b65363
```

All 36 entries in the evidence manifest were verified. The reported project process exited 0 after 1:17.15. Both controls completed as intended. Recorded input hashes agree before and after the run. These checks establish consistency of the supplied evidence, not independent authentication of the server execution.

| Target | Recorded result |
| --- | --- |
| `GlobalTheory.CovHt.HtTopG.slope_le_height`, generic conclusion | Sides not definitionally identical |
| `GlobalTheory.CovHt.HtTopG.height_add_log_nonneg`, generic conclusion | Sides not definitionally identical |
| `GlobalTheory.CovHt.FrameCmp.val_le`, generic conclusion | Sides not definitionally identical |
| `heightAt_eq_of_cover` applying `slope_le_height`, first observed application | Sides not definitionally identical |
| `FrameCmp.htCmp` applying `val_le`, first observed application | Sides not definitionally identical |

The comparison used full transparency. No compared side was print-truncated. The two application searches reached their first matches without hitting their caps. The assigned-height control closed by `rfl`; `example : RiemannHypothesis := riemannHypothesis` also compiled in the imported environment.

The first-application scope is not exhaustive. In particular, the slope application's context retains parameters and hypotheses, including `p`, `Y`, and a locally quantified function `sl`. This is not the result of substituting every concrete headline-proof argument. A negative definitional-equality result is not a proof of mathematical inequality or of non-vacuity.

## Direct source mapping

Source paths below are relative to `src/` in the saved checkout recorded as commit `753431bfe28701f6f3937f664fcaf08daa139c03`. This section is source inspection, not a fresh compiled-term check or proof of headline-path membership for every named declaration.

### 1. Assignment

`Development/AbelianVarietyTheory/Definitions/GlobalTwisting/SetUnipotentTranslate.lean`:

- Lines 25–31: `setDiv` replaces the height and lattice fields of a newly constructed datum. It also assigns `HH` using `max` and supplies its bound with `le_max_right`.
- Lines 379–401: `LedPart.ht` is the explicit formula, and `LedPart.pt` constructs the new datum and supplies `h_eq` by reflexivity.

This confirms an assigned field. It does not say that an arbitrary pre-existing height equals the formula, nor that an arbitrary upper bound on the assigned height follows.

### 2. Formula

`Formalism/LocalRingCardinality/KernelPlaceMeanBound.lean`, lines 25–27, defines `hExpl6` from `SZbP`, finite sums of `kernelPlaceMeanBound` and `L6lo`, and a mean of logarithms of `kapR`. It is not syntactically the constant zero.

### 3. The pair of bounds most closely matching the criticism

`Formalism/LocalToGlobal/Divisibility/RecBridge.lean`, lines 128–133, defines `Formalism.L2.DIV.WordFacts`. Besides a lattice-map inclusion, it requires:

```text
Bk u ≠ 0 → htMap (Bk u) ≤ D.div.h u
D.div.RR.muDual + D.div.h u - L.Fo ≤ L.MAIN u + error terms
```

This is schematic notation; the source contains the full typed arguments. The nonzero premise in the first bound matters. Whether it is satisfied at a concrete application must be recorded, not assumed.

At lines 135–153, `wordFacts_of` consumes separate numerical bounds `c2` and `c3`, and an equality `tH` connecting the assigned height to the numerical expression. It uses `c2` after rewriting for the first bound, and arithmetic reasoning for the second. At lines 179–202, `wordFacts_of_clauses` supplies those obligations from `DivClausesR`, using `htMap_le_of_bound` for the first. The latter uses a logarithmic norm estimate. None of these source observations alone determines what happens after concrete specialization.

### 4. Identity and bound remain separate inputs to the bridge

In the same file, `linkDIV_at_words`, lines 327–339, receives:

```lean
(hh : ∀ u, D.div.h u = hExpl6 D L Z Csz u)
(hH : Formalism.MainNotions.LocalQuadraticParts.FrameNumberBound D L Z Csz CH)
```

One proof branch is:

```lean
have hfun : D.div.h = hExpl6 D L Z Csz := funext hh
-- ...
· rw [hfun]; exact hH
```

The local proof uses an already supplied bound after substituting the formula. This refutes the reading that this branch obtains the bound from the identity alone. It does not prove necessity of `hH` or validate its concrete supplier.

`FrameNumberBound` in `Formalism/SharpRestriction/Divisibility/LocalQuadraticParts.lean`, lines 350 and 363–364, expands to:

```text
sFrame D.div.Nu (hExpl6 D L Z Csz) + D.div.RR.muMax
  ≤ L.sc.x ^ CH * L.sc.b
```

In `linkDIVt_of_rows` and `linkDIVt_of_rowsF`, the height equality comes from `Fm.h_eq`, whereas the bound comes from `B.hh hN`. These are separate fields in the generic source. This is not yet a trace of the concrete `B` selected by a headline theorem.

## Interpretation and correction to the audit criterion

Defining an auxiliary quantity by a formula is legal. If `H := F`, the equality `H = F` is automatic; the bound `H ≤ G` is equivalent to `F ≤ G` and still needs justification. A reflexive intermediate step can occur inside a valid proof.

Consequently, even proving that one inspected bound becomes reflexive would not by itself invalidate RH. Conversely, finding one non-reflexive bound would not establish the intended geometric interpretation of the whole development. Necessity of an auxiliary construction is not a requirement for proof validity either.

For formal invalidity, the criticism needs to identify a defect in the accepted statement, its assumptions, or its verification. If a sound checker accepts a closed proof of the independently fixed Mathlib RH statement with only the allowed axioms, internal definitions called “geometry” cannot turn that conclusion into a different statement. Human review can still challenge the geometric explanation or identify a discrepancy in those verification premises.

The [Lean FRO/Mathlib statement](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/) reports independent statement comparison and proof checking. That is external reported evidence, not a result of Harry's still-unreported Comparator run. The compiled example in v0.4 establishes its type only in the imported environment.

## Next bounded investigation

Prioritize the actual `WordFacts` application and its `DivClausesR` arguments, with `FrameNumberBound` as the adjacent bound to track. Before any new server run:

1. Locate the selected construction in the existing compiled dependency evidence. Record the concrete call and substitutions, or explicitly mark that path identification as incomplete.
2. Preserve both numerical bounds, the `Bk u ≠ 0` premise, the equality `tH`, and the proofs supplied for `c2` and `c3`. Do not compare only generic theorem conclusions.
3. Determine whether either side becomes definitionally identical after those substitutions. Record any use of propositional rewriting separately from definitional reduction.
4. If a premise becomes false, classify the conditional branch as vacuous at that instance; do not infer a missing witness or invalidity of a closed theorem from it.
5. Request Nielsen's exact declaration and concrete application if her intended comparison differs. A different target must be documented before testing, rather than selected after seeing a result.

No new probe version or server run is required to establish the source distinctions in this report. The open task is concrete application identification, not another census or wholesale rebuild. This report does not resolve the separate Stage 3 census follow-ups.

## Suggested reviewer question

Our audit confirms that the constructed height is assigned by definition. In `Formalism.L2.DIV.linkDIV_at_words`, however, the height identity and `FrameNumberBound` are separate inputs; the proof rewrites with the former and invokes the latter. `WordFacts` also separates the height identity from its lower and upper bounds. Which fully qualified declaration and concrete application do you claim makes the relevant inequality reflexive? Providing the instantiated left and right sides would let us test your precise allegation against the pinned compiled release.

This question has not been sent to anyone.

## Hashes of the source snapshots inspected for this mapping

These identify the local source bytes reviewed, not a new authentication of the complete checkout.

```text
52560bbc51e012b706fc6838bfa75eb15f2cf05f7e6f9ccde98d2d8b5c5c60df  Development/AbelianVarietyTheory/Definitions/GlobalTwisting/SetUnipotentTranslate.lean
22fdce18696511899e2818b3ea8b2868f97cb810b02b8f9b1fc1cbbd98f120af  Formalism/LocalRingCardinality/KernelPlaceMeanBound.lean
ba20a46a7a5132ecd646b85dfd4ec4df838e818543083930b34d2a11533e962b  Formalism/LocalToGlobal/Divisibility/RecBridge.lean
7b0dcf3680ea9942d350110db269931f859b2276885b417445ecf5629be1dc5c  Formalism/SharpRestriction/Divisibility/LocalQuadraticParts.lean
```
