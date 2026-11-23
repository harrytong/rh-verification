import Lean

/- Tool tests only. Never imported into Main or the statement check. -/
namespace RHStage2Fixture
def Marker : Prop := True
axiom fakePremise : Marker
theorem regions (h : Marker) : Marker := h
def alwaysTrue (_ : Nat) : Prop := True
def unitType (_ : Nat) : Type := PUnit
def constantNat (_ : Nat) : Nat := 7
def identityNat (n : Nat) : Nat := n
def wrapped (_ : Nat) : Nat := (fun _ : Nat => 7) 11
end RHStage2Fixture
