"""Small independent checks for MIT 22.615 Lecture 21/22 theory review.
No old exam scan. No dependencies beyond Python standard library.
"""
import json
import math
from pathlib import Path

MU0=4*math.pi*1e-7

def simpson(f,a,b,n):
    h=(b-a)/n
    return h/3*(f(a)+f(b)+4*sum(f(a+h*j) for j in range(1,n,2))+2*sum(f(a+h*j) for j in range(2,n,2)))

def wire_examples():
    R0=1.;a=.1;I0=1e6
    ell=math.log(8*R0/a)
    L=lambda R:MU0*R*(math.log(8*R/a)-2)
    Lp=MU0*(ell-1);Lpp=MU0/R0
    B0=I0*Lp/(4*math.pi*R0)
    ncrit=1-R0*Lpp/Lp+R0*Lp/(2*L(R0))
    rows=[]
    for nb in [-.5,.5,2.]:
        def U(R,Z):
            if nb==2:
                flux_mid=2*math.pi*B0*R0**2*math.log(R/R0)
            else:
                flux_mid=2*math.pi*B0*R0**nb*(R**(2-nb)-R0**(2-nb))/(2-nb)
            bprime=-nb*B0*R0**nb/R**(nb+1)
            # Local vacuum-field Taylor extension, sufficient for the Hessian:
            # Phi_ext(R,Z)=Phi_ext(R,0)-pi*R*b'(R)*Z^2+O(Z^4).
            flux_ext=flux_mid-math.pi*R*bprime*Z*Z
            I=(L(R0)*I0+flux_ext)/L(R)
            return .5*L(R)*I*I
        KR=.5*I0*I0*(Lpp-Lp*Lp/(2*L(R0))+(nb-1)*Lp/R0)
        KZ=-I0*I0*Lp*nb/(2*R0)
        h=1e-4
        KRfd=-(U(R0+h,0)-2*U(R0,0)+U(R0-h,0))/(h*h)
        KZfd=-(U(R0,h)-2*U(R0,0)+U(R0,-h))/(h*h)
        assert abs(KR-KRfd)/max(1,abs(KR))<2e-6
        assert abs(KZ-KZfd)/max(1,abs(KZ))<2e-6
        rows.append(dict(n_field=nb,KR_N_m=KR,KZ_N_m=KZ,KR_fd_N_m=KRfd,KZ_fd_N_m=KZfd,
            horizontal_stable=KR<0,vertical_stable=KZ<0))
    return dict(R0_m=R0,a_m=a,I_A=I0,L_H=L(R0),Bz_equilibrium_T=B0,n_horizontal_exact=ncrit,
        n_horizontal_leading_log=1.5,examples=rows)

def mercier_circle_examples():
    # x=r/a; q=q0+0.4*x^2, local beta=0.04*(1-x^2).
    rows=[]
    for q0 in [.95,1.05]:
        x=.1;q=q0+.4*x*x;rq_r=.8*x*x;r_beta_r=-.08*x*x
        shear=(rq_r/q)**2
        pressure=4*r_beta_r*(1-q*q)
        rows.append(dict(q0=q0,r_over_a=x,q=q,shear_term=shear,pressure_term=pressure,
            criterion_LHS=shear+pressure,local_interchange_stable=shear+pressure>0))
    assert rows[0]['criterion_LHS']<0<rows[1]['criterion_LHS']
    return rows

def mercier_general_cylinder_examples():
    # Same-coordinate cylindrical limit of the reconstructed general Mercier
    # coefficient. Independently compare with Lecture 18's Suydam coefficient.
    # These are local equilibria, not complete bounded screw-pinch profiles.
    R=3.;r=.5;Bz=2.;Bt=.3;q=r*Bz/(R*Bt);qr=.8
    J=r/Bt;B2=Bz*Bz+Bt*Bt;F=R*Bz
    A=R*R*Bt*Bt/(J*B2)
    kn=-Bt*Bt/(r*B2)
    C=R*Bt*kn/B2
    rows=[]
    for pr in [-1e5,-1.2e5]:
        pp=pr/(R*Bt);qp=qr/(R*Bt)
        Lam=F*(MU0*pp*F-(R*R*Bt*Bt/J)*qp)
        # All chi-dependent coefficients are constant on this cylindrical
        # surface, so Mercier's special weighted mean equals each value.
        covariance=Lam/(B2*B2)-(1/B2)*(Lam/B2)
        Dfull=(MU0*pp/(qp*qp*A*A))*(2*C+covariance)
        Ds=-2*MU0*pr*q*q/(r*Bz*Bz*qr*qr)
        lhs=r*Bz*Bz*(qr/q)**2+8*MU0*pr
        # Construct field derivatives satisfying both the chosen q' and the
        # exact local radial force balance p'+(B^2)'/(2mu0)+Bt^2/(mu0*r)=0.
        d=qr/q-1/r
        ut=(-MU0*pr-Bt*Bt/r-Bz*Bz*d)/B2
        uz=ut+d
        force_residual=MU0*pr+Bt*Bt*(ut+1/r)+Bz*Bz*uz
        qr_reconstructed=q*(1/r+uz-ut)
        assert abs(Dfull-Ds)<1e-12
        assert abs(covariance)<1e-12
        assert abs(force_residual)<1e-12
        assert abs(qr_reconstructed-qr)<1e-12
        assert (Dfull<.25)==(lhs>0)
        rows.append(dict(p_r_Pa_m=pr,p_psi=pp,q_psi=qp,Lambda_M=Lam,
            covariance=covariance,D_general=Dfull,D_Suydam=Ds,
            Suydam_LHS_T2_m=lhs,localized_interchange_pass=Dfull<.25,
            Btheta_log_derivative_m_inv=ut,Bz_log_derivative_m_inv=uz,
            local_force_residual_T2_m=force_residual,q_r_reconstructed_m_inv=qr_reconstructed))
    assert rows[0]['localized_interchange_pass'] and not rows[1]['localized_interchange_pass']
    return dict(R0_m=R,r_m=r,Bz_T=Bz,Btheta_T=Bt,q=q,q_r_m_inv=qr,
        J_m_T=J,A_T_m=A,kappa_n_m_inv=kn,examples=rows)

def ballooning_examples():
    # theta0=0, X=exp(-theta^2/2), admissible at +-infinity.
    rows=[]
    for S,alpha in [(1.,0.),(1.,1.4),(1.,4.)]:
        exact=math.sqrt(math.pi)*(.5+.75*S*S-alpha*math.exp(-.25)*(1+7*S/4)+alpha*alpha*(3-math.exp(-1))/4)
        def density(t):
            X=math.exp(-t*t/2);Xp=-t*X;Lam=S*t-alpha*math.sin(t)
            return (1+Lam*Lam)*Xp*Xp-alpha*(math.cos(t)+Lam*math.sin(t))*X*X
        coarse=simpson(density,-10,10,10000);fine=simpson(density,-10,10,20000)
        assert abs(exact-fine)<1e-12
        rows.append(dict(S=S,alpha=alpha,theta0=0,energy_exact=exact,energy_Simpson_10000=coarse,
            energy_Simpson_20000=fine,negative_trial_proves_instability=exact<0,
            positive_trial_proves_full_stability=False))
    assert rows[1]['energy_exact']<0
    return rows

if __name__=='__main__':
    result=dict(wire=wire_examples(),mercier_circular=mercier_circle_examples(),
        mercier_general_cylindrical=mercier_general_cylinder_examples(),s_alpha_trial=ballooning_examples())
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
