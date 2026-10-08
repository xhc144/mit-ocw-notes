"""Actual symbolic residual and numerical checks for PS1--PS5 editorial solutions."""
import json, math, hashlib
from pathlib import Path
import sympy as s
from scipy.integrate import quad, solve_ivp
p=Path(__file__).resolve().parents[1];t=s.symbols('t',real=True); checks=[]
def check(name,expr):
 residual=s.simplify(expr);checks.append({'name':name,'residual':str(residual),'passed':residual==0})
def op(y,a,b,c):return a*s.diff(y,t,2)+b*s.diff(y,t)+c*y
k0,a,C=s.symbols('k0 a C',positive=True)
y=C*s.exp(-k0/(a+t));check('PS1 II0 solution',s.diff(y,t)-k0*y/(a+t)**2)
sig=s.symbols('sigma',positive=True);x=s.exp(-sig*t);y=sig*t*x/2;z=1-x-y
check('PS2 II4 equal-half-life x',s.diff(x,t)+sig*x);check('PS2 II4 equal-half-life y',s.diff(y,t)+sig*y-sig*x/2);check('PS2 II4 equal-half-life z',s.diff(z,t)-sig*x/2-sig*y)
mu=s.symbols('mu',positive=True);xu=s.exp(-sig*t);yu=sig*(s.exp(-sig*t)-s.exp(-mu*t))/(2*(mu-sig));zu=1-xu-yu
check('PS2 II4 actual unequal-half-life y',s.diff(yu,t)+mu*yu-sig*xu/2);check('PS2 II4 actual unequal-half-life z',s.diff(zu,t)-sig*xu/2-mu*yu);check('PS2 II4 unequal initial y',yu.subs(t,0));check('PS2 II4 equal-rate limit',s.limit(yu,mu,sig)-y)
check('PS2 II4 conservation',x+y+z-1);check('PS2 II4 all initial values',x.subs(t,0)-1+y.subs(t,0)+z.subs(t,0))
y=(3*s.cos(2*t)+2*s.sin(2*t))/13;check('PS2 II7 response',s.diff(y,t)+3*y-s.cos(2*t))
b=s.symbols('b');u=b*s.exp(-t/2)/(1+2*b*(1-s.exp(-t/2)));check('PS3 II9 exact excess with shifted origin',s.diff(u,t)+u/2+u**2)
x0,v0=s.symbols('x0 v0');y=(5*x0+2*v0)*s.exp(-t/2)/4-(x0+2*v0)*s.exp(-5*t/2)/4
check('PS3 II11 ode',op(y,s.Rational(1,2),s.Rational(3,2),s.Rational(5,8)));check('PS3 II11 initial position',y.subs(t,0)-x0);check('PS3 II11 initial velocity',s.diff(y,t).subs(t,0)-v0)
y=4/s.sqrt(19)*s.exp(-t/4)*s.sin(s.sqrt(19)*t/4);check('PS3 II12 ode',op(y,s.Rational(1,2),s.Rational(1,4),s.Rational(5,8)));check('PS3 II12 initial velocity',s.diff(y,t).subs(t,0)-1)
y=s.exp(3*t)*(5*s.cos(4*t)+4*s.sin(4*t))/41;check('PS4 II13a',s.diff(y,t)+2*y-s.exp(3*t)*s.cos(4*t))
y=(s.cos(t)+s.sin(t))/2+s.exp(-t/2)*(-s.cos(s.sqrt(7)*t/2)/2-3*s.sin(s.sqrt(7)*t/2)/(2*s.sqrt(7)))
check('PS4 II13e ode',op(y,1,1,2)-s.cos(t));check('PS4 II13e position',y.subs(t,0));check('PS4 II13e velocity',s.diff(y,t).subs(t,0))
y=s.exp(2*t)*(t**2/10-s.Rational(9,50)*t+s.Rational(111,500));check('PS4 II15c',op(y,2,1,0)-(t**2+1)*s.exp(2*t))
y=-t**3/3-3*t;check('PS4 II15b',s.diff(y,t,3)-s.diff(y,t)-t**2-1)
y=t**2-2-s.cos(2*t-1)/3;check('PS5 I17 erratum',op(y,1,0,1)-t**2-s.cos(2*t-1))
omega=s.symbols('omega',positive=True);D=(4-omega**2)**2+omega**2/4;r=s.sqrt(s.Rational(31,8));check('PS4 II16 maximum derivative',s.diff(D,omega).subs(omega,r));check('PS4 II16 maximum denominator',D.subs(omega,r)-s.Rational(63,64))
alpha=math.log(2)/(2*math.pi);damping=alpha/math.sqrt(100+alpha**2)
metrics={'trust_initial':240000*(1-math.exp(-1)),'PS3_zero_spacing':4*math.pi/math.sqrt(19),'PS3_pseudoperiod':8*math.pi/math.sqrt(19),'PS4_pseudoperiod':4*math.pi/math.sqrt(7),'resonance_frequency':math.sqrt(31/8),'max_gain':32/math.sqrt(63),'frequency_45deg':(math.sqrt(65)-1)/4,'nyquist_45_real':4/((math.sqrt(65)-1)/4),'damping_exact_n10':damping,'damping_approx_n10':alpha/10,'damping_relative_approx_error_percent':100*((alpha/10)/damping-1)}
coeff=[((-1)**j)/(2*j+1) for j in range(5)]
S=lambda x:sum(c*math.cos((2*j+1)*x) for j,c in enumerate(coeff))
f=lambda x: math.pi/4 if abs(x)<math.pi/2 else -math.pi/4
err=sum(quad(lambda x:(f(x)-S(x))**2,a,b,epsabs=1e-12)[0] for a,b in [(-math.pi,-math.pi/2),(-math.pi/2,math.pi/2),(math.pi/2,math.pi)])/(2*math.pi)
formula=math.pi**2/16-sum(c*c for c in coeff)/2
metrics['Fourier_five_coefficients_rms_quadrature']=math.sqrt(err);metrics['Fourier_five_coefficients_rms_formula']=math.sqrt(formula);metrics['Fourier_rms_squared_difference']=abs(err-formula)
for j in range(5):
 perturb=coeff.copy();perturb[j]+=.1
 err2=sum(quad(lambda x:(f(x)-sum(c*math.cos((2*k+1)*x) for k,c in enumerate(perturb)))**2,a,b)[0] for a,b in [(-math.pi,-math.pi/2),(-math.pi/2,math.pi/2),(math.pi/2,math.pi)])/(2*math.pi)
 checks.append({'name':f'PS5 II20 RMS one coefficient perturbation {2*j+1}','increment':err2-err,'expected':.005,'passed':abs(err2-err-.005)<1e-10})
# Numerical plot check, not proof of the separatrix theorem.
sol=solve_ivp(lambda x,y:[y[0]**2-x],(16,-2.25),[4+1/64],rtol=1e-10,atol=1e-12,dense_output=True)
metrics['PS1_numeric_separatrix_y0']=float(sol.sol(0)[0]);metrics['PS1_numeric_plot_integrator_success']=bool(sol.success)
tex=p/'coursework/ps01-05.tex';out={'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'tex_sha256':hashlib.sha256(tex.read_bytes()).hexdigest(),'checks':checks,'metrics':metrics,'all_checks_passed':all(c['passed'] for c in checks),'limitations':'Residuals verify stated formulas, not all qualitative proofs. The separatrix graph is a numerical reconstruction; its integrator status is not a proof.'}
(p/'review/ps01-05-check-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':out['all_checks_passed'],'metrics':metrics},indent=2))
