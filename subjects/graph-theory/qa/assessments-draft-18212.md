# 18.212 冻结课程作业初稿记录

本记录是写者自查，不是独立数学交叉审稿，也不是人类专家鉴定。按 math-lecture-writing 的 review-gates 分开数学正文、有限计算、来源与临时版面 evidence。父代理安排另一个独立代理阅读全文后，才可登记独立审读。

## 绑定正文与范围

- 正文：`subjects/graph-theory/assessments/18212/main.tex`
- 当前正文 SHA-256：`dab99503ea0e31a2d42d4bfe11f7d44f0b3526ecbda327ab77dc875a641f3c81`
- 原題19道：PSet1 Q2、3、10、12、19；PSet2 Q7、9；PSet3 Q1–11、14。19个exercise、19个solution；PSet3 Q4包含两条恒等式，按解答目标为20个单元。
- 没有收录边界候选PSet1Q18、PSet2Q14；没有改写其他学科、主书模板、章正文、全局清单、根README、主PDF/ZIP，也没有远端写入。
- 所有题保留原题号标签，标签形式 `mit:18212-pset3-q1`。仅简体中文原生LaTeX重编，未嵌英文PDF页。
- 本分册片段本身不重定义环境和模板，临时编译复制既有graph-theory主文件前导，与probability锁定模板同系。

## 官方答案映射

官方作者为Alexander Postnikov（题面），Andrew Lin为官方课堂解答记录者；学生署名按对应条目保留。课程年份2019。原卷共5页（4页题面+1页许可），来源逐文件许可和元数据证据已在 `qa/assessments-inventory-18212.json` 登记，许可CC BY-NC-SA 4.0。下表的解答编号是答案文件内部重编号，不是原PSet题号。

| 原卷原题 | 本稿标签 | 官方答案参考 |
|---|---|---|
| PSet1 Q2 | `mit:18212-pset1-q2` | 无公开对应官方答案；编者独立补解 |
| PSet1 Q3 | `mit:18212-pset1-q3` | SolII局部4，第2–3页 |
| PSet1 Q10 | `mit:18212-pset1-q10` | SolII局部6，第3页 |
| PSet1 Q12 | `mit:18212-pset1-q12` | SolII局部5，第3页 |
| PSet1 Q19 | `mit:18212-pset1-q19` | 无公开对应官方答案；编者独立补解 |
| PSet2 Q7 | `mit:18212-pset2-q7` | 无公开对应官方答案；编者独立补解 |
| PSet2 Q9 | `mit:18212-pset2-q9` | SolI局部4，第2页 |
| PSet3 Q1 | `mit:18212-pset3-q1` | Sol局部1，第1页 |
| PSet3 Q2 | `mit:18212-pset3-q2` | 无公开对应官方答案；编者独立补解 |
| PSet3 Q3 | `mit:18212-pset3-q3` | 无公开对应官方答案；编者独立补解 |
| PSet3 Q4 | `mit:18212-pset3-q4` | Sol局部3，第2–3页，两条恒等式 |
| PSet3 Q5 | `mit:18212-pset3-q5` | Sol局部4，第3页 |
| PSet3 Q6 | `mit:18212-pset3-q6` | 无公开对应官方答案；编者独立补解 |
| PSet3 Q7 | `mit:18212-pset3-q7` | 无公开对应官方答案；编者独立补解 |
| PSet3 Q8 | `mit:18212-pset3-q8` | Sol局部2，第1页，≤k误印at least已纠正 |
| PSet3 Q9 | `mit:18212-pset3-q9` | Sol局部6，第4页，仅二叉树↔Dyck详述，其他为编者补解 |
| PSet3 Q10 | `mit:18212-pset3-q10` | 无公开对应官方答案；编者独立补解 |
| PSet3 Q11 | `mit:18212-pset3-q11` | 无公开对应官方答案；编者独立补解 |
| PSet3 Q14 | `mit:18212-pset3-q14` | 无公开对应官方答案；编者独立补解 |

9道题有公开官方答案参考，10道没有对应公开官方答案。9道中的简述和缺口均没有误称为完整官方答案；特别是PSet3Q9只有一个双射在官方文件里展开，本稿树↔停车的递归构造和其他逆算法是编者补足。PSet3Q8题面明确≤k，答案第1页的at least是原文误写，不按误写造题。

