#!/usr/bin/env python3
"""Read-only finite checks for the authored 6.042J graph exercise draft.

These checks complement mathematical proofs; they are not independent model
review, and they do not compile or visually inspect the book.
"""
from collections import deque
from fractions import Fraction as F
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json
import math
import re

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
RESULTS = {}


def undirected(pairs):
    return {frozenset(x) for x in pairs}


def adj(V, E):
    return {v: {next(iter(e - {v})) for e in E if v in e} for v in V}


def closure(V, E):
    r = {v: {b for a, b in E if a == v} for v in V}
    for _ in V:
        for v in V:
            r[v] |= set().union(*(r[w] for w in tuple(r[v]))) if r[v] else set()
    return r


def min_terms(V, E, cap):
    preds = {v: {a for a, b in E if b == v} for v in V}
    q, seen = deque([(frozenset(), [])]), {frozenset()}
    while q:
        done, schedule = q.popleft()
        if len(done) == len(V):
            return schedule
        available = [v for v in V if v not in done and preds[v] <= done]
        for batch in combinations(available, min(cap, len(available))):
            new = done | frozenset(batch)
            if new not in seen:
                seen.add(new)
                q.append((new, schedule + [batch]))
    raise AssertionError('DAG not schedulable')


def stable(M, boys, girls):
    inv = {g: b for b, g in M.items()}
    return not any(
        boys[b].index(g) < boys[b].index(M[b])
        and girls[g].index(b) < girls[g].index(inv[g])
        for b in boys for g in girls
    )


# Coverage is checked against the already frozen source inventory, not against
# a count invented by this script.
inventory = json.loads((ROOT / 'subjects/graph-theory/qa/assessments-inventory-6042.json').read_text())
online_index = json.loads((ROOT / 'sources/graph-theory/assessments/6042/online-feedback-index.json').read_text())
text = '\n'.join(p.read_text() for p in sorted(HERE.glob('*.tex')))
labels = re.findall(r'\\label\{([^}]+)\}', text)
assert len(labels) == len(set(labels)), 'duplicate labels'
pdf_map = []
for item in inventory['pdf_files']:
    code = item['filename'].removeprefix('MIT6_042JS15_').removesuffix('.pdf')
    if code == 'cp32':
        continue
    code = {'midterm3': 'mt3', 'finalexam': 'final'}.get(code, code)
    for question in item['questions']:
        if question['scope'] == 'graph-theory':
            assert hashlib.sha256((ROOT / item['local_path']).read_bytes()).hexdigest() == item['sha256']
            label = f"mit:6042-{code}-q{question['id']}"
            assert label in labels, label
            pdf_map.append({'label': label, 'source': item['filename'], 'problem': question['id'],
                            'physical_start_page': question['physical_start_page'],
                            'answer_units': question['top_level_answer_unit_count'],
                            'letters': question['explicit_top_level_subquestion_labels']})
assert len(pdf_map) == 50
assert sum(x['answer_units'] for x in pdf_map) == 147
online_map = []
for item in online_index:
    if item.get('scope') != 'graph-theory':
        continue
    assert hashlib.sha256((ROOT / item['local_path']).read_bytes()).hexdigest() == item['sha256']
    for image in item.get('images', []):
        assert hashlib.sha256((ROOT / image['local_path']).read_bytes()).hexdigest() == image['sha256']
    title = item['title'].replace(' [optional]', '').replace('&', 'and')
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    for qid in item['question_ids']:
        label = f"mit:6042-online-{slug}-{qid.lower()}"
        assert label in labels, label
        online_map.append({'title': item['title'], 'qid': qid, 'label': label,
                           'html_path': item['local_path'], 'html_sha256': item['sha256'],
                           'historical_url': item['official_url_historical']})
assert len(online_map) == 75
assert text.count('\\begin{exercise}') == text.count('\\end{exercise}') == 86
assert text.count('\\begin{solution}') == text.count('\\end{solution}') == 86
for i in range(1, 6):
    assert f'mit:6042-cp32-q{i}' in labels
RESULTS['coverage'] = {'pdf_questions': 50, 'pdf_answer_units': 147,
                       'online_pages': 36, 'online_answer_units': 75,
                       'cp32_aliases': 5, 'native_exercises': 86}

# PS7 source graphs and an explicit edge-preserving isomorphism.
G1 = undirected([(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 6), (2, 9),
                 (3, 7), (4, 10), (5, 8), (6, 7), (7, 8), (8, 9), (9, 10), (10, 6)])
G4 = undirected([(i, i + 1) for i in range(1, 9)]
                + [(9, 1), (1, 10), (4, 10), (7, 10), (9, 5), (2, 6), (8, 3)])
