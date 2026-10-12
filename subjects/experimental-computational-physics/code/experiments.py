"""Physical measurement simulations and atomistic models, all synthetic/model data.
Run: python code/experiments.py. Dependencies: numpy, scipy. Fixed seed.
No authentic laboratory observations are represented by this program.
"""
from pathlib import Path
import json, numpy as np
from scipy.signal import welch
from scipy.optimize import minimize_scalar
from scipy.integrate import simpson
ROOT=Path(__file__).resolve().parents[1]
(ROOT/"qa").mkdir(exist_ok=True)
(ROOT/"data").mkdir(exist_ok=True)
rng=np.random.default_rng(20261012)
results={'seed':20261012,'data_kind':'synthetic measurements and explicitly specified model simulations'}

def csv(name,header,a):np.savetxt(ROOT/'data'/name,a,delimiter=',',header=header,comments='',fmt='%.11g')
# Measurement chain: known input slope, independent voltage noise.
h,e,kb,T=6.62607015e-34,1.602176634e-19,1.380649e-23,300.
f=np.array([5.2,5.6,6.1,6.5,7.,7.5]);sigma=.012
voltage=h/e*f*1e14-1.60+rng.normal(0,sigma,len(f));X=np.c_[f,np.ones(len(f))]
beta=np.linalg.lstsq(X,voltage,rcond=None)[0];cov=sigma**2*np.linalg.inv(X.T@X);pred=X@beta
csv('photoelectric.csv','freq_scaled,voltage,fit',np.c_[f,voltage,pred])
results['photoelectric']={'slope_V_per_1e14Hz':float(beta[0]),'h_estimate_J_s':float(e*beta[0]/1e14),'u_h_J_s':float(e*np.sqrt(cov[0,0])/1e14),'intercept_V':float(beta[1]),'chi2':float(np.sum(((voltage-pred)/sigma)**2)),'dof':4,'covariance':cov.tolist()}
results['poisson']=[]
for mu in [1,5,10,100]:
 z=rng.poisson(mu,10000);results['poisson'].append({'mean_input':mu,'sample_mean':float(z.mean()),'sample_variance':float(z.var(ddof=1))})
# Non-paralyzable counter; each accepted event initiates a blind interval.
rate,dead,horizon=200.,.002,2000.
times=np.cumsum(rng.exponential(1/rate,int(rate*horizon*1.02)));times=times[times<horizon]
last=-np.inf;accepted=0
for t in times:
 if t-last>=dead:accepted+=1;last=t
results['dead_time']={'true_rate':rate,'duration_s':horizon,'dead_time_s':dead,'recorded_rate':accepted/horizon,'predicted_rate':rate/(1+rate*dead)}
# Exact OU discrete transition; no exposure averaging or detector noise.
gamma=6*np.pi*.001*.5e-6;k=2e-6;dt=1e-4;tau=gamma/k;rho=np.exp(-dt/tau);var=kb*T/k
trace=np.empty(131072);trace[0]=rng.normal(0,np.sqrt(var));noise=rng.normal(0,np.sqrt(var*(1-rho*rho)),len(trace)-1)
for i in range(1,len(trace)):trace[i]=rho*trace[i-1]+noise[i-1]
freq,psd=welch(trace,fs=1/dt,nperseg=8192)
csv('trap-psd.csv','frequency,psd,model',np.c_[freq[1:],psd[1:]*1e18,4*kb*T*gamma/(k*k+(2*np.pi*freq[1:]*gamma)**2)*1e18])
rhat=float(np.dot(trace[:-1],trace[1:])/np.dot(trace[:-1],trace[:-1]));results['trap']={'units':'SI; plotted PSD nm^2/Hz','n':len(trace),'dt_s':dt,'k_input_N_per_m':k,'variance_input_m2':var,'variance_sample_m2':float(trace.var()),'k_from_variance_N_per_m':float(kb*T/trace.var()),'tau_input_s':tau,'tau_from_lag_s':float(-dt/np.log(rhat)),'PSD_integral_m2':float(np.trapezoid(psd,freq))}
# Unshifted Au LJ lattice sums: parameters from the official GULP handout.
AuA,AuB=214180.2,625.482
Au=[]
for nc in [2,4,7]:
 coords=[]
 for i in range(-nc,nc+1):
  for j in range(-nc,nc+1):
   for z in range(-nc,nc+1):
    for basis in [[0,0,0],[0,.5,.5],[.5,0,.5],[.5,.5,0]]:
     r=np.linalg.norm((np.array([i,j,z])+basis)*np.sqrt(2))
     if r>0:coords.append(r)
 coords=np.array(coords);S6=float(np.sum(coords**-6));S12=float(np.sum(coords**-12))
 nearest=(2*AuA*S12/(AuB*S6))**(1/6);Au.append({'shell_cells':nc,'S6':S6,'S12':S12,'lattice_constant_Angstrom':float(np.sqrt(2)*nearest)})
