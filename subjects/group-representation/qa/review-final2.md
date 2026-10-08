# 期末作业第2题独立推导与核对记录

2026-10-08, 受委派 Agent `/root/review_final2`. 本 Agent 独立推导并复核本题; 主 Agent 另负责最终整书交叉审读、编译、源码 ZIP 和远端核验. 不虚构第二位专家, 不把有限例子的测试当作一般证明.

## 范围与来源

仅写 `chapters/final-2.tex` 和本记录. 未改主文件、其他章节、根目录清单或上传工具, 没有提交或上传, 没有接触2016 AMS出版书.

- 原题: `sources/group-representation/pdf/e1bcbdf2202bc6f8d7fb533d39a444ab_MIT18_712F10_712tk.pdf`, 实际PDF第1页第2题. 这是一个题目, 原件无小问. 中文题面保留有限域、二维仿射群、分类所有不可约表示及求特征标的完整要求.
- 理论源: `sources/group-representation/pdf/24d8b3fa2ce48e48ee6c2d8d5e3562f6_MIT18_712F10_replect.pdf`, 109页公开旧版. 已读印刷页68–75的第4.24节及76–77的第4.26节; 实际PDF页序与这些印刷页码相同. 实际打开68、74、75、76、77页及期末作业第1页图像. 特别核对74页虚表示构造、75页内积计算、76页半直积特征标公式.
- 解答明确标为中文编者/AI独立解答, 不冒称期末官方答案.
- 已读 math-lecture-writing 和 math-latex-typesetting 主文件. 远程 references 读取失败后, 读取仓库 topology/vendor 中同名 Skill 的写作、审校、来源、交付和固定版式参考文件. 预编译完整保留本学科主文件既有锁定类.

## 数学推导与检查

章节没有停留在一般半直积定理的口号. 已写出并复核:

1. GL2(Fq)四种共轭类型的参数、类大小和类数. 二次扩域乘法模型覆盖所有特征, 不使用旧讲义仅适用于奇特征的平方根基.
2. Lα、Stα、Pαβ、Cθ四族全部参数、维数、数量、等价关系、四类特征标值; 另给整数参数 αt 和 θj, 可直接求值.
3. 利用两个双陪集的Mackey内积计算证明主系列与Steinberg族的不可约性及参数区别. Cθ由实际表示整数差构造, 完整核对交叉内积 δθκ+δθκ^q; 正单位值决定其确为实际不可约特征标.
4. GL2全部维数平方和等于 q(q−1)^2(q+1). q=2时不使用错误的“所有一维表示来自determinant”命题; Cθ此时正是额外的符号表示.
5. 平移特征 λy(v)=ψ(yv)只有零与非零两个轨道. H={[[1,0],[b,d]]}的q−1个商群特征及唯一(q−1)维R全部列出, 三种类值、不可约性与平方和完整证明.
6. 全仿射群不可约族为GL2四族的提升加q−1个Qτ及一个QR. 权空间论证证明不可约、不同参数不等价及无遗漏, 全Γ的平方和再次核对.
7. 完整诱导有限和的归一化与平移消去有推导. 定义 Wg={y:yg=y}, kg=dim Wg, εg(v)=1[v∈im(g−I)], 得 Qτ=τ(det g)(q^kg εg(v)−1). QR在g=I时为(q−1)(q²1[v=0]−1), 非平凡幺幂g时为1−q εg(v), 其余为0. 行向量零化空间与加法特征求和均有理由.
8. q=2完整S3/S4检验: 维数1,1,2,3,3, 平方和24; 两个三维族的五类值为(3,1,−1,0,−1)与(3,−1,−1,0,1). 逐类辨认非零平移、幺幂线性部分对应的两种平移条件和非分裂线性部分.

一般论证位于章节内. 下述数值枚举是附加核对, 不代替证明.

## 实际有限群枚举

附完整Python脚本, 枚举q=2,3,4,5的全部可逆矩阵及全部仿射元素. q=4使用F16的四元素固定子域, 实际覆盖偶特征非素域, 没有把整数模4当作域. 核对GL2及Γ完整特征标Gram矩阵、两个维数平方和、非零轨道每个元素的直接稳定子诱导求和与闭式.

