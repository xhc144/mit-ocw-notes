# Native workflow and recovery

The original uploader already provided snapshot SHA256 checks, incremental byte comparison, one Git add/commit/push, protected paths, private-repository validation, hook preservation, and fresh-fetch verification. These are retained features, not claimed as new. The upgrade adds persistent frozen snapshots/workspace/candidate, local repo-wide process locks, bounded transient retries, source concurrency, phase timing, obvious credential blocking, and a portable repo installer.

## Explicit manifest

```json
{"version":1,"repo":"owner/private-repo","branch":"main","expected_head":"40 hex commit SHA","files":[{"source":"output/example.txt","path":"notes/example.txt","sha256":"64 hex SHA256"}]}
```

Read exact repo metadata and branch HEAD before selecting the batch. Compute hashes of the actual selected bytes. The source root and target repo are separate concepts. Do not scan broad account/home directories. The manifest supports existing branches and normal regular files; it rejects duplicate keys/targets, parent/child conflicts, `.git`, traversal, symlinks, and protected `.gitattributes`, `.lfsconfig`, `.gitmodules` writes. Credentials such as `.env`, `.ssh/id_rsa`, `.aws/credentials`, private-key files, obvious tokens/private-key headers are blocked before remote access. Safe examples can use names such as `config.example.json` and explicit placeholder values. There is no arbitrary secret-scan override. Encoded, compressed or unusual secrets may evade signatures; inspect selected bytes yourself.

## Persistent state

Use a dedicated checkpoint directory owned by the current user with mode 0700. Keep it outside selected upload paths and Git commits. It stores the exact manifest identity, source-root/target binding, individually frozen snapshots, Git workspace, pending commit and receipts. Once frozen, files are not reread from mutable source during transfer/resume. Each resumed snapshot is rehashed to detect corruption; the scanner runs when initially freezing bytes. An incomplete source snapshot is restarted at file granularity. Completed snapshots and the pending Git candidate survive interruption and source deletion.

Use exactly the same manifest/checkpoint to resume. Add `--verify-only` for read-only recovery: matching remote content returns `NOOP_VERIFIED`; incomplete content stops without staging/publishing. The source directory may be absent if all files were frozen. A changed repo, branch, expected HEAD, source root, target mapping or hash stops with `CHECKPOINT_TARGET_OR_MANIFEST_MISMATCH`. The checkpoint is private working state, not a distributable credential container or a Git artifact. Keep it until remote verification succeeds and cleanup is authorized. A denial recorded in the checkpoint stops later automated writes; review/resolve the original refusal through the normal provider process before making any separately authorized new attempt.

With a checkpoint, checkout materializes selected existing paths and rule files only. It preserves the full index/tree and marks omitted paths skip-worktree. Fetch requests `blob:none`; an unsupported server may still transfer the full tree. Existing objects and staged content can be reused for the warm attempt. Final verification uses a fresh isolated repository and hashes every selected raw blob, preserving the remote commit/ref checks. No throughput multiple, GB migration duration or byte-range continuation is guaranteed.

## Retry policy

CLI default: two additional transient attempts, exponential delay/jitter (base 1 second), at most four source workers. Git operations and commit/ref writes are serial. Before retrying a push, inspect the remote head: a matching candidate continues to full verification without another push; an unchanged expected head may retry the same candidate; any other head stops. Recheck private target, routes and ref before the retry. Preserve authentication/signing/hooks and ordinary fast-forward rules. Never force or auto-merge/rebase.

429 honors explicit Retry-After. Missing Retry-After defaults to at least 60 seconds; long waits are returned as `RETRY_DEFERRED` for later resumption. A 401/403, hook rejection, non-fast-forward or explicit denial is not transient. Read-only metadata/HEAD/fetch may retry known timeout/429/5xx errors. Generic command failures stop. A process lock serializes all local branches of one repo. It is not a distributed lock or a strict expected-SHA CAS; coordinate a single writer across environments. The inherited normal-push race limitation remains documented in the original tool README/tests.

Receipts include freeze/preflight/checkout/compare/stage/commit/push/verify/total timing for phases actually executed, reused snapshots/work/candidate, changed/skipped paths, retry events and verified head/files. `DRY_RUN_VERIFIED` does not publish. `PUBLISHED_VERIFIED` means the actual remote candidate was fetched and all manifest bytes verified. `NOOP_VERIFIED` means current remote content already matches. A stopped receipt can report that publication may have occurred; recover by reading the actual branch first, never by blindly repeating a write.

## LFS and capability boundaries

The skill's CLI stops on LFS and normal files above 100 MiB; it does not initialize LFS, alter tracking rules, transmit LFS objects, buy quota or enable billing. The legacy Python `execute` API keeps its preexisting LFS code path only so the original 53 regression tests remain unchanged; this skill and all CLI invocations use detection-only mode. Invoke the CLI or explicitly set `lfs_detect_only=True` if integrating the Python function.

Native dependencies: Python 3.11+, POSIX, Git, gh and existing authorized identity/access. The program reads selected input files, invokes existing trusted Git/credential helpers/hooks, and is not their sandbox. Command timeout covers external process groups/blob streams, not the whole batch or source hashing. No credentials are read from files, printed or generated by the uploader.
