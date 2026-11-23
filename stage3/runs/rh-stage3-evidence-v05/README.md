# Stage 3.4: targeted argument occurrences (v0.5)

This increment follows successful v0.4 consumer/provenance collection. It
examines where arguments occur in ten selected stored bodies, including the
next class-sum consumer and the covolume supplier. Read USE_PROTOCOL.md for the
frozen questions, limits and interpretation rules.

## Run

Save rh-audit-stage3-v0.5.zip in Downloads:

```bash
(
set -euo pipefail
unzip "$HOME/Downloads/rh-audit-stage3-v0.5.zip" -d "$HOME/rh-verification/tools"
python3 "$HOME/rh-verification/tools/rh-audit-stage3-v0.5/audit_stage3.py" --phase uses
)
```

The sequence is positive fixture, intentional negative fixture, provenance
fixture, argument-occurrence fixture, then a single project import. A failed
fixture stops before the project probe. `--phase use-smoke` runs fixtures only;
it is optional since `uses` includes them. Older phases remain available and
do not need repeating.

Share the final stage3-evidence.zip. It includes uses.log, argument-occurrences.json,
use-provenance.json, uses-blocks.json, use-fixture-result.json, bounded source
snapshots/index, protocols, code, run metadata and checksums.

## Meaning and limits

Counts separate occurrences inside binder domains/let types from other expression
positions. Other-position occurrences do not automatically establish witness
discharge or necessity. Zero counts are meaningful only for completed scans of
the explicit lambda remainder; no unfolding, reduction or eta expansion occurs.
Targets are chosen from the prior investigation, not randomly sampled.

Comparator remains untouched. Project cap: 2 CPUs, 100 GiB memory, no extra swap,
30 minutes; each fixture uses 4 GiB. One container at a time. Read-only project,
no network, rebuild, export copy or global traversal. New sources are capped
at 8 MiB/160 files and each log at 64 MiB. Requires 116 GiB available RAM and
21 GiB disk. Failures preserve evidence.

This does not complete Stage 3 or establish an RH/GRH verdict. Daniel's broader
control/stratification/unknown/sample-use requests remain open.

See TEST_RESULTS.txt. The authoring workspace has no Lean executable. Python
checks ran here; the new Lean helper has NOT been compiled here. The mandatory
server fixtures are the next executable validation gate, not a claim that
unrun code is already validated. Selected input hashes do not cover every
compiled dependency artifact.
