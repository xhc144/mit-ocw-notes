import itertools,json,hashlib
from pathlib import Path

def hamilton(adj,vertices,A,B,W=None):
    # Exact bit-mask reachability; optionally preserve the W order.
    vs=sorted(vertices); index={v:i for i,v in enumerate(vs)}
    full=(1<<len(vs))-1; wi={} if W is None else {v:i for i,v in enumerate(W)}
    levels=[{} for _ in range(1<<len(vs))]
    levels[1<<index[A]][A]=1
    for mask in range(1<<len(vs)):
        if not levels[mask]:continue
        for v in list(levels[mask]):
            passed=0 if W is None else sum(bool(mask&(1<<index[w])) for w in W)
            for u in adj[v]:
                if u not in index or mask&(1<<index[u]):continue
                if u==B and (mask|(1<<index[u]))!=full:continue
                if W is not None and u in wi and wi[u]!=passed:continue
                levels[mask|(1<<index[u])][u]=1
    return B in levels[full]

counts={"disks":0,"strip_instances":0,"whitney_endpoint_instances":0}
for m in range(4,7):
    faces=[]
    for i in range(m):
        j=(i+1)%m
        faces.extend([(m,i,j),(m+1,j,i)])
    faceedges=[{tuple(sorted(e)) for e in itertools.combinations(f,2)} for f in faces]
    for mask in range(1,(1<<len(faces))-1):
        ids=[i for i in range(len(faces)) if mask>>i&1]
        reached={ids[0]}
        while True:
            new=reached|{i for i in ids if any(faceedges[i]&faceedges[j] for j in reached)}
            if new==reached:break
            reached=new
        if len(reached)!=len(ids):continue
        multiplicity={}
        for i in ids:
            for e in faceedges[i]:multiplicity[e]=multiplicity.get(e,0)+1
        boundary=[e for e,c in multiplicity.items() if c==1]
        ba={}
        for a,b in boundary:ba.setdefault(a,[]).append(b);ba.setdefault(b,[]).append(a)
        if not ba or any(len(x)!=2 for x in ba.values()):continue
        start=min(ba);bc=[start];prev=None;cur=start
        while True:
            nxt=next(x for x in ba[cur] if x!=prev)
            if nxt==start:break
            if nxt in bc:break
            bc.append(nxt);prev,cur=cur,nxt
        if len(bc)!=len(ba) or nxt!=start:continue
        vertices=set(v for e in multiplicity for v in e)
        if len(vertices)-len(multiplicity)+len(ids)!=1:continue
        adj={v:set() for v in vertices}
        for a,b in multiplicity:adj[a].add(b);adj[b].add(a)
        bedges=set(boundary)
        def no_chord(arc):
            return all(tuple(sorted((a,b))) in bedges or b not in adj[a] for a,b in itertools.combinations(arc,2))
        counts['disks']+=1
        # All root positions and all splits. U shares A with W and has an
        # adjacent terminal x-y boundary edge; U vertices other than A removed.
        for rot in range(len(bc)):
            cyc=bc[rot:]+bc[:rot];A=cyc[0]
            for cut in range(1,len(cyc)-1):
                U=cyc[:cut+1];x=U[-1];y=cyc[cut+1];W=[A]+list(reversed(cyc[cut+1:]))
                if not no_chord(W):continue
                if any(not (adj[u]&set(W)) for u in U[1:]):continue
                remaining=vertices-set(U[1:])
                assert hamilton(adj,remaining,A,y,W), (m,ids,U,W)
                counts['strip_instances']+=1
            # A chosen endpoint; B,C give the three chord-free arcs.
            for j in range(1,len(cyc)-1):
                for k in range(j+1,len(cyc)):
                    if all(no_chord(arc) for arc in [cyc[:j+1],cyc[j:k+1],cyc[k:]+[A]]):
                        assert hamilton(adj,vertices,A,cyc[j]), (m,ids,cyc,j,k)
                        counts['whitney_endpoint_instances']+=1
data={"family":"all simple-boundary connected facial disks in 4-,5-,6-gonal bipyramids (6,7,8 vertices)","method":"exact Hamilton path bitmask dynamic programming, no implementation of drafted inductive construction","counts":counts,"result":"PASS","limit":"finite exact tests do not replace the general proof or independent mathematical review","draft_sha256":hashlib.sha256((Path(__file__).resolve().parents[1]/'assessments/18315/hw5.tex').read_bytes()).hexdigest()}
Path('/tmp/whitney-fan-strip-finite-check.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data))
