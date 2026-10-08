# 18.433 Fall 2003 收录题目：作者初稿与自检记录

本记录是撰稿模型的自检，不是独立交叉审核，不是人类数学专家审定，也不是官方答案。另一独立代理及主代理复审尚待完成。本文件只涵盖冻结的15道原题、25个叶题；没有声称整册PDF、目录、最终ZIP或远端交付已验收。

## 绑定与来源

- 初稿：`subjects/graph-theory/assessments/18433/main.tex`，SHA256 `e3793c717e87e080f0c1cf6f134379cc4d0f76a95cae775248a46d0a2db10854`。
- 冻结范围：作业1题1–7，作业2题1–5，作业3题6，作业4题2–3。每题包含中文全题与编者独立解答，各有一个exercise、sourceof、solution；共15组。字母小问16个，未拆分整题9个，共25个叶题。
- 官方文件清单、版权与下载包核验详见 `assessments-inventory-18433.json`，SHA256 `b0ccf07ed041d373dc3bf8d96900ecc2d29ab24c961af4ea16783bc964866940`。课程网页与完整官方ZIP均未公开这四份作业的独立官方答案文件；原题先修与讲义的工作示例不冒称作业答案。
- 课程名称 Combinatorial Optimization，Santosh Vempala，Fall 2003。原PDF显示相应教师姓名，但无PDF Author字段，不推定每题独创作者。原课程学期与PDF创建于2004年分开登记。
- 官方ZIP资源逐文件许可元数据：CC BY-NC-SA 4.0。中文改编继承署名、非商业与相同方式共享条件；题目来源显示课程、学期、作业、题号、PDF页。没有嵌入英文PDF整页；题解与例图（本稿无图）为编者独立编写。

| 官方题面 | 页数 | SHA256 |
|---|---:|---|
| a1.pdf | 2 | `2e71f8a41d6cb73a3b90f82da81923c4d6050a08618aa1721dd98967f7abcb73` |
| a2.pdf | 1 | `166f46de7c3e6a4e3c80a34fba62e70f441eae25ba0d5a02aa1a05bdd3a0f49d` |
| a3.pdf | 2 | `01605dc2cf9ac2bf285954d70897525c8d07879f8f42a37db73bc1c5c3cb79d4` |
| a4.pdf | 1 | `a0d1ea5e572f9b1885fddf01a2ba9186d8e8aa7b1dbec601ab3ced69e7c99d7f` |

## 原题对应与条件台账

各标签均为`mit:18433-aN-qN`，原字母逐项对应，顺序未改。以下原页码从各PDF自身第一页计，不按合册页计。所有答案均非官方。

| 原作业及题号 | 原页 | 叶题 | 解答内容 | 原条件与编者说明 |
|---|---|---|---|---|
| A1 Q1 | 1 | 整题 | 二部图与奇圈；BFS分层及奇闭迹缩短 | 无实质补条件；有限无向简单图沿用本册 |
| A1 Q2 | 1 | (a)(b)(c) | 线性时间极大匹配；P4反例；二近似 | 极大与最大严格区分 |
| A1 Q3 | 1 | 整题 | 按权重降序贪心及双端充电证明 | 编者补非负边权；负权单边反例说明必要性 |
| A1 Q4 | 1 | (a)(b)(c) | 连通、Euler、二染色的正反证书 | Euler按非孤立顶点支撑连通；零边按空闭迹约定 |
| A1 Q5 | 1–2 | 整题 | 最短增广路批量后距离严格增长 | 原题任意增广路表述不真；明确补最短且极大顶点不交批，列8点反例 |
| A1 Q6 | 2 | 整题 | 独立集/顶点覆盖、匹配/边覆盖等式 | 原题无孤立点条件保留；空图单独约定 |
| A1 Q7 | 2 | (a)(b) | 独立集IP、二部图松弛整点性扰动证明 | 添加变量上下界以含孤立点；解释极点及非平凡凸组合 |
| A2 Q1 | 1 | 整题 | 有向点版Menger，点拆分单位容量及割/路径恢复 | 编者补无直接s→t弧及只删内部点；解释反例 |
| A2 Q2 | 1 | 整题 | 最大瓶颈路，索引堆及定点证明 | 非负容量；−∞区别无路与容量0路 |
| A2 Q3 | 1 | 整题 | 近小割严格计数及精确收缩概率 | 原题未写连通；补n≥2、连通、k≥1、2k整数、无序非平凡割；8孤立点反例 |
| A2 Q4 | 1 | 整题 | 瓶颈路/最大单边割的阈值证明 | 非负容量；有向割只数出弧；无路及空割最大值0 |
| A2 Q5 | 1 | 整题 | 最少回退弧增广，距离及临界身份不变量 | 从零流开始，每次瓶颈增广，保留残量身份；允许精确实数，不偷加整数条件 |
| A3 Q6 | 2 | (a)(b) | TSP割IP及LP强分离预言机、低维仿射空间接口 | 编者补n≥3与二进制有理输入；基础有理优化算法定理明确作为先修调用 |
| A4 Q2 | 1 | (a)(b) | 二边连通子图NP-hard、含闭耳的二近似 | 有限简单图n≥3；不可行先报告；桥/圈等价和可行承诺归约说明 |
| A4 Q3 | 1 | (a)(b)(c)(d) | 最大无圈子图近似/IP/间隙上确界2/最短圈LP分离 | 自环先删、平行及反向弧各保留身份；整数间隙LP/OPT且零边不取0/0 |

