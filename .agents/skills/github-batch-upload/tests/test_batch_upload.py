import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
"""Integration checks against throwaway local bare repos; no network or real data."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import batch_upload as batch


class BatchIntegration(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="batch-upload-tests-")
        self.base = Path(self.temp.name)
        self.remote = self.base / "fixture.git"
        self.seed = self.base / "writer"
        self.source = self.base / "input"; self.source.mkdir()
        self.manifest = self.base / "manifest.json"
        self.environment = patch.dict(os.environ, {
            "GIT_AUTHOR_NAME": "Local Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
            "GIT_COMMITTER_NAME": "Local Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
        })
        self.environment.start()
        self.git(None, "init", "--bare", "--quiet", "--initial-branch=main", str(self.remote))
        self.git(None, "init", "--quiet", "--initial-branch=main", str(self.seed))
        self.git(self.seed, "remote", "add", "origin", str(self.remote))
        (self.seed / "unrelated.txt").write_bytes(b"keep this content\n")
        (self.seed / "same.txt").write_bytes(b"already there\n")
        (self.seed / "executable.sh").write_bytes(b"old script\n")
        os.chmod(self.seed / "executable.sh", 0o755)
        self.git(self.seed, "add", "--", "unrelated.txt", "same.txt", "executable.sh")
        self.git(self.seed, "commit", "--quiet", "-m", "fixture baseline")
        self.git(self.seed, "push", "--quiet", "origin", "HEAD:refs/heads/main")
        self.head = self.remote_head()

    def tearDown(self):
        self.environment.stop()
        self.temp.cleanup()

    def git(self, cwd, *args):
        p = subprocess.run(["git", *args], cwd=cwd, capture_output=True)
        self.assertEqual(p.returncode, 0, "local fixture Git command failed")
        return p.stdout

    def remote_head(self):
        return self.git(self.remote, "rev-parse", "refs/heads/main").decode().strip()

    def make_manifest(self, contents=None):
        contents = contents or {"notes/数学 1.txt": b"new maths\n", "same.txt": b"already there\n"}
        files = []
        for i, (path, value) in enumerate(contents.items()):
            src = "input-" + str(i)
            (self.source / src).write_bytes(value)
            files.append({"source": src, "path": path, "sha256": hashlib.sha256(value).hexdigest()})
        data = {"version": 1, "repo": "fixture/authorized-private", "branch": "main",
                "expected_head": self.head, "files": files}
        self.manifest.write_text(json.dumps(data, ensure_ascii=False))
        return data

    def call(self, **kwargs):
        return batch.execute(self.manifest, self.source, test_remote=self.remote, **kwargs)

    def advance_writer(self):
        (self.seed / "worker.txt").write_bytes(b"other worker advanced branch\n")
        self.git(self.seed, "add", "--", "worker.txt")
        self.git(self.seed, "commit", "--quiet", "-m", "other worker")
        self.git(self.seed, "push", "--quiet", "origin", "HEAD:refs/heads/main")
        return self.remote_head()

    def test_default_dry_run_preserves_branch_and_dirty_writer(self):
        self.make_manifest()
        (self.seed / "unrelated.txt").write_bytes(b"user uncommitted edit\n")
        (self.seed / "untracked.txt").write_bytes(b"user untracked bytes\n")
        before = self.git(self.seed, "status", "--porcelain", "-z")
        report = self.call()
        self.assertEqual(report["status"], "DRY_RUN_VERIFIED")
        self.assertFalse(report["remote_write_attempted"])
        self.assertEqual(report["skipped"], ["same.txt"])
        self.assertEqual(self.remote_head(), self.head)
        self.assertEqual(self.git(self.seed, "status", "--porcelain", "-z"), before)
        self.assertEqual((self.seed / "unrelated.txt").read_bytes(), b"user uncommitted edit\n")

    def test_many_files_one_commit_and_idempotent_rerun(self):
        payload = {f"notes/file-{i:03}.txt": f"content {i}\n".encode() for i in range(48)}
        payload.update({"notes/中文 空格.txt": b"utf8 filename\n", "glob[1]$().txt": b"literal filename\n",
                        "executable.sh": b"new script\n", "same.txt": b"already there\n"})
        data = self.make_manifest(payload)
        report = self.call(publish=True)
        self.assertEqual(report["status"], "PUBLISHED_VERIFIED")
        self.assertEqual(report["verified_files"], 52)
        published = self.remote_head()
        self.assertNotEqual(published, self.head)
        self.assertEqual(self.git(self.remote, "rev-parse", "main^").decode().strip(), self.head)
        changed = set(self.git(self.remote, "diff", "--name-only", "-z", self.head, published).decode().split("\0")[:-1])
        self.assertEqual(changed, set(payload) - {"same.txt"})
        self.assertEqual(self.git(self.remote, "show", "main:unrelated.txt"), b"keep this content\n")
        self.assertTrue(self.git(self.remote, "ls-tree", "main", "executable.sh").startswith(b"100755"))
        again = self.call(publish=True)  # Same old expected_head, all bytes already present.
        self.assertEqual(again["status"], "NOOP_VERIFIED")
        self.assertFalse(again["remote_write_attempted"])
        self.assertEqual(len(again["skipped"]), len(data["files"]))
        self.assertEqual(self.remote_head(), published)

    def test_wrong_sha256_stops_before_remote_read(self):
        data = self.make_manifest()
        data["files"][0]["sha256"] = "0" * 64
        self.manifest.write_text(json.dumps(data))
        with patch.object(batch, "check_private", side_effect=AssertionError("must not access remote")):
            with self.assertRaises(batch.Stop) as caught:
                self.call(publish=True)
        self.assertEqual(caught.exception.code, "SOURCE_HASH_MISMATCH")
        self.assertEqual(self.remote_head(), self.head)

    def test_stale_head_with_pending_changes_stops(self):
        self.make_manifest()
        advanced = self.advance_writer()
        with self.assertRaises(batch.Stop) as caught:
            self.call(publish=True)
        self.assertEqual(caught.exception.code, "HEAD_CONFLICT")
        self.assertFalse(caught.exception.details["remote_write_attempted"])
        self.assertEqual(self.remote_head(), advanced)

    def test_concurrent_head_change_before_push_stops(self):
        self.make_manifest()
        seen = []
        def other_writer(candidate):
            seen.append(self.advance_writer())
        with self.assertRaises(batch.Stop) as caught:
            self.call(publish=True, before_publish=other_writer)
        self.assertEqual(caught.exception.code, "HEAD_CONFLICT_BEFORE_PUSH")
        self.assertFalse(caught.exception.details["remote_write_attempted"])
        self.assertEqual(self.remote_head(), seen[0])

    def test_race_after_last_check_rejected_by_normal_git_push(self):
        self.make_manifest()
        seen = []
        with self.assertRaises(batch.Stop) as caught:
            self.call(publish=True, after_head_check=lambda candidate: seen.append(self.advance_writer()))
        self.assertEqual(caught.exception.code, "COMMAND_FAILED")
        self.assertTrue(caught.exception.details["remote_write_attempted"])
        self.assertFalse(caught.exception.details["automatic_write_retry"])
        self.assertEqual(self.remote_head(), seen[0])
        self.assertEqual(self.git(self.remote, "show", "main:worker.txt"), b"other worker advanced branch\n")

    def test_manifest_path_rejections(self):
        for value in ("../escape", "/absolute", ".git/config", "x/.git/objects", "a//b", "a/./b", "a\nb", "x\\b"):
            with self.subTest(value=value):
                data = self.make_manifest()
                data["files"][0]["path"] = value
                self.manifest.write_text(json.dumps(data))
                with self.assertRaises(batch.Stop) as caught:
                    self.call(publish=True)
                self.assertEqual(caught.exception.code, "INVALID_PATH")
        self.assertEqual(self.remote_head(), self.head)

    def test_source_symlink_rejected(self):
        self.make_manifest()
        src = self.source / "input-0"
        src.unlink(); src.symlink_to(self.seed / "unrelated.txt")
        with self.assertRaises(batch.Stop) as caught:
            self.call(publish=True)
        self.assertEqual(caught.exception.code, "SYMLINK_PATH")
        self.assertEqual(self.remote_head(), self.head)

    def test_target_symlink_rejected(self):
        (self.seed / "linked").symlink_to("unrelated.txt")
        self.git(self.seed, "add", "--", "linked")
        self.git(self.seed, "commit", "--quiet", "-m", "fixture symlink")
        self.git(self.seed, "push", "--quiet", "origin", "HEAD:refs/heads/main")
        self.head = self.remote_head()
        self.make_manifest({"linked": b"forbidden overwrite\n"})
        with self.assertRaises(batch.Stop) as caught:
            self.call(publish=True)
        self.assertEqual(caught.exception.code, "NONREGULAR_TARGET")
        self.assertEqual(self.remote_head(), self.head)

    def test_private_metadata_gate_and_denial(self):
        data = self.make_manifest()
        for metadata in ({"full_name": data["repo"], "private": False, "visibility": "public", "archived": False},
                         {"full_name": "wrong/repository", "private": True, "visibility": "private", "archived": False},
                         {"full_name": data["repo"], "private": True, "visibility": "private", "archived": True}):
            with patch.object(batch, "run", return_value=json.dumps(metadata).encode()):
                with self.assertRaises(batch.Stop) as caught:
                    batch.check_private(data)
                self.assertEqual(caught.exception.code, "REPOSITORY_NOT_ACTIVE_PRIVATE")
        with patch.object(batch, "run", side_effect=batch.Stop("AUTH_DENIED")):
            with self.assertRaises(batch.Stop) as caught:
                batch.check_private(data)
            self.assertEqual(caught.exception.code, "AUTH_DENIED")

    def test_protected_attributes_not_changed(self):
        self.make_manifest({".gitattributes": b"*.pdf filter=lfs\n"})
        with self.assertRaises(batch.Stop) as caught:
            self.call(publish=True)
        self.assertEqual(caught.exception.code, "PROTECTED_RULE_FILE")

    def test_git_normalization_hash_mismatch_stops(self):
        (self.seed / ".gitattributes").write_text("*.txt text eol=lf\n")
        self.git(self.seed, "add", "--", ".gitattributes")
        self.git(self.seed, "commit", "--quiet", "-m", "fixture text normalization")
        self.git(self.seed, "push", "--quiet", "origin", "HEAD:refs/heads/main")
        self.head = self.remote_head()
        self.make_manifest({"windows.txt": b"raw CRLF\r\n"})
        with self.assertRaises(batch.Stop) as caught:
            self.call(publish=True)
        self.assertEqual(caught.exception.code, "PUBLISHED_HASH_MISMATCH")
        self.assertEqual(self.remote_head(), self.head)

    def test_cli_dry_run_default(self):
        self.make_manifest()
        p = subprocess.run(["python3", str(Path(batch.__file__)), str(self.manifest), "--source-root", str(self.source),
                            "--test-only-local-remote", str(self.remote)], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        report = json.loads(p.stdout)
        self.assertEqual(report["mode"], "dry-run")
        self.assertEqual(report["status"], "DRY_RUN_VERIFIED")
        self.assertEqual(self.remote_head(), self.head)

    def test_lfs_bytes_uploaded_and_freshly_verified(self):
        # Official Git LFS defaults only, injected for this fixture; no global config edits.
        lfs_config = {
            "GIT_CONFIG_COUNT": "4",
            "GIT_CONFIG_KEY_0": "filter.lfs.clean", "GIT_CONFIG_VALUE_0": "git-lfs clean -- %f",
            "GIT_CONFIG_KEY_1": "filter.lfs.smudge", "GIT_CONFIG_VALUE_1": "git-lfs smudge -- %f",
            "GIT_CONFIG_KEY_2": "filter.lfs.process", "GIT_CONFIG_VALUE_2": "git-lfs filter-process",
            "GIT_CONFIG_KEY_3": "filter.lfs.required", "GIT_CONFIG_VALUE_3": "true",
        }
        with patch.dict(os.environ, lfs_config):
            (self.seed / ".gitattributes").write_text("*.bin filter=lfs diff=lfs merge=lfs -text\n")
            self.git(self.seed, "add", "--", ".gitattributes")
            self.git(self.seed, "commit", "--quiet", "-m", "fixture existing LFS rule")
            self.git(self.seed, "push", "--quiet", "origin", "HEAD:refs/heads/main")
            self.head = self.remote_head()
            payload = b"fixture binary payload\0" * 8000
            self.make_manifest({"document.bin": payload})
            dry = self.call()
            self.assertEqual(dry["lfs_files"], ["document.bin"])
            self.assertFalse(dry["remote_write_attempted"])
            self.assertFalse(dry["lfs_payload_verified"])
            self.assertEqual(self.remote_head(), self.head)
            report = self.call(publish=True)
            self.assertEqual(report["status"], "PUBLISHED_VERIFIED")
            self.assertTrue(report["lfs_payload_verified"])
            oid = hashlib.sha256(payload).hexdigest()
            pointer = self.git(self.remote, "show", "main:document.bin")
            self.assertIn(("oid sha256:" + oid).encode(), pointer)
            self.assertEqual(self.call(publish=True)["status"], "NOOP_VERIFIED")
            self.assertEqual(self.git(self.remote, "show", "main:.gitattributes"), b"*.bin filter=lfs diff=lfs merge=lfs -text\n")

    def test_custom_lfs_endpoint_stops(self):
        (self.seed / ".gitattributes").write_text("*.bin filter=lfs -text\n")
        (self.seed / ".lfsconfig").write_text("[lfs]\n\turl = https://example.invalid/custom-lfs\n")
        self.git(self.seed, "add", "--", ".gitattributes", ".lfsconfig")
        self.git(self.seed, "commit", "--quiet", "-m", "fixture custom LFS route")
        self.git(self.seed, "push", "--quiet", "origin", "HEAD:refs/heads/main")
        self.head = self.remote_head()
        self.make_manifest({"document.bin": b"fixture bytes"})
        with self.assertRaises(batch.Stop) as caught:
            self.call(publish=True)
        self.assertEqual(caught.exception.code, "CUSTOM_LFS_ROUTE_UNSUPPORTED")
        self.assertEqual(self.remote_head(), self.head)

    def test_uninitialized_lfs_filter_stops(self):
        (self.seed / ".gitattributes").write_text("*.bin filter=lfs -text\n")
        self.git(self.seed, "add", "--", ".gitattributes")
        self.git(self.seed, "commit", "--quiet", "-m", "fixture LFS rule without client configuration")
        self.git(self.seed, "push", "--quiet", "origin", "HEAD:refs/heads/main")
        self.head = self.remote_head()
        self.make_manifest({"document.bin": b"fixture bytes"})
        with patch.dict(os.environ, {
                "GIT_CONFIG_COUNT": "2", "GIT_CONFIG_KEY_0": "filter.lfs.clean", "GIT_CONFIG_VALUE_0": "",
                "GIT_CONFIG_KEY_1": "filter.lfs.process", "GIT_CONFIG_VALUE_1": ""}):
            with self.assertRaises(batch.Stop) as caught:
                self.call(publish=True)
        self.assertEqual(caught.exception.code, "LFS_FILTER_NOT_CONFIGURED")
        self.assertFalse(caught.exception.details["remote_write_attempted"])
        self.assertEqual(self.remote_head(), self.head)

    def test_server_hook_rejection_is_preserved(self):
        self.make_manifest()
        hook = self.remote / "hooks" / "pre-receive"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
        with patch.object(batch, "git", wraps=batch.git) as calls:
            with self.assertRaises(batch.Stop) as caught:
                self.call(publish=True)
        self.assertEqual(caught.exception.code, "COMMAND_FAILED")
        self.assertFalse(caught.exception.details["automatic_write_retry"])
        pushes = [c for c in calls.call_args_list if len(c.args) > 1 and c.args[1] == "push"]
        self.assertEqual(len(pushes), 1)
        self.assertEqual(self.remote_head(), self.head)
        self.assertTrue(hook.exists())

    def test_verification_failure_reports_already_published_commit(self):
        self.make_manifest()
        original_verify = batch.verify
        def fail_after_push(cwd, *args, **kwargs):
            if cwd.name == "verification":
                raise batch.Stop("SIMULATED_VERIFICATION_FAILURE")
            return original_verify(cwd, *args, **kwargs)
        with patch.object(batch, "verify", side_effect=fail_after_push):
            with self.assertRaises(batch.Stop) as caught:
                self.call(publish=True)
        details = caught.exception.details
        self.assertEqual(caught.exception.code, "SIMULATED_VERIFICATION_FAILURE")
        self.assertTrue(details["git_push_returned_success"])
        self.assertTrue(details["publication_may_have_occurred"])
        self.assertFalse(details["automatic_write_retry"])
        self.assertEqual(self.remote_head(), details["candidate_commit"])
        self.assertEqual(self.call()["status"], "NOOP_VERIFIED")

    def test_missing_cross_environment_source_stops(self):
        self.make_manifest()
        (self.source / "input-0").unlink()
        with patch.object(batch, "check_private", side_effect=AssertionError("must not read remote")):
            with self.assertRaises(batch.Stop) as caught:
                self.call(publish=True)
        self.assertEqual(caught.exception.code, "SOURCE_UNAVAILABLE")
        self.assertEqual(self.remote_head(), self.head)


if __name__ == "__main__":
    unittest.main(verbosity=2)
