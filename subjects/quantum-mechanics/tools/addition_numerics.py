#!/usr/bin/env python3
"""Generate only the 2026-10-11 addition figures; no downloaded/old figures changed."""
from pathlib import Path
import json, hashlib
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq, minimize_scalar
from scipy.linalg import eigh
from scipy.special import airy

ROOT=Path(__file__).resolve().parents[1]
CH=ROOT/'chapters'
receipt={'scope':'new addition figures and independent reproducible numerical checks',
         'figures':[], 'no_source_scans_copied':True}
def plot(lines,xlabel,ylabel,extra='',height='4.2cm'):
    s=r'\begin{center}\begin{tikzpicture}'+'\n'+r'\begin{axis}[width=.82\textwidth,height='+height+',xlabel={'+xlabel+'},ylabel={'+ylabel+r'},grid=major,legend style={font=\small},'+extra+']\n'
    for x,y,label in lines:
        s+=r'\addplot+[mark=none] coordinates{'
        s+=' '.join(f'({a:.9g},{b:.9g})' for a,b in zip(x,y) if np.isfinite(a+b))+'};\n'
        if label:s+=r'\addlegendentry{'+label+'}\n'
    return s+r'\end{axis}\end{tikzpicture}\end{center}'+'\n'
def save(name,s):
    (CH/name).write_text(s);receipt['figures'].append(name)

# Hermite spectral approximation: powers constructed in a larger space before crop.
quartic=[]
for N in (40,60,80):
    nn=N+8;a=np.diag(np.sqrt(np.arange(1,nn)),1);x=(a+a.T)/2;p=-1j*(a-a.T)
    H=(p@p/2+x@x@x@x)[:N,:N]
    e=eigh(H,eigvals_only=True,subset_by_index=(0,5))
    quartic.append({'dimension':N,'energies':e.tolist()})
assert abs(e[0]-.6679862591558)<1e-10 and abs(e[1]-2.393644016482)<1e-10
receipt['quartic_hermite']=quartic
ai=quad(lambda t:(np.exp(1j*np.pi/6)*np.exp(-t**3/3+1j*np.exp(1j*np.pi/6)*t)).real,0,np.inf,epsabs=1e-12)[0]/np.pi
receipt['airy_rotated_integral']={'Ai1':ai,'scipy_Ai1':float(airy(1)[0])}
assert abs(ai-airy(1)[0])<1e-12

# Step well determinant roots, and explicit forward shooting residuals.
z0=2*np.pi
def det(E):
    k=z0*np.sqrt(E);q=z0*np.sqrt(abs(E-1))
    if abs(E-1)<1e-12:return np.sin(k)+k*np.cos(k)
    if E<1:return np.sin(k)*np.cosh(q)+k*np.cos(k)*np.sinh(q)/q
    return np.sin(k)*np.cos(q)+k*np.cos(k)*np.sin(q)/q
grid=np.linspace(1e-7,7,4001)
roots=[brentq(det,a,b,xtol=1e-14) for a,b in zip(grid[:-1],grid[1:]) if det(a)*det(b)<0][:9]
assert abs(roots[8]-5.557413654033)<1e-10
shoot=[]
for E in roots[:4]:
    y=solve_ivp(lambda u,Y:[Y[1],-z0*z0*E*Y[0]],(0,1),[0,1],rtol=2e-11,atol=2e-13).y[:,-1]
    y=solve_ivp(lambda u,Y:[Y[1],z0*z0*(1-E)*Y[0]],(1,2),y,rtol=2e-11,atol=2e-13).y[:,-1]
    shoot.append(float(y[0]))
E=roots[8];k=z0*np.sqrt(E);q=z0*np.sqrt(E-1);AL=np.sin(q)/np.sin(k)
u=np.linspace(0,2,401);y=np.where(u<1,AL*np.sin(k*u),np.sin(q*(2-u)))
s=plot([(u,y,'')],r'$u=x/a$',r'$\psi_9$','xmin=0,xmax=2')
# H2+ ground matching and shape (normalization computed by quadrature).
def hmatch(E):
    kap=np.sqrt(-E);q=np.sqrt(1.7402+E);v=np.cosh(.2*kap);dv=kap*np.sinh(.2*kap)
    Y=v*np.cos(2*q)+dv*np.sin(2*q)/q;DY=-q*v*np.sin(2*q)+dv*np.cos(2*q)
    return DY+kap*Y
