"""Finite-instance circuit checks, exact probabilities, and original vector plots."""
from pathlib import Path
import json,math,itertools
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];F=ROOT/'figures';F.mkdir(exist_ok=True);report={}
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);H=(X+Z)/math.sqrt(2)
def kron(ps):
 out=np.array([[1]],complex)
 for p in ps:out=np.kron(out,p)
 return out
def gate(n,which,m):return kron([m if j==which else I for j in range(n)])
def controlled(n,c,t,m):
 ps=[I]*n;ps[c]=np.diag([1,0]);a=kron(ps);ps[c]=np.diag([0,1]);ps[t]=m;return a+kron(ps)
# Optional PS8 original first page: negative X, ZZ, then negative Y.
RX=gate(2,0,(I-1j*X)/math.sqrt(2));RY=gate(2,0,(I-1j*Y)/math.sqrt(2));ZZ=kron([Z,Z]);E=(np.eye(4)-1j*ZZ)/math.sqrt(2)
U8=RX@E@RY;S=np.diag([1,1j]);expected=np.array([[1-1j,0,0,0],[0,0,0,-1-1j],[0,0,1+1j,0],[0,1-1j,0,0]],complex)/math.sqrt(2)
report['optional_PS8_original_gate_sequence']='exp(-i*pi*X1/4) exp(-i*pi*Z1Z2/4) exp(-i*pi*Y1/4); visually verified from original PDF, final Y corrected after independent reader review'
report['optional_PS8_matrix_residual']=float(np.max(np.abs(U8-expected)))
report['optional_PS8_CNOT_residual']=float(np.max(np.abs(np.exp(1j*math.pi/4)*kron([S.conj().T,S])@U8-controlled(2,1,0,X))))
assert report['optional_PS8_matrix_residual']<1e-12
assert report['optional_PS8_CNOT_residual']<1e-12
U=np.eye(8);U[[5,6]]=U[[6,5]]
# first-control Fredkin images.
SW=controlled(3,1,2,X)@controlled(3,2,1,X)@controlled(3,1,2,X)
CX12=controlled(3,0,1,X);CX13=controlled(3,0,2,X);CZ12=controlled(3,0,1,Z);CZ13=controlled(3,0,2,Z)
images=[gate(3,0,X)@SW,gate(3,1,X)@CX12@CX13,gate(3,2,X)@CX12@CX13,gate(3,0,Z),gate(3,1,Z)@CZ12@CZ13,gate(3,2,Z)@CZ12@CZ13]
report['Fredkin_conjugation_residuals']=[float(np.max(np.abs(U@gate(3,j%3,X if j<3 else Z)@U.T-images[j]))) for j in range(6)]
report['phase_matched_search']=[]
for N in [4,10,100,143,1024]:
 alpha=1/math.sqrt(N);q=math.ceil(math.pi/(4*math.asin(alpha))-.5);ang=2*math.asin(min(1,math.sin(math.pi/(4*q+2))/alpha));v=np.array([alpha,math.sqrt(1-alpha*alpha)],complex)
 U1=np.eye(2)+(np.exp(-1j*ang)-1)*np.outer(v,v.conj());U2=np.diag([np.exp(-1j*ang),1]);v2=np.linalg.matrix_power(U1@U2,q)@v
 report['phase_matched_search'].append({'N':N,'queries':q,'phase':ang,'success':float(abs(v2[0])**2)})
K=sum(math.comb(100,j)*2**(100-j) for j in range(77,84));P=sum(math.comb(100,j)*.8**j*.2**(100-j) for j in range(77,84));report['typical']={'strings':str(K),'probability':P,'fixed_bits':math.ceil(math.log2(K))}
# precise Bayesian posterior curves.
r=20;ks=np.arange(r);qs=np.cos(math.pi*ks/r)**2
fig,ax=plt.subplots(figsize=(7,3.5))
for t in [10,50,200]:
 n0=round(.7*t);p=qs**n0*(1-qs)**(t-n0);p/=p.sum();ax.plot(ks,p,'o-',label=f't={t}, n0={n0}')
ax.set(xlabel='k',ylabel='posterior probability');ax.legend();fig.tight_layout();fig.savefig(F/'phase-posteriors.pdf');plt.close(fig)
rng=np.random.default_rng(143);w=np.ones(r)/r;record=[];truth=3;grid=np.arange(200)/200
for t in range(50):
 probs=np.cos(math.pi*(ks[:,None]/r-grid[None,:]))**2
 ent=lambda a:-(np.where(a>0,a*np.log2(np.maximum(a,1e-300)),0)+np.where(a<1,(1-a)*np.log2(np.maximum(1-a,1e-300)),0))
 score=ent(w@probs)-w@ent(probs);j=int(np.argmax(score));theta=grid[j];m=int(rng.random()>probs[truth,j]);w*=probs[:,j] if m==0 else 1-probs[:,j];w/=w.sum();record.append({'t':t+1,'theta':float(theta),'outcome':m,'truth_posterior':float(w[truth]),'entropy':float(ent(w).sum())})
