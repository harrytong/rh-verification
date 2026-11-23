# Stage 4 v0.7: follow the observed proof helpers

Prepared 2026-11-23 after inspecting v0.6 evidence and before the new project run.
This is a targeted correction, not a blind or preregistered sample.

Evidence archive SHA-256:
`7730ef46b1439a1a4cb8e95be4f8cfa7cf847901c135558529fa6c39ecc81a98`.

The v0.6 constructor arguments identify the following exact names under
`Formalism.L2.DIV.DivisionPackageFace.ofOpen`:

| Field | Observed helper | Next call to inspect |
| --- | --- | --- |
| hTie | _proof_7 | Formalism.L2.DIV.hTie_of |
| rhs | _proof_10 | Formalism.L2.DIV.rhs_le_record |

Retain the constructor scan. Move the two direct call scans to these helper
bodies and dump both helper declarations. The requested collection is therefore
14 arguments, nine comparisons and 13 declaration records. These are coverage
targets, not predicted mathematical outcomes. Existing source/artifact pins,
fixtures and resource limits apply. Missing helpers or calls remain incomplete
coverage; do not guess a replacement name or interpret them as missing proofs.

No unbounded transitive unfolding is introduced. The collection still examines
a parameterized package builder, not a fully specialized headline theorem.
The earlier SUPPLIER_PROTOCOL.md records the original v0.6 design; this document
supersedes its two helper owner choices and declaration count for v0.7.

Separately report records containing the visible `⋯` pretty-printer elision
marker. Character truncation and pretty-printing elision are different. Absence
of that marker does not certify complete printing. Comparisons use stored
expressions, not rendered text. No result here alone establishes semantic
equivalence to the protected challenge, necessity, or an RH/GRH verdict.