results['Au_pair_minimum_Angstrom']=(2*AuA/AuB)**(1/6)
results['Au_lattice_sums']=Au
# Force-shifted LJ: E and forces evaluated from precisely the same model.
rc=2.5
vc=4*(rc**-12-rc**-6);vpc=24*(rc**-7-2*rc**-13)
def ef(pos,box):
 dr=pos[:,None,:]-pos[None,:,:];dr-=box*np.rint(dr/box)
 r2=np.sum(dr*dr,axis=2);np.fill_diagonal(r2,np.inf)
 mask=r2<rc*rc;inv=np.where(mask,1/r2,0.);r=np.sqrt(np.where(mask,r2,1.))
 val=np.where(mask,4*(inv**6-inv**3)-vc-(r-rc)*vpc,0.)
 fac=np.where(mask,24*(2*inv**7-inv**4)+vpc/r,0.)
 return .5*float(val.sum()),np.sum(fac[:,:,None]*dr,axis=1)
def fcc(ncell=3,density=.8):
 n=4*ncell**3;box=(n/density)**(1/3);basis=np.array([[0,0,0],[0,.5,.5],[.5,0,.5],[.5,.5,0]])
 return np.array([(np.array([i,j,k])+b)*box/ncell for i in range(ncell) for j in range(ncell) for k in range(ncell) for b in basis]),box
pos,box=fcc();vel=rng.normal(0,1,pos.shape);vel-=vel.mean(0);vel*=np.sqrt((3*len(pos)-3)*.3/np.sum(vel**2))
energy,force=ef(pos,box);eps=1e-6;probe=pos.copy();probe[0,0]+=eps;Ep=ef(probe,box)[0];probe[0,0]-=2*eps;Em=ef(probe,box)[0]
results['force_check']={'analytic':float(force[0,0]),'finite_difference':float(-(Ep-Em)/(2*eps)),'residual':float(abs(force[0,0]+(Ep-Em)/(2*eps)))}
assert results['force_check']['residual']<1e-6
# A non-symmetric displaced configuration avoids a zero-force-only check.
pert=pos.copy();pert[0]+=np.array([.023,-.017,.011]);E0,F0=ef(pert,box);pp=pert.copy();pp[0,0]+=eps;pm=pert.copy();pm[0,0]-=eps
results['force_check_displaced']={'residual':float(abs(F0[0,0]+(ef(pp,box)[0]-ef(pm,box)[0])/(2*eps)))}
assert results['force_check_displaced']['residual']<1e-5
results['md']=[]
for step in [.002,.001]:
 p=pos.copy();v=vel.copy();unwrapped=p.copy();E,F=ef(p,box);samples=[]
 for i in range(round(4/step)):
  v+=step/2*F;unwrapped+=step*v;p=unwrapped%box;E,F=ef(p,box);v+=step/2*F
  if i%10==0:samples.append([(i+1)*step,E+.5*np.sum(v*v),E,.5*np.sum(v*v),np.mean(np.sum((unwrapped-pos)**2,axis=1))])
 a=np.array(samples);csv('md-'+str(step)+'.csv','time,total,potential,kinetic,msd',a)
 results['md'].append({'N':len(pos),'density':.8,'cutoff':rc,'potential':'force-shifted LJ','dt':step,'duration':4,'energy_mean':float(a[:,1].mean()),'energy_std':float(a[:,1].std()),'energy_span':float(np.ptp(a[:,1])),'msd_final':float(a[-1,4]),'initial_energy':float(energy+.5*np.sum(vel*vel))})
# Periodic 1D quantum Hamiltonian: H=.5(-i d/dx + k)^2 + .4 cos(x).
def bands(G,kval):
 g=np.arange(-G,G+1);H=np.diag(.5*(g+kval)**2);off=np.full(2*G,.2);H+=np.diag(off,1)+np.diag(off,-1)
 return np.linalg.eigvalsh(H)
results['plane_wave']=[{'G':G,'eigenvalues':bands(G,.3)[:3].tolist()} for G in [2,3,5,9]]
ks=np.linspace(-.5,.5,121);csv('bands.csv','k,E0,E1,E2',np.array([[q,*bands(9,q)[:3]] for q in ks]))
assert np.max(np.abs(bands(5,.3)[:3]-bands(9,.3)[:3]))<1e-7
# 4x4 adsorbate lattice. Unique oriented NN and diagonal pairs.
L=4;N=L*L;ind=np.arange(N).reshape(L,L);nn=[];nnn=[]
for i in range(L):
 for j in range(L):
  nn.append([ind[(i+1)%L,j],ind[(i-1)%L,j],ind[i,(j+1)%L],ind[i,(j-1)%L]])
  nnn.append([ind[(i+1)%L,(j+1)%L],ind[(i+1)%L,(j-1)%L],ind[(i-1)%L,(j+1)%L],ind[(i-1)%L,(j-1)%L]])
