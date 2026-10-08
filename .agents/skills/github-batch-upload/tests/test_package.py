"""Portable install and no-network connector planning checks."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import base64
import hashlib
import json
import tempfile
import unittest
from unittest.mock import patch
import install
import connector_manifest as connector
import batch_upload as batch


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.repo = self.base / 'repo'; self.repo.mkdir()
        (self.repo / '.git').mkdir()
        (self.repo / 'AGENTS.md').write_text('preserve instructions')
        other = self.repo / '.agents' / 'skills' / 'existing'; other.mkdir(parents=True)
        (other / 'SKILL.md').write_text('preserve other skill')
        self.source = self.base / 'skill'; self.source.mkdir()
        (self.source / 'SKILL.md').write_text('skill source v1')
        self.make_index()

    def tearDown(self):
        self.temp.cleanup()

    def make_index(self):
        data = {'name': 'github-batch-upload', 'version': 1, 'release': '2.0.0', 'files': {'SKILL.md': hashlib.sha256((self.source / 'SKILL.md').read_bytes()).hexdigest()}}
        (self.source / 'install-manifest.json').write_text(json.dumps(data))

    def test_install_idempotent_preserves_other_skills_and_agents(self):
        self.assertEqual(install.install(self.repo, self.source)['status'], 'INSTALLED')
        self.assertEqual(install.install(self.repo, self.source)['status'], 'ALREADY_INSTALLED')
        self.assertEqual((self.repo / 'AGENTS.md').read_text(), 'preserve instructions')
        self.assertEqual((self.repo / '.agents/skills/existing/SKILL.md').read_text(), 'preserve other skill')

    def test_installer_rejects_local_edits_and_unknown_files(self):
        result = install.install(self.repo, self.source)
        target = Path(result['path'])
        (target / 'SKILL.md').write_text('local edit')
        with self.assertRaises(install.InstallError):
            install.install(self.repo, self.source)
        (target / 'SKILL.md').write_text('skill source v1')
        (target / 'custom.txt').write_text('user bytes')
        with self.assertRaises(install.InstallError):
            install.install(self.repo, self.source)

    def test_clean_indexed_upgrade(self):
        install.install(self.repo, self.source)
        (self.source / 'SKILL.md').write_text('skill source v2')
        self.make_index()
        self.assertEqual(install.install(self.repo, self.source)['status'], 'INSTALLED')
        self.assertEqual((self.repo / '.agents/skills/github-batch-upload/SKILL.md').read_text(), 'skill source v2')

    def test_installer_rejects_corruption_traversal_and_symlink(self):
        (self.source / 'SKILL.md').write_text('corrupted')
        with self.assertRaises(install.InstallError):
            install.install(self.repo, self.source)
        for path in ('../escape', 'a//b', 'C:/escape'):
            (self.source / 'install-manifest.json').write_text(json.dumps({'name': 'github-batch-upload', 'version': 1, 'files': {path: '0' * 64}}))
            with self.assertRaises(install.InstallError):
                install.install(self.repo, self.source)
        self.make_index()
        target = self.repo / '.agents/skills/github-batch-upload'
        target.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(install.InstallError):
            install.install(self.repo, self.source)

    def manifest(self, content=b'fixture', path='notes/example.txt'):
        root = self.base / 'input'; root.mkdir(exist_ok=True)
        (root / 'selected').write_bytes(content)
        m = {'version': 1, 'repo': 'fixture/private', 'branch': 'main', 'expected_head': 'a' * 40,
             'files': [{'source': 'selected', 'path': path, 'sha256': hashlib.sha256(content).hexdigest()}]}
        manifest = self.base / 'manifest.json'; manifest.write_text(json.dumps(m))
        return manifest, root, self.base / 'checkpoint'

    def test_connector_plan_without_git_is_preparation_only_and_hashes_real_blob(self):
        args = self.manifest()
        with patch.object(batch, 'git', side_effect=AssertionError('must not invoke Git')):
            plan = connector.prepare(*args, emit_blob=0)
        self.assertEqual(plan['status'], 'FROZEN_PLAN_ONLY')
        self.assertEqual(plan['verified_files'], 0)
        self.assertFalse(plan['remote_write_attempted'])
        self.assertEqual(plan['entries'][0]['expected_blob_sha'], hashlib.sha1(b'blob 7\0fixture').hexdigest())
        self.assertEqual(base64.b64decode(plan['blob_input']['content']), b'fixture')
        (args[1] / 'selected').unlink()
        self.assertEqual(connector.prepare(*args)['reused_snapshots'], 1)

    def test_connector_blocks_secret_content_and_lfs_pointer(self):
        args = self.manifest(b'-----BEGIN ' + b'PRIVATE KEY-----')
        with self.assertRaises(batch.Stop) as caught:
            connector.prepare(*args)
        self.assertEqual(caught.exception.code, 'SECRET_CONTENT_REJECTED')
        import shutil
        shutil.rmtree(args[2])
        args = self.manifest(b'version https://git-lfs.github.com/spec/v1\noid sha256:' + b'a' * 64 + b'\nsize 9\n')
        with self.assertRaises(batch.Stop) as caught:
            connector.prepare(*args)
        self.assertEqual(caught.exception.code, 'LFS_POINTER_INPUT_REQUIRES_SEPARATE_WORKFLOW')

    def test_connector_branch_validation_without_git(self):
        manifest, root, cp = self.manifest()
        data = json.loads(manifest.read_text())
        for branch in ('a..b', '../escape', 'main:other', 'a//b', 'a@{1}', 'a.lock', 'a b'):
            data['branch'] = branch; manifest.write_text(json.dumps(data))
            with patch.object(batch, 'git', side_effect=AssertionError('no Git')), self.assertRaises(batch.Stop):
                batch.load_manifest(manifest, validate_branch_git=False)


if __name__ == '__main__':
    unittest.main()
