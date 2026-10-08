#!/usr/bin/env python3
"""Finite independent spot checks for graph book chapters 15–16.
These tests cannot prove the theorems, asymptotic claims, or PDF/source compliance.
"""
import itertools, json, math
import numpy as np

TOL = 2e-9
results = {'method': 'Exhaustive labelled simple graphs n<=6; independently computed exact clique/common-neighbor/cut data and NumPy spectral data; selected positive-weight walks and finite-field incidence graphs.'}

def subsets(n):
    return [s for s in range(1 << n)]

def clique_number(n, adj):
    omega = 0
    for s in range(1 << n):
        if s.bit_count() <= omega:
            continue
        if all((adj[v] & s).bit_count() == s.bit_count()-1 for v in range(n) if s >> v & 1):
            omega = s.bit_count()
    return omega

def alpha_number(n, adj):
    return max(s.bit_count() for s in range(1 << n) if all(not (adj[v] & s) for v in range(n) if s >> v & 1))

def common_kst(n, adj, s, t):
    for vs in itertools.combinations(range(n), s):
        common = (1 << n)-1
        for v in vs:
            common &= adj[v]
        if common.bit_count() >= t:
            return True
    return False

def twin_classes(n, adj):
    groups = {}
    for v in range(n):
        groups.setdefault(adj[v], []).append(v)
    return list(groups.values())

def symmetry_test(n, adj):
    groups = twin_classes(n, adj)
    oldscore = sum(len(g)**2 for g in groups)
    oldomega = clique_number(n, adj)
    checks = 0
    for ia, ib in itertools.combinations(range(len(groups)), 2):
        a, b = groups[ia], groups[ib]
        va, vb = a[0], b[0]
        if adj[va] >> vb & 1 or adj[va].bit_count() != adj[vb].bit_count():
            continue
        new = adj.copy()
        amask = sum(1 << v for v in a)
        nb = adj[vb]
        for v in range(n):
            if v in a:
                new[v] = nb
            elif nb >> v & 1:
                new[v] |= amask
            else:
                new[v] &= ~amask
        assert sum(x.bit_count() for x in new) == sum(x.bit_count() for x in adj)
        assert clique_number(n, new) <= oldomega
        assert sum(len(g)**2 for g in twin_classes(n, new)) >= oldscore + 2*len(a)*len(b)
        for g in groups:
            if g != a:
                assert len({new[v] for v in g}) == 1
        checks += 1
    return checks

allgraphs = regulargraphs = cheegergraphs = symmetrychecks = kstgraphs = 0
maxima = {}
max_cheeger_lower_excess = max_cheeger_upper_excess = max_mixing_excess = 0.
for n in range(7):
    pairs = list(itertools.combinations(range(n), 2))
    optimum = {r: 0 for r in range(1,7)}
    indicators = np.array([[float(s >> v & 1) for v in range(n)] for s in range(1, (1 << n)-1)]) if n >= 2 else None
    for mask in range(1 << len(pairs)):
        allgraphs += 1
        adj = [0]*n
        m = mask.bit_count()
        A = np.zeros((n,n))
        for j,(u,v) in enumerate(pairs):
            if mask >> j & 1:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
                A[u,v] = A[v,u] = 1.
        omega = clique_number(n, adj)
        for r in range(1,7):
            if omega <= r:
                optimum[r] = max(optimum[r], m)
        if n <= 5:
            symmetrychecks += symmetry_test(n, adj)
        if n >= 1:
            for s,t in ((2,2),(2,3),(3,2),(3,3)):
                if not common_kst(n, adj, s, t):
                    kstgraphs += 1
                    bound = .5 * (t-1)**(1/s) * n**(2-1/s) + .5*(s-1)*n
                    assert m <= bound+TOL
            if not common_kst(n, adj, 2, 2):
                assert 4*m*m - 2*m*n <= n*n*(n-1)
        if n < 2:
            continue
        degree = A.sum(axis=1)
        if n <= 5 and np.all(degree == degree[0]):
            regulargraphs += 1
            d = degree[0]
            eigen = np.linalg.eigvalsh(A)
            # Remove the constant-vector eigenvalue d (including repeated d).
            other = list(eigen)
            other.pop(int(np.argmax(other)))
            star = max(abs(x) for x in other)
            allind = np.vstack((np.zeros((1,n)), indicators, np.ones((1,n))))
            sizes = allind.sum(axis=1)
            observed = allind @ A @ allind.T
            pred = d*np.outer(sizes,sizes)/n
            rhs = star*np.sqrt(np.outer(sizes*(1-sizes/n), sizes*(1-sizes/n)))
            excess = float(np.max(np.abs(observed-pred)-rhs))
            max_mixing_excess = max(max_mixing_excess, excess)
            assert excess < TOL
            if d > 0:
                tau = float(eigen[0])
                assert tau < 0
                assert alpha_number(n,adj) <= -tau*n/(d-tau)+TOL
            assert abs(np.trace(np.linalg.matrix_power(A,4)) - np.sum(eigen**4)) < TOL
        if np.any(degree == 0):
            continue
        norm = np.sqrt(degree)
        Lap = np.eye(n) - A/np.outer(norm,norm)
        eigen = np.linalg.eigvalsh(Lap)
        if eigen[1] < 1e-8:
            continue
        cheegergraphs += 1
        mu = float(eigen[1])
        volumes = indicators @ degree
        cuts = volumes - np.einsum('ij,ij->i', indicators @ A, indicators)
        eligible = volumes <= degree.sum()/2 + 1e-8
        h = float(np.min(cuts[eligible]/volumes[eligible]))
        max_cheeger_lower_excess = max(max_cheeger_lower_excess, mu/2-h)
        max_cheeger_upper_excess = max(max_cheeger_upper_excess, h-math.sqrt(2*mu))
        assert mu/2 <= h+TOL and h <= math.sqrt(2*mu)+TOL
    for r, observed in optimum.items():
        q,s = divmod(n,r)
        expected = (n*n-s*(q+1)**2-(r-s)*q*q)//2
        assert observed == expected
    maxima[str(n)] = optimum
