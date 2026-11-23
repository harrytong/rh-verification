# Stage 3: decisive verification and targeted use audit

Prepared for Harry Tong on 23 November 2026 (America/New_York).
Status: proposed protocol; no Stage 3 experiment has been executed.
The Stage 1 and Stage 2 results below were already known when this plan was written.
Freeze the implemented protocol, fixtures, budgets and selection manifests before collecting new experimental outcomes. Do not describe this document as preregistration of results already observed.

## 1. Questions and decision rules

The primary question is whether the pinned artifact supplies valid proofs of the independently specified RH and Dirichlet-GRH statements, relative to the permitted axioms and the stated verification assumptions. The secondary question is what the disputed auxiliary geometry and height constructions actually contribute.

These questions must not be conflated. If the exported proof checks under independent kernels, its statements and all statement-defining dependencies match a trusted challenge, and only permitted axioms are used, an auxiliary predicate being True does not by itself invalidate that formal proof. Conversely, a descriptive census or a successful local abstraction is not an independent proof of RH.

| Possible evidence | Permitted conclusion | What it does not establish |
|---|---|---|
| Completed protected comparison, permitted-axiom audit and configured kernel acceptance | The pinned artifact meets those formal verification checks, subject to their trust assumptions | Absolute soundness, a human-readable explanation, or correctness of every mathematical name used internally |
| Concrete mismatch between a headline's mathematical definitions and the trusted challenge | The artifact has not proved the required statement through that comparison | That RH is false |
| A reproducible, used unpermitted axiom or unchecked declaration | The affected artifact fails the specified verification standard | That RH is false |
| A supported, well-formed proof export is rejected for a specific invalid inference | A concrete proof-checking failure needing reproduction and isolation | Automatic diagnosis of its cause; unsupported syntax, tool incompatibility and resource exhaustion are separate outcomes |
| A local semantic contract is disproved on the actual constructed object | That contract or proposed interpretation is false on that object | A flaw in the final proof unless the final derivation actually requires that contract |
| A disputed value is a hypothesis witness at a checked application | It has that local use | Global indispensability, unsoundness, or that the mathematical hypothesis is substantive |
| A replacement fails to elaborate | That attempted replacement failed | Necessity or invalidity of the original proof |
| No flaw is found in selected tests | Those tests found no flaw | Exhaustive refutation of all possible criticism |

Decision language: `formal checks passed`, `specific failure reproduced`, `local role established`, or `unresolved`. Do not force a binary answer when evidence remains incomplete. Formal invalidity of an artifact and falsity of RH are different claims.

## 2. Frozen baseline and completed evidence

- Project commit: `753431bfe28701f6f3937f664fcaf08daa139c03`.
- Mathlib commit: `0df444a360eaa60ab8c11dca51a86af692955474`.
- Proof compiler: Lean 4.33.1; existing judging environment: Lean 4.36.0.
- Main.olean SHA-256: `9146dfb4148e24d2252e04c50742f3e49dd126dfcc5006d10bf5f873ddf796ad`.
- Statements.olean SHA-256: `f8e0aed3c2d69390b6dd3bb24e13aa25e043a02ca42f021e3f6e4ec8b57fd6b1`.
- Solution export SHA-256: `5ea74b912147c5c93cc2b6d70cc727cf908df2f62ac6a20480a3fa02f6be244e`.
- Challenge export SHA-256: `bd484ac9886a96f26b1d9a7a59ebd45b7a70d102c015d4f31f9302bbdd6ab2b9`.
- Permitted axioms: `propext`, `Classical.choice`, `Quot.sound`.

The original build, statement examples, axiom reports, matching published export and standalone Nanoda check are completed evidence. Nanoda reported no typechecker errors and one pretty-printer diagnostic. Comparator was still running at the last user report. Its completion must be recorded, not presumed.

Stage 2 census completed 213,831 of 214,234 definition analyses in a union of 1,478,222 declarations; 403 were unknown. Of completed definitions, the four primary category counts were 294, 600, 130 and 9. These count definitions containing matching sites, with overlap; they do not count invalid steps or individual fields. Record inspection reached its depth bound for 12,603 definitions. Only the first 20 unknown diagnostics were retained.

The already observed local transport results used universal-predicate or universal-closure assumptions. They do not show a genuinely restrictive geometry predicate suffices in the headline theorem. The Stage 1 old route through `hypsE₂`/`plugAll` was absent from the pinned headline closures; do not treat it as the active route.

