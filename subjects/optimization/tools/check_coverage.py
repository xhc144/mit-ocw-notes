"""Check frozen problem inventory against complete, labeled exercise/solution pairs."""
from pathlib import Path
import re,json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    inventory=json.loads((ROOT/'assessment-coverage.json').read_text())
    problems=inventory['problems']; errors=[];found={};refs=[]
    for p in (ROOT/'assessments').glob('*.tex'):
        s=p.read_text(); pattern=r'\\begin\{exercise\}(.*?)\\end\{exercise\}\s*\\begin\{solution\}(.*?)\\end\{solution\}'
        matches=list(re.finditer(pattern,s,re.S))
        if len(matches)!=s.count('\\begin{exercise}'):errors.append(f'{p.name}: unpaired exercise/solution')
        for m in matches:
            labels=re.findall(r'\\label\{(ass:[^}]+)\}',m.group(1))
            if len(labels)!=1:errors.append(f'{p.name}: exercise needs one inventory label')
            for label in labels:
                if label in found:errors.append('Duplicate problem label '+label)
                found[label]={'file':str(p.relative_to(ROOT)),'statement_chars':len(m.group(1).strip()),'solution_chars':len(m.group(2).strip())}
                if len(m.group(2).strip())<40:errors.append('Empty/truncated solution '+label)
    expected={a['label'] for a in problems}
    if len(expected)!=len(problems):errors.append('Repeated frozen problem labels')
    errors+=['Missing '+x for x in sorted(expected-set(found))]+['Extra '+x for x in sorted(set(found)-expected)]
    main=(ROOT/'main.tex').read_text(); files=[ROOT/'main.tex']+[ROOT/(n+'.tex' if not n.endswith('.tex') else n) for n in re.findall(r'\\input\{([^}]+)\}',main)]
    text='\n'.join(p.read_text() for p in files)
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    for label in set(labels):
        if labels.count(label)>1:errors.append('Repeated TeX label '+label)
    for label in re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}',text):
        if label not in labels:errors.append('Unresolved source reference '+label)
    source_records=json.loads((ROOT/'sources/assessment-resources.json').read_text())
    for r in source_records:
        p=ROOT/r['path']
        if p.exists() and sha(p)!=r['sha256']:errors.append('Source bytes changed '+r['path'])
    baseline='cb7e27ae7a1cff846ab46871d7ab81bdc59e8132'; body=[]
    for p in sorted((ROOT/'chapters').glob('*.tex')):
        rel='subjects/optimization/'+str(p.relative_to(ROOT))
        old=subprocess.check_output(['git','show',baseline+':'+rel],cwd=ROOT,text=True)
        new=p.read_text()
        for label in ['ex:lp-cycle','ex:conjugate-models']:
            new=new.replace('\\label{'+label+'}\n','')
        new=new.replace(r'b=2400\,\mathbf1',r'b=2400\mathbf1')
        match=old==new;body.append({'path':str(p.relative_to(ROOT)),'preserved_except_two_crossreference_labels_and_one_thin_space':match})
        if not match:errors.append('Original chapter changed unexpectedly '+str(p.relative_to(ROOT)))
    report={'status':'passed' if not errors else 'failed','major_problems':len(problems),'first_level_blocks':sum(a['first_level_count'] for a in problems),
            'problems':found,'errors':errors,'original_body_preservation':body,
            'inventory_sha256':sha(ROOT/'assessment-coverage.json'),
            'tex_hashes':{str(p.relative_to(ROOT)):sha(p) for p in files},
            'limits':'Checks labels, paired content, frozen inventory, sources and original body bytes; mathematical and transcription verification requires the separate independent reviews.'}
    (ROOT/'review/coverage-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:report[k] for k in ['status','major_problems','first_level_blocks','errors']},ensure_ascii=False))
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
