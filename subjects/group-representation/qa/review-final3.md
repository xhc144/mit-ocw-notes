# MIT 18.712 (2010) 期末作业第3题独立审读

审读对象：`chapters/final-3.tex`。本任务只创建该题解及本记录；未改主文件、其余章节、全局清单或上传工具。

## 题源与边界

- 官方题面：MIT 18.712, Fall 2010, Takehome Assignment，第1页第3题。原件为 `sources/group-representation/pdf/e1bcbdf2202bc6f8d7fb533d39a444ab_MIT18_712F10_712tk.pdf`，第2页为 OCW 说明。官方资源页：https://ocw.mit.edu/courses/18-712-introduction-to-representation-theory-fall-2010/resources/mit18_712f10_712tk/ 。资源页明确称其为课程 final assignment。
- 数学来源核读：公开旧讲义（首页2011-02-01，109页）§3.8，印刷页41–42，A5旋转表示、奇置换扭曲三维表示、五点置换四维表示的构造；Problem 5.5，印刷页80–81，SU(2)有限子群自然二维表示及McKay图的定义。网址：https://ocw.mit.edu/courses/18-712-introduction-to-representation-theory-fall-2010/24d8b3fa2ce48e48ee6c2d8d5e3562f6_MIT18_712F10_replect.pdf 。未读取或使用2016年AMS书。
- 题面为官方题；本中文解答为AI/编者独立撰写，不标作官方答案。非本科主线的McKay对象仅为解此题在本地计算必要张量积，未声称覆盖一般箭图分类或Gabriel定理。

## 数学审查结果

1. 群为SU(2)中A5的二重覆盖，阶数120，中心元z=-I。循环子群阶数仅1、2、3、4、5、6、10；同阶子群共轭，实际数量分别1、1、10、15、6、10、6，共49个。各循环子群上的全部一维特征标用7种共轭代表的31列完整覆盖。
2. 九个共轭类按自然迹t=2、-2、0、1、-1、φ、-φ、τ、-τ排列，大小1、1、30、20、20、12、12、12、12。保留了阶数5与10元素、阶数3与6元素的不同提升，未把Γ混同A5。
3. 不可约表示为1、V、V'、A、A'、B、C、D、E，维数1、2、2、3、3、4、4、5、6。Sym^0至Sym^5及两个A5表示是实际表示；V'=V⊗B−E首先作为虚表示，再以整数系数、范数1和正维数证明实际不可约，避免用非负权重误代表示存在性证明。
4. 从递推P[n+1]=tP[n]−P[n−1]、A5几何表示及置换表示重新导出特征标。解析实际TeX内特征标表与独立计算逐项精确对比。81个Gram矩阵条目精确得到I9；维数平方和120；Sym^6V=A'⊕B，不能把维数7对称幂误当不可约。
5. C4、C6、C10三个完整权重表实际解析后与独立构造逐项对比。9×(4+6+10)=180个幂的特征标与对应权重的根单位和，以SymPy精确三角/代数化简核实，未以浮点近似作为最终验证。
6. C2、C3、C5表由权重下标取模折叠，解析实际TeX中的合并表与折叠值一致。C2从C4、C6、C10三条路径折叠一致。所有表项为非负整数、各行和为维数。全部31个诱导特征标的每列加权维数均为120/d。
7. 逐项计算V张量积的9×9矩阵，结果为文中8条无重边、无环边的McKay图；链1—V—A—C—D—E—B—V'在E接端点A'，确为仿射E8。不是仅引用图名或已知表。
8. Frobenius互反的字符指数方向检查通过：η(d,j)(h)=ζ_d^j时，重数为权重j，DFT使用ζ_d^(-jk)。换生成元h→h^u时新列j对应旧列u^(-1)j，避免把V'在C10上的±3权重误记成±1。

## 编译和视觉

使用主文件现有完整固定类与记号前导，在`/tmp/final3-review/`建立只输入此节的检查入口，未改排版参数。系统默认TeX树未找到ctex；通过现有`TEXMFHOME=/workspace/.local/texmf`运行XeLaTeX成功，未安装包或修改权限。无shell escape。第二次成功编译后没有Overfull、Underfull、缺字、未解析引用或TeX错误；仅有filecontents覆盖同一适配类的预期提示。Fontconfig缓存目录提示不影响实际字体加载和产出。

