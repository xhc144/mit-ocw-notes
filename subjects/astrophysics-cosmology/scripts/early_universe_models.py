"""Executed numerical models for public MIT 8.286 PS2, PS6 and PS8--10.

No original source PDFs/images are redistributed. PS8.5 reads the actual
OCW Perlmutter factual table supplied separately; it does not substitute SNLS.
"""
from pathlib import Path
import argparse,hashlib,json,re,math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import zeta
p=argparse.ArgumentParser()
p.add_argument('--out',type=Path,required=True)
p.add_argument('--perlmutter-text',type=Path,required=True)
a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
c=299792458.;G=6.67430e-11;hbar=1.054571817e-34;kB=1.380649e-23
eV=1.602176634e-19;Mpc=3.085677581491367e22;year=31557600.
T0=2.725;H0=67.3*1000/Mpc
def E(z,m,v,r=0,k=None):
 if k is None:k=1-m-v-r
 return np.sqrt(m*(1+z)**3+v+r*(1+z)**4+k*(1+z)**2)
def chi(z,m,v,r=0):
 return quad(lambda x:1/E(x,m,v,r),0,z,epsabs=2e-12,epsrel=2e-12)[0]
def dl_dimensionless(z,m,v):
 k=1-m-v;I=chi(z,m,v)
 DM=I if abs(k)<1e-12 else (math.sinh(math.sqrt(k)*I)/math.sqrt(k) if k>0 else math.sin(math.sqrt(-k)*I)/math.sqrt(-k))
 return (1+z)*DM
def radiation_density(energy,g):
 return g*math.pi**2*energy**4/(30*hbar**3*c**5)
def radiation_time(energy,g):
 return math.sqrt(3/(32*math.pi*G*radiation_density(energy,g)))
result={}
z=8.55;rp=2*c/(67*1000/Mpc)*(1-(1+z)**-.5)
result['PS2']=dict(z=z,H0_km_s_Mpc=67,te_over_t0=(1+z)**-1.5,present_distance_Mpc=rp/Mpc,present_distance_ly=rp/(c*year),recession_over_c=2*(1-(1+z)**-.5))
result['PS6_extra_neutrino']={str(g):dict(g=g,t_s=radiation_time(1e6*eV,g),rho_g_cm3=radiation_density(1e6*eV,g)/1000) for g in [10.75,12.5]}
# Scale-cancelled conformal integrals; use x=a/a0 to control the early endpoint.
def horizon(m,v,r,k):
 return quad(lambda x:1/np.sqrt(r+m*x+k*x*x+v*x**4),0,1,epsabs=2e-12,epsrel=2e-12)[0]
def age(m,v,r,k):
 return quad(lambda x:x/np.sqrt(r+m*x+k*x*x+v*x**4),0,1,epsabs=2e-12,epsrel=2e-12)[0]
causal={}
for r in [0.,9.2e-5]:
 m=.315;v=.685;k=1-m-v-r;eta=horizon(m,v,r,k)
 root=brentq(lambda z:chi(z,m,v,r)-eta/2,2,5,xtol=2e-12)
 # An independent forward/backward equality at the solved reflection event.
 outbound=quad(lambda x:1/np.sqrt(r+m*x+k*x*x+v*x**4),0,1/(1+root),epsabs=2e-12)[0]
 inbound=chi(root,m,v,r);assert abs(outbound-inbound)<1e-9
 causal[str(r)]=dict(Om=m,Ov=v,Or=r,Ok=k,eta0_H0=eta,redshift=root,outbound_minus_inbound=outbound-inbound)
result['PS8_causal']=causal
# Table requested to five significant figures, in SI seconds squared/metres squared.
rows=[]
for z in np.arange(.1,1.50001,.1):
 d=dl_dimensionless(float(z),.3,.7)
 rows.append([z,1/(4*np.pi*c*c*d*d)])
np.savetxt(a.out/'early-flux-table.csv',rows,delimiter=',',header='z,J_over_P_H0_squared_SI',comments='')
result['PS8_flux_units']='J/(P H0^2) in s^2 m^-2; multiply by c^2 for dimensionless version'
# Actual 60-point historical table; parse every row, keep no original page images.
raw=a.perlmutter_text.read_text()
records=[]
for line in raw.splitlines():
 m=re.fullmatch(r'\s*(19\d{2}[A-Za-z]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s*',line)
 if m:records.append((m[1],*[float(m[i]) for i in range(2,6)]))
assert len(records)==60,len(records)
data=np.array([r[1:] for r in records])
z,dz,mag,dmag=data.T
# Assignment asks a plot, not a publication-quality reanalysis of selected fit C.
# All tabulated points retained; profile only the nuisance magnitude zero point.
models=[(1.,0.,'EdS'),(.3,0.,'open'),(.3,.7,'flatLambda')]
fits=[]
grid=np.geomspace(.008,3,360);curves=[grid]
for m,v,name in models:
 base=np.array([5*math.log10(dl_dimensionless(float(x),m,v)) for x in z])
 weights=dmag**-2
 intercept=float(np.sum(weights*(mag-base))/sum(weights))
 chi2=float(np.sum(((mag-base-intercept)/dmag)**2))
 curves.append(np.array([5*math.log10(dl_dimensionless(float(x),m,v))+intercept for x in grid]))
 fits.append(dict(name=name,Om=m,Ov=v,magnitude_intercept=intercept,chi2_mag_errors_only=chi2))
