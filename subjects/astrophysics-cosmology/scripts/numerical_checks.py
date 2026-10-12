"""Reproduce the numerical examples. Requires numpy and scipy; no external data."""
from pathlib import Path
import json, math
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq
base=Path(__file__).resolve().parents[1]
G=6.67430e-11;c=299792458.;h=6.62607015e-34;k=1.380649e-23
mp=1.67262192369e-27;me=9.1093837139e-31;hb=h/(2*math.pi)
Ms=1.98847e30;Ls=3.828e26;Rs=6.957e8;pc=3.085677581491367e16;yr=365.25*86400
H0=71000/(1e6*pc);om=.3;ol=.7
E=lambda z:math.sqrt(om*(1+z)**3+ol)
chi=lambda z:c/H0*quad(lambda zz:1/E(zz),0,z,epsabs=1e-8)[0]/(1e6*pc)
out={}
out['planck']={'sigma_cgs':2*math.pi**5*k**4/(15*h**3*c**2)*1e3,'lambda_peak_T_cmK':h*c/(k*brentq(lambda x:5*(-math.expm1(-x))-x,1,8))*100,'nu_peak_over_T':k/h*brentq(lambda x:3*(-math.expm1(-x))-x,1,5)}
temps=[]
for rho in np.logspace(-10,-2,81):
 n=rho*1000/mp
 S=lambda t:(2*math.pi*me*k*t/h**2)**1.5*math.exp(-13.6*1.602176634e-19/(k*t))
 temp=brentq(lambda t:S(t)-n/2,1000,1e6);temps.append((rho,temp))
np.savetxt(base/'qa/saha-half-ionization.csv',temps,delimiter=',',header='rho_g_cm3,T_K',comments='')
out['saha_endpoints']=temps[0],temps[-1]
def lane(n):
 def fun(x,y):return [y[1],-2*y[1]/x-max(y[0],0.)**n]
 def stop(x,y):return y[0]
 stop.terminal=True;stop.direction=-1
 sol=solve_ivp(fun,[1e-6,12],[1-1e-12/6,-1e-6/3],events=stop,rtol=2e-11,atol=1e-12,max_step=.01)
 x=sol.t[-1];theta,der=sol.y[:,-1];return x,-x*x*der
out['lane_emden']={str(n):lane(n) for n in [1.5,3.]}
for n in [1.5,3.]:
 mu=2;rhoc=1e9
 K=(3*math.pi**2)**(2/3)*hb**2/(5*me*(mu*mp)**(5/3)) if n==1.5 else (3*math.pi**2)**(1/3)*hb*c/(4*(mu*mp)**(4/3))
 alpha=math.sqrt((n+1)*K*rhoc**(1/n-1)/(4*math.pi*G));x,w=out['lane_emden'][str(n)]
 out[f'white_dwarf_n{n}']={'R_km':alpha*x/1000,'M_solar':4*math.pi*alpha**3*rhoc*w/Ms}
out['main_sequence']=[{'M_solar':m,'T_K':10**lt,'L_solar':10**ll,'R_solar':math.sqrt(10**ll)*(5772/10**lt)**2,'lifetime_yr_X0.7':.007*f*.7*m*Ms*c*c/(10**ll*Ls)/yr} for m,lt,ll,f in [(.085,3.438,-3.297,1),(90,4.722,6.045,.1)]]
out['oort']={'v_km_s':8.5*(14.82+12.37),'dv_dR_km_s_kpc':-(14.82-12.37),'kappa_km_s_kpc':math.sqrt(4*12.37*(14.82+12.37)),'kappa_over_Omega':math.sqrt(4*12.37/(14.82+12.37)),'orbit_Myr':2*math.pi*1000*pc/(27190)/yr/1e6}
z1=4711/1206-1;z2=4836/1206-1
out['absorption']={'z1':z1,'z2':z2,'delta_chi_Mpc':chi(z2)-chi(z1),'relative_z':(1+z2)/(1+z1)-1,'sigma_Mpc2_at_z2':2*H0*E(2)/(0.001*9)*1e6*pc/c}
rad=8.5e-5
ER=lambda z:math.sqrt(rad*(1+z)**4+om*(1+z)**3+ol)
rho0=om*3*H0*H0/(8*math.pi*G)
def horizon(z):
 ac=1/(1+z)
 com=c/H0*quad(lambda a:1/math.sqrt(rad+om*a+ol*a**4),0,ac)[0]
 return com/(1+z),com
