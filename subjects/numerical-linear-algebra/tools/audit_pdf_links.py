"""Check resolved internal annotations/bookmarks, including hyperref named links.

Requires PyMuPDF. Run from this subject: python3 tools/audit_pdf_links.py.
This checks destinations, not website availability or mathematical correctness.
"""
import hashlib
import json
from pathlib import Path
import sys
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'dist/main.pdf'
doc = fitz.open(path)
names = doc.resolve_names()
internal, external, errors = [], [], []
for i, page in enumerate(doc):
    for link in page.get_links():
        if link['kind'] == fitz.LINK_URI:
            external.append({'from_page': i + 1, 'uri': link['uri']})
            continue
        if link['kind'] in (fitz.LINK_GOTO, fitz.LINK_NAMED):
            name = link.get('nameddest')
            target = names.get(name, link) if name else link
            dest = target.get('page', -1)
            row = {'from_page': i + 1, 'to_page': dest + 1, 'name': name}
            internal.append(row)
            if not 0 <= dest < len(doc) or (name and name not in names):
                errors.append(row)
        else:
            errors.append({'from_page': i + 1, 'unknown_link_kind': link['kind']})
toc = doc.get_toc()
for level, title, page in toc:
    if not 1 <= page <= len(doc):
        errors.append({'bookmark': title, 'to_page': page})
fom = {name: names[name]['page'] + 1 for name in ('exercise.9.1', 'exercise.16.1')}
for source, dest in [('exercise.9.1', 'exercise.16.1'), ('exercise.16.1', 'exercise.9.1')]:
    if not any(r['from_page'] == fom[source] and r['name'] == dest for r in internal):
        errors.append({'missing_FOM_reciprocal_link': [source, dest]})
report = {'status': 'PASS' if not errors else 'FAIL',
          'pdf_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
          'page_count': len(doc), 'internal_annotations': len(internal),
          'external_URI_annotations': len(external), 'bookmarks': len(toc),
          'named_destinations': len(names), 'FOM_reciprocal_targets': fom,
          'errors': errors, 'links': internal,
          'limits': 'Destination resolution and page bounds only; external URLs not requested.'}
(ROOT / 'qa/assessment-link-checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'links'}, ensure_ascii=False))
if errors:
    raise SystemExit(1)
