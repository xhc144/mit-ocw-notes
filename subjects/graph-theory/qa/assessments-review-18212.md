# 18.212 Spring 2019：19道收录题独立数学审核

2026-10-08独立审核代理完整只读审查477行题稿的全部19道原题及全部请求，未参与撰写，不编辑原稿。结合官方题面/课堂解答与另写的精确复算，未发现实质数学缺口或待修问题。本记录是独立模型审读，不是人类数学专家审定；作者自检不代替此审核，本文小规模计算也不代替一般证明。没有审定整册PDF视觉、目录链接、最终源码ZIP或远端交付。

## 最终哈希与范围

- 稿件 `subjects/graph-theory/assessments/18212/main.tex`，SHA256 `dab99503ea0e31a2d42d4bfe11f7d44f0b3526ecbda327ab77dc875a641f3c81`，最终机械复核与下述纯排版差异校验完成。
- 原题：PSet1 Q2,3,10,12,19；PSet2 Q7,9；PSet3 Q1–11及Q14。共19道原题；Q4两条无字母恒等式均解答。Q9四集合间完整双射链均覆盖，不把四集合或等价条件虚算为原题字母小问。
- 来源inventory `assessments-inventory-18212.json`，SHA256 `758203a1f5d479da8b3eaf6d60b3e58e49b795e8f5a872e27670f84bec580014`。其初调查的selection_frozen/phase字段说明该文件登记时状态；实际本审核范围以上述父代理后续冻结清单为准，未修改原清单。
- 课程 Algebraic Combinatorics，Alexander Postnikov，Spring 2019；课堂Solutions由Andrew Lin记录，部分注明学生展示姓名。题稿明确官方已贴局部答案与编者独立补解，没有将后者称官方答案。
- 稿件引用同册18.315 HW3 Q3、Q4的完整证明；共同依赖稿 `hw3.tex` SHA256 `fe6e82e34fa2560c9a7eae3b4a987d2196efce3ffdfd78b609076230ec10ebe3`，已在本代理独立基础审核中完整核查。

2026-10-08合册排版lint后的重新绑定：PS1 Q12第74行的行内钩长公式仅删去displaystyle命令。逐字机械恢复该命令后，整个稿件恰得到上轮已独审SHA256 `29604b2e3bff224ec916e63243156796253e0338c4f2adb73bd592fa1929ecf2`。故题面、公式数学内容、证明、19题映射、例与其他行均未变，原独立数学结论保持；原复算结果适用。以上是源码差异核查，没有冒称本轮已重看最终PDF页。

## 逐题审核