## 3. Priority A: final-statement and proof-integrity checks

### A1. Finish the existing Comparator record

Leave the existing process and inputs untouched. On completion, retain the complete log, exact executable and input hashes, configuration, process exit status, statement-comparison result, axiom result and each configured checker result. An overall shell success marker alone is not a substitute for inspecting the actual checker output. Record incomplete or incompatible stages separately.

If a stage fails, first classify the failure: typechecking rejection, statement mismatch, prohibited axiom, unsupported export feature, version mismatch, out-of-memory, timeout, logging failure, or other process failure. Reproduce only the failed operation in isolation after identifying it; do not rerun the whole build automatically.

### A2. Independently ground the five intended statements

Use a trusted Mathlib-only environment to specify all five target propositions. This environment must not import Main or project-specific elaborators, notation or instances. Verify the exact pinned Mathlib/core provenance. Retain the elaborated expression, universe levels, typeclass instances, casts, quantifier domains and transitive statement-defining dependencies, not only a pretty-printed alias.

The corresponding Main-side statement must be compared against that independent specification; a second example compiled after importing Main is useful but does not independently protect the meaning of imported definitions. Reuse the existing protected comparison rather than duplicating its expensive kernel replay.

Check: the natural-number domain in the trivial-zero exclusion; Complex and Real arithmetic and order instances; riemannZeta; the critical value 1/2; the exclusion at s = 1; the positive modulus condition; the Dirichlet character and L-function definitions; and primitive-character restrictions. Explicitly state that the GRH target here concerns Dirichlet L-functions, not every possible generalized L-function formulation.

Success: all five elaborated targets and their defining dependencies match the trusted specifications, with no added assumptions. A mismatch is a priority finding to isolate. A changed spelling that is definitionally equivalent is not a mismatch.

## 4. Priority B: targeted application and contract audit

For every target, produce an evidence packet containing the fully qualified declaration and module, original source hash, raw type and value, local context, exact application or projection, instantiated binder types, argument values, and a complete reference path to an identified headline root. Separate a stored type reference from a proof-body application. Show more than a membership-table yes.

### B1. The active anyGeometry route

Primary declarations:

- `GlobalTheory.Mem.Top.Bl.anyGeometry` and `geoCl`/`GeoCl`.
- `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound`.
- `GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt`.
- The called `open_and_linked_of_stronger_extension_alt`, `linked_bundles_l3_of_open_alt`, and `allRows_of_open0_alt` declarations, resolving and recording their complete names from the pinned environment.

The copied baseline contains three explicit `geoCl anyGeometry` arguments. Record each application separately. Identify how `hOpen1`, `hOpenA`, `hFun` and `hL3` are produced and consumed, including the obligations discharged by projection functions such as `fun ... x => ⟨x.1.1⟩`.

Tests:

1. Distinguish supplying a predicate parameter from supplying a proof of a proposition involving that predicate.
2. Trace actual construction and later projection of the geometry field in `OAt`/`OX`; establish whether it is demanded at the relevant use or is transported alongside other fields.
3. Build an obligation table for all premises of the active bundle theorem, not just the geometry parameter. Trace their actual suppliers toward `allChi`/`rhOfAll` until assumptions are discharged or an explicit audit boundary is reached.
4. Generalize a small connected group of affected declarations to arbitrary `P : GeoP`, preserving explicit parameters across helper boundaries. Every remaining specialization to the original predicate must be listed. Retain the first elaboration error and its precise type context.
5. If feasible, formulate the exact weaker premise needed at each application rather than imposing universal P by default. Recheck copied proof bodies under that premise. Report sufficiency only; claim a weakest premise only with a separate necessity argument over a clearly specified interface.

Do not read a failure caused by an unchanged specialized helper as an unsatisfiable mathematical premise. Do not call a wrapper that ultimately invokes the unchanged original target a reconstruction without the questioned route.

### B2. Degenerate-model construction and preservation of information

Primary declarations:

- `Formalism.L2.Geo.geoDegenerate`, `algDegenerate`, `padDegenerate`, `mdlJunk`, `divXFl`, and `famFlJ`.
- `GlobalTheory.Mem.Top.DivRec.geoOver_stages`, `exists_divT`, `divEx_prov`, `divEx_of_ox`.
- `GlobalTheory.Mem.Top.Closing.divEx_geoCl`, `memberE_closing_alt_alt`.
- `GlobalTheory.T.member_exists_baseLattice_alt` and its active callers.

