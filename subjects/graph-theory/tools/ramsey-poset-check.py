#!/usr/bin/env python3
"""Finite exact checks supplement (and do not replace) a written-proof review."""
from fractions import Fraction
from itertools import combinations, permutations
from math import comb, factorial
import hashlib
import json
import pathlib


def connected(adj, remaining):
    if not remaining:
        return True
    found = 0
    pending = remaining & -remaining
    while pending:
        vbit = pending & -pending
        pending ^= vbit
        if found & vbit:
            continue
        found |= vbit
        pending |= adj[vbit.bit_length() - 1] & remaining & ~found
    return found == remaining


def independent(adj, subset):
    for v in range(len(adj)):
        if subset >> v & 1 and adj[v] & subset:
            return False
    return True


def hamilton(adj):
    n = len(adj)
    for p in permutations(range(1, n)):
        seq = (0,) + p + (0,)
        if all(adj[u] >> v & 1 for u, v in zip(seq, seq[1:])):
            return True
    return False


def graph_checks():
    total = eligible = ramsey5_counterexamples = ramsey6_checked = 0
    for n in range(1, 7):
        allbits = (1 << n) - 1
        edges = list(combinations(range(n), 2))
        for mask in range(1 << len(edges)):
            adj = [0] * n
            for i, (u, v) in enumerate(edges):
                if mask >> i & 1:
                    adj[u] |= 1 << v
                    adj[v] |= 1 << u
            alpha = max(s.bit_count() for s in range(1 << n) if independent(adj, s))
            cw = sum((Fraction(1, a.bit_count() + 1) for a in adj), Fraction())
            assert alpha >= cw
            assert cw >= Fraction(n * n, sum(a.bit_count() + 1 for a in adj))
            total += 1
            if n in (5, 6):
                triangle = any(adj[a] >> b & 1 and adj[a] >> c & 1 and adj[b] >> c & 1
                               for a, b, c in combinations(range(n), 3))
                if n == 5 and not triangle and alpha < 3:
                    ramsey5_counterexamples += 1
                if n == 6:
                    assert triangle or alpha >= 3
                    ramsey6_checked += 1
            if n >= 3 and all(connected(adj, allbits ^ removed)
                              for removed in range(1 << n) if removed.bit_count() < alpha):
                eligible += 1
                assert hamilton(adj), (n, mask, alpha)
    assert ramsey5_counterexamples > 0
    return {"labelled_simple_graphs_n_1_to_6": total,
            "chvatal_erdos_eligible_graphs": eligible,
            "ramsey_3_3_five_vertex_counterexamples": ramsey5_counterexamples,
            "ramsey_3_3_six_vertex_graphs": ramsey6_checked}


def partition_min(valid, n):
    dp = [n + 1] * (1 << n)
    dp[0] = 0
    for mask in range(1, 1 << n):
        bit = mask & -mask
        sub = mask
        while sub:
            if sub & bit and valid[sub]:
                dp[mask] = min(dp[mask], 1 + dp[mask ^ sub])
            sub = (sub - 1) & mask
    return dp[-1]


def matching_size(rel, n):
    states = {0}
    for u in range(n):
        new = set(states)
        for used in states:
            for v in range(n):
                if rel[u] >> v & 1 and not used >> v & 1:
                    new.add(used | 1 << v)
        states = new
    return max(s.bit_count() for s in states)


def poset_checks():
    tested = {}
    for n in range(0, 7):
        pairs = list(combinations(range(n), 2))
        count = 0
        for mask in range(1 << len(pairs)):
            rel = [0] * n
            for k, (i, j) in enumerate(pairs):
                if mask >> k & 1:
                    rel[i] |= 1 << j
            if any(rel[j] & ~rel[i] for i in range(n) for j in range(n) if rel[i] >> j & 1):
                continue
            chains, antichains = [], []
            for subset in range(1 << n):
                vertices = [i for i in range(n) if subset >> i & 1]
                chains.append(all(rel[i] >> j & 1 for i, j in combinations(vertices, 2)))
                antichains.append(all(not rel[i] >> j & 1 for i, j in combinations(vertices, 2)))
            width = max(s.bit_count() for s in range(1 << n) if antichains[s])
            height = max(s.bit_count() for s in range(1 << n) if chains[s])
            assert partition_min(chains, n) == width == n - matching_size(rel, n)
            assert partition_min(antichains, n) == height
            count += 1
        tested[str(n)] = count
    return {"naturally_labelled_posets_by_vertex_count": tested,
            "total_posets_checked": sum(tested.values())}


def increasing_trail_checks():
    n, tested = 4, 0
    edges = list(combinations(range(n), 2))
    for m in range(len(edges) + 1):
        for ordered_edges in permutations(edges, m):
            adj = [[] for _ in range(n)]
            for label, (u, v) in enumerate(ordered_edges):
                adj[u].append((v, label))
                adj[v].append((u, label))
            def extend(v, last_label, used):
                return max([0] + [1 + extend(w, label, used | 1 << label)
                           for w, label in adj[v]
                           if label > last_label and not used >> label & 1])
            longest = max(extend(v, -1, 0) for v in range(n))
            assert n * longest >= 2 * m
            tested += 1
    return {"graphs_and_all_distinct_edge_orderings_on_4_vertices": tested,
            "method": "independent recursive enumeration of actual increasing edge trails"}


def sperner_checks():
    tested = {}
    for n in range(5):
        subsets = list(range(1 << n))
        count = 0
        for f in range(1 << len(subsets)):
            family = [s for s in subsets if f >> s & 1]
            if any(a & b in (a, b) for a, b in combinations(family, 2)):
                continue
            assert sum((Fraction(1, comb(n, s.bit_count())) for s in family), Fraction()) <= 1
            assert len(family) <= comb(n, n // 2)
            count += 1
        tested[str(n)] = count
    return {"boolean_lattice_antichains_by_ground_set_size": tested}


def sequence_checks():
    total = 0
    for n in range(1, 8):
        for seq in permutations(range(n)):
            up = down = 0
            for mask in range(1 << n):
                sub = [seq[i] for i in range(n) if mask >> i & 1]
                if all(a < b for a, b in zip(sub, sub[1:])):
                    up = max(up, len(sub))
                if all(a > b for a, b in zip(sub, sub[1:])):
                    down = max(down, len(sub))
            for r in range(1, n):
                for s in range(1, n):
                    if r * s + 1 <= n:
                        assert up >= r + 1 or down >= s + 1
            total += 1
    return {"distinct_order_types_of_sequences_length_1_to_7": total,
            "method": "enumeration of every subsequence, without LIS/LDS update recurrences"}


if __name__ == "__main__":
    result = {"status": "passed", "limitations": "Finite exact tests are not general proofs.",
              "graphs": graph_checks(), "posets": poset_checks(),
              "increasing_trails": increasing_trail_checks(),
              "sperner_lym": sperner_checks(), "erdos_szekeres": sequence_checks()}
    for k in range(3, 101):
        assert 2 ** (2 + k) < factorial(k) ** 2
    result["ramsey_first_moment_strict_bound_integers_k_3_to_100"] = 98
    result["script_sha256"] = hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(result, ensure_ascii=False, indent=2))
