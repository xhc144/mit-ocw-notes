"""Download MIT OCW official resources; preserve byte hashes and extracted content."""
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urljoin
from html.parser import HTMLParser
import hashlib, json, re, subprocess, concurrent.futures

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ocw.mit.edu'
COURSES = {'6.253':'6-253-convex-analysis-and-optimization-spring-2012',
           '15.053':'15-053-optimization-methods-in-management-science-spring-2013'}
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.href=None; self.text=''
    def handle_starttag(self, tag, attrs):
        if tag=='a': self.href=dict(attrs).get('href'); self.text=''
    def handle_data(self,data):
        if self.href: self.text+=data
    def handle_endtag(self,tag):
        if tag=='a' and self.href: self.links.append((self.href,self.text.strip())); self.href=None
def get(url):
    with urlopen(Request(url,headers={'User-Agent':'MIT-OCW-notes source verification'}),timeout=60) as r: return r.read()
def acquire(item):
    course,section,url,title=item
    raw=get(url)
    p=ROOT/'sources'/course/'assessments'; p.mkdir(parents=True,exist_ok=True)
    h=Links(); h.feed(raw.decode())
    downloads=[urljoin(BASE,u) for u,t in h.links if re.search(r'\.(pdf|xls|xlsx|xlsb)$',u,re.I)]
    if not downloads: return None
    u=downloads[0]; name=u.rsplit('/',1)[-1]
    name=re.sub(r'^[a-f0-9]{32}_','',name)
    data=get(u); path=p/name; path.write_bytes(data)
    rec={'course':course,'section':section,'title':title,'resource_page':url,'url':u,'path':str(path.relative_to(ROOT)),
         'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'accessed':'2026-10-08'}
    if path.suffix.lower()=='.pdf':
        subprocess.run(['pdftotext','-layout',str(path),str(path.with_suffix('.txt'))],check=True)
        import fitz
        doc=fitz.open(path); rec['pages']=len(doc)
        txt=path.with_suffix('.txt').read_text()
        rec['rights_lines']=[s.strip() for s in txt.splitlines() if re.search(r'copyright|rights reserved|excluded|removed|permission|courtesy',s,re.I)]
    else:
        import xlrd, io
        if path.suffix.lower()=='.xlsb':
            import pyxlsb
            with pyxlsb.open_workbook(str(path)) as wb:
                sheets={}
                for name in wb.sheets:
                    with wb.get_sheet(name) as s: sheets[name]=[[c.v for c in row] for row in s.rows()]
            rec['actual_format']='xlsb'
        elif data[:2]==b'PK':
            import openpyxl
            wb=openpyxl.load_workbook(io.BytesIO(data),data_only=True)
            sheets={s.title:[[c for c in row] for row in s.values] for s in wb.worksheets}
            rec['actual_format']='xlsx'
        else:
            wb=xlrd.open_workbook(path)
            sheets={s.name:[s.row_values(i) for i in range(s.nrows)] for s in wb.sheets()}
            rec['actual_format']='xls'
        path.with_suffix('.cells.json').write_text(json.dumps(sheets,ensure_ascii=False,indent=2))
        rec['sheets']={name:{'rows':len(rows),'cols':max(map(len,rows),default=0)} for name,rows in sheets.items()}
    return rec
def main():
    manifest=ROOT/'sources/assessment-resources.json'
    previous={r['url']:r for r in json.loads(manifest.read_text())} if manifest.exists() else {}
    items=[]
    for course,slug in COURSES.items():
        sections=['syllabus','lecture-notes','assignments','exams'] if course=='6.253' else ['syllabus','assignments','recitations','study-materials']
        for sec in sections:
            u=f'{BASE}/courses/{slug}/pages/{sec}/'; raw=get(u)
            p=ROOT/'sources'/course; p.mkdir(parents=True,exist_ok=True)
            (p/(sec+'.html')).write_bytes(raw)
            h=Links(); h.feed(raw.decode())
            seen=set()
            for href,title in h.links:
                if '/resources/' in href and re.search(r'\((PDF|XLS|XLSX)\)',title) and href not in seen:
                    if sec=='lecture-notes': continue
                    seen.add(href); items.append((course,sec,urljoin(BASE,href),title))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        records=[r for r in pool.map(acquire,items) if r]
    for r in records:
        old=previous.get(r['url'],{})
        if old.get('sha256')==r['sha256']:
            for key in ['license','derivative_treatment','archive_status','rights_page_notice','extracted_content_path']:
                if key in old:r[key]=old[key]
        else:
            r['archive_status']='local_only_pending_new_rights_review'
            r['extracted_content_path']=str(Path(r['path']).with_suffix('.txt' if 'pages' in r else '.cells.json'))
    manifest.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps([{'course':r['course'],'title':r['title'],'file':r['path'],'pages':r.get('pages'),'sheets':r.get('sheets'),'rights':r.get('rights_lines')} for r in records],ensure_ascii=False,indent=2))
if __name__=='__main__': main()
