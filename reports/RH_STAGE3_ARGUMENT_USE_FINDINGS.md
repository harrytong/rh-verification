# Stage 3.4 findings: argument occurrences and class-sum use

Prepared 23 November 2026 from the uploaded v0.5 evidence. This report reviews
recorded server output and pinned source snapshots; it is not an independent
rerun of Lean or the proof checkers.

**Conclusion:** the targeted collection succeeded. The newly retrieved class-sum
implementation contains a concrete use of its class-sum hypothesis in a rewrite.
This extends the earlier finding of forwarding into a certificate. However,
79 of 113 bounded argument scans were truncated, including the scans of that
hypothesis. Their zero counts cannot establish non-use. The completed scans
identify explicit argument occurrences in the point-condition consumer and
covolume supplier, without establishing necessity of anyGeometry, its geometric
meaning, or a verdict on the complete RH/GRH proof.

## 1. Run and integrity

Server directory:
`/home/harry/rh-verification/critics-audit-stage3/stage3-mc73ncns`

Run: **23 November 2026, 03:17:40–03:20:03 EST**.
The project Lean process took **2 minutes 11.96 seconds**, exit 0, with maximum
RSS **49.68 GiB**. The process statistics describe this probe, not total system
memory or Comparator memory.

Evidence ZIP SHA-256:

```
16cfdf5e833e65b032fb1caf0a6187f8b08357ffa8e523ed5daef992b6d5e699
```

Verified from the supplied bytes:

* All 250 files listed in EVIDENCE_SHA256SUMS match their hashes.
* All 72 package files listed in SHA256SUMS match both the evidence archive
  and the original delivered v0.5 package.
* The recorded use-protocol, target-configuration and package-manifest hashes
  agree with the corresponding files.
* The recorded selected-input hashes before and after the run are identical.
* Reconstructing the occurrence, provenance, declaration-block and use-fixture
  JSON outputs from the logs reproduces the supplied files exactly.

Positive, provenance and argument fixtures completed with exit 0. The negative
fixture returned the intended type error, True.intro where False was expected.
The argument fixture covered 12 synthetic traversal cases plus stored-theorem
extraction and the two outer-prefix caps. These validate specified tool behavior;
they are not an RH check.

The project probe completed with exit 0. All ten printed axiom lists contain
only propext, Classical.choice and Quot.sound. This repeats a declaration-level
inspection; it is not a new independent-kernel result. No Comparator completion
record is included in this archive.

## 2. Completeness matters

There are **113 explicit outer-lambda binder scans** across ten targets:
**34 complete; 79 truncated**. Every truncated record reports 100,000 visited
nodes, the preregistered node limit. All ten prefix scans stopped at a
non-lambda head; none reported the outer-step or binder-count cap.

| Target (abbreviated) | Binders | Complete scans | Truncated scans |
|---|---:|---:|---:|
| BigTop.PtAt.nmjT_at_tied_alt | 21 | 0 | 21 |
| ClassSumLift.eM_eq_thPe_alt | 33 | 0 | 33 |
| Fc.Ind.evWC_onPt_of_guarded_alt | 9 | 9 | 0 |
| Fc.Ind.eventual_L3_of_covolume_alt | 6 | 0 | 6 |
| Fc.TieOfLink.hasTie_of_linked | 3 | 0 | 3 |
| SelfIntersectionVolumeEstimates.topCovolG_alt_alt | 7 | 7 | 0 |
| CovTop.CovolumeBoundOfX | 0 | 0 | 0 |
| CovHt.FrameCmp.htCmp | 16 | 0 | 16 |
| CompHt.recVals | 9 | 9 | 0 |
| CompHt.htVals | 9 | 9 | 0 |

Except SelfIntersectionVolumeEstimates, these abbreviations have the prefix
GlobalTheory. Zero binders for CovolumeBoundOfX means no explicit outer lambda
was exposed in its stored body; it does not mean that the definition lacks
conditions or dependencies.

The scanner labels occurrences inside lambda/forall domains or let types as
`binder_or_let_type_position`, and all other positions as
`other_expression_position`. The latter includes proof arguments, implicit
arguments, types passed as arguments, and possibly discarded let values.
It does not by itself identify a necessary or computationally relevant use.

In particular, hPin in nmjT_at_tied_alt and hP in eM_eq_thPe_alt both have zero
observed counts **with truncated=true**. Those records are inconclusive, not
absence findings. The source use described below demonstrates why treating
these zero counts as absence would be wrong.

The separate direct-reference collection has 2,269 summed type/body reference
entries, no reference-limit truncations and no missing referenced declarations.
These entries are not 2,269 unique global declarations. Source collection copied
160 files (1,364,591 bytes); 438 additional queued paths have file-count-cap
status. All ten target owners were collected. Printed output contains 352
elision indicators, so rendered terms must not be presented as complete.

## 3. Concrete new finding: the class-sum hypothesis is used locally

All source paths below are relative to collected-source/ in the evidence ZIP.
For this section, the common directory is:

`Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/`

The recorded source chain is:

