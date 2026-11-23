# Preregistered semantic tests: bounded census

Read CENSUS_PREREGISTRATION.md for frozen classes, counting units, scope, and exclusions.
These are Lean MetaM definitional-equality tests under all transparency, not additional independent kernel checks.
Unknown tests are never counted as confirmed nontrivial cases. Anonymous records arbitrarily buried in proof terms are outside the field denominator.

## independent-Mathlib-control

Closure declarations: 24,931.
Definitions attempted: 5,771; completed: 5,768; unknown: 3.
Record constructor fields visited in completed analyses: 16,974; definitions hitting the record depth bound: 233.

### definitions/at-least-one-hit

Denominator: 5,768.

| Frozen category | Confirmed hits |
|---|---:|
| Prop-valued-definition-definitionally-True | 25 |
| unit-typed-constructor-field | 5 |
| definitionally-zero-linear-map | 6 |
| definitionally-zero-measure | 2 |
| unit-valued-definition-auxiliary | 1 |
| unit-type-family-value-auxiliary | 1 |
| reserved | 0 |

### origin/Lean-core/definitions

Denominator: 1,930.

| Frozen category | Confirmed hits |
|---|---:|
| Prop-valued-definition-definitionally-True | 0 |
| unit-typed-constructor-field | 1 |
| definitionally-zero-linear-map | 0 |
| definitionally-zero-measure | 0 |
| unit-valued-definition-auxiliary | 1 |
| unit-type-family-value-auxiliary | 1 |
| reserved | 0 |

### origin/Mathlib/definitions

Denominator: 3,792.

| Frozen category | Confirmed hits |
|---|---:|
| Prop-valued-definition-definitionally-True | 25 |
| unit-typed-constructor-field | 4 |
| definitionally-zero-linear-map | 6 |
| definitionally-zero-measure | 2 |
| unit-valued-definition-auxiliary | 0 |
| unit-type-family-value-auxiliary | 0 |
| reserved | 0 |

### classified-sites/overlapping-categories

Denominator: 43.

| Frozen category | Confirmed hits |
|---|---:|
| Prop-valued-definition-definitionally-True | 25 |
| unit-typed-constructor-field | 5 |
| definitionally-zero-linear-map | 9 |
| definitionally-zero-measure | 2 |
| unit-valued-definition-auxiliary | 1 |
| unit-type-family-value-auxiliary | 1 |
| reserved | 0 |

### origin/other-project-or-package/definitions

Denominator: 46.

| Frozen category | Confirmed hits |
|---|---:|
| Prop-valued-definition-definitionally-True | 0 |
| unit-typed-constructor-field | 0 |
| definitionally-zero-linear-map | 0 |
| definitionally-zero-measure | 0 |
| unit-valued-definition-auxiliary | 0 |
| unit-type-family-value-auxiliary | 0 |
| reserved | 0 |

### First unknown diagnostics

```text
UniformConvergenceCLM.instSMulOfSMulCommClassOfContinuousConstSMul: failed to synthesize
  Zero (UniformConvergenceCLM σ F 𝔖)

Hint: Additional diagnostic information may be available using the `set_option diagnostics true` command.
UniformConvergenceCLM.instAddCommGroup._aux_4: failed to synthesize
  Zero (UniformConvergenceCLM σ F 𝔖)

Hint: Additional diagnostic information may be available using the `set_option diagnostics true` command.
UniformConvergenceCLM.ofFun: failed to synthesize
  Zero (UniformConvergenceCLM σ F 𝔖)

Hint: Additional diagnostic information may be available using the `set_option diagnostics true` command.
```

## five-headline-reference-union

Closure declarations: 1,478,222.
Definitions attempted: 214,234; completed: 213,831; unknown: 403.
Record constructor fields visited in completed analyses: 730,453; definitions hitting the record depth bound: 12,603.

### definitions/at-least-one-hit

Denominator: 213,831.

| Frozen category | Confirmed hits |
|---|---:|
| Prop-valued-definition-definitionally-True | 294 |
| unit-typed-constructor-field | 600 |
| definitionally-zero-linear-map | 130 |
| definitionally-zero-measure | 9 |
| unit-valued-definition-auxiliary | 12 |
| unit-type-family-value-auxiliary | 131 |
| reserved | 0 |

### origin/Mathlib/definitions

Denominator: 32,959.

| Frozen category | Confirmed hits |
|---|---:|
| Prop-valued-definition-definitionally-True | 127 |
| unit-typed-constructor-field | 141 |
| definitionally-zero-linear-map | 46 |
| definitionally-zero-measure | 6 |
| unit-valued-definition-auxiliary | 8 |
| unit-type-family-value-auxiliary | 17 |
| reserved | 0 |

