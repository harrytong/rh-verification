# RH critics audit — Stage 4 v0.7

This follow-up inspects the constructor `DivisionPackageFace.ofOpen` and its
proofs for `hTie` and `rhs`. It also records the division-clause input structures
and supplier declarations, and collects bounded source matches for the remaining
`inp` construction.

The constructor is still parameterized. This package does not promise to decide
the entire criticism or to substitute all the way from the headline theorem.
See `SUPPLIER_PROTOCOL.md` for the exact evidence and stopping boundary.

## Run

```bash
(
set -euo pipefail
unzip "$HOME/Downloads/rh-audit-stage4-v0.7.zip" \
    -d "$HOME/rh-verification/tools"
python3 \
    "$HOME/rh-verification/tools/rh-audit-stage4-v0.7/audit_stage4.py" \
    --phase suppliers
)
```

The runner searches pinned source, runs isolated controls, then imports `Main`.
A failed fixture prevents the project probe. Source search can be quiet for up
to its three-minute guard. Main import is also normally quiet.

Resources: separate container, 2 logical CPUs, 100 GiB project memory limit;
preflight requires 116 GiB available host RAM and 21 GiB free disk. Source
collection is capped at 24 MiB; log output at 64 MiB per process. No project
rebuild and no action on Comparator.

After the run, share the new `stage4-evidence.zip`. Key files:

- `CLAIM_RESULTS.json`: compiled coverage, truncations, and source coverage flag.
- `supplier-records.json` / `suppliers.log`: constructor arguments and declarations.
- `supplier-source-index.json`: matched, selected and omitted source files.
- `supplier-source-hits.json`: literal source locations, not dependency evidence.
- `supplier-source/collected-source/`: files checked against pinned Git contents.
- `supplier-fixture.log`: the new Lean fixture's actual result.
- `run-metadata.json`: protocol hashes, limits and exits.

The expected compiled collection is 14 arguments, nine comparisons, and thirteen
declaration records. Unknowns and truncation remain explicit. Read these before
making any mathematical claim.

## Testing

The unchanged v0.5 helper already passed on Harry's server. New code is checked
locally with Python tests and reviewed against the collected source. Lean is
unavailable in the authoring environment: the new Lean fixture remains mandatory
on the server, and no local Lean compile success is claimed.

Older phases `height`, `wordfacts`, and `smoke` remain available. Run `suppliers`
for this follow-up; it includes all required controls.

## v0.7 correction

v0.6 captured the actual constructor, but the two proofs were references to
`ofOpen._proof_7` and `ofOpen._proof_10`. Its direct-body scans therefore did not
cover the selected helper calls. This release follows exactly those observed
declarations, under the same source and compiled-artifact pins. If either call
is absent or hidden farther down, coverage remains incomplete; absence is not
a mathematical failure. The scan remains bounded and does not recursively
unfold arbitrary declarations.

See STAGE4_V06_FINDINGS.md and HELPER_FOLLOWUP_PROTOCOL.md. Rendered expressions
can contain Lean elisions even when no character cap was reached; the summary
now reports visible elision markers separately. This does not alter the
expression-based comparisons.
