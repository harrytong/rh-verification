# Stage 3.2: domain boundaries and obligation chains

Prepared 23 November 2026, before executing the new project probes. Package v0.3.
This protocol is informed by the completed v0.2 run, not preregistered before
that earlier run. Its hash is recorded in every new run's metadata.

## Question and prior evidence

The v0.2 supplier accepted an arbitrary `Γ : GeoP`, including False, while keeping
the original unitary-group hypotheses. Its conclusion changes with Γ. The
source `OverIx.lean` defines `OAt Γ` with both `geo : Γ ...` and `lam : LamAre ...`.
Thus successful generalization does not itself establish independence from a
geometry condition, construction of a point, or necessity of a trivial witness.

The previous evidence ZIP has SHA-256
`80399d497943c10776ea5986600456424cb8e20b734546999e56a1e43b85805e`.
We read its logs and source snapshots; this authoring environment did not
independently rerun that Lean computation.

## Fixed probes

### D: Local domain boundary

`DomainBoundary.lean` attempts five theorems, with all external object parameters
universally quantified and no existence assumption added:

1. `Nonempty (OAt Γ t X)` iff the corresponding Γ predicate AND `LamAre` hold.
2. `Nonempty (OAt anyGeometry t X)` iff `LamAre` holds.
3. No inhabitant of `OAt False t X`.
4. No proof of `GeoCl False D J X` (repeat the previously accepted induction).
5. No inhabitant of `OAt (geoCl False) t X`.

Success establishes exactly these local domain statements. It does not prove
that `LamAre` has mathematical content at the selected points, that the entire
open package is vacuous, or that the original proof uses an empty domain.
In particular, `OAt anyGeometry` remains subject to its other field. The code
does not produce an inhabitant without that field's proof.

The toy fixture checks analogous record statements without importing Main.
Its success is a tooling check, not validation of the project theorems.

### W: Comparison witness obligations

Print the exact stored declarations and axiom dependencies named in
`chain-targets.json` for `witness-chain`: the class-sum and linked-ties suppliers,
the weak-compatibility supplier, and the three selected consumers. Source
snapshots already show how these applications connect. The purpose is to expose
the next premise and witness, not infer necessity from occurrence.

Review the comparison witness's type and each argument receiving its properties.
Distinguish a proof of a premise from ordinary data and incidental references.
Do not count this purposefully selected chain as Daniel's representative census
sample. If a proof rendering is abbreviated, resolve it from the pinned source
or a subsequent explicit typed application before claiming a complete use trace.

### H: Height comparison obligations

Print the five stored declarations listed for `height-chain`, including the
geometric bound at a place, its conditional supplier, the mean-bound consumer,
the cover-height equation and the cover-height comparison.

Review which point and height occur in each conclusion and which premises supply
their relationship. The previously established existing-point round trip does
not supply an intrinsic-height agreement for arbitrary LedPart data. A printed
lemma with a matching name is not evidence that the final mathematical quantity
has been identified correctly.

## Evidence and decision rules

- Each positive step requires exit status zero AND its terminal markers. Every
  error is retained, with the first Lean error initially classified as requiring
  manual review. Later steps do not run after failure.
- The deliberately negative fixture must yield the specified type mismatch.
- Missing declaration, missing import, elaboration/interface error, unavailable
  mathematical premise, and resource exhaustion must be distinguished. None
  automatically refutes the submitted proof.
- Chain output is split into named begin/end blocks. Missing, duplicate, empty,
  or out-of-order blocks fail collection. Line positions, rendered-text hashes
  and visible elision counts are recorded. An absence of elision characters
  does not certify a complete raw expression.
- Main is imported throughout the project probes. These are local theorems and
  inspection commands in the original environment, not a reconstruction that
  excludes the disputed route, nor a fresh independent kernel verdict.
- Preserve every outcome, including failed and partial runs. Report no new
  RH/GRH verdict, necessity verdict, or resolution of the critics from this
  collection alone.

## Source and execution limits

Twelve fixed source roots and one level of recognized project imports are
requested in `source-requests.json`, at most 160 considered files, 2 MiB per
file and 8 MiB total copied. Bytes are checked against the pinned git revision.
Missing paths and caps are recorded. This is bounded source context, not the
complete proof closure or a search establishing absence.

The `obligations` sequence is fixtures, domains, witness-chain, height-chain.
Individual steps are available for subsequent focused reruns. Default limits
remain 2 logical CPUs, 100 GiB memory without additional swap, 1,800 seconds per
project process, and 64 MiB per log. The runner requires 21 GiB disk free and
116 GiB available host RAM before default project probes. It imports read-only
compiled files, does not build Main or copy the proof export, and never queries
or controls Comparator.

## Stage 3 still outstanding

The census work remains separate: a second control under the identical
classifier, project/library and instance/non-instance strata, all-unknown
accounting with exact budgets, the larger-budget `LedPart.pt` classifier probe,
and fixed sampling followed by use classification. The new named-case tests
must not be reported as completion of those requests. Daniel's review of prior
records was not an independent reproduction of the runs.
