# Stage 3 v0.9: inspect the theta proof

This follows v0.8's explicit extension constructor. It inspects emtTheta_L_alt, the producer of YRel, and the data used in the theta identity. It also inspects the constructor itself so its compiled direct references can be compared with the source trace.

```bash
(
set -euo pipefail
unzip "$HOME/Downloads/rh-audit-stage3-v0.9.zip" -d "$HOME/rh-verification/tools"
python3 "$HOME/rh-verification/tools/rh-audit-stage3-v0.9/audit_stage3.py" --phase theta
)
```

Run once and return the resulting stage3-evidence.zip, including on failure. Three fixtures run first. One Main import then inspects ten required declarations and collects bounded pinned source context. Previous phases remain available but need not be repeated.

Key outputs: theta.log, theta-blocks.json, theta-provenance.json, collected-source-index.json and source snapshots, run-metadata.json, protocol and target list. All declaration and source evidence remains subject to recorded caps and printer elisions.

Comparator is untouched. Project/toolchain mounts remain read-only. Default limits: 2 CPUs, 100 GiB RAM, 30 minutes per project step, 64 MiB log, 250 requested source paths and 8 MiB source bytes. The runner checks for 116 GiB available RAM and 21 GiB free disk. No export copy or rebuild.

A completed run means collection succeeded. It does not establish nonvacuity, necessity or RH/GRH validity. See THETA_PROTOCOL.md for the interpretation rules fixed before results.

No Lean executable is available in the packaging environment. ThetaIdentity.lean has not been compiled there. The provenance helper and fixtures are unchanged from the successful v0.8 run and will run again on the server. TEST_RESULTS.txt records Python validation separately.
