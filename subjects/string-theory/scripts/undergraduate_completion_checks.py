#!/usr/bin/env python3
"""Exact algebra and independent finite-state checks for expanded 8.251."""
import json, math
from pathlib import Path
import sympy as s
from scipy.integrate import quad
from scipy.special import jn_zeros
ROOT=Path(__file__).resolve().parents[1]
pp,p2,p3,m,t,k=s.symbols('pp p2 p3 m t k',positive=True)
pm=(p2*p2+p3*p3+m*m)/(2*pp)
psi=s.Function('psi')(pp,p2,p3)
I=s.I
def Xm(f): return -I*s.diff(f,pp)+k*pm*t*f
def X2(f): return I*s.diff(f,p2)+k*p2*t*f
def X3(f): return I*s.diff(f,p3)+k*p3*t*f
def Xp(f): return k*pp*t*f
def Mpm(f): return I*(pp*s.diff(f,pp)+f/2)
def Mm2(f): return -I*(p2*s.diff(f,pp)+pm*s.diff(f,p2)+s.diff(pm,p2)*f/2)
def comm(A,B): return s.simplify(A(B(psi))-B(A(psi)))
checks={
 'Mpm_Xplus':s.simplify(comm(Mpm,Xp)-I*Xp(psi)),
 'Mpm_Xminus':s.simplify(comm(Mpm,Xm)+I*Xm(psi)),
 'Mpm_X2':comm(Mpm,X2),
 'Mm2_Xplus':s.simplify(comm(Mm2,Xp)+I*k*t*p2*psi),
 'Mm2_Xminus':s.simplify(comm(Mm2,Xm)-I/2*(I*s.diff(pm/pp*psi,p2)+pm/pp*I*s.diff(psi,p2))),
 'Mm2_X2':s.simplify(comm(Mm2,X2)+I*Xm(psi)-I/2*(I*s.diff(p2/pp*psi,p2)+p2/pp*I*s.diff(psi,p2))),
 'Mm2_X3':s.simplify(comm(Mm2,X3)-I/2*(I*s.diff(p3/pp*psi,p2)+p3/pp*I*s.diff(psi,p2)))
}
assert all(v==0 for v in checks.values()),checks
R,V,H,K=s.symbols('R V H K',positive=True)
L=-K*R*s.sqrt(1-(V-H*R)**2)
ham=s.simplify(V*s.diff(L,V)-L)
expected=K*R*(1+H*R*(V-H*R))/s.sqrt(1-(V-H*R)**2)
assert s.simplify(ham-expected)==0
statpot=K*R*s.sqrt(1-H*H*R*R)
rstar=1/(s.sqrt(2)*H)
assert s.simplify(s.diff(statpot,R).subs(R,rstar))==0
growth=s.simplify(-s.diff(statpot,R,2).subs(R,rstar)/s.diff(L,V,2).subs({R:rstar,V:0}))
assert growth==2*H*H
def conv(a,b,N):return [sum(a[j]*b[i-j] for j in range(i+1)) for i in range(N+1)]
def bosferm(bos,ferm,half,N,parity=None):
 # Work in units half a level; include fermion parity as separate DP axis.
 a=[[0]*(N+1) for _ in range(2)];a[0][0]=1
 for freq in range(2,N+1,2):
  for _ in range(bos):
   for j in range(freq,N+1):
    for par in range(2):a[par][j]+=a[par][j-freq]
 for freq in range(1 if half else 2,N+1,2):
  for _ in range(ferm):
   for j in range(N,freq-1,-1):
    old0,old1=a[0][j-freq],a[1][j-freq]
    a[0][j]+=old1;a[1][j]+=old0
 return a[parity] if parity is not None else [a[0][j]+a[1][j] for j in range(N+1)]
nsleft=bosferm(8,32,True,4,0)
assert [nsleft[0],nsleft[2],nsleft[4]]==[1,504,40996]
nsright=bosferm(8,8,True,9,1)
assert [nsright[i] for i in [1,3,5,7,9]]==[8,128,1152,7680,42112]
rleft=[32768*x for x in bosferm(8,32,False,2)]
assert [rleft[0],rleft[2]]==[32768,1310720]
nd=[0]*5;nd[0]=1
for n in [2,4]:
 for _ in range(23):
  for j in range(n,5):nd[j]+=nd[j-n]
for n in [1,3]:
 for j in range(n,5):nd[j]+=nd[j-n]
assert nd==[1,1,24,25,324]
gamma=float(jn_zeros(0,2)[1])
mean=quad(lambda u:math.cos(gamma*math.sin(u)),0,2*math.pi,epsabs=1e-12)[0]/(2*math.pi)
assert abs(mean)<1e-12
cusp_angles=[]
for target in [-3*math.pi/2,-math.pi/2,math.pi/2,3*math.pi/2]:
 a=math.acos(target/gamma);cusp_angles +=[a,2*math.pi-a]
assert len(set(round(x,10) for x in cusp_angles))==8
report={'status':'PASS','scope':'Exact differential-operator commutators away from p+=0; exact de Sitter Hamiltonian and linear stability; independent integer DP state counts; numerical closure/cusp check. Does not establish full string Lorentz algebra or nonperturbative consistency.',
 'particle_operator_residuals':{k:str(v) for k,v in checks.items()},
 'de_sitter_growth_squared':str(growth),
 'left_NS_counts':[nsleft[0],nsleft[2],nsleft[4]],
 'left_R_counts':[rleft[0],rleft[2]],
 'right_NS_counts':[nsright[i] for i in [1,3,5,7,9]],
 'heterotic_first_massive_total':(40996+32768)*(128+128),
 'one_ND_23_integer_counts':nd,'closed_cusp_gamma':gamma,
 'closed_curve_mean':mean,'eight_cusp_angles_rad':sorted(cusp_angles),
 'earliest_cusp_ct_over_L':math.asin(math.pi/(2*gamma))/(2*math.pi)}
(ROOT/'qa/undergraduate-completion-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))

