# 18.433 课程作业：独立数学审读

审读代理：matrix_electric_audit。此代理没有参与18433正文写作，独立读完全部题面、解答及重点一般证明，并核对对应官方题面。这是独立模型审读，不是人类专家审定；不将程序输出或作者自查称为一般数学证明。

## 结论及绑定范围

对当前正文未发现阻断性数学错误。已审范围为作业1全部Q1–7、作业2全部Q1–5、作业3Q6(a)(b)、作业4Q2(a)(b)和Q3(a)–(d)，共15原题、25叶题，完整读过全部正文，而非只检查四个重点。结论覆盖明示补充条件下的数学命题、构造和算法推导。调用的Hamilton圈NP-complete性及有理椭球法基础优化定理是明确边界，不声称本片段证明它们。

- 正文：`subjects/graph-theory/assessments/18433/main.tex`
- 初读及最终复核SHA-256均为：`e3793c717e87e080f0c1cf6f134379cc4d0f76a95cae775248a46d0a2db10854`
- 已读math-lecture-writing的`writing-and-proof.md`和`review-gates.md`，区分文本数学审读、有限计算和交付检查。
- 只新写本报告，未改正文、其他学科、主文件、主PDF/ZIP或远端。

## 官方题面核对

实际打开官方A1第1、2页、A2第1页、A3第2页、A4第1页，共5张相关题面；A3第1页其余凸规划题未入本次冻结范围，没有声称审读那些解答。A1、A2、A3的文本提取含字体编码乱码，因此依据实际PDF渲染核对英文命题与中文内容。原题没有独立答案，正文逐题标为编者独立解答，与所读资源状态一致。

- A1Q5原文只写maximal set of disjoint augmenting paths，正文把最短和顶点不相交作为明示补条件，并证明未补最短时反例成立。
- A2Q1原题未明确内部点不可删端点/无直接s→t，正文显式补条件，避免直接弧使顶点分离数无定义的例外。
- A2Q3原题any undirected graph遗漏连通约定；正文连通条件及8孤立点反例准确。
- A2Q5原文指撤回原弧流量的reverse arcs，正文保留每条原弧的残量身份，成本0/1含义正确，没有把反向邻点误当同一原弧身份。
- A3Q6两问忠实保留，LP仅解松弛，未声称分数点给旅行商最优圈。
- A4Q2是二边连通，不是二顶点连通；正文允许闭合耳，契合原题。A4Q3比值明确LP/整数最优，与原卷一致。

## 各题一般证明审读

| 原题 | 独立核对的支持与条件 | 结果 |
|---|---|---|
| A1Q1 | 分量最短路奇偶划分；奇闭行走通过重复点剖分下降得到奇圈 | 未见缺口 |
| A1Q2(a–c) | 一次扫描实现O(n+m)，四顶点路反例，极大匹配端点覆盖及最大匹配记账 | 未见缺口 |
| A1Q3 | 非负权补条件实质必要；排序后每条最优边记给早选且不轻的边，每贪心边至多2条，负权反例有效 | 未见缺口 |
| A1Q4(a–c) | 肯定/否定证书两侧均有；Euler忽略孤立点及空巡回约定，偶度连通边支撑的拼接存在性展开 | 未见缺口 |
| A1Q5 | 虚源汇分层距离、翻转后的旧距离不等式、等长新路只能用旧正层弧、共点必用新匹配反向弧、极大性矛盾 | 未见缺口 |
| A1Q6 | 独立集补集覆盖；最大匹配加边得到边覆盖；最小边覆盖每边有叶端导致星形分量，构造匹配 | 未见缺口 |
| A1Q7(a,b) | 0–1独立集IP和显式上下界；分数紧边分量上的二分正负扰动，整数相邻点不能连紧边；有限约束正余量 | 未见缺口 |
| A2Q1 | B=n+1拆点，最小割<n+1强制只有单位拆点弧；分离集/割及整数无圈路流两向对应，直接弧排除 | 未见缺口 |
| A2Q2 | 最大瓶颈Dijkstra类标签确定证明，−∞区分无路与真实0容量路，索引堆明确 | 未见缺口 |
| A2Q3 | 收缩时最小割下界不降、生存乘积1/binom(n,r)、均匀无序二分输出概率和目标互斥计数，严格界与n<r边界 | 未见缺口 |
| A2Q4 | 每路跨割给弱界；严格大于瓶颈的阈值可达集给反界，无路/空割约定 | 未见缺口 |
| A2Q5 | 身份成本互补1、最短路每弧紧、旧距离是新图可行势导致不减、再次临界前反向使用迫使尾距至少+1；2nm及精确有理位长 | 未见缺口 |
| A3Q6(a,b) | 度2+所有非平凡割的IP；有理界检查/根到全部汇最小割的强分离；输出0/1行，既有最大流支持；完全图度矩阵秩、n=3直接点及n≥4严格点保证仿射包接口 | 未见缺口；有理椭球基础定理明确调用 |
| A4Q2(a,b) | Hamilton≤n边判定归约，非二边连通输入映固定图以满足承诺；桥判据、圈起始、外部分量两条连接边、可闭合耳和n+q计数，OPT≥n | 未见缺口；HamiltonNP-complete背景调用 |
| A4Q3(a–d) | 全序前/后向半数保证和OPT=max次序前向；圈约束IP；稀疏随机定向图统一次序概率界+短圈删边+LP可行分数点，ratio上确界2；最小圈权oracle与显式满维箱 | 未见缺口；LP优化使用前题基础定理 |

