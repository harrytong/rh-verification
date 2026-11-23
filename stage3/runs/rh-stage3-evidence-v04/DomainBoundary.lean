import Main
set_option pp.all true
set_option autoImplicit false

noncomputable section
open Formalism.BasicNotions Formalism.MainNotions Formalism.MainNotions.Inhab
open Formalism.L2.Host GlobalTheory.EX GlobalTheory.EX.OB
open GlobalTheory.Mem GlobalTheory.Mem.Col2 GlobalTheory.Mem.Top.GroupRetwisting
open GlobalTheory.Mem.Top GlobalTheory.Mem.Top.Bl NumberField IsDedekindDomain
attribute [local instance] Formalism.BasicNotions.Host.cmStar

namespace RHStage3Domains
variable {K : Ctx} {B : Base} {f : Fr B.toPre} {T : TwDat B}
variable {w : ColW B f T} {Z : w.Lt} {Wt : Set B.places.Pl}
variable {p0 : BaseLevelRowSide (w.D Z)}
variable (t : RowsT K w Z Wt p0) (X : DivX (w.D Z))

-- Exact local inhabitance boundary. This does not construct an OAt object.
theorem oat_nonempty_iff (Γ : GeoP) :
    Nonempty (OAt Γ t X) ↔
      Γ (w.st Z).toD7 t.r.z.core.toCore X ∧ LamAre t.r.Z X := by
  constructor
  · rintro ⟨o⟩
    exact ⟨o.geo, o.lam⟩
  · rintro ⟨hGeo, hLam⟩
    exact ⟨⟨hGeo, hLam⟩⟩

theorem oat_any_iff_lam :
    Nonempty (OAt anyGeometry t X) ↔ LamAre t.r.Z X := by
  constructor
  · rintro ⟨o⟩
    exact o.lam
  · intro hLam
    exact ⟨⟨True.intro, hLam⟩⟩

theorem oat_false_empty :
    ¬ Nonempty (OAt (fun _ _ _ => False) t X) := by
  rintro ⟨o⟩
  exact o.geo

-- The same GeoCl induction already accepted in the v0.2 server run.
theorem false_closure_empty {D : D7} {J : Formalism.L2.Pj.Core D} {Y : DivX D} :
    ¬ GeoCl (fun _ _ _ => False) D J Y := by
  intro h
  induction h with
  | base hp => exact hp
  | step N h previous ih => exact ih

theorem oat_false_closure_empty :
    ¬ Nonempty (OAt (geoCl (fun _ _ _ => False)) t X) := by
  rintro ⟨o⟩
  exact false_closure_empty o.geo

#print oat_nonempty_iff
#print axioms oat_nonempty_iff
#print oat_any_iff_lam
#print axioms oat_any_iff_lam
#print oat_false_empty
#print axioms oat_false_empty
#print false_closure_empty
#print axioms false_closure_empty
#print oat_false_closure_empty
#print axioms oat_false_closure_empty
#eval IO.println "RH_STAGE3_DOMAIN_BOUNDARIES_END"
end RHStage3Domains
end
