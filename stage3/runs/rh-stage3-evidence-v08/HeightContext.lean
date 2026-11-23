import Main

set_option pp.all true

#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.EX.OB.setDiv"
#print GlobalTheory.EX.OB.setDiv
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.EX.OB.setDiv"
#eval IO.println "RH_STAGE3_DECL_BEGIN Formalism.MainNotions.Inhab.ExtraAt"
#print Formalism.MainNotions.Inhab.ExtraAt
#eval IO.println "RH_STAGE3_DECL_END Formalism.MainNotions.Inhab.ExtraAt"
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.EX.OB.LedPart.ht"
#print GlobalTheory.EX.OB.LedPart.ht
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.EX.OB.LedPart.ht"
#eval IO.println "RH_STAGE3_DECL_BEGIN GlobalTheory.EX.OB.LedPart.pt"
#print GlobalTheory.EX.OB.LedPart.pt
#eval IO.println "RH_STAGE3_DECL_END GlobalTheory.EX.OB.LedPart.pt"
#eval IO.println "RH_STAGE3_DECL_BEGIN Formalism.BasicNotions.DV.hExpl6"
#print Formalism.BasicNotions.DV.hExpl6
#eval IO.println "RH_STAGE3_DECL_END Formalism.BasicNotions.DV.hExpl6"
#eval IO.println "RH_STAGE3_DECL_BEGIN SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt"
#print SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt
#eval IO.println "RH_STAGE3_DECL_END SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt"

noncomputable section
namespace GlobalTheory.EX.OB
open Formalism.BasicNotions Formalism.MainNotions Formalism.MainNotions.Inhab
open GlobalTheory.EX
namespace LedPart
variable {C : FC} {D : D7} {Y : Lay D} (p : LedPart C Y)

-- This checks the assigned height of the NEW object, not of the old D.
theorem stage3_assigned_height (u : D.what₂.Word) :
    p.pt.D.div.h u = p.ht u := by
  trace "RH_STAGE3_CONTEXT H1_ASSIGNED_HEIGHT"
  trace_state
  rfl

-- This spells out the actual dependent record contract on that new object.
theorem stage3_constructed_height_contract (u : D.what₂.Word) :
    p.pt.D.div.h u = Formalism.BasicNotions.DV.hExpl6 p.pt.D p.pt.L p.pt.xa.X C.Csz u := by
  trace "RH_STAGE3_CONTEXT H2_CONSTRUCTED_CONTRACT"
  trace_state
  exact p.pt.xa.h_eq u

end LedPart
end GlobalTheory.EX.OB
end

#print GlobalTheory.EX.OB.LedPart.stage3_assigned_height
#print axioms GlobalTheory.EX.OB.LedPart.stage3_assigned_height
#print GlobalTheory.EX.OB.LedPart.stage3_constructed_height_contract
#print axioms GlobalTheory.EX.OB.LedPart.stage3_constructed_height_contract
#eval IO.println "RH_STAGE3_HEIGHT_END"
