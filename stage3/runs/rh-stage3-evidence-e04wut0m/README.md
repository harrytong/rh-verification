# Stage 3.0: targeted geometry and height inspection

Prepared 23 November 2026 with ChatGPT assistance. This is the first implementation
increment of Stage 3, not a completed Stage 3 result.

## What this package does

1. Validates the recorded project/Mathlib revisions, compiler, headline `.olean`
   hashes, and the twelve selected source snapshots before running probes.
2. Runs an isolated positive Lean fixture and a deliberately invalid negative
   fixture. Both must behave as expected before Main is imported.
3. Compiles a renamed copy of the previously successful bundle baseline with five
   `trace_state` points. It retains all three `geoCl anyGeometry` applications.
4. Prints selected stored declarations, including the two distinct `geo` fields,
   and the bundle's resulting elaborated proof term with `pp.all` enabled.
5. Checks two explicitly stated height equations on the constructed `p.pt` object.
6. Saves commands, logs, source snapshots, code, hashes, exit statuses and metadata
   in a new evidence ZIP. The selected input hashes are checked again on success.

This increment collects evidence for manual typed-application review. It does not
automatically classify all witness uses, establish necessity, change a predicate,
run another census, or perform a new independent kernel verification. The copied
bundle still uses original helpers. Importing Main is disclosed: this is not a
proof reconstruction that excludes the questioned route. Printed output is an
elaborator rendering, not a substitute for an independent raw-expression export;
any printer truncation must be resolved before claiming a complete application.

## Installation and execution

Save `rh-audit-stage3-v0.1.zip` in `$HOME/Downloads`, then:

```bash
(
set -euo pipefail
unzip "$HOME/Downloads/rh-audit-stage3-v0.1.zip" -d "$HOME/rh-verification/tools"
python3 "$HOME/rh-verification/tools/rh-audit-stage3-v0.1/audit_stage3.py" --phase inspect
)
```

The `inspect` phase runs both fixtures, geometry, then height. A failure stops the
sequence and archives partial evidence. For only the fixture gate, use `--phase
smoke`. To run one case later, use `--phase geometry` or `--phase height`; each
case rechecks the fixture gate. No large audit starts after a failed fixture.

Full term output goes to logs rather than flooding the terminal. A progress line
appears every minute while a command is quiet. The default project-probe time
guard is 1,800 seconds per process; it is a limit, not an ETA. A time-limit failure
is incomplete collection, not proof rejection. `--probe-seconds` can explicitly
raise it up to 7,200 seconds if needed after reviewing the failure.

At the end, share the printed `stage3-evidence.zip`. It contains `geometry.log`,
`height.log` when reached, the positive/negative fixture logs and metadata. An
expected type error in `negative.log` is intentional and is not a project error.

## Resource and isolation limits

- Original source/toolchain mounts are read-only; no Lake build or export occurs.
- One uniquely named Stage 3 container at a time, 2 logical CPUs, 100 GiB RAM,
  no extra swap, network disabled, dropped capabilities, read-only root.
- Fixtures have no project mount or project search path and use a 4 GiB cap.
- At least 21 GiB free disk and 116 GiB available RAM are required before a
  default project probe (100 GiB limit plus 16 GiB host reserve).
- Each log is capped at 64 MiB. The small package includes source extracts; it
  never copies the 57 GiB proof export or writes a complete dependency graph.
- Only a container created by this run, identified by its own Docker CID file,
  can be stopped by the runner on interruption/resource failure. Comparator is
  never queried, stopped, restarted or modified.
- The existing Docker image is resolved to its image ID before use.

The checks are provenance checks against our saved evidence, not a fresh
authentication of every dependency artifact. They do not replace Comparator.

## Validation status at release

See `TEST_RESULTS.txt`. Python runner tests and source/diff checks were run in the
authoring workspace. Lean 4.33.1 is unavailable there, and its release download
was denied by that environment's network. Consequently **these new Lean probes
are not described as locally compiled**. The on-server fixture gate is mandatory.
The geometry body is unchanged from the saved Stage 2 baseline except its new
name and trace commands; a test enforces that fact. The new height propositions
still require your pinned compiler to accept them.

## Scope of the next increments

`PROTOCOL.md` records the exact next questions and Daniel Fairbanks's latest
request for origin/instance separation. Full candidate replay, use classification,
additional controls and the 403-unknown breakdown remain pending. Do not describe
their planned outputs as findings from this first package.
