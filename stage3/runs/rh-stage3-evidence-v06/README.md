# Stage 3.5: class-sum supplier and targeted searches (v0.6)

This increment follows the successful v0.5 run. It retrieves the class-sum
supplier and searches for five selected binder occurrences, including hPin/hP.
It records a first occurrence and its syntactic application context, rather
than attempting another count of every occurrence.

## Run

```bash
(
set -euo pipefail
unzip "$HOME/Downloads/rh-audit-stage3-v0.6.zip" -d "$HOME/rh-verification/tools"
python3 "$HOME/rh-verification/tools/rh-audit-stage3-v0.6/audit_stage3.py" --phase providers
)
```

The sequence is positive, intentional negative, provenance and search fixtures,
then a single project import. A fixture failure stops before the project probe.
`--phase search-smoke` runs only fixtures; providers already includes them.
Previous phases remain available and do not need repeating.

Upload the final stage3-evidence.zip. It contains providers.log,
provider-provenance.json, targeted-occurrences.json, providers-blocks.json,
search-fixture-result.json, source snapshots/index, protocols, code, metadata
and checksums.

## Reading the result

Found means a syntactic occurrence was found in a projection omitting binder
domains and let types. It does not establish necessity or hypothesis discharge.
Not-found-in-projection never establishes full-body absence. All omission and
truncation indicators must accompany the interpretation. SOURCE_REVIEW_V06.md
records why these targets were chosen; PROVIDER_PROTOCOL.md fixes the method.

Comparator is untouched. At most 2 CPUs and 100 GiB memory for the project,
4 GiB for fixtures, one owned container at a time. Requires 116 GiB available
RAM and 21 GiB free disk. No rebuild, export copy, global traversal or census.
Source collection remains capped at 8 MiB/160 files, each log at 64 MiB, and
the project step at 30 minutes by default.

Python validation is documented in TEST_RESULTS.txt. There is no local Lean
executable, so the NEW Lean search helper has not been compiled here. Mandatory
server fixtures provide the next gate. v0.5's successful scanner does not
validate this new scanner. No new RH/GRH or independent-kernel verdict is asserted.
