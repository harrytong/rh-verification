# Stage 3.3: consumer implementations and provenance (v0.4)

This increment follows the completed v0.3 domain and obligation collection.
It inspects eight underlying declarations and collects source modules using
provenance from the compiled environment. See `CONSUMER_PROTOCOL.md` for the
questions and interpretation rules fixed before this run.

## Run

Save `rh-audit-stage3-v0.4.zip` in Downloads, then run:

```bash
(
set -euo pipefail
unzip "$HOME/Downloads/rh-audit-stage3-v0.4.zip" -d "$HOME/rh-verification/tools"
python3 "$HOME/rh-verification/tools/rh-audit-stage3-v0.4/audit_stage3.py" --phase consumers
)
```

The sequence is positive fixture, intentional negative fixture, provenance
fixture, then one project import for `consumers`. A failed fixture stops the
sequence before the project import. `--phase provenance-smoke` runs the fixtures
alone; it is optional because `consumers` includes them. Older phases remain
available and need not be repeated.

Share the printed `stage3-evidence.zip`. New evidence includes:

* `consumers.log`: selected declarations and axiom lists, plus provenance rows;
* `consumer-provenance.json`: target metadata, direct references and limits;
* `consumers-blocks.json`: rendered-block hashes and elision indicators;
* `collected-source-index.json` and `collected-source/`: bounded, git-verified
  source context, including skipped and capped entries;
* `provenance-fixture-result.json`: isolated tool checks;
* code, protocols, configuration, run metadata, input and evidence hashes.

## Resource limits

Comparator is not inspected or controlled. One owned container runs at a time.
Project and toolchain mounts are read-only. No rebuild, export copy, or full
reference graph occurs. Project cap: 2 logical CPUs, 100 GiB RAM, no additional
swap, no network, 30-minute timeout. Fixtures use 4 GiB. Each log is capped at
64 MiB; new sources at 8 MiB, with at most 160 copied files.

The default project probe requires 116 GiB available RAM and 21 GiB disk free.
Failures archive available evidence. Quiet steps report time every minute.

## Scope and validation

The output supports review of witness construction/use and the actual height
comparison. References alone do not establish necessity. Type references include
binders and conclusion; body references include annotations and implicit
arguments. This probe does not label those finer roles. Prints can be elided.

This is a targeted increment, not completion of Stage 3. Second-control,
stratified-census, full-unknown and frozen-sample-use work remain outstanding.
No new independent kernel verdict is asserted.

See `TEST_RESULTS.txt`. Python tests ran locally. The authoring workspace has no
Lean executable: the new Lean code has **not been compiled here**. Mandatory
server fixtures check the helper before the project import. Prior successful
probes do not validate new code. Input hashes cover selected files, not every
dependency artifact.
