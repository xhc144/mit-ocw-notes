"""Finite numeric computations for public PS7.2 and PS8.2.

numpy/scipy only. EOS anchors frozen before calculation. TOV rho is energy/c^2.
Enthalpy integration avoids a singular density derivative at the surface.
"""
from pathlib import Path
import argparse,json,math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq,minimize_scalar
from scipy.special import expit
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True)
args=parser.parse_args();out=args.out;out.mkdir(parents=True,exist_ok=True)
G=6.67430e-8;c=2.99792458e10;k=1.380649e-16;hb=1.054571817e-27
mu=1.66053906660e-24;Ms=1.98847e33;MeV=1.602176634e-6
results={}
def save(name,arr,header):np.savetxt(out/name,arr,delimiter=',',header=header,comments='')
rho=1e7;Q=87.78*MeV
def nse(T):
 m4=4*mu+2.42*MeV/c**2;m56=56*mu-53.9*MeV/c**2
 lognq=lambda m:1.5*math.log(m*k*T/(2*math.pi*hb**2))
 logK=lognq(m56)-14*lognq(m4)+Q/(k*T)
 logC=math.log(56*mu)+logK+13*math.log(rho)-14*math.log(4*mu)
 def balance(u):return -np.logaddexp(0,-u)+14*np.logaddexp(0,u)-logC
 u=brentq(balance,-1000,1000);assert abs(balance(u))<1e-8
 return float(expit(u)),logC
temps=np.linspace(4.5e9,6.5e9,401)
save('stellar-NSE.csv',[(T/1e9,1-nse(T)[0],nse(T)[0]) for T in temps],'T9,X_He4,X_Ni56')
half=brentq(lambda T:nse(T)[1]-13*math.log(2),4.5e9,6.5e9)
results['NSE']={'rho_g_cm3':rho,'Q_MeV':87.78,'half_Ni56_T_K':half,'all_charge_mass_constraints_checked':True,'nuclear_spin_weights':1,'model':'pure He4/Ni56 Maxwell-Boltzmann ideal nuclei, no other NSE species or screening'}

gamma=math.log(100)/math.log(5);rho_anchor=1.7e14;P_anchor=1.602176634e33;K=P_anchor/rho_anchor**gamma
rho0=1e14;rho1=10**14.6;Klow=5.5e9
P0=Klow*rho0**(5/3);P1=rho1*c*c;A=(P1-P0)/(rho1-rho0);B=P0-A*rho0
h0=2.5*math.log1p(Klow*rho0**(2/3)/c**2)
h1=h0+A/(c*c+A)*math.log(((c*c+A)*rho1+B)/((c*c+A)*rho0+B))
def state(rho,model):
 if model=='power':
  P=K*rho**gamma;h=gamma/(gamma-1)*math.log1p(P/(rho*c*c));cs2=gamma*P/rho
 elif rho<rho0:
  P=Klow*rho**(5/3);h=2.5*math.log1p(P/(rho*c*c));cs2=5*P/(3*rho)
 elif rho<=rho1:
  P=A*rho+B;h=h0+A/(c*c+A)*math.log(((c*c+A)*rho+B)/((c*c+A)*rho0+B));cs2=A
 else:
  P=rho*c*c;h=h1+.5*math.log(rho/rho1);cs2=c*c
 return P,h,cs2
def inverse(h,model):
 if h<=0:return 0.,0.
 if model=='power':
  rho=(c*c*math.expm1((gamma-1)/gamma*h)/K)**(1/(gamma-1))
 elif h<h0:rho=(c*c*math.expm1(h/2.5)/Klow)**1.5
 elif h<=h1:
  rho=(math.exp((h-h0)*(c*c+A)/A)*((c*c+A)*rho0+B)-B)/(c*c+A)
 else:rho=rho1*math.exp(2*(h-h1))
 return rho,state(rho,model)[0]
for model in ['power','hybrid']:
 for density in np.geomspace(1e8,10**16.5,100):
  P,h,cs=state(density,model);back=inverse(h,model)[0]
  assert abs(back/density-1)<1e-8
