# RH / Dirichlet-GRH verification and critics’ audit

**Maintainer: Harry Tong. Updated 26 November 2026, 18:54 EST.**

This repository records a local rebuild, proof export, independent Nanoda check,
and four stages of AI-assisted investigation of objections to the published
Lean formalization associated with Levent Alpöge. The five audited statements
concern RH and Dirichlet L-functions; “GRH” here is not a claim about every
possible generalized L-function.

**Current conclusion:** the audit confirmed several constructions highlighted
by the critics and traced explicit conditions, witnesses, and bound proofs
surrounding them. We found no formal proof defect in the inspected routes.
Those observations alone do not establish invalidity of the headline theorems.
Broader semantic objections remain unresolved. **The tuned standalone Lean
paranoid replay passed. Harry’s protected Comparator has accepted the solution
through Lean paranoid and nanoda; its Lean default-kernel stage is still running.
The overall Comparator verdict remains pending as of 26 November, 18:54 EST.**

Stage 4 is **closed within its selected scope**. We rely on the recorded formal
checking for upstream proof obligations; we do not interpret a premise of a
helper theorem as evidence of a missing witness. This stopping decision is not
a new proof of semantic equivalence or a global refutation of the critics.

## Latest verification update — 26 November 2026

The standalone Lean paranoid replay with `MIMALLOC_GENERIC_COLLECT=1000000`
finished successfully in **21:43:05**, with checker, Docker and logging exit
codes all zero. Peak checker RSS was **98.8 GiB**; peak container memory was
**109.8 GiB**, below its 120 GiB limit, with no recorded OOM events or kills.

