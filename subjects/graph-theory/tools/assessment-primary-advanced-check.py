import itertools, json, hashlib
from pathlib import Path

def cycle_count(p):
    seen=set(); cycles=[]
    for a in range(len(p)):
        if a in seen: continue
        cur=[]; b=a
        while b not in seen:
            cur.append(b); seen.add(b); b=p[b]
        if len(cur)>1: cycles.append(cur)
    return cycles

def compose(p,q): return tuple(p[q[a]] for a in range(len(p)))
def inverse(p):
    out=[0]*len(p)
    for i,j in enumerate(p): out[j]=i
    return tuple(out)

def gray(n):
    if n==3:
        return [tuple(x-1 for x in p) for p in [(1,2,3),(2,1,3),(2,3,1),(3,2,1),(3,1,2),(1,3,2)]]
    out=[]
    for i,p in enumerate(gray(n-1)):
        for a in (range(n-1,-1,-1) if i%2==0 else range(n)):
            out.append(p[:a]+(n-1,)+p[a:])
    return out

def cross(e,f):
    a,b=sorted(e);c,d=sorted(f)
    return a<c<b<d or c<a<d<b

data={"scope":"finite exact examples only, not a substitute for general proofs", "checks":{}}
total=0
for n in range(1,8):
    for p in itertools.permutations(range(n)):
        cyc=cycle_count(p); total+=1
        if len(cyc)<2: continue
        reps=[c[0] for c in cyc]; t=list(range(n))
        for a,b in zip(reps,reps[1:]+reps[:1]): t[a]=b
        merged=compose(p,t)
        assert len(cycle_count(merged))==1
        assert len(cycle_count(compose(inverse(merged),p)))==1
data["checks"]["birkhoff_two_cycle_factorization"]={"n_max":7,"permutations":total,"result":"PASS"}
gcounts=[]
for n in range(3,8):
    seq=gray(n); assert len(seq)==len(set(seq))
    assert set(seq)==set(itertools.permutations(range(n)))
    for p,q in zip(seq,seq[1:]+seq[:1]):
        ids=[a for a in range(n) if p[a]!=q[a]]
        assert len(ids)==2 and ids[1]==ids[0]+1
        assert p[ids[0]]==q[ids[1]] and p[ids[1]]==q[ids[0]]
    gcounts.append({"n":n,"vertices":len(seq),"closing_edge_checked":True})
data["checks"]["gray_hamilton_cycles"]={"instances":gcounts,"result":"PASS"}
page_counts=[]
for n in range(4,51):
    pages=[[] for _ in range((n+1)//2)]
    for a,b in itertools.combinations(range(n),2): pages[((a+b)%n)//2].append((a,b))
    for edges in pages:
        assert not any(cross(e,f) for e,f in itertools.combinations(edges,2))
    page_counts.append(len(pages))
data["checks"]["complete_graph_residue_pages"]={"n_min":4,"n_max":50,"graphs":len(page_counts),"result":"PASS"}

def cube(n):
    if n==1: return [0,1],[[(0,1)]]
    order,pages=cube(n-1); bit=1<<(n-1)
    new=order+[v+bit for v in reversed(order)]
    pgs=[p+[(a+bit,b+bit) for a,b in p] for p in pages]
    pgs.append([(v,v+bit) for v in order])
    return new,pgs

qcounts=[]
for n in range(1,9):
    order,pgs=cube(n); pos={v:a for a,v in enumerate(order)}
    edges={tuple(sorted(e)) for page in pgs for e in page}
    expected={(a,a^(1<<b)) for a in range(1<<n) for b in range(n) if a<(a^(1<<b))}
    assert edges==expected and len(pgs)==n
    for page in pgs:
        transformed=[(pos[a],pos[b]) for a,b in page]
        assert not any(cross(e,f) for e,f in itertools.combinations(transformed,2))
    qcounts.append({"dimension":n,"vertices":1<<n,"edges":len(edges),"pages":len(pgs)})
data["checks"]["hypercube_reverse_copy_pages"]={"instances":qcounts,"result":"PASS"}
for name in ["hw5.tex","hw6.tex"]:
    p=(Path(__file__).resolve().parents[1]/'assessments/18315')/name
    data.setdefault("draft_hashes",{})[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
target=Path('/tmp/18315-advanced-finite-check.json');target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(data,ensure_ascii=False))
