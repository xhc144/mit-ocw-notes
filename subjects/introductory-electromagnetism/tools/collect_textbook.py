#!/usr/bin/env python3
"""Append the user's 14-chapter Course Notes selection without resetting batch one."""
import concurrent.futures, hashlib, json, pathlib, re, urllib.parse, urllib.request
from html.parser import HTMLParser
import fitz

ROOT = pathlib.Path(__file__).resolve().parents[3]
DEST = ROOT / 'sources/introductory-electromagnetism'
MF = ROOT / 'manifests/introductory-electromagnetism-sources.json'
BASE = 'https://ocw.mit.edu'
COURSE = BASE + '/courses/8-02-physics-ii-electricity-and-magnetism-spring-2007/'
IDS = ['chapter1fields', 'chap2coulomb_law', 'ch3electri_poten', 'chapte4gauss_law',
       'chap5capacitance', 'chapter6current', 'chap7dc_circuits', 'ch8magneti_field',
       'ch9sourc_b_field', 'cha10faraday_law', 'chap11inductance', 'cha12ac_circuits',
       'chapte13em_waves', 'ch14_inter_diffr']

class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a': self.links.append(dict(attrs).get('href', ''))

def get(url):
    assert urllib.parse.urlparse(url).hostname == 'ocw.mit.edu'
    with urllib.request.urlopen(url, timeout=60) as response:
        assert urllib.parse.urlparse(response.url).hostname == 'ocw.mit.edu'
        return response.read(), response.url

manifest = json.loads(MF.read_text())
frozen = {'batch': '14-chapter Course Notes required as the main theoretical source',
          'frozen_at': '2026-10-11T16:31:00Z', 'course': COURSE,
          'resources': [{'id': name, 'chapter': i, 'kind': 'course-note-chapter',
                         'resource_url': COURSE + 'resources/' + name + '/',
                         'status': 'frozen_selected'} for i, name in enumerate(IDS, 1)]}
freeze_path = DEST / 'selection-textbook-frozen.json'
if not freeze_path.exists():
    freeze_path.write_text(json.dumps(frozen, ensure_ascii=False, indent=2) + '\n')
print('FROZEN 14 chapters before PDF downloads', flush=True)

def collect(item):
    data, final = get(item['resource_url']); parser = Links(); parser.feed(data.decode())
    urls = list(dict.fromkeys(urllib.parse.urljoin(BASE, link) for link in parser.links
                             if urllib.parse.urlparse(link).path.endswith('.pdf')))
    if len(urls) != 1: raise ValueError((item['id'], urls))
    data, final = get(urls[0]); assert data.startswith(b'%PDF-')
    doc = fitz.open(stream=data, filetype='pdf'); assert len(doc) and not doc.is_encrypted
    text = '\n'.join(page.get_text() for page in doc)
    out = DEST / '8.02-spring2007' / (item['id'] + '.pdf')
    out.write_bytes(data); out.with_suffix('.txt').write_text(text)
    return dict(item, status='downloaded_verified', url=urls[0], final_url=final,
                path=out.relative_to(ROOT).as_posix(), text_path=out.with_suffix('.txt').relative_to(ROOT).as_posix(),
                sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), pages=len(doc),
                license='CC BY-NC-SA 4.0 unless an object bears an explicit exception',
                attribution='MIT OpenCourseWare; Peter Dourmashkin, Eric Hudson, Sen-Ben Liao and MIT 8.02 course staff',
                rights_review='pending object-level independent review', archive_allowed=False)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    added = list(pool.map(collect, frozen['resources']))
manifest['resources'] = [x for x in manifest['resources'] if x['id'] not in IDS] + added
manifest['selection'] = 'Main theoretical source: all 14 Course Notes chapters, plus all 36 session summaries and all 11 Friday problem-solving worksheets from 8.02 Spring 2007. Other course layers and 8.022 PDFs are not selected.'
manifest['selection_batches'] = ['sources/introductory-electromagnetism/selection-frozen.json',
                                  'sources/introductory-electromagnetism/selection-textbook-frozen.json']
MF.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print('VERIFIED', len(added), 'new PDFs', sum(x['pages'] for x in added), 'new pages', flush=True)
