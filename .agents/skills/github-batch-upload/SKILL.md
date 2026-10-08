---
name: github-batch-upload
description: "Upload an explicitly selected batch of authorized files to an existing private GitHub repository with a frozen manifest, native Git packing, content deduplication, checkpoints and remote integrity verification. Use for 批量Git上传、批量GitHub上传、上传恢复 or installing this portable uploader. Reuse the bundled audited tool; do not rebuild an uploader or generate credentials."
---

# GitHub batch upload

1. Read the current repo's AGENTS.md, check status and remote HEAD, and establish exact authorized repo, branch and paths. Preserve unrelated changes and existing skills. Task authorization persists; do not ask again for authorized writes. Respect explicit authentication, service or policy denials.
2. Read [workflow](references/workflow.md). Reuse `scripts/batch_upload.py`, derived from `xhc144/lecture-notes/tools/github-batch-upload` at `a170d65a5646eafb0798f12c741f1cc9b7efbbba`. Use native Git first. Never replace it with per-file Contents API calls.
3. Freeze an explicit version-1 manifest with source paths, target paths, SHA256 and expected HEAD. No globbing, reselecting or dropping files during transfer. Store one private checkpoint outside the selected tree. Inspect sources for credentials; automatic blocking covers only known names and obvious signatures.
4. Run dry-run, then publish within the authorized scope, using the same manifest and checkpoint:

   ```bash
   python3 <skill>/scripts/batch_upload.py manifest.json --source-root /authorized/input --checkpoint /private/batch-state --dry-run
   python3 <skill>/scripts/batch_upload.py manifest.json --source-root /authorized/input --checkpoint /private/batch-state --publish
   ```

5. Coordinate one writer across environments for each repository, including different branches. The script locks local processes; it cannot lock another machine. Source snapshot workers are bounded (default 2, maximum 4). Git commands and ref updates are serial. Never force-push, rewrite history, bypass hooks or change security/network settings.
6. On timeout, 429 or 5xx, inspect the actual remote ref before a bounded retry. Authentication/hook/permission failures stop. Resume the same checkpoint: completed frozen files survive source deletion; a pending candidate commit is reused. Do not clear a denied checkpoint to bypass a refusal.
7. Treat only `PUBLISHED_VERIFIED` or `NOOP_VERIFIED` with matching remote ref and complete manifest hashes as success. Dry-run, staged blobs or an unverified commit are preparation. Recovery reuses files/Git objects; no HTTP Range/tus byte continuation is promised.
8. Large files or any LFS route are detection-only in the CLI. Explain the finding and use a separately authorized workflow; never buy storage, enable billing, generate tokens or upload credentials.

If native Git cannot execute in the environment (not because of a denial), use the already connected GitHub app and [connector fallback](references/connector-fallback.md). Do not request/create a token or change endpoints to overcome an explicit refusal.

For installation, read [installation](references/installation.md) and run `python3 <skill>/scripts/install.py --repo <repo-root>`. It copies only this package to `.agents/skills/github-batch-upload`, preserves other skills/AGENTS, and reports conflicts with local edits. This is repo installation, not personal-skills initialization. Report which environment was actually tested; committing a folder does not prove another saved environment loaded it.
