# Stage 3 v0.10: constructing character data and normalizing the theta identity

Review date: 23 November 2026. This report reviews uploaded logs, compiled-declaration reference records and pinned source snapshots. Lean was not rerun in the review environment.

## Main finding

We now have a source-level account of how the character record's theta field is filled. `GlobalTheory.ChoiceRead.exists_stC_choice_alt` obtains a semilinear map `e`, a unit `u`, and proofs of basis, lattice and theta properties from a local-component supplier. It rescales the map by the inverse unit, installs that map in the choice record, and uses `ThetaAt.smul_inv` and `emtTheta_withE` to produce the required `EMtTheta` field.

This advances beyond v0.9's observation that the localized identity is transported from `l.c.th`. At the inspected constructor, that field is derived from a local theta identity by explicit normalization. The local-component implementation also contains algebraic reasoning involving embeddings, lattices, class sums and coefficient descent; it is not merely a wrapper returning `True.intro` at this point.

These are local findings under stated hypotheses. They do not establish that every hypothesis is nonvacuous at the headline inputs, that this route is indispensable, or that the critics' broader objections are resolved. Source complexity is not a substitute for those checks.

## Run and evidence checks

Evidence archive: `stage3-evidence(9).zip`.

SHA-256: `1cff7e206078852cc67a4523e029301367dfdb032241b2d82202f4e94dcb2f56`.

Server run directory: `/home/harry/rh-verification/critics-audit-stage3/stage3-mu7ihu69`.

Recorded run: 04:33:36–04:35:54 EST on 23 November 2026. The character inspection took 2:11.68, exited 0 and reported maximum RSS 52,089,004 KiB. Positive and provenance fixtures passed; the negative fixture produced its expected type error.

Review checks completed:

- All 363 evidence-manifest entries and 99 package-manifest entries match their hashes. The package manifest matches the previously delivered v0.10 package.
- All 33 recorded input hashes are unchanged before and after execution.
- The provenance, declaration-block index and provenance-fixture JSON were regenerated with the delivered runner and match the archived results.
- All 250 collected source hashes match, totaling 1,555,813 bytes. The source collector excluded another 97 requested paths at its file-count cap. The snapshot is therefore incomplete. Git-pin equality is recorded by the server runner; no new upstream checkout was fetched in this review.
- Twelve targets were present, with no direct-reference-list truncation. All twelve printed axiom lists contain only `propext`, `Classical.choice` and `Quot.sound`.
- There are 1,032 `⋯` printer-elision indicators. Printed declarations are not complete serialized proof terms.

Project revision: `753431bfe28701f6f3937f664fcaf08daa139c03`.

Mathlib revision: `0df444a360eaa60ab8c11dca51a86af692955474`.

This is consistency review of supplied evidence, not an independent rerun or new kernel-check verdict. Comparator was not inspected or controlled.

## Constructor and normalization

All paths below are relative to the archive's `collected-source/`. `TPS/` abbreviates `Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/`; `IE/` abbreviates `Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/`.

`TPS/NonGaloisExistsChoice.lean:19–37` gives the relevant constructor:

1. Apply `T.local_component_at_place_determined_alt` under the supplied global hypotheses and local choice conditions.
2. Extract `e`, `u`, `hb`, `hl`, and `hth` from the resulting witnesses.
3. Define the map `G` as the inverse-unit multiple of `e`.
4. Derive the basis and lattice properties for `G`.
5. Construct `HeightCountingCharacterData`, using `withE` to install the selected map and `tupWithE` to update the tied data.
6. Fill the theta field through `emtTheta_withE`, `pick_eq`, and `(hth v hv i).smul_inv _`.

In `IE/ChoiceSideWithE.lean`:

- `withE` replaces `eMt` and its basis/lattice proofs while retaining the other choice fields.
- `pick` selects `G` at the relevant nontrivial places and valid positive indices; it retains the original map outside that range. `pick_eq` proves the relevant branch is selected.
- `ThetaAt` states a conditional theta identity with scalar multiplier `t`.
- `ThetaAt.smul_inv` (lines 147–154) uses linearity and inverse-unit cancellation to change that multiplier to one.
- `emtTheta_withE` (lines 156–166) applies the supplied pointwise `ThetaAt` identity and simplifies `one_smul`.

Schematically, the normalization is

\[
\operatorname{thPe}(e(x))=u\cdot S
\quad\Longrightarrow\quad
\operatorname{thPe}(u^{-1}\cdot e(x))=S.
\]

