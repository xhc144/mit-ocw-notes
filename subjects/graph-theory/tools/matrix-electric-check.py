from itertools import combinations, product
from fractions import Fraction as F
from math import factorial
from functools import lru_cache
import hashlib, json

def solve(M, rhs):
    n=len(rhs); A=[[F(x) for x in row]+[F(rhs[i])] for i,row in enumerate(M)]
    for k in range(n):
        p=next(i for i in range(k,n) if A[i][k]); A[k],A[p]=A[p],A[k]
        v=A[k][k]; A[k]=[x/v for x in A[k]]
        for i in range(n):
            if i!=k:
                v=A[i][k]; A[i]=[x-v*y for x,y in zip(A[i], A[k])]
    return [r[-1] for r in A]

def det(M):
    n=len(M); A=[[F(x) for x in row] for row in M]; z=F(1)
    for k in range(n):
        ps=[i for i in range(k,n) if A[i][k]]
        if not ps: return F(0)
        p=ps[0]
        if p!=k: A[k],A[p]=A[p],A[k]; z=-z
        v=A[k][k];z*=v
        for i in range(k+1,n):
            q=A[i][k]/v
            for j in range(k,n): A[i][j]-=q*A[k][j]
    return z

def minor(M,r):return [[x for j,x in enumerate(row) if j!=r] for i,row in enumerate(M) if i!=r]
def connected(n,edges):
    seen={0}
    while True:
        old=set(seen)
        for u,v in edges:
            if u in seen or v in seen:seen.update((u,v))
        if seen==old:return len(seen)==n

def spanning_tree_sum(n,es):
    return sum((__import__('math').prod(w for u,v,w in S) for S in combinations(es,n-1) if connected(n,[(u,v) for u,v,w in S])),0)

def two_root_forest_sum(n, es, a, b):
    result=0
    for S in combinations(es,n-2):
        parent=list(range(n))
        def root(x):
            while x!=parent[x]:x=parent[x]
            return x
        good=True
        for u,v,w in S:
            u,v=root(u),root(v)
            if u==v:good=False;break
            parent[u]=v
        if good and root(a)!=root(b):
            result+=__import__('math').prod(w for u,v,w in S)
    return result

def edge_tree_weight(n, es, e):
    return sum((__import__('math').prod(w for u,v,w in S) for S in combinations(es,n-1) if e in S and connected(n,[(u,v) for u,v,w in S])),0)

undirected_graphs=0; commute_pairs=0; undirected_cofactors=0; forest_checks=0; edge_prob_checks=0
for n in range(2,6):
    poss=list(combinations(range(n),2))
    for mask in range(1<<len(poss)):
        es=[(u,v,1+j%5) for j,(u,v) in enumerate(poss) if mask>>j&1]
        if not connected(n,[(u,v) for u,v,w in es]):continue
        undirected_graphs+=1
        L=[[0]*n for _ in range(n)]
        for u,v,w in es:L[u][u]+=w;L[v][v]+=w;L[u][v]-=w;L[v][u]-=w
        trees=spanning_tree_sum(n,es)
        for b in range(n):
            assert det(minor(L,b))==trees
            undirected_cofactors+=1
        d=[L[i][i] for i in range(n)]; vol=sum(d); hits={}
        for b in range(n):
            ids=[i for i in range(n) if i!=b]
            x=solve(minor(L,b),[d[i] for i in ids]); hits[b]={**dict(zip(ids,x)),b:F(0)}
        for a,b in combinations(range(n),2):
            ids=[i for i in range(n) if i!=b]
            phi=solve(minor(L,b),[int(i==a) for i in ids]);R=dict(zip(ids,phi))[a]
            assert hits[b][a]+hits[a][b]==vol*R
            assert R>0
            F_ab=two_root_forest_sum(n,es,a,b)
            assert R==F(F_ab,trees)
            reduced=minor(L,b); ia=ids.index(a)
            assert det(minor(reduced,ia))==F_ab
            forest_checks+=1
            for e in es:
                u,v,w=e
                if (u,v)==(a,b):
                    assert F(edge_tree_weight(n,es,e),trees)==w*R
                    edge_prob_checks+=1
            commute_pairs+=1

