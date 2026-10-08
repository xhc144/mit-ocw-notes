#!/usr/bin/env python3
"""Mechanically inspect a PDF and render every page for separate visual review.

This tool does not verify mathematical correctness or a fixed LaTeX template.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import fitz


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--dpi', type=int, default=110)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(args.pdf)
    problems, links, texts, renders = [], [], [], []
    page_count = len(doc)
    for index, page in enumerate(doc):
        text = page.get_text()
        texts.append(text)
        if '\ufffd' in text:
            problems.append({'page': index + 1, 'kind': 'replacement_character'})
        for link in page.get_links():
            record = {'source_page': index + 1, 'kind': link['kind']}
            if link['kind'] == fitz.LINK_GOTO:
                target = link.get('page', -1)
                record['target_page'] = target + 1
                if not (0 <= target < page_count):
                    problems.append({'page': index + 1, 'kind': 'invalid_internal_link', 'target_page': target + 1})
            elif link['kind'] == fitz.LINK_URI:
                record['uri'] = link.get('uri')
            elif link['kind'] == fitz.LINK_NAMED:
                record['name'] = link.get('nameddest', link.get('name'))
                if not record['name']:
                    problems.append({'page': index + 1, 'kind': 'unnamed_named_link'})
            links.append(record)
        render = args.out / f'page-{index + 1:04d}.png'
        page.get_pixmap(dpi=args.dpi, alpha=False).save(render)
        renders.append(str(render))
    outline = doc.get_toc()
    for level, title, target in outline:
        if not (1 <= target <= page_count):
            problems.append({'kind': 'invalid_outline_target', 'title': title, 'target_page': target})
    all_text = '\f\n'.join(texts)
    (args.out / 'text.txt').write_text(all_text, encoding='utf-8')
    report = {
        'pdf': str(args.pdf.resolve()),
        'sha256': hashlib.sha256(args.pdf.read_bytes()).hexdigest(),
        'page_count': page_count,
        'nonempty_text_pages': sum(bool(text.strip()) for text in texts),
        'outline': outline,
        'links': links,
        'rendered_pages': renders,
        'mechanical_problems': problems,
        'visual_review': 'not_performed_by_this_script',
        'mathematics_review': 'not_performed_by_this_script',
        'fixed_template_review': 'not_performed_by_this_script',
    }
    (args.out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'pages': page_count, 'outline_entries': len(outline), 'links': len(links), 'mechanical_problems': len(problems)}, ensure_ascii=False))
    if problems:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
