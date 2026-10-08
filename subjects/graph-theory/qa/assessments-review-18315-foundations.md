# 18.315 基础作业稿独立数学审核

审核对象为hw1、hw2、hw3、hw4、hw7、hw8六份题解；独立审核代理未参与这些稿件的撰写，只读审稿，未编辑原稿。2026-10-08完整逐题审读16道原题、25个叶题，并对照官方题面，未发现实质数学错误，无待修数学问题。本记录是模型独立审读，不是人类专家审定。作者自检与本文复算分开；有限计算不证明任意规模断言。未对合册PDF版面、链接或最终ZIP作本轮验收。

## 最终绑定

| 源稿 | 行数 | SHA256 |
|---|---:|---|
| `hw1.tex` | 114 | `adef0820c176afe2be934bf13df3a6cd062d38d08a7841eaa6e716eff29882af` |
| `hw2.tex` | 104 | `e937c3af6101d1622e5120f167d589a5a509748816c30d311e87330984c8eda1` |
| `hw3.tex` | 128 | `fe6e82e34fa2560c9a7eae3b4a987d2196efce3ffdfd78b609076230ec10ebe3` |
| `hw4.tex` | 103 | `30f379a2b55dec57d5ef0ce3fcefe6db5ae038b0918d4648f0dde3381f092c45` |
| `hw7.tex` | 93 | `49d7fa133169195960e5c0c8a79c26938ca852069343a8c41a1720d3fbb977ba` |
| `hw8.tex` | 65 | `0f8078890c02dc58ffb2e3a261a9682f799e5d694eccc2e4db2d94862417d3bc` |

官方inventory SHA256 `3cd990e6752094a612c59043b44d597675fc6eda7b4a829beeaa21282d9e003d`。官方课程网页学期Spring 2005与八份原PDF页首FALL 2005冲突，稿件保存“原卷Fall 2005”而未篡改原题学期；本轮没有另行猜测日期或书目缺失题面。所有收录答案均编者独立解答，无公开作业官方答案。

2026-10-08合册预编译后重新核查hw2纯排版修订：第42行emph改textbf；六类边从inline拆为独立display并用quad间隔。将这两处机械还原后恰得到原已审稿SHA256 `5d5990c952dbae7ec27030763cdc150b8e3687285706ddfff8d4e8d1d04b1b02`，证明、参数、边集、表格与反例完全未改；再次读取六份hash，只有hw2变动，另五份一致。更新上表与后续hw2行号，数学审核结论保持。

## 逐题结论与证明核查

