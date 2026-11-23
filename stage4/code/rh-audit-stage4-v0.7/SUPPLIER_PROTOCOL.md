# Stage 4 v0.6 — package construction and input suppliers

Prepared 2026-11-23 after v0.5, before this probe is run against the compiled
project. Targets were chosen after source inspection; this is not blind sampling.

## Question and honest boundary

v0.5 observed arguments to generic wrappers. v0.6 inspects the structure
constructor in `Formalism.L2.DIV.DivisionPackageFace.ofOpen`, the proof-producing
calls inside it, and the declarations producing division clauses.

`ofOpen` is a specific package-building definition, but still takes parameters,
including `inp`. It is not itself a fully specialized closed headline proof.
This phase must not label an input as missing merely because it is a parameter.
The bounded source collection locates upstream suppliers to inspect; a literal
match is not proof of use on a headline path.

## Recorded compiled evidence

Keep the v0.5 comparison and argument scanners unchanged. Observe the first
stored application for each of these three caller/callee pairs, with caller
`Formalism.L2.DIV.DivisionPackageFace.ofOpen`:

| Callee (same DIV namespace) | Arguments | Compared types after entering forall binders |
| --- | --- | --- |
| DivisionPackageFace.mk | R, inp, hTie, rhs | hTie, rhs |
| hTie_of | hk, hnum, hh | hnum, hh |
| rhs_le_record | H, t, hC0, hC1, hC2, hCabs, hLa | hC0, hC1, hC2, hCabs, hLa |

Expected collection: 14 argument records and nine comparisons. The callee's
parameter types are instantiated with earlier supplied arguments. Local
hypotheses are preserved; they are not rewritten into the comparison's sides.

Also record types and available stored bodies for eleven named declarations:
`DivInputs0R`, `DivInputs0R.mk`, `DivInputsR`, `DivInputsR.mk`, `DivClausesR`,
`divClausesR_of`, `linkDIV_L2R_clauses`, `linkDIV_L2R_face`, `RecNums.ofNum`,
`hTie_of`, `rhs_le_record`, all with prefix `Formalism.L2.DIV.`.

The constructor types disclose the input structures' fields. An inductive or
constructor has no stored definition body; JSON null there is not an error.
An absent declaration instead produces status unknown and incomplete coverage.
Declaration printing is capped at 80,000 characters for a body, 24,000 for its
type, and 512 body references; truncation is explicit. Existing argument-print
caps remain unchanged. Printed definitions are evidence for review, not an
additional typechecker verdict.

## Source collection

Search the pinned Git commit for these fixed literal strings: `structure
DivInputs0R`, `divClausesR_of`, `DivInputs0R`, `InpAtAlt`, `ptK_of_real_alt`, and
`DivisionPackageFace.ofOpen`. This is a source-navigation operation only.

Record the matching file list. Prioritize eight named files already identified
from imports and source. Then collect up to 80 files, at most 2 MiB each and
24 MiB total, checking each copied file against pinned Git contents. Search has
a 180-second guard; collection records missing files, selection caps and byte
caps. Retain at most 20,000 matching lines, each at most 2,000 characters, with
truncation flags. A failure or cap remains visible and does not prevent the
separate compiled inspection from reporting its own coverage.

The original source snapshots are still checked before/after the run. Newly
collected source is verified against the pinned commit when collected. The
search does not establish compiled reachability, actual use, or necessity.

## Controls, resources and interpretation

Run the existing negative, comparison and argument fixtures, then a new
structure-constructor fixture through the same scanner. The new fixture checks
a forwarded input, reflexive fields, a declaration with a stored body, and an
absent declaration reported as unknown. Stop before Main if any fixture fails.

Keep the existing separate read-only container, 2 CPU cap, 100 GiB project RAM
cap, 30-minute project wall guard and disk/memory preflight. Never control the
Comparator or modify project files. No rebuild or additional proof export.

Definitional identity, when observed, concerns the inspected context only.
Nonidentity does not establish nonvacuity or a useful geometric interpretation.
An arithmetic estimate with assumptions must be traced to its concrete supplied
inputs before claiming it answers the criticism. A record field that forwards
an assumption is not evidence of a Lean error or an absent existence witness.

## Stage boundary

Use the compiled constructor records and source suppliers together to report
what is established and exactly where any unresolved input remains. Do not
claim the broader height criticism is resolved if the concrete headline
instantiation has not been connected. No automatic RH/GRH, necessity, or
Comparator verdict is produced.
