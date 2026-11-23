# Nielsen/Chu RH critique: compiled dependency audit findings

**Finding:** The completed audit confirms that the unrestricted geometry predicate and several degenerate-model constructions occur in the stored dependency closures of all five headline theorems. It also excludes the older `hypsE₂`/`plugAll` route and four named extraction lemmas from those closures. These are concrete dependency results; they do not establish an invalid mathematical inference.

## Scope and integrity

- Source commit: `753431bfe28701f6f3937f664fcaf08daa139c03`.
- Mathlib commit: `0df444a360eaa60ab8c11dca51a86af692955474`.
- Project toolchain: Lean 4.33.1. The separate, ongoing Comparator uses the previously installed judging toolchain.
- Audit started: 2026-11-22T14:30:10.341040-05:00; finished: 2026-11-22T15:07:33.389354-05:00. Both timestamps are Eastern Standard Time.
- Main inspection process elapsed: 37 minutes 14.81 seconds; exit status 0.
- Mandatory isolated smoke test: passed. Main is imported into a separate inspection process; the artificial premise used in the test fixture is not an axiom of the imported RH environment.
- Union graph: 1,478,243 declarations, 158,689,342 stored edges, no missing referenced declarations.
- Forty-seven watched names were tested against five roots in two traversal modes: 470 reachability records.
- Uploaded evidence ZIP SHA-256: `631b10943cc058181f0dfec034f60f96b908ee2cbeec92ab04379c4f62dc76ae`.
- All 352 collected follow-up source file hashes match their accompanying index. The uploaded Lean trace program matches the hash in run metadata.
- The runner checked the pinned source and headline compiled-file hashes before and after inspection. This report analyzes the user-supplied run artifacts; it does not claim access to the server or an independent rerun of its large compiled environment.

## What the two traversal modes mean

**Reference mode** follows constants appearing in declaration types, definition values, theorem proofs, and opaque values. It does not merely follow file imports.

**Expanded mode** additionally follows inductive constructors, mutual inductive declarations, constructor parents, and recursor reduction-rule dependencies. This broader closure can include declarations not explicitly referenced by the chosen proof term.

A path is a syntactic witness, not a proof that every visited declaration is indispensable. Types, unused lets, and unused arguments can introduce references. The audit does not normalize and minimize the proof. An absent named lemma does not exclude an inlined proof or a different argument. All watched targets have the same yes/no membership in both modes for a given root.

## Axiom results

Every one of the ten passes found exactly `propext`, `Classical.choice`, and `Quot.sound`. No additional axiom, including `sorryAx`, was reported in these closures. This is a fresh stored-declaration traversal, not another kernel-checking run.

| Headline theorem | Reference closure | Expanded closure | Axioms |
|---|---:|---:|---|
| `riemannHypothesis` | 1,478,198 | 1,478,219 | the same three |
| `riemannZeta_eq_zero_re` | 1,478,200 | 1,478,221 | the same three |
| `LFunction_ne_zero_of_half_lt_re` | 1,478,190 | 1,478,211 | the same three |
| `LFunction_eq_zero_re` | 1,478,203 | 1,478,224 | the same three |
| `LFunction_eq_zero_re_of_isPrimitive` | 1,478,193 | 1,478,214 | the same three |

## Findings relevant to the criticism

1. **Unrestricted geometry is on all five reference paths.** `GlobalTheory.Mem.Top.Bl.anyGeometry` is present in all five closures. Source inspection confirms its body is `fun _ _ _ => True`. `GeoCl` and `geoCl` are also reachable. This resolves the factual dependency question that Chu originally left open; an import-only explanation is insufficient.

2. **Several degenerate witnesses are also reachable.** `geoDegenerate`, `algDegenerate`, `padDegenerate`, `mdlJunk`, `divXFl`, and `famFlJ` occur in all five closures. The definition of `divXFl` assigns `iMj` the zero linear map. In contrast, `geoDegenerateNoTau`, `algJunk`, `padJunk`, and `compatibleDivisorData` are present in the environment but absent from all five closures. Broad statements that every model bearing a “junk” name lies on the final route are therefore inaccurate for this revision.

