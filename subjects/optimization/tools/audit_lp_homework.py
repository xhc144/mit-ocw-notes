#!/usr/bin/env python3
"""Recompute MIT 15.053 homework LPs and exact tableau/certificate checks.

Run from any directory. Requires numpy, scipy, sympy; reads every cached XLS
cell table rather than inferring spreadsheet contents from filenames.
"""
from pathlib import Path
import hashlib, itertools, json
import numpy as np
from scipy.optimize import linprog
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'sources/15.053/assessments'
OUT = ROOT / 'review/lp-homework-numerical.json'
results = {}

def lp(c, A, b, bounds=None, eq=None):
    c, A, b = np.asarray(c,float), np.asarray(A,float), np.asarray(b,float)
    r=linprog(-c,A_ub=A,b_ub=b,bounds=bounds or [(0,None)]*len(c),
              A_eq=None if eq is None else eq[0], b_eq=None if eq is None else eq[1],method='highs')
    assert r.success, r.message
    y=-r.ineqlin.marginals
    # The upper-bound marginals are included for certificate verification.
    ub=np.array([q[1] if q[1] is not None else np.inf for q in (bounds or [(0,None)]*len(c))])
    upper=-r.upper.marginals
    lower=-r.lower.marginals
    lb=np.array([q[0] if q[0] is not None else -np.inf for q in (bounds or [(0,None)]*len(c))])
    dual=float(b@y+sum(ub[i]*upper[i] for i in range(len(c)) if np.isfinite(ub[i]))+sum(lb[i]*lower[i] for i in range(len(c)) if np.isfinite(lb[i])))
    assert np.max(A@r.x-b)<1e-6
    if eq is None:
        assert abs(dual-c@r.x)<1e-5
        assert np.max(c-A.T@y-upper)<1e-6
    return {'x':r.x.tolist(),'value':float(c@r.x),'slack':(b-A@r.x).tolist(),'dual':y.tolist(),'upper_dual':upper.tolist(),'lower_dual':lower.tolist()}

def blend(prices=(7.9,6.9,5.), deluxe_cap=None, delete=None, availability=(4000,5000,3500,5500)):
    costs=np.array([.60,.52,.48,.35]); c=np.tile(prices,4)-np.repeat(costs,3)
    A=[]; b=[]; names=[]
    for i in range(4):
        row=np.zeros((4,3));row[i,:]=1;A.append(row.ravel());b.append(availability[i]);names.append('supply '+str(i))
    for j in range(3):
        for i,sgn,ratio in [(0,1,[.6,.15,None][j]),(2,-1,[.2,.6,.5][j]),(3,1,[.1,.25,.45][j])]:
            if ratio is None or delete==(i,j):continue
            row=np.zeros((4,3));row[:,j]=-sgn*ratio;row[i,j]+=sgn
            A.append(row.ravel());b.append(0);names.append(f'component {i} mixture {j}')
    if deluxe_cap is not None:
        row=np.zeros((4,3));row[:,0]=1;A.append(row.ravel());b.append(deluxe_cap);names.append('deluxe cap')
    d=lp(c,A,b);d['mix']=np.array(d['x']).reshape(4,3).sum(axis=0).tolist();d['constraint_names']=names
    return d

Q=np.array([[7,3,12,6,18,17],[2,5,3,2,15,17],[5,1,3,2,9,2]],float)
REV=np.array([200,120,180,130,430,260]); MAT=np.array([35,25,40,45,170,60]); DEM=[2000,1500,1800,1200,1000,1000]
def testing(labor=(16,12,18), hours=(130,130,100), external=False, revenue=127):
    q=Q.copy();rev=REV.copy();mat=MAT.copy();bounds=[(0,x) for x in DEM]
    if external:
        q=np.column_stack([q,[3,2,6]]);rev=np.append(rev,revenue);mat=np.append(mat,50);bounds.append((0,None))
    return lp(rev-mat-np.asarray(labor)@q/60,q,np.asarray(hours)*60,bounds)

def exact_simplex(A,b,c,basis,bland=True):
    A,b,c=sp.Matrix(A),sp.Matrix(b),sp.Matrix([c]);history=[]
    for _ in range(50):
        B=A[:,basis]; beta=B.inv()*b; row=c[:,basis]*B.inv(); red=c-row*A
        history.append({'basis':[i+1 for i in basis],'xB':[str(v) for v in beta],'value':str((row*b)[0]),'reduced':[str(v) for v in red]})
        enter=next((j for j in range(A.cols) if j not in basis and red[j]>0),None)
        if enter is None:return history
        col=B.inv()*A[:,enter]
        ratios=[(beta[i]/col[i],basis[i],i) for i in range(A.rows) if col[i]>0]
        assert ratios,'unexpected unbounded LP'
        _,_,leave=min(ratios);basis=basis.copy();basis[leave]=enter
    raise AssertionError('pivot limit')

