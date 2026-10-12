"""Bind substantive Chinese sections to the actual retrieved lecture files."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'source-inventory.json').read_text())
mas={
1:(5,'Kraus、环境等距、Choi与完全正；根保真度'),
2:(6,'连续误差展开、Knill--Laflamme必要与充分结构、Shor码'),
3:(6,'CSS对偶码、Fourier支持、Steane综合征'),
4:(7,'二元辛表示、投影维数、逻辑正规化子、测量更新'),
5:(7,'环面边/星算符、同调逻辑环、距离与anyon相位'),
6:(7,'Clifford更新、横向传播与编码逻辑操作；PS2中途错误'),
7:(8,'验证猫、四轮停机、Y资源注入与级联递推'),
8:(9,'图态稳定子、删除Z测量、链式传态与前馈'),
9:(4,'Bell传态分支与UP副产物；第9章一步测量门'),
10:(9,'绝热搜索隙与调度、历史态传播项、合法钟和能量保护'),
11:(3,'连续搜索、行走色散、Ambainis缓存与五维矩阵、成本优化'),
12:(10,'Abel陪集振幅、离散对数显式函数、Pell调节子周期流程'),
13:(10,'表示正交与矩阵QFT、二面体相位合成、Heisenberg实例'),
14:(11,'BSC容量、强/弱典型、CPTP压缩器、保真度界、类型集中'),
15:(12,'Gram平方根POVM、相对熵条件、Holevo、HSW打包路线'),
16:(12,'正规化容量优化、擦除信道、参考系统与父/母协议账'),
17:(12,'主序见第11章；混合Bell谱/PPT阈值；非局域CNOT与SWAP'),
18:(13,'多项式指纹、SMP模型、量子指纹误判与一次性签名全流程'),
19:(13,'策略/Nash、PQ、囚徒收益表、SU2差别、公共品GHZ机制'),
20:(13,'EPR抽样、纯化保真度到熵、CSS到BB84、移除量子存储')}
rows=[]
for n,(ch,claim) in mas.items():
 files=[f for f in d['files'] if f['course'].startswith('mas-') and re.search(r'lecture_?'+str(n)+r'(?:\.|_)',f['local'])]
 assert files, n
 rows.append({'course':'MAS.865J Spring 2006','lecture':n,'files':[f['url'] for f in files],
 'status':'substantive_reconstruction','chapter':ch,'actual_content':claim,
 'proof_boundary':'Explicit finite models are derived. General HSW/decoupling, full Hallgren/Kuperberg complexity, low-dimensional PPT sufficiency and full security/adiabatic theorems remain identified cited results.',
 'lecturer':'Sean Hallgren (guest)' if n in [12,13] else ('Isaac Chuang' if n in [1,2,6,7,8,9,10,17,18,19,20] else 'Peter Shor')})
shor={2:(1,'前置量子数学沿用量子卷；本卷补符号、物理噪声与概率接口','prerequisite_plus_bridge'),
4:(1,'计算模型、可逆oracle、垃圾消除和资源计数','substantive_reconstruction'),
5:(1,'相位反冲、Deutsch--Jozsa、Bernstein--Vazirani振幅','substantive_reconstruction'),
11:(3,'量子计数精度、未知M、Grover混合下界','substantive_reconstruction'),
12:(4,'超密编码、传态四分支与第三方参考','substantive_reconstruction'),
13:(1,'普适门构造、误差预算；模型扩展见第9章','substantive_reconstruction'),
14:(9,'图态与自适应测量链','substantive_reconstruction'),
16:(6,'纠错条件及重复/九位码','substantive_reconstruction'),
19:(1,'T1/T2与物理实现接口；光子离子细节沿用AMO卷','prerequisite_plus_bridge'),
23:(8,'容错辅助、单故障传播、级联阈值条件','substantive_reconstruction')}
for n in range(1,24):
 files=[f for f in d['files'] if '18-435' in f['course'] and re.search(r'qc_lec0?'+str(n)+r'\.pdf$',f['local'])]
 if n in shor:
  ch,claim,status=shor[n]; assert files,n
 else:ch,claim,status=None,'此原讲笔记未公开取回；相应主题按MAS和可得文件组织，不声称翻译了缺失原讲','source_missing'
 rows.append({'course':'18.435J Fall 2003','lecture':n,'files':[f['url'] for f in files],'status':status,'chapter':ch,'actual_content':claim})
out={'schema_version':2,'edition':'content revision 2026-10-12','status_definition':'A substantive row names the derivation/task actually written, not a topic checkbox or line-by-line translation claim. Prerequisite and missing-original-source rows are distinct. MAS21-26 project sessions are not theoretical lectures.','lectures':rows}
(ROOT/'lecture-coverage.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
text=['# 逐讲正文覆盖（修订版）','','逐讲列具体推导/协议，区分主线重编、先修衔接和缺失原讲文件。高级引用定理的证明边界见正文。','','| 课程/讲次 | 状态 | 本卷实际内容 |','|---|---|---|']
for r in rows:text.append(f"| {r['course']} L{r['lecture']} | {r['status']} | "+(f"第{r['chapter']}章：" if r['chapter'] else '')+r['actual_content']+' |')
(ROOT/'LECTURE-COVERAGE.md').write_text('\n'.join(text)+'\n')
tex=[r'\originalsection{逐讲内容与原件可得性}',r'MAS二十讲均有实际PDF. 下表列出正文推导而非仅出现的名词; 完整研究定理的证明层级仍按前述边界.',r'\begin{longtable}{p{.09\linewidth}p{.12\linewidth}p{.72\linewidth}}',r'\toprule 讲 & 章 & 实际写入的推导/协议\\\midrule\endhead']
for n,(ch,claim) in mas.items():tex.append(f'{n} & {ch} & {claim}'+r'\\')
tex += [r'\bottomrule\end{longtable}',r'18.435实际取得的原讲PDF仅L2、4、5、11、12、13、14、16、19、23十份. L2的基础量子数学、L19的详细实验器件作为先修或与AMO卷衔接, 其余八讲的计算/纠错链见上列章节. L1、3、6--10、15、17--18、20--22没有取得原讲文件, 对应主题可由MAS和作业材料建立, 但不称那些缺失原讲已经翻译. 完整逐讲文件链接及状态见\texttt{lecture-coverage.json}.']
(ROOT/'chapters/lecture-coverage.tex').write_text('\n'.join(tex)+'\n')
c=json.loads((ROOT/'coverage.json').read_text());c['lecture_coverage_record']='lecture-coverage.json';c['edition']='expanded content revision';(ROOT/'coverage.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
