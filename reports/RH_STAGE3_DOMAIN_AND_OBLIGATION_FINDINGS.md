# Stage 3 v0.3 findings: domain boundaries and proof obligations

Reviewed 23 November 2026. This report reviews Harry Tong's uploaded evidence
from `stage3-ffpn8emg`, phase `obligations`. It checks recorded outputs and source
snapshots; it does not independently rerun Lean.

**Result:** all five domain propositions compiled. The witness and height
inspection steps also completed. The False specialization has an empty local
object domain, while anyGeometry leaves a separate LamAre requirement. The
comparison properties are passed into specific consumers; compatibility is
also stored in a resulting record. These facts narrow the investigation but do
not establish that the headline proof is correct or that the critics are correct.

## Integrity and run status

- Evidence ZIP SHA-256: `36257f9ba12cdea1666f6f7192db608808b21aa737b9e274481251a3f62946c6`.
  It matches the pasted terminal output.
- All 142 entries in EVIDENCE_SHA256SUMS verify. The package manifest entries,
  protocol hash, target-list hash and per-declaration rendered-block hashes also verify.
- Domain protocol SHA-256: `e28914b84440fd70ffb713ab7a6e74ea164bf9be0c7ffb70af8fd37785966368`.
- Recorded selected input hashes agree before and after the run.
- Execution: 23 November 2026, approximately 02:40:41–02:44:40 EST.
- Positive fixture exited 0. Negative fixture exited 1 with the intended type
  error. Domains, witness-chain and height-chain each exited 0.
- Bounded source collection contains 67 files, 333,068 bytes. All are recorded
  as matching pinned git contents; there are no missing-path or cap entries.
- Comparator was not inspected or controlled. This run produces no new
  independent kernel-check result.

## 1. The local geometry-domain boundary is now explicit

Lean accepted five propositions in DomainBoundary.lean. Suppressing the lengthy
dependent parameters, the main equivalence is:

```text
Nonempty (OAt Γ t X) ↔ Γ D J X ∧ LamAre t.r.Z X
```

The D and J here are exactly the underlying objects selected by t and its
context, as specified in the source and printed theorem, not independently
chosen replacements. The specializations establish:

```text
Nonempty (OAt anyGeometry t X) ↔ LamAre t.r.Z X
¬ Nonempty (OAt False t X)
¬ GeoCl False D J X
¬ Nonempty (OAt (geoCl False) t X)
```

All five axiom reports list only propext, Classical.choice and Quot.sound.
The end marker and zero exit status occur after all five commands.

**Interpretation:** the earlier successful supplier specialization to False
cannot be read as construction of an OAt object satisfying False. This local
object type has no inhabitants. Conversely, anyGeometry removes only the Γ
field's restriction: LamAre remains necessary and sufficient for this record's
inhabitance at the fixed other parameters.

This does not establish that LamAre is nontrivial at the particular points, that
all enclosing domains are empty, or that the original headline proof uses an
empty domain. It does not show geometry irrelevant to RH. The new theorems
clarify the scope of the v0.2 abstraction result.

Evidence: DomainBoundary.lean; domains.log, with axiom reports at lines 3500,
6972, 7030, 7157 and 7236, and terminal marker at 7237.

## 2. The comparison properties have specific local uses

The compiled declaration for `GlobalTheory.T.class_sum_divisor_all_alt` is a
wrapper around `GlobalTheory.GeoTies.linked_ties_alt`. The newly collected
ThirdPlaceSeries/LinkedTies.lean shows two distinct suppliers near its end:

- `class_sum_divisibility_of_extensionWithLaw` supplies the class-sum obligation,
  using the relevant divisor premise in the subsequent application.
- `ties_of_tiesB_alt` supplies CompatibilityConditions using TiesB, a recursion
  condition, a realised-point result and a twisting condition.

The separate comparison-existence wrapper
`linkedAt_tie_of_nonempty_extensionWithLaw` resolves to `GlobalTheory.Fc.RL.at_tie_alt`.
Its full construction is still a follow-up target.

On the consumer side:

1. `pNmj_of_pDiv_of_classSumPin_alt` passes hpin, its ClassSumPin argument, to
   `lattice_family_adoption_fourth_alt` alongside the divisor and normalization
   premises. The collected statement wrapper identifies the latter's underlying
   implementation as `GlobalTheory.BigTop.PtAt.nmjT_at_tied_alt`.
