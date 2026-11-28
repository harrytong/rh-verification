# Local RH / Dirichlet-GRH verification completed

Harry Tong — 28 November 2026

## Result

The original protected Comparator completed successfully on Harry’s home Ubuntu
server. Lean paranoid, the independently implemented nanoda kernel, and Lean’s
default kernel each accepted the exported solution. Comparator reported:

```
Your solution is okay!
Comparator exit status: 0
COMPARATOR VERIFICATION PASSED
```

All five configured headline statements were checked against the protected
challenge, permitting only `propext`, `Quot.sound` and `Classical.choice`.
GRH here refers to Dirichlet L-functions, not every possible class of L-functions.
Harry has concluded this local verification project.

## Timing and provenance

- Original log: `~/rh-verification/logs/comparator-20261122-034314.log`.
- Start: 22 November 2026, 03:43:16 EST.
- Wall time: **141:35:16** = **509,716 seconds** = 5 days, 21:35:16.
- Approximate completion: 28 November, 01:18:32 EST (06:18:32 UTC), inferred
  from the start and duration, not printed as an end timestamp.
- Completion observed in Harry’s monitor output at 03:35:12 EST on 28 November.
- Lean judge: 4.36.0, commit `611c117bfaf7b7ae1cfcf246ce6fba31e8f509e9`.
- Project revision: `753431bfe28701f6f3937f664fcaf08daa139c03`, built with Lean 4.33.1.
- Protected challenge SHA-256 verified before launch:
  `bd484ac9886a96f26b1d9a7a59ebd45b7a70d102c015d4f31f9302bbdd6ab2b9`.
- Solution export: 61,570,595,788 bytes; previously recorded SHA-256
  `5ea74b912147c5c93cc2b6d70cc727cf908df2f62ac6a20480a3fa02f6be244e`.
  This update does not recompute the 61 GB export hash.

This Comparator invocation consumed existing exports. It is not a new source
build. The earlier rebuild and export remain separately documented evidence.
The original launch used `LEAN_NUM_THREADS=72`; observed checker stages used
approximately one CPU core. The timing wrapper reported user 5660.93 s,
system 83.51 s, CPU 1%, and maximum RSS 86,882,212 KiB. These wrapper counters
are not claimed to measure aggregate CPU time or whole-process-tree peak RAM.

## Separate tuned check and credit

The standalone paranoid check passed in **21:43:05**. Andrew Sutherland (MIT)
documented `MIMALLOC_GENERIC_COLLECT=1000000` in his
[verification record](https://math.mit.edu/~drew/grh/); Harry applied that setting
to the stock checker. The recorded original Comparator command did not set it.
The standalone run’s statement that it was not a completed Comparator verdict
remains correct for that run. The original Comparator now provides the verdict.

## Evidence preservation

The preparation is based on Harry’s supplied completed terminal transcript.
The update helper additionally requires the completed original server log,
validates its success markers and elapsed time, and copies both checker logs
byte-for-byte into a timestamped folder under
`verification-updates/20261128/server-log-snapshots/`. COLLECTION.json records
source paths, sizes and SHA-256. No raw log is fabricated from the transcript.
Earlier snapshots and reports are preserved, including their pending statuses.
Pre-update current documents and archive manifest are backed up under
`publication/history/pre-20261128-update/`.

## Scope at closure

Formal verification of the five configured endpoints has passed. The scoped
critics’ audit found no formal proof defect in the inspected routes. It did not
exhaustively resolve every intended interpretation of auxiliary constructions,
complete every census follow-up, or independently derive a new mathematical
proof. Closing local verification does not rewrite those historical boundaries.
This update does not claim a local verification of the later compact editions.