| q | GL2阶 / 不可约数 | Γ阶 / 不可约数 | Γ Gram最大误差 | 诱导与闭式最大差 |
|---|---|---|---|---|
| 2 | 6 / 3 | 24 / 5 | 1.285e−16 | 2.449e−16 |
| 3 | 48 / 8 | 432 / 11 | 6.661e−16 | 2.674e−15 |
| 4 | 180 / 15 | 2880 / 19 | 1.712e−15 | 2.939e−15 |
| 5 | 480 / 24 | 12000 / 29 | 2.777e−15 | 7.944e−15 |

全部平方和精确等于群阶, 小于1e−10的误差断言全部通过. Γ元素覆盖数依次为24、432、2880、12000.

## 实际编译、视觉与链接

在 `/tmp/group-final2-build` 用当前主文件的完整导言区创建一次性诊断入口, 只引入此章; 没有向交付目录增加碎片PDF. 使用既有 `TEXMFHOME=/workspace/.local/texmf`, XeLaTeX两轮和 `-no-shell-escape -interaction=nonstopmode -halt-on-error`. 最终日志无Overfull、Underfull、undefined或Missing character. 普通filecontents覆盖适配类警告是模板正常行为.

最终诊断PDF实际7页. 已实际打开1.4倍渲染的最终1–7页, 查看中文、表格、公式、跨页、页眉和末尾空心QED, 未发现重叠或溢出. 14个内部命名目标链接均能解析至有效页码. 本记录只认证此章节诊断版本; 集成后的整书页码、目录、源码ZIP重编和远端文件由主Agent另行验证.

本题数学未见未解决阻塞. 主Agent最终整书复核尚待完成, 不在本记录中冒称通过.

## 绑定哈希

- chapters/final-2.tex SHA-256: `a01eff37fa11e56b101a22c0440324ab261bcad186c66786ca10dd6b4d43f984`
- 7页诊断PDF SHA-256: `48b376379ec8520f16ca761a22bd7c2a098a054a65035bbddcb77c2701f1fafa`
- 所附核对脚本 SHA-256: `d117064d61d8dc814e8fb382b3b2b8ddf33999e127c30361cb975ac0ea89e269`

## 可复跑的核对脚本

Python 3与NumPy; 将以下代码保存为临时文件, 执行 `OPENBLAS_NUM_THREADS=1 python check_characters.py`. 无网络、凭据或其他数学库依赖.