Inspect the actual zero-map, zero-measure and unit-valued fields at these construction/use sites. For each, record whether the receiving binder is a proposition, ordinary data, an instance, a type parameter, or a dependent structure component. Follow the projections used to derive the next numerical or analytic conclusion.

Where a critic proposes that a geometric model must have a nonzero rank, positive degree, nonzero measure, genuine surface witness or injective map, write that proposed contract explicitly and identify its provenance. Do not assume it merely from a declaration's name. Test the actual model against that contract, and determine whether a caller's declared theorem requires it.

For the absent `geoOf`, `geoOf_surf`, `GeoTiedP.geoTied`, `GeoTiedP.formsTieX` and `degree_value_of_determinant`, inspect whether their mathematical content is supplied by another active declaration. Absence of the named wrapper is not absence of an equivalent argument.

An optional local false-predicate experiment may test whether a particular existence package genuinely needs a geometry witness. If an explicit instance makes its target empty and Lean checks that fact, it establishes that local constraint. It does not refute the original theorem using a different predicate. Arbitrary 0-to-1 or Unit-to-Bool edits are not valid nondegeneracy experiments without satisfying all dependent fields.

### B3. The height construction: fixed-object identity versus assigned data

Primary declarations:

- `GlobalTheory.EX.OB.LedPart.pt` and `LedPart.ht`.
- `Formalism.BasicNotions.DV.hExpl6`.
- The relevant `setDiv`, `divTr`, point-record height field and preservation/transport declarations.
- `SelfIntersectionVolumeEstimates.topCovolSlim2_use_alt_alt` and the actual height/covolume declarations on the active route, as the recorded graph establishes them.

The source defines ht from hExpl6, builds a new point over `setDiv ... p.ht`, and fills a field named h_eq by rfl. This is a construction to examine, not by itself an erroneous identity.

Tests:

1. Retry pt and ht with larger classification budgets, recording whether the failing component was the whole value or a nested field. A failure in one nested field must not erase known results for unrelated fields in the new diagnostic report.
2. Print the exact type of h_eq and the two sides of the equality after dependent substitution. Identify which base object each side belongs to before and after setDiv.
3. Distinguish an assigned coordinate from an independently defined invariant of a fixed object. If the intended interpretation requires an intrinsic height or volume, state that invariant separately and find the actual comparison/preservation lemma used.
4. At the first numerical consequence that consumes this construction, record all positivity, nonzero, injectivity and normalization hypotheses and their actual witnesses.
5. A kernel-checked counterexample to a proposed interpretation is a local semantic finding. It becomes an artifact-invalidity finding only after demonstrating that the fixed final claim requires the false contract and the actual verification fails or uses an inadmissible assumption.

### B4. Optional elimination certificate

Attempt only bounded, targeted simplifications with a useful expected result. To show a named construction is avoidable, produce a newly checked proof of the same target whose transitive proof dependencies exclude that construction under the documented traversal. Report residual synonyms, aliases and corresponding constructions; name removal alone may only show that one spelling was unnecessary.

Equality of two proof terms by proof irrelevance is not a dependency-elimination certificate. A failure to eliminate a dependency does not prove necessity. These are secondary tests, not a reason to launch a fresh full rebuild while Comparator runs.

## 5. Daniel's descriptive and sampling requests

### C1. Existing rates and counting universe

| Cohort | Classified definitions | Unknown/attempted | Unknown share | True/1,000 | Unit-field/1,000 | Zero linear map/1,000 | Zero measure/1,000 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Five-headline union | 213,831 | 403/214,234 | 0.1881% | 1.375 | 2.806 | 0.608 | 0.042 |
| Existing independent Mathlib control | 5,768 | 3/5,771 | 0.0520% | 4.334 | 0.867 | 1.040 | 0.347 |

Both use reachable `.defnInfo` declarations, including compiler-generated definitions with no exclusion filter. Theorem statements/bodies contribute to graph traversal, but theorem declarations are not counted as definition values. Do not call definitions containing unit fields individual fields. Separately report hit-site totals and the number of all inspected fields.

### C2. Second independent controls

Keep the original three-root control intact. Before classification outcomes are collected, record two additional Mathlib-only root manifests from distinct mathematical areas:

- all theorem declarations whose recorded originating module begins `Mathlib.AlgebraicGeometry.`;
- all theorem declarations whose recorded originating module begins `Mathlib.Probability.`.

