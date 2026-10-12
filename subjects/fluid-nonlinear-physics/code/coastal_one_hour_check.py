"""Independent shore transient and spectral checks for the one-hour example."""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import quad
from scipy.special import j0
from extended_physics_checks import coastal

ROOT=Path(__file__).resolve().parents[1]

def main():
    stress=.1;rho=1025.;h=10.;gravity=9.81;f=1e-4;t=3600.
    G=stress/rho;c=np.sqrt(gravity*h);tau=f*t;scale=G/(c*f)
    # At x=0 the Laplace transform is -1/(s^2*sqrt(s^2+1));
    # its causal inverse is the twice-integrated Bessel kernel below.
    dimensionless=-quad(lambda z:(tau-z)*j0(z),0,tau,epsabs=1e-13,epsrel=1e-13)[0]
    complete=scale*dimensionless;secular=-t*G/c;checks=[]
    for Q,dq in [(300.,.04),(600.,.02),(1200.,.01)]:
        field,residual=coastal(0.,tau,Q,dq);height=scale*field[2]
        assert abs(height-complete)<3e-9 and np.max(abs(residual))<1e-12
        checks.append({'q_cutoff':Q,'dq':dq,'shore_height_m':float(height),'difference_from_Bessel_integral_m':float(height-complete)})
    small=1e-3;value=-quad(lambda z:(small-z)*j0(z),0,small)[0]
    assert abs(value/(-small*small/2)-1)<1e-6
    report={'status':'PASS','parameters':{'wind_stress_Pa':stress,'density_kg_m3':rho,'depth_m':h,'g_m_s2':gravity,'f_s_inverse':f,'time_s':t,'ft':tau},'full_transient_shore_height_m':float(complete),'secular_term_shore_height_m':float(secular),'secular_to_complete_ratio':float(secular/complete),'Rossby_radius_m':float(c/f),'independent_formula':'eta(0,t)=-G/(cf)*integral_0^(ft) (ft-z) J0(z) dz','spectral_cross_checks':checks,'early_time_dimensionless_leading_term':'-tau^2/2','interpretation':'At ft=0.36 the secular term is not the actual one-hour water level; use the full transient.','not_observation':True}
    (ROOT/'qa/coastal-one-hour-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Coastal one-hour full transient PASS',complete,flush=True)

if __name__=='__main__':main()
