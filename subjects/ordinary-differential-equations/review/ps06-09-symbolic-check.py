"""Auxiliary symbolic verification; does not replace the written proofs."""
import hashlib,json
from pathlib import Path
import sympy as S
root=Path(__file__).resolve().parents[1]
t=S.symbols('t',real=True);s=S.symbols('s');a,b,k,om=S.symbols('a b k om',real=True,nonzero=True)
checks=[]
def zero(name,expr):
 v=S.simplify(expr);assert v==0,(name,v);checks.append({'name':name,'residual':str(v)})
def ivp(name,x,operator,rhs,initial):
 zero(name+'.ODE',operator(x)-rhs)
 for j,value in enumerate(initial):zero(name+f'.initial-{j}',S.diff(x,t,j).subs(t,0)-value)
w=S.exp(-t)*S.sin(t)/2;v=(1-S.exp(-t)*(S.cos(t)+S.sin(t)))/4
ivp('PS6-II24.impulse',w,lambda x:2*S.diff(x,t,2)+4*S.diff(x,t)+4*x,0,[0,S.Rational(1,2)])
ivp('PS6-II24.step',v,lambda x:2*S.diff(x,t,2)+4*S.diff(x,t)+4*x,1,[0,0]);zero('PS6-II24.derivative',S.diff(v,t)-w)
x=(k*S.cos(om*t)+om*S.sin(om*t)-k*S.exp(-k*t))/(k*k+om*om)
ivp('PS6-II25.harmonic',x,lambda x:S.diff(x,t)+k*x,S.cos(om*t),[0])
x=(1-S.cos(om*t))/(om*om);ivp('PS6-II25.constant',x,lambda x:S.diff(x,t,2)+om*om*x,1,[0,0])
q=S.symbols('q');zero('PS6-II25.commutation-a',S.integrate((t-q)**2*q,(q,0,t))-t**4/12);zero('PS6-II25.commutation-b',S.integrate((t-q)*q**2,(q,0,t))-t**4/12)
zero('PS6-II25.association-a',S.integrate((t-q)**3*q/6,(q,0,t))-t**5/120);zero('PS6-II25.association-b',S.integrate((t-q)*q**3/6,(q,0,t))-t**5/120)
zero('PS7-II27.partial-fractions',-a/(b*b*s)+1/(b*s*s)+a/(b*b*(s+b/a))-1/(s*s*(a*s+b)))
x=t/b-a/b**2*(1-S.exp(-b*t/a));ivp('PS7-II27.ramp',x,lambda x:a*S.diff(x,t)+b*x,t,[0]);ivp('PS7-II27.ramp-b0',t*t/(2*a),lambda x:a*S.diff(x,t),t,[0])
w=S.exp(-t)*S.sin(t)/3;ivp('PS7-II28a',w,lambda x:3*S.diff(x,t,2)+6*S.diff(x,t)+6*x,0,[0,S.Rational(1,3)])
al=S.sqrt(2)/2;w=(S.cosh(al*t)*S.sin(al*t)-S.sinh(al*t)*S.cos(al*t))/S.sqrt(2)
ivp('PS7-II28b-original-plus-I',w,lambda x:S.diff(x,t,4)+x,0,[0,0,0,1])
W=S.Rational(3,2)/(s*s+s+S.Rational(5,2));zero('PS8-II29.transfer',(S.Rational(2,3)*s*s+S.Rational(2,3)*s+S.Rational(5,3))*W-1)
x=(3*S.exp(-t)-S.exp(-3*t))/2;ivp('PS8-II32d',x,lambda x:S.diff(x,t,2)+4*S.diff(x,t)+3*x,0,[1,0])
x=S.Rational(2,3)*S.exp(-t/2)*S.sin(3*t/2);ivp('PS8-II32f',x,lambda x:S.diff(x,t,2)+S.diff(x,t)+S.Rational(5,2)*x,0,[0,1])
A=S.Matrix([[S.Rational(1,2),1],[-S.Rational(9,4),S.Rational(1,2)]])
u=S.exp(t/2)*S.Matrix([S.cos(3*t/2),-S.Rational(3,2)*S.sin(3*t/2)])
for i,r in enumerate(S.diff(u,t)-A*u):zero(f'PS9-II34a.system-{i}',r)
B=S.Matrix([[1,b],[0,1]]);u=S.exp(t)*S.Matrix([b*t,1])
for i,r in enumerate(S.diff(u,t)-B*u):zero(f'PS9-II34b.complement-{i}',r)
z=S.symbols('z');aa=S.symbols('aa');A=S.Matrix([[aa,-3],[1,-1]])
zero('PS9-II35.charpoly',A.charpoly(z).as_expr()-(z*z-(aa-1)*z+3-aa))
for boundary in [-1-2*S.sqrt(3),-1+2*S.sqrt(3)]:zero('PS9-II35.repeated-boundary',((aa-1)**2-4*(3-aa)).subs(aa,boundary))
A=S.Matrix([[0,1],[-2,-2]]);E=S.exp(-t)*S.Matrix([[S.cos(t)+S.sin(t),S.sin(t)],[-2*S.sin(t),S.cos(t)-S.sin(t)]])
for i,r in enumerate(S.diff(E,t)-A*E):zero(f'PS9-II36b.exponential-{i}',r)
assert E.subs(t,0)==S.eye(2)
A=S.Matrix([[4,-1],[2,1]]);E=S.Matrix([[2*S.exp(3*t)-S.exp(2*t),-S.exp(3*t)+S.exp(2*t)],[2*S.exp(3*t)-2*S.exp(2*t),-S.exp(3*t)+2*S.exp(2*t)]])
for i,r in enumerate(S.diff(E,t)-A*E):zero(f'PS9-II36c.exponential-{i}',r)
assert E.subs(t,0)==S.eye(2)
tex=root/'coursework/ps06-09.tex'
report={'kind':'symbolic-auxiliary-check','tex_sha256':hashlib.sha256(tex.read_bytes()).hexdigest(),'assertions':len(checks)+2,'zero_residual_checks':checks,'identity_initial_matrix_checks':2,'limits':'Ordinary t>0 ODE/initial values only; distributions, completeness, qualitative arguments and source fidelity are checked in the prose and independent review, not by this script.'}
(root/'review/ps06-09-symbolic-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'assertions':report['assertions'],'tex_sha256':report['tex_sha256']}))
