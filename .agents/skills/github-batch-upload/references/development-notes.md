# Development checks and limits

Initial upgrade test runs caught an accidental helper recursion, test-hook callback signature compatibility, LFS detection ordering, and authentication classification treating digits inside commit SHAs as HTTP status codes. These were corrected before any production write. A later failing source-deletion test tried to remove a nonempty fixture directory; the fixture was corrected and the final run includes deletion of the entire original source directory.

A final synthetic counterexample found that replacing a checkpoint snapshot with a FIFO could block reads. Nonblocking/no-follow cache opens and restored-content secret checks now reject it; two regressions were added.

Final authoritative results are `validation.json` (84 package tests) and `core-validation.json` (77 core tests including 53 unchanged originals). Earlier intermediate failures are not counted as passing evidence. All inputs/remotes are synthetic/local. The original historical audit/test evidence in lecture-notes remains unchanged.

The local comparison in `benchmark.json` is one run per mode. It shows a cold-start cost from scanning/checkpoint persistence and reuse of 60 snapshots/staged files on the warm pass. It does not establish real GitHub throughput or a GB transfer estimate.

Remaining limits: native POSIX only; Windows install/runtime not exercised; local lock does not coordinate machines; ordinary push retains the inherited non-CAS race boundary; obvious-secret rules are incomplete; final verification still reads every selected blob; no byte-range continuation; connected-app fallback is an agent workflow with local plan tests, not a tested automatic online uploader. The legacy Python LFS API remains for unchanged baseline regression coverage; CLI/skill are detection-only.
