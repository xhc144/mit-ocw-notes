#!/usr/bin/env python3
"""Finite numerical checks supporting, rather than replacing, the manuscript's proofs."""
import hashlib,itertools,json,math,pathlib
from collections import Counter
import numpy as np
import mpmath as mp
from scipy.optimize import brentq,minimize_scalar
ROOT=pathlib.Path(__file__).resolve().parents[1]
(ROOT/'figures').mkdir(exist_ok=True);(ROOT/'qa').mkdir(exist_ok=True)
mp.mp.dps=35
out={'scope':'Finite quadratures, matrices, graph enumeration and small seeded Monte Carlo; no thermodynamic-limit or full classification proof','versions':{'numpy':np.__version__,'mpmath':mp.__version__}}
h=6.62607015e-34;hb=h/(2*math.pi);kb=1.380649e-23;me=9.1093837139e-31;mpa=1.67262192369e-27;c=299792458.;G=6.67430e-11;amu=1.66053906660e-27
lam=lambda mass,T:h/math.sqrt(2*math.pi*mass*kb*T)
gases={}
for name,mass in [('H2',2*mpa),('He',4*mpa),('O2',32*mpa)]:
 x=101325/(kb*300)*lam(mass,300)**3;gases[name]={'lambda_m':lam(mass,300),'n_lambda3':x,'Tq_fixed_n_K':300*x**(2/3),'Tq_fixed_P_K':300*x**.4}
T=1.6e7;np_=6e4/mpa;na_=1e5/(4*mpa);ne_=np_+2*na_;P=kb*T*(np_+na_+ne_);Pr=7.5657e-16*T**4/3
solar={'n_lambda3_over_g':{'electron':ne_*lam(me,T)**3/2,'proton':np_*lam(mpa,T)**3/2,'alpha':na_*lam(4*mpa,T)**3},'P_gas_Pa':P,'P_rad_Pa':Pr,'ratio':P/Pr}
he3TF=hb**2*(3*math.pi**2/(46e-30))**(2/3)/(2*3.0160293*amu*kb)
metalEF=hb**2*(3*math.pi**2*1e29)**(2/3)/(2*me)/1.602176634e-19
M=2e30;BH={'temperature_K':hb*c**3/(8*math.pi*kb*G*M),'delta_entropy_bits':8*math.pi*G*M*M/(hb*c*math.log(2)),'evaporation_years':5120*math.pi*G**2*M**3/(hb*c**4)/(365.25*86400),'mass_at_2p7K_kg':hb*c**3/(8*math.pi*kb*G*2.7)}
H=kb*273/(29*amu*9.81);everP=math.exp(-9000/H);everTb=1/(1/373.15-(461.5/2.3e6)*math.log(everP))
out['estimates']={'room_gases':gases,'solar':solar,'He3_TF_K':he3TF,'metal_EF_eV':metalEF,'metal_compressibility_Angstrom3_per_eV':3/(2*.1*metalEF),'black_hole':BH,'Everest_isothermal_air':{'Tair_K':273,'scale_height_m':H,'pressure_atm':everP,'boiling_K':everTb},'He4_sound_speed_m_per_s':(2*math.pi**2*kb**4/(15*hb**3*145*20.4))**(1/3)}
# Exact Gauss-Hermite moments and peculiar heat flux, normal Gaussian variance one.
x,w=np.polynomial.hermite.hermgauss(12);px,py=np.meshgrid(np.sqrt(2)*x,np.sqrt(2)*x);weights=np.outer(w,w)/math.pi;p2=px*px+py*py
avg=lambda f:float(np.sum(weights*f))
wick={'p2':avg(p2),'p4':avg(p2**2),'p6':avg(p2**3),'px2_p4':avg(px*px*p2**2)}
assert abs(wick['px2_p4']-24)<1e-11
# m=kB=T=n=tau=1; grad ln n=.3, grad ln T=.2, F=.1.
delta=-px*(.3-.2-.1+.1*p2);u=avg(px*delta);Q=avg(px*p2*delta)/2;heat=Q-2*u
assert abs(u+.4)<1e-12 and abs(heat+.4)<1e-12
out['lorentz_gaussian']={'quadrature':'12x12 Gauss-Hermite; algebraic polynomials exact to included order','moments':wick,'mass_velocity':u,'lab_energy_flux':Q,'peculiar_heat_flux':heat,'reference_heat_flux':-.4,'official_22_coefficient_corrected_to':24}
# Fixed and free harmonic chains.
N=14;L=2*np.eye(N-1)-np.eye(N-1,k=1)-np.eye(N-1,k=-1);cov=np.linalg.inv(L);ref=np.array([[min(i,j)-i*j/N for j in range(1,N)]for i in range(1,N)])
Lf=2*np.eye(N)-np.eye(N,k=1)-np.eye(N,k=-1);Lf[-1,-1]=1;covf=np.linalg.inv(Lf);reff=np.array([[min(i,j)for j in range(1,N+1)]for i in range(1,N+1)])
err=float(np.max(abs(cov-ref)));errf=float(np.max(abs(covf-reff)));assert max(err,errf)<1e-10
out['harmonic_chain']={'N_springs':N,'fixed_end_inverse_error':err,'free_end_inverse_error':errf}
# Mehler unnormalised heat kernel satisfies Bloch equation by finite derivatives.
def kernel(beta,q,qp):return math.sqrt(1/(2*math.pi*math.sinh(beta)))*math.exp(-((q*q+qp*qp)*math.cosh(beta)-2*q*qp)/(2*math.sinh(beta)))
errs=[]
for beta,q,qp in [(.4,.3,-.5),(1.,.5,.8),(2.,1.1,-.2)]:
 db=1e-5;dq=1e-4;K=kernel(beta,q,qp);lhs=-(kernel(beta+db,q,qp)-kernel(beta-db,q,qp))/(2*db);rhs=-.5*(kernel(beta,q+dq,qp)-2*K+kernel(beta,q-dq,qp))/dq**2+.5*q*q*K;errs.append(abs(lhs-rhs)/max(abs(lhs),abs(rhs),1e-6))