3. **The older named route is excluded.** The name `UpperTheory.Lit.hypsE` is absent from the environment. `UpperTheory.Lit.hypsE₂`, `UpperTheory.Lit.everyE₂`, and `UpperTheory.Top.plugAll` exist but are absent from every headline closure, even in expanded mode. The newer `nonempty_hyps_definite_side_of_closed_bound` and `every_character_of_green_v_win` are present and reachable. The newer constructor still passes `geoCl anyGeometry`; correcting the route does not remove that observation.

4. **The four named extraction lemmas are excluded.** `geoOf_surf`, `GeoTiedP.geoTied`, `GeoTiedP.formsTieX`, and `degree_value_of_determinant` exist but are absent from all five closures, in both modes. The predicate `GlobalTheory.Mem.Top.Bl.geoOf` is also absent from all five closures. This is stronger evidence than the earlier text search. It does not prove that their intended mathematical content is absent by every other route.

5. **The constructed height is reachable.** `GlobalTheory.EX.OB.LedPart.ht`, `LedPart.pt`, and `Formalism.BasicNotions.DV.hExpl6` are reachable from every root. Source inspection confirms the assignment to `hExpl6` and the `rfl` identity. The shortest stored path to `hExpl6` includes a declaration-type edge through `GlobalTheory.Fc.LkT`; the audit must not portray every shortest path as a sequence of proof applications.

6. **Other supplied premises remain to be interpreted.** The reachable theorem `every_character_of_theta_integrals_local_matching` takes, among other arguments, `CovolumeBoundOfX`, theta-integral agreement, and local matching. Its bundle-construction theorem takes these arguments as well. `HypsAlt` has numerous fields, including bounded-realization, counting, and selection conditions. The final source supplies a covolume-bound argument via `SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt`; that theorem and the two watched Hilbert-Samuel/Moriwaki inputs are in every closure. Merely identifying a trivial geometry component does not inspect or dispose of these other obligations. This report has not completed a human mathematical audit of all their definitions and proofs.

## Exact witness paths

The paths below come from reference mode for `riemannHypothesis`. Every arrow is labeled with the kind of stored reference that produced it. Full per-root paths remain in the evidence ZIP.

### `GlobalTheory.Mem.Top.Bl.anyGeometry`

```text
riemannHypothesis
  --[theorem-proof]--> rhOfAll
  --[theorem-proof]--> allChi
  --[theorem-proof]--> UpperTheory.FinalTheorems.everyCharacter
  --[theorem-proof]--> UpperTheory.FinalTheorems.everyCharacter_of_row
  --[theorem-proof]--> UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin
  --[theorem-proof]--> UpperTheory.Lit.every_character_of_theta_integrals_local_matching
  --[theorem-proof]--> UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound
  --[theorem-proof]--> GlobalTheory.Mem.Top.Bl.anyGeometry
```

### `Formalism.L2.Geo.geoDegenerate`

```text
riemannHypothesis
  --[theorem-proof]--> rhOfAll
  --[theorem-proof]--> allChi
  --[theorem-proof]--> UpperTheory.FinalTheorems.everyCharacter
  --[theorem-proof]--> UpperTheory.FinalTheorems.everyCharacter_of_row
  --[theorem-proof]--> UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin
  --[theorem-proof]--> UpperTheory.Lit.every_character_of_theta_integrals_local_matching
  --[theorem-proof]--> UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound
  --[theorem-proof]--> GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt
  --[theorem-proof]--> GlobalTheory.T.large_unramified_exponent_bundles_exist_alt
  --[theorem-proof]--> GlobalTheory.Fc.StageOneU.member_bundles_large_unramified_exponents_alt
  --[theorem-proof]--> GlobalTheory.T.member_exists_baseLattice_alt
  --[theorem-proof]--> GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_prime_alt
  --[theorem-proof]--> GlobalTheory.Mem.Top.Bl.exists_baseLattice_of_pair_alt
  --[theorem-proof]--> GlobalTheory.Mem.Top.Closing.memberE_closing_alt_alt
  --[theorem-proof]--> GlobalTheory.Mem.Top.Closing.divEx_geoCl
  --[theorem-proof]--> GlobalTheory.Mem.Top.DivRec.divEx_of_ox
  --[theorem-proof]--> GlobalTheory.Mem.Top.DivRec.divEx_prov
  --[theorem-proof]--> GlobalTheory.Mem.Top.DivRec.exists_divT
  --[theorem-proof]--> GlobalTheory.Mem.Top.DivRec.geoOver_stages
  --[theorem-proof]--> Formalism.L2.Geo.divXFl
  --[definition-value]--> Formalism.L2.Geo.geoDegenerate
```

