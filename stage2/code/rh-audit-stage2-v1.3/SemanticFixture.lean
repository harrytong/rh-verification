import Mathlib
namespace RHStage2SemanticFixture
def truthAlias (_ : Nat) : Prop := (fun P : Prop => P) True
def equalityPredicate (n : Nat) : Prop := n = n
def zeroLinear : ℝ →ₗ[ℝ] ℝ := 0
def identityLinear : ℝ →ₗ[ℝ] ℝ := LinearMap.id
def zeroMeasure : MeasureTheory.Measure ℝ := 0
structure Record where
  point : Unit
  linear : ℝ →ₗ[ℝ] ℝ
  predicate : Nat → Prop
def record : Record := ⟨(), 0, truthAlias⟩
end RHStage2SemanticFixture
