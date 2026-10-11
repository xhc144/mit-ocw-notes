#!/usr/bin/env python3
"""Ideal rigid-beam course project simulation; not a construction specification."""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import differential_evolution
G=9.81
M1,M2=30.,1.
def parameters(lengths):
 l1,l2,ls=lengths;mb=.1*np.sqrt(M1)*(l1+l2);c=(l2-l1)/2;ib=mb*(l1+l2)**2/12
 A=M1*l1*l1+M2*l2*l2+ib+mb*c*c;B=M2*ls*ls;C=M2*l2*ls;D=G*(M1*l1-M2*l2-mb*c);Ds=M2*G*ls
 return l1,l2,ls,mb,c,ib,A,B,C,D,Ds

def simulate(lengths):
 l1,l2,ls,mb,c,ib,A,B,C,D,Ds=parameters(lengths)
 def fun(t,y):
  b,s,bd,sd=y;co=np.cos(b-s);si=np.sin(b-s)
  bdd,sdd=np.linalg.solve([[A,-C*co],[-C*co,B]],[C*si*sd*sd-D*np.sin(b),-C*si*bd*bd-Ds*np.sin(s)])
  return [bd,sd,bdd,sdd]
 def vel(y):
  b,s,bd,sd=y;return np.array([-l2*np.cos(b)*bd+ls*np.cos(s)*sd,-l2*np.sin(b)*bd+ls*np.sin(s)*sd])
 def event(t,y):return vel(y)[1]-vel(y)[0]
 event.direction=-1;event.terminal=False
 sol=solve_ivp(fun,[0,8],[3*np.pi/4,np.pi/2,0,0],rtol=2e-9,atol=1e-10,events=event,max_step=.012)
 candidates=[]
 for t,y in zip(sol.t_events[0],sol.y_events[0]):
  if t<1e-5:continue
  v=vel(y)
  if v[0]<=0 or v[1]<=0:continue
  before=sol.y[:,sol.t<=t];tens=[]
  for ti,yi in zip(sol.t[sol.t<=t],before.T):
   b,s,bd,sd=yi;bdd=fun(ti,yi)[2];tens.append(M2*(G*np.cos(s)-l2*np.sin(b-s)*bdd-l2*np.cos(b-s)*bd*bd+ls*sd*sd))
  if min(tens)<-1e-6:continue
  U0=D*(1-np.cos(3*np.pi/4))+Ds
  if U0<=0:continue
  ke=M2*np.dot(v,v)/2
  candidates.append((ke/U0,t,y,v,min(tens),U0))
 if not candidates:return None
 best=max(candidates,key=lambda x:x[0]);eff,t,y,v,tmin,U0=best
 b,s,bd,sd=sol.y
 energy=.5*A*bd**2+.5*B*sd**2-C*np.cos(b-s)*bd*sd-D*np.cos(b)-Ds*np.cos(s)
 return {'lengths_m':list(map(float,lengths)),'beam_mass_kg':float(mb),'release_time_s':float(t),'release_state':y.tolist(),'velocity_m_s':v.tolist(),'speed_m_s':float(np.linalg.norm(v)),'energy_efficiency_including_projectile_potential':float(eff),'U0_J':float(U0),'minimum_sling_tension_before_release_N':float(tmin),'max_absolute_energy_error_J':float(np.max(np.abs(energy-energy[0]))),'energy_error_interval_s':8,'model':'massless taut sling, fixed pivot, no dissipation; initial angles 3pi/4 and pi/2, rest','claim':'feasible numerical candidate within stated search bounds; no global optimality claim'}
if __name__=='__main__':
 # Freeze a reproducible candidate; bounded optimization used only when explicitly requested.
 result=simulate([1.,4.,5.])
 if result is None:
  bounds=[(.5,1.5),(1.,6.),(1.,7.)]
  def objective(x):
   r=simulate(x);return 2 if r is None else -r['energy_efficiency_including_projectile_potential']
  opt=differential_evolution(objective,bounds,maxiter=8,popsize=4,seed=223,workers=1,polish=False)
  result=simulate(opt.x);result['search_bounds_m']=bounds
 out=Path(__file__).resolve().parents[1]/'qa/project-numerical-check.json'
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))

def export_course_plot():
 from scipy.integrate import solve_ivp
 r=json.loads((Path(__file__).resolve().parents[1]/'qa/project-numerical-check.json').read_text())
 l1,l2,ls,mb,c,ib,A,B,C,D,Ds=parameters(r['lengths_m']);tf=r['release_time_s']
 def fun(t,y):
  b,s,bd,sd=y;co=np.cos(b-s);si=np.sin(b-s)
  bdd,sdd=np.linalg.solve([[A,-C*co],[-C*co,B]],[C*si*sd*sd-D*np.sin(b),-C*si*bd*bd-Ds*np.sin(s)])
  return [bd,sd,bdd,sdd]
 ts=np.linspace(0,tf,151)
 sol=solve_ivp(fun,[0,tf],[3*np.pi/4,np.pi/2,0,0],t_eval=ts,rtol=2e-11,atol=1e-12,max_step=.006)
 b,s,bd,sd=sol.y;vx=-l2*np.cos(b)*bd+ls*np.cos(s)*sd;vy=-l2*np.sin(b)*bd+ls*np.sin(s)*sd
 x=-l2*np.sin(b)+ls*np.sin(s);y=l2*np.cos(b)-ls*np.cos(s);ep=.5*M2*(vx*vx+vy*vy)
 total=.5*A*bd**2+.5*B*sd**2-C*np.cos(b-s)*bd*sd-D*np.cos(b)-Ds*np.cos(s)
 x1=l1*np.sin(b);y1=-l1*np.cos(b);e1=.5*M1*l1*l1*bd*bd
 data=np.column_stack([ts,b,s,x,y,vx,vy,ep/r['U0_J'],x1,y1,e1,ep])
 out=Path(__file__).resolve().parents[1]/'figures';out.mkdir(exist_ok=True)
 np.savetxt(out/'project.csv',data,delimiter=',',header='time,beam,sling,x,y,vx,vy,eff,x1,y1,energy1,energy2',comments='')
 report={'refined_final_velocity_m_s':[float(vx[-1]),float(vy[-1])],'velocity_difference_from_first_run_m_s':float(np.linalg.norm(np.array([vx[-1],vy[-1]])-r['velocity_m_s'])),'relative_energy_error':float(np.max(np.abs(total-total[0]))/r['U0_J']),'samples_before_release':151,'purpose':'independent step/tolerance refinement and actual data for plots'}
 (Path(__file__).resolve().parents[1]/'qa/project-refinement-check.json').write_text(json.dumps(report,indent=2)+'\n')
 return report
