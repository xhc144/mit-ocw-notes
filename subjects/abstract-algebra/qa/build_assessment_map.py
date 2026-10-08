import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[3];out=root/'subjects/abstract-algebra'
complete={1:{},2:{1:2,3:1,6:1},3:{1:3,5:1,6:1},4:{2:1,5:3},5:{3:2,10:1,12:1,13:1,14:1},6:{1:1,6:1,8:1,9:1,10:1,11:1,12:2,13:1},7:{9:1},8:{3:3,5:2,10:3},9:{1:1,2:2,3:1,4:1,5:2,6:3,7:1,8:1,9:3,10:2,11:1,12:1},10:{3:1,7:1},11:{5:2,6:1,7:1,8:2,9:4,10:1}}
counts=[11,14,7,11,14,13,13,13,12,8,10]
# Exact book-only locators transcribed from the public homework PDFs.
missing={
1:{1:'H 1 §2 #1',2:'H 1 §2 #2',3:'J 3 #5',4:'J 3 #10',5:'H 2 §1 #21',6:'H 2 §1 #28',7:'H 2 §1 #29',8:'H 2 §1 #30',9:'H 2 §1 #31',10:'J 3 #48',11:'J 3 #49'},
2:{2:'H 2 §4 #1(b)',4:'H 2 §4 #13',5:'H 2 §4 #14',7:'H 2 §4 #16',8:'H 2 §4 #24',9:'H 2 §4 #26',10:'H 2 §4 #27',11:'H 2 §4 #36',12:'H 2 §4 #37',13:'H 2 §4 #38',14:'J 3 #50'},
3:{2:'H 3 §2 #1',3:'H 3 §2 #2',4:'H 3 §2 #3(a,f)',7:'H 3 §2 #17'},
4:{1:'H 2 §5 #1',3:'H 2 §5 #12',4:'H 2 §5 #17',6:'H 2 §5 #26',7:'H 2 §5 #27',8:'H 2 §5 #37',9:'H 2 §5 #43',10:'H 2 §5 #49',11:'H 2 §5 #52'},
5:{1:'H 2 §6 #1',2:'H 2 §6 #2',4:'H 2 §6 #7',5:'H 2 §6 #8',6:'H 2 §6 #11',7:'H 2 §6 #13',8:'H 2 §7 #2',9:'H 2 §7 #4',11:'H 2 §7 #4'},
6:{2:'H 2 §9 #2',3:'H 3 §3 #1',4:'H 3 §3 #2',5:'H 3 §3 #3',7:'H 3 §3 #7'},
7:{1:'H 4 §1 #2',2:'H 4 §1 #8',3:'H 4 §1 #10',4:'H 4 §1 #14',5:'H 4 §1 #15',6:'H 4 §1 #19',7:'H 4 §1 #22',8:'H 4 §1 #20',10:'H 4 §1 #31',11:'H 4 §2 #2',12:'H 4 §2 #3',13:'H 4 §2 #8'},
8:{1:'H 4 §3 #1',2:'H 4 §3 #2',4:'H 4 §3 #9',6:'H 4 §3 #16',7:'H 4 §3 #18',8:'H 4 §3 #19',9:'H 4 §3 #20',11:'H 4 §4 #1',12:'H 4 §3 #26',13:'H 4 §3 #27'},
10:{1:'H 4 §5 #3(a,d)',2:'H 4 §5 #10',4:'H 4 §5 #13',5:'H 4 §5 #14',6:'H 4 §5 #18',8:'H 4 §5 #25'},
11:{1:'H 4 §6 #2',2:'H 4 §6 #3',3:'H 4 §6 #4',4:'H 4 §6 #5'}}
manifest=json.loads((root/'sources/abstract-algebra/assessment-manifest.json').read_text());by={f['id']:f for f in manifest['files']};items=[]
for hw,total in enumerate(counts,1):
 for q in range(1,total+1):
  public=q in complete[hw];assert public or q in missing[hw],(hw,q)
  entry=dict(id=f'HW{hw}-Q{q}',course='18.703 Spring 2013',file=f'hw{hw:02}',question=q,public_statement=public,subquestions=complete[hw].get(q),source_url=by[f'hw{hw:02}']['resource_url'],solution_origin='AI independently written and reviewed' if public else None,status='included in main PDF' if public else 'book reference only; no public problem text in selected course',book_locator=missing.get(hw,{}).get(q))
  if (hw,q)==(5,11):entry['duplicate_of']='HW5-Q9'
  if (hw,q)==(5,12):entry['duplicate_of']='Practice1-Q5';entry['solution_mapping']='exams.tex ex:commute'
  if hw==11:entry['printed_header_error']='PDF says Homework #9; official resource and index identify HW11'
  items.append(entry)
for n,subs in [(1,[3,3,1,1,1,2,1]),(2,[3,2,1,2,2,1]),(3,[6,2,1,2,2,3,1,1,2,1,3])]:
 for q,k in enumerate(subs,1):items.append(dict(id=f'Practice{n}-Q{q}',course='18.703 Spring 2013',file=f'practice{n:02}',question=q,public_statement=True,subquestions=k,source_url=by[f'practice{n:02}']['resource_url'],solution_origin='AI independently written and reviewed',status='included in main PDF'))
assert len(items)==150 and sum(x['public_statement'] for x in items)==69 and sum(x['subquestions'] or 0 for x in items)==116
(out/'assessment-map.json').write_text(json.dumps(dict(access_date='2026-10-08',counts=dict(numbered_questions=150,public_questions=69,public_subquestions=116,reference_only_questions=81,distinct_reference_only=80,distinct_public_questions=68),books={'H':'I. N. Herstein, Abstract Algebra, Macmillan, 1986, as assigned by course','J':'Tom Judson, Abstract Algebra: Theory and Applications, 2013 course reference; exact historical edition not supplied'},official_solutions='none linked on course assignments/exams pages',missing_exams='actual two midterms and final not published on selected course exam page',items=items),ensure_ascii=False,indent=2))
