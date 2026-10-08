"""Bind the manually checked OCW question structure to actual source bytes."""
from pathlib import Path
import hashlib, json, re
import fitz

ROOT = Path(__file__).resolve().parents[3]
BOOK = ROOT / 'subjects/functional-analysis'
SRC = ROOT / 'sources/functional-analysis/18.102-spring-2021/assessments'
PARTS = {
 'ps01':['ab','','','ab','abc'], 'ps02':['ab','ab','','ab','abc'],
 'ps03':['ab','abc','','abc'], 'ps04':['','','ab'],
 'ps05':['ab','ab','abc','ab'], 'ps06':['ab','','abc',''],
 'ps07':['abcd','ab','','ab'], 'ps08':['ab','ab','abc','ab'],
 'ps09':['abc','ab','','ab','ab'], 'ps10':['abc','','','ab','abcde','abc'],
 'midterm':['','','ab','ab','ab'], 'final-assignment':['','','','ab','']}
LABEL = {'final-assignment':'final'}
REUSE = {
 'ps01:1':['lem:holder-seq'], 'ps01:2':['thm:lpseqbanach'],
 'ps01:3':['thm:lpseqbanach'], 'ps01:5':['thm:dual-lp'],
 'ps02:2':['thm:quotient'], 'ps02:3':['thm:series','thm:quotient'],
 'ps03:1':['legacy:ch03:example1'],
 'ps07:1':['legacy:ch05:exercise1','prop:lp-density'],
 'ps07:4':['prop:parallelogram'],
 'ps08:1':['thm:onb','legacy:ch06:exercise1'],
 'ps08:2':['cor:orthodecompose'], 'ps09:3':['legacy:ch07:exercise1'],
 'ps09:4':['thm:projection'], 'ps10:2':['thm:continuouskernelcompact'],
 'ps10:3':['thm:compact-approx'], 'ps10:4':['thm:compactnorm'],
 'midterm:3':['cor:stronglimit','legacy:ch04:exercise1'],
 'final:3':['ps08:2'], 'final:4':['legacy:ch10:exercise1'],
 'final:5':['legacy:ch11:example1']}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 manifest=json.loads((SRC/'manifest.json').read_text())
 frozen=[]; number=lettered=unsplit=units=pages=0
 for file in manifest['files']:
  key=file['id']; parts=PARTS[key]; text=(SRC/(key+'.txt')).read_text().split('MIT OpenCourseWare')[0]
  starts=list(re.finditer(r'(?m)^\s{0,8}([1-6])\.\s',text))
  assert [int(m.group(1)) for m in starts]==list(range(1,len(parts)+1))
  pdf=fitz.open(SRC/file['path']); scans=[]
  for idx,page in enumerate(pdf):
   raw=page.get_text()
   scans.append({'page':idx+1,'images':len(page.get_images()),
    'individual_rights_markers': re.findall(r'.{0,60}(?:copyright|used with permission|all rights reserved|courtesy|©).{0,80}',raw,re.I),
    'ocw_attribution_page':'MIT OpenCourseWare' in raw and 'Spring 2021' in raw})
  assert scans[-1]['ocw_attribution_page']
  q=[]
  label=LABEL.get(key,key)
  tex=BOOK/'chapters'/(key+'.tex')
  for i,(m,sub) in enumerate(zip(starts,parts),1):
   end=starts[i].start() if i<len(starts) else len(text)
   qid=f'{label}:{i}'
   assert '\\label{'+qid+'}' in tex.read_text()
   q.append({'original_number':i,'explicit_subparts':list(sub),
    'units':[f'{qid}({x})' for x in sub] if sub else [qid],
    'source_extracted_text':text[m.start():end].strip(),
    'source_text_limitations':'PDF text extraction drops some overbars and math layout; independently checked against original PDF.',
    'translation_label':qid,'translation_file':str(tex.relative_to(BOOK)),
    'reused_existing_results':REUSE.get(qid,[]),
    'all_original_targets_retained':True,
    'additional_targets': ['two separately evaluated integrals'] if qid=='final:2' else []})
  nletter=sum(map(len,parts)); nplain=sum(not x for x in parts); nunits=nletter+nplain
  number+=len(parts);lettered+=nletter;unsplit+=nplain;units+=nunits;pages+=file['pages']
  frozen.append({**file,'source_text_sha256':sha(SRC/(key+'.txt')),
    'translation_sha256':sha(tex),'problem_count':len(parts),
    'explicit_lettered_subparts':nletter,'unsplit_problems':nplain,'solution_units':nunits,
    'license':'CC BY-NC-SA 4.0 (OCW terms; no individual restriction found)',
    'rights_scan':scans,'questions':q})
 result={'schema_version':1,'course':'18.102/18.1021, Spring 2021',
  'instructor':'Casey Rodriguez','official_answers_available':False,
  'counting_rule':'One explicit lettered subpart or one original numbered problem without lettered subparts is one solution unit. Final problem 2 is one unit with two fully evaluated integrals.',
  'totals':{'files':len(frozen),'physical_pdf_pages':pages,'numbered_problems':number,
   'explicit_lettered_subparts':lettered,'unsplit_problems':unsplit,'solution_units':units},
  'files':frozen}
 assert (number,lettered,unsplit,units,pages)==(54,87,18,105,36)
 (BOOK/'assessment-inventory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 (SRC/'question-inventory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result['totals']))
if __name__=='__main__':main()
