# Stage 3.3: consumer implementations and source provenance

Protocol v0.4, prepared 23 November 2026 before these probes run against Harry
Tong's compiled environment. The runner hashes this protocol, the target
configuration, package manifest and selected inputs.

## Prior evidence

The v0.3 run established that `OAt Γ` requires Γ and `LamAre`, that
`OAt anyGeometry` requires `LamAre`, and that the corresponding False domains
are empty. Acceptance of an arbitrary-predicate supplier therefore does not
show that the original inhabited route ignores geometry.

Collected source forwards a `ClassSumPin` argument, stores `ties` in a row
record, and invokes a height-comparison theorem through a wrapper whose
`PublishedHodgeBundleTheorems` argument is unused. These observations do not
settle what the underlying constructions or consumers require.

## Fixed targets

Eight targets are selected from prior recorded code, not new probe output.
Exact names and budgets are in `provenance-targets.json`.

| Target | Question for source review |
| --- | --- |
| `GlobalTheory.Fc.RL.at_tie_alt` | How is the tied comparison witness obtained, under which assumptions? |
| `GlobalTheory.BigTop.PtAt.nmjT_at_tied_alt` | How does the consumer handle the forwarded class-sum hypothesis? |
| `GlobalTheory.T.eventually_onPt_of_pDiv_ties_and_onPt` | Which row fields and tiedness conditions are needed to pass to points? |
| `GlobalTheory.Fc.Ind.RowPointSummands` | What is the interface of the supplied row data? |
| `GlobalTheory.CovHt.FrameCmp.htCmp` | What establishes the height comparison below the wrapper? |
| `GlobalTheory.CovHt.HTCmp` | What is its exact proposition and quantified domain? |
| `GlobalTheory.CovHt.cover_height_comparison` | Confirm the wrapper-to-implementation relationship in the same environment. |
| `GlobalTheory.Fc.Ind.eventual_L3_of_covolume_alt` | Locate the row-to-point consumer from the recorded caller. |

The bare names `recVals` and `htVals` occur in the previously collected `HTCmp`
source. Their fully qualified names must be obtained from compiled references;
this package does not guess their namespaces or require guessed targets. Their
owner modules will be collected if present in retained eligible references.

## Method and gates

1. Run the existing positive and intentional negative fixtures without a project
   mount. Failure stops the run.
2. Run a new isolated fixture containing exactly the same provenance helper as
   the project probe. Require a known body reference, a known type reference,
   exclusion of an unreferenced declaration, theorem-body recognition, an
   imported declaration's module, and an explicitly reported zero-budget cap.
3. Import pinned `Main`; print each target's declaration and axiom list. Require
   each nonempty print block exactly once in configured order.
4. Record declaration kind and module via compiled environment metadata.
   Enumerate `Expr.getUsedConstants` separately on the stored type and available
   definition/theorem/opaque body. Retain at most 4,096 entries per location;
   record total, retained and truncated. No unfolding or transitive compiled
   graph traversal occurs.
5. Collect target source modules first, directly referenced project modules in
   lexical order second, and one level of source imports last. Only configured
   project prefixes are eligible. Verify each file byte-for-byte against the
   pinned git revision. Record missing paths, skipped prefixes and caps.

Limits: 160 copied source files, 2 MiB per file, 8 MiB total; 64 MiB log per
step; 30 minutes per project probe by default. Limits imply incomplete
collection, not absence. Imported sources are context, not established proof
dependencies. Reference ordering is the stored-expression traversal order;
module selection after the targets is lexical and reproducible from the log.

## Interpretation fixed before outcomes

* A direct stored reference is syntactic. It does not establish necessary use,
  discharge of a hypothesis, or mathematical content.
* `type` includes binders and conclusion. `body` includes annotations and
  implicit arguments. No finer use classification is inferred automatically.
* Names follow Lean's `getUsedConstants` implementation. This probe does not
  separately classify projection metadata or every occurrence. Review the
  collected implementation before claiming a field is consumed.
* An unused wrapper argument does not invalidate a theorem: its callee may
  establish the result from other inputs. Zero and unit constructions may be
  legitimate. Their actual interface and interpretation must be examined.
* An empty alternative domain can explain local vacuity. Showing the original
  headline proof uses it requires its actual instantiation and consequence.
* A source module can contain unrelated declarations. Membership in a copied
  module is not membership in a theorem's stored reference set.
* Printed expressions may be elided. Block hashes authenticate rendered text,
  not complete raw proof terms. An elided printout cannot establish absence.
* Missing targets, malformed records, mismatch, timeout and tool errors mean
  incomplete collection. Preserve the first error; do not infer proof failure.

Completion means the requested collection and input checks finished. It makes
no new RH/GRH correctness, flaw or necessity verdict and performs no independent
kernel verification. Comparator is untouched. Selective input checks do not
authenticate every compiled dependency.

## Outstanding work

Daniel Fairbanks' second control, full project/library/instance strata, every
unknown's reason and budget, larger-budget `LedPart.pt` classification and a
preregistered sample of actual witness use remain outstanding. These deliberately
chosen cases are not a representative sample or a substitute for those controls.
Interpret the returned implementations before choosing any further intervention.
