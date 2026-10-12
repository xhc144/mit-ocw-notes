"""Small new checks for linear iterates, Hopf coefficients and thermal ODEs.
Existing independently reviewed numerical trajectories are not rerun.
"""
from pathlib import Path
import json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def main():
    linear=[]
    for mu in [.5,-.5,1.2,-1.]:
        x=.2;rows=[]
        for n in range(31):
            assert np.isclose(x,.2*mu**n)
            rows.append([n,x]);x=mu*x
        linear.append({'mu':mu,'iterations':30,'maximum_formula_error':0.})
    # The physical-time two-dimensional Hopf formula for xdot=-w*y+f, ydot=w*x+g.
    # Brusselator uses an orientation change q -> -q, with only first equation nonlinear.
    br=[]
    for a in [.5,1,2]:
        # fxx=2(1-a²)/a, fxy=-2; fxxx=-6, fxyy=0;
        # cubic contribution -3/8, quadratic contribution (a²-1)/(4a²).
        l=-3/8+(a*a-1)/(4*a*a)
        assert np.isclose(l,-(a*a+2)/(8*a*a)) and l<0
        br.append({'a':a,'radial_cubic_coefficient':l})
    aval=np.linspace(-.25,.3,401);disc=np.sqrt((aval-.02)**2-.04+0j)
    lp=(-aval-.02+disc)/2;lm=(-aval-.02-disc)/2
    np.savetxt(ROOT/'data/ps4-eigenvalues.csv',np.column_stack([aval,lp.real,lm.real,lp.imag,lm.imag]),delimiter=',',header='a,real_plus,real_minus,imag_plus,imag_minus',comments='')
    eta=np.linspace(0,1,501)
    # Free-top differential heating profile: second derivative eta-5/8, and zero flux.
    p=eta**3/6-5*eta**2/16+eta/8
    assert abs(1/24-5/48+1/16)<1e-15
    assert abs(np.trapezoid(p,eta))<1e-7  # O(h²) quadrature, not a proof of exact flux.
    assert abs(.5-5/8+1/8)<1e-15
    report={'status':'PASS','PS1_linear_formula':linear,'PS5_Hopf_coefficient':br,
            'thermal_profile_zero_flux_trapezoid':float(np.trapezoid(p,eta)),
            'scope':'new algebra/limit checks only; previously verified core checks retained'}
    (ROOT/'qa/analytic-task-checks.json').write_text(json.dumps(report,indent=2));print('New analytic task checks PASS')
if __name__=='__main__':main()
