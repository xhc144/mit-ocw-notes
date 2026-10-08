"""Check actual internal link destinations, page geometry and vector-only figures."""
from pathlib import Path
import hashlib,json,sys
import fitz
ROOT=Path(__file__).resolve().parents[1]
def main():
    path=ROOT/(sys.argv[1] if len(sys.argv)>1 else 'dist/main.pdf'); doc=fitz.open(path)
    errors=[]; links=[]; images=0
    for i,page in enumerate(doc):
        if (round(page.rect.width,2),round(page.rect.height,2))!=(612,792):errors.append(f'Page {i+1}: geometry')
        images+=len(page.get_images())
        for link in page.get_links():
            item={'source_page':i+1,'kind':link['kind']}
            if link['kind'] in [fitz.LINK_GOTO,fitz.LINK_NAMED]:
                dest=link.get('page',-1);item['destination_page']=dest+1;item['named_destination']=link.get('nameddest')
                if not 0<=dest<len(doc):errors.append(f'Page {i+1}: unresolved internal link {link}')
            elif link['kind']==fitz.LINK_URI:item['uri']=link['uri']
            else:errors.append(f'Page {i+1}: unexpected link action')
            links.append(item)
    toc=doc.get_toc()
    for level,name,page in toc:
        if not 1<=page<=len(doc):errors.append('Invalid outline '+name)
    report={'status':'passed' if not errors else 'failed','pdf':str(path.relative_to(ROOT)),
        'pdf_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pages':len(doc),'outlines':len(toc),
        'links':len(links),'raster_image_placements':images,'link_records':links,'errors':errors,
        'limits':'Checks embedded destinations and page size, not external website availability or mathematical correctness.'}
    (ROOT/'review/pdf-link-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','pages','outlines','links','raster_image_placements','errors']}))
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