| 稿件/原题 | 范围 | 独立核查结论 |
|---|---|---|
| hw1 Q1(a)(b) | 行15–34 | 奇偶独立染色给严格指数下界；限制到互不相交小块给上界，limsup≤每个a_m且liminf≥inf，足以证明正极限，无须不合法拼块。 |
| hw1 Q2(a)(b) | 行44–69 | 行优先前缀中左邻点已有度≤2；条件于其余颜色时均匀分布在至少k−2个合法色上，故两个先邻同色概率≤1/(k−2)。各前缀计数之比正是均匀前缀的平均延伸数，可以逐步相乘。数值及低估误差独立复算一致。 |
| hw1 Q3(a)(b) | 行80–92 | 网格2退化证明对任意诱导子图适用；模拟删点改色时至多禁止三个色，k≥4足够，最后目标色合法。 |
| hw1 Q5 | 行102–113 | n<5无样本须排除；固定二分的超几何概率逐因子≤(B/M)^{2n}，无序二分并集界严格<1/2；n/(n−1)单调给25/32统一界正确。 |
| hw2 Q2 | 行13–30 | 简单平面图边界3v−6应用于含外三点的诱导图；任意边子集Hall条件成立，左右等大使每个内顶点恰分三边，三个不同叶形成非诱导爪即可。空三角形边界已处理。 |
| hw2 Q3(a)(b) | 行42–84 | 官方原定义未固定出度；有向圈翻转保持各点出度。两列二十面体27边分区逐边独立核验，无漏边/重复，顶点2出度0/3，足以否定任意圈翻转，亦否定仅三圈。固定出度修订的任意圈证明成立，稿件没有冒称证明其三角形版本。 |
| hw2 Q4 | 行96–103 | 正反颜色赋±1/3，三色贡献±1，双色贡献0；内部有向边成对抵消，保留边界。 |
| hw3 Q3 | 行14–48 | 最大元偶位与最小元奇位的两个计数分别覆盖全部排列，左右模式取补保计数；递推n≥1及u0=u1=1准确产生U'=(U²+1)/2。连通分量指数公式、w=-2、C'=U(-2z)系数符号正确。 |
| hw3 Q4 | 行60–85 | 最大邻居DFS非树边只连祖先后代；每个允许边parent(j)–i与反序(i,j)唯一对应，j为真祖先，故不是树边。增加任意允许边子集不改变搜索，分割全部连通子图。独立穷举每一棵实际DFS树的纤维大小等于2^{inv}。 |
| hw3 Q5(a)(b)(c) | 行99–127 | n=1原不等式无界明确纠正；n≥2坐标自动≤1。奇偶仿射反转给篱笆偏序保序映射与体积；理想链恢复时永不进入者取k，其余首次进入时取相应阶段，双射正确。有限严格排名和重复坐标的O(k^{n−1})计数给体积首项。 |
| hw4 Q1 | 行14–30 | 各部和为0子空间与部常值子空间覆盖全维，非零谱及矩阵树系数核对正确；r=1及N=1边界单列。 |
| hw4 Q4(a)(b) | 行41–61 | 固定图染色多项式离线可算，位长O(log(q+2))；固定列状态转移扫描n列，各项O(n)位，总位时间关于n多项式。没有把n二进制长度与n混淆。 |
| hw4 Q6 | 行71–102 | 树固定m中选v−1边，中央二项式上界及偶/奇m推导正确。K5块在同一割点合并且余边接路径，生成树乘积125^{floor(m/10)}，给渐近指数下界，未声称最优。m=0空树下界1可解释。 |
| hw7 Q3(a)(b)(c) | 行16–92 | 2q点构造实现所有有理有限密度；最大密度存在且删点平均使α_n非增。Turán超饱和得到cN^{r+1}团；多部超图共同链归纳的所有常数/阈值正确，随机分部保留固定比例，再由完整超图推出普通多部子图。极限分类跨t→∞闭合，α=1单独处理，确排除1/3且强于有理性。 |
| hw8 Q2 | 行18–33 | 多项式交错分配给根树钩长公式，子树h值不变，双向计数及n=1边界正确。 |
| hw8 Q4 | 行44–64 | 线性扩展的目标首元素可交换到前端，所有经过者不可比；归纳、Young格偏序与根树祖先偏序均满足，n(n−1)/2交换界成立。 |

## 原题及歧义交叉核实

读了六份原PDF对应的全部题面文本，并为符号/定义风险实际打开官方HW2第1页与HW7第1页PNG：HW2确说全部claw coverings而没有各点固定出度限制；HW7(b)实际为不等于1/3，文本提取失落不等号。此处的源页视觉只用于数学题面辨识，不等于整册视觉验收。

- HW2第1页PNG SHA256 `f283cc0de4157ed6bf21c1ac08d7a0375d0bd6170d56d357b347a0da366c8e23`。
- HW7第1页PNG SHA256 `8dffad4035d86bad08b2c2a0ed798ec56ecfd3c404b0c1ba16f8ba425c201be6`。

## 独立有限复算

独立审核者另写Python脚本，没有复用作者测试输出。高精度浮点只用于打印L_k与误差界的数值，证明依据稿中符号不等式；其余小图与二项式/整数序列检查用整数完全枚举。