实际单节PDF为5页，每页612×792 bp，已逐页渲染到1.5倍并通过view_image查看全部五页。字符表和四组权重表可读、无重叠或越界；固定页眉正常；最后证毕符号正常。第3、4页末尾留白来自把整张表保留在下一页，已视觉核对，没有省略题解内容。此记录仅证明本节临时入口的编译和视觉，不代替父任务最终合编、目录链接、ZIP干净重编和远端校验。

正文SHA-256：`df350bc1035c62a34d2b2fe3a90602f9c5c5d91c11447aa868a024b5dc351cff`。
单节检查PDF SHA-256：`9d91c382711245a6d94648aa41c0c7211ebb0a4f90e8ab0a5fd5a7861990dffa`。

## 可复算检查脚本

以下脚本不依赖英文原件或第三方特征标表，仅依赖SymPy与实际题解TeX；中间路径`/tmp/final3-review/`供本轮检查使用。输出中`Vp`、`Ap`分别对应V'、A'。

```python
import sympy as s
import json
x=s.symbols('x'); ph=(1+s.sqrt(5))/2; ta=ph-1
P=[s.Integer(1),x]
for n in range(2,7): P.append(s.expand(x*P[-1]-P[-2]))
ts=list(map(s.sympify,[2,-2,0,1,-1,ph,-ph,ta,-ta])); sizes=[1,1,30,20,20,12,12,12,12]
B=list(map(s.sympify,[4,4,0,1,1,-1,-1,-1,-1])); Ap=list(map(s.sympify,[3,3,-1,0,0,-ta,-ta,ph,ph]))
names=['1','V','Vp','A','Ap','B','C','D','E']
polys=[P[0],P[1],None,P[2],None,None,P[3],P[4],P[5]]
chars=[]
for name,f in zip(names,polys):
 vals=[s.simplify(f.subs(x,t)) for t in ts] if f is not None else Ap if name=='Ap' else B if name=='B' else [s.simplify(t*b-P[5].subs(x,t)) for t,b in zip(ts,B)]
 chars.append(vals)
gram=s.Matrix([[s.simplify(sum(k*a*b for k,a,b in zip(sizes,aa,bb))/s.Integer(120)) for bb in chars] for aa in chars])
assert gram==s.eye(9)
assert sum(v[0]**2 for v in chars)==120
assert all(s.simplify(P[6].subs(x,t)-chars[4][k]-chars[5][k])==0 for k,t in enumerate(ts))
W={4:[[1,0,0,0],[0,1,0,1],[0,1,0,1],[1,0,2,0],[1,0,2,0],[2,0,2,0],[0,2,0,2],[3,0,2,0],[0,3,0,3]],
6:[[1,0,0,0,0,0],[0,1,0,0,0,1],[0,1,0,0,0,1],[1,0,1,0,1,0],[1,0,1,0,1,0],[2,0,1,0,1,0],[0,1,0,2,0,1],[1,0,2,0,2,0],[0,2,0,2,0,2]],
10:[[1,0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,1],[0,0,0,1,0,0,0,1,0,0],[1,0,1,0,0,0,0,0,1,0],[1,0,0,0,1,0,1,0,0,0],[0,0,1,0,1,0,1,0,1,0],[0,1,0,1,0,0,0,1,0,1],[1,0,1,0,1,0,1,0,1,0],[0,1,0,1,0,2,0,1,0,1]]}
trace_count=0
folds={}
for m,Wm in W.items():
 assert all(sum(row)==chars[ix][0] for ix,row in enumerate(Wm))
 assert all(v>=0 for row in Wm for v in row)
 for ix,row in enumerate(Wm):
  for k in range(m):
   # The imaginary terms cancel because every weight row is symmetric.
   assert all(row[r]==row[-r %m] for r in range(m))
   trace=sum(a*s.cos(2*s.pi*r*k/m) for r,a in enumerate(row))
   t=s.trigsimp(2*s.cos(2*s.pi*k/m))
   ii=next(ii for ii,t0 in enumerate(ts) if s.simplify(t-t0)==0)
   assert s.simplify(s.expand_trig(trace-chars[ix][ii]))==0,(m,ix,k,trace,chars[ix][ii])
   trace_count+=1
 for d in [v for v in (1,2,3,4,5,6,10) if m%v==0]:
  F=[[sum(row[r] for r in range(m) if r%d==j) for j in range(d)] for row in Wm]
  if d in folds: assert F==folds[d]
  folds[d]=F
  for j in range(d): assert sum(F[ix][j]*chars[ix][0] for ix in range(9))==120//d
# Each entry of the McKay matrix is derived from the full class table.
M=s.Matrix([[s.simplify(sum(k*t*a*b for k,t,a,b in zip(sizes,ts,aa,bb))/s.Integer(120)) for bb in chars] for aa in chars])
assert M==M.T
edges=[(0,1),(1,3),(3,6),(6,7),(7,8),(8,5),(5,2),(8,4)]
expected=s.zeros(9)
for a,b in edges: expected[a,b]=expected[b,a]=1
assert M==expected
# Parse actual manuscript tables rather than just validate copied constants.
import re
text=open('/workspace/mit-ocw-notes/subjects/group-representation/chapters/final-3.tex').read()
tables=re.findall(r'\\begin\{tabular\}.*?\\end\{tabular\}',text,re.S)
parsed=[]
character_rows=[]
for line in tables[0].splitlines():
 if re.match(r'^\$(?:\\mathbf1|V|V\x27|A|A\x27|B|C|D|E)\$&',line):
  cells=line.split('\\\\')[0].split('&')[1:]
  character_rows.append([s.sympify(c.replace('$','').replace('\\varphi','ph').replace('\\tau','ta'),locals={'ph':ph,'ta':ta}) for c in cells])
assert len(character_rows)==9
assert all(s.simplify(a-b)==0 for aa,bb in zip(character_rows,chars) for a,b in zip(aa,bb))
for table in tables:
 rows=[]
 for line in table.splitlines():
  if re.match(r'^\$(?:\\mathbf1|V|V\x27|A|A\x27|B|C|D|E)\$&',line):
   cells=line.split('\\\\')[0].split('&')[1:]
   if all(re.fullmatch(r'\d+',c.strip()) for c in cells):rows.append(list(map(int,cells)))
 if len(rows)==9: parsed.append(rows)
assert parsed[:3]==[W[4],W[6],W[10]]
assert parsed[3]==[folds[2][i]+folds[3][i]+folds[5][i] for i in range(9)]
# Dimensions of all 31 individual characters (one representative of each subgroup).
assert sum(folds)==31
result={'gram_identity_exact':True,'manuscript_character_table_equal_derived_characters':True,'sum_dimension_squares':120,'symmetric_power_6_split':'Ap+B','weight_character_checks_exact':trace_count,'manuscript_weight_tables_equal_checked_tables':True,'mckay_edges':edges,'cyclic_orders':sorted(folds),'total_cyclic_characters':31,'all_multiplicities_nonnegative':True,'all_induced_dimensions_equal_index':True,'central_C2_fold_agrees_for_4_6_10':True}
open('/tmp/final3-review/check.json','w').write(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
```

实际输出：

```json
{
  "gram_identity_exact": true,
  "manuscript_character_table_equal_derived_characters": true,
  "sum_dimension_squares": 120,
  "symmetric_power_6_split": "Ap+B",
  "weight_character_checks_exact": 180,
  "manuscript_weight_tables_equal_checked_tables": true,
  "mckay_edges": [
    [
      0,
      1
    ],
    [
      1,
      3
    ],
    [
      3,
      6
    ],
    [
      6,
      7
    ],
    [
      7,
      8
    ],
    [
      8,
      5
    ],
    [
      5,
      2
    ],
    [
      8,
      4
    ]
  ],
  "cyclic_orders": [
    1,
    2,
    3,
    4,
    5,
    6,
    10
  ],
  "total_cyclic_characters": 31,
  "all_multiplicities_nonnegative": true,
  "all_induced_dimensions_equal_index": true,
  "central_C2_fold_agrees_for_4_6_10": true
}
```

当前结论：本题数学、来源、单节编译及五页视觉检查通过；父任务仍应进行独立最终复核和合编检查。没有未解数学缺项。