hroot=brentq(hmatch,-1.6,-1.0,xtol=1e-14);kap=np.sqrt(-hroot);q=np.sqrt(1.7402+hroot)
def hpsi(u):
    u=np.abs(np.asarray(u));v=np.cosh(.2*kap);dv=kap*np.sinh(.2*kap)
    end=v*np.cos(2*q)+dv*np.sin(2*q)/q
    out=np.empty_like(u,dtype=float)
    first=u<.2;middle=(u>=.2)&(u<2.2);last=u>=2.2
    out[first]=np.cosh(kap*u[first])
    out[middle]=v*np.cos(q*(u[middle]-.2))+dv*np.sin(q*(u[middle]-.2))/q
    out[last]=end*np.exp(-kap*(u[last]-2.2))
    return out
hnorm=np.sqrt(2*quad(lambda t:float(hpsi(t)**2),0,np.inf,points=None,epsabs=1e-10)[0])
xx=np.linspace(-5,5,401);s+=plot([(xx,hpsi(xx)/hnorm,'')],r'$x/a_0$',r'$\psi_g$')
save('figure-804-ps6-shooting.tex',s)
receipt['step_well']={'energies':roots,'forward_shooting_boundary_residuals':shoot,'ninth_nodes':8,'amplitude_ratio':float(abs(AL)),'WKB_ratio':float(np.sqrt(q/k)) if False else float(((E-1)/E)**.25)}
receipt['H2plus']={'electron_energy_over_Ry':float(hroot),'matching_residual':float(hmatch(hroot))}

lam=np.linspace(.01,3,241)
even=np.array([brentq(lambda s:s-l*(1+np.exp(-2*s)),1e-12,2*l+1) for l in lam])
odd=np.array([brentq(lambda s:s-l*(1-np.exp(-2*s)),1e-10,l+1) if l>.5 else np.nan for l in lam])
save('figure-804-ps7-double-delta.tex',plot([(lam,-even**2/2,'偶态'),(lam,-odd**2/2,'奇态')],r'$\lambda$',r'$E/[\hbar^2/(ma^2)]$','legend pos=south west'))
xi=np.linspace(.01,5,401);L=xi/(1+np.exp(-2*xi));elec=-(1+np.exp(-2*xi))**2
s=plot([(L,elec,'电子能')],r'$\lambda$',r'$E/E_\infty$','ymin=-4.2,ymax=-.8')
s+=plot([(L,elec+b/L,rf'$\beta={b}$') for b in (.1,.31,.6)],r'$\lambda$',r'$F$','ymin=-2.5,ymax=1,legend pos=south east')
save('figure-804-ps8-bond.tex',s)
def bond(t,b=.31):
    L=t/(1+np.exp(-2*t));return -(1+np.exp(-2*t))**2+b/L
bo=minimize_scalar(bond,bounds=(.1,1.5),method='bounded',options={'xatol':1e-13})
receipt['bond_minimum']={'lambda':float(bo.x/(1+np.exp(-2*bo.x))),'energy':float(bo.fun)}

# Full wave, not just the reflected component. Substitution K=sqrt(2)sin(t)
# removes endpoint square root to improve Gaussian quadrature convergence.
def wave(u,tau,N=320,derivative=False):
    t,w=np.polynomial.legendre.leggauss(N);t=(t+1)*np.pi/4;w=w*np.pi/4
    K=np.sqrt(2)*np.sin(t);Q=np.sqrt(2)*np.cos(t);weights=w*np.sqrt(2)*np.cos(t)
    phase=(1-K*K+1j*K*Q)
    env=np.exp(-16*(K-1)**2-1j*K*K*tau/2)*weights
    inc=np.exp(1j*np.outer(np.atleast_1d(u),K));ref=phase*np.exp(-1j*np.outer(np.atleast_1d(u),K))
    return ((1j*K*(inc+ref)) if derivative else (inc-ref))@env
u=np.linspace(-30,0,301);s=''
for tau in (-20,-5,0,20):
    s+=plot([(u,abs(wave(u,tau))**2,'')],r'$u$',rf'$|a^{{1/2}}\Psi|^2,\ \tau={tau}$',height='3.6cm')
save('figure-804-ps8-reflection.tex',s)
peaks=[]
for N in (160,320,640,1280):
    dp=lambda u:float(2*(wave(u,20,N)[0].conjugate()*wave(u,20,N,derivative=True)[0]).real)
    root=brentq(dp,-19,-16,xtol=1e-13)
    peaks.append({'nodes':N,'peak':float(root),'density_derivative_residual':dp(root)})
receipt['full_reflection_packet_peaks']=peaks
assert abs(peaks[-1]['peak']+17.91783232261)<2e-6

