"""Reproducible finite checks and vector-plot tables for the expanded course."""
from pathlib import Path
import csv,json,math
import numpy as np
from scipy.integrate import quad
from scipy.special import beta,betainc,gamma
import sympy as sp
root=Path(__file__).resolve().parents[1];qa=root/'qa'
I0=math.sqrt(math.pi)*gamma(.75)/gamma(.25)
I0_quad=quad(lambda u:u*u/math.sqrt(1-u**4),0,1,epsabs=1e-11)[0]
coeff=2*I0**2/math.pi;coeff_gamma=4*math.pi**2/gamma(.25)**4
assert abs(I0-I0_quad)<1e-9 and abs(coeff-coeff_gamma)<1e-13
with (qa/'wilson-profile.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['x_over_L','z_over_L'])
 u=np.linspace(0,1,151)
 points=[(-.5*betainc(.5,.75,1-v**4),v/(2*I0)) for v in u]
 points +=[(.5*betainc(.5,.75,1-v**4),v/(2*I0)) for v in u[::-1]][1:]
 w.writerows(points)
# An independently integrated Feynman-parameter simplex for the d=4, Delta=4 three-point integral.
def inner(v,u):
 a=u;b=(1-u)*v;cc=(1-u)*(1-v);Q=a*b+b*cc+4*cc*a
 if Q==0:return 0.
 return (1-u)*a**3*b**3*cc**3/Q**6
simplex=quad(lambda u:quad(lambda v:inner(v,u),0,1,epsabs=2e-11)[0],0,1,epsabs=2e-11)[0]
I3_integrated=360/math.pi**4*simplex;I3_closed=3/(16*math.pi**4)
assert abs(I3_integrated/I3_closed-1)<2e-7
z,r,d,Delta=sp.symbols('z r d Delta',positive=True)
K=(z/(z*z+r*r))**Delta
res=sp.diff(K,z,2)+(1-d)/z*sp.diff(K,z)+sp.diff(K,r,2)+(d-1)/r*sp.diff(K,r)-Delta*(Delta-d)/z**2*K
res=sp.simplify(res);assert res==0
with (qa/'hawking-page.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['a','TR','F_normalized'])
 for a in np.linspace(.18,2.,240):w.writerow([a,(4*a*a+2)/(4*math.pi*a),a*a*(1-a*a)])
q=.5;low_T_beta=1.0;high_T_beta=.5
out={'wilson_zero_temperature':{'I0_beta':float(I0),'I0_direct_quad':float(I0_quad),'potential_coefficient':float(coeff),'coefficient_gamma_identity':float(coeff_gamma),'turning_point_zstar_over_L':float(1/(2*I0))},'three_point_d4_Delta4_points_minus1_0_1':{'simplex_integral':simplex,'bulk_integral_feynman_parameters':I3_integrated,'closed_Gamma_integral':I3_closed,'relative_error':I3_integrated/I3_closed-1},'scalar_bulk_boundary_kernel_PDE_symbolic_residual':str(res),'Hawking_Page_d4':{'a_minimum_temperature':1/math.sqrt(2),'TR_min':math.sqrt(2)/math.pi,'TR_transition':3/(2*math.pi),'F_at_a1':0,'entropy_strong_free_ratio':.75},'gauge_projected_two_matrix_oscillators':{'critical_beta':math.log(2),'first_holonomy_coefficient_at_beta1':1-2*math.exp(-low_T_beta),'first_holonomy_coefficient_at_beta0p5':1-2*math.exp(-high_T_beta),'unprojected_logZ_over_N2_at_beta1':-2*math.log(1-math.exp(-low_T_beta))},'scope':'One symbolic kernel identity plus stated finite integral/scale examples. This is not independent expert review or verification of every course conclusion.'}
(qa/'holography-course-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
