# Stage 4 v0.2: findings from the first completed project run

Reviewed evidence: `stage4-evidence.zip` from `stage4-jv0d55yd`.
SHA-256: `0eaea5fa6c8e448e65b4521876606d47eb09683d61774eb7a21b18f29313bc58`.
The archive checksum and every entry in its evidence manifest were verified.
This is review of Harry's recorded run, not a second independent rerun.

## Results

| Test | Recorded result | Scope |
| --- | --- | --- |
| Invalid `False := True.intro` fixture | Rejected as expected | Audit control |
| Six comparison fixtures | Passed | Checks generic, applied and let-bound comparisons, including equality hypotheses |
| `example : RiemannHypothesis := riemannHypothesis` | Compiled | Correct type in the imported environment; not a protected-challenge comparison |
| Constructed height `p.pt.D.div.h u = p.ht u` | Proved by `rfl` | Confirms this assigned-height identity |
| `slope_le_height` generic conclusion | Sides not definitionally identical | Its local parameters and hypotheses remain present |
| `height_add_log_nonneg` generic conclusion | Sides not definitionally identical | Same limitation |
| `FrameCmp.val_le` generic conclusion | Sides not definitionally identical | Same limitation |
| `FrameCmp.htCmp` application of `FrameCmp.val_le` | Sides not definitionally identical | Actual arguments at one stored call site |
| `heightAt_eq_of_cover` application of `slope_le_height` | Not reached before node cap | Unresolved; cannot infer absence or reflexivity |

The last scan visited 250,000 expression nodes and found zero watched applications
before stopping. The `htCmp` scan finished after 49,049 visited nodes and found one
`val_le` application. The recorded `collection_complete` is false, correctly.

## Concrete comparisons

The generic slope inequality has the form

`(1 - rhoB ...) * max 0 (s + cs) ≤ Y.ht ... + cs + (cc + htCost ... * l1 ...)`.

The fully applied `val_le` inside `htCmp` compares

`val_vw la q Valued.v (evR Xo c f y)`

with

`nval T.V e (evI y₀ f) + ↑(↑(vLa la ↑q) * htEx E q * l1 u)`.

The actual expressions, fully qualified names and local contexts are preserved
in `comparison-records.json`. The printed lhs/rhs fields of all four recorded
comparisons have `truncated: false`. The test used transparency `all`; it did not
rewrite by local hypotheses or specialize arguments from more distant callers.

## What this establishes

The constructed height identity really is reflexive. However, the three generic
comparison conclusions and one inspected immediate application are not simply
identical expressions under the audit's definitional-equality test. The former
fact does not by itself establish the latter allegation.

The more important immediate slope application is still unresolved because of
the traversal cap. These results neither establish the critics' overall invalidity
claim nor refute all of their arguments. The exact mathematical comparison meant
by the paper still needs to be matched to a declaration and application site.

The literal statement that the final theorem has only the type
`RiemannHypothesis = RiemannHypothesis` is contradicted by the successful example
and printed type in this imported environment. This does not replace Comparator's
independent statement-correspondence checks.

## Operational record

The project process exited 0 after 1 minute 18.69 seconds. Input hashes before and
after agree. The reported root axiom list was `propext`, `Classical.choice` and
`Quot.sound`. Comparator was neither inspected nor controlled. The run did not
provide a new independent kernel replay or an RH/GRH verdict.

Next: the v0.3 amendment searches for the first specified application with a more
appropriate bounded traversal order. It does not resume the existence-provider
detour or change the original proof.
