#!/usr/bin/env python3
"""Run numeric examples; these checks supplement, never replace, general derivations."""
import hashlib,json,math,pathlib,platform
ROOT=pathlib.Path(__file__).resolve().parents[1]
def bisect(f,a,b):
    fa=f(a)
    for _ in range(100):
        c=(a+b)/2;fc=f(c)
        if fa*fc<=0:b=c
        else:a=c;fa=fc
    return (a+b)/2
kb=1.380649e-23
hydrogen={str(T):4*math.exp(-10.2/(8.617333262e-5*T)) for T in (300,1000)}
a=1.381e-16;mp=1.67e-24;R=1.2e-13;T=4e7
threshold=(4.8e-10)**2/R;y=threshold/(a*T)
prob=2/math.sqrt(math.pi)*math.sqrt(y)*math.exp(-y)
speed=math.sqrt(8*a*T/(math.pi*mp));cross=math.pi*(2*R)**2;n=100/mp
freepath=1/(n*cross);tau=freepath/speed;total=2e33/mp
hbar=1.054571817e-27
fields={label:hbar*hbar*(6*math.pi**2*den)**(2/3)/(4*mass*abs(mu))/1e4 for label,mass,mu,den in [('copper',9.11e-28,-9.27e-21,8.45e22),('helium3',5.01e-24,1.075e-23,1.64e22)]}
def omega(t):return t+math.sin(t)
def g(t):return 2*t+math.sin(t)+t*math.cos(t)
fold=bisect(lambda t:2+2*math.cos(t)-t*math.sin(t),1,2.5)
critical=bisect(lambda t:t*t*(1+math.cos(t))-math.pi*(g(t)-math.pi),.5,1.6)
nc=1/g(critical)
rotor=[]
for u in (.1,.03,.01,.003):
    # Terms beyond this cutoff are exponentially small; actual direct state sum.
    cutoff=math.ceil(math.sqrt(60/u))+5
    exact=math.fsum((2*l+1)*math.exp(-u*l*(l+1)) for l in range(cutoff+1))
    approx=1/u+1/3+u/15
    rotor.append({'u':u,'cutoff_l':cutoff,'direct_Z':exact,'approx_Z':approx,'difference':exact-approx,'difference_over_u2':(exact-approx)/u**2})
raman={}
for species,theta,even_weight,odd_weight in [('N2',2.9,6,3),('Cl2',.35,6,10)]:
    envelope_peak=(math.sqrt(2*300/theta)-1)/2
    cutoff=math.ceil(envelope_peak)+4
    # The continuous unweighted envelope decreases for L > envelope_peak.
    # Beyond the cutoff both parity branches therefore keep decreasing.
    intensities=[(even_weight if l%2==0 else odd_weight)*(2*l+1)*math.exp(-l*(l+1)*theta/300)for l in range(cutoff+1)]
    peak=max(range(cutoff+1),key=intensities.__getitem__)
    parity_peaks={str(parity):max(range(parity,cutoff+1,2),key=intensities.__getitem__)for parity in (0,1)}
    raman[species]={'temperature_K':300,'rotational_temperature_K':theta,'spin_weights_even_odd':[even_weight,odd_weight],'unweighted_continuous_envelope_peak_L':envelope_peak,'enumerated_L_max':cutoff,'weighted_peak_L':peak,'stokes_line_index_from_L0':peak+1,'parity_peak_L':parity_peaks,'weighted_intensities_unnormalized':{str(l):intensities[l]for l in range(max(0,peak-2),min(cutoff,peak+2)+1)},'model':'Original OCW population model; common normalization and scattering matrix element variation omitted. Rayleigh and anti-Stokes lines excluded from this index.','cutoff_justification':'Derivative of envelope is negative beyond L*, so every later member of either fixed-weight parity branch decreases.'}
record={'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'python':platform.python_version(),'method':'IEEE double arithmetic, bisection 100 iterations, direct convergent spectral sum','limitations':'Numeric evaluations and model-specific root checks; no replacement for general proofs or rigorous finite-size/critical limits.','macro_energy_relative_std':math.sqrt(2/(3*2.69e19)),'hydrogen_level_ratio':hydrogen,'helium_cooling_T0_K':1/(2+15*128/(64*15)),'classical_star':{'threshold_erg':threshold,'threshold_over_kT':y,'log10_tail_approx':math.log10(prob),'tail_approx':prob,'speed_cm_s':speed,'cross_section_cm2':cross,'freepath_cm':freepath,'mean_time_s':tau,'fusion_wait_s':tau/prob,'pair_events_s':total*prob/(2*tau),'participant_events_s':total*prob/tau,'tail_asymptotic_relative_error_scale':1/(2*y)},'noise':{'capacitor_microvolt':math.sqrt(kb*300/1e-10)*1e6,'inductor_nanoamp':math.sqrt(kb*300/1e-3)*1e9,'power_10MHz_W':kb*300*1e7},'complete_polarization_T':fields,'helium_solubility':{'n3_cm-3':(2*1e-23*.5e-16/1e-54)**1.5/(3*math.pi**2),'fraction':((2*1e-23*.5e-16/1e-54)**1.5/(3*math.pi**2))/(2e22+(2*1e-23*.5e-16/1e-54)**1.5/(3*math.pi**2))},'rod_model':{'theta_fold':fold,'n_fold_l2':1/g(fold),'theta_critical':critical,'n_critical_l2':nc,'stationary_residual':nc*g(critical)-1,'entropy_difference_at_critical':math.log(critical*(1-nc*omega(critical)))-math.log(math.pi*(1-nc*math.pi))},'rotor_asymptotic':rotor}
record['weighted_rotational_raman']=raman
(ROOT/'qa/numerical-reproduction.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False,indent=2))
