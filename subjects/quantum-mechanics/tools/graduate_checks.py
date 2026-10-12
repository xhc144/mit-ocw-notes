#!/usr/bin/env python3
"""Recompute explicit graduate formula checks. Not an independent full proof review."""
from pathlib import Path
import hashlib,json,math,itertools
import numpy as np
import sympy as S
import scipy.special as sp
from scipy.integrate import simpson
from scipy.linalg import expm
from scipy.constants import m_e,e,epsilon_0,mu_0,hbar,c,physical_constants
from sympy.physics.wigner import wigner_3j,wigner_6j
ROOT=Path(__file__).resolve().parents[1]
records={}
# Radiation radial integrals, E2 rate and 2S hyperfine leading-order model.
r,a=S.symbols('r a',positive=True)
R10=2*a**(-S.Rational(3,2))*S.exp(-r/a)
R21=r*S.exp(-r/(2*a))/(2*S.sqrt(6)*a**S.Rational(5,2))
R32=4*r*r*S.exp(-r/(3*a))/(81*S.sqrt(30)*a**S.Rational(7,2))
I1=S.integrate(R10*R21*r**3,(r,0,S.oo));I2=S.integrate(R10*R32*r**4,(r,0,S.oo))
assert S.simplify(I1-256*a/(81*S.sqrt(6)))==0
assert S.simplify(I2-1215*a*a/(128*S.sqrt(30)))==0
bohr=physical_constants['Bohr radius'][0];muB=physical_constants['Bohr magneton'][0];muN=physical_constants['nuclear magneton'][0];gp=5.5856946893
w2S=(2*mu_0/3)*2*muB*gp*muN/(8*math.pi*bohr**3)/hbar
G2S=mu_0*w2S**3*((2*muB+gp*muN)/2)**2/(3*math.pi*hbar*c**3)
wE2=physical_constants['Rydberg constant times hc in J'][0]*(1-1/9)/hbar
GE2=e*e*wE2**5*float((I2/a**2))**2*bohr**4/(300*math.pi*epsilon_0*hbar*c**5)
records['radiation']={'E1_radial':str(I1),'E2_radial':str(I2),'2S_hyperfine_leading_model_rate_per_s':G2S,'3d_to_1s_E2_rate_per_s':GE2,'2S_is_not_21cm_1S':True}
j=S.Rational(1,2);states=[(j,j),(j,-j),(3*j,3*j),(3*j,j),(3*j,-j),(3*j,-3*j)]
M=[]
for F,m in states:
 row=[S.simplify(2*(2*F+1)*(2*Fp+1)*wigner_6j(j,Fp,1,F,j,1)**2*wigner_3j(Fp,1,F,-mp,mp-m,m)**2)if abs(mp-m)<=1 else S.Integer(0)for Fp,mp in states]
 assert sum(row)==1;M.append(row)
expected=S.Matrix([[1,2,12,8,4,0],[2,1,0,4,8,12],[12,0,9,6,0,0],[8,4,6,1,8,0],[4,8,0,8,1,6],[0,12,0,0,6,9]])/27
assert S.Matrix(M)==expected;records['deuterium_branch_matrix']='all36 entries equal Wigner 3j/6j result, rows sum1 at common frequency'
Z=S.symbols('Z',positive=True);k=Z-S.Rational(1,2)
int4=S.expand(2*k**3*((Z/k)**3/3-Z/k+S.Rational(2,3)))
EE=S.simplify(-k*k-int4);assert S.expand(EE+(Z-S.Rational(1,4))**2+S.Rational(1,48))==0
records['hartree']={'energy':str(EE),'domain':'normalizable csch stationary solution Z>1/2; limit at1/2; not claimed exact correlated energy'}
# d3 weights and all LS highest weight multiplicities.
weights={}
for b in itertools.combinations(range(10),3):
 ml=sum(i//2-2 for i in b);ms=sum(1 if i%2==0 else -1 for i in b);weights[ml,ms]=weights.get((ml,ms),0)+1
terms=[]
for ss in [3,1]:
 for L in range(7):
  n=weights.get((L,ss),0)-weights.get((L+1,ss),0)-weights.get((L,ss+2),0)+weights.get((L+1,ss+2),0)
  if n:terms.append([L,ss,n])
assert terms==[[1,3,1],[3,3,1],[1,1,1],[2,1,2],[3,1,1],[4,1,1],[5,1,1]]
assert sum(n*(2*l+1)*(ss+1)for l,ss,n in terms)==120
records['d3']={'terms_L_2S_multiplicity':terms,'total_dimension':120}
# Printed p3 basis Gram and highest weights.
basis=list(itertools.combinations(range(6),3));statesP=[{(0,4,5):1,(2,3,4):1},{(0,2,5):1,(1,2,4):-1},{(0,2,3):1,(0,1,4):1},{(1,4,5):1,(2,3,5):1},{(0,3,5):1,(1,3,4):-1},{(1,2,3):1,(0,1,5):1}]
V=S.Matrix([[v.get(b,0)/S.sqrt(2)for v in statesP]for b in basis]);assert V.T*V==S.eye(6)
def one(b,i,j):
 if j not in b:return None
 aa=list(b);sg=(-1)**aa.index(j);aa.remove(j)
 if i in aa:return None
 sg*=(-1)**sum(x<i for x in aa);aa.append(i);return tuple(sorted(aa)),sg
for mode in ['L+','S+']:
 out={}
 for b,coef in statesP[0].items():
  for jj in b:
   ii=jj+2 if mode=='L+' else jj-1
   if (mode=='L+'and jj//2<2)or(mode=='S+'and jj%2==1):
    z=one(b,ii,jj)
    if z:bb,sg=z;out[bb]=out.get(bb,0)+coef*sg
 assert all(v==0 for v in out.values())
records['p3_2P']='six printed Slater combinations orthonormal; highest weight annihilated by L+ and S+'
# Gamma/Weyl exact transformation and all Clifford basis traces.
I=S.eye(2);O=S.zeros(2);pa=[S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-S.I],[S.I,0]]),S.diag(1,-1)]
U=S.BlockMatrix([[I,I],[-I,I]]).as_explicit()/S.sqrt(2)
g=[S.diag(1,1,-1,-1)]+[S.BlockMatrix([[O,p],[-p,O]]).as_explicit()for p in pa]
assert U*g[0]*U.T==S.BlockMatrix([[O,-I],[-I,O]]).as_explicit()
for gi in g[1:]:assert U*gi*U.T==gi
GG=[]
for mask in range(16):
 A=S.eye(4)
 for ii in range(4):
  if mask&(1<<ii):A=A*g[ii]
 GG.append(A)
