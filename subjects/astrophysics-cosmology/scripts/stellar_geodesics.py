"""Actual Schwarzschild integrations for 8.901 PS7.3 public parts.

G=c=M=1. Converts to a ten-solar-mass source only in the text.
Does not claim to have obtained or compared restricted textbook equations.
"""
from pathlib import Path
import argparse,math,json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args()
out=args.out;out.mkdir(parents=True,exist_ok=True);records=[]
def run(name,r0,pr0,L,E,massive,duration=1800):
 def fun(s,y):
  r,pr,phi,t=y;f=1-2/r
  acc=(-1/r**2+L**2/r**3-3*L**2/r**4) if massive else L**2*(r-3)/r**4
  return [pr,acc,L/r**2,E/f]
 def capture(s,y):return y[0]-2.0001
 capture.terminal=True;capture.direction=-1
 def far(s,y):return y[0]-60
 far.terminal=True;far.direction=1
 sol=solve_ivp(fun,[0,duration],[r0,pr0,0,0],events=[capture,far],method='DOP853',rtol=1e-10,atol=[1e-11,1e-11,1e-11,1e-9],max_step=.5,dense_output=True)
 assert sol.success,sol.message
 ts=np.linspace(0,sol.t[-1],1200);r,pr,phi,t=sol.sol(ts)
 V=(1-2/r)*((1 if massive else 0)+L*L/(r*r));err=np.max(np.abs(pr*pr+V-E*E))
 assert err<1e-7,(name,err)
 xy=np.c_[ts,r,pr,phi,t,r*np.cos(phi),r*np.sin(phi)]
 np.savetxt(out/('stellar-geodesic-'+name+'.csv'),xy,delimiter=',',header='affine,r,pr,phi,t,x,y',comments='')
 # Actual-sample subset for vector figures; the full conserved-energy table stays intact.
 step=2 if name=='bound-precession' else 5
 ix=np.unique(np.r_[np.arange(0,len(ts),step),np.arange(max(0,len(ts)-60),len(ts))])
 np.savetxt(out/('stellar-geodesic-'+name+'-plot.csv'),xy[ix],delimiter=',',header='affine,r,pr,phi,t,x,y',comments='')
 records.append({'name':name,'initial_r':r0,'initial_pr':pr0,'angular_momentum':L,'energy':E,'massive':massive,'affine_end':sol.t[-1],'minimum_r':float(min(r)),'last_r':float(r[-1]),'energy_constraint_max_error':float(err),'capture':len(sol.t_events[0])>0,'reached_r60':len(sol.t_events[1])>0})

# Drop from local rest at r=12.
r0=12.;E=math.sqrt(1-2/r0);run('radial-drop',r0,0,0,E,True)
# Near-critical unbound impact parameters: E > 1.
E=1.1;rc=brentq(lambda r:(r-2)**2/(r*(r-3))-E*E,3.000001,4)
Lc=math.sqrt(rc*rc/(rc-3))
for name,factor in [('unbound-turn',1.001),('unbound-capture',.999)]:
 L=Lc*factor;r0=40.;pr0=-math.sqrt(E*E-(1-2/r0)*(1+L*L/r0**2));run(name,r0,pr0,L,E,True)
# Bound orbit with exact peri/apocenter energy equality.
rp=6.;ra=12.;L2=2*ra*ra*rp*rp/(ra*rp*(ra+rp)-2*(ra*ra+ra*rp+rp*rp))
L=math.sqrt(L2);E=math.sqrt((1-2/ra)*(1+L2/ra**2));run('bound-precession',ra,0,L,E,True,2600)
# Circular orbits and small perturbations, holding L then setting initial E.
for rbase,label in [(8.,'stable'),(4.,'unstable'),(5.9,'below-ISCO'),(6.1,'above-ISCO')]:
 L=math.sqrt(rbase*rbase/(rbase-3))
 for frac,which in [(0,'circle'),(.001,'out'),(-.001,'in')]:
  r0=rbase*(1+frac);E=math.sqrt((1-2/r0)*(1+L*L/r0**2))
  run(label+'-'+which,r0,0,L,E,True,1500)
# Photons seen at r=2.3 in a static local frame, angle from outward radial direction.
r0=2.3;critical=math.asin(3*math.sqrt(3)*math.sqrt(1-2/r0)/r0)
for name,angle in [('radial',0),('escaping',.8*critical),('escaping-025',.25*critical),('escaping-050',.5*critical),('escaping-099',.99*critical),('captured',1.02*critical),('captured-1001',1.001*critical),('captured-115',1.15*critical),('inward',math.pi-.5*critical)]:
 L=r0*math.sin(angle)/math.sqrt(1-2/r0);run('photon-'+name,r0,math.cos(angle),L,1.,False)
summary={'status':'PASS-actual-numerical-integration','units':'G=c=M=1','source_mass_for_conversion_solar':10,'unbound_energy':1.1,'critical_massive_radius':rc,'critical_massive_L':Lc,'photon_start_r':2.3,'outward_escape_half_angle_deg':math.degrees(critical),'ISCO_from_potential_second_derivative':6,'record_count':len(records),'records':records,'textbook_comparison':'not performed; Shapiro-Teukolsky equations and exercise not obtained; derived public conditions independently'}
(out/'stellar-geodesic-results.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
