# Stage 4 v0.5: supplied height-bound arguments

Prepared 2026-11-23, before running this probe against Harry's compiled project.
The source was inspected before selecting targets. This is a targeted follow-up,
not a blind sample or a preregistered statistical test.

## Question

At the stored applications constructing `Formalism.L2.DIV.WordFacts`, which
proof terms supply the lower bound `c2`, upper bound `c3`, and assigned-height
identity `tH`? What premises remain in their local context?

The source has a conditional lower bound: a nonzero-map premise is essential
to the statement. The probe must retain it. A conditional bound is not evidence
that the premise has been satisfied at a particular headline instantiation.

## Fixed targets

All names below have prefix `Formalism.L2.DIV.`.

| Stored caller | Watched callee | Arguments recorded | Comparison of sides |
| --- | --- | --- | --- |
| wordFacts_of_clauses | wordFacts_of | c2, c3, tH, tR | all four |
| wordFacts_of_face | wordFacts_of_clauses | hcl, tH, tR | tH, tR |
| wordFacts_of_tied | wordFacts_of_face | hcl, tH, tR | tH, tR |
| DivisionPackage.wordFacts | wordFacts_of_tied | hcl, tH, tR | tH, tR |
| DivisionPackageFace.wordFacts | wordFacts_of_face | hcl, tH, tR | tH, tR |

Expected coverage: five first-call observations, 16 supplied arguments, and
12 comparison records. `hcl` is recorded without pretending that its conjunction
is a single comparison. Its argument expression and referenced constants are
evidence for the next supplier to inspect.

## Method and bounds

Import the pinned `Main`; inspect stored theorem/definition/opaque bodies.
Walk maximal applications, lambda bodies and local let bodies/values, entering
their local contexts. Exclude binder annotations as call evidence. Skip a
subtree only when its expression contains no reference to the watched callee.
Stop at the first watched application in each caller, with the v0.4 order:
last argument first; let body before let value. Do not expand callee bodies.

Read the callee's dependent telescope in argument order. Instantiate earlier
parameters with the actual supplied expressions before recording each selected
argument's expected type. Enter all forall binders in a selected comparison
type, record them, and compare the resulting two sides under transparency `all`.
Propositional assumptions are not rewritten into those sides.

Record the argument's expression, outer syntactic shape, expected type, local
context, and constant references. Shape labels describe syntax only: a local
reference is not a missing proof, and a lambda is not evidence of necessity.
Pretty printing is capped at 24,000 characters per argument, 6,000 per other
expression, and 256 constant references. Each cap is visible. A completed
collection with truncated fields may still need a focused follow-up to read
those fields in full.

Limits inherited from v0.4: 250,000 expression visits and depth 600 per caller;
10,000,000 raw heartbeats per Meta action; 2 CPUs, 100 GiB RAM, 30-minute project
wall guard; 64 MiB log cap. No project writes or Comparator control. Keep the
existing 20 GiB disk reserve plus 1 GiB output allowance. Source collection is
bounded to five named files, at most 10 MiB total.

## Controls and failure handling

Run the existing expected-type-error control and v0.4 comparison fixture first.
Run a new fixture through the same argument scanner before importing Main.
It checks dependent argument substitution, forwarded versus constructed terms,
a retained nonzero premise, equal and different sides, local lets, an absent
callee, and a requested parameter that does not exist.

Any failed fixture stops the project phase. Exceptions, missing parameters,
absent calls, incomplete scans, and non-comparison/unknown results remain
coverage problems. No fallback invents a result. Preserve the first error and
evidence archive. The source snapshots and input hashes are checked against the
existing pins before and after the project phase.

## Interpretation

1. A successful recorded application establishes that these expressions occur
   as supplied arguments in this stored wrapper. It does not establish their
   ultimate specialization in the five headline proofs.
2. Identical sides establish definitional reflexivity at the inspected context.
   This alone neither invalidates the theorem nor shows that another bound is
   vacuous.
3. Different sides establish only nonidentity under the specified reduction.
   They do not establish a useful numerical bound, nonvacuity, necessity, or
   correctness of a mathematical interpretation.
4. A supplied local hypothesis or record projection is an obligation to trace
   upstream, not a Lean compilation error or evidence that no witness exists.
5. The probe makes no new RH/GRH, necessity, or Comparator verdict.

## Decision after the run

Read the `c2`/`c3` arguments and their retained premises first. Then inspect the
two `hcl` suppliers in the package wrappers. Use the actual references to select
the next concrete supplier; do not repeat a broad closure census. Resolve any
missing/truncated evidence before drawing a claim-level conclusion.