### origin/other-project-or-package/definitions

Denominator: 178,039.

| Frozen category | Confirmed hits |
|---|---:|
| Prop-valued-definition-definitionally-True | 166 |
| unit-typed-constructor-field | 458 |
| definitionally-zero-linear-map | 84 |
| definitionally-zero-measure | 3 |
| unit-valued-definition-auxiliary | 3 |
| unit-type-family-value-auxiliary | 113 |
| reserved | 0 |

### origin/Lean-core/definitions

Denominator: 2,833.

| Frozen category | Confirmed hits |
|---|---:|
| Prop-valued-definition-definitionally-True | 1 |
| unit-typed-constructor-field | 1 |
| definitionally-zero-linear-map | 0 |
| definitionally-zero-measure | 0 |
| unit-valued-definition-auxiliary | 1 |
| unit-type-family-value-auxiliary | 1 |
| reserved | 0 |

### classified-sites/overlapping-categories

Denominator: 2,338.

| Frozen category | Confirmed hits |
|---|---:|
| Prop-valued-definition-definitionally-True | 566 |
| unit-typed-constructor-field | 1,079 |
| definitionally-zero-linear-map | 267 |
| definitionally-zero-measure | 13 |
| unit-valued-definition-auxiliary | 12 |
| unit-type-family-value-auxiliary | 401 |
| reserved | 0 |

### First unknown diagnostics

