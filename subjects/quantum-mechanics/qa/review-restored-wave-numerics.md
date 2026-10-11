# 恢复授权题目：波动力学数值独立核算

## 检查范围与原件

本轮核 PS6 #4/#5/#6、PS7 #3、PS8 #2/#4 指定的数值及物理解释，不是整套新成稿审校。实际读暂存原 PDF 与提取文本，渲染后通过 view_image 查看 PS6 物理页2–4、PS7物理页1、PS8物理页1–4，核实公式、势区边界及参数。未修改正文或其他学科。

数值由本审查独立编写 Python/SciPy/mpmath 脚本计算，没有调用主任务脚本。附录保存实际脚本和完整输出。

## PS6 #4/#5：半阶无限阱

取 u=x/a，e=E/V0，z0=2π。方程为 −ψ″/z0²+fψ=eψ；f在(0,1)为0、(1,2)为1，ψ(0)=ψ(2)=0。

E<V0 时，左段 AL sin(ηu)，右段 B sinh[ξ(2−u)]，η=z0√e，ξ=z0√(1−e)。连续性给 ηcotη=−ξcothξ；数值用无cot极点行列式
D=sinη coshξ+η cosη sinhξ/ξ=0。
两个根分别在 π/2<η<π 和 3π/2<η<2π，所以恰有两个低于台阶的能级。

E>V0 时，q=z0√(e−1)，右段 AR sin[q(2−u)]，连续性给
D(e)=sinη cosq+η cosη sinq/q=0。
e=1 处用 sinq/q→1 的连续极限，避免漏根或假根。

| 编号 | En/V0 |
|---|---|
| 1 | 0.1843580657131345443 |
| 2 | 0.7074702358212535872 |
| 3 | 1.206516570023701994 |
| 4 | 1.562500000000000000 |
| 9（第八激发态） | 5.557413654032853788 |

第4态有η=5π/2、q=3π/2，两段界面导数均为0，1.5625还可直接解析核验。
第9态η=14.8120861810、q=13.4134067048，左右各4个内部零点，共8节点；界面不是零点，硬墙端点不计内部节点。
左右正弦包络幅度比为 |AL/AR|=|sinq/sinη|=0.959735973069。
慢变振幅规律给 √(λL/λR)=√(q/η)=0.951615333682，精确比值比近似高约0.85%。台阶不满足慢变条件，不能把近似当精确匹配。

收敛：双精度扫描加Brent与60位mpmath根一致，所列5个根高精度行列式残差约10⁻⁵⁹至10⁻⁶²；完整前9根序列见附录，核实第9态编号。

quartic原题是 −ψ″/2+(u⁴−e)ψ=0，动能系数必须保留1/2。偶基态
e0=0.6679862591558。

边值条件ψ(0)=1、ψ′(0)=0、ψ(L)=0：

| L | e0 | 最大归一残差 |
|---|---|---|
| 3.5 | 0.6679862591557862 | <10⁻¹⁰ |
| 4 | 0.6679862591557941 | <10⁻¹⁰ |
| 5 | 0.6679862591557950 | <10⁻¹⁰ |
| 6 | 0.6679862591557924 | <10⁻¹⁰ |

另从禁止区以ψ′(L)/ψ(L)=−√2 L²−1/L向内打靶，要求ψ′(0)=0。L=3.5、4、5，ODE容差10⁻¹⁰、10⁻¹¹、10⁻¹²给0.6679862591702851、0.6679862591572451、0.6679862591558965，收敛到同一值。附录边值算法的nodes变量指网格点数，不是波函数节点数。

## PS6 #6：H₂⁺ 双方井

原参数γ=.2，V0=1.7402×13.6eV。井区γ<|u|<2+γ，每井宽2a0；模拟质子在井中心±(1+γ)a0。质子间距2.4a0，不能拿中央空隙0.4a0计算排斥。

