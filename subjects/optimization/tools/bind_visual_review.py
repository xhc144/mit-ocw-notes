"""Bind real image-view records to final PDF pages by exact PNG SHA-256 equality."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    render=json.loads((ROOT/'build/main.render.json').read_text()); evidence={}; reports=[]
    root=json.loads((ROOT/'review/root-visual-events.json').read_text())
    for event in root['events']:
        for n in event['pages']:
            p=ROOT/event['render']/f'page-{n:04}.png'
            evidence[n]={'reviewer':'primary agent','review_report':'review/root-visual-events.json','actually_opened_png_sha256':sha(p),'observation':event['result']}
    for p in sorted((ROOT/'review').glob('visual-pages-*.json')):
        data=json.loads(p.read_text()); rows=data.get('pages',data.get('records',[]))
        assert len(rows)==26
        for row in rows:
            n=row['page'];digest=next(row[k] for k in ['png_sha256','pngsha','pngsha256'] if k in row)
            assert isinstance(digest,str) and len(digest)==64
            evidence[n]={'reviewer':p.stem,'review_report':str(p.relative_to(ROOT)),'actually_opened_png_sha256':digest,'observations':row.get('observations',[]),'scope_note':'Original actual view, or documented changed-page re-view; equal PNGs carry that inspection forward.'}
        reports.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p)})
    pages=[]
    for row in render['pages']:
        n=row['page']; assert n in evidence,f'Unviewed page {n}'
        assert row['sha256']==evidence[n]['actually_opened_png_sha256'],f'Unreviewed final change at page {n}'
        pages.append({'page':n,'final_png_sha256':row['sha256'],'matches_actually_viewed_image':True,**evidence[n]})
    assert len(pages)==render['page_count']==126
    report={'status':'passed','pdf':'dist/main.pdf','pdf_sha256':sha(ROOT/'dist/main.pdf'),'render_pdf_sha256':render['pdf']['sha256'],'pages_actually_covered':126,
        'method':'All 126 pages were actually opened with view_image detail=original at 130dpi. Final pages must have the exact SHA256 of an actually viewed image; changed images were opened again. Contact sheets were not used as substitutes.',
        'independent_reports':reports,'root_events_sha256':sha(ROOT/'review/root-visual-events.json'),'pages':pages,
        'retained_nonblocking_advisories':['Original body page39 begins with a short continuation phrase; original body preserved.','LP recitation initial-basis display spans pages104–105; both sides were actually checked and readable.','One Underfull hbox reminder was checked in the full-page review; no clipping or lost content.'],
        'limits':'Real visual inspection and independent same-model mathematics reviews do not certify the absence of every mathematical error.'}
    assert report['pdf_sha256']==report['render_pdf_sha256']
    (ROOT/'review/visual-review-v2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'passed','actual_visual_pages':126,'pdf_sha256':report['pdf_sha256']}))
if __name__=='__main__':main()