# Green-kernel exact multi-delta states; separate vertical axes for each state.
def multidelta(n):
    pts=np.arange(n)-(n-1)/2;g=3;d=abs(pts[:,None]-pts[None,:])
    ss=[];lines=[];res=[]
    for j in range(n):
        f=lambda s: eigh(np.exp(-s*d),eigvals_only=True)[::-1][j]-s/g
        root=brentq(f,.01,2*g+1,xtol=1e-14);K=np.exp(-root*d);vals,vec=eigh(K);v=vec[:,-1-j]
        if v[-1]<0:v=-v
        H=np.exp(-root*d)*(d+1/root);v=v/np.sqrt(v@H@v)
        u=np.linspace(pts[0]-1.5,pts[-1]+1.5,401)
        y=np.exp(-root*abs(u[:,None]-pts))@v
        lines.append((u,y,rf'$n={j}$'));ss.append(root);res.append(float(np.max(abs(K@v-root/g*v))))
    receipt[f'{n}_delta']={'coupling':g,'kappa_a':ss,'kernel_residuals':res}
    return ''.join(plot([line],r'$x/a$',line[2],height='2.8cm') for line in lines)
save('figure-805-ps1-three-delta.tex',multidelta(3))
save('figure-theory-five-delta.tex',multidelta(5))

# Orthogonal polynomial projection: six exact coefficient formulas used below.
P=np.pi
as_=np.array([105*(P**4-153*P**2+1485)/(8*P**6),-315*(P**4-125*P**2+1155)/(4*P**8),693*(P**4-105*P**2+945)/(8*P**10)])
bs=np.array([-105*(2*P**2-27)/(8*P**4),315*(4*P**2-45)/(4*P**6),-1575*(2*P**2-21)/(8*P**8)])
x=np.linspace(-P,P,301)
sinproj=sum(as_[j]*x**(2*j+1) for j in range(3));cosproj=sum(bs[j]*x**(2*j) for j in range(3))
s=plot([(x,np.sin(x),'原函数'),(x,sinproj,'正交投影'),(x,x-x**3/6+x**5/120,'Taylor')],r'$x$',r'$\sin x$','legend pos=north west')
s+=plot([(x,np.cos(x),'原函数'),(x,cosproj,'正交投影'),(x,1-x*x/2+x**4/24,'Taylor')],r'$x$',r'$\cos x$','legend pos=north west')
save('figure-805-ps4-projection.tex',s)
receipt['projection']={'sin_coefficients':as_.tolist(),'cos_coefficients':bs.tolist(),'orthogonality_residuals':
 [quad(lambda x,i=i:(np.sin(x)-sum(as_[j]*x**(2*j+1)for j in range(3)))*x**i,-P,P)[0]for i in range(6)]+
 [quad(lambda x,i=i:(np.cos(x)-sum(bs[j]*x**(2*j)for j in range(3)))*x**i,-P,P)[0]for i in range(6)]}

g=np.r_[np.linspace(-3,-.08,160),np.nan,np.linspace(.08,3,160)]
# Separate branches; never connect across the undefined origin.
save('figure-805-ps8-squeezed.tex',plot([(g[:160],np.sqrt(2)/abs(np.tanh(g[:160])),''),(g[161:],np.sqrt(2)/abs(np.tanh(g[161:])),'')],r'$\gamma$',r'$\Delta N/\langle N\rangle$','ymin=0,ymax=10'))
th=np.linspace(0,np.pi/2,241)
save('figure-805-ps10-bell.tex',plot([(th,abs(np.cos(2*th)-np.cos(th))+np.cos(th),'量子预测'),(th,np.ones_like(th),'局域界')],r'$\theta$',r'$F(\theta)$','legend pos=south east'))

lines=[]
for n in range(1,4):
    z=np.linspace((n-.5)*P+.004,n*P-.004,101);y=-z/np.tan(z);keep=y<8;lines.append((z[keep],y[keep],rf'$n={n}$'))
for v in (2,4,7):
    z=np.linspace(0,v,101);lines.append((z,np.sqrt(v*v-z*z),rf'$v_0={v}$'))
save('figure-805-ps11-spherical.tex',plot(lines,r'$\eta$',r'$\epsilon$','ymin=0,ymax=8,legend pos=north west'))
x=np.linspace(.25,9,301)
s=plot([(x,6/x**2-c*np.exp(-x)/x,rf'$g^\prime={c}$')for c in (10,40,100)],r'$x$',r'$V_{\rm eff}$','ymin=-25,ymax=25')
x=np.linspace(0,10,301);y=x**3*(1-x/2)*np.exp(-x);y=y/max(abs(y))
s+=plot([(x,y,'定性径向态')],r'$x$',r'$u_2$','legend pos=north east')
save('figure-805-ps11-yukawa.tex',s)
b=np.linspace(-6,6,241)
save('figure-805-ps11-hyperfine.tex',plot([(b,1+b,r'$T_+$'),(b,1-b,r'$T_-$'),(b,-1+np.sqrt(b*b+4),r'$E_+$'),(b,-1-np.sqrt(b*b+4),r'$E_-$')],r'$\varepsilon/\varepsilon^\prime$',r'$E/\varepsilon^\prime$','legend pos=north west'))

