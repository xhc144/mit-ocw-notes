#!/usr/bin/env python3
"""Independent scale/limit checks for the historical supplement; standard library."""
import json,math,pathlib,re,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
E=1.602176634e-19; ME=9.1093837139e-31; MP=1.67262192595e-27
EPS=8.8541878188e-12; K=1.380649e-23; H=6.62607015e-34; MU=4e-7*math.pi
checks={}
def check(name,actual,target,rel=1e-3):
    if not math.isfinite(actual) or abs(actual-target)>rel*max(abs(target),1e-30):raise AssertionError((name,actual,target))
    checks[name]={'computed':actual,'manuscript_target':target,'relative_tolerance':rel}
# 2002 PS1 Saha: state factor g=1 and 50% ionized ideal mixture.
def saha(T):return (2*math.pi*ME*K*T/H**2)**1.5*math.exp(-13.6*E/(K*T))-101325/(3*K*T)
lo,hi=10000.,20000.
for _ in range(100):
    mid=(lo+hi)/2
    if saha(mid)>0:hi=mid
    else:lo=mid
check('2002_ps1_saha_kelvin',(lo+hi)/2,15365.48,1e-4)
# 2002 PS2 Fermi mirrors, using proton and initial equal perpendicular/parallel energy.
v0=math.sqrt(2*500*E/MP);vf=math.sqrt(2*2000*E/MP)
check('2002_ps2_mirror_bounces',(vf-v0)/(2*1e4),15.46,1e-3)
check('2002_ps2_mirror_time_per_metre',math.log(vf/v0)/(2*1e4),3.4657359e-5,1e-5)
# 2002 PS2 C-Mod drifts, Maxwell thermal averages.
T=2000*E;B=4.5;R=.66
check('2002_ps2_EcrossB',1e5/B,22222.22,1e-4)
check('2002_ps2_gradB',T/(E*B*R),674.0,2e-3)
check('2002_ps2_curvature_thermal_average',2*(T/2)/(E*B*R),674.0,2e-3)
# 2002 PS3 free paths with explicitly stated empirical thermal rates.
def freepath(T_eV,n_cm3,ln,mass,coeff):
    return math.sqrt(2*T_eV*E/mass)/(coeff*n_cm3*ln/T_eV**1.5)
check('2002_ps3_electron_tokamak_m',freepath(4000,1e14,17,ME,2.91e-6),1918.24,1e-4)
check('2002_ps3_ion_tokamak_m',freepath(4000,1e14,17,MP,4.80e-8),2713.95,1e-4)
check('2002_ps3_electron_processing_m',freepath(5,5e12,11,ME,2.91e-6),.09264,2e-4)
# 2002 PS3 alpha local slowing rates, re-evaluated from scanned official NRL formula convention.
nu_alpha_e=1.6e-9*(1/4)*10000**(-1.5)*1e14*4*16
check('2002_ps3_alpha_electron_local_s',1/nu_alpha_e,.390625,1e-8)
for mass,target in ((2,15.157176914),(3,19.487798889)):
    nu=9e-8*(1/4+1/mass)*math.sqrt(4)/(3.5e6**1.5)*(1e14/2)*4*16
    check('2002_ps3_alpha_ion_local_s_'+str(mass),1/nu,target,1e-8)
# 2002 PS3 loop voltage and electron-ion-only runaway threshold.
eta=5.2e-5*16/1000**1.5;Ef=eta*4e5/(math.pi*.3**2)
check('2002_ps3_loop_V',2*math.pi*1.2*Ef,.2806,2e-3)
check('2002_ps3_runaway_eV',1e19*E**3*16/(8*math.pi*EPS**2*Ef)/E,56003.,1e-4)
# 2002 PS4 Ampere integral and pressure derivative for specified J_z.
a=.3;I=4e5;c1=2*I/(math.pi*a*a)
def Btheta(r):
    x=(r/a)**2
    return MU*I/(2*math.pi*r)*x*x/(1+x)**2
def pressure(r):
    x=(r/a)**2;u=1/(1+x)
    return MU*c1*c1*a*a/8*(u*u/2-2*u**3/3+u**4/4)
r=.4;h=1e-5
J=c1*(r/a)**2/(1+(r/a)**2)**3
check('2002_ps4_pinch_force_balance',(pressure(r+h)-pressure(r-h))/(2*h),-J*Btheta(r),1e-7)
# 2003 MHD marginal formula and sign both sides of wall.
for kappa in (1.25,2.,3.,5.):
    w=(kappa*kappa+1)/(kappa*math.sqrt(kappa*kappa-1))
    u1=math.asinh(1/math.sqrt(kappa*kappa-1))
    u2=math.acosh(w*kappa/math.sqrt(kappa*kappa-1))
    check('2003_MHD_marginal_kappa_'+str(kappa),1/math.tanh(u2-u1),kappa,1e-12)
check('2003_MHD_w_kappa_2',5/(2*math.sqrt(3)),1.443375673,1e-9)
# Count only actual new exercise environments; MHD steps are one comprehensive group.
expected={'historical-2005.tex':7,'historical-2005-exams.tex':2,'historical-2002-ps1-2.tex':7,'historical-2002-ps3-4.tex':6,'historical-2002-ps5-6.tex':8,'historical-2002-ps7-8.tex':6,'historical-2002-mid.tex':6,'historical-2002-final.tex':6,'historical-2003-mhd-exam.tex':5}
for fn,n in expected.items():
    s=(ROOT/'chapters'/fn).read_text()
    actual=s.count('\\begin{exercise}')
    if actual!=n:raise AssertionError((fn,actual,n))
checks['new_original_numbered_exercises']=sum(expected.values())
checks['new_comprehensive_groups']=9+39+1
checks['total_comprehensive_groups']=60+checks['new_comprehensive_groups']
checks['historical_freeze_sha256']=hashlib.sha256((ROOT/'qa/historical-supplement-freeze.json').read_bytes()).hexdigest()
out=ROOT/'qa/historical-revision-numerical-checks.json';out.write_text(json.dumps({'status':'PASS','checks':checks},ensure_ascii=False,indent=2)+'\n')
print(out)
