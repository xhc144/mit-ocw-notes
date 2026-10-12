"""Exact component checks for the explicitly normalized five-dimensional EM example."""
from pathlib import Path
import json,sympy as s
z,R,M,Q=s.symbols('z R M Q',positive=True);n=5
f=1-M*z**4+Q**2*z**6/3
metric=[R**2/(z**2*f),-R**2*f/z**2]+[R**2/z**2]*3
inv=[1/v for v in metric]
def g(a,b):return metric[a] if a==b else s.Integer(0)
def derivative(expr,index):return s.diff(expr,z) if index==0 else s.Integer(0)
Gamma=[[[s.simplify(inv[a]*(derivative(g(a,c),b)+derivative(g(a,b),c)-derivative(g(b,c),a))/2) for c in range(n)] for b in range(n)] for a in range(n)]
Ricci=[]
for b in range(n):
 row=[]
 for c in range(n):
  expr=sum(derivative(Gamma[a][b][c],a)-derivative(Gamma[a][b][a],c)+sum(Gamma[a][b][c]*Gamma[v][a][v]-Gamma[v][b][a]*Gamma[a][c][v] for v in range(n)) for a in range(n))
  row.append(s.simplify(expr))
 Ricci.append(row)
F=s.zeros(n);F[0,1]=-2*Q*z;F[1,0]=2*Q*z
F2=s.simplify(sum(inv[a]*inv[b]*F[a,b]**2 for a in range(n) for b in range(n)))
res=[]
for a in range(n):
 for b in range(n):
  rhs=-4/R**2*g(a,b)+R**2/2*(sum(inv[p]*F[a,p]*F[b,p] for p in range(n))-g(a,b)*F2/6)
  val=s.simplify(Ricci[a][b]-rhs);assert val==0,(a,b,val)
  res.append({'component':[a,b],'residual':str(val)})
maxwell=s.simplify(s.diff(R**5/z**5*inv[0]*inv[1]*F[0,1],z));assert maxwell==0
q,h,C=s.symbols('q h C',positive=True)
e=3*C*(1+q*q)/h**4;entropy=4*s.pi*C/h**3;rho=2*s.sqrt(3)*C*q/h**3;T=(1-q*q/2)/(s.pi*h);mu=s.sqrt(3)*q/h
first_law=[s.simplify(s.diff(e,v)-T*s.diff(entropy,v)-mu*s.diff(rho,v)) for v in [q,h]]
assert first_law==[0,0]
pressure=C*(1+q*q)/h**4;gibbs=s.simplify(e+pressure-T*entropy-mu*rho);assert gibbs==0
out={'coordinates':['z','t','x1','x2','x3'],'action_gauge_coefficient':'-R^2 F^2/4 inside Einstein action with prefactor 1/(16piG)','f':'1-M*z^4+Q^2*z^6/3','At_derivative':'-2Qz','einstein_25_components':res,'maxwell_residual':str(maxwell),'first_law_q_and_h_residual':[str(v) for v in first_law],'gibbs_relation_residual':str(gibbs),'scope':'Exact algebra for this EM ansatz and stated EOS normalization; no proof of stability of all charged IIB fields or of full AdS/CFT.'}
root=Path(__file__).resolve().parents[1];(root/'qa/einstein-maxwell-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='einstein_25_components'},ensure_ascii=False))
