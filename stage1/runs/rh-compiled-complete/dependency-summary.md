# RH/Dirichlet-GRH compiled dependency audit

Source commit: `753431bfe28701f6f3937f664fcaf08daa139c03`
Mathlib commit: `0df444a360eaa60ab8c11dca51a86af692955474`
Lean: `4.33.1`

Isolated smoke test passed: **True**
Full audit completed: **True**
Container exit status: `0`

This is a stored-syntax dependency audit, not an independent kernel check or a verdict on mathematical validity.
Reference paths follow constants in types and definition/theorem/opaque bodies. Expanded paths also follow inductive declarations and recursor rules.
A syntactic path can pass through unused lets or arguments. Absence of a named lemma does not exclude an inlined or alternative argument.

Union graph declarations: 1,478,243
Union graph edges: 158,689,342
Missing referenced declarations: []

- `riemannHypothesis` (references): 1,478,198 declarations; axioms: `propext, Classical.choice, Quot.sound`
- `riemannHypothesis` (expanded): 1,478,219 declarations; axioms: `propext, Classical.choice, Quot.sound`
- `riemannZeta_eq_zero_re` (references): 1,478,200 declarations; axioms: `propext, Classical.choice, Quot.sound`
- `riemannZeta_eq_zero_re` (expanded): 1,478,221 declarations; axioms: `propext, Classical.choice, Quot.sound`
- `LFunction_ne_zero_of_half_lt_re` (references): 1,478,190 declarations; axioms: `propext, Classical.choice, Quot.sound`
- `LFunction_ne_zero_of_half_lt_re` (expanded): 1,478,211 declarations; axioms: `propext, Classical.choice, Quot.sound`
- `LFunction_eq_zero_re` (references): 1,478,203 declarations; axioms: `propext, Classical.choice, Quot.sound`
- `LFunction_eq_zero_re` (expanded): 1,478,224 declarations; axioms: `propext, Classical.choice, Quot.sound`
- `LFunction_eq_zero_re_of_isPrimitive` (references): 1,478,193 declarations; axioms: `propext, Classical.choice, Quot.sound`
- `LFunction_eq_zero_re_of_isPrimitive` (expanded): 1,478,214 declarations; axioms: `propext, Classical.choice, Quot.sound`

## Watched declarations

| Declaration | Present in imported environment | RH reference path | Dirichlet nonvanishing reference path |
|---|---|---|---|
| `GlobalTheory.Mem.Top.Bl.anyGeometry` | yes | yes | yes |
| `GlobalTheory.Mem.Top.Bl.geoOf` | yes | no | no |
| `GlobalTheory.Mem.Top.Bl.GeoCl` | yes | yes | yes |
| `GlobalTheory.Mem.Top.Bl.geoCl` | yes | yes | yes |
| `GlobalTheory.Mem.Top.Bl.OXModel.geoOf_surf` | yes | no | no |
| `UpperTheory.Lit.hypsE` | no | no | no |
| `UpperTheory.Lit.hypsE₂` | yes | no | no |
| `UpperTheory.Lit.everyE₂` | yes | no | no |
| `UpperTheory.Top.plugAll` | yes | no | no |
| `UpperTheory.Top.every_character_of_green_v_win` | yes | yes | yes |
| `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound` | yes | yes | yes |
| `UpperTheory.Lit.every_character_of_theta_integrals_local_matching` | yes | yes | yes |
| `UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin` | yes | yes | yes |
| `UpperTheory.FinalTheorems.everyCharacter_of_row` | yes | yes | yes |
| `UpperTheory.FinalTheorems.everyCharacter` | yes | yes | yes |
| `GlobalTheory.Mem.Top.DivRec.geoOver_stages` | yes | yes | yes |
| `GlobalTheory.Mem.Top.DivRec.exists_divT` | yes | yes | yes |
| `GlobalTheory.Mem.Top.DivRec.divEx_prov` | yes | yes | yes |
| `GlobalTheory.Mem.Top.DivRec.divEx_of_ox` | yes | yes | yes |
| `GlobalTheory.Mem.Top.Closing.divEx_geoCl` | yes | yes | yes |
| `GlobalTheory.Mem.Top.Closing.memberE_closing_alt_alt` | yes | yes | yes |
| `GlobalTheory.T.member_exists_baseLattice_alt` | yes | yes | yes |
| `Formalism.L2.Geo.geoDegenerate` | yes | yes | yes |
| `Formalism.L2.Geo.geoDegenerateNoTau` | yes | no | no |
| `Formalism.L2.Geo.algDegenerate` | yes | yes | yes |
| `Formalism.L2.Geo.algJunk` | yes | no | no |
| `Formalism.L2.Geo.padDegenerate` | yes | yes | yes |
| `Formalism.L2.Geo.padJunk` | yes | no | no |
| `Formalism.L2.Geo.mdlJunk` | yes | yes | yes |
| `Formalism.L2.Geo.divXFl` | yes | yes | yes |
| `Formalism.L2.Geo.compatibleDivisorData` | yes | no | no |
| `Formalism.L2.Geo.famFlJ` | yes | yes | yes |
| `Formalism.L2.Geo.GeoTiedP.geoTied` | yes | no | no |
| `Formalism.L2.Geo.GeoTiedP.formsTieX` | yes | no | no |
| `Formalism.MainNotions.placeRankTwoOne.degree_value_of_determinant` | yes | no | no |
| `GlobalTheory.EX.OB.LedPart.ht` | yes | yes | yes |
| `GlobalTheory.EX.OB.LedPart.pt` | yes | yes | yes |
| `Formalism.BasicNotions.DV.hExpl6` | yes | yes | yes |
| `SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt` | yes | yes | yes |
| `PositivityTheory.Pf1.HilbertSamuelMoriwaki.hsUse_outright` | yes | yes | yes |
| `PositivityTheory.Pf1.HilbertSamuelMoriwaki.moriwakiBig_outright` | yes | yes | yes |
| `allChi` | yes | yes | yes |
| `rhOfAll` | yes | yes | no |
| `Formalism.VW.rh_of_every` | yes | yes | no |
| `RiemannHypothesis` | yes | yes | no |
| `riemannZeta` | yes | yes | yes |
| `DirichletCharacter.LFunction` | yes | yes | yes |
