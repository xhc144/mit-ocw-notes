#!/usr/bin/env python3
"""Refine selected numerical examples and export actual trajectory evidence."""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp
from concurrent.futures import ProcessPoolExecutor
from nonlinear_check import single,write_csv,ROOT

def verify_one(amp):
    pts,r=single('rlc',amp,2/3,discard=900,keep=120)
    return amp,pts,r

def main():
    report=json.loads((ROOT/'qa/nonlinear-numerical-check.json').read_text());cases=report['rlc_scan_case_candidates'];verified=[]
    with ProcessPoolExecutor(max_workers=4) as pool:
        values=list(pool.map(verify_one,cases))
    T=3*np.pi
    for i,(amp,pts,r) in enumerate(values):
        verified.append(r);write_csv(f'rlc-section-{i}.csv',['x','w'],pts)
        def fun(t,y):return [y[1],-y[1]/10-y[0]**3+amp*np.cos((2/3)*t)]
        t0=1020*T;ts=np.linspace(t0,t0+6*T,1801)
        sol=solve_ivp(fun,[ts[0],ts[-1]],pts[-1],t_eval=ts,rtol=2e-10,atol=2e-12,max_step=T/256)
        write_csv(f'rlc-phase-{i}.csv',['x','w'],sol.y.T)
    amp=cases[2]
    def fun(t,y):return [y[1],-y[1]/10-y[0]**3+amp*np.cos((2/3)*t),y[3],-y[3]/10-y[2]**3+amp*np.cos((2/3)*t)]
    ts=np.linspace(0,70*T,1401);sol=solve_ivp(fun,[0,ts[-1]],[.2,0.,.2+1e-8,0.],t_eval=ts,rtol=2e-11,atol=2e-13,max_step=T/256)
    diff=np.linalg.norm(sol.y[:2]-sol.y[2:],axis=0)
    write_csv('rlc-sensitivity.csv',['time','delta'],np.column_stack([ts,diff]));report['rlc_adaptive_cases']=verified;report['rlc_sensitivity']={'B':amp,'initial_difference':1e-8,'final_time':float(ts[-1]),'maximum_state_difference':float(diff.max())}
    # Undamped examples: no asymptotic-attractor classification. Compare local regions.
    data=np.loadtxt(ROOT/'figures/pendulum-wide-diagnostics.csv',delimiter=',',skiprows=1)
    candidates=[]
    for j in range(10,len(data)-10):
        if data[j,1]<.002 and np.any(data[max(0,j-25):j,1]>.03) and np.any(data[j+1:min(len(data),j+26),1]>.03):candidates.append(j)
    amp=float(data[candidates[len(candidates)//2],0]) if candidates else .2
    und=[]
    for a in [amp,.252,.05]:
        pts,r=single('pendulum',a,.7,discard=350,keep=180)
        write_csv(f'pendulum-section-{len(und)}.csv',['theta','w'],pts);und.append(r)
    report['undamped_adaptive_cases']=und
    (ROOT/'qa/nonlinear-numerical-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'rlc':verified,'undamped':und,'sensitivity':report['rlc_sensitivity']},indent=2))
if __name__=='__main__':main()