mapping = dict(zip(range(1, 11), [1, 2, 3, 4, 10, 9, 8, 7, 6, 5]))
assert {frozenset(mapping[v] for v in e) for e in G1} == G4
assert not any(undirected(zip(c, c[1:] + c[:1])) <= G1 for c in permutations(range(1, 11), 4))
RESULTS['ps7_isomorphism'] = {'G1_G4': 'explicit mapping verified', 'G1_four_cycles': 0}

# PS8: check the source PDF's actual vector edges, the relettering, triangle
# absence, displayed 4-colouring and exhaustive impossibility of 3-colouring.
import fitz
page = fitz.open(ROOT / 'sources/graph-theory/assessments/6042/originals/MIT6_042JS15_ps8.pdf')[0]
positions = []
for drawing in page.get_drawings():
    fill = drawing['fill']
    if fill and fill[0] > 0.5 and fill[1] < 0.1:
        rect = drawing['rect']
        positions.append(((rect.x0 + rect.x1) / 2, (rect.y0 + rect.y1) / 2))
assert len(positions) == 11
actual_edges = set()
for drawing in page.get_drawings():
    for item in drawing['items']:
        if item[0] != 'l':
            continue
        a, b = item[1:]
        ia = min(range(11), key=lambda i: math.dist(positions[i], a))
        ib = min(range(11), key=lambda i: math.dist(positions[i], b))
        if ia != ib and math.dist(positions[ia], a) < 3 and math.dist(positions[ib], b) < 3:
            actual_edges.add(frozenset((ia, ib)))
# v_i occupy source positions 0..4, u_i positions 7,6,5,9,8; w position10.
point_map = [0, 1, 2, 3, 4, 7, 6, 5, 9, 8, 10]
mycielski = undirected([(i, (i + 1) % 5) for i in range(5)]
                       + [(5 + i, (i - 1) % 5) for i in range(5)]
                       + [(5 + i, (i + 1) % 5) for i in range(5)]
                       + [(10, 5 + i) for i in range(5)])
assert {frozenset(point_map[x] for x in e) for e in mycielski} == actual_edges
assert not any(undirected(combinations(c, 2)) <= mycielski for c in combinations(range(11), 3))
col = [1, 2, 1, 2, 3] * 2 + [4]
assert all(len({col[x] for x in e}) == 2 for e in mycielski)
A = adj(range(11), mycielski)
order = sorted(A, key=lambda v: -len(A[v]))


def three_color(i, assigned):
    if i == len(order):
        return True
    v = order[i]
    for color in range(3):
        if all(assigned.get(w) != color for w in A[v]):
            assigned[v] = color
            if three_color(i + 1, assigned):
                return True
            del assigned[v]
    return False


assert not three_color(0, {})
RESULTS['ps8_source_graph'] = {'actual_vector_edges': 20, 'source_relettering': 'equal',
                              'triangles': 0, 'four_coloring': 'verified', 'three_coloring': 'impossible by exhaustive search'}

# The partial-preference example is stable for every one of its 256 completions.
for choices in product((0, 1), repeat=8):
    def pair(a, b, reverse):
        return [b, a] if reverse else [a, b]
    boys = {0: [0, 1] + pair(2, 3, choices[0]),
            1: [1, 0] + pair(2, 3, choices[1]),
            2: pair(0, 1, choices[2]) + [3, 2],
            3: pair(0, 1, choices[3]) + [2, 3]}
    girls = {0: [1, 0] + pair(2, 3, choices[4]),
             1: [0, 1] + pair(2, 3, choices[5]),
             2: pair(0, 1, choices[6]) + [2, 3],
             3: pair(0, 1, choices[7]) + [3, 2]}
    for matches in ([0, 1, 2, 3], [1, 0, 2, 3], [0, 1, 3, 2]):
        assert stable(dict(enumerate(matches)), boys, girls)
boys = {i: [(i + j) % 3 for j in range(3)] for i in range(3)}
girls = {i: [(i + j) % 3 for j in (1, 2, 0)] for i in range(3)}
assert all(stable({i: (i + s) % 3 for i in range(3)}, boys, girls) for s in range(3))
RESULTS['ps8_stability'] = {'partial_completions': 256, 'displayed_matchings_each': 3, 'odd_three_person_gadget': 3}

# Exhaust all the auxiliary colourings, proving the actual source gadget tables
# have the claimed outputs rather than merely testing a chosen assignment.
gate = [('T', 'F'), ('T', 'N'), ('F', 'N'), ('N', 'P'), ('N', 'Q'), ('N', 'O'),
        ('T', 'x'), ('x', 'O'), ('x', 'z'), ('O', 'u'), ('O', 'v'), ('u', 'v'),
        ('u', 'P'), ('v', 'Q'), ('P', 'z'), ('Q', 'z')]
