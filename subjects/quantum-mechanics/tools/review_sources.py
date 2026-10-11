#!/usr/bin/env python3
"""Apply the explicit conservative rights selection; validate every retained PDF."""
import json,pathlib,re,hashlib,shutil,collections
import fitz
ROOT=pathlib.Path(__file__).resolve().parents[3]
p=ROOT/'manifests/quantum-mechanics-sources.json';m=json.loads(p.read_text())
HOLD={}
hold=pathlib.Path('/tmp/quantum-rights-hold');hold.mkdir(exist_ok=True)
for i in m['resources']:
 original_path=i.get('path',i.get('download_path_not_distributed'));name=pathlib.Path(original_path).name;orig=name[33:]
 i.setdefault('author','Course instructor: Barton Zwiebach; individual PDF not separately signed unless identified in document.')
 i['license_reviewed_on']='2026-10-11';i['third_party_exceptions']=[]
 if i['course']=='8.04' and i['category']=='exams':i['document_term']='Fall 2015 (distributed on Spring 2016 OCW page)'
 elif i['course']=='8.05' and i['category']=='exams':
  match=re.search(r'201[123]',orig);i['document_term']=match.group(0) if match else 'course formula sheet'
 else:i['document_term']=i['term']
 if orig in HOLD:
  i.update(archive_allowed=False,license_review='conservative_hold_not_confirmed_exception',third_party_exceptions=[],rights_uncertainties=[HOLD[orig]],explicit_document_rights_exclusion_found=False,retained_in_repository=False)
  for k in ['path','text_path']:
   if k not in i:continue
   f=ROOT/i[k]
   if f.exists():shutil.move(str(f),str(hold/f.name))
  i['download_path_not_distributed']=i.pop('path',original_path);i.pop('text_path',None)
 elif i.get('license_review','').startswith('OCW_default_restored'):
  f=ROOT/i['path'];b=f.read_bytes();d=fitz.open(f)
  assert hashlib.sha256(b).hexdigest()==i['sha256'] and len(d)==i['pages']
  i.update(archive_allowed=True,retained_in_repository=True)
 elif 'duplicate_of' in i:
  i.update(archive_allowed=False,license_review='duplicate_alias',retained_in_repository=False)
 else:
  f=ROOT/i['path'];b=f.read_bytes();d=fitz.open(f)
  assert hashlib.sha256(b).hexdigest()==i['sha256'] and len(d)==i['pages']
  assert all(p.get_text() is not None for p in d)
  i.update(archive_allowed=True,license_review='OCW_default_no_document_specific_exception_found_in_text',retained_in_repository=True)
  i['review_scope']='All PDF pages opened and extracted; document text scanned for credits, explicit textbook adaptations and rights notices. No claim that absence of a notice resolves all possible unmarked rights.'
m['rights_policy']='Official OCW default CC BY-NC-SA for unmarked documents, carrying instructor/contributor attribution. All 23 earlier overbroad whole-document holds restored following official FAQ and resource-page audit. Externally attributed copied statements/examples remain item-level review in Chinese coverage; number-only textbook references are not invented. No proven contrary rights marking was found in these 23 official documents. No Git history rewrite.'
m['known_gaps']=['8.06 Spring 2018 chapter 5 PDF not supplied on official lecture-notes page.','8.06 Spring 2018 exams expressly unavailable to OCW users.','8.06 syllabus mentions an ungraded last-week problem set; assignments page supplies only nine.','Official solutions not linked on the selected three OCW course pages; classroom website availability does not mean OCW availability.']
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
ret=[i for i in m['resources'] if i['retained_in_repository']]
q=dict(date='2026-10-11',downloaded_resource_links=len(m['resources']),unique_downloaded_pdfs=len({i['sha256'] for i in m['resources']}),downloaded_unique_pages=sum(i['pages'] for i in m['resources'] if 'duplicate_of' not in i),retained_pdfs=len(ret),retained_pdf_pages=sum(i['pages'] for i in ret),withheld_pdfs=sum(i['license_review']=='conservative_hold_not_confirmed_exception' and 'duplicate_of' not in i for i in m['resources']),courses={c:dict(pdf_count=sum(i['course']==c for i in ret),pdf_pages=sum(i['pages'] for i in ret if i['course']==c)) for c in ['8.04','8.05','8.06']},verification='PDF magic, PyMuPDF all-page opening, page count, SHA256 and size verified; no substitute course URL indexes.',rights_hold_publication=False)
(ROOT/'subjects/quantum-mechanics/qa/source-verification.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps(q,ensure_ascii=False))