## 写者一般证明自查

- PSet1Q2：有限吸收区间解、边界唯一性、递增事件并集、无穷区间极限，p=0、1及p=1/2分开；Q3：初始段反射的逆映射、可达奇偶条件，偏置路径权重与计数分开。
- PSet1Q10：两长度都以指定位置结尾，编码两两异；Q12：根为最小、祖先先于后代，归纳交错计数，不扩大为任意树边定向的偏序；Q19：括号配对后未配对串变换，证明平衡块配对稳定并提供实际对合逆算法。
- PSet2Q7：正文已证Kőnig作为明确基点，匹配变路径链、链变匹配、最小覆盖变反链；不循环引用Dilworth本身。
- PSet2Q9：共同覆盖的非对角项和可加/可删角差1分别证明DU−UD=I；形式指数运算的局部有限性、正规排序及形式微分方程唯一性均展开，再独立计K2n完美匹配数。原题只要求数目等式，未谎称算子推导提供双射。
- PSet3Q1：删除部的顺序由剩余大小唯一决定，指定部叶存在；任意词对的解码候选存在、邻点仍存活、所得树连通、相应度数=未读次数+1保证两向互逆。
- PSet3Q2：矩阵树谱乘积式系数推导及三部空间全部维数；Q3允许旧G不连通，常数方向与其正交补清楚，不在x=0非法除法。
- PSet3Q4：出树采用反图出度Laplacian，原入度矩阵重算对角，不直接转置；A→B删加边的两分支分解；负幂端点统一为H0=1；第一式归纳及有限差分本地证明。
- PSet3Q5：字符正交基和全部立方体特征值本地证明；BEST依正文完整证明，指定首弧与循环转动一一对应，不识别反向/自同构，n=1、2核对。
- PSet3Q6：有限连通无自环立方体n≥1、不同端点、单位注入/接地、坐标置换唯一性、切集电流总和；通勤核对采用体积n2^n。Q7：吸收几乎必然的统一概率窗口证明、两边界、差分归一化，端点k=0,n和n=1包含。
- PSet3Q8：成功停车→可行排列→尾段容量→排序的可行排列；交换维护未到车/空位可行分配，给出原顺序的贪心成功证明。
- PSet3Q9：全部4类对象组成双射链，每条均有逆算法。树递归中内树非根顶点B\{v}与内停车汽车B\{n}使用相同序位但并非同一集合，正文明确区别，逆向空位j恢复B及v。Q10逐点证明反序与停车位移均分成内、外及r，不仅以递推等势代替双射。正文列n=2三棵树及n=3有2反序的树/停车例子。
- PSet3Q11：已读父代理写出的18.315 HW3Q3/Q4全文，使用同册稳定标签，根0全标号+1后根1仍最小，点数为n+1。两前题分别完整证明fn(q)=TKn(1,q)、TKn+1(1,−1)=An，保留18.212独立映射。
- PSet3Q14：Catalan路径数的反射、有限DAG、展开行列式的首次相交尾交换反号对合、非恒等端点排列必相交、唯一嵌套山形全部本地证明。

## 已实际运行的有限核对

以下是写者编写并实际运行的程序，不是独立模型审稿；有限例子不能替代上述一般证明。两个脚本全文收录在本记录末尾，方便从Markdown提取重跑。

- 临时脚本 `/tmp/check-18212-bijections.py`，SHA-256 `d105d4891a552c911e5a6aa47cce233f7ed1c94e8b298d75b45f1256c2532c36`；实际输出 `/tmp/check-18212-bijections.json`，SHA-256 `6ff9ec2637af5a1ada0d1885e0c7a0a5c3fd013a58b543b532ffc10cd7c733fd`。
- 临时脚本 `/tmp/check-18212-finite.py`，SHA-256 `8fcf3e9d725cd9220cda88570bcef223d1fb2ff4a358769ad1c99103df60647f`；实际输出 `/tmp/check-18212-finite.json`，SHA-256 `a2f622f5f7d4d73351c2b7158484a1084703ee67dcdbda34c53b10f7442e56d7`。

