import Main
set_option pp.all true

open Formalism.BasicNotions Formalism.MainNotions Formalism.MainNotions.Inhab
open GlobalTheory.EX GlobalTheory.EX.OB
namespace RHStage3Followup

-- Preservation for an arbitrary LedPart requires an explicit agreement premise.
-- This proves sufficiency of that premise, not its availability upstream.
theorem stage3_height_preserved_given_agreement
    {C : FC} {D : D7} {Y : Lay D} (p : LedPart C Y)
    (hOriginal : ∀ u, D.div.h u = DV.hExpl6 D p.L Y.X C.Csz u)
    (u : D.what₂.Word) : p.pt.D.div.h u = D.div.h u := by
  exact (hOriginal u).symm

-- A genuine special case already supplied by the project: start with a Pt.
-- The Pt already carries the height contract used to recover its height.
theorem stage3_height_roundtrip {C : FC} (p : GlobalTheory.EX.Pt C) :
    (LedPart.ofPt p).pt.D.div.h = p.D.div.h := by
  exact (GlobalTheory.EX.OB.pt_ofPt p).2

theorem stage3_height_roundtrip_at {C : FC} (p : GlobalTheory.EX.Pt C) (u : p.D.what₂.Word) :
    (LedPart.ofPt p).pt.D.div.h u = p.D.div.h u := by
  exact congrFun (stage3_height_roundtrip p) u

-- This equivalence spells out the missing premise exactly. It does not prove it.
theorem stage3_height_agreement_iff
    {C : FC} {D : D7} {Y : Lay D} (p : LedPart C Y) :
    (∀ u, p.pt.D.div.h u = D.div.h u) ↔
    (∀ u, D.div.h u = DV.hExpl6 D p.L Y.X C.Csz u) := by
  constructor
  · intro h u
    exact (h u).symm
  · intro h u
    exact (h u).symm

#print stage3_height_preserved_given_agreement
#print axioms stage3_height_preserved_given_agreement
#print stage3_height_roundtrip
#print axioms stage3_height_roundtrip
#print stage3_height_roundtrip_at
#print axioms stage3_height_roundtrip_at
#print stage3_height_agreement_iff
#print axioms stage3_height_agreement_iff
#eval IO.println "RH_STAGE3_HEIGHT_BOUNDARY_THEOREMS_ACCEPTED"
end RHStage3Followup

#print GlobalTheory.EX.OB.pt_ofPt
#print GlobalTheory.EX.OB.LedPart.ofPt
#print GlobalTheory.EX.OB.Lay.ofPt
#print GlobalTheory.EX.OB.LedPart.ofPt_pt
#print GlobalTheory.EX.OB.LedPart.pt_has
#print GlobalTheory.EX.OB.RecEx
#print GlobalTheory.EX.OB.nonempty_ledPart_iff
#eval IO.println "RH_STAGE3_HEIGHT_BOUNDARY_END"
