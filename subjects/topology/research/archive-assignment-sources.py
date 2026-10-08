#!/usr/bin/env python3
"""Archive the explicitly selected official assignment sources; no Git operations."""
import concurrent.futures
import datetime
import hashlib
import html.parser
import json
from pathlib import Path
import urllib.request

import fitz

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'research/source-manifest.json'


class TextParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style'}:
            self.skip += 1
        if tag in {'p', 'div', 'li', 'tr', 'h1', 'h2', 'h3', 'br'}:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in {'script', 'style'} and self.skip:
            self.skip -= 1
        if tag in {'p', 'div', 'li', 'tr', 'h1', 'h2', 'h3'}:
            self.parts.append('\n')

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def plan():
    rows = []
    for name in ('18.s190-iap2023', '18.900-spring2023', '18.901-fall2004',
                 '18.904-spring2011', '18.905-fall2016', '18.950-fall2008',
                 '18.965-fall2004', '18.102-spring2021'):
        meta = json.loads((ROOT / 'sources' / name / 'SOURCE.json').read_text())
        base = meta['course_url']
        pages = ['syllabus']
        if name in {'18.901-fall2004', '18.905-fall2016', '18.965-fall2004', '18.102-spring2021'}:
            pages += ['calendar']
        if name in {'18.901-fall2004', '18.950-fall2008'}:
            pages += ['assignments']
        if name == '18.102-spring2021':
            pages += ['lecture-notes-and-readings']
        for page in pages:
            rows.append((name, f'html/assignment-{page}.html', base + f'pages/{page}/', meta['attribution']))
    base900 = 'https://ocw.mit.edu/courses/18-900-geometry-and-topology-in-the-plane-spring-2023/'
    for n in (4, 29, 30, 31, 33, 40):
        fn = f'mit18_900s23_q{n}.pdf'
        rows.append(('18.900-spring2023', 'pdf/' + fn, base900 + fn, 'Paul Seidel'))
    rows.append(('18.900-spring2023', 'pdf/mit18_900s23_lec6.pdf', base900 + 'mit18_900s23_lec6.pdf', 'Paul Seidel'))
    rows.append(('18.901-fall2004', 'pdf/problemset_5.pdf',
                 'https://ocw.mit.edu/courses/18-901-introduction-to-topology-fall-2004/d6c5d6d30bf26300b6f1b2c278791796_problemset_5.pdf', 'James Munkres'))
    return rows


def download(spec):
    course, relative, url, author = spec
    path = ROOT / 'sources' / course / relative
    data = urllib.request.urlopen(url, timeout=60).read()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != data:
        raise RuntimeError(f'Refuse to overwrite a differing original: {path}')
    path.write_bytes(data)
    kind = path.suffix[1:]
    row = dict(path=str(path.relative_to(ROOT)), url=url, kind=kind, bytes=len(data),
               sha256=hashlib.sha256(data).hexdigest(), status='downloaded_and_checksum_recorded',
               license='CC-BY-NC-SA-4.0', license_url='https://creativecommons.org/licenses/by-nc-sa/4.0/',
               attribution=author)
    if kind == 'pdf':
        if not data.startswith(b'%PDF-'):
            raise RuntimeError(f'Not a PDF: {url}')
        doc = fitz.open(stream=data, filetype='pdf')
        row.update(pdf_pages=len(doc), pdf_metadata_author=doc.metadata.get('author'),
                   pdf_metadata_title=doc.metadata.get('title'))
        content = '\n\f\n'.join(p.get_text() for p in doc)
    else:
        parser = TextParser()
        parser.feed(data.decode('utf-8'))
        content = '\n'.join(line.strip() for line in ''.join(parser.parts).splitlines() if line.strip())
    text_path = ROOT / 'sources' / course / 'text' / (path.stem + '.txt')
    text_path.parent.mkdir(parents=True, exist_ok=True)
    text_data = (content + '\n').encode()
    text_path.write_bytes(text_data)
    extracted = dict(row, path=str(text_path.relative_to(ROOT)), kind='extracted_text',
                     bytes=len(text_data), sha256=hashlib.sha256(text_data).hexdigest(),
                     status='generated_from_archived_original', derived_from=row['path'])
    for key in ('pdf_pages', 'pdf_metadata_author', 'pdf_metadata_title'):
        extracted.pop(key, None)
    return course, [row, extracted]


if __name__ == '__main__':
    manifest = json.loads(MANIFEST.read_text())
    old = {r['path']: r for r in manifest['files']}
    specs = plan()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(download, specs))
    added = []
    for course, rows in results:
        course_path = ROOT / 'sources' / course / 'SOURCE.json'
        meta = json.loads(course_path.read_text())
        course_rows = {r['path']: r for r in meta['files']}
        for row in rows:
            old[row['path']] = row
            course_rows[row['path']] = row
            added.append(row)
        meta['files'] = list(course_rows.values())
        meta['assignment_revision_retrieved_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        course_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n')
    manifest['files'] = list(old.values())
    counts = manifest['counts']
    pdfs = [r for r in old.values() if r['kind'] == 'pdf']
    counts.update(all_pdf_files=len(pdfs), all_pdf_pages=sum(r['pdf_pages'] for r in pdfs),
                  archived_remote_files=sum(r['kind'] != 'extracted_text' for r in old.values()),
                  extracted_texts=sum(r['kind'] == 'extracted_text' for r in old.values()),
                  assignment_added_pdf_files=sum(r['kind'] == 'pdf' for r in added),
                  assignment_added_pdf_pages=sum(r.get('pdf_pages', 0) for r in added))
    manifest['assignment_revision_retrieved_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'review/assignment-source-acquisition.json').write_text(json.dumps(
        {'explicit_urls': len(specs), 'files': added, 'counts': counts}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(counts, ensure_ascii=False))
