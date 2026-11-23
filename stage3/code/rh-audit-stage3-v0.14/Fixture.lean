import Lean

set_option pp.all true
namespace RHStage3Fixture

def parameterUse (P : Nat → Prop) : Nat → Prop := P
theorem witnessUse (P : Nat → Prop) (n : Nat) (h : P n) : P n := h
structure Payload where
  n : Nat
  positive : 0 < n
theorem dataUse (p : Payload) : 0 < p.n := p.positive
structure Datum where
  height : Nat
def assign (d : Datum) (h : Nat) : Datum := { d with height := h }
theorem assignedHeight (d : Datum) (h : Nat) : (assign d h).height = h := rfl
theorem universalTransport (P : Nat → Prop) (h : ∀ n, P n) (n : Nat) : P n := by
  trace "RH_STAGE3_CONTEXT FIXTURE"
  trace_state
  exact witnessUse P n (h n)

#print parameterUse
#print witnessUse
#print dataUse
#print assignedHeight
#print universalTransport
#print axioms universalTransport
-- Toy boundary checks for the new experiment; these are not RH declarations.
def restricted (P : Nat → Prop) : Prop := ∀ n, P n → n = n
theorem arbitraryRestricted (P : Nat → Prop) : restricted P := fun _ _ => rfl
theorem falseRestricted : restricted (fun _ => False) := arbitraryRestricted _
theorem assignedPreserved (d : Datum) (h : Nat) (agree : d.height = h) :
    (assign d h).height = d.height := agree.symm
#print arbitraryRestricted
#print falseRestricted
#print assignedPreserved
-- Record-domain analogues; independently gated, but not project validation.
structure Scoped (P : Nat → Prop) (n : Nat) where
  predicate : P n
  other : 0 < n
theorem scoped_iff (P : Nat → Prop) (n : Nat) :
    Nonempty (Scoped P n) ↔ P n ∧ 0 < n := by
  constructor
  · intro h
    cases h with
    | intro o => exact ⟨o.predicate, o.other⟩
  · intro h
    exact ⟨⟨h.1, h.2⟩⟩
theorem scoped_false_empty (n : Nat) : ¬ Nonempty (Scoped (fun _ => False) n) := by
  intro h
  cases h with
  | intro o => exact o.predicate
theorem scoped_true_iff (n : Nat) :
    Nonempty (Scoped (fun _ => True) n) ↔ 0 < n := by
  constructor
  · intro h
    cases h with
    | intro o => exact o.other
  · intro h; exact ⟨⟨True.intro, h⟩⟩
#print scoped_iff
#print scoped_false_empty
#print scoped_true_iff
#eval IO.println "RH_STAGE3_POSITIVE_FIXTURE_END"
end RHStage3Fixture