## 四个重点的逻辑检查

**A1Q5。** 最短路上的顶点增广后全已匹配，且它们的M′匹配边恰是所选路旧非匹配边的翻转。任何新等长增广路若通过这些点，内部交错必使用那条新反向匹配弧；该弧降低旧距离而不可能属于等长路。所以等长路必顶点不交，与阶段前同长路组极大性冲突。正文所给长5路反例在翻转后确实还有长3路；单路组未使用的自由点之间无边，因此确为极大组。

**A2Q5。** 此题0/1成本与普通按弧数最短的增广不同，正文没有偷换算法。若一身份成本w临界时尾距为a，头距a+w；再次出现必须使用互补成本1−w的相反身份，该次紧性加上全点距离不减，推出新的原尾距≥a+w+1−w=a+1。以后再次临界仍不减，有限整数距离0…n−1给每身份≤n次；2m身份记账即≤2nm，不依赖容量整数或正瓶颈下界。抗平行弧和反向原弧时必须保留身份，正文已经明确保留。

**A4Q2。** 二边连通图可以有割点，闭合耳对这种情形必要。外部分量到H仅一条连接边会是G的桥，故可选两条；简单图排除两条完全同端点的重复边，因此闭合耳也是合法圈。每耳p个新点/p+1条边，先有ℓ≥3圈，得到n+q≤2n−ℓ≤2n−3。固定五点两三角形共点图的外部四个度2点迫使全部六边，因此它在阈值n=5下是合法承诺的否定实例。

**A4Q3(c)。** 固定g≥3和δ∈(0,0.1)后，pN阶n^(1+1/(2g))压过n log n，使全部n!次序同时受界。短有向圈期望≤g n^((g−1)/(2g))，删至多n弧不会新增圈；mH≥(1−δ)pN−n为正且足以把损失吸收到(1/2+2δ)mH上界中。重要方向是F_H≤F_original，M−mH≤n，给OPT_H≤mH/2+n/2+δpN/2；正文方向正确。圈长j≥g使常数向量x=1−1/g满足j(1−1/g)≤j−1。先任选更大g/更小δ，再取各自足够大n，得比值任意接近2，配通用上界2得上确界，未声称有限样本精确达到2。

## 独立小实例核对

我另写并实际运行 `/tmp/18433-independent-check.py`，没有使用作者的核验脚本或仅复制其输出。脚本全文放在报告末尾。有限计算是额外证据，不证明以上一般结论，特别不能证明随机图渐近存在性。

- 脚本SHA-256：`8a0dc007b54c4bde73af7d0aa69d33b0784a419640ab97f7268b55bff541e77e`；输出SHA-256：`11e5906c272cbfe46ee4e3e306a9764f22d0c13520defcbf286075371359df2e`。
- A1Q5：穷举3×3二分图512张、其全部5504个匹配，枚举所有最短增广路及顶点不交极大子组；7080个阶段全部验证增广后最短长度严格上升或不再有增广路。
- A2Q5：固定随机种子184332026，300个3…7点精确有理容量网络，含平行和反向原弧；每次枚举全部简单源汇路，从最少反向身份数的路随机取一条。另加一个强制先走s–a–b–t、下一次须用b–a反向身份的四点网络，总301张；210次实际增广（其中4次正反向成本）、单网络最多7次，逐阶段比较完整势不减、各路弧紧、同身份再临界尾距至少+1，并将最终流值与枚举全部源汇割的最小容量比较，全部一致。这些小实例未出现同一身份再次临界，因此该检查在本样本上没有直接提供再次临界事件的数值见证；其一般保证由上面的独立逻辑审读支持。这里只是小网络，不能把210这个值作为一般复杂度界。
- A4Q2：穷举3、4、5点全部264个二边连通简单图，实际耳构造后验证生成、连通无桥、边数≤2n−3；再枚举生成子图精确计算OPT并核对≤2OPT，全部成立。额外五点两三角形共点图实际使用闭合耳，输出全部6边，契合承诺归约反例。
- A4Q3(c)的渐近界通过上面的独立一般推理审读，不以小随机样本或代码替代。

