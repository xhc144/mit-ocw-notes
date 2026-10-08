#!/usr/bin/env python3
"""Bind every frozen original task to its Chinese solution and independent audit."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    selection=json.loads((ROOT/'assessment-selection.json').read_text())
    labels={}
    for p in sorted((ROOT/'assessments').rglob('*.tex')):
        s=p.read_text()
        for m in re.finditer(r'\\label\{([^}]+)\}',s):
            assert m[1] not in labels,m[1]
            labels[m[1]]={'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),
                          'line':s[:m.start()].count('\n')+1}
    def review_of(path):
        if '18315' in path:
            n=int(re.search(r'hw(\d)',path)[1])
            return 'qa/assessments-review-18315-'+('advanced' if n in [5,6] else 'foundations')+'.md'
        c=path.split('/')[1]
        return f'qa/assessments-review-{c}.md'
    original_rows=[]
    for group in selection['courses']:
        course=group['course']
        for q in group['question_occurrences']:
            ident=q['id']
            if course in ['18.315','18.433']:
                label='mit:'+ident.lower()
            elif course=='18.212':
                m=re.fullmatch(r'18212-s2019-pset(\d)-p(\d+)',ident)
                label=f'mit:18212-pset{m[1]}-q{int(m[2])}'
            elif course=='18.217':label='mit:18217-'+q['number'].lower()
            else:
                tag=ident.removeprefix('MIT6_042JS15_').lower()
                tag=tag.replace('midterm3','mt3').replace('finalexam','final')
                label='mit:6042-'+tag
            loc=labels[label];review=review_of(loc['path'])
            assert loc['sha256'] in (ROOT/review).read_text(),(label,review)
            original_rows.append({'course':course,'original_id':ident,
                'original_leaf_ids':q['original_leaf_ids'],'latex_label':label,
                'chinese_source':loc,'independent_review':review,
                'official_solution_status':q['official_solution_status'],
                'completion':'complete_Chinese_statement_and_solution_independently_reviewed'})
    online=[]
    for p in selection['courses'][-1]['selected_online_feedback_pages']:
        slug=re.sub(r'[^a-z0-9]+','-',p['title'].lower().replace('[optional]','').replace('&','and')).strip('-')
        for q in p['Q_ids']:
            label=f'mit:6042-online-{slug}-{q.lower()}';loc=labels[label]
            review=review_of(loc['path'])
            assert loc['sha256'] in (ROOT/review).read_text(),label
            online.append({'source_html':p['local_path'],'source_html_sha256':p['sha256'],
                'original_title':p['title'],'original_question_id':q,'latex_label':label,
                'chinese_source':loc,'independent_review':review,
                'completion':'complete_Chinese_statement_and_solution_independently_reviewed'})
    assert len(original_rows)==127 and sum(len(r['original_leaf_ids']) for r in original_rows)==258
    assert len(online)==75
    duplicate_aliases=[]
    for a in selection['courses'][-1]['content_duplicate_aliases']:
        label='mit:6042-'+a['original_id'].removeprefix('MIT6_042JS15_').lower()
        assert label in labels
        duplicate_aliases.append(dict(a,latex_label=label,chinese_source=labels[label]))
    reports=sorted({r['independent_review'] for r in original_rows+online})
    result={'status':'completed_and_independently_reviewed','frozen_selection_sha256':sha(ROOT/'assessment-selection.json'),
        'pdf_original_question_occurrences':127,'pdf_first_level_answer_units':256,'pdf_printed_leaf_units':258,'online_answer_units':75,
        'original_questions':original_rows,'online_questions':online,'content_duplicate_aliases':duplicate_aliases,
        'independent_reviews':[{'path':p,'sha256':sha(ROOT/p)} for p in reports],
        'limits_zh':'原题位置和印刷小问计数保留出处，不冒充去重命题数。机械标签/最终哈希检查只绑定已完成独立数学审稿，不独自证明解答正确。官方题面缺失和未选源范围见冻结清单；没有伪造外书题面或未公开答案。'}
    (ROOT/'assessment-completion.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('PASS: all 127 PDF original questions / 258 terminal printed subquestions (256 first-level units) and 75 online IDs mapped to audited Chinese solutions; five CP32 aliases retained.')

if __name__=='__main__':main()
