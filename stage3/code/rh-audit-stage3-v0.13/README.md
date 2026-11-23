# Stage 3 v0.13: theta existence and zero-fallback boundary

This follows the successful v0.12 integral inspection. It traces the concrete RealSide constructor and the separate existence witnesses used to turn weak, zero-fallback theta data into the stronger properties consumed by the integral proof. See REALIZATION_PROTOCOL.md and SOURCE_REVIEW_V013.md.

```bash
(
set -euo pipefail
unzip "$HOME/Downloads/rh-audit-stage3-v0.13.zip" -d "$HOME/rh-verification/tools"
python3 "$HOME/rh-verification/tools/rh-audit-stage3-v0.13/audit_stage3.py" --phase realization
)
```

Run this new phase once; do not repeat earlier phases. Return the resulting stage3-evidence.zip even on failure. The phase runs three small fixtures and one Main import, with 17 targets and two conditional lemmas about the imported OrZero definition.

Outputs: realization.log, realization-provenance.json, realization-blocks.json, collected-source-index.json and snapshots, run-metadata.json, protocol/config hashes, and checksummed evidence archive.

Comparator is untouched. Proof/toolchain mounts are read-only. Limits remain 2 logical CPUs, 100 GiB RAM, 30 minutes per project step, 64 MiB per log, and 8 MiB collected source. Require 116 GiB available RAM and 21 GiB free disk. The script does not rebuild the project or copy the large export.

The new Lean probe has NOT been compiled locally because no Lean executable is available here. The provenance helper and three existing fixtures are unchanged; Python tests exercise runner and parser behavior, not Lean correctness. The server run will establish whether the requested Lean commands compile.

Successful collection is not an RH/GRH, necessity, non-vacuity, or Comparator verdict. This phase does not complete the separate census/control work.
