# Stage 3 v0.8: finiteness suppliers and initial extension construction

Protocol fixed before this increment's project run on 2026-11-23. It is informed by the completed v0.7 results and is not a retrospective preregistration of earlier findings.

## Question and scope

Where is the particular extension witness, and ultimately its RealExpansionExtraData.th proof, supplied? v0.7 identified EMtTheta's conditional theta/tensor equality, but did not resolve the construction or nonvacuity of its antecedents. Both v0.7 selected-argument searches were capped and inconclusive.

This increment collects the eight declarations listed in construction-targets.json. Their names occur in v0.7 collected source or compiled-reference records. It reports stored declaration kind, owner module, direct type/body references, printed declarations and axiom lists. It performs no new selected-argument search: enlarging the two exhausted searches would not by itself establish necessity.

## Frozen sequence and limits

1. Positive and negative fixtures, then the unchanged provenance fixture.
2. One Main import for Construction.lean. Every target is required; a missing target or failed command is an error. The success marker alone is insufficient: normal exit, ordered target records and begin/end blocks are checked.
3. Collect owner source files first, explicit priority files second, then direct-reference modules matching the frozen priority fragments. Other reference modules remain in the provenance data and are explicitly listed as not seeded for collection. They may still be collected through imports. Follow project imports breadth-first to depth 2.
4. Limits: 4,096 retained references per location, 250 requested source paths, 2 MiB per source, 8 MiB total source. Missing files and cap exclusions are recorded. Project step: 2 logical CPUs, 100 GiB RAM, 1,800 seconds, 64 MiB log. No global closure is traversed.
5. Produce a lexical navigation index for RealExpansionExtraData, EMtTheta, th assignments, and the finiteness supplier. Include comments; do not claim that a text match is a constructor application or witness use. Retain at most 2,000 matching lines, at most 1,000 characters per line, and label either truncation.
6. Preserve protocol/config hashes, input hashes before and after, stdout/stderr, source hashes and archive checksum. Source snapshots must match the pinned project's git contents.

## Interpretation rule

The reported owner and direct references locate declarations. They do not establish complete use, nonvacuity, semantic necessity, or the intended meaning of the headline statements. Pretty-printer elisions remain explicit. An uncollected file or unmatched lexical pattern is not evidence of absence.

To progress beyond provenance, review the actual supplier body and identify the constructor argument or theorem supplying .th, preserving its hypotheses. At that application, determine the instantiated place/index domains and EMtTheta antecedents. If the route only transports an existing witness, record that boundary and trace the original supplier. Do not turn a conditional existence lemma into an unconditional claim.

## Outstanding work

This targeted phase does not complete Daniel's second control, full unknown-reason census, larger-budget LedPart.pt probe, provenance/instance/generated strata, or fixed use-classification sample. It is not a new independent kernel check. Comparator is not inspected, stopped or reconfigured.
