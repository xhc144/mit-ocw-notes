"""Only newly requested PS1.6(c), PS5.4, PS7.1(b), PS8.1(d) checks."""
from pathlib import Path
import json
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import expm_multiply
from scipy.special import betainc
from scipy.optimize import minimize_scalar

ROOT=Path(__file__).resolve().parents[1]
O=ROOT/'data';Q=ROOT/'qa';Q.mkdir(exist_ok=True)
types=np.loadtxt(O/'public/cSNPsAfricanEuropeanType.dat',comments='%')
edges=np.linspace(0,.5,26);hist_rows=[(edges[:-1]+edges[1:])/2];fits=[]
for pop in [0,1]:
    for typ in [2,3]:
        x=types[types[:,0]==typ,pop+1];y=np.minimum(x,1-x)
        hist=np.histogram(y[(y>0)&(y<.5)],edges)[0]
        hist_rows.append(hist/(hist.sum()*.02))
        fe=edges[1:];counts=np.histogram(y[(y>.02)&(y<.5)],fe)[0]
        def probabilities(alpha):
            pr=np.diff(betainc(alpha,alpha,fe));return pr/pr.sum()
        def nll(alpha):return -np.sum(counts*np.log(np.maximum(probabilities(alpha),1e-300)))
        fit=minimize_scalar(nll,bounds=(.0001,3),method='bounded')
        fits.append({'population':['AD','ED'][pop],'type':int(typ),'polymorphic_retained':int(hist.sum()),'fit_x_interval':[.02,.5],'conditional_symmetric_Beta_alpha':float(fit.x),'alpha_lower_search_limit':.0001,'not_a_reliable_selection_or_population_estimate':True})
np.savetxt(O/'snp-type-density.csv',np.column_stack(hist_rows),delimiter=',',header='x,AD_nonsyn,AD_syn,ED_nonsyn,ED_syn',comments='')
xx=np.linspace(.005,.5,301);models=[]
from scipy.special import beta
for alpha in [.2,1.,2.]:models.append(2*(xx*(1-xx))**(alpha-1)/beta(alpha,alpha))
gamma=-8.;alpha=.2
raw=(xx*(1-xx))**(alpha-1)*(np.exp(gamma*xx)+np.exp(gamma*(1-xx)))
# This selected curve is normalized on the displayed interval only.
models.append(raw/np.trapezoid(raw,xx))
np.savetxt(O/'snp-model-shapes.csv',np.column_stack([xx,*models]),delimiter=',',header='x,alpha02,alpha1,alpha2,selected_gamma_minus8_display_normalized',comments='')

arr=np.genfromtxt(O/'ramachandran-1TEN.csv',delimiter=',',names=True,dtype=None,encoding='utf8')
quadrant=int(np.sum((arr['phi']<0)&(arr['psi']>0)))
restricted=int(np.sum((arr['phi']<0)&(arr['psi']>90)))
assert quadrant==70 and restricted==66
ph=np.loadtxt(O/'purr-random-energy.csv',delimiter=',',skiprows=1)
assert int(ph[:,1].sum())==100000

a,b=2.,1.
times=np.linspace(0,30,301)
def birthdeath(nmax):
    diag=np.full(nmax,-a-b);diag[0]=-a;diag[-1]=-b
    G=diags([np.full(nmax-1,a),diag,np.full(nmax-1,b)],[-1,0,1],format='csr')
    p0=np.zeros(nmax);p0[0]=1.
    P=expm_multiply(G,p0,start=0,stop=30,num=len(times))
    ell=np.arange(1,nmax+1,dtype=float)
    mean=P@ell;var=P@(ell*ell)-mean*mean
    assert np.max(np.abs(P.sum(axis=1)-1))<1e-12 and np.min(P)>-1e-14
    return P,mean,var
P,mean,var=birthdeath(256);P2,m2,v2=birthdeath(512)
error=max(np.max(np.abs(mean-m2)),np.max(np.abs(var-v2)))
assert error<1e-9 and P[:,-1].max()<1e-25
np.savetxt(O/'filament-transient-moments.csv',np.column_stack([times,mean,var,1+(a-b)*times,1+(a-b)*times+b/(a-b),(a+b)*times]),delimiter=',',header='t,mean_ell,variance,free_boundary_mean,large_t_mean,large_t_variance',comments='')
idx=300;ell=np.arange(1,130)
gaussian=np.exp(-(ell-mean[idx])**2/(2*var[idx]))/np.sqrt(2*np.pi*var[idx])
np.savetxt(O/'filament-transient-distribution.csv',np.column_stack([ell,P[idx,:129],gaussian]),delimiter=',',header='ell,exact_t30,Gaussian_central_approximation',comments='')
out={'kind':'new original-data plots and explicitly chosen teaching birth-death model; no new empirical observations','SNP_classification_fits':fits,'ramachandran_regions':{'phi_lt_0_psi_gt_0':quadrant,'phi_lt_0_psi_gt_90':restricted,'degrees':True,'not_DSSP_assignment':True},'PurR_histogram':{'source_csv':'data/purr-random-energy.csv','bins':len(ph),'total_random_sequences':int(ph[:,1].sum())},'filament_time_model':{'a_per_second':a,'b_per_second':b,'initial_length':1,'lower_reflecting_length':1,'upper_caps_tested':[256,512],'max_moment_difference':float(error),'max_upper_boundary_probability':float(P[:,-1].max()),'times_and_moments':[{'t':float(times[i]),'mean':float(mean[i]),'variance':float(var[i])} for i in [0,1,10,50,100,200,300]],'Gaussian_is_only_central_large_time_approximation':True}}
(Q/'remaining-task-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out['filament_time_model'],ensure_ascii=False,indent=2))
