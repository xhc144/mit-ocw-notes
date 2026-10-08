import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
"""Upgrade regressions against isolated synthetic bare Git remotes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
import batch_upload as batch
import test_batch_upload as baseline


class UpgradeIntegration(unittest.TestCase):
    setUp = baseline.BatchIntegration.setUp
    tearDown = baseline.BatchIntegration.tearDown
    git = baseline.BatchIntegration.git
    remote_head = baseline.BatchIntegration.remote_head
    make_manifest = baseline.BatchIntegration.make_manifest
    advance_writer = baseline.BatchIntegration.advance_writer

    def call(self, **kwargs):
        return batch.execute(self.manifest, self.source, test_remote=self.remote,
                             checkpoint=self.base / 'checkpoint', retry_delay=0,
                             lfs_detect_only=True, **kwargs)

    def stop(self, code, **kwargs):
        with self.assertRaises(batch.Stop) as caught:
            self.call(**kwargs)
        self.assertEqual(caught.exception.code, code)
        return caught.exception.details

    def test_frozen_snapshots_survive_source_mutation_and_deletion(self):
        self.make_manifest()
        dry = self.call()
        (self.source / 'input-0').write_bytes(b'changed later')
        (self.source / 'input-1').unlink()
        report = self.call(publish=True)
        self.assertEqual(report['status'], 'PUBLISHED_VERIFIED')
        self.assertEqual(report['reused_snapshots'], 2)
        self.assertTrue(report['reused_work'])
        self.assertEqual(self.git(self.remote, 'show', 'main:notes/数学 1.txt'), b'new maths\n')
        self.assertEqual(set(dry['timings_seconds']), {'freeze', 'preflight', 'checkout', 'compare', 'stage', 'total'})
        for remaining in self.source.iterdir():
            remaining.unlink()
        self.source.rmdir()
        self.assertEqual(self.call(verify_only=True)['status'], 'NOOP_VERIFIED')

    def test_lost_push_receipt_recovers_without_sources_or_second_push(self):
        self.make_manifest()
        real = batch.git
        pushes = []
        def lost(cwd, *args, **kw):
            result = real(cwd, *args, **kw)
            if args[0] == 'push':
                pushes.append(args)
                raise batch.Stop('COMMAND_TIMEOUT', program='git')
            return result
        with patch.object(batch, 'git', side_effect=lost):
            receipt = self.stop('COMMAND_TIMEOUT', publish=True)
        for f in self.source.iterdir():
            f.unlink()
        def no_push(cwd, *args, **kw):
            self.assertNotEqual(args[0], 'push')
            return real(cwd, *args, **kw)
        with patch.object(batch, 'git', side_effect=no_push):
            report = self.call(publish=True)
        self.assertEqual(report['status'], 'NOOP_VERIFIED')
        self.assertEqual(report['verified_head'], receipt['candidate_commit'])
        self.assertEqual(len(pushes), 1)

    def test_retry_after_accepted_timeout_reads_ref_and_never_pushes_twice(self):
        self.make_manifest()
        real = batch.git
        pushes = []
        def lost(cwd, *args, **kw):
            result = real(cwd, *args, **kw)
            if args[0] == 'push':
                pushes.append(args)
                raise batch.Stop('COMMAND_TIMEOUT', program='git')
            return result
        with patch.object(batch, 'git', side_effect=lost):
            report = self.call(publish=True, retries=2)
        self.assertEqual(report['status'], 'PUBLISHED_VERIFIED')
        self.assertTrue(report['remote_confirmed_after_transient'])
        self.assertFalse(report['automatic_write_retry'])
        self.assertEqual(len(pushes), 1)

    def test_pending_candidate_is_reused_after_timeout_and_source_removal(self):
        self.make_manifest()
        real = batch.git
        def timeout(cwd, *args, **kw):
            if args[0] == 'push':
                raise batch.Stop('COMMAND_TIMEOUT', program='git')
            return real(cwd, *args, **kw)
        with patch.object(batch, 'git', side_effect=timeout):
            receipt = self.stop('COMMAND_TIMEOUT', publish=True)
        for f in self.source.iterdir():
            f.unlink()
        report = self.call(publish=True)
        self.assertTrue(report['reused_candidate'])
        self.assertEqual(report['verified_head'], receipt['candidate_commit'])
        self.assertEqual(self.git(self.remote, 'rev-list', '--count', 'main').strip(), b'2')

    def test_rate_limit_5xx_timeout_retry_with_remote_inspection(self):
        for code in ('REMOTE_RATE_LIMITED', 'REMOTE_TRANSIENT_ERROR', 'COMMAND_TIMEOUT'):
            with self.subTest(code=code):
                self.make_manifest({f'{code}.txt': b'new fixture'})
                cp = self.base / 'checkpoint'
                if cp.exists():
                    import shutil
                    shutil.rmtree(cp)
                real = batch.git
                attempts, trace = [], []
                def flaky(cwd, *args, **kw):
                    trace.append(args[0])
                    if args[0] == 'push':
                        attempts.append(args)
                        if len(attempts) == 1:
                            raise batch.Stop(code, retry_after=0)
                    return real(cwd, *args, **kw)
                with patch.object(batch, 'git', side_effect=flaky):
                    report = self.call(publish=True, retries=2)
                self.assertTrue(report['automatic_write_retry'])
                self.assertEqual(len(attempts), 2)
                i, j = [k for k, x in enumerate(trace) if x == 'push']
                self.assertIn('ls-remote', trace[i + 1:j])
                self.assertEqual(attempts[0], attempts[1])
                self.head = self.remote_head()

    def test_retry_conflict_preserves_other_writer(self):
        self.make_manifest()
        real = batch.git
        def conflict(cwd, *args, **kw):
            if args[0] == 'push':
                self.advance_writer()
                raise batch.Stop('REMOTE_TRANSIENT_ERROR')
            return real(cwd, *args, **kw)
        with patch.object(batch, 'git', side_effect=conflict):
            self.stop('HEAD_CONFLICT_DURING_RETRY', publish=True, retries=2)
        self.assertEqual(self.git(self.remote, 'show', 'main:worker.txt'), b'other worker advanced branch\n')

    def test_auth_and_hook_denial_are_not_retried_or_resumed(self):
        for code in ('AUTH_DENIED', 'COMMAND_FAILED'):
            with self.subTest(code=code):
                self.make_manifest()
                cp = self.base / 'checkpoint'
                if cp.exists():
                    import shutil
                    shutil.rmtree(cp)
                real = batch.git
                attempts = []
                def denied(cwd, *args, **kw):
                    if args[0] == 'push':
                        attempts.append(1)
                        raise batch.Stop(code)
                    return real(cwd, *args, **kw)
                with patch.object(batch, 'git', side_effect=denied):
                    self.stop(code, publish=True, retries=3)
                self.assertEqual(len(attempts), 1)
                self.stop('CHECKPOINT_DENIAL_REQUIRES_REVIEW', publish=True)
        self.assertEqual(self.remote_head(), self.head)

    def test_retry_exhaustion_and_retry_after_deferred(self):
        self.make_manifest()
        with patch.object(batch, 'remote_read', wraps=batch.remote_read), patch.object(batch, 'backoff', wraps=batch.backoff):
            real = batch.git
            pushes = []
            def unavailable(cwd, *args, **kw):
                if args[0] == 'push':
                    pushes.append(1)
                    raise batch.Stop('REMOTE_TRANSIENT_ERROR')
                return real(cwd, *args, **kw)
            with patch.object(batch, 'git', side_effect=unavailable):
                self.stop('REMOTE_TRANSIENT_ERROR', publish=True, retries=2)
            self.assertEqual(len(pushes), 3)
        with self.assertRaises(batch.Stop) as caught:
            batch.backoff(batch.Stop('REMOTE_RATE_LIMITED', retry_after=120), 0, 'test')
        self.assertEqual(caught.exception.code, 'RETRY_DEFERRED')

    def test_remote_read_retries_transients_but_not_auth(self):
        token = batch.RETRY.set((2, 0))
        try:
            calls = []
            def read():
                calls.append(1)
                if len(calls) < 3:
                    raise batch.Stop('REMOTE_TRANSIENT_ERROR')
                return 'ok'
            self.assertEqual(batch.remote_read(read, 'test'), 'ok')
            self.assertEqual(len(calls), 3)
            with self.assertRaises(batch.Stop):
                batch.remote_read(lambda: (_ for _ in ()).throw(batch.Stop('AUTH_DENIED')), 'test')
        finally:
            batch.RETRY.reset(token)

    def test_checkpoint_wrong_repo_branch_manifest_and_fixture_rejected(self):
        data = self.make_manifest()
        self.call()
        for field, value in (('repo', 'wrong/private'), ('branch', 'feature'), ('expected_head', 'a' * 40)):
            changed = {**data, field: value}
            self.manifest.write_text(json.dumps(changed))
            self.stop('CHECKPOINT_TARGET_OR_MANIFEST_MISMATCH', publish=True)
        self.manifest.write_text(json.dumps(data))
        wrong = self.base / 'wrong.git'
        self.git(None, 'clone', '--bare', '--quiet', str(self.remote), str(wrong))
        with self.assertRaises(batch.Stop) as caught:
            batch.execute(self.manifest, self.source, test_remote=wrong, checkpoint=self.base / 'checkpoint')
        self.assertEqual(caught.exception.code, 'CHECKPOINT_TARGET_OR_MANIFEST_MISMATCH')

    def test_checkpoint_corrupt_snapshot_and_symlink_rejected(self):
        self.make_manifest()
        self.call()
        saved = self.base / 'checkpoint' / 'snapshots' / '0'
        original = saved.read_bytes()
        saved.write_bytes(b'tampered')
        self.stop('CHECKPOINT_HASH_MISMATCH', publish=True)
        saved.unlink(); saved.symlink_to(self.source / 'input-0')
        self.stop('CHECKPOINT_SYMLINK', publish=True)
        saved.unlink(); saved.write_bytes(original)
        workgit = self.base / 'checkpoint' / 'work' / '.git'
        workgit.rename(workgit.with_name('hidden-git'))
        workgit.symlink_to(workgit.with_name('hidden-git'), target_is_directory=True)
        self.stop('CHECKPOINT_SYMLINK', publish=True)

    def test_missing_branch_lock_and_cross_branch_lock(self):
        self.make_manifest()
        key = hashlib.sha256(('fixture/authorized-private|' + str(self.remote)).encode()).hexdigest()
        directory = Path(__import__('tempfile').gettempdir()) / ('github-batch-upload-locks-' + str(os.getuid()))
        with batch.process_lock(directory, key):
            self.stop('WRITER_LOCKED', publish=True)
            data = json.loads(self.manifest.read_text()); data['branch'] = 'another'
            self.manifest.write_text(json.dumps(data))
            self.stop('WRITER_LOCKED', publish=True)
        self.assertEqual(self.remote_head(), self.head)

    def test_sensitive_paths_and_content_rejected_before_remote(self):
        for path in ('.env', '.ssh/id_rsa', 'a/.aws/credentials', 'private.pem', '.env.production', 'a/.git/config', '../escape', 'a\\escape'):
            self.make_manifest({path: b'fake fixture text'})
            with patch.object(batch, 'check_private', side_effect=AssertionError('no remote')):
                with self.assertRaises(batch.Stop):
                    self.call(publish=True)
        for content in (b'-----BEGIN ' + b'PRIVATE KEY-----\nfake\n', b'ghp_' + b'x' * 36, b'AKIA' + b'A' * 16, b'password="' + b'x' * 20 + b'"'):
            import shutil
            shutil.rmtree(self.base / 'checkpoint', ignore_errors=True)
            self.make_manifest({'ordinary.txt': content})
            with patch.object(batch, 'check_private', side_effect=AssertionError('no remote')):
                self.stop('SECRET_CONTENT_REJECTED', publish=True)
        self.assertEqual(self.remote_head(), self.head)

    def test_secret_across_chunk_boundary_and_safe_example(self):
        self.make_manifest({'notes.txt': b'a' * (1024 * 1024 - 2) + b'ghp_' + b'x' * 36})
        self.stop('SECRET_CONTENT_REJECTED')
        import shutil
        shutil.rmtree(self.base / 'checkpoint')
        self.make_manifest({'config.example.json': b'{"password":"YOUR_PASSWORD","api_key":"example"}'})
        self.assertEqual(self.call()['status'], 'DRY_RUN_VERIFIED')

    def test_partial_freeze_recovers_completed_files(self):
        self.make_manifest()
        (self.source / 'input-1').unlink()
        self.stop('SOURCE_UNAVAILABLE')
        saved = self.base / 'checkpoint' / 'snapshots' / '0'
        self.assertTrue(saved.is_file())
        (self.source / 'input-0').unlink()
        (self.source / 'input-1').write_bytes(b'already there\n')
        self.assertEqual(self.call(publish=True, workers=1)['status'], 'PUBLISHED_VERIFIED')

    def test_selected_checkout_preserves_unrelated_content_without_materializing(self):
        self.make_manifest()
        report = self.call()
        work = self.base / 'checkpoint' / 'work'
        self.assertFalse((work / 'unrelated.txt').exists())
        self.assertEqual(self.git(work, 'show', 'HEAD:unrelated.txt'), b'keep this content\n')
        self.assertEqual(report['status'], 'DRY_RUN_VERIFIED')
        self.assertEqual(self.call(publish=True)['status'], 'PUBLISHED_VERIFIED')
        self.assertEqual(self.git(self.remote, 'show', 'main:unrelated.txt'), b'keep this content\n')

    def test_filtered_fetch_omits_unrelated_blob_when_remote_supports_filter(self):
        self.git(self.remote, 'config', 'uploadpack.allowFilter', 'true')
        self.git(self.remote, 'config', 'uploadpack.allowAnySHA1InWant', 'true')
        self.make_manifest()
        self.call()
        work = self.base / 'checkpoint' / 'work'
        oid = self.git(self.remote, 'rev-parse', 'main:unrelated.txt').decode().strip()
        env = os.environ.copy(); env['GIT_NO_LAZY_FETCH'] = '1'
        result = subprocess.run(['git', 'cat-file', '-e', oid], cwd=work, env=env, capture_output=True)
        self.assertNotEqual(result.returncode, 0)

    def test_duplicate_manifest_and_conflicting_remote_preserve_history(self):
        data = self.make_manifest()
        data['files'].append(data['files'][0])
        self.manifest.write_text(json.dumps(data))
        self.stop('DUPLICATE_TARGET')
        self.make_manifest(); self.call()
        newhead = self.advance_writer()
        self.stop('HEAD_CONFLICT', publish=True)
        self.assertEqual(self.remote_head(), newhead)

    def test_lfs_detection_does_not_initialize_or_transfer(self):
        (self.seed / '.gitattributes').write_text('*.bin filter=lfs\n')
        self.git(self.seed, 'add', '--', '.gitattributes')
        self.git(self.seed, 'commit', '--quiet', '-m', 'LFS detection fixture')
        self.git(self.seed, 'push', '--quiet', 'origin', 'HEAD:refs/heads/main')
        self.head = self.remote_head()
        self.make_manifest({'note.bin': b'fixture'})
        self.stop('LFS_DETECTED_REQUIRES_SEPARATE_WORKFLOW', publish=True)
        self.assertFalse((self.remote / 'lfs').exists())

    def test_cli_secret_receipt_never_includes_payload(self):
        secret = 'ghp_' + 'x' * 36
        self.make_manifest({'ordinary.txt': secret.encode()})
        result = subprocess.run([sys.executable, str(Path(batch.__file__)), str(self.manifest), '--source-root', str(self.source), '--publish', '--test-only-local-remote', str(self.remote)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(secret, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['code'], 'SECRET_CONTENT_REJECTED')

    def test_checkpoint_fifo_refused_without_blocking(self):
        self.make_manifest(); self.call()
        saved = self.base / 'checkpoint' / 'snapshots' / '0'
        saved.unlink(); os.mkfifo(saved)
        result = subprocess.run([sys.executable, str(Path(batch.__file__)), str(self.manifest), '--source-root', str(self.source), '--checkpoint', str(self.base / 'checkpoint'), '--verify-only', '--test-only-local-remote', str(self.remote)], capture_output=True, text=True, timeout=2)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)['code'], 'CHECKPOINT_NONREGULAR')
        self.assertEqual(self.remote_head(), self.head)

    def test_restored_snapshot_obvious_secret_is_blocked_even_with_matching_hash(self):
        value = b'ghp_' + b'x' * 36
        saved = self.base / 'restored-cache'; saved.write_bytes(value)
        f = {'path': 'notes.txt', 'sha256': hashlib.sha256(value).hexdigest()}
        with self.assertRaises(batch.Stop) as caught:
            batch.validate_snapshot(saved, f)
        self.assertEqual(caught.exception.code, 'SECRET_CONTENT_REJECTED')

    def test_verify_only_never_pushes_and_requires_remote_content(self):
        self.make_manifest()
        self.stop('REMOTE_CONTENT_NOT_COMPLETE', verify_only=True)
        self.assertEqual(self.remote_head(), self.head)
        self.assertEqual(self.call(publish=True)['status'], 'PUBLISHED_VERIFIED')
        self.assertEqual(self.call(verify_only=True)['status'], 'NOOP_VERIFIED')
        self.stop('VERIFY_ONLY_CANNOT_PUBLISH', verify_only=True, publish=True)

    def test_failure_classification_and_invalid_policy(self):
        for msg, code in ((b'HTTP 429 retry-after: 12', 'REMOTE_RATE_LIMITED'), (b'HTTP 503', 'REMOTE_TRANSIENT_ERROR'), (b'HTTP 403', 'AUTH_DENIED'), (b'hook declined HTTP 503', 'COMMAND_FAILED')):
            self.assertEqual(batch.classify_failure(msg), code)
        self.assertEqual(batch.classify_failure(b'failed ref abcdef401dead 403abcd'), 'COMMAND_FAILED')
        self.make_manifest()
        for kwargs in ({'retries': 6}, {'workers': 0}, {'retries': True}):
            self.stop('INVALID_RETRY_OR_WORKER_POLICY', **kwargs)


if __name__ == '__main__':
    unittest.main()
