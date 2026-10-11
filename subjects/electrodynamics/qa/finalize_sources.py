#!/usr/bin/env python3
import json,hashlib,shutil,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; CACHE=Path('/tmp/electrodynamics-candidates')
j=json.loads((CACHE/'collection.json').read_text())
held={
'mit8_07f12_ln15':'原件明确标注 Standard YouTube License 内容 excluded from Creative Commons; 不打包完整原件.',
'mit8_07f12_ln17':'第25页含 Griffiths 商业教材扫描题面; 保守暂缓整件再分发, 未将其误称为官方明示排除.'}
for e in j['files']:
 if e['course_id']=='8-311-spring-2004': e['authors']=['Chiyan Luo'] if e['id'].startswith('solution') else ['Leonid Levitov']
 elif e['kind'] in ['assignments','exams']: e['authors']=['Alan Guth']
 e['license']='CC BY-NC-SA 4.0 subject to MIT OCW terms and identified third-party exceptions'
 e['attribution']='; '.join(e['authors'])+'. '+e['title']+'. MIT OpenCourseWare, '+e['semester']+'.'
 e.pop('local_candidate',None)
 e['accessed_on']='2026-10-11'
 if e['course_id']=='8-311-spring-2004':
  if e['id'].startswith('solution'):
   e['title']='Problem Set '+e['id'].replace('solution','')+' Solutions'
   e['special_attribution']='Courtesy of Chiyan Luo. Used with permission.'
  elif re.fullmatch(r'ps\d+',e['id']): e['title']='Problem Set '+e['id'][2:]
  else: e['title']={'wave_guides':'Wave Guides','field_osc':'Field Oscillators','power_spec':'Power Spectrum of Radiation','charge_mov':'Charge Moving in a Dielectric','final':'Final Exam','final_solution':'Final Exam Solution'}[e['id']]
 if e['id']=='mit8_07f12_ln13': e['special_attribution']='Courtesy of Hongsheng Chen and Min Chen. Used with permission.'
 if e['id']=='final_solution': e['author_note']='个体解答作者未在官方索引标注; Leonid Levitov 为课程教师, 不冒充个体作者.'
 e['attribution']='; '.join(e['authors'])+'. '+e['title']+'. MIT OpenCourseWare, '+e['semester']+'.'
 if 'special_attribution' in e: e['attribution']+=' '+e['special_attribution']
 if e['id'] in held:
  e.update(archive_allowed=False,status='verified-candidate-withheld',path=None,third_party_exception=held[e['id']])
 else:
  rel=f"sources/electrodynamics/{e['course_id']}/{e['kind']}/{e['id']}.pdf"
  p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(CACHE/(e['id']+'.pdf'),p)
  assert hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256']
  e.update(archive_allowed=True,status='downloaded-verified',path=rel,third_party_exception='未发现另列许可例外; 教材题号和阅读引用不授予对应商业教材题面许可.')
for p in j['pages']:
 if p['status']=='retrieved':
  sec=p['url'].split('/courses/')[1].split('/',1)[1]
  src=CACHE/f"{p['course_id']}-{sec.replace('/','_') or 'home'}.html"
  rel=f"sources/electrodynamics/{p['course_id']}/metadata/{src.name}"
  target=ROOT/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target)
  p['path']=rel;p.pop('text',None)
m={'schema_version':1,'subject':'electrodynamics','checked_at':'2026-10-11','primary_course':{'id':'8.07','title':'Electromagnetism II','semester':'Fall 2012','authors':['Alan Guth','Min Chen'],'url':'https://ocw.mit.edu/courses/8-07-electromagnetism-ii-fall-2012/'},'advanced_course':{'id':'8.311','title':'Electromagnetic Theory','semester':'Spring 2004','authors':['Leonid Levitov'],'url':'https://ocw.mit.edu/courses/8-311-electromagnetic-theory-spring-2004/','scope':'4 supplemental notes, 12 assignments with official solutions, final with official solution; not a complete lecture-note set'},'8.312_status':'本次未定位到可核实的 OCW 课程, 未伪造原件或资源.', 'licensing_policy':'保留原作者与官方来源; 中文重编非 MIT 官方中文或官方认可. 题号引用不视为获得商业教材题面, 另列例外不按默认 CC 许可打包.', 'license_interpretation_source':'https://mitocw.zendesk.com/hc/en-us/articles/4414756181403-How-is-all-rights-reserved-content-different-from-the-rest-of-OCW-content/', 'files':j['files'],'metadata_pages':j['pages']}
(ROOT/'manifests/electrodynamics-sources.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print('archived PDFs',sum(e['archive_allowed'] for e in m['files']),'withheld PDFs',sum(not e['archive_allowed'] for e in m['files']),'archived pages',sum(e['pages'] for e in m['files'] if e['archive_allowed']))
