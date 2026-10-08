#!/usr/bin/env python3
"""Reproduce MIT 18.330 PS1--PS6 numerical work (AI-authored, not MIT code).
Run from any directory. Requires Python 3, NumPy, SciPy, Matplotlib, mpmath.
Figures/data are written beside this script and in ../figures/assessments/.
"""
from pathlib import Path
import json, math
import numpy as np
from scipy.linalg import solve_banded, eigh_tridiagonal
from scipy.interpolate import CubicSpline
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
FIG=HERE.parent/'figures'/'assessments'; FIG.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'figure.figsize':(6.8,3.4),'savefig.bbox':'tight'})
results={}
def save(name):
    plt.tight_layout();plt.savefig(FIG/(name+'.pdf'),metadata={'CreationDate':None,'ModDate':None});plt.close()
def slope(h,e): return float(np.polyfit(np.log(h[-5:]),np.log(np.asarray(e)[-5:]),1)[0])
def csv(name,rows,header): np.savetxt(HERE/(name+'.csv'),rows,delimiter=',',header=header,comments='')
# PS1: count TERMS, not last summation index; 3 decimal place absolute accuracy.
s=0.; first=None
for m in range(1,2001):
    s+=(-1.)**(m-1)/(2*m-1)
    if abs(s-math.pi/4)<=.0005 and first is None:first=(m,s)
assert first[0]==500
results['ps1_pi']={'accuracy_definition':'absolute error <= 0.5e-3','terms':first[0],'sum':first[1],'exact':math.pi/4}
mp.mp.dps=90
rows=[]
for N in [25,50,75,100,125,150,200]:
    t=s=1.; st=tt=mp.mpf(1)
    for n in range(1,N+1):
        t*=(-25.)/n;s+=t
        tt*=mp.mpf(-25)/n;st+=tt
    rows.append([N,s,float(st),float(mp.exp(-25))])
results['ps1_cancellation']=[{'N':int(r[0]),'double':r[1],'90_digit_sum':r[2],'exact':r[3]} for r in rows]
csv('ps1_cancellation',rows,'last_index_N,double,high_precision,exact')
# PS2: quadrature and finite differences.
f=lambda x:x/(1+x**4)
df=lambda x:(1-3*x**4)/(1+x**4)**2
g=lambda x:(x+1)**3*(x-2)**2
If=.5*(math.atan(4)-math.atan(1));Ig=3**6/60
Ns=2**np.arange(5,16);hs=3/Ns
rows=[]
for N,h in zip(Ns,hs):
    x=np.linspace(-1,2,N+1);y=f(x);z=g(x)
    rect=h*np.sum(y[:-1]);trap=h*(np.sum(y[1:-1])+(y[0]+y[-1])/2)
    rg=h*np.sum(z[:-1]);tg=h*(np.sum(z[1:-1])+(z[0]+z[-1])/2)
    forward=(y[2:]-y[1:-1])/h;center=(y[2:]-y[:-2])/(2*h)
    rows.append([N,h,abs(rect-If),abs(trap-If),abs(rg-Ig),abs(tg-Ig),np.max(abs(forward-df(x[1:-1]))),np.max(abs(center-df(x[1:-1])))])
a=np.array(rows);csv('ps2_convergence',a,'N,h,f_rectangle,f_trapezoid,g_rectangle,g_trapezoid,forward,centered')
results['ps2']={'integral_f':If,'integral_g':Ig,'derivative_f_at_1':df(1),'observed_orders':{k:slope(hs,a[:,j]) for k,j in [('rectangle_f',2),('trapezoid_f',3),('rectangle_g',4),('trapezoid_g',5),('forward',6),('centered',7)]}}
results['ps2']['observed_orders']['rectangle_g']=float(np.polyfit(np.log(hs[:5]),np.log(a[:5,4]),1)[0])
results['ps2']['observed_orders']['trapezoid_g']=float(np.polyfit(np.log(hs[:5]),np.log(a[:5,5]),1)[0])
results['ps2']['g_fit_note']='First five grids; finer errors reach the floating-point floor.'
assert abs(results['ps2']['observed_orders']['rectangle_g']-4)<.001
for cols,name in [([2,3,4,5],'ps2_quadrature'),([6,7],'ps2_differences')]:
    for j in cols:plt.loglog(hs,a[:,j],'.-',label=['','','Rectangle f','Trapezoid f','Rectangle g','Trapezoid g','Forward','Centered'][j])
    plt.xlabel('h');plt.ylabel('Absolute error');plt.legend();plt.grid(True,which='both',alpha=.25);save(name)