A3 Q6(b)及A4 Q3(d)精确调用“有理多面体强分离→精确线性优化”基础算法定理；正文给出行系数、编码长度、已知外界、低维仿射空间、可行性、精确有理最优点与恢复接口要求，并完整证明实际需要的图论分离算法及复杂度。有限精度有理椭球算法的全部证明作为原课线性优化先修明确依赖，不伪称已在这一题解内完成。A3还核完全图无向关联矩阵的秩及显式相对内点；A4给显式有理内立方体。若独立审核要求自足证明该基础算法，需要另设经专门审定的算法附录，不能用未经核验的误差界草率替代。

A4 Q3(c)的间隙下界为严格的概率存在证明：同时控制所有顶点次序、弧数和短圈数，删短圈后构造可行分数解，得到趋近2的有限图序列。明确“上确界为2”，不宣称所有有限实例达到2。A4 Q2同时处理输入预先承诺二边连通时的NP-hard归约，使用两个三角形共享一个顶点的固定否实例。

为核课堂背景，实际打开官方Fall 2003椭球讲义5页与分离预言机讲义3页的120dpi图像；这8页只作为原课工具背景证据，不作为完整有限精度算法证明。对应PDF SHA256分别为`21d93ae5f0cbc97ab2237126405b9f535bdcda502707af2edda7e0ab475eda66`、`d20bf23fdf4f49b3cce7c17a04f8321ffba46aa58fef0ed0affe164f8b95f6e5`。

## 有限精确验证

作者自编Python脚本使用整数及Fraction有理数。结果如下；这些计算用于抓取小图错误，不是任意规模的证明，不验证随机间隙构造的渐近存在性、Hamilton问题NP-complete性或有理优化基础定理。

```json
{
  "matching_cover_all_simple_graphs_n1_to5": 1099,
  "weighted_greedy_n4_edge_absent_0_1_3": 4096,
  "shortest_batch_bipartite_3x3": {
    "graphs": 512,
    "all_matchings": 5504,
    "maximal_batches_checked": 7080
  },
  "bipartite_LP_half_grid_n5": {
    "candidate_points": 15552,
    "feasible_fractional_rank_checks": 5314
  },
  "least_backward_flow": {
    "binary_networks_n4": 4096,
    "integer_networks_n5": 1000,
    "rational_networks_n5": 300,
    "seed": 184332003,
    "max_observed_augmentations": 7,
    "checks": "exact all-cut max-flow; conservation; capacity; distance monotonicity; repeated-critical tail increases"
  },
  "ear_construct_all_bridgeless_simple_graphs_n3_to5": 264,
  "near_cut_simple_graphs_n2_to5": {
    "connected_graphs": 771,
    "target_cut_exact_probabilities": 11098,
    "r_values": [
      2,
      3,
      4
    ]
  },
  "directed_cycle_oracle_n3_absent_0_half_1": 4096,
  "TSP_cut_oracle_n4_capacity_0_half_1": 729,
  "limitations": "Finite exact computations check selected formulas, constructions and invariants; do not prove arbitrary graphs, asymptotic random-gap existence, NP completeness, or the finite-precision ellipsoid foundation theorem."
}
```

