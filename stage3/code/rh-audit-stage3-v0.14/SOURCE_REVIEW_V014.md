# Source basis for v0.14

No new online claims are incorporated. Targets are selected from preserved local evidence.

- v0.13: ReadPk.lean declares GlobalTheory.Mem.R3.Rw.Moved and its intersectionNumber_baseChange and exAt fields.
- v0.13: NonzeroPlacesOverPrimesLifts.lean, namespace GlobalTheory.Mem.R3.Rw, declares St, HasBare, and WeightCaseCondition.
- v0.13: NonzeroPlacesOverPrimes.lean, namespace GlobalTheory.Mem.Top.Bl, declares Start, DatEx, and UnitaryCaseCondition.
- v0.13 compiled provenance identifies all ten GlobalTheory.TwInputs.RealSide.ofPins._proof_n names and the owner module of GlobalTheory.HeightCounting.Up.AllSt.
- Preserved v0.09 source StrictHenselianAcyclic.lean explicitly defines AllSt as StepW Start followed by universal quantification over Pre2 and St.
- Preserved v0.09 source ExistsMovedDataStateLocalisationsStatement.lean explicitly declares GlobalTheory.T.exists_movedData_state_localisations and invokes GlobalTheory.HeightCounting.Fin3.MvLoc.exists_moved_loc. Its input includes x : St P. This is not identified as the initial state provider.
- Moved.mk and St.mk are expected constructor names for the recorded structures; server inspection must confirm their presence. Other target names are literal source declarations or recorded compiled references.

All target owner/source bytes collected on the server are verified against the same pinned Git commit. Earlier snapshots guide selection only. No mathematical conclusion is inferred from a declaration's name.
