# Publication validation — 23 November 2026

This validates packaging and upload preparation, not Lean or RH.

- Seven publication-helper tests passed: preservation/backups, symlink rejection,
  scoped collection/deduplication/compression, bounded log copies, collection
  byte-limit failure recording, checksum corruption and path traversal detection.
- Shell syntax check passed for publish.sh.
- All 5,978 copied inventory records matched their stored size and SHA-256.
- All 3,828 entries in available EVIDENCE_SHA256SUMS files matched their files.
- Relative links in the new README, index, closing assessment, verification
  history and scope documents resolve in the prepared payload.
- High-confidence private-key and GitHub-token pattern scan found no matches
  in the prepared non-ZIP payload.
- The root-level upload script passed end-to-end tests against two local bare
  repositories: one with no commits and one with an empty tree and retained
  history. Both produced the intended root folders with no audit/ wrapper.
- No Lean rerun, user-server access or actual GitHub commit/push was performed here.
- Additional server snapshots are collected later and have their own index;
  they are outside the prepared archive manifest and this validation.

The bundle includes helper test source. Original audit TEST_RESULTS files are
historical evidence; this publication validation does not substitute for them.
