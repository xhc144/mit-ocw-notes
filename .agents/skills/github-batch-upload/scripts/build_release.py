#!/usr/bin/env python3
"""Build a deterministic self-contained skill ZIP and verified copy index."""
import hashlib
import json
from pathlib import Path
import zipfile


def build(root=None):
    root = Path(root or Path(__file__).resolve().parents[1])
    files = {}
    for base in ('SKILL.md', 'README.md', 'VERSION', 'agents', 'references', 'scripts', 'tests'):
        candidate = root / base
        for path in ([candidate] if candidate.is_file() else sorted(candidate.rglob('*'))):
            if path.is_symlink():
                raise ValueError('symlink package entry')
            if not path.is_file() or '__pycache__' in path.parts or path.suffix == '.pyc':
                continue
            files[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    index = {'version': 1, 'name': 'github-batch-upload', 'release': (root / 'VERSION').read_text().strip(), 'files': dict(sorted(files.items()))}
    (root / 'install-manifest.json').write_text(json.dumps(index, ensure_ascii=False, sort_keys=True, indent=2) + '\n')
    entries = sorted([*files, 'install-manifest.json'])
    destination = root / 'dist'; destination.mkdir(exist_ok=True)
    archive = destination / 'github-batch-upload.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for relative in entries:
            entry = zipfile.ZipInfo('github-batch-upload/' + relative, date_time=(2026, 10, 8, 0, 0, 0))
            entry.external_attr = 0o100644 << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            output.writestr(entry, (root / relative).read_bytes())
    with zipfile.ZipFile(archive) as check:
        if check.testzip() is not None:
            raise ValueError('ZIP integrity failed')
        for relative in entries:
            if check.read('github-batch-upload/' + relative) != (root / relative).read_bytes():
                raise ValueError('ZIP bytes mismatch')
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (destination / 'SHA256SUMS').write_text(digest + '  github-batch-upload.zip\n')
    return {'archive': str(archive), 'sha256': digest, 'files': len(entries), 'size_bytes': archive.stat().st_size}


if __name__ == '__main__':
    print(json.dumps(build(), indent=2))