assert max(errs)<2e-6
out['mehler_kernel']={'parameters':'m=omega=hbar=1','finite_Bloch_relative_errors':errs,'not_a_general_proof':True}
# Majority block enumeration and local honeycomb weight polynomials.
states=list(itertools.product((-1,1),repeat=4));class_table=Counter();Zplus=0;a_site=0;K=.7
for s in states:
 Msum=sum(s);bonds=sum(s[i]*s[(i+1)%4]for i in range(4));Pplus=1 if Msum>0 else (0 if Msum<0 else .5);wt=math.exp(K*bonds)*Pplus;Zplus+=wt;a_site+=wt*s[0];class_table[(Msum,bonds,Pplus)]+=1
a_site/=Zplus;assert abs(a_site-(math.exp(4*K)+2)/(math.exp(4*K)+6+math.exp(-4*K)))<1e-13
nvl_a=lambda K:(math.exp(4*K)+2)/(math.exp(4*K)+6+math.exp(-4*K));nvl=lambda K:2*K*nvl_a(K)**2
nvlK=brentq(lambda K:nvl(K)-K,.1,1);step=1e-5;nvl_lambda=(nvl(nvlK+step)-nvl(nvlK-step))/(2*step)
blocks=[]
for s in states:
 S=1 if sum(s)>0 else (-1 if sum(s)<0 else s[0]);blocks.append((s,S))
polys=[]
for target in (1,-1):
 coeff=Counter()
 for a,A in blocks:
  for b,B in blocks:
   if A==1 and B==target:coeff[sum(a[0]*v for v in a[1:])+sum(b[0]*v for v in b[1:])+a[1]*b[1]+a[2]*b[2]]+=1
 polys.append(dict(coeff))
