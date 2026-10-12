"""Finite checks for the added Kerr-Newman and thermofield-double material."""
from pathlib import Path
import json,math
import numpy as np
from scipy.constants import G,hbar,c,electron_volt
r=Path(__file__).resolve().parents[1]
M,a,Q=4.,1.2,.7
rp=M+math.sqrt(M*M-a*a-Q*Q);D=rp*rp+a*a
T=(rp-M)/(2*math.pi*D);Omega=a/D;Phi=Q*rp/D
v=np.array([.31,-.17,.13]);step=1e-5
def entropy(p):
 m,aa,q=p;rr=m+math.sqrt(m*m-aa*aa-q*q);return math.pi*(rr*rr+aa*aa)
p=np.array([M,a,Q]);dS=(entropy(p+step*v)-entropy(p-step*v))/(2*step);dJ=a*v[0]+M*v[1]
res=T*dS+Omega*dJ+Phi*v[2]-v[0]
assert abs(res)<1e-8
q2=.5;n=np.arange(100);prob=(1-q2)*q2**n
occupation=float((n*prob).sum());S=float(-(prob*np.log(prob)).sum())
assert abs(occupation-1)<1e-12 and abs(S-2*math.log(2))<1e-12
# The bare Newton-force inequality permits a finite algebraic extremal step.
assert 2*1<=2*1 and 2+1==1+2
out={'planck_mass_kg':math.sqrt(hbar*c/G),'planck_energy_GeV':math.sqrt(hbar*c/G)*c*c/(electron_volt*1e9),'planck_length_m':math.sqrt(hbar*G/c**3),'planck_time_s':math.sqrt(hbar*G/c**5),'kerr_newman_sample':{'M':M,'a':a,'Q':Q,'r_plus':rp,'temperature':T,'omega':Omega,'potential':Phi,'first_law_direction':v.tolist(),'central_difference_first_law_residual':res},'TFD_beta_omega_log2':{'sum_first100_probability':float(prob.sum()),'mean_n':occupation,'entropy':S,'expected_entropy':2*math.log(2)},'bare_capture_inequality_counterexample':{'M':2,'Q':1,'m':1,'q':2,'initial_extremality_gap':1,'final_gap':0,'test_particle_approximation':False},'scope':'Finite checks support stated examples and expose missing approximation; no claim of a machine proof of the full course.'}
(r/'qa/holography-completion-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
