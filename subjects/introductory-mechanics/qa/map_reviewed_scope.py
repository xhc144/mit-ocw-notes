"""Persist the independently read source-to-manuscript semantic mapping.

Rules below are reviewer-authored content correspondences, not keyword coverage tests.
The body readpack supplements TOCs; hashes bind this review to the actually read TeX.
"""
from pathlib import Path
import hashlib, json, re

ROOT = Path('/workspace/mit-ocw-notes')
QA = ROOT / 'subjects/introductory-mechanics/qa'
CH = ROOT / 'subjects/introductory-mechanics/chapters'
scope = json.loads((QA / 'primary-textbook-scope.json').read_text())
body = json.loads((QA / 'scope-body-readpack.json').read_text())
body_index = {(x['chapter'], x['heading']): x for x in body}

def anchor(file, heading):
    p = CH / file
    text = p.read_text()
    lines = text.splitlines()
    marker = '\\originalsection{' + heading + '}'
    start = next(i for i, line in enumerate(lines) if marker in line)
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith('\\originalsection')), len(lines))
    return {'file': str(p.relative_to(ROOT)), 'line': start + 1,
            'section': heading, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
            'evidence_excerpt': '\n'.join(lines[start+1:end])[:220]}

def target(n, heading):
    return anchor(f'ch{n:02d}.tex', heading)