assert polys[0]=={8:1,6:2,4:7,2:14,0:17,-2:14,-4:7,-6:2} and polys[1]=={4:9,2:16,0:13,-2:16,-4:9,-8:1}
R=lambda J,P:sum(v*math.exp(k*J)for k,v in P.items());hc=lambda J:.5*math.log(R(J,polys[0])/R(J,polys[1]));hcK=brentq(lambda J:hc(J)-J,1,2);hcL=(hc(hcK+step)-hc(hcK-step))/(2*step)
mk=[]
for q in (3,1):
 F=lambda K:math.log((math.exp(4*K)+q-1)/(2*math.exp(2*K)+q-2));kr=brentq(lambda K:F(K)-K,.1,1.5);ll=(F(kr+step)-F(kr-step))/(2*step);mk.append({'q':q,'K_star':kr,'thermal_eigenvalue':ll,'yt':math.log(ll)/math.log(2)})
out['realspace_rg']={'square_block_configuration_classes':[{'M':k[0],'bond_sum':k[1],'Pplus':k[2],'count':v}for k,v in sorted(class_table.items())],'nvl_K_star':nvlK,'nvl_yt':math.log(nvl_lambda)/math.log(2),'nvl_yh':1.5,'honeycomb_polynomials':polys,'honeycomb_K_star':hcK,'honeycomb_nu':math.log(2)/math.log(hcL),'honeycomb_exact_K_star':.5*math.log(2+math.sqrt(3)),'MK_order':'bond moving then decimation','MK_fixed_points':mk}
# Potts star-triangle all relevant colour classes.
star=[]
for q in (2,3,4,5):
 vh=brentq(lambda v:v**3-3*q*v-q*q,.1,10);xx=1+vh;A=xx**3+q-1;B=xx*xx+xx+q-2;C=3*xx+q-3;L=math.log(A*C*C/B**3);vt=B/C-1;assert abs(L)<1e-10 and abs(vh*vt-q)<1e-9;star.append({'q':q,'v_h':vh,'v_t':vt,'three_spin_L':L,'duality_residual':vh*vt-q})
out['potts_star_triangle']=star
# Cubic fixed point eigenvalues in two regimes.
cubic=[]
for n in (3,5):
 u=1/(3*n);v=(n-4)/(9*n);J=np.array([[1-2*(n+8)*u-6*v,-6*u],[-12*v,1-12*u-18*v]]);ev=np.sort(np.linalg.eigvals(J));refev=np.sort([-1,(4-n)/(3*n)]);assert np.max(abs(ev-refev))<1e-12;cubic.append({'n':n,'epsilon':1,'rescaled_u':u,'rescaled_v':v,'eigenvalues':ev.tolist(),'scope':'algebra at one-loop; epsilon=1 used only to normalise eigenvalues, not quantitative real critical estimate'})
out['cubic_rg']=cubic
# Small seeded 1D Metropolis, compare with exact finite ring; blocked error estimate.
rng=np.random.default_rng(333334);ns=64;spins=rng.choice([-1,1],ns);Kmc=.6;energies=[]
for sweep in range(16000):
 for parity in (0,1):
  idx=np.arange(parity,ns,2);de=2*Kmc*spins[idx]*(spins[(idx-1)%ns]+spins[(idx+1)%ns]);accept=(rng.random(len(idx))<.5)&(rng.random(len(idx))<np.minimum(1,np.exp(-de)));spins[idx[accept]]*=-1
 if sweep>=2000:energies.append(-np.mean(spins*np.roll(spins,-1)))