### `Formalism.BasicNotions.DV.hExpl6`

```text
riemannHypothesis
  --[theorem-proof]--> rhOfAll
  --[theorem-proof]--> allChi
  --[theorem-proof]--> UpperTheory.FinalTheorems.everyCharacter
  --[theorem-proof]--> UpperTheory.FinalTheorems.everyCharacter_of_row
  --[theorem-proof]--> UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin
  --[theorem-proof]--> UpperTheory.Lit.every_character_of_theta_integrals_local_matching
  --[theorem-proof]--> UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound
  --[type]--> GlobalTheory.Fc.LkT
  --[definition-value]--> GlobalTheory.Fc.BPt.D
  --[definition-value]--> GlobalTheory.EX.OB.LedPart.pt
  --[definition-value]--> GlobalTheory.EX.OB.LedPart.ht
  --[definition-value]--> Formalism.BasicNotions.DV.hExpl6
```

## Full watched-name membership

“Yes” means reference-mode reachability from the named root, not mathematical indispensability. The expanded-mode answers are identical for these watched names. Missing names and existing-but-unreachable names are distinguished.

| Watched name | Exists | RH | Zeta zeros | Dirichlet nonvanishing | Dirichlet zeros | Primitive zeros |
|---|---|---|---|---|---|---|
| `GlobalTheory.Mem.Top.Bl.anyGeometry` | yes | yes | yes | yes | yes | yes |
| `GlobalTheory.Mem.Top.Bl.geoOf` | yes | no | no | no | no | no |
| `GlobalTheory.Mem.Top.Bl.GeoCl` | yes | yes | yes | yes | yes | yes |
| `GlobalTheory.Mem.Top.Bl.geoCl` | yes | yes | yes | yes | yes | yes |
| `GlobalTheory.Mem.Top.Bl.OXModel.geoOf_surf` | yes | no | no | no | no | no |
| `UpperTheory.Lit.hypsE` | no | no | no | no | no | no |
| `UpperTheory.Lit.hypsE₂` | yes | no | no | no | no | no |
| `UpperTheory.Lit.everyE₂` | yes | no | no | no | no | no |
| `UpperTheory.Top.plugAll` | yes | no | no | no | no | no |
| `UpperTheory.Top.every_character_of_green_v_win` | yes | yes | yes | yes | yes | yes |
| `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound` | yes | yes | yes | yes | yes | yes |
| `UpperTheory.Lit.every_character_of_theta_integrals_local_matching` | yes | yes | yes | yes | yes | yes |
| `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin` | yes | yes | yes | yes | yes | yes |
| `UpperTheory.FinalTheorems.everyCharacter_of_row` | yes | yes | yes | yes | yes | yes |
| `UpperTheory.FinalTheorems.everyCharacter` | yes | yes | yes | yes | yes | yes |
| `GlobalTheory.Mem.Top.DivRec.geoOver_stages` | yes | yes | yes | yes | yes | yes |
| `GlobalTheory.Mem.Top.DivRec.exists_divT` | yes | yes | yes | yes | yes | yes |
| `GlobalTheory.Mem.Top.DivRec.divEx_prov` | yes | yes | yes | yes | yes | yes |
| `GlobalTheory.Mem.Top.DivRec.divEx_of_ox` | yes | yes | yes | yes | yes | yes |
| `GlobalTheory.Mem.Top.Closing.divEx_geoCl` | yes | yes | yes | yes | yes | yes |
| `GlobalTheory.Mem.Top.Closing.memberE_closing_alt_alt` | yes | yes | yes | yes | yes | yes |
| `GlobalTheory.T.member_exists_baseLattice_alt` | yes | yes | yes | yes | yes | yes |
| `Formalism.L2.Geo.geoDegenerate` | yes | yes | yes | yes | yes | yes |
| `Formalism.L2.Geo.geoDegenerateNoTau` | yes | no | no | no | no | no |
| `Formalism.L2.Geo.algDegenerate` | yes | yes | yes | yes | yes | yes |
| `Formalism.L2.Geo.algJunk` | yes | no | no | no | no | no |
| `Formalism.L2.Geo.padDegenerate` | yes | yes | yes | yes | yes | yes |
| `Formalism.L2.Geo.padJunk` | yes | no | no | no | no | no |
| `Formalism.L2.Geo.mdlJunk` | yes | yes | yes | yes | yes | yes |
| `Formalism.L2.Geo.divXFl` | yes | yes | yes | yes | yes | yes |
| `Formalism.L2.Geo.compatibleDivisorData` | yes | no | no | no | no | no |
| `Formalism.L2.Geo.famFlJ` | yes | yes | yes | yes | yes | yes |
| `Formalism.L2.Geo.GeoTiedP.geoTied` | yes | no | no | no | no | no |
| `Formalism.L2.Geo.GeoTiedP.formsTieX` | yes | no | no | no | no | no |
| `Formalism.MainNotions.placeRankTwoOne.degree_value_of_determinant` | yes | no | no | no | no | no |
| `GlobalTheory.EX.OB.LedPart.ht` | yes | yes | yes | yes | yes | yes |
| `GlobalTheory.EX.OB.LedPart.pt` | yes | yes | yes | yes | yes | yes |
| `Formalism.BasicNotions.DV.hExpl6` | yes | yes | yes | yes | yes | yes |
| `SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt` | yes | yes | yes | yes | yes | yes |
| `PositivityTheory.Pf1.HilbertSamuelMoriwaki.hsUse_outright` | yes | yes | yes | yes | yes | yes |
| `PositivityTheory.Pf1.HilbertSamuelMoriwaki.moriwakiBig_outright` | yes | yes | yes | yes | yes | yes |
| `allChi` | yes | yes | yes | yes | yes | yes |
| `rhOfAll` | yes | yes | yes | no | no | no |
| `Formalism.VW.rh_of_every` | yes | yes | yes | no | no | no |
| `RiemannHypothesis` | yes | yes | yes | no | no | no |
| `riemannZeta` | yes | yes | yes | yes | yes | yes |
| `DirichletCharacter.LFunction` | yes | yes | yes | yes | yes | yes |

