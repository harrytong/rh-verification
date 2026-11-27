# Verification record and evidence availability

Closing snapshot: 23 November 2026, US Eastern time. “Recorded” below means
Harry supplied the result, not that the publication assembly reran Lean.

## Headline declarations

`riemannHypothesis`, `riemannZeta_eq_zero_re`,
`LFunction_ne_zero_of_half_lt_re`, `LFunction_eq_zero_re`,
`LFunction_eq_zero_re_of_isPrimitive`.

## Recorded checks

Preparation began around 01:00 EST on Saturday 21 November; compilation began
around 02:00 and the successful build was reported around 19:05. This overall
timeline includes an initial failed module and retries. The final timed
`lake build Main` retry reported 1:24:04, exit 0, and 183,893 jobs; it is not
the elapsed time of a clean build of every module from scratch.

The clean headline audit exited 0 and reported only `propext`, `Classical.choice`
and `Quot.sound`. The initial audit with unsupported `pp.width` exited 1 and is
not the successful statement-audit result.

Export completed in 2:29:45, exit 0, producing 61,570,595,788 bytes. Standalone
Nanoda checked 1,484,733 declarations in 1:03:30, exit 0, with no typechecker
errors and one pretty-printer error (`Unable to print axioms`). Preserve that
diagnostic when quoting its success. Standalone Nanoda is not the full protected
Comparator operation.

The last supplied Comparator log says `Running Lean paranoid kernel on solution`.
No completed outcome is asserted. A later server-log snapshot may contain new
output; it must be inspected before changing the status. The publication scripts
never stop, restart or run Comparator and do not interpret a partial log as a verdict.

## Identifiers

| Artifact | SHA-256 |
| --- | --- |
| `Main.olean` | `9146dfb4148e24d2252e04c50742f3e49dd126dfcc5006d10bf5f873ddf796ad` |
| `Statements.olean` | `f8e0aed3c2d69390b6dd3bb24e13aa25e043a02ca42f021e3f6e4ec8b57fd6b1` |
| `solution.export` | `5ea74b912147c5c93cc2b6d70cc727cf908df2f62ac6a20480a3fa02f6be244e` |
| protected `challenge.export`, as recorded | `bd484ac9886a96f26b1d9a7a59ebd45b7a70d102c015d4f31f9302bbdd6ab2b9` |
| Nanoda executable, as recorded | `8241c5e6baa29490aa118d382f97961b208ae730fdb96545c2abed74c9ece5a8` |

Source revision: `753431bfe28701f6f3937f664fcaf08daa139c03`.
Mathlib revision: `0df444a360eaa60ab8c11dca51a86af692955474`.
Project audit toolchain: Lean 4.33.1. Judging toolchain: Lean 4.36.0,
commit `611c117bfaf7b7ae1cfcf246ce6fba31e8f509e9`.

## Available and missing material

The consolidated archive preserves supplied evidence ZIPs and their extracted
contents. Stage 2 transport and semantic-census archives are available here;
some earlier inspect/abstraction and failed smoke runs exist only in pasted
terminal records or on the server until the local collector adds them.
Stage 3 code is available through v0.14; supplied evidence through v0.13.
Stage 4 evidence includes the failed v0.1 fixture and incomplete v0.2/v0.3/v0.6
collections, as well as later completed selected collections.

`server-snapshots/`, if present, contains additional data copied by the local
collector. Its JSON index records source paths, hashes, deduplicated files,
exclusions and files that changed while being copied. These added files have
not automatically received the same interpretive review as the uploaded runs.

Multi-gigabyte proof exports, compiled build caches, model files, credentials,
and unrelated server files are outside this publication. Hashes identify the
exports without committing their bytes. The collector does not traverse the
proof checkout or Docker storage. No original log is fabricated from a chat
summary. Source snapshots are bounded extracts, not the entire proof source tree.
