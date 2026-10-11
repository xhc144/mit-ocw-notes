#!/usr/bin/env python3
"""Independent reproductions of OCW 8.09 Psets 9/10, no external notebook execution.
NumPy vectorized RK4; all times/damping/forcing are dimensionless.
Numerical evidence does not prove infinite-time chaos or exact periodicity.
"""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import root, brentq
ROOT=Path(__file__).resolve().parents[1]

def scan(kind,values,omega,steps=256,discard=500,keep=100):
    values=np.asarray(values,float); n=len(values); T=2*np.pi/omega;dt=T/steps
    # Columns x,w,u,v: state and one tangent direction; initial angle/current .2.
    y=np.tile([.2,0.,1.,0.],(n,1)); logs=np.zeros(n);samples=[]
    def rhs(t,z):
        x,w,u,v=z.T
        if kind=='rlc':
            f=-w/10-x**3+values*np.cos(omega*t);df=-3*x*x;damping=.1
        else:
            f=-np.sin(x)-values*np.cos(omega*t);df=-np.cos(x);damping=0.
        return np.column_stack([w,f,v,df*u-damping*v])
    for k in range((discard+keep)*steps):
        t=k*dt;k1=rhs(t,y);k2=rhs(t+dt/2,y+dt*k1/2);k3=rhs(t+dt/2,y+dt*k2/2);k4=rhs(t+dt,y+dt*k3)
        y+=dt*(k1+2*k2+2*k3+k4)/6
        if (k+1)%steps==0:
            norms=np.linalg.norm(y[:,2:],axis=1);y[:,2:]/=norms[:,None]
            period=(k+1)//steps
            if period>discard:
                logs+=np.log(norms);samples.append(y[:,:2].copy())
    data=np.asarray(samples)
    if kind=='pendulum': data[:,:,0]=(data[:,:,0]+np.pi)%(2*np.pi)-np.pi
    periods=[]
    for j in range(n):
        p=0
        for lag in [1,2,4,8,16]:
            d=data[-40:,j]-data[-40-lag:-lag,j]
            if kind=='pendulum':d[:,0]=(d[:,0]+np.pi)%(2*np.pi)-np.pi
            if np.max(np.linalg.norm(d,axis=1))<1e-5:p=lag;break
        periods.append(p)
    return data,logs/(keep*T),np.array(periods)

def single(kind,amp,omega,steps=512,discard=900,keep=120):
    from scipy.integrate import solve_ivp
    T=2*np.pi/omega
    def fun(t,y):
        x,w,u,v=y
        if kind=='rlc':return [w,-w/10-x**3+amp*np.cos(omega*t),v,-3*x*x*u-v/10]
        return [w,-np.sin(x)-amp*np.cos(omega*t),v,-np.cos(x)*u]
    # Independent adaptive solver; periodically normalize tangent.
    y=np.array([.2,0.,1.,0.]);samples=[];logs=[]
    for i in range(discard+keep):
        sol=solve_ivp(fun,[i*T,(i+1)*T],y,rtol=2e-10,atol=2e-12,max_step=T/64)
        y=sol.y[:,-1];norm=np.linalg.norm(y[2:]);y[2:]/=norm
        if i>=discard:samples.append(y[:2].copy());logs.append(np.log(norm))
    pts=np.array(samples)
    if kind=='pendulum':pts[:,0]=(pts[:,0]+np.pi)%(2*np.pi)-np.pi
    lag_errors={}
    for lag in [1,2,4,8,16]:
        d=pts[-40:]-pts[-40-lag:-lag]
        if kind=='pendulum':d[:,0]=(d[:,0]+np.pi)%(2*np.pi)-np.pi
        lag_errors[str(lag)]=float(np.max(np.linalg.norm(d,axis=1)))
    return pts,{'amplitude':amp,'finite_time_lyapunov_per_time':float(np.mean(logs)/T),'recurrence_errors':lag_errors,'discard_periods':discard,'observed_periods':keep,'solver':'solve_ivp, rtol 2e-10, atol 2e-12, maximum step T/64'}

def write_csv(name,cols,data):
    np.savetxt(ROOT/'figures'/name,data,delimiter=',',header=','.join(cols),comments='',fmt='%.10g')

