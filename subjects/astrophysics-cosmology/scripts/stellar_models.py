"""Numerical demonstrations for public 8.901 problems, explicit idealized models.

numpy/scipy required; no network, original textbook, image, or unlicensed table.
Run with --out DIRECTORY. Constants and model limits accompany the manuscript.
"""
from pathlib import Path
import argparse, json, math
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
from scipy.special import logsumexp

parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True)
args=parser.parse_args();out=args.out;out.mkdir(parents=True,exist_ok=True)
G=6.67430e-11;c=299792458.;h=6.62607015e-34;hb=h/(2*math.pi);k=1.380649e-23
mp=1.67262192369e-27;me=9.1093837139e-31;mu=1.66053906660e-27
Ms=1.98847e30;Ls=3.828e26;Rs=6.957e8;pc=3.085677581491367e16
yr=365.25*86400;day=86400;ev=1.602176634e-19
results={}
def save(name,arr,header):np.savetxt(out/name,arr,delimiter=',',header=header,comments='')

# Earth/Moon: NASA fact sheet constants; mandated uniform-sphere moment of inertia.
Me=5.9722e24;Mm=7.346e22;Re=6378.137e3;a0=3.84e8
mt=Me+Mm;mured=Me*Mm/mt;I=.4*Me*Re**2;Om=math.sqrt(G*mt/a0**3)
w=2*math.pi/(23.9345*3600);alpha=mured*a0*a0/I;j=1+w/(alpha*Om)
eps=lambda s:-1/s+alpha*(j-math.sqrt(s))**2
d_eps=lambda s:1/s**2-alpha*(j-math.sqrt(s))/math.sqrt(s)
roots=[brentq(d_eps,.001,.5,xtol=1e-14),brentq(d_eps,.5,5,xtol=1e-14)]
Eunit=G*Me*Mm/(2*a0);loss=Eunit*(eps(1)-eps(roots[1]))
ocean_fraction=.7;dissipation_fraction=.03
power=2/day*(ocean_fraction*4*math.pi*Re**2*1000*9.81)*dissipation_fraction
save('stellar-tide.csv',[(s,eps(s)) for s in np.geomspace(.015,3,400)],'s,epsilon')
results['tidal']={'alpha':alpha,'j':j,'s_extrema':roots,'a_extrema_km':[s*a0/1000 for s in roots],
 'period_days':[2*math.pi/Om*s**1.5/day for s in roots],
 'omega_matches_orbit_max_relative_error':max(abs(alpha*(j-math.sqrt(s))*s**1.5-1) for s in roots),
 'energy_loss_J':loss,'ocean_fraction_extra_assumption':ocean_fraction,
 'heat_fraction_extra_assumption':dissipation_fraction,'power_W':power,'time_yr':loss/power/yr,
 'finite_check_s_extrema':[float(d_eps(s)) for s in roots]}
assert results['tidal']['omega_matches_orbit_max_relative_error']<1e-9

stars=['EG And','Z And','T CrB','BF Cyg','V1329 Cyg','CI Cyg','AG Dra','V443 Her','BX Mon','RS Oph','V2116 Oph','AG Peg','AX Per','FG Ser','V343 Ser']
period=np.array([482.6,759,227.6,757.2,956.5,853.8,548.7,599.4,1259,455.7,1042,818.2,682.1,633.5,450.5])
K=np.array([7.3,6.7,23.9,6.7,7.8,6.7,5.9,2.5,4.6,16.7,16,5.4,7.8,6.9,2.7])
f=period*day*(K*1000)**3/(2*math.pi*G*Ms);fmax=.56**3/(1.5+.56)**2
mins=[brentq(lambda m:m**3/(1.5+m)**2-fv,.00001,20) for fv in f]
results['binary']={'f_max_typical':fmax,'individual':[{'name':n,'f_solar':float(fv),'minimum_M2_solar_M1_1p5':m} for n,fv,m in zip(stars,f,mins)],'outliers':[n for n,fv in zip(stars,f) if fv>fmax]}
fs=np.sort(f);save('stellar-binary-cdf.csv',np.c_[fs,np.arange(15)/15,(np.arange(15)+1)/15],'f_solar,CDF_strict,CDF_right')
grid=np.linspace(0,float(max(f)*1.05),400);cdf=1-np.sqrt(1-np.minimum(grid/fmax,1)**(2/3));save('stellar-binary-expected.csv',np.c_[grid,cdf],'f_solar,CDF')
N=(2.5/(math.log(10)*.02))**2;sky_ratio=10**(.4*(24-22.5))*math.pi*.5**2
Phi0=3631e-26/h*math.log(4850/3950);A=math.pi*.5**2
results['photon_count']={'N_no_sky':N,'sky_to_source_ratio':sky_ratio,'N_with_known_background':N*(1+sky_ratio),'explicit_AB_tophat_3950_4850A_zero_flux_photons_m2_s':Phi0,'t20_1m_s':N/(A*Phi0*1e-8),'t24_1m_s':N*(1+sky_ratio)/(A*Phi0*10**(-.4*24)),'t24_4m_s':N*(1+sky_ratio)/(16*A*Phi0*10**(-.4*24))}
results['historical']={'earth_radius_km':5000*.160/math.radians(7),'sun_moon_distance_ratio':1/math.sin(math.pi*(35/1440)/29.53),'lunar_image':'HTTP403; no numerical shadow ratio invented'}