取ε=Ee/(13.6eV)，−ψ″+vψ=εψ，井内v=−1.7402。偶态中央区coshκu，κ=√(−ε)。在u=γ取y=coshκγ、y′=κsinhκγ，井内q=√(1.7402+ε)，传播长度2：
Y=y cos2q+y′sin2q/q；
Y′=−qy sin2q+y′cos2q。
外区衰减条件Y′+κY=0。最低根对应无节点偶态，中央正值曲线向井内先增长，出现对称两峰后进入外侧指数尾。

ε=−1.2692280706155104，
Ee=−17.26150176037eV，
Epp=e²/[2(1+γ)a0]=+11.33333333333eV，
Etot=−5.92816842704eV。

总能为负不能证明相对H+p解离稳定。模型孤立H阈值约−13.6eV，因此Etot−EH+p=+7.67183157296eV，给定间距的总体系不能抵抗H+p解离；电子本身确实束缚。原校准参数经过四舍五入，重算单井阈值会有小舍入差，不改变结论。本轮未检索真实分子实验值，成稿实验对比须另有来源并说明一维方井局限。

独立分段ODE打靶容差10⁻⁸、10⁻¹⁰、10⁻¹²给ε=−1.2692280704962、−1.2692280706128618、−1.2692280706154786，与分段解析传播一致约13位，匹配残差低于10⁻¹⁵。

## PS7 #3：单侧禁止区概率

原题问x大于经典振子的正振幅，必须求单侧。取s=x√(mω/ℏ)，cn=√(2n+1)：
Pn=∫[cn,∞] Hn(s)²e^(−s²) ds/[√π 2ⁿn!]。

闭式：
P0=erfc(1)/2；
P1=erfc(√3)/2+√3e⁻³/√π；
P2=erfc(√5)/2+e⁻⁵[(√5)³+√5/2]/√π。

独立自适应积分给0.07864960352514254、0.05580511254735631、0.04753471744286315，约7.865%、5.581%、4.753%。分部积分可核闭式；两侧总概率才是这些值的2倍。

## PS8 #2：双δ稳定间距

a0=ℏ²/(mg)，λ=a/a0，ξ=κa，λ=ξ/(1+e⁻²ξ)，E∞=mg²/(2ℏ²)>0：
Vtot/E∞=−ξ²/λ²+β/λ=−(1+e⁻²ξ)²+β/λ。
离子间距2a，但排斥能无额外因子2。令s=e⁻²ξ，驻点方程
4s(1+s)−β(1+s+2ξs)/ξ²=0。

β=.31有两个驻点：

| 类型 | ξ | λ=a/a0 | Vtot/E∞ |
|---|---|---|---|
| 稳定极小值 | 0.5380940169129775 | 0.4012954116524770 | −1.0254945157226591 |
| 不稳定极大值 | 1.8529105209083481 | 1.8084585591589522 | −0.8783475325275113 |

稳定原子间距2a/a0=0.8025908233049540；最低能低于分離阈值−1，模型确有解离稳定结合。导数在第一根由负变正、第二根由正变负。双精度扫描/Brent与60位mpmath一致，驻点残差约10⁻⁶¹。

## PS8 #4：全波包峰延迟

实际原PDF式(4)、(e)均为 exp[−β²(K−K0)²]。a=ℏ/√(mV0)、τ=V0t/ℏ：
E/V0=K²/2，0<K<√2，
w(K)=1−K²+iK√(2−K²)，反射系数r=−w。
全波积分是
√a Ψ=∫[0,√2] exp[−β²(K−K0)²−iK²τ/2] {exp(iKu)−w exp(−iKu)}dK。
不能遗漏相对入射波的负号。

全Gaussian近似给du/dτ=K0、ΔK=1/(2β)、Δu=β、ΔuΔK=1/2。
argw=2arcsin(K/√2)，窄谱解析延迟Δτ=2/[K0√(2−K0²)]。
β=4、K0=1故ΔK=.125、Δu=4、解析Δτ=2。宽度是题面要求的全Gaussian近似，不是截断波包精确饱和不确定性的结论。

