"""Declared numerical estimates for the actual exp11/13/48/51 preparation tasks.
These are model calculations, not apparatus observations.
"""
from pathlib import Path
import json
import numpy as np
from scipy import constants as c
ROOT=Path(__file__).resolve().parents[1]
def main():
    hEv=c.h/c.e;kEv=c.k/c.e;muB=c.physical_constants['Bohr magneton in eV/T'][0]
    mass=57*c.atomic_mass;E=14400*c.e
    # Rationalized relativistic expression avoids subtracting two large energies.
    recoil=E*E/(np.sqrt((mass*c.c*c.c)**2+E*E)+mass*c.c*c.c)/c.e
    width=c.hbar/c.e*np.log(2)/9.8e-8
    cavity=[]
    for n,L in [(3.5,250e-6),(1.,.02)]:
        cavity.append({'n':n,'L_m':L,'spacing_GHz':c.c/(2*n*L)/1e9,'spacing_nm':(780e-9)**2/(2*n*L)/1e-9})
    land=[]
    for I,gI in [(2.5,-.0002936400),(1.5,-.0009951414)]:
        for F in [I+.5,I-.5]:
            cj=(F*(F+1)+.75-I*(I+1))/(2*F*(F+1));ci=1-cj
            g=2*cj+gI*ci
            land.append({'I':I,'F':F,'nuclear_angular_projection_fraction':ci,'nuclear_gI_in_Bohr_units':gI,'gF_with_gJ2':g,'nuclear_magnetic_projection_fraction':gI*ci/g})
    a=1e-6;eta=1e-3;rho=1000;v=20e-6;tau=2*rho*a*a/(9*eta)
    report={'status':'PASS','kind':'declared analytical model estimates, no physical observations',
      'rubidium':{'D2_eV':c.h*c.c/780e-9/c.e,'fine_eV':c.h*c.c*(1/780e-9-1/794.8e-9)/c.e,
      'Rb85_ground_hfs_eV':hEv*3.035732e9,'Rb85_adjacent_1gauss_eV':muB*1e-4/3,
      'P12_population_per_mole_320K':c.N_A*np.exp(-c.h*c.c/794.8e-9/c.e/(kEv*320)),
      'F3_extreme_population_difference_per_mole_Rb85':c.N_A/12*2*muB*1e-4/(kEv*320),'lande':land},
      'mossbauer':{'recoil_eV':recoil,'crystal_mass_kg':1e-9,'crystal_recoil_eV':(E/c.c)**2/(2e-9)/c.e,'natural_FWHM_eV':width,'one_width_speed_m_s':c.c*width/14400,'input_half_life_s':9.8e-8},
      'spectroscopy':{'GHz_per_nm_at780':-c.c/(780e-9)**2*1e-18,'cavity':cavity},
      'bacterium_sphere':{'a_m':a,'speed_m_s':v,'tau_m_s':tau,'coast_distance_m':v*tau,'initial_drag_pN':6*np.pi*eta*a*v*1e12},
      'ideal_Boston_dipole_inclination_deg':float(np.degrees(np.arctan(2*np.tan(np.radians(42.4)))))}
    assert .0019<recoil<.0020 and 9e-5<report['mossbauer']['one_width_speed_m_s']<1.1e-4
    (ROOT/'qa/prelab-checks.json').write_text(json.dumps(report,indent=2));print('Public prelab estimates PASS')
if __name__=='__main__':main()
