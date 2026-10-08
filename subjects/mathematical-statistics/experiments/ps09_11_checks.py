#!/usr/bin/env python3
"""Reproducible numerical checks of PS9--11; these do not replace proofs."""
import hashlib
import json
from pathlib import Path
import platform
import sys
import numpy as np
import scipy
from scipy.integrate import quad
from scipy.special import expit, gammaln
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
SEED = 18650911
rng = np.random.default_rng(SEED)
checks = {}

# PS9: exact node risks for every node, correlated interpolation, and simulation.
n, k, noise_var, reps = 120, 24, .49, 20000
x = np.arange(n + 1) / n
truth = np.sin(np.pi * x)
W = np.zeros((n + 1, n + 1))
for i in range(n + 1):
    mask = abs(np.arange(n + 1) - i) <= k
    W[i, mask] = 1 / mask.sum()
sizes = (W > 0).sum(axis=1)
node_mean = W @ truth
node_cov = noise_var * W @ W.T
node_risk = (node_mean - truth)**2 + np.diag(node_cov)
node_bound = np.pi**2*k*k/(n*n) + noise_var/k
assert sizes.min() >= k+1 and sizes.max() <= 2*k+1
assert np.max(node_risk) <= node_bound + 1e-12
Y = truth + np.sqrt(noise_var)*rng.standard_normal((reps, n+1))
hat = Y @ W.T
mc_risk = np.mean((hat-truth)**2, axis=0)
mc_se = np.std((hat-truth)**2, axis=0, ddof=1)/np.sqrt(reps)
assert np.all(abs(mc_risk-node_risk) <= 7*mc_se)

def integrated_mse(z):
    i = min(int(z*n), n-1)
    t = z*n-i
    bias = (1-t)*node_mean[i]+t*node_mean[i+1]-np.sin(np.pi*z)
    var = ((1-t)**2*node_cov[i,i] + t*t*node_cov[i+1,i+1]
           + 2*t*(1-t)*node_cov[i,i+1])
    return bias*bias+var
integrated_risk = sum(quad(integrated_mse, i/n, (i+1)/n)[0] for i in range(n))
integrated_bound = 9*np.pi**2*k*k/(4*n*n)+noise_var/k
assert integrated_risk <= integrated_bound
checks['ps09_regression'] = dict(n=n,k=k,noise_variance=noise_var,repetitions=reps,
    min_window=int(sizes.min()),max_window=int(sizes.max()),
    max_exact_node_risk=float(node_risk.max()),node_bound=float(node_bound),
    max_mc_error_in_standard_errors=float(np.max(abs(mc_risk-node_risk)/mc_se)),
    integrated_exact_risk=integrated_risk,integrated_bound=integrated_bound,
    adjacent_node_covariance=float(node_cov[60,61]))
# Density f(u)=3u^2, u in [0,1], L=6, n=200, h=1/8, x=1/2.
dn, h, z, L = 200, .125, .5, 6.
p = (z+h)**3-(z-h)**3
bias = p/(2*h)-3*z*z
variance = p*(1-p)/(4*dn*h*h)
assert np.isclose(bias,h*h)
assert abs(bias) <= L*h/2 and variance <= L/(2*dn*h)
checks['ps09_density'] = dict(n=dn,h=h,x=z,L=L,probability=p,bias=bias,
    variance=variance,risk=bias*bias+variance,bound=L*L*h*h/4+L/(2*dn*h),
    uniform_boundary_bias=-.5)

# PS10: Jeffreys posterior normalization and first moment; ridge full/singular X.
S, sample_n = 7.5, 6
alpha, rate = sample_n/2, S/2
def ig(t):
    return np.exp(alpha*np.log(rate)-gammaln(alpha)-(alpha+1)*np.log(t)-rate/t)
ig_norm = quad(ig,0,np.inf)[0]
ig_mean = quad(lambda t:t*ig(t),0,np.inf)[0]
assert abs(ig_norm-1) < 1e-9 and abs(ig_mean-S/(sample_n-2)) < 1e-9
checks['ps10_inverse_gamma'] = dict(n=sample_n,S=S,normalization=ig_norm,
    integrated_mean=ig_mean,formula_mean=S/(sample_n-2))
