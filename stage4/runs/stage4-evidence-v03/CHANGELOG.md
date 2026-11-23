# v0.3 — targeted application follow-up

The v0.2 uploaded run passed the corrected Lean helper and project examples.
Three generic comparisons and one applied valuation comparison had nonidentical
sides. The slope caller traversal reached its node cap without a match.

Changes: descending argument order, let-body-first traversal, explicit first-match
mode with scope recorded, one new Lean fixture, and a separately hashed protocol
amendment. The definitional-equality comparison code, proof inputs and resource
limits are unchanged. No claim of exhaustive call coverage is made.

The source-review report is STAGE4_V02_FINDINGS.md. Original v0.2 evidence SHA-256:
`0eaea5fa6c8e448e65b4521876606d47eb09683d61774eb7a21b18f29313bc58`.

# v0.2 — audit-tool monad correction

Input evidence: `stage4-evidence.zip`, SHA-256
`d3b11abae6c74a24d44040749154a916db6ff5013d0f53f22ad93ed86f87298a`.

The negative fixture behaved as expected. The comparison fixture exited 1 after
three type mismatches at lines 65, 71 and 74 of the assembled file. In each case,
`Lean.Elab.Command.liftIO` returned `CommandElabM Unit` where `MetaM Unit` was
required. The later evaluation error mentioning `sorry` was a consequence of
these failed audit definitions, not a sorry in the project's proof. No Main
import was started by this run.

Fixes:

- Use `emitMeta : List (String × Json) → MetaM Unit`, implemented with generic
  `liftM`, for all three emissions inside the comparison computation.
- Open `Lean.Elab.Command` only after the shared helper, for the `run_cmd` blocks.
- Add regressions for namespace separation and rejecting an end marker when
  compilation has failed.

Unchanged: PROTOCOL.md bytes and hash, comparison targets, controls, source and
compiled-input pins, resource budgets, interpretation rules and Comparator
isolation. The protocol retains its original v0.1 registration label intentionally.

Validation: local Python tests and static assembly checks only. The authoring
environment has no Lean executable. The corrected Lean helper must pass the
same server-side controls before any project result is collected.