These are explicitly module-family unions, not single-theorem closures and not random samples. Root membership is determined from module metadata, not string matching theorem names. Validate availability at the pinned Mathlib revision; abort and document an amendment if a selected family is absent. Hash and timestamp each sorted root manifest before its semantic run. Do not choose or adjust roots after seeing hit rates.

Use fresh Mathlib-only processes, verify Main/headline declarations are absent, and use the same traversal, categories, definition eligibility, baseline budgets and field depth as the main census. Report actual sizes, overlap in definition names, generated-definition treatment, unknowns, depth limits, and rates. Do not promise size matching; report variation across cohorts without p-values or a null-model interpretation. If resources require one control first, AlgebraicGeometry precedes Probability.

### C3. Candidate registry and reproducible use sample

The old aggregate output does not retain all candidate names. Collect the complete primary-category candidate registry during the diagnostic replay: declaration name, origin module, site path, instantiated type, category and value fingerprint. Preserve the old aggregate counting units.

Before inspecting new use outcomes, freeze this sampling rule:

1. Build the unique definition-name list for each of the four primary categories from the full headline registry, including generated definitions and all origins.
2. Order names by SHA-256 of UTF-8 `RH-stage3-use-v1|<category-label>|<fully-qualified-name>`, breaking ties by exact name.
3. Select the first min(12, N) definitions per category. With the old counts this would give 12 + 12 + 12 + 9 = 45 category slots, possibly fewer unique definitions because of overlap. If replay counts change, report the change and apply the same frozen rule.
4. Preserve category membership when deduplicating work. Publish the complete selection manifest before inspecting the use classifications. For selected definitions inspect all recorded matching sites within the census scope, not only a convenient example.
5. Report definition-level results separately from site/application-level results. A definition may have several roles. Do not count one observed witness application as proof that all uses or all five roots have that role.

The named B1-B3 targets are an additional hypothesis-driven case series. Keep them separate from the deterministic sample; do not insert them into it to obtain a preferred split. The sample tests the method and supplies examples; it is not a representative random estimate of all witness uses.

Use a fixed set of labels, with multiple labels allowed:

- `propositional-witness`: an actual checked application supplies a proof argument to a Prop-valued binder and the instantiated obligation or its witness depends on the candidate. Show the obligation and the dependency link explicitly. The candidate predicate may occur in the obligation even when True.intro, rather than the predicate itself, is the argument.
- `dependent-data-witness`: ordinary data supplied to a dependent construction that subsequently provides such a proof; show the construction and the consuming proof application.
- `ordinary-data-or-parameter`: an actual data/type/instance/predicate argument without an established hypothesis-discharge link at the reviewed application. This is a local description, not a global nonuse claim.
- `signature-reference`: occurrence only in a declaration type or an instantiated signature in the evidence examined.
- `construction-reference`: occurrence in a value or helper body, with no use-role link yet established.
- `eliminated-in-checked-reconstruction`: the stated bounded reconstruction removed the reference, with the certificate described in B4.
- `unresolved`: limits, inaccessible opaque details, missing producer-consumer link, or ambiguous reduction prevent classification.

Inspect argument roles by instantiating the called function's dependent telescope in the current local context. Detect Prop using the instantiated binder type, not the variable name or binder index alone. Handle let bindings, lambdas, instances, record projections and local proof variables. Track field origin through projections where possible. Pure substring occurrence or a shortest graph path is insufficient.

Report both a bounded occurrence review and any positive witness-use evidence. Do not label a candidate ordinary-only or globally unused unless all relevant occurrences under a specified complete scope have been checked. Every item is already in a dependency closure: "off the path" is not a valid substitute for this analysis. Separate root-specific evidence from reference paths involving theorem types only.

### C4. Recover all unknowns and retry selected cases

Because only 20 samples were saved, the exact 403-way diagnostic split cannot be reconstructed from the old ZIP. Run one bounded diagnostic replay of the original main cohort and controls with full unknown and candidate logging; do not rebuild Main or write a giant edge graph.

Keep the baseline classifier, categories and resource bounds unchanged as far as possible. Record any instrumentation change and any count drift rather than retroactively rewriting Stage 2. Preserve original classification outcomes and counts in one table; report diagnostic retries and recovered classifications separately.

