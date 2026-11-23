# Stage 3.3 findings: selected consumers and height comparison

Prepared 23 November 2026 from the uploaded v0.4 evidence. This is review of
recorded server output and collected source, not an independent rerun.

**Conclusion:** the inspected route contains concrete witness construction,
forwarding of a class-sum hypothesis into a returned certificate, and use of a
point-condition proof to satisfy a downstream premise. The height-comparison
implementation constructs a comparison valuation and applies a proved
inequality. These are more specific findings than membership in a large
reference closure. They do not establish necessity of the disputed geometry
predicate or validate the complete mathematical interpretation of RH/GRH.
Neither the critics' full allegation nor its negation is established here.

## 1. Run and integrity

Server folder: `/home/harry/rh-verification/critics-audit-stage3/stage3-e6awxog_`.
Run: 23 November 2026, approximately **02:58:46–03:00:38 EST**.
The project Lean process took **1 minute 40.70 seconds**, with exit status 0.

Evidence ZIP SHA-256:

```
92fd02423f25b113b84845e10c317d8cd25a6810691412229d4e263739809062
```

Verified locally from the supplied bytes:

* All **239 files** in `EVIDENCE_SHA256SUMS` match their recorded hashes.
* All **65 package files** in `SHA256SUMS` match both the archive and the
  original v0.4 package.
* Protocol, target-configuration and package-manifest hashes agree with metadata.
* The recorded before/after hashes of selected project inputs are identical.
* Reconstructing provenance records and printed-block indexes from `consumers.log`
  reproduces the supplied JSON indexes.
* The positive fixture, provenance fixture and consumer probe exited 0. The
  negative fixture exited 1 for the intended `True` versus `False` type mismatch.
* All eight target declarations were found. Their 1,147 retained type/body
  reference entries have no missing referenced declarations and no reference
  truncation. This is a sum of entries across locations, not 1,147 unique names.
* Each target's printed axiom list contains only `propext`, `Classical.choice`
  and `Quot.sound`.

Source collection copied **160 files, 1,475,418 bytes**. Each copied-file hash
matches the index; the runner records byte comparison with pinned git contents.
Another **268 queued source paths** received `file-count-cap`. Consequently the
source collection is deliberately incomplete. All eight target owner modules
were collected. The log has **180 elision indicators**; a complete raw-term
export is not claimed.

These integrity checks confirm consistency of the supplied evidence. They do
not independently authenticate the original source repository, every compiled
artifact, or the reported server execution. Comparator was not inspected or
controlled by this run, and no new Comparator verdict is available here.

## 2. Comparison witnesses: a conditional construction, not a free inhabitant

`GlobalTheory.Fc.RL.at_tie_alt` is defined in
`ThirdPlaceSeries/AtTie.lean`, lines 19–21. It delegates to
`LinkedAt.of_row (RowE.row (TieOfLink.hasTie_of_linked ...))`.
Its seven initial published-theorem assumptions and final extension-existence
assumption are introduced anonymously and are not supplied to that final call.
That is a local observation about this wrapper, not proof that the larger route
can dispense with the mathematical facts those assumptions describe.

The next implementation is available in `ThirdPlaceSeries/RowEHasTie.lean`:

* `hasTie_of_linked`, lines 71–90, destructures a linkage proof into `q`, a
  bundle `b'`, a bundle witness `w`, and an equality identifying the data.
* It builds normalization/compatibility inputs and calls `nonempty_tie_of_wit`.
* `nonempty_tie_of_wit`, lines 58–70, supplies recursion and compatibility data
  to `tie_of_rpk_alt`, which constructs `Nonempty b.Comparison₂`.

**Supported:** the inspected witness route uses linkage data and an existing
bundle witness. It does not simply assert that every arbitrary comparison type
is inhabited.

**Unresolved:** where the relevant linkage and bundle witness are obtained at
actual headline instantiations, and whether any relevant domain is empty or
semantically weaker than intended. The earlier `OAt False` experiment does not
answer that question about the original `anyGeometry` route.

## 3. Class-sum hypothesis: passed into a returned certificate

In `ThirdPlaceSeries/NmjTAtTied.lean`, lines 23–28,
`GlobalTheory.BigTop.PtAt.nmjT_at_tied_alt` names its class-sum hypothesis `hPin`.
Line 27 supplies it to `GlobalTheory.T.lattice_family_adoption_third_alt`, together
with `hDiv`, `hAg` and `hSum`, producing `hTh`. Line 28 assigns `hTh` to the
`eMj_th` field of the returned expansion-majorant certificate.

**Supported:** this hypothesis is explicitly supplied at a lemma application,
and the result of that application is retained in the returned certificate.
This is a concrete source-level use, beyond merely appearing somewhere in the
reference closure.

**Unresolved:** whether the callee uses `hPin` essentially, whether the predicate
it proves is vacuous in the relevant instance, and whether subsequent consumers
need that certificate field. No deletion, replacement, or proof-minimization
necessity test was performed in v0.4. This is not a completed sample-use census.