nn=np.array(nn);nnn=np.array(nnn)
states=2*((np.arange(2**N)[:,None]>>np.arange(N))&1)-1
bare=np.sum(states*(states[:,nn].sum(2)-2*states[:,nnn].sum(2)),axis=1)/2
mag=states.sum(1)
def total(s,mu):return .5*np.sum(s*(s[nn].sum(1)-2*s[nnn].sum(1)))-mu*s.sum()
s=rng.choice([-1,1],N);i=3;mu=1.7;delta=-2*s[i]*(s[nn[i]].sum()-2*s[nnn[i]].sum()-mu);sp=s.copy();sp[i]*=-1
assert abs(total(sp,mu)-total(s,mu)-delta)<1e-12
results['lattice_groundstate']={'min_energy_per_site_at_mu0':float(bare.min()/N),'n_groundstates':int(np.sum(bare==bare.min()))}
results['mc']=[];curve=[]
for temp in [2.,6.,12.]:
 for mu in [-8.,-4.,0.,4.,8.]:
  ene=bare-mu*mag;w=np.exp(-(ene-ene.min())/temp);w/=w.sum();exact=float(w@((1+mag/N)/2))
  s=rng.choice([-1,1],N);obs=[]
  for sweep in range(8000):
   for _ in range(N):
    i=rng.integers(N);delta=-2*s[i]*(s[nn[i]].sum()-2*s[nnn[i]].sum()-mu)
    if delta<=0 or rng.random()<np.exp(-delta/temp):s[i]*=-1
   # Reversible sublattice proposal bridges the ordered/full coexistence bottleneck.
   sub=(np.indices((L,L)).sum(0).ravel()%2)==rng.integers(2)
   sp=s.copy();sp[sub]*=-1;delta=total(sp,mu)-total(s,mu)
   if delta<=0 or rng.random()<np.exp(-delta/temp):s=sp
   if sweep>=2000:obs.append((1+s.mean())/2)
  obs=np.array(obs);blocks=obs.reshape(60,100).mean(1);se=blocks.std(ddof=1)/np.sqrt(60)
  row={'T':temp,'mu':mu,'exact_theta':exact,'sample_theta':float(obs.mean()),'block_se':float(se),'sweeps':8000,'burnin':2000};results['mc'].append(row);curve.append([temp,mu,exact,obs.mean(),se])
  if abs(obs.mean()-exact)>=max(8*se,.02): print('MC nonconvergence:',row,flush=True)
  assert abs(obs.mean()-exact)<max(8*se,.02)
csv('mc.csv','T,mu,exact,sample,se',np.array(curve))
# Thermodynamic integration between harmonic references, analytical benchmark.
lams=np.linspace(0,1,101);spring=1+3*lams;derivative=3*T*kb/(2*spring)
DF=simpson(derivative,x=lams);results['thermodynamic_integration']={'deltaF_over_kBT':float(DF/(kb*T)),'exact':float(.5*np.log(4)),'abs_error':float(abs(DF/(kb*T)-.5*np.log(4)))}
# Real-time event KMC, distinct from Metropolis sweep counting.
u,w,spacing,end,npaths=3.,1.,1.,100.,4000
final=[]
for _ in range(npaths):
 t=0.;x=0
 while True:
  t+=rng.exponential(1/(u+w))
  if t>end:break
  x+=1 if rng.random()<u/(u+w) else -1
 final.append(x)
final=np.array(final)*spacing
results['kmc']={'duration':end,'paths':npaths,'v_estimate':float(final.mean()/end),'v_exact':spacing*(u-w),'D_estimate':float(final.var(ddof=1)/(2*end)),'D_exact':spacing**2*(u+w)/2}
(ROOT/'qa'/'model-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in results.items() if k not in ['mc']},ensure_ascii=False,indent=2))
print('MC comparisons:',len(results['mc']))

# Exact two-qubit Deutsch-Jozsa model, not an experimental NMR readout.
Hq=np.array([[1,1],[1,-1]])/np.sqrt(2);Hboth=np.kron(Hq,Hq);Hfirst=np.kron(Hq,np.eye(2));state=np.array([0.,1.,0.,0.]);dj=[]
for vals in [(0,0),(1,1),(0,1),(1,0)]:
 U=np.zeros((4,4))
 for x in [0,1]:
  for y in [0,1]:U[2*x+(y^vals[x]),2*x+y]=1
 assert np.allclose(U.T@U,np.eye(4))
 out=Hfirst@U@Hboth@state;prob=float(np.sum(out[:2]**2));expected=1. if vals[0]==vals[1] else 0.
 assert abs(prob-expected)<1e-12
 dj.append({'function_values':vals,'first_qubit_probability_0':prob,'expected':expected})
(ROOT/'qa/quantum-circuit-model.json').write_text(json.dumps({'data_kind':'exact simulator; no NMR experiment','Deutsch_Jozsa':dj},indent=2))
