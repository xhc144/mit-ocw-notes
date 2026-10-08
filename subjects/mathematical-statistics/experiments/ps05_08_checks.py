#!/usr/bin/env python3
"""Reproducible numerical checks for MIT18.650 PS5--8 authored solutions.
Numerical checks support calculations; they do not certify proofs. R is not run.
"""
from pathlib import Path
from datetime import datetime, timezone
from itertools import permutations, combinations
import json, math, platform, shutil
import numpy as np
import scipy
from scipy.stats import norm, t

SUBJECT_ROOT = Path(__file__).resolve().parents[1]

SEED = 65007
B = 50000
rng = np.random.default_rng(SEED)
checks = {}

checks['ps05_p02'] = {}
for name, sp2 in [('ML_denominator', 10 * (.22 + .17)/18),
                  ('unbiased_denominator', (.22 + .17)/2)]:
    value = .36 / math.sqrt(sp2 * .2)
    checks['ps05_p02'][name] = dict(pooled_variance=sp2, t=value,
                                   df=18, p_value=float(2*t.sf(value,18)))
checks['ps05_p02']['critical_5_percent'] = float(t.ppf(.975,18))
checks['ps05_p03'] = []
for mean, variance in [(2.41,5.20),(3.28,15.95)]:
    z = 10*(mean-math.sqrt(variance))/math.sqrt(1.5*variance)
    checks['ps05_p03'].append(dict(mean=mean, variance=variance,
                                   z=z, p_value=float(norm.cdf(z))))
checks['ps06_p01'] = []
for n in [50,49]:
    z = math.sqrt(n)*(1-.98)
    checks['ps06_p01'].append(dict(n=n,z=z,p_value=float(norm.sf(z))))
p,q,r = .384,.506,.205
variance = p*(1-p)*q*(1-q)
z = math.sqrt(1000)*(r-p*q)/math.sqrt(variance)
checks['ps06_p03_table'] = dict(p=p,q=q,r=r, covariance=r-p*q,
                               variance=variance,z=z,
                               p_value=float(2*norm.sf(abs(z))))
# Verify Delta-method variance calculation under arbitrary feasible joint laws.
errors = []
for p,q,r in [(.3,.6,.2),(.2,.8,.16),(.5,.5,.1),(.384,.506,.205)]:
    Sigma = np.array([[p*(1-p),r-p*q,r*(1-p)],
                      [r-p*q,q*(1-q),r*(1-q)],
                      [r*(1-p),r*(1-q),r*(1-r)]])
    a = np.array([-q,-p,1.])
    expanded = (q*q*p*(1-p)+p*p*q*(1-q)+r*(1-r)
                +2*p*q*(r-p*q)-2*q*r*(1-p)-2*p*r*(1-q))
    outcomes = np.array([0.,-q,-p,1-p-q])
    probs = np.array([1-p-q+r,p-r,q-r,r])
    direct = probs@outcomes**2-(probs@outcomes)**2
    errors.append(max(abs(a@Sigma@a-expanded),abs(direct-expanded)))
checks['ps06_delta_variance_max_error'] = max(errors)

# KS exact finite computation from sorted merged group labels.
def ks_from_labels(labels,n,m):
    labels=np.asarray(labels)
    return np.max(np.abs(np.cumsum(labels,axis=-1)/n-
                         np.cumsum(1-labels,axis=-1)/m),axis=-1)
def quantile_type1(x, probability):
    return float(np.sort(x)[math.ceil(len(x)*probability)-1])
n,m=20,25
u=rng.random((B,n+m))
labels=(np.argsort(u,axis=1)<n).astype(int)
ks=ks_from_labels(labels,n,m)
checks['ps07_p02_simulation'] = dict(n=n,m=m,B=B,alpha=.05,
                                    quantile_type1=quantile_type1(ks,.95))
small_n,small_m=3,4
ks_exact=[]
for pos in combinations(range(small_n+small_m),small_n):
    lab=np.zeros(small_n+small_m,dtype=int);lab[list(pos)]=1
    ks_exact.append(float(ks_from_labels(lab,small_n,small_m)))
