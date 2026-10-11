#!/usr/bin/env python3
"""Apply the explicit conservative rights selection; validate every retained PDF."""
import json,pathlib,re,hashlib,shutil,collections
import fitz
ROOT=pathlib.Path(__file__).resolve().parents[3]
p=ROOT/'manifests/quantum-mechanics-sources.json';m=json.loads(p.read_text())
HOLD={
'MIT8_04S16_ps6_2016.pdf':'Contains Griffiths Problem 2.45 reference without a supplied problem statement.',
'MIT8_04S16_ps7_2016.pdf':'Contains Griffiths 2.47 and Problem 2.42.',
'MIT8_05F13_ps1.pdf':'Variation on Griffiths 2.2, textbook-dependent square-well question, and problem-number-only 2.38.',
'MIT8_05F13_ps3.pdf':'Contains question from Axler.',
'MIT8_05F13_ps5.pdf':'Contains Griffiths 3.32 problem-number-only reference.',
'MIT8_05F13_ps10.pdf':'Contains Griffiths Problem 4.57; lecture exercises also referenced rather than printed.',
'MIT8_05F13_ps11.pdf':'Mixed angular-momentum questions and textbook table/solution dependencies; held conservatively.',
'MIT8_06S18ps6.pdf':'Contains Griffiths 9.11 and 9.14 problem-number-only references.',
'MIT8_06S18ps7.pdf':'Aharonov-Bohm question explicitly follows Griffiths example and diagram.',
'MIT8_05F13_Chap_01.pdf':'Contains example explicitly attributed to Griffiths.',
'MIT8_05F13_Chap_03.pdf':'Text explicitly follows the discussion in Axler; separate adaptation permission not established.',
'MIT8_04S16_ps3_2016.pdf':'Problem 5 attributed to Merzbacher; textbook-derived question redistribution not established.',
'MIT8_04S16_ps8_2016.pdf':'Problem 5 based on Griffiths 2.33.',
'MIT8_04S16_ps10_2016.pdf':'Problems 3 and 5 based on Ohanian.',
'MIT8_05F13_ps2.pdf':'Exercise based on Shankar 5.2.2.',
'MIT8_05F13_ps4.pdf':'Problems based on Griffiths, Shankar and Axler.',
'MIT8_05F13_ps8.pdf':'Problem 5 based on Sakurai 2.9.',
'MIT8_06S18ch4.pdf':'Contains example based on Griffiths Problem 9.3; whole PDF withheld conservatively.',
'MIT8_06S18ps2.pdf':'Explicit adaptations from Schiff, textbook Feynman-Hellmann questions and Griffiths 6.36.',
'MIT8_06S18ps3.pdf':'Contains problem based on Sakurai.',
'MIT8_06S18ps4.pdf':'Contains problem loosely based on Griffiths 8.6.',
'MIT8_06S18ps8.pdf':'Problem 6 based on Griffiths 11.16–11.18.',
'MIT8_06S18ps9.pdf':'Problem 3 explicitly inspired by Cohen-Tannoudji; permission for source problem not established.'}
hold=pathlib.Path('/tmp/quantum-rights-hold');hold.mkdir(exist_ok=True)
for i in m['resources']:
 original_path=i.get('path',i.get('download_path_not_distributed'));name=pathlib.Path(original_path).name;orig=name[33:]
 i['author']='Course instructor: Barton Zwiebach; individual PDF not separately signed unless identified in document.'
 i['license_reviewed_on']='2026-10-11';i['third_party_exceptions']=[]
 if i['course']=='8.04' and i['category']=='exams':i['document_term']='Fall 2015 (distributed on Spring 2016 OCW page)'
 elif i['course']=='8.05' and i['category']=='exams':
  match=re.search(r'201[123]',orig);i['document_term']=match.group(0) if match else 'course formula sheet'
 else:i['document_term']=i['term']
 if orig in HOLD:
  i.update(archive_allowed=False,license_review='withheld_textbook_derived_content',third_party_exceptions=[HOLD[orig]],retained_in_repository=False)
  for k in ['path','text_path']:
   if k not in i:continue
   f=ROOT/i[k]
   if f.exists():shutil.move(str(f),str(hold/f.name))
  i['download_path_not_distributed']=i.pop('path',original_path);i.pop('text_path',None)
 elif 'duplicate_of' in i:
  i.update(archive_allowed=False,license_review='duplicate_alias',retained_in_repository=False)
 else:
  f=ROOT/i['path'];b=f.read_bytes();d=fitz.open(f)
  assert hashlib.sha256(b).hexdigest()==i['sha256'] and len(d)==i['pages']
  assert all(p.get_text() is not None for p in d)
  i.update(archive_allowed=True,license_review='OCW_default_no_document_specific_exception_found_in_text',retained_in_repository=True)
  i['review_scope']='All PDF pages opened and extracted; document text scanned for credits, explicit textbook adaptations and rights notices. No claim that absence of a notice resolves all possible unmarked rights.'
m['rights_policy']='CC BY-NC-SA 4.0 is the OCW default, not a license for commercial textbooks or identified third-party adaptations. Entire mixed PDFs are withheld pending separate permission; reading references alone do not trigger withholding. No external textbook or site image is bundled.'
m['known_gaps']=['8.06 Spring 2018 chapter 5 PDF not supplied on official lecture-notes page.','8.06 Spring 2018 exams expressly unavailable to OCW users.','8.06 syllabus mentions an ungraded last-week problem set; assignments page supplies only nine.','Official solutions not linked on the selected three OCW course pages; classroom website availability does not mean OCW availability.']
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
ret=[i for i in m['resources'] if i['retained_in_repository']]
q=dict(date='2026-10-11',downloaded_resource_links=len(m['resources']),unique_downloaded_pdfs=len({i['sha256'] for i in m['resources']}),downloaded_unique_pages=sum(i['pages'] for i in m['resources'] if 'duplicate_of' not in i),retained_pdfs=len(ret),retained_pdf_pages=sum(i['pages'] for i in ret),withheld_pdfs=sum(i['license_review']=='withheld_textbook_derived_content' and 'duplicate_of' not in i for i in m['resources']),courses={c:dict(pdf_count=sum(i['course']==c for i in ret),pdf_pages=sum(i['pages'] for i in ret if i['course']==c)) for c in ['8.04','8.05','8.06']},verification='PDF magic, PyMuPDF all-page opening, page count, SHA256 and size verified; no substitute course URL indexes.',rights_hold_publication=False)
(ROOT/'subjects/quantum-mechanics/qa/source-verification.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps(q,ensure_ascii=False))
