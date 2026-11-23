# Stage 3 v0.10: trace the original theta supplier

The v0.9 run showed that emtTheta_L_alt transports the identity stored in l.c.th. This increment inspects the character-data constructor, the level-existence suppliers, and the local-component result used to fill the theta field.

```bash
(
set -euo pipefail
unzip "$HOME/Downloads/rh-audit-stage3-v0.10.zip" -d "$HOME/rh-verification/tools"
python3 "$HOME/rh-verification/tools/rh-audit-stage3-v0.10/audit_stage3.py" --phase character
)
```

Run once and return the resulting stage3-evidence.zip, including on failure. Three fixtures run first, followed by one Main import inspecting twelve required declarations. Previous phases need not be repeated.

Key outputs: character.log, character-blocks.json, character-provenance.json, collected-source-index.json and source snapshots, run-metadata.json, protocol and target configuration. Missing sources, reference caps and printed elisions remain explicit limitations.

Comparator is untouched. Project and toolchain mounts are read-only. Default limits remain 2 logical CPUs, 100 GiB RAM, 30 minutes per project step, 64 MiB log, 250 requested source paths and 8 MiB collected source. The runner requires 116 GiB available RAM and 21 GiB free disk before a project step. No export copy or proof rebuild.

A completed run means evidence collection succeeded. It does not establish nonvacuity, necessity, circularity, or RH/GRH validity. CHARACTER_PROTOCOL.md fixes the interpretation rules before the run; SOURCE_REVIEW_V010.md records why these targets were selected.

No Lean executable is available in the packaging environment. CharacterConstruction.lean has NOT been compiled here. Its provenance helper and fixtures are byte-identical to those used in the successful v0.9 server run. TEST_RESULTS.txt distinguishes Python runner tests from the actual Lean run still required on Harry's server.
