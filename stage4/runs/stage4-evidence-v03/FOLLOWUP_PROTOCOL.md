# v0.3: bounded first-application follow-up

This amendment follows the v0.2 run, before any v0.3 outcome. It changes search
order and stopping rules, not the expressions compared or the comparison test.
Both the original protocol hash and this amendment's hash are recorded.

## Trigger

The v0.2 evidence ZIP has SHA-256
`0eaea5fa6c8e448e65b4521876606d47eb09683d61774eb7a21b18f29313bc58`.
Its three generic conclusions and its `htCmp → val_le` application had different
sides under the definitional-equality test. The scan of `heightAt_eq_of_cover`
exhausted 250,000 nodes before finding a watched application. That is incomplete
coverage, not absence of a call or evidence of proof failure.

## Prospective change

For each of the same two caller/callee pairs, search maximal application spines
in descending argument-index order and visit let bodies before let values. Keep
the same correct local context and original let values. This order is chosen
because dependent type arguments can be large, while proof arguments often occur
later. This is a search heuristic, not a claim about every argument's role.

Stop after the first application of the named callee has been inspected. Record
`first-match-observed`, the path, inferred type comparison and count. An unsupported
type or comparison exception stays unresolved. If a branch was skipped by a cap,
record `scan_capped` even when another branch yields the requested application.
A found application's local comparison is valid evidence about that application;
it is not exhaustive evidence about all applications.

Only `slope_le_height` is watched in the first owner and `val_le` in the second.
The additional search for `le_refl`/`le_rfl` is deferred, so it cannot consume this
target's search budget or stop it at an unrelated auxiliary premise. The source
snapshot preserves the auxiliary-premise evidence for human review.

The three generic probes, statement example, assigned-height control, source
pins, runtime protections, limits and definitions of comparison outcomes remain
unchanged. An additional first-match fixture must pass. This amendment supersedes
the original protocol's exhaustive caller scan and auxiliary-call search for v0.3.

## Output interpretation

`collection_complete` now means all requested generic results and the first
application result for each selected pair were obtained without a comparison
unknown. `exhaustive_application_coverage` is always false. No absence claim is
permitted from an early stop. Even two different call-site sides do not rule out
a further upstream specialization, and the paper's exact targeted inequality must
still be identified before adjudicating its assertion.

This follow-up has no predetermined desired result. Identical sides support the
local identity claim; different sides oppose it at that instance; missing or
unclassified instances leave it unresolved. None is an RH/GRH validity verdict.
