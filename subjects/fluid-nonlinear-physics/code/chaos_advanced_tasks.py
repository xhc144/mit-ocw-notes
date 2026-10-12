"""New PS8.5--7, PS9.3, PS10.2--3 computations; old checks.py unchanged."""
from pathlib import Path
import json
import numpy as np
from numba import njit
from scipy.optimize import root
from scipy.spatial import cKDTree
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[1]
def save(n,h,a):np.savetxt(ROOT/'data'/n,a,delimiter=',',header=h,comments='')

@njit
def lf(y,r):
    x,v,z=y;return np.array([10*(v-x),x*(r-z)-v,x*v-8*z/3])
@njit
def lorenz(r,initial,dt,tend):
    n=round(tend/dt);stride=round(.02/dt);y=initial.copy();out=np.zeros((n//stride+1,4));out[0,1:]=y;j=1
    for i in range(n):
        k1=lf(y,r);k2=lf(y+dt*k1/2,r);k3=lf(y+dt*k2/2,r);k4=lf(y+dt*k3,r)
        y+=dt*(k1+2*k2+2*k3+k4)/6
        if (i+1)%stride==0:out[j,0]=(i+1)*dt;out[j,1:]=y;j+=1
    return out[:j]
@njit
def tangent_field(y,r):
    x,v,z=y[:3];q=y[3:];d=lf(y[:3],r);J=np.array([[-10.,10.,0.],[r-z,-1.,-x],[v,x,-8/3]])
    return np.concatenate((d,J@q))
@njit
def lyapunov(r,dt,tend=600.):
    y=np.array([.01,.01,.01,1/np.sqrt(3),1/np.sqrt(3),1/np.sqrt(3)])
    interval=round(.1/dt);logs=np.zeros(round(tend/.1));j=0
    for i in range(round(tend/dt)):
        k1=tangent_field(y,r);k2=tangent_field(y+dt*k1/2,r);k3=tangent_field(y+dt*k2/2,r);k4=tangent_field(y+dt*k3,r);y+=dt*(k1+2*k2+2*k3+k4)/6
        if (i+1)%interval==0:
            mag=np.sqrt(np.sum(y[3:]**2));logs[j]=np.log(mag)/.1;j+=1;y[3:]/=mag
    return logs

@njit
def mapping(x,mu,kind):
    if kind==0:return x*np.exp(mu*(1-x))
    return mu*(1-(2*x-1)**4)
@njit
def iterate(mu,kind,burn,tail):
    x=.3;out=np.zeros(tail)
    for j in range(burn+tail):
        x=mapping(x,mu,kind)
        if j>=burn:out[j-burn]=x
    return out
def derivative(x,mu,kind):
    return np.exp(mu*(1-x))*(1-mu*x) if kind==0 else -8*mu*(2*x-1)**3
def critical(mu_guess,p,kind):
    x0=float(iterate(mu_guess-.0005,kind,6000,1)[0])
    def equations(z):
        x,mu=z;start=x;mult=1.
        for _ in range(p):mult*=derivative(x,mu,kind);x=mapping(x,mu,kind)
        return [x-start,mult+1]
    sol=root(equations,[x0,mu_guess],tol=1e-11);assert sol.success or np.max(np.abs(equations(sol.x)))<1e-8
    assert np.max(np.abs(equations(sol.x)))<1e-8
    x,mu=sol.x;orb=[]
    for _ in range(p):orb.append(x);x=mapping(x,mu,kind)
    assert p==1 or abs(mapping(orb[0],mu,kind)-orb[0])>1e-5
    return float(mu),{'period_before_doubling':p,'mu':float(mu),'root_residual':float(np.max(np.abs(equations(sol.x)))),'cycle':list(map(float,orb))}

def ps8_peak_events():
    """PS8.5 maxima from continuous-time downward dX/dt zero crossings."""
    result={}
    for r in [166.,166.1]:
        def rhs(t,y):
            x,v,z=y
            return [10*(v-x),x*(r-z)-v,x*v-8*z/3]
        def maximum(t,y):return 10*(y[1]-y[0])
        maximum.direction=-1
        maximum.terminal=False
        trials=[]
        for tolerance in [1e-10,1e-11]:
            sol=solve_ivp(rhs,(0.,600.),[.01,.01,.01],method='DOP853',rtol=tolerance,atol=tolerance/100,events=maximum,dense_output=True,max_step=.04)
            assert sol.success
            keep=sol.t_events[0]>=100.;times=sol.t_events[0][keep];states=sol.y_events[0][keep];peaks=states[:,0]
            residual=np.abs(10*(states[:,1]-states[:,0]));curvature=np.array([10*rhs(t,y)[1] for t,y in zip(times,states)])
            assert len(peaks)>1000 and np.max(residual)<1e-6 and np.all(curvature<0)
            levels=len(np.unique(np.round(peaks,2)))
            if r==166.:assert levels==3 and np.max(np.abs(peaks[3:]-peaks[:-3]))<1e-5
            else:assert levels>100
            trials.append({'rtol':tolerance,'atol':tolerance/100,'number_X_maxima':len(peaks),'distinct_peak_levels_rounded_.01':levels,'maximum_abs_dXdt_at_event':float(np.max(residual)),'largest_curvature_at_maximum':float(np.max(curvature)),'three_step_peak_difference_max':float(np.max(np.abs(peaks[3:]-peaks[:-3])))})
            if tolerance==1e-10:
                primary_peaks=peaks.copy();primary_times=times.copy();primary_states=states.copy()
                sample_times=np.linspace(550.,600.,2501);trace=sol.sol(sample_times).T
                save(f'ps8-r{r:g}-X.csv','t,X,Y,Z',np.c_[sample_times,trace])
        peaks=primary_peaks
        save(f'ps8-r{r:g}-maxima.csv','Xn,Xnext',np.c_[peaks[:-1],peaks[1:]])
        save(f'ps8-r{r:g}-peak-events.csv','t,X,Y,Z',np.c_[primary_times,primary_states])
        result[str(r)]={'r':r,'initial':[.01,.01,.01],'solver':'DOP853','rtol':1e-10,'atol':1e-12,'max_step':.04,'end':600,'transient_discard':100,'peak_detection':'continuous dX/dt=0 downward events, negative curvature checked; independent of trace output grid','number_X_maxima':len(peaks),'distinct_peak_levels_rounded_.01':len(np.unique(np.round(peaks,2))),'tolerance_checks':trials,'correction':'Earlier 0.02-output-grid maxima produced phase-alignment scatter; replaced by event maxima.','finite_time_behavior_note':'r166 has three repeating peak levels in this window; r166.1 has a broad irregular peak map. Counts for the irregular trajectory can vary with numerical tolerances; neither level counts nor finite-time traces are infinite-time proofs.'}
    return result

def peaks_only():
    report=ROOT/'qa/chaos-advanced-tasks.json'
    previous=json.loads(report.read_text());updated=ps8_peak_events()
    previous['results'].update(updated)
    previous['targeted_correction']='Only PS8.5 r166/r166.1 rerun; all other numerical results preserved.'
    report.write_text(json.dumps(previous,indent=2))
    print('PS8.5 continuous peak events PASS',json.dumps(updated),flush=True)

def main():
    result=ps8_peak_events()
    l1=lyapunov(170.,.001);l2=lyapunov(170.,.0005);production=l1[1000:];blocks=production.reshape(10,-1).mean(axis=1)
    a=lorenz(170.,np.array([.01,.01,.01]),.001,25.);b=lorenz(170.,np.array([.01+1e-8,.01,.01]),.001,25.);distance=np.linalg.norm(a[:,1:]-b[:,1:],axis=1);save('ps8-r170-separation.csv','t,distance',np.c_[a[:,0],distance])
    result['r170']={'largest_Lyapunov_finite_time':float(production.mean()),'block_std_diagnostic':float(blocks.std(ddof=1)),'dt_half_estimate':float(l2[1000:].mean()),'time_window':[100,600],'reset_interval':.1,'dt_values':[.001,.0005],'initial_separation':1e-8,'late_separation_max':float(distance[-500:].max()),'no_infinite_time_proof':True}
    r=24.5;f=np.sqrt((8/3)*(r-1));initials=[np.array([f+1e-5,f,r-1]),np.array([.01,.01,.01])];extra=[]
    for i,ini in enumerate(initials):
        a=lorenz(r,ini,.001,600.);save(f'ps8-chosen-r24.5-start{i}.csv','t,X,Y,Z',a[a[:,0]>=550][::3]);extra.append({'initial':ini.tolist(),'last50_X_range':float(np.ptp(a[a[:,0]>=550,1]))})
    result['self_chosen_r24.5']={'examples':extra,'purpose':'test dependence on basin/initial state below the nonzero-equilibrium Hopf; trace retained even if long chaotic transient settles'}
    # GP dimension uses the already completed r28 trajectory; no old ODE is
    # rerun. Theiler exclusion removes temporally neighboring pairs.
    raw=np.genfromtxt(ROOT/'data/lorenz.csv',delimiter=',',names=True);x=raw['X'][raw['t']>=40];x=(x-x.mean())/x.std();radii=np.geomspace(.03,2.,45);dims=[]
    for m in [3,5,7,10]:
        tau=4;points=np.column_stack([x[k*tau:len(x)-(m-1-k)*tau] for k in range(m)]);N=len(points);W=25
        tree=cKDTree(points);counts=(tree.count_neighbors(tree,radii)-N)/2
        for lag in range(1,W+1):
            dist=np.linalg.norm(points[lag:]-points[:-lag],axis=1);counts-=np.array([(dist<=r).sum() for r in radii])
        denom=N*(N-1)/2-sum(N-lag for lag in range(1,W+1));C=counts/denom;fit=(C>=.001)&(C<=.03)
        assert fit.sum()>=5 and np.all(C>=0)
        coef=np.polyfit(np.log(radii[fit]),np.log(C[fit]),1);save(f'ps9-GP-m{m}.csv','radius,correlation_sum',np.c_[radii[C>0],C[C>0]])
        dims.append({'embedding_m':m,'delay_samples':tau,'sample_dt':.04,'N':N,'Theiler_samples':W,'fitted_slope':float(coef[0]),'fit_radius_range':radii[fit][[0,-1]].tolist(),'fit_C_range':C[fit][[0,-1]].tolist(),'fit_points':int(fit.sum())})
    result['PS9_correlation_dimension']={'trajectory_reused':'data/lorenz.csv from already independently passed r28 run','time_window':[40,200],'units':'all delay coordinates divided by one global X standard deviation','cases':dims,'finite_data_estimate_not_Hausdorff_proof':True}
    for kind,name,domain,guesses in [(0,'ricker',(0.,4.),[2.,2.526,2.656,2.684]),(1,'quartic',(.4,1.),None)]:
        cloud=[]
        for mu in np.linspace(*domain,501):
            values=iterate(float(mu),kind,5000,32)
            cloud.extend([[mu,v] for v in values])
        save(f'ps10-{name}-bifurcation.csv','mu,x',cloud)
        if guesses is None:
            guessed=[];last=0
            for mu in np.linspace(.7,1.,1501):
                z=iterate(float(mu),kind,8000,128);period=next((p for p in [1,2,4,8,16] if np.max(abs(z[p:]-z[:-p]))<1e-5),0)
                if last in [1,2,4,8] and period==2*last:guessed.append(mu)
                if period:last=period
                if len(guessed)>=4:break
            assert len(guessed)>=4,guessed;guesses=guessed
        criticals=[]
        for i,g in enumerate(guesses):_,row=critical(float(g),2**i,kind);criticals.append(row)
        mu=np.array([q['mu'] for q in criticals]);assert np.all(np.diff(mu)>0)
        ratios=((mu[2]-mu[1])/(mu[3]-mu[2]),(mu[1]-mu[0])/(mu[2]-mu[1]))
        result[name]={'period_doubling':criticals,'finite_ratios_latest_first':list(map(float,ratios)),'bifurcation_grid':501,'burn_iterations':5000,'tail_per_parameter':32,'universality':'Ricker has quadratic maximum; quartic map has fourth-order maximum. Finite ratios are not required to equal their limits.'}
    (ROOT/'qa/chaos-advanced-tasks.json').write_text(json.dumps({'status':'PASS','results':result},indent=2));print('Advanced chaos public tasks PASS',flush=True)
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--ps8-peaks-only',action='store_true');args=parser.parse_args()
    if args.ps8_peaks_only:peaks_only()
    else:main()
