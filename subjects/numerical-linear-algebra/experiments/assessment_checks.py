"""Independent reproducible numerical verification of MIT assessment solutions.
Run Python 3 with numpy, scipy, matplotlib, mpmath installed; fixed seed 18335.
Julia programming tasks are also run by assessment_checks.jl (stdlibs only).
"""
from pathlib import Path
from decimal import Decimal,localcontext
import math,json,hashlib,csv,platform
import numpy as np
import scipy,scipy.linalg as la
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
QA_DIR=ROOT/'qa';QA_DIR.mkdir(exist_ok=True)
rng=np.random.default_rng(18335);checks=[]
def check(name,value,limit,detail=None):
    value=float(value);limit=float(limit)
    row={'name':name,'value':value,'limit':limit,'passed':value<=limit}
    if detail is not None:row['detail']=detail
    checks.append(row)
    if not row['passed']:raise AssertionError(row)
def rel(a,b):return abs(a-b)/abs(b)
# Scalar cancellation: high precision reference for exact floating-point inputs.
mp.mp.dps=150
x=1.0;y=1e-20
cotgood=(math.sin(y)/math.sin(x))/math.sin(x+y)
ref=mp.cot(mp.mpf(x))-mp.cot(mp.mpf(x)+mp.mpf(y))
check('PS1 Q2 cotdiff relative error',float(abs(mp.mpf(cotgood)-ref)/abs(ref)),2e-15)
with localcontext() as ctx:
    ctx.prec=1100;x=Decimal(2);digits=[];ratios=[]
    for k in range(7):
        e=x-1;f=x*x*x-1;fp=3*x*x;fpp=6*x;D=fp*fp-2*f*fpp
        d=f/fp if D<0 else 2*f/(fp+D.sqrt())
        x-=d;new=x-1;digits.append(float(-abs(new).log10()));ratios.append(float(new/(e**3)))
    check('PS1 Q3 cubic constant',abs(ratios[-1]+1/3),1e-10)
# Draw data produced by actual Julia binary32 operations.
data=np.genfromtxt(ROOT/'experiments/julia-results/summation.csv',delimiter=',',names=True)
fig,ax=plt.subplots(figsize=(6.8,3.3),layout='constrained')
for key,label in [('sequential','sequential'),('pairwise','pairwise'),('blocked','pairwise, cutoff 200')]:
    ax.loglog(data['n'],np.maximum(data[key],1e-18),'.-',label=label)
ax.loglog(data['n'],data['bound_pairwise'],'k--',label='pairwise worst-case bound')
ax.loglog(data['n'],data['bound_blocked'],'k:',label='blocked worst-case bound')
ax.set(xlabel='number of binary32 inputs',ylabel='relative summation error')
ax.legend(fontsize=8);ax.grid(True,which='both',alpha=.2)
fig.savefig(ROOT/'experiments/assessment-summation.pdf');plt.close(fig)
# PS2 matrix norm and conditioning derivative.
A=rng.normal(size=(10,7));B=A[np.ix_([0,2,3],[1,2,4,5])]
check('PS2 Q2 submatrix norm ratio',np.linalg.norm(B,2)/np.linalg.norm(A,2),1)
x=rng.normal(size=7);v=rng.normal(size=10);v/=np.linalg.norm(v)
E=np.outer(v,x)/np.linalg.norm(x)
check('PS2 Q3 Frobenius derivative attained',abs(np.linalg.norm(E@x)/np.linalg.norm(E,'fro')-np.linalg.norm(x)),1e-12)
# Three SVD claims, rectangular and rank deficient.
U,s,Vh=np.linalg.svd(A,full_matrices=True)
M=np.block([[np.zeros((7,7)),A.T],[A,np.zeros((10,10))]])
for i in range(7):
    z=np.r_[Vh[i],U[:,i]]/np.sqrt(2)
    check(f'PS2 Q4 dilation eigenpair {i}',np.linalg.norm(M@z-s[i]*z),2e-13)
