#!/usr/bin/env python3
"""Recompute selected physically sensitive values independently, standard library."""
from pathlib import Path
import math,json,argparse,cmath
ROOT=Path(__file__).resolve().parents[1]
e=1.602176634e-19;eps=8.8541878128e-12;me=9.1093837015e-31;mp=1.67262192369e-27;kB=1.380649e-23;h=6.62607015e-34;mu=4*math.pi*1e-7

def bisect(f,lo,hi):
 assert f(lo)*f(hi)<0
 for _ in range(80):
  mid=(lo+hi)/2
  if f(lo)*f(mid)<0:hi=mid
  else:lo=mid
 return (lo+hi)/2

def simpson(f,lo,hi,n=100000):
 step=(hi-lo)/n
 return step/3*(f(lo)+f(hi)+sum((4 if i%2 else 2)*f(lo+step*i)for i in range(1,n)))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=ROOT/'qa/basic-numerics.json');args=ap.parse_args()
 saha=lambda t:2*(2*math.pi*me*t*e)**1.5/h**3*math.exp(-13/t)-101325/(3*t*e)
 T=bisect(saha,.1,10)
 capacitances=[]
 for n in [1e20,1e12]:
  lam=math.sqrt(eps*1000*e/(n*e**2));capacitances.append(dict(n=n,lambda_m=lam,C_F=4*math.pi*eps*.1*(1+.1/lam)))
 table=[]
 for nl,tl in [(9,2.5),(17,4),(21,5),(22,3),(0,3.5),(6.5,5),(11.5,3),(13,6.5),(20,8),(18,3)]:
  n=10**nl;Tk=10**tl;lam=math.sqrt(eps*kB*Tk/(n*e**2));a=(3/(4*math.pi*n))**(1/3);gamma=e*e/(4*math.pi*eps*a*kB*Tk)
  table.append(dict(logn=nl,logT_K=tl,lambda_m=lam,Lambda=n*lam**3,fpe_Hz=math.sqrt(n*e*e/(eps*me))/(2*math.pi),Gamma=gamma,degeneracy=n*(h/math.sqrt(2*math.pi*me*kB*Tk))**3))
 A=200/15**1.5;B=.188;Uc=(B/A)**(2/3);U0=3.5;Uf=.015
 time=lambda u:math.log((U0**1.5+B/A)/(u**1.5+B/A))/(3*A)
 Ue=simpson(lambda u:u**1.5/(u**1.5+Uc**1.5),Uf,U0);Ui=U0-Uf-Ue
 alpha=dict(Uc_MeV=Uc,tcrit_s=time(Uc),tfinal_s=time(Uf),remaining_s=time(Uf)-time(Uc),fe=Ue/(Ue+Ui),fi=Ui/(Ue+Ui),initial_energy_fraction_e=Ue/U0,initial_energy_fraction_i=Ui/U0,residual_fraction=Uf/U0)
 assert abs(alpha['fe']+alpha['fi']-1)<1e-14
 r=1.28e7;Bb=3.75e-6;W=1e6*e
 earth=dict(period_s=2*math.pi*e*Bb*r*r/(4*W),gyroradius_m=math.sqrt(2*mp*2/3*W)/(e*Bb))
 f=210e9;fc=lambda r:e*5/(1+r/67)/(2*math.pi*me)
 density=lambda val:4*math.pi**2*eps*me/e**2*val
 ncut=density(f*(f-fc(12.5)))/(1-(12.5/20)**2)
 nres=density(f*f-fc(7.25)**2)/(1-(7.25/20)**2)
 rres=bisect(lambda r:ncut*(1-(r/20)**2)*e**2/(4*math.pi**2*eps*me)+fc(r)**2-f*f,0,15)
 buddenb=(2*math.pi*f/299792458)**2*.1275/.075
 # Independent complex substitution of the quasi-neutral drifting Lorentz roots.
 delta=math.sqrt(me/mp);V=2.;ve=30.;vi=.002;k=.7;residuals=[]
 for sign in [-1,1]:
  omega=k*(delta*delta*V+sign*delta*(vi-ve))/(1+delta*delta)-1j*k*(sign*delta*V+vi+delta*delta*ve)/(1+delta*delta)
  aa=omega-k*V+1j*k*ve;bb=omega+1j*k*vi
  residuals.append(abs(1/aa**2+delta**2/bb**2))
 assert max(residuals)<1e-12
 eta=5.2e-5*17/2000**1.5;field=eta*4e5/(math.pi*.3**2);Wrun=3*1e19*e**3*17/(8*math.pi*eps**2*field)
 rec=dict(Spitzer_runaway=dict(eta_Ohm_m=eta,E_V_m=field,loop_V=2*math.pi*1.2*field,formal_nonrel_runaway_MeV=Wrun/(1e6*e),formal_v_over_c=math.sqrt(2*Wrun/me)/299792458),status='PASS',scope='Sensitive numerical examples plus independent complex dispersion substitution; not all manuscript mathematics.',saha=dict(T_eV=T,T_K=T*e/kB,electron_vs_300K_gas=300*kB/(3*T*e)),capacitances=capacitances,plasma_table=table,alpha_slowdown=alpha,earth_drift=earth,Bennett_current_A=math.sqrt(8*math.pi**2*.01**2*1e20*1e4*e/mu),optical_final=dict(n0_cutoff_m_inv3=ncut,n0_resonance_m_inv3=nres,relative_inconsistency=nres/ncut-1,predicted_resonance_cm=rres,budden_b_m_inv2=buddenb,budden_a_m_inv1=-buddenb*.0525,reflection_exponent=math.pi*math.sqrt(buddenb)*.0525),Lorentz_dispersion_residuals=residuals)
 args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');print(args.out)
if __name__=='__main__':main()