| Location | Observation |
|---|---|
| NmjTAtTied.lean, theorem nmjT_at_tied_alt | Forwards hPin to lattice_family_adoption_third_alt; stores the result in eMj_th of its returned certificate. |
| EMEqThPeStatement.lean, reviewed in v0.4 | The wrapper delegates to GlobalTheory.ClassSumLift.eM_eq_thPe_alt. |
| EMEqThPe.lean, lines 90–94 | eM_eq_thPe_alt introduces hP and passes it to GlobalTheory.ClassSumLift.at_index_alt. |
| EMEqThPe.lean, lines 50–87 | at_index_alt accepts hP : IndefiniteClassSumCondition B.Q and applies it at line 76 to rewrite the goal. |

The crucial source expression is:

```lean
rw [hP w i h1 h2 _ ht hw c x e1 hx y e2 n a f e3]
```

The subsequent proof applies hsum, uses injectivity, and supplies the agreement
condition hjD. Compiled direct-body references for eM_eq_thPe_alt include
GlobalTheory.ClassSumLift.at_index_alt, consistent with the retrieved source.
The at_index_alt body was read from the git-verified source; it was not a
separate argument-scan target in v0.5.

ClassSumPinT.lean, lines 22–35, defines IndefiniteClassSumCondition as a
universally quantified, conditional equality between a theta expression and a
finite tensor sum. Its source is not simply `:= True`. That observation does
not establish that it is nontrivial after all definitions and particular
parameters are instantiated, nor that its quantified domains are inhabited.

**Supported statement:** this particular source proof applies a class-sum
hypothesis as an equality rewrite. It is more than a name merely appearing in
a reference closure.

**Not supported:** that anyGeometry itself is necessary; that its use faithfully
encodes the intended geometry; that this equality cannot be obtained another
way; or that the entire headline proof has now been audited. The provenance
and supplier of this hypothesis at the relevant headline instantiation still
matter. hP here is a local parameter name, not a global identifier for a single
hypothesis throughout the project.

## 4. Completed consumer scans

### Point-condition consumer

GlobalTheory.Fc.Ind.evWC_onPt_of_guarded_alt has nine completed scans. Its h,
hd, hR and hG parameters each have **one other-position occurrence and zero
annotation-position occurrences**.

In EvWCOnPtOfGuarded.lean, lines 23–32, the proof combines h', hR and hG,
extracts eventual witnesses, and passes the resulting point-condition proof
`hb x hx e2 i` to the supplied implication ha. This is concrete forwarding of
a proof satisfying a downstream premise. It does not identify the ties field
as necessary: the receiving implication and its provider determine which
parts of the record are used.

### Covolume supplier

SelfIntersectionVolumeEstimates.topCovolG_alt_alt has seven completed scans:

| Parameter | Annotation-position occurrences | Other-position occurrences |
|---|---:|---:|
| hSB | 0 | 1 |
| hX | 0 | 9 |
| hP | 0 | 19 |
| hH | 0 | 2 |
| hGD | 0 | 8 |
| hQ | 0 | 8 |
| hD | 0 | 1 |

TopCovolG.lean, lines 39–58, constructs the bound through covering, height,
lower-bound and truncation lemmas. Thus none of these seven parameters is
syntactically absent from the inspected stored body. The counts are syntactic
occurrences, not counts of independent mathematical arguments or evidence
that each parameter is indispensable. No proof reduction or ablation was run.

### Valuation definitions and height comparison

GlobalTheory.CompHt.recVals and GlobalTheory.CompHt.htVals each have nine
completed binder scans. Their geometric/data parameters occur in their stored
bodies. The latter is built from htValSet and a valuation proof.

In Definitions/Divisors/IsLatBasisHtLatIffSpanEq.lean, lines 477–489, htValSet
requires existential prime, algebra, frame, comparison and valuation data.
This makes the actual domain explicit. It does not prove nonemptiness at the
headline instantiation or identify it with every intended geometric valuation.

All sixteen scans of GlobalTheory.CovHt.FrameCmp.htCmp were truncated. The
previous source review of its comparison construction remains useful, but
v0.5 supplies no complete argument-use census for that theorem.

## 5. What to investigate next

1. Trace the provider of IndefiniteClassSumCondition at the actual selected
   headline route, through the geometry closure and the relevant instantiation.
   The consumer now has an identified rewrite; the provider and domain are the
   important remaining questions.
2. For selected arguments such as hPin/hP, use a narrowly targeted traversal
   that avoids spending the entire budget in unrelated annotations, with
   separate accounting for skipped regions. Preserve unknown results rather
   than silently treating budget exhaustion as absence. Any improved scanner
   needs fixtures before use. Inspect the enclosing applications, not just
   occurrence totals.
3. Trace which part of PointConditions' the covolume argument requires,
   particularly ties, and determine whether the relevant domains are populated.
4. Continue the separate preregistered census work requested by Daniel:
   second control, project/library/instance/generated strata, every unknown's
   reason and budget, a larger-budget LedPart.pt probe, and frozen per-category
   samples classified by actual witness discharge versus incidental presence.

These are targeted audit results. They neither demonstrate that the claimed
RH/GRH proof is flawed nor settle the critics' allegations in the author's
favor. Comparator status remains a separate, unfinished question in the
available record.
