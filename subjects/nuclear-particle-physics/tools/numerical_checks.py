#!/usr/bin/env python3
"""Independent unit-consistent checks of selected course models (standard library)."""
import math,json,pathlib,argparse
ROOT=pathlib.Path(__file__).resolve().parents[1]
def simpson(f,a,b,n=20000):
 h=(b-a)/n
 return h/3*(f(a)+f(b)+sum((4 if i%2 else 2)*f(a+i*h) for i in range(1,n)))
def deuteron(B):
 mu=469.5;hc=197.327;R=2.1;V=35
 k=math.sqrt(2*mu*(V-B))/hc;q=math.sqrt(2*mu*B)/hc
 A2=1/(R/2-math.sin(2*k*R)/(4*k)+math.sin(k*R)**2/(2*q))
 rms=math.sqrt(simpson(lambda r:r*r*A2*(math.sin(k*r)**2 if r<R else math.sin(k*R)**2*math.exp(-2*q*(r-R))),0,80))
 return dict(B_MeV=B,k_fm_inv=k,kappa_fm_inv=q,matching_residual_fm_inv=k/math.tan(k*R)+q,A_fm_inv_half=math.sqrt(A2),P_out=A2*math.sin(k*R)**2/(2*q),RMS_relative_fm=rms)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=pathlib.Path,default=ROOT/'qa/numerical-checks.json');a=ap.parse_args()
 lo,hi=.001,10
 for _ in range(70):
  b=(lo+hi)/2
  if deuteron(b)['matching_residual_fm_inv']>0:hi=b
  else:lo=b
 d=deuteron((lo+hi)/2)
 assert abs(d['matching_residual_fm_inv'])<1e-12
 assert abs(d['P_out']-.6000751)<1e-6
 mpi=.13957;k=.427;theta=math.radians(2.5)
 emax=k*mpi/math.sin(theta);peak=mpi/math.sin(theta)
 def enu(ep):return k*mpi**2/(ep-math.sqrt(ep*ep-mpi*mpi)*math.cos(theta))
 T=16*5*(85-5)/85**2*math.exp(-80)
 weights=[3*4.18**2,3*1.28**2,1.78**2,.11**2];h=sum(weights)
 data=dict(status='PASS',units='energies MeV except T2K GeV; Higgs model weights GeV^2; deuteron radii fm; alpha times seconds',deuteron_input=deuteron(2.2),deuteron_consistent=d,T2K=dict(E_peak_parent_GeV=peak,E_max_GeV=emax,E_parent1_GeV=enu(1),E_parent5_GeV=enu(5)),alpha_2010=dict(transmission=T,wait_s=1/(6e22*T)),higgs_problem1_3=dict(weighted_mass_squared_GeV2=h,branching_percent=[100*w/h for w in weights],model='four fermion channels; colour factor 3 for quarks; not total physical Higgs width'),scope='Selected sensitive model calculations; not a claim of independent verification of every equation.')
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');print(a.out)
if __name__=='__main__':main()