Here `u` is a unit, not an arbitrary scalar that might be zero. This does not prove `S` or the relevant vector spaces are nonzero at the actual headline instantiation.

The compiled body-reference record for `exists_stC_choice_alt` includes the local-component supplier, `HeightCountingCharacterData.mk`, `withE`, `emtTheta_withE`, `pick_eq` and `ThetaAt.smul_inv`. These corroborate the source route. They do not, on their own, give complete argument-use or necessity evidence.

## Where the local identity comes from

`T.local_component_at_place_determined_alt` delegates to `GlobalTheory.PlaceRead.exists_local_map_at_place_alt`; its compiled reference record confirms this link.

The implementation is in `TPS/LocalComponentAtPlaceDetermined.lean`:

| Source step | What it does | Remaining issue |
| --- | --- | --- |
| `exists_local_map_at_place_alt`, lines 166 onward | Builds the `AtPlace` input using field, rationality, choice and series data; invokes `exists_basisAt_latAt_thetaAt_of_atPlace`. | The suppliers of those inputs remain part of the obligation. |
| `exists_basisAt_latAt_thetaAt_of_atPlace`, lines 95–162 | Lifts a complex map to the coefficient field, proves basis/lattice properties and derives `ThetaAt` up to a unit. | It relies on faithful-reading, proportionality and unit-existence results. |
| `exists_local_component_at_place_alt`, lines 36–94 | Uses a theta-lift/class-sum identity, conjugation, expansion evaluation and rescaling. | The invoked theta-lift theorem and its actual assumptions need further inspection. |

The last step calls the exact supplier

`GlobalTheory.T.thetaLift_twistLevelForm_eq_unit_mul_classSum`.

Its declaration body was not located in the collected source set. It is the highest-priority next target, alongside the proportionality/descent result `GlobalTheory.T.chosenField_forms_proportional_of_readings` and the unit supplier `GlobalTheory.T.exists_integral_unit_of_isUnitAwayFromLevel_embedding`.

An explicit case split in lines 148–161 deserves accurate interpretation. If the complex scalar descends to the coefficient field, the proof obtains a unit. Otherwise, it chooses unit one and uses the proportionality result: the zero case closes by zero identities, and the nonzero case would produce a descended scalar, contradicting that branch assumption. The occurrence of a zero case or `absurd` here does not establish a flaw or that the whole proof is vacuous. The content of the proportionality theorem and the concrete inputs must be checked.

These nested implementation steps are source observations. This phase recorded direct compiled references for the twelve selected targets, not for every nested helper named in this section.

## Level existence and retained hypotheses

The source and selected compiled references connect the level-existence wrapper to `stage_c_nonempty_of_published_inputs`, which combines `sc_of_sck_alt` with `stageCExists_of_casselmanWallach`. The latter delegates to `LevCmp.stageCExists_of_harishChandra_serN`, using the non-Galois character constructor. `sc_of_sck_alt` chooses conjugate settings and extracts the resulting character-data witness.

This establishes a local supplier route. It does not eliminate its hypotheses: discrete-series coverage, Casselman–Wallach, Harish-Chandra modules, `PublishedInputsThirdLayerAlt`, `SerN`, and the relevant local data. `PublishedInputsThirdLayerAlt` is a proposition-valued structure with named fields, including ray-class and representation-theoretic inputs. A hypothesis carrying such a name is not automatically an extra Lean axiom, and an axiom report does not prove that its premises have been supplied at every use site.

## Next decision point and limits

The next useful increment should inspect the theta-lift/class-sum theorem's compiled owner and body, plus the proportionality and unit suppliers. At the resulting construction, track the place/index domains and equality antecedents with their actual arguments. Report any further assumptions or transport explicitly.

This phase has not proved the route nonvacuous or circular, has not shown that `anyGeometry` invalidates a headline theorem, and has not established a new RH/GRH verdict. Daniel Fairbanks' broader requests—second control, full unknown accounting, larger-budget `LedPart.pt`, stratification and preregistered witness-use sampling—also remain separate unfinished work.

Suggested public wording:

> We traced the stored theta identity to a character-data constructor that normalizes a local map by an invertible scalar. Its supplier contains explicit algebraic steps, and we have identified the earlier theta-lift/class-sum theorem on which they rely. This narrows the next audit target; it does not yet settle the correctness or nonvacuity of the full RH/GRH proof.
