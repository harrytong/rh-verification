# Stage 3 v0.10: character-data construction and original theta supplier

Frozen on 23 November 2026 before the new project run. This protocol follows the completed v0.9 evidence (SHA-256 dbb49c17bb13c9f34cbaa9b0179473a4c9670f98f25f2db2cb4ee75e692a671d) and uses supplier names found in the earlier v0.8 pinned source snapshots. Selection is targeted and informed by prior results, not a random sample.

## Question and fixed targets

The localized theta lemma uses l.c.th. Does the supplier of that character-data record establish the original theta identity, transport another one, or take it as an input? What assumptions and instantiations support the supplier?

Twelve required declarations are frozen in character-targets.json. They include the character-data type, the level-existence condition, its wrapper and implementation, the choice-to-existence bridge, the third-stage wrapper and implementation, the non-Galois wrapper and explicit constructor, the local-component supplier, emtTheta_withE, and the localized theta consumer.

A name appearing in an earlier source call is grounds to inspect it, not evidence that the server lookup or its mathematical interpretation has already succeeded. Every required target must be present or the phase fails and retains the first error.

## Procedure

1. Run the unchanged positive, expected-negative, and provenance fixtures. A failure stops before Main.
2. Import Main once using CharacterConstruction.lean. Print each stored declaration and its axiom dependencies with paired markers; record its owner module and direct type/body constants using the unchanged provenance helper.
3. Require normal exit, final marker, all ordered targets, validated reference records, and nonempty declaration blocks. Keep all printed elision indicators and reference caps explicit.
4. Collect source owners first, then the explicitly prioritized roots, selected direct-reference modules, and their project imports to depth 2. Verify collected bytes against the pinned git revision. Record missing paths and all exclusions; a complete requested set is not a complete proof closure.
5. Preserve before/after input hashes, protocol and target hashes, logs, source index, and the evidence manifest/archive.

Limits: 2 logical CPUs, 100 GiB RAM, 1,800 seconds per project step, 64 MiB per log, 4,096 direct references per location, 250 requested source paths, 2 MiB per source file and 8 MiB source total. Retain the existing free-disk and available-memory checks. No proof-source edits, rebuilds, export copies, global graph traversals, or Comparator inspection/control.

## Interpretation rules fixed before execution

- Follow the source assignment to the character record's th field; do not infer its origin from its field type alone.
- Preserve the distinction between a locally available proof, a field projection, a theorem producing a witness under assumptions, and a closed headline proof.
- In exists_stC_choice_alt, trace the result named hc, its extracted e/u/hb/hl/hth witnesses, inverse-unit scaling, and the role of emtTheta_withE. Inspect the local-component theorem's own body and retained hypotheses before calling the theta identity substantive or vacuous.
- Record source applications separately from compiled direct-reference evidence. This phase does not extract all argument positions from compiled terms.
- Explicitly inspect whether relevant inequalities, membership conditions, index domains or representation equalities are merely forwarded, actually established, or discharged by impossibility. Any vacuity claim needs an exact instantiation and a derivation. Source names and empty types elsewhere are insufficient.
- Standard axioms in a conditional theorem do not eliminate its explicit hypotheses. A predicate named PublishedInputsThirdLayerAlt is not thereby an extra Lean axiom; inspect the actual declaration and its suppliers.
- A record constructor and a theorem about it can be legitimate even if another property is transported. Transport alone establishes neither circularity nor semantic necessity.
- If another supplier remains, report its exact name and obligation. Do not extrapolate to a global RH/GRH verdict.

## Unfinished broader audit

This phase is not the second census control, unknown-budget accounting, LedPart.pt probe, project/library and instance/generated stratification, or preregistered witness-use sampling requested by Daniel Fairbanks. It also supplies no independent-kernel or Comparator completion verdict.
