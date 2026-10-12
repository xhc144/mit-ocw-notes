"""Independent local checks of MIT 22.611J Chap5 formulae.

Standard-library only. These verify algebra and the stated asymptotic models;
they do not solve the full kinetic complex dispersion relation or scan modes.
"""
import cmath
import json
import math
from pathlib import Path


def det3(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
        -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
        +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def cold_example():
    # Frequency is normalized to |Omega_e|. Immobile ions neutralize electrons.
    omega=1.5;Omega=-1.;wp2=.5;theta=math.pi/4
    S=1-wp2/(omega*omega-Omega*Omega)
    D=Omega*wp2/(omega*(omega*omega-Omega*Omega))
    P=1-wp2/(omega*omega)
    R=S+D;L=S-D;s=math.sin(theta);c=math.cos(theta)
    A=S*s*s+P*c*c;B=R*L*s*s+P*S*(1+c*c);C=P*R*L
    F2=(R*L-P*S)**2*s**4+4*P*P*D*D*c*c
    assert abs(F2-(B*B-4*A*C))<1e-15
    rows=[]
    for sign in [-1,1]:
        z=(B+sign*math.sqrt(F2))/(2*A)
        M=[[S-z*c*c,-1j*D,z*s*c],[1j*D,S-z,0],[z*s*c,0,P-z*s*s]]
        E=[1.,-1j*D/(S-z),-z*s*c/(P-z*s*s)]
        ME=[sum(M[i][j]*E[j] for j in range(3)) for i in range(3)]
        assert max(abs(v) for v in ME)<1e-14
        assert abs(det3(M))<1e-14
        ah=1-2*(A-B+C)/(2*A-B+sign*math.sqrt(F2))
        assert abs(z-ah)<1e-14
        rows.append(dict(sign=sign,N_squared=z,det_real=det3(M).real,
            matrix_residual=max(abs(v) for v in ME),
            Ey_over_Ex_imag=E[1].imag,Ez_over_Ex=E[2],
            E_dot_k_direction_real=(s*E[0]+c*E[2]).real))
    # Verify determinant identity at three values away from the roots.
    for z in [-1.,.2,2.]:
        M=[[S-z*c*c,-1j*D,z*s*c],[1j*D,S-z,0],[z*s*c,0,P-z*s*s]]
        assert abs(det3(M)-(A*z*z-B*z+C))<1e-14
    return dict(omega_over_abs_Omega_e=omega,omega_pe_squared_over_Omega_e_squared=wp2,
        theta_deg=45,S=S,D=D,P=P,R=R,L=L,A=A,B=B,C=C,F_squared=F2,branches=rows)


def langmuir_asymptotic_examples():
    rows=[]
    for K in [.15,.2]:
        gamma=-math.sqrt(math.pi/8)*K**-3*math.exp(-1/(2*K*K)-1.5)
        wr=math.sqrt(1+3*K*K)
        rows.append(dict(k_lambda_D=K,omega_r_over_omega_p=wr,
            gamma_over_omega_p=gamma,abs_gamma_over_omega_r=abs(gamma/wr)))
    return rows


def ion_acoustic_truncated_checks():
    # k=1, Te/mi=1, x=k^2 lambda_De^2. omega_pi^2=1/x,
    # omega_pe^2=1/(mu*x). This is the explicitly truncated Eq5.279 model.
    # Its real root and derivative are exact within this truncated model.
    mu=1/1836.;rows=[]
    for tau,x in [(.01,.01),(.05,.01)]:
        wp_i2=1/x;wp_e2=wp_i2/mu
        y=(1+math.sqrt(1+12*tau*(1+x)))/(2*(1+x))
        wr=math.sqrt(y)
        eps=lambda w:1+1/x-wp_i2/(w*w)*(1+3*tau/(w*w))
        derivative=wp_i2/wr**3*(2+12*tau/y)
        h=wr*1e-5
        derivative_fd=(eps(wr+h)-eps(wr-h))/(2*h)
        derivative_printed_5289=wp_i2/wr**3*(2+16*tau/y)
        def Fprime(v,sigma):
            return -v/(math.sqrt(2*math.pi)*sigma**3)*math.exp(-v*v/(2*sigma*sigma))
        ei_e=-math.pi*wp_e2*Fprime(wr,1/math.sqrt(mu))
        ei_i=-math.pi*wp_i2*Fprime(wr,math.sqrt(tau))
        gamma_e=-ei_e/(wr*derivative)
        gamma_i=-ei_i/(wr*derivative)
        compact=-math.sqrt(math.pi/2)*y**1.5/(2+12*tau/y)*(math.sqrt(mu)*math.exp(-mu*y/2)
            +tau**-1.5*math.exp(-y/(2*tau)))
        y_source_5283=(1+3*tau)/(1+x)
        y_pade=3*tau+1/(1+x)
        assert abs(eps(wr))<1e-12
        assert abs(derivative_fd/derivative-1)<1e-9
        assert abs(compact-(gamma_e+gamma_i))<1e-14
        assert abs(y_pade-y_source_5283-3*tau*x/(1+x))<1e-14
        assert abs(derivative_printed_5289/derivative-1)>.01
        rows.append(dict(Ti_over_Te=tau,k_lambda_De_squared=x,mass_ratio_e_i=mu,
            y_phase_speed_squared_in_Te_mi=y,epsilon_r_root_residual=eps(wr),
            epsilon_r_derivative=derivative,epsilon_r_derivative_finite_difference=derivative_fd,
            derivative_printed_5289=derivative_printed_5289,
            derivative_printed_relative_error=derivative_printed_5289/derivative-1,
            gamma_e_over_omega_r=gamma_e,gamma_i_over_omega_r=gamma_i,
            gamma_total_over_omega_r=compact,
            y_source_5283=y_source_5283,y_from_pade_5282=y_pade,
            full_kinetic_complex_root_solved=False))
    return rows


if __name__=='__main__':
    result=dict(cold_arbitrary_angle=cold_example(),langmuir_weak_asymptotic=langmuir_asymptotic_examples(),
        ion_acoustic_explicit_truncated_model=ion_acoustic_truncated_checks())
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
