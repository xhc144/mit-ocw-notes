"""Reproduce selected physical calculations and analyze unmodified MIT OCW data."""
from pathlib import Path
import json, numpy as np
from scipy.integrate import solve_ivp,solve_bvp,quad
from scipy.optimize import brentq
from scipy.special import beta
from scipy.signal import welch
ROOT=Path(__file__).resolve().parents[1]
(ROOT/"qa").mkdir(exist_ok=True)
(ROOT/"data").mkdir(exist_ok=True)
result={'data_types':{'exp1.csv':'official published experimental data: Dubois and Berge, MIT 12.006J PS7','exp2.csv':'same experiment, second location','all_other_outputs':'specified deterministic mathematical models'}}
def csv(name,header,a):np.savetxt(ROOT/'data'/name,a,delimiter=',',header=header,comments='',fmt='%.10g')
# Independent integration and special-function evaluation of Rayleigh collapse.
integ=quad(lambda y:y**1.5/np.sqrt(1-y**3),0,1)[0];coef=np.sqrt(1.5)*integ
result['cavity']={'integral':integ,'beta_integral':float(beta(5/6,.5)/3),'time_coefficient':coef,'residual':float(abs(integ-beta(5/6,.5)/3))}
assert result['cavity']['residual']<1e-8
# Open-channel cell problem yields the exact coefficient.
I=quad(lambda y:(y*y-y**3/3-2*y/3)**2,0,1)[0]
result['dispersion']={'integral':I,'expected':8/945,'residual':abs(I-8/945)};assert abs(I-8/945)<1e-12
# Radome: distinguish rainfall per horizontal projection vs per local surface.
nu=1e-6;P=.002/3600;R=100;g=9.81
result['radome']={'vertical_rain_h_m':float((3*nu*P*R/(2*g))**(1/3)),'uniform_surface_rain_equator_h_m':float((3*nu*P*R/g)**(1/3))}
# Blasius physically motivated BVP (not a new generic numerical-method chapter).
eta=np.linspace(0,12,400)
def fun(x,y):return np.vstack([y[1],y[2],-.5*y[0]*y[2]])
def bc(a,b):return np.array([a[0],a[1],b[1]-1])
y=np.vstack([eta+np.exp(-eta)-1,1-np.exp(-eta),np.exp(-eta)])
sol=solve_bvp(fun,bc,eta,y,tol=1e-9,max_nodes=5000);assert sol.success
result['blasius']={'fpp0':float(sol.sol(0)[2]),'boundary_residual':float(np.max(abs(bc(sol.sol(0),sol.sol(12))))),'max_rms_residual':float(sol.rms_residuals.max())}
csv('blasius.csv','eta,velocity',np.c_[eta,sol.sol(eta)[1]])
# Public data analysis: sample index, no invented seconds or absolute temperature.
result['data_analysis']=[]
for n in [1,2]:
 a=np.loadtxt(ROOT/'data'/f'exp{n}.csv',delimiter=',');x=a[:,1]-a[:,1].mean();f,s=welch(x,fs=1,nperseg=2048,noverlap=1024)
 csv(f'exp{n}-spectrum.csv','frequency,PSD',np.c_[f[1:],s[1:]])
 tau=4;stride=8;embed=np.c_[x[:-2*tau:stride],x[tau:-tau:stride],x[2*tau::stride]];csv(f'exp{n}-delay.csv','x,y,z',embed)
 top=np.argsort(s[1:])[-5:]+1
 result['data_analysis'].append({'name':f'exp{n}.csv','samples':len(x),'mean_raw':float(a[:,1].mean()),'std_raw':float(a[:,1].std()),'frequency_units':'cycles/sample','strongest_frequency':float(f[np.argmax(s[1:])+1]),'top5':[[float(f[i]),float(s[i])] for i in top[::-1]],'delay_samples':tau})
# Lorenz: exact initial conditions from the publicly linked lorenz.py.
sigma,b=10.,8/3
result['lorenz']=[]
for r in [10.,28.]:
 def fun(t,v):x,y,z=v;return [sigma*(y-x),x*(r-z)-y,x*y-b*z]
 t=np.arange(0,200.0001,.002)
 out=solve_ivp(fun,(0,200),[.01,.01,.01],method='DOP853',rtol=1e-10,atol=1e-12,t_eval=t);assert out.success
 a=out.y.T;fixed=np.array([np.sqrt(b*(r-1))]*2+[r-1]);J=np.array([[-sigma,sigma,0],[1,-1,-fixed[0]],[fixed[0],fixed[0],-b]])
 ev=np.linalg.eigvals(J)
 row={'r':r,'initial':[.01,.01,.01],'t_end':200,'output_dt':.002,'method':'DOP853','rtol':1e-10,'atol':1e-12,'nonzero_fixed_eigenvalues':[[float(e.real),float(e.imag)] for e in ev],'final':a[-1].tolist(),'max_abs':a.max(0).tolist(),'sign_changes_X_after100':int(np.sum(np.diff(np.sign(a[t>100,0]))!=0))};result['lorenz'].append(row)
 if r==28:
  csv('lorenz.csv','t,X,Y,Z',np.c_[t[::20],a[::20]])
  cut=(t>=100)&(t<=140);csv('lorenz-plot.csv','t,X,Y,Z',np.c_[t[cut][::20],a[cut][::20]])
