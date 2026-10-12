"""Analytic and numerical checks for public MIT 22.615 2007 HW4 problem 3.
This reconstructs only the supplied hard-core Z-pinch problem, not textbook
Problems 8.6/8.7. gamma=2, perfect radial walls, all axial wave numbers.
"""
import json
import numpy as np
from scipy.optimize import minimize_scalar
from midterm_reference import OUT

def A(u):return (u-1)*(u*u-4*u-1)/(u+1)**3
def beta(chi,uw):return chi*uw*(uw-1)/((uw+1)**2*(1+chi*A(uw)))
def P(u):return (u-1)/(u+1)**3
def rPprime(u):return 4*u*(2-u)/(u+1)**4
def B2(u,chi):return (1+chi*A(u))/u
def g0(u,chi):
    # dimensionless numerator of m=0 energy after axial displacement minimization
    pp=2*chi*P(u);b=B2(u,chi)
    return 4*chi*rPprime(u)+8*pp*b/(b+2*pp)
def g1(u,chi):return B2(u,chi)+4*chi*rPprime(u)
def chi0(uw):return (uw+1)**2*(2*uw-1)/((uw-1)**2*(2*uw+1))

def main():
    us=(5+np.sqrt(17))/2
    F=lambda u:u*u*(u-1)/(u+1)**4
    ns=minimize_scalar(lambda u:-F(u),bounds=(2,8),method='bounded',options={'xatol':1e-13})
    ch1=1/(24*F(us)-1)
    result=dict(u_star=float(us),r_star_over_rc=float(np.sqrt(us)),chi1=float(ch1),beta1_infinite=float(ch1/(1+ch1)),chi0_infinite=1.,beta0_infinite=.5,
        independently_optimized_u_star=float(ns.x),profile_form='p=(K/rc^4)*(u-1)/(u+1)^3, u=(r/rc)^2',
        normalization='chi=mu0*K/(2*Bc^2*rc^4), Bc=mu0*Ic/(2*pi*rc)',finite_wall=[])
    for uw in [10,100,1e3,1e4,1e6]:
        c0=chi0(uw);bb0=beta(c0,uw);bb1=beta(ch1,uw)
        exactbb0=(2*uw-1)*(uw+1)/(4*uw*(uw-2))
        assert abs(bb0-exactbb0)<1e-13
        result['finite_wall'].append(dict(rw_over_rc=float(np.sqrt(uw)),uw=uw,chi0=float(c0),beta0=float(bb0),beta1=float(bb1)))
    uu=np.geomspace(1.000001,1e6,2001)
    # Independently test the original local criteria and their reduced expressions.
    reduced1=(1+ch1*(1-24*uu**2*(uu-1)/(uu+1)**4))/uu
    assert np.max(abs(g1(uu,ch1)-reduced1))<1e-14
    assert abs(g1(us,ch1))<1e-14
    assert g1(us,ch1*1.001)<0
    assert g0(1e4,1.01)<0
    assert np.min(g0(uu,1))>-1e-14
    # Force balance: d(u Bhat^2)/du=-2*chi*u*dPhat/du.
    h=1e-4
    zz=np.linspace(1.01,20,400)
    derivative=ch1*(A(zz+h)-A(zz-h))/(2*h)
    expected=-8*ch1*zz*(2-zz)/(zz+1)**4
    result['force_balance_fd_error']=float(np.max(abs(derivative-expected)))
    assert result['force_balance_fd_error']<1e-8
    result['m1_criterion_reduction_error']=float(np.max(abs(g1(uu,ch1)-reduced1)))
    result['m0_at_chi1p01_r100rc']=float(g0(1e4,1.01))
    result['m1_at_critical']=float(g1(us,ch1))
    (OUT/'hw4_ldx_results.json').write_text(json.dumps(result,indent=2))
    np.savetxt(OUT/'hw4_ldx_profiles.csv',np.column_stack([uu,np.sqrt(uu),P(uu),B2(uu,1),g0(uu,1),g1(uu,ch1)]),delimiter=',',header='u,r_over_rc,p_over_P,B2_over_Bc2_at_chi1,g0_at_chi1,g1_at_chi1critical',comments='')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