额外手核并计算A1 Q5缺最短条件的8点反例：原最短增广路长3，选择长5且极大的顶点不交批后新最短仍长3；A2 Q3非连通反例的127个零割严格超过64。脚本与有限结果SHA256分别为`47769fbe0bc99a9fabdadace383f8c267fc5de401c29678fa1cb41a48a621b86`与`c4bd4ca0d58202a65630fcc52405f20be9b44440263a1dcd424d471e86bd1ad9`。下附原脚本，可直接从代码块复制后复算；临时运行路径不是最终交付文件。

## 临时编译与真实视觉覆盖

临时驱动由主册`main.tex`的document前导精确复制，仅输入本题组并添加临时审稿章名。模板没有换版，未编译/覆盖主册dist。驱动SHA256 `c398afa2d33c712809490960a42e63ec8639e94b4002c983b0f7508077dad7c2`。使用既有`TEXMFHOME=/tmp/graph-texmf`、`XDG_CACHE_HOME=/tmp/graph-font-cache`，XeLaTeX连续三轮，`-no-shell-escape -halt-on-error -interaction=nonstopmode`。

- 临时PDF `/tmp/18433-draft-build/draft.pdf`：12页，342139字节，SHA256 `5088591569ac0f389c26711b1edf5b1b0fb2a30a56925cb833cbde7c6be733af`。
- 三轮标准输出SHA256：`f39e2cba2d9833fec90d32766655e4392193bbb8c26b53cebdd89b4b3176c406`、`98f551df264991c73b2e186aa17730f205c96d748ae0debb0c4430de613c50a0`、`98f551df264991c73b2e186aa17730f205c96d748ae0debb0c4430de613c50a0`。最终log SHA256 `b3d76afa89acee54219096f491cb8a16f8a53bb2018781e08f52732739cf281d`。
- 无Overfull/Underfull、缺字、字体替换或未定义引用警告；仅有锁定适配类的filecontents覆盖临时文件提示。
- 130dpi渲染12页均逐张实际调用view_image打开并检查。第4–6页的首次批次因工具输出截断未计入覆盖，随后逐张重开。模型视觉检查不是人类校样。12页中文、公式、页眉、标题清楚，无发现公式越界/字体缺失/标签碰撞。第3页底部开始Q6题面并有两行正文，续至4页；此为正常续页，尚须按合册实际页重新检查。无TikZ图形。
- 以下hash绑定真实打开的当前临时PNG，不是主册最终分页；最终合册仍须完整逐页视觉、链接、干净重编及ZIP验收。

| 临时PNG | SHA256 | 实际视觉结论 |
|---|---|---|
| `page-01.png` | `260a40dd40fcda56eb5823df22461717f6bbcbaefd9d42719788ae075bdce2de` | 已实际打开；未发现版面缺陷 |
| `page-02.png` | `ecd31abb1db5d41cd7edf86f2cc0be54aa309bfaf0ce2756393242b49bcda5f4` | 已实际打开；未发现版面缺陷 |
| `page-03.png` | `4e4d47e7c2815296bb3da013354a9e13ec02890ae3a783e7e231b66cb866b4b8` | 已实际打开；未发现版面缺陷 |
| `page-04.png` | `3f2520e17bb81a7002f73b70b1c671ce0ff93593368b20fa444e1b046e5c52cb` | 已实际打开；未发现版面缺陷 |
| `page-05.png` | `f7eca9ce6ec3c3cf846a7a45b5abc59b60315f00aeb845f874ddfcf71bd9b652` | 已实际打开；未发现版面缺陷 |
| `page-06.png` | `f17106e14d45fff4cb759cd4c1b9fe0e16b53332a06104425a8c0d5930ae82e2` | 已实际打开；未发现版面缺陷 |
| `page-07.png` | `d084a799bbdda7968d53b59adf527631ff01f05ba31590475fa49423af55b9e2` | 已实际打开；未发现版面缺陷 |
| `page-08.png` | `8f8c0b639a13093ed401e01ff5e4bb1030011d54e7750918259fc12041762123` | 已实际打开；未发现版面缺陷 |
| `page-09.png` | `fd267de1c3be50373fe50eced164c18fc816d1c26d0173bb8c117c99eeffdd85` | 已实际打开；未发现版面缺陷 |
| `page-10.png` | `e40c4fc3fc44ba80b322f769a1647be989853f420514d95a1522686f4c6262b8` | 已实际打开；未发现版面缺陷 |
| `page-11.png` | `29a31677409c81de5e9bb690a38f8de8743f5fb81671bdfcde5d0778454015b9` | 已实际打开；未发现版面缺陷 |
| `page-12.png` | `c0cda5137e27008a364a8f739b01435cd32ee658ead35263bbe693334c31a00f` | 已实际打开；未发现版面缺陷 |

