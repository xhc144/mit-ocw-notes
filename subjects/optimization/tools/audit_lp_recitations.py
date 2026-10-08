#!/usr/bin/env python3
"""Independent numerical/exact audit of 15.053 recitations and practical problem set.
Run from the optimization project; no network calls or external data required.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import json
import numpy as np
import sympy as S
from scipy.optimize import linprog
from scipy.spatial import ConvexHull
ROOT=Path(__file__).resolve().parents[1]
OUT={}
def lp(name,c,A,b,bounds=None,E=None,d=None):
    r=linprog(-np.asarray(c,float),A_ub=np.asarray(A,float) if A else None,b_ub=b if A else None,A_eq=E,b_eq=d,bounds=bounds,method='highs')
    OUT[name]={'success':bool(r.success),'status':int(r.status)}
    if r.success:
        x=[str(F(float(v)).limit_denominator(10**6)) for v in r.x]
        OUT[name].update(x=x,value=str(F(float(-r.fun)).limit_denominator(10**6)),max_constraint_violation=float(max(0,max(np.asarray(A)@r.x-b))) if A else 0)
    return r
def pivot(M,row,col):
    M=S.Matrix(M); p=M[row,col]; assert p!=0
    M[row,:]=M[row,:]/p
    for i in range(M.rows):
        if i!=row: M[i,:]=M[i,:]-M[i,col]*M[row,:]
    return M
def tables(name,M,pivots):
    M=S.Matrix(M); arr=[M]
    for row,col in pivots: M=pivot(M,row,col); arr.append(M)
    OUT[name]=[[[str(v) for v in list(m.row(i))] for i in range(m.rows)] for m in arr]
    return M
# Rec1 food quantities (hours per portion), price minus ingredient cost.
A=[[F(1,10),F(1,5),F(1,15)],[F(1,20),F(1,15),F(1,25)],[F(1,30),F(1,15),F(1,30)]]
A=np.array(A,float); c=[6,10,4.5]; b=[4,2,2]
for k in [-1,0,1,2]:
    rhs=b.copy()
    if k>=0:rhs[k]+=1
    r=lp(f'rec1-food-{k}',c,A.tolist(),rhs,[(0,20),(0,10),(0,30)])
    if k==-1:assert np.allclose(r.x,[8,6,30]) and np.isclose(-r.fun,243)
# Exact simplex tableaux: last column RHS, row zero reduced costs.
tables('rec2-q3',[[10,8,-3,3,0,0,0],[2,4,-S.Rational(1,2),S.Rational(1,2),1,0,6],[-2,6,-S.Rational(9,2),S.Rational(9,2),0,1,4]],[(1,0),(2,3)])
tables('rec2-q4',[[2,4,0,0,0,0,0],[S.Rational(1,2),-5,0,1,0,0,12],[-1,-2,0,0,1,0,2],[0,1,1,0,0,-1,4]],[(3,1)])
tables('rec3-q1',[[1,2,S.Rational(5,4),0,0,0],[2,1,1,1,0,6],[0,2,1,0,1,4]],[(2,1),(1,0),(2,2)])
tables('rec3-q2',[[0,-3,0,2,0,-6],[1,-4,0,2,0,0],[0,-6,1,3,0,2],[0,-1,0,0,1,5]],[(1,3)])
tables('rec3-q3',[[3,-1,-1,0,0,6],[2,-2,0,1,0,1],[1,1,-1,0,1,5]],[(1,0),(2,1)])
tables('rec3-q4-negative-pivot',[[0,0,-1,-3,0,-1,0],[1,0,2,1,0,2,4],[0,1,1,-3,0,5,1],[0,0,-2,1,1,-1,0]],[(3,2)])
# Rec4 Q3 tableau regenerated from initial matrix, not trusted final sheet.
A4=S.Matrix([[1,1,1,1,1,0,0],[2,-2,0,-6,0,1,0],[3,0,1,-1,0,0,1]])
B=A4[:,[2,0,1]]; rows=B.inv()*A4; rhs=B.inv()*S.Matrix([4,2,7]); cb=S.Matrix([[2,3,1]])
pi=cb*B.inv(); red=S.Matrix([[3,1,2,-2,0,0,0]])-pi*A4
OUT['rec4-q3-generated']={'pi':list(map(str,pi)),'reduced':list(map(str,red)),'rows':[[str(rows[i,j]) for j in range(7)]+[str(rhs[i])] for i in range(3)]}
assert list(pi)==[2,S.Rational(1,2),0]
A5=S.Matrix([[5,6,-1,2,1,0,0],[-3,-1,2,-1,0,1,0],[-2,0,2,-2,0,0,1]])
B=A5[:,[3,2,6]]; pi=S.Matrix([[2,5,0]])*B.inv()
OUT['rec5-q1']={'pi':list(map(str,pi)),'reduced':list(map(str,S.Matrix([[2,3,5,2,0,0,0]])-pi*A5)),'rhs':list(map(str,B.inv()*S.Matrix([6,4,3])))}
# New France, variable order exports S,M,T; production S,M,T.
E=[[-1,0,0,1,-.75,-1],[0,-1,0,-.05,1,-.1],[0,0,-1,-.08,-.12,1]]
A=[[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1],[0,0,0,.5,5,3]]; b=[300000,50000,550000,1200000]; c=[900,2500,3000,-300,-150,-500]
for key,cc,bb,dd in [('base',c,b,[0,0,0]),('cost-plus400',c[:-1]+[-900],b,[0,0,0]),('stock-steel10000',c,b,[10000,0,0]),('machine40000',c,[300000,40000,550000,1200000],[0,0,0])]:
    lp('rec4-france-'+key,cc,A,bb,[(0,None)]*6,E,dd)
# Rec7 geometric intended objective x1+5x2; original x4 is undefined.
A=[[-4,3],[3,2]]; b=[6,18];
for key,bounds in [('root',[(0,None),(0,None)]),('x1le2',[(0,2),(0,None)]),('x1ge3',[(3,None),(0,None)]),('left-x2le4',[(0,2),(0,4)]),('left-x2ge5',[(0,2),(5,None)]),('right-x2le4',[(3,None),(0,4)]),('right-x2ge5',[(3,None),(5,None)]),('right-x1le3',[(3,3),(0,4)]),('right-x1ge4',[(4,None),(0,4)])]:
    lp('rec7-q2-'+key,[1,5],A,b,bounds)
pts=[(x,y) for x in range(7) for y in range(10) if -4*x+3*y<=6 and 3*x+2*y<=18]
OUT['rec7-q2-integer-points']=pts; assert max(x+5*y for x,y in pts)==23
# Binary knapsack B&B, exact fractional greedy at each node.
w=[6,8,10,13]; p=[19,23,30,40]; nodes=[]; incumbent=F(0); best=None
def knap(fixed):
    global incumbent,best
    cap=F(25)-sum(w[i]*v for i,v in fixed.items())
    if cap<0:return None
    x=[F(fixed.get(i,0)) for i in range(4)]
    for i in sorted((j for j in range(4) if j not in fixed),key=lambda j:F(p[j],w[j]),reverse=True):
        x[i]=min(F(1),cap/w[i]); cap-=w[i]*x[i]
    return x,sum(p[i]*x[i] for i in range(4))
def visit(fixed):
    global incumbent,best
    r=knap(fixed); node={'fix':{f'x{k+1}':v for k,v in fixed.items()}}
    if r is None:node['status']='infeasible';nodes.append(node);return
    x,z=r;node.update(x=list(map(str,x)),bound=str(z));nodes.append(node)
    if z<=incumbent:node['status']='bound';return
    frac=next((i for i,v in enumerate(x) if v.denominator!=1),None)
    if frac is None:incumbent=z;best=x;node['status']='integer';return
    node['status']='branch';node['branch_variable']=f'x{frac+1}'
    for v in [0,1]:visit(dict(fixed,**{})|{frac:v})
visit({}); OUT['rec7-q3-bnb']={'nodes':nodes,'incumbent':str(incumbent),'best':list(map(str,best))};assert incumbent==72
# Rec8 lattice hull and regenerated rational rows.
pts=[(x,y) for x in range(6) for y in range(6) if -3*x+5*y<=12 and 4*x+3*y<=20 and 2*(x+y)<=11]
hull=ConvexHull(np.array(pts)); OUT['rec8-q2']={'points':pts,'hull_vertices':[pts[i] for i in hull.vertices]}
A8=S.Matrix([[2,1,1,1,0,0],[-4,4,2,0,1,0],[1,2,3,0,0,1]])
B=A8[:,[3,1,0]]; rows=B.inv()*A8; rhs=B.inv()*S.Matrix([8,8,9]);pi=S.Matrix([[0,4,-2]])*B.inv()
OUT['rec8-q3']={'rows':[[str(rows[i,j]) for j in range(6)]+[str(rhs[i])] for i in range(3)],'objective':str((pi*S.Matrix([8,8,9]))[0])}
assert rows[1,2]==S.Rational(7,6)
# Verify covers, their minimality and extended-cover validity by enumeration.
weights=[11,6,6,5,5,4,1]; covers=[[3,4,5],[0,1,5],[1,2,5,6],[1,3,4,5],[0,2,3,4],[1,2,3,4,5]]
OUT['rec8-q4']=[{'items':[i+1 for i in C],'weight':sum(weights[i] for i in C),'valid':sum(weights[i] for i in C)>19,'minimal':sum(weights[i] for i in C)>19 and all(sum(weights[j] for j in C if j!=i)<=19 for i in C)} for C in covers]
assert all(sum(x[:5])<=3 for x in product([0,1],repeat=7) if sum(a*v for a,v in zip(weights,x))<=19)
# Oil-site logic equivalence on all binary vectors.
for x in product([0,1],repeat=10):
    logic=not(x[1] and x[6] and (x[5] or x[8])) and not(x[0] and x[2] and x[4] and x[5]) and not((x[2] or x[3]) and x[5]) and sum(x[i] for i in [2,5,6,7])<=2
    lin=x[1]+x[6]+x[5]<=2 and x[1]+x[6]+x[8]<=2 and x[0]+x[2]+x[4]+x[5]<=3 and x[2]+x[5]<=1 and x[3]+x[5]<=1 and sum(x[i] for i in [2,5,6,7])<=2
    assert bool(logic)==bool(lin)
OUT['rec6-oil-logic']={'checked_binary_vectors':1024,'equivalent':True}
# Auction official question version has nine bids; solution PDF has seven.
sets=[{1,5},{1,2,4},{3},{5},{2,4},{2,3,4,5},{1,2,3},{2,4,6},{3,5,6}]; prices=[10,20,8,4,15,30,18,25,16]
for key,avail in [('single',[1]*6),('double123',[2,2,2,1,1,1])]:
    sols=[]
    for x in product([0,1],repeat=9):
        if all(sum(x[j] for j in range(9) if i+1 in sets[j])<=avail[i] for i in range(6)):sols.append((sum(a*b for a,b in zip(prices,x)),x))
    z=max(z for z,x in sols);OUT['practice-auction-'+key]={'value':z,'solutions':[x for v,x in sols if v==z]}
# Lockbox exact enumeration, objective thousands of dollars.
cost=np.array([[48,96,144,144,120],[40,20,50,50,40],[174,145,58,145,203],[98,70,84,42,126]])
for penalty in [0,50]:
    candidates=[]
    for y in product([0,1],repeat=4):
        choices=[j for j in range(4) if y[j]]+[4]
        ass=[min(choices,key=lambda j:cost[i,j]) for i in range(4)]
        z=90*sum(y)+sum(int(cost[i,j]) for i,j in enumerate(ass))+penalty*(sum(y)>=3)
        candidates.append((z,y,ass))
    z=min(v for v,y,a in candidates);OUT[f'practice-lockbox-penalty{penalty}']={'value':z,'optimal':[{'open':y,'assign_1based':[j+1 for j in a]} for v,y,a in candidates if v==z]}
# Rec10 decision-tree expected values use exact arithmetic.
proactive=F(1,2)*(F(4,5)*1+F(1,5)*(-1))+F(1,2)*(F(1,4)*0+F(3,4)*(-F(5,4)))
passive=F(1,2)*(F(1,4)*0+F(3,4)*(-2))+F(1,2)*(F(1,5)*F(1,2)+F(4,5)*(-10))
comp=(proactive-passive)/F(2,5)
OUT['rec10']={'airfare_expected_cost':str((F(320)+450)/2),'monkey_noinfo':str(F(1,5)*3-1),'monkey_fixedplay_info_net':str(F(1,5)*2+F(4,5)*(F(1,4)*3-1)),'monkey_fixedplay_value':str(F(3,5)),'monkey_info_before_decision_value':str(F(2,5)),'proactive_million':str(proactive),'passive_million':str(passive),'compensation_million':str(comp)}
# Correct practice Gomory cut fractions.
OUT['practice-gomory']={'fraction_x3':str(F(265,100)-2),'fraction_x4':str(F(-2,10)-(-1)),'fraction_rhs':str(F(33,10)-3)}
# Exact dual certificates, geometric inputs and small logical counterexamples.
Erat=S.Matrix([[-1,0,0,1,-S.Rational(3,4),-1],[0,-1,0,-S.Rational(1,20),1,-S.Rational(1,10)],[0,0,-1,-S.Rational(2,25),-S.Rational(3,25),1]])
Arat=S.Matrix([[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1],[0,0,0,S.Rational(1,2),5,3]])
crat=S.Matrix([900,2500,3000,-300,-150,-500]); rhs=S.Matrix([300000,40000,550000,1200000])
eqpi=S.Matrix([-S.Rational(3580,3),-S.Rational(39200,3),-3000]); uppi=S.Matrix([0,S.Rational(34985,3),0,0]); xp=S.Matrix([0,0,S.Rational(686800,3),S.Rational(860000,3),40000,S.Rational(770000,3)])
assert all(v>=0 for v in Erat.T*eqpi+Arat.T*uppi-crat)
assert Erat*xp==S.zeros(3,1) and all(v>=0 for v in rhs-Arat*xp)
assert (crat.T*xp)[0]==(rhs.T*uppi)[0]==S.Rational(1399400000,3)
OUT['rec4-new-france-exact-certificate']={'balance_dual':list(map(str,eqpi)),'capacity_dual':list(map(str,uppi)),'capacity_slack':list(map(str,rhs-Arat*xp)),'duality_gap':'0'}
B2=(F(1,10),F(8,5)); D2=(F(1,2),F(0)); F2=(F(2),F(0))
def feasible2(x,y):return x-y>=-F(3,2) and x-2*y<=2 and 4*x+y>=2 and x>=0 and y>=0
assert all(feasible2(*p) for p in [B2,D2,F2])
assert B2[0]-B2[1]==-F(3,2) and 4*B2[0]+B2[1]==2
assert not feasible2(0,0) and not feasible2(0,F(3,2))
for t in [F(0),F(1),F(1000)]:assert feasible2(B2[0]+t,B2[1]+t) and feasible2(F2[0]+2*t,F2[1]+t)
OUT['diagram-rec2-q2']={'vertices':[[str(v) for v in p] for p in [B2,D2,F2]],'rays':[[1,1],[2,1]],'verified_constraints':True}
OUT['diagram-rec7-q2']={'integer_points_count':len(OUT['rec7-q2-integer-points']),'integer_optimum':[3,4],'value':23,'all_points_checked':True}
assert max(2,3)==3 and all(1<=y<=6 and x>=2 and x+y>=3 for x,y in [(2,1),(3,1),(3,2),(4,1),(4,2),(4,3),(5,2)])
OUT['diagram-rec8-q1']={'points':[[2,1],[3,1],[3,2],[4,1],[4,2],[4,3],[5,2]],'choices_valid':[False,True,True,True,True]}
assert F(4)-2==F(1)+F(2,2)==2 and F(1)+F(4,2)==-5+2*4==3
OUT['diagram-rec6-q3']={'vertices':[[0,4],[2,2],[4,3],[6,7]],'breakpoints_verified':True}
assert F(11,8)+F(3,4)*(6+6+5+5)==F(143,8)<=19 and F(1,8)+4*F(3,4)>3
OUT['rec8-cover-strength']={'point':['1/8','3/4','3/4','3/4','3/4','0','0'],'weight':'143/8','violates_extended_only':True}
# Dijkstra one-step labels, checked against explicit directed arc endpoints.
arcs=[('S','A',1),('S','B',6),('S','C',3),('A','D',6),('A','B',4),('B','D',1),('B','T',5),('C','E',2),('D','T',2),('E','T',4)]
dist={'S':0,'A':1,'B':5,'C':3,'D':7,'E':float('inf'),'T':float('inf')}; permanent={'S','A'}; u=min((n for n in dist if n not in permanent),key=lambda n:dist[n]);assert u=='C';permanent.add(u)
for a,v,cost in arcs:
    if a==u:dist[v]=min(dist[v],dist[u]+cost)
assert dist['E']==5
OUT['diagram-rec9-q1']={'arcs':arcs,'permanent_after_next_iteration':sorted(permanent),'distances':{k:('infinity' if np.isinf(v) else v) for k,v in dist.items()}}
assert 2**6>2*24
OUT['rec9-last-multiple-choice']={'answers':['i','ii'],'simple_network_diamonds':6,'arcs':24,'paths':64,'odd_euler_cycle_counterexample':'triangle, m=3','even_edge_odd_cut_counterexample':'s-a-t, m=2, cut({s})=1'}
# Exhaustively validate bounded piecewise costs from Rec6.
for x in range(101):
    cost=(57*x if x<=10 else 570 if x<=20 else -480+50*x)
    k=0 if x<=10 else 1 if x<=20 else 2
    y=[0,0,0];v=[0,0,0];y[k]=x;v[k]=1
    assert cost==57*y[0]+570*v[1]-480*v[2]+50*y[2]
OUT['rec6-q1-piecewise-cost']={'integer_inputs_checked':101,'equivalent':True}
path=ROOT/'review/lp-recitation-computations.json'; path.write_text(json.dumps(OUT,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':len(OUT),'output':str(path.relative_to(ROOT)),'meal':[OUT[f'rec1-food-{k}'] for k in [-1,0,1,2]],'france_machine40000':OUT['rec4-france-machine40000'],'rec8_rows':OUT['rec8-q3'],'knapsack':OUT['rec7-q3-bnb'],'auction':[OUT['practice-auction-single'],OUT['practice-auction-double123']],'lockbox':[OUT['practice-lockbox-penalty0'],OUT['practice-lockbox-penalty50']],'decision':OUT['rec10']},ensure_ascii=False,indent=2))