for kind in ('OR', 'AND'):
    edges = gate if kind == 'OR' else [('F' if a == 'T' and b == 'x' else a, b) for a, b in gate]
    for p, q in product('TF', repeat=2):
        outputs = set()
        for values in product('TFN', repeat=5):
            colors = dict(zip(('O', 'u', 'v', 'x', 'z'), values))
            colors.update(T='T', F='F', N='N', P=p, Q=q)
            if all(colors[a] != colors[b] for a, b in edges):
                outputs.add(colors['O'])
        expected = ('T' if 'T' in (p, q) else 'F') if kind == 'OR' else ('T' if p == q == 'T' else 'F')
        assert outputs == {expected}
RESULTS['logic_gadget'] = 'all eight OR/AND input cases exhaustively verified'

# Check every arc of the three explicit cube path families, not only their
# claimed lengths or common endpoints.
cube_paths = {
    '100': ['000 100', '000 010 110 100', '000 001 101 100'],
    '110': ['000 100 110', '000 010 110', '000 001 011 111 110'],
    '111': ['000 100 110 111', '000 010 011 111', '000 001 101 111'],
}
for target, strings in cube_paths.items():
    paths = [s.split() for s in strings]
    for path in paths:
        assert path[0] == '000' and path[-1] == target
        assert len(path) == len(set(path))
        assert all(sum(x != y for x, y in zip(a, b)) == 1 for a, b in zip(path, path[1:]))
    assert all(not set(a[1:-1]) & set(b[1:-1]) for a, b in combinations(paths, 2))
RESULTS['cube_path_families'] = 'all nine displayed paths adjacent and internally disjoint'

# Source-weighted grid: compute the actual Prim choices and Kruskal result from
# exact rational weights, checking the displayed edge list and total weight.
grid = [(i, j) for i in range(4) for j in range(4)]
grid_edges = {}
for i in range(3):
    for j in range(4):
        grid_edges[f'h{i}{j}'] = ((i, j), (i + 1, j), F(4 * i + j, 100))
        grid_edges[f'v{j}{i}'] = ((j, i), (j, i + 1), 1 + F(i + 4 * j, 100))
tree_vertices, prim = {(1, 2)}, []
while len(tree_vertices) < 16:
    name = min((name for name, (u, v, weight) in grid_edges.items()
                if (u in tree_vertices) != (v in tree_vertices)), key=lambda name: grid_edges[name][2])
    u, v, _ = grid_edges[name]
    tree_vertices.update((u, v))
    prim.append(name)
assert prim == ['h02', 'h12', 'h22', 'v01', 'h01', 'h11', 'h21', 'v00',
                'h00', 'h10', 'h20', 'v02', 'h03', 'h13', 'h23']
parts, kruskal = [{v} for v in grid], []
for name in sorted(grid_edges, key=lambda name: grid_edges[name][2]):
    u, v, _ = grid_edges[name]
    left = next(part for part in parts if u in part)
    right = next(part for part in parts if v in part)
    if left is not right:
        parts.remove(left)
        parts.remove(right)
        parts.append(left | right)
        kruskal.append(name)
assert set(prim) == set(kruskal)
assert sum(grid_edges[name][2] for name in prim) == F(369, 100)
RESULTS['cp21_grid_mst'] = {'prim_sequence': prim, 'kruskal_same_edges': True, 'exact_weight': '369/100'}

# Check register interference as an independent consequence of the displayed
# live sets, together with the actual register partition.
live_sets = [set('ab'), set('ac'), set('acd'), set('acde'), set('adf'), set('dfg'), set('dgh')]
interference = set().union(*(undirected(combinations(s, 2)) for s in live_sets))
assert interference == undirected([tuple(e) for e in ['ab', 'ac', 'ad', 'cd', 'ae', 'ce', 'de', 'af', 'df', 'dg', 'fg', 'dh', 'gh']])
registers = [set('ag'), set('bcfh'), set('d'), set('e')]
assert all(not any(e <= register for e in interference) for register in registers)
assert undirected(combinations('acde', 2)) <= interference
RESULTS['register_allocation'] = {'live_set_edges': 13, 'displayed_four_register_partition': 'proper', 'lower_bound_clique': 'acde'}

# Longest subsequences: enumerate all actual subsequences, not arbitrary sets.
sequence = [6, 4, 7, 9, 1, 2, 5, 3, 8]
expected = {1: [(1, 2, 5, 8), (1, 2, 3, 8)],
            -1: [(6, 4, 1), (6, 4, 2), (6, 4, 3), (6, 5, 3), (7, 5, 3), (9, 5, 3)]}
for direction in (1, -1):
    longest = []
    for length in range(1, 10):
        valid = [c for c in combinations(sequence, length)
                 if all(direction * a < direction * b for a, b in zip(c, c[1:]))]
        if valid:
            longest = valid
    assert set(longest) == set(expected[direction])
RESULTS['cp18_subsequences'] = {'all_longest_increasing': 2, 'all_longest_decreasing': 6}