## 可选清晰度建议及范围局限

两项不阻断的建议已消息发送父代理：A4Q2桥判据引用边Menger时可增加稳定标签`thm:mengeredge`；A2Q5的0–1队列实现可明确条目带距离快照、忽略旧/已确定条目，仅第一次确定时扫描出弧，以使“一次最终确定”实现说明更直接。当前数学证明无需这些措辞修订即可成立；报告绑定的是上述未改正文SHA，若正文修改，应复核变化并更新绑定。

未编译或查看最终主书PDF，没有声称完成排版/逐页视觉/目录链接、ZIP清洁重编、许可证终审或远端交付完整性验证。官方源题面实际查看与最终书PDF视觉是两件事。未另行重证复杂度理论和整套有限精度椭球基础定理。审读范围不含本次未收录的A3其余题及A4Q1，也不含其他课程册。

## 官方PDF绑定

- `sources/graph-theory/assessments/18433/pdf/a1.pdf`：`2e71f8a41d6cb73a3b90f82da81923c4d6050a08618aa1721dd98967f7abcb73`
- `sources/graph-theory/assessments/18433/pdf/a2.pdf`：`166f46de7c3e6a4e3c80a34fba62e70f441eae25ba0d5a02aa1a05bdd3a0f49d`
- `sources/graph-theory/assessments/18433/pdf/a3.pdf`：`01605dc2cf9ac2bf285954d70897525c8d07879f8f42a37db73bc1c5c3cb79d4`
- `sources/graph-theory/assessments/18433/pdf/a4.pdf`：`a0d1ea5e572f9b1885fddf01a2ba9186d8e8aa7b1dbec601ab3ced69e7c99d7f`

## 独立核对完整脚本