def decide(c, s):
    sid, h = s['source_section'], s['source_heading']
    a=[]; note=''
    def use(n, heading, explanation):
        nonlocal note
        a.append(target(n, heading)); note += explanation + '；'
    if sid.startswith('14A'):
        return [], 'cross_subject_boundary', '热学附录：内能状态、温度、气体、均分与第一定律不在此册重编；机械耗散转内能联系已在ch07。'
    if c==1:
        use(1,'单位体系与坐标计算','历史形成与原子/高速适用边界')
        use(14,'狭义相对论的基本限制','高速边界的定量接口')
    elif c==2:
        if sid.startswith('2.1'):use(1,'单位体系与坐标计算','七种SI定义、精确定义与测量误差、rad/sr和完整估算例')
        elif sid.startswith('2.2') or sid=='2.3':use(1,'测量与模型','基本/导出量纲、无量纲函数与量纲分析不能定系数');use(1,'单位体系与坐标计算','定义常数的单位及G的量纲')
        else:use(1,'单位体系与坐标计算','Fermi分解假设、人数×瓶数×体积×密度、误差与有效数字')
    elif c==3:
        if 'Cylindrical Coordinate' in h or sid.startswith('3.4') or 'Transformation' in h:
            use(1,'单位体系与坐标计算','柱坐标完整定义、被动转轴分量、叉积分量/反交换/分配/右手基')
        else:use(1,'矢量及投影','坐标分量、长度、相加相减、点积/叉积与投影')
    elif c==4:
        if sid.startswith('4.2') or sid.startswith('4.3'):use(1,'导数与积分','位置/位移/时间与平均-瞬时速度、有向面积和路程区别')
        elif sid=='4.5':use(2,'直线运动与初值','两次积分的常加速度解及消时公式')
        else:use(2,'积分初值与轨道表达','平均加速度、积分初值、非恒加速度示范、积分平均值条件');use(1,'导数与积分','导数/积分及图形面积的含义')
    elif c==5:use(2,'平面抛射与相对运动','二维分量共用时间、等高条件及相对加速度');use(2,'积分初值与轨道表达','消时抛物线和竖直例外')
    elif c==6:use(2,'极坐标与圆周运动','单位向量求导得到速度、径向/切向加速度、非圆极坐标');use(2,'积分初值与轨道表达','周期/频率、右手角速度及变化轴的角加速度')
    elif c==7:
        if sid=='7.1.1':use(1,'单位体系与坐标计算','同校准力下质量比与惯性/称量区别')
        else:use(3,'惯性系与运动方程','惯性系、牛顿三定律、不同作用对象的作用反作用');use(5,'动量与冲量','第二定律的动量形式')
    elif c==8:
        if sid=='8.2.4':use(12,'球壳、地球内部与测量','电荷与质量不同、库仑逆平方力吸引/排斥，电学另册')
        elif sid=='8.2.2':use(1,'单位体系与坐标计算','惯性/引力质量等价实验事实');use(12,'球壳、地球内部与测量','引力质量与惯性质量实验联系')
        elif sid.startswith('8.5'):use(4,'有质量绳与缠绕摩擦','张力定义/质量绳段');use(4,'微段方程与边界','微段二阶定律和末端边界')
        elif sid=='8.6':use(4,'线性及平方阻力','两阻力模型、终端速度及积分、上下运动符号和流动适用条件')
        elif sid.startswith('8.3.2'):use(3,'摩擦与斜面','静摩擦范围、动摩擦方向、临滑与反向运动')
        elif sid=='8.7':use(4,'绳长约束与滑轮','多绳段/动滑轮约束');use(4,'有质量绳与缠绕摩擦','capstan微段与临滑关系');use(14,'平移与转动参考系','加速楔对应有效重力/惯性力');use(4,'线性及平方阻力','自由落体的阻力积分')
        else:use(3,'惯性系与运动方程','选系统、受力图、投影、模型与约束');use(3,'引力、支持力、绳与弹簧','力律、近地重力、弹簧、非负接触与轻绳')
    elif c==9:
        if 'Appendix' in h:use(12,'球壳、地球内部与测量','球壳环元积分及壳内势常数/壳外点质量')
        elif sid.startswith('9.2'):use(12,'有效势与圆轨道','引力圆轨速率');use(12,'逆平方轨道与椭圆','Kepler周期面积推导')
        else:use(3,'摩擦与斜面','圆锥摆、径向合力和竖直圆绳张力限制');use(12,'两体轨道与能量分类','双星的共同周期与质心分配')
    elif c==10:
        if sid=='10.2':use(5,'动量与冲量','动量单位/参考系及变力积分、平均力')
        elif sid in ['10.5','10.6']:use(5,'系统与质心','离散/连续质心、质量元及质心平移方程')
        else:use(5,'系统与质心','系统内外力、方向性守恒、孤立/非孤立及爆炸质心');use(5,'动量与冲量','先定系统/时间/外冲量，再求并核单位方向')
    elif c==11:use(2,'平面抛射与相对运动','位置与速度差');use(2,'积分初值与轨道表达','Galilean变换、相对惯性系与方程同形');use(5,'质心系与相对动能','惯性系动能与碰撞不变量')
    elif c==12:
        if sid.startswith('12.3'):use(6,'火箭方程','推力的相对出口动量、质量比积分、恒重力与离台条件')
        elif sid=='12.1.3':use(6,'动量通量','具有入流惯性速度的一般方程');use(6,'发射流率与收集流率的区别','移动船进入率与喷口发射率不同')
        elif sid=='12.2':use(6,'动量通量','收沙/漏沙/具有入流动量的模型');use(6,'发射流率与收集流率的区别','q=λ(u−v)的移动边界');a.append(anchor('ps06.tex','作业 6: 相对速度与质量流'));note+='单级/两级质量比及卸掉空罐由SC PS6 Q3完整实施；'
        else:use(6,'动量通量','四种入/出流、有/无相对动量项，短时封闭集合推导')
    elif c==13:
        if sid.startswith('13.9'):use(7,'路径功的坐标计算','直角/柱坐标微位移与参数路径积分')
        elif 'Appendix' in h:use(7,'功与动能定理','两粒子内力总功不抵消');use(5,'质心系与相对动能','相对动能µu²/2与内力功对应')
        else:use(7,'功与动能定理','恒/变力、一维到三维点积功、动能变化及瞬时功率');use(1,'矢量及投影','点积的几何与分量定义')
    elif c==14:
        if sid=='14.6':use(7,'势能曲线与平衡','能量图、允许区/转向点及稳定性')
        else:use(7,'保守力与势能','路径独立、势差和零点、多保守力/非保守外功、摩擦转内能及源能量');use(10,'滚动动力学','静摩擦总功为零的固定接触条件与移动接触例外')
    elif c==15:
        if sid.startswith('15.2'):use(5,'质心系与相对动能','相对速度、零质心动量、动能分解、不同惯性系ΔK条件')
        elif sid.startswith('15.6') or sid.startswith('15.7'):use(8,'质心系与二维弹性碰撞','质心系两反向动量旋转与实验室散射角、等质量垂直退化条件')
        else:use(8,'恢复系数与一维碰撞','恢复系数、弹性/非弹性/超弹性分类和完整一维末速');use(8,'弹道摆与多重碰撞','粘合后能量及多球碰撞次序')
    elif c==16:
        if sid.startswith('16.2'):use(2,'极坐标与圆周运动','角速/角加速度符号与切向/径向量');use(9,'刚体定轴运动','共同角度、不同轴距速度')
        elif sid=='16.4':use(9,'转动方程与功','转动功与能量及有惯量滑轮');use(13,'单摆与物理摆','固定轴下落/摆的能量联系')
        else:use(9,'刚体定轴运动','惯量质量元、杆/盘积分及平行轴定理展开证明')
    elif c==17:
        if sid.startswith('17.2'):use(1,'矢量及投影','叉积与右手方向');use(1,'单位体系与坐标计算','叉积代数与两基下分量')
        elif sid=='17.4.2':use(9,'重心与质心','均匀重力场下积分等效及非均匀场限制')
        else:use(9,'转动方程与功','参考点力矩/符号、定轴力矩方程、转动功动能与功率')
    elif c==18:use(9,'静力平衡与构件','合力/合矩、力臂与广义杠杆、换点差为位移叉乘合力的证明');a.append(anchor('ps10.tex','作业 10: 惯量与力矩'));note+='悬杆与坡上人题实施力臂条件；'
    elif c==19:
        if sid in ['19.5','19.9']:use(11,'角冲量与受约束模型','外角冲量时间积分、短过程与支点条件')
        else:use(11,'角动量及参考点','质点/系统角动量、固定点/质心/任意移动点导数及守恒');use(9,'转动方程与功','固定轴分量关系')
    elif c==20:
        if 'Appendix' in h:use(10,'刚体分解的几何理由','保持距离/夹角的旋转，瞬时速度分解与有限转角区别')
        elif sid=='20.3':use(11,'角动量及参考点','质心轨道项+自转项')
        elif sid.startswith('20.4'):use(5,'质心系与相对动能','混合项为零的系统动能分解')
        else:use(10,'刚体速度与无滑条件','平移加转动及接触速度');use(10,'滚动动力学','平动/转动能量与约束');a.append(anchor('ps12.tex','作业 12: 滚动与冲量'));note+='yo-yo、内滚环、摆线等题实施非静止表面约束；'
    elif c==21:use(10,'滚动动力学','平动/转动方程同时求解，摩擦功的条件');use(10,'滑动到滚动','真实摩擦、无滑转换时刻与相对滑移耗散');use(11,'角动量及参考点','质心/移动参考点外矩关系')
    elif c==22:
        if sid.startswith('22.3'):use(11,'从倾斜轨道到力偶: 同一角动量原则','受约束质点→两质点杆→移轴力偶→转盘/静盘完整机制链');use(11,'角冲量与受约束模型','支承线冲量及横向角冲量')
        elif sid=='22.4':use(11,'陀螺与冲量','倾斜快自旋陀螺');use(11,'强制进动与支承载荷','强制平台双支座载荷差与磨坊碾轮的额外压紧')
        else:use(11,'陀螺与冲量','三维角速度、τ=Ω×L与快自旋/慢进动/章动限制');use(10,'刚体分解的几何理由','瞬时角速度可以相加、有限旋转一般不可交换')
    elif c==23:
        if '23B' in sid or '23C' in sid or '23D' in sid or '23A' in sid or sid=='23.2.1':use(13,'方程求解与复合摆','一般解与能量唯一性、复数定义/Euler、共轭根、重根与驱动复幅值')
        elif sid.startswith('23.3.'):use(13,'单摆与物理摆','单摆力矩与能量两条途径、有限振幅积分')
        elif sid=='23.4':use(13,'把不同机制化为振子','滚动圆柱有效质量与整段U管液柱的连续质量')
        elif sid.startswith('23.5') or sid.startswith('23.6'):use(13,'阻尼、驱动与共振','阻尼三态、瞬时/平均能量、稳态幅相、两共振峰及平均功率');use(13,'把不同机制化为振子','弱阻尼洛伦兹半高宽与Q')
        else:use(13,'简谐运动与能量','周期/振幅/相位、初值、SHM能量与任意稳定势小振动')
    elif c==24:
        if sid=='24.3':use(13,'方程求解与复合摆','扭丝恢复矩和复合摆惯量/有向重力臂')
        else:use(13,'单摆与物理摆','单摆/物理摆力矩、小角与大振幅椭圆积分/θ0²修正')
    elif c==25:
        if sid.startswith('25.2') or sid=='25.5' or sid.startswith('25.4'):use(12,'两体轨道与能量分类','两体方程、约化质量及重建、固定非零L下完整能量分类')
        elif sid=='25.7':use(12,'两次脉冲的转移轨道','椭圆相切两次切向脉冲和飞行半周期');a.append(anchor('exams.tex','期末: 综合应用'));note+='r³中心力/有效势/小振动由Final7完整实施；'
        elif '25B.2.5' in sid or '25B.2.6' in sid:use(12,'两次脉冲的转移轨道','一般相对椭圆E-L常量关系与近/远日速度')
        elif '25C' in sid or '25B' in sid:use(12,'两体轨道与能量分类','配方推椭圆、中心偏移与半轴');use(12,'逆平方轨道与椭圆','近日/远日、半轴及周期关系')
        else:use(12,'有效势与圆轨道','能量与角动量常量、面积速度');use(12,'逆平方轨道与椭圆','Binet链式推导、圆锥曲线及Kepler周期');note+='25A两路径以等价Binet推导覆盖结果与条件，不声称逐字重印原积分方法；'
    elif c==31:
        if '31.B' in sid:use(2,'极坐标与圆周运动','两次乘积法则的极坐标加速度推导')
        elif sid.startswith('31.5'):use(14,'地球及旋转台','离心竖直分量、纬度与南北半球科里奥利方向')
        elif sid in ['31.6','31.7']:use(14,'地球及旋转台','旋转矩阵轨迹、复数变换解转台摆和Foucault适用条件')
        else:use(14,'平移与转动参考系','基矢导数→任意向量→两次位置求导→完整旋转牛顿方程')
    return a, 'covered_substantive', note.rstrip('；')