```python
import cmath,itertools,json,math
import numpy as np

class Field:
 def __init__(self,p,poly):
  self.p=p;self.poly=poly;self.n=len(poly)-1;self.size=p**self.n
  self.digits=[[(a//p**i)%p for i in range(self.n)] for a in range(self.size)]
  self.add=[[sum(((self.digits[a][i]+self.digits[b][i])%p)*p**i for i in range(self.n)) for b in range(self.size)] for a in range(self.size)]
  self.neg=[sum((-self.digits[a][i]%p)*p**i for i in range(self.n)) for a in range(self.size)]
  self.mul=[[self._mul(a,b) for b in range(self.size)] for a in range(self.size)]
 def _mul(self,a,b):
  v=[0]*(2*self.n-1)
  for i,x in enumerate(self.digits[a]):
   for j,y in enumerate(self.digits[b]):v[i+j]=(v[i+j]+x*y)%self.p
  for k in range(2*self.n-2,self.n-1,-1):
   x=v[k]
   for j in range(self.n+1):v[k-self.n+j]=(v[k-self.n+j]-x*self.poly[j])%self.p
  return sum(v[i]*self.p**i for i in range(self.n))
 def power(self,a,n):
  z=1
  while n:
   if n&1:z=self.mul[z][a]
   a=self.mul[a][a];n>>=1
  return z

def check(q,p,poly):
 e=Field(p,poly); add=e.add;mul=e.mul;neg=e.neg
 sub=lambda a,b:add[a][neg[b]]
 inv=lambda a:e.power(a,q*q-2)
 F=[a for a in range(q*q) if e.power(a,q)==a]
 assert len(F)==q
 nz=[a for a in F if a]
 vec=list(itertools.product(F,repeat=2));rows=[a for a in vec if a!=(0,0)]
 I=(1,0,0,1);O=(0,0,0,0)
 def mm(g,h):
  a,b,c,d=g;x,y,z,w=h
  return (add[mul[a][x]][mul[b][z]],add[mul[a][y]][mul[b][w]],add[mul[c][x]][mul[d][z]],add[mul[c][y]][mul[d][w]])
 def mv(g,v):return (add[mul[g[0]][v[0]]][mul[g[1]][v[1]]],add[mul[g[2]][v[0]]][mul[g[3]][v[1]]])
 def ym(y,g):return (add[mul[y[0]][g[0]]][mul[y[1]][g[2]]],add[mul[y[0]][g[1]]][mul[y[1]][g[3]]])
 def dot(y,v):return add[mul[y[0]][v[0]]][mul[y[1]][v[1]]]
 def det(g):return sub(mul[g[0]][g[3]],mul[g[1]][g[2]])
 def mi(g):
  a,b,c,d=g;u=inv(det(g));return tuple(mul[u][t] for t in (d,neg[b],neg[c],a))
 K=[g for g in itertools.product(F,repeat=4) if det(g)]
 assert len(K)==q*(q-1)*(q*q-1)
 gamma=next(a for a in range(1,q*q) if len({e.power(a,j) for j in range(q*q-1)})==q*q-1)
 logE={e.power(gamma,j):j for j in range(q*q-1)}
 genF=e.power(gamma,q+1);logF={e.power(genF,j):j for j in range(q-1)}
 alpha=lambda t,a:cmath.exp(2j*math.pi*t*logF[a]/(q-1))
 theta=lambda t,a:cmath.exp(2j*math.pi*t*logE[a]/(q*q-1))
 f=round(math.log(q,p))
 def psi(a):
  tr=0
  for j in range(f):tr=add[tr][e.power(a,p**j)]
  assert tr<p
  return cmath.exp(2j*math.pi*tr/p)
 pars=[('L',a) for a in range(q-1)]+[('S',a) for a in range(q-1)]+[('P',a,b) for a in range(q-1) for b in range(a+1,q-1)]
 pars += [('C',j) for j in range(q*q-1) if j%(q+1) and j<(q*j)%(q*q-1)]
 assert len(pars)==q*q-1
 def typ(g):
  a,b,c,d=g
  if b==c==0 and a==d:return ('scalar',a)
  tr=add[a][d];dt=det(g)
  roots=[x for x in nz if add[sub(mul[x][x],mul[tr][x])][dt]==0]
  if len(roots)==1:return ('jordan',roots[0])
  if len(roots)==2:return ('split',*roots)
  roots=[x for x in range(1,q*q) if add[sub(mul[x][x],mul[tr][x])][dt]==0]
  assert len(roots)==2
  return ('elliptic',roots[0])
 def vals(g):
  tp=typ(g);a=tp[1];dt=det(g);out=[]
  for par in pars:
   fam,t=par[:2]
   if fam=='L':z=alpha(t,dt)
   elif fam=='S':z=alpha(t,dt)*{'scalar':q,'jordan':0,'split':1,'elliptic':-1}[tp[0]]
   elif fam=='P':
    u=par[2]
    if tp[0]=='elliptic':z=0
    elif tp[0]=='split':z=alpha(t,a)*alpha(u,tp[2])+alpha(u,a)*alpha(t,tp[2])
    else:z=alpha(t,a)*alpha(u,a)*(q+1 if tp[0]=='scalar' else 1)
   else:
    if tp[0]=='split':z=0
    elif tp[0]=='elliptic':z=-theta(t,a)-theta(t,e.power(a,q))
    else:z=theta(t,a)*(q-1 if tp[0]=='scalar' else -1)
   out.append(z)
  return out
 kc=np.array([vals(g) for g in K],complex).T
 kerr=float(np.max(abs(kc@kc.conj().T/len(K)-np.eye(len(pars)))))
 assert kerr<1e-10
 dims=[round(z.real) for z in vals(I)]
 assert sum(d*d for d in dims)==len(K)
 lifts=[];direct_error=0
 trow={}
 for y in rows:
  t=next((*y,*z) for z in vec if det((*y,*z)))
  trow[y]=(t,mi(t))
 ac=[]
 for g in K:
  delta=(sub(g[0],1),g[1],g[2],sub(g[3],1))
  image={mv(delta,v) for v in vec}
  fixed=[y for y in rows if ym(y,g)==y]
  unipotent=(g!=I and mm(delta,delta)==O)
  conjugates=[]
  for y in fixed:
   t,tinv=trow[y];h=mm(mm(t,g),tinv)
   assert h[0]==1 and h[1]==0
   r=(q-1 if h[2]==0 else -1) if h[3]==1 else 0
   conjugates.append((y,h[3],r))
  for v in vec:
   s=(len(fixed)+1)*(v in image)-1
   closed=[alpha(t,det(g))*s for t in range(q-1)]
   closed.append((q-1)*s if g==I else -s if unipotent else 0)
   direct=[sum(psi(dot(y,v))*alpha(t,d) for y,d,r in conjugates) for t in range(q-1)]
   direct.append(sum(psi(dot(y,v))*r for y,d,r in conjugates))
   direct_error=max(direct_error,max(abs(a-b) for a,b in zip(closed,direct)))
   ac.append(vals(g)+closed)
 affine=np.array(ac,complex).T
 aerr=float(np.max(abs(affine@affine.conj().T/(q*q*len(K))-np.eye(len(pars)+q))))
 adims=dims+[q*q-1]*(q-1)+[(q*q-1)*(q-1)]
 assert sum(d*d for d in adims)==q*q*len(K)
 assert direct_error<1e-10 and aerr<1e-10
 return {'q':q,'K_order':len(K),'K_irreducibles':len(pars),'K_square_sum':sum(d*d for d in dims),'K_gram_max_error':kerr,'Gamma_order':q*q*len(K),'Gamma_irreducibles':len(pars)+q,'Gamma_square_sum':sum(d*d for d in adims),'Gamma_gram_max_error':aerr,'direct_induced_vs_closed_max_error':direct_error,'all_Gamma_elements_checked':q*q*len(K)}

results=[check(2,2,[1,1,1]),check(3,3,[1,0,1]),check(4,2,[1,1,0,0,1]),check(5,5,[2,0,1])]
print(json.dumps(results,ensure_ascii=False,indent=2))
```

