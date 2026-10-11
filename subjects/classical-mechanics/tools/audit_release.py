#!/usr/bin/env python3
"""Verify packaged OCW originals and the Chinese PDF's actual navigation."""
from pathlib import Path
import json,hashlib
import fitz
SUBJECT=Path(__file__).resolve().parents[1]
REPO=SUBJECT.parents[1]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 manifest=json.loads((REPO/'manifests/classical-mechanics-sources.json').read_text());source_checks=[]
 for r in manifest['resources']:
  if not r.get('packaged') or not r.get('pdf_validated'):continue
  p=REPO/r['path'];doc=fitz.open(p)
  check={'path':r['path'],'sha256_matches':sha(p)==r['sha256'],'bytes_match':p.stat().st_size==r['bytes'],'pages_match':len(doc)==r['pages'],'pages':len(doc)}
  assert all(check[k] for k in ['sha256_matches','bytes_match','pages_match']);source_checks.append(check)
 packaged=list((REPO/'sources/classical-mechanics').rglob('*.pdf'))
 assert {p.relative_to(REPO).as_posix() for p in packaged}=={r['path'] for r in source_checks}
 pdf=SUBJECT/'classical-mechanics-zh.pdf';doc=fitz.open(pdf);bad=[];links=0;toc=doc.get_toc(simple=False);title_checks=[]
 norm=lambda t:''.join(t.split())
 for level,title,page,dest in toc:
  if not 1<=page<=len(doc):bad.append(['bookmark',title,page]);continue
  # A target page may start before its heading, but must contain that exact heading.
  clean=title.lstrip('0123456789. ');ok=norm(clean) in norm(doc[page-1].get_text());title_checks.append({'title':title,'page':page,'target_page_contains_title':ok})
  if not ok:bad.append(['bookmark title mismatch',title,page])
 external=[];named_checks=[];names=doc.resolve_names()
 for i,p in enumerate(doc):
  for l in p.get_links():
   if l['kind']==fitz.LINK_NAMED and l.get('nameddest'):
    name=l['nameddest'];pageidx,x,y=doc.resolve_link('#'+name);links+=1
    good=name in names and 0<=pageidx<len(doc) and doc[pageidx].rect.contains(fitz.Point(x,y))
    named_checks.append({'source_page':i+1,'name':name,'resolved_page':pageidx+1,'resolved_point':[x,y],'valid':good})
    if not good:bad.append(['named link',i+1,name])
   elif l['kind']==fitz.LINK_GOTO:
    links+=1
    if not 0<=l.get('page',-1)<len(doc):bad.append(['link',i+1,l])
    point=l.get('to')
    if point is not None and not doc[l['page']].rect.contains(point):bad.append(['link point outside page',i+1,str(point)])
   elif l['kind']==fitz.LINK_URI:external.append(l['uri'])
 fonts={}
 for p in doc:
  for f in p.get_fonts(full=True):
   if f[0] not in fonts:
    info=doc.extract_font(f[0]);fonts[f[0]]={'name':f[3],'type':f[2],'embedded_bytes':len(info[3])}
 assert not bad,bad
 assert all(f['embedded_bytes']>0 for f in fonts.values())
 result={'pdf':pdf.name,'pdf_sha256':sha(pdf),'pages':len(doc),'actual_bookmarks':len(toc),'validated_internal_links':links,'bookmark_targets':title_checks,'external_links':sorted(set(external)),'named_link_checks':named_checks,'navigation_errors':bad,'fonts':list(fonts.values()),'packaged_original_pdf_files':len(source_checks),'packaged_original_pages':sum(c['pages'] for c in source_checks),'packaged_original_checks':source_checks,'scope':'Hash/page/navigation/font checks; mathematical and visual review are separate reports.'}
 (SUBJECT/'qa/release-evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['pages','actual_bookmarks','validated_internal_links','packaged_original_pdf_files','packaged_original_pages','pdf_sha256']},indent=2))
if __name__=='__main__':main()
