"""Independent numerical reconstruction of MIT 22.615 Spring 2007 final.
High-beta ordering, three polynomial displacement harmonics; no fitted answers.
Coordinates are right handed (r,theta,z), z=-R0*phi; n=1 exp(i theta*m+i*z/R0).
Energy is scaled by the common positive toroidal volume / mu0 factor.
"""
import json
import os
from functools import lru_cache
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq, minimize_scalar

HERE=Path(__file__).resolve().parent
DEFAULT_OUT=HERE.parents[1]/'qa'/'numerics' if HERE.name=='mhd' else HERE
OUT=Path(os.environ.get('MHD_OUTPUT_DIR',DEFAULT_OUT))
OUT.mkdir(parents=True,exist_ok=True)
Q0=1.05

@lru_cache(None)
def angular_mesh(nth):
    # Split at theta=pi: near-separatrix variation is then at an endpoint,
    # where Gauss nodes resolve the narrow peak quadratically in nth.
    t,wt=leggauss(nth//2)
    return np.concatenate(((t+1)*np.pi/2,np.pi+(t+1)*np.pi/2)),np.concatenate((wt*np.pi/2,wt*np.pi/2))

def zcrit():
    return brentq(lambda z:z*np.log(z/(2-z))-2,1.01,1.99,xtol=1e-14)

def alpha_sep(z):
    L=np.log(z/(2-z))
    return np.sqrt(z*(2-z*L)/(L+2/(2-z)))

def nu_of(z,alpha):
    return alpha*np.log(z/(2-z))/(1-alpha*alpha/(z*(2-z)))

def qprime_of(nu):
    eta=np.sqrt(1+3*nu*nu)
    return Q0*np.sqrt(eta*(2+eta)/3)

def eq(z,alpha,nth=512):
    nu=nu_of(z,alpha); qp=qprime_of(nu)
    L=z/alpha; U=(2-z)/alpha
    if alpha<=0 or alpha>alpha_sep(z)*(1+1e-9) or U<1-1e-9:
        raise ValueError(('inadmissible',z,alpha,nu))
    chi=np.log(L)-nu/2*(L-1/L)
    theta,wt=angular_mesh(nth)
    c=np.cos(theta)
    lo=np.ones_like(theta); hi=np.full_like(theta,L)
    for _ in range(62):
        rb=(lo+hi)/2
        f=np.log(rb)+nu/2*(rb-1/rb)*c-chi
        hi=np.where(f>0,rb,hi); lo=np.where(f<=0,rb,lo)
    rb=(hi+lo)/2
    Ahat=alpha*alpha*np.sum(wt*rb*rb)/(2*np.pi)
    qa=qp*np.sum(wt*rb*rb/(1+nu/2*(rb+1/rb)*c))/(2*np.pi)
    qacore=qp/np.sqrt(1-nu*nu)
    qstar=qp*Ahat/alpha**2
    bte=nu/qp**2*alpha**3/Ahat
    return dict(zeta1=float(z),alpha=float(alpha),nuprime=float(nu),qprime=float(qp),
        area_hat=float(Ahat),qcore=float(qacore),qa=float(qa),qstar=float(qstar),
        inv_qstar=float(1/qstar),beta_over_epsilon=float(bte),chi_edge=float(chi)),(theta,rb)

def core_fields(nu,q,r,theta):
    c=np.cos(theta); s=np.sin(theta)
    br=nu/(2*q)*(r*r-1)*s
    bt=(r+nu/2*(3*r*r-1)*c)/q
    brr=nu/q*r*s; brt=nu/(2*q)*(r*r-1)*c
    btr=(1+3*nu*r*c)/q; btt=-nu/(2*q)*(3*r*r-1)*s
    j=2/q*(1+2*nu*r*c)
    pr=-2*r+nu*(1-3*r*r)*c
    pt=-nu*(1-r*r)*s # phat_theta / r
    return br,bt,brr,brt,btr,btt,j,pr,pt

def fluid_matrix(m,nu,q,nr=48,nth=64):
    z,w=leggauss(nr); r=(z[:,None]+1)/2
    t=np.arange(nth)[None,:]*2*np.pi/nth
    wt=w[:,None]/2*r*2*np.pi/nth
    br,bt,brr,brt,btr,btt,j,pr,pt=core_fields(nu,q,r,t)
    c=np.cos(t); s=np.sin(t)
    us=[]; vs=[]; Qrs=[]; Qts=[]
    for k in [m-1,m,m+1]:
        u=r**(k-1)*np.exp(1j*k*t); v=1j*u
        qr=(br*(k-1)/r+1j*k*bt/r-1j-brr-1j*brt/r)*u
        qt=(1j*br*(k-1)/r-k*bt/r+1+bt/r-btr-1j*(btt+br)/r)*u
        us.append(u);vs.append(v);Qrs.append(qr);Qts.append(qt)
    W=np.empty((3,3),complex)
    for i in range(3):
        for k in range(3):
            energy=np.conj(Qrs[i])*Qrs[k]+np.conj(Qts[i])*Qts[k]
            energy-=j*(np.conj(vs[i])*Qrs[k]-np.conj(us[i])*Qts[k])
            energy-=2*nu/q**2*(us[k]*pr+vs[k]*pt)*(-np.conj(us[i])*c+np.conj(vs[i])*s)
            W[i,k]=np.sum(wt*energy)
    asym=np.max(np.abs(W-W.conj().T)); imag=np.max(np.abs(W.imag))
    if asym>2e-10 or imag>2e-10: raise ValueError(('non-Hermitian',m,nu,q,asym,imag,W))
    return W.real

def vacuum_matrix(m,e):
    nu=e['nuprime']; q=e['qprime']; alpha=e['alpha']; qc=e['qcore']; qa=e['qa']
    js=np.arange(m-1,m+2); ls=np.arange(max(1,m-2),m+3)
    C=np.zeros((len(ls),3)); lambdas=[]; walls=[]
    for i,l in enumerate(ls):
        for k,j in enumerate(js):
            if l==j: C[i,k]=j/q-1
            if l==j+1: C[i,k]=nu*(j+1)/(2*q)
            if l==j-1: C[i,k]=nu*(j-1)/(2*q)
        if qc<l<qa:
            b2=1+(1/alpha**2-1)*(l-qc)/(qa-qc)
            ab_power=b2**(-l)
            lam=(1+ab_power)/(1-ab_power)
            walls.append(np.sqrt(b2))
        else:lam=1.;walls.append(None) # null denotes the specified wall at infinity
        lambdas.append(lam)
    W=2*np.pi*C.T@np.diag(np.array(lambdas)/ls)@C
    return W,dict(harmonics=ls.tolist(),C=C.tolist(),wall_over_core=walls,Lambda=lambdas)

def stability(m,e,nr=48,nth=64):
    WF=fluid_matrix(m,e['nuprime'],e['qprime'],nr,nth)
    WV,bc=vacuum_matrix(m,e)
    vals=np.linalg.eigvalsh(WF+WV)
    return dict(m=m,WF=WF.tolist(),WV=WV.tolist(),W=(WF+WV).tolist(),eigenvalues=vals.tolist(),boundary=bc)

@lru_cache(None)
def fluid_coefficients(m):
    C=np.diag([2*np.pi/j for j in [m-1,m,m+1]])
    As=[];Bs=[]
    for nu in [0.,1.,-1.]:
        W1=fluid_matrix(m,nu,1.);W2=fluid_matrix(m,nu,2.)
        As.append(2*W1-4*W2+2*C);Bs.append(4*W2-W1-3*C)
    return As[0],(As[1]-As[2])/2,(As[1]+As[2])/2-As[0],Bs[0],(Bs[1]-Bs[2])/2,C

def fast_fluid(m,nu,q):
    # Exact monomial radial integrals and Fourier angular orthogonality.
    js=np.arange(m-1,m+2,dtype=float)
    diag=2*(js-2)/q**2-4*(js-1)/(js*q)+2/js+nu*nu*js*(js-3)/((js+1)*q*q)
    W=np.diag(diag)
    for k,j in enumerate(js[:-1]):
        W[k,k+1]=W[k+1,k]=nu*((2*j-5)/q**2-2*(j-1)/((j+1)*q))
    W[0,2]=W[2,0]=nu*nu*(js[0]-3)/(2*q*q)
    return np.pi*W

def min_eigen(e,mrange=range(2,9)):
    vals=[]
    for m in mrange:
        WV,_=vacuum_matrix(m,e)
        vals.append(np.linalg.eigvalsh(fast_fluid(m,e['nuprime'],e['qprime'])+WV)[0])
    i=int(np.argmin(vals))
    return float(vals[i]),list(mrange)[i]

def checks():
    errs=[]
    for m in [2,3,5,8]:
        q=1.73;W=fluid_matrix(m,0,q)
        expected=np.diag([2*np.pi/j*(j/q-1)*((j-2)/q-1) for j in [m-1,m,m+1]])
        errs.append(np.max(abs(W-expected)))
    return dict(zeta_crit=zcrit(),max_cylindrical_fluid_error=float(max(errs)))

def main():
    report=checks(); rows=[]
    for z,al in [(1.1,.6),(1.25,.5),(1.4,.3),(1.55,.12)]:
        e,curve=eq(z,al)
        e['stability']=[stability(m,e) for m in range(2,9)]
        e['worst_eigenvalue']=min(k['eigenvalues'][0] for k in e['stability'])
        rows.append(e)
    report['sample_equilibria']=rows
    (OUT/'final_reference_results.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(dict(zeta_crit=report['zeta_crit'],cyl_error=report['max_cylindrical_fluid_error'],samples=[{k:e[k] for k in ['zeta1','alpha','nuprime','qstar','qa','beta_over_epsilon','worst_eigenvalue']} for e in rows]),indent=2))

if __name__=='__main__':main()
