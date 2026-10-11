from pathlib import Path
import re,json,hashlib
r=Path('/workspace/mit-ocw-notes');o=r/'subjects/introductory-mechanics/qa';p=r/'sources/introductory-mechanics/8-01sc-classical-mechanics-fall-2016/pdf'
mapping={1:[1],2:[1],3:[1,2,9],4:[2],5:[2],6:[2],7:[3],8:[3,4],9:[3,12],10:[5],11:[2,14],12:[6],13:[7],14:[7],15:[8],16:[9,13],17:[9,10],18:[9],19:[11],20:[10,11],21:[10],22:[11],23:[13],24:[13],25:[12],31:[14]}
notes={1:'理论建立的历史、牛顿力学适用限度；相对论与量子边界。',2:'SI七基本单位、秒/米/千克/安培/开尔文/摩尔/坎德拉定义、弧度/球面度、常用量与常量量纲、量纲分析无法决定无量纲函数、费米估算方法。PDF内容已更新为现代SI定义，不能从Fall2016标签猜版本。',3:'向量代数、直角及柱坐标、旋转坐标分量变换、叉积性质/右手法则/两坐标表达。原件3.3.2编号重复，保留标题区别。',4:'位移/平均及瞬时速度/平均及瞬时加速度、常加速度、曲线面积与不定/定积分。',5:'二维向量运动学、抛体与消参轨道方程。',6:'圆运动速度/角速率的几何推导、径向与切向加速度、周期频率、角速度向量与角加速度、非圆中心平面运动极坐标公式。',7:'质量校准、第一定律与惯性系、动量形式第二定律、作用反作用且不能配错作用对象。',8:'Hooke力、引力/等效原理/近地引力/Coulomb力、接触静动摩擦、受力图中的系统/力/坐标/建模、绳张力与连续系统微分方程、低/高速阻力。capstan与滑轮约束虽在例题中，已被8.01SC PS4及8.012引用题实质使用，正文不能省。',9:'圆运动动力学、月球与万有引力、圆轨Kepler第三定律、9A球壳内部场零和外部点质量场的积分证明。',10:'冲量、内外力分解、粒子系统、质心离散/连续定义及平移运动、孤立/非孤立系统动量。',11:'Galilean坐标变换、相对惯性系/相对性原理、速度加法。',12:'物质流入/流出有或无动量转移四模型、火箭推力/无重力火箭方程/恒定重力火箭。',13:'能量定义、动能、变加速度、常力变力功、功动能定理、功率、点积、任意路径功在直角及柱坐标中的积分、三维功动能/瞬时功率、13A两粒子系统内外力功。',14:'总能量与机械能区别、保守/非保守力、势能差与零点、多保守力叠加、近地引力/弹簧/反平方势、能量图、闭合系统内部非保守功、摩擦能耗与source energy。14A热力学附录明示范围外，正文仍解释摩擦转内能。',15:'相对速度与质心系、质心动能拆分、不同惯性系ΔK相同条件、碰撞分类、一维实验室/质心系弹性碰撞、二维实验室/质心系碰撞及散射角。',16:'固定轴转动、角速率加速度符号、切向量、转动动能和惯量、积分求杆盘惯量、平行轴定理含16A证明、转动能量守恒。',17:'叉积、力矩定义/符号、固定轴力矩方程与惯量、重心（并非所有非均匀场都等质心）、转动功/能/功率。',18:'静力平衡、杠杆定律与广义杠杆定律、18A静力平衡中力矩参考点无关证明。',19:'点粒子角动量/右手法则、力矩与角动量导数的参考点条件、角动量守恒/角冲量、系统角动量、固定轴版本和外角冲量。',20:'平移加转动约束、无滑滚动、系统角动量轨道项+自转项、动能质心拆分、固定轴转动能、20A Chasles定理。',21:'质心平移与转动方程同时满足、移动固定轴运动、功动能定理含静摩擦不作功的适用条件。',22:'三维角速度向量、陀螺进动、进动机制：小冲量作用质点、受约束物、杆、轴、旋转盘、非旋转盘；不能仅列τ=Ω×L。',23:'周期/SHM解析一般解与相位、能量与力/能量两法推单摆、阻尼三状态及欠阻尼能量、驱动稳态振幅相位共振、机械能/平均功率/Q、小振动展开、23A–D微分方程和复数推导工具。',24:'力矩法单摆、物理摆、扭摆/复合摆（实质主题位于例题）、24A大振幅周期高阶修正。',25:'两体质心/约化质量、能量角动量常量、轨道方程、有效势图及圆/椭圆/抛物线/双曲线、两体各自轨道、Kepler三法则、25A轨道积分推导/25B椭圆轨道关系/25C椭圆几何。',31:'平动加速系、刚体角速度与旋转导数、旋转加速度与第二定律、地球离心力与g纬度修正、科里奥利南北半球方向、两系粒子轨迹转换、旋转平台摆、31A导数变换代数证明、31B极坐标加速度。'}
rows=[];raw=[]
for ch in mapping:
 f=next(x for x in p.glob('*.txt') if re.search(r'_chapter'+str(ch)+r'(?:new)?\.txt$',x.name));pdf=f.with_suffix('.pdf');t=f.read_text();pages=t.split('\f');toc=pages[0]
 for page in pages[1:]:
  if re.search(r'\.{3,}',page) and not re.search(r'\bChapter '+str(ch)+r'\b',page):toc+='\n'+page
  else:break
 raw.append(f'=== {f.name} ===\n'+toc.strip())
 lines=[l.strip() for l in toc.splitlines() if l.strip()];head=[];current=None
 for line in lines:
  line=re.sub(r'\.{2,}\s*\d*\s*$','',line).strip()
  if '©' in line or re.match(r'^\d+(?:-\d+)?$',line):continue
  if re.search(r'\bExample\b',line):
   if current:head.append(current);current=None
   continue
  if line.startswith('Methodology for Estimation Problems'):
   if current:head.append(current)
   current='2.4-methodology Methodology for Estimation Problems'
   continue
  if re.match(r'^(?:\d+(?:[A-Z])?\.[1-9]\d*(?:\.\d+)*\.? |2\.4-methodology |Chapter 1\.1 |Appendix )',line):
   if current:head.append(current)
   current=line
  elif current and not re.match(r'^(?:Example |Chapter |\d+$)',line):
   current+=' '+line
  elif re.match(r'^(?:Example )',line):
   if current:head.append(current);current=None
 if current:head.append(current)
 cleaned=[]
 for line in head:
  title=re.sub(r'\.{2,}\s*\d+\s*$','',line).strip();title=re.sub(r'(?<=[A-Za-z)])\s*\d+\s*$','',title).strip()
  idm=re.match(r'^((?:\d+[A-Z]?\.\d+(?:\.\d+)?\.?|Chapter 1\.1|Appendix \d+\.?[A-Z](?::)?))',title)
  sid=idm[1] if idm else title.split(':')[0]
  cleaned.append({'source_section':sid,'source_heading':title,'coverage_status':'pending_new_manuscript'})
 # body headings omitted by TOC; numbering duplicate handled by literal heading
 for line in t.splitlines():
  match=re.match(r'^\s*('+str(ch)+r'\.[1-9]\d*(?:\.\d+)?\.?)\s+([A-Z][A-Za-z’:, -]+)\s*$',line)
  if match and match[1] not in [x['source_section'] for x in cleaned]:cleaned.append({'source_section':match[1],'source_heading':match[0].strip(),'coverage_status':'pending_new_manuscript','locator_note':'正文标题，目录漏列'})
 rows.append({'source_chapter':ch,'source_pdf':str(pdf.relative_to(r)),'source_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'read_level':'complete TOC and body section headings; selected substantive passages; not all example solutions read','target_manuscript_chapters':mapping[ch],'substantive_scope':notes[ch],'sections':cleaned})
data={'schema_version':1,'status':'source_scope_extracted; manuscript_coverage_pending','selected_chapters':list(mapping),'chapters':rows,'exclusions':['26–30其他分册内容','14A热学附录（保留摩擦耗散为内能的力学联系）'],'criterion':'每个原节的实质概念/推导/条件须有正文落点；逐例原文翻译不是要求，标题关键词匹配不是覆盖证明。'}
(o/'primary-textbook-scope.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');(o/'primary-textbook-toc.txt').write_text('\n\n'.join(raw)+'\n')
print('chapters',len(rows),'headings',sum(len(x['sections']) for x in rows))
