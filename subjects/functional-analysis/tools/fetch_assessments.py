"""Archive explicitly selected official OCW assessment files and course pages."""
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urljoin
from html.parser import HTMLParser
import hashlib, json
import fitz

ROOT = Path(__file__).resolve().parents[3]
DEST = ROOT / 'sources/functional-analysis/18.102-spring-2021/assessments'
BASE = 'https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2021/'

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            attrs = dict(attrs)
            if 'href' in attrs: self.links.append(attrs['href'])

def fetch(url, path):
    data = urlopen(url, timeout=60).read()
    path.write_bytes(data)
    return data

def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for page in ['assignments-and-exams', 'syllabus', 'calendar']:
        fetch(BASE + 'pages/' + page + '/', DEST / (page + '.html'))
    items = [(f'ps{i:02}', f'homework-{i}') for i in range(1, 11)]
    items += [('midterm', 'midterm-exam'), ('final-assignment', 'final-assignment')]
    records = []
    for key, slug in items:
        resource = BASE + 'resources/' + slug + '/'
        html = fetch(resource, DEST / (key + '-resource.html'))
        parser = Links(); parser.feed(html.decode())
        pdfs = sorted(set(urljoin(resource, x) for x in parser.links if x.endswith('.pdf')))
        if len(pdfs) != 1: raise RuntimeError((slug, pdfs))
        data = fetch(pdfs[0], DEST / (key + '.pdf'))
        doc = fitz.open(stream=data, filetype='pdf')
        text = '\n\f\n'.join(page.get_text(sort=True) for page in doc)
        (DEST / (key + '.txt')).write_text(text, encoding='utf-8')
        records.append(dict(id=key, resource_url=resource, download_url=pdfs[0],
                            path=f'{key}.pdf', bytes=len(data), pages=len(doc),
                            sha256=hashlib.sha256(data).hexdigest()))
        print(key, len(doc), len(data), flush=True)
    (DEST / 'manifest.json').write_text(json.dumps(dict(course='MIT 18.102 Spring 2021',
        instructor='Casey Rodriguez', retrieved='2026-10-08', files=records),
        ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

if __name__ == '__main__': main()