## 实际完整输出

```json
[
  {
    "q": 2,
    "K_order": 6,
    "K_irreducibles": 3,
    "K_square_sum": 6,
    "K_gram_max_error": 1.3343220141622404e-16,
    "Gamma_order": 24,
    "Gamma_irreducibles": 5,
    "Gamma_square_sum": 24,
    "Gamma_gram_max_error": 1.2853092654502116e-16,
    "direct_induced_vs_closed_max_error": 2.4492935982947064e-16,
    "all_Gamma_elements_checked": 24
  },
  {
    "q": 3,
    "K_order": 48,
    "K_irreducibles": 8,
    "K_square_sum": 48,
    "K_gram_max_error": 8.881784197001252e-16,
    "Gamma_order": 432,
    "Gamma_irreducibles": 11,
    "Gamma_square_sum": 432,
    "Gamma_gram_max_error": 6.661338147750939e-16,
    "direct_induced_vs_closed_max_error": 2.673771110915334e-15,
    "all_Gamma_elements_checked": 432
  },
  {
    "q": 4,
    "K_order": 180,
    "K_irreducibles": 15,
    "K_square_sum": 180,
    "K_gram_max_error": 1.7168329763565887e-15,
    "Gamma_order": 2880,
    "Gamma_irreducibles": 19,
    "Gamma_square_sum": 2880,
    "Gamma_gram_max_error": 1.7119194711189392e-15,
    "direct_induced_vs_closed_max_error": 2.939152317953647e-15,
    "all_Gamma_elements_checked": 2880
  },
  {
    "q": 5,
    "K_order": 480,
    "K_irreducibles": 24,
    "K_square_sum": 480,
    "K_gram_max_error": 2.7433125689005183e-15,
    "Gamma_order": 12000,
    "Gamma_irreducibles": 29,
    "Gamma_square_sum": 12000,
    "Gamma_gram_max_error": 2.7772071608068983e-15,
    "direct_induced_vs_closed_max_error": 7.944109290391274e-15,
    "all_Gamma_elements_checked": 12000
  }
]
```
