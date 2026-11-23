# Stage 4 v0.3 result: slope application still unresolved

Evidence SHA-256:
`237f0e325bb09eef1c37b5fd0a8800836b61791e3e92e90e804fdecbfcdd29a4`.
The uploaded archive and its evidence-manifest entries were checked. Recorded
input hashes before/after match. This is review of Harry's run, not independent
reexecution.

The invalid example was rejected as expected. All seven comparison controls
passed, including the two-call fixture that checks first-match traversal order.
The project process exited successfully, but `collection_complete` is false.

| Target | Result |
| --- | --- |
| `slope_le_height`, generic conclusion | Sides not definitionally identical |
| `height_add_log_nonneg`, generic conclusion | Sides not definitionally identical |
| `FrameCmp.val_le`, generic conclusion | Sides not definitionally identical |
| `FrameCmp.htCmp → FrameCmp.val_le`, first observed application | Sides not definitionally identical; reached after 21,703 walker visits |
| `heightAt_eq_of_cover → slope_le_height` | Zero matches before the 250,000-node cap; unresolved |

The new traversal order reduced visits to the known valuation application but
did not reach the slope application. It supplied no new conclusion about that
missing comparison. A successful collector exit is not complete coverage.

The assigned-height reflexivity control and the example of type
`RiemannHypothesis` still compiled. These facts and the four nonidentical-side
results neither establish the critics' overall invalidity claim nor refute all
their arguments. Further upstream specialization and the identification of the
paper's precise inequality remain outside the inspected scope.

The v0.4 change filters branches by their stored constant references and reports
those references explicitly. It does not change the equality test or increase
the resource caps. Comparator remains untouched.