def maps():
    result={};rs=np.linspace(3,4,501);x=np.full_like(rs,.2)
    for i in range(1500):x=rs*x*(1-x)
    samples=[]
    for i in range(60):x=rs*x*(1-x);samples.append(np.column_stack([rs,x]))
    write_csv('logistic-bifurcation.csv',['r','x'],np.vstack(samples))
    # Locate loss of stability of period p by f^p(x)=x and product f'(orbit)=-1.
    bif=[3.]
    for p,guess in [(2,[.44,3.449]),(4,[.36,3.544]),(8,[.35,3.5644])]:
        def equations(z):
            v,r=z;start=v;mu=1.
            for _ in range(p):mu*=r*(1-2*v);v=r*v*(1-v)
            return [v-start,mu+1]
        sol=root(equations,guess,tol=1e-12)
        if not sol.success and np.linalg.norm(equations(sol.x))>1e-9:raise RuntimeError('period boundary root did not converge')
        bif.append(float(sol.x[1]))
    result['logistic_period_doubling_r']=bif
    result['successive_ratios']=[(bif[i]-bif[i-1])/(bif[i+1]-bif[i]) for i in [1,2]]
    sensitivity=[]
    for r in [3.2,4.]:
        a,b=.2,.2+1e-10
        for i in range(81):sensitivity.append([r,i,abs(a-b)]);a=r*a*(1-a);b=r*b*(1-b)
    write_csv('map-sensitivity.csv',['r','n','delta'],sensitivity)
    for name,rs,fun in [('cosine',np.linspace(0,3,501),lambda r,x:r*np.cos(x)),('cubic',np.linspace(1,2.59,501),lambda r,x:r*x-x**3),('exponential',np.linspace(0,10,501),lambda r,x:np.exp(-r*x))]:
        x=np.full_like(rs,.2)
        for i in range(2000):x=fun(rs,x)
        samples=[]
        for i in range(40):x=fun(rs,x);samples.append(np.column_stack([rs,x]))
        write_csv(name+'-map.csv',['r','x'],np.vstack(samples))
    return result

def main():
    report={'initial_state':[.2,0.],'forcing_phase':0,'scope':'finite-time numerical evidence, no proof of exact periodicity or infinite-time chaos'}
    vals=np.linspace(6,11,301);data,le,per=scan('rlc',vals,2/3)
    write_csv('rlc-bifurcation.csv',['B','x'],np.column_stack([np.tile(vals,32),data[-32:,:,0].reshape(-1)]))
    write_csv('rlc-diagnostics.csv',['B','lyapunov','period'],np.column_stack([vals,le,per]))
    cases=[]
    for desired in [2,4]:
        inds=np.flatnonzero(per==desired)
        if len(inds):cases.append(float(vals[inds[len(inds)//2]]))
    inds=np.flatnonzero(le>.02)
    if len(inds):cases+= [float(vals[inds[len(inds)//3]]),float(vals[inds[2*len(inds)//3]])]
    report['rlc_scan_case_candidates']=cases
    report['rlc_scan_observed_periods']=sorted(set(map(int,per)))
    report['rlc_scan_max_lyapunov']=float(le.max())
    # Full adaptive verification supplied in a follow-up call after case selection.
    for name,lo,hi in [('pendulum-wide',.1,2),('pendulum-small',0,.1)]:
        vals=np.linspace(lo,hi,301);data,le,per=scan('pendulum',vals,.7,steps=384,discard=250,keep=100)
        write_csv(name+'-bifurcation.csv',['a','theta'],np.column_stack([np.tile(vals,32),data[-32:,:,0].reshape(-1)]))
        write_csv(name+'-diagnostics.csv',['a','lyapunov','period'],np.column_stack([vals,le,per]))
        report[name]={'max_finite_time_lyapunov':float(le.max()),'minimum_positive_above_002':float(vals[np.flatnonzero(le>.02)[0]]) if np.any(le>.02) else None,'periodic_candidate_parameters':vals[per>0].tolist()}
    report.update(maps())
    (ROOT/'qa/nonlinear-numerical-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
