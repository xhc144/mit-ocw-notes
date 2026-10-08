#!/usr/bin/env python3
"""Freeze the authorised assessment selection without altering audit inventories."""
import hashlib
import json
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[3]
BOOK = ROOT / 'subjects/graph-theory'
SOURCES = ROOT / 'sources/graph-theory/assessments'

def read(course):
    p = BOOK / f'qa/assessments-inventory-{course}.json'
    return json.loads(p.read_text()), {'path': str(p.relative_to(ROOT)),
        'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

def main():
    inventories, evidence = {}, []
    for course in ('18315', '18433', '18212', '18217', '6042'):
        inventories[course], ref = read(course)
        evidence.append(ref)
    groups = []
    primary = json.loads((BOOK / 'qa/assessments-selection-18315.json').read_text())
    selected_primary = {q['id'] for q in inventories['18315']['top_level_questions']
        if q['category'] == 'graph_relevant'} | {'18315-HW3-Q5'}
    rows = []
    for q in inventories['18315']['top_level_questions']:
        if q['id'] in selected_primary:
            rows.append({'id': q['id'], 'original_leaf_ids': q['printed_leaf_ids'],
                'official_solution_status': 'no_public_official_solution',
                'source_pages': q['physical_pages'], 'topic_zh': q['topic_summary_zh']})
    assert len(rows) == 20 and sum(len(q['original_leaf_ids']) for q in rows) == 36
    groups.append({'course': '18.315', 'question_occurrences': rows,
        'external_statement_missing': inventories['18315']['external_references'],
        'boundary_zh': '19道图论题加HW3题5路径多面体三小问；不复制只列书号的缺失题面。'})
    rows = []
    for a in inventories['18433']['assignments']:
        for q in a['questions']:
            if q['id'] in inventories['18433']['proposed_graph_scope']['related_top_level_ids']:
                rows.append({'id': q['id'], 'original_leaf_ids': q['leaf_ids'],
                    'official_solution_status': q['official_solution_status'],
                    'source_pages': q['pdf_pages'], 'topic_zh': q['topic_zh']})
    assert len(rows) == 15 and sum(len(q['original_leaf_ids']) for q in rows) == 25
    groups.append({'course': '18.433', 'question_occurrences': rows,
        'boundary_zh': 'A1全7题、A2全5题、A3题6、A4题2至3；非图论的其余优化题不编入。'})
    rows = []
    for q in inventories['18212']['problems']:
        if q['recommended_for_graph_freeze']:
            leaves = [q['id'] + '-' + p.strip('()') for p in q['original_explicit_subpart_labels']] or [q['id']]
            rows.append({'id': q['id'], 'original_leaf_ids': leaves,
                'official_solution_status': q['official_solution_status'],
                'official_solution_resources': q['official_solution_resources'],
                'source_pages': q['source_pdf_pages'], 'topic_zh': q['summary_zh'],
                'editorial_count_note': q['editorial_subpart_note']})
    assert len(rows) == 19 and sum(len(q['original_leaf_ids']) for q in rows) == 19
    groups.append({'course': '18.212', 'question_occurrences': rows,
        'boundary_zh': '图、树、偏序、Dyck路径与停车函数19题；两条未编号Abel恒等式仍是原题Q4的一个印刷叶题。'})
    selected = {'A1','A3','B17','B18'} | {f'B{i}' for i in range(1,13)} | {f'D{i}' for i in range(1,8)}
    rows = []
    for q in inventories['18217']['questions']:
        if q['number'] in selected:
            tasks = [t for t in q['task_units'] if not(q['number']=='A3' and t.get('part')=='c')]
            rows.append({'id': q['stable_id'], 'number': q['number'],
                'original_leaf_ids': [t['stable_id'] for t in tasks],
                'task_units': tasks, 'source_pages': q['physical_pdf_pages'],
                'official_solution_status': q['official_solution_status'], 'topic_zh': q['topic_zh']})
    assert len(rows) == 23 and sum(len(q['original_leaf_ids']) for q in rows) == 29
    groups.append({'course': '18.217', 'question_occurrences': rows,
        'boundary_zh': 'A1、A3(a,b,d)、B1至12、B17至18、D1至7；A3(d)原标不提交，仍作为明确选取的补充。A3(c)及其余图论研究专题未采用，加法组合不在范围。'})
    rows, aliases = [], []
    for f in inventories['6042']['pdf_files']:
        for q in f['questions']:
            if q['scope'] != 'graph-theory':
                continue
            ident = f['filename'].removesuffix('.pdf') + '-Q' + q['id']
            if f['filename'] == 'MIT6_042JS15_cp32.pdf':
                aliases.append({'original_id': ident,
                    'canonical_original_id': ident.replace('cp32','cp19'),
                    'reason': '正文内容重复，保留原卷映射，不重计新的题目'})
                continue
            first_level = [ident + p for p in q['explicit_top_level_subquestion_labels']] or [ident]
            assert len(first_level) == q['top_level_answer_unit_count']
            leaves = first_level[:]
            nested=[]
            if f['filename']=='MIT6_042JS15_cp17.pdf' and q['id']=='4':
                parent=ident+'f'
                children=[parent+'('+r+')' for r in ['i','ii','iii']]
                leaves=[leaf for leaf in leaves if leaf!=parent]+children
                nested=[{'parent_first_level_id':parent,'printed_children':children,
                    'policy':'原卷f的三条罗马编号为嵌套小问，替换父任务计末端；不是多选选项或图标签。'}]
            rows.append({'id': ident, 'original_leaf_ids': leaves,
                'original_first_level_ids':first_level,'nested_printed_subquestions':nested,
                'official_solution_status': f['official_solution_status'],
                'source_pages': [q['physical_start_page']], 'topic_zh': q['topic_zh'],
                'source_file': f['local_path'], 'pdf_url': f['official_public_pdf_url']})
    assert len(rows) == 50 and len(aliases) == 5
    online = inventories['6042']['online_feedback_inventory']['selected_graph_pages']
    assert len(online) == 36 and sum(len(p['Q_ids']) for p in online) == 75
    groups.append({'course': '6.042J', 'question_occurrences': rows,
        'content_duplicate_aliases': aliases, 'selected_online_feedback_pages': online,
        'boundary_zh': '50个PDF原题位置与36个在线页的75个回答单元；CP32五题与CP19内容相同，仅留别名。同题在作业、课堂、考试或在线出现时保留来源位置；正文可以合并并交叉引用完整解答。'})
    selection = {'schema_version': 1, 'frozen_on': '2026-10-08',
        'status': 'source_and_question_selection_frozen_before_final_build',
        'inventories_sha256': evidence, 'courses': groups,
        'selected_pdf_question_occurrences': sum(len(g['question_occurrences']) for g in groups),
        'selected_pdf_printed_leaf_units': sum(len(q['original_leaf_ids']) for g in groups for q in g['question_occurrences']),
        'selected_pdf_first_level_answer_units':256,
        'selected_online_pages': 36, 'selected_online_answer_units': 75,
        'counting_zh': '127大题、256一级回答单元；6.042 CP17题4(f)有(i)至(iii)三个嵌套小问，替换一级父项后末端印刷小问共258（6.042为149而非一级147）。大题/末端小问是原题位置数，不是去重后的数学命题数；不拆未编号要求，不把填空项目、答案、选项或图标签再计为题。跨来源同题的正文合并映射在逐题完成清单中登记。',
        'solution_policy_zh': '同一主PDF完整中文题面和解答；逐题区分官方参考、原题订正与编者独立推导；原English PDF仅放sources，ZIP不含它们。'}
    resources = []
    for c in inventories:
        d = inventories[c]
        if c=='18315': rs=d['resources']
        elif c=='18433': rs=d['assignments']
        elif c=='18212': rs=d['resources']
        elif c=='18217': rs=d['source_files']
        else: rs=d['pdf_files']
        for r in rs:
            raw = r.get('source_pdf') or r.get('path') or r.get('local_path') or r.get('source_file',{}).get('path')
            p = ROOT/raw
            pdf = fitz.open(p)
            sha = hashlib.sha256(p.read_bytes()).hexdigest()
            recorded = r.get('sha256') or r.get('source_file',{}).get('sha256')
            assert sha == recorded, raw
            resources.append({'course':c, 'path':raw, 'pages':len(pdf),
                'bytes':p.stat().st_size, 'sha256':sha, 'pdf_metadata':pdf.metadata,
                'per_file_source_record':r})
    assert len(resources)==77 and sum(r['pages'] for r in resources)==278
    manifest={'schema_version':1, 'frozen_on':'2026-10-08',
        'pdf_files':77,'pdf_pages':278,'pdf_resources':resources,
        'inventories_sha256':evidence,
        'deduplication':{'18212':inventories['18212']['content_deduplication'],
            '6042':inventories['6042']['content_deduplication']},
        'archive_coverage_zh':'新增PDF77文件278物理页；其中18.212五份讨论讲义与五份答案内容对应，分别登记文件但不重复计题。18.433其余讲义只索引，未下载入此新增PDF计数。171在线HTML页均保存，冻结选用36页75单元。旧主源34文件1062页保持不变，共111个归档PDF、1340物理页。这个数字不是正文覆盖页数，也不宣称所有课程资源全文重编。'}
    for name, data in [('assessment-selection.json',selection),('assessment-source-manifest.json',manifest)]:
        body=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
        (BOOK/name).write_text(body)
        (ROOT/'sources/graph-theory'/name).write_text(body)
    print(json.dumps({'selected_questions':selection['selected_pdf_question_occurrences'],
        'printed_leaves':selection['selected_pdf_printed_leaf_units'],
        'online_answers':75,'new_source_pdfs':77,'new_source_pages':278}))

if __name__ == '__main__':
    main()
