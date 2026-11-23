# Stage 3.4 targeted argument occurrences: preregistered protocol

Prepared 2026-11-23 before the v0.5 project run. This protocol supplements,
and does not replace, Daniel Fairbanks's requested census/control/unknown work.
The runner records this file's hash before any server probe.

## Question and frozen selection

Follow the concrete hPin forwarding observed in NmjTAtTied to
GlobalTheory.ClassSumLift.eM_eq_thPe_alt, and the RowPointSummands route to
its actual consumer and covolume supplier. Inspect height valuation domains
alongside FrameCmp.htCmp. The exact ten ordered targets and budgets are in
use-targets.json. Selection is purposive, not a statistical sample.

The selected topCovolG_alt_alt is a supplier of CovolumeBoundOfX. Its inclusion
does not establish that this particular supplier is necessary in every headline
proof. The receiving class-sum declaration's implementation is not yet available
in our collected source; compiled provenance will locate its owning module.

## Method

For each target obtain the stored definition, theorem or opaque body. Peel its
explicit outer lambda prefix, skipping metadata only. For each lambda, count
references to that binder's de Bruijn index in its remaining body. Increment the
index under nested lambda, forall and let bodies; do not increment it in their
domains, let types or let values.

Two purely syntactic locations are recorded:

1. binder_or_let_type_position: within a lambda/forall domain or a let type,
   including subexpressions nested anywhere within that annotation;
2. other_expression_position: every other occurrence in that remainder.

The second label includes implicit arguments, arguments that themselves are
propositions/types, discarded let values, and proof terms. It is NOT a
classification as a witness discharging a hypothesis, computational use, or
semantic necessity. Forall codomains inherit their surrounding label. We do
not infer types, unfold constants, reduce terms, normalize proofs, remove
arguments, or claim all function binders have been exposed. Peeling stops at
a non-lambda head, including a let or an application. No eta expansion occurs.

Each binder scan has 100,000 visited expression nodes and depth limit 600.
At most 128 binders and 256 outer steps are inspected per declaration.
Exhaustion produces explicit truncation/cap records. DAG sharing is visited
by syntactic occurrence, not deduplicated by memory identity. Bound counts
are per inspection, not counts of unique mathematical uses.

For a complete scan, zero means only that this binder has no syntactic
occurrence in the scanned remainder. Positive annotation-only counts are
reported separately. A positive other-position count requires inspection of
the enclosing application before drawing any hypothesis-discharge conclusion.
No amount of occurrence counting alone establishes necessity.

## Source and print evidence

Reuse v0.4 compiled provenance: getUsedConstants on stored type and body,
limit 4,096 references per location. Collect target-owner source files first,
then direct-reference owner modules in lexical order and one import level.
Maximum 160 files, 2 MiB per file, 8 MiB total. Every copied source is compared
with pinned git contents. Missing and capped entries remain explicit.
Type/body provenance and argument-position counts are different measurements.
Printed declarations can be elided; raw-expression counts do not depend on
those rendered strings. Original logs, block hashes, caps and input hashes
are retained.

## Gates and resource limits

Run positive and intentional negative Lean fixtures, existing provenance
fixtures, then the new argument fixtures before importing Main. The argument
fixture covers direct/absent references, shadowing, outer references under
binders, annotation positions, forall, lets, projection, inherited annotation,
metadata, node/depth limits, stored theorem extraction, and outer/binder caps.
Synthetic Expr tests check traversal mechanics and need not be well-typed terms.
A real identity theorem checks stored-body integration. Fail closed on missing
or invalid records. No later project step starts after a fixture failure.

One owned container at a time; 2 logical CPUs, 100 GiB project memory,
4 GiB fixtures, read-only project/toolchain, no network, no extra swap,
30-minute default project timeout and 64 MiB log cap. Require 116 GiB available
RAM and 21 GiB free disk at project start. No Comparator inspection/control,
rebuild, export copy, global graph or full census.

## Reporting and open work

Publish per-target counts, original binder names/ordinals, limits, first errors,
source provenance and any elisions. Distinguish collection success from an
interpretation of the proof. A new RH/GRH or independent-kernel verdict is not
part of this experiment.

Still outstanding: all unknown reasons and budgets, larger-budget LedPart.pt,
second control, project/library/instance/generated strata, frozen per-category
sampling, and application-level witness-versus-incidental classification.
This targeted study must not be presented as completing those requests.
