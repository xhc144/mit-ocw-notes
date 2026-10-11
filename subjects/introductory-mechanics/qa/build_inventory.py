from pathlib import Path
import re,json,hashlib
root=Path('/workspace/mit-ocw-notes');out=root/'subjects/introductory-mechanics/qa';p=root/'sources/introductory-mechanics/8-012-physics-i-classical-mechanics-fall-2008/pdf'
manifest=json.loads((root/'manifests/introductory-mechanics-sources.json').read_text())
assets={a['filename']:a for a in manifest['assets']}
base='https://ocw.mit.edu/courses/8-012-physics-i-classical-mechanics-fall-2008/'
manual={
'ps1':[(9,'Two Trains and a Bee',['a:逐段飞行距离、求和','b:总碰撞时间法']), (10,'Dimensional Analysis',['a:恒星振动频率','b:球的二次阻力','c:终端速度并给替代推导','d:单摆频率与无量纲初角依赖'])],
'ps2':[(11,'Bridge Building',['a:七梁各铰点力、方向和拉压性','b:加分，n三角桥2n+1梁推广']), (12,'Order of Magnitude Estimates',['a:全人类牵手绕地球圈数','b:角秒每年投影至月球的速度与比较','c:30mph碰撞保持20g内的溃缩区长度','d:附近恒星质量密度与空气比较'])],
'ps3':[],
'ps4':[(9,'The super-astro-blaster',['a:n球最高反弹高度与1km所需球数','b:逃逸速度估算与所需球数']), (10,'A falling chain',['单问:桌边支撑力随时间；图为长链在桌边外侧、底端U形绕边，最终挂于桌下'])],
'ps5':[(10,'Solar Energy',['a:波士顿用电平均功率估算','b:太阳入射功率与年度实际可用功率','c:供电需覆盖土地比例及障碍','d:宿舍屋顶与四人独栋住宅比较','e:80000kWh/人/年换瓦，解释与(a)差异并评估全能源需求'])],
'ps6':[(7,'Hanging Cylinder',['单问:最小绳角与非最大角解释；绳切于圆柱右上侧、圆柱接触左墙'])],
'ps7':[(11,'Superball Bounce',['a:第一次反弹后的水平速度与角速度','b:第二次反弹与多次运动规律'])],
'ps8':[(8,'Rectangular Symmetry',['a:三个中心轴惯量与垂直轴定理','b:角动量与角速度非平行、a≠b时角速度沿另一对角线']), (9,"Euler’s Disk",['a:总角速度方向与Ωsinα大小','b:原式Ω=2√(g/(Lsinα))及α极限；原图半径R、公式L未定义，按L=R解读','c:俯视盘面旋转频率2(1−cosα)√(g/(Lsinα))；L按原图半径R'])],
'ps9':[(10,'Moment of Inertia of a Water Molecule',['a:质心、主轴与主轴系惯量张量','b:无力矩转动不稳定轴'])],
'ps10':[(10,'Spinning up Figure Skater',['a:变化角速度引入Euler/azimuthal惯性力','b:旋转系推导dotω与ω,R,dotr关系','c:惯性系角动量推导同式','d:半径减半的转速倍率'])],
'exam1':[(1,'Quick Multiple Choice Questions',['a:四力律有效性','b:轮胎滑动摩擦方向','c:有质量静止绳两端拉力','d:摆最低点合力方向','e:质量倍增绳长减半周期']), (2,'The Accelerated Atwood Machine',['a:两块与动滑轮受力图','b:不滑动加速度','c:滑动时两块加速度和大小关系','d:最小致滑拉力']), (3,'Hanging Rope',['a:正弦线密度归一化λ0','b:自由端张力','c:距挂点z处张力']), (4,'Don’t Slip!',['a:初始最大角加速度','b:摩擦力极坐标向量随时间','c:开始滑动时刻']), (5,'Will the LHC Destroy the World?',['a:穿地振动周期量纲估算','b:均匀地球简谐运动与准确周期','c:同总质量/半径中心较密对周期影响','d:加分，能源转黑洞质量半径数量级与风险讨论'])],
'exam2':[(1,'Quick Multiple Choice Questions',['a:一维m,2m弹性碰撞选项','b:三次碰撞最大冲量','c:漏沙车速度','d:复合圆盘质心','e:弹簧最远端落粘土守恒量']), (2,'Collision',['a:二维碰后U与θ','b:动能变化与超弹性判别']), (3,'Cube on a Sphere',['a:沿球面速度','b:脱离角']), (4,'Tabletop Rocket',['a:起动条件','b:最高速度','c:燃尽后路程','d:加分，总路程']), (5,'Planet Orbit',['a:圆轨道势能/动能/总能','b:逃逸最小增能与速率倍率','c:F=−Amv²vhat每周期能量损失','d:每周期半径变化、径向速度与方向'])],
'exam3':[(1,'Quick Multiple Choice Questions',['a:骑车上坡摩擦方向','b:指定自转/倾角陀螺进动方向','c:绳绕棒运动守恒量','d:等冲量哑铃质心速度','e:等冲量哑铃动能']), (2,'Catch Pendulum',['a:捕获后角速度','b:粘合机械能损失','c:转180度入射最小速度']), (3,'Swinging bar',['a:枢轴接触力作功','b:角速度随摆角','c:角加速度随摆角','d:杆对枢轴水平/竖直力']), (4,'Atwood machine',['a:轮圈与六根轮辐惯量','b:重盘从h下降着地速度','c:重盘粘地后轻盘最大高度']), (5,'Rolling a coin',['a:进动大小/方向','b:总角速度极坐标向量','c:倾角，须列全运动方程','d:加分，一阶α总角动量向量'])],
'final':[(1,'Multiple Choice & Short Answer Questions',['a:两行星轨道速度和角动量比较','b:Chasles定理','c:收臂滑冰者守恒量','d:G量纲','e:由陀螺自转/进动方向反推重力','f:加分，跳水照片旋转向量与前/后翻']), (2,'Atwood Machine',['a:轻块上/下运动两条件','b:轻块下行加速度']), (3,'Rocket in an Interstellar Cloud',['a:燃烧及二次阻力运动方程','b:保持v0所需推力','c:燃尽后的速度随时间','d:加分，90度锥头粒子弹性碰撞导出A和二次阻力']), (4,'Sticky Disks',['a:粘合后质心速度及自转','b:最终不自转ω0','c:一般机械能损失，另列官方不自转特例']), (5,'Cylindrical Top',['a:冲量后平移速度','b:倾角和升起哪端','c:进动速率/方向，R≪L','d:加分，逆进动最小倾角和冲量；不能默认R≪L']), (6,'Bead on a Spinning Rod',['a:保持r0的力','b:释放后惯性系极坐标位置','c:旋转系惯性力与两系真实杆力']), (7,'Central Potential',['a:F=−Ar³rhat的有效势、极值和能否经过原点','b:r0圆轨道所需初速度','c:小振动频率与轨道周期比较'])]
}
inventory=[]
for key in manual:
 f=next(p.glob(f'*_{key}.txt'));pdf=f.with_suffix('.pdf');a=assets.get(pdf.name,{})
 refs=[]
 if key.startswith('ps'):
  for m in re.finditer(r'(\d+)\. Kleppner & Kolenkow, Problem (\d+\.\d+)',f.read_text()):
   refs.append({'number':int(m[1]),'type':'textbook_reference_only','textbook':'Kleppner & Kolenkow, An Introduction to Mechanics, 1973','reference':m[2],'subquestions':None,'scope_rule':'保留题号及已发布勘误；没有已许可完整题面，不猜写全文','rights':'题号/书目引用；未授权复制教材题面'})
 probs=refs+[{'number':n,'type':'mit_full_statement','title':title,'subquestions':subs,'rights':'unmarked MIT OCW text under CC BY-NC-SA 4.0; no object-specific contrary notice found in inspected source pages','figures':'unmarked diagrams; redraw with original geometry' if not(key=='final' and n==1) else 'e:unmarked diagram; f:uncredited diver photo separately unresolved, no contrary marking found, use link or independently sourced/redrawn illustration preserving clues'} for n,title,subs in manual[key]]
 probs.sort(key=lambda x:x['number'])
 inventory.append({'id':key,'official_url':a.get('url',base+pdf.name),'source_pdf':str(pdf.relative_to(root)),'source_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'read_level':'all statement text plus all assessment page thumbnails; key diagrams high resolution','optional':key=='ps10','problem_count':len(probs),'problems':probs})
sol=[]
for key in ['exam1sol','exam2sol','exam3sol','final_sol']:
 f=next(p.glob(f'*_{key}.pdf'));a=assets.get(f.name,{})
 sol.append({'id':key,'source_pdf':str(f.relative_to(root)),'official_url':a.get('url',base+f.name),'rights':'unmarked MIT OCW solution text/diagrams under CC BY-NC-SA 4.0; no contrary notice found on inspected page thumbnails','read_level':'solution prose and page thumbnails; key omitted equations read in high-resolution renders; not all formulas independently recalculated','full_math_review':'pending against new notes'})
obj={'schema_version':1,'audit_date':'2026-10-11','assessments':inventory,'official_solutions':sol,'counts':{'assignments':10,'assignment_numbered_problems_excluding_collaboration_q0':98,'textbook_reference_only':85,'mit_full_assignment_problems':13,'exam_sets':4,'exam_main_problems':22,'mit_assignment_leaf_requests':33,'exam_leaf_requests':77},'limitations':['教材引用题小问未知，subquestions=null绝不表示无小问','未把作业的协作声明Q0算物理题；PS6实验提案另列教学范围','正文与最终PDF未产生时不标数学或版面审校完成','没有已公开10套作业官方解答取回证据；仅4套考试官方解答已取回']}
obj['counts']['mit_assignment_leaf_requests']=sum(len(x['subquestions']) for a in inventory if a['id'].startswith('ps') for x in a['problems'] if x['type']=='mit_full_statement')
obj['counts']['exam_leaf_requests']=sum(len(x['subquestions']) for a in inventory if not a['id'].startswith('ps') for x in a['problems'])
(out/'assessment-inventory.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(obj['counts'])
