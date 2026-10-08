#!/usr/bin/env python3
"""Verify release PDF navigation and the locked class, without claiming math review."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def norm(s):
    return ''.join(c for c in s if c.isalnum())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    d = fitz.open(args.pdf)
    errors, outlines, links = [], [], []
    for level, title, page, dest in d.get_toc(False):
        ok = 1 <= page <= len(d)
        text_matches = ok and norm(title) in norm(d[page-1].get_text())
        if not text_matches:
            errors.append(f'outline heading not on destination page: {title}')
        outlines.append({'level': level, 'title': title, 'physical_page': page,
                         'heading_on_destination_page': bool(text_matches),
                         'named_destination': dest.get('nameddest')})
    for i, p in enumerate(d):
        if tuple(round(x, 2) for x in (p.rect.width, p.rect.height)) != (612.0, 792.0):
            errors.append(f'wrong page size: {i+1}')
        for l in p.get_links():
            rect = l['from']
            valid = p.rect.contains(rect) and not rect.is_empty
            target = l.get('page')
            if target is not None:
                valid = valid and 0 <= target < len(d)
            elif l.get('uri'):
                valid = valid and l['uri'].startswith('https://')
            else:
                valid = False
            if not valid:
                errors.append(f'invalid link on physical page {i+1}: {l}')
            links.append({'source_physical_page': i+1, 'kind': l['kind'],
                          'destination_physical_page': target+1 if target is not None else None,
                          'named_destination': l.get('nameddest'), 'uri': l.get('uri'),
                          'valid_rectangle_and_destination': bool(valid)})
    s = (ROOT/'main.tex').read_text()
    block = re.search(r'% WZ-LOCKED-CLASS-BEGIN.*?% WZ-LOCKED-CLASS-END', s, re.S).group(0)
    block_hash = hashlib.sha256(block.encode()).hexdigest()
    if block_hash != 'de41f091f341740c436084acea209a40d1777864533b6626b9f2b6d7fdf3b74f':
        errors.append('locked class differs from the frozen authorized class hash')
    golden = ROOT.parent/'probability/main.tex'
    golden_match = None
    if golden.is_file():
        gb = re.search(r'% WZ-LOCKED-CLASS-BEGIN.*?% WZ-LOCKED-CLASS-END', golden.read_text(), re.S).group(0)
        golden_match = block == gb
        if not golden_match:
            errors.append('locked class differs from probability golden source')
    labels = []
    for p in sorted((ROOT/'chapters').glob('ch*.tex')):
        labels.extend(re.findall(r'\\label\{(ex:\d+[abc])\}', p.read_text()))
    answers = re.findall(r'习题\\ref\{(ex:\d+[abc])\}', (ROOT/'chapters/solutions.tex').read_text())
    expected = {f'ex:{n}{l}' for n in range(1, 13) for l in 'abc'}
    if len(labels) != 36 or set(labels) != expected or len(answers) != 36 or set(answers) != expected:
        errors.append('exercise/answer labels do not form the expected 36 unique pairs')
    bad_controls = []
    for p in [ROOT/'main.tex', *sorted((ROOT/'chapters').glob('*.tex'))]:
        if any(x < 32 and x not in (9, 10) for x in p.read_bytes()):
            bad_controls.append(p.relative_to(ROOT).as_posix())
    if bad_controls:
        errors.append(f'unexpected source control bytes: {bad_controls}')
    result = {'schema_version': 1, 'pdf_sha256': digest(args.pdf), 'physical_pages': len(d),
              'outline_count': len(outlines), 'link_count': len(links),
              'internal_link_count': sum(x['destination_physical_page'] is not None for x in links),
              'external_link_count': sum(x['uri'] is not None for x in links),
              'exercise_count': len(labels), 'complete_answer_count': len(answers),
              'locked_class_sha256': block_hash,
              'identical_to_probability_locked_class': golden_match,
              'outlines': outlines, 'links': links, 'errors': errors,
              'status': 'PASS' if not errors else 'FAIL',
              'limits': ['No mathematical or visual assessment is performed by this script.',
                         'External URLs are structurally checked; source acquisition is separately audited.']}
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('outlines', 'links')}, ensure_ascii=False))
    raise SystemExit(bool(errors))

if __name__ == '__main__':
    main()