**Tuning credit:** Andrew Sutherland (MIT) documented this allocator setting in
his [RH verification record](https://math.mit.edu/~drew/grh/). Harry applied that
setting locally to the stock Lean 4.36.0 paranoid checker. This is a local
reproduction of the documented tuning, not a new verification algorithm or
an independently implemented kernel.

The original Comparator remains active: paranoid and nanoda acceptance are
recorded; the default-kernel stage has run for 24:03:08 at the supplied snapshot.
The separate tuned pass does not complete or replace that Comparator run.
See the [dated report](reports/VERIFICATION_UPDATE_20261126.md), including
provenance, exact counters and the supplied terminal excerpt.

## Start here

- [Closing assessment and claim-by-claim recap](reports/CLOSING_ASSESSMENT.md)
- [All stages, code versions, runs, and evidence archives](INDEX.md)
- [Verification history, provenance, and evidence gaps](VERIFICATION_STATUS.md)
- [Stage 1 dependency findings](stage1/code/RH_critics_dependency_findings.md)
- [Stage 2 census and control comparison](stage2/runs/rh-stage2-semantic-evidence/semantic-census-comparison.md)
- [Stage 3 findings](INDEX.md#stage-3)
- [Stage 4 final recorded collection](stage4/runs/stage4-evidence-v07/CLAIM_RESULTS.json)
- [Scope, unfinished work, and reproduction notes](SCOPE_AND_REPRODUCTION.md)

Stages 1–4 are published directly at the repository root in `stage1/`,
`stage2/`, `stage3/` and `stage4/`. Reports, publication metadata and terminal
excerpts are alongside them. Earlier reports describe what was known at their
writing time; use this README and the closing assessment for the current interpretation. Historical “next target” sections do not
override the decision to close Stage 4.

## Recorded verification status

| Check | Recorded outcome | Limit of the result |
| --- | --- | --- |
| `lake build Main` | Successful; 183,893 jobs reported | Jobs include reused work; this is not a count of newly proved theorems |
| Headline statement / axiom inspection | Five declarations; only `propext`, `Classical.choice`, `Quot.sound` reported | In the imported environment, not independently compared with the protected challenge |
| Proof export | 61,570,595,788 bytes; checksum matched the published value in the recorded run | Byte agreement alone is not a proof check |
| Standalone Nanoda | 1,484,733 declarations; no typechecker errors; exit 0; 1:03:30 elapsed | Also reported one pretty-printer error, “Unable to print axioms” |
| Protected Comparator | Lean paranoid and nanoda accepted; Lean default kernel running at 18:54 EST on 26 November | Overall statement-comparison / axiom-check verdict still pending |
| Tuned standalone Lean paranoid replay | Exit 0; 21:43:05; 98.8 GiB peak checker RSS | Same stock checker with Sutherland’s allocator setting; not a full Comparator verdict |
| Stage 1 | Stored dependency traversal completed | Reachability is not necessity or a kernel replay |
| Stage 2 | Statement, transport and bounded semantic-census results recorded | Census classes are candidates for inspection, not defects |
| Stage 3 | Targeted geometry, height, theta, descent and realization probes recorded through v0.13 | v0.14 code is archived, but no corresponding completed run was supplied |
| Stage 4 | Final v0.7 selected coverage complete: 14 arguments, 9 comparisons, 13 declaration records | Bounded parameterized constructor/helper inspection, not all headline applications |

Build, export and Nanoda numbers above come from Harry’s supplied terminal
record. The upload helper adds available original server logs separately;
the assembly does not fabricate missing full logs or a Comparator outcome.

## What the audit established

1. **The controversial definitions really occur.** `anyGeometry` is `True`;
   it and selected degenerate-model declarations occur in the five stored
   reference closures. Four named extraction lemmas and the older named
   `hypsE₂` / `everyE₂` / `plugAll` route are absent from those closures at the
   pinned revision. Absence of a name does not rule out an inlined or different
   argument, and the newer route still includes `anyGeometry`.
2. **One trivial predicate does not make the whole package trivial.** Local
   domain probes retain `LamAre`; compatibility and class-sum conditions have
   identifiable suppliers and consumers. One supplier generalized to arbitrary
   predicates. Its `False` instance has an empty local object domain and must
   not be advertised as an RH proof with false geometry.
3. **Fallbacks have conditions.** The inspected weak-to-strong theta conversion
   consumes explicit existence witnesses. The theta interface requires
   integrability and equality to an integral. Particular zero/unit fallback
   branches have explicit case reasoning. These observations do not prove
   nonzeroness or semantic adequacy everywhere.
4. **Height assignment and height bounds are distinct.** The assigned-height
   equality can hold by `rfl`. Selected consumers additionally use bounds, and
   the inspected division-clause construction derives estimates before using
   `R.divIneq`. v0.7 traces `hTie_of` and `rhs_le_record` through generated proof
   helpers. Their premises remain explicit.
5. **No inspected missing-proof defect was found.** A helper accepting `hh` or
   an existence field is normal proof composition. We withdraw the unsupported
   suggestion that Lean simply overlooked an unconstructed witness.

Negative definitional-equality tests are not proofs of mathematical inequality,
nonvacuity, or nontriviality after every concrete specialization. Likewise,
finding a reflexive step is not evidence that a closed headline theorem is
invalid. The exact statement, assumptions and verification premises matter.

## Census: candidates, not a defect count

The headline closure census attempted 214,234 definitions: 213,831 completed
and 403 unknown. Among completed definitions, 294 had a True-predicate hit,
600 had a unit-typed-constructor-field hit, 130 a zero-linear-map hit, and 9 a
zero-measure hit. **These four figures count definitions with at least one hit,
not the total number of fields or expression occurrences. Categories overlap.**

The same classifier’s control completed 5,768 definitions with 3 unknown;
the corresponding hit counts were 25 / 5 / 6 / 2. The control closure is much
smaller and is not a random sample. Library instances and ordinary constructions
can legitimately contribute to these categories. Full method and denominators
are preserved with the census.

Daniel Fairbanks’ requests for a second control, fuller instance/non-instance
breakdowns, a fixed witness-use sample, and complete accounting/retries of
unknowns are not all completed by the later named-case probes. His comments
were review of recorded material, not an independent rerun or endorsement of
the whole proof. See the scope document.

## Provenance and tools

- Project revision: `753431bfe28701f6f3937f664fcaf08daa139c03`
- Mathlib revision: `0df444a360eaa60ab8c11dca51a86af692955474`
- Project audit toolchain: Lean 4.33.1; separate judging toolchain: Lean 4.36.0.
- [Artifact hashes and verification record](VERIFICATION_STATUS.md)

Harry executed the large Lean runs on his Ubuntu server. AI assistance was
used to write probes and analyze supplied logs and sources. Reviewing those
records is not an independent reproduction on another machine. Checksums
establish byte consistency, not independent authentication of execution.

The archive includes runnable Python, Lean sources and templates, protocols,
tests, generated probes, logs, JSON records, source snapshots, historical
reports and original evidence ZIPs. `phase_completed` and `coverage_complete`
are different. Failed fixtures and capped searches remain visible.

## Review and reuse

For a correction, cite the pinned revision, fully qualified declaration,
concrete application and relevant evidence file. In particular, identify the
exact instantiated inequality if claiming that it collapses to reflexivity.

Original source snapshots retain their upstream ownership and licensing.
This repository does not assign a new license to third-party Lean/Mathlib
material or claim authorship of the RH proof. Audit fixtures are isolated
tests; intentional negative fixtures are not part of the RH theorem environment.
