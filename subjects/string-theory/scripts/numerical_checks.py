"""Independent finite-order spectrum and worldsheet checks. numpy/scipy required."""
from pathlib import Path
import json,math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq,minimize_scalar
base=Path(__file__).resolve().parents[1]
def mul(a,b,n):
 c=[0]*(n+1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   if i+j<=n:c[i+j]+=x*y
 return c
def count_bos(d,n):
 a=[1]+[0]*n
 for m in range(1,n+1):
  b=[0]*(n+1)
  for j in range(n//m+1):b[j*m]=math.comb(d+j-1,j)
  a=mul(a,b,n)
 return a
def count_R(n):
 a=count_bos(8,n)
 for m in range(1,n+1):
  b=[0]*(n+1)
  for j in range(min(8,n//m)+1):b[j*m]=math.comb(8,j)
  a=mul(a,b,n)
 return [8*x for x in a]
def count_NS(n):
 # q exponent is 2N. The GSO projection retains odd fermion number.
 a=[1]+[0]*n;b=a[:]
 for m in range(1,n//2+1):
  f=[0]*(n+1)
  for j in range(n//(2*m)+1):f[2*m*j]=math.comb(8+j-1,j)
  a=mul(a,f,n);b=mul(b,f,n)
 for m in range(1,n+1,2):
  f=[0]*(n+1);g=[0]*(n+1)
  for j in range(min(8,n//m)+1):f[m*j]=math.comb(8,j);g[m*j]=(-1)**j*math.comb(8,j)
  a=mul(a,f,n);b=mul(b,g,n)
 return [(a[2*j+1]-b[2*j+1])//2 for j in range((n+1)//2)]
bos=count_bos(24,4);R=count_R(4);NS=count_NS(9)
assert R==NS
def integrand(y,a):
 if y<1e-6:return .5*(1-a**4)*y*y
 return (math.sqrt((1-a**4*y**4)/(1-y**4))-1)/y**2
def sep(a):
 return 2*a*math.sqrt(1-a**4)*quad(lambda th:math.sin(th)**2/math.sqrt((1-a**4*math.sin(th)**4)*(1+math.sin(th)**2)),0,math.pi/2,epsabs=1e-11)[0]
def free(a):return (quad(lambda y:integrand(y,a),0,1,epsabs=1e-10)[0]-1+a)/a
ac=brentq(free,.1,.9);amax=minimize_scalar(lambda a:-sep(a),bounds=(.01,.999),method='bounded',options={'xatol':1e-11}).x
data=[]
for a in np.linspace(.03,.99,150):data.append((a,sep(a)/math.pi,free(a)))
np.savetxt(base/'qa/thermal-wilson.csv',data,delimiter=',',header='zstar_zh,L_times_T,free_dimensionless',comments='')
out={'bosonic_open_degeneracies_N0_to4':bos,'open_superstring_R_mass0_to4':R,'open_superstring_NS_mass0_to4':NS,'closed_bosonic_degeneracies':[x*x for x in bos],'typeII_boson_and_fermion_separately':[2*x*x for x in R],'vacuum_length_micrometer':(1.055e-34/(7.6e-27*2.998e8))**.25*1e6,'wilson_zero_T_integral':quad(lambda y:y*y/math.sqrt(1-y**4),0,1)[0],'wilson_thermal':{'critical_zstar_over_zh':ac,'critical_L_T':sep(ac)/math.pi,'max_zstar_over_zh':amax,'max_L_T':sep(amax)/math.pi},'species_entropy_coefficient_C':(64*math.pi**3/3645)**.25/math.pi,'cusp_events_one_shape_period_in_units_L_c':[[0,0],[.125,.375]]}
assert out['bosonic_open_degeneracies_N0_to4']==[1,24,324,3200,25650]
(base/'qa/numerical-results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
