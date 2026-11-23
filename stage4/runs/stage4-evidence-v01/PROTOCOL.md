# Stage 4: testing the critics' claims

Version 0.1. Protocol fixed before the first Stage 4 project run. The runner records
this file's SHA-256 and the run's UTC timestamp. This is prospective registration
for this package, not a claim of independent registration or independent review.

## Question and correction

Does the height comparison identified in the criticism become a comparison of
definitionally identical expressions in the submitted proof?

Our earlier inability to locate a provider was not evidence that a proof omitted
a witness. We withdraw that inference. Lean accepts proofs of propositions under
their actual types and hypotheses. An assumed premise is not an unfulfilled goal;
a conditional theorem must not be reported as an unconditional theorem.

This stage tests a specific inference attributed to Nielsen and repeated in
discussion of Chu's review: assigned height and copied data allegedly make the
important height inequality reflexive. It does not presume that every height
inequality in the project is the inequality the critic intended.

## Claim ledger

| Claim | Test / status in this package |
| --- | --- |
| `anyGeometry` is constantly True and occurs on the reported route | Prior audit question; not retested here. Truth and reachability alone do not establish invalidity. |
| The constructed object's height is assigned by definition | Positive project control: prove `p.pt.D.div.h u = p.ht u` by `rfl`. This concerns the constructed object, not arbitrary original data. |
| The substantive comparison therefore has identical sides | New test: compare sides of three named inequalities and two immediate stored call-site instances. Keep all local parameters and hypotheses. |
| The final theorem has only the type `RiemannHypothesis = RiemannHypothesis` | Compile `example : RiemannHypothesis := riemannHypothesis` and print its type, definition and axioms. A successful example refutes that literal type claim in the imported environment. It does not independently compare the imported definitions with a protected challenge. |
| These findings invalidate the intended RH/GRH theorem | Not inferred from any local comparison result. Requires an actual defect in the statement correspondence, assumptions or verification chain. |

Attribution pointers, not archived primary documents:

- Nielsen publication listing: https://philpeople.org/profiles/jenny-lorraine-nielsen/publications?order=added
- Chu review: https://dev.to/frankchu/grh-proofs-geometry-is-fun-true-in-24-files-2n2b

These URLs are mutable. This package does not establish a paper version number or
contain a fresh independent review of those pages. Its target is the specific
reflexive-comparison allegation discussed in our audit.

## Fixed targets

Generic conclusions, with all outer binders instantiated by fresh rigid local
variables:

1. `GlobalTheory.CovHt.HtTopG.slope_le_height`
2. `GlobalTheory.CovHt.HtTopG.height_add_log_nonneg`
3. `GlobalTheory.CovHt.FrameCmp.val_le`

Immediate application sites, in original stored proof bodies:

1. `heightAt_eq_of_cover` calling `slope_le_height` (both in `GlobalTheory.CovHt.HtTopG`).
2. `GlobalTheory.CovHt.FrameCmp.htCmp` calling `GlobalTheory.CovHt.FrameCmp.val_le`.

The first owner is also scanned for `le_refl` and `le_rfl` applications, to separate
auxiliary reflexive premises from the main inequality. Absence of those names
is not absence of every possible encoding of reflexivity.

Selection rationale: the preserved source has an explicit height/slope inequality,
an immediate call supplying a reflexive auxiliary log bound, and a separate
valuation comparison used by `htCmp`. These are concrete, plausible candidates.
The exact comparison intended by the paper still needs to be matched to a result.

## Method

- Read the pinned compiled environment. Add audit examples only in a separate
  imported module. Never edit project declarations or replace proof terms.
- For generic conclusions, enter the actual syntactic forall binders with fresh
  free variables. Do not use hypotheses as rewriting rules.
- For application sites, enter lambda and let binders with their real contexts.
  Infer the type of each maximal application of a watched constant. This preserves
  that application's supplied arguments; it is not a generic theorem reprint.
- Recognize direct Eq/LE/LT applications before reducing away relation instances.
  Try reducible weak-head normalization only when a direct relation is absent.
  Other shapes remain `not-a-direct-comparison`, not a negative result.
- Compare the last two relation arguments with `isDefEq` under transparency `all`.
  Metavariables, exceptions and resource bounds produce unresolved outcomes.
- Record sides, local types and let values. Pretty-printed text is capped at 6,000
  characters per field with explicit truncation flags. Computations use the full
  expressions. Human review must account for any printed elisions/truncations.
- Only selected proof bodies are scanned. No callee body expansion, theorem proof
  minimization, transitive specialization from RH, or graph-wide census occurs.
  A local let may be used in reduction even if its body contains other declarations.

## Controls and bounds

Before any Main import, the same helper must distinguish:

- equal sides;
- different sides with an inequality hypothesis;
- different sides with an equality hypothesis (hypotheses are not substitution);
- a fully applied theorem with equal arguments;
- a fully applied theorem with different arguments;
- a let-bound definitionally equal argument.

A separate invalid `False := True.intro` example must fail with the expected type
error, not a startup error or timeout. Controls run without the project mount.

Per owner/action: 10,000,000 raw Core heartbeat units, recursion limit 2,000.
Per proof-body scan: 250,000 visited expression nodes, depth 600, 64 matched calls.
These are bounds on the new inspection code, not counts of distinct declarations.
Core heartbeat budget is shared across comparisons in each owner/action, not a
wall-clock budget per comparison. An exception preserves earlier emitted records
and marks the owner unresolved. Errors are preserved verbatim; no unsupported
automatic distinction between timeout and mathematical failure is made.

Container: two logical CPUs; 4 GiB/180 seconds for controls; 100 GiB/1,800 seconds
for the project. Logs cap at 64 MiB each. At least 116 GiB available host RAM and
21 GiB free disk are required for the project step. No Comparator commands run.

## Interpretation fixed in advance

| Output | Permitted conclusion | Prohibited inference |
| --- | --- | --- |
| definitionally-identical, Eq or LE | The two sides coincide by definitional reduction at this recorded boundary/instance. | That RH is false, the entire proof is vacuous, or this occurrence is indispensable. |
| not-definitionally-identical | The sides do not coincide under this definitional-equality check at these local parameters. | That the proposition is unprovable, that no later specialization makes the sides identical, that it is mathematically deep, or that all criticism is refuted. |
| LT with identical sides | Record the result for manual investigation; strict order is not discharged by reflexivity. | That an inequality proof has automatically succeeded. |
| missing/partial call, unsupported shape, exception or cap | Unresolved coverage. | Treating the case as absent, nonreflexive, or proof failure. |

Each conclusion is local to the recorded comparison. The actual paper target
must not be confused with any other inequality. Except for the assigned-height
positive control, this package compares expressions; it does not attempt to
replace the theorem's proof with `rfl` or `le_rfl`. The actual paper target
must be identified before a critic's assertion is labelled supported or refuted.
If these are not that target, ask for its fully qualified declaration and exact
application site. Do not start another unrestricted supplier trace.

## What would settle the larger dispute?

Facts about True predicates and copied fields can be correct without invalidating
a sound proof of an independently matched final statement. To substantiate the
strong invalidity claim, show a concrete mismatch in that statement or its
dependencies/assumptions, or a reproducible verification defect. To refute a
particular code allegation, show the exact targeted compiled expression contradicts
it. A local nonreflexive inequality cannot refute every possible objection.

Daniel's requests for additional controls, exhaustive unknown reporting and
preselected witness-use sampling remain separate pending work; this small stage
does not claim to complete them. It incorporates his distinction between use and
presence by examining actual applications, with no inference of necessity.
