"""Merge the source-audited inventories and generate the linked book index."""
from pathlib import Path
from collections import OrderedDict
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
REPORTS=['convex-assessment-audit.json','lp-homework-audit.json','lp-recitation-audit.json']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def display_name(name):
    if m:=re.fullmatch(r'ps(\d)(?:-g(\d))?',name):
        return '作业'+m[1]+('（组'+m[2]+'）' if m[2] else '')
    if m:=re.fullmatch(r'recitation-(\d+)',name):return '习题课'+str(int(m[1]))
    if name=='midterm-2-practical-problem-set':return '期中2综合练习'
    if m:=re.fullmatch(r'Homework (\d) \(Spring (\d+)\)',name):return '作业'+m[1]+'（'+m[2]+'春季）'
    if m:=re.fullmatch(r'Midterm \(Spring (\d+)\)',name):return '期中考试（'+m[1]+'春季）'
    return name
def main():
    problems=[]; audits=[]
    for name in REPORTS:
        p=ROOT/'review'/name; d=json.loads(p.read_text())
        rows=d['problems']; problems.extend(rows)
        audits.append({'path':'review/'+name,'sha256':sha(p),'main_problems':len(rows),'first_level_blocks':sum(x['first_level_count'] for x in rows)})
    assert len(problems)==97 and len({x['label'] for x in problems})==97
    assert sum(x['first_level_count'] for x in problems)==308
    for p in problems:
        assert p['source_file'] and p['source_pages'] and p['answer_provenance']
        assert p['first_level_count']==len(p['first_level_subquestions'])
    report={'schema_version':2,'baseline_commit':'cb7e27ae7a1cff846ab46871d7ab81bdc59e8132',
        'main_problems':97,'first_level_blocks':308,
        'count_rule':'Original Problem/Question; first numbered response layer only. Deeper semantic tasks retained in each source audit.',
        'original_body':'13 chapters preserved except two crossreference labels and one thin space between a coefficient and the all-ones vector',
        'source_audits':audits,'problems':problems,
        'known_source_gaps':['15.053 actual midterm and quiz papers absent in checked official inventory','Rec10 deleted copyright images not restored','External textbook narrative excluded; mathematical data and tasks restated'],
        'verification_limits':'Inventory/paired-source checks require independent mathematical and transcription reviews; those reports and PDF visual review are separate.'}
    (ROOT/'assessment-coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    # The displayed numbers are this book's exercise numbers; every frozen main problem has its own clickable link.
    groups=OrderedDict()
    for p in problems:groups.setdefault((p['course'],p['collection']),[]).append(p)
    lines=[r'\originalsection{逐题内链索引}',r'各组下列编号为本册习题编号, 点击可回到题面; 原题号、重复编号及组别在相应题面保留. 原文件页码和第一层子问见逐题电子清单.']
    for (course,name),rows in groups.items():
        name=display_name(str(name)).replace('&',r'\&').replace('_',r'\_').replace('%',r'\%')
        links='、'.join(r'\ref{'+p['label']+'}' for p in rows)
        lines.append(r'\noindent\textbf{'+course+' '+name+r'}：'+links+r'.\par')
    p=ROOT/'assessments/source-map.tex'; s=p.read_text().split('% GENERATED-PROBLEM-INDEX')[0].rstrip()
    p.write_text(s+'\n\n% GENERATED-PROBLEM-INDEX\n'+'\n'.join(lines)+'\n')
    print(json.dumps({'main_problems':97,'first_level_blocks':308,'groups':len(groups),'inventory_sha256':sha(ROOT/'assessment-coverage.json')}))
if __name__=='__main__':main()
