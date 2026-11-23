# Stage 3 v0.14: bounded follow-up on state witness providers

Fixed 23 November 2026 before project execution. Based on v0.13 evidence SHA-256 e1e208fd2397101c1cf3c0e13995788ae36c3f1d2999d5398f91a3a8805a1487.

## Why this scope is limited

V0.13 showed an explicit existence premise at the inspected weak-to-strong theta conversion. The presence of a zero fallback was not evidence that this premise was bypassed. This follow-up identifies the immediate source of the premise and the surrounding state quantification. It is not designed to prove or refute Nielsen's or Chu's anyGeometry criticism, and it must not turn into an unlimited supplier chase.

The original criticism concerns the mathematical content and role of anyGeometry on a headline route. Merely confirming that ExAt exists, or finding more upstream premises, does not settle that criticism. Any proposed next experiment must name the critic's exact claim, the code occurrence, and an outcome that would change our assessment.

## Questions

1. What are the stored types of Moved, its constructor, its Holds and ExAt fields, St and its constructor? Which obligations are supplied by a caller?
2. How does AllSt quantify over states? Compare Start, HasBare, DatEx, UnitaryCaseCondition, and WeightCaseCondition. Do not infer state inhabitation from a universally quantified state property.
3. What does exists_movedData_state_localisations actually assume and construct, and what does its implementation MvLoc.exists_moved_loc reference? This is a transport candidate starting from an existing state, not an established initial-state provider.
4. Which of the ten generated RealSide.ofPins._proof_n bodies carries the characterisation/existence conversion? Inspect these compiled helpers directly rather than inventing direct edges from the source alone.
5. Where in the pinned source are explicit moved-record field assignments and state/existence obligations mentioned? Gather bounded source context to distinguish construction candidates from consumers. Lexical hits are not proof-use results.

## Fixed procedure

The 25 targets and their order are fixed in state-witness-targets.json and chain-targets.json. Names are grounded in v0.13 compiled references and preserved source snapshots. Missing targets fail; no fuzzy substitution.

Run the unchanged positive, expected-negative, and provenance fixtures. Import Main once. For each target record its owner module, stored type/body constant references (limit 4096 per location), printed declaration, and axiom list. Require every record and declaration block in order, exit 0, and RH_STAGE3_STATE_WITNESSES_END. No new mathematical boundary lemma is claimed in this increment.

After the Lean probe, run two lexical file searches against the fixed Git commit, confined to src/**/*.lean. The exact POSIX regexes are in the target JSON. Sort matching file paths lexically and select at most 60 files per group. Record total matching files, every selected and omitted path, and exit status; counts are file counts, not declaration or occurrence counts. Each search has a 90-second timeout and a 4 MiB output cap checked during execution. Search errors or output-cap failures fail the phase; no silent absence claim. Only the search process owned by this runner may be terminated.

Prioritize target owner files, fixed source roots, selected lexical candidates, then selected reference modules. Collect imports to depth one. Preserve the existing Git byte verification. Source caps: 250 requested paths, 2 MiB per file, 8 MiB total. Record every omission. Comments may match; positional record construction may be missed. A missing match never establishes absence from the proof.

Resource limits remain two logical CPUs and 100 GiB RAM for Docker project probes, 1800 seconds per project step, 64 MiB per log. Host Git searches use one Git worker. Require 116 GiB MemAvailable and 21 GiB free disk before project execution. No project edits, rebuilds, export copies, Comparator inspection, or Comparator control.

## Interpretation and stopping rule

Classify observations as record requirement, conditional transport, explicit witness construction, or unresolved. Any source-to-compiled linkage must distinguish a direct reference from transitive reachability and from an actual argument supplying a hypothesis.

A successful collection is not an RH/GRH verdict, a necessity result, nonzero-operator proof, or proof of state inhabitation. A transport theorem requiring an existing state is not an initial-state construction. An existence proof may still concern a mathematically weak predicate.

After this bounded collection, write the obligation map and stop this branch unless a specific inconsistency, unintended assumption, or documented link to the criticized anyGeometry step justifies further tracing. Do not automatically issue another supplier-following phase. Return priority to a test tied to the critics' precise claim.

Daniel Fairbanks' second control, complete unknown accounting, project/library/instance stratification, and preregistered use sampling remain separate unfinished deliverables.