result['lorenz_critical']=sigma*(sigma+b+3)/(sigma-b-1)
# Henon fixed points, unstable eigenvector slope, bounded map cloud.
alpha,bh=1.4,.3
roots=np.roots([alpha,1-bh,-1]);xf=float(roots.max());yf=bh*xf;J=np.array([[-2*alpha*xf,1],[bh,0]])
vals,vecs=np.linalg.eig(J);u=vecs[:,np.argmax(np.abs(vals))];slope=float(u[1]/u[0])
x,y=xf+1e-4,yf;a=[]
for i in range(30000):x,y=1+y-alpha*x*x,bh*x;a.append([x,y])
a=np.array(a)[1000:];csv('henon.csv','X,Y',a[::20])
result['henon']={'fixed_points':[[float(x),float(bh*x)] for x in roots],'eigenvalues':vals.tolist(),'predicted_unstable_slope':slope,'alpha_c':3*(1-bh)**2/4,'samples':len(a)}
local=[];near=np.array([xf,yf])+1e-8*u/np.linalg.norm(u)
for it in range(12):
 delta=near-[xf,yf];local.append({'step':it,'distance':float(np.linalg.norm(delta)),'slope':float(delta[1]/delta[0])})
 near=np.array([1+near[1]-alpha*near[0]**2,bh*near[0]])
result['henon']['local_unstable_branch']=local

# Exact implicit superstable roots with lower-period roots explicitly excluded.
def orbit(r,p):
 x=.5
 for _ in range(p):x=r*x*(1-x)
 return x-.5
rs=[];previous=2.
for n in range(1,8):
 grid=np.linspace(previous+1e-7,3.5700,2001);v=np.array([orbit(r,2**n) for r in grid]);idx=np.where(v[:-1]*v[1:]<0)[0]
 if not len(idx):raise RuntimeError('No primitive superstable bracket')
 i=idx[0];root=brentq(lambda r:orbit(r,2**n),grid[i],grid[i+1],xtol=1e-14);rs.append(root);previous=root
result['superstable']=[{'n':n+1,'period':2**(n+1),'r':float(r),'mu':float(r/4),'residual':float(abs(orbit(r,2**(n+1))))} for n,r in enumerate(rs)]
result['superstable_ratio']=(rs[5]-rs[4])/(rs[6]-rs[5])
# Lava shape and volume integral; finite differences are not used as a proof.
z=np.linspace(0,1,301);profile=(3*(1-z*z)/16)**(1/3);csv('lava.csv','eta,f',np.c_[z,profile])
I=quad(lambda z:z*(3*(1-z*z)/16)**(1/3),0,1)[0];exactI=3/8*(3/16)**(1/3)
result['lava']={'integral':I,'expected':exactI,'residual':float(abs(I-exactI))};assert abs(I-exactI)<1e-9
(ROOT/'qa'/'numerical-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))

# Public lecture 19 Rossler example, explicit author-chosen model parameters.
from scipy.integrate import solve_ivp
rs_a=rs_b=.2;rs_c=5.7
def rs_field(t,rs_y):
 rs_x,rs_v,rs_z=rs_y[:3];out=np.array([-rs_v-rs_z,rs_x+rs_a*rs_v,rs_b+rs_z*(rs_x-rs_c)])
 if len(rs_y)==3:return out
 rs_J=np.array([[0,-1,-1],[1,rs_a,0],[rs_z,0,rs_x-rs_c]])
 return np.concatenate([out,rs_J@rs_y[3:]])
rs_times=np.arange(0,200.001,.02);rs_sol=solve_ivp(rs_field,[0,200],[1,0,0],t_eval=rs_times,rtol=1e-10,atol=1e-12,method='DOP853');assert rs_sol.success
rs_take=np.flatnonzero(rs_times>=150)[::4];np.savetxt(ROOT/'data/rossler-plot.csv',rs_sol.y[:,rs_take].T,delimiter=',',header='x,y,z',comments='')
rs_state=np.array([1.,0.,0.,1/np.sqrt(3),1/np.sqrt(3),1/np.sqrt(3)]);rs_logs=[];rs_div=[]
for rs_n in range(800):
 rs_step=solve_ivp(rs_field,[0,.5],rs_state,rtol=1e-9,atol=1e-11,method='DOP853');assert rs_step.success
 rs_state=rs_step.y[:,-1];rs_norm=np.linalg.norm(rs_state[3:]);rs_state[3:]/=rs_norm
 if rs_n>=200:rs_logs.append(np.log(rs_norm));rs_div.append(rs_a+rs_state[0]-rs_c)
rs_report={'data_kind':'deterministic authored Rossler model simulation, no experimental data','a':rs_a,'b':rs_b,'c':rs_c,'total_time':400,'discarded_time':100,'renormalization_interval':.5,'largest_finite_time_lyapunov_estimate':float(sum(rs_logs)/(len(rs_logs)*.5)),'mean_divergence_endpoint_sampled':float(np.mean(rs_div)),'no_rigorous_asymptotic_proof_claimed':True}
(ROOT/'qa/rossler-model.json').write_text(json.dumps(rs_report,indent=2));print('Rossler check',rs_report)
