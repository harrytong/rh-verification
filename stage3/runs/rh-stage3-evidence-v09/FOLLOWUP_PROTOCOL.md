# Stage 3.1: supplier generalization and height boundary

Protocol prepared 23 November 2026 before running these new Lean experiments.
Package version: 0.2. This is another bounded increment, not completion of Stage 3.

## New source observations, not experiment results

The pinned `OpenOrbitOfUnramifiedExponents.lean` constructs the twelve-field open
package. Its `hGeo` is supplied by `linkedAt_geometricWeakTies_of_tie` using
`P.rayClassFieldSt`, an extension implication, `hDiv`, and `hTie`. Its existence
is not justified merely by typing `True.intro` at this application.

`SetUnipotentTranslate.lean` already supplies `GlobalTheory.EX.OB.pt_ofPt`:
starting with a `Pt C`, converting to `LedPart` and back preserves the lattice
and height fields. The height proof uses the starting point's `xa.h_eq` contract.
This special case must not be presented as preservation for every arbitrary
`LedPart C Y`, or as a comparison with an independently defined intrinsic height.

`Row` and `RowE` quantify over selected/linked objects and include implication
premises. A supplier accepting an arbitrary predicate might restrict its domain
rather than construct witnesses satisfying every predicate. Successful
specialization to False would therefore require a domain/nonemptiness review.

## Frozen experiments and interpretations

1. **Height boundary:** check height preservation under an explicit agreement
   premise; check the existing round-trip case as a new explicit theorem; check
   the equivalence between preservation and that agreement premise. These tests
   do not assert that the premise is available for the headline proof.
2. **Supplier collection:** print the two geometry suppliers, compatibility
   predicates, domain/selection definitions and the next covolume supplier.
   Record bounded additional source context from the pinned git revision.
   Printed terms can still contain elisions: no complete-use claim is authorized.
3. **Geometry baseline:** compile a renamed exact copy of
   `open_orbit_of_unramified_exponents_alt` before its generalization.
4. **Geometry generalization:** replace every explicit `geoCl anyGeometry` in
   that copied body with a universally quantified `auditGamma : GeoP`; expand
   the two `parametersOfDependence` applications to the corresponding
   `parametersOfExtension ... auditGamma`. Make no other proof-body change.
   No `forall D J X, auditGamma D J X` premise is added. The exact diff is saved.
5. **False boundary:** specialize the generalized supplier to False and check
   separately that `GeoCl False` has no inhabitants. The supplier remains
   conditional on the original unitary-group hypotheses. It is not a theorem
   asserting the existence of a geometric point for False.

If the generic supplier compiles, it proves that this local supplier has the
generalized type in the imported environment. It does not remove the original
route from imported helpers, rebuild Main, establish a minimal assumption set,
or establish that geometry is irrelevant to the headline theorems.

If it fails, preserve the first elaboration error and its full log. The runner
labels it unclassified. Manual review must distinguish a type/interface problem,
an unavailable premise, a resource limit, or an audit-tool error. Failure alone
does not refute the submitted proof. A baseline marker is recorded separately;
Lean may continue processing commands after an error, so no marker overrides a
nonzero exit status or demonstrates success of an earlier declaration by itself.

## Collection and resource scope

The new `followup` phase runs fixtures, then height boundary, supplier collection,
then generic geometry. It stops and archives evidence on a failure. Already
completed steps need not be repeated: each named phase can be run separately.

Additional source requests are six explicit roots and one level of recognized
project imports, maximum 120 considered files, 2 MiB per file, 8 MiB total copied.
Files must match the pinned git blob; caps and unavailable paths are recorded.
This collection is not a complete dependency graph and does not establish absence.
The roots, limits, and source index are included in the evidence.

The existing isolation is retained: separate capped containers, read-only mounts,
2 logical CPUs, 100 GiB RAM by default, 64 MiB maximum log per step, no project
builds or export copies, and no Comparator inspection or control.

## Daniel's remaining requests

These experiments address local use and the interpretation of abstraction, not
the full census follow-up. The second control, identical classifier denominators,
origin/instance strata, all-unknown logging and targeted budget retries, and
preregistered sample-use classification remain outstanding. Their original
selection rules in PROTOCOL.md and PARENT_PLAN.md remain in force. Do not publish
the new named-case tests as representative samples or as fulfillment of all
Stage 3 requests.
