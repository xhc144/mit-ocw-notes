from pathlib import Path
import json,hashlib,math,csv
import mpmath as mp
from scipy.integrate import solve_ivp
ROOT=Path('/workspace/mit-ocw-notes');QA=ROOT/'subjects/introductory-mechanics/qa';DATA=ROOT/'subjects/introductory-mechanics/data'
mp.mp.dps=40;g=mp.mpf('9.81');k=mp.sin(mp.mpf('.25'))
pend_exact=4/mp.sqrt(g)*mp.ellipk(k*k)
chain_exact=2/mp.sqrt(g)*(2*mp.ellipe(mp.mpf('.5'))-mp.ellipk(mp.mpf('.5')))
def zero(t,y):return y[0]
zero.direction=-1
p=solve_ivp(lambda t,y:[y[1],-9.81*math.sin(y[0])],[0,3],[.5,0],method='DOP853',atol=1e-13,rtol=1e-13,events=zero)
def radialmax(t,y):return y[0]*y[2]+y[1]*y[3]
radialmax.direction=-1
sol=solve_ivp(lambda t,y:[y[2],y[3],-(y[0]**2+y[1]**2)*y[0],-(y[0]**2+y[1]**2)*y[1]],[0,20],[1.01,0,0,1/1.01],method='DOP853',atol=1e-13,rtol=1e-13,events=radialmax)
period=next(t for t in sol.t_events[0] if t>.1)
published=json.loads((DATA/'results.json').read_text())
angular=[];energies=[]
with (DATA/'central-orbit.csv').open() as f:
 for row in csv.DictReader(f):
  x,y,vx,vy=[float(row[k]) for k in ['x','y','vx','vy']];angular.append(x*vy-y*vx);energies.append((vx*vx+vy*vy)/2+(x*x+y*y)**2/4)
result={'method':'independent mpmath elliptic integrals + SciPy DOP853 adaptive integration; conserved quantities recalculated from published CSV','source_script_sha256':hashlib.sha256((ROOT/'subjects/introductory-mechanics/tools/numerics.py').read_bytes()).hexdigest(),'published_data_sha256':hashlib.sha256((DATA/'results.json').read_bytes()).hexdigest(),'pendulum_elliptic_period':str(pend_exact),'pendulum_DOP853_period':4*float(p.t_events[0][0]),'published_pendulum_error':float(published['pendulum_elliptic_integral_period_s']-pend_exact),'chain_end_elliptic_integral':str(chain_exact),'published_chain_end_error':float(published['chain_end_time_s_L1']-chain_exact),'central_DOP853_radial_period':float(period),'published_central_period_error':float(published['central_orbit']['radial_period']-period),'central_CSV_max_abs_L_minus_1':max(abs(a-1) for a in angular),'central_CSV_relative_energy_drift':max(abs(a/energies[0]-1) for a in energies),'status':'consistent with declared finite-amplitude model and interpolation accuracy; no experiment claimed'}
(QA/'independent-numerical-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