# Directed trees are separately enumerated by choosing one individually labelled arc per nonroot vertex.
def directed_tree_count(n,arcs,r):
    opts=[[k for k,(u,v) in enumerate(arcs) if u==i] for i in range(n) if i!=r]
    z=0
    for ss in product(*opts):
        out={arcs[k][0]:arcs[k][1] for k in ss}
        okay=True
        for i in range(n):
            j=i;seen=set()
            while j!=r and j not in seen:seen.add(j);j=out[j]
            if j!=r:okay=False;break
        z+=okay
    return z

def euler_count(n,arcs,r,e0):
    full=(1<<len(arcs))-1
    @lru_cache(None)
    def rec(v,mask):
        if mask==full:return int(v==r)
        return sum(rec(w,mask|(1<<k)) for k,(u,w) in enumerate(arcs) if u==v and not(mask>>k&1))
    return rec(arcs[e0][1],1<<e0)

def strongly_connected(n,arcs):
    for s in range(n):
        seen={s}
        while True:
            old=set(seen)
            seen.update(v for u,v in arcs if u in old)
            if seen==old:break
        if len(seen)<n:return False
    return True

def check_directed(n,arcs):
    global directed_cases,directed_cofactors,best_checks
    if not arcs or not strongly_connected(n,arcs):return
    dp=[sum(u==i for u,v in arcs) for i in range(n)]
    dm=[sum(v==i for u,v in arcs) for i in range(n)]
    L=[[0]*n for _ in range(n)]
    for u,v in arcs:
        if u!=v:L[u][u]+=1;L[u][v]-=1
    for r in range(n):
        tr=directed_tree_count(n,arcs,r)
        assert det(minor(L,r))==tr
        directed_cofactors+=1
        if dp==dm:
            z=tr
            for d in dp:z*=factorial(d-1)
            for e0,(u,v) in enumerate(arcs):
                if u==r:
                    assert euler_count(n,arcs,r,e0)==z
                    best_checks+=1
    directed_cases+=1

directed_cases=directed_cofactors=best_checks=0
# All nonloop arc multiplicities 0, 1, 2 on 3 vertices; all strongly connected are checked.
poss=[(u,v) for u in range(3) for v in range(3) if u!=v]
for ns in product(range(3),repeat=6):
    arcs=[e for e,c in zip(poss,ns) for _ in range(c)]
    check_directed(3,arcs)
# Parallel arcs and loops: all balanced two-vertex multiplicities up to 2, loops up to 2.
for mult,la,lb in product(range(1,3),range(3),range(3)):
    check_directed(2,[(0,1)]*mult+[(1,0)]*mult+[(0,0)]*la+[(1,1)]*lb)
for loops in range(1,5):check_directed(1,[(0,0)]*loops)
# Three-vertex directed cycles, with every choice of 0/1 self-loop at each vertex.
for mult in (1,2):
    for loops in product(range(2),repeat=3):
        check_directed(3,[(0,1)]*mult+[(1,2)]*mult+[(2,0)]*mult+[(i,i) for i,x in enumerate(loops) if x])
summary=dict(undirected_connected_weighted_graphs=undirected_graphs,undirected_cofactors=undirected_cofactors,commute_unordered_pairs=commute_pairs,directed_multigraph_cases=directed_cases,directed_cofactors=directed_cofactors,best_root_and_fixed_first_arc_cases=best_checks,two_root_forest_resistance_cases=forest_checks,random_tree_edge_probability_cases=edge_prob_checks,all_exact_rational_checks_passed=True)
print(json.dumps(summary,indent=2))
