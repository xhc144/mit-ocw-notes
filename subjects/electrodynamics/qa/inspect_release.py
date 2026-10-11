#!/usr/bin/env python3
"""Check exact source hashes and actual PDF destinations; no mathematical certification."""
import json,hashlib,re,sys
from pathlib import Path
import fitz
root=Path(__file__).resolve().parents[1];repo=root.parents[1]
pdf=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root/'build/main.pdf'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((repo/'manifests/electrodynamics-sources.json').read_text());source_issues=[]
for f in m['files']:
 if f['archive_allowed']:
  p=repo/f['path'];d=fitz.open(p)
  if not p.read_bytes().startswith(b'%PDF-') or d.page_count!=f['pages'] or sha(p)!=f['sha256']:source_issues.append(f['id'])
d=fitz.open(pdf);issues=[];goto=uri=0;names=d.resolve_names();toc_links=0
for pi,p in enumerate(d):
 for k in p.get_links():
  if k['kind'] in (fitz.LINK_GOTO,fitz.LINK_NAMED):
   goto+=1
   if pi < d.get_toc()[0][2]-1:toc_links+=1
   if k.get('nameddest') and k['nameddest'] not in names:issues.append({'unresolved_named_destination':k['nameddest']})
   if not (0<=k['page']<len(d)):issues.append({'page':pi+1,'bad_destination':k})
   elif 'to' in k and not d[k['page']].rect.contains(k['to']):issues.append({'page':pi+1,'destination_outside_page':str(k['to'])})
  elif k['kind']==fitz.LINK_URI:uri+=1
  if not p.rect.contains(k['from']):issues.append({'page':pi+1,'link_outside_page':str(k['from'])})
clean=lambda s:re.sub(r'[\s:：\d.]+','',s)
for level,title,page in d.get_toc():
 if not 1<=page<=len(d) or clean(title) not in clean(d[page-1].get_text()):issues.append({'bookmark':title,'target_page':page,'title_not_found':True})
if toc_links!=len(d.get_toc()):issues.append({'toc_link_count':toc_links,'bookmark_count':len(d.get_toc())})
text='\n'.join(p.get_text() for p in d)
if '\ufffd' in text:issues.append({'replacement_character':True})
report={'date':'2026-10-11','pdf':str(pdf.relative_to(root)),'pdf_sha256':sha(pdf),'pages':len(d),'outlines':len(d.get_toc()),'internal_links':goto,'toc_links':toc_links,'resolved_named_destinations':len(names),'external_links':uri,'archive_files_checked':61,'archive_sha256_and_page_issues':source_issues,'pdf_issues':issues,'status':'PASS' if not issues and not source_issues else 'FAIL','limits':'URL targets are retained from checked OCW source metadata. PDF structural checks do not certify physics, pedagogy or visual layout.'}
(root/'qa/release-structure.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
assert report['status']=='PASS'
