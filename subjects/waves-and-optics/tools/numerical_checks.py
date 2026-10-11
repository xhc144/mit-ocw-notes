#!/usr/bin/env python3
"""Reproduce selected numerical examples; these checks are not general proofs."""
import hashlib,json,math,pathlib
import numpy as np
import mpmath as mp
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
    mp.mp.dps=35
    z=float(mp.besseljzero(1,1));D=np.array([[21.,-15.],[-5.,11.5]])
    vals,vecs=np.linalg.eig(D);freqs=sorted(np.sqrt(vals).tolist())
    theta=math.asin(math.sqrt((4-1.33**2)/3));r=math.asin(math.sin(theta)/1.33)
    beta=np.linspace(-7,7,4001);amp=np.exp(1j*beta)+1/math.sqrt(2)+np.exp(-1j*beta)
    intensity=(math.sqrt(2)*np.cos(beta)+.5)**2*2
    errors={'ps2_5_matrix_eigen_residual':float(np.max(np.abs(D@vecs-vecs@np.diag(vals)))),'ps10_2_complex_amplitude_intensity_error':float(np.max(np.abs(abs(amp)**2-intensity)))}
    assert max(errors.values())<1e-12
    values={'ps2_5_frequencies_rad_s':freqs,'sound_speed_m_s':math.sqrt(1.4e5/1.2),'J1_first_positive_zero':z,'circular_aperture_coefficient':z/math.pi,'rainbow_theta_degrees':math.degrees(theta),'rainbow_radius_degrees':math.degrees(4*r-2*theta),'ps9_1_vp_over_c':math.sqrt(2),'ps9_1_vg_over_c':1/math.sqrt(2),'ps10_3_intensity':2+2*math.cos(math.sqrt(3)*math.pi/2)}
    report={'status':'PASS','method':'Python numpy and mpmath actually executed','values':values,'errors':errors,'limitation':'Specific matrices, samples and numeric special-function roots; algebraic arguments remain in the text.','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'chapters').glob('*.tex'))}}
    out=ROOT/'qa/numerical-checks.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(values,ensure_ascii=False))
if __name__=='__main__':main()