(ROOT/'qa/feedback-record.json').write_text(json.dumps({'N':143,'y':5,'order':20,'truth_k':truth,'seed':143,'measurements':record},indent=2))
fig,ax=plt.subplots(figsize=(6,3));ax.plot([a['t'] for a in record],[a['truth_posterior'] for a in record]);ax.set(xlabel='trial',ylabel='posterior of k=3',ylim=(0,1));fig.tight_layout();fig.savefig(F/'phase-feedback.pdf');plt.close(fig)
# Simple amplitude-damping fidelity plots.
t=np.linspace(0,6,301);gamma=1-np.exp(-t)
fig,ax=plt.subplots(figsize=(6,3));ax.plot(t,(1+np.sqrt(1-gamma))/2,label='one-qubit +');ax.plot(t,1-gamma,label='one-qubit worst / dual-rail');ax.plot(t,np.ones_like(t),label='postselected dual-rail');ax.set(xlabel='t/T1',ylabel='squared fidelity',ylim=(0,1.05));ax.legend();fig.tight_layout();fig.savefig(F/'amplitude-fidelities.pdf');plt.close(fig)
# Exact Shor recovery. Encode in conventional GHZ-block basis.
V=np.zeros((512,2),complex)
for bits in itertools.product([0,1],repeat=3):
 idx=int(''.join(str(b)*3 for b in bits),2);V[idx,0]=1/math.sqrt(8);V[idx,1]=(-1)**sum(bits)/math.sqrt(8)
# Generate 256 syndrome representatives: 0 or one X in each block, 0 or a Z in one block.
reps=[]
for errs in itertools.product(range(4),repeat=3):
 mask=0
 for b,k in enumerate(errs):
  if k:mask^=1<<(8-(3*b+k-1))
 for zblock in range(4):
  zmask=0 if not zblock else 1<<(8-3*(zblock-1));reps.append((mask,zmask))
# <r_L|R_s acting on computational vectors is obtained from R_s^dagger|r_L>.
rows=np.zeros((256,2,512),complex)
for s,(xm,zm) in enumerate(reps):
 for j in np.flatnonzero(np.any(V,axis=1)):
  # Order X then Z in R_s^dagger; sign choice only syndrome-wide, immaterial.
  target=j^xm;sign=(-1)**((j&zm).bit_count());rows[s,:,target]=V[j,:]*sign
# orthonormal syndrome subspaces check.
flat=rows.reshape(512,512);report['Shor_recovery_basis_residual']=float(np.max(np.abs(flat@flat.conj().T-np.eye(512))))
curves={name:[] for name in ['0','1','+','y+']};gs=np.linspace(0,.5,26)
psis=[np.array([1,0]),np.array([0,1]),np.array([1,1])/math.sqrt(2),np.array([1,1j])/math.sqrt(2)]
for g in gs:
 E=np.zeros((512,512,2),complex)
 for mask in range(512):
  for j in np.flatnonzero(np.any(V,axis=1)):
   if mask&j!=mask:continue
   a=g**(mask.bit_count()/2)*(1-g)**((j.bit_count()-mask.bit_count())/2)
   E[mask,j^mask,:]=a*V[j,:]
 # K[s,e,r,t]
 K=np.einsum('srj,ejt->sert',rows.conj(),E,optimize=True)
 for (name,arr),psi in zip(curves.items(),psis):
  amps=np.einsum('r,sert,t->se',psi.conj(),K,psi,optimize=True);arr.append(float(np.sum(np.abs(amps)**2)))
 report.setdefault('Shor_channel_trace_residuals',[]).append(float(np.max(np.abs(np.einsum('sert,seru->tu',K.conj(),K)-np.eye(2)))))
fig,ax=plt.subplots(figsize=(6,3))
for name,ys in curves.items():ax.plot(gs,ys,label=name)
ax.set(xlabel='gamma',ylabel='decoded squared fidelity',ylim=(0,1.05));ax.legend();fig.tight_layout();fig.savefig(F/'shor-amplitude.pdf');plt.close(fig)
report['Shor_fidelities']={'gamma':gs.tolist(),'curves':curves,'decoder':'per-block majority X, then majority block Z; all 256 orthogonal syndromes'}
# Expand the QFT graph modules into an explicit edge list with all measurement labels.
nextid=3;ports=[0,1,2];edges=[];measure=[]
def new():
 global nextid
 i=nextid;nextid+=1;return i
def h_gate(q):
 old=ports[q];a=new();edges.append([old,a]);measure.append({'vertex':old,'angle':0,'frame_adjust':'Pauli frame propagated'});ports[q]=a
def rz(q,theta):
 old=ports[q];a=new();b=new();edges.extend([[old,a],[a,b]]);measure.extend([{'vertex':old,'angle':-theta,'frame_adjust':'negate angle if incoming X frame=1'},{'vertex':a,'angle':0,'frame_adjust':'Pauli frame propagated'}]);ports[q]=b
def cz(a,b):
 edges.append([ports[a],ports[b]])
 for _ in range(2):h_gate(a);h_gate(b)
def cn(a,b):h_gate(b);cz(a,b);h_gate(b)
def cp(a,b,theta):rz(a,theta/2);rz(b,theta/2);cn(a,b);rz(b,-theta/2);cn(a,b)
h_gate(0);cp(1,0,math.pi/2);cp(2,0,math.pi/4);h_gate(1);cp(2,1,math.pi/2);h_gate(2);cn(0,2);cn(2,0);cn(0,2)
assert nextid==78
(ROOT/'qa/qft-cluster-graph.json').write_text(json.dumps({'vertices':list(range(nextid)),'inputs':[0,1,2],'outputs':ports,'edges':edges,'measurements_in_order':measure,'rule':'one-bit teleportation X^m H Rz(-theta); propagate frame before measuring; final outputs corrected'},indent=2))
report['QFT_graph_vertices']=nextid;report['finite_checks_only']=True
assert max(report['Fredkin_conjugation_residuals'])<1e-12
assert report['Shor_recovery_basis_residual']<1e-12
assert max(report['Shor_channel_trace_residuals'])<1e-10
(ROOT/'qa/numerical-results.json').write_text(json.dumps(report,indent=2));print('All finite matrix checks passed; figures and exact numeric results written.')