树—停车函数：n=1…6，各自枚举全部带标号树和全部n^n希望函数，再筛选停车成功者；逐个验证编码合法、反解精确恢复原边集、不重复、所有停车函数覆盖、反序数=位移。

| n | 树/停车函数数 | 反序多项式从常数项起的系数 |
|---|---:|---|
| 1 | 1 | [1] |
| 2 | 3 | [2, 1] |
| 3 | 16 | [6, 6, 3, 1] |
| 4 | 125 | [24, 36, 30, 20, 10, 4, 1] |
| 5 | 1296 | [120, 240, 270, 240, 180, 120, 70, 35, 15, 5, 1] |
| 6 | 16807 | [720, 1800, 2520, 2730, 2520, 2100, 1610, 1140, 750, 455, 252, 126, 56, 21, 6, 1] |

- 包含双射：全部长度1…12的0–1串，逐个检查对合、互补层大小、低层集合包含关系。长度12共4096串。
- 二部树编码：1≤m,n≤4的16组，任意词对均解码且反编码精确恢复，同时独立穷举全部Prüfer树筛出二部树比较集合；K4,4有4096棵。
- Young格闭游走：从真实相邻分拆逐步动态计数，n=0…7得到 `[1,1,3,15,105,945,10395,135135]`，与完美匹配闭式一致。
- 三部树：m,n,k=1…3全部27组，以实际Laplacian余子式求行列式核对；K3,3,3得到419904。
- 立方体电阻：n=1…5，以完整Laplacian接地主子矩阵精确解电位，得到 `1,1,5/6,2/3,8/15`，与分层公式一致；没有把分层公式自代入当作独立计算。
- 立方体Euler：n=1、2从固定首弧直接递归枚举全部弧序列，得到1、4，核对BEST计数惯例。
- 两条Abel恒等式：n=0…6，用符号多项式展开核对，端点按H0=1处理。
- Catalan矩阵：n=1…9精确行列式均为1。
- 首次命中：i0=1…4、m=1…12逐步路径计数，不允许提前触0，核对反射闭式。
- 补图树多项式：n=1…4所有75个简单图，实际两个Laplacian行列式除共同因子x，核对多项式互反式。

## 临时版面与未完成范围

实际复制主书前导在 `/tmp/18212-draft-build/main.tex` 做原生XeLaTeX临时检查；使用现有 `TEXMFHOME=/tmp/graph-texmf`，无安装升级，未覆盖本册build/dist。连续两次编译成功，临时PDF为14页，没有Overfull、Missing character或TeX错误。临时导入旧主书aux可显示既有正文引用，18315新题引用尚未在旧aux中，所以有4条相关未定义引用警告；它们目标标签已实读存在，最终全书仍需重新编译解析。

实际查看14页的三张联系表，未见裁切/页眉冲突/公式溢出；另打开第7、11、13页完整渲染核对Abel矩阵、递归定义和行列式路径式。这里只是临时草稿版面查看，不能代替最终整册逐页视觉、目录链接/交叉链接检查；未声称ZIP清洁重编、远端完整性或版权终审。正文无新增插图。最终书PDF、页数、链接、ZIP、远端和独立审读由父代理统一完成。

## 绑定官方PDF及共享证明

- `sources/graph-theory/assessments/18212/originals/pset1.pdf`：`25c13409a5e6c0aec298e25a322ad21a6e801d40a4b59481fecb3987823e3132`
- `sources/graph-theory/assessments/18212/originals/pset2.pdf`：`501e5fdc50401dd2c465f371ed933b5f01bc87f106ee2d33fcc3bb1dd9fc3e0f`
- `sources/graph-theory/assessments/18212/originals/pset3.pdf`：`e0e73cf8e4c26ddef2615f1c1d371a80f9e7857828aa7684e80ae9d8ba4e211b`
- `sources/graph-theory/assessments/18212/originals/pset1_solnii.pdf`：`76ce4b89847d40071938e5ed1a539d066b65d8e57c5e811bca86f285d27ac168`
- `sources/graph-theory/assessments/18212/originals/pset2_solni.pdf`：`a7ed913e28e46562fa6cd674d6fe94b823580528fa7684a6fa686cc6c0282389`
- `sources/graph-theory/assessments/18212/originals/pset3_soln.pdf`：`24b9395ada7e3b8d58ab9e9c868c440ea22b4500904f5219400ce908071f3a9c`
- 已阅共享证明文件 `subjects/graph-theory/assessments/18315/hw3.tex`：`fe6e82e34fa2560c9a7eae3b4a987d2196efce3ffdfd78b609076230ec10ebe3`（只审读Q3/Q4的引用支持，不声称对该文件其余题作独审）。

