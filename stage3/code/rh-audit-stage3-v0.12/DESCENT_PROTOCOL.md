# Stage 3 v0.11: theta lift and coefficient descent

Frozen 23 November 2026 before this increment's project run. Selection is informed by v0.10 evidence, SHA-256 1cff7e206078852cc67a4523e029301367dfdb032241b2d82202f4e94dcb2f56. It is targeted, not random sampling.

## Question

What proves the theta-lift/class-sum identity invoked in the local-component construction? What does the proportionality theorem establish in its zero and nonzero cases, and how does the unit-existence theorem justify normalization?

Eight required targets are fixed in descent-targets.json. The first three are exact source calls in ThirdPlaceSeries/LocalComponentAtPlaceDetermined.lean: thetaLift_twistLevelForm_eq_unit_mul_classSum (line 72), chosenField_forms_proportional_of_readings (147), and exists_integral_unit_of_isUnitAwayFromLevel_embedding (151). Their owners are resolved from the compiled environment; no source filename is guessed. Three local implementations plus the definitions ThetaAt and EMtTheta provide context.

## Collection

Run unchanged positive, expected-negative and provenance fixtures before Main. Import Main once with ThetaDescent.lean. Record each target's owner, kind, stored type/body constant references, printed declaration and axioms. Require all targets in the fixed order, valid reference records, declaration blocks, exit 0 and the end marker. Preserve the first error and evidence on failure.

Source collection prioritizes all target owners, explicit caller/definition source, matching direct-reference modules, then imports to depth 2. Verify bytes against pinned git contents; record missing paths and caps. Preserve before/after input hashes, protocol/config hashes, full logs and manifests.

Limits unchanged: 2 logical CPUs, 100 GiB memory, 1,800 seconds per project step, 64 MiB per log, 4,096 references per location, 250 requested source paths, 2 MiB per source and 8 MiB total source. No project edits, rebuild, export copies, global traversal or Comparator inspection/control.

## Interpretation rules

1. For the theta-lift supplier, identify whether the body proves an identity, transports one, invokes another theorem, or receives the substantive identity through a hypothesis. Preserve the precise hypotheses and actual caller arguments where the source permits.
2. For proportionality, record which conclusion requires nonzero input. Distinguish a legitimate zero case and contradiction branch from a demonstration that all relevant inputs collapse. The latter requires a concrete instantiation and derivation.
3. For the unit supplier, inspect the embedding, integrality, nonzero and level assumptions. Do not equate a syntactically declared unit with a demonstrated nonzero value of every associated vector or space.
4. Compare ThetaAt and EMtTheta conditions: place restriction, index membership and representation equality. Complex formulas alone are not nonvacuity evidence.
5. Keep compiled references, source application sites and semantic necessity distinct. Pretty-printer elisions and source caps prohibit completeness claims. This phase adds no new argument-use extractor.
6. Standard axioms in a conditional theorem do not discharge its hypotheses. If an upstream obligation remains, report its name and exact role rather than announcing an RH/GRH verdict.

This phase does not complete Daniel Fairbanks' second control, all-unknown accounting, LedPart.pt probe, stratification or preregistered witness-use sampling. No independent-kernel or Comparator-completion verdict is produced.
