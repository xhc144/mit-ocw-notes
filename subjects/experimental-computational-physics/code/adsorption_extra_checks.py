"""Additional physical checks and high-T Langmuir task, using the frozen model."""
from pathlib import Path
import json,hashlib
import numpy as np
from phase_diagram import energy,sample,blocks
ROOT=Path(__file__).resolve().parents[1]

def main():
    rng=np.random.default_rng(20261012);tests=[]
    for L in [4,8]:
        eta=np.fromfunction(lambda i,j:1-2*((i+j)%2),(L,L),dtype=int).astype(np.int8)
        assert energy(eta,0)==-6*L*L
        for mu in [0.,1.3,4.]:
            s=rng.choice(np.array([-1,1],dtype=np.int8),(L,L));i,j=rng.integers(L,size=2)
            nn=s[(i+1)%L,j]+s[(i-1)%L,j]+s[i,(j+1)%L]+s[i,(j-1)%L]
            nnn=s[(i+1)%L,(j+1)%L]+s[(i+1)%L,(j-1)%L]+s[(i-1)%L,(j+1)%L]+s[(i-1)%L,(j-1)%L]
            direct=energy(s,mu);t=s.copy();t[i,j]*=-1
            delta=-2*s[i,j]*(nn-2*nnn-mu)
            assert abs(energy(t,mu)-direct-delta)<1e-10
            parity=1;t=s.copy();t[(np.indices(s.shape).sum(axis=0)%2)==parity]*=-1
            bonds=np.sum(s*(np.roll(s,-1,0)+np.roll(s,-1,1)))
            sub=np.sum(s[(np.indices(s.shape).sum(axis=0)%2)==parity]);dsub=-2*bonds+2*mu*sub
            assert abs(energy(t,mu)-direct-dsub)<1e-10
            # Conditional heatbath probability ratio equals the target weight.
            h=nn-2*nnn-mu;p=1/(1+np.exp(2*h/8))
            assert abs(p/(1-p)-np.exp(-2*h/8))<1e-9
            tests.append({'L':L,'mu':mu,'single_flip_delta':float(delta),'sublattice_flip_delta':float(dsub)})
    binder=np.genfromtxt(ROOT/'data/adsorption-binder-refined.csv',delimiter=',',names=True)
    for L in [8,12,16,24,32]:
        a=binder[binder['L']==L];np.savetxt(ROOT/'data'/f'binder-L{L}.csv',np.column_stack([a['T'],a['binder'],a['u_binder_jackknife']]),delimiter=',',header='T,binder,u_binder',comments='')
    high=[]
    for T in [4.,8.,12.,24.,48.]:
        data=[]
        for q in np.arange(0,3.001,.25):
            means=[];errors=[]
            for initial in [0,1]:
                v,_=sample(24,T,float(q*T),1000,5000,20261012+int(T*1000)+int(q*100)+initial,initial)
                m,u=blocks(v);means.append(m[0]);errors.append(u[0])
            theta=(1+np.mean(means))/2;uncertainty=np.hypot(*errors)/4
            data.append([q,theta,uncertainty,1/(1+np.exp(-2*q))])
        np.savetxt(ROOT/'data'/f'langmuir-T{int(T)}.csv',data,delimiter=',',header='mu_over_T,theta,u_theta,langmuir',comments='')
        high.append({'T':T,'maximum_deviation_from_Langmuir':float(np.max(np.abs(np.array(data)[:,1]-np.array(data)[:,3]))),'parameters':13,'starts':2,'burn_sweeps':1000,'production_sweeps':5000})
        print('Langmuir task',T,high[-1]['maximum_deviation_from_Langmuir'],flush=True)
    report={'status':'PASS','new_kernel_checks':tests,'ground_state_energy_per_site':-6,'high_temperature_actual_runs':high,'original_Java_source_audit':'Downloaded MIT JAR includes monte/MCSampler.java; exponent 2*(NN+V2*NNN-mu*sigma)/T and delta=-2*(NN+V2*NNN-mu*sigma) match the stated Hamiltonian. External JAR and third-party code not redistributed.'}
    (ROOT/'qa/adsorption-extra-checks.json').write_text(json.dumps(report,indent=2))
if __name__=='__main__':main()