I=quad(lambda t:np.sqrt(1-t**4),0,1,epsabs=1e-13)[0]
wkb=(np.pi/(2*np.sqrt(2)*I))**(4/3)*(np.arange(6)+.5)**(4/3)
orig=np.array([.667986,2.39364,4.69680,7.33573,10.2443,13.3793]);err=(wkb/orig-1)*100
tab=r'\begin{center}\begin{tabular}{rrrr}\toprule $n$&WKB&原题数值&相对误差(\%)\\\midrule'+'\n'
for n in range(6):tab+=f'{n}&{wkb[n]:.8f}&{orig[n]:.6f}&{err[n]:.6f}'+r'\\'+'\n'
save('table-806-ps4-quartic.tex',tab+r'\bottomrule\end{tabular}\end{center}'+'\n')
receipt['quartic_WKB']={'I':I,'energies':wkb.tolist(),'relative_errors_percent':err.tolist()}

# Interaction-picture first order system; exactly equivalent to specified B ODE.
tau=np.linspace(-25,25,801);gamma=.1
def lz(t,Y):
    ph=np.exp(1j*gamma*t*t/2)
    return [-1j*gamma*ph*Y[1],-1j*gamma/ph*Y[0]]
lzsol=solve_ivp(lz,(-25,25),[0j,1+0j],t_eval=tau,rtol=2e-11,atol=2e-13)
pr=abs(lzsol.y[1])**2;limit=np.exp(-2*P*gamma)
save('figure-806-ps7-landau-zener.tex',plot([(tau,pr,'有限端点积分'),(tau,np.full_like(tau,limit),'无穷时间公式')],r'$\tau$',r'$|B|^2$','legend pos=south west'))
receipt['landau_zener']={'finite_endpoint_survival':float(pr[-1]),'infinite_formula':float(limit),'norm_error':float(max(abs(np.sum(abs(lzsol.y)**2,axis=0)-1)))}
assert abs(pr[-1]-.5685032248)<1e-8
flux=np.linspace(-1,2,181)
save('figure-806-ps7-ab.tex',plot([(flux,(n-flux)**2,rf'$n={n}$')for n in range(-1,4)],r'$\eta$',r'$E/[\hbar^2/(2mb^2)]$','ymin=0,ymax=5'))

lines=[]
for j in range(6):
    lo=1e-4 if j==0 else (j-.5)*P+.025;hi=(j+.5)*P-.025
    z=np.linspace(lo,hi,81);lines.append((z,1-np.tan(z)/z,''))
s=plot(lines,r'$\gamma b$',r'$a/b$','ymin=-5,ymax=5')
x=np.linspace(0,3,181);lines=[]
for z in (0,P/4,P/2,P):
    if z==0:y=x
    else:y=np.where(x<=1,np.sin(z*x)/z,np.sin(z)/z+np.cos(z)*(x-1))
    lines.append((x,y,rf'$\gamma b={z/P:.2g}\pi$'))
s+=plot(lines,r'$r/b$',r'$u$','legend pos=north west')
save('figure-806-ps8-square-well.tex',s)
receipt['scattering_length_zero']=float(brentq(lambda z:np.tan(z)-z,P+.01,1.5*P-.01))
K=np.linspace(.001,10,2401);la=20
phase=np.unwrap(2*np.arctan2(-la*np.sin(K)**2,K+la*np.sin(K)*np.cos(K)))/2
# Retain enough adaptive density around the narrow peaks for truthful plot.
s=plot([(K[::3],phase[::3],r'$\lambda=20$')],r'$K=kR$',r'$\delta_0$')
s+=plot([(K[::3],(np.sin(phase)/K)[::3]**2,'壳势'),(K[::3],(np.sin(K)/K)[::3]**2,'硬球')],r'$K$',r'$\sigma_0/(4\pi R^2)$','legend pos=north east')
save('figure-806-ps8-delta-shell.tex',s)
receipt['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(ROOT/'qa/addition-numerics.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(f"Generated {len(receipt['figures'])} reproducible addition inputs.")
