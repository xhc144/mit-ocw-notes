#!/usr/bin/env python3
"""Check final native Chinese PDF, destinations, source hashes and style lock."""
import argparse, hashlib, json, re, unicodedata
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def fold(s): return re.sub(r'\s+','',unicodedata.normalize('NFKC',s))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pdf',type=Path,default=ROOT/'dist/main.pdf')
    p.add_argument('--out',type=Path,default=ROOT/'qa/final-checks.json')
    args=p.parse_args()
    doc=fitz.open(args.pdf); names=doc.resolve_names(); toc=doc.get_toc(simple=False)
    assert len(doc)==56 and len(toc)==115
    internal=[];external=[]
    for index,page in enumerate(doc):
        assert abs(page.rect.width-612)<.1 and abs(page.rect.height-792)<.1
        assert re.search(r'[\u4e00-\u9fff]',page.get_text()), index+1
        assert not page.get_images(), 'No English original-page bitmap is allowed'
        for link in page.get_links():
            if link['kind']==fitz.LINK_URI:
                assert link.get('uri','').startswith('https://')
                external.append({'source_page':index+1,'url':link['uri']})
            else:
                assert link['kind'] in [fitz.LINK_GOTO,fitz.LINK_NAMED]
                dst=names[link['nameddest']] if link.get('nameddest') else link
                assert 0<=dst['page']<len(doc)
                internal.append({'source_page':index+1,'target_page':dst['page']+1,'destination':link.get('nameddest')})
    bookmarks=[]
    for level,title,page,destination in toc:
        assert 1<=page<=len(doc)
        assert fold(title) in fold(doc[page-1].get_text()),(title,page)
        dst=names[destination['nameddest']]
        assert dst['page']+1==page
        bookmarks.append({'level':level,'title':title,'physical_page':page,'destination':destination['nameddest']})
    maintext=(ROOT/'main.tex').read_text();baseline=(ROOT/'qa/style-baseline.tex').read_text()
    def locked(s):return s[s.index('% WZ-LOCKED-CLASS-BEGIN'):s.index('% WZ-LOCKED-CLASS-END')+len('% WZ-LOCKED-CLASS-END')]
    assert locked(maintext)==locked(baseline)
    report=json.loads((ROOT/'qa/typesetting/validation_report.json').read_text())
    assert report['automated_status']=='PASS' and not report['errors']
    for item in report['sources']: assert sha(ROOT/item['path'])==item['sha256']
    render=json.loads((ROOT/'qa/typesetting/main.render.json').read_text())
    assert sha(args.pdf)==render['pdf']['sha256']
    groups={'classical-review.md':range(1,8),'polynomial-algorithm-review.md':range(8,13),
            'matrix-electric-review.md':[13,14],'spectral-extremal-review.md':[15,16],
            'ramsey-poset-review.md':[17]}
    for name,chapters in groups.items():
        text=(ROOT/'qa'/name).read_text()
        for n in chapters: assert sha(ROOT/f'chapters/ch{n:02}.tex') in text,(name,n)
    body='\n'.join((ROOT/f'chapters/ch{n:02}.tex').read_text() for n in range(1,18))
    assert not re.search(r'\\(?:includegraphics|includepdf|pdfximage)',body+maintext)
    assert '边染色' in body and '匹配' in body
    counts={env:len(re.findall(r'\\begin\{'+env+r'\}',body)) for env in ['theorem','lemma','proposition','corollary','definition','proof','example','exercise','solution','tikzpicture']}
    out={'status':'passed','pdf':{'path':'dist/main.pdf','sha256':sha(args.pdf),'bytes':args.pdf.stat().st_size,
                                'physical_pages':len(doc),'front_pages':5,'main_and_references_pages':51,
                                'embedded_raster_images':0,'all_pages_have_native_chinese_text':True},
         'style_locked_zone_sha256':hashlib.sha256(locked(maintext).encode()).hexdigest(),
         'style_matches_probability_locked_baseline':True,'final_automated_build':'PASS',
         'independent_math_qa_all_17_final_hashes_match':True,'counts':counts,
         'bookmark_count':len(bookmarks),'bookmarks_all_targets_have_matching_titles':True,
         'bookmarks':bookmarks,'internal_links':internal,'external_links':external,
         'limitations':'机械核验不替代一般数学证明、实际逐页视觉或人类专家校样；外部URL未在这里逐一请求。'}
    args.out.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(f'PASS: {len(doc)} native Chinese pages, {len(bookmarks)} bookmark targets, {len(internal)} internal links, {len(external)} external links; 17 audited chapter hashes.')

if __name__=='__main__':main()