```python
from itertools import combinations,product
from fractions import Fraction
from collections import deque
import random,json,heapq
rng=random.Random(184332026)

def aug_paths(E,M,a,b):
 A=set(range(a));B=set(range(a,a+b));matched=set(sum(([u,v] for u,v in M),[]));out={u:[] for u in A|B}
 for u,v in E:
  if (u,v) in M:out[v].append(u)
  else:out[u].append(v)
 P=[]
 def rec(path):
  u=path[-1]
  if u in B and u not in matched:P.append(tuple(path));return
  for v in out[u]:
   if v not in path:rec(path+[v])
 for u in A-matched:rec([u])
 if not P:return []
 L=min(map(len,P));return [p for p in P if len(p)==L]
def edge_set(path,a):return {tuple(sorted((u,v))) for u,v in zip(path,path[1:])}
out={'shortest_phase':{'graphs':0,'matchings':0,'maximal_path_groups':0}}
for mask in range(512):
 E=[(u,3+v) for u in range(3) for v in range(3) if (mask>>(3*u+v))&1];out['shortest_phase']['graphs']+=1
 for ms in range(1<<len(E)):
  M={E[i] for i in range(len(E)) if (ms>>i)&1}
  ends=[v for e in M for v in e]
  if len(ends)!=len(set(ends)):continue
  out['shortest_phase']['matchings']+=1;P=aug_paths(E,M,3,3)
  if not P:continue
  for bits in range(1,1<<len(P)):
   chosen=[P[i] for i in range(len(P)) if (bits>>i)&1];verts=[v for p in chosen for v in p]
   if len(verts)!=len(set(verts)):continue
   used=set(verts)
   if any(not(set(p)&used) for p in P):continue
   new=set(M)
   for p in chosen:new.symmetric_difference_update(edge_set(p,3))
   Q=aug_paths(E,new,3,3);assert not Q or len(Q[0])>len(P[0]);out['shortest_phase']['maximal_path_groups']+=1

out['fewest_back_arcs']={'networks':0,'augmentations':0,'max_augmentations':0,'parallel_antiparallel_included':True,'positive_back_cost_augmentations':0,'recritical_events':0}
for case in range(301):
 n=rng.randrange(3,8);E=[]
 for u in range(n):
  for v in range(n):
   if u!=v and rng.random()<.28:
    for q in range(1+(rng.random()<.14)):E.append((u,v,Fraction(rng.randrange(0,13),rng.randrange(1,6))))
 if case==300:
  n=4;E=[(0,1,Fraction(1)),(0,2,Fraction(1)),(1,2,Fraction(1)),(1,3,Fraction(1)),(2,3,Fraction(1))]
 f=[Fraction(0)]*len(E);last={};augs=0
 def residual():
  R=[]
  for i,(u,v,c) in enumerate(E):
   if c>f[i]:R.append((u,v,0,i,1,c-f[i]))
   if f[i]>0:R.append((v,u,1,i,-1,f[i]))
  return R
 def distances(R):
  d=[float('inf')]*n;d[0]=0;Q=[(0,0)];adj=[[] for _ in range(n)]
  for e in R:adj[e[0]].append(e)
  while Q:
   q,u=heapq.heappop(Q)
   if q!=d[u]:continue
   for _,v,w,*_ in adj[u]:
    if q+w<d[v]:d[v]=q+w;heapq.heappush(Q,(d[v],v))
  return d
 while True:
  R=residual();d=distances(R);P=[];adj=[[] for _ in range(n)]
  for e in R:adj[e[0]].append(e)
  def paths(u,vs,es,cost):
   if u==n-1:
    if cost==d[-1]:P.append(es)
    return
   for e in adj[u]:
    if e[1] not in vs and cost+e[2]<=d[-1]:paths(e[1],vs|{e[1]},es+[e],cost+e[2])
  if d[-1]==float('inf'):break
  paths(0,{0},[],0);assert P;p=max(P,key=len) if case==300 and augs==0 else rng.choice(P);out['fewest_back_arcs']['positive_back_cost_augmentations']+=d[-1]>0;delta=min(e[-1] for e in p);augs+=1
  for u,v,w,i,sign,r in p:
   assert d[v]==d[u]+w
   if r==delta:
    ident=(i,sign)
    if ident in last:
     assert d[u]>=last[ident]+1;out['fewest_back_arcs']['recritical_events']+=1
    last[ident]=d[u]
   f[i]+=sign*delta
  dn=distances(residual());assert all(a<=b for a,b in zip(d,dn));assert augs<=2*n*len(E)
 val=sum(f[i] for i,e in enumerate(E) if e[0]==0)-sum(f[i] for i,e in enumerate(E) if e[1]==0)
 cuts=[]
 for mask in range(1<<(n-2)):
  S={0}|{u for u in range(1,n-1) if (mask>>(u-1))&1};cuts.append(sum((c for u,v,c in E if u in S and v not in S),Fraction(0)))
 assert val==min(cuts)
 out['fewest_back_arcs']['networks']+=1;out['fewest_back_arcs']['augmentations']+=augs;out['fewest_back_arcs']['max_augmentations']=max(augs,out['fewest_back_arcs']['max_augmentations'])

def connected(n,E):
 A=[set() for _ in range(n)]
 for u,v in E:A[u].add(v);A[v].add(u)
 seen={0};Q=[0]
 for u in Q:
  for v in A[u]-seen:seen.add(v);Q.append(v)
 return len(seen)==n
def bridgeless(n,E):return connected(n,E) and all(connected(n,E-{e}) for e in E)
def ear(n,E):
 A=[set() for _ in range(n)]
 for u,v in E:A[u].add(v);A[v].add(u)
 cycles=[]
 def rec(path):
  u=path[-1]
  for v in A[u]:
   if v==path[0] and len(path)>=3:cycles.append(path[:]);return
   if v not in path:rec(path+[v])
 rec([0]);cycle=min(cycles,key=lambda x:(len(x),x));V=set(cycle);H={tuple(sorted((u,v))) for u,v in zip(cycle,cycle[1:]+cycle[:1])}
 while len(V)<n:
  x=min(set(range(n))-V);C={x};Q=[x]
  for u in Q:
   for v in A[u]-(V|C):C.add(v);Q.append(v)
  cross=sorted((u,v) for u in V for v in A[u]&C);assert len(cross)>=2;(u,x),(v,y)=cross[:2]
  par={x:None};Q=[x]
  for z in Q:
   for w in A[z]&C:
    if w not in par:par[w]=z;Q.append(w)
  path=[y]
  while path[-1]!=x:path.append(par[path[-1]])
  path=path[::-1];H.add(tuple(sorted((u,x))));H.add(tuple(sorted((v,y))));H.update(tuple(sorted((a,b))) for a,b in zip(path,path[1:]));V.update(path)
 assert bridgeless(n,H) and len(H)<=2*n-3
 return H
out['ear_construction']={'graphs':0,'exact_opt_comparisons':0,'closed_ear_case':False}
for n in [3,4,5]:
 allE=list(combinations(range(n),2))
 for mask in range(1<<len(allE)):
  E={e for i,e in enumerate(allE) if (mask>>i)&1}
  if not bridgeless(n,E):continue
  H=ear(n,E);opt=None
  for k in range(n,len(E)+1):
   if any(bridgeless(n,set(S)) for S in combinations(E,k)):opt=k;break
  assert opt is not None and len(H)<=2*opt;out['ear_construction']['graphs']+=1;out['ear_construction']['exact_opt_comparisons']+=1
fig8={(0,1),(1,2),(0,2),(0,3),(3,4),(0,4)};H=ear(5,fig8);assert H==fig8 and len(H)==6;out['ear_construction']['closed_ear_case']=True
print(json.dumps(out,indent=2,ensure_ascii=False))
```
