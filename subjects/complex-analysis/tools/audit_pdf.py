#!/usr/bin/env python3
"""Audit actual PDF page text, embedded fonts, outline and internal link destinations."""
import argparse
import hashlib
import json
from pathlib import Path
import fitz

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('pdf', type=Path)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
issues = []
records = []
with fitz.open(args.pdf) as doc:
    toc = doc.get_toc()
    internal = external = 0
    named_destinations = []
    internal_destinations = []
    for level, label, page in toc:
        if not 1 <= page <= len(doc):
            issues.append(f'Invalid outline destination: {label}')
    for i, page in enumerate(doc):
        text = page.get_text()
        links = page.get_links()
        for link in links:
            if link['kind'] in (fitz.LINK_GOTO, fitz.LINK_NAMED):
                internal += 1
                internal_destinations.append({'source_page': i+1, 'target_page': link.get('page', -1)+1})
                if not 0 <= link.get('page', -1) < len(doc):
                    issues.append(f'Invalid link on page {i+1}')
                if link['kind'] == fitz.LINK_NAMED:
                    named_destinations.append({'source_page': i+1, 'name': link.get('nameddest'), 'target_page': link.get('page', -1)+1})
            elif link['kind'] == fitz.LINK_URI:
                external += 1
        if '\ufffd' in text:
            issues.append(f'Replacement character on page {i+1}')
        records.append({'page': i+1, 'text_chars': len(text), 'text_sha256': hashlib.sha256(text.encode()).hexdigest(), 'links': len(links)})
    fonts = []
    for font in {tuple(x) for p in doc for x in p.get_fonts(full=True)}:
        xref = font[0]
        if xref:
            name, ext, typ, data = doc.extract_font(xref)
            fonts.append({'name': name, 'embedded': bool(data), 'bytes': len(data)})
            if not data:
                issues.append(f'Unembedded font: {name}')
    first_main_page = next(page for level, label, page in toc if level == 1 and label.startswith('1 '))
    contents_start = next(i+1 for i,p in enumerate(doc) if i+1 < first_main_page and '\n目录\n' in '\n'+p.get_text())
    contents_pages = list(range(contents_start, first_main_page))
    toc_links = [x for x in internal_destinations if x['source_page'] in contents_pages]
    if len(toc_links) != len(toc) or [x['target_page'] for x in toc_links] != [x[2] for x in toc]:
        issues.append('Contents links do not match the complete outline destinations')
    result = {'status': 'PASS' if not issues else 'FAIL', 'pdf_sha256': hashlib.sha256(args.pdf.read_bytes()).hexdigest(), 'pages': len(doc), 'outline': toc, 'outline_entries': len(toc), 'internal_links': internal, 'contents_pages': contents_pages, 'contents_links_checked': len(toc_links), 'named_destinations': named_destinations, 'external_links': external, 'fonts': sorted(fonts, key=lambda x: x['name']), 'per_page': records, 'issues': issues, 'limitation': 'Destination validity is checked locally; external web availability and visual/mathematical correctness are separate reviews.'}
args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ['status', 'pages', 'outline_entries', 'internal_links', 'external_links', 'issues']}))
if issues:
    raise SystemExit(1)