for c in scope['chapters']:
    c['read_level']='complete TOC/body-heading inventory; substantive narrative passages at every non-thermal section read; all manuscript theory and assessments read; selected mechanism derivations and ambiguous original figures read in detail; not every source example solution or every PDF page read in full'
    for s in c['sections']:
        targets, status, note = decide(c['source_chapter'], s)
        s.update(coverage_status=status, manuscript_locations=targets, coverage_basis=note)
        b=body_index.get((c['source_chapter'],s['source_heading']))
        if b:s['source_body_evidence']={'text_line':b['source_line'],'excerpt_read':b['body_excerpt'][:430],'readpack':'qa/scope-body-readpack.json'}
scope['status']='semantic_source_section_mapping_completed; source/example read-depth limits retained; final PDF visual review pending'
scope['reviewed_manuscript_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(CH.glob('ch*.tex'))}
scope['coverage_counts']={status:sum(s['coverage_status']==status for c in scope['chapters'] for s in c['sections']) for status in ['covered_substantive','cross_subject_boundary']}
scope['embedded_substantive_mechanisms']=[
 {'source':'8.7 Example8.11 capstan','target':target(4,'有质量绳与缠绕摩擦'),'status':'covered'},
 {'source':'12.2 Example12.4 moving boat / actual catch flux','target':target(6,'发射流率与收集流率的区别'),'status':'covered'},
 {'source':'12.3 Example12.5 two-stage rocket','target':anchor('ps06.tex','作业 6: 相对速度与质量流'),'status':'covered'},
 {'source':'22.4 Example22.4 forced platform supports and Example22.5 grain mill','target':target(11,'强制进动与支承载荷'),'status':'covered'},
 {'source':'23.4 Example23.3 rolling spring and Example23.4 U-tube','target':target(13,'把不同机制化为振子'),'status':'covered'},
 {'source':'24.3 torsional oscillator and compound physical pendulum','target':target(13,'方程求解与复合摆'),'status':'covered'},
 {'source':'25.7 Example25.4 Hohmann transfer','target':target(12,'两次脉冲的转移轨道'),'status':'covered'}]
(QA/'primary-textbook-scope.json').write_text(json.dumps(scope,ensure_ascii=False,indent=2)+'\n')
md=['# 主教材逐节实质覆盖映射','', '本表按实际源正文段落及完整中文稿阅读形成。covered_substantive 指概念、机制、公式与条件有教学落点，不代表每一源例数值与每一种等价证明都逐字重编。所有源目录项逐条保留；14A明确跨科。具体正文哈希、证据段及源文本行见 primary-textbook-scope.json。PDF图尚待最终视觉检查。','', '|源节|实质落点|判断|','|---|---|---|']
for c in scope['chapters']:
    for s in c['sections']:
        locations=', '.join(f"{Path(a['file']).name}:{a['line']} {a['section']}" for a in s['manuscript_locations']) or '热学分册边界'
        md.append(f"|{s['source_heading'].replace('|','/')}|{locations}|{s['coverage_status']}|")
(QA/'textbook-coverage-review.md').write_text('\n'.join(md)+'\n')
print(scope['coverage_counts'])
