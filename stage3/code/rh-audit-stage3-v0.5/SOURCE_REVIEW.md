# Stage 3 initial source review

This is a review of saved source at the recorded project revision, not a report
of executed Stage 3 Lean tests. Source files and SHA-256 values are bundled in
source-manifest.json. The runner compares their bytes with the server checkout.
Source excerpts do not replace the stored-term audit or the pending Comparator.

## Geometry: two different fields named geo

In AutomorphicMembership/OverIx.lean, line 19 defines anyGeometry to return True.
At lines 44–47, OAt contains BOTH a geo field asserting Γ at the selected object
and a lam field asserting LamAre. The definition of LamAre (lines 32–39) includes
an existential choice of labels and equalities involving logLam and Real.log.
Setting Γ to True removes the restriction in that one geo field. It does not,
by that substitution alone, discharge LamAre.

In ThirdPlaceSeries/GeometricWeakTies.lean, lines 36–38 define
GeometricWeakCompatibility' using an existential comparison witness t and a
conjunction of IotaPointSummands, ClassSumPin, CompatibilityConditions and More.
OpenParameterStatements.geo (line 48) is a LinkedAt statement about that predicate.
It is NOT simply the geo field of OAt under another spelling. Whether its nested
conditions have substantive content requires further inspection.

In LinkedBundlesL3OfOpen.lean, lines 33–44, the proof combines o.geo with other
conditions, obtains hgeo, and uses `choose τ hτ`. Components of hτ are supplied to
the construction of hrows, and the result is used with hCov to obtain the L3 bound.
This is an explicit source-level producer-consumer route worth checking. It does
not by itself show which part of hgeo depends on anyGeometry or is indispensable.

RowFunAtGridA.lean similarly obtains a geometric condition through
geometric_condition_large_grid_alt using o.hDivG and o.tie. It chooses τ and uses
selected hτ components in subsequent lemmas. Thus observing the literal predicate
argument alone leaves substantial surrounding obligations unexamined.

The three literal `geoCl anyGeometry` applications in
SiegelEisensteinSecondTermHypotheses.lean are at lines 60, 63 and 67. They go to:

1. open_and_linked_of_stronger_extension_alt (producing hMono);
2. the quantified result hCF0 obtained from rowFun_at_gridA_alt (producing hFun);
3. linked_bundles_l3_of_open_alt (producing hL3).

The geometry probe retains all three and exposes their local context. The final
consumer is hypotheses_nonempty_of_unramified_exponents_alt. Our previous universal
P transport rewrote back to the specialized closure at these boundaries; it did
not establish necessity or remove this route.

## Height: a constructed object rather than the original object

GlobalTwisting/SetUnipotentTranslate.lean, lines 25–31, defines setDiv by replacing
the divisor submodule data and the height field h in D. It also changes HH and
provides its bound. This is visibly an object construction in the source.

At line 379, LedPart.ht is hExpl6 evaluated on the original D, p.L and Y.X. At
lines 381–401, LedPart.pt builds a point whose D is `setDiv D (nPrime p.L) p.ht`;
its size/divisor data are transported using ledTr and divTr. The field h_eq is
filled by `fun _ => rfl`.

In InertJacobiLevels/AsmIface.lean, line 163, ExtraAt.h_eq has the contract:

```lean
∀ u, D.div.h u = DV.hExpl6 D L X C.Csz u
```

When supplied by p.pt.xa, D/L/X are the constructed point's data. Our height
probe makes those substitutions explicit. A successful rfl check on the new
object would not assert that an independently fixed original height was equal
to this formula. The next substantive question is which later bound uses the
construction and how it is connected to the required analytic quantity.

hExpl6 itself, in LocalRingCardinality/KernelPlaceMeanBound.lean lines 25–27, is a
formula involving SZbP, finite sums of kernelPlaceMeanBound and L6lo, and a mean
of logarithms. Its classifier timeout cannot be read as evidence that it is zero
or trivial. No new classification result for LedPart.pt is available here.

## Conclusions currently supported

- There are concrete local applications and field contracts to inspect.
- `anyGeometry = True` is confirmed in the saved source; it does not imply that
  every condition in OpenParameterStatements is True.
- The rfl height field belongs to a constructed object with reassigned data.
- Neither observation proves or disproves RH, resolves necessity, or completes
  the critics' mathematical argument. The exact typed probes and subsequent
  consuming inequalities remain the next evidence to collect.