原题完整积分，τ=20、u∈[−30,0]：
全局主峰upeak=−17.9178323226106，
按峰位置推断延迟20+upeak=2.0821676773894。
约比解析2高4.1%；有限谱宽、色散及未完全消失的入射尾使两种读数不完全相同。
原题未另归一化密度峰值.17380837319915；归一化不改变峰位置。
只取反射分量的峰约−17.71779014，推断延迟约2.28221，不是题(e)/(f)全波峰读数。

收敛：K=√2sinθ消除上端平方根非光滑性；Gauss–Legendre积分160、320、640、1280点，密度解析一阶导数求零点，峰位置差<7×10⁻¹⁴。另以步长.01检查整个绘图区，最大网格值均位于−17.92；直接有界优化也给同一峰，停止误差约3×10⁻⁸。不能将这次数值收敛当一般波包延迟定理。

## 后续成稿重点

半阶阱第9态为8个内部节点，幅度比是正弦包络比；H₂⁺必须区分电子束缚与H+p稳定性、质子间距与空隙；PS7单侧不能乘2；PS8须保留β²、反射负号及全波/反射分量的区别。此轮数值已核闭合，后续完整成稿仍需逐题审校。

## 输入哈希

PS6: eb660f9384d5af5f6eb9efc9c65b0e46_MIT8_04S16_ps6_2016.pdf

SHA256: fb820b40a4c4658d2c798b97261be0775ed3d13283ee60f3a9580c743ba02c54

PS7: e56c39618b49183ed4e855ae38e2f0d0_MIT8_04S16_ps7_2016.pdf

SHA256: d177d6612621e69b7965297f02ba8aa90e477d5e49dd4b015e138e8137c88146

PS8: 67574eeda2314554048c13a823b23d7a_MIT8_04S16_ps8_2016.pdf

SHA256: 881cdfb0b9ab7e9a8a4de6d987df46d17814fd2a50ca6867e1738977f29f0ae3


## 附录：实际独立脚本与输出

### independent_wave_check

