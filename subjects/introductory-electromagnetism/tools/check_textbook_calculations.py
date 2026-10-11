#!/usr/bin/env python3
"""Actual finite reproductions; analytical proofs are in the manuscript."""
import hashlib
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parents[1]
eps = 8.8541878128e-12
c = 299792458.0
k = 9e9
e = 1.6e-19  # the frozen hydrogen/oil-drop problem's rounded value

def bisect(f, low, high, iterations=100):
    assert f(low) * f(high) < 0
    for _ in range(iterations):
        mid = (low + high) / 2
        if f(low) * f(mid) <= 0:
            high = mid
        else:
            low = mid
    return (low + high) / 2

out = {'numerical_verification_is_not_a_general_proof': True,
       'constants': {'eps_F_per_m': eps, 'c_m_per_s': c,
                     'rounded_k_N_m2_per_C2': k, 'rounded_e_C': e},
       'units_note': 'Every value uses SI internally unless its name specifies otherwise.'}
a = .02
factor = k * 6e-6 * 3e-6 / a**2
fx = factor * (math.sqrt(2)/4 - 1)
fy = factor * math.sqrt(2)/4
out['2.1'] = {'Fx_N': fx, 'Fy_N': fy, 'F_N': math.hypot(fx, fy),
              'angle_deg': math.degrees(math.atan2(fy, fx))}
fe = k * e**2 / (.53e-10)**2
out['2.13.1'] = {'Fe_N': fe, 'E_N_per_C': fe/e,
                  'official_b_using_other_radius_E_N_per_C': k*e/(.50e-10)**2}
mass = (4/3)*math.pi*(1.64e-6)**3*851
charge = -mass*9.8/1.92e5
out['2.13.2'] = {'mass_kg': mass, 'charge_C': charge, 'charge_over_e': charge/e}
out['5.5'] = {'energy_density_J_per_m3': eps*(3e6)**2/2}
out['6.5.1'] = {'resistance_ohm': 3e-8*3e6/(7*math.pi*(.73e-3/2)**2)}
out['6.5.3'] = {'drift_m_per_s': 6/(.25*e*6e26),
                'drift_cm_per_s': 100*6/(.25*e*6e26)}
def rlc(resistance, inductance, capacitance, peak_v, omega):
    xl = omega*inductance
    xc = 1/(omega*capacitance)
    z = math.hypot(resistance, xl-xc)
    amp = peak_v/z
    return {'XL_ohm': xl, 'XC_ohm': xc, 'Z_ohm': z, 'I0_A': amp,
            'phi_deg': math.degrees(math.atan2(xl-xc,resistance)),
            'VR0_V': amp*resistance, 'VL0_V': amp*xl, 'VC0_V': amp*xc,
            'VLC0_V': amp*abs(xl-xc)}
out['12.9.1'] = rlc(40,.160,100e-6,40,200)
out['12.9.2'] = rlc(40,.080,50e-6,150,100)
omega0 = 1/math.sqrt(.010*100e-9)
out['12.9.3'] = {'omega0_rad_per_s': omega0, 'f0_Hz': omega0/(2*math.pi),
                  'I0_A': 10, 'Q': omega0*.010/20, 'VL0_V': omega0*.010*10}
out['12.9.4'] = {'half_amplitude_frequency_Hz': math.sqrt((25**2-4*10**2)/3)/(.250*2*math.pi)}
out['12.9.6'] = {'R_ohm': 200*.4/math.tan(math.pi/6), 'amplitude_ratio_R': math.cos(math.pi/6),
                  'amplitude_ratio_L': .5}
out['13.1'] = {'E0_V_per_m': math.sqrt(2*1350/(eps*c)),
               'B0_T': math.sqrt(2*1350/(eps*c))/c,
               'solar_power_W': 4*math.pi*(1.5e11)**2*1350}
out['14.1'] = {'path_difference_m': .150e-3*.02/1.2,
               'path_difference_over_lambda': .150e-3*.02/1.2/(833e-9)}
out['14.3'] = {'screen_distance_m': .001*math.sqrt(1-(600e-9/.8e-3)**2)/(600e-9/.8e-3),
               'central_width_m': .002}
out['14.11.1'] = {'max_order_below_45deg': math.floor(.320e-3*math.sin(math.pi/4)/500e-9),
                  'count': 905}
out['14.11.2'] = {'phase_a_rad': 2*math.pi*.100e-3*math.sin(math.radians(.8))/500e-9,
                  'phase_b_rad_small_angle': 2*math.pi*.100e-3*.004/500e-9,
                  'angle_c_deg': math.degrees(math.asin(500e-9/(6*math.pi*.100e-3))),
                  'angle_d_deg': math.degrees(math.asin(500e-9/(4*.100e-3)))}
phase = 2*math.acos(math.sqrt(.6))
out['14.11.4'] = {'minimum_phase_rad': phase, 'path_difference_nm': 500*phase/(2*math.pi)}
beta1 = bisect(lambda b: b*math.cos(b)-math.sin(b), math.pi, 1.5*math.pi)
beta2 = bisect(lambda b: b*math.cos(b)-math.sin(b), 2*math.pi, 2.5*math.pi)
out['14.11.5'] = {'beta1': beta1, 'beta2': beta2,
                  'lambda_midpoint_nm': 2*.8e-3*.0016/(5*.8)*1e9,
                  'lambda_true_maximum_nm': math.pi*.8e-3*.0016/math.hypot(.8,.0016)/beta2*1e9,
                  'beta2_residual': beta2*math.cos(beta2)-math.sin(beta2)}
out['14.11.6'] = [{'order': m, 'angle_deg': math.degrees(math.asin(m*500e-9/2.8e-6)),
                   'relative_intensity': 1 if m==0 else (math.sin(math.pi*m/4)/(math.pi*m/4))**2}
                  for m in range(6)]
assert 8.20e-8 < fe < 8.21e-8
assert abs(beta2*math.cos(beta2)-math.sin(beta2)) < 1e-12
assert out['14.11.1']['max_order_below_45deg'] == 452
# Actual finite circuit checks against the separately derived formulas.
checks = []
for R1,R2,R3,E1,E2 in [(2,3,4,5,7),(1,1,1,1,1),(10,17,8,3,11)]:
    den = R1*R2+R1*R3+R2*R3
    I1=(E1*R3+E2*R3+E2*R2)/den
    I2=-(E1*R1+E1*R3+E2*R3)/den
    I3=(E2*R2-E1*R1)/den
    residuals = [I1+I2-I3,E2-I1*R1-I3*R3,-I2*R2-E1+I1*R1-E2,
                 E2*I1-E1*I2-(R1*I1**2+R2*I2**2+R3*I3**2)]
    assert max(abs(x) for x in residuals) < 1e-10
    checks.append({'parameters': [R1,R2,R3,E1,E2], 'residuals': residuals})
out['7.8_finite_examples_only'] = checks
out['source_script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(root/'qa/textbook-numerical-reproduction.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','numeric_objects':len(out)-4,'beta2':beta2,
                  'lambda_true_maximum_nm':out['14.11.5']['lambda_true_maximum_nm']},ensure_ascii=False))
