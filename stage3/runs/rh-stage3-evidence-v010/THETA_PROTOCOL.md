# Stage 3 v0.9: theta identity and reading relation

Frozen on 2026-11-23 before this increment's project run. Informed by completed v0.8 evidence, archive SHA-256 d2c2e5b5b612cd06cb0dbea5c5ecacfbbadfd4439c94bcfc3909a1517722c309.

## Question

The v0.8 source located an explicit RealExpansionExtraData constructor in Fin3.nonempty_nMore_of_xdAll, assigning .th through T.emtTheta_of_yRel and .geo through a separate supplier. The theta wrapper delegates to Fin3.emtTheta_L_alt. This phase inspects that implementation, the producer of YRel, the relation definition, the instantiated expansion/character data, and the relevant construction call sites.

The ten required targets are frozen in theta-targets.json. Names are grounded in v0.8 source; their compiled availability is checked by the actual server run. The selected declarations include both the wrapper and implementation so that their direct compiled reference relationship can be checked. No new mathematical lemma is asserted by the probe.

## Execution and evidence

1. Positive and expected-negative fixtures, then the unchanged provenance fixture. Failures stop before Main.
2. One Main import for ThetaIdentity.lean, using the byte-identical established provenance helper. Report stored declaration kind, owner module and direct type/body constants; print each declaration and its axiom list inside indexed markers.
3. Every target is required. Validate ordered target/reference records, normal process exit, end marker and nonempty declaration blocks. Preserve the first error and archive evidence on failure.
4. Collect target owner source files first, explicit priority files next, matching direct-reference modules next, then project imports breadth-first to depth 2. All non-seeded reference modules remain listed in the provenance/selection records. Optional missing source paths and caps are explicit.
5. Keep protocol/config hashes, before/after input hashes, all logs, source index/hashes and final evidence archive checksum.

Limits remain: 4,096 references per location; 250 requested source paths, 2 MiB per source and 8 MiB total source; 2 logical CPUs, 100 GiB memory, 1,800 seconds per project step and 64 MiB per log. No global traversal, source mutation, rebuild, export copy or Comparator control. No repeated capped binder searches.

## Review rules fixed before results

- Trace the actual body of emtTheta_L_alt. If it invokes an earlier theta theorem or record field, name that supplier and preserve its inputs. Merely reaching another supplier is not a nonvacuity result.
- Inspect the producer of YRel and distinguish a direct construction of the relation from accepting it as an assumption or transporting it.
- Inspect which fields of l, Y, yStructureLocal and characterChoiceLocal enter the identity. Record whether a conclusion follows from equality transport, algebraic reasoning, existing hypotheses, contradiction, or a combination, only where the body supports that description.
- Identify where the EMtTheta place inequality, index membership and representation-equality antecedent are introduced or used. A conditional implication can be mathematically appropriate; showing it is conditional does not show a flaw. Conversely, a complex formula or a named theorem does not establish nonvacuity.
- Keep direct compiled references, source application sites, printed expressions and semantic necessity as distinct evidence levels. Pretty-printer elisions are not complete proof terms. This phase does not claim exact compiled argument-use extraction for every source call.
- If the actual inputs collapse a condition, specify the exact instantiation and derivation. Do not infer this from names, True occurrences elsewhere, a census frequency or a missing source file.

## Remaining scope

This is targeted local inspection, not an end-to-end RH/GRH verdict or independent kernel check. It does not complete the second census control, all-unknown accounting, LedPart.pt larger-budget probe, project/library and instance/generated stratification, or preregistered witness-use sampling requested by Daniel Fairbanks.
