"""Actual MIT OCW supplied data; no synthetic observations mixed into public files."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.special import betainc,zeta
from scipy.optimize import minimize_scalar
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'data/public';O=ROOT/'data';Q=ROOT/'qa';Q.mkdir(exist_ok=True)
seq=''.join(x.strip().upper() for x in (P/'U00096.fna').read_text().splitlines() if not x.startswith('>'))
assert set(seq)==set('ACGT')
N=len(seq);alphabet='ACGT';idx=np.frombuffer(seq.encode(),dtype=np.uint8);mapping=np.zeros(256,dtype=np.int64)
for i,b in enumerate(alphabet):mapping[ord(b)]=i
x=mapping[idx];freq=np.bincount(x,minlength=4)/N
# Optional original PS1.2 explicitly allows only three forward reading frames.
lengths=[];frame_counts=[]
for off in range(3):
 triple=np.array([seq[i:i+3] for i in range(off,N-2,3)])
 stop=np.flatnonzero(np.isin(triple,['TAA','TAG','TGA']))
 gap=np.diff(stop)-1;lengths.extend(gap.tolist());frame_counts.append({'offset':off,'triplets':len(triple),'stops':len(stop),'complete_intervals':len(gap)})
lengths=np.array(lengths);pstop=freq[3]*freq[0]*freq[0]+freq[3]*freq[0]*freq[2]+freq[3]*freq[2]*freq[0]
rows=[]
for L in range(0,1501,10):rows.append([L,int(np.sum(lengths>=L)),len(lengths)*(1-3/64)**L,len(lengths)*(1-pstop)**L])
np.savetxt(O/'orf-tail.csv',rows,delimiter=',',header='length,observed,equal_background,composition_background',comments='')
cc={};mi=[]
for sep in [1,2,3,6,9,30,100,300,1000]:
 pair=np.bincount(4*x+np.roll(x,-sep),minlength=16).reshape(4,4)/N
 corr=pair/(freq[:,None]*freq[None,:]);I=float(np.sum(pair*np.log2(corr)));mi.append([sep,I,float(np.max(np.abs(corr-1)))])
 cc[str(sep)]={'joint':pair.tolist(),'correlation':corr.tolist(),'mutual_information_bits':I}
np.savetxt(O/'sequence-correlations.csv',mi,delimiter=',',header='separation,mutual_information,max_deviation',comments='')
# Folded frequency histogram. Fixed/absent alleles excluded, and fit ignores x<=.02.
snp=np.loadtxt(P/'cSNPsAfricanEuropean.dat');typed=np.loadtxt(P/'cSNPsAfricanEuropeanType.dat',comments='%');fold=np.minimum(snp,1-snp)
edges=np.linspace(0,.5,26);snpout=[];fit=[]
for c in range(2):
 val=fold[:,c];hist=np.histogram(val[(val>0)&(val<.5)],bins=edges)[0]
 fit_edges=edges[1:];count=np.histogram(val[(val>.02)&(val<.5)],bins=fit_edges)[0]
 def probs(a):
  cdf=betainc(a,a,fit_edges);w=np.diff(cdf);return w/w.sum()
 def nll(a):return -float(np.sum(count*np.log(np.maximum(probs(a),1e-300))))
 opt=minimize_scalar(nll,bounds=(.0001,3),method='bounded',options={'xatol':1e-9});a=float(opt.x);pv=probs(a)
 # Multinomial Pearson diagnostic only; ascertainment and correlated SNPs violate iid calibration.
 expected=count.sum()*pv;chi=float(np.sum((count-expected)**2/expected))
 fit.append({'population':['AD','ED'][c],'alpha_2Nmu_gene_copy_convention':a,'N_naive_mu_1e8':a/2e-8,'n_retained':int(count.sum()),'pearson_statistic_not_calibrated_pvalue':chi,'bins':24,'fit_interval':[.02,.5],'interpretation':'naive binned conditional Beta fit; not a reliable demographic estimate'})
 snpout.append(hist)
np.savetxt(O/'snp-histogram.csv',np.column_stack([(edges[:-1]+edges[1:])/2,*snpout]),delimiter=',',header='x,AD,ED',comments='')
typecount={}
for typ in [1,2,3]:
 a=typed[typed[:,0]==typ,1:];v=np.minimum(a,1-a)
 typecount[str(typ)]={'rows':len(a),'AD_polymorphic':int(np.sum((v[:,0]>0)&(v[:,0]<.5))),'ED_polymorphic':int(np.sum((v[:,1]>0)&(v[:,1]<.5))),'AD_folded_mean_polymorphic':float(np.mean(v[:,0][(v[:,0]>0)&(v[:,0]<.5)])),'ED_folded_mean_polymorphic':float(np.mean(v[:,1][(v[:,1]>0)&(v[:,1]<.5)]))}
# PurR PWM uses .5 pseudocount for EACH base, with measured genome composition background.
sites=[s.strip() for s in (P/'purR_sites.txt').read_text().splitlines() if s.strip()];assert len({len(s) for s in sites})==1
L=len(sites[0]);counts=np.zeros((L,4))
for s in sites:
 for i,b in enumerate(s):counts[i,alphabet.index(b)]+=1
prob=(counts+.5)/(len(sites)+2);W=np.log(prob/freq[None,:]);information=float(np.sum(prob*np.log2(prob/freq)))
train=np.array([sum(W[i,alphabet.index(b)] for i,b in enumerate(s)) for s in sites]);rng=np.random.default_rng(20261012)
rand=rng.choice(4,size=(100000,L),p=freq);score=np.zeros(len(rand))
for i in range(L):score+=W[i,rand[:,i]]
hist,ed=np.histogram(-score,bins=40);np.savetxt(O/'purr-random-energy.csv',np.column_stack([(ed[1:]+ed[:-1])/2,hist]),delimiter=',',header='energy_kT,count',comments='')
rc=seq.translate(str.maketrans('ACGT','TGCA'))[::-1];scans=[];details=[]
for strand,source in [('+',x),('-',mapping[np.frombuffer(rc.encode(),dtype=np.uint8)])]:
 sc=np.zeros(N-L+1)
 for i in range(L):sc+=W[i,source[i:i+len(sc)]]
 scans.append(sc)
 if strand=='+':forward=sc
hit_summary=[]
for delta in [-1.,0.,.5,1.]:
 # E=-score, threshold E mean+.delta => score>mean-delta.
 threshold=float(train.mean()-delta);hits=sum(int(np.sum(sc>threshold)) for sc in scans)
 recovered=sum(float(sum(W[i,alphabet.index(b)] for i,b in enumerate(s)))>threshold and (s in seq or s in rc) for s in sites)
 in_genome=sum(s in seq or s in rc for s in sites)
 hit_summary.append({'threshold_delta_kT':delta,'score_threshold':threshold,'candidate_windows_both_strands':hits,'training_rows_present':in_genome,'training_rows_recovered':recovered,'classification':'unvalidated candidates, not proven false positives'})
# Locations table retained for threshold delta .5; gene association is descriptive only.
threshold=train.mean()-.5
for strand,sc in zip(['+','-'],scans):
 for j in np.flatnonzero(sc>threshold):
  start=int(j+1 if strand=='+' else N-j-L+1);details.append([start,strand,float(sc[j])])
(O/'purr-candidates.csv').write_text('genome_start_1based,strand,score_nats\n'+'\n'.join(f'{a},{b},{c:.8f}' for a,b,c in sorted(details))+'\n')
# Force-induced PS DNA model phase boundary; stable analytic formula at h=0.
phase=[]
for h in np.linspace(0,6,121):
 y=1/(1+zeta(1.5)) if h==0 else np.expm1(2*h/zeta(1.5))/(np.exp(h+2*h/zeta(1.5))-np.exp(-h))*np.exp(h*h/12)
 phase.append([h,y])
np.savetxt(O/'dna-force-boundary.csv',phase,delimiter=',',header='h,w_over_g2_critical',comments='')
res={'kind':'analysis of original MIT public data; original observations not generated here','input_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in P.iterdir()},'genome':{'bases':N,'frequencies_ACGT':freq.tolist(),'p_stop_composition_background':float(pstop),'complete_forward_ORF_intervals':len(lengths),'frames':frame_counts,'tail_at_600':next(r for r in rows if r[0]==600),'correlations':cc},'SNP':{'rows':len(snp),'fit':fit,'types':typecount,'limitations':['ascertainment','frequency rounding','population structure','linked sites','unknown denominator of opportunities for synonymous/non-synonymous']},'PurR':{'sites':len(sites),'length':L,'pseudocount_per_base':.5,'background_ACGT':freq.tolist(),'information_bits':information,'training_score_mean':float(train.mean()),'training_score_min':float(train.min()),'random_score_mean':float(score.mean()),'threshold_scan':hit_summary}}
(Q/'public-data-analysis.json').write_text(json.dumps(res,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in res.items() if k!='input_hashes'},ensure_ascii=False)[:1100]);print('Actual public-data analyses completed.')
