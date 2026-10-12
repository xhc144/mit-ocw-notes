"""Full parameter survey for the *specified* Lab5 Ising model.

Finite-size simulation and Binder evidence, not empirical H/Pd observations or
a rigorous infinite-lattice theorem. Existing 4x4 MD/MC checks are untouched.
"""
from pathlib import Path
import argparse, json, time
import numpy as np
from numba import njit
ROOT=Path(__file__).resolve().parents[1]
@njit
def energy(s,mu):
    L=len(s);e=0.
    for i in range(L):
        for j in range(L):
            e+=s[i,j]*(s[(i+1)%L,j]+s[i,(j+1)%L]-2*s[(i+1)%L,(j+1)%L]-2*s[(i+1)%L,(j-1)%L]-mu)
    return e
@njit
def sample(L,T,mu,burn,production,seed,initial):
    np.random.seed(seed);s=np.empty((L,L),np.int8)
    for i in range(L):
        for j in range(L):
            s[i,j]=1 if initial==0 else (-1 if (i+j)%2 else 1)
    # Four colors avoid simultaneous interacting NN or NNN updates.
    values=np.zeros((production//5,5));hist=np.zeros(51,np.int64);colors=np.arange(4)
    for sweep in range(burn+production):
        np.random.shuffle(colors)
        for color in colors:
            a=color//2;b=color%2
            for i in range(a,L,2):
                for j in range(b,L,2):
                    nn=s[(i+1)%L,j]+s[(i-1)%L,j]+s[i,(j+1)%L]+s[i,(j-1)%L]
                    nnn=s[(i+1)%L,(j+1)%L]+s[(i+1)%L,(j-1)%L]+s[(i-1)%L,(j+1)%L]+s[(i-1)%L,(j-1)%L]
                    h=nn-2*nnn-mu
                    argument=min(60.,max(-60.,2*h/T))
                    probability=1/(1+np.exp(argument))
                    s[i,j]=1 if np.random.random()<probability else -1
        # Symmetric whole-sublattice proposals cross the competing uniform/checkerboard basins.
        if sweep%10==0:
            parity=np.random.randint(2);sub=0.;bonds=0.
            for i in range(L):
                for j in range(L):
                    if (i+j)%2==parity:sub+=s[i,j]
                    bonds+=s[i,j]*(s[(i+1)%L,j]+s[i,(j+1)%L])
            delta=-2*bonds+2*mu*sub
            if delta<=0 or np.random.random()<np.exp(-delta/T):
                for i in range(L):
                    for j in range(L):
                        if (i+j)%2==parity:s[i,j]*=-1
        if sweep>=burn and (sweep-burn)%5==0:
            m=0.;ms=0.
            for i in range(L):
                for j in range(L):
                    m+=s[i,j];ms+=s[i,j]*(1 if (i+j)%2==0 else -1)
            m/=L*L;ms/=L*L;e=energy(s,mu)/(L*L)
            k=(sweep-burn)//5;values[k,0]=m;values[k,1]=abs(ms);values[k,2]=ms*ms;values[k,3]=ms**4;values[k,4]=e
            theta=(1+m)/2;hist[min(50,int(theta*50))]+=1
    return values,hist
@njit
def wolff_zero_field(L,T,burn,production,seed):
    np.random.seed(seed);s=np.ones((L,L),np.int8);p1=1-np.exp(-2/T);p2=1-np.exp(-4/T)
    stack=np.empty(L*L,np.int64);seen=np.zeros(L*L,np.int8);values=np.zeros((production,3))
    for step in range(burn+production):
        seen[:]=0;start=np.random.randint(L*L);stack[0]=start;seen[start]=1;tail=1;head=0;old=s[start//L,start%L]
        while head<tail:
            site=stack[head];head+=1;i=site//L;j=site%L
            for a,b,p in [(1,0,p1),(-1,0,p1),(0,1,p1),(0,-1,p1),(1,1,p2),(1,-1,p2),(-1,1,p2),(-1,-1,p2)]:
                ni=(i+a)%L;nj=(j+b)%L;idx=ni*L+nj
                if seen[idx]==0 and s[ni,nj]==old and np.random.random()<p:
                    stack[tail]=idx;tail+=1;seen[idx]=1
        for k in range(tail):s[stack[k]//L,stack[k]%L]*=-1
        if step>=burn:
            m=s.sum()/(L*L);values[step-burn,0]=abs(m);values[step-burn,1]=m*m;values[step-burn,2]=m**4
    return values

def blocks(values,count=20):
    usable=len(values)//count*count
    means=values[:usable].reshape(count,-1,values.shape[1]).mean(axis=1)
    return means.mean(axis=0),means.std(axis=0,ddof=1)/np.sqrt(count)
def main(quick=False):
    out=ROOT/'data';qa=ROOT/'qa';out.mkdir(exist_ok=True);qa.mkdir(exist_ok=True)
    sizes=[8,12,16,24] if not quick else [4]
    temperatures=[1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,12.] if not quick else [6.]
    fields=np.arange(0,8.01,.5) if not quick else [0.,2.]
    burn,production=(1000,3000) if not quick else (200,1000)
    rows=[];checks=[];histrows=[];started=time.time()
    for L in sizes:
        for T in temperatures:
            for mu in fields:
                means=[];errs=[]
                for initial in [0,1]:
                    seed=20261012+L*100000+int(T*1000)+int(mu*100)+initial
                    val,hist=sample(L,T,float(mu),burn,production,seed,initial)
                    mean,err=blocks(val);means.append(mean);errs.append(err)
                    if T in [1.,2.,4.] and mu in [3.5,4.,4.5] and L==sizes[-1]:
                        for k,n in enumerate(hist):histrows.append([L,T,mu,initial,k/50.,int(n)])
                mean=np.mean(means,axis=0);err=np.sqrt(np.sum(np.array(errs)**2,axis=0))/2
                ms2=mean[2];binder=1-mean[3]/(3*ms2**2) if ms2 else 0.
                difference=abs(means[0][0]-means[1][0]);tolerance=5*np.hypot(errs[0][0],errs[1][0])+.02
                row=[L,T,float(mu),(1+mean[0])/2,mean[1],binder,err[0]/2,err[1],int(difference>tolerance)]
                rows.append(row)
                if difference>tolerance:checks.append({'L':L,'T':T,'mu':float(mu),'start_dependence_uniform_m':float(difference),'tolerance':float(tolerance),'classification':'not_converged_by_this_diagnostic; retain flag, do not claim stable phase'})
            print('Phase grid',L,T,'elapsed',round(time.time()-started,1),flush=True)
    np.savetxt(out/'adsorption-phase-grid.csv',rows,delimiter=',',header='L,T,mu,theta,abs_staggered,binder,u_theta,u_order,unresolved_start_dependence',comments='')
    largest=np.array([r for r in rows if r[0]==sizes[-1]])
    # Exact spin-inversion symmetry supplies the negative-mu side, explicitly marked in QA.
    plotted=[]
    for r in largest:
        plotted.append([r[1],r[3],r[4],r[8]])
        if r[2]>0:plotted.append([r[1],1-r[3],r[4],r[8]])
    np.savetxt(out/'adsorption-phase-plot.csv',plotted,delimiter=',',header='T,theta,order,unresolved',comments='')
    if histrows:np.savetxt(out/'adsorption-coexistence-histograms.csv',histrows,delimiter=',',header='L,T,mu,start,theta_bin,count',comments='')
    critical=[]
    for L in sizes:
        for T in (np.arange(5.,9.01,.25) if not quick else [6.]):
            val=wolff_zero_field(L,float(T),1000 if not quick else 100,5000 if not quick else 500,20261012+L*100000+int(T*1000))
            mean,err=blocks(val);binder=1-mean[2]/(3*mean[1]**2)
            batches=val[:len(val)//20*20].reshape(20,-1,3).mean(axis=1)
            block_binder=1-batches[:,2]/(3*batches[:,1]**2)
            u_binder=block_binder.std(ddof=1)/np.sqrt(20)
            critical.append([L,T,mean[0],binder,err[0],u_binder])
        print('Binder scan',L,flush=True)
    np.savetxt(out/'adsorption-binder.csv',critical,delimiter=',',header='L,T,abs_staggered,binder,u_order,u_binder_block_diagnostic',comments='')
    versions={'numpy':np.__version__}
    import numba;versions['numba']=numba.__version__
    report={'kind':'simulation of actual Lab5 Hamiltonian, V1=1,V2=-2, each unordered pair once; not H/Pd experimental observations','sizes':sizes,'temperatures':temperatures,'mu_values':list(map(float,fields)),'grid_points':len(rows),'starts_per_point':2,'burn_sweeps':burn,'production_sweeps':production,'sample_stride_sweeps':5,'blocks':20,'update':'four-color conditional heatbath plus symmetric whole-sublattice Metropolis every10 sweeps','zero_mu_Binder_update':'gauge-transformed ferromagnetic J1=1,J2=2 Wolff clusters','zero_mu_Binder_points':len(critical),'negative_mu_plot':'exact spin-inversion symmetry, not separately sampled','unresolved_grid_points':checks,'wall_seconds':time.time()-started,'versions':versions,'limits':['finite sizes and finite sampling, critical and coexistence curves require uncertainty/size checks','start-dependent points remain flagged, not certified as equilibrated','order magnitude/color is an observable, not a proof of thermodynamic phase stability']}
    (qa/'adsorption-phase-analysis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print('Phase scan completed',len(rows),'unresolved',len(checks),flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--quick',action='store_true');main(ap.parse_args().quick)
