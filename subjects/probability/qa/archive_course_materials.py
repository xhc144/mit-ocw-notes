"""Archive official OCW course material with per-resource evidence.

Reads only MIT OCW URLs; no external-textbook problem statements are fetched.
"""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen
import json
import re
import fitz

ROOT = Path(__file__).resolve().parents[3]
BASE = "https://ocw.mit.edu/courses/18-600-probability-and-random-variables-fall-2019/"
OUT = ROOT / "sources/18.600-fall-2019"

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.current = None
    def handle_starttag(self, tag, attrs):
        if tag == "a": self.current = [dict(attrs).get("href", ""), ""]
    def handle_data(self, data):
        if self.current is not None: self.current[1] += data
    def handle_endtag(self, tag):
        if tag == "a" and self.current is not None:
            self.links.append(tuple(self.current)); self.current = None

def get(url):
    if not url.startswith(BASE): raise ValueError("Unexpected download origin")
    with urlopen(url, timeout=60) as r: return r.read()

def archive(entry):
    title, resource, category = entry
    ident = resource.rstrip("/").split("/")[-1]
    raw = get(resource)
    (OUT / "html" / (ident + ".html")).write_bytes(raw)
    parser = Links(); parser.feed(raw.decode())
    pdfs = sorted(set(urljoin(resource, u) for u, _ in parser.links if u.lower().split("?")[0].endswith(".pdf")))
    if len(pdfs) != 1: raise ValueError((ident, pdfs))
    url = pdfs[0]; data = get(url)
    doc = fitz.open(stream=data, filetype="pdf")
    text = "\n".join(p.get_text() for p in doc)
    markers = [line.strip() for line in text.splitlines() if re.search(r"rights reserved|copyright|courtesy|©", line, re.I)]
    reserved = any(re.search(r"rights reserved", x, re.I) for x in markers)
    external_textbook = category == "assignments" and "Problem Set" in title
    hold = reserved or external_textbook
    filename = url.rsplit("/", 1)[-1]
    images = [i+1 for i,p in enumerate(doc) if p.get_images()]
    result = dict(id=ident, title=title, category=category, resource_url=resource,
        pdf_url=url, filename=filename, sha256=sha256(data).hexdigest(), bytes=len(data),
        pages=len(doc), rights_markers=markers,
        status="hold_explicit_rights" if reserved else "hold_external_textbook" if external_textbook else "archived_default_cc",
        default_license="CC BY-NC-SA 4.0", downloaded_on="2026-10-08",
        embedded_image_pages=images, local_pdf=None if hold else "pdf/"+filename,
        local_text=None if hold else "text/"+ident+".txt",
        rights_review_methods=["full_extracted_text_marker_scan", "official_resource_page_review", "all_pages_embedded_raster_inventory"],
        hold_reason="Identifiable Ross textbook excerpts; user prohibits copying external-textbook statements. Mixed original is retained only in temporary inspection storage, not distributed." if external_textbook else None)
    if hold:
        inspection = Path("/tmp/probability-held-sources"); inspection.mkdir(exist_ok=True)
        (inspection / filename).write_bytes(data)
        (inspection / (ident+".txt")).write_text(text)
        result["inspection_pdf"] = str(inspection / filename)
        result["inspection_text"] = str(inspection / (ident+".txt"))
    if not hold:
        (OUT / "pdf" / filename).write_bytes(data)
        (OUT / "text" / (ident+".txt")).write_text(text)
    return result

def main():
    entries = []
    for page in ["syllabus", "calendar", "readings", "assignments", "exams", "instructor-insights"]:
        raw = get(BASE+"pages/"+page+"/")
        (OUT / "html" / (page+".html")).write_bytes(raw)
        parser = Links(); parser.feed(raw.decode())
        if page in ["assignments", "exams"]:
            for url,title in parser.links:
                absolute = urljoin(BASE,url)
                if "/resources/" in absolute and "PDF" in title:
                    item = (title.strip(), absolute, page)
                    if item not in entries: entries.append(item)
    with ThreadPoolExecutor(max_workers=6) as pool: files = list(pool.map(archive, entries))
    previous = json.loads((OUT / "source-manifest.json").read_text())
    hashes = {x["sha256"]: x["id"] for x in previous["files"]}
    for x in files:
        x["identical_lecture_resource"] = hashes.get(x["sha256"])
    result = dict(course=previous["course"], term=previous["term"], instructor=previous["instructor"],
        accessed_on="2026-10-08", resource_count=len(files), total_resource_pages=sum(x["pages"] for x in files),
        unique_sha256_count=len({x["sha256"] for x in files}),
        archived_count=sum(x["status"] == "archived_default_cc" for x in files),
        held_count=sum(x["status"] != "archived_default_cc" for x in files),
        archived_pages=sum(x["pages"] for x in files if x["status"] == "archived_default_cc"),
        held_pages=sum(x["pages"] for x in files if x["status"] != "archived_default_cc"), files=files)
    (OUT / "course-materials-manifest.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k != "files"},ensure_ascii=False))
    for x in files: print(x["id"],x["pages"],x["title"],x["status"],x["identical_lecture_resource"] or "")

if __name__ == "__main__": main()
