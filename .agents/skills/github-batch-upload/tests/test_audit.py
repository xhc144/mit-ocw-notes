import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
"""Security/failure regressions. All remotes and payloads are temporary fixtures."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

import batch_upload as batch
import test_batch_upload as baseline


# Do not inherit TestCase: re-use fixture helpers without duplicating baseline tests.
class AuditIntegration(unittest.TestCase):
    setUp = baseline.BatchIntegration.setUp
    tearDown = baseline.BatchIntegration.tearDown
    git = baseline.BatchIntegration.git
    remote_head = baseline.BatchIntegration.remote_head
    make_manifest = baseline.BatchIntegration.make_manifest
    call = baseline.BatchIntegration.call
    advance_writer = baseline.BatchIntegration.advance_writer

    def config(self, values):
        env = {'GIT_CONFIG_COUNT': str(len(values))}
        for index, (key, value) in enumerate(values.items()):
            env['GIT_CONFIG_KEY_' + str(index)] = key
            env['GIT_CONFIG_VALUE_' + str(index)] = value
        return patch.dict(os.environ, env)

    def cli(self, *extra, env=None):
        active = os.environ.copy()
        if env:
            active.update(env)
        return subprocess.run([sys.executable, str(Path(batch.__file__)), str(self.manifest),
                               '--source-root', str(self.source), '--test-only-local-remote',
                               str(self.remote), *extra], env=active, capture_output=True, text=True)

    def stop_code(self, code, **kwargs):
        with self.assertRaises(batch.Stop) as caught:
            self.call(**kwargs)
        self.assertEqual(caught.exception.code, code)
        return caught.exception.details

    def seed_rules(self, rules):
        (self.seed / '.gitattributes').write_text(rules)
        self.git(self.seed, 'add', '--', '.gitattributes')
        self.git(self.seed, 'commit', '--quiet', '-m', 'existing fixture rules')
        self.git(self.seed, 'push', '--quiet', 'origin', 'HEAD:refs/heads/main')
        self.head = self.remote_head()

    def lfs_config(self, **additional):
        values = {'filter.lfs.clean': 'git-lfs clean -- %f',
                  'filter.lfs.smudge': 'git-lfs smudge -- %f',
                  'filter.lfs.process': 'git-lfs filter-process', 'filter.lfs.required': 'true'}
        values.update(additional)
        return self.config(values)

    def large_manifest(self, mebibytes, path):
        # Stream a reproducible payload without keeping the whole file in RAM.
        block = hashlib.shake_256(b'local audit fixture').digest(1024 * 1024)
        digest = hashlib.sha256()
        with (self.source / 'large').open('wb') as stream:
            for _ in range(mebibytes):
                stream.write(block)
                digest.update(block)
        data = {'version': 1, 'repo': 'fixture/authorized-private', 'branch': 'main',
                'expected_head': self.head,
                'files': [{'source': 'large', 'path': path, 'sha256': digest.hexdigest()}]}
        self.manifest.write_text(json.dumps(data))
        return data, mebibytes * 1024 * 1024

    def test_external_git_state_environment_rejected_before_commands(self):
        self.make_manifest()
        caller_index = self.base / 'caller-index'
        caller_index.write_bytes(b'caller bytes must survive')
        index_bytes = (self.seed / '.git' / 'index').read_bytes()
        for key in sorted(batch.UNSAFE_GIT_ENV):
            with self.subTest(key=key), patch.dict(os.environ, {key: str(caller_index)}):
                with patch.object(batch, 'git', side_effect=AssertionError('must not invoke Git')):
                    self.stop_code('UNSAFE_GIT_ENVIRONMENT', publish=True)
        self.assertEqual(caller_index.read_bytes(), b'caller bytes must survive')
        self.assertEqual((self.seed / '.git' / 'index').read_bytes(), index_bytes)
        self.assertEqual(self.remote_head(), self.head)

    def test_wrong_url_rewrite_and_pushurl_rejected_without_writes(self):
        wrong = self.base / 'wrong.git'
        self.git(None, 'clone', '--quiet', '--bare', str(self.remote), str(wrong))
        self.make_manifest()
        for values in ({'url.' + str(wrong) + '.insteadOf': str(self.remote)},
                       {'url.' + str(wrong) + '.pushInsteadOf': str(self.remote)},
                       {'remote.origin.pushurl': str(wrong)}):
            with self.subTest(keys=list(values)), self.config(values):
                details = self.stop_code('REMOTE_ROUTE_CHANGED', publish=True)
                self.assertFalse(details['remote_write_attempted'])
        self.assertEqual(self.remote_head(), self.head)
        self.assertEqual(self.git(wrong, 'rev-parse', 'main').decode().strip(), self.head)

    def test_local_worktree_redirect_rejected(self):
        self.make_manifest()
        before = self.git(self.seed, 'status', '--porcelain', '-z')
        original = batch.git
        def redirect(cwd, *args, **kwargs):
            output = original(cwd, *args, **kwargs)
            if args[0] == 'init':
                original(cwd, 'config', 'core.worktree', str(self.seed))
            return output
        with patch.object(batch, 'git', side_effect=redirect):
            self.stop_code('WORKSPACE_REDIRECTED', publish=True)
        self.assertEqual(self.git(self.seed, 'status', '--porcelain', '-z'), before)
        self.assertEqual(self.remote_head(), self.head)

    def test_unrelated_smudge_never_runs_in_dry_run(self):
        self.seed_rules('unrelated.txt filter=sideeffect\n')
        self.make_manifest()
        marker = self.base / 'smudge-executed'
        with self.config({'filter.sideeffect.smudge': 'touch ' + str(marker) + '; cat',
                          'filter.sideeffect.clean': 'cat'}):
            self.stop_code('UNSUPPORTED_CHECKOUT_FILTER')
        self.assertFalse(marker.exists())
        self.assertEqual(self.remote_head(), self.head)

    def test_custom_lfs_command_never_runs(self):
        self.seed_rules('*.bin filter=lfs -text\n')
        self.make_manifest({'document.bin': b'local bytes'})
        marker = self.base / 'lfs-command-executed'
        with self.lfs_config(**{'filter.lfs.process': 'touch ' + str(marker) + '; git-lfs filter-process'}):
            self.stop_code('UNSUPPORTED_LFS_FILTER_COMMAND')
        self.assertFalse(marker.exists())
        self.assertEqual(self.remote_head(), self.head)

    def test_lfs_external_storage_extensions_and_object_url_rewrite_rejected(self):
        self.seed_rules('*.bin filter=lfs -text\n')
        self.make_manifest({'document.bin': b'fixture bytes'})
        outside = self.base / 'outside-lfs'
        for values in ({'lfs.storage': str(outside)},
                       {'lfs.extension.audit.clean': 'touch ' + str(outside)},
                       {'url.' + str(outside) + '.insteadOf': 'https://payload.invalid/objects/'},
                       {'lfs.remote.searchall': 'true'}, {'lfs.remote.autodetect': 'true'},
                       {'remote.lfspushdefault': 'wrong'}):
            with self.subTest(keys=list(values)), self.lfs_config(**values):
                self.stop_code('CUSTOM_LFS_ROUTE_UNSUPPORTED')
        self.assertFalse(outside.exists())
        self.assertEqual(self.remote_head(), self.head)

    def test_dry_run_does_not_trigger_post_checkout_hook(self):
        self.make_manifest()
        hooks = self.base / 'client-hooks'; hooks.mkdir()
        marker = self.base / 'post-checkout-ran'
        hook = hooks / 'post-checkout'
        hook.write_text('#!/bin/sh\ntouch ' + str(marker) + '\n'); hook.chmod(0o755)
        with self.config({'core.hooksPath': str(hooks)}):
            self.assertEqual(self.call()['status'], 'DRY_RUN_VERIFIED')
        self.assertFalse(marker.exists())

    def test_commit_hook_changed_content_stops_before_push(self):
        self.make_manifest()
        hooks = self.base / 'client-hooks'; hooks.mkdir()
        hook = hooks / 'pre-commit'
        hook.write_text('#!/bin/sh\nprintf "hook mutation\\n" > unrelated.txt\ngit add -- unrelated.txt\n')
        hook.chmod(0o755)
        with self.config({'core.hooksPath': str(hooks)}):
            details = self.stop_code('COMMIT_OR_HOOK_CHANGED_REVIEWED_CONTENT', publish=True)
        self.assertFalse(details['remote_write_attempted'])
        self.assertEqual(self.remote_head(), self.head)
        self.assertEqual(self.git(self.remote, 'show', 'main:unrelated.txt'), b'keep this content\n')

    def test_client_pre_push_hook_rejection_is_preserved(self):
        self.make_manifest()
        hooks = self.base / 'client-hooks'; hooks.mkdir()
        hook = hooks / 'pre-push'
        hook.write_text('#!/bin/sh\nexit 1\n'); hook.chmod(0o755)
        with self.config({'core.hooksPath': str(hooks)}):
            self.stop_code('COMMAND_FAILED', publish=True)
        self.assertEqual(self.remote_head(), self.head)

    def test_lfs_config_symlink_rejected_before_reading_it(self):
        (self.seed / '.lfsconfig').symlink_to(self.source / 'private-file')
        self.git(self.seed, 'add', '--', '.lfsconfig')
        self.git(self.seed, 'commit', '--quiet', '-m', 'fixture config symlink')
        self.git(self.seed, 'push', '--quiet', 'origin', 'HEAD:refs/heads/main')
        self.head = self.remote_head(); self.make_manifest()
        self.stop_code('NONREGULAR_LFS_CONFIG', publish=True)
        self.assertEqual(self.remote_head(), self.head)

    def test_source_parent_symlink_swap_cannot_escape(self):
        data = self.make_manifest()
        nested = self.source / 'nested'
        nested.mkdir()
        (self.source / 'input-0').rename(nested / 'payload')
        data['files'][0]['source'] = 'nested/payload'
        self.manifest.write_text(json.dumps(data))
        outside = self.base / 'outside'; outside.mkdir()
        (outside / 'payload').write_bytes((nested / 'payload').read_bytes())
        original = batch.non_symlink_path
        def swap(root, relative):
            result = original(root, relative)
            if root == self.source and relative == 'nested/payload':
                nested.rename(self.source / 'old-nested')
                nested.symlink_to(outside, target_is_directory=True)
            return result
        with patch.object(batch, 'non_symlink_path', side_effect=swap):
            self.stop_code('SOURCE_UNAVAILABLE', publish=True)
        self.assertEqual(self.remote_head(), self.head)

    def test_symlink_parent_directory_and_nonregular_target_preserved(self):
        (self.seed / 'linked-parent').symlink_to(self.source, target_is_directory=True)
        (self.seed / 'directory').mkdir()
        (self.seed / 'directory' / 'keep').write_bytes(b'existing child')
        self.git(self.seed, 'add', '--', 'linked-parent', 'directory')
        self.git(self.seed, 'commit', '--quiet', '-m', 'fixture targets')
        self.git(self.seed, 'push', '--quiet', 'origin', 'HEAD:refs/heads/main')
        self.head = self.remote_head()
        for target, code in (('linked-parent/escaped', 'SYMLINK_PATH'), ('directory', 'NONREGULAR_TARGET')):
            self.make_manifest({target: b'must not overwrite'})
            self.stop_code(code, publish=True)
        self.assertFalse((self.source / 'escaped').exists())
        self.assertEqual(self.git(self.remote, 'show', 'main:directory/keep'), b'existing child')
        self.assertEqual(self.remote_head(), self.head)

    def test_source_fifo_is_rejected_without_blocking(self):
        self.make_manifest()
        src = self.source / 'input-0'; src.unlink(); os.mkfifo(src)
        self.stop_code('NONREGULAR_SOURCE', publish=True)
        self.assertEqual(self.remote_head(), self.head)

    def test_manifest_duplicates_prefixes_and_protected_nested_rules(self):
        original = self.make_manifest()
        for mutation, code in ((lambda d: d['files'].append(dict(d['files'][0])), 'DUPLICATE_TARGET'),
                               (lambda d: d['files'][1].update(path='notes'), 'TARGET_PREFIX_CONFLICT'),
                               (lambda d: d['files'][0].update(path='notes/.gitmodules'), 'PROTECTED_RULE_FILE')):
            data = json.loads(json.dumps(original)); mutation(data)
            self.manifest.write_text(json.dumps(data))
            self.stop_code(code, publish=True)
        self.manifest.write_text('{"version":1,"version":1}')
        self.stop_code('DUPLICATE_JSON_KEY')
        self.assertEqual(self.remote_head(), self.head)

    def test_branch_exactness_and_invalid_ref_stops_before_write(self):
        for branch in ('../main', 'main:other', '-main', 'main\nother', 'main..x', 'main@{1}'):
            data = self.make_manifest(); data['branch'] = branch
            self.manifest.write_text(json.dumps(data))
            with self.subTest(branch=branch), self.assertRaises(batch.Stop):
                self.call(publish=True)
        self.git(self.remote, 'update-ref', 'refs/heads/feature/a', self.head)
        data = self.make_manifest(); data['branch'] = 'feature/a'
        self.manifest.write_text(json.dumps(data))
        result = self.call(publish=True)
        self.assertEqual(result['status'], 'PUBLISHED_VERIFIED')
        self.assertEqual(self.remote_head(), self.head)
        self.assertEqual(self.git(self.remote, 'rev-parse', 'refs/heads/feature/a').decode().strip(), result['verified_head'])

    def test_missing_branch_and_nonbare_test_remote_rejected(self):
        data = self.make_manifest(); data['branch'] = 'missing'
        self.manifest.write_text(json.dumps(data))
        self.stop_code('COMMAND_FAILED', publish=True)
        with self.assertRaises(batch.Stop) as caught:
            batch.execute(self.manifest, self.source, test_remote=self.seed, publish=True)
        self.assertEqual(caught.exception.code, 'TEST_REMOTE_NOT_BARE')
        self.assertEqual(self.remote_head(), self.head)

    def test_private_permission_gate_and_malformed_metadata(self):
        data = self.make_manifest()
        for value in (None, [], {}, {'full_name': 123}):
            with self.subTest(value=value), patch.object(batch, 'run', return_value=json.dumps(value).encode()):
                with self.assertRaises(batch.Stop) as caught:
                    batch.check_private(data, publish=True)
                self.assertEqual(caught.exception.code, 'METADATA_INVALID')
        for permissions in (None, [], {}, {'push': False}, {'push': 1}):
            metadata = {'full_name': data['repo'], 'private': True, 'visibility': 'private',
                        'archived': False, 'permissions': permissions}
            with self.subTest(permissions=permissions), patch.object(batch, 'run', return_value=json.dumps(metadata).encode()):
                with self.assertRaises(batch.Stop) as caught:
                    batch.check_private(data, publish=True)
                self.assertEqual(caught.exception.code, 'PUSH_PERMISSION_UNCONFIRMED')

    def test_hook_secret_output_never_reaches_cli_receipt(self):
        self.make_manifest()
        secret = 'AUDIT_SYNTHETIC_SECRET_do_not_print'
        hook = self.remote / 'hooks' / 'pre-receive'
        hook.write_text('#!/bin/sh\nprintf "' + secret + '\\n" >&2\nexit 1\n'); hook.chmod(0o755)
        process = self.cli('--publish')
        self.assertEqual(process.returncode, 2)
        self.assertNotIn(secret, process.stdout + process.stderr)
        self.assertEqual(json.loads(process.stdout)['code'], 'COMMAND_FAILED')
        self.assertEqual(self.remote_head(), self.head)

    def test_timeout_kills_command_descendants(self):
        marker = self.base / 'child-survived'
        script = self.base / 'spawn.py'
        script.write_text('import subprocess, sys, time\n'
                          'subprocess.Popen([sys.executable, "-c", '
                          '"import time; from pathlib import Path; time.sleep(0.6); Path(' + repr(str(marker)) + ').touch()"] )\n'
                          'time.sleep(5)\n')
        started = time.monotonic()
        with self.assertRaises(batch.Stop) as caught:
            batch.run([sys.executable, str(script)], timeout=0.1)
        self.assertEqual(caught.exception.code, 'COMMAND_TIMEOUT')
        time.sleep(0.7)
        self.assertFalse(marker.exists())
        self.assertLess(time.monotonic() - started, 3)

    def test_blob_stream_timeout_returns_structured_stop(self):
        self.make_manifest({'same.txt': b'already there\n'})
        bindir = self.base / 'bin'; bindir.mkdir()
        real_git = subprocess.run(['which', 'git'], capture_output=True, text=True, check=True).stdout.strip()
        wrapper = bindir / 'git'
        wrapper.write_text('#!/bin/sh\nif [ "$1" = "cat-file" ] && [ "$2" = "--batch" ]; then sleep 5; exit 0; fi\nexec ' + real_git + ' "$@"\n')
        wrapper.chmod(0o755)
        with patch.dict(os.environ, {'PATH': str(bindir) + os.pathsep + os.environ['PATH']}):
            details = self.stop_code('COMMAND_TIMEOUT', command_timeout=0.2)
        self.assertFalse(details['remote_write_attempted'])
        self.assertEqual(self.remote_head(), self.head)

    def test_lfs_config_timeout_returns_structured_stop(self):
        self.seed_rules('*.bin filter=lfs -text\n'); self.make_manifest({'file.bin': b'bytes'})
        original = batch.run
        def timeout(args, **kwargs):
            if args[:3] == ['git', 'config', '--get']:
                raise batch.Stop('COMMAND_TIMEOUT', program='git')
            return original(args, **kwargs)
        with patch.object(batch, 'run', side_effect=timeout):
            details = self.stop_code('COMMAND_TIMEOUT', publish=True)
        self.assertFalse(details['remote_write_attempted'])

    def test_push_accepted_then_connection_timeout_recovers_read_only(self):
        self.make_manifest()
        original = batch.git
        push_calls = []
        def disconnect(cwd, *args, **kwargs):
            output = original(cwd, *args, **kwargs)
            if args[0] == 'push':
                push_calls.append(args)
                raise batch.Stop('COMMAND_TIMEOUT', program='git')
            return output
        with patch.object(batch, 'git', side_effect=disconnect):
            details = self.stop_code('COMMAND_TIMEOUT', publish=True)
        self.assertEqual(len(push_calls), 1)
        self.assertTrue(details['publication_may_have_occurred'])
        self.assertFalse(details['automatic_write_retry'])
        self.assertEqual(self.remote_head(), details['candidate_commit'])
        again = self.call()
        self.assertEqual(again['status'], 'NOOP_VERIFIED')
        self.assertFalse(again['remote_write_attempted'])

    def test_push_timeout_before_acceptance_has_no_partial_branch_and_can_rerun(self):
        self.make_manifest()
        hook = self.remote / 'hooks' / 'pre-receive'
        hook.write_text('#!/bin/sh\nsleep 5\nexit 0\n'); hook.chmod(0o755)
        details = self.stop_code('COMMAND_TIMEOUT', publish=True, command_timeout=0.3)
        self.assertTrue(details['publication_may_have_occurred'])
        self.assertFalse(details['automatic_write_retry'])
        self.assertEqual(self.remote_head(), self.head)
        hook.unlink()
        self.assertEqual(self.call()['status'], 'DRY_RUN_VERIFIED')
        self.assertEqual(self.call(publish=True)['status'], 'PUBLISHED_VERIFIED')

    def test_fetch_head_race_preserves_other_writer(self):
        self.make_manifest()
        original = batch.checkout
        advanced = []
        def change(directory, remote, branch, observed):
            advanced.append(self.advance_writer())
            return original(directory, remote, branch, observed)
        with patch.object(batch, 'checkout', side_effect=change):
            self.stop_code('HEAD_CHANGED_DURING_FETCH', publish=True)
        self.assertEqual(self.remote_head(), advanced[0])

    def test_noop_head_race_is_not_reported_verified(self):
        self.make_manifest({'same.txt': b'already there\n'})
        original = batch.verify
        advanced = []
        def change(*args, **kwargs):
            result = original(*args, **kwargs)
            advanced.append(self.advance_writer())
            return result
        with patch.object(batch, 'verify', side_effect=change):
            self.stop_code('HEAD_CHANGED_DURING_VERIFICATION')
        self.assertEqual(self.remote_head(), advanced[0])

    def test_backward_or_deleted_ref_race_stops_with_default_shallow_checkout(self):
        ancestor = self.head
        self.head = self.advance_writer()
        expected = self.head
        for deletion in (False, True):
            self.git(self.remote, 'update-ref', 'refs/heads/main', expected)
            self.make_manifest({'race.txt': b'candidate after expected head'})
            def move_back(candidate):
                if deletion:
                    self.git(self.remote, 'update-ref', '-d', 'refs/heads/main')
                else:
                    self.git(self.remote, 'update-ref', 'refs/heads/main', ancestor)
            with self.subTest(deletion=deletion):
                self.stop_code('COMMAND_FAILED', publish=True, after_head_check=move_back)

    def test_existing_hook_fetch_history_demonstrates_non_cas_limit(self):
        # Hooks are supported and preserved. A hook may fetch more history.
        # With history present, ordinary push may accept rollback/deletion races.
        ancestor = self.head
        self.head = self.advance_writer()
        expected = self.head
        hooks = self.base / 'client-hooks'; hooks.mkdir()
        hook = hooks / 'pre-commit'
        hook.write_text('#!/bin/sh\ngit fetch --quiet --unshallow origin\n'); hook.chmod(0o755)
        for deletion in (False, True):
            self.git(self.remote, 'update-ref', 'refs/heads/main', expected)
            self.make_manifest({'race.txt': b'candidate after expected head'})
            def move_back(candidate):
                if deletion:
                    self.git(self.remote, 'update-ref', '-d', 'refs/heads/main')
                else:
                    self.git(self.remote, 'update-ref', 'refs/heads/main', ancestor)
            with self.subTest(deletion=deletion), self.config({'core.hooksPath': str(hooks)}):
                result = self.call(publish=True, after_head_check=move_back)
                self.assertEqual(result['status'], 'PUBLISHED_VERIFIED')
            self.assertEqual(self.git(self.remote, 'rev-parse', 'main^').decode().strip(), expected)

    def test_lfs_upload_head_race_preserves_other_writer(self):
        with self.lfs_config():
            self.seed_rules('*.bin filter=lfs -text\n')
            self.make_manifest({'file.bin': b'local LFS bytes'})
            original = batch.git
            advanced = []
            def race(cwd, *args, **kwargs):
                result = original(cwd, *args, **kwargs)
                if args[:2] == ('lfs', 'push'):
                    advanced.append(self.advance_writer())
                return result
            with patch.object(batch, 'git', side_effect=race):
                details = self.stop_code('HEAD_CONFLICT_AFTER_LFS_UPLOAD', publish=True)
            self.assertTrue(details['remote_write_attempted'])
            self.assertEqual(self.remote_head(), advanced[0])

    def test_keyboard_interrupt_stops_with_recovery_receipt(self):
        self.make_manifest()
        original = batch.git
        def interrupted(cwd, *args, **kwargs):
            if args[0] == 'push':
                raise KeyboardInterrupt
            return original(cwd, *args, **kwargs)
        with patch.object(batch, 'git', side_effect=interrupted):
            details = self.stop_code('INTERRUPTED', publish=True)
        self.assertTrue(details['publication_may_have_occurred'])
        self.assertFalse(details['automatic_write_retry'])
        self.assertEqual(self.remote_head(), self.head)

    def test_plain_16_mib_real_bytes_and_idempotence(self):
        data, size = self.large_manifest(16, 'payload.dat')
        report = self.call(publish=True)
        self.assertEqual(report['changed_source_bytes'], size)
        payload = self.git(self.remote, 'show', 'main:payload.dat')
        self.assertEqual(len(payload), size)
        self.assertEqual(hashlib.sha256(payload).hexdigest(), data['files'][0]['sha256'])
        self.assertEqual(self.call()['status'], 'NOOP_VERIFIED')

    def test_plain_101_mib_rejected_before_push(self):
        self.large_manifest(101, 'oversize.dat')
        details = self.stop_code('NEEDS_EXPLICIT_LFS_RULE', publish=True)
        self.assertFalse(details['remote_write_attempted'])
        self.assertEqual(self.remote_head(), self.head)

    def test_lfs_101_mib_real_bytes_missing_object_and_recovery(self):
        with self.lfs_config():
            self.seed_rules('*.bin filter=lfs diff=lfs merge=lfs -text\n')
            data, size = self.large_manifest(101, 'large.bin')
            digest = data['files'][0]['sha256']
            result = self.call(publish=True)
            self.assertTrue(result['lfs_payload_verified'])
            obj = self.remote / 'lfs' / 'objects' / digest[:2] / digest[2:4] / digest
            self.assertTrue(obj.exists())
            self.assertEqual(obj.stat().st_size, size)
            with obj.open('rb') as stream:
                self.assertEqual(hashlib.file_digest(stream, 'sha256').hexdigest(), digest)
            obj.rename(obj.with_suffix('.saved'))
            with self.assertRaises(batch.Stop):
                self.call()  # A pointer alone never qualifies as NOOP_VERIFIED.
            self.assertEqual(self.remote_head(), result['verified_head'])
            obj.with_suffix('.saved').rename(obj)
            self.assertEqual(self.call()['status'], 'NOOP_VERIFIED')

    def test_partial_lfs_object_upload_rejected_branch_recovers(self):
        with self.lfs_config():
            self.seed_rules('*.bin filter=lfs -text\n')
            data = self.make_manifest({'document.bin': b'checkpoint payload\0' * 8192})
            oid = data['files'][0]['sha256']
            hook = self.remote / 'hooks' / 'pre-receive'
            hook.write_text('#!/bin/sh\nexit 1\n'); hook.chmod(0o755)
            details = self.stop_code('COMMAND_FAILED', publish=True)
            self.assertTrue(details['remote_write_attempted'])
            self.assertEqual(self.remote_head(), self.head)
            obj = self.remote / 'lfs' / 'objects' / oid[:2] / oid[2:4] / oid
            self.assertTrue(obj.exists())  # Objects remain after ref update rejection.
            self.assertEqual(self.call()['status'], 'DRY_RUN_VERIFIED')
            hook.unlink()
            result = self.call(publish=True)
            self.assertTrue(result['lfs_payload_verified'])
            self.assertEqual(self.call()['status'], 'NOOP_VERIFIED')

    def test_invalid_timeout_never_invokes_git(self):
        self.make_manifest()
        for timeout in (0, -1, float('nan'), float('inf'), 1e300, True, '1'):
            with self.subTest(timeout=timeout), patch.object(batch, 'git', side_effect=AssertionError('must not run')):
                self.stop_code('INVALID_COMMAND_TIMEOUT', command_timeout=timeout)
        process = self.cli('--publish', '--command-timeout', 'nan')
        self.assertEqual(process.returncode, 2)
        self.assertEqual(json.loads(process.stdout)['code'], 'INVALID_COMMAND_TIMEOUT')
        self.assertEqual(self.remote_head(), self.head)


if __name__ == '__main__':
    unittest.main(verbosity=2)