# Helium Saha equation: the chosen allowed density is 10^-6 g/cm^3.
rho_si=1e-3;nHe=rho_si/(4*mu)
def helium(T):
 base=(2*math.pi*me*k*T/h**2)**1.5
 logS0=math.log(4*base)-24.6*ev/(k*T);logS1=math.log(base)-54.4*ev/(k*T)
 def fr(logne):
  w=np.array([0.,logS0-logne,logS0+logS1-2*logne]);return np.exp(w-logsumexp(w))
 def balance(logne):
  a=fr(logne);return math.exp(logne)/nHe-a[1]-2*a[2]
 ln=brentq(balance,math.log(nHe)-70,math.log(2*nHe));a=fr(ln)
 assert abs(math.exp(ln)/nHe-a[1]-2*a[2])<1e-9
 return [T,*a,float(a[1]+2*a[2])]
save('stellar-helium-saha.csv',[helium(T) for T in np.linspace(40000,200000,500)],'T_K,He0,He1,He2,e_per_He')
results['helium']={'density_g_cm3':1e-6,'state_fractions_at_100k':helium(1e5),'electron_balance_checked_all_500':True,'half_neutral_T_K':brentq(lambda T:helium(T)[1]-.5,10000,50000),'half_doubly_ionized_T_K':brentq(lambda T:helium(T)[3]-.5,10000,200000)}

# Lane--Emden six actual solutions; source's noninteger power stops at first zero.
lane_data=[]
for n in [1.,1.5,2.,2.5,3.,3.5]:
 def fun(x,y):return [y[1],-2*y[1]/x-max(y[0],0.)**n]
 def stop(x,y):return y[0]
 stop.terminal=True;stop.direction=-1
 sol=solve_ivp(fun,[1e-5,30],[1-1e-10/6+n*1e-20/120,-1e-5/3+n*1e-15/30],events=stop,method='DOP853',rtol=2e-11,atol=2e-13,max_step=.025,dense_output=True)
 assert sol.t_events[0].size==1
 x1=sol.t[-1];v=sol.y[1,-1];xs=np.linspace(1e-5,x1,500);theta=np.maximum(sol.sol(xs)[0],0)
 save('stellar-lane-n'+str(n).replace('.','p')+'.csv',np.c_[xs,theta,theta**n],'xi,theta,rho_over_central')
 row={'n':n,'xi1':x1,'minus_xi2_theta_prime':-x1*x1*v,'rho_c_over_mean':x1/(-3*v),'central_pressure_factor':1/(4*math.pi*(n+1)*v*v)}
 if n==1:
  err=max(abs(sol.sol(xs)[0]-np.sin(xs)/xs));assert err<1e-9;row['analytic_n1_max_error']=err
 lane_data.append(row)
results['lane_emden']=lane_data

atomic={'H1':1.00782503223,'H2':2.01410177812,'He4':4.00260325413,'C12':12.,'O16':15.99491461957,'Mg24':23.985041697,'F19':18.99840316273,'N15':15.00010889888}
uc2=mu*c*c/(1e6*ev);e_u=me/mu
results['nuclear_Q_MeV']={'12C12C_Mg':(24-atomic['Mg24'])*uc2,'12C12C_O2He':(24-atomic['O16']-2*atomic['He4'])*uc2,'19Fp_OHe':(atomic['F19']+atomic['H1']-atomic['O16']-atomic['He4'])*uc2,'pp_DeNu':(2*atomic['H1']-atomic['H2']-2*e_u)*uc2,'15Np_CHe':(atomic['N15']+atomic['H1']-12-atomic['He4'])*uc2}
results['coulomb']={'speed_density_ratio_10rms_to_rms':100*math.exp(-148.5),'solar_proton_count_pure_H':Ms/mp,'Gamow_coefficient_keV':2*math.pi*(1/137.035999084)*math.sqrt(mu*c*c/(2*1e3*ev))}
assert abs(results['coulomb']['Gamow_coefficient_keV']-31.28)<.02

