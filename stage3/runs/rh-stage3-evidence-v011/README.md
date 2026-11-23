# Stage 3 v0.11: theta-lift and descent suppliers

This follows v0.10's character-data constructor. It inspects the upstream theta-lift/class-sum theorem, coefficient-field proportionality theorem, and integral-unit supplier, with their local callers and identity definitions.

```bash
(
set -euo pipefail
unzip "$HOME/Downloads/rh-audit-stage3-v0.11.zip" -d "$HOME/rh-verification/tools"
python3 "$HOME/rh-verification/tools/rh-audit-stage3-v0.11/audit_stage3.py" --phase descent
)
```

Run once and return the resulting stage3-evidence.zip, including on failure. Three fixtures precede one Main import inspecting eight required declarations. Do not repeat earlier phases.

Outputs: descent.log, descent-provenance.json, descent-blocks.json, collected-source-index.json and snapshots, run-metadata.json, protocol/config and checksums. Any caps or printer elisions remain limitations.

Comparator is untouched; project/toolchain mounts are read-only. Default limits remain 2 logical CPUs, 100 GiB RAM, 30 minutes per project step, 64 MiB log and 8 MiB collected source. The runner requires 116 GiB available memory and 21 GiB free disk. No proof rebuild or export copy.

The new Lean probe has NOT been compiled locally: no Lean executable is available here. The provenance helper and fixtures are byte-identical to v0.10 and run again before the project probe. Python tests validate runner behavior only; see TEST_RESULTS.txt.

Successful collection is not a proof-validity, necessity or nonvacuity verdict. DESCENT_PROTOCOL.md fixes review rules and scope before the run.
