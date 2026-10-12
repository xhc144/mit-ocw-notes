"""Actually compute the newly restored PS1--6 model and public-data tasks."""
from pathlib import Path
import json,hashlib,shutil
import numpy as np
from numba import njit
from scipy.integrate import solve_ivp
from scipy.signal import welch
ROOT=Path(__file__).resolve().parents[1]
def save(name,header,a):np.savetxt(ROOT/'data'/name,a,delimiter=',',header=header,comments='')

@njit
def fhn(a,x0,y0,dt,tend):
    n=int(round(tend/dt));x=x0;y=y0;lo=1e100;hi=-1e100;plot=np.zeros((n//20+1,3));plot[0]=[0.,x,y];j=1
    for i in range(n):
        f=lambda xx,yy:(-yy+xx*(a-xx)*(xx-1),.01*xx-.02*yy)
        k1,l1=f(x,y);k2,l2=f(x+dt*k1/2,y+dt*l1/2);k3,l3=f(x+dt*k2/2,y+dt*l2/2);k4,l4=f(x+dt*k3,y+dt*l3)
        x+=dt*(k1+2*k2+2*k3+k4)/6;y+=dt*(l1+2*l2+2*l3+l4)/6
        if i>n*.75:lo=min(lo,x);hi=max(hi,x)
        if (i+1)%20==0:plot[j]=[(i+1)*dt,x,y];j+=1
    return hi-lo,x,y,plot[:j]

def main():
    report={};data=ROOT/'data'
    # Logistic tasks use the original factor4 convention.
    logistic=[]
    for mu in [.5,.76,.89,.91]:
        x=.2;y=.20000001;rows=[]
        for j in range(600):rows.append([j,x,y,abs(x-y)]);x=4*mu*x*(1-x);y=4*mu*y*(1-y)
        save(f'ps1-logistic-mu{mu:.2f}.csv','iteration,x,x_perturbed,distance',rows);tail=np.array(rows)[-256:,1];z=tail.copy()
        lyap=float(np.mean(np.log(np.maximum(abs(4*mu*(1-2*z)),1e-300))))
        period=next((p for p in range(1,65) if np.max(abs(tail[p:]-tail[:-p]))<1e-7),None)
        logistic.append({'mu':mu,'initial':.2,'perturbed_initial':.20000001,'observed_period':period,'finite_orbit_Lyapunov':lyap})
    report['PS1']=logistic
    # Original Allee example r1,a8,b13; separate initial conditions.
    a=8.;b=13.;r=1.;roots=[(a-np.sqrt(a*a-4*b))/2,(a+np.sqrt(a*a-4*b))/2];times=np.linspace(0,2,801);series=[times]
    for n0 in [1.,2.,3.,5.,7.]:
        sol=solve_ivp(lambda t,y:r*y*(-y*y+a*y-b),(0,2),[n0],t_eval=times,rtol=1e-10,atol=1e-12);assert sol.success;series.append(sol.y[0])
    save('ps2-allee-initials.csv','t,N1,N2,N3,N5,N7',np.array(series).T)
    # Explicit additive-noise SDE illustration; distinct from crude original
    # per-step noise, which depends on dt. Fixed seed, no fabricated observations.
    rng=np.random.default_rng(20261012);dt=.0005;end=30.;n=int(end/dt);N=5.;sigma=.12;rows=[];deviations=[]
    for i in range(n):
        t=i*dt;bb=13.+2.9*t/end;target=(8+np.sqrt(max(0,64-4*bb)))/2
        N+=N*(-N*N+8*N-bb)*dt+sigma*np.sqrt(dt)*rng.normal()
        rows.append([t,bb,N,target]);deviations.append(N-target)
    save('ps2-allee-noisy.csv','t,b,N,quasistatic_branch',np.array(rows)[::20]);windows=[]
    for center in [5.,15.,25.]:
        lo=int((center-2)/dt);hi=int((center+2)/dt);z=np.array(deviations[lo:hi]);lag=int(.02/dt)
        windows.append({'center_time':center,'variance_detrended':float(z.var()),'autocorrelation_lag_.02':float(np.corrcoef(z[:-lag],z[lag:])[0,1])})
    report['PS2']={'r':r,'a':a,'b_fixed':b,'fixed_points':[0.,*roots],'noise':{'kind':'specified additive SDE illustration, Euler--Maruyama, not experimental data','sigma':sigma,'dt':dt,'b_change':[13.,15.9],'seed':20261012,'windows':windows}}
    # VdP includes two initial states; large-mu periods already computed by
    # extended_physics_checks, so only required time/phase plots are added.
    vdp=[]
    for mu in [.1,20.]:
        for idx,initial in enumerate([[1.,1.],[3.,0.]]):
            end=500. if mu==.1 else 300.;t=np.arange(0,end+.025,.05)
            sol=solve_ivp(lambda tt,v:[v[1],-mu*v[1]*(v[0]*v[0]-1)-v[0]],(0,end),initial,t_eval=t,method='Radau' if mu>1 else 'DOP853',rtol=1e-9,atol=1e-11);assert sol.success
            rows=np.c_[t,sol.y.T];cut=t> (450 if mu==.1 else 200);save(f'ps3-vdp-mu{mu:g}-start{idx}.csv','t,x,xdot',rows[cut][::2]);vdp.append({'mu':mu,'initial':initial,'tail_amplitude':float(np.max(abs(sol.y[0,cut]))),'end':end})
    # Population example, explicitly a=b=c=d=1. Light-loss perturbation is
    # instantaneous P reduction, and is not equivalent to parameter change.
    t=np.linspace(0,40,4001);lv=[]
    for idx,initial in enumerate([[1.4,1.],[.4,1.],[0.,1.]]):
        sol=solve_ivp(lambda tt,y:[y[0]*(1-y[1]),y[1]*(y[0]-1)],(0,40),initial,t_eval=t,rtol=1e-10,atol=1e-12);assert sol.success
        save(f'ps3-plankton-start{idx}.csv','t,P,Z',np.c_[t[::4],sol.y[:,::4].T])
        if initial[0]>0:
            inv=sol.y[0]-np.log(sol.y[0])+sol.y[1]-np.log(sol.y[1]);error=float(np.ptp(inv));assert error<1e-6
        else:error=None
        lv.append({'initial':initial,'first_integral_max_drift':error})
    report['PS3']={'vdp':vdp,'plankton':lv,'large_mu_periods_reused':'qa/extended-physics-checks.json'}
    # Locate FHN cycle fold from provided (0.2,0), retaining finite integration
    # time and an explicit amplitude diagnostic. This is not a proof.
    scan=[]
    for a in np.linspace(-.025,.005,61):
        amp,x,y,_=fhn(float(a),.2,0.,.05,4000.);scan.append([a,amp,x,y])
    save('ps4-fhn-scan.csv','a,tail_amplitude,x_end,y_end',scan);cycles=[x for x in scan if x[1]>.3];stable=[x for x in scan if x[1]<1e-4]
    assert cycles and stable;lower=max(x[0] for x in cycles);upper=min(x[0] for x in stable if x[0]>lower)
    for _ in range(13):
        mid=(lower+upper)/2;amp,_,_,_=fhn(mid,.2,0.,.05,6000.)
        if amp>.3:lower=mid
        else:upper=mid
    chosen=(-.02+lower)/2;examples=[]
    for tag,aa,x0 in [('bistable-small',chosen,1e-5),('bistable-large',chosen,.2),('excitable-small',.02,.02),('excitable-large',.02,.2)]:
        amp,x,y,plot=fhn(aa,x0,0.,.05,1500.);save('ps4-'+tag+'.csv','t,x,y',plot);examples.append({'tag':tag,'a':aa,'x0':x0,'tail_amplitude':amp,'maximum_x':float(plot[:,1].max())})
    exc=[]
    for x0 in np.linspace(.01,.2,191):
        _,_,_,plot=fhn(.02,float(x0),0.,.05,400.);exc.append([x0,np.max(plot[:,1])])
    save('ps4-excitation-response.csv','x0,maximum_x',exc);fine=next(x[0] for x in exc if x[1]>.5)
    report['PS4']={'Hopf_a':-.02,'cycle_fold_bracket_by_finite_tail_amplitude': [lower,upper],'fold_diagnostic':'>.3 x-range in final quarter; RK4 dt.05, t6000','bistable_a':chosen,'examples':examples,'excitation_half_unit_response_first_x0':fine,'continuous_excitation_not_discontinuous_bifurcation':True}
    # Brusselator near Hopf; period is in model time units.
    a=1.;b=2.01;t=np.arange(0,1000.0001,.05)
    sol=solve_ivp(lambda tt,z:[a+z[0]**2*z[1]-(b+1)*z[0],b*z[0]-z[0]**2*z[1]],(0,1000),[1.1,b],t_eval=t,rtol=1e-10,atol=1e-12,method='DOP853');assert sol.success
    take=t>=500;v=sol.y[0,take]-a;freq,PSD=welch(v,fs=20,nperseg=8192,noverlap=4096);save('ps5-brusselator-spectrum.csv','frequency,PSD',np.c_[freq[1:],PSD[1:]]);save('ps5-brusselator-trajectory.csv','t,x,y',np.c_[t[t>900][::2],sol.y[:,t>900][:,::2].T]);report['PS5_Brusselator']={'a':a,'b':b,'predicted_Hopf_frequency':a/(2*np.pi),'observed_spectral_peak':float(freq[1:][np.argmax(PSD[1:])]),'PSD_window_time':409.6}
    # Official already-uniform20yr ice-core series; do not interpolate again.
    src=Path('/tmp/mit-physics-research/chaos/ice_core_data.csv');target=data/'ice_core_data.csv'
    if not target.exists():shutil.copyfile(src,target)
    ice=np.loadtxt(target,delimiter=',');dt=float(np.diff(ice[:,0]).mean());assert np.max(abs(np.diff(ice[:,0])-dt))<1e-8
    z=ice[:,1]-ice[:,1].mean();window=np.hanning(len(z));ff=np.fft.rfftfreq(len(z),dt);power=abs(np.fft.rfft(window*z))**2*dt/np.sum(window**2);power[1:-1]*=2
    save('ps5-ice-spectrum.csv','frequency_per_year,PSD_C2_year',np.c_[ff[1:],power[1:]]);peaks=[]
    for period,band in [(100000,(80000,130000)),(41000,(35000,47000)),(23000,(19000,26000))]:
        ids=np.flatnonzero((ff>=1/band[1])&(ff<=1/band[0]));k=ids[np.argmax(power[ids])];peaks.append({'target_period_year':period,'selected_local_peak_period_year':float(1/ff[k]),'band_year':band})
    report['PS5_ice']={'source':'MIT 12.006J official ice_core_data.csv, cited Parrenin et al2013','input_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'samples':len(z),'dt_year':dt,'input_is_uniformly_sampled_course_data':True,'PSD':'demean,Hann,one-sided full-record periodogram; not raw original ice sampling','peaks':peaks}
    # PS6 uses the actual initial state in publicly provided roessler.py.
    def field(t,z):x,y,zz=z;return [-y-zz,x+.2*y,.2+zz*(x-5.7)]
    def event(t,z):return z[0]
    event.direction=1
    t=np.arange(0,1000.0001,.02);sol=solve_ivp(field,(0,1000),[0.,5.7,.05],t_eval=t,events=event,rtol=1e-10,atol=1e-12,method='DOP853');assert sol.success
    valid=t>=100;v=sol.y[:,valid];tt=t[valid];save('ps6-rossler-time.csv','t,x,y,z',np.c_[tt[-3000::4],v[:,-3000::4].T]);fr,p=welch(v,fs=50,nperseg=8192,axis=1);save('ps6-rossler-spectra.csv','frequency,Sx,Sy,Sz',np.c_[fr[1:],p[:,1:].T]);cross=sol.y_events[0][sol.t_events[0]>100];save('ps6-rossler-section.csv','x,y,z',cross);delay=10;z=v[0];embed=np.c_[z[:-2*delay:8],z[delay:-delay:8],z[2*delay::8]];save('ps6-rossler-delay.csv','x_now,x_delay,x_2delay',embed)
    report['PS6']={'initial':[0,5.7,.05],'tend':1000,'output_dt':.02,'DOP853_rtol':1e-10,'transient_discard_time':100,'positive_crossings_x0':len(cross),'delay_time':.2,'spectrum_frequency_units':'cycles/model_time','earlier_general_rossler_example_untouched':True}
    (ROOT/'qa/chaos-intro-tasks.json').write_text(json.dumps({'status':'PASS','results':report},indent=2));print('PS1--6 actual tasks completed',flush=True)
if __name__=='__main__':main()