2. `pRows_of_parts_alt` constructs a RowPointSummands record and assigns its
   compatibility proof hT to `ties := hT`.

The second observation is particularly important for use classification:
**being stored in a proof field is an identifiable use, but is not by itself
proof that a later mathematical conclusion depends indispensably on that field.**
We have not traced every later projection or established erasure/necessity.
Likewise, passing hpin to a consumer does not establish that all downstream
bodies need it after reduction.

Evidence: witness-chain.log blocks 3–85, 1473–1863 and 1864–3870;
collected-source/.../ThirdPlaceSeries/LinkedTies.lean lines 74–76;
PNmjOfPDivOfClassSumPin.lean lines 15–16; PRowsOfParts.lean line 36;
NmjTAtTiedStatement.lean.

## 3. The height chain has explicit premises and a nonemptiness requirement

The collected HodgeBundleWeights/GeometricOfHyp.lean proves
`geometric_height_bound_at_place` by combining domain/lattice regularity,
birationality and a proportionality result, followed by a degree inequality.
At this layer it is not a body that simply supplies True.intro.
This observation does not certify the mathematical adequacy of its nested
objects, predicates or supporting theorems.

`heightAt_eq_of_cover` explicitly takes:

```text
hne : Nonempty (Comp Y.d.Xo₂ Y.d.c₂)
```

Its proof obtains an object Z from hne and uses a short-generation premise at Z
to establish `1 ≤ abelian₂`. This is a concrete use of a nonemptiness premise in
this height lemma. The upstream height supplier passes a component of the
GoodCov/deep-goodness data into this argument. Whether that upstream data
constructs the intended mathematical object remains to be reviewed.

The proof also passes the components of hGe to `slope_le_height`, together with
other estimates. Thus the inspected height layer carries explicit geometric
and numerical obligations. It does not establish the missing identification
between an arbitrary assigned record height and an independently specified
intrinsic height.

One further source observation narrows the next target:
`cover_height_comparison` accepts PublishedHodgeBundleTheorems, but its displayed
wrapper body ignores that argument and returns `GlobalTheory.CovHt.FrameCmp.htCmp`.
Both the collected source and compiled rendering agree. An unused wrapper
premise is not an error: the underlying theorem may already be available without
it. The next audit target is the actual htCmp construction and the HTCmp
predicate, rather than assuming that the wrapper's premise explains the comparison.

Evidence: collected-source/.../HodgeBundleWeights/GeometricOfHyp.lean lines 48–56;
HeightAddLogNonneg.lean, especially the hne argument and its elimination;
CoverHeightComparison.lean lines 33–35; height-chain.log lines 6432–6459.

## 4. Rendering and scope limits

The logs contain visible elisions: 115 in domains, 67 in witness-chain, and 182
in height-chain. The block indexes identify their locations. Source snapshots
resolve the specific applications discussed above, but these are not complete
raw-expression exports. Even a block with no visible elision is not certified
complete solely by that fact.

The five local domain theorems were compiled against imported Main. The eleven
chain targets were printed and had their axiom dependencies queried; this does
not constitute independent rechecking of their stored proof bodies. The reported
axiom lists contain only the three standard axioms above.

These named cases are not a random or preregistered representative sample of
the census. Daniel Fairbanks's second control, origin/instance strata, full
unknown accounting, larger-budget LedPart.pt classification, and fixed sample-use
review remain outstanding. This report does not complete Stage 3.

## Next discriminating targets

1. Trace the original anyGeometry route's actual inhabitance and linkage
   construction, including `GlobalTheory.Fc.RL.at_tie_alt`. Do not infer this
   from the False-domain experiment.
2. Follow ClassSumPin into `nmjT_at_tied_alt`, and follow the constructed record's
   ties field into an actual downstream consumer. Separate storage, forwarding
   and mathematical use.
3. Inspect `GlobalTheory.CovHt.FrameCmp.htCmp` and HTCmp, and trace the source of
   the explicit nonemptiness premise and the required height comparison.
4. Complete the separately specified census controls and unknown/sample analyses.

**Publication-safe conclusion:** the new run proves the exact local boundary
between a geometry predicate and the objects carrying its proof, and identifies
additional uses of comparison and height premises. It supplies neither a
refutation of the critics nor a finding that the RH/GRH formalization is flawed.
