"""Source-specific coverage of the two core transcript courses, excluding elective whole-course claims."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'source-inventory.json').read_text())
mapping421={
1:('1','二能级旋转Hamiltonian、共振与失谐'),2:('1','Rabi矩阵指数、旋转参考系、脉冲概率'),
3:('1','Ramsey相位与两脉冲干涉'),4:('1','回波、绝热跟随与共振读出'),5:('1–2','共振尺度与真实原子能量层级'),
6:('2','多电子变分、交换与自旋'),7:('2','精细结构、有限核、Welton领先对数'),
8:('2–3','角动量与超精细结构'),9:('2–3','量子亏损、弱/强场态'),10:('3','Zeeman、Landé与Breit--Rabi块'),
11:('3','Stark混合、宇称、分子转动偶极'),12:('3–4','磁/电场与偶极辐射接口'),
13:('4','最小耦合到电偶极、选择规则'),14:('4','经典/量子驱动、旋波与反旋'),
15:('4–5','发射率、Einstein系数、模式密度'),16:('5','开放二能级、饱和与寿命'),
17:('5–6','衰减相关与线宽'),18:('6','自然、碰撞和Doppler线型'),
19:('6','Gaussian/Lorentz/Voigt卷积及展宽机制'),20:('6–7','非均匀展宽及双光子中间态'),
21:('7','双光子失谐、有效耦合'),22:('7','密度矩阵相干、暗态'),23:('7','Raman/EIT与路径相干'),
24:('7','相干操控的近似条件'),25:('7','干涉、暗态与实验读数')}
mapping422={
1:('8–14','专题结构与先修衔接，基础原子结构沿用1–7章'),
2:('4、8','量子模式与偶极Hamiltonian，省略重复基础推导'),
3:('8','量子光场、相干/数态与Q函数'),4:('8','压缩Bogoliubov变换、矩与损耗'),
5:('8','单光子与非经典计数统计'),6:('9','Schmidt、传态与纯态纠缠'),
7:('9','Mach--Zehnder、误差传播、Yurke与散粒噪声'),8:('8–9','二阶相关、HBT、原子交换干涉'),
9:('10','虚激发、极化率、色散力图像'),10:('10','二阶van der Waals与延迟尺度'),
11:('10','平行板模式和、背景扣除、Euler--Maclaurin压力'),
12:('10','共振交换与Jaynes--Cummings流形'),13:('5','主方程、Bloch方程和稳态'),
14:('5、10','Bloch极点、相干/非相干Mollow谱权重与峰宽'),
15:('5','跳跃、无跳跃演化、记录与非唯一unravelling'),
16:('12','散射/偶极力、反冲与力相关扩散'),17:('10、12','缀饰支、随机切换、滞后摩擦和实际Sisyphus循环'),
18:('13','蒸发能量账、效率、碰撞率幂律与runaway条件'),
19:('13','GP、愈合长度、TF、Bogoliubov耗尽、Mott平均场边界'),
20:('13','Fermi面、Cooper对数、BCS波函数/隙/粒子数与BEC跨越'),
21:('14','Paul阱、边带、Cirac--Zoller三脉冲与几何相位门')}
rows=[]
for prefix,mapping in [('8-421',mapping421),('8-422',mapping422)]:
 for n,(ch,claim) in mapping.items():
  fs=[]
  for f in d['files']:
   if not f['course'].startswith(prefix) or not f['local'].endswith('.pdf'):continue
   if any(re.search(r'/lecture-?'+str(n)+r'(?:-|/)',u) for u in f['resource_pages']):fs.append(f)
  assert fs,(prefix,n)
  rows.append({'course':prefix.replace('-','.')+' '+('Spring 2014' if prefix=='8-421' else 'Spring 2013'),
   'lecture':n,'files':[f['url'] for f in fs],'resource_pages':[f['resource_pages'][-1] for f in fs],
   'status':'prerequisite_plus_bridge' if prefix=='8-422' and n in [1,2] else 'substantive_topic_reconstruction',
   'chapters':ch,'actual_content':claim,
   'boundary':'Topic reconstruction with stated models and approximations; not a literal transcript of all interaction, examples or inaudible boardwork.'})
record={'schema_version':2,'edition':'expanded content revision','core_sessions':46,'core_transcript_segments':53,
 'definition':'Only actual retrieved transcript PDFs mapped to derivations count; elective 6.974/6.453 are selected supplements, not whole courses.',
 'lectures':rows}
(ROOT/'lecture-coverage.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
md=['# 两门核心课逐讲覆盖','','状态区分实质主题重编和先修衔接；不是逐句转写承诺。选读6.974、6.453不计全课完成。','','| 课/讲 | 章 | 实際推导/任务 |','|---|---|---|']
for r in rows:md.append(f"| {r['course']} L{r['lecture']} | {r['chapters']} | {r['actual_content']} |")
(ROOT/'LECTURE-COVERAGE.md').write_text('\n'.join(md)+'\n')
tex=[r'\originalsection{核心课逐讲内容的实际位置}',r'下表按实际取得转写文件列推导位置, 不把课程目录的一个名词视为完整证明. 课堂互动及INAUDIBLE原话不补造, 6.974和6.453仍为选读.',r'\begin{longtable}{p{.15\linewidth}p{.13\linewidth}p{.65\linewidth}}',r'\toprule 课程/讲 & 章 & 实际主题推导\\\midrule\endhead']
for r in rows:tex.append(r['course'].split()[0]+f" L{r['lecture']} & {r['chapters']} & {r['actual_content']}"+r'\\')
tex += [r'\bottomrule\end{longtable}']
(ROOT/'chapters/lecture-coverage.tex').write_text('\n'.join(tex)+'\n')
c=json.loads((ROOT/'coverage.json').read_text());c['lecture_coverage_record']='lecture-coverage.json';c['edition']='expanded content revision';(ROOT/'coverage.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
p=ROOT/'chapters/source-map.tex';s=p.read_text();s=s.replace(r'\textbf{未计为交付的内容.}',r'\input{chapters/lecture-coverage.tex}'+'\n\n'+r'\textbf{未计为交付的内容.}');p.write_text(s)
p=ROOT/'SOURCES.md';s=p.read_text().replace('完整来源索引：','逐讲具体推导和原件段数见 [LECTURE-COVERAGE.md](LECTURE-COVERAGE.md) 与 [lecture-coverage.json](lecture-coverage.json)。\n\n完整来源索引：');p.write_text(s)
