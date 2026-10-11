#!/usr/bin/env python3
"""Deterministic phase portraits from actual equations, kept separate from proofs."""
import numpy as np
from scipy.integrate import solve_ivp
from nonlinear_check import ROOT,write_csv

def main():
    for i,initial in enumerate([[-.3,.3],[-1,.7],[-2,-.8],[.8,-2.5],[1.8,-3.5],[2.2,-.7],[1.5,-.2],[.2,-.3]]):
        def f(t,q):x,y=q;return [x*(4+y-x*x),y*(x-1)]
        def limit(t,q):return 30-np.linalg.norm(q)
        limit.terminal=True
        sol=solve_ivp(f,[0,8],initial,rtol=1e-10,atol=1e-12,events=limit,max_step=.02,dense_output=True)
        pts=sol.sol(np.linspace(0,sol.t[-1],301)).T
        write_csv(f'fixedpoint-{i}.csv',['x','y'],pts)
    results=[]
    for i,initial in enumerate([[np.pi/3+.18,0],[-np.pi/3-.18,0],[0,5.]]):
        def f(t,q):theta,w=q;return [w,np.sin(theta)*(np.cos(theta)-.5)-w]
        sol=solve_ivp(f,[0,20],initial,rtol=1e-10,atol=1e-12,t_eval=np.linspace(0,20,501),max_step=.03)
        write_csv(f'hoop-{i}.csv',['theta','w'],sol.y.T)
        results.append({'initial_state':initial,'maximum_theta':float(sol.y[0].max()),'minimum_theta':float(sol.y[0].min())})
    import json
    (ROOT/'qa/phase-plot-check.json').write_text(json.dumps({'hoop_b':1,'hoop_gamma':2,'trajectories':results,'high_velocity_crosses_top':bool(results[-1]['maximum_theta']>np.pi)},indent=2)+'\n')
if __name__=='__main__':main()
