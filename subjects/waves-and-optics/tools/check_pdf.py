#!/usr/bin/env python3
"""Resolve every contents/bookmark destination in the real compiled PDF."""
import argparse,collections,hashlib,json,pathlib,re
import fitz
def clean(s):return re.sub(r'\s+','',s)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('pdf',type=pathlib.Path);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args()
    d=fitz.open(a.pdf);names=d.resolve_names();bad=[];internal=[];external=[]
    for i,p in enumerate(d,1):
        for l in p.get_links():
            if l['kind'] in (fitz.LINK_NAMED,fitz.LINK_GOTO):
                destination=names.get(l.get('nameddest'),l);target=destination.get('page',-1)
                item={'from_page':i,'name':l.get('nameddest'),'to_page':target+1}
                internal.append(item)
                if not 0<=target<len(d):bad.append(item)
            elif l['kind']==fitz.LINK_URI:external.append({'from_page':i,'url':l.get('uri')})
            else:bad.append({'from_page':i,'unsupported_link_kind':l['kind']})
    bookmarks=[]
    for level,title,page,info in d.get_toc(simple=False):
        destination=names.get(info.get('nameddest'),info);target=destination.get('page',-1)
        heading_found=0<=target<len(d)and clean(title)in clean(d[target].get_text())
        b={'level':level,'title':title,'page':page,'resolved_page':target+1,'title_found_on_destination_page':heading_found}
        bookmarks.append(b)
        if target+1!=page or not heading_found:bad.append(b)
    record={'date':'2026-10-11','pdf_sha256':hashlib.sha256(a.pdf.read_bytes()).hexdigest(),'pages':len(d),'internal_links':len(internal),'external_links':len(external),'bookmarks':len(bookmarks),'internal_link_details':internal,'bookmark_details':bookmarks,'issues':bad,'status':'PASS'if not bad else'FAIL','limitation':'Resolved destinations and matching page text checked; external links recorded, no promise of permanent external availability. Visual review separate.'}
    a.out.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n');print(record['status'],len(d),'pages',len(internal),'internal links',len(bookmarks),'bookmarks',len(bad),'issues')
    if bad:raise SystemExit(1)
if __name__=='__main__':main()
