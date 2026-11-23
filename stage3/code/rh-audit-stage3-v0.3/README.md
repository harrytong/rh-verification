# Stage 3.2: domain boundaries and obligation chains (v0.3)

This increment follows the successful v0.2 run. It tests the exact inhabitance
conditions of objects parameterized by geometry, then collects selected
comparison-witness and height-consumer declarations. Read `DOMAIN_PROTOCOL.md`
for the questions and interpretation rules fixed before these new tests run.

## Run

Save `rh-audit-stage3-v0.3.zip` in Downloads:

```bash
(
set -euo pipefail
unzip "$HOME/Downloads/rh-audit-stage3-v0.3.zip" -d "$HOME/rh-verification/tools"
python3 "$HOME/rh-verification/tools/rh-audit-stage3-v0.3/audit_stage3.py" --phase obligations
)
```

The sequence is positive fixture, intentional negative fixture, `domains`,
`witness-chain`, `height-chain`. Failures stop the sequence and are archived.
All three named project steps can also be selected individually with `--phase`.
The older phases are retained; they need not be repeated for this increment.

At completion, share the printed `stage3-evidence.zip`. It contains the code,
protocol and hashes, logs, metadata, selected source snapshots, bounded additional
source collection, and a block index for each completed chain-printing step.

## What the new tests establish if accepted

The domain theorems identify the exact conjunction required to inhabit `OAt Γ`;
specialize it to `anyGeometry`; and show emptiness for False and `geoCl False`.
These are local domain statements. They do not establish emptiness or correctness
of the original RH proof. The comparison and height steps expose stored lemma
types, bodies and axioms for further manual review; they are evidence collection,
not necessity tests or new independent kernel verification.

## Resource protection

Comparator is left untouched. Only one container owned by this run is active
at a time. Project mounts are read-only; no project build or large export copy
occurs. Default cap: 2 logical CPUs, 100 GiB RAM, no extra swap, no network.
Fixtures use 4 GiB and cannot import the project. Each project probe has a
30-minute guard and a 64 MiB log cap. A quiet probe prints progress every minute.

The host must have at least 21 GiB disk free and 116 GiB available RAM before
each default project probe. Source collection copies at most 8 MiB. The output
does not include a full dependency graph. Timeout, resource or tool failures
are recorded as incomplete collection, not as proof rejection.

## Validation status

Python tests and package checks are in `TEST_RESULTS.txt`. The authoring workspace
has no Lean executable: the new Lean files have **not been compiled here**.
The on-server fixture gate and project-probe exit statuses are required.
The old v0.2 successful run is prior evidence, not validation of these new files.

The runner verifies the saved project/Mathlib revisions, selected source hashes,
headline compiled-file hashes and compiler hash. These provenance checks do not
authenticate every dependency artifact and do not replace Comparator.

The second control, census strata, full unknown breakdown and preregistered
sample-use analysis remain pending. This is a bounded Stage 3 increment.