原有数学/视觉QA未编辑，当前SHA256仍分别为`aaedcfee8aa207a067d931a3603837245b3290470cd715f8c19deb0b2c6b5b2c`、`7a923087c9e9a20d5225c3c2a906e6e02c4659516b4f171c23d5a1f78b83fc2d`。本任务没有修改17章正文、主册模板、最终PDF、源码ZIP、根文件或远端。

## 复算脚本

```python
from itertools import combinations,product
from collections import deque
from functools import lru_cache
from fractions import Fraction as F
import heapq,random,json,time
R=random.Random(184332003);out={}
def undir_edges(n):return list(combinations(range(n),2))
def connected(n,edges):
 if n==0:return True
 a=[[] for _ in range(n)]
 for u,v in edges:a[u].append(v);a[v].append(u)
 seen={0};q=[0]
 for u in q:
  for v in a[u]:
   if v not in seen:seen.add(v);q.append(v)
 return len(seen)==n

def bridgeless(n,edges):return connected(n,edges) and all(connected(n,edges[:i]+edges[i+1:]) for i in range(len(edges)))
def matchings(edges):
 ans=[]
 def go(i,used,mask):
  if i==len(edges):ans.append(mask);return
  go(i+1,used,mask);u,v=edges[i]
  if not used&((1<<u)|(1<<v)):go(i+1,used|(1<<u)|(1<<v),mask|(1<<i))
 go(0,0,0);return ans
# Matching/cover equalities and weighted greedy.
c=0
for n in range(1,6):
 E=undir_edges(n)
 for bits in range(1<<len(E)):
  edges=[e for i,e in enumerate(E) if bits>>i&1];ms=matchings(edges);nu=max(x.bit_count() for x in ms)
  alpha=max(S.bit_count() for S in range(1<<n) if all(not(S>>u&1 and S>>v&1) for u,v in edges));tau=min(S.bit_count() for S in range(1<<n) if all(S>>u&1 or S>>v&1 for u,v in edges));assert alpha+tau==n
  if all(any(v in e for e in edges) for v in range(n)):
   rho=min(S.bit_count() for S in range(1<<len(edges)) if all(any(S>>i&1 and v in e for i,e in enumerate(edges)) for v in range(n)));assert nu+rho==n
  c+=1
out['matching_cover_all_simple_graphs_n1_to5']=c
E=undir_edges(4);c=0
for choice in product([-1,0,1,3],repeat=len(E)):
 edges=[e for e,w in zip(E,choice) if w>=0];weights=[w for w in choice if w>=0];used=set();value=0
 for i in sorted(range(len(edges)),key=lambda i:(-weights[i],i)):
  u,v=edges[i]
  if u not in used and v not in used:used|={u,v};value+=weights[i]
 opt=max(sum(w for i,w in enumerate(weights) if M>>i&1) for M in matchings(edges));assert 2*value>=opt;c+=1
out['weighted_greedy_n4_edge_absent_0_1_3']=c
# Hopcroft--Karp shortest maximal vertex-disjoint batches.
E=[(a,b) for a in range(3) for b in range(3,6)];stage_count=0;matching_count=0
for bits in range(1<<len(E)):
 edges=[e for i,e in enumerate(E) if bits>>i&1]
 def aug_paths(M):
  matched={v for i,e in enumerate(edges) if M>>i&1 for v in e};adj=[[] for _ in range(6)]
  for i,(u,v) in enumerate(edges):
   if M>>i&1:adj[v].append((u,i))
   else:adj[u].append((v,i))
  paths=[]
  def dfs(u,nodes,mask):
   if u>=3 and u not in matched:paths.append((len(nodes)-1,sum(1<<v for v in nodes),mask));return
   for v,i in adj[u]:
    if v not in nodes:dfs(v,nodes+[v],mask|(1<<i))
  for s in range(3):
   if s not in matched:dfs(s,[s],0)
  if not paths:return []
  L=min(p[0] for p in paths);return [p for p in paths if p[0]==L]
 for M in matchings(edges):
  matching_count+=1;ps=aug_paths(M)
  if not ps:continue
  L=ps[0][0]
  for S in range(1,1<<len(ps)):
   used=0;flip=0;valid=True
   for i,(_,vs,es) in enumerate(ps):
    if S>>i&1:
     if used&vs:valid=False;break
     used|=vs;flip^=es
   if not valid or any(not(S>>i&1) and not(used&vs) for i,(_,vs,_) in enumerate(ps)):continue
   new=M^flip;newps=aug_paths(new);assert not newps or newps[0][0]>L;stage_count+=1
out['shortest_batch_bipartite_3x3']={'graphs':512,'all_matchings':matching_count,'maximal_batches_checked':stage_count}
# Fractional points cannot be vertices in bipartite stable-set LP.
def rank(rows,n):
 a=[[F(x) for x in row] for row in rows];r=0
 for col in range(n):
  k=next((k for k in range(r,len(a)) if a[k][col]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=a[r][col];a[r]=[x/v for x in a[r]]
  for k in range(r+1,len(a)):
   if a[k][col]:v=a[k][col];a[k]=[x-v*y for x,y in zip(a[k],a[r])]
  r+=1
 return r
c=0;feas=0
E=[(a,b) for a in range(2) for b in range(2,5)]
for bits in range(64):
 edges=[e for i,e in enumerate(E) if bits>>i&1]
 for x in product([F(0),F(1,2),F(1)],repeat=5):
  c+=1
  if any(x[u]+x[v]>1 for u,v in edges) or all(v in (0,1) for v in x):continue
  rows=[]
  for v in range(5):
   if x[v] in (0,1):rows.append([int(i==v) for i in range(5)])
  for u,v in edges:
   if x[u]+x[v]==1:rows.append([int(i in (u,v)) for i in range(5)])
  assert rank(rows,5)<5;feas+=1
out['bipartite_LP_half_grid_n5']={'candidate_points':c,'feasible_fractional_rank_checks':feas}
# Least-backward residual augmentations, against all cuts; exact arithmetic.
def least_backward_flow(n,arcs):
 flows=[F(0) for _ in arcs];prior=[-1]*(2*len(arcs));steps=0;ds_old=None
 while True:
  res=[]
  for i,(u,v,c) in enumerate(arcs):
   if c>flows[i]:res.append((u,v,c-flows[i],0,i,2*i))
   if flows[i]>0:res.append((v,u,flows[i],1,i,2*i+1))
  ds=[10**9]*n;ds[0]=0
  for _ in range(n-1):
   change=False
   for u,v,c,w,i,j in res:
    if ds[u]+w<ds[v]:ds[v]=ds[u]+w;change=True
   if not change:break
  if ds_old is not None:assert all(a>=b for a,b in zip(ds,ds_old))
  if ds[-1]>=10**9:break
  adj=[[] for _ in range(n)]
  for e in res:
   u,v,c,w,i,j=e
   if ds[v]==ds[u]+w:adj[u].append(e)
  def path(u,seen):
   if u==n-1:return []
   for e in adj[u]:
    if e[1] not in seen:
     tail=path(e[1],seen|{e[1]})
     if tail is not None:return [e]+tail
  p=path(0,{0});assert p is not None;delta=min(e[2] for e in p)
  for u,v,c,w,i,j in p:
   if c==delta:
    assert ds[u]>=prior[j]+1 if prior[j]>=0 else True
    prior[j]=ds[u]
   flows[i]+=delta if w==0 else -delta
  assert all(0<=f<=c for f,(_,_,c) in zip(flows,arcs))
  for v in range(1,n-1):assert sum(f for f,(u,t,c) in zip(flows,arcs) if t==v)==sum(f for f,(s,u,c) in zip(flows,arcs) if s==v)
  steps+=1;assert steps<=2*n*len(arcs);ds_old=ds
 value=sum(f for f,(u,v,c) in zip(flows,arcs) if u==0)-sum(f for f,(u,v,c) in zip(flows,arcs) if v==0)
 opt=min(sum(c for u,v,c in arcs if S>>u&1 and not(S>>v&1)) for S in range(1<<n) if S&1 and not(S>>(n-1)&1));assert value==opt
 return steps
E=[(u,v) for u in range(4) for v in range(4) if u!=v];maxsteps=0
for bits in range(4096):maxsteps=max(maxsteps,least_backward_flow(4,[(u,v,F(1)) for i,(u,v) in enumerate(E) if bits>>i&1]))
for _ in range(1000):
 arcs=[(u,v,F(R.randrange(8))) for u in range(5) for v in range(5) if u!=v and R.random()<.45]
 if arcs and R.random()<.8:arcs.append(R.choice(arcs))
 maxsteps=max(maxsteps,least_backward_flow(5,arcs))
for _ in range(300):
 arcs=[(u,v,F(R.randrange(10),R.randrange(1,8))) for u in range(5) for v in range(5) if u!=v and R.random()<.4]
 maxsteps=max(maxsteps,least_backward_flow(5,arcs))
out['least_backward_flow']={'binary_networks_n4':4096,'integer_networks_n5':1000,'rational_networks_n5':300,'seed':184332003,'max_observed_augmentations':maxsteps,'checks':'exact all-cut max-flow; conservation; capacity; distance monotonicity; repeated-critical tail increases'}
# The constructive closed/open ear algorithm.
def ear(n,edges):
 def findpath(start,end,allowed,excluded=None):
  a=[[] for _ in range(n)]
  for i,(u,v) in enumerate(edges):
   if i==excluded or u not in allowed or v not in allowed:continue
   a[u].append((v,i));a[v].append((u,i))
  prev={start:None};q=[start]
  for u in q:
   if u==end:break
   for v,i in a[u]:
    if v not in prev:prev[v]=(u,i);q.append(v)
  assert end in prev;es=[];vs={end};v=end
  while v!=start:u,i=prev[v];es.append(i);vs.add(u);v=u
  return set(es),vs
 u,v=edges[0];hs,hv=findpath(u,v,set(range(n)),0);hs.add(0)
 while len(hv)<n:
  outside=set(range(n))-hv;start=min(outside);C={start};q=[start]
  for u in q:
   for a,b in edges:
    v=b if a==u else a if b==u else None
    if v is not None and v in outside and v not in C:C.add(v);q.append(v)
  cuts=[(i,a,b) if a in hv else (i,b,a) for i,(a,b) in enumerate(edges) if (a in hv and b in C) or (b in hv and a in C)];assert len(cuts)>=2
  i,u,x=cuts[0];j,v,y=cuts[1];ps,pv=findpath(x,y,C);hs|=ps|{i,j};hv|=pv
  hedges=[edges[i] for i in sorted(hs)];newn=len(hv);mp={v:i for i,v in enumerate(sorted(hv))};assert bridgeless(newn,[(mp[u],mp[v]) for u,v in hedges])
 assert len(hs)<=2*n-3;return len(hs)
c=0
for n in range(3,6):
 E=undir_edges(n)
 for bits in range(1<<len(E)):
  edges=[e for i,e in enumerate(E) if bits>>i&1]
  if bridgeless(n,edges):ear(n,edges);c+=1
out['ear_construct_all_bridgeless_simple_graphs_n3_to5']=c
# Near-min-cut exact count and stopped-contraction output probabilities.
c=0;targets=0
for n in range(2,6):
 E=undir_edges(n)
 for bits in range(1<<len(E)):
  edges=[e for i,e in enumerate(E) if bits>>i&1]
  if not connected(n,edges):continue
  cuts=[S for S in range(1,1<<n) if S&1 and S!=(1<<n)-1];sizes={S:sum(bool(S>>u&1)!=bool(S>>v&1) for u,v in edges) for S in cuts};lam=min(sizes.values())
  for r in [2,3,4]:
   near=[S for S in cuts if 2*sizes[S]<=r*lam];assert len(near)<n**r
   if r>n:continue
   for S in near:
    @lru_cache(None)
    def surv(parts):
     if len(parts)==r:return F(1,2**(r-1)-1)
     loc={v:i for i,P in enumerate(parts) for v in range(n) if P>>v&1};active=[(u,v) for u,v in edges if loc[u]!=loc[v]];total=F(0)
     for u,v in active:
      if bool(S>>u&1)!=bool(S>>v&1):continue
      i,j=loc[u],loc[v];new=tuple(sorted([P for k,P in enumerate(parts) if k not in (i,j)]+[parts[i]|parts[j]]));total+=surv(new)/len(active)
     return total
    prob=surv(tuple(1<<v for v in range(n)));import math
    assert prob>=F(1,math.comb(n,r)*(2**(r-1)-1));targets+=1
  c+=1
out['near_cut_simple_graphs_n2_to5']={'connected_graphs':c,'target_cut_exact_probabilities':targets,'r_values':[2,3,4]}
# Directed cycle separation vs complete simple-cycle enumeration, n3.
E=[(u,v) for u in range(3) for v in range(3) if u!=v];c=0
for vals in product([None,F(0),F(1,2),F(1)],repeat=6):
 es=[(u,v,x) for (u,v),x in zip(E,vals) if x is not None];adj=[[] for _ in range(3)]
 for u,v,x in es:adj[u].append((v,1-x))
 cycles=[]
 def dfs(start,u,seen,w):
  for v,y in adj[u]:
   if v==start:cycles.append(w+y)
   elif v not in seen:dfs(start,v,seen|{v},w+y)
 for v in range(3):dfs(v,v,{v},F(0))
 direct=min(cycles,default=F(999));d=[[F(999)]*3 for _ in range(3)]
 for v in range(3):d[v][v]=0
 for u,v,x in es:d[u][v]=min(d[u][v],1-x)
 for k in range(3):
  for u in range(3):
   for v in range(3):d[u][v]=min(d[u][v],d[u][k]+d[k][v])
 oracle=min((1-x+d[v][u] for u,v,x in es if d[v][u]<999),default=F(999));assert oracle==direct;c+=1
out['directed_cycle_oracle_n3_absent_0_half_1']=c
# TSP separation root all sinks vs all undirected cuts, n4.
E=undir_edges(4);c=0
for xs in product([F(0),F(1,2),F(1)],repeat=6):
 cut=lambda S:sum(x for (u,v),x in zip(E,xs) if bool(S>>u&1)!=bool(S>>v&1))
 direct=min(cut(S) for S in range(1,15));roots=min(min(cut(S) for S in range(1,15) if S&1 and not(S>>t&1)) for t in [1,2,3]);assert direct==roots
 for t in [1,2,3]:
  order=[0]+[v for v in range(1,4) if v!=t]+[t];mp={v:i for i,v in enumerate(order)};arcs=[]
  for (u,v),x in zip(E,xs):arcs.extend([(mp[u],mp[v],x),(mp[v],mp[u],x)])
  least_backward_flow(4,arcs)
 c+=1
out['TSP_cut_oracle_n4_capacity_0_half_1']=c
out['limitations']='Finite exact computations check selected formulas, constructions and invariants; do not prove arbitrary graphs, asymptotic random-gap existence, NP completeness, or the finite-precision ellipsoid foundation theorem.'
open('/tmp/18433-draft-finite-checks.json','w').write(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

```
