"""Small independent numerical checks, not a substitute for proof or Julia execution."""
import numpy as np,json,pathlib
checks=[]
def check(name,error,tol=1e-11):
 error=float(error);assert error<tol,(name,error,tol);checks.append({'name':name,'error':error,'tolerance':tol,'pass':True})
A=np.array([[1.,1.],[1.,0.],[0.,1.]]);b=np.array([1.,2.,0.]);x=np.array([5/3,-1/3]);r=b-A@x
check('QR least squares normal orthogonality',np.linalg.norm(A.T@r))
check('QR least squares residual norm',abs(np.linalg.norm(r)-1/np.sqrt(3)))
A=np.array([[4.,2.,0.],[2.,5.,1.],[0.,1.,3.]]);L=np.array([[2.,0.,0.],[1.,2.,0.],[0.,.5,np.sqrt(11)/2]])
check('Cholesky worked factor',np.linalg.norm(A-L@L.T))
A=np.diag([1.,2.]);b=np.ones(2);x=np.zeros(2);r=b.copy();p=r.copy();path=[]
for k in range(2):
 q=A@p;rr=r@r;a=rr/(p@q);x=x+a*p;r=r-a*q;path.append(x.copy());new=r@r
 if new<1e-30:break
 p=r+(new/rr)*p
check('CG first iterate',np.linalg.norm(path[0]-np.array([2/3,2/3])))
check('CG second iterate',np.linalg.norm(x-np.array([1.,.5])))
A=np.diag([1.,2.]);alpha=3/5;r=np.ones(2)-alpha*(A@np.ones(2))
check('one-step GMRES residual',abs(np.linalg.norm(r)-1/np.sqrt(5)))
A=np.array([[2.,-1.,0.],[-1.,2.,-1.],[0.,-1.,2.]]);V=np.diag([1.,-1.,1.]);T=V.T@A@V
check('Lanczos tridiagonal example',np.linalg.norm(T-np.array([[2.,1.,0.],[1.,2.,1.],[0.,1.,2.]])))
for n in [3,5,8]:
 A=np.zeros((n,n));A[(np.arange(n)+1)%n,np.arange(n)]=1.;b=np.eye(n)[:,0]
 for k in range(1,n):
  Z=np.eye(n)[:,:k];y=np.linalg.lstsq(A@Z,b,rcond=None)[0]
  check(f'cyclic GMRES stagnation n={n} k={k}',abs(np.linalg.norm(b-A@Z@y)-1.))
for n in [3,7,25]:
 A=2*np.eye(n)-np.eye(n,k=1)-np.eye(n,k=-1)
 eig=4*np.sin(np.pi*np.arange(1,n+1)/(2*(n+1)))**2
 check(f'Poisson sine spectrum n={n}',np.max(np.abs(np.linalg.eigvalsh(A)-eig)))
rng=np.random.default_rng(18335);B=rng.standard_normal((7,7));A=B.T@B+np.eye(7);M=np.diag(np.diag(A));C=np.linalg.cholesky(M)
At=np.linalg.solve(C,A)@np.linalg.inv(C.T)
check('PCG symmetric transform Hermitian',np.linalg.norm(At-At.T))
v=rng.standard_normal(7);e=v;et=C.T@e
check('PCG energy preservation',abs(et@At@et-e@A@e))
A=np.array([[4.,-1.,-1.,-1.],[-1.,2.,0.,0.],[-1.,0.,2.,0.],[-1.,0.,0.,2.]])
L=np.linalg.cholesky(A);check('star center-first ten factor entries',abs(np.count_nonzero(np.abs(L)>1e-14)-10))
perm=[1,2,3,0];L=np.linalg.cholesky(A[np.ix_(perm,perm)])
check('star leaves-first seven factor entries',abs(np.count_nonzero(np.abs(L)>1e-14)-7))
result={'checks':checks,'count':len(checks),'status':'all_pass','scope':'Selected worked examples and finite-dimensional identities in NumPy; not full mathematical verification, not Julia runtime validation'}
pathlib.Path(__file__).with_name('numerical-example-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'count':len(checks),'status':'all_pass'},ensure_ascii=False))
