# Stage 4 v0.6 evidence review

Archive: stage4-evidence(5).zip. SHA-256:
`7730ef46b1439a1a4cb8e95be4f8cfa7cf847901c135558529fa6c39ecc81a98`.
All 83 files in EVIDENCE_SHA256SUMS verified. Input fingerprints before and after
the run match. Recomputing the v0.6 Python summary confirms incomplete coverage.
All requested processes finished as expected, including the negative fixture's
intentional rejection. Process completion and coverage completion differ.

## Compiled observations

The constructor supplies `R` with `RecNums.ofNum` and forwards its local `inp`.
Its `hTie` field is supplied through `ofOpen._proof_7`; its `rhs` field through
`ofOpen._proof_10`. Both field conclusion comparisons returned
`not-definitionally-identical`. This does not assess proof necessity or whether
their premises have the intended mathematical meaning.

The scanner did not unfold these referenced constants. Consequently its direct
searches in `ofOpen` for `hTie_of` and `rhs_le_record` returned no calls. The ten
selected arguments to those calls were not collected. This is an audit coverage
gap, not evidence that Lean accepted an absent proof. v0.7 targets the actual
helper names recorded by v0.6.

The `divClausesR_of` declaration record is truncated. Other rendered terms also
contain Lean's `⋯` elisions, even where the character-cap flag is false. Do not
describe these as complete proof-term dumps.

## Pinned source observations

The source collector returned 16 files with no selection cap or omission,
verified against pinned Git contents. Paths below are relative to
supplier-source/collected-source in the v0.6 evidence.

1. `Formalism/LocalToGlobal/Divisibility/ConstantGeTwentyEight.lean`, lines 184–247:
   `divClausesR_of` constructs all four conjuncts of `DivClausesR`. It separates
   zero-map and nonzero-map cases for the norm witness. The nonzero branch uses
   `height_chain_atR` and input bounds. The third conjunct derives intermediate
   bounds and finishes with `R.divIneq ... hC hM hpass I.errB`. The local `rfl`
   at line 243 expands `boundBR`; it is not the entire third-conjunct proof.
2. `Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/InpAtOf.lean`:
   `inpAt_of_alt` constructs inputs using row witnesses, arithmetic data,
   `DivisionInputsWithoutNorm.ofRows`, `toDef`, and `toDivInputs0R`. Its existence
   rebuts an inference that the presence of an `inp` parameter alone means no
   supplier was written. It remains a conditional construction.
3. The adjacent `Wire4F.lean` explicitly calls `inpAt_of_alt`. Arithmetic witnesses
   are obtained from `arithClause_rec`; row witnesses flow from the local `hd`
   obtained through the theorem's row assumptions. This traces one more source
   layer; it does not independently establish every premise in the final proof.

## What follows and what remains open

At the inspected local layer, the height estimate has a proof assembled from
named bounds and input fields. Calling this entire layer merely an `rfl`
identity is unsupported by these sources. That narrow observation does not
resolve criticism of other height definitions, geometry witnesses, upstream
premises, or the final theorem's intended meaning.

The next bounded check inspects the two recorded compiled helpers. Broader
questions require the concrete upstream witnesses and an exact mapping to each
critic's claim. No new Comparator or independent-kernel result was collected.