zrec=1100;zeq=om/rad-1;Drec=c/H0*quad(lambda z:1/ER(z),0,zrec)[0]
out['baby_pictures_assumptions']={'z_rec':zrec,'Omega_r':rad,'galaxy_mass_solar':1e12}
rg=(3*1e12*Ms/(4*math.pi*rho0))**(1/3)
out['baby_pictures']={'galaxy_diameter_arcmin':2*rg/Drec*180/math.pi*60,'200_comoving_Mpc_degrees':200e6*pc/Drec*180/math.pi,'mass_matter_within_particle_horizon_rec_solar':4*math.pi/3*rho0*horizon(zrec)[1]**3/Ms,'mass_matter_within_particle_horizon_eq_solar':4*math.pi/3*rho0*horizon(zeq)[1]**3/Ms}
t=13.7e9*yr;r=700000*pc;v=-121000
eta=brentq(lambda eta:math.sin(eta)*(eta-math.sin(eta))/(1-math.cos(eta))**2-v*t/r,math.pi+.01,2*math.pi-.01)
mass=r**3*(eta-math.sin(eta))**2/(G*t*t*(1-math.cos(eta))**3)
out['timing']={'eta':eta,'M_solar':mass/Ms,'M_over_L_solar':mass/Ms/3e10,'MW_radius_kpc_v220':G*(mass/2)/(220000**2)/(1000*pc)}
z=8;rho_bg=3*H0**2/(8*math.pi*G)*om*(1+z)**3;rho_ta=9*math.pi**2/16*rho_bg
tff=math.sqrt(3*math.pi/(32*G*rho_ta));rho_vir=8*rho_ta
Rvir=(3*1e12*Ms/(4*math.pi*rho_vir))**(1/3);T=mp*G*1e12*Ms/(5*k*Rvir)
nb=.05*rho_vir/mp;cool=3*k*T/(nb*1e-36)
out['top_hat_pure_H_convention']={'t_ff_Myr':tff/yr/1e6,'R_vir_kpc_M1e12':Rvir/(1000*pc),'T_K_M1e12':T,'t_cool_Myr_M1e12':cool/yr/1e6,'M_max_solar':1e12*(tff/cool)**1.5}
out['cloud_T150_n1e8_molecular_mu2']={}
rho=1e14*2*mp;cs=math.sqrt(k*150/(2*mp));RJ=.5*cs*math.sqrt(math.pi/(G*rho));MJ=4*math.pi/3*rho*RJ**3
out['cloud_T150_n1e8_molecular_mu2']={'R_J_AU':RJ/1.495978707e11,'M_J_solar':MJ/Ms,'P_gradient_Pa_m':rho*cs*cs/RJ,'gravity_force_density_N_m3':G*MJ*rho/RJ**2,'gravity_energy_density_J_m3':3*G*MJ*MJ/(5*RJ)/(4*math.pi/3*RJ**3),'magnetic_energy_density_J_m3_B10microG':(1e-9)**2/(2*4*math.pi*1e-7)}
r0=.5*pc;rf=100*1.495978707e11;omega=math.sqrt(2*G*Ms*rf)/r0**2;vf=.8*omega*r0*r0/rf
out['rotation_cloud']={'omega0_s-1':omega,'v0_cm_s':omega*r0*100,'vf_km_s':vf/1000,'period_years':2*math.pi*rf/vf/yr,'Kepler_period_years':2*math.pi*math.sqrt(rf**3/(G*Ms))/yr}
rp=brentq(lambda r:math.log(r)+.125/r**2-.125,.05,.9)
T_rad=2*quad(lambda th:(1-rp)*math.sin(2*th)/math.sqrt(max(2*(.125-math.log(rp+(1-rp)*math.sin(th)**2)-.125/(rp+(1-rp)*math.sin(th)**2)**2),1e-30)),0,math.pi/2,epsabs=1e-8)[0]
def orbitfun(t,q):
 x,y,vx,vy=q;rr=x*x+y*y;return [vx,vy,-x/rr,-y/rr]
sol=solve_ivp(orbitfun,[0,75*T_rad],[1,0,0,.5],method='DOP853',rtol=1e-11,atol=1e-12,max_step=T_rad/150,dense_output=True)
ts=np.arange(0,75*T_rad,T_rad/50);q=sol.sol(ts).T
np.savetxt(base/'qa/logarithmic-orbit.csv',np.c_[ts,q],delimiter=',',header='t,x,y,vx,vy',comments='')
out['logarithmic_orbit']={'r_pericenter':rp,'radial_period':T_rad,'radial_periods':75,'sample_count':len(ts),'max_energy_error':float(np.max(np.abs(np.sum(q[:,2:]**2,axis=1)/2+np.log(np.linalg.norm(q[:,:2],axis=1))-.125))),'max_angular_momentum_error':float(np.max(np.abs(q[:,0]*q[:,3]-q[:,1]*q[:,2]-.5)))}
event=c/H0*quad(lambda a:1/math.sqrt(om*a+ol*a**4),1,np.inf)[0]/(1e6*pc)
out['present_event_horizon']={'Mpc':event,'redshift_of_current_horizon_location':brentq(lambda z:chi(z)-event,0,10)}
(base/'qa/numerical-results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
print(json.dumps(out,indent=2,ensure_ascii=False))