# Equal-modulus power iteration and two-column Ritz extraction.
A=np.diag([2.,-2.,.4]);x=np.array([1.,.7,.5]);x/=np.linalg.norm(x)
prev=x.copy()
for k in range(30):prev,x=x,A@x/np.linalg.norm(A@x)
Q=np.linalg.qr(np.column_stack([prev,x]))[0];vals,Z=np.linalg.eig(Q.T@A@Q)
check('PS4 Q2 two-vector Ritz eigenvalues',np.max(np.abs(np.sort(vals)-[-2,2])),1e-12)
check('PS4 Q2 eigen residual',np.linalg.norm(A@Q@Z-Q@Z@np.diag(vals)),1e-11)
# Perturbed near-singular solve: large scale error, small normalized direction error.
A=np.diag([1e-20,1.,3.]);E=np.diag([1e-16,2e-16,-3e-16]);b=np.array([1.,1.,1.])
w=np.linalg.solve(A,b);wt=np.linalg.solve(A+E,b)
check('PS4 Q3 normalized inverse direction',np.linalg.norm(wt[1:])/np.linalg.norm(wt),2e-15,
      {'unnormalized_relative_error':float(np.linalg.norm(wt-w)/np.linalg.norm(w))})
# 2019 Q3 logsumexp: retain small tail via log1p.
def lse(x):
    j=int(np.argmax(x));M=float(x[j]);t=math.fsum(math.exp(float(v)-M) for i,v in enumerate(x) if i!=j)
    return M+math.log1p(t)
for vals in [[1000.,1001.],[-1000.,-1001.],[1e-20,math.log(1e-20)]]:
    ref=mp.log(mp.fsum(mp.exp(mp.mpf(v)) for v in vals))
    check('2019 Q3 logsumexp '+str(vals),float(abs(mp.mpf(lse(vals))-ref)/abs(ref)),2e-14)
# 2019 Q4 tridiagonal determinant including zero intermediate minor.
def detrec(d,b,z):
    p0=1.;p1=d[0]-z
    for k in range(1,len(d)):p0,p1=p1,(d[k]-z)*p1-abs(b[k-1])**2*p0
    return p1
for m in [2,6]:
    d=rng.normal(size=m);b=rng.normal(size=m-1)+1j*rng.normal(size=m-1)
    T=np.diag(d)+np.diag(b,1)+np.diag(b.conj(),-1)
    for z in [d[0],.2,.7+1j]:
        a=detrec(d,b,z);r=np.linalg.det(T-z*np.eye(m))
        check(f'2019 Q4 det recurrence m={m},z={z}',abs(a-r)/max(1,abs(r)),2e-13)
# 2008 Q1 explicit Schur row substitution, disjoint spectra.
A=rng.normal(size=(4,4))+4*np.eye(4);B=rng.normal(size=(3,3))-4*np.eye(3);C=rng.normal(size=(4,3))
TA,QA=la.schur(A,output='complex');TB,QB=la.schur(B,output='complex');Cp=QA.conj().T@C@QB;Xp=np.zeros_like(Cp)
for j in reversed(range(4)):
    rhs=Cp[j]-TA[j,j+1:]@Xp[j+1:]
    Xp[j]=la.solve_triangular((TA[j,j]*np.eye(3)-TB).T,rhs,lower=True)
X=QA@Xp@QB.conj().T
check('2008 Q1 Sylvester row substitution',np.linalg.norm(A@X-X@B-C)/np.linalg.norm(C),1e-12)
# PSD conjugate gradients: null component preserved.
def cg(A,b,x,maxiter):
    x=x.copy();r=b-A@x;p=r.copy()
    for k in range(maxiter):
        rr=r@r
        if np.sqrt(rr)<1e-13:break
        Ap=A@p;alpha=rr/(p@Ap);x+=alpha*p;r-=alpha*Ap;p=r+(r@r)/rr*p
    return x