# Red-giant empirical core relations, ideal helium flash with fixed density/Y.
xi=.1;xf=.45;core_C=2e5*Ls/(.007*c*c*Ms)
t_end=(xi**(-5)-xf**(-5))/(5*core_C)
ts=np.linspace(0,t_end,500);x=(xi**-5-5*core_C*ts)**(-1/5);L=2e5*x**6;R=3700*x**4;T=5772*(L/R**2)**.25
save('stellar-giant-evolution.csv',np.c_[ts/yr,x,L,R,T],'t_yr,Mcore_solar,L_solar,R_solar,Teff_K')
results['giant']={'time_0p1_to_0p45core_yr':t_end/yr,'initial':{'L_solar':L[0],'R_solar':R[0],'T_K':T[0]},'final':{'L_solar':L[-1],'R_solar':R[-1],'T_K':T[-1]}}
rho=2e5;xfermi=(rho/2e6)**(1/3);T0=1.5e8;Tcrit=(rho/1e-8)**(2/3)
def heating(T):T9=T/1e9;return 5.1e8*rho*rho/T9**3*math.exp(-4.4027/T9)
cvion=3*k/(4*mp)*1e4;cv_correct=3*k/(8*mp)*1e4
def cv(T,ionic):return 1.35e5*T*xfermi*math.sqrt(1+xfermi*xfermi)/rho+ionic
def flash_time(T,ionic):return quad(lambda tt:cv(tt,ionic)/heating(tt),T0,T,epsabs=1e-7,epsrel=1e-10)[0]
Ts=np.geomspace(T0,Tcrit,400)
save('stellar-helium-flash.csv',[(tt,flash_time(tt,cvion),flash_time(tt,cv_correct),heating(tt)) for tt in Ts],'T_K,t_printed_s,t_ideal_ion_s,epsilon_erg_g_s')
results['helium_flash']={'fixed_rho_g_cm3':rho,'T_degeneracy_criterion_K':Tcrit,'time_to_criterion_printed_s':flash_time(Tcrit,cvion),'time_to_criterion_corrected_ionic_s':flash_time(Tcrit,cv_correct),'time_to_double_T_printed_s':flash_time(2*T0,cvion),'ionic_cv_printed_erg_g_K':cvion,'ionic_cv_monatomic_erg_g_K':cv_correct}

# Binary white dwarf data, explicit Mestel-envelope and white-dwarf clock models.
par=.201;a_arc=6.89;P=247.9;ratio=.37
a_au=a_arc/par;Mtot=a_au**3/P**2;Mb=Mtot/(1+ratio);Mc=Mtot-Mb
lum=10**(-.4*(9.6-4.74));rsolar=math.sqrt(lum)*(5772/16900)**2;rhobar=3*Mc*Ms/(4*math.pi*(rsolar*Rs)**3)/1000
results['eri_BC']={'distance_pc':1/par,'a_AU':a_au,'total_M_solar':Mtot,'B_M_solar':Mb,'C_M_solar':Mc,'B_L_solar_Mbolsun4p74':lum,'B_R_solar':rsolar,'B_mean_rho_g_cm3':3*Mb*Ms/(4*math.pi*(rsolar*Rs)**3)/1000,'note':'B is white dwarf; C companion. Ratio aB/aC=M_C/M_B=0.37.'}
assert abs(Mc/Mb-ratio)<1e-12
Gcg=G*1e3;ccg=c*100;kcg=k*1e7;hbcg=hb*1e7;mpcg=mp*1e3;mucg=mu*1e3;mecg=me*1e3
M=.6*Ms*1e3;R=.012*Rs*100;rh=3*M/(4*math.pi*R**3);ionA=12;Z=6
e2=(1/137.035999084)*hbcg*ccg # Gaussian cgs, erg cm
rws=(3*ionA*mpcg/(4*math.pi*rh))**(1/3);Tc=Z**2*e2/(160*rws*kcg)
muenv=1/(.75*.9+.5*.1);kappa0=4.34e24*.1+3.68e22*.9
Knr=(3*math.pi**2)**(2/3)*hbcg**2/(5*mecg*(2*mpcg)**(5/3))
arad=4*(2*math.pi**5*kcg**4/(15*(h*1e7)**3*ccg**2))/ccg
Lcr=64*math.pi*arad*ccg*Gcg*M*(muenv*mpcg)**4*Knr**3/(51*kappa0*kcg**4)*Tc**3.5
latent=M/(ionA*mpcg)*kcg*Tc
results['WD_crystallization_explicit_envelope']={'rho_mean_g_cm3':rh,'ion_spacing_cm':rws,'Tc_K':Tc,'Kramers_opacity_coefficient_extra_assumption':kappa0,'mu_envelope':muenv,'L_solar':Lcr/(Ls*1e7),'latent_cooling_yr':latent/Lcr/yr,'model':'Mestel Kramers envelope matched at ideal/electron-degeneracy pressure equality; temperature gradient and boundary approximations, not unique source-given luminosity'}
def wdclock(lum):return 8.8e6*(12/12)**(-1)*.6**(5/7)*(12/2)**(-2/7)*lum**(-5/7)
progen=8.;logm=math.log10(progen);mainlife=10**(9.921-3.6648*logm+1.9697*logm**2-.9369*logm**3)
Lhalo=.012**2*(4000/5772)**4
results['WD_age_source_A_mu_12']={'disk_L_solar':10**(-4.4),'disk_cooling_yr':wdclock(10**(-4.4)),'halo_L_solar_R0p012':Lhalo,'halo_cooling_yr':wdclock(Lhalo),'assumed_minimum_progenitor_lifetime_M8_yr':mainlife,'note':'follow given A=mu=12; mu is source clock parameter, not silently replaced by envelope mean molecular weight'}

