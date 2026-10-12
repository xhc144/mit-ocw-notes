"""Reproducible teaching-model checks for original-course foundation bridges."""
from pathlib import Path
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
(ROOT / 'qa').mkdir(exist_ok=True)
p = .3
genotypes = np.array([p*p, 2*p*(1-p), (1-p)**2])
assert np.isclose(genotypes.sum(), 1) and np.isclose(genotypes[0]+genotypes[1]/2, p)
N = 50
expected_heterozygosity = (1-1/(2*N))*2*p*(1-p)
w = np.array([1.2, 1.1, 1.0])
weighted = genotypes*w
ps = (weighted[0]+weighted[1]/2)/weighted.sum()
selection_formula = p*(1-p)*(p*(w[0]-w[1])+(1-p)*(w[1]-w[2]))/weighted.sum()
assert np.isclose(ps-p, selection_formula)

f = np.array([.7, .3])
M = np.array([[1-.005/f[0], .005/f[0]], [.005/f[1], 1-.005/f[1]]])
assert np.allclose(M.sum(axis=1), 1) and np.allclose(f@M, f)
assert np.isclose(np.sum(f*(1-M.diagonal())), .01)
pam = {}
for n in [1, 100, 250, 1000]:
    Mn = np.linalg.matrix_power(M, n)
    Q = f[:,None]*Mn
    assert np.allclose(Q, Q.T)
    pam[str(n)] = {'matrix': Mn.tolist(), 'observed_difference_probability': float(1-np.trace(Q)), 'natural_log_odds': np.log(Mn/f[None,:]).tolist()}

recruitment = []
for c in [0., 1.]:
    for r in [0., 100.]:
        polymerase = .1
        omega = 20.
        weights = np.array([1., polymerase, c, r, r*c, omega*c*polymerase])
        enumerated = (weights[1]+weights[5])/weights.sum()
        formula = polymerase*(1+omega*c)/((1+r)*(1+c)+polymerase*(1+omega*c))
        assert np.isclose(enumerated, formula)
        recruitment.append({'p': polymerase, 'c': c, 'r': r, 'omega': omega, 'polymerase_occupation': float(formula)})

v0, ap, am = 1., .2, .8
def cumulant(k):
    L = np.array([[-ap+v0*k, am], [ap, -am-v0*k]])
    return np.linalg.eigvals(L).real.max()
eps = 1e-4
drift = v0*(am-ap)/(ap+am)
diffusion = 4*v0*v0*ap*am/(ap+am)**3
numeric_drift = (cumulant(eps)-cumulant(-eps))/(2*eps)
numeric_diffusion = (cumulant(eps)-2*cumulant(0)+cumulant(-eps))/(2*eps*eps)
assert abs(numeric_drift-drift)<1e-7 and abs(numeric_diffusion-diffusion)<1e-7
out = {'data_kind': 'explicitly specified teaching models, not empirical biological measurements', 'hardy_weinberg': {'p': p, 'genotype_probabilities': genotypes.tolist(), 'N_diploid': N, 'expected_next_heterozygosity': expected_heterozygosity, 'fitness': w.tolist(), 'after_selection_p': float(ps)}, 'PAM_two_symbol_demonstration': {'background_f': f.tolist(), 'accepted_changes_per_step': .01, 'powers': pam}, 'lac_multistate_enumeration': recruitment, 'run_tumble_one_dimensional_model': {'v0': v0, 'alpha_plus': ap, 'alpha_minus': am, 'drift': drift, 'D': diffusion, 'tilted_generator_numeric_drift': float(numeric_drift), 'tilted_generator_numeric_D': float(numeric_diffusion)}}
(ROOT/'qa/foundation-checks.json').write_text(json.dumps(out, ensure_ascii=False, indent=2))
print('Foundation models: HW/selection, PAM powers, promoter state enumeration and run-tumble cumulants checked.')
