from itertools import product,combinations
from heapq import heapify,heappush,heappop
from collections import deque,Counter
import json,hashlib

def prufer_tree(code,N):
 deg=[1]*N
 for x in code:deg[x]+=1
 leaves=[x for x in range(N) if deg[x]==1];heapify(leaves);E=[]
 for x in code:
  l=heappop(leaves);E.append(tuple(sorted((l,x))));deg[l]-=1;deg[x]-=1
  if deg[x]==1:heappush(leaves,x)
 if N>1:E.append(tuple(sorted((heappop(leaves),heappop(leaves)))))
 return tuple(sorted(E))
def adj(E,n):
 a=[set() for _ in range(n+1)]
 for u,v in E:a[u].add(v);a[v].add(u)
 return a

def forward(E,n):
 if n==0:return ()
 a=adj(E,n);par={0:None};q=[0]
 for u in q:
  for v in a[u]:
   if v not in par:par[v]=u;q.append(v)
 v=n
 while par[v]!=0:v=par[v]
 B=set();stack=[v]
 while stack:
  u=stack.pop();B.add(u);stack.extend(x for x in a[u] if x!=par[u])
 j=len(B);r=sum(b<v for b in B);C=sorted(set(range(1,n+1))-B)
 left={v:0,**{b:k+1 for k,b in enumerate(sorted(B-{v}))}};right={0:0,**{b:k+1 for k,b in enumerate(C)}}
 EL=tuple(sorted(tuple(sorted((left[x],left[y]))) for x,y in E if x in B and y in B))
 ER=tuple(sorted(tuple(sorted((right[x],right[y]))) for x,y in E if x in right and y in right))
 g=forward(EL,j-1);h=forward(ER,n-j);f=[0]*n
 for b,t in zip(sorted(B-{n}),g):f[b-1]=t
 for b,t in zip(C,h):f[b-1]=j+t
 f[n-1]=j-r
 return tuple(f)
def park(f):
 S=set(range(1,len(f)+1));spots=[]
 for p in f:
  cand=[x for x in S if x>=p]
  if not cand:return None
  x=min(cand);S.remove(x);spots.append(x)
 return spots

def inverse(f):
 n=len(f)
 if n==0:return ()
 avail=set(range(1,n+1));spots=[]
 for p in f[:-1]:
  x=min(x for x in avail if x>=p);avail.remove(x);spots.append(x)
 j=next(iter(avail));S=[i+1 for i,x in enumerate(spots) if x<j];C=[i+1 for i,x in enumerate(spots) if x>j];B=sorted(S+[n]);r=j-f[-1];v=B[r]
 g=tuple(f[i-1] for i in S);h=tuple(f[i-1]-j for i in C)
 lm={0:v,**{k+1:b for k,b in enumerate(x for x in B if x!=v)}};rm={0:0,**{k+1:b for k,b in enumerate(C)}}
 E=[tuple(sorted((0,v)))]
 E.extend(tuple(sorted((lm[x],lm[y]))) for x,y in inverse(g))
 E.extend(tuple(sorted((rm[x],rm[y]))) for x,y in inverse(h))
 return tuple(sorted(E))
def inv(E,n):
 a=adj(E,n);par={0:None};q=[0]
 for u in q:
  for v in a[u]:
   if v not in par:par[v]=u;q.append(v)
 total=0
 for i in range(1,n+1):
  v=par[i]
  while v is not None:
   total+=v>i;v=par[v]
 return total

def bracket(s):
 stack=[];paired=set()
 for i,b in enumerate(s):
  if b:stack.append(i)
  elif stack:
   j=stack.pop();paired.update([i,j])
 un=[i for i in range(len(s)) if i not in paired];a=sum(s[i]==0 for i in un);b=len(un)-a;t=list(s)
 for i,x in zip(un,[0]*b+[1]*a):t[i]=x
 return tuple(t)

def bip_encode(E,m,n):
 A=set(range(m));B=set(range(m,m+n));adjc={x:set() for x in A|B}
 for u,v in E:adjc[u].add(v);adjc[v].add(u)
 aa=[];bb=[]
 while len(A)+len(B)>2:
  side=A if len(A)>=len(B) else B;l=min(x for x in side if len(adjc[x])==1);v=next(iter(adjc[l]));(bb if l in A else aa).append(v);side.remove(l);adjc[v].remove(l);del adjc[l]
 return tuple(aa),tuple(bb)
def bip_decode(aa,bb,m,n):
 A=set(range(m));B=set(range(m,m+n));ia=ib=0;E=[]
 while len(A)+len(B)>2:
  if len(A)>=len(B):l=min(A-set(aa[ia:]));v=bb[ib];ib+=1;A.remove(l)
  else:l=min(B-set(bb[ib:]));v=aa[ia];ia+=1;B.remove(l)
  E.append(tuple(sorted((l,v))))
 E.append(tuple(sorted((next(iter(A)),next(iter(B))))));return tuple(sorted(E))

out={'tree_parking':[],'bracket':[],'bipartite':[]}
for n in range(1,7):
 seen=set();poly=Counter()
 for code in product(range(n+1),repeat=n-1):
  E=prufer_tree(code,n+1);f=forward(E,n);assert park(f) is not None;assert inverse(f)==E;assert inv(E,n)==n*(n+1)//2-sum(f);assert f not in seen;seen.add(f);poly[inv(E,n)]+=1
 pfs={f for f in product(range(1,n+1),repeat=n) if park(f) is not None};assert seen==pfs
 out['tree_parking'].append({'n':n,'trees':len(seen),'parking_functions':len(pfs),'inversion_coefficients':[poly[k] for k in range(max(poly)+1)]})
for n in range(1,13):
 cnt=0
 for s in product([0,1],repeat=n):
  t=bracket(s);assert bracket(t)==s;assert sum(t)==n-sum(s)
  if sum(s)<=n/2:assert all(not x or y for x,y in zip(s,t))
  cnt+=1
 out['bracket'].append({'n':n,'words':cnt})
for m in range(1,5):
 for n in range(1,5):
  pairs=set()
  for aa in product(range(m),repeat=n-1):
   for bb in product(range(m,m+n),repeat=m-1):
    E=bip_decode(aa,bb,m,n);assert all((u<m)!=(v<m) for u,v in E);assert bip_encode(E,m,n)==(aa,bb);assert E not in pairs;pairs.add(E)
  trees={prufer_tree(c,m+n) for c in product(range(m+n),repeat=m+n-2) if all((u<m)!=(v<m) for u,v in prufer_tree(c,m+n))}
  assert pairs==trees
  out['bipartite'].append({'m':m,'n':n,'trees':len(pairs)})
print(json.dumps(out,indent=2,ensure_ascii=False))