A=np.diag([0.,0.,1.,2.,5.]);b=np.array([0.,0.,1.,2.,3.]);x0=rng.normal(size=5);x=cg(A,b,x0,4)
check('2008 Q3 CG null component',np.linalg.norm(x[:2]-x0[:2]),1e-14)
check('2008 Q3 CG residual',np.linalg.norm(A@x-b),1e-12)
x=cg(A,np.zeros(5),x0,4);check('2008 Q3 null vector construction',np.linalg.norm(A@x),1e-12)
# 2008 Q5 rectangular block condition number.
B=rng.normal(size=(5,3));B*=.6/np.linalg.norm(B,2)
M=np.block([[np.eye(5),B],[B.T,np.eye(3)]])
check('2008 Q5 rectangular block condition',abs(np.linalg.cond(M)-4),1e-12)
# 2008 Q6 Cholesky-weighted QR.
A=rng.normal(size=(8,3));b=rng.normal(size=8);S=rng.normal(size=(8,8));W=S.T@S+np.eye(8);R=la.cholesky(W)
Q,T=np.linalg.qr(R@A);x=la.solve_triangular(T,Q.T@R@b)
check('2008 Q6 weighted stationarity',np.linalg.norm(A.T@W@(A@x-b))/np.linalg.norm(A.T@W@b),2e-13)
# 2009 Q1 merge block QR and exact structural triangularity.
A=rng.normal(size=(12,6));Q1,R1=np.linalg.qr(A[:,:3]);Q2,R2=np.linalg.qr(A[:,3:]);C=Q1.T@Q2;V=Q2-Q1@C;R=la.cholesky(V.T@V);Q2p=la.solve_triangular(R.T,V.T,lower=True).T;Q=np.column_stack([Q1,Q2p]);T=Q.T@A
check('2009 Q1 merged orthogonality',np.linalg.norm(Q.T@Q-np.eye(6)),1e-12)
check('2009 Q1 original-column triangularity',np.linalg.norm(np.tril(T,-1)),1e-12)
# 2009 Q2 missing simple eigenvalue => exact subspace closure.
A=np.diag([1.,2.,3.,4.]);b=np.array([1.,0.,2.,3.]);K=np.column_stack([b,A@b,A@A@b]);Q=np.linalg.qr(K)[0];T=Q.T@A@Q
check('2009 Q2 excluded eigenvalue',np.max(np.abs(np.sort(np.linalg.eigvalsh(T))-[1,3,4])),1e-12)
# 2009 Q3 absorb b perturbation into A (including ill-conditioned A).
A=np.diag([1e-10,2.,3.]);E=rng.normal(size=(3,3))*1e-16;b=np.array([1.,2.,3.]);e=rng.normal(size=3)*1e-16;x=np.linalg.solve(A+E,b+e)
Ep=E-np.outer(e,x)/(x@x)
check('2009 Q3 absorbed perturbation residual',np.linalg.norm((A+Ep)@x-b),1e-12)
check('2009 Q3 A-relative perturbation',np.linalg.norm(Ep,2)/np.linalg.norm(A,2),1e-15)
# 2011 Q4 scalar cancellation and overflowing large root.
xx=1e-8;check('2011 Q4 1-cos repaired',abs(2*math.sin(xx/2)**2-xx*xx/2)/(xx*xx/2),2e-15)
b=1e308;s=math.sqrt(1-(1/b)**2);small=-(1/b)/(1+s)
check('2011 Q4 huge-b small root',abs(small-(-5e-309)),math.ulp(small))
# 2012 log1p reverse Taylor implementation with geometric tail bound.
def log1p_series(x):
    if x==0:return 0.
    if abs(x)>.5:return math.log(1+x)
    terms=[];term=x;k=1;rough=0.
    while True:
        terms.append(term);rough+=term
        k+=1;term=-term*x*(k-1)/k
        if abs(term)/(1-abs(x))<=np.finfo(float).eps/2*abs(rough):break
    return math.fsum(reversed(terms))
for x in [1e-20,-1e-20,.49,-.49,1e-3]:
    ref=mp.log1p(mp.mpf(x));check('2012 Q1 log1p '+str(x),float(abs(mp.mpf(log1p_series(x))-ref)/abs(ref)),2e-15)
# 2013 Q2 correct selected inverse element, wrong formula demonstrably different.
A=rng.normal(size=(9,4));Q,R=np.linalg.qr(A);C=np.linalg.inv(A.T@A)
Y=la.solve_triangular(R.T,np.eye(4),lower=True);correct=Y.T@Y
check('2013 Q2 selected inverse order',np.linalg.norm(correct-C)/np.linalg.norm(C),1e-12,
      {'official_wrong_order_relative_error':float(np.linalg.norm(np.linalg.inv(R).T@np.linalg.inv(R)-C)/np.linalg.norm(C))})
# 2013 Q3 complex full-QR rank-one update via explicit Givens sequence.
def givens(a,b):
    r=math.hypot(abs(a),abs(b))
    if r==0:return np.eye(2,dtype=complex)
    c=np.conj(a)/r;s=np.conj(b)/r
    return np.array([[c,s],[-np.conj(s),np.conj(c)]])
