"""Independent residual/initial-value checks; numerical checks do not prove qualitative diagrams."""
import sympy as s
import json, hashlib
from pathlib import Path
x,t=s.symbols('x t',positive=True);I=s.I
checks=[]
def check(label,value):
 result=s.simplify(s.expand_trig(value));checks.append({'id':label,'residual':str(result),'pass':result==0})
def ode(label,y,coef,rhs,var=t):check(label,sum(a*s.diff(y,var,k)for k,a in enumerate(coef))-rhs)
ode('ex1-3b',(s.pi+s.sin(t))/t,[1,t],s.cos(t));check('ex1-3b-ic',((s.pi+s.sin(t))/t).subs(t,s.pi)-1)
ode('ex1-5b',s.exp(2*t)/5+4*s.exp(-3*t)/5,[3,1],s.exp(2*t))
ode('ex1-5d',(3*s.cos(2*t)+2*s.sin(2*t))/13,[3,1],s.cos(2*t))
ode('ex2-2a',(t-s.Rational(4,5))*s.exp(2*t),[1,0,1],5*t*s.exp(2*t))
ode('ex2-5c',t*s.sin(2*t)/2,[8,0,2],4*s.cos(2*t))
ode('final-2d',(1+s.cos(x))/x**2,[2,x],-s.sin(x)/x,x)
ode('final-4a',t**2-t+s.Rational(1,4),[8,4,1],8*t**2)
ode('final-4d',t**3+s.exp(-2*t)*s.sin(2*t),[8,4,1],6*t+12*t*t+8*t**3)
check('final-4d-initial-x',(t**3+s.exp(-2*t)*s.sin(2*t)).subs(t,0))
check('final-4d-initial-dx',s.diff(t**3+s.exp(-2*t)*s.sin(2*t),t).subs(t,0)-2)
ode('final-6c',s.exp(-t)*(1-s.cos(2*t))/2,[s.Rational(5,2),1,s.Rational(1,2)],s.exp(-t))
ode('prex1-4a',t*t/4+s.Symbol('C')/t**2,[2,t],t*t)
ode('prex1-4b',(s.cos(2*t)+s.sin(2*t))/4,[2,1],s.cos(2*t))
ode('prex2-2',t*t-4*t+2,[1,2,3],t*t)
ode('prex2-3',t*s.exp(-t),[2,3,1],s.exp(-t))
ode('prex2-6',s.exp(-t)*(3*s.cos(t)+2*s.sin(t))/13,[1,0,0,1],s.exp(-t)*s.cos(t))
ode('prfinal-2e',x*x/5+4/(5*x**3),[3,x],x*x,x)
check('prfinal-2e-ic',(x*x/5+4/(5*x**3)).subs(x,1)-1)
ode('prfinal-4a',t*t/2-t+1,[2,2,1],t*t+1)
ode('prfinal-4b',(s.exp(-2*t)+1)/2,[2,2,1],s.exp(-2*t)+1)
ode('prfinal-4c',(s.sin(t)-2*s.cos(t))/5,[2,2,1],s.sin(t))
ode('prfinal-5c-resonant',-t*s.cos(t)/2,[1,0,1],s.sin(t))
q=s.symbols('s');check('prex3-4b-partial',-1/(2*(q+1))+((q+1)/2+2)/((q+1)**2+4)-2*q/((q+1)*(q*q+2*q+5)))
P=s.Matrix([[1,3],[2,4]]);E=P*s.diag(s.exp(2*t),s.exp(-2*t))*P.inv();B=P*s.diag(2,-2)*P.inv()
for k,z in enumerate(E.diff(t)-B*E):check('final-8d-matrix'+str(k),z)
u=E*s.Matrix([1,1]);
for k,z in enumerate(u.subs(t,0)-s.Matrix([1,1])):check('final-8e-ic'+str(k),z)
# explicit numeric Euler calculations
check('ex1-euler',s.Rational(17,4)-(s.Rational(5,2)+s.Rational(1,2)*(1+s.Rational(5,2))))
check('final-euler',s.Rational(39,32)-(s.Rational(1,2)+s.Rational(1,2)*(s.Rational(3,2)-s.Rational(1,16))))
tex=Path(__file__).parents[1]/'coursework/exams.tex'
out={'type':'symbolic_residual_checks_not_mathematical_proof','tex_sha256':hashlib.sha256(tex.read_bytes()).hexdigest(),'checks':checks,'passed':sum(z['pass']for z in checks),'total':len(checks)}
Path(__file__).with_name('exams-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(out['passed'],out['total']);assert out['passed']==out['total']
