# Version 1.5

The semantic tool compiled in version 1.4 but its dynamic import was rejected:
loading environment extensions requires `Lean.enableInitializersExecution`.
This version calls that API immediately before the semantic import, and marks
the runtime entry point unsafe as required by that API. The syntactic tool
continues to import with loadExts false and is unchanged.

Semantic imports and the subsequent traversal are sequential. No imported
compacted regions are explicitly freed. The existing sandbox and all proof
source/artifact pins remain unchanged. Neither census had started when the
version-1.4 preflight failed. The census specification is unchanged.

References:
https://leanprover-community.github.io/mathlib4_docs/Lean/ImportingFlag.html
https://leanprover-community.github.io/mathlib4_docs/Lean/Environment.html

## Version 1.4

Corrects the two multiline structure-literal layouts rejected by the pinned
compiler in the semantic tool. Uses one field per line, consistently indented,
for both the Analysis result and Core.Context values. No census category or
bound is changed. The shared tool already validated on the server is unchanged.

Adds a standalone `semantic-smoke` phase: it runs the tool fixtures and exits
without starting either control or headline census. The failed syntax preflight
started neither census. The successful transport experiments remain unchanged.

## Version 1.3

Adds `abstraction-transport`. The preceding run compiled the generic GeoCl
lemmas and the baseline, while both local arbitrary-predicate variants
failed at hOpen1 and hFun: imported interfaces retain the original geometry
specialization. Merely making the universal-P premise available did not
request propositional transport in the copied proof.

Two new probes explicitly prove equality of the closure predicates and use
it when supplying hOpen1, then normalize hFun/hL3 before the specialized
final call. One assumes universal P; the other assumes universal GeoCl P.
These remain scoped conditional experiments with unchanged imports. They
do not claim a weakest predicate, global independence, or a refutation.

The previously compiled baseline is reused only after checking its source
hash and prior run metadata. Original inputs and logs remain unchanged.
All failed probe outputs remain failures even if Lean prints a recovered
declaration containing sorryAx after an elaboration error.

## Version 1.2

The server compiled the corrected shared tool and reached the isolated
fixture, which rejected the manually constructed OfNat test. The fixture
had used `mkNatLit` for OfNat's numeric index argument. At Lean 4.33.1,
`mkNatLit` already constructs a frontend OfNat application; the test thus
nested that encoding where the classifier expected a raw numeral literal.

This version uses explicit raw literal Expr constructors for that argument,
supplies the matching OfNat instance, and separately tests raw literals and
the frontend `mkNatLit` form for both zero and one. The syntactic classifier
itself is unchanged from 1.1. No test is removed or bypassed.

Reference for these constructors:
https://leanprover-community.github.io/mathlib4_docs/Lean/Expr.html#Lean.mkNatLit

The failed runs stopped before Main. No new proof-audit result is claimed.

## Version 1.1

Corrects two errors reported by Harry's pinned Lean 4.33.1 compiler during
the initial tool preflight. That run stopped before the Main import.

- The syntactic zero classifier now binds an explicitly typed `Array Expr`
  before indexing and uses fully qualified expression/literal constructors.
- The final census dispatch now binds its label and options inside an
  explicit `else` block before calling `RHStage2.census`. This avoids the
  multiline application being parsed as a partially applied function.
- Added Lean smoke cases for literal zero/nonzero and OfNat zero/nonzero.

The inspection method, source/compiler pins, preregistered census categories,
resource limits, and original proof inputs are unchanged. The semantic tool
is generated from the corrected shared source automatically.

Python regression tests are separate from Lean compilation. Local Python
tests pass; the corrected Lean program must pass the included server
preflight. No new RH/GRH verification result is claimed.
