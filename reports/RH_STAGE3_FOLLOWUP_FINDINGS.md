# Stage 3 follow-up findings: arbitrary geometry predicate and height preservation

Reviewed 23 November 2026. Evidence: Harry Tong's recorded `stage3-vmd5ehpj` run of package v0.2, phase `followup`. This review inspected the uploaded logs and source snapshots; it did not independently rerun Lean.

**Main result:** the selected open-package supplier generalizes to an arbitrary geometry predicate without adding a universal-truth premise. The height tests also confirm a preservation theorem for an existing-point round trip and isolate the exact agreement premise for arbitrary LedPart data. These are local results, not an RH/GRH verdict or a completed necessity analysis.

## Integrity and execution

- ZIP SHA-256: `80399d497943c10776ea5986600456424cb8e20b734546999e56a1e43b85805e`; matches the terminal output. Every entry in `EVIDENCE_SHA256SUMS` verifies.
- Protocol SHA-256 recorded in metadata: `2694032263c19550433ee122b9440ff3dc97a9dc6220631099335022636e7fd6`.
- Project revision `753431bfe28701f6f3937f664fcaf08daa139c03`; Mathlib revision `0df444a360eaa60ab8c11dca51a86af692955474`.
- Recorded selected input hashes agree before and after the run. The positive fixture passed; the negative fixture produced its intended type error. Boundary, suppliers, and geometry-general all exited 0.
- Run approximately 02:21:04–02:25:01 EST on 23 November 2026.
- Additional collection: 43 source files, 182,680 bytes. The collector records all 43 as matching the pinned git contents, with no missing-path or cap entries.
- Comparator was not inspected or controlled; no independent kernel check was performed by this package.

## 1. The arbitrary-predicate result passed

After the unchanged renamed baseline compiled, Lean accepted this schematic statement:

```text
for every Γ : GeoP,
  UnitaryGroupThirdPlaceHypotheses →
  for every hL and cDep,
    OpenParameterStatements
      (parametersOfExtension (extensionWithList hL cDep) SExt.none Γ)
```

There is no additional premise asserting `∀ D J X, Γ D J X`. The original unitary-group premise and other quantified inputs remain. The generalized proof retains the original helper calls and changes the predicate parameter and corresponding parameter-record applications, as documented by the saved diff.

Lean also accepted its specialization to `Γ := fun _ _ _ => False`, and separately accepted that `GeoCl False` has no inhabitants. All three new geometry theorems report only `propext`, `Classical.choice`, and `Quot.sound` as axioms.

This is stronger than Stage 2's transport result, which assumed a universally true predicate or closure. It establishes that this particular local supplier can be generalized without that assumption. It does not generalize the five headline theorems or remove dependencies from imported helpers.

Evidence: `geometry-general.log` lines 3–13, 2192–2204, and 2330; `GeometryGeneral.lean`; `SupplierGeneralization.diff`.

## 2. Why the False specialization is not a contradiction

The predicate parameter also changes the objects described by the conclusion. In the supplied source:

- `Parameters.s` places `OX p.Γ` into its slots.
- `OX Γ` is built from `OAt Γ`.
- An `OAt Γ` record contains a proof field `geo : Γ ...` as well as `lam`.
- `LinkedAt`, `Row`, `RowE`, and `IsSel` involve linkage and selection conditions and implications over eligible objects.

Thus a theorem about all eligible objects need not produce an eligible object when the predicate is False. The source already shows that an `OAt False` record would require a proof of False. The current package did not compile an explicit theorem tracing this emptiness through every enclosing linkage/selection layer, so it does not certify complete vacuity of the entire package.

The correct inference is limited: this supplier does not require an extra universal-truth premise for Γ. One cannot infer that Γ is unnecessary in the whole proof, nor that an empty-domain version proves RH.

Evidence: `sources/.../AutomorphicMembership/OverIx.lean`; `sources/.../ThirdPlaceSeries/CoreAltAltBis.lean`; `suppliers.log` lines 7031–7120.

## 3. The compatibility witness has an identifiable supplier and consumer

The newly collected `RowGeo0At.lean` shows that `geometricWeakTies_of_linked_ties` combines:

1. `class_sum_divisor_all_alt`, supplied with ray-field, extension, and divisor premises;
2. the linked-ties premise, from which it obtains a comparison witness `t`;
3. the properties of that same `t`, repackaged as geometric weak compatibility.

`RowGeoAtGridA.lean` follows the same pattern and adds the grid condition through `grid_field_has_lattices_alt` using the compatibility proof.

On the consumer side, `EvWPRowsOfRows.lean` passes `ClassSumPin` to `pNmj_of_pDiv_classSumPin` and passes `CompatibilityConditions` to `bundle_lines_of_primitive_frames_div_nmj`. This is a concrete local chain of proof arguments, beyond a membership entry in the large closure. It is not a proof of indispensability after simplification, nor an independent validation of the nested mathematical definitions.

`ClassSumPin` itself is printed and supplied as source: it is a quantified equality involving class-sum data and tensor products under stated hypotheses. It is not syntactically the definition `True`. We have not established that it is nontrivial on the particular objects used by the headline proof.

## 4. Height: a real special case and an explicit general boundary

All four new height propositions compiled. In abbreviated notation they establish:

```text
Original-height agreement → assigned height equals original height

(LedPart.ofPt p).pt.D.div.h = p.D.div.h       for p : Pt C

(∀ u, p.pt.D.div.h u = D.div.h u)
  ↔ (∀ u, D.div.h u = hExpl6 D p.L Y.X C.Csz u)
```

The pointwise round-trip equation compiled as well. All four report only the three standard axioms above.

The round trip uses the project's existing `pt_ofPt` theorem. Starting with a `Pt` supplies its height contract already. This is important positive evidence about that conversion, but it does not supply the agreement premise for arbitrary `LedPart` data or identify the stored height with a separately specified intrinsic height.

Evidence: `boundary.log` lines 3–605; `HeightBoundary.lean`; `SetUnipotentTranslate.lean` lines 456–468.

## 5. Next targets and outstanding work

The next geometry targets are `class_sum_divisor_all_alt` and the comparison-witness supplier behind the linked-ties premise. The next consumer targets are `pNmj_of_pDiv_classSumPin` and `bundle_lines_of_primitive_frames_div_nmj`. They narrow the investigation to the exact obligations being supplied and used.

For height, the collected `HeightLowerBoundGeneral.lean` calls `height_of_meanAll_bound` with a geometric-bound result. `GeometricOfHyp.lean` reaches `geometric_height_bound_at_place`. The connection between these estimates, the assigned record height, and the final required quantity still needs explicit review; it has not been established by the four equations alone.

Printed terms still contain elisions: 16 in the boundary log, 302 in suppliers, and 43 in geometry-general. Accepted declarations and exit status establish the local compilation results, but these renderings are not complete raw proof-term exports.

Daniel Fairbanks's full control comparisons, origin/instance strata, preregistered use samples, exhaustive unknown accounting, and larger-budget classifier retries remain outstanding. This named-case follow-up is not a replacement for them.

**Publication-safe conclusion:** the local geometry supplier passed an arbitrary-predicate abstraction test without a universal-truth assumption, and the height conversion preserves height in the existing-point round-trip case. The effect on the intended RH/GRH proof remains under investigation. No claim that the critics have been refuted, or that their allegation is established, follows from this run.
