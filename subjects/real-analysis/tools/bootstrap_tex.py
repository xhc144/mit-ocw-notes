#!/usr/bin/env python3
"""Install pinned Chinese TeX resources and fixed-template fonts locally.

Package hashes were verified against signed Debian trixie metadata on 2026-10-08.
The CM Unicode archive checksum was verified against official TeX Live metadata.
This does not modify the system TeX installation or install a fixed document style.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request
from pathlib import Path


PACKAGES = {
    'texlive-lang-chinese_2024.20250309-1_all.deb': '583cd26483b79d32191a8d0a198e80546415d6eca4f23a4bedd253ebdb661291',
    'texlive-lang-cjk_2024.20250309-1_all.deb': '56c795c17b392766c66132f469aab024c374eb92848685ab1d66072a14115b66',
}
BASE_URL = 'https://deb.debian.org/debian/pool/main/t/texlive-lang/'
FONT_URL = 'https://mirrors.ctan.org/systems/texlive/tlnet/archive/cm-unicode.tar.xz'
FONT_SHA512 = '5d6cce2e396ffa0dc887e839f4ef57865db9eda3dcdf6a62737008b53837c40ee1498d97ab06eab8f0802e745787fa5c107c0738a8dedd4e65f6996aee555c48'


def digest(path: Path, algorithm: str = 'sha256') -> str:
    value = hashlib.new(algorithm)
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def download(url: str, target: Path, expected: str, algorithm: str = 'sha256') -> None:
    if target.is_file() and digest(target, algorithm) == expected:
        return
    temporary = target.with_name(target.name + '.part')
    request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        with temporary.open('wb') as stream:
            shutil.copyfileobj(response, stream, length=1024 * 1024)
    if digest(temporary, algorithm) != expected:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f'{algorithm} mismatch: {target.name}; resource was not installed')
    temporary.replace(target)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--texmf-dir', type=Path, default=Path('/workspace/.local/texmf'))
    parser.add_argument('--cache-dir', type=Path, default=Path('/workspace/.local/topology-toolchain/downloads'))
    args = parser.parse_args()
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    args.texmf_dir.mkdir(parents=True, exist_ok=True)
    for filename, expected in PACKAGES.items():
        package = args.cache_dir / filename
        download(BASE_URL + filename, package, expected)
        if digest(package) != expected:
            raise RuntimeError(f'SHA256 mismatch: {filename}')
        with tempfile.TemporaryDirectory(prefix='topology-tex-', dir='/tmp') as temporary_dir:
            subprocess.run(['dpkg-deb', '-x', str(package), temporary_dir], check=True)
            source = Path(temporary_dir) / 'usr/share/texlive/texmf-dist'
            if not source.is_dir():
                raise RuntimeError(f'Expected TEXMF tree missing in {filename}')
            if (source / 'tex/latex/l3kernel').exists():
                raise RuntimeError(f'Unexpected l3kernel override in {filename}')
            shutil.copytree(source, args.texmf_dir, dirs_exist_ok=True, ignore_dangling_symlinks=True)
        print(f'Verified and extracted {filename}')
    font_archive = args.cache_dir / 'cm-unicode.tar.xz'
    download(FONT_URL, font_archive, FONT_SHA512, 'sha512')
    with tempfile.TemporaryDirectory(prefix='topology-fonts-', dir='/tmp') as temporary_dir:
        with tarfile.open(font_archive, 'r:xz') as archive:
            archive.extractall(temporary_dir, filter='data')
        source = Path(temporary_dir) / 'fonts/opentype/public/cm-unicode'
        for name in ['cmunrm.otf', 'cmunbx.otf', 'cmunti.otf', 'cmunbi.otf']:
            if not (source / name).is_file():
                raise RuntimeError(f'Fixed template font missing: {name}')
        target = args.texmf_dir / 'fonts/opentype/public/cm-unicode'
        shutil.copytree(source, target, dirs_exist_ok=True)
        font_docs = Path(temporary_dir) / 'doc/fonts/cm-unicode'
        if font_docs.is_dir():
            shutil.copytree(font_docs, args.texmf_dir / 'doc/fonts/cm-unicode', dirs_exist_ok=True)
    print('Verified and extracted CM Unicode 0.7.0 OpenType fonts; fonts are runtime dependencies only.')
    print(f'TEXMFHOME={args.texmf_dir.resolve()}')
    print('System l3kernel and system binaries were left unchanged.')


if __name__ == '__main__':
    main()
