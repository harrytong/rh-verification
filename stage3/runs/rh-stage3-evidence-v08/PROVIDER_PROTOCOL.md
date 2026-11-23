# Stage 3.5: class-sum supplier and selected occurrence searches

Frozen on 23 November 2026 before this package's project execution. The runner
records this file and provider-targets.json hashes before probes.

## Motivation and selection

v0.5 retrieved a concrete rewrite using a class-sum hypothesis, but 79 of 113
per-binder counts hit the node budget. No zero count from those incomplete
scans establishes non-use. This increment asks who provides that hypothesis
and retrieves selected occurrences without repeating a full body census.

Prior pinned source gives the following local route:

* LinkedTies.lean, GlobalTheory.GeoTies.linked_ties_alt, obtains hcs from
  GlobalTheory.T.class_sum_divisibility_of_extensionWithLaw and applies hcs.2
  to a divisor-condition proof at lines 74–75.
* PNmjOfPDivOfClassSumPin.lean forwards hpin to the lattice-family wrapper.
* NmjTAtTied.lean forwards hPin into the class-sum comparison.
* EMEqThPe.lean forwards hP to at_index_alt, where hP supplies a rewrite.

These are selected local source relations; the package does not certify that
this is the unique or necessary route for the headline proofs.
Eight targets and five binder searches are fixed in provider-targets.json.
Their compiled owning modules and direct references determine source retrieval.
Target owners are prioritized, followed by direct-reference owners containing
ClassSumPin, LinkedTies or EMEqThPe, then remaining owners in lexical order.
One import level, 160 files and 8 MiB total remain the collection limits.
This prioritization is explicit and is not an exhaustive dependency search.

## Search semantics

Select the first explicit outer lambda whose stored binder name equals the
configured name, skipping metadata. Record its actual ordinal. Stop with an
error if not found within 256 outer steps or before a non-lambda head. Do not
infer a binder from source spelling if the compiled name differs.

Within the selected binder's remainder, perform a depth-first search with
application arguments before functions, binder bodies before their omitted
domains, and let bodies before let values. Skip lambda/forall domains and let
types, counting each omitted annotation root. Track the selected variable's
de Bruijn index under binders. Projection and metadata bodies are included.
Stop at the first selected bvar occurrence. No unfolding, reduction, type
inference, expression rewriting or environment mutation occurs.

Each search has 100,000 visited nodes and depth limit 600. Paths record the
syntactic traversal. On a hit, record the nearest enclosing application along
the search return path, if any, the branch containing the hit, whether that
child is exactly the selected bvar, and the syntactic function head with its
preceding-argument count. Function-spine inspection is capped at 1,024 links.
A function head may be a bound variable, projection, lambda or other expression;
there is no claim that an unknown head is a missing declaration. Bound-variable
head indices refer to that local context and are not global declaration names.

A found occurrence is positive syntactic evidence even if an earlier branch
was truncated. It is not necessarily a witness discharging a hypothesis: type
arguments, implicit arguments and discarded let values can remain in this
projection. First-hit order is a search choice, not mathematical importance.
Application context is not a certified callee-signature match.

`not-found-in-projection` is NEVER full-body absence. Annotation roots were
omitted deliberately. Truncation additionally marks an incomplete search of
the projection. A recorded application with a truncated function spine cannot
be treated as a fully resolved call. No necessity verdict is inferred.

## Gates and resource envelope

Positive, intentional negative, provenance and targeted-search fixtures run
before a single Main import. Search fixtures cover binding/shadowing,
annotation omission, lets, projections, metadata, node/depth exhaustion (including a positive hit after an earlier
depth-capped branch), argument
and function application contexts, and real stored-theorem extraction.
Synthetic expression fixtures need not be well-typed; they test traversal.
Missing or malformed evidence fails closed and preserves available logs.

The inherited limits remain: 2 CPUs, 100 GiB project memory, 4 GiB fixtures,
no additional swap or network, read-only mounts, 30-minute project timeout,
64 MiB per log, 116 GiB available RAM and 21 GiB free disk required at start.
No Comparator control, rebuild, export copy or global graph/census.

## Interpretation and unfinished work

Report provider prerequisites, actual returned propositions, recorded occurrences
and every cap/error. Inspect the source against compiled provenance. Prints
may be elided; they are not raw proof exports. Source checks compare against
the pinned commit; selected artifact hashes do not cover every .olean.

The supplier, its domain and its actual headline instantiation must be connected
before making a global claim about anyGeometry. No such verdict is precommitted.
Daniel's second control, strata, complete unknown records, LedPart.pt probe and
frozen sampled witness-use classification remain separate outstanding tasks.
