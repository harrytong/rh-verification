# Verification update — 26 November 2026

Snapshot: **18:54:42 EST / 23:54:42 UTC**. Supplied by Harry Tong from his
Ubuntu AI-Server. This report analyzes supplied execution output; the
publication assistant did not rerun the checker or access the server.

## Result

**The tuned standalone Lean paranoid replay passed.** `/usr/bin/time` reports
exit 0, the checker wrapper reports exit 0, and Docker/checker and logging
statuses are both zero. The original protected Comparator remains pending.

| Run / step | Recorded status |
| --- | --- |
| Original Comparator: Lean paranoid | Accepts the solution |
| Original Comparator: nanoda | Accepts the solution |
| Original Comparator: Lean default kernel | Running; elapsed 24:03:08 |
| Original Comparator overall | Pending; process elapsed 111:11:27 |
| Separate tuned paranoid replay | Passed; elapsed 21:43:05 |

The separate replay is the same stock Lean paranoid implementation with an
allocator environment setting. It is not an additional independent kernel
implementation and does not substitute for the original Comparator’s final
statement-matching and permitted-axiom verdict.

## Credit and configuration

**Credit: Andrew Sutherland (MIT)** documented
`MIMALLOC_GENERIC_COLLECT=1000000` and comparative runs in his
[RH verification record](https://math.mit.edu/~drew/grh/).
Harry applied that setting locally. This report does not claim that Harry
invented the tuning or that the elapsed times constitute a controlled benchmark.
Sutherland’s own runs and conclusions are separate from Harry’s local results.

- Lean 4.36.0, commit `611c117bfaf7b7ae1cfcf246ce6fba31e8f509e9`.
- Command: `leanchecker-paranoid --silent --from-export /proof/solution.export`.
- Docker image: `rh-lean-check:1`; container: `rh-paranoid-tuned`.
- Allocator: `MIMALLOC_GENERIC_COLLECT=1000000`; `LEAN_NUM_THREADS=1`.
- Container memory limit: 120 GiB; memory-plus-swap limit: 120 GiB
  (container swap disabled); CPU quota: 2.
- Read-only toolchain and export mounts, no network, read-only container root.
- Export path: `/home/harry/rh-verification/verification-data/solution.export`.
- Recorded export size: 61,570,595,788 bytes.
- Checker executable SHA-256:
  `cd9a6ddb5fbf8f649c789dc905236e1ddee9fb32a323c141a4e63478f72e47b6`.

The export SHA-256 previously recorded in this project is
`5ea74b912147c5c93cc2b6d70cc727cf908df2f62ac6a20480a3fa02f6be244e`.
The tuned startup output records the path and size, not a new SHA-256 of the
export. Do not describe this run as freshly rehashing that export.

## Timing and memory

| Measurement | Raw value | Interpretation |
| --- | --- | --- |
| Checker elapsed | 21:43:05 | 78,185 seconds |
| User CPU | 77,450.83 seconds | Reported by time |
| System CPU | 720.35 seconds | Reported by time |
| CPU utilization | 99% | About one CPU core |
| Maximum process RSS | 103,594,140 KiB | 98.795 GiB |
| Cgroup memory peak | 117,896,380,416 bytes | 109.800 GiB |
| Cgroup memory events | low/high/max/oom/oom_kill/oom_group_kill all 0 | No recorded limit hits or OOM kills |
| time: Swaps | 0 | Per-command counter; not a claim that host swap was empty |

Startup was logged at 10:00:40 EST on 25 November. A finish around 07:43 EST
on 26 November is inferred from startup and duration; the supplied excerpt
contains no explicit checker finish timestamp. The original Comparator started
22 November at 03:43:16 EST. Its original paranoid phase has no per-phase timed
completion record in this excerpt, so no exact speedup ratio is reported.

At the monitor snapshot the host had 169 GiB available RAM, 873 MiB swap used,
and 389G available on the root filesystem. These are host observations, not
peak requirements of either checker.

## Evidence and scope

- [Supplied monitor excerpt](../verification-updates/20261126/monitor-excerpt.txt):
  selected blocks copied from Harry’s message, explicitly labeled as an excerpt.
- [Structured results](../verification-updates/20261126/RESULTS.json).
- The update helper copies the two original server logs into a new timestamped
  directory under `verification-updates/20261126/server-log-snapshots/` and
  records provenance in `COLLECTION.json`. That later snapshot can contain
  new output not covered by this report.

No new Stage 1–4 audit experiments were performed. The previous scoped audit
conclusions remain unchanged. Acceptance of the exported proof by a checker,
end-to-end challenge comparison, and interpretation of auxiliary constructions
remain separate questions.
