#!/usr/bin/env python3
"""Reproducible original numerical figures, not scans of source figures."""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from scipy.linalg import eigh_tridiagonal
ROOT=Path(__file__).resolve().parents[1]
def f(lam):
    g=lambda x: np.exp(-100*(x-2)**2+50j*(x-lam*x**4/32))
    return quad(lambda x:g(x).real,1,3,epsabs=1e-12)[0]+1j*quad(lambda x:g(x).imag,1,3,epsabs=1e-12)[0]
opt=minimize_scalar(lambda x:-abs(f(x)),bounds=(.7,1),method='bounded',options={'xatol':1e-13})
receipt={'integral_lambda_star':{'lambda':1,'value':[f(1).real,f(1).imag],'magnitude':abs(f(1))},'integral_numeric_maximum':{'lambda':opt.x,'value':[f(opt.x).real,f(opt.x).imag],'magnitude':abs(f(opt.x))},'well_phase_endpoints':[]}
def coords(x,y,stride=1):return ' '.join(f'({a:.8g},{b:.8g})' for a,b in zip(x[::stride],y[::stride]))
def graph(name,lines,xlabel,ylabel,extra='',width='0.78\\textwidth',height='4.5cm'):
    s='\\begin{center}\\begin{tikzpicture}\n\\begin{axis}[width='+width+',height='+height+',xlabel={'+xlabel+'},ylabel={'+ylabel+'},grid=major,legend style={font=\\small},'+extra+']\n'
    for x,y,label in lines:
        s+='\\addplot+[mark=none] coordinates{'+coords(x,y)+'};\n'
        if label:s+='\\addlegendentry{'+label+'}\n'
    s+='\\end{axis}\\end{tikzpicture}\\end{center}\n'
    (ROOT/'chapters'/name).write_text(s)
l=np.linspace(0,1,151);graph('figure-ps9-integral.tex',[(l,np.array([abs(f(x))for x in l]),'')],r'$\lambda$',r'$|f(\lambda)|$')
lines=[]
for z,end in [(2,15),(5,20),(9,30)]:
 u=np.linspace(1e-7,end,12001);v=np.sqrt(u*u+z*z);a=np.unwrap(np.angle(v*np.cos(v)+1j*u*np.sin(v)));delta=a-u-a[0]
 receipt['well_phase_endpoints'].append({'z0':z,'u_end':end,'delta':delta[-1],'delta_over_pi':delta[-1]/np.pi,'bound_count':int(np.floor(z/np.pi+.5))})
 lines.append((u[::40],delta[::40]/np.pi,f'$z_0={z}$'))
graph('figure-ps9-well-phase.tex',lines,r'$u=ka$',r'$\delta/\pi$',extra='legend pos=south west')
u=np.linspace(1e-7,35,14001);z=5;theta=np.empty_like(u);lower=u<z;w=np.sqrt(z*z-u[lower]**2);theta[lower]=np.arctan2(u[lower]*np.sinh(w),w*np.cosh(w));v=np.sqrt(u[~lower]**2-z*z);theta[~lower]=np.arctan2(u[~lower]*np.sin(v),v*np.cos(v));delta=np.unwrap(theta)-u
graph('figure-ps9-barrier-phase.tex',[(u[::40],delta[::40]/np.pi,'')],r'$u=ka$',r'$\delta/\pi$')
def deltafun(u):return np.arctan2(-10*np.sin(u)**2,u+5*np.sin(2*u))
def amp(u):return 1/np.sqrt(1+10*np.sin(2*u)/u+100*np.sin(u)**2/u**2)
u=np.linspace(1e-5,10,18001);d=deltafun(u);delay=np.gradient(d,u);a=amp(u)
res=[]
for lo,hi in [(2.4,3.13),(5.3,6.27),(8.3,9.42)]:
 rr=minimize_scalar(lambda u:-amp(u),bounds=(lo,hi),method='bounded');x=rr.x;h=1e-5
 res.append({'u_amplitude_peak':x,'amplitude':amp(x),'dimensionless_delay':(deltafun(x+h)-deltafun(x-h))/(2*h)})
receipt['delta_wall_resonances']=res
graph('figure-ps9-delta-phase.tex',[(u[::40],d[::40],'')],r'$u=ka$',r'$\delta$')
graph('figure-ps9-delta-delay.tex',[(u[::25],delay[::25],'')],r'$u=ka$',r'$\mathrm d\delta/\mathrm du$')
graph('figure-ps9-delta-amplitude.tex',[(u[::25],a[::25],'')],r'$u=ka$',r'$|A|$')
# Test2 uses a numerical model of the qualitative central hump; not invented exact source data.
x=np.linspace(-1,1,1601);h=x[1]-x[0];V=np.where(abs(x)<.6,6*(1-(x/.6)**2),0);E,U=eigh_tridiagonal(.15*2/h**2+V[1:-1],np.full(len(x)-3,-.15/h**2),select='i',select_range=(0,4));receipt['test2_qualitative_model']={'kinetic_coefficient':.15,'hump_height':6,'hump_halfwidth':.6,'energies':E.tolist(),'not_source_exact_data':True}
for n in [0,1,4]:
 y=np.r_[0,U[:,n],0];y=y/max(abs(y));y*=1 if y[np.argmax(abs(y))]>0 else -1
 graph(f'figure-test2-wave{n+1}.tex',[(x[::8],y[::8],'')],r'$x/a$',r'$\psi_{'+str(n+1)+'}$',extra='xmin=-1,xmax=1,ymin=-1.2,ymax=1.2',height='3cm')
(ROOT/'qa/assessment-numerics.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
