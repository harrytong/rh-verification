import Lean

/- Isolated audit-tool test data. This is never imported into the RH project.
   The artificial axiom tests whether the dependency walker actually reads
   theorem and opaque bodies; it is not a premise added to the RH proof. -/
namespace RHCriticsFixture

axiom fakePremise : True
def hiddenDef : True := fakePremise
theorem viaTheorem : True := hiddenDef
opaque viaOpaque : True := viaTheorem
theorem root : True := viaOpaque
theorem irrelevant : True := True.intro

inductive Choice where
  | ordinary : Choice
  | hidden (h : fakePremise = fakePremise) : Choice

theorem choiceRoot : Nonempty Choice := ⟨Choice.ordinary⟩

end RHCriticsFixture