blocks_mc=np.array(energies).reshape(-1,100).mean(axis=1);se=blocks_mc.std(ddof=1)/math.sqrt(len(blocks_mc));t=math.tanh(Kmc);exact=-(t+t**(ns-1))/(1+t**ns);mean=float(np.mean(energies));assert abs(mean-exact)<6*se
out['metropolis_1d']={'seed':333334,'sites':ns,'K':Kmc,'sweeps':16000,'discarded':2000,'samples':14000,'block_sweeps':100,'proposal_probability_per_spin':.5,'aperiodicity':'lazy proposals remove deterministic zero-energy sublattice cycles','mean_energy_per_site_J':mean,'block_standard_error':se,'exact_finite_ring':exact,'difference_in_block_SE':abs(mean-exact)/se,'scope':'finite chain algorithm check, not critical finite-size inference'}
# Ring instability and Bose heat curves.
li=lambda s,z:mp.polylog(s,z)
ring=lambda x:1-(li(.5,x)-li(1.5,x))/(2*x)-(1-mp.mpf(2)**(-mp.mpf(2.5)))*x
root=mp.findroot(ring,(.65,.75));out['boson_ring_spinodal_nlambda3']=float(root)
def heat(s,z):return s*(s+1)*li(s+1,z)/li(s,z)-s*s*li(s,z)/li(s-1,z)
maxima=[]
for s in (1.01,1.05,1.1,1.2,1.5):
 opt=minimize_scalar(lambda z:-float(heat(s,z)/s),bounds=(1e-5,.99999),method='bounded',options={'xatol':2e-7});Rc=float((s+1)*mp.zeta(s+1)/mp.zeta(s));maxima.append({'s_d_over_2':s,'critical_left_ratio':Rc,'normal_branch_peak_ratio':-opt.fun,'z_at_normal_peak':opt.x,'global_peak_ratio':max(Rc,-opt.fun,1.)})
out['bose_heat_maxima']=maxima
# Vector figure with parameterised Bose normal branch, sorted by actual T/Tc.
zs=sorted(set(list(np.linspace(.001,.96,85))+[1-10**(-v)for v in np.linspace(1.5,12,65)]));pts=[]
for z in zs:
 tt=float((mp.zeta(1.5)/li(1.5,z))**(mp.mpf(2)/3));cc=float(heat(mp.mpf(1.5),mp.mpf(z)))
 if tt<=4:pts.append((tt,cc))
pts.sort();low=[(v,float(1.5*2.5*mp.zeta(2.5)/mp.zeta(1.5))*v**1.5)for v in np.linspace(0,1,70)]
def coords(points):return ' '.join(f'({x:.9g},{y:.9g})'for x,y in points)
(ROOT/'figures/bose-heat.tex').write_text('\\begin{center}\\begin{tikzpicture}\\begin{axis}[width=10cm,height=4.5cm,xlabel={$T/T_c$},ylabel={$C/(N\\kb)$},xmin=0,xmax=4,ymin=0,ymax=2.1]\n\\addplot[thick,structurecolor] coordinates {'+coords(low)+'};\n\\addplot[thick,structurecolor] coordinates {'+coords(pts)+'};\n\\addplot[dashed,gray,domain=0:4]{1.5};\\end{axis}\\end{tikzpicture}\\end{center}\n')
sat=3*2**(2/3)/4;stoner=[]
for rr in np.linspace(.8,1.4,180):
 if rr<=1:mm=0
 elif rr>=sat:mm=1
 else:mm=brentq(lambda m:((1+m)**(2/3)-(1-m)**(2/3))/m-4*rr/3,1e-6,1)
 stoner.append((rr,mm))
(ROOT/'figures/stoner.tex').write_text('\\begin{center}\\begin{tikzpicture}\\begin{axis}[width=10cm,height=4.5cm,xlabel={$\\alpha/\\alpha_c$},ylabel={$|m_s|$},xmin=.8,xmax=1.4,ymin=0,ymax=1.05]\\addplot[thick,structurecolor] coordinates {'+coords(stoner)+'};\\end{axis}\\end{tikzpicture}\\end{center}\n')
out['vector_figures']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in (ROOT/'figures').glob('*.tex')}
(ROOT/'qa/numerical-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('Numerical checks passed; two vector figures generated.')
