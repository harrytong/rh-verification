# Source review leading to v0.5

Reviewed the v0.4 collected-source snapshots and prior pinned package sources.
These are findings from source reading, not new v0.5 execution results.

* ThirdPlaceSeries/NmjTAtTied.lean forwards hPin to
  GlobalTheory.T.lattice_family_adoption_third_alt and stores the result in eMj_th.
* ThirdPlaceSeries/EMEqThPeStatement.lean identifies the next implementation as
  GlobalTheory.ClassSumLift.eM_eq_thPe_alt. Its owner source was outside the
  previous bounded collection. v0.5 asks compiled provenance for that owner.
* ThirdPlaceSeries/EvWCOnPtOfGuarded.lean passes a PointConditions' witness
  into the supplied eventual implication. This alone does not show its ties
  field is essential.
* ThirdPlaceSeries/EventualL3OfCovolume.lean supplies that implication from
  CovolumeBoundOfX, forwarding the point-condition record with RecTied.
* ThirdPlaceSeries/TopCovolG.lean defines
  SelfIntersectionVolumeEstimates.topCovolG_alt_alt. Its proof combines height,
  covering degree, lower-bound, bad-locus and truncation facts to construct
  CovolumeBoundOfX. This is a concrete supplier to inspect, not proof that it
  is the unique or necessary headline route.
* The actual valuation definitions are GlobalTheory.CompHt.recVals and
  GlobalTheory.CompHt.htVals; the namespace is CompHt, not CovHt.
  The latter's source definition uses existential frame/valuation data.

Raw argument occurrence counts can help distinguish unused wrappers from
forwarding. They cannot determine mathematical necessity or geometric fidelity.
No new interpretation of the two critics' overall claims follows merely from
successfully running this package.
