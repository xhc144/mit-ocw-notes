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
    assert len(doc)>100 and len(toc)>115
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
    assessment_groups={
        'assessments-review-18315-foundations.md':[f'assessments/18315/hw{n}.tex' for n in [1,2,3,4,7,8]],
        'assessments-review-18315-advanced.md':['assessments/18315/hw5.tex','assessments/18315/hw6.tex'],
        'assessments-review-18433.md':['assessments/18433/main.tex'],
        'assessments-review-18212.md':['assessments/18212/main.tex'],
        'assessments-review-18217.md':['assessments/18217/main.tex'],
        'assessments-review-6042.md':[p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'assessments/6042').glob('*.tex'))]}
    assessed=[]
    for review,files in assessment_groups.items():
        text=(ROOT/'qa'/review).read_text()
        for name in files:
            assert sha(ROOT/name) in text,(review,name)
            assessed.append({'path':name,'sha256':sha(ROOT/name),'independent_review':'qa/'+review})
    meta_review=(ROOT/'qa/course-metadata-review.md').read_text()
    for name in ['frontmatter/course-info.tex','frontmatter/supplementary-courses.tex']:
        assert sha(ROOT/name) in meta_review,name
    body='\n'.join((ROOT/f'chapters/ch{n:02}.tex').read_text() for n in range(1,18))
    body+='\n'+'\n'.join((ROOT/p['path']).read_text() for p in assessed)
    assert not re.search(r'\\(?:includegraphics|includepdf|pdfximage)',body+maintext)
    assert '边染色' in body and '匹配' in body
    counts={env:len(re.findall(r'\\begin\{'+env+r'\}',body)) for env in ['theorem','lemma','proposition','corollary','definition','proof','example','exercise','solution','tikzpicture']}
    first_chapter=next(page for level,title,page,_ in toc if title.startswith('1 ') or title.startswith('1\u2003') or ('图、度数' in title and level==1))
    selection=json.loads((ROOT/'assessment-selection.json').read_text())
    out={'status':'passed','pdf':{'path':'dist/main.pdf','sha256':sha(args.pdf),'bytes':args.pdf.stat().st_size,
                                'physical_pages':len(doc),'front_pages':first_chapter-1,'main_and_references_pages':len(doc)-first_chapter+1,
                                'embedded_raster_images':0,'all_pages_have_native_chinese_text':True},
         'style_locked_zone_sha256':hashlib.sha256(locked(maintext).encode()).hexdigest(),
         'style_matches_probability_locked_baseline':True,'final_automated_build':'PASS',
         'independent_math_qa_all_17_final_hashes_match':True,'counts':counts,
         'independent_assessment_reviews_all_final_hashes_match':True,'assessment_sources':assessed,
         'independent_course_metadata_review_final_hashes_match':True,
         'selected_pdf_question_occurrences':selection['selected_pdf_question_occurrences'],
         'selected_pdf_printed_leaf_units':selection['selected_pdf_printed_leaf_units'],
         'selected_online_answer_units':selection['selected_online_answer_units'],
         'bookmark_count':len(bookmarks),'bookmarks_all_targets_have_matching_titles':True,
         'bookmarks':bookmarks,'internal_links':internal,'external_links':external,
         'limitations':'机械核验不替代一般数学证明、实际逐页视觉或人类专家校样；外部URL未在这里逐一请求。'}
    args.out.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(f'PASS: {len(doc)} native Chinese pages, {len(bookmarks)} bookmark targets, {len(internal)} internal links, {len(external)} external links; 17 chapter and {len(assessed)} assessment source hashes independently audited.')

if __name__=='__main__':main()