```json
{
  "grid_lower_bound_values": {
    "1000000": {
      "mantissa": "9.80394713331914990376631805258760448059945238969923394852500440160174029499874155866244003",
      "exponent": 59999,
      "relative_underestimate_bound": "0.00000000980103915608742773022282519958330706099539198887828177708656108276242692197420887161102252"
    },
    "1000": {
      "mantissa": "2.46832206931335560096427909410101746810129182171656191863567120469068360047701237439720805",
      "exponent": 29991,
      "relative_underestimate_bound": "0.00979206437826337380330666512554035876036287138285307297573956102676308287898009288273176445"
    }
  },
  "claw_counterexample": {
    "icosahedron_edges_after_face_deletion": 27,
    "A_and_B_valid_partitions": true,
    "outdegree_2": [
      0,
      3
    ],
    "outdegree_7": [
      3,
      0
    ]
  },
  "DFS_maximum_neighbor_all_connected_graphs_n1_to6": {
    "count": 27476,
    "signed_Tutte_values": [
      {
        "n": 1,
        "connected_graphs": 1,
        "T_n_1_minus1": 1
      },
      {
        "n": 2,
        "connected_graphs": 1,
        "T_n_1_minus1": 1
      },
      {
        "n": 3,
        "connected_graphs": 4,
        "T_n_1_minus1": 1
      },
      {
        "n": 4,
        "connected_graphs": 38,
        "T_n_1_minus1": 2
      },
      {
        "n": 5,
        "connected_graphs": 728,
        "T_n_1_minus1": 5
      },
      {
        "n": 6,
        "connected_graphs": 26704,
        "T_n_1_minus1": 16
      }
    ]
  },
  "A_m_central_binomial_bound_checked": 201,
  "path_polytope_checks": [
    {
      "n": 2,
      "alternating_permutations": 1,
      "k_1_2_3_bijection_counts_match": true
    },
    {
      "n": 3,
      "alternating_permutations": 2,
      "k_1_2_3_bijection_counts_match": true
    },
    {
      "n": 4,
      "alternating_permutations": 5,
      "k_1_2_3_bijection_counts_match": true
    },
    {
      "n": 5,
      "alternating_permutations": 16,
      "k_1_2_3_bijection_counts_match": true
    },
    {
      "n": 6,
      "alternating_permutations": 61,
      "k_1_2_3_bijection_counts_match": true
    },
    {
      "n": 7,
      "alternating_permutations": 272,
      "k_1_2_3_bijection_counts_match": true
    }
  ]
}
```

DFS枚举覆盖n≤6的所有连通简单标号图，逐图验证非树边可允许性并逐搜索树核纤维2^{inv}，不是仅比最终总数；Tutte符号和另外与枚举交错排列比较。路径检查为n=2–7、k=1,2,3的仿射对应整数点数。有限验证未验证大图、渐近O项、超图吹胀引理或Turán定理本身；这些结论通过逐步独立审读证明。

脚本SHA256 `3b330368df4ff43f1bb111df847f6b1cf586b211cc80bfb8d54aad2f9cdb3dda`；结果SHA256 `5e59feb2ba258f0e0fcb4c658cf1fff3c14eede730bcb5d94be977f56ca4f111`。以下存脚本原文以便复算，临时文件不必随源码ZIP交付。未做正文修订，表中最终hash再次机械读取一致。

