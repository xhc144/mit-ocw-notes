"""Independent weak-moment solution of MIT 22.615 Spring 2007 midterm.
Uses the standard GS pressure coefficient (one mu0), not the printed typo.
No solutions/expected numerical conclusions were supplied to this review.
"""
import json
import os
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import root, brentq, minimize_scalar

HERE=Path(__file__).resolve().parent
DEFAULT_OUT=HERE.parents[1]/'qa'/'numerics' if HERE.name=='mhd' else HERE
OUT=Path(os.environ.get('MHD_OUTPUT_DIR',DEFAULT_OUT))
OUT.mkdir(parents=True,exist_ok=True)
KA=1.7; DA=.4; AL=.07
MU0=4*np.pi*1e-7; A=2.; R0=6.2; B0=5.3
EPS=A/R0 # .32 in the problem is rounded; this keeps dimensional q consistent.

def mesh(nr=72,nm=192):
    z,w=leggauss(nr)
    r=(z[:,None]+1)/2; mu=np.arange(nm)[None,:]*2*np.pi/nm
    return r,mu,w[:,None]/2*np.ones_like(mu)*2*np.pi/nm

def shape(r,mu,sig,kap,d0):
    D=np.arcsin(DA)*(d0*r*r+(1-d0)*r**4)
    Dr=np.arcsin(DA)*(2*d0*r+4*(1-d0)*r**3)
    t=mu+D*np.sin(mu); tr=Dr*np.sin(mu); tm=1+D*np.cos(mu)
    k=kap+(KA-kap)*r*r; kr=2*(KA-kap)*r
    x=sig*(1-r*r)+r*np.cos(t); y=k*r*np.sin(mu)
    xr=-2*sig*r+np.cos(t)-r*np.sin(t)*tr
    xm=-r*np.sin(t)*tm
    yr=(k+r*kr)*np.sin(mu); ym=k*r*np.cos(mu)
    jac=xr*ym-yr*xm; G=xm*xm+ym*ym; H=xr*xm+yr*ym
    return x,y,xr,xm,yr,ym,jac,G,H

def flux(r,lam=None):
    if lam is None: return r*r,2*r
    den=27*lam+5
    return (36*lam*r*r+9*(1-lam)*r**4-4*r**6)/den, (72*lam*r+36*(1-lam)*r**3-24*r**5)/den

def profile(p):
    h=(1-p)**2; hp=-2*(1-p)
    f=(1-p)**2*(1+3*AL+2*p)/(1+3*AL)
    fp=-6*(1-p)*(AL+p)/(1+3*AL)
    return h,hp,f,fp

def moment(v,beta,weights='poly',lam=None,nr=72,nm=192):
    l,C,sig,kap,d0=v
    r,mu,w=mesh(nr,nm)
    x,y,xr,xm,yr,ym,jac,G,H=shape(r,mu,sig,kap,d0)
    s=1+EPS*x; p,gp=flux(r,lam); h,hp,f,fp=profile(p)
    source=2*beta/l**2*(s*s-1)*hp+2*C*fp
    rb=np.ones((1,nm)); mb=mu
    xb,yb,xrb,xmb,yrb,ymb,jb,Gb,Hb=shape(rb,mb,sig,kap,d0)
    sb=1+EPS*xb; pb,gpb=flux(rb,lam)
    bd=gpb*Gb/(jb*sb); T=bd.sum()*2*np.pi/nm
    res=[l*T/(4*np.pi)-1]
    for n in range(4):
        if weights=='poly':
            W=[np.ones_like(x),x,x*x,y*y][n]
            Wb=[np.ones_like(xb),xb,xb*xb,yb*yb][n]
            Wx=[np.zeros_like(x),np.ones_like(x),2*x,np.zeros_like(x)][n]
            Wy=[np.zeros_like(x),np.zeros_like(x),np.zeros_like(x),2*y][n]
            grad=gp*(Wx*ym-Wy*xm)/s
        else:
            W=np.cos(n*mu)+np.zeros_like(r); Wb=np.cos(n*mb)
            Wmu=-n*np.sin(n*mu)
            grad=gp*(-Wmu*H)/(jac*s)
        residual=(Wb*bd).sum()*2*np.pi/nm-np.sum(w*grad)+np.sum(w*W*source*jac/s)
        res.append(residual/(4*np.pi))
    return np.array(res)

def solve(beta,start=None,weights='poly',lam=None,nr=72,nm=192):
    if start is None: start=np.array([.8,2.,.2,1.6,.4])
    sol=root(lambda v:moment(v,beta,weights,lam,nr,nm),start,tol=1e-10)
    if not sol.success or np.max(np.abs(sol.fun))>1e-8:
        raise ValueError((beta,sol.message,sol.x,sol.fun))
    r,mu,w=mesh(nr,nm)
    jac=shape(r,mu,*sol.x[2:])[6]
    if jac.min()<=0: raise ValueError(('folded map',beta,sol.x,jac.min()))
    return sol.x