ridge_checks = []
for singular in (False, True):
    X = rng.normal(size=(8,3))
    if singular: X[:,2] = 2*X[:,0]
    beta = np.array([1.,-.5,.75]); lam=.8; sigma2=.7
    A = X.T@X+lam*np.eye(3); C = np.linalg.solve(A,X.T)
    mean = C@X@beta; cov=sigma2*C@C.T
    risk = float(np.sum((mean-beta)**2)+np.trace(cov))
    expression = float(lam**2*beta@np.linalg.solve(A,np.linalg.solve(A,beta))
                       + sigma2*np.trace(np.linalg.solve(A,X.T@X)@np.linalg.inv(A)))
    assert abs(risk-expression) < 1e-10
    draws = X@beta+np.sqrt(sigma2)*rng.normal(size=(reps,8))
    estimates=draws@C.T
    sqerr=np.sum((estimates-beta)**2,axis=1)
    err=float(abs(sqerr.mean()-risk)); se=float(sqerr.std(ddof=1)/np.sqrt(reps))
    assert err < 7*se
    sample = rng.normal(size=(9,3)); B=rng.normal(size=(2,3))
    empirical=np.cov(sample,rowvar=False,bias=True)
    transformed=np.cov(sample@B.T,rowvar=False,bias=True)
    residual=float(np.max(abs(transformed-B@empirical@B.T)))
    assert residual < 1e-10
    ridge_checks.append(dict(singular=singular,rank=int(np.linalg.matrix_rank(X)),
      exact_risk=risk,formula_risk=expression,mc_risk=float(sqerr.mean()),
      mc_error_standard_errors=err/se,covariance_transform_residual=residual))
checks['ps10_ridge_covariance']=ridge_checks

# PS11: numerical integration/summation for all seven explicitly listed families.
p=.37; eta=np.log(p/(1-p)); A=np.logaddexp(0,eta)
ber = [np.exp(eta*t-A) for t in (0,1)]
mu=.8; sigma2=1.6; e1=mu/sigma2; e2=-1/(2*sigma2)
An=.5*np.log(np.pi/(-e2))-e1*e1/(4*e2)
lam=1.7; alpha=2.3; beta=1.7; theta=2.4
Ag=gammaln(alpha)-alpha*np.log(beta)
family_norms={
 'Bernoulli':sum(ber),
 'normal_fixed_variance':quad(lambda t: np.exp(-t*t/2+mu*t-mu*mu/2)/np.sqrt(2*np.pi),-np.inf,np.inf)[0],
 'normal_two_parameters':quad(lambda t:np.exp(e1*t+e2*t*t-An),-np.inf,np.inf)[0],
 'exponential':quad(lambda t:np.exp(-lam*t+np.log(lam)),0,np.inf)[0],
 'uniform':quad(lambda t:1/theta,0,theta)[0],
 'gamma':quad(lambda t:np.exp((alpha-1)*np.log(t)-beta*t-Ag),0,np.inf)[0],
 'Poisson':sum(np.exp(t*np.log(lam)-lam-gammaln(t+1)) for t in range(100)),
}
assert np.allclose(list(family_norms.values()),1,atol=1e-9)
assert np.allclose(ber,[1-p,p])
checks['ps11_seven_family_normalizations']=family_norms
mean=quad(lambda t:t*np.exp((alpha-1)*np.log(t)-beta*t-Ag),0,np.inf)[0]
second=quad(lambda t:t*t*np.exp((alpha-1)*np.log(t)-beta*t-Ag),0,np.inf)[0]
assert abs(mean-alpha/beta)<1e-9 and abs(second-mean*mean-alpha/beta**2)<1e-9
checks['ps11_gamma_moments']=dict(mean=mean,variance=second-mean*mean,
    expected_mean=alpha/beta,expected_variance=alpha/beta**2)
links=[]
for t in (-3.,-.8,0.,.9,3.):
    F=quad(lambda u:np.exp(-abs(u))/(1+np.exp(-abs(u)))**2,-np.inf,t)[0]
    expected=float(expit(t))
    assert abs(F-expected)<1e-9
    recovered=float(np.log(expected/(1-expected)))
    probit=float(norm.ppf(norm.cdf(t)))
    assert abs(recovered-t)<1e-9 and abs(probit-t)<1e-9
    links.append(dict(eta=t,integrated_logistic_cdf=F,logit=recovered,probit=probit))
checks['ps11_links']=links
sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
    for p in [Path(__file__),*[ROOT/f'assignments/ps{i:02}.tex' for i in (9,10,11)]]}
output=dict(status='passed',seed=SEED,python=sys.version.split()[0],
    numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform(),
    note='Actual numerical validation; not a replacement for general mathematical proofs.',
    source_sha256=sources,checks=checks)
out=Path(__file__).with_suffix('.json')
out.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':output['status'],'output':str(out),'check_groups':len(checks)},ensure_ascii=False))