| 原题 | 稿中解答行 | 数学核查结果 |
|---|---|---|
| PS1 Q2 | 12–31 | 有限[0,N]吸收先证明概率1；调和方程唯一性与解成立；事件随N递增并趋于最终命中0，p=0,1及p=1/2边界全处理。 |
| PS1 Q3 | 40–57 | 删最后左步后从i0到1；坏路径反射为从−i0到1，右步数ℓ精确，计数差=(i0/m)binom(m,r)。反射只计数不混淆偏置概率；奇偶、长度和0^0边界一致。 |
| PS1 Q10 | 66–68 | 以指定位置结尾的LIS/LDS编码所有有序对不同，鸽笼矛盾成立，条件正整数和元素互异明示。 |
| PS1 Q12 | 78–88 | 根最小的树偏序祖先方向明确，子树线性扩张交错唯一，多项式系数与h(root)=n给钩长。没有推给任意树边定向；n=1正确。 |
| PS1 Q19 | 97–106 | LIFO括号配对、未配对0^a1^b、a≥b及包含性正确；配对不跨未配对位保证改串保持配对，变换真正为对合，端点n=2k恒等。 |
| PS2 Q7 | 117–122 | 比较图最大匹配到链分划的路径/孤点双向转换给N−ν；Kőnig覆盖排除原点至多ν，剩余原点为反链，与链界夹等号，空偏序处理。 |
| PS2 Q9 | 131–155 | 共上/下覆盖非对角相同，加角−删角=1给DU−UD=I；形式算子每系数有限、正规排序求导符号正确、回空系数e^{t²/2}给匹配数。只要求计数等式，不误称已有对象双射。 |
| PS3 Q1 | 166–175 | 每步删点部由大小固定，所选大部存在叶；任意词对未读长度保证候选、邻点仍在。度数=1+未读词中出现次数，双向逐步恢复，m=1/n=1空词均成立。 |
| PS3 Q2 | 184–198 | 拉普拉斯分部内零和与部常值子空间覆盖全维，0/N谱与部N−size谱正确，系数余子式证明支持谱树数公式。 |
| PS3 Q3 | 209–224 | 加锥根边权x给xF=det(xI+L)，不连通允许多零特征值；补谱n−λ、符号及n=1空乘积一致，多项式延拓约去x合法。 |
| PS3 Q4 | 240–263 | 有向树按反图出度矩阵解释原图出树，入弧块对角明确，删A→B分解可逆；第一式对x求导加x=−y有限差分确定常数，所有端点H0=1。两式为多项式恒等式，含零/负参数。 |
| PS3 Q5 | 272–292 | 循环序列只识别旋转等价固定首弧；立方体字符构成正交全基，谱2k及重数给树数，BEST定义与本册固定首弧定理吻合。不同起点/首弧计数因子明确，无隐去n。 |
| PS3 Q6 | 301–314 | 电位唯一性保证坐标置换对称，同层合并合理；层割Kirchhoff总流1、边数n binom(n−1,k)正确，串联电压及通勤核对满足有限连通不同端点。 |
| PS3 Q7 | 323–337 | 有限吸收游戏终止概率1已证明，第一步调和式与差分比例k/(n−k)正确；逐顶点和原立方体边界系统独立比较吻合。 |
| PS3 Q8 | 351–361 | 官方at least笔误按题面改为at most；条件→排序a_j≤j证明无缺项；可行分配与原到达顺序的贪心交换不变量完整。 |
| PS3 Q9 | 376–406 | 停车/Dyck按希望位分块与首个右侧D序号互逆；二叉树唯一首返回分解保左孩子增大。根树递归用最大点所属分支，内非根与接收车号不同集合按序位映射明确；左右独立区域及最后空位j恢复B,v,r,g,h，归纳双向成立。 |
| PS3 Q10 | 420–436 | 分支B与外C无跨祖先，v在内部改0移出正好r个反序；其他标号顺序保持。位移递推同为A(g)+A(h)+r，逐对象统计保留，例与三阶多项式一致。 |
| PS3 Q11 | 445–450 | 标号统一+1变K_{n+1}根1，Tutte取值点数正确；同册完整最大邻居DFS及交错EGF证明经独审，取值本身非负，无需绝对值。 |
| PS3 Q14 | 459–476 | 起终点跨距2(i+j−1)，Catalan反射参数正确；有限格有向无环，最早x再y及编号选对确保尾交换再选同点同对，是反号对合。交错终点使偶高度差越零，相交矛盾，故恒等。在x=1的高度上界迫使唯一嵌套山形，贡献+1。 |

## 题面与官方答案对应

全部19题中文请求已对照三个原题PDF的提取全文及inventory题号映射。重点实际打开原PSet3第2页与Solutions第1页PNG，确认Q8题面为≤k而官方局部Problem2误写at least k，以及Q9二叉树/带标号Dyck条件。官方局部编号与原题编号分开标注正确；PS3Q9的四集合完整逆构造来自编者补全，官方课堂只给局部二叉树/Dyck与停车提示，这个边界在稿中准确。源页视觉用于题面和笔误辨识，未据此声称中文成书逐页视觉已完成。

| 实际打开源PNG | SHA256 |
|---|---|
| `pset3-p02.png` | `ea5ee4f15e912932618247e270213593b0cc7296cfd52f1852eb9344ffff80ba` |
| `pset3_soln-p01.png` | `cf1132e909b96050836702a063f142a3feb3f40eb9f60c919da5cb5a813e345d` |

所调用本册标签konig、matrix-tree、directedmatrix-tree、best、potential、commute、dilworth、es均机械确认存在；另读BEST固定首弧和有向矩阵树方向说明，与本题使用相符。本审核未替代对应章的整章审核。线性代数的实对称谱与形式幂级数运算为明确数学背景；本题关键谱/算子/组合转换均实际展开证明。