# PS3: explicit clamped cubic spline second derivative system.
N=10;x=np.arange(N+1,dtype=float);y=np.ones(N+1);y[1]=0
B=np.zeros((3,N+1));B[1]=4;B[1,0]=B[1,-1]=2;B[0,1:]=1;B[2,:-1]=1
rhs=np.r_[6*(y[1]-y[0]),6*(y[2:]-2*y[1:-1]+y[:-2]),-6*(y[-1]-y[-2])]
M=solve_banded((1,1),B,rhs)
xx=np.linspace(0,N,2001);j=np.minimum(xx.astype(int),N-1);t=xx-j
cubic=M[j]*(1-t)**3/6+M[j+1]*t**3/6+(y[j]-M[j]/6)*(1-t)+(y[j+1]-M[j+1]/6)*t
ref=CubicSpline(x,y,bc_type=((1,0.),(1,0.)))
assert np.max(abs(cubic-ref(xx)))<1e-13
z=np.zeros(N+1)
for j0 in range(N):z[j0+1]=-z[j0]+2*(y[j0+1]-y[j0])
quad=y[j]+z[j]*t+(z[j+1]-z[j])*t**2/2
left_derivative=-M[0]/3-M[1]/6+y[1]-y[0]
right_derivative=M[-2]/6+M[-1]/3+y[-1]-y[-2]
assert abs(left_derivative)+abs(right_derivative)<1e-12
results['ps3']={'second_derivatives':M.tolist(),'quadratic_slopes':z.tolist(),'cubic_vs_scipy_max_error':float(np.max(abs(cubic-ref(xx)))),'endpoint_derivatives':[float(left_derivative),float(right_derivative)]}
csv('ps3_splines',np.c_[xx,cubic,quad],'x,clamped_cubic,quadratic')
plt.plot(xx,cubic,label='Clamped cubic');plt.plot(xx,quad,label='Quadratic');plt.plot(x,y,'ko',ms=3);plt.xlabel('x');plt.ylabel('s(x)');plt.legend();plt.grid(alpha=.25);save('ps3_splines')
# PS4: Newton iterations, with residual checks.
v=1.;seq=[v]
for _ in range(7):v=(2*v+3/v**2)/3;seq.append(v)
results['ps4_cube_root']={'iterates':seq,'value':v,'residual':v**3-3}
def newton(fun,jac,v):
    history=[];v=np.array(v,dtype=float)
    for _ in range(30):
        r=fun(v);history.append([*v,float(np.linalg.norm(r,np.inf))])
        if np.linalg.norm(r,np.inf)<5e-14:break
        v-=np.linalg.solve(jac(v),r)
    assert np.linalg.norm(fun(v),np.inf)<1e-11
    return v,history
fun=lambda x:np.array([x@x-100,np.prod(x)-1,x[0]-x[1]-np.sin(x[2])])
jac=lambda x:np.array([2*x,[x[1]*x[2],x[0]*x[2],x[0]*x[1]],[1.,-1.,-np.cos(x[2])]])
v,hist=newton(fun,jac,[7.,7.,.02]);csv('ps4_system_iterations',hist,'x1,x2,x3,residual_inf');results['ps4_system']={'initial':[7,7,.02],'solution':v.tolist(),'residual':fun(v).tolist()}
def F(q):
    V,I,R=q;d=V-R*I;return d*d+10*((R-2)**2+(V-2.9)**2+(I-1.4)**2)
def grad(q):
    V,I,R=q;d=V-R*I;return 2*d*np.array([1.,-R,-I])+20*(q-np.array([2.9,1.4,2.]))
def hess(q):
    V,I,R=q;d=V-R*I;r=np.array([1.,-R,-I]);D=np.array([[0.,0.,0.],[0.,0.,-1.],[0.,-1.,0.]])
    return 2*np.outer(r,r)+2*d*D+20*np.eye(3)