```text
GlobalTheory.Mem.Top.Bl.ColW.D: (deterministic) timeout at `whnf`, maximum number of heartbeats (2000) has been reached

Note: Use `set_option maxHeartbeats <num>` to set the limit.(invalid MessageData.lazy, missing context)
GlobalTheory.Mem.R3.famR: (deterministic) timeout at `whnf`, maximum number of heartbeats (2000) has been reached

Note: Use `set_option maxHeartbeats <num>` to set the limit.(invalid MessageData.lazy, missing context)
GlobalTheory.LieVB.Lie: failed to synthesize
  Zero
    (↑((GlobalTheory.VB.homPresheaf (GlobalTheory.LieVB.omega G) (GlobalTheory.structureModule S)).obj
          X) →ₗ[↑(S.ringCatSheaf.obj.obj X)]
      ↑((ModuleCat.restrictScalars (RingCat.Hom.hom (S.ringCatSheaf.obj.map f))).obj
          (ModuleCat.of ↑(S.ringCatSheaf.obj.obj Y)
            ↑((GlobalTheory.VB.homPresheaf (GlobalTheory.LieVB.omega G) (GlobalTheory.structureModule S)).obj Y))))

Hint: Additional diagnostic information may be available using the `set_option diagnostics true` command.
GlobalTheory.structureModule: failed to synthesize
  Zero
    (↑(X✝.ringCatSheaf.obj.obj X) →ₗ[↑(X✝.ringCatSheaf.obj.obj X)]
      ↑((ModuleCat.restrictScalars (RingCat.Hom.hom (X✝.ringCatSheaf.obj.map f))).obj
          (ModuleCat.of ↑(X✝.ringCatSheaf.obj.obj Y) ↑(X✝.ringCatSheaf.obj.obj Y))))

Hint: Additional diagnostic information may be available using the `set_option diagnostics true` command.
GlobalTheory.Cp.SquareIntegrableColumns.toS: (deterministic) timeout at `whnf`, maximum number of heartbeats (2000) has been reached

Note: Use `set_option maxHeartbeats <num>` to set the limit.(invalid MessageData.lazy, missing context)
GlobalTheory.Mem.Col2.TC.rec7: (deterministic) timeout at `whnf`, maximum number of heartbeats (2000) has been reached

Note: Use `set_option maxHeartbeats <num>` to set the limit.(invalid MessageData.lazy, missing context)
GlobalTheory.BigTop.Fun.lamOf: (deterministic) timeout at `whnf`, maximum number of heartbeats (2000) has been reached

Note: Use `set_option maxHeartbeats <num>` to set the limit.(invalid MessageData.lazy, missing context)
GlobalTheory.Mem.R3.famC: (deterministic) timeout at `whnf`, maximum number of heartbeats (2000) has been reached

Note: Use `set_option maxHeartbeats <num>` to set the limit.(invalid MessageData.lazy, missing context)
GlobalTheory.VB.dual: failed to synthesize
  Zero
    (↑((GlobalTheory.VB.homPresheaf F (GlobalTheory.structureModule X✝)).obj X) →ₗ[↑(X✝.ringCatSheaf.obj.obj X)]
      ↑((ModuleCat.restrictScalars (RingCat.Hom.hom (X✝.ringCatSheaf.obj.map f))).obj
          (ModuleCat.of ↑(X✝.ringCatSheaf.obj.obj Y)
            ↑((GlobalTheory.VB.homPresheaf F (GlobalTheory.structureModule X✝)).obj Y))))

Hint: Additional diagnostic information may be available using the `set_option diagnostics true` command.
GlobalTheory.twist: failed to synthesize
  Zero
    (↑((GlobalTheory.Twist.secPresheaf F L).obj X) →ₗ[↑(X✝.ringCatSheaf.obj.obj X)]
      ↑((ModuleCat.restrictScalars (RingCat.Hom.hom (X✝.ringCatSheaf.obj.map f))).obj
          (ModuleCat.of ↑(X✝.ringCatSheaf.obj.obj Y) ↑((GlobalTheory.Twist.secPresheaf F L).obj Y))))

Hint: Additional diagnostic information may be available using the `set_option diagnostics true` command.
SheafOfModules.unit: failed to synthesize
  Zero
    (↑(R.obj.obj X) →ₗ[↑(R.obj.obj X)]
      ↑((ModuleCat.restrictScalars (RingCat.Hom.hom (R.obj.map f))).obj (ModuleCat.of ↑(R.obj.obj Y) ↑(R.obj.obj Y))))

Hint: Additional diagnostic information may be available using the `set_option diagnostics true` command.
GlobalTheory.LB.toMod: failed to synthesize
  Zero
    (↑((GlobalTheory.LB.secPresheaf L).obj X) →ₗ[↑(X✝.ringCatSheaf.obj.obj X)]
      ↑((ModuleCat.restrictScalars (RingCat.Hom.hom (X✝.ringCatSheaf.obj.map f))).obj
          (ModuleCat.of ↑(X✝.ringCatSheaf.obj.obj Y) ↑((GlobalTheory.LB.secPresheaf L).obj Y))))

Hint: Additional diagnostic information may be available using the `set_option diagnostics true` command.
GlobalTheory.LB.unitMod: failed to synthesize
  Zero
    (↑(X✝.ringCatSheaf.obj.obj X) →ₗ[↑(X✝.ringCatSheaf.obj.obj X)]
      ↑((ModuleCat.restrictScalars (RingCat.Hom.hom (X✝.ringCatSheaf.obj.map f))).obj
          (ModuleCat.of ↑(X✝.ringCatSheaf.obj.obj Y) ↑(X✝.ringCatSheaf.obj.obj Y))))

Hint: Additional diagnostic information may be available using the `set_option diagnostics true` command.
PositivityTheory.Rg.BcB.F.rlΘ₂: (deterministic) timeout at `whnf`, maximum number of heartbeats (2000) has been reached

Note: Use `set_option maxHeartbeats <num>` to set the limit.(invalid MessageData.lazy, missing context)
GlobalTheory.Cp.ColRec3.ev: (deterministic) timeout at `whnf`, maximum number of heartbeats (2000) has been reached

Note: Use `set_option maxHeartbeats <num>` to set the limit.(invalid MessageData.lazy, missing context)
Formalism.L2.DIV.ColRec3.ev: (deterministic) timeout at `whnf`, maximum number of heartbeats (2000) has been reached

Note: Use `set_option maxHeartbeats <num>` to set the limit.(invalid MessageData.lazy, missing context)
GlobalTheory.Cp.ColRec3.toS: (deterministic) timeout at `whnf`, maximum number of heartbeats (2000) has been reached

Note: Use `set_option maxHeartbeats <num>` to set the limit.(invalid MessageData.lazy, missing context)
GlobalTheory.EX.OB.LedPart.pt: (deterministic) timeout at `whnf`, maximum number of heartbeats (2000) has been reached

Note: Use `set_option maxHeartbeats <num>` to set the limit.(invalid MessageData.lazy, missing context)
GlobalTheory.FunObj.LaP: (deterministic) timeout at `whnf`, maximum number of heartbeats (2000) has been reached

Note: Use `set_option maxHeartbeats <num>` to set the limit.(invalid MessageData.lazy, missing context)
Formalism.BasicNotions.DV.aPlusQ: (deterministic) timeout at `whnf`, maximum number of heartbeats (2000) has been reached

Note: Use `set_option maxHeartbeats <num>` to set the limit.(invalid MessageData.lazy, missing context)
```

## Remaining use-role work

Value classification does not determine whether an object discharges a required hypothesis, is used as ordinary data, or occurs in irrelevant syntax.
The edge reports classify the selected witness paths, not every application in the full closure. A global witness-versus-ordinary census remains unestablished and must not be fabricated from these counts.
The independent Mathlib closure is not assumed to match the headline closure in size or subject. Do not interpret differences as evidence of invalidity or statistical unusualness.
