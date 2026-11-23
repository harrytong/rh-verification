# Stage 3 v0.12: integral identity and theta realization

This follows v0.11's coefficient-descent review. It inspects the integral identity, its caller proofs, the records carrying theta assumptions and two flat-vector dilation suppliers. Eleven targets are fixed before the run in INTEGRAL_PROTOCOL.md and integral-targets.json.

```bash
(
set -euo pipefail
unzip "$HOME/Downloads/rh-audit-stage3-v0.12.zip" -d "$HOME/rh-verification/tools"
python3 "$HOME/rh-verification/tools/rh-audit-stage3-v0.12/audit_stage3.py" --phase integral
)
```

Run once and return stage3-evidence.zip, including on failure. Three fixtures precede one Main import. Do not repeat earlier phases.

Outputs: integral.log, integral-provenance.json, integral-blocks.json, collected-source-index.json and snapshots, run-metadata.json, protocol/config and checksums. Caps and printer elisions remain explicit limitations.

Comparator is untouched. Project/toolchain mounts are read-only. Defaults remain 2 logical CPUs, 100 GiB RAM, 30 minutes per project step, 64 MiB log and 8 MiB collected source. The runner requires 116 GiB available memory and 21 GiB free disk. No proof rebuild or export copy.

The new Lean probe has NOT been compiled locally; no Lean executable is available here. The shared provenance helper and fixtures are unchanged from v0.11 and run again before the project probe. Python tests validate runner behavior only; see TEST_RESULTS.txt.

Successful collection is not a proof-validity, necessity, nonvacuity or Comparator verdict. This focused phase does not complete Daniel Fairbanks' broader census/control requests.