def performance(beta,v,qstar=None,lam=None,nr=128,nm=512):
    l,C,sig,kap,d0=v
    r,mu,w=mesh(nr,nm)
    x,y,xr,xm,yr,ym,jac,G,H=shape(r,mu,sig,kap,d0)
    s=1+EPS*x; p,gp=flux(r,lam); h,hp,f,fp=profile(p)
    rr=np.linspace(1e-6,1,2001)[:,None]
    sh=shape(rr,mu,sig,kap,d0); ss=1+EPS*sh[0]
    pp,gpp=flux(rr,lam); hh,hpp,ff,fpp=profile(pp)
    HH=np.sum(sh[6]/ss,axis=1)*2*np.pi/nm/(np.pi*KA*l*gpp[:,0])
    VV=-beta*hh[:,0]+C*l*l*ff[:,0]
    def h_v_at(z):
        z=np.array([[z]]); sz=shape(z,mu,sig,kap,d0)
        pz,gpz=flux(z,lam); hz,hpz,fz,fpz=profile(pz)
        HZ=np.sum(sz[6]/(1+EPS*sz[0]))*2*np.pi/nm/(np.pi*KA*l*gpz[0,0])
        return HZ,float((-beta*hz+C*l*l*fz)[0,0])
    if qstar is None:
        target=4/HH**2-(EPS*KA)**2*VV
        k=int(np.argmax(target))
        lo=max(1e-7,rr[max(k-2,0),0]); hi=min(1.,rr[min(k+2,len(rr)-1),0])
        so=minimize_scalar(lambda z:-(4/h_v_at(z)[0]**2-(EPS*KA)**2*h_v_at(z)[1]),bounds=(lo,hi),method='bounded',options={'xatol':1e-12})
        qstar=np.sqrt(max(float(np.max(target)),-so.fun))
    q=HH*np.sqrt(qstar*qstar+(EPS*KA)**2*VV)
    tau=EPS*KA/qstar
    # Physical dimensions use the specified R0,a (EPS=.32 was for geometry).
    I=2*np.pi*A*A*KA*B0/(MU0*R0*qstar)
    p0=beta*MU0*I*I/(8*np.pi*np.pi*A*A)
    psib=MU0*R0*I*l/(4*np.pi)
    k0=2*C*psib*psib/(B0*B0*A*A*R0*R0)
    fact=1-2*MU0*p0/B0**2*h+2*k0*f
    qi=np.sum(jac/s,axis=1)*2*np.pi/nm*A*A*B0/(2*np.pi*psib*gp[:,0])*np.sqrt(fact[:,0])
    jb=-(4.7/6)*np.sqrt(R0)/(A**1.5*B0)*p0*qi*(hp[:,0]*gp[:,0])/np.sqrt(r[:,0])
    IB=np.sum(w*jac*jb[:,None])*A*A
    betav=2*MU0*p0/B0**2*np.sum(w*h*s*jac)/np.sum(w*s*jac)
    src=2*beta/l**2*(s*s-1)*hp+2*C*fp
    javg=-psib/(MU0*A*A*R0)*np.sum(src*jac,axis=1)/np.sum(s*jac,axis=1)
    jr=-(4.7/6)*np.sqrt(R0)/(A**1.5*B0)*p0*q*hpp[:,0]*gpp[:,0]/np.sqrt(rr[:,0])
    imin=int(np.argmin(q)); lo=max(1e-7,rr[max(imin-2,0),0]); hi=min(1.,rr[min(imin+2,len(rr)-1),0])
    so=minimize_scalar(lambda z:h_v_at(z)[0]**2*(qstar*qstar+(EPS*KA)**2*h_v_at(z)[1]),bounds=(lo,hi),method='bounded',options={'xatol':1e-12})
    result=dict(beta0=beta,l0=l,C0=C,sigma0=sig,kappa0=kap,delta0=d0,
        qstar=qstar,qmin=float(np.sqrt(so.fun)),rho_qmin=float(so.x),
        I_MA=I/1e6,p0_Pa=p0,beta=betav,fB=IB/I,IB_MA=IB/1e6,
        Troyon=.14*EPS*KA/qstar,min_Jacobian=float(np.min(jac)),
        F2_min=float(np.min(fact)))
    return result,(rr[:,0],q,jr),(r[:,0],qi,jb,javg)

def main():
    lam=.2; weights='cos'
    rows=[]; v=None
    for beta in np.linspace(0,1.8,19):
        v=solve(beta,v,weights=weights,lam=lam)
        rr,profile,prof=performance(beta,v,lam=lam)
        rows.append(rr)
    (OUT/'midterm_scan.json').write_text(json.dumps(rows,indent=2))
    last=None
    def fb_at(b):
        vv=solve(b,weights=weights,lam=lam)
        return performance(b,vv,lam=lam)[0]['fB']-.75
    bb=brentq(fb_at,1,1.8,xtol=2e-9)
    vv=solve(bb,weights=weights,lam=lam); result,pro,pr=performance(bb,vv,lam=lam)
    result['path']='midterm_help cosine moments, lambda=0.2, qmin=2'
    result['lambda']=lam
    result['epsilon']=EPS
    result['moment_residual_max']=float(np.max(np.abs(moment(vv,bb,weights=weights,lam=lam,nr=144,nm=768))))
    result['current_drive_MA']=1.2*40/(4*R0)
    result['drive_required_MW']=.25*result['I_MA']*4*R0/1.2
    (OUT/'midterm_75.json').write_text(json.dumps(result,indent=2))
    np.savetxt(OUT/'midterm_q_bootstrap.csv',np.column_stack(pro),delimiter=',',header='rho,q,JB_A_m2',comments='')
    np.savetxt(OUT/'midterm_currents.csv',np.column_stack(pr),delimiter=',',header='rho,q,JB_A_m2,Jtotal_avg_A_m2',comments='')
    m=np.linspace(0,2*np.pi,361)[None,:]
    surf=[]
    for r in np.linspace(.1,1,10):
        sh=shape(np.array([[r]]),m,*vv[2:]); surf.append(np.column_stack([np.full(361,r),sh[0].ravel(),sh[1].ravel()]))
    np.savetxt(OUT/'midterm_flux_surfaces.csv',np.vstack(surf),delimiter=',',header='rho,x,y',comments='')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