## Assessment

**Supported:** Several precise code observations in the criticism are correct, and the relevant unrestricted/degenerate constructions are connected to the final stored proof terms. The four named extraction lemmas are absent from those dependency closures.

**Corrected:** The proposed route through `hypsE`/`hypsE₂` and `plugAll` is not the route in this pinned proof. Some other degenerate/junk models named in the criticism are also absent from the final closures.

**Not established:** The implication “a trivial auxiliary predicate is reachable, therefore no proof of RH was supplied.” An auxiliary predicate can impose no condition while the rest of a theorem has substantive premises. A missing wrapper lemma can be bypassed by direct field extraction or another proof. A concrete refutation must identify a failure in a required inference, the fixed final definitions, the axiom restriction, or the trusted checking assumptions. The trace alone supplies none of those failures.

If the final statement and its transitive definitions match the protected Mathlib challenge, and a sound independent kernel accepts a derivation using the permitted foundational axioms, arbitrary auxiliary definitions do not invalidate that derivation. Human interpretation of the geometric narrative is a separate question. This is a conditional logical assessment, not a claim that the still-running Comparator has passed.

## Verification status at this point

- Full project Main build: previously reported successful.
- Standalone Nanoda: previously reported 1,484,733 declarations with no typechecker errors, exit 0; the reported pretty-printer diagnostic remains part of that record.
- This compiled-dependency audit: completed, ten passes, only the three permitted axioms, no missing referenced declarations.
- Comparator: still running according to the most recent user status. No final Comparator acceptance is claimed here.

No additional build or export is required to preserve these findings. Keep the existing source pin, export hashes, logs, and completed evidence ZIP.
