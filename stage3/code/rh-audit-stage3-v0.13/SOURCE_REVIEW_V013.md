# Source basis for v0.13

These observations precede the v0.13 Lean run. They are source readings, not new compiled results.

Project pin: `753431bfe28701f6f3937f664fcaf08daa139c03`.

1. v0.11 collected `Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/LocalComponentAtPlaceDetermined.lean:179` constructs `X` using `RealSide.ofPins x.m.z.geo x.m.z.pins x.m.intersectionNumber_baseChange x.m.inGeo ...`. The enclosing theorem is `GlobalTheory.PlaceRead.exists_local_map_at_place_alt`. This is a concrete caller on the route already investigated, not an arbitrary search hit for a constructor.
2. v0.12 collected `Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/OfFirstStepLoc.lean:17–25` defines `RealSide.ofPins`. Its `char` field is `RealDat3.characterisation_of_weak p.char h.aux.ex`.
3. v0.12 collected `Formalism/LocalToGlobal/IndefiniteReal/ZeroPartEigenvalueConvention.lean:272–274` calls `RealDat.thP_of_weak h.base.thP e` when constructing `Char3`.
4. v0.12 collected `Formalism/LocalToGlobal/IndefiniteReal/LinksW.lean:15` defines `OrZero p x` as `((∃ y, p y) → p x) ∧ ((¬ ∃ y, p y) → x = 0)`. `thP_of_weak` at lines 161–165 applies the first components of the weak properties to `ExAt` witnesses, including `e.thF i t`.
5. The same file's `PThF` requires membership, an integral-realizing theta operator, and equality of the selected function with that operator. `ExAt` includes existential witnesses for `ioP`, `thF`, `thG`, and other constructions.
6. v0.11 collected `Formalism/LocalToGlobal/IndefiniteReal/BaseLiftsPackageOfPrimitiveLinks.lean:224–228` declares `Formalism.IndefR.Links.UnusedChoiceStatements`, whose `ex` field is `R.toRealDat.ExAt`. Its name provides no evidence of whether the field is used.
7. The preserved `StableIffCarrierEq.lean:81–90` source declares `GlobalTheory.Mem.R3.Pins.char` and `Holds.aux`. The new run will recollect these owners against the pinned checkout.
8. v0.12 collected `OrthogonalComplementCharacterisation.lean:164–174` defines the integral and the integrability/equality fields of `Formalism.IndefR.Lift.IsThetaP`.
9. v0.12 collected `IntegralEqClassSumOfLe.lean:200` invokes the exact qualified name `GlobalTheory.Mass.Levels.measure_comap_finE`. v0.13 will obtain its stored declaration and owner directly rather than guessing its source path.

The v0.12 source cap omitted some useful upstream files. Explicit priority roots in v0.13 include the relevant records and state files. No global source search, global environment scan, or reconstruction of the full dependency graph is performed.
