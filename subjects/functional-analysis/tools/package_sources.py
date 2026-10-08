#!/usr/bin/env python3
"""Create a deterministic clean source ZIP from this book's named input trees."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=None)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = args.out or root / 'functional-analysis-source.zip'
    selected = [root / name for name in (
        'main.tex', 'README.md', 'BUILD.md', 'ATTRIBUTION.md', 'LICENSE.md',
        'source-manifest.json', 'assessment-inventory.json',
        'qa/review-banach.md', 'qa/review-hilbert.md',
        'qa/review-assessments-1.md', 'qa/review-assessments-2.md',
        'qa/review-assessments-3.md', 'qa/review-coverage.md',
        'qa/core-preservation.json', 'qa/template-lock.json',
        'qa/source-integrity.json', 'qa/visual-review.json',
        'qa/visual-pages-1.json', 'qa/visual-pages-2.json', 'qa/visual-pages-3.json',
    )]
    for directory in ('chapters', 'vendor/math-latex-typesetting', 'tools'):
        selected.extend(p for p in (root / directory).rglob('*') if p.is_file()
                        and '__pycache__' not in p.parts and p.suffix != '.pyc')
    selected = sorted(set(selected))
    members = []
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in selected:
            if path.is_symlink():
                raise RuntimeError(f'Symlink is not a clean source: {path}')
            relative = path.relative_to(root).as_posix()
            if path.suffix.lower() in {'.otf', '.ttf', '.pdf', '.png', '.zip'}:
                raise RuntimeError(f'Unexpected binary source: {relative}')
            raw = path.read_bytes()
            info = zipfile.ZipInfo('functional-analysis/' + relative, (2026, 10, 8, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, raw, compresslevel=9)
            members.append({'path': relative, 'bytes': len(raw),
                            'sha256': hashlib.sha256(raw).hexdigest()})
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
    record = {'zip': output.name, 'bytes': output.stat().st_size,
              'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
              'members': members, 'excluded': ['fonts', 'PDFs', 'page images',
              'build cache', 'original OCW ZIP', 'macOS metadata']}
    report = root / 'qa/source-package.json'
    report.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'zip': str(output), 'members': len(members),
                      'bytes': record['bytes'], 'sha256': record['sha256']}))


if __name__ == '__main__':
    main()
