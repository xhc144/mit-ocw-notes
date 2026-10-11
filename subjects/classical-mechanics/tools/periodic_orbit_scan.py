#!/usr/bin/env python3
"""Bracketed shooting and local periodic-island numerical evidence."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from periodic_orbit_check import flow,T
from nonlinear_check import ROOT,write_csv
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
found=[]
for a in [.3,.6,1.,1.4,1.7]:
 qs=np.linspace(-np.pi,np.pi,241);y=np.column_stack([qs,np.zeros_like(qs)]);dt=(T/2)/768
 def f(t,y):return np.column_stack([y[:,1],-np.sin(y[:,0])-a*np.cos(.7*t)])
 for k in range(768):
  t=k*dt;k1=f(t,y);k2=f(t+dt/2,y+dt*k1/2);k3=f(t+dt/2,y+dt*k2/2);k4=f(t+dt,y+dt*k3);y+=dt*(k1+2*k2+2*k3+k4)/6
 def terminal(q):
  def ff(t,z):return [z[1],-np.sin(z[0])-a*np.cos(.7*t)]
  return solve_ivp(ff,[0,T/2],[q,0],rtol=1e-10,atol=1e-12,max_step=T/120).y[1,-1]
 for j in range(len(qs)-1):
  if y[j,1]*y[j+1,1]<0:
   q=brentq(terminal,qs[j],qs[j+1],xtol=1e-12);z=flow([q,0],a).y[:,-1];M=z[2:].reshape(2,2)
   r={'a':a,'initial_state':[q,0.],'closure_error':float(np.linalg.norm(z[:2]-[q,0])),'monodromy_trace':float(np.trace(M)),'monodromy_determinant':float(np.linalg.det(M)),'elliptic':bool(abs(np.trace(M))<2),'method':'zero velocity at t=0 and T/2 by bracketed shooting, forcing time-reversal symmetry'}
   found.append(r)
report={'all_attempts_converged':found,'claim':'local periodic-orbit and linear-stability numerical evidence; not an attracting periodic window or global chaos threshold'}
pick=next((r for r in found if r['elliptic']),None)
if pick:
 a=pick['a'];q=np.array(pick['initial_state']);report['selected']=pick
 pts=flow(q,a,True).sol(np.linspace(0,T,401))[:2].T;write_csv('pendulum-periodic-orbit.csv',['theta','w'],pts)
 def ff(t,z):return [z[1],-np.sin(z[0])-a*np.cos(.7*t)]
 ts=np.arange(181)*T;sol=solve_ivp(ff,[0,ts[-1]],q+[.002,0],t_eval=ts,rtol=1e-11,atol=1e-13,max_step=T/100);pts=sol.y.T;pts[:,0]=(pts[:,0]+np.pi)%(2*np.pi)-np.pi
 write_csv('pendulum-periodic-island.csv',['theta','w'],pts)
(ROOT/'qa/periodic-orbit-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'selected':pick,'roots':len(found)},indent=2))