v,hist=newton(grad,hess,[2.9,1.4,2.]);csv('ps4_fit_iterations',hist,'V,I,R,gradient_inf');results['ps4_fit']={'minimizer':v.tolist(),'minimum':F(v),'gradient_inf':float(np.linalg.norm(grad(v),np.inf)),'hessian_eigenvalues':np.linalg.eigvalsh(hess(v)).tolist()}
# PS5: phase trajectories, stability and nonlinear decay.
h=.1;steps=200;A=np.array([[0.,1.],[-1.,0.]])
updates={'Forward Euler':np.eye(2)+h*A,'Backward Euler':np.linalg.inv(np.eye(2)-h*A),'Trapezoidal':np.linalg.solve(np.eye(2)-h*A/2,np.eye(2)+h*A/2)}
phase={}
for name,Q in updates.items():
    trajectory=[np.array([0.,1.])]
    for _ in range(steps):trajectory.append(Q@trajectory[-1])
    arr=np.array(trajectory);phase[name]={'final_radius':float(np.linalg.norm(arr[-1])),'max_radius_error':float(np.max(abs(np.linalg.norm(arr,axis=1)-1)))}
    plt.plot(arr[:,0],arr[:,1],label=name)
t=np.linspace(0,2*np.pi,500);plt.plot(np.sin(t),np.cos(t),'k--',lw=.7);plt.axis('equal');plt.xlabel('y');plt.ylabel('z');plt.legend();plt.grid(alpha=.25);save('ps5_phase');results['ps5_phase']=phase
trajs={}
for h in [.005,.01,.015,.02,.021]:
    ts=np.arange(round(.3/h)+1)*h;ys=[100.]
    for _ in ts[1:]:
        with np.errstate(over='ignore',invalid='ignore'):yn=np.float64(ys[-1])-h*np.float64(ys[-1])**2
        ys.append(float(yn))
    vals=np.array(ys);trajs[str(h)]={'first_values':ys[:5],'final':ys[-1] if np.isfinite(ys[-1]) else 'overflow to -infinity','min':float(np.min(vals)) if np.all(np.isfinite(vals)) else '-infinity','max':float(np.max(vals))}
    plt.plot(ts,np.clip(vals,-130,110),'.-',label=f'h={h:g}')
t=np.linspace(0,.3,400);plt.plot(t,1/(t+.01),'k--',label='Exact');plt.ylim(-130,110);plt.xlabel('t');plt.ylabel('y (clipped below -130)');plt.legend(ncol=2);plt.grid(alpha=.25);save('ps5_nonlinear');results['ps5_nonlinear']=trajs
# PS6: eliminate U0=U1; reduced unknowns j=1,...,N-1.
def mixed_system(N):
    h=1/N;m=N-1;diag=np.full(m,2/h**2);diag[0]=1/h**2;off=np.full(m-1,-1/h**2)
    return h,diag,off
N=256;h,d,e=mixed_system(N);lam,V=eigh_tridiagonal(d,e,select='i',select_range=(0,2));x=np.arange(N)/N
for k in range(3):
    vv=np.r_[V[0,k],V[:,k]];vv/=vv[0];plt.plot(x,vv,label=f'Discrete n={k}')
    plt.plot(x,np.cos((k+.5)*np.pi*x),'--',lw=.8)
plt.xlabel('x');plt.ylabel('Eigenfunction (v(0)=1)');plt.legend();plt.grid(alpha=.25);save('ps6_eigenvectors')
results['ps6_eigenvalues']={'N':N,'discrete':lam.tolist(),'continuous':[((k+.5)*np.pi)**2 for k in range(3)]}
rows=[]
for N in 2**np.arange(4,13):
    h,d,e=mixed_system(N);B=np.zeros((3,N-1));B[1]=d;B[0,1:]=e;B[2,:-1]=e;U1=solve_banded((1,1),B,np.ones(N-1));U=np.r_[U1[0],U1];x=np.arange(N)*h;exact=(1-x*x)/2
    closed=exact-h*(1-x)/2
    assert np.max(abs(U-closed))<2e-10
    rows.append([N,h,np.sqrt(h*np.sum((exact-U)**2)),np.sqrt(h*np.sum((exact-closed)**2))])
a=np.array(rows);csv('ps6_convergence',a,'N,h,error_L2h,closed_form_error');results['ps6_convergence']={'order':slope(a[:,1],a[:,2]),'errors':a[:,2].tolist()}
plt.loglog(a[:,1],a[:,2],'.-',label='Mixed BVP error');plt.xlabel('h');plt.ylabel('Discrete L2 error');plt.grid(True,which='both',alpha=.25);plt.legend();save('ps6_convergence')
# Sample code paths required to verify all computation-dependent answers.
assert results['ps4_fit']['minimum']<.01
assert phase['Trapezoidal']['max_radius_error']<1e-12
assert z.tolist()==[0.,-2.,4.,-4.,4.,-4.,4.,-4.,4.,-4.,4.]
(HERE/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2,allow_nan=False))