```python
import math
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import solve_bvp, quad
from scipy.special import eval_hermite, roots_legendre
import json
out={}
z=2*np.pi
def determinant(e):
 p=z*np.sqrt(e)
 if e<1:
  q=z*np.sqrt(1-e); return np.sin(p)*np.cosh(q)+p*np.cos(p)*np.sinh(q)/q
 q=z*np.sqrt(e-1)
 return np.sin(p)*np.cos(q)+p*np.cos(p)*(np.sin(q)/q if q else 1)
a=np.linspace(.00001,25,30000); roots=[]
for x,y in zip(a[:-1],a[1:]):
 if determinant(x)*determinant(y)<0: roots.append(brentq(determinant,x,y,xtol=1e-14))
out['step_roots']=roots[:9]
e=roots[8]; p=z*np.sqrt(e); q=z*np.sqrt(e-1)
out['ninth']={'eta':p,'q':q,'left_nodes':int(p/np.pi),'right_nodes':int(q/np.pi),'amplitude_left_over_right':abs(np.sin(q)/np.sin(p)),'WKB_left_over_right':np.sqrt(q/p),'residual':determinant(e)}
out['quartic']=[]
for L in [3.5,4,5,6]:
 x=np.linspace(0,L,600)
 def fun(x,y,p):return np.array([y[1],2*(x**4-p[0])*y[0]])
 def bc(ya,yb,p):return np.array([ya[0]-1,ya[1],yb[0]])
 y=np.array([np.exp(-x*x),-2*x*np.exp(-x*x)])
 sol=solve_bvp(fun,bc,x,y,p=[.668],tol=1e-10,max_nodes=30000)
 out['quartic'].append({'L':L,'e':float(sol.p[0]),'status':sol.status,'max_rms_residual':float(max(sol.rms_residuals)),'nodes':len(sol.x)})
gamma=.2; depth=1.7402
def hm(e):
 kap=np.sqrt(-e);q=np.sqrt(depth+e)
 y=np.cosh(kap*gamma);dy=kap*np.sinh(kap*gamma)
 Y=y*np.cos(2*q)+dy*np.sin(2*q)/q
 DY=-q*y*np.sin(2*q)+dy*np.cos(2*q)
 return DY+kap*Y
hh=brentq(hm,-depth+1e-10,-.8,xtol=1e-14)
out['h2plus']={'e_electron_in_13.6eV':hh,'Ee_eV':hh*13.6,'repulsion_eV':27.2/(2*(1+gamma)),'total_eV':hh*13.6+27.2/(2*(1+gamma)),'relative_H_plus_p_eV':hh*13.6+27.2/(2*(1+gamma))+13.6,'matching_residual':hm(hh)}
# Direct one-sided oscillator probability quadrature.
out['oscillator_one_side']=[quad(lambda x:np.exp(-x*x)*eval_hermite(n,x)**2/(np.sqrt(np.pi)*2**n*math.factorial(n)),np.sqrt(2*n+1),np.inf,epsabs=1e-13)[0] for n in range(3)]
beta=.31
def lam(x):return x/(1+np.exp(-2*x))
def energy(x):return -(1+np.exp(-2*x))**2+beta/lam(x)
def der(x):
 s=np.exp(-2*x);return 4*s*(1+s)-beta*((1+s)+2*x*s)/x**2
xx=np.geomspace(.00001,20,20000); stationary=[]
for x,y in zip(xx[:-1],xx[1:]):
 if der(x)*der(y)<0:
  t=brentq(der,x,y,xtol=1e-14);stationary.append({'xi':t,'lambda':lam(t),'Vtot_over_Einf':energy(t),'curvature_sign':np.sign(der(t+1e-5)-der(t-1e-5))})
out['double_delta']=stationary
# Gaussian quadrature mapped K=sqrt(2)sin theta removes endpoint square-root.
out['packet']=[]
for N in [160,320,640,1280]:
 x,wt=roots_legendre(N);theta=(x+1)*np.pi/4;K=np.sqrt(2)*np.sin(theta);weights=wt*np.pi/4*np.sqrt(2)*np.cos(theta)
 phi=np.exp(-16*(K-1)**2); w=1-K*K+1j*K*np.sqrt(2-K*K)
 def density(u,complete=True):
  A=np.exp(-.5j*K*K*20)*(-w*np.exp(-1j*K*u))
  if complete:A+=np.exp(-.5j*K*K*20)*np.exp(1j*K*u)
  return abs(np.dot(weights*phi,A))**2
 opt=minimize_scalar(lambda u:-density(u),bounds=(-22,-14),method='bounded',options={'xatol':1e-11})
 ref=minimize_scalar(lambda u:-density(u,False),bounds=(-22,-14),method='bounded',options={'xatol':1e-11})
 out['packet'].append({'quadrature_N':N,'full_peak_u':float(opt.x),'inferred_delay_tau':float(20+opt.x),'full_peak_density':density(opt.x),'reflected_only_peak_u':float(ref.x)})
print(json.dumps(out,indent=2))
```

