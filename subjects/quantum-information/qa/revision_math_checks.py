"""Finite independent checks of the expanded derivations; no general theorem claims."""
from pathlib import Path
import numpy as np,json,math,itertools
ROOT=Path(__file__).resolve().parents[1];out={}
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);H=(X+Z)/math.sqrt(2)
out['Ambainis_five_dimensional_walk']=[]
for N,r in [(20,4),(100,20),(1000,100),(10000,400)]:
 A=np.eye(5);B=np.eye(5)
 for inds,i in [([0,1],0),([2,3],1)]:
  u=np.sqrt(np.array([N-r-2+i,2-i])/(N-r));A[np.ix_(inds,inds)]=2*np.outer(u,u)-np.eye(2)
 for inds,m in [([2,1],1),([4,3],2)]:
  v=np.sqrt(np.array([r+1-m,m])/(r+1));B[np.ix_(inds,inds)]=2*np.outer(v,v)-np.eye(2)
 actual=sorted(np.angle(np.linalg.eigvals(B@A)))
 t=[math.acos(1-2*j*(N+1-j)/((r+1)*(N-r))) for j in [1,2]]
 expected=sorted([0,*t,*[-v for v in t]])
 err=float(max(abs(np.array(actual)-expected)))
 assert err<1e-10
 out['Ambainis_five_dimensional_walk'].append({'N':N,'r':r,'eigenphase_residual':err})
# Root fidelity agrees with direct Kraus output, and worst input is excited.
out['root_fidelity']=[]
for g in [0,.1,.5,.9,1]:
 K0=np.diag([1,math.sqrt(1-g)]);K1=np.array([[0,math.sqrt(g)],[0,0]])
 v=np.array([1,1])/math.sqrt(2);rho=sum(np.outer(K@v,(K@v).conj()) for K in [K0,K1])
 root=math.sqrt(float((v@rho@v).real));closed=math.sqrt((1+math.sqrt(1-g))/2)
 assert abs(root-closed)<1e-12
 grid=np.linspace(0,1,1001);q=math.sqrt(1-g);F2=1-grid*(1-q)**2-2*grid**2*q*(1-q)
 assert abs(min(F2)-(1-g))<1e-12
 out['root_fidelity'].append({'gamma':g,'Fplus':root,'Fmin':q})
old=json.loads((ROOT/'qa/numerical-results.json').read_text())['Shor_fidelities'];errs=[]
for j,g in enumerate(old['gamma']):
 a=3*g*g-2*g**3;b=1-a;c=(1-g)**1.5
 pred={'0':(1+c*(3-c*c)/2)/2,'1':(1+c*(3-c*c)/2)/2,'+':(1+a**3+b**3)/2,'y+':(1+c*(3*b*b-c*c)/2)/2}
 errs += [abs(v-old['curves'][k][j]) for k,v in pred.items()]
out['Shor_closed_form_vs_full_Kraus_max_residual']=max(errs);assert max(errs)<1e-10
# Original PS8 X--ZZ--Y and corrected CNOT.
S=np.diag([1,1j]);U8=np.kron((I-1j*X)/math.sqrt(2),I)@((np.eye(4)-1j*np.kron(Z,Z))/math.sqrt(2))@np.kron((I-1j*Y)/math.sqrt(2),I)
C=np.eye(4);C[[1,3]]=C[[3,1]]
err=np.max(abs(np.exp(1j*math.pi/4)*np.kron(S.conj().T,S)@U8-C));assert err<1e-12
out['PS8_original_Y_CNOT_residual']=float(err)
# Quantum prisoner payoff table, including SU(2) Y deviation.
J=(np.eye(4)+1j*np.kron(X,X))/math.sqrt(2);v0=np.array([1,0,0,0],complex)
ua=np.array([3,0,5,1]);ub=np.array([3,5,0,1]);pay=[]
for A in [I,X,Z]:
 row=[]
 for B in [I,X,Z]:
  v=J.conj().T@np.kron(A,B)@J@v0;p=abs(v)**2;row.append([float(p@ua),float(p@ub)])
 pay.append(row)
expected=[[[3,3],[0,5],[1,1]],[[5,0],[1,1],[0,5]],[[1,1],[5,0],[3,3]]]
assert np.max(abs(np.array(pay)-expected))<1e-12
v=J.conj().T@np.kron(Y,Z)@J@v0;assert abs(abs(v[2])**2-1)<1e-12
out['quantum_prisoner_table']=pay;out['unrestricted_Y_against_Z_Alice_payoff']=float(abs(v[2])**2*5)
# Heisenberg multiplication and invariant right-vector label.
p=5;w=np.exp(2j*math.pi/p);t=np.arange(p)
def rep(k,g):
 x,y,z=g;M=np.zeros((p,p),complex)
 for j in range(p):M[(j+x)%p,j]=w**(k*(z+y*j))
 return M
g=(1,2,3);h=(2,1,4);gh=((g[0]+h[0])%p,(g[1]+h[1])%p,(g[2]+h[2]+g[1]*h[0])%p)
err=np.max(abs(rep(2,g)@rep(2,h)-rep(2,gh)));assert err<1e-12
P=sum(rep(2,(x,0,3*x%p)) for x in range(p))/p
phi=w**((2*3%p)*t)/math.sqrt(p);err2=np.max(abs(P-np.outer(phi,phi.conj())));assert err2<1e-12
out['Heisenberg_representation_residual']=float(err);out['Heisenberg_hidden_projector_residual']=float(err2)
# Known modular addition F^dag D F.
N=8;a=3;ix=np.arange(N);F=np.exp(2j*math.pi*np.outer(ix,ix)/N)/math.sqrt(N)
U=F.conj().T@np.diag(np.exp(2j*math.pi*a*ix/N))@F
P=np.zeros((N,N))
for x in ix:P[(x+a)%N,x]=1
err=np.max(abs(U-P));assert err<1e-12;out['Fourier_modular_adder_residual']=float(err)
out['scope']='Independent finite matrices and existing full-Kraus data comparison. Not a proof of general fault tolerance, capacity, security or all input sizes.'
(ROOT/'qa/revision-math-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
