# Version 1.1

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