# Midterm DAG: enumerate all size-three antichains to check the word 'two'.
Vexam = list('ABCDEFGH')
Eexam = [tuple(e) for e in ('AD', 'DE', 'BE', 'BF', 'CF', 'EG', 'FH')]
Cexam = closure(Vexam, Eexam)
exam_antichains = [c for c in combinations(Vexam, 3)
                  if all(v not in Cexam[u] and u not in Cexam[v] for u, v in combinations(c, 2))]
assert exam_antichains == [('A', 'B', 'C'), ('B', 'C', 'D')]
assert len(min_terms(Vexam, Eexam, 2)) == 4
RESULTS['mt3_dag'] = {'maximum_antichains': [list(c) for c in exam_antichains], 'two_person_schedule': 4}

# CP17 and online scheduling are intentionally different prerequisite tables.
V = ['18.01', '8.01', '6.001', '6.042', '18.02', '18.03', '8.02', '6.034',
     '6.046', '6.002', '6.003', '6.004', '6.840', '6.033', '6.857']
E = [('18.01', v) for v in ('6.042', '18.02', '18.03')]
E += [('6.046', '6.840'), ('8.01', '8.02'), ('6.001', '6.034'), ('6.042', '6.046')]
E += [(v, '6.002') for v in ('18.03', '8.02')]
E += [(v, w) for v in ('6.001', '6.002') for w in ('6.003', '6.004')]
E += [('6.004', '6.033'), ('6.033', '6.857')]
C = closure(V, E)
five = [c for c in combinations(V, 5) if '18.03' not in c and all(v not in C[u] and u not in C[v] for u, v in combinations(c, 2))]
assert len(five) == 9
assert len(min_terms(V, E, 2)) == 8 and len(min_terms(V, E, 3)) == 6
RESULTS['cp17_schedule'] = {'five_antichains_without_1803': 9, 'two_per_term': 8, 'three_per_term': 6}
V = ['18.01', '18.02', '18.03', '8.01', '8.02', '6.01', '6.042', '6.046', '6.02', '6.006', '6.034', '6.004']
E = [('18.01', v) for v in ('6.042', '18.02', '18.03')]
E += [('8.01', v) for v in ('8.02', '6.01')]
E += [('6.042', v) for v in ('6.046', '6.006')]
E += [(v, '6.02') for v in ('18.02', '18.03', '8.02', '6.01')]
E += [('6.01', v) for v in ('6.006', '6.034')] + [('6.02', '6.004')]
C = closure(V, E)
six = [c for c in combinations(V, 6) if all(v not in C[u] and u not in C[v] for u, v in combinations(c, 2))]
assert six and not any(all(v not in C[u] and u not in C[v] for u, v in combinations(c, 2)) for c in combinations(V, 7))
RESULTS['online_schedule_corrigendum'] = {'official_Q4': 5, 'actual_width': 6, 'six_antichain': list(six[0])}

# Direct enumeration of all 64 four-vertex random graphs confirms CP30's two
# non-independent examples exactly, without relying on rounded arithmetic.
edges = list(combinations(range(4), 2))
counts = [0] * 5
for bits in product((0, 1), repeat=6):
    selected = undirected(e for e, bit in zip(edges, bits) if bit)
    def p(a, b):
        return any(frozenset((a, k)) in selected and frozenset((k, b)) in selected
                   for k in range(4) if k not in (a, b))
    a, b, c = p(0, 1), p(1, 2), p(2, 3)
    for i, value in enumerate((a, b, c, a and b, a and c)):
        counts[i] += value
assert counts == [28, 28, 28, 17, 20]
RESULTS['cp30_random_graph_enumeration'] = {'graphs': 64, 'event_counts': counts}

# Rational stationary equations for all source walk matrices.
walks = [([[0, 1], [1, 0]], [F(1, 2), F(1, 2)]),
         ([[0, 1], [F(9, 10), F(1, 10)]], [F(9, 19), F(10, 19)]),
         ([[1, 0, 0, 0], [F(1, 2), 0, F(1, 2), 0], [0, F(1, 2), 0, F(1, 2)], [0, 0, 0, 1]], [F(2, 7), 0, 0, F(5, 7)])]
for P, pi in walks:
    assert all(sum(pi[i] * P[i][j] for i in range(len(pi))) == pi[j] for j in range(len(pi)))
assert F(1, 3) == F(1, 2) * F(2, 3) and F(2, 3) == (F(1, 3) + 1) / 2
RESULTS['walk_stationary_equations'] = 'exact rational equations verified'

RESULTS['tex_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.glob('*.tex'))}
RESULTS['pdf_id_mapping'] = pdf_map
RESULTS['online_id_mapping'] = online_map
print(json.dumps(RESULTS, ensure_ascii=False, indent=2))
