# Stage 3 v0.6: class-sum supplier and targeted argument occurrences

Reviewed 23 November 2026. This report evaluates Harry Tong's uploaded evidence from `stage3-t6g8w4fr`. It is an inspection of recorded output and collected source, not a fresh execution of Lean or an independent reproduction of the server run.

## Conclusion

The probe completed successfully and strengthens the evidence for **local argument use**. Three selected binders were found in stored proof-body application expressions. The source trace also identifies a specific obligation behind the class-sum certificate: an `EMtTheta` proof extracted from the `.th` field of an extension record.

This does not establish that `anyGeometry` is necessary, unnecessary, or invalid. It does not settle RH/GRH or the critics' objection. Two bounded searches were inconclusive. The next meaningful target is the construction of the extension record and its `.th` field at the relevant instantiation, together with the inhabitedness and interpretation of the domains involved.

## Evidence and integrity

- Uploaded archive: `stage3-evidence(5).zip`.
- Archive SHA-256: `a809a74f9a95d7cd877777872e1c0ff86278e528bb4059ea29ba6c94282e7421`.
- All 257 entries in `EVIDENCE_SHA256SUMS` and all 79 entries in the package's `SHA256SUMS` matched the extracted bytes.
- Recomputed targeted-search, provenance, declaration-block and both fixture summaries from the logs using the previously delivered v0.6 Python runner; all five matched the archived JSON summaries.
- The recorded before/after hashes for the selected inputs are identical. This checks the listed inputs, not every file in the compiled environment.
- All 160 collected source files match their recorded SHA-256 values. The runner records these as checked against the pinned Git source; this review did not independently fetch that Git revision.
- Source pin: `753431bfe28701f6f3937f664fcaf08daa139c03`.
- Mathlib pin: `0df444a360eaa60ab8c11dca51a86af692955474`.
- Proof inspection used the recorded Lean 4.33.1 executable, distinct from the Comparator's judging toolchain.

The run lasted from 03:31:45 to 03:34:13 EST. The project probe took 2:20.39 and exited with status 0; maximum reported RSS was 52,128,544 KiB, approximately 49.71 GiB. Positive, provenance and search fixtures passed. The negative fixture produced its expected type error. These fixture results validate the tested tool behavior, not RH.

The eight inspected declarations' reported axiom lists contain only `propext`, `Classical.choice`, and `Quot.sound`. No new independent kernel run was performed. Comparator was neither inspected nor controlled by this phase.

## Targeted stored-expression results

The search omits binder-domain and let-type annotations, visits application arguments before functions, and stops at the first selected-binder occurrence. It does not unfold or normalize expressions. Limits are 100,000 visited nodes and depth 600 per search. A first occurrence is not an exhaustive use analysis or a necessity test.

Names in this table are abbreviated; full names and paths are in `targeted-occurrences.json`.

| Target / binder | Recorded result | Local application context | Nodes visited |
| --- | --- | --- | ---: |
| `GeoTies.linked_ties_alt` / `Γ` | Found; no limit reached before hit | Argument of `Mem.Top.Bl.parametersOfExtension` | 517 |
| `Fc.Ind.pNmj_of_pDiv_of_classSumPin_alt` / `hpin` | Found; no limit reached before hit | Argument of `T.lattice_family_adoption_fourth_alt` | 2 |
| `BigTop.PtAt.nmjT_at_tied_alt` / `hPin` | Inconclusive; node limit reached | No hit in visited projection | 100,000 |
| `ClassSumLift.eM_eq_thPe_alt` / `hP` | Found; no limit reached before hit | Argument of `ClassSumLift.at_index_alt` | 43,832 |
| `ClassSumLift.at_index_alt` / `hP` | Inconclusive; node limit reached | No hit in visited projection | 100,000 |

For each positive result, the selected application child is the binder's bound-variable expression. The recorded numbers of preceding application arguments are respectively 3, 20, and 17. These are syntactic application-spine counts; they are not a verified mapping to named explicit hypothesis parameters.

The `Γ` hit is particularly limited: it shows that the geometry parameter is passed into a parameter construction. It does not show a proof of `Γ D J X` being consumed. Even annotation-omitting traversal can encounter expressions that serve type-level or implicit-argument roles inside applications.

The two capped searches cannot support an absence claim. Earlier source inspection showed `hPin` passed onward and `hP` used in a rewrite; this run's failure to reach those occurrences does not contradict that source evidence.

## Newly resolved supplier trace

Paths below are relative to `collected-source/`. Let `TPS/` abbreviate `Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/`.

