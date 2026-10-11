#!/usr/bin/env python3
"""Reproduce numerical examples and finite checks; no general proof claim."""
import hashlib,json,math,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
e=1.602176634e-19;c=299792458.;g=9.8
eps=8.8541878128e-12
mass=12e9*e/c**2
out=dict(carbon_mass_kg_under_problem_GeV_approximation=mass,
 mass_spectrometer_voltage_V=e*.2**2/(8*mass),
 child_support_B_T=20*g/100,
 child_small_oscillation_Hz=math.sqrt(math.sqrt(2)*g)/(2*math.pi),
 slab_charge_density_C_per_m3=-15*eps,
 numerical_verification_is_not_a_general_proof=True)
# Finite checks of the original black-box calculations, with units kept in manuscript.
out['black_box_1']=dict(R_ohm=10,C_farad=.01,amplitude_A=(100*math.sqrt(2))/math.sqrt(10**2+(1/(10*.01))**2),phase_rad=math.atan2(-1/(10*.01),10))
out['black_box_2']=dict(L_H=2,C_F=.5,reactance_at_omega1_ohm=2-1/.5,reactance_at_omega2_ohm=4-1/(2*.5),power_at_omega1_W=6**2/(2*3))
assert abs(out['black_box_1']['amplitude_A']-10)<1e-12
assert out['black_box_2']['reactance_at_omega1_ohm']==0
out['source_script_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
(R/'qa/numerical-reproduction.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False))