## 可复跑脚本：check-18212-bijections

```python
from itertools import product,combinations
from heapq import heapify,heappush,heappop
from collections import deque,Counter
import json,hashlib

def prufer_tree(code,N):
 deg=[1]*N
 for x in code:deg[x]+=1
 leaves=[x for x in range(N) if deg[x]==1];heapify(leaves);E=[]
 for x in code:
  l=heappop(leaves);E.append(tuple(sorted((l,x))));deg[l]-=1;deg[x]-=1
  if deg[x]==1:heappush(leaves,x)
 if N>1:E.append(tuple(sorted((heappop(leaves),heappop(leaves)))))
 return tuple(sorted(E))
def adj(E,n):
 a=[set() for _ in range(n+1)]
 for u,v in E:a[u].add(v);a[v].add(u)
 return a

def forward(E,n):
 if n==0:return ()
 a=adj(E,n);par={0:None};q=[0]
 for u in q:
  for v in a[u]:
   if v not in par:par[v]=u;q.append(v)
 v=n
 while par[v]!=0:v=par[v]
 B=set();stack=[v]
 while stack:
  u=stack.pop();B.add(u);stack.extend(x for x in a[u] if x!=par[u])
 j=len(B);r=sum(b<v for b in B);C=sorted(set(range(1,n+1))-B)
 left={v:0,**{b:k+1 for k,b in enumerate(sorted(B-{v}))}};right={0:0,**{b:k+1 for k,b in enumerate(C)}}
 EL=tuple(sorted(tuple(sorted((left[x],left[y]))) for x,y in E if x in B and y in B))
 ER=tuple(sorted(tuple(sorted((right[x],right[y]))) for x,y in E if x in right and y in right))
 g=forward(EL,j-1);h=forward(ER,n-j);f=[0]*n
 for b,t in zip(sorted(B-{n}),g):f[b-1]=t
 for b,t in zip(C,h):f[b-1]=j+t
 f[n-1]=j-r
 return tuple(f)
def park(f):
 S=set(range(1,len(f)+1));spots=[]
 for p in f:
  cand=[x for x in S if x>=p]
  if not cand:return None
  x=min(cand);S.remove(x);spots.append(x)
 return spots

def inverse(f):
 n=len(f)
 if n==0:return ()
 avail=set(range(1,n+1));spots=[]
 for p in f[:-1]:
  x=min(x for x in avail if x>=p);avail.remove(x);spots.append(x)
 j=next(iter(avail));S=[i+1 for i,x in enumerate(spots) if x<j];C=[i+1 for i,x in enumerate(spots) if x>j];B=sorted(S+[n]);r=j-f[-1];v=B[r]
 g=tuple(f[i-1] for i in S);h=tuple(f[i-1]-j for i in C)
 lm={0:v,**{k+1:b for k,b in enumerate(x for x in B if x!=v)}};rm={0:0,**{k+1:b for k,b in enumerate(C)}}
 E=[tuple(sorted((0,v)))]
 E.extend(tuple(sorted((lm[x],lm[y]))) for x,y in inverse(g))
 E.extend(tuple(sorted((rm[x],rm[y]))) for x,y in inverse(h))
 return tuple(sorted(E))
def inv(E,n):
 a=adj(E,n);par={0:None};q=[0]
 for u in q:
  for v in a[u]:
   if v not in par:par[v]=u;q.append(v)
 total=0
 for i in range(1,n+1):
  v=par[i]
  while v is not None:
   total+=v>i;v=par[v]
 return total

def bracket(s):
 stack=[];paired=set()
 for i,b in enumerate(s):
  if b:stack.append(i)
  elif stack:
   j=stack.pop();paired.update([i,j])
 un=[i for i in range(len(s)) if i not in paired];a=sum(s[i]==0 for i in un);b=len(un)-a;t=list(s)
 for i,x in zip(un,[0]*b+[1]*a):t[i]=x
 return tuple(t)

def bip_encode(E,m,n):
 A=set(range(m));B=set(range(m,m+n));adjc={x:set() for x in A|B}
 for u,v in E:adjc[u].add(v);adjc[v].add(u)
 aa=[];bb=[]
 while len(A)+len(B)>2:
  side=A if len(A)>=len(B) else B;l=min(x for x in side if len(adjc[x])==1);v=next(iter(adjc[l]));(bb if l in A else aa).append(v);side.remove(l);adjc[v].remove(l);del adjc[l]
 return tuple(aa),tuple(bb)
def bip_decode(aa,bb,m,n):
 A=set(range(m));B=set(range(m,m+n));ia=ib=0;E=[]
 while len(A)+len(B)>2:
  if len(A)>=len(B):l=min(A-set(aa[ia:]));v=bb[ib];ib+=1;A.remove(l)
  else:l=min(B-set(bb[ib:]));v=aa[ia];ia+=1;B.remove(l)
  E.append(tuple(sorted((l,v))))
 E.append(tuple(sorted((next(iter(A)),next(iter(B))))));return tuple(sorted(E))

out={'tree_parking':[],'bracket':[],'bipartite':[]}
for n in range(1,7):
 seen=set();poly=Counter()
 for code in product(range(n+1),repeat=n-1):
  E=prufer_tree(code,n+1);f=forward(E,n);assert park(f) is not None;assert inverse(f)==E;assert inv(E,n)==n*(n+1)//2-sum(f);assert f not in seen;seen.add(f);poly[inv(E,n)]+=1
 pfs={f for f in product(range(1,n+1),repeat=n) if park(f) is not None};assert seen==pfs
 out['tree_parking'].append({'n':n,'trees':len(seen),'parking_functions':len(pfs),'inversion_coefficients':[poly[k] for k in range(max(poly)+1)]})
for n in range(1,13):
 cnt=0
 for s in product([0,1],repeat=n):
  t=bracket(s);assert bracket(t)==s;assert sum(t)==n-sum(s)
  if sum(s)<=n/2:assert all(not x or y for x,y in zip(s,t))
  cnt+=1
 out['bracket'].append({'n':n,'words':cnt})
for m in range(1,5):
 for n in range(1,5):
  pairs=set()
  for aa in product(range(m),repeat=n-1):
   for bb in product(range(m,m+n),repeat=m-1):
    E=bip_decode(aa,bb,m,n);assert all((u<m)!=(v<m) for u,v in E);assert bip_encode(E,m,n)==(aa,bb);assert E not in pairs;pairs.add(E)
  trees={prufer_tree(c,m+n) for c in product(range(m+n),repeat=m+n-2) if all((u<m)!=(v<m) for u,v in prufer_tree(c,m+n))}
  assert pairs==trees
  out['bipartite'].append({'m':m,'n':n,'trees':len(pairs)})
print(json.dumps(out,indent=2,ensure_ascii=False))
```