## 独立有限精确复算

另写脚本用整数、Fraction及SymPy精确符号运算；无浮点模拟，未复用作者测试输出。

```json
{
  "bipartite_word_pairs_m_n_1_to4": 5140,
  "tree_parking_recursive_inverse_all_n0_to6": [
    {
      "n": 0,
      "trees_parking_functions": 1,
      "statistic_polynomial_coefficients": [
        1
      ]
    },
    {
      "n": 1,
      "trees_parking_functions": 1,
      "statistic_polynomial_coefficients": [
        1
      ]
    },
    {
      "n": 2,
      "trees_parking_functions": 3,
      "statistic_polynomial_coefficients": [
        2,
        1
      ]
    },
    {
      "n": 3,
      "trees_parking_functions": 16,
      "statistic_polynomial_coefficients": [
        6,
        6,
        3,
        1
      ]
    },
    {
      "n": 4,
      "trees_parking_functions": 125,
      "statistic_polynomial_coefficients": [
        24,
        36,
        30,
        20,
        10,
        4,
        1
      ]
    },
    {
      "n": 5,
      "trees_parking_functions": 1296,
      "statistic_polynomial_coefficients": [
        120,
        240,
        270,
        240,
        180,
        120,
        70,
        35,
        15,
        5,
        1
      ]
    },
    {
      "n": 6,
      "trees_parking_functions": 16807,
      "statistic_polynomial_coefficients": [
        720,
        1800,
        2520,
        2730,
        2520,
        2100,
        1610,
        1140,
        750,
        455,
        252,
        126,
        56,
        21,
        6,
        1
      ]
    }
  ],
  "Dyck_binary_pf_roundtrips_n0_to5": 1442,
  "containment_bracket_involution_all_bitstrings_n1_to12": 8190,
  "first_hit_count_cases": 96,
  "Catalan_det_n1_to10_and_LGV_families_n1_to3": {
    "families": 989,
    "unique_nonintersection_families_total": 3
  },
  "Abel_symbolic_identity_cases": 18,
  "Young_lattice_exact_closed_walks_n0_to7": [
    1,
    1,
    3,
    15,
    105,
    945,
    10395,
    135135
  ],
  "direct_grounded_cube_resistance_n1_to4": [
    "1",
    "1",
    "5/6",
    "2/3"
  ],
  "direct_Dicewalk_boundary_system_n1_to4": [
    {
      "n": 1,
      "all_cube_vertex_probabilities_match": true
    },
    {
      "n": 2,
      "all_cube_vertex_probabilities_match": true
    },
    {
      "n": 3,
      "all_cube_vertex_probabilities_match": true
    },
    {
      "n": 4,
      "all_cube_vertex_probabilities_match": true
    }
  ]
}
```

- 树↔停车在n=0…6全部18,249对象上与独立Prüfer枚举及全函数停车测试对比，双向互逆且每个反序数等于位移；不仅比较对象总数。
- 二部词对在m,n=1…4全部5,140对逐对解码再编码，无重复生成树；不把这个有限范围当成一般双射证明。
- PS3Q14 n=1…3全部989个路径族检查交换再交换及唯一不交族，另n≤10精确行列式；这些只是证明实现和参数的有限校验。
- Young格直接走图，电网络直接接地矩阵求逆、游戏直接全立方体边界线性系统，未复用正文的层公式为计算过程。
- PS3Q11有限符号统计−1评估与直接交错排列比较；无限参数或一般图证明依靠前面的独立审读而非样本。

脚本SHA256 `1974ec6a028ecf561b35f56f5878d7dc7cf175d37a90618a2c40555ad502f7c4`；结果SHA256 `9f4fae4cac518bec4e815b66854fc6ad150dd254381f670949a29827835a57af`。无正文修订，以下脚本保留可复算证据。

