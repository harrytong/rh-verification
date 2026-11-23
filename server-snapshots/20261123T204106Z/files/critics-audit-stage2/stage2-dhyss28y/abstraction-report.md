# Scoped geometry abstraction experiments

These are local experiments against the original imported environment. They do not globally parameterize Main or modify the original definitions.
The body of the selected theorem is copied from the pinned source. The baseline clone must compile before its three literal geometry arguments are generalized.
A universal-P premise, if present, is merely available to the unchanged copied proof script. Its success/failure does not determine a weakest requirement on P.

## generic-GeoCl-interface

Compiled: **True**; log: `probe-generic-GeoCl-interface.log`.
Provisional first-error category: `no-elaboration-error-found`.
Reviewed classification: pending. No interpretation of a failure as necessity or invalidity is automatic.

## baseline

Compiled: **True**; log: `probe-baseline.log`.
Provisional first-error category: `no-elaboration-error-found`.
Reviewed classification: pending. No interpretation of a failure as necessity or invalidity is automatic.

## arbitrary-P

Compiled: **False**; log: `probe-arbitrary-P.log`.
Provisional first-error category: `type-or-interface-mismatch; premise-status-unresolved`.
Reviewed classification: pending. No interpretation of a failure as necessity or invalidity is automatic.

```text
/audit/AbstractionArbitraryP.lean:63:25: error: Application type mismatch: The argument
  hOpen1
has type
  S0.OpenParameterStatements (parametersOfDependence hL (max CF0 CF1))
but is expected to have type
  S0.OpenParameterStatements
    (parametersOfExtension (GlobalTheory.HeightCounting.Up.extensionWithList hL (max CF0 CF1)) SExt.none
      (geoCl auditGamma))
in the application
  hMono.right hOpen1
```

## universal-P

Compiled: **False**; log: `probe-universal-P.log`.
Provisional first-error category: `type-or-interface-mismatch; premise-status-unresolved`.
Reviewed classification: pending. No interpretation of a failure as necessity or invalidity is automatic.

```text
/audit/AbstractionUniversalP.lean:63:25: error: Application type mismatch: The argument
  hOpen1
has type
  S0.OpenParameterStatements (parametersOfDependence hL (max CF0 CF1))
but is expected to have type
  S0.OpenParameterStatements
    (parametersOfExtension (GlobalTheory.HeightCounting.Up.extensionWithList hL (max CF0 CF1)) SExt.none
      (geoCl auditGamma))
in the application
  hMono.right hOpen1
```

## What successful generic lemmas would establish

A universal P is sufficient for GeoCl P at every input. Any particular GeoCl P witness has a seed satisfying P somewhere in its constructor derivation. GeoCl False is empty. GeoCl anyGeometry is universal.
These statements explain the generic closure interface. They do not show whether every other premise of the headline theorem has the intended mathematical meaning.
