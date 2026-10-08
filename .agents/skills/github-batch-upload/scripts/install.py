#!/usr/bin/env python3
"""Copy this complete skill into one repo .agents/skills. No account/config changes."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import uuid

NAME = 'github-batch-upload'


class InstallError(Exception):
    pass


def no_symlinks(path):
    for part in (path, *path.parents):
        if part.is_symlink():
            raise InstallError('SYMLINK_PATH')


def inventory(root):
    result = {}
    for path in root.rglob('*'):
        if path.is_symlink():
            raise InstallError('SYMLINK_PACKAGE_ENTRY')
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def verify(root):
    manifest = root / 'install-manifest.json'
    no_symlinks(manifest)
    data = json.loads(manifest.read_text(encoding='utf-8'))
    if data.get('name') != NAME or data.get('version') != 1 or not isinstance(data.get('files'), dict):
        raise InstallError('INVALID_INSTALL_MANIFEST')
    for relative, expected in data['files'].items():
        parts = relative.split("/") if isinstance(relative, str) else []
        if not parts or PurePosixPath(relative).is_absolute() or any(p in ('', '.', '..', '.git') for p in parts) or '\\' in relative or ':' in relative or any(ord(c) < 32 for c in relative):
            raise InstallError('INVALID_PACKAGE_PATH')
        path = root / relative
        no_symlinks(path)
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise InstallError('PACKAGE_HASH_MISMATCH')
    return data


def install(repo, source=None):
    source = Path(source or Path(__file__).resolve().parents[1]).absolute()
    no_symlinks(source)
    data = verify(source)
    repo = Path(repo).absolute()
    no_symlinks(repo)
    if not repo.is_dir() or not (repo / '.git').exists():
        raise InstallError('REPOSITORY_ROOT_REQUIRED')
    skills = repo / '.agents' / 'skills'
    no_symlinks(skills)
    destination = skills / NAME
    if destination.exists():
        no_symlinks(destination)
        previous = verify(destination)
        actual = inventory(destination)
        expected_names = set(previous['files']) | {'install-manifest.json'}
        if set(actual) != expected_names:
            raise InstallError('LOCAL_INSTALL_MODIFIED')
        if previous == data:
            return {'status': 'ALREADY_INSTALLED', 'path': str(destination), 'files': len(data['files']) + 1}
    skills.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix='.' + NAME + '-stage-', dir=skills))
    backup = None
    try:
        for relative in [*data['files'], 'install-manifest.json']:
            target = temporary / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / relative, target)
        verify(temporary)
        if destination.exists():
            backup = skills / ('.' + NAME + '-backup-' + uuid.uuid4().hex)
            os.replace(destination, backup)
        try:
            os.replace(temporary, destination)
        except BaseException:
            if backup:
                os.replace(backup, destination)
                backup = None
            raise
        if backup:
            shutil.rmtree(backup)
        return {'status': 'INSTALLED', 'path': str(destination), 'files': len(data['files']) + 1}
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.repo), ensure_ascii=False, indent=2))
        return 0
    except (InstallError, OSError, ValueError, KeyError, TypeError) as error:
        code = str(error) if isinstance(error, InstallError) else 'INSTALL_INPUT_OR_IO_ERROR'
        print(json.dumps({'status': 'STOPPED', 'code': code}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
