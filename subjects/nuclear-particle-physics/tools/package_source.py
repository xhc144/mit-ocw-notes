#!/usr/bin/env python3
"""Publish one checked PDF and a reproducible, independently buildable source ZIP."""
import argparse
import hashlib
import pathlib
import shutil
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
NAME = 'nuclear-particle-physics'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf', type=pathlib.Path, required=True)
    args = ap.parse_args()
    pdf = args.pdf.resolve()
    if not pdf.is_file():
        ap.error(f'PDF does not exist: {pdf}')
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    output_pdf = dist / f'{NAME}-zh.pdf'
    shutil.copyfile(pdf, output_pdf)
    files = [ROOT / name for name in
             ('main.tex', 'course-info.tex', 'README.md', 'BUILDING.md',
              'source-manifest.json')]
    for subdir, glob in (('chapters', '*.tex'), ('figures', '*.pdf'),
                         ('tools', '*.py')):
        files.extend(sorted((ROOT / subdir).glob(glob)))
    files.extend(sorted(p for p in (ROOT / 'vendor').rglob('*')
                        if p.is_file() and '__pycache__' not in p.parts))
    # Old release-specific QA files have their own fixed PDF hashes. The revised
    # book's current checks and source provenance are carried separately.
    current_qa = {
        'coverage-freeze.json', 'recitation-coverage-freeze.json',
        'recitation-source-review.md', 'recitation-nuclear-instruments-review.md',
        'exam-figure-provenance.json', 'license-exceptions.json',
        'nuclear-data.json', 'numerical-checks.json',
        'independent-review-8701.md', 'revision-validation.json',
        'revision-checkpoint.json',
    }
    files.extend(sorted(ROOT / 'qa' / name for name in current_qa))
    if not all(p.is_file() and p.is_relative_to(ROOT) for p in files):
        raise RuntimeError('A source file is missing or outside the subject directory')
    output_zip = dist / f'{NAME}-source.zip'
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED,
                         compresslevel=9) as archive:
        for path in sorted(set(files)):
            member = f'{NAME}/{path.relative_to(ROOT)}'
            info = zipfile.ZipInfo(member, date_time=(2026, 10, 12, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    with zipfile.ZipFile(output_zip) as archive:
        if archive.testzip() is not None:
            raise RuntimeError('ZIP CRC check failed')
    print(f'PDF {output_pdf} {sha256(output_pdf)}')
    print(f'ZIP {output_zip} {sha256(output_zip)} ({len(files)} files)')


if __name__ == '__main__':
    main()
