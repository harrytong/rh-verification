# Stage 3 v0.12: integral identity and supplied theta realization

Fixed 23 November 2026 before this increment's project run. Selection follows v0.11 evidence archive SHA-256 `6529451a52fb9ce02ce165537494c985824ad93ca1c5f742c950a401ae1df762`. This is targeted inspection, not random sampling or a new independent-kernel check.

## Questions

1. What are the exact hypotheses, conclusion and implementation of `GlobalTheory.LiftUnfold.integral_theta`?
2. What does `thF_eq_princ` obtain from `hC.thP.thF`, and how are those supplied equalities connected to its invocation of the integral identity?
3. What do `Hk3.Core`, its `thP` field, `RealSide.char` and `RealDat3.Char3` require? Identify any further realization record or field by its stored qualified name and owner.
4. What do the two dilation suppliers used by `flat_eq_unit_smul_om` actually prove and require? Which assumptions ensure nonzero scalars, and which, if any, ensure nonzero vectors or nonempty domains?

Eleven targets and their order are fixed in integral-targets.json. Names come from v0.11 collected source or compiled reference records. The Core projection is grounded in its structure field; Char3 is grounded in the compiled qualified projection names and RealSide's field type. Missing targets fail the phase; there is no fuzzy-name fallback.

## Collection and limits

Run unchanged positive, expected-negative and provenance fixtures, then import Main once using ThetaIntegral.lean. Record owner modules, declaration kinds, stored type/body constant references, printed declarations and axiom reports. Require all targets in order, valid reference records, declaration blocks, exit 0 and the final marker. Keep the first failure and evidence archive if any step fails.

Source collection prioritizes target owners, then explicit caller/record sources, selected reference modules and imports to depth 2. Preserve source verification records, omitted/capped paths, before/after input hashes, protocol/config hashes, complete logs and manifests. A collected source snapshot is not independently shown to be byte-for-byte the source that produced an imported compiled declaration; stored references and source inspection remain distinct evidence layers.

Unchanged limits: 2 logical CPUs; 100 GiB container RAM; 1,800 seconds per project step; 64 MiB per log; 4,096 references per location; 250 source paths; 2 MiB per source file and 8 MiB source total. The runner requires 116 GiB MemAvailable and 21 GiB free disk. No project edits, rebuilds, export copies or Comparator inspection/control.

## Interpretation fixed before results

- Distinguish an integral identity from the hypothesis identifying the supplied theta object with that integral. Preserve both sides, quantifiers and assumptions when summarizing the connection.
- A proof field in a structure is a hypothesis at this use site. Its presence is neither an additional axiom nor evidence that the final theorem assumes its own conclusion. Trace its constructor or supplier before making such a claim.
- For each reviewed invocation, record actual caller expressions as far as source and output permit. Stored constant references alone do not establish which argument discharges a hypothesis.
- Separate nonzero scalar conditions, nonzero vector conditions, inhabited domains and faithful/injective maps. None automatically substitutes for the others.
- A zero or unit-valued construction is not itself a defect. A counterexample, inconsistent semantic identification, demonstrably vacuous relevant premise, or another explicit defect is needed to substantiate a criticism.
- Successful local inspection does not establish that this route is necessary, that all definitions match the intended mathematics, or that the full RH/GRH proof is correct. No absence claim may be based on bounded source collection or elided pretty printing.
- If the substantive obligation moves into another field or theorem, identify that obligation and the specific caller argument. Do not replace the unresolved question with a success verdict.

This phase does not implement Daniel Fairbanks' second control, full unknown accounting, LedPart.pt probe, category stratification or preregistered witness-use sampling. Those remain separate unfinished work.