```python
import itertools,math,collections,json
from fractions import Fraction
import sympy as sp
out={}
def edges_from_prufer(w,N):
    deg=[1]*N
    for a in w:deg[a]+=1
    e=[]
    for a in w:
        u=next(i for i in range(N) if deg[i]==1);e.append(tuple(sorted((a,u))));deg[u]-=1;deg[a]-=1
    a,b=[i for i in range(N) if deg[i]==1];e.append((a,b));return frozenset(e)
def adj(e,vs):
    a={v:set() for v in vs}
    for u,v in e:a[u].add(v);a[v].add(u)
    return a
def parking(f):
    free=set(range(1,len(f)+1));pos=[]
    for val in f:
        s=next((j for j in sorted(free) if j>=val),None)
        if s is None:return None
        pos.append(s);free.remove(s)
    return pos
# Fixed-part bipartite words, all m,n<=4.
def bi_decode(A,B,alpha,beta):
    A=set(A);B=set(B);alpha=list(alpha);beta=list(beta);e=set()
    while len(A)+len(B)>2:
        if len(A)>=len(B):
            u=min(A-set(alpha));v=beta.pop(0);assert v in B;A.remove(u)
        else:
            v=min(B-set(beta));u=alpha.pop(0);assert u in A;B.remove(v)
        e.add(tuple(sorted((u,v))))
    e.add(tuple(sorted((next(iter(A)),next(iter(B))))));return frozenset(e)
def bi_encode(e,A,B):
    A=set(A);B=set(B);g=adj(e,A|B);al=[];be=[]
    while len(A)+len(B)>2:
        if len(A)>=len(B):
            u=min(v for v in A if len(g[v])==1);v=next(iter(g[u]));be.append(v);A.remove(u)
        else:
            v=min(u for u in B if len(g[u])==1);u=next(iter(g[v]));al.append(u);B.remove(v)
        g[u].remove(v);g[v].remove(u)
    return tuple(al),tuple(be)
bi=0
for m in range(1,5):
 for n in range(1,5):
    A=tuple(range(m));B=tuple(range(m,m+n));trees=set()
    for al in itertools.product(A,repeat=n-1):
     for be in itertools.product(B,repeat=m-1):
        e=bi_decode(A,B,al,be);assert bi_encode(e,A,B)==(al,be);trees.add(e);bi+=1
    assert len(trees)==m**(n-1)*n**(m-1)
out['bipartite_word_pairs_m_n_1_to4']=bi
# Recursive tree/parking maps, implemented without reuse of author script.
def tree_f(e,n):
    if n==0:return ()
    g=adj(e,range(n+1));seen={0};stack=[n];B=set()
    while stack:
        v=stack.pop()
        if v in seen:continue
        seen.add(v);B.add(v);stack.extend(g[v]-seen)
    v=next(iter(g[0]&B));j=len(B);r=sum(b<v for b in B);C=set(range(1,n+1))-B
    def mapped(sub,root):
        mp={root:0};mp.update({a:i+1 for i,a in enumerate(sorted(sub-{root}))})
        return frozenset(tuple(sorted((mp[a],mp[b]))) for a,b in e if a in sub and b in sub)
    left=tree_f(mapped(B,v),j-1);right=tree_f(mapped(C|{0},0),n-j)
    f={n:j-r}
    f.update(zip(sorted(B-{n}),left));f.update((c,j+x) for c,x in zip(sorted(C),right))
    return tuple(f[i] for i in range(1,n+1))
def f_tree(f):
    n=len(f)
    if not n:return frozenset()
    free=set(range(1,n+1));S=[];C=[]
    p=[]
    for i,x in enumerate(f[:-1],1):
        v=min(k for k in free if k>=x);p.append(v);free.remove(v)
    j=next(iter(free));r=j-f[-1];assert 0<=r<j
    S=[i for i,v in enumerate(p,1) if v<j];C=[i for i,v in enumerate(p,1) if v>j]
    B=sorted(S+[n]);v=B[r]
    g=tuple(f[s-1] for s in S);h=tuple(f[c-1]-j for c in C)
    e=set()
    def restore(sub,root,ee):
        names={0:root};names.update({i+1:a for i,a in enumerate(sorted(set(sub)-{root}))})
        for a,b in ee:e.add(tuple(sorted((names[a],names[b]))))
    restore(B,v,f_tree(g));restore([0]+C,0,f_tree(h));e.add((0,v));return frozenset(e)
def inversions(e,n):
    g=adj(e,range(n+1));par={0:None};todo=[0]
    for v in todo:
        for u in g[v]:
            if u not in par:par[u]=v;todo.append(u)
    ans=0
    for i in range(1,n+1):
        j=par[i]
        while j is not None:
            ans+=i<j;j=par[j]
    return ans
pcounts=[]
for n in range(0,7):
    images=set();poly=collections.Counter()
    seqs=[()] if n==0 else itertools.product(range(n+1),repeat=n-1)
    for w in seqs:
        e=frozenset() if n==0 else edges_from_prufer(w,n+1)
        f=tree_f(e,n);pos=parking(f);assert pos is not None and f_tree(f)==e
        inv=inversions(e,n);area=n*(n+1)//2-sum(f);assert inv==area
        images.add(f);poly[area]+=1
    allpf={f for f in itertools.product(range(1,n+1),repeat=n) if parking(f) is not None}
    assert images==allpf
    zig=sum(all((p[i]<p[i+1]) if i%2==0 else (p[i]>p[i+1]) for i in range(n-1)) for p in itertools.permutations(range(n)))
    assert sum(v*(-1)**a for a,v in poly.items())==zig
    pcounts.append({'n':n,'trees_parking_functions':len(images),'statistic_polynomial_coefficients':[poly[a] for a in range(max(poly)+1)]})
out['tree_parking_recursive_inverse_all_n0_to6']=pcounts
# Dyck / planar binary tree conversions checked on all parking functions n<=5.
def pf_word(f):
    return tuple(x for k in range(1,len(f)+1) for x in [i for i,v in enumerate(f,1) if v==k]+[0])
def word_pf(w):
    f={};j=1
    for v in w:
        if v:f[v]=j
        else:j+=1
    return tuple(f[i] for i in range(1,len(f)+1))
def word_tree(w):
    if not w:return None
    ht=1;k=1
    while ht:ht+=1 if w[k] else -1;k+=1
    return (w[0],word_tree(w[1:k-1]),word_tree(w[k:]))
def tree_word(t):
    if t is None:return ()
    v,L,R=t;assert L is None or L[0]>v
    return (v,)+tree_word(L)+(0,)+tree_word(R)
words=0
for n in range(0,6):
    for f in itertools.product(range(1,n+1),repeat=n):
        if parking(f) is None:continue
        w=pf_word(f);assert word_pf(w)==f and tree_word(word_tree(w))==w
        ht=0
        for v in w:ht+=1 if v else -1;assert ht>=0
        assert ht==0;words+=1
out['Dyck_binary_pf_roundtrips_n0_to5']=words
# Bracket containment involution for every bitstring n<=12.
def invol(s):
    stack=[];paired=set()
    for i,x in enumerate(s):
        if x:stack.append(i)
        elif stack:paired.add(i);paired.add(stack.pop())
    free=[i for i in range(len(s)) if i not in paired];a=sum(s[i]==0 for i in free);b=len(free)-a
    t=list(s)
    for j,i in enumerate(free):t[i]=int(j>=b)
    return tuple(t)
ct=0
for n in range(1,13):
 for s in itertools.product((0,1),repeat=n):
    t=invol(s);assert invol(t)==s and sum(t)==n-sum(s)
    if sum(s)<=n/2:assert all(a<=b for a,b in zip(s,t))
    ct+=1
out['containment_bracket_involution_all_bitstrings_n1_to12']=ct
# First hitting counts by exact step dynamic programming.
for start in range(1,7):
    a={start:1}
    for t in range(1,17):
        b=collections.Counter();hit=0
        for i,v in a.items():
            b[i+1]+=v
            if i==1:hit+=v
            else:b[i-1]+=v
        a=b
        expect=0 if t<start or (t-start)%2 else Fraction(start,t)*math.comb(t,(t-start)//2)
        assert hit==expect
out['first_hit_count_cases']=6*16
# Catalan determinant and actual tail-switch involution.
def catalan(k):return math.comb(2*k,k)//(k+1)
for n in range(1,11):assert sp.det(sp.Matrix([[catalan(i+j+1) for j in range(n)] for i in range(n)]))==1
def paths(a,b):
    ans=[]
    def go(x,y,p):
        if x==b:
            if y==0:ans.append(tuple(p))
            return
        if y+1<=b-x-1:go(x+1,y+1,p+[(x+1,y+1)])
        if y>0:go(x+1,y-1,p+[(x+1,y-1)])
    go(a,0,[(a,0)]);return ans
def switch(fam):
    points=collections.defaultdict(list)
    for i,p in enumerate(fam):
        for z in p:points[z].append(i)
    zs=[z for z,v in points.items() if len(v)>1]
    if not zs:return None
    z=min(zs);i,j=points[z][:2];a=fam[i].index(z);b=fam[j].index(z);f=list(fam)
    f[i]=fam[i][:a]+fam[j][b:];f[j]=fam[j][:b]+fam[i][a:];return tuple(f)
count=0;free=0
for n in range(1,4):
    for perm in itertools.permutations(range(n)):
        for fam in itertools.product(*(paths(-2*i,2*(perm[i]+1)) for i in range(n))):
            count+=1;f=switch(fam)
            if f is None:
                free+=1;assert perm==tuple(range(n))
                for i,p in enumerate(fam):
                    assert max(y for x,y in p)==2*i+1
            else:
                assert switch(f)==fam
                ends=[p[-1] for p in f];assert sorted(ends)==sorted(p[-1] for p in fam)
out['Catalan_det_n1_to10_and_LGV_families_n1_to3']={'families':count,'unique_nonintersection_families_total':free}
# Abel polynomial identities, exact symbolic arithmetic.
x,y,z=sp.symbols('x y z')
H=lambda t,k:1 if k==0 else t*(t+k*z)**(k-1)
for n in range(0,9):
    a=sum(math.comb(n,k)*H(y,k)*(x-k*z)**(n-k) for k in range(n+1))
    b=sum(math.comb(n,k)*H(x,k)*H(y,n-k) for k in range(n+1))
    assert sp.expand(a-(x+y)**n)==0 and sp.expand(b-H(x+y,n))==0
out['Abel_symbolic_identity_cases']=18
# Young lattice walk counts via explicit partition neighbors.
def neigh(a):
    ans=set()
    for i in range(len(a)):
        b=list(a);b[i]+=1
        if i==0 or b[i]<=b[i-1]:ans.add(tuple(b))
        b=list(a);b[i]-=1
        if i==len(a)-1 or b[i]>=b[i+1]:
            if b[-1]==0:b.pop()
            ans.add(tuple(b))
    ans.add(a+(1,));return ans
cur={():1};walk=[]
for t in range(15):
    if t%2==0:
        val=cur.get((),0);n=t//2
        assert val==math.factorial(2*n)//(2**n*math.factorial(n));walk.append(val)
    nxt=collections.Counter()
    for a,v in cur.items():
        for b in neigh(a):nxt[b]+=v
    cur=nxt
out['Young_lattice_exact_closed_walks_n0_to7']=walk
# Direct grounded cube rational solve for effective resistance, separate from symmetry proof.
Rs=[];Hs=[]
for n in range(1,5):
    N=2**n;L=sp.zeros(N)
    for v in range(N):
        L[v,v]=n
        for i in range(n):L[v,v^(1<<i)]=-1
    source=sp.zeros(N-1,1);source[0]=1
    phi=L[:N-1,:N-1].inv()*source
    R=sum(Fraction(1,math.comb(n-1,k)) for k in range(n))/n
    assert phi[0]==sp.Rational(R.numerator,R.denominator);Rs.append(str(R))
    # Hitting probability full transient cube, two boundary vertices.
    if N>2:
        interior=list(range(1,N-1));rhs=sp.Matrix([-L[v,N-1] for v in interior])
        sol=L.extract(interior,interior).inv()*rhs
        den=sum(Fraction(1,math.comb(n-1,j)) for j in range(n))
        for i,v in enumerate(interior):
            k=v.bit_count();hh=sum(Fraction(1,math.comb(n-1,j)) for j in range(k))/den
            assert sol[i]==sp.Rational(hh.numerator,hh.denominator)
    Hs.append({'n':n,'all_cube_vertex_probabilities_match':True})
out['direct_grounded_cube_resistance_n1_to4']=Rs
out['direct_Dicewalk_boundary_system_n1_to4']=Hs
print(json.dumps(out,ensure_ascii=False,indent=2))

```
