# v0.4: filter branches by stored constant references

Prospective amendment after the v0.3 result. Input evidence SHA-256:
`237f0e325bb09eef1c37b5fd0a8800836b61791e3e92e90e804fdecbfcdd29a4`.
The v0.3 slope caller scan again exhausted 250,000 visited nodes with zero matches.
The three generic comparisons and applied valuation comparison remained
not-definitionally-identical. No slope-application conclusion was obtained.

## Method change

Before descending into a subtree, obtain `Expr.getUsedConstants`. If no watched
callee name is present, skip that subtree. A direct syntactic application must
contain the callee constant; this is a necessary condition, not an assertion
that every retained subtree contains an application in a proof position.

The reference extractor may include annotations, so retained branches can still
be irrelevant. The walker continues to omit binder annotations. No declaration
body is unfolded to search for a call. A local let value is still visited in its
own branch, under the proper local context. This filter does not establish
absence from a transitive dependency closure.

Record the whole owner's direct constant-reference count, the first 256 names
with a truncation flag, and the complete intersection with the watched names.
This distinguishes a traversal budget problem from an absent direct reference.
It also makes possible a concrete diagnosis if elaboration placed the source
call in a separate auxiliary declaration. No automatic auxiliary expansion is
added in this version.

Record `pruned_subtrees` in scan outcomes. Keep the first-application scope,
comparison logic, targets, source pins, wall-time and memory caps unchanged.
The 250,000 node bound counts walker visits, not the internal work done by
`getUsedConstants`. Reference extraction is not claimed to have its own node
bound; the container wall-time/memory guards still apply. Core heartbeat limits
apply within the existing Meta action, but are not a separate guarantee for
every pure reference-extraction operation.

## Controls and interpretation

All previous comparison and first-match controls must pass with filtering active.
An extra theorem with no watched call must produce zero comparisons and at least
one skipped subtree. A missing expected application in the project remains
unresolved even if its name is absent from the owner's immediate references.

Both previous protocol hashes and this amendment's hash are recorded. The result
is about the inspected first application only, never all uses or necessity.
The original registered interpretation rules remain unchanged.