def integrate(rhoc,model,rtol=2e-9,start_cm=1.0,max_step=.03):
 Pc,hc,cs=state(rhoc,model);scale=1e6;x0=start_cm/scale
 m0=4*math.pi*rhoc*start_cm**3/(3*Ms)
 hstart=hc-2*math.pi*G*(rhoc/3+Pc/c**2)*start_cm**2/c**2
 def fun(x,y):
  m,hh=y;density,P=inverse(hh,model);r=x*scale;compact=2*G*m*Ms/(r*c*c)
  assert compact<1,'horizon reached in static TOV integration'
  return [4*math.pi*scale*r*r*density/Ms,-G*(m*Ms+4*math.pi*r**3*P/c**2)*scale/(r*r*(1-compact)*c*c)]
 def surface(x,y):return y[1]
 surface.terminal=True;surface.direction=-1
 sol=solve_ivp(fun,[x0,100],[m0,hstart],events=surface,method='DOP853',rtol=rtol,atol=[1e-11,1e-13],max_step=max_step,dense_output=True)
 assert sol.success and len(sol.t_events[0])==1,(model,rhoc,sol.message)
 R=sol.t[-1]*scale;M=sol.y[0,-1]
 return {'rhoc':rhoc,'logrhoc':math.log10(rhoc),'M_solar':M,'R_km':R/1e5,'central_cs2_over_c2':cs/c**2,'compactness_2GM_Rc2':2*G*M*Ms/(R*c*c)},sol
for model in ['power','hybrid']:
 logs=np.linspace(14.0001,16.4999,151);rows=[integrate(10**v,model)[0] for v in logs]
 save('stellar-TOV-'+model+'.csv',[[r['logrhoc'],r['M_solar'],r['R_km'],r['central_cs2_over_c2']] for r in rows],'logrho_c,M_solar,R_km,cs2_c_over_c2')
 max_i=int(np.argmax([r['M_solar'] for r in rows]));lo=logs[max(0,max_i-1)];hi=logs[min(len(logs)-1,max_i+1)]
 opt=minimize_scalar(lambda logrho:-integrate(10**logrho,model)[0]['M_solar'],bounds=(lo,hi),method='bounded',options={'xatol':1e-6})
 best,sol=integrate(10**opt.x,model)
 tight,_=integrate(best['rhoc'],model,rtol=1e-10,start_cm=.1,max_step=.01)
 errM=abs(tight['M_solar']/best['M_solar']-1);errR=abs(tight['R_km']/best['R_km']-1)
 assert errM<1e-6 and errR<1e-5
 xs=np.linspace(sol.t[0],sol.t[-1],500);ys=sol.sol(xs);dens=np.array([inverse(hh,model)[0] for hh in ys[1]])
 save('stellar-TOV-'+model+'-profile.csv',np.c_[xs*10,ys[0],dens/best['rhoc']],'r_km,M_solar,rho_over_central')
 stable=[r for r in rows if r['logrhoc']<=best['logrhoc']]
 save('stellar-TOV-'+model+'-rising.csv',[[r['logrhoc'],r['M_solar'],r['R_km']] for r in stable],'logrho_c,M_solar,R_km')
 results['TOV_'+model]={'grid_count':151,'density_log_interval':[14.0001,16.4999],'maximum_in_range':best,'convergence_relative_M':errM,'convergence_relative_R':errR,'method':'enthalpy and enclosed mass, DOP853; first h=0 surface; rising central-density branch only, not full radial-mode analysis'}
results['EOS']={'gamma_power':gamma,'K_power_cgs':K,'chosen_anchors':'average non-SQM Figure1, (n=.1,P=1) and (n=.5,P=100), P in MeV fm^-3','rho_causality_power_g_cm3':(c*c/(gamma*K))**(1/(gamma-1)),'hybrid_linear_dPdrho_over_c2':A/c**2,'warning':'given hybrid linear transition is acausal, even though high branch P=rho c^2 saturates the causal limit; power law also fails at high rho'}
(out/'stellar-tov-nse-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