# Source-specified winds; gamma domain is kept explicit.
for Lscl in [1e5,3e5,1e6,2e6]:
 masses=np.geomspace(1,150,400);vs=math.sqrt(2*G*Ms/Rs)/1000/2.6*np.sqrt(masses)
 mom=10**(-1.37+2.07*math.log10(Lscl/1e6));mdot0=mom/vs
 Gamma=.03*(Lscl*Ls)/(4*math.pi*G*masses*Ms*c)
 mdotg=np.full(len(masses),np.nan);good=Gamma<1;mdotg[good]=mdot0[good]/np.sqrt(1-Gamma[good])
 save('stellar-wind-L'+str(int(Lscl))+'.csv',np.c_[masses,mdot0,mdotg,Gamma],'M_solar,Mdot_no_Gamma,Mdot_Gamma,Gamma')
Lg=7000;Tg=3000;Rg=math.sqrt(Lg)*(5772/Tg)**2;R_fixed=310.;tt=(1-.6**2)/(8e-13*Lg*R_fixed)
ts=np.linspace(0,tt,300);mass=np.sqrt(1-8e-13*Lg*R_fixed*ts)
save('stellar-reimers.csv',np.c_[ts/1e5,mass],'t_1e5yr,M_solar')
results['reimers_eta1_fixed_L_T']={'R_solar_from_part_a':Rg,'R_solar_fixed_for_parts_c_d':R_fixed,'time_M1_to_M0p6_yr':tt}

# Collapse energetics, neutron-star spin and dispersion, quadrupole application.
M=1.2*Ms
ri=(3*M/(4*math.pi*1e12))**(1/3);rf=(3*M/(4*math.pi*1e18))**(1/3)
release=3*G*M*M/5*(1/rf-1/ri)
results['core_collapse_uniform']={'R_initial_km':ri/1000,'R_final_km':rf/1000,'released_erg':release*1e7}
Pmin=2*math.pi*math.sqrt((10000.)**3/(G*1.4*Ms));q=.25
# constant volume, Re-Rp=(5/4)q Rm; slow-rotation expression is extrapolated.
flatten=5*q/4;Req=brentq(lambda rr:rr**2*(rr-flatten)-1,1,2);Rp=Req-flatten
results['rotation_NS']={'Pmin_ms':Pmin*1000,'P_2Pmin_ms':2*Pmin*1000,'q_rotation':q,'Re_over_Rmean':Req,'Rp_over_Rmean':Rp,'Re_over_Rp':Req/Rp,'warning':'q=0.25 is outside controlled slow-rotation regime'}
e2=(1/137.035999084)*(hb*1e7)*(c*100);DM=10.;delay=e2/(2*math.pi*(me*1e3)*(c*100)*(400e6)**2)*DM*(pc*100)
results['plasma_delay_DM10_400MHz_s']=delay
M=1.4*Ms;Porb=7.75*3600;chirp=2**(-1/5)*M
Pdot=-192*math.pi/5*(2*math.pi*G*chirp/(c**3*Porb))**(5/3)
ecc=.617;eccfac=(1+73*ecc**2/24+37*ecc**4/96)/(1-ecc**2)**3.5
results['GW_equal_mass_circular_7p75hr']={'M_each_solar':1.4,'Pdot':Pdot,'eccentricity_example':ecc,'Peters_enhancement_example':eccfac,'Pdot_with_that_enhancement':Pdot*eccfac,'not_a_full_Hulse_Taylor_fit':True}
magcoef=(1e30**2/(1e-8*Ms*1e3/yr*math.sqrt(Gcg*Ms*1e3)))**(2/7)
results['magnetosphere_coefficient_etaOmega1_cm']=magcoef

results['checks']={'n1_Lane_Emden_against_analytic':True,'helium_charge_balance':True,'tide_synchronous_roots':True,'all_calculations_executed':True,'mathematical_QA_scope':'named models only; not a general stellar-evolution simulation'}
(out/'stellar-model-results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(results,indent=2,ensure_ascii=False))
