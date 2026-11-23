# RH critics audit — Stage 4 v0.5

A focused follow-up to the completed v0.4 height comparisons. This version
records the actual proof arguments supplying the `WordFacts` lower and upper
bounds at five selected stored wrapper calls. It preserves the lower bound's
nonzero-map premise and records the two package-level clause suppliers.

Read `ARGUMENT_PROTOCOL.md` for the fixed targets, limits and interpretation.
These are generic stored wrappers, not full transitive specializations of the
five headline proofs. A reflexive identity or an unused-looking parameter is
not by itself a flaw in RH/GRH.

## Run on Harry's AI-Server

Download `rh-audit-stage4-v0.5.zip` into `$HOME/Downloads`, then:

```bash
(
set -euo pipefail
unzip "$HOME/Downloads/rh-audit-stage4-v0.5.zip" \
    -d "$HOME/rh-verification/tools"
python3 \
    "$HOME/rh-verification/tools/rh-audit-stage4-v0.5/audit_stage4.py" \
    --phase wordfacts
)
```

The runner checks the negative control, the existing comparison fixture, and a
new argument fixture before importing `Main`. A failed control stops the run.
For controls alone use `--phase smoke`. The old `--phase height` remains available
for reproducibility; it is not needed for this follow-up.

## Resources and evidence

Separate read-only container, 2 logical CPUs and 100 GiB maximum for the project
probe. The preflight requires at least 116 GiB available host RAM and 21 GiB free
disk. It uses existing compiled modules and never controls the Comparator.
The project has a 30-minute wall guard; this is a limit, not a duration estimate.

Output is a new directory below `$HOME/rh-verification/critics-audit-stage4`.
Share its `stage4-evidence.zip` after the run. Key files:

- `CLAIM_RESULTS.json`: coverage and explicit limitations.
- `argument-records.json`: supplied expressions, expected types, local contexts,
  retained binders and comparison records.
- `wordfacts.log`: printed `WordFacts`, statement check and complete probe output.
- `argument-fixture.log`: the new fixture's actual Lean output.
- `run-metadata.json`: protocol hashes, pinned inputs, exits and limits.
- `collected-source/`: bounded source context verified against the pinned commit.

The expected project coverage is 16 argument records and 12 comparisons across
five first-call observations. Unknown or missing observations are not verdicts.
Read any truncation flags before claiming the evidence fully displays a term.
The selected `hcl` arguments are recorded but are not themselves classified as
single inequalities.

## Validation status

Python guard/coverage tests run in the authoring environment. The new Lean code
has not been compiled there because Lean is unavailable. The server-side fixture
is mandatory and runs the same helper used by the project probe. See
`TEST_RESULTS.txt` for the exact local test result.

The previous v0.4 helper and controls are retained. `PROTOCOL.md`,
`FOLLOWUP_PROTOCOL.md` and `REFERENCE_FILTER_PROTOCOL.md` describe those earlier
phases; `ARGUMENT_PROTOCOL.md` describes the new phase.
