"""Targeted Binder uncertainty and high-field completion of the Lab5 survey."""
from pathlib import Path
import json,time
import numpy as np
from phase_diagram import wolff_zero_field,sample,blocks
ROOT=Path(__file__).resolve().parents[1];started=time.time();rows=[]
for L in [8,12,16,24,32]:
    for T in [7.8,8.0,8.1,8.2,8.3,8.4,8.6]:
        batch=[]
        for repeat in range(3):
            val=wolff_zero_field(L,T,1000,10000,20261012+L*100000+int(T*1000)+repeat*10000000)
            batch.extend(val.reshape(20,-1,3).mean(axis=1))
        batch=np.array(batch);mean=batch.mean(axis=0);binder=1-mean[2]/(3*mean[1]**2)
        jack=(batch.sum(axis=0)[None,:]-batch)/(len(batch)-1)
        bj=1-jack[:,2]/(3*jack[:,1]**2)
        u=np.sqrt((len(batch)-1)*np.mean((bj-bj.mean())**2))
        rows.append([L,T,mean[0],binder,u])
    print('Refined Binder',L,'seconds',round(time.time()-started,1),flush=True)
np.savetxt(ROOT/'data/adsorption-binder-refined.csv',rows,delimiter=',',header='L,T,abs_staggered,binder,u_binder_jackknife',comments='')
extension=[]
for T,fields in [(3.,[10.,12.]),(4.,[10.,12.,16.]),(6.,[10.,12.,18.,24.]),(8.,[10.,12.,16.,24.,32.]),(10.,[10.,12.,16.,20.,30.,40.]),(12.,[10.,12.,16.,24.,36.,48.])]:
    for mu in fields:
        v,h=sample(24,T,mu,1000,3000,20261012+int(T*10000+mu*100),0);mean,err=blocks(v)
        theta=(1+mean[0])/2
        extension.extend([[T,theta,mean[1],0.],[T,1-theta,mean[1],0.]])
path=ROOT/'data/adsorption-phase-plot.csv';old=np.loadtxt(path,delimiter=',',skiprows=1)
np.savetxt(path,np.vstack([old,extension]),delimiter=',',header='T,theta,order,unresolved',comments='')
hist=np.loadtxt(ROOT/'data/adsorption-coexistence-histograms.csv',delimiter=',',skiprows=1)
grid=np.arange(51)/50.;cols=[grid]
for T in [1.,2.,4.]:
    data=hist[(hist[:,1]==T)&(hist[:,2]==4.)];counts=np.zeros(51)
    for row in data:counts[int(round(row[4]*50))]+=row[5]
    cols.append(counts/counts.sum())
np.savetxt(ROOT/'data/adsorption-coexistence-plot.csv',np.column_stack(cols),delimiter=',',header='theta_bin,T1_mu4,T2_mu4,T4_mu4',comments='')
j={'kind':'actual new simulation refinements, not H/Pd experiment','critical_sizes':[8,12,16,24,32],'critical_T':[7.8,8.,8.1,8.2,8.3,8.4,8.6],'independent_seeds_per_critical_point':3,'burn_clusters':1000,'production_clusters':10000,'uncertainty':'delete-one-block jackknife over60 blocks, remains finite-time correlation diagnostic','high_field_completion_L':24,'high_field_temperatures':[3,4,6,8,10,12],'negative_mu_side':'exact spin inversion symmetry, not independent data','wall_seconds':time.time()-started,'coexistence_histogram':'existing completed field survey, combined two starts, bin51 at theta=1 is endpoint mass'}
(ROOT/'qa/adsorption-phase-refinement.json').write_text(json.dumps(j,ensure_ascii=False,indent=2));print('Refinement finished',flush=True)
