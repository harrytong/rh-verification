import Main

/- These lemmas test the generic GeoCl interface only. They do not generalize
   Main or replace anyGeometry inside imported declarations. -/
open Formalism.BasicNotions Formalism.MainNotions
open GlobalTheory.Mem.Top.Bl

namespace RHStage2Abstraction

theorem universalPredicate_suffices (P : GeoP)
    (hP : ∀ D J X, P D J X) (D : D7)
    (J : Formalism.L2.Pj.Core D) (X : DivX D) :
    geoCl P D J X := GeoCl.base (hP D J X)

theorem closure_requires_a_seed (P : GeoP) {D : D7}
    {J : Formalism.L2.Pj.Core D} {X : DivX D} (h : GeoCl P D J X) :
    ∃ (D₀ : D7) (J₀ : Formalism.L2.Pj.Core D₀) (X₀ : DivX D₀), P D₀ J₀ X₀ := by
  induction h with
  | base hp => exact ⟨_, _, _, hp⟩
  | step N h previous ih => exact ih

theorem falsePredicate_has_empty_closure {D : D7}
    {J : Formalism.L2.Pj.Core D} {X : DivX D} :
    ¬ GeoCl (fun _ _ _ => False) D J X := by
  intro h
  induction h with
  | base hp => exact hp
  | step N h previous ih => exact ih

theorem anyGeometry_has_universal_closure (D : D7)
    (J : Formalism.L2.Pj.Core D) (X : DivX D) :
    geoCl anyGeometry D J X := GeoCl.base True.intro

#check universalPredicate_suffices
#check closure_requires_a_seed
#check falsePredicate_has_empty_closure
#check anyGeometry_has_universal_closure
#print axioms universalPredicate_suffices
#print axioms closure_requires_a_seed
#print axioms falsePredicate_has_empty_closure
#print axioms anyGeometry_has_universal_closure
end RHStage2Abstraction
