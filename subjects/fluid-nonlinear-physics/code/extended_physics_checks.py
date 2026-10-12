"""New derivation checks; earlier independently passed core scripts are unchanged."""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import quad,simpson,solve_ivp
ROOT=Path(__file__).resolve().parents[1]

def coastal(X,tau,Q=600.,dq=.02):
    q=np.linspace(0,Q,round(Q/dq)+1);w=np.sqrt(1+q*q)
    s=X*np.sinc(q*X/np.pi)
    integ=lambda a:2/np.pi*simpson(a,x=q)
    u=1-np.exp(-X)-integ(s*np.cos(w*tau)/(w*w))
    v=tau*np.exp(-X)+integ(s*np.sin(w*tau)/(w**3))
    eta=-tau*np.exp(-X)+integ(np.cos(q*X)*np.sin(w*tau)/(w**3))
    ut=integ(s*np.sin(w*tau)/w)
    ux=np.exp(-X)-integ(np.cos(q*X)*np.cos(w*tau)/(w*w))
    vt=np.exp(-X)+integ(s*np.cos(w*tau)/(w*w))
    et=-np.exp(-X)+integ(np.cos(q*X)*np.cos(w*tau)/(w*w))
    ex=tau*np.exp(-X)-integ(q*np.sin(q*X)*np.sin(w*tau)/(w**3))
    return np.array([u,v,eta]),np.array([et+ux,ut-v+ex,vt+u-1])

def main():
    results={}
    # Unit sphere, mu=U=1: traction integration checks the two fractions.
    pressure=quad(lambda t:3*np.pi*np.cos(t)**2*np.sin(t),0,np.pi)[0]
    shear=quad(lambda t:3*np.pi*np.sin(t)**3,0,np.pi)[0]
    assert abs(pressure-2*np.pi)<1e-12 and abs(shear-4*np.pi)<1e-12
    results['sphere_traction']={'pressure':pressure,'shear':shear,'total':pressure+shear,'analytic_total':6*np.pi}
    f=lambda x:np.tanh(x);fp=lambda x:1/np.cosh(x)**2
    x=np.linspace(-3,3,121);f2=-2*f(x)*fp(x);f3=4*f(x)**2*fp(x)-2*fp(x)**2
    residual=f3+2*(fp(x)**2+f(x)*f2)
    assert np.max(abs(residual))<1e-12
    jetJ=quad(lambda z:1/np.cosh(z)**4,-30,30)[0]
    results['plane_jet']={'ODE_residual':float(np.max(abs(residual))),'sech4_integral':jetJ,'analytic':4/3}
    coag=[]
    for tau in [0.,.1,1.,10.]:
        k=np.arange(1,20001);n=np.zeros(len(k));n[0]=1 if tau==0 else 0
        if tau>0:n=np.exp((k-1)*np.log(tau)-(k+1)*np.log1p(tau))
        assert abs(n.sum()-1/(1+tau))<1e-12 and abs(np.sum(k*n)-1)<1e-12
        coag.append({'tau':tau,'N':float(n.sum()),'mass':float(np.sum(k*n))})
    results['coagulation_constant_kernel']=coag
    # Random physical amplitudes verify all three scaling coefficients.
    nu=.03;kap=.01;H=2.;m=np.pi/H;k=m/np.sqrt(2);q2=k*k+m*m;ga=2.;DT=1.
    aa=k*m/(np.sqrt(2)*kap*q2);bb=aa*ga*k/(nu*q2*q2)
    A=.02;B=.1;C=.03;X,Y,Z=aa*A,bb*B,np.sqrt(2)*bb*C
    actual=np.array([aa*(-nu*q2*A+ga*k*B/q2),bb*(DT/H*k*A-kap*q2*B-k*m*A*C),np.sqrt(2)*bb*(k*m*A*B/2-4*kap*m*m*C)])/(kap*q2)
    sigma=nu/kap;r=ga*k*k*DT/(H*nu*kap*q2**3);b=4*m*m/q2
    standard=np.array([sigma*(Y-X),r*X-Y-X*Z,X*Y-b*Z]);error=float(np.max(abs(actual-standard)));assert error<1e-10
    results['RBC_Lorenz_scaling']={'sigma':sigma,'r':r,'b':b,'residual':error,'temperature_scale_note':'b_s=a_s*g*alpha*k/(nu*q0^4); no extra kappa'}
    # Direct substitution of the original ring dimensional model.
    a=2.;Gamma=3.;K=2.;ga=5.;T1=4.;q=.2;T3=.3;T4=.4
    X=q/(a*K);Y=ga*T3/(2*a*Gamma*K);Z=ga*T4/(2*a*Gamma*K)
    lhs=np.array([(-Gamma*q+ga*T3/2)/(a*K),ga*(-K*T3+q*T1/a-q*T4/a)/(2*a*Gamma*K),ga*(-K*T4+q*T3/a)/(2*a*Gamma*K)])/K
    rhs=np.array([Gamma/K*(Y-X),ga*T1/(2*a*Gamma*K)*X-Y-X*Z,X*Y-Z]);assert np.max(abs(lhs-rhs))<1e-12
    results['original_ring_Lorenz']={'b':1,'residual':float(np.max(abs(lhs-rhs)))}
    coastal_checks=[]
    for X in [0.,.2,1.,2.,4.]:
        v0,_=coastal(X,0.);v,res=coastal(X,4.);coarse,_=coastal(X,4.,300.,.04)
        assert np.max(abs(v0))<3e-5 and np.max(abs(res))<1e-12
        if X==0:assert v[0]==0 and v[1]==4
        coastal_checks.append({'X':X,'initial_residual':float(np.max(abs(v0))),'PDE_residual':float(np.max(abs(res))),'quadrature_difference':float(np.max(abs(v-coarse)))})
    rows=[]
    for X in np.linspace(0,4,81):v,_=coastal(float(X),4.);rows.append([X,*v])
    np.savetxt(ROOT/'data/coastal-step-tau4.csv',rows,delimiter=',',header='X,u,v,eta',comments='')
    results['coastal_step']=coastal_checks
    g=.1/1025;c=np.sqrt(9.81*10);results['coastal_chosen_example']={'wind_Pa':.1,'rho_kg_m3':1025,'h_m':10,'f_s_inverse':1e-4,'Rossby_radius_m':c/1e-4,'one_hour_shore_secular_height_m':-3600*g/c,'not_observation':True}
    periods=[]
    def event(t,y):return y[0]
    event.direction=1;event.terminal=False
    for mu in [10.,20.,40.]:
        sol=solve_ivp(lambda t,y:[y[1],mu*(1-y[0]*y[0])*y[1]-y[0]],(0,12*mu),[2.,0.],method='Radau',rtol=1e-8,atol=1e-10,events=event,max_step=mu/20)
        tt=sol.t_events[0];assert sol.success and len(tt)>=3
        period=float(np.mean(np.diff(tt)[-3:]));leading=mu*(3-2*np.log(2));periods.append({'mu':mu,'period':period,'leading_period':leading,'relative_difference':period/leading-1})
    results['large_mu_van_der_Pol']=periods
    (ROOT/'qa/extended-physics-checks.json').write_text(json.dumps({'status':'PASS','results':results},indent=2));print('Extended physics checks PASS',flush=True)
if __name__=='__main__':main()
