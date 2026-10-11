"""Bind the completed independent review to the actually read final artifacts."""
from pathlib import Path
import json, hashlib, ast
ROOT=Path('/workspace/mit-ocw-notes'); R=ROOT/'subjects/introductory-mechanics'; Q=R/'qa'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pdfsha=sha(R/'introductory-mechanics.pdf')
assert pdfsha=='c8ccb5c8e0a4fdce3dbcfa2b7bfcd40ab00411ebcb7c07a54e66184fe3f337bc'
visual={'pdf_sha256':pdfsha,'pages':58,'status':'no blocking issue in the actual visual scope reviewed','contact_sheet_pages_viewed':list(range(1,59)),'high_resolution_pages_viewed':[10,29,37,46,48,52,53,54,55],'last_change':{'from_pdf_sha256':'c3090a8df4a7d4f73b54ac3a2a84b98d7dec63ae55f0276be324af6a6862dcab','pixel_comparison_changed_pages':[37],'method':'PIL RGB pixel difference of all 58 author-rendered page PNGs, followed by independent PyMuPDF high-resolution page37 render and viewing'},'read_limits':'All pages visually inspected as contact sheets for gross layout. Only the listed critical pages were additionally inspected at high resolution. This is not a claim that every PDF page was reread at high resolution. All manuscript text and reproduced solutions had separately been fully read in TeX.','critical_results':{'10':'radius, tangent velocity and inward acceleration clearly separated; current ch02 label placement reread','29':'elevator velocity graph matches time intervals and area','37':'U,K,E arrows visible, U0 subscripts complete after clip=false, label clear of curve; current ps08 reread','46':'numerical results, units, tables, model boundaries readable','48':'three-object free-body diagrams retain all requested forces and correct directions; equation/threshold match independent calculation','52':'source photo present; flip upper-left, twist along legs upper-right, total steeper upper-right; qualitative nature stated','53':'disk collision equations/general versus no-spin special case readable','54':'strong impulse qualification, actual effective-potential minimum and plot labels readable','55':'formula sheet entries and explicit correction of source work-energy typo readable'}}
(Q/'pdf-visual-snapshot.json').write_text(json.dumps(visual,ensure_ascii=False,indent=2)+'\n')
for name in ['primary-textbook-scope.json','assessment-manuscript-review.json','theory-final-content-review.json']:
 p=Q/name;d=json.loads(p.read_text());d['final_pdf_sha256']=pdfsha;d['visual_review']='see pdf-visual-snapshot.json for exact viewed pages and resolution limits'
 if name=='primary-textbook-scope.json':d['status']='completed semantic source-section mapping and final scoped PDF visual review; source/example read-depth limits retained'
 elif name=='theory-final-content-review.json':d['status']='all 14 theory manuscripts read; substantive mapping completed; no remaining major mathematical finding; final scoped PDF visual review completed'
 else:
  d['status']='completed independent content/math review of primary62/121, advanced13/34, exams22/80,85reference objects and final scoped PDF visual review'
  d['unreviewed']=['Not every raw source example solution was read word-for-word; not every PDF page inspected at high resolution. These limits do not leave any reproduced assessment request unchecked.']
  for a in d['primary_problem_reviews']:
   if a['id']=='sc-ps8-5':a['note']='U/K/E各有箭头，负势能及E的下标完整；最终物理第37页已高清查看。U/K在±0.45对称位置有相同势能高度。'
  for a in d['exam_problem_reviews']:
   a['note']=a['note'].replace('FBD视觉待查。','三对象FBD已在最终物理第48页高清核方向。').replace('图待最终视觉。','照片和三向量图已在最终物理第52页高清核对。')
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
p=Q/'textbook-coverage-review.md';t=p.read_text().replace('PDF图尚待最终视觉检查。','最终PDF视觉范围与哈希见 pdf-visual-snapshot.json；已完成全册缩略版面与九个重点页高清检查。');p.write_text(t)
final='''# 独立终审结论（2026-10-11）

现稿14章理论、12套主作业62题/121请求、进阶独立13题/34请求、四考试22题/80请求、85条教材题号引用已实际完整读过；所有已重编题解经独立计算核查。所选26章的328节目录项逐条保留：306个非热学项有实质内容与教学落点，14A的22项明确交热学分册。当前未发现阻断发布的数学、题面小问覆盖或实质主题缺口。

最终58页PDF SHA256：`'''+pdfsha+'''`。已实际查看1–58页联系图以检查整体版面；另外高清查看物理页10、29、37、46、48、52、53、54、55。明确核过圆周图、升降机v-t图、U/K/E图、数值表、三物体FBD、原照片与空翻/扭转/总角速度图、有效势图和公式表。c309版至本版逐页PNG比较只有37页变化，该页已重新查看。没有把缩略版检查称为全册高清逐字检查。记录见 `pdf-visual-snapshot.json`。

逐節定位和稿件哈希见 `primary-textbook-scope.json`、`textbook-coverage-review.md`；逐题/小问和哈希见 `assessment-inventory.json`、`assessment-manuscript-review.json`。独立数值算法证据见 `independent-numerical-review.json`。源阅读范围仍明确：全部题面及重点图已核；教材各非热学节的实质段落已读，并精读关键机制；未声称所有原例逐字翻译/全体源PDF逐页高清全读。

下列初审/内容阶段记录保留为发现和修复历史，其中旧“待补/待PDF”字段不代表最终仍待办。

---

'''
p=Q/'manuscript-review.md';t=p.read_text();p.write_text(final+t)
p=Q/'source-assessment-audit.md';p.write_text(p.read_text()+'\n\n## 最终审校状态\n\n'+final.split('下列初审')[0].replace('# 独立终审结论（2026-10-11）','2026-10-11 独立内容及明确范围内的视觉审校完成。'))
receipt={'status':'completed_no_remaining_blocking_finding_in_reviewed_scope','date':'2026-10-11','pdf_sha256':pdfsha,'pdf_pages':58,'scope_counts':{'textbook_chapters':26,'substantive_sections':306,'cross_subject_thermal_sections':22,'primary_main':62,'primary_requests':121,'advanced_mit_main':13,'advanced_mit_requests':34,'exam_main':22,'exam_requests':80,'reference_only':85},'manuscript_sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((R/'chapters').glob('*.tex'))},'manifest_sha256':sha(ROOT/'manifests/introductory-mechanics-sources.json'),'visual_record':'qa/pdf-visual-snapshot.json','limitations':['All raw textbook examples and original proofs were not individually recalculated or read word-for-word.','58 pages examined as contact sheets; nine named pages additionally high-resolution.','Final Q5 bonus exact strong-impact threshold is not determined by unspecified impact/contact model; manuscript explicitly qualifies the official approximation.','85 Kleppner-Kolenkow items remain title/number references, not guessed full questions.']}
receipt['qa_deliverable_sha256']={p.name:sha(p) for p in [Q/'assessment-inventory.json',Q/'primary-textbook-scope.json',Q/'assessment-manuscript-review.json',Q/'theory-final-content-review.json',Q/'pdf-visual-snapshot.json',Q/'independent-numerical-review.json',Q/'manuscript-review.md',Q/'source-assessment-audit.md',Q/'textbook-coverage-review.md']}
(Q/'independent-final-review.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
for p in Q.glob('*.json'):json.loads(p.read_text())
for p in Q.glob('*.py'):ast.parse(p.read_text())
print('Completed final review. JSON/Python syntax verified. PDF',pdfsha)
