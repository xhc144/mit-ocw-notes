"""Deterministic numerical checks of authored solutions, not experimental data."""
from pathlib import Path
import json, numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
(ROOT/"qa").mkdir(exist_ok=True)
(ROOT/"data").mkdir(exist_ok=True)
a,b='GAATTC','GATTA'
def align(local=False):
 F=np.zeros((len(a)+1,len(b)+1));paths={}
 if not local:F[:,0]=-2*np.arange(len(a)+1);F[0,:]=-2*np.arange(len(b)+1)
 for i in range(1,len(a)+1):
  for j in range(1,len(b)+1):
   vals=[F[i-1,j-1]+(1.5 if a[i-1]==b[j-1] else -1),F[i-1,j]-2,F[i,j-1]-2]
   F[i,j]=max([0]+vals) if local else max(vals)
 def back(i,j,x='',y=''):
  if (local and F[i,j]==0) or (i==0 and j==0):return [(x[::-1],y[::-1])]
  out=[]
  if i and j and abs(F[i,j]-F[i-1,j-1]-(1.5 if a[i-1]==b[j-1] else -1))<1e-10:out+=back(i-1,j-1,x+a[i-1],y+b[j-1])
  if i and abs(F[i,j]-F[i-1,j]+2)<1e-10:out+=back(i-1,j,x+a[i-1],y+'-')
  if j and abs(F[i,j]-F[i,j-1]+2)<1e-10:out+=back(i,j-1,x+'-',y+b[j-1])
  return out
 i,j=np.unravel_index(F.argmax(),F.shape) if local else (len(a),len(b))
 return F,sorted(set(back(i,j))),float(F[i,j])
G,gpaths,gs=align();L,lpaths,ls=align(True)
for key,F in [('global',G),('local',L)]:
 rows=[' & '+ ' & '.join(['$-$']+list(b))+r'\\\midrule']
 for lab,row in zip(['$-$']+list(a),F):rows.append(lab+' & '+' & '.join(f'{v:g}' for v in row)+r'\\')
 (ROOT/'data'/f'{key}-matrix.tex').write_text('\\begin{tabular}{c'+'r'*(len(b)+1)+'}\\toprule\n'+'\n'.join(rows)+'\n\\bottomrule\\end{tabular}\n')
p,q,pp,pm=.02,.03,.04,.01
M=np.array([[1-q-p-pp,q,p,pm],[q,1-q-p-pm,pp,p],[p,pm,1-q-p-pp,q],[pp,p,q,1-q-p-pm]])
stat=np.array([q+pm,q+pp,q+pm,q+pp])/(2*(2*q+pp+pm))
# Two-state drift/diffusion via tilted-generator eigenvalue derivatives.
u1,u2,w1,w2,d=2000.,50.,20.,.5,8.
S=u1+u2+w1+w2;delta=u1*u2-w1*w2
v=d*delta/S;D=d*d*((u1*u2+w1*w2)/(2*S)-delta**2/S**3)
# Poisson-Boltzmann and chain-bending identities.
z,lb,mu=2.,.7,1.3
normal=quad(lambda y:1/(2*np.pi*z*z*lb*(y+mu)**2),0,np.inf)[0]
# Fundamental force-extension moment for isotropic Gaussian chain.
N=100;a2=1.;F=.02;kt=1.
X=N*a2*F/(3*kt)
result={'data_kind':'deterministic model computations; no measurements','alignment':{'global_score':gs,'global_paths':gpaths,'local_score':ls,'local_paths':lpaths,'global_matrix':G.tolist(),'local_matrix':L.tolist()},'asymmetric_mutation':{'matrix_column_sums':M.sum(0).tolist(),'stationary':stat.tolist(),'residual':float(np.linalg.norm(M@stat-stat))},'two_state_motor':{'v_nm_per_s':v,'D_nm2_per_s':D,'fE_pN_at_kT_4_1':4.1*v/D,'stall_pN_at_kT_4_1':4.1/d*np.log(u1*u2/(w1*w2))},'pb_number_integral':normal,'pb_expected':1/(2*np.pi*z*z*lb*mu),'gaussian_chain_extension':X,'orf_exact_600':2*5e6*(3/64)**2*(61/64)**600,'orf_at_least_600':2*5e6*(3/64)*(61/64)**600}
assert result['asymmetric_mutation']['residual']<1e-12
assert abs(normal-result['pb_expected'])<1e-10
print('Alignment computed:',gs,ls,gpaths,lpaths)
assert abs(gs-3.0)<1e-12 and abs(ls-4.5)<1e-12
(ROOT/'qa'/'numerical-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))

rows=['mu,lambda']
for mu in np.linspace(.5,5,91):
 lam=0. if mu==.5 else brentq(lambda l:np.expm1(l)/4+np.expm1(-mu*l)/2,1e-8,2)
 rows.append(f'{mu:.8f},{lam:.10f}')
(ROOT/'data'/'alignment-lambda.csv').write_text('\n'.join(rows)+'\n')
print('Numerical identities and alignment matrices checked.')