## 可复跑脚本：check-18212-finite

```python
import sympy as s
from itertools import product,combinations
from math import comb,factorial
from fractions import Fraction
import json

def lap(adj):
 N=len(adj);return s.Matrix([[sum(adj[i]) if i==j else -adj[i][j] for j in range(N)] for i in range(N)])
def young_add(l):
 z=[]
 for i in range(len(l)+1):
  if i==len(l):z.append(l+(1,))
  elif i==0 or l[i-1]>l[i]:z.append(l[:i]+(l[i]+1,)+l[i+1:])
 return z
def young_del(l):
 z=[]
 for i,a in enumerate(l):
  if i==len(l)-1 or a>l[i+1]:
   t=l[:i]+(a-1,)+l[i+1:];z.append(tuple(x for x in t if x))
 return z
out={}
D={():1};walk=[]
for r in range(15):
 if r%2==0:
  n=r//2;v=D.get((),0);assert v==factorial(2*n)//(2**n*factorial(n));walk.append(v)
 nxt={}
 for l,c in D.items():
  for q in young_add(l)+young_del(l):nxt[q]=nxt.get(q,0)+c
 D=nxt
out['young_closed_walks_n0_to7']=walk
out['tripartite_cases']=[]
for m,n,k in product(range(1,4),repeat=3):
 N=m+n+k;parts=[0]*m+[1]*n+[2]*k;A=[[int(parts[i]!=parts[j]) for j in range(N)] for i in range(N)];v=lap(A)[:-1,:-1].det();expected=N*(n+k)**(m-1)*(m+k)**(n-1)*(m+n)**(k-1);assert v==expected;out['tripartite_cases'].append([m,n,k,int(v)])
out['cube_resistance']=[]
for n in range(1,6):
 N=2**n;A=[[int((i^j).bit_count()==1) for j in range(N)] for i in range(N)];L=lap(A);M=L[:-1,:-1];rhs=s.zeros(N-1,1);rhs[0]=1;v=(M.inv()*rhs)[0];expected=sum((Fraction(1,comb(n-1,k)) for k in range(n)),Fraction(0))/n;assert v==s.Rational(expected.numerator,expected.denominator);out['cube_resistance'].append(str(v))
# Euler words from the fixed first arc (0,1), without quotienting reversal.
out['cube_euler_n1_n2']=[]
for n in [1,2]:
 N=2**n;E=[(i,j) for i in range(N) for j in range(N) if (i^j).bit_count()==1];first=E.index((0,1));count=[0]
 def rec(v,used):
  if len(used)==len(E):count[0]+=v==0;return
  for e,(a,b) in enumerate(E):
   if a==v and e not in used:rec(b,used|{e})
 rec(1,{first});tau=lap([[int((i^j).bit_count()==1) for j in range(N)] for i in range(N)])[:-1,:-1].det();assert count[0]==tau*factorial(n-1)**N;out['cube_euler_n1_n2'].append(count[0])
x,y,z=s.symbols('x y z');H=lambda n,t:1 if n==0 else t*(t+n*z)**(n-1)
for n in range(7):
 assert s.expand(sum(comb(n,k)*H(k,y)*(x-k*z)**(n-k) for k in range(n+1))-(x+y)**n)==0
 assert s.expand(sum(comb(n,k)*H(k,x)*H(n-k,y) for k in range(n+1))-H(n,x+y))==0
out['abel_symbolic_n0_to6']=True
out['catalan_hankel_n1_to9']=[]
C=lambda r:comb(2*r,r)//(r+1)
for n in range(1,10):
 v=s.Matrix([[C(i+j+1) for j in range(n)] for i in range(n)]).det();assert v==1;out['catalan_hankel_n1_to9'].append(int(v))
for i0 in range(1,5):
 paths={i0:1}
 for m in range(1,13):
  nxt={};hit=0
  for i,c in paths.items():
   for j in [i-1,i+1]:
    if j==0:hit+=c
    else:nxt[j]=nxt.get(j,0)+c
  paths=nxt;expected=0 if m<i0 or (m-i0)%2 else Fraction(i0,m)*comb(m,(m-i0)//2);assert hit==expected
out['first_hit_counts_i1_to4_m1_to12']=True
out['complement_polynomial_graphs']=0
for n in range(1,5):
 edges=list(combinations(range(n),2))
 for mask in range(2**len(edges)):
  A=[[0]*n for _ in range(n)]
  for e,(i,j) in enumerate(edges):A[i][j]=A[j][i]=(mask>>e)&1
  B=[[int(i!=j and not A[i][j]) for j in range(n)] for i in range(n)]
  F=s.cancel((lap(A)+x*s.eye(n)).det()/x);G=s.cancel((lap(B)+x*s.eye(n)).det()/x);assert s.expand(G-(-1)**(n-1)*F.subs(x,-x-n))==0;out['complement_polynomial_graphs']+=1
print(json.dumps(out,indent=2,ensure_ascii=False))
```

## 合册纯排版返修

2026-10-08：PSet 1 Q12 行内树钩长公式删除 `\displaystyle`，恢复模板正常行内运算符高度；题面、公式内容与数学解答均未改动。上面的作者冻结 SHA 已同步更新。此次修改仍须已审者核对差异后更新独立审查绑定。