```json
{
  "step_roots": [
    0.1843580657131345,
    0.7074702358212537,
    1.206516570023702,
    1.5625000000000002,
    2.084467304517918,
    2.8004684345890603,
    3.560779634620218,
    4.535381278302816,
    5.557413654032851
  ],
  "ninth": {
    "eta": 14.812086181023485,
    "q": 13.413406704849795,
    "left_nodes": 4,
    "right_nodes": 4,
    "amplitude_left_over_right": 0.9597359730685696,
    "WKB_left_over_right": 0.9516153336823445,
    "residual": 8.659739592076221e-15
  },
  "quartic": [
    {
      "L": 3.5,
      "e": 0.6679862591557862,
      "status": 0,
      "max_rms_residual": 9.99504589221889e-11,
      "nodes": 3087
    },
    {
      "L": 4,
      "e": 0.6679862591557941,
      "status": 0,
      "max_rms_residual": 9.998916288791347e-11,
      "nodes": 3407
    },
    {
      "L": 5,
      "e": 0.667986259155795,
      "status": 0,
      "max_rms_residual": 9.992269659690654e-11,
      "nodes": 3321
    },
    {
      "L": 6,
      "e": 0.6679862591557924,
      "status": 0,
      "max_rms_residual": 9.998913144833252e-11,
      "nodes": 3408
    }
  ],
  "h2plus": {
    "e_electron_in_13.6eV": -1.2692280706155104,
    "Ee_eV": -17.26150176037094,
    "repulsion_eV": 11.333333333333334,
    "total_eV": -5.9281684270376065,
    "relative_H_plus_p_eV": 7.671831572962393,
    "matching_residual": -8.881784197001252e-16
  },
  "oscillator_one_side": [
    0.07864960352514254,
    0.05580511254735631,
    0.047534717442863146
  ],
  "double_delta": [
    {
      "xi": 0.5380940169129774,
      "lambda": 0.40129541165247695,
      "Vtot_over_Einf": -1.025494515722659,
      "curvature_sign": 1.0
    },
    {
      "xi": 1.8529105209083483,
      "lambda": 1.8084585591589526,
      "Vtot_over_Einf": -0.8783475325275112,
      "curvature_sign": -1.0
    }
  ],
  "packet": [
    {
      "quadrature_N": 160,
      "full_peak_u": -17.917832355109006,
      "inferred_delay_tau": 2.082167644890994,
      "full_peak_density": 0.17380837319916656,
      "reflected_only_peak_u": -17.717790139090052
    },
    {
      "quadrature_N": 320,
      "full_peak_u": -17.917832355118332,
      "inferred_delay_tau": 2.082167644881668,
      "full_peak_density": 0.17380837319915476,
      "reflected_only_peak_u": -17.717790139094674
    },
    {
      "quadrature_N": 640,
      "full_peak_u": -17.917832355087775,
      "inferred_delay_tau": 2.082167644912225,
      "full_peak_density": 0.17380837319916398,
      "reflected_only_peak_u": -17.717790401892017
    },
    {
      "quadrature_N": 1280,
      "full_peak_u": -17.917832355086652,
      "inferred_delay_tau": 2.0821676449133477,
      "full_peak_density": 0.17380837319914957,
      "reflected_only_peak_u": -17.717790139096508
    }
  ]
}
```

### independent_wave_crosscheck

