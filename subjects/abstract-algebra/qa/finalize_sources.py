from pathlib import Path
import json,hashlib,fitz,zipfile,re
root=Path(__file__).resolve().parents[3];src=root/'sources/abstract-algebra';sub=root/'subjects/abstract-algebra'
primary=json.loads((src/'source-manifest.json').read_text());ass=json.loads((src/'assessment-manifest.json').read_text());records=[f for f in primary['files'] if f['id'].startswith(('18.703','RES.'))]+ass['files']
assert len(records)==41 and len({f['id'] for f in records})==41
for f in records:
 p=root/f['path']; assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
 f['license_url']='https://creativecommons.org/licenses/by-nc-sa/4.0/'
 f['terms_url']='https://ocw.mit.edu/pages/privacy-and-terms-of-use/'
 f['item_rights_review']='Official course/resource metadata, complete extracted PDF text or all TeX/text ZIP members inspected for copyright/permission/rights/courtesy markers; no separate restrictive item statement found. Book references recorded separately; no external textbook files acquired.'
 f['third_party_exceptions']=[]
 f['third_party_scope']='Herstein/Judson references in homework are attribution to external books, not blanket rights to the books. Reference-only text not reconstructed. Public mathematical conditions restated in Chinese; no external book images or pages reused.' if f['id'].startswith('hw') else 'No explicit item exception found; original images not reused in Chinese volume.'
 if f['id'].startswith('18.703') or f['id'].startswith(('hw','practice')):f['authors']=['James McKernan'];f['faculty_notes']=True
 elif f['id'].startswith('RES.18-011'):f['authors']=['Jakin Ng','Sanjana Das','Ethan Yang'];f['lecturer']='Davesh Maulik';f['faculty_checked']=False
 else:f['authors']=['Sanjana Das','Jakin Ng'];f['lecturer']='Roman Bezrukavnikov';f['note_supervisor']='Ashay Athalye';f['faculty_checked']=False
 f['review_status']='item metadata, actual pages, hashes, attribution and explicit rights markers verified'
 if p.suffix=='.pdf':
  d=fitz.open(p); assert len(d)==f['pages'];f['page_text_lengths']=[len(pg.get_text()) for pg in d]
 else:
  z=zipfile.ZipFile(p);f['zip_members']=[dict(path=n,bytes=z.getinfo(n).file_size,sha256=hashlib.sha256(z.read(n)).hexdigest()) for n in z.namelist() if not n.endswith('/')];f['executed_source_code']=False
 f['in_chinese_source_zip']=False
inventory=[]
for p in sorted(src.rglob('*')):
 if p.is_file() and p.name not in ['source-manifest.json','archive-inventory.json']:
  inventory.append(dict(path=str(p.relative_to(root)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
manifest=dict(access_date='2026-10-08',primary_course='18.703 Spring 2013',resource_count=len(records),pdf_count=sum((root/f['path']).suffix=='.pdf' for f in records),pdf_pages=sum(f['pages'] or 0 for f in records),notes_pages=489,assessment_pages=56,files=records,deduplication='23 primary notes have distinct SHA256. Full student PDFs selected once; their individual lecture PDFs were not separately archived. Official TeX packages retained as source format only, never included in Chinese source ZIP. HW5 Q9/Q11 book-only duplicate and HW5 Q12/Practice1 Q5 exact mathematical duplicate mapped in assessment-map.json.',metadata_pages=['syllabus','calendar','readings','assignments','exams'],license='CC BY-NC-SA 4.0 default with individual exceptions taking precedence',limitations='No permission inferred for external Herstein/Judson books. Instructor accuracy disclaimer preserved for both student-note resources. No guarantee that a marker scan detects unlabelled ownership; original figures not reused.')
(src/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));(sub/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(src/'archive-inventory.json').write_text(json.dumps(dict(files=inventory),ensure_ascii=False,indent=2))
print('sources',len(records),'PDFs',manifest['pdf_count'],'pages',manifest['pdf_pages'],'inventory',len(inventory))
