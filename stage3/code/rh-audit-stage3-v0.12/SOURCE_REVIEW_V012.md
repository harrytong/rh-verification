# Selection basis for v0.12

Evidence: stage3-evidence(10).zip, SHA-256 6529451a52fb9ce02ce165537494c985824ad93ca1c5f742c950a401ae1df762. Paths below refer to its collected-source directory.

`Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/ThetaLiftTwistLevelFormEqUnitMulClassSum.lean` defines `GlobalTheory.LiftClassSumTwist.thF_eq_princ` at line 107 and `thF_eq_classSum` at 165. It constructs `GlobalTheory.Hk3.Core` from X.char fields, opens hC.thP.thF at 141 and calls `GlobalTheory.LiftUnfold.integral_theta` at 152. Lines 174 and 176 call flat-vector existence and normalization.

`Development/AbelianVarietyTheory/Definitions/GaloisGeometry/NormalFam.lean` defines `GlobalTheory.Hk3.Core` at 89 and its `thP : R.IsThP` field at 95. This grounds the selected projection `GlobalTheory.Hk3.Core.thP`.

`Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/UnivChar.lean` defines RealSide at 32 and its `char : R.Char3 F` field. The v0.11 compiled reference records identify `GlobalTheory.TwInputs.RealSide.char` and the qualified `Formalism.IndefR.Links.RealDat3.Char3.lev` and `.models` projections, with the latter owned by `Formalism.LocalToGlobal.IndefiniteReal.ZeroPartEigenvalueConvention`. This grounds the record/projection names and explicit source request; the contents of that requested owner were not reviewed in v0.11.

`Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/FlatVectorEqUnitMulCentralTranslateLiftVector.lean` defines `GlobalTheory.FlatLift.flat_eq_unit_smul_om` at 52. Its body calls `GlobalTheory.T.weilRep_central_acts_by_dilation_unit` and `GlobalTheory.T.lift_vector_eq_unit_mul_dilated_flat_datum`. Their implementations remain inspection targets.

`Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/FlatVecExistsUnique.lean` defines `GlobalTheory.FlatVecExist.flatVec_existsUnique` at 90.

Explicit source roots also include `Formalism/LocalToGlobal/IndefiniteReal/LinksChar.lean`, an import of the collected ConcretePkgSpec.lean. Requesting it is navigation to possible record definitions, not a claim about its unseen contents.

v0.11 established the local zero/nonzero explanation of coefficient descent and the integrality-based unit construction. It did not establish nonvacuity at headline inputs. This package follows the remaining realization and integral assumptions; it does not reclassify the previous result as a global verification.
