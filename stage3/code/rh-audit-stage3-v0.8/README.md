# Stage 3 v0.8: trace the finiteness supplier

This follows v0.7's extension findings. It prioritizes FinitenessOfHyp and related suppliers to trace where the extension record and its .th proof originate.

```bash
(
set -euo pipefail
unzip "$HOME/Downloads/rh-audit-stage3-v0.8.zip" -d "$HOME/rh-verification/tools"
python3 "$HOME/rh-verification/tools/rh-audit-stage3-v0.8/audit_stage3.py" --phase construction
)
```

Run once and return the resulting stage3-evidence.zip. Prior phases remain available but need not be repeated. Three fixtures run first, then one Main import inspects eight declarations. Target owners and explicitly requested supplier files receive priority over general direct-reference source collection. A source index records collection limits and a separate lexical index helps locate candidate construction sites.

Key outputs: construction.log, construction-blocks.json, construction-provenance.json, construction-source-hits.json, collected-source-index.json, source snapshots, run-metadata.json and the frozen protocol/targets. Keep the evidence archive even on failure.

Comparator is untouched. Project and toolchain mounts remain read-only. Limits: 2 CPUs, 100 GiB RAM, 30 minutes per project step, 64 MiB per log, 250 requested source paths and 8 MiB source bytes. Default checks require at least 116 GiB available RAM and 21 GiB free disk. No export copy, rebuild, or global census is performed.

Successful completion means the requested collection succeeded. It does not certify that .th was constructed nonvacuously, that any geometry condition is necessary, or that RH/GRH has received a new verdict.

No local Lean executable is available in the packaging environment. Construction.lean was not compiled there. Its inspection helper is identical to the one that passed the uploaded v0.7 fixtures; this run repeats the relevant fixtures. See TEST_RESULTS.txt for Python validation and CONSTRUCTION_PROTOCOL.md for scope.