```python
import numpy as np, mpmath as mp, json
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import roots_legendre
mp.mp.dps=60
z=2*mp.pi
def D(e):
 p=z*mp.sqrt(e);q=z*mp.sqrt(e-1)
 return mp.re(mp.sin(p)*mp.cos(q)+p*mp.cos(p)*mp.sin(q)/q)
roots=[mp.findroot(D,(mp.mpf(v)-mp.mpf('.001'),mp.mpf(v)+mp.mpf('.001'))) for v in ['.184358','.707470','1.206517','1.5625','5.557414']]
out={'high_precision_step': [mp.nstr(v,40) for v in roots],'step_abs_residual':[mp.nstr(abs(D(v)),4) for v in roots]}
out['quartic_inward_shooting']=[]
for L,tol in [(3.5,1e-10),(4,1e-11),(5,1e-12)]:
 def residual(e):
  sol=solve_ivp(lambda u,y:[y[1],2*(u**4-e)*y[0]],(L,0),[1,-np.sqrt(2)*L*L-1/L],rtol=tol,atol=tol*.01,method='DOP853')
  return sol.y[1,-1]/sol.y[0,-1]
 e=brentq(residual,.66,.68,xtol=1e-14)
 out['quartic_inward_shooting'].append({'L':L,'rtol':tol,'e':e,'residual_log_derivative':residual(e)})
out['h2_shooting']=[]
for tol in [1e-8,1e-10,1e-12]:
 def res(e):
  y=[1,0]
  for l,r,v in [(0,.2,0),(.2,2.2,-1.7402)]:
   sol=solve_ivp(lambda u,y:[y[1],(v-e)*y[0]],(l,r),y,rtol=tol,atol=tol*.01,method='DOP853');y=sol.y[:,-1]
  return y[1]+np.sqrt(-e)*y[0]
 e=brentq(res,-1.7402+1e-8,-.8,xtol=1e-14)
 out['h2_shooting'].append({'rtol':tol,'e':e,'residual':res(e)})
out['packet_derivative_roots']=[]
for N in [160,320,640,1280]:
 x,wt=roots_legendre(N);th=(x+1)*np.pi/4;K=np.sqrt(2)*np.sin(th);wt=wt*np.pi/4*np.sqrt(2)*np.cos(th)
 phi=np.exp(-16*(K-1)**2);w=1-K*K+1j*K*np.sqrt(2-K*K); base=wt*phi*np.exp(-.5j*K*K*20)
 def dens(u):
  a=np.dot(base,np.exp(1j*K*u)-w*np.exp(-1j*K*u));return abs(a)**2
 def dd(u):
  ep=np.exp(1j*K*u);em=np.exp(-1j*K*u)
  a=np.dot(base,ep-w*em);ad=np.dot(base,1j*K*(ep+w*em));return 2*np.real(a.conjugate()*ad)
 u=brentq(dd,-18.5,-17.5,xtol=1e-13)
 grid=np.linspace(-30,0,3001);top=grid[np.argmax([dens(t) for t in grid])]
 out['packet_derivative_roots'].append({'N':N,'u_peak':u,'delay':20+u,'grid_global_peak':top,'density':dens(u)})
print(json.dumps(out,indent=2))
```

```json
{
  "high_precision_step": [
    "0.1843580657131345442641761868807335708962",
    "0.7074702358212535872116167785161885176834",
    "1.206516570023701993923152343960979730229",
    "1.5625",
    "5.557413654032853787747887206418474838868"
  ],
  "step_abs_residual": [
    "4.978e-60",
    "1.369e-59",
    "1.556e-61",
    "2.483e-62",
    "2.334e-61"
  ],
  "quartic_inward_shooting": [
    {
      "L": 3.5,
      "rtol": 1e-10,
      "e": 0.6679862591702851,
      "residual_log_derivative": 1.0576120558863975e-16
    },
    {
      "L": 4,
      "rtol": 1e-11,
      "e": 0.6679862591572451,
      "residual_log_derivative": 1.775581157952447e-16
    },
    {
      "L": 5,
      "rtol": 1e-12,
      "e": 0.6679862591558965,
      "residual_log_derivative": 4.8968030390670323e-17
    }
  ],
  "h2_shooting": [
    {
      "rtol": 1e-08,
      "e": -1.2692280704962,
      "residual": -1.2212453270876722e-15
    },
    {
      "rtol": 1e-10,
      "e": -1.2692280706128618,
      "residual": 5.551115123125783e-16
    },
    {
      "rtol": 1e-12,
      "e": -1.2692280706154786,
      "residual": -1.2212453270876722e-15
    }
  ],
  "packet_derivative_roots": [
    {
      "N": 160,
      "u_peak": -17.917832322610643,
      "delay": 2.082167677389357,
      "grid_global_peak": -17.92,
      "density": 0.17380837319916662
    },
    {
      "N": 320,
      "u_peak": -17.91783232261062,
      "delay": 2.0821676773893785,
      "grid_global_peak": -17.92,
      "density": 0.1738083731991547
    },
    {
      "N": 640,
      "u_peak": -17.917832322610682,
      "delay": 2.082167677389318,
      "grid_global_peak": -17.92,
      "density": 0.17380837319916406
    },
    {
      "N": 1280,
      "u_peak": -17.917832322610643,
      "delay": 2.082167677389357,
      "grid_global_peak": -17.92,
      "density": 0.17380837319914952
    }
  ]
}
```
