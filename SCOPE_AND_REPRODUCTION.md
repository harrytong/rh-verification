# Scope and reproduction

This publication preserves evidence and exact issued audit packages. Do not
confuse a successful inspection process, complete selected coverage, a census
classification, a Lean build, a kernel replay, and protected statement comparison.

## Reproduction

1. Read the root README and the relevant stage protocol first.
2. Use the pinned source revision, dependencies and project toolchain recorded
   in the run metadata. The full compiled proof environment is not included.
3. For exact historical reproduction, use that run’s saved code or the matching
   archive under `stageN/packages/`; do not substitute a later version silently.
4. Follow the package README for its command. Existing runners use explicit
   paths under `$HOME/rh-verification`, Docker isolation, resource guards and
   output directories separate from the proof checkout.
5. Verify the package `SHA256SUMS` and evidence `EVIDENCE_SHA256SUMS`, where present.
   A checksum authenticates consistency with those bytes, not the server operator.
6. Read complete logs and JSON coverage fields. Expected negative-fixture errors
   are deliberate controls. Unexpected errors or caps are unresolved results.

Source snapshots, generated Lean probes, Python runners and historical Markdown
are retained under each run. The publication uploader does not execute any
audit, Lean proof or Docker command.

## Remaining research scope

Daniel Fairbanks proposed comparative controls, explicit denominators and
unknown rates, instance/non-instance breakdowns, preregistered use sampling,
and targeted larger-budget retries. Stage 2 includes one same-classifier
control and some origin reporting. The subsequent named-case probes do not
complete the second-control, full stratification, sampled-use, or exhaustive
unknown-accounting program. In particular, the retained unknown-message sample
does not classify all 403 unknowns. Do not infer completion from a tool package
being present.

The selected geometry generalization and False-domain tests are local. Constant
references, first-call observations and argument occurrences do not prove
necessity after normalization. A field can be present or used without carrying
the intended interpretation. Conversely, a mathematically redundant intermediate
construction does not invalidate a correctly checked closed theorem.

Stage 4 was closed by an explicit scope decision after v0.7. We accept formal
upstream obligations within the recorded verification scope and found no
missing-proof defect in the inspected route. The closure does not announce a
new Comparator verdict, global refutation of Nielsen/Chu, or independent
reproduction by Daniel or by the AI authoring environment.

## Attribution and historical documents

Harry ran the server jobs; AI assistance produced audit tooling and analyses.
Upstream Lean/Mathlib source retains its original authorship and licensing.
Historical reports remain byte-preserved where copied from evidence. Their
then-current next steps and incomplete hypotheses are not silently rewritten.
The root README and closing assessment state the current interpretation.
