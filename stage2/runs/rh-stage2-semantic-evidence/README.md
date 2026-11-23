# RH/Dirichlet-GRH audit: stage 2, version 1.5

Version 1.5 enables initializer execution before dynamically importing the
semantic environment with extensions. This is required by Lean's import API.
The tool entry point is marked `unsafe` because that runtime API is unsafe;
no mathematical declaration or kernel setting is changed. The procedure
remains sequential inside its sandbox, with imported regions retained until
process exit. The standalone semantic preflight still cannot start a census.

Version 1.4 corrects two multiline structure-literal layouts in the semantic
tool and adds a standalone `semantic-smoke` phase that cannot launch either
census. Version 1.3 adds explicit interface-transport experiments after the first
abstraction run. Version 1.2 corrected a malformed synthetic numeral in the
smoke fixture; version 1.1 fixed the initial two compilation errors. See
CHANGELOG.md. The installation directory remains
`rh-audit-stage2-v1`; no original proof file or prior run log is overwritten.

This package implements the next experiments prompted by Daniel Fairbanks's
two LinkedIn comments. It preserves the original checkout, compiled proof,
exports, and running Comparator. It does not announce a new proof verdict.

## What is ready, and what is still open

| Review request | Version 1 experiment | Limit |
|---|---|---|
| Closure saturation | Recompute fractions and extract all 66 distinct witness edges from completed stage-1 records | Descriptive only |
| Exact RH example | `example : RiemannHypothesis := riemannHypothesis`, explicit expanded RH example, five statement checks, axiom prints, raw stored type expressions | Does not replace protected Comparator comparison |
| Edge classification | All direct references in stored binder domains, conclusion, body, and structural registry; retain multiple labels | A binder domain is not automatically a propositional premise |
| Local minimization | Bounded deletion of explicit unused lets and unused explicit lambda arguments; optional raw/pruned union comparison | Does not remove arbitrary named-constant arguments or globally minimize proofs |
| Abstraction | Generic `GeoCl P` lemmas plus a baseline copy and arbitrary-P versions of the actual bundle theorem's three literal geometry arguments | Imported declarations remain unchanged; this is not a globally generalized Main |
| Census | Fixed syntactic categories and separate bounded semantic tests for definitionally-True predicates, unit fields, zero linear maps, zero measures | Read the preregistration for exact denominators, unknowns, and field coverage |
| Independent control | Fresh Mathlib-only control with the same traversal and tests | Actual size is reported; no matched-size claim |
| Full replacement | Optional fresh isolated baseline and changed-definition builds | Deferred until checkers stop and sufficient storage exists; failure needs interpretation |
| Witness versus ordinary use | Selected paths exposed for review | **Global typed use-role counts remain open** |

See `CENSUS_PREREGISTRATION.md` before running the censuses. The package does
not silently turn syntactic zero-head matches into semantic zero-map counts.

## Validation status at delivery

The Python driver has local regression tests using the completed stage-1
records, controlled subprocess failures, output-path checks, mutation
guards, generated probes, and a simulated orchestration run. Those tests do
not validate Lean execution. The new Lean programs have **not** been
compiled in this workspace: it has neither Harry's pinned compiler nor the
compiled project. Each execution phase first compiles and runs an isolated
Lean fixture on the server. A failed fixture blocks the large Main import.
The semantic phase additionally requires a real Mathlib fixture to pass.
No new server result is claimed by the presence of this package.

## Requirements and pins

Use Harry's existing Ubuntu account and image `rh-lean-check:1`. Python 3.10+
standard library; `git`, `docker`, `sudo`, and the installed pinned compiler.
No downloads, pip installs, `lake update`, export copies, or new Docker image.

- Project: `~/rh-verification/riemann-hypothesis`
- Source: `753431bfe28701f6f3937f664fcaf08daa139c03`
- Mathlib: `0df444a360eaa60ab8c11dca51a86af692955474`
- Lean: `~/.elan/toolchains/leanprover--lean4---v4.33.1`
- Prior evidence: `~/rh-verification/critics-audit/proof-trace-8tnvwr47/records.jsonl`
- New outputs: unique folders in `~/rh-verification/critics-audit-stage2`
- Container: `rh-audit-stage2`; defaults **2 logical CPUs, 100 GiB RAM**, no
  network, no extra swap, read-only root/project/toolchain, writable `/tmp`.

The 4.36.0 judging toolchain is not used or changed by these experiments.

## Start here while Comparator runs

Extract the download into `~/rh-verification/tools`; the archive has its own
`rh-audit-stage2-v1` directory. Then run **only the first phase**:

```bash
python3 "$HOME/rh-verification/tools/rh-audit-stage2-v1/audit_stage2.py" --phase inspect
```

This verifies pins and previous headline hashes, runs a small tool fixture,
compiles the explicit statements, and classifies/prunes the 66 prior edges.
The initial Main import can be quiet. Resource limits apply to the new
container, not to Comparator. Memory pressure can still affect both jobs;
use `free -h` and the new container's stats when assessing host resources.

```bash
sudo docker stats --no-stream rh-audit-stage2
```

Share the printed `stage2-evidence.zip` and the console output. An error
preserves a partial evidence ZIP. If the fixture fails, share its diagnostics;
do not skip it or start the large phases to work around it.

## Subsequent phases, run one at a time

For Harry's completed version-1.2 abstraction run, the next experiment is:

