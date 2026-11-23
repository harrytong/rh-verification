# Nielsen/Chu critique: findings from Harry's pinned source

Source: `753431bfe28701f6f3937f664fcaf08daa139c03`.
Mathlib: `0df444a360eaa60ab8c11dca51a86af692955474`.
Lean: `leanprover/lean4:v4.33.1`.
Evidence: the uploaded source-evidence.zip, collected 2026-11-22 14:11 EST.

This document reports source inspection. It does not claim that a compiled
dependency trace has already run or that mathematical invalidity follows.

## Confirmed source facts

1. `anyGeometry` is defined as `fun _ _ _ => True` in
   `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/OverIx.lean:19`.
   The collector finds 162 exact-token textual occurrences in 24 files, including
   comments/strings if present. This reproduces Chu's 24-file observation.
2. `GeoCl.base` accepts a proof of the underlying predicate in
   `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/NotGeoClFalse.lean:22`.
   Consequently `geoCl anyGeometry D J X` is inhabited by `GeoCl.base True.intro`
   for every appropriately typed input. This establishes that this particular
   certificate imposes no restriction. It does not establish that all other
   hypotheses of a later analytic theorem impose no restriction.
3. `geoDegenerate`, `algDegenerate`, `padDegenerate`, `mdlJunk`, `geoDegenerateNoTau`,
   `algJunk`, and `padJunk` exist in
   `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean`.
   Many predicates are `True`; many types are `PUnit`; several measures/norms are
   zero. The model is not literally all zero: `geoDegenerate.inter` uses the
   integer flag-degree formula, for example. Full field definitions matter.
4. In that file, `divXFl` at line 829 sets `iMj` to the zero linear map at line
   860. `compatibleDivisorData` also uses a zero map at line 708. These are
   distinct constructions, not interchangeable names for one declaration.
5. `GlobalTheory.EX.OB.LedPart.ht` is defined to equal `DV.hExpl6 ...` at
   `src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/SetUnipotentTranslate.lean:379`.
   `LedPart.pt` supplies `h_eq := fun _ => rfl` at line 400. This confirms an
   identity by construction, not that other estimates about the assigned height
   are automatic. The formula itself contains sums and logarithmic terms;
   see `src/Formalism/LocalRingCardinality/KernelPlaceMeanBound.lean:25`.
6. `geoOf_surf`, `GeoTiedP.geoTied`, `GeoTiedP.formsTieX`, and
   `degree_value_of_determinant` each have one exact-token textual occurrence
   in the scanned source: their declaration. This is evidence of no named text
   calls in those tracked project files. It does not yet certify compiled
   non-reachability, exclude metaprogram-generated calls, or exclude equivalent
   arguments proved separately.

## Correction to the proposed top-level chain

The exact ASCII token `hypsE` has zero occurrences. The older file
`src/Development/AutomorphicArithmetic/ThetaCorrespondence/FockModels/EveryCharacterE.lean`
defines `UpperTheory.Lit.hypsE₂` at line 41 and `everyE₂` at line 67.
`everyE₂` calls `plugAll` at line 70.

The final source instead explicitly calls this newer route:

```
riemannHypothesis
  -> rhOfAll
  -> Formalism.VW.rh_of_every allChi
allChi
  -> UpperTheory.FinalTheorems.everyCharacter
  -> UpperTheory.FinalTheorems.everyCharacter_of_row
  -> UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin
  -> UpperTheory.Lit.every_character_of_theta_integrals_local_matching
  -> UpperTheory.Top.every_character_of_green_v_win
     [given a bundle constructed by
      UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound]
```

This is a source-call outline, not yet the complete compiled dependency path.
The new `nonempty_hyps_definite_side_of_closed_bound` ALSO passes
`geoCl anyGeometry` in its body. This happens in
`src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/SiegelEisensteinSecondTermHypotheses.lean:60`,
with further occurrences at lines 63 and 67. The named-route correction does
not make the substantive question disappear. Conversely, an import of the
older EveryCharacterE module does not establish use of its theorems.

## Concrete lower-level route worth testing

In `TupPinsOfMuIsW.lean`, `geoOver_stages` constructs a witness using `divXFl`
and `famFlJ`; `exists_divT` invokes it. `divEx_prov` invokes `exists_divT`;
`divEx_of_ox` invokes `divEx_prov`. In
`PublishedInputsImplyConclusion.lean`, `divEx_geoCl` invokes `divEx_of_ox`
and upgrades the unrestricted predicate using `geoCl_of`.
`MemberEClosing.lean`'s `memberE_closing_alt_alt` passes `divEx_geoCl` onward.
The compiled audit tests whether this route is reachable from each final root.

## Final statement inspection

`src/Main.lean` types the headline RH theorem as the root `RiemannHypothesis`.
The collected pinned Mathlib file
`Mathlib/NumberTheory/LSeries/RiemannZeta.lean:185` defines it as the familiar
zeta-zero statement, excluding negative even integers and the pole.
`src/Statements.lean` defines the Dirichlet statements using
`DirichletCharacter.LFunction`, which the pinned Mathlib defines through
`ZMod.LFunction`. This is source-level evidence, separate from the ongoing
Comparator's protected-statement comparison.

## What would constitute a conclusion

A syntactic path to a trivial auxiliary predicate confirms its presence in
the stored derivation, not an invalid inference. A predicate's descriptive
name is not an additional logical premise. A specific gap requires showing
which required implication, interpretation of the final statement, axiom
restriction, or kernel rule fails. An unused extraction lemma by itself does
not establish such a failure. The semantic adequacy of an intermediate
geometric interpretation is also distinct from derivability of the final
fixed statement under the admitted foundational axioms.

The next audit reports explicit theorem/opaque-body paths, per-root axiom
closures, and expanded inductive dependencies. It is an inspection tool and
does not replace Nanoda or Comparator.