for ii,A in enumerate(GG):
 assert A*A in [S.eye(4),-S.eye(4)]
 for jj,B in enumerate(GG):
  if ii!=jj:assert S.trace(A*B)==0
records['dirac']='specified U yields negative off-diagonal gamma0; all16 Clifford products trace-orthogonal'
# Compare Ramsey formula directly to exact two pulse SU2 product.
x=np.array([[0,1],[1,0]],complex);z=np.diag([1,-1]);worst=0
rng=np.random.default_rng(8321)
for _ in range(100):
 Om=float(rng.uniform(.1,4));De=float(rng.uniform(-3,3));tau=float(rng.uniform(.01,2));T=float(rng.uniform(0,3));W=math.hypot(Om,De)
 up=expm(-.5j*tau*(Om*x+De*z));ut=up@expm(-.5j*De*T*z)@up
 pp=abs(ut[1,1])**2;cc=math.cos(W*tau/2);ss=math.sin(W*tau/2);d=De*T/2
 formula=1-4*Om**2/W**2*ss**2*(cc*math.cos(d)-De/W*ss*math.sin(d))**2
 worst=max(worst,abs(pp-formula))
assert worst<1e-12;records['ramsey']={'100_parameter_cases_max_abs_error':worst}
# Hard sphere convergence and angular integral against partial-wave total.
angular=[]
for rho in [.1,.5,1,10,25,100]:
 ell=np.arange(math.ceil(rho+4*rho**(1/3)+14));jv=sp.spherical_jn(ell,rho);nv=sp.spherical_yn(ell,rho);aell=jv/(nv-1j*jv)
 total=4*np.sum((2*ell+1)*abs(aell)**2)/rho**2
 theta=np.linspace(0,np.pi,6001);ff=sum((2*l+1)*aell[l]*sp.eval_legendre(l,np.cos(theta))for l in ell)/rho
 integ=2*simpson(abs(ff)**2*np.sin(theta),x=theta)
 ext=np.arange(len(ell)+24);aj=sp.spherical_jn(ext,rho);an=sp.spherical_yn(ext,rho);aa=aj/(an-1j*aj);ext_total=4*np.sum((2*ext+1)*abs(aa)**2)/rho**2
 assert abs(total-integ)<1e-5;assert abs(total-ext_total)<1e-10
 angular.append({'rho':rho,'sigma_over_piR2':float(total),'angular_integral_abs_error':float(abs(total-integ)),'extended_cutoff_abs_error':float(abs(total-ext_total))})
records['hard_sphere']=angular
paths=sorted((ROOT/'chapters').glob('*graduate*.tex'))+[ROOT/'chapters'/n for n in []]
report={'status':'PASS','scope':'explicit symbolic/numerical checks listed; not independent or exhaustive full proof review','checks':records,'checked_manuscript_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths},'versions':{'numpy':np.__version__,'sympy':S.__version__}}
(ROOT/'qa/graduate-formula-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('Graduate explicit checks PASS')