results.update(labelled_graphs=allgraphs, regular_graphs_mixing_and_hoffman=regulargraphs,
               connected_unweighted_graphs_cheeger=cheegergraphs,
               twin_class_clone_checks=symmetrychecks, forbidden_bipartite_graph_inequality_checks=kstgraphs,
               exact_turan_extrema=maxima, floating_point_tolerance=TOL,
               maximum_mixing_excess=max_mixing_excess,
               maximum_cheeger_lower_excess=max_cheeger_lower_excess,
               maximum_cheeger_upper_excess=max_cheeger_upper_excess)

rng = np.random.default_rng(1821718315)
weightchecks = walkchecks = 0
for n in range(2,9):
    for trial in range(16):
        # A spanning path guarantees connectedness. Additional random edges,
        # integer positive weights, and all-zero diagonals give valid networks.
        C = np.zeros((n,n))
        for u in range(n-1):
            C[u,u+1] = C[u+1,u] = int(rng.integers(1,10))
        for u,v in itertools.combinations(range(n),2):
            if C[u,v] == 0 and rng.random() < .4:
                C[u,v] = C[v,u] = int(rng.integers(1,10))
        degree = C.sum(axis=1)
        pi = degree/degree.sum()
        normalized = np.eye(n)-C/np.sqrt(np.outer(degree,degree))
        mu = float(np.linalg.eigvalsh(normalized)[1])
        sets = np.array([[float(s >> v & 1) for v in range(n)] for s in range(1, (1 << n)-1)])
        volumes = sets @ degree
        cuts = volumes-np.einsum('ij,ij->i', sets @ C,sets)
        eligible = volumes <= degree.sum()/2+1e-8
        h = float(np.min(cuts[eligible]/volumes[eligible]))
        assert mu/2 <= h+TOL and h <= math.sqrt(2*mu)+TOL
        weightchecks += 1
        Q = (np.eye(n)+C/degree[:,None])/2
        decay = max(0.,1-mu/2)
        for t in (0,1,2,5,10):
            Qt = np.linalg.matrix_power(Q,t)
            for s in range(n):
                tv = .5*np.sum(np.abs(Qt[s]-pi))
                bound = .5*math.sqrt(1/pi[s]-1)*(decay**t)
                assert tv <= bound+TOL
                walkchecks += 1
results.update(connected_positive_weight_graphs_cheeger=weightchecks, lazy_walk_start_time_checks=walkchecks)

fieldchecks = []
for q in (2,3,5,7,11):
    points = list(itertools.product(range(q),repeat=2))
    B = np.array([[(y-a*x-b)%q == 0 for a,b in points] for x,y in points],dtype=int)
    assert np.all(B.sum(axis=0)==q) and np.all(B.sum(axis=1)==q)
    assert int(B.sum()) == q**3
    common = B @ B.T
    np.fill_diagonal(common,0)
    assert int(common.max()) <= 1
    fieldchecks.append({'prime':q,'vertices':2*q*q,'edges':q**3,'maximum_common_lines_of_distinct_points':int(common.max())})
results['finite_field_incidence_checks'] = fieldchecks
results['limitations'] = 'Finite checks support boundary/constant verification only; they do not prove the symbolic statements, dense-graph asymptotics, copyright, layout, or deliverable integrity.'
print(json.dumps(results,ensure_ascii=False,indent=2))
