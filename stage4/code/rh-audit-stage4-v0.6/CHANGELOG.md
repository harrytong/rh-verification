# v0.4 — reference-filtered application search

The v0.3 slope scan still reached its node cap. This version skips branches whose
stored constant references exclude the watched callee, and records owner-level
references and pruning counts. It adds an absent-call fixture. Comparison logic,
selected callers/callees, first-match scope and runtime caps are unchanged.
The change is registered separately in REFERENCE_FILTER_PROTOCOL.md.

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

## v0.5 — supplied WordFacts proof arguments

- Added `--phase wordfacts` without modifying the v0.4 comparison helper.
- Record dependent argument types and actual supplied terms for five fixed
  caller/callee edges; explicitly retain the nonzero premise of `c2`.
- Record `hcl` suppliers at both package wrappers; no transitive specialization
  or necessity inference is claimed.
- Added isolated argument fixtures and coverage rejection for missing arguments,
  lost premises, caps, unknowns, and missing/duplicate comparison records.
- Added pinned RecBridge source context and bounded collection of LinkDIVL2R3Col.
- New Lean code awaits the mandatory server-side fixture; local tests are Python.

## v0.6 — constructor fields and upstream inputs

- Added `suppliers` phase inspecting actual `DivisionPackageFace.mk` arguments
  inside `ofOpen` and calls to `hTie_of` and `rhs_le_record`.
- Kept the successfully exercised v0.5 argument/comparison helpers unchanged.
- Added bounded declaration records and an isolated structure fixture.
- Added pinned Git literal source discovery and verified source collection for
  the remaining `DivInputs0R` / `InpAtAlt` suppliers, with explicit caps/errors.
- The constructor still has parameters; no full headline specialization claimed.
