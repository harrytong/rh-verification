# RH critics audit — Stage 4 v0.4

This follow-up addresses the still-incomplete `heightAt_eq_of_cover → slope_le_height`
search after v0.3. Read STAGE4_V03_FINDINGS.md, PROTOCOL.md, FOLLOWUP_PROTOCOL.md
and REFERENCE_FILTER_PROTOCOL.md. No result from the new search is assumed.

## Run

```bash
python3 "$HOME/rh-verification/tools/rh-audit-stage4-v0.4/audit_stage4.py" --phase height
```

Controls run first, without the project mount. Only if they pass does the runner
import Main once. For controls alone, use `--phase smoke`.

The new search skips subtrees without the watched constant in their stored
references. It reports owner-level references and skipped-subtree counts. It
visits later arguments first and stops at the first selected
callee application. This is explicitly a single-application test, not an exhaustive
scan of every call. The generic probes and comparison algorithm are unchanged.
The old auxiliary `le_refl` search is deferred. Caps and unsupported comparisons
remain unresolved. All three protocol hashes are recorded.

## Inputs and limits

Defaults use the existing `rh-lean-check:1` image, Lean v4.33.1, and pinned
`~/rh-verification/riemann-hypothesis`. Executable, Main/Statements and selected
source hashes are checked. These identify inputs; they do not independently
establish trust in every compiled dependency.

Two CPUs, 100 GiB project-container limit, 30-minute project wall limit, 64 MiB
per log. Require 116 GiB available RAM and 21 GiB free disk. No checkout writes,
rebuilds, exports, or Comparator interactions occur. Previous evidence is retained.

## Output

A fresh folder under `~/rh-verification/critics-audit-stage4/` contains:

- `height.log` and `comparison-records.json`: actual checks and local contexts.
- `CLAIM_RESULTS.json`: requested comparisons and unresolved cases. For v0.4,
  `collection_complete` covers the generic probes and first selected applications;
  `exhaustive_application_coverage` is always false.
- `run-metadata.json`: protocol hashes, source pins, limits, exits and timestamps.
- `collected-source/`: three sources verified against the pinned Git revision.
- `stage4-evidence.zip`: the complete bounded evidence bundle, including failures.

Please return the evidence ZIP. Process success is not an RH/GRH verdict. A
compiler-control failure is an audit-tool failure, not a proof failure.

## Validation

The v0.3 comparison core, traversal and seven controls passed on Harry's server.
The v0.4 reference filter and additional absent-call control have not
been compiled in the authoring environment, which has no Lean executable. The
same mandatory fixture gate remains in place. See TEST_RESULTS.txt for Python
driver tests and CHANGELOG.md for the version history.
