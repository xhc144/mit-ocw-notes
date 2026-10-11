#!/usr/bin/env python3
"""Search symmetric periodic trajectories while preserving the published initial state."""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[1]
T=2*np.pi/.7

def integrate(a,periods,rtol=2e-11):
    def rhs(t,z):
        q,w=z[:2];M=z[2:].reshape(2,2)
        A=np.array([[0.,1.],[-np.cos(q),0.]])
        return np.r_[w,-np.sin(q)-a*np.cos(.7*t),(A@M).ravel()]
    return solve_ivp(rhs,[0,periods*T],np.r_[.2,0.,np.eye(2).ravel()],rtol=rtol,atol=rtol/100,max_step=T/120,method='DOP853')

def main():
    records=[]
    for period in [1,2,4]:
        amps=np.linspace(.1,2,601);states=np.tile([.2,0.],(len(amps),1));steps=512*period;dt=(period*T/2)/steps
        def rhs(t,z):return np.column_stack([z[:,1],-np.sin(z[:,0])-amps*np.cos(.7*t)])
        for k in range(steps):
            t=k*dt;k1=rhs(t,states);k2=rhs(t+dt/2,states+dt*k1/2);k3=rhs(t+dt/2,states+dt*k2/2);k4=rhs(t+dt,states+dt*k3)
            states+=dt*(k1+2*k2+2*k3+k4)/6
        brackets=np.flatnonzero(states[:-1,1]*states[1:,1]<0)
        for j in brackets:
            def terminal(a):return integrate(a,period/2).y[1,-1]
            lo,hi=amps[j:j+2]
            if terminal(lo)*terminal(hi)>=0:continue
            a=brentq(terminal,lo,hi,xtol=2e-13)
            sol=integrate(a,period);fine=integrate(a,period,2e-12)
            q,w=sol.y[:2,-1];M=sol.y[2:,-1].reshape(2,2)
            closure=np.linalg.norm([(q-.2+np.pi)%(2*np.pi)-np.pi,w])
            rec={'period_multiple_tested':period,'amplitude':float(a),'initial_state':[.2,0.],
                 'forcing_phase':0.,'closure_error':float(closure),'monodromy_trace':float(np.trace(M)),
                 'monodromy_determinant':float(np.linalg.det(M)),'elliptic_linear_type':bool(abs(np.trace(M))<2),
                 'refinement_state_difference':float(np.linalg.norm(sol.y[:2,-1]-fine.y[:2,-1])),
                 'minimum_period_not_certified':True}
            records.append(rec)
    for rec in records:
        good=rec['closure_error']<1e-8 and abs(rec['monodromy_determinant']-1)<1e-4 and rec['refinement_state_difference']<1e-8
        rec['numerical_quality_passed']=bool(good)
        rec['elliptic_linear_type']=bool(good and abs(rec['monodromy_trace'])<2-1e-5)
        rec['classification']='unreliable_due_to_closure_or_monodromy_conditioning' if not good else ('near_parabolic_unclassified' if abs(abs(rec['monodromy_trace'])-2)<1e-5 else ('elliptic' if rec['elliptic_linear_type'] else 'hyperbolic'))
    report={'initial_state':[.2,0.],'forcing_frequency':.7,'forcing_sign':'negative',
            'search_grid':{'lower':.1,'upper':2.,'points':601,'symmetry_half_periods':[.5,1.,2.]},
            'method':'Vectorized RK4 brackets, independent adaptive DOP853 roots, monodromy and tolerance refinement.',
            'roots':records,'scope':'Isolated tuned amplitudes with a fixed initial state; no claim of an interval of finite-period responses. An undamped elliptic island generally produces quasi-periodic nearby fixed-initial trajectories. Large unstable monodromy matrices lose determinant accuracy through cancellation; failed candidates are retained explicitly as unreliable, not certified.',
            'subpart_a_status':'partial: fixed-initial broad scan supplied; between-chaos periodic window has not been established.'}
    (ROOT/'qa/fixed-initial-period-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'candidates':len(records),'quality_passed':sum(r['numerical_quality_passed'] for r in records),'elliptic':sum(r['elliptic_linear_type'] for r in records)},ensure_ascii=False))

if __name__=='__main__':main()