np.savetxt(a.out/'early-supernova-derived.csv',np.c_[z,dz,mag,dmag],delimiter=',',header='z,z_error,magnitude,magnitude_error',comments='')
np.savetxt(a.out/'early-supernova-curves.csv',np.array(curves).T,delimiter=',',header='z,EdS,open,flatLambda',comments='')
result['PS8_supernova']=dict(rows=60,source_original_pdf_sha256='ab16858edcfd07de636e0e1090e16c8c9852493adf2a1b170b9c5d5c78e97d06',parsed_text_sha256=hashlib.sha256(a.perlmutter_text.read_bytes()).hexdigest(),selection='all 60 tabulated Perlmutter points, no clipping or claimed reproduction of paper fit C',errors='magnitude errors only in illustrative profile fit; redshift error bars shown; not a full observational likelihood',fits=fits)
# Given PS10 values sum to 1.000092, retain the closure curvature explicitly.
m=.315;v=.685;r=9.2e-5;k=1-m-v-r
eta=horizon(m,v,r,k);Rp=c/H0*eta;t0=age(m,v,r,k)/H0
gs0=2+(7/8)*6*(4/11)
Efalse=1e16*1e9*eV;rho_false=Efalse**4/(hbar**3*c**5)
Hi=math.sqrt(8*np.pi*G*rho_false/3)
gRH=300.
TRH_energy=(30/(np.pi**2*gRH))**.25*Efalse
aend=(gs0/gRH)**(1/3)*kB*T0/TRH_energy
Zmin=Rp*Hi/c*aend
result['PS10']=dict(Om=m,Ov=v,Or=r,Ok=k,eta0_H0=eta,horizon_Mpc=Rp/Mpc,horizon_ly=Rp/(c*year),age_Gyr=t0/(year*1e9),g_s_today=gs0,E16=1.,gRH=gRH,beta=1.,H_inflation_s_inverse=Hi,reheat_kT_GeV=TRH_energy/(1e9*eV),Zmin=Zmin,Nmin=math.log(Zmin),flat_rounding_alternative_horizon_Mpc=c/H0*horizon(m,1-m-r,r,0)/Mpc)
# Map present observed radius to t=1s; radius and diameter conventions explicit.
Tenergy=math.sqrt(radiation_time(1e6*eV,10.75))*(1e6*eV)
a1=(gs0/10.75)**(1/3)*kB*T0/Tenergy
result['PS9_horizon']=dict(t_s=1.,thermal_kT_MeV=Tenergy/(1e6*eV),a_at_1s=a1,radius_today_m=Rp,mapped_radius_m=Rp*a1,physical_particle_horizon_m=2*c,radius_over_horizon=Rp*a1/(2*c),diameter_over_horizon=Rp*a1/c,post_annihilation_entropy_included=True)
ok=.9
delta=2*ok*H0*1e-37/math.sqrt(9.2e-5)
result['PS9_flatness']=dict(assumed_total_Omega0=.1,assumed_Om0=.1-9.2e-5,Or0=9.2e-5,Ov0=0.,Ok0=ok,H0_km_s_Mpc=67.3,t_s=1e-37,delta=delta,normalization='explicit supplemental present radiation/Hubble parameters; early radiation domination')
# Monopole constant-number-to-photon-ratio approximation specifically requested.
g=200.;TcE=1e16*1e9*eV;tGUT=radiation_time(TcE,g)
nM=(2*c*tGUT)**-3
ngamma=2*zeta(3)/np.pi**2*(TcE/(hbar*c))**3
ratio=nM/ngamma
ngamma0=2*zeta(3)/np.pi**2*(kB*T0/(hbar*c))**3
massM=1e18*1e9*eV/c**2;rhoc=3*H0**2/(8*np.pi*G)
Omega=massM*ratio*ngamma0/rhoc
result['PS9_10_monopole']=dict(g_GUT=g,kTc_GeV=1e16,mass_GeV_c2=1e18,t_GUT_s=tGUT,correlation_length_m=2*c*tGUT,nM_m_inverse3=nM,ngamma_m_inverse3=ngamma,nM_over_ngamma=ratio,photon_density_today_m_inverse3=ngamma0,Omega_same_photon_ratio_as_question=Omega,Omega_with_entropy_dilution=Omega*gs0/g,warning='correlation-length estimate and specified no-annihilation assumption; photons are actually reheated by disappearing thermal species')
# Vacuum-cutoff estimate: lambda_min=lP means kmax=2pi/lP.
lP=math.sqrt(hbar*G/c**3);kmax=2*np.pi/lP
rhoq=hbar*kmax**4/(8*np.pi**2*c)
result['PS9_vacuum']=dict(planck_length_m=lP,rho_cutoff_kg_m3=rhoq,rho_over_critical=rhoq/rhoc,cutoff_convention='wavelength lP, not wave number 1/lP; two photon polarizations; renormalized vacuum not predicted by this raw cutoff')
eps=1e-6
assert abs(2*(1-(1+eps)**-.5)/eps-1)<1e-5
assert np.isfinite(np.array(curves)).all() and np.isfinite(data).all()
def check_finite(x):
 if isinstance(x,float):assert math.isfinite(x),x
 elif isinstance(x,dict):
  for y in x.values():check_finite(y)
 elif isinstance(x,list):
  for y in x:check_finite(y)
check_finite(result)
result['checks']=dict(PS2_small_z_distance_limit=True,causal_integrals_independently_matched=True,source_rows_exactly_60=True,finite_all_outputs=True,scope='named background integrals and historical illustrative data plot; no invented full BBN network or Gadget simulation')
(a.out/'early-universe-model-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