ks_exact=np.asarray(ks_exact)
critical=quantile_type1(ks_exact,.95)
checks['ps07_p02_exact_demo'] = dict(n=small_n,m=small_m,
    permutations=len(ks_exact),critical=critical,
    strict_rejection_probability=float(np.mean(ks_exact>critical)))

# Spearman null: fix first permutation, independently simulate second.
n=10
center=np.arange(1,n+1)-(n+1)/2
den=center@center
perms=np.argsort(rng.random((B,n)),axis=1)+1
spearman=((perms-(n+1)/2)@center)/den
checks['ps07_p03_simulation'] = dict(n=n,B=B,alpha=.05,
    one_sided_quantile=quantile_type1(spearman,.95),
    two_sided_abs_quantile=quantile_type1(abs(spearman),.95),
    mean=float(spearman.mean()),variance=float(spearman.var()),
    exact_null_variance=1/(n-1))
permutation=perms[0]
formula=12*np.arange(1,n+1)@permutation/(n*(n*n-1))-3*(n+1)/(n-1)
direct=float(np.corrcoef(np.arange(1,n+1),permutation)[0,1])
checks['ps07_p03_formula'] = dict(formula=float(formula),direct=direct,
                                absolute_error=abs(float(formula)-direct))
n=5
center=np.arange(1,n+1)-(n+1)/2
den=center@center
spearman_exact=np.asarray([center@(np.asarray(p)-(n+1)/2)/den
                          for p in permutations(range(1,n+1))])
c=quantile_type1(abs(spearman_exact),.95)
checks['ps07_p03_exact_demo'] = dict(n=n,permutations=len(spearman_exact),
    abs_critical=c,strict_rejection_probability=float(np.mean(abs(spearman_exact)>c)),
    mean=float(spearman_exact.mean()),variance=float(spearman_exact.var()),
    symmetry_error=float(np.max(np.abs(np.sort(spearman_exact)+
                                         np.sort(spearman_exact)[::-1]))))

# PS8 fixed-design GLS: numerical normal equations, covariance, and risk identity.
n,p=12,3
X=rng.normal(size=(n,p))
C=rng.normal(size=(n,n));Sigma=C@C.T+.5*np.eye(n)
A=X.T@np.linalg.solve(Sigma,X)
K=np.linalg.solve(A,X.T@np.linalg.inv(Sigma))
beta=np.array([1.,-.5,2.]);Y=X@beta+rng.multivariate_normal(np.zeros(n),Sigma)
betahat=K@Y
checks['ps08_p01_algebra'] = dict(
    normal_equation_error=float(np.max(abs(X.T@np.linalg.solve(Sigma,Y-X@betahat)))),
    covariance_error=float(np.max(abs(K@Sigma@K.T-np.linalg.inv(A)))),
    risk=float(np.trace(np.linalg.inv(A))))
# Check the 2x2 random-design asymptotic covariance formula.
mu,v,sigma2=.7,1.3,2.
M=np.array([[1.,mu],[mu,mu*mu+v]])
manual=sigma2/v*np.array([[mu*mu+v,-mu],[-mu,1.]])
checks['ps08_p02_covariance_error'] = float(np.max(abs(sigma2*np.linalg.inv(M)-manual)))
assert checks['ps06_delta_variance_max_error']<1e-12
assert checks['ps07_p03_formula']['absolute_error']<1e-12
assert checks['ps07_p02_exact_demo']['strict_rejection_probability']<=.05
assert checks['ps07_p03_exact_demo']['strict_rejection_probability']<=.05
assert checks['ps08_p01_algebra']['covariance_error']<1e-12
assert checks['ps08_p01_algebra']['normal_equation_error']<1e-12
assert checks['ps08_p02_covariance_error']<1e-12
record=dict(run_time_utc=datetime.now(timezone.utc).isoformat(),
    python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
    seed=SEED,B=B,R_executable_found=shutil.which('R'),R_run=False,
    scope='Numerical calculations and Monte Carlo/every-permutation checks only; not a proof audit',
    checks=checks)
output=SUBJECT_ROOT / 'experiments' / 'ps05_08_checks-results.json'
output.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False,indent=2))
