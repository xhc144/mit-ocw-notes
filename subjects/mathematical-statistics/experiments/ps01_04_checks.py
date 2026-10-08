"""Numerical evidence for independently derived PS1--4 solutions; not a proof audit."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar, root_scalar
from scipy.stats import binom, norm

ROOT = Path(__file__).resolve().parents[1]
report = {"seed": 186504, "checks": {}, "source_sha256": {}}
for i in range(1, 5):
    p = ROOT / "assignments" / f"ps{i:02d}.tex"
    report["source_sha256"][str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()

z, x, n = 1.96, .7341, 10000
a = z*z/n
h = math.sqrt(a*x*(1-x)+a*a/4)
intervals = {
    "J1": [x-z/(2*math.sqrt(n)), x+z/(2*math.sqrt(n))],
    "J2": [(x+a/2-h)/(1+a), (x+a/2+h)/(1+a)],
    "J3": [x-z*math.sqrt(x*(1-x)/n), x+z*math.sqrt(x*(1-x)/n)],
}
report["checks"]["ps1_election_intervals"] = {k: {"ends": v, "length": v[1]-v[0]} for k,v in intervals.items()}
report["checks"]["ps1_sample_sizes"] = {
    "J1": math.ceil((z/.05)**2), "J2": math.ceil((z/.05)**2-z*z),
    "J2_worst_length_n1532": z/math.sqrt(1532+z*z),
    "J2_worst_bound_n1533": z/math.sqrt(1533+z*z),
}
# Exact finite-n enumeration illustrates that the text claims asymptotic coverage.
k = np.arange(n+1)
y = k/n
prob = binom.pmf(k, n, x)
cover1 = np.abs(y-x) <= z/(2*math.sqrt(n))
cover2 = np.abs(y-x) <= z*math.sqrt(x*(1-x)/n)
cover3 = np.abs(y-x) <= z*np.sqrt(y*(1-y)/n)
report["checks"]["ps1_finite_n_coverages_at_p7341"] = {
    name: float(prob[mask].sum()) for name, mask in zip(["J1", "J2", "J3"], [cover1,cover2,cover3])
}
# Check scalar likelihood maximizers by optimizing likelihoods, independently of their score roots.
xs = np.array([1.2, 1.7, 2.5, 3.1])
u = np.array([.12, .31, .67, .84])
tau = 1.3
models = [
    ("Pareto_shape", lambda t: len(xs)*np.log(t)-t*np.log(xs).sum(), len(xs)/np.log(xs).sum()),
    ("sqrt_theta_density", lambda t: len(u)*np.log(np.sqrt(t))+(np.sqrt(t)-1)*np.log(u).sum(), (-len(u)/np.log(u).sum())**2),
    ("Rayleigh_scale", lambda t: -2*len(xs)*np.log(t)-np.square(xs).sum()/(2*t*t), np.sqrt(np.square(xs).mean()/2)),
    ("Weibull_rate", lambda t: len(xs)*np.log(t)-t*np.power(xs,tau).sum(), len(xs)/np.power(xs,tau).sum()),
    ("N_theta_theta", lambda t: -.5*len(xs)*np.log(t)-np.square(xs-t).sum()/(2*t), (np.sqrt(1+4*np.square(xs).mean())-1)/2),
]
likelihood_checks = {}
for name, ll, analytic in models:
    opt = minimize_scalar(lambda t: -ll(t), bounds=(.0001,100), method="bounded", options={"xatol":1e-11})
    err = abs(float(opt.x)-float(analytic))
    assert opt.success and err < 2e-6, (name, err)
    likelihood_checks[name] = {"analytic": float(analytic), "optimized": float(opt.x), "abs_error": err}
report["checks"]["ps3_likelihood_optimization"] = likelihood_checks
# A direct KL expectation integral, and direct TV density integrations on each sign region.
a_mu,b_mu,v = 1.2,-.4,2.3
kl_int = quad(lambda t: norm.pdf(t,loc=a_mu,scale=math.sqrt(v))*((t-b_mu)**2-(t-a_mu)**2)/(2*v), -np.inf,np.inf)[0]
kl_formula = (a_mu-b_mu)**2/(2*v)
assert abs(kl_int-kl_formula) < 1e-9
s,t = 1.7,4.2
tv_int = .5*(quad(lambda q: abs(1/s-1/t),0,s)[0]+quad(lambda q: 1/t,s,t)[0])
assert abs(tv_int-(1-s/t)) < 1e-12
report["checks"]["ps3_divergence_integration"] = {"normal_KL_integral": kl_int,"normal_KL_formula":kl_formula,"uniform_TV_integral":tv_int,"uniform_TV_formula":1-s/t}
# Integrate Gaussian score outer products to verify parameterization by variance, not standard deviation.
mu,v = .8,1.6
score_mu = lambda t:(t-mu)/v
score_v = lambda t:-1/(2*v)+(t-mu)**2/(2*v*v)
f = lambda t:norm.pdf(t,loc=mu,scale=math.sqrt(v))
I = [[quad(lambda t: f(t)*a(t)*b(t),-np.inf,np.inf)[0] for b in [score_mu,score_v]] for a in [score_mu,score_v]]
assert np.allclose(I,np.diag([1/v,1/(2*v*v)]),atol=1e-10)
report["checks"]["ps4_normal_Fisher_quadrature"] = I
# Positive design root and its global information maximum.
root = root_scalar(lambda u:u-2*(1-math.exp(-u)),bracket=(1,2),xtol=1e-13).root
opt = minimize_scalar(lambda u:-u*u/math.expm1(u),bounds=(.0001,10),method="bounded")
ratio = root*root/math.expm1(root)
assert abs(root-float(opt.x))<2e-6
report["checks"]["ps4_threshold_design"] = {"lambda_z_positive_root":root,"root_residual":root-2*(1-math.exp(-root)),"numerical_information_maximizer":float(opt.x),"maximum_information_ratio":ratio}
# Reproducible simulations are supporting checks, not replacements for the proofs.
rng = np.random.default_rng(report["seed"])
uniform_rows = []
for nn in [5,20,100]:
    # The maximum's exact inverse CDF avoids unnecessary generation of nn full observations.
    maxima = 2*rng.random(50000)**(1/nn)
    exact_upper = maxima/.05**(1/nn)
    approx_upper = maxima/(1-math.log(20)/nn)
    uniform_rows.append({"n":nn,"exact_interval_empirical_coverage":float(np.mean(exact_upper>=2)),"asymptotic_interval_empirical_coverage":float(np.mean(approx_upper>=2)),"asymptotic_interval_exact_coverage":1-(1-math.log(20)/nn)**nn})
report["checks"]["ps2_uniform_interval_simulation"] = uniform_rows
lam,zz,nn = .7,root/.7,2000
pp = math.exp(-lam*zz)
fractions = rng.binomial(nn,pp,60000)/nn
assert np.all(fractions>0)
estimates = -np.log(fractions)/zz
emp_var = float(nn*np.var(estimates,ddof=1))
theory = math.expm1(lam*zz)/(zz*zz)
assert abs(emp_var/theory-1)<.04
report["checks"]["ps4_delta_method_simulation"] = {"lambda":lam,"threshold":zz,"n":nn,"replications":len(estimates),"mean_estimator":float(np.mean(estimates)),"n_times_empirical_variance":emp_var,"asymptotic_variance":theory,"variance_ratio":emp_var/theory}
report["status"] = "all stated numerical assertions passed; not a proof or visual audit"
out = Path(__file__).with_name("ps01_04_results.json")
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":report["status"],"result_file":str(out),"threshold_design":report["checks"]["ps4_threshold_design"]},ensure_ascii=False))
