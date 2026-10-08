#!/usr/bin/env python3
"""Finalize the reviewed official source inventory; no remote writes."""
from pathlib import Path
import json,re,shutil,hashlib,fitz
ROOT=Path(__file__).resolve().parents[3]; S=ROOT/'sources/ordinary-differential-equations'; Q=ROOT/'subjects/ordinary-differential-equations/review'
x=json.loads((Q/'source-investigation.json').read_text());entries=[]
notes={'g':'Graphical and Numerical Methods','c':'Complex Numbers','d':'Definite Integral Solutions','o':'Linear Differential Operators','s':'Stability','ir':'Input-Response Models','i':'Impulse Response and Convolution','lt':'Laplace Transform','ls1':'Review of Linear Algebra','ls2':'Homogeneous Linear Systems','ls3':'Complex and Repeated Eigenvalues','ls4':'Decoupling Systems','ls5':'Theory of Linear Systems','ls6':'Solution Matrices','gs':'Graphing ODE Systems','lc':'Limit Cycles'}
for a in x['sources']:
 e={k:v for k,v in a.items() if k not in ['temporary_original','text_sha256']}
 id=e['id'];text=Path('/tmp/ode-source-review/'+id+'.pdf');d=fitz.open(text)
 is_sn=bool(re.search(r'chapter_|appendix_|preface',id)); is_ex=bool(re.search(r'_\d(?:ex|sol)$|^section-3-solutions$',id))
 is_dynamics=e['course'].startswith('12-')
 flags=e['rights_review_lines'];restricted=is_dynamics and any(re.search(r'excluded|all rights reserved|used with permission',f,re.I) for f in flags)
 if id=='mit18_03s10_sup':
  e.update(document_authors=['Haynes R. Miller'],document_version='Spring 2010; cover copyright years 2004, 2006, 2008, 2010',title='18.03 Supplementary Notes')
 elif is_dynamics:
  txt=d[0].get_text();date=re.search(r'(?:September|October|November|December) \d{1,2}, 2022',txt)
  e.update(document_authors=['Daniel H. Rothman'],document_version=date.group() if date else 'Fall 2022 course version; exact document date not established',title=e['listed_label'].replace(' (PDF)',''))
 elif id=='mit18_03s10_reading_lec29':
  e.update(document_authors=['Jeremy Orloff'],document_version='Spring 2010 course version; original composition date not established',title='18.03 Difference Equations and Z-Transforms')
 elif is_sn:
  e.update(document_authors=['Haynes R. Miller'],document_version='Spring 2010 separately posted version; not necessarily identical to combined volume',title=re.sub(r'\s+',' ',d[0].get_text()[:170]).strip())
 elif re.match(r'mit18_03s10_c\d',id):
  date=re.search(r'(?:Feb|March|April|May)[a-z.]* \d{1,2}, 2010',d[0].get_text())
  e.update(document_authors=['Haynes Miller'],document_version=date.group() if date else 'Spring 2010 class-notes version',title=e['description'].strip())
 else:
  suffix=id.split('_')[-1];e.update(document_authors=['Arthur Mattuck'],author_evidence='Official readings index identifies Notes and Exercises as authored by Mattuck; embedded generic PDF metadata is not treated as author authority',document_version='Spring 2010 course posting; original composition date not established',title=notes.get(suffix,'Notes and Exercises: '+suffix))
 if restricted:
  e.update(archive_allowed=False,status='link-only-rights-exception',reuse='Mathematical concepts independently derived where used; third-party text/figures not copied',license='MIT OCW default CC BY-NC-SA 4.0 with explicit third-party exceptions; whole file withheld')
 elif is_ex:
  e.update(archive_allowed=False,status='link-only-outside-selected-scope',reuse='Exercise and solution collection not translated or archived in this book',license='Official default CC BY-NC-SA 4.0; scope exclusion is not a rights denial')
 elif is_sn and id not in ['mit18_03s10_chapter_1','mit18_03s10_preface']:
  e.update(archive_allowed=False,status='content-deduplicated',deduplicated_to='mit18_03s10_sup',deduplication='PDF section title, formulas and substantive text correspond to combined volume; separate OCW footer/layout retained only by official link, not claimed byte-identical',license='CC BY-NC-SA 4.0')
 else:
  dest=S/e['course']/(id+'.pdf');dest.parent.mkdir(exist_ok=True);shutil.copyfile(text,dest)
  e.update(archive_allowed=True,status='archived-verified',path=dest.relative_to(ROOT).as_posix(),license='CC BY-NC-SA 4.0',rights_verification='Official resource page CC license; full extracted-text rights scan reviewed; image-only Mattuck pages visually reviewed; no file-specific reservation found')
  if id in ['mit18_03s10_chapter_1','mit18_03s10_preface']:e['deduplication']='Distinct version relative to combined volume: added/revised substantive prose; independently retained'
 e['checked_on']='2026-10-08';e['license_url']='https://creativecommons.org/licenses/by-nc-sa/4.0/';e['terms_url']='https://ocw.mit.edu/pages/privacy-and-terms-of-use/'
 entries.append(e)
from collections import Counter
summary={'investigated_files':len(entries),'investigated_pdf_pages_including_duplicates':sum(e['pages'] for e in entries),'states':dict(Counter(e['status'] for e in entries)),'archived_files':sum(e['archive_allowed'] for e in entries),'archived_pages':sum(e['pages'] for e in entries if e['archive_allowed']),'archived_bytes':sum(e['bytes'] for e in entries if e['archive_allowed'])}
data={'schema_version':1,'checked_on':'2026-10-08','course_version_is_not_original_authorship_date':True,'scope':'36 classroom notes; Miller combined notes plus two distinct split versions; 16 Mattuck note files; Orloff supplement; all 16 dynamics files investigated, four permission-clear files archived, others link-only; 14 exercise/solution resources link-only outside scope','summary':summary,'sources':entries}
(S/'source-manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
shutil.copyfile(S/'source-manifest.json',ROOT/'subjects/ordinary-differential-equations/source-manifest.json')
for p in S.rglob('*'):
 if p.is_file() and (p.suffix=='.txt' or p.name.endswith('.resource.html')):p.unlink()
print(json.dumps(summary,ensure_ascii=False,indent=2))