```bash
python3 "$HOME/rh-verification/tools/rh-audit-stage2-v1/audit_stage2.py" \
  --phase abstraction-transport \
  --abstraction-prior "$HOME/rh-verification/critics-audit-stage2/stage2-dhyss28y"
```

This checks the prior run's pins, successful baseline result and baseline
source hash. The new baseline source must match that compiled baseline byte
for byte, so it is not compiled again. Only the two new transport probes run
after the small tool fixture. Both retain the original theorem's other
premises and its imported dependencies.

The first probe assumes universal `auditGamma`, proves
`geoCl auditGamma = geoCl anyGeometry` by function/proposition extensionality,
and rewrites explicitly at the two failed interfaces. The second assumes
universal `geoCl auditGamma` directly. This closure premise follows from
universal auditGamma; strict weakness is not claimed. Neither experiment
infers a weakest requirement on the predicate or generalizes Main globally.
No fresh full project build is involved.

The server's original local experiments compiled four generic GeoCl lemmas
and the baseline. Both untransported variants failed at specialized types.
Their `sorryAx` output comes from failed experimental elaboration, not the
original Main. The new transport probes still require server compilation.

For a fresh initial abstraction run after reviewing the inspection results:

```bash
python3 "$HOME/rh-verification/tools/rh-audit-stage2-v1/audit_stage2.py" --phase abstraction
```

This runs the generic closure interface lemmas, a renamed baseline copy of
the actual bundle theorem, a copy with its three literal geometry arguments
changed to arbitrary `auditGamma`, and a version making universal
`auditGamma` available as a premise. The baseline must compile first. The
probe report stores the **first** elaboration error and a provisional label;
human classification remains pending. The copied proof script does not
infer a weakest precondition or rewrite imported dependencies.

In particular, success at that local boundary does not show the whole proof
is independent of `anyGeometry`, and failure does not establish that a new
premise is unsatisfiable. The generic lemmas separately test that universal
P is sufficient, a seed satisfying P is necessary for a closure witness,
False has empty closure, and anyGeometry has universal closure.

The following are longer traversals, not prerequisites to start `inspect`:

Before the first semantic census, validate only the semantic tool and its
Mathlib fixture with `--phase semantic-smoke`. It does not import Main or
start a closure census. Both `smoke-passed` and `semantic-smoke-passed` plus
phase completion are required before treating that preflight as successful.

```bash
python3 "$HOME/rh-verification/tools/rh-audit-stage2-v1/audit_stage2.py" --phase census
python3 "$HOME/rh-verification/tools/rh-audit-stage2-v1/audit_stage2.py" --phase semantic-census
python3 "$HOME/rh-verification/tools/rh-audit-stage2-v1/audit_stage2.py" --phase pruned-closure
```

`census` reports syntactic shapes. `semantic-census` performs bounded MetaM
tests with structure/instance environment extensions loaded. They are
separate procedures. Missing roots or missing referenced declarations stop
the procedure. Per-definition semantic timeouts are reported as unknown.

`pruned-closure` traverses the raw and locally reduced union in separate
processes. It reports membership from **any** of the five roots, not separate
per-root results. These are analyses of transformed expressions, not new
proof declarations checked by an independent kernel.

## Replacement rebuilds: defer

Read-only planning is available now:

```bash
python3 "$HOME/rh-verification/tools/rh-audit-stage2-v1/audit_stage2.py" --phase mutation-plan
```

The opt-in `mutation-build` phase refuses to start while Comparator,
leanchecker-paranoid or Nanoda is detected. It also requires an estimated
fresh project-build allocation plus source and a reserve. The last reported
65 GiB free on Harry's root filesystem is not a basis for assuming a fresh
full rebuild fits. Do not delete the current proof outputs or export to make
room. A separate Linux filesystem can be selected using `--output` once its
identity, free space and intended use have been established.

When resources permit, an isolated source archive of the exact commit is
extracted to a new experiment directory. Dependency packages and the
original checkout are mounted read-only. The project's own `.lake/build`
starts empty. A baseline `lake build Main` and statement check must succeed
before changing one exact definition. Lake then rebuilds the changed project.
Existing original project oleans are **not** mixed with changed source.

Variants are `benign-beta` (a definitionally equal control) and
`restrict-false` (the strongest restrictive predicate). Each run has its own
fresh baseline and can take substantial time and space. These variants are
diagnostic, secondary to the scoped abstraction tests. They do not construct
genuine non-degenerate geometry. No automatic conversion of PUnit to Bool or
zero to one is attempted.

Successful rebuilds still require independent checking before a new formal
verification claim. Failure logs and first errors must be examined before
assigning mathematical significance.

## Reading and publishing results

Every phase records process exit status, input hashes and pins. The evidence
ZIP excludes the optional full experiment checkout/build. It includes logs,
generated probe sources, specifications and structured records. Reports say
whether a phase completed; **completion of an abstraction experiment means
its outcomes were recorded**, not that every attempted theorem compiled.

Publish completed outputs with their scope. Do not call all remaining uses
ordinary, all True-valued objects vacuous, all reachable definitions
necessary, or a broken interface a mathematical refutation. The final
statement's protected interpretation and the independent kernel checks
remain separate from these diagnostic experiments.

Lean's validation guidance:
https://lean-lang.org/doc/reference/latest/ValidatingProofs/

Daniel's linked draft was not retrievable in this workspace. This version
responds to the two comments Harry supplied and does not claim to have
reviewed that separate draft.
