#!/usr/bin/env python3
"""Reproduce declared initial-value models using only Python's standard library."""
from pathlib import Path
import csv,json,math,hashlib
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; DATA.mkdir(exist_ok=True)
g=9.81

def rk4(f,t,y,h):
    k1=f(t,y); k2=f(t+h/2,[a+h*b/2 for a,b in zip(y,k1)])
    k3=f(t+h/2,[a+h*b/2 for a,b in zip(y,k2)])
    k4=f(t+h,[a+h*b for a,b in zip(y,k3)])
    return [a+h*(b+2*c+2*d+e)/6 for a,b,c,d,e in zip(y,k1,k2,k3,k4)]

def simpson(f,a,b,n=20000):
    h=(b-a)/n
    return h/3*(f(a)+f(b)+4*sum(f(a+(2*j-1)*h) for j in range(1,n//2+1))+2*sum(f(a+2*j*h) for j in range(1,n//2)))

rows=[]
for h in [.02,.01,.005,.0025]:
    y=[.5,0.];t=0.;e0=g*(1-math.cos(y[0]));drift=0.;q=None; trajectory=[]
    while t<10:
        z=rk4(lambda t,q:[q[1],-g*math.sin(q[0])],t,y,h)
        if q is None and y[0]>0>=z[0]:q=t+h*y[0]/(y[0]-z[0])
        e=z[1]**2/2+g*(1-math.cos(z[0]));drift=max(drift,abs(e/e0-1))
        trajectory.append((t+h,*z,e));t+=h;y=z
    rows.append({'step_s':h,'period_s':4*q,'max_relative_energy_drift':drift})
    if h==.0025:
        with (DATA/'pendulum.csv').open('w',newline='') as f:
            w=csv.writer(f);w.writerow(['time_s','theta_rad','omega_rad_per_s','energy_per_mass']);w.writerows(trajectory)
k=math.sin(.25)
exact=4/math.sqrt(g)*simpson(lambda x:1/math.sqrt(1-k*k*math.sin(x)**2),0,math.pi/2)
small=2*math.pi/math.sqrt(g)
chain=[]
for fraction in [0,.1,.25,.5,.75,.9,.99]:
    phi=math.asin(math.sqrt(fraction))
    tm=2/math.sqrt(g)*simpson(lambda p:math.cos(p)**2/math.sqrt(1-.5*math.sin(p)**2),0,phi,4000)
    force=0 if fraction==0 else fraction+fraction*(1-fraction/2)/(1-fraction)
    chain.append({'y_over_L':fraction,'time_s_L1':tm,'support_over_Mg':force})
chain_end=2/math.sqrt(g)*simpson(lambda p:math.cos(p)**2/math.sqrt(1-.5*math.sin(p)**2),0,math.pi/2)
with (DATA/'folded-chain.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(chain[0]));w.writeheader();w.writerows(chain)

def orbit_der(t,q):
    x,y,vx,vy=q;r2=x*x+y*y;return [vx,vy,-r2*x,-r2*y]
q=[1.01,0.,0.,1/1.01];t=0;h=.001;last_rdot=0.;maxima=[0.];drift=0.;e0=(q[2]**2+q[3]**2)/2+(q[0]**2+q[1]**2)**2/4;orbit=[]
while t<20:
    z=rk4(orbit_der,t,q,h);r=math.hypot(z[0],z[1]);rdot=(z[0]*z[2]+z[1]*z[3])/r
    if last_rdot>0 and rdot<=0:maxima.append(t+h*last_rdot/(last_rdot-rdot))
    energy=(z[2]**2+z[3]**2)/2+r**4/4;drift=max(drift,abs(energy/e0-1))
    orbit.append((t+h,*z,r,energy));last_rdot=rdot;t+=h;q=z
with (DATA/'central-orbit.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['time','x','y','vx','vy','radius','energy']);w.writerows(orbit[::10])
central_period=maxima[1]
rocket=[3000*math.log(2.81/.35),3000*math.log(2.81/.78),3000*math.log(6.4/2.1)]
result={'method':'stdlib RK4 + composite Simpson; crossing times linear interpolation','pendulum':rows,'pendulum_elliptic_integral_period_s':exact,'pendulum_small_angle_period_s':small,'chain':chain,'chain_end_time_s_L1':chain_end,'central_orbit':{'step':h,'initial':[1.01,0,0,1/1.01],'radial_period':central_period,'linear_radial_period':2*math.pi/math.sqrt(6),'max_relative_energy_drift':drift},'rocket_speeds_m_per_s':rocket+[sum(rocket[1:])]}
(DATA/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
tex=[r'\begin{center}\begin{tabular}{rrr}\toprule',r'步长 / s & 单摆周期 / s & 10 s 最大相对能量漂移 \\\midrule']
def sci_tex(value):
    exponent=math.floor(math.log10(abs(value)))
    return f"${value/10**exponent:.3f}\\times10^{{{exponent}}}$"
for row in rows:
    tex.append(f"{row['step_s']:.4f} & {row['period_s']:.8f} & {sci_tex(row['max_relative_energy_drift'])} \\\\")
tex.extend([r'\bottomrule\end{tabular}\end{center}',f'独立 Simpson 积分有限振幅周期为 {exact:.8f} s, 小角周期为 {small:.8f} s. 周期插值本身只有二阶, 不能把过零时间误差也称为四阶.',r'链条采用前述无耗散折返模型, $L=1$ m. 用 $y=L\sin^2\phi$ 消去端点根号, 实际积分得如下支力曲线点; 不把末端奇异力当成实测峰值.',r'\begin{center}\begin{tabular}{rrr}\toprule',r'$y/L$ & $t$ / s & $F_S/(Mg)$ \\\midrule'])
for r in chain:tex.append(f"{r['y_over_L']:.2f} & {r['time_s_L1']:.6f} & {r['support_over_Mg']:.4f} \\\\")
tex.extend([r'\bottomrule\end{tabular}\end{center}',f'折返完成时刻的有限极限为 {chain_end:.8f} s; 此时理想支力发散, 最终静止的 $Mg$ 不是该曲线连续延拓.',f'另运行期末第 7 题的中心力初值: $A=m=L=1$, 初 $r=1.01$, 纯切向速率 $1/1.01$. 步长 0.001, 积分 20 时间单位. 实得径向周期 {central_period:.8f}, 线性预测 $2\\pi/\\sqrt6={2*math.pi/math.sqrt(6):.8f}$; 有限振幅差约 {abs(central_period/(2*math.pi/math.sqrt(6))-1):.3g}. 最大相对能量漂移 {drift:.3g}. 数据仅验证这一接近圆轨道的复现, 一般结论由正文推导保证.'])
(ROOT/'chapters/numerical-results.tex').write_text('\n'.join(tex)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
