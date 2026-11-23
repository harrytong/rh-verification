# Stage 3 v0.13: existence witnesses at the zero-fallback boundary

Fixed 23 November 2026, before this increment's project execution. The selection follows v0.12 evidence SHA-256 `93cba55fe65cdde9f6f7028286f8f1eeedce82d47d2d9ad0a7555fb880ef20b4` and the earlier v0.11/v0.05 source snapshots identified in SOURCE_REVIEW_V013.md. This is targeted inspection, not a census or an independent kernel replay.

## Questions fixed before the run

1. Does the compiled body of `GlobalTheory.PlaceRead.exists_local_map_at_place_alt` reference `RealSide.ofPins`, matching the concrete source call on the previously traced route?
2. What arguments does `RealSide.ofPins` supply to `RealDat3.characterisation_of_weak`? In particular, preserve `p.char` and `h.aux.ex`, rather than describing the resulting record as an unconditional existence construction.
3. How does `RealDat.thP_of_weak` turn `IsThPW` into `IsThP` using `ExAt`? Which existence witnesses enable the `OrZero` properties to yield the required theta properties?
4. What exactly do `ExAt.thF`, `PThF`, and `Lift.IsThetaP` require, including integrability and equality with the integral?
5. Where do `Holds.aux`, `UnusedChoiceStatements.ex`, and `Pins.char` come from at this boundary? Collect their owner modules and source context so the next provider can be identified without guessing from names.
6. What are the exact hypotheses of `GlobalTheory.Mass.Levels.measure_comap_finE`, the normalization helper identified in v0.12?

The 17 targets and their order are fixed in realization-targets.json and chain-targets.json. Names are grounded in preserved source or prior references; projection names come from declared fields. Missing names fail explicitly; no fuzzy fallback is used.

## Procedure

Run the unchanged positive, expected-negative, and provenance fixtures. Then import Main once, inspect the 17 stored declarations, and record owner modules, declaration kinds, direct type/body constant references, printed declarations, and axiom lists. Compile two conditional lemmas about the actual imported `OrZero`: an existence witness gives the selected value's property, and absence of any witness forces the selected value to zero. These lemmas do not produce `ExAt`, prove nonvanishing, or identify the actual headline branch.

Require all target records and declaration blocks in order, exit status 0, and both final markers. Preserve the first error and logs on failure. The runner records protocol/config/package hashes, resource limits, source provenance, and before/after input hashes.

Source collection prioritizes target owners and the explicit constructor/record files, followed by selected reference modules and imports to depth two. Cap at 250 requested paths, 2 MiB per file, and 8 MiB total. Omitted paths are recorded. This is bounded context, not a full reference closure; in particular no absence claim is licensed by a missing snapshot.

The existing runtime limits remain: 2 logical CPUs, 100 GiB RAM, 1,800 seconds per project step, 64 MiB per log, and 4,096 references per location. Require 116 GiB MemAvailable and 21 GiB free disk before a project step. No edits to the proof checkout, rebuild, export copying, Comparator inspection, or Comparator control.

## Interpretation rules

- `OrZero p x` alone does not establish `p x`. Its existence premise must be supplied before interpreting its first component as a valid witness.
- With an existence witness, the first component establishes `p x`; this does not imply `x ≠ 0`, since zero may itself satisfy `p`.
- A record called `UnusedChoiceStatements` is not presumed unused. Track actual fields and applications.
- A constructor requiring `Holds` and `ExAt` transfers an obligation; it does not prove those inputs exist. Identify their providers before claiming non-vacuity or circularity.
- A stored reference establishes syntactic reference, not necessity. Preserve quantifiers, domain restrictions, and all remaining hypotheses when explaining the route.
- An integral identity, an integrability witness, measure normalization, and nonzero values are different assertions. Do not use one as a substitute for another.
- Successful collection is neither an RH/GRH verdict nor a demonstration that the criticized geometry is indispensable or dispensable. A local counterexample to an overstrong interpretation would concern that interpretation, not automatically the headline theorem.

This increment does not perform Daniel Fairbanks' second control, exhaustive unknown analysis, project/library stratification, or preregistered use sampling. Those work items remain separate. It also does not construct the entire upstream ExAt witness in advance: its purpose is to inspect the concrete boundary and identify the next supplier precisely.
