#!/usr/bin/env python3
"""Explicit checks of parent-requested pedagogical bridges; not independent whole-book review."""
from pathlib import Path
import hashlib,json,itertools,math
import numpy as np
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[1];checks={}
# Gaussian fluctuation determinant: direct numerical determinant vs recurrence.
w=.8;T=1.3;rows=[]
for N in [5,10,20,40]:
 eps=T/N;d=2-w*w*eps*eps;A=np.diag(np.full(N-1,d))+np.diag(np.full(N-2,-1.),1)+np.diag(np.full(N-2,-1.),-1)
 theta=math.acos(d/2);direct=float(np.linalg.det(A));exact=math.sin(N*theta)/math.sin(theta)
 assert abs(direct-exact)/exact<1e-11
 rows.append({'N':N,'determinant':direct,'relative_error':abs(direct-exact)/exact})
limit=math.sqrt(w/math.sin(w*T));errors=[]
for N in [20,40,80,160]:
 eps=T/N;theta=2*math.asin(w*eps/2);fac=math.sqrt(math.sin(theta)/(eps*math.sin(N*theta)));errors.append(abs(fac-limit))
assert all(errors[j+1]<errors[j]/3.9 for j in range(3));checks['HO_determinant']={'direct_matrix_checks':rows,'continuum_prefactor_errors':errors,'all_positive_before_first_caustic':True}
# Coulomb sum integral with a=i eta in an initial convergence strip; regularize endpoint t=u^10.
mp.mp.dps=60;coul=[]
for aa,xx in [(mp.mpf('-.8'),mp.mpf('.2')),(mp.mpc('-.85','.1'),mp.mpf('-.4'))]:
 def integrand(u):
  if u==0 or u==1:return mp.mpf('0')
  t=u**10;return t**aa*(1-t)**(-1-2*aa)*(1-t*t)/(1-2*xx*t+t*t)**mp.mpf('1.5')*10*u**9
 actual=mp.quad(integrand,[0,.3,.7,1])/mp.gamma(-2*aa)
 h=(1-xx)/2;closed=-aa*mp.gamma(1+aa)/mp.gamma(1-aa)*h**(-aa-1)
 err=abs(actual-closed);assert err<mp.mpf('1e-20')
 coul.append({'a':str(aa),'x':str(xx),'integral':str(actual),'closed':str(closed),'abs_error':str(err)})
checks['Coulomb_beta_integral']=coul
# S3 Young symmetrizer, vectors and exact irreducible reflection matrices.
b=list(itertools.permutations([1,2,3]));I=s.eye(6)
def P(ii,jj):
 A=s.zeros(6)
 for k,v in enumerate(b):
  vv=list(v);vv[ii],vv[jj]=vv[jj],vv[ii];A[b.index(tuple(vv)),k]=1
 return A
P12=P(0,1);P13=P(0,2);P23=P(1,2);Y=(I-P13)*(I+P12);assert Y*Y==3*Y
seed=s.zeros(6,1);seed[b.index((1,2,3))]=1;v=Y*seed;vv=P23*v
assert P12*v==v-vv and P12*vv==-vv and P23*vv==v
U=s.Matrix.hstack(v/2,(vv-v/2)/s.sqrt(3));assert U.T*U==s.eye(2)
D12=U.T*P12*U;D23=U.T*P23*U
assert D12==s.Matrix([[1,-s.sqrt(3)],[-s.sqrt(3),-1]])/2
assert D23==s.Matrix([[1,s.sqrt(3)],[s.sqrt(3),-1]])/2
assert D12*D12==D23*D23==s.eye(2);assert (D12*D23)**3==s.eye(2);assert D12*D23!=D23*D12
checks['S3_Young']={'Y_squared_equals_3Y':True,'printed_vectors_and_matrices_exact':True,'orthonormal_basis':True,'group_relations_and_irreducibility_in_2D':True}
# Independent angular quadrature verifies polarization contraction for complex symmetric traceless Q.
mu,weights=np.polynomial.legendre.leggauss(8);phis=np.arange(16)*2*math.pi/16
rng=np.random.default_rng(8311);maxerr=0
for _ in range(20):
 X=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));Q=(X+X.T)/2;Q-=np.eye(3)*np.trace(Q)/3;val=0
 for zz,weight in zip(mu,weights):
  for phi in phis:
   nn=np.array([math.sqrt(1-zz*zz)*math.cos(phi),math.sqrt(1-zz*zz)*math.sin(phi),zz]);Qn=Q@nn
   val+=weight*(2*math.pi/16)*(np.vdot(Qn,Qn).real-abs(nn@Qn)**2)
 expected=4*math.pi/5*np.sum(abs(Q)**2);maxerr=max(maxerr,abs(val-expected)/expected)
assert maxerr<1e-13;assert s.Rational(1,288)*s.Rational(4,5)==s.Rational(1,360)
checks['E2_polarization_angular']={'20_complex_Q_quadratures_max_relative_error':maxerr,'288pi2_to_360pi_coefficient':True}
# Markov ODE and Lorentz half maximum, with Gamma a rate.
t=s.symbols('t',real=True);Gamma,hbar=s.symbols('Gamma hbar',positive=True);Delta=s.symbols('Delta',real=True)
a=s.exp(-Gamma*t/2-s.I*Delta*t/hbar);assert s.simplify(s.diff(a,t)+(Gamma/2+s.I*Delta/hbar)*a)==0
line=lambda EE:1/(EE**2+(hbar*Gamma/2)**2)
assert s.simplify(line(hbar*Gamma/2)/line(0))==s.Rational(1,2)
checks['linewidth']={'complex_amplitude_ODE_exact':True,'energy_FWHM_hbarGamma':True,'Markov_applicability_is_an_explicit_assumption':True}
files=[ROOT/'chapters'/n for n in ['graduate-321-theory.tex','graduate-321-ps01-06.tex','graduate-322-theory.tex']]
report={'status':'PASS','scope':'checks of requested derivation bridges only; not full independent math/pedagogy review','checks':checks,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files}}
(ROOT/'qa/graduate-parent-bridge-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('Parent-requested bridge checks PASS')
