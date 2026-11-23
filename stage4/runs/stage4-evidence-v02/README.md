# RH critics audit — Stage 4 v0.2

Purpose: test the alleged reflexive height comparison at concrete declarations
and immediate application sites. Read PROTOCOL.md before interpreting results.

This is a new, limited branch of the audit. Stage 3 v0.24's provider exploration
is on hold. No proof checkout writes, rebuilds, large export copies, or Comparator
interactions are performed.

## Run

On Harry's existing Ubuntu verification server:

```bash
python3 "$HOME/rh-verification/tools/rh-audit-stage4-v0.2/audit_stage4.py" --phase height
```

This runs controls first and stops if any control fails. Only then does it import
Main once for the project checks. For controls alone, use `--phase smoke`.

The defaults expect the existing `rh-lean-check:1` image, Lean v4.33.1 toolchain,
and pinned `~/rh-verification/riemann-hypothesis` checkout. SHA-256 checks protect
the executable, Main/Statements artifacts and three supplied source snapshots.
These hashes identify inputs; they do not independently establish trust in every
transitive compiled dependency. The separately running Comparator addresses a
different verification task.

## Output

Each run creates a new directory under `~/rh-verification/critics-audit-stage4/`.

- `height.log`: statement check, assigned-height proof and comparison records.
- `comparison-records.json`: all machine-readable project probe events.
- `CLAIM_RESULTS.json`: comparisons and explicit unresolved coverage issues.
- `run-metadata.json`: protocol hash, pins, limits, exit codes and completion state.
- `collected-source/`: three source files checked against the pinned Git revision.
- `stage4-evidence.zip`: small evidence bundle, including controls and failures.

Please return the evidence ZIP. A successful process exit means collection
finished; check `collection_complete` for scan coverage. Neither value is an
RH/GRH validity verdict. A failed compiler control means an audit-tool problem,
not a defect in the original proof.

## Validation status

The Python driver has local automated tests. The new Lean comparison helper has
not been compiled in the authoring environment, which has no Lean installation.
Server-side controls are mandatory. Older execution utilities and the assigned
height control were adapted from previously exercised audit code; that does not
make the new Lean helper prevalidated. See TEST_RESULTS.txt.

## v0.2 correction

The v0.1 fixture failed because opening `Lean.Elab.Command` made unqualified
`liftIO` select a `CommandElabM` function inside the `MetaM` comparison helper.
Version 0.2 uses an explicitly `MetaM`-typed `emitMeta` helper with generic
`liftM`. The protocol, targets, budgets and interpretation rules are unchanged.
The original protocol hash is preserved. This is a tool repair, not a change
to the proof or an audit finding. See CHANGELOG.md.