m,n=8,4;A=rng.normal(size=(m,n))+1j*rng.normal(size=(m,n));u=rng.normal(size=m)+1j*rng.normal(size=m);v=rng.normal(size=n)+1j*rng.normal(size=n)
Q,R=np.linalg.qr(A,mode='complete');z=Q.conj().T@u;G=np.eye(m,dtype=complex)
for k in reversed(range(1,m)):
    g=givens(z[k-1],z[k]);z[k-1:k+1]=g@z[k-1:k+1];G[k-1:k+1]=g@G[k-1:k+1]
H=G@R+np.outer(z,np.conj(v));check('2013 Q3 Hessenberg update',np.linalg.norm(np.tril(H,-2)),2e-13)
F=np.eye(m,dtype=complex);T=H.copy()
for k in range(n):
    g=givens(T[k,k],T[k+1,k]);T[k:k+2]=g@T[k:k+2];F[k:k+2]=g@F[k:k+2]
Qp=Q@G.conj().T@F.conj().T
check('2013 Q3 reconstruction',np.linalg.norm(Qp@T-(A+np.outer(u,np.conj(v))))/np.linalg.norm(A+np.outer(u,np.conj(v))),1e-12)
check('2013 Q3 triangularity',np.linalg.norm(np.tril(T,-1)),2e-13)
# 2015 Q1 same-input backward counterexample uses exact integer ratios.
x=1+2**-52;num,den=x.as_integer_ratio();yn,yd=(3*x).as_integer_ratio()
check('2015 Q1 same-input counterexample exists',0 if 3*num*yd!=yn*den else 1,0)
# 2015 Q2 CGS/MGS right-hand-side implementation comparison.
def gs(A,modified):
    Q=np.zeros_like(A);R=np.zeros((A.shape[1],A.shape[1]))
    for j in range(A.shape[1]):
        v=A[:,j].copy()
        for i in range(j):
            R[i,j]=Q[:,i]@(v if modified else A[:,j]);v-=Q[:,i]*R[i,j]
        R[j,j]=np.linalg.norm(v);Q[:,j]=v/R[j,j]
    return Q,R
m,n=30,5;basis=np.linalg.qr(rng.normal(size=(m,n)))[0];A=basis[:,[0]]@np.ones((1,n))+1e-8*basis;b=rng.normal(size=m)
comparison={}
for name,modified in [('CGS',False),('MGS',True)]:
    Q,R=gs(A,modified);Qb,Rb=gs(np.column_stack([A,b]),modified)
    direct=Q.T@b;aug=Rb[:n,-1]
    comparison[name]={'rhs_difference':float(np.linalg.norm(direct-aug)),'orthogonality_loss':float(np.linalg.norm(Q.T@Q-np.eye(n)))}
check('2015 Q2 CGS equal operation path',comparison['CGS']['rhs_difference'],1e-14)
# 2015 Q3 B-MGS using cached B columns and generalized eigenpairs.
m=5;S=rng.normal(size=(m,m));B=S.T@S+np.eye(m);A=rng.normal(size=(m,m));A=A+A.T;V=np.linalg.solve(B,A);W=A.copy();Ss=np.zeros((m,m));R=np.zeros((m,m))
for j in range(m):
    R[j,j]=np.sqrt(V[:,j]@W[:,j]);Ss[:,j]=V[:,j]/R[j,j];t=W[:,j]/R[j,j]
    for k in range(j+1,m):
        R[j,k]=Ss[:,j]@W[:,k];V[:,k]-=Ss[:,j]*R[j,k];W[:,k]-=t*R[j,k]
check('2015 Q3 SR B-orthogonality',np.linalg.norm(Ss.T@B@Ss-np.eye(m)),2e-11)
check('2015 Q3 SR reconstruction',np.linalg.norm(Ss@R-np.linalg.solve(B,A)),2e-11)
vals,X=la.eigh(A,B)
check('2015 Q3 generalized eigenpairs',np.linalg.norm(A@X-B@X@np.diag(vals)),2e-12)
report={'status':'passed','seed':18335,'runtime':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},'checks':checks,'newton_digits':digits,'newton_cubic_ratios':ratios,'gs_rhs_comparison':comparison,'limits':'Finite samples validate implementation and stated examples, not general mathematical proofs or worst-case performance.','scripts':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'experiments/assessment_checks.jl']}}
(QA_DIR/'assessment-numerical-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Python assessment checks passed:',len(checks))
