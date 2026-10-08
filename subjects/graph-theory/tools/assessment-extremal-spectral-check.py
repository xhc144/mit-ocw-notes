import itertools,json,math,pathlib,time
import numpy as np
start=time.time(); counts={"simple_graphs":0,"rademacher_cases":0,"book_identity_cases":0,"book_bound_cases":0,"stability_cases":0,"degree_domination_cases":0,"triangle_free_min_degree_cases":0,"laplace_cut_cases":0,"balanced_spectral_color_cases":0}
def tr(n,r):
    q,s=divmod(n,r); return (n*n-s*(q+1)**2-(r-s)*q*q)//2

def constructed(ad,r):
    n=len(ad)
    if r==1: return [0]*n,[list(range(n))]
    if n==0:return [],[[] for _ in range(r)]
    v=max(range(n),key=lambda x:ad[x].bit_count()); X=[x for x in range(n) if ad[v]>>x&1]; Y=[x for x in range(n) if not(ad[v]>>x&1)]
    sub=[sum(1<<j for j,y in enumerate(X) if ad[x]>>y&1) for x in X]
    hh,pp=constructed(sub,r-1); H=[0]*n
    for i,x in enumerate(X):
        H[x]=sum(1<<X[j] for j in range(len(X)) if hh[i]>>j&1)|sum(1<<y for y in Y)
    for y in Y:H[y]=sum(1<<x for x in X)
    return H,[[X[j] for j in p] for p in pp]+[Y]
for n in range(1,7):
    pairs=list(itertools.combinations(range(n),2)); quart=list(itertools.combinations(range(n),4))
    for mask in range(1<<len(pairs)):
        ad=[0]*n; edges=[]
        for j,(u,v) in enumerate(pairs):
            if mask>>j&1:ad[u]|=1<<v;ad[v]|=1<<u;edges.append((u,v))
        counts['simple_graphs']+=1;m=len(edges);d=[x.bit_count() for x in ad];ce=[(ad[u]&ad[v]).bit_count() for u,v in edges];T=sum(ce)//3;Q=I0=0
        for vs in quart:
            deg=sorted(sum((ad[x]>>y)&1 for y in vs if y!=x) for x in vs)
            Q+=deg==[3,3,3,3];I0+=deg==[0,2,2,2]
        ae=[n-d[u]-d[v]+c for (u,v),c in zip(edges,ce)]
        assert n*T+8*Q+2*I0==sum(c*(c+a) for c,a in zip(ce,ae));counts['book_identity_cases']+=1
        if m>=n*n//4+1:
            assert T>=n//2;counts['rademacher_cases']+=1
            assert 6*max(ce)>n;counts['book_bound_cases']+=1
        for r,free in [(1,m==0),(2,T==0),(3,Q==0)]:
            if not free:continue
            H,pp=constructed(ad,r)
            assert all(H[v].bit_count()>=d[v] for v in range(n));counts['degree_domination_cases']+=1
            kept=sum(1 for u,v in edges if any(u in p and v in p for p in pp)==False)
            assert m-kept<=tr(n,r)-m;counts['stability_cases']+=1
        if T==0 and min(d)>2*n/5:
            color={};okay=True
            for rt in range(n):
                if rt in color:continue
                color[rt]=0;todo=[rt]
                while todo:
                    u=todo.pop()
                    for v in range(n):
                        if not(ad[u]>>v&1):continue
                        if v in color:okay &= color[v]!=color[u]
                        else:color[v]=1-color[u];todo.append(v)
            assert okay;counts['triangle_free_min_degree_cases']+=1
        if n<=5 and n>=2:
            A=np.array([[(ad[i]>>j)&1 for j in range(n)] for i in range(n)],dtype=float);lam2=np.linalg.eigvalsh(np.diag(d)-A)[1]
            for sm in range(1<<n):
                s=sm.bit_count()
                if 2*s>n:continue
                cut=sum(((sm>>u)&1)!=((sm>>v)&1) for u,v in edges)
                assert cut+1e-9>=lam2*s/2;counts['laplace_cut_cases']+=1
        if n<=6 and len(set(d))==1 and d[0]>0:
            A=np.array([[(ad[i]>>j)&1 for j in range(n)] for i in range(n)],dtype=float);vals=np.linalg.eigvalsh(A);bound=max(abs(vals[:-1]));dd=d[0]
            for k in range(1,n+1):
                if n%k or bound>dd/k+1e-9:continue
                for col in itertools.product(range(k),repeat=n):
                    if any(col.count(i)!=n//k for i in range(k)):continue
                    assert any({col[w] for w in range(n) if ad[v]>>w&1}==set(range(k)) for v in range(n));counts['balanced_spectral_color_cases']+=1
leg={}
for p in [3,5,7,11,13,17,19,23,29,31]:
    squares={i*i%p for i in range(1,p)};chi=[0 if i==0 else (1 if i in squares else -1) for i in range(p)];M=np.array([[chi[(i+j)%p] for j in range(p)] for i in range(p)],dtype=np.int64)
    assert np.array_equal(M@M.T,p*np.eye(p,dtype=np.int64)-np.ones((p,p),dtype=np.int64));leg[str(p)]='exact integer identity pI-J'
sharp=[]
for t in range(1,13):
    groups=[list(range(i*t,(i+1)*t)) for i in range(3)];off=3*t;groups += [list(range(off+i*(t-1),off+(i+1)*(t-1))) for i in range(3)]
    n=6*t-3;ad=[0]*n
    for a,b in [(0,1),(0,2),(1,2),(3,4),(3,5),(4,5),(0,3),(1,4),(2,5)]:
        for u in groups[a]:
            for v in groups[b]:ad[u]|=1<<v;ad[v]|=1<<u
    m=sum(x.bit_count() for x in ad)//2;book=max((ad[u]&ad[v]).bit_count() for u in range(n) for v in range(u+1,n) if ad[u]>>v&1)
    assert m==n*n//4+1 and book==t;sharp.append({'t':t,'n':n,'m':m,'book':book})
tree=[]
for q in [1,2,3,4]:
    for R in range(1,6):
        levels=[[0]];parent=[-1]
        for i in range(R):
            nxt=[]
            for v in levels[-1]:
                for j in range(q):parent.append(v);nxt.append(len(parent)-1)
            levels.append(nxt)
        f=np.zeros(len(parent));theta=math.pi/(R+2)
        for i,lev in enumerate(levels):
            for x in lev:f[x]=q**(-i/2)*math.sin((i+1)*theta)
        af=np.zeros(len(parent))
        for x,pa in enumerate(parent):
            if pa>=0:af[x]+=f[pa];af[pa]+=f[x]
        err=float(np.max(abs(af-2*math.sqrt(q)*math.cos(theta)*f)));assert err<1e-12;tree.append({'q':q,'R':R,'vertices':len(parent),'maximum_eigenvector_residual':err})
r={'status':'PASS','counts':counts,'legendre_correlations':leg,'book_sharp_sequence':sharp,'finite_tree_vectors':tree,'seconds':time.time()-start,'limits':'Finite checks verify identities and small cases; they do not replace general proofs, source-license review, independent cross-review, or PDF page visual inspection.'}
pathlib.Path('/tmp/assessment18217_checks.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':r['status'],'counts':counts,'seconds':r['seconds']},ensure_ascii=False))