```python
import itertools,math,json
from fractions import Fraction
import mpmath as mp
out={}
mp.mp.dps=90
out['grid_lower_bound_values']={}
for k in (1000000,1000):
    logL=mp.log10(k)+198*mp.log10(k-1)+9801*mp.log10(k-2)
    exp=int(mp.floor(logL));coef=mp.power(10,logL-exp)
    err=-mp.expm1(-mp.mpf(9801)/(k-2)**2)
    out['grid_lower_bound_values'][str(k)]={'mantissa':str(coef),'exponent':exp,'relative_underestimate_bound':str(err)}
    assert err < (mp.mpf('1e-8') if k==1000000 else mp.mpf('.0099'))
E=set()
def add(u,v):E.add(tuple(sorted((u,v))))
for i in range(5):
    a=1+i;b=6+i
    for u,v in [(0,a),(11,b),(a,1+(i+1)%5),(b,6+(i+1)%5),(a,b),(a,6+(i-1)%5)]:add(u,v)
E-= {(0,1),(0,2),(1,2)}
A={3:[4,2,0],4:[5,8,0],5:[10,1,0],6:[10,2,1],7:[6,3,2],8:[9,7,3],9:[4,11,5],10:[11,9,1],11:[8,7,6]}
B={2:[7,6,3],3:[8,7,0],4:[8,3,0],5:[4,1,0],6:[10,7,1],8:[11,9,7],9:[4,10,5],10:[11,5,1],11:[6,9,7]}
for cover in (A,B):
    es=[tuple(sorted((u,v))) for u,vs in cover.items() for v in vs]
    assert len(es)==len(set(es))==27 and set(es)==E
out['claw_counterexample']={'icosahedron_edges_after_face_deletion':len(E),'A_and_B_valid_partitions':True,'outdegree_2': [0,3],'outdegree_7':[3,0]}
Tvals=[];tot=0
for n in range(1,7):
    es=list(itertools.combinations(range(1,n+1),2));tutte=0;conn=0;cells={};cellinv={}
    for mask in range(1<<len(es)):
        adj=[[] for _ in range(n+1)]
        for j,(u,v) in enumerate(es):
            if mask>>j&1:adj[u].append(v);adj[v].append(u)
        seen={1};parent={1:None};tree=set()
        def dfs(u):
            for v in sorted(adj[u],reverse=True):
                if v not in seen:
                    seen.add(v);parent[v]=u;tree.add(tuple(sorted((u,v))));dfs(v)
        dfs(1)
        if len(seen)<n:continue
        conn+=1;tot+=1
        allowed=set();inv=0
        for i in range(1,n+1):
            j=parent[i]
            while j is not None:
                if i<j:
                    inv+=1;allowed.add(tuple(sorted((parent[j],i))))
                j=parent[j]
        actual={es[j] for j in range(len(es)) if mask>>j&1}
        assert actual-tree <= allowed and len(allowed)==inv
        key=tuple(sorted(tree));cells[key]=cells.get(key,0)+1;cellinv[key]=inv
        tutte+=(-2)**(len(actual)-n+1)
    assert all(cells[key]==2**cellinv[key] for key in cells)
    un=sum(all((p[i]<p[i+1]) if i%2==0 else (p[i]>p[i+1]) for i in range(n-2)) for p in itertools.permutations(range(n-1)))
    assert tutte==un
    Tvals.append({'n':n,'connected_graphs':conn,'T_n_1_minus1':tutte})
out['DFS_maximum_neighbor_all_connected_graphs_n1_to6']= {'count':tot,'signed_Tutte_values':Tvals}
for m in range(0,201):
    # squared bound avoids floating arithmetic
    assert math.comb(m,m//2)**2*(m//2+1)<=4**m
out['A_m_central_binomial_bound_checked']=201
out['path_polytope_checks']=[]
for n in range(2,8):
    u=sum(all((p[i]<p[i+1]) if i%2==0 else (p[i]>p[i+1]) for i in range(n-1)) for p in itertools.permutations(range(n)))
    for k in (1,2,3):
        x=sum(all(v[i]+v[i+1]<=k for i in range(n-1)) for v in itertools.product(range(k+1),repeat=n))
        y=sum(all((v[i]<=v[i+1]) if i%2==0 else (v[i]>=v[i+1]) for i in range(n-1)) for v in itertools.product(range(k+1),repeat=n))
        assert x==y
    out['path_polytope_checks'].append({'n':n,'alternating_permutations':u,'k_1_2_3_bijection_counts_match':True})
print(json.dumps(out,ensure_ascii=False,indent=2))

```