## 4. Row conditions: discharged as a downstream premise

`ThirdPlaceSeries/PtOf.lean`, line 83, defines `RowPointSummands` by
`b.pt.PointConditions'`. In `ThirdPlaceSeries/Realised.lean`, lines 63–80,
`PointConditions'` includes a `ties : p.CompatibilityConditions` field alongside
other conditions. `EventuallyAtPoints`, lines 117–118, quantifies over a point
and requires a proof of its `PointConditions'` before yielding its conclusion.

`ThirdPlaceSeries/EvWCOnPtOfGuarded.lean`, lines 12–32, consumes the eventual
row-condition hypothesis `hR`. After obtaining `hb`, its final application
passes `hb x hx e2 i` to `ha`, for the selected point. This supplies the required
`PointConditions'` premise.

**Supported:** the record containing `ties` is used to discharge a downstream
premise. It is not merely constructed and then never passed anywhere in this
local route.

**Unresolved:** whether the downstream proof projects and essentially uses the
specific `ties` field. Passing a whole record does not establish necessity of
every field. Determining that requires the actual proof supplied as `ha` at the
relevant instantiation, not just this generic transport lemma.

## 5. Height comparison: an explicit construction and inequality

The compiled module lookup identifies `GlobalTheory.CovHt.FrameCmp.htCmp` in
`Development/AbelianVarietyTheory/Proofs/DivisorProofs/SumAbsExOfLe.lean`,
lines 378–387. This resolves the implementation below the previously observed
wrapper `cover_height_comparison`.

`HTCmp` is defined in `Definitions/Divisors/SemiposAtOfPositive.lean`, lines
80–82. Schematically, under the displayed prime/place conditions, it says:

```
for each v belonging to recVals at the place,
there exists w belonging to htVals at the place,
such that w(f) ≤ v(f) + the specified error bound
for the quantified weights and sections.
```

The proof of `htCmp`:

1. Unpacks the supplied membership witness for the input valuation.
2. Calls `exists_isHTFrameCp y₀ hy` to obtain a suitable frame.
3. Identifies its prime with the required prime using coprimality and the
   prime ideal conditions.
4. Constructs a member of the target valuation set and proves the inequality
   with `val_le hy h ho u hf`.

The local `val_le` proof, lines 346–372, uses a frame comparison from
`exists_frBor`, valuation identities, and an exponent-sum bound. Thus the
previously printed wrapper's unused published-theorem parameter does **not**
by itself expose a missing proof of this local comparison.

Compiled references also resolve the previously unqualified names:

* `GlobalTheory.CompHt.recVals`, in
  `Definitions/Divisors/IsHomogeneousCompIdeal.lean`, line 250, is built from
  `valSet Xo c (algCls Xo c)` with a valuation-property proof.
* `GlobalTheory.CompHt.htVals`, in
  `Definitions/Divisors/IsLatBasisHtLatIffSpanEq.lean`, lines 477–490, uses a
  set specified by existence of prime, field/valuation and frame data, plus a
  displayed evaluation formula. It is not written there as the universal set
  or a constant-True predicate.

**Supported:** there is a concrete conditional comparison construction beneath
this wrapper. The displayed local implementation is not just `True.intro`.

**Unresolved:** nonemptiness of the input valuation set at the actual application,
adequacy of the underlying moduli/frame definitions, correctness of the intended
mathematical interpretation, and identification with the specific intrinsic
height disputed by the critics. A substantial conditional proof can still have
an empty or inadequately specified domain; these results do not exclude that.

## 6. What this changes, and what remains

The most useful advance is specificity: we now have actual source-level uses
and the implementation of a named height comparison, rather than only broad
reachability results. It would be too strong to say either that the critics
have been refuted or that these findings expose an RH flaw.

Priority follow-ups are:

1. Follow the actual instantiation that supplies the eventual point statement;
   determine whether it consumes `PointConditions'.ties`, and how that relates
   to the original geometry predicate.
2. Inspect `lattice_family_adoption_third_alt` and its returned equation to
   determine what `hPin` contributes, before designing a scoped intervention.
3. Trace the linkage/bundle witness supplier and the input-valuation witness at
   the relevant applications. Distinguish conditional constructions from
   established inhabitants.
4. Complete Daniel Fairbanks' remaining controls, origin/instance strata,
   unknown-budget breakdown and preregistered sample-use classification. These
   selected cases cannot substitute for a representative sample.

Stage 3 remains in progress. This run is evidence collection and source review,
not a new independent-kernel check or a necessity verdict.

## Evidence locations

All quoted source paths are relative to `collected-source/` inside the evidence
ZIP. `ThirdPlaceSeries/` abbreviates
`Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/`;
`Definitions/Divisors/` abbreviates
`Development/AbelianVarietyTheory/Definitions/Divisors/`.
The stored target renderings and axiom reports are in `consumers.log`, indexed
by `consumers-blocks.json`; module and reference metadata are in
`consumer-provenance.json`.
