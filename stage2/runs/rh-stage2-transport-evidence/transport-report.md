# Explicit transport at the two failed abstraction interfaces

The prior baseline source must match the already compiled baseline byte for byte. It is not rebuilt here.
Two conditional copies of that proof are tested. Both still replace only its three literal geometry arguments; imported declarations are unchanged.
The universal-P case proves geoCl P = geoCl anyGeometry using its universal-P premise and the base constructor. The closure case assumes universal geoCl P directly, then proves the same equality.
That equality is used explicitly when supplying hOpen1 and before passing hFun/hL3 to the specialized final interface. Neither probe simply invokes the original bundle theorem.

| Probe | Process succeeded | Reported sorryAx |
|---|---|---|
| universal-P-transport | True | False |
| universal-closure-transport | True | False |

## Interpretation

Success would show that explicit propositional transport resolves these local interface mismatches under the stated premise. It would not generalize the whole project, identify a weakest geometric condition, or establish global necessity or invalidity.
Universal P implies universal GeoCl P by the base constructor. The converse, or strict weakness of the closure premise in this development, is not established by this test.
Failure must be read from the first diagnostic. A failed declaration's sorryAx output is error recovery in the experimental file, not a new axiom of Main.