def run():
    # Load every actual cell, recording dimensions, counts, and hashes.
    sheets={}
    for p in sorted(SRC.glob('*.cells.json')):
        d=json.loads(p.read_text());sheets[p.name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sheets':{k:{'rows':len(v),'columns':max(map(len,v)),'nonblank':sum(x not in ('',None,' ') for row in v for x in row)} for k,v in d.items()}}
    results['spreadsheets_read']=sheets
    results['cover']=lp([4,6,10],[[1/6000,1/5000,1/3000],[.04,.045,.21]],[5,6000],[(5000,10000),(0,15000),(4000,8000)])
    results['blend_base']=blend()
    results['blend_remove_D_caps']=[blend(delete=(3,j)) for j in range(3)]
    results['blend_deluxe_prices']={str(p):blend((p,6.9,5)) for p in [7.95,8,8.05,7.9*1.05,8.2,8.25,8.5,8.69]}
    results['blend_more_A']=blend(availability=(4001,5000,3500,5500))
    results['blend_modified']=blend((7.7,6.8,4.9),12000)
    results['blend_standard_prices']={str(p):blend((7.7,p,4.9),12000) for p in [6.85,6.9,6.95,7.2,7.5]}
    # Thresholds obtained from dual pricing; independent near-threshold reruns.
    results['blend_economy_price_tests']={str(p):blend((7.9,6.9,p)) for p in [5.175,5.18,5.2]}
    results['blend_modified_economy_tests']={str(p):blend((7.7,6.8,p),12000) for p in [5.7,5.75,5.76]}
    results['blend_thresholds']={'economy_base':blend((7.9,6.9,1619/312)),
        'economy_modified':blend((7.7,6.8,5.70625),12000),'deluxe_break':blend((8.21,6.9,5.0))}
    assert abs(results['blend_thresholds']['economy_base']['value']-results['blend_base']['value'])<1e-6
    assert abs(results['blend_thresholds']['economy_modified']['value']-results['blend_modified']['value'])<1e-6
    assert abs(results['blend_thresholds']['deluxe_break']['value']-(308960/3+12500*(8.21-7.9)))<1e-6
    assert abs(results['blend_deluxe_prices']['8.69']['value']-(125000*8.69-64495)/9)<1e-6
    results['testing_base']=testing()
    results['testing_hours']={str(t):testing(hours=(130,130+t,100)) for t in [1,2,3,5,10,15,20]}
    results['testing_changed_labor']=testing((18,13,20))
    results['testing_modified']=testing((18,15,12),external=True)
    results['testing_modified_hours']={str(t):testing((18,15,12),(130,130+t,100),True) for t in [1,2,3,10,15,20]}
    results['testing_external_revenues']={str(p):testing((18,15,12),external=True,revenue=p) for p in [128,129,130]}
    # Exact two-column dual and symbolic sensitivity conditions.
    rate=sp.symbols('rate');qs=sp.Matrix([[7,3],[2,5]])
    coef=sp.Matrix([165-sp.Rational(7*16+2*12,60)-5*rate/60,95-sp.Rational(3*16+5*12,60)-rate/60])
    pi=qs.T.inv()*coef
    allcost=sp.Matrix([sp.Rational(int(REV[j]-MAT[j]))-sp.Rational(int(16*Q[0,j]+12*Q[1,j]),60)-sp.Rational(int(Q[2,j]),60)*rate for j in range(6)])
    reduced=[sp.factor(allcost[j]-pi[0]*int(Q[0,j])-pi[1]*int(Q[1,j])) for j in range(6)]
    results['testing_labor3_exact']={'dual':[str(v) for v in pi],'reduced':[str(v) for v in reduced]}
    results['tires']=lp([600,400,800],[[2,2,4],[3,2,2],[2,1,2]],[12,14,16])
    furnitureA=np.array([[1.2,1.7,1.2],[.8,0,2.3],[2,3,4.5]])
    furnitureb=np.array([1000,1200,2000])
    results['furniture_base']=lp([3,3,5],furnitureA,furnitureb)
    results['furniture_force_50_benches']=lp([3,3,5],furnitureA,furnitureb,[(0,None),(50,None),(0,None)])
    forced=np.array([1.2,3,2.4]); r=lp([3,3,5],furnitureA,furnitureb-forced)
    r['total_with_new_bench']=r['value']+2.5
    assert abs(r['x'][0]-699.16)<1e-7
    assert abs(r['x'][2]-(400/3-.16))<1e-7
    assert abs(r['total_with_new_bench']-(8300/3-.82))<1e-7
    results['furniture_new_bench_1']=r
    results['tires_simplex']=exact_simplex([[2,2,4,1,0,0],[3,2,2,0,1,0],[2,1,2,0,0,1]],[12,14,16],[600,400,800,0,0,0],[3,4,5])
    a=sp.Matrix([[1,6,1,-1],[2,-4,2,-4],[4,0,1,1]]);b=sp.Matrix([8,4,6])
    x=sp.Matrix([sp.Rational(5,6),sp.Rational(3,4),sp.Rational(8,3),0]);assert a*x==b
    optimum=sp.Matrix([0,sp.Rational(7,11),sp.Rational(56,11),sp.Rational(10,11)]);assert a*optimum==b
    pi=a[:,[1,2,3]].T.inv()*sp.Matrix([2,2,-3]);assert all(v<=0 for v in sp.Matrix([[1,2,2,-3]])-pi.T*a)
    results['phase1_2']={'phase1':[str(v) for v in x],'phase2':[str(v) for v in optimum],'value':'96/11','dual':[str(v) for v in pi]}
    degA=[[-8,sp.Rational(1,4),9,-1,1,0,0],[-12,sp.Rational(1,2),3,sp.Rational(-1,2),0,1,0],[0,0,0,1,0,0,1]]
    results['bland_degeneracy']=exact_simplex(degA,[0,0,2],[-20,sp.Rational(3,4),-6,sp.Rational(1,2),0,0,0],[4,5,6])
    for step in results['bland_degeneracy']:
        step['value_excluding_constant']=step['value']
        step['value']=str(sp.sympify(step['value'])+3)
    capital=[10,14,8,6,12,8];npv=[33,45,25,17,39,23]
    nodes=[[],[(0,0)],[(0,1)],[(0,0),(1,0)],[(0,0),(1,1)]]
    results['capital_nodes']=[]
    for fix in nodes:
        bounds=[(0,1)]*6
        for i,v in fix:bounds[i]=(v,v)
        results['capital_nodes'].append(lp(npv,[capital],[28],bounds))
    cut1=[1,1,0,0,1,0];cut2=[1,0,1,0,1,0]
    results['capital_cuts']=[lp(npv,[capital],[28],[(0,1)]*6),lp(npv,[capital,cut1],[28,2],[(0,1)]*6),lp(npv,[capital,cut1,cut2],[28,2,2],[(0,1)]*6)]
    feasible=[(sum(v*a for v,a in zip(x,npv)),x) for x in itertools.product([0,1],repeat=6) if sum(v*a for v,a in zip(x,capital))<=28]
    results['capital_integer']=max(feasible)
    # Exhaustively verify the XOR model and optimal M over the original IP.
    pairs=[(a,b) for a in range(78) for b in range(44) if 9*a+16*b<=700]
    for a,b in pairs:
        u,v=2*a+b,4*a-b
        wanted=(u<=50)!=(v>=20)
        modeled=any(u<=50+104*(1-w) and u>=51-51*w and v>=20-63*w and v<=19+289*(1-w) for w in [0,1])
        assert wanted==modeled
    results['logic_XOR_check']={'pairs_checked':len(pairs),'M':[104,51,63,289],'u_max':max(2*a+b for a,b in pairs),'v_max':max(4*a-b for a,b in pairs),'v_min':min(4*a-b for a,b in pairs)}
    triples=0
    for a,b in pairs:
        for s in range((700-9*a-16*b)//5+1):
            triples+=1
            wanted=sum([a>=50,b<=25,s<=100])>=2
            modeled=any(a>=50-50*(1-w1) and b<=25 and s<=100 and w1+w2+w3>=2 for w1,w2,w3 in itertools.product([0,1],repeat=3))
            assert wanted==modeled
    results['logic_at_least_two']={'triples_checked':triples,'joint_minimal_M':[50,0,0],'independently_deactivated_M':[50,18,40]}
    results['gomory']={
        'relaxation':lp([4,3],[[2,1],[-1,2]],[11,6]),
        'first_cut':lp([4,3],[[2,1],[-1,2],[0,1]],[11,6,4]),
        'second_cut':lp([4,3],[[2,1],[-1,2],[0,1],[1,1]],[11,6,4,7])}
    results['oil_project_feasible_counts']={
        'one_year':sum(sum(v*a for v,a in zip(x,[11,9,14,17]))<=32 and sum(v*a for v,a in zip(x,[28,20,25,30]))>=73 for x in itertools.product([0,1],repeat=4)),
        'three_year':sum(all(sum(v*a for v,a in zip(x,row))<=cap for row,cap in zip([[5,4,6,8],[4,3,5,5],[3,3,4,5]],[18,10,7])) and all(sum(v*a for v,a in zip(x,row))>=low for row,low in zip([[5,5,6,8],[5,7,9,10],[8,8,10,12]],[20,25,30])) for x in itertools.product([0,1],repeat=4))}
    OUT.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(f'Wrote {OUT.relative_to(ROOT)}; all numerical/certificate assertions passed.')
    print(f"Read {len(sheets)} spreadsheet cell files; XOR pairs {len(pairs)}; joint-logic triples {triples}.")

if __name__=='__main__':run()
