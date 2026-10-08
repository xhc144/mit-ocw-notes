"""Hand-audited leaves from actual MIT assessment sheets (not PDF counts)."""
import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[3];src=root/'sources/18.335j-spring-2019/assessments'
PS={1:{1:['reference'],2:['a','b'],3:['a','b','c'],4:['a','b','c']},2:{1:['a','b'],2:['a','b'],3:['whole'],4:['a','b','c']},3:{1:['a','b','c'],2:['a','b'],3:['a','b']},4:{1:['whole'],2:['a','b'],3:['reference'],4:['reference']}}
EX={19:{1:['whole'],2:['a','b'],3:['whole'],4:['whole']},8:{1:['a','b','c','d'],2:['whole'],3:['a','b','c','d'],4:['whole'],5:['whole'],6:['whole']},9:{1:['1','2'],2:['whole'],3:['whole']},10:{1:['a','b','c'],2:['a','b'],3:['a','b']},11:{1:['a','b'],2:['whole'],3:['a(i)','a(ii)','b'],4:['a','b','c']},12:{1:['a','b','c'],2:['a','b','c'],3:['whole']},13:{1:['a','b'],2:['a','b'],3:['a','b','c']},15:{1:['a','b(i)','b(ii)'],2:['a','b','c'],3:['a','b','c']}}
REF={(1,1,'reference'):'13.2',(2,1,'a'):'15.1',(2,1,'b'):'16.1',(2,2,'b'):'3.4',(2,4,'a'):'4.5',(2,4,'b'):'5.2',(2,4,'c'):'5.4',(3,1,'a'):'10.4',(3,1,'c'):'28.2',(4,3,'reference'):'27.5',(4,4,'reference'):'33.2'}
rows=[]
for typ,tables in [('pset',PS),('exam',EX)]:
 for year,qs in tables.items():
  sid=f'mit18_335js19_{typ}{year if typ=="pset" else f"{year:02d}"}';p=src/(sid+'.pdf')
  for q,leaves in qs.items():
   row={'id':f'{typ}{year:02d}-q{q}','source_id':sid,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'numbered_problem':q,'leaves_as_printed':leaves,'official_solution':typ=='pset' or year!=9,'solution_method':'official-solution translated and mathematically corrected' if typ=='pset' or year!=9 else 'AI-authored solution; no official answer exists','external_exercises':{leaf:REF[year,q,leaf] for leaf in leaves if typ=='pset' and (year,q,leaf) in REF}}
   row['original_problem_text_status']='MIT sheet complete' if not row['external_exercises'] else 'external textbook question omitted by MIT; original full text unavailable; reference preserved, MIT solution explained without inventing original question'
   rows.append(row)
summary={'top_level_homework_problems':15,'top_level_exam_problems':29,'exam_leaf_questions':60,'homework_leaf_slots_printed_on_MIT_sheets':29,'homework_external_textbook_exercise_slots':11,'homework_MIT_defined_leaf_questions':18,'excluded_from_math_problem_count':'2019 exam Problem 0 honor code, score headings, explanatory premises (2019 Q4 a/b), and hidden textbook subquestions','gaps':['11 textbook exercise slots cite Trefethen/Bau only; no original full question or hidden subquestion count is claimed.','2009 has no official answer: all 3 mathematical problems require explicitly AI-authored solutions.'],'items':rows}
(src/'question-inventory.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print({k:v for k,v in summary.items() if k!='items'})
