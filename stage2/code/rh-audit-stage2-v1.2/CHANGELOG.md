# Version 1.2

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