For each failure retain: declaration, site if available, analysis phase, exception category, rendered message in a live context, raw heartbeat budget/usage, monotonic elapsed time, recursion limit, and result of any retry. Split timeouts, zero-instance synthesis failures, unresolved metavariables, recursion/depth limits, unsupported shape, and unexpected exceptions. Do not collapse every zero-related failure into a proof failure or a timeout. Retain successful partial site analyses separately if an overall definition remains unknown; do not add partial hits to the old completed-definition rate.

The original per-definition budget was 2,000,000 internal heartbeats, displayed by Lean as 2,000 heartbeat units, with recursion limit 2,000; it was not a seconds-based timeout. Record inspection had depth four.

Retry pt, ht, hExpl6 and all named B1-B3 targets that remain unknown at 10x then 100x that raw heartbeat budget, preserving baseline field depth. An outer 120-second wall-clock guard per targeted retry may terminate a job but must be labeled separately from a heartbeat timeout. Resource-limit outcomes remain unknown. Do not classify another cohort with the higher limits and compare it directly to the old lower-budget rates.

For zero-instance failures, first determine whether the expected Zero instance is unavailable because the probe lost a local instance or cannot reconstruct a dependent type. Validate fixes in small positive and negative fixtures. Any revised classifier gets a new method version; comparable new rates require applying it to all compared cohorts.

## 6. Execution order, fixtures and resources

1. Freeze and publish this decision framework, the implemented protocol and fixture results. Keep known Stage 2 results visibly separate.
2. Complete small positive/negative fixtures for use classification and diagnostics, with no Main import. Include a genuine proof argument, a predicate parameter that is not a proof argument, a data field later used by a proof, a signature-only reference, a removable unused let, a generated definition, a dependent Zero-instance case, and a forced resource failure. A failed fixture blocks the relevant phase.
3. Run targeted B1 and B3 inspection first; these have the highest immediate value. Perform B2 next. Each session should import Main once and reuse the environment within the same process where practical.
4. In a separate serial phase, perform the original-budget diagnostic census replay, preserving all candidates and unknowns, then freeze the sample manifest.
5. Run the sampled application review, followed by the additional independent controls. Report progress and intermediate artifacts by phase, not as a new proof verdict.
6. When Comparator finishes, incorporate its actual results into the final verification ledger without changing these diagnostic findings.

On Harry's current server: original project, toolchains, exports and running Comparator remain untouched. New files go under a separate stage-3 output directory. Use one audit process/container at a time, initially capped at 2 logical CPUs and 100 GiB with no extra swap allowance; inspect host available memory before importing Main alongside Comparator. Do not start a second process because the first is quiet.

Maintain at least 20 GiB of free disk as a planning reserve and stop before starting a phase that cannot fit within the remaining output allowance. Target at most 2 GiB of new output for Stage 3 by logging selected applications and compact records, not full million-node expression dumps. Do not copy the 57 GiB export, delete existing evidence, or initiate an entire counterfactual build. If a later whole-project mutation becomes justified, design it as a separate isolated experiment with its own space assessment and baseline rebuild.

No runtime estimate is promised before pilot measurements. A 72-thread environment variable does not turn these metaprogramming traversals or the observed paranoid checker into parallel workloads.

## 7. Publication and stopping rules

Publish under a separate `stage3/` directory: protocol and hashes, source/Mathlib/toolchain pins, code, fixture logs, candidate/control/sample manifests, complete unknown diagnostics, typed use packets, local contract probes, rates with denominators, a verification ledger, and concise findings with limitations. Do not overwrite Stage 1 or Stage 2. Preserve unsuccessful probes and first errors. Disclose ChatGPT assistance.

For each target report: allegation, exact formal contract tested, baseline result, experimental result, axiom/checker status, root/use connection, and the narrow conclusion supported.

Stop expanding a diagnostic avenue when its result cannot affect a stated allegation or resolve a specified uncertainty. Escalate immediately when a concrete statement mismatch, prohibited dependency or reproducible supported-kernel rejection appears. Reduce such a finding before publicizing it as invalidity. If a local interpretation fails but the formal target remains verified, publish that distinction explicitly.

Successful primary formal verification need not wait for every census unknown to be resolved. Conversely, successful semantic statistics cannot replace the primary formal checks.

## Methodological reference

Lean Language Reference, "Validating a Lean Proof":
https://lean-lang.org/doc/reference/latest/ValidatingProofs/

The reference distinguishes axiom auditing, replay, trusted challenge statement/definition comparison, configured independent kernels, and remaining trust assumptions. This plan applies that distinction rather than treating descriptive triviality counts as a proof-validity test.
