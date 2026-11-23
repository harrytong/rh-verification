# Stage 3 v0.7: extension obligations and witness suppliers

This follows the completed v0.6 provider probe. The question is where the extension record and its EMtTheta proof come from, beyond their being carried through a record field.

```bash
(
set -euo pipefail
unzip "$HOME/Downloads/rh-audit-stage3-v0.7.zip" -d "$HOME/rh-verification/tools"
python3 "$HOME/rh-verification/tools/rh-audit-stage3-v0.7/audit_stage3.py" --phase extensions
)
```

Run once. Previous phases remain available but do not need repeating. The four fixtures run first; any failure stops before the project probe. Then one Main import inspects 18 declarations and searches two selected arguments using the unchanged v0.6 helpers. It collects bounded pinned source context for the existence route.

Upload the final `stage3-evidence.zip`. Key files are extensions.log, extensions-blocks.json, extension-provenance.json, targeted-occurrences.json, collected-source-index.json, source snapshots, run-metadata.json, and the frozen protocol and targets. Retain the whole archive even on failure.

A successful run means the requested inspection completed. It does not mean the record was proved non-vacuously inhabited, the disputed geometry was proved necessary, or RH/GRH received a new verdict. A capped search is inconclusive. Read EXTENSION_PROTOCOL.md before interpreting results.

Comparator is untouched. Project mounts are read-only. Limits: 2 CPUs, 100 GiB, 30 minutes per project step, 64 MiB per log; source collection at most 200 requested paths and 8 MiB. The runner requires at least 116 GiB available RAM and 21 GiB free disk at the default memory setting. No export copy or rebuild.

No Lean executable is available in the packaging environment. The project target list is not locally Lean-compiled. The reused helpers passed Harry's v0.6 fixtures; this package reruns them. Python test results are in TEST_RESULTS.txt. Broader census/control requests are not completed by this targeted phase.