1. **`TPS/LinkedTies.lean`, lines 74–75.** `linked_ties_alt` obtains `hcs` from `GlobalTheory.T.class_sum_divisibility_of_extensionWithLaw`, passing `hL`, `N`, `S`, `Γ`, `hN` and the point/bundle witnesses. It uses `hcs.2` with a divisor-condition proof to supply the class-sum component.
2. **`TPS/ClassSumPinOfReadAtStatement.lean`, lines 20–21.** The named supplier is a wrapper for `GlobalTheory.ClassSumPinLink.pIota_classSumPin_alt`.
3. **`TPS/ClassSumPinOfReadAt.lean`, lines 81–95.** The implementation accepts a hypothesis `hN` that converts an inhabitant of the selected `N ... c` into `Nonempty (extensionWithLaw ... c)`. At line 90 it applies `hN` to `q.x.nx.2` and extracts a witness `m`. At line 91 it passes **`m.1.th`** into `eMtTheta_of_args_alt` to obtain an `EMtTheta` proof in the required coordinates. It then constructs `ReadAtAlt` and applies `classSumPin_of_readAt_of_pDiv` using the divisor hypothesis `hD`.
4. **`TPS/SameGaloisLevelExists.lean`, line 41.** `extensionWithLaw` is defined as `defaultExtension ... × PLift (BkLaw (w.D Z))`. Thus `m.1` is the default-extension component.
5. **`TPS/RootsOfUnityRingLeWittIntegers.lean`, lines 76–97.** `defaultExtension` is an instance of the structure `RealExpansionExtraData`. Its field `th`, at line 87, has type `EMtTheta Y r.nexp nch`. The structure also contains other requirements, including a `geo` field at line 85. The existence of that field alone does not establish its mathematical adequacy or necessity, and it should not be conflated with the separate parameter `Γ`.
6. **`Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/ClassSumDivisibilityBundle.lean`, lines 28–38.** `classSumPin_of_read` introduces the class-sum inputs, applies the supplied `hth : EMtTheta ...`, then rewrites using the sum equality, a theta-cast lemma, `hD.thTheta`, and the reading compatibility hypothesis `hjW`.

This is a concrete local explanation of where the certificate comes from. The inspected code transports and applies supplied mathematical conditions; the displayed supplier body is not simply `True.intro`. However, it moves the unresolved question upstream: **how is the relevant extension inhabitant constructed, how is its `.th` field proved, and what do these predicates mean at the actual inputs?** A conditional theorem carrying this obligation is not by itself evidence that the obligation has been discharged non-vacuously in the headline proof.

## Coverage limits

Provenance contains 2,896 reference entries summed over the eight targets' types and bodies, with no missing declarations and no reference-list truncation. This number is not a count of unique declarations or certified witness-discharge edges.

Source collection reached its 160-file cap: 1,446,412 bytes were collected and 225 queued paths were marked `file-count-cap`. Printed declarations contain 455 `⋯` indicators. Neither the printed output nor the collected source is a complete proof closure.

No replacement, abstraction rebuild, proof minimization, end-to-end necessity test, or proof of domain inhabitedness was performed in this run. Integrity checks preserve the relationship among this package's files; they do not independently certify every imported artifact or the intended mathematical interpretation of the headline statement.

## Next targeted work

Prioritize the supplier obligation over merely increasing whole-body scan limits:

1. Inspect the stored definitions of `RealExpansionExtraData`, `defaultExtension`, `extensionWithLaw`, and `EMtTheta`, with their owners and relevant constructor applications.
2. Trace the actual construction passed through `hN` on the previously identified route. Distinguish an assumed extension witness from a constructed one, and identify the term supplying `.th`.
3. At the relevant application sites, check the instantiated callee parameter types and argument terms. Separate geometry-index propagation from supplying a proof of a geometry condition, and separate local use from semantic necessity.
4. Check whether the specific quantified domains and premises are inhabited/satisfiable and whether the resulting condition corresponds to the intended mathematical assertion. Do not treat the presence of a `geo` or `th` field as an answer.

Daniel Fairbanks's broader requests remain separately outstanding: the second control, project/library/instance/generated stratification, complete unknown-reason accounting and the larger-budget `LedPart.pt` probe, and preregistered sampling with a reproducible witness-use classification. These targeted cases do not complete that census follow-up.

## Public wording

“Our latest audit located concrete uses of selected class-sum arguments in the compiled proof terms and traced the certificate supplier to an explicit `EMtTheta` obligation in an extension record. Two bounded searches remain inconclusive. We are now tracing how that obligation is constructed and used at the relevant inputs. These findings do not yet settle the geometry criticism or establish an overall RH/GRH verdict.”
