#!/usr/bin/env python3
"""Independent numerical spot checks; these are not proofs or a complete audit."""
from pathlib import Path
import hashlib,json,math
import numpy as np
from scipy.integrate import quad

ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    checks=[]
    value,error=quad(lambda z:z,0,1)
    checks.append({'name':'Schwinger form-factor parameter integral after x integration','computed_F2_over_e2':value/(4*math.pi**2),'expected':1/(8*math.pi**2),'absolute_error':abs(value-.5)/(4*math.pi**2),'integration_error':error})
    a,_=quad(lambda x:x*(1-x)*math.log(x*(1-x)),0,1)
    checks.append({'name':'Vacuum-polarization finite constant','computed':a,'expected':-5/18,'absolute_error':abs(a+5/18)})
    mat=np.array([[-.8,0,-.6],[0,-.8,-.6],[-.1,-.1,-.4]])
    eig=np.sort(np.linalg.eigvals(mat).real)
    checks.append({'name':'Two-scalar O(2) quartic stability eigenvalues divided by epsilon','computed':eig.tolist(),'expected':[-1.,-.8,-.2],'max_error':float(np.max(np.abs(eig-[-1.,-.8,-.2])))})
    sigma=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]
    zero=np.zeros((2,2));one=np.eye(2)
    gamma=[np.block([[one,zero],[zero,-one]])]+[np.block([[zero,s],[-s,zero]])for s in sigma]
    eta=np.diag([1.,-1.,-1.,-1.]);I=np.eye(4)
    cliff=max(float(np.max(np.abs(gamma[a]@gamma[b]+gamma[b]@gamma[a]-2*eta[a,b]*I)))for a in range(4)for b in range(4))
    checks.append({'name':'Explicit four-by-four Clifford algebra (+---)','max_error':cliff})
    def slash(p):return sum(gamma[i]*(eta[i,i]*p[i])for i in range(4))
    def dot(p,q):return float(p@eta@q)
    scattering=[]
    for m,M,E,theta in [(.4,2.,1.2,.5),(.2,3.,2.,1.1),(.1,10.,4.,2.),(.7,4.,2.5,2.8)]:
        p=math.sqrt(E*E-m*m);co=math.cos(theta)
        Ep=((E+M)*(M*E+m*m)+p*p*co*math.sqrt(M*M-m*m*math.sin(theta)**2))/((E+M)**2-p*p*co*co)
        pp=math.sqrt(Ep*Ep-m*m)
        p1=np.array([E,0,0,p]);p2=np.array([M,0,0,0]);k1=np.array([Ep,pp*math.sin(theta),0,pp*co]);k2=p1+p2-k1
        s=dot(p1+p2,p1+p2);t=dot(p1-k1,p1-k1);u=dot(p1-k2,p1-k2);A=m*m+M*M
        product=0j
        for mu in range(4):
            for nu in range(4):
                Te=np.trace((slash(k1)+m*I)@gamma[mu]@(slash(p1)+m*I)@gamma[nu])
                Tm=np.trace((slash(k2)+M*I)@(eta[mu,mu]*gamma[mu])@(slash(p2)+M*I)@(eta[nu,nu]*gamma[nu]))
                product+=Te*Tm
        direct=product.real/(4*t*t);compact=2*((s-A)**2+(u-A)**2+2*A*t)/(t*t)
        residual=abs((E+M)*Ep-p*pp*co-(M*E+m*m))
        scattering.append({'m':m,'M':M,'E':E,'theta':theta,'on_shell_error':abs(dot(k2,k2)-M*M),'unsquared_energy_equation_error':residual,'gamma_trace_over_e4':direct,'invariant_formula_over_e4':compact,'relative_error':abs(direct-compact)/max(1,abs(compact))})
    checks.append({'name':'e-muon scattering: gamma traces vs invariant formula and finite-mass lab root','samples':scattering})
    errors=[x.get('max_error',x.get('absolute_error',0))for x in checks]
    errors.extend(s['relative_error']for s in scattering)
    assert max(errors)<1e-10
    out={'date':'2026-10-12','status':'PASS for listed finite checks','scope':'Four-by-four matrices, numerical quadrature and four physical kinematic samples; not a proof of general formulas or complete mathematical correctness. Full analytic reasoning is in the TeX and independent review reports.','checks':checks,'source_sha256':{str(p.relative_to(ROOT)):sha(p)for p in [ROOT/'chapters/ch16.tex',ROOT/'chapters/ch18.tex',ROOT/'chapters/assessment-8323-ps12.tex']}}
    p=ROOT/'qa/formula-spotchecks.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(p)
if __name__=='__main__':main()
