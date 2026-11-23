# Stage 3 v0.14: state witness providers

This is a bounded follow-up to v0.13. It examines the immediate existence-obligation source and distinguishes state construction from transport of an existing state. It also inspects ten generated proof helpers omitted from the previous direct-edge account.

The zero fallback alone was not evidence of a bypass: v0.13 established that the inspected conversion explicitly takes an existence proof. This phase is diagnostic, not a decisive test of the anyGeometry criticism. See STATE_WITNESS_PROTOCOL.md for its stopping rule.

```bash
(
set -euo pipefail
unzip "$HOME/Downloads/rh-audit-stage3-v0.14.zip" -d "$HOME/rh-verification/tools"
python3 "$HOME/rh-verification/tools/rh-audit-stage3-v0.14/audit_stage3.py" --phase state-witnesses
)
```

Run the new phase once. Return stage3-evidence.zip, including on failure. Three small fixtures precede one Main import and inspection of 25 declarations. Two bounded searches over the pinned source then collect construction candidates. They do not automatically classify any hit as a dependency or witness.

Outputs include state-witnesses.log, state-witness-provenance.json, state-witnesses-blocks.json, state-witness-navigation.json, collected source, metadata, and a checksummed evidence archive.

Comparator is untouched. Proof/toolchain mounts are read-only. Docker limits remain two CPUs, 100 GiB RAM and 30 minutes per project step. Host Git searches use one worker, 90 seconds per group, and a 4 MiB output cap. Source snapshots are capped at 8 MiB total. No export copying or project rebuild. Required headroom: 116 GiB available RAM and 21 GiB free disk.

The new Lean probe has not been compiled locally: Lean is unavailable in the authoring environment. It reuses the successful v0.13 provenance helper and fixtures unchanged. Python tests exercise orchestration, parsing and pinned-source search; they do not substitute for the server Lean run.

Completion of this phase is not completion of Stage 3 or Comparator verification.
