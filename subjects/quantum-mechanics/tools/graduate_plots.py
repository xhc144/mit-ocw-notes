from pathlib import Path
import sympy as S, numpy as np, scipy.special as sp, scipy.optimize as opt, json
root=Path(__file__).resolve().parents[1]
# p3 highest weight: order -1up,-1down,0up,0down,1up,1down
import itertools, math
basis=list(itertools.combinations(range(6),3));sel=[b for b in basis if sum((i//2)-1 for i in b)==1 and sum(1 if i%2==0 else -1 for i in b)==1]
def one(b,i,j):
 if j not in b:return None
 a=list(b);sg=(-1)**a.index(j);a.remove(j)
 if i in a:return None
 sg*=(-1)**sum(x<i for x in a);a.append(i);return tuple(sorted(a)),sg
def action(vec,kind):
 out={}
 for b,v in vec.items():
  for j in b:
   i=j+2 if kind=='L' else j-1
   if (kind=='L' and j//2<2) or (kind=='S' and j%2==1):
    z=one(b,i,j)
    if z:bb,sg=z;out[bb]=out.get(bb,0)+sg*v*(S.sqrt(2) if kind=='L' else 1)
 return out
M=S.zeros(len(basis)*2,len(sel))
for j,b in enumerate(sel):
 for k,kind in enumerate(['L','S']):
  for bb,v in action({b:1},kind).items():M[k*len(basis)+basis.index(bb),j]=v
null=M.nullspace();print('p3',sel,null)
# d3 count weight multiplicities and strip SU2 irreps using highest-weight differences
weights={}
for b in itertools.combinations(range(10),3):
 ml=sum(i//2-2 for i in b);ms=sum(1 if i%2==0 else -1 for i in b);weights[ml,ms]=weights.get((ml,ms),0)+1
terms=[]
for twiceS in [3,1]:
 for L in range(7):
  n=weights.get((L,twiceS),0)-weights.get((L+1,twiceS),0)-weights.get((L,twiceS+2),0)+weights.get((L+1,twiceS+2),0)
  if n:terms.append([L,twiceS,n])
print('d3 terms',terms);assert sum(n*(2*l+1)*(s+1)for l,s,n in terms)==120
# Hartree exact integral check
Z=S.symbols('Z',positive=True);k=Z-S.Rational(1,2);int4=S.expand(2*k**3*((Z/k)**3/3-Z/k+S.Rational(2,3)));E=S.simplify(-k*k-int4);assert S.expand(E+Z**2-Z/2+S.Rational(1,12))==0
# KG gamma conventions
I=S.eye(2);O=S.zeros(2);pa=[S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-S.I],[S.I,0]]),S.diag(1,-1)];U=S.BlockMatrix([[I,I],[-I,I]]).as_explicit()/S.sqrt(2);g0=S.diag(1,1,-1,-1);gs=[S.BlockMatrix([[O,p],[-p,O]]).as_explicit()for p in pa];g5=S.I*g0*gs[0]*gs[1]*gs[2];print('gamma0W',U*g0*U.T,'gamma5W',U*g5*U.T)
# hard sphere amplitudes and cross sections
rho=np.linspace(.04,100,1001);cross=[]
for x in rho:
 ell=np.arange(math.ceil(x+4*x**(1/3)+14));j=sp.spherical_jn(ell,x);n=sp.spherical_yn(ell,x);a=j/(n-1j*j);cross.append(4*np.sum((2*ell+1)*np.abs(a)**2)/x**2)
angles=np.linspace(0,np.pi,601);curves=[]
for x in [.1,.5,1,10,25,100]:
 ell=np.arange(math.ceil(x+4*x**(1/3)+14));j=sp.spherical_jn(ell,x);n=sp.spherical_yn(ell,x);a=j/(n-1j*j);f=sum((2*l+1)*a[l]*sp.eval_legendre(l,np.cos(angles))for l in ell)/x;curves.append(np.abs(f)**2)
# neutral atom: SI Rutherford times form-factor [1-F]^2, /Z2 area in a0^2
from scipy.constants import m_e,e,epsilon_0,hbar,physical_constants
bohr=physical_constants['Bohr radius'][0];energy=1000*e;p=math.sqrt(2*m_e*energy);q=2*p*np.sin(angles/2)/hbar;z=q*bohr;F=np.ones_like(z);F[1:]=3*(np.sin(z[1:])-z[1:]*np.cos(z[1:]))/z[1:]**3
fac=2*m_e*(e*e/(4*np.pi*epsilon_0))/hbar**2
amp=np.empty_like(q);amp[1:]=fac*(1-F[1:])/q[1:]**2;amp[0]=fac*bohr**2/10
neutral=amp**2/bohr**2
s=['\\begin{figure}[htbp]\\centering','\\begin{tikzpicture}\\begin{semilogyaxis}[width=.94\\textwidth,height=6cm,xlabel={$\\theta$（度）},ylabel={$|f/R|^2$},xmin=0,xmax=180,legend columns=3,legend style={font=\\small},ymin=1e-6]']
for x,v in zip([.1,.5,1,10,25,100],curves):
 s+=['\\addplot+[no marks] coordinates {'+' '.join(f'({t*180/np.pi:.3f},{max(a,1e-12):.7g})'for t,a in zip(angles,v))+'};',f'\\addlegendentry{{$kR={x}$}}']
s+=['\\end{semilogyaxis}\\end{tikzpicture}\\caption{8.322 PS11 Q1：硬球六个波数的微分截面。纵轴为对数，前向峰及衍射振荡均由分波求和得出。}\\end{figure}']
s+=['\\begin{figure}[htbp]\\centering\\begin{tikzpicture}\\begin{axis}[width=.94\\textwidth,height=4.8cm,xlabel={$kR$},ylabel={$\\sigma/(\\pi R^2)$},xmin=0,xmax=100,ymin=1.5,ymax=4.1]','\\addplot[blue,no marks] coordinates {'+' '.join(f'({t:.5g},{v:.8g})'for t,v in zip(rho,cross))+'};','\\addplot[dashed] coordinates {(0,2)(100,2)};','\\end{axis}\\end{tikzpicture}\\caption{硬球总截面从低能$4\\pi R^2$趋向高能$2\\pi R^2$，横轴完整覆盖至100。}\\end{figure}']
s+=['\\begin{figure}[htbp]\\centering\\begin{tikzpicture}\\begin{axis}[width=.94\\textwidth,height=4.8cm,xlabel={$\\theta$（度）},ylabel={$(\\dd\\sigma/\\dd\\Omega)/(Z^2a_0^2)$},xmin=0,xmax=180]','\\addplot[blue,no marks] coordinates {'+' '.join(f'({t*180/np.pi:.3f},{v:.8g})'for t,v in zip(angles,neutral))+'};','\\end{axis}\\end{tikzpicture}\\caption{PS11 Q5：1 keV电子与均匀电子云中性原子的Born微分截面，核电荷数$Z$按比例因子保留。}\\end{figure}']
(root/'chapters/figure-graduate-322-scattering.tex').write_text('\n'.join(s)+'\n')
report={'status':'PASS','p3_highest_weight_basis':sel,'p3_nullvector':str(null[0]),'d3_terms':[{'L':l,'2S':ss,'multiplicity':n}for l,ss,n in terms],'d3_dimension':120,'hartree_exact_energy':str(E),'hard_sphere_low_energy_ratio':cross[0],'hard_sphere_rho100_ratio':cross[-1],'hard_sphere_angular_samples':601,'total_cross_section_samples':1001,'neutral_forward_limit_f_over_Z_a0':amp[0]/bohr,'plot_scope':'numerical illustrations, not mathematical proofs'}
(root/'qa/graduate-322-computations.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
# Complete Kronig--Penney allowed region for a=1, 0<=lambda,q<=100.
from scipy.optimize import brentq
bands=['\\begin{figure}[htbp]\\centering\\begin{tikzpicture}\\begin{axis}[width=.94\\textwidth,height=7cm,xlabel={$\\lambda$},ylabel={$\\sqrt{2E}$},xmin=0,xmax=100,ymin=0,ymax=100]']
for band in range(32):
    boundary=[]
    for strength in np.linspace(0,100,151):
        left=band*math.pi;right=(band+1)*math.pi
        wave=left if strength==0 else brentq(lambda wave:math.cos(wave)+strength*math.sin(wave)/wave-(-1)**band,max(left+1e-7,1e-7),right-1e-7,xtol=1e-11)
        boundary.append((strength,wave))
    poly=boundary+[(100,min(right,100)),(0,min(right,100))]
    bands.append('\\addplot[draw=blue!60,fill=blue!20,line width=.2pt] coordinates {'+' '.join(f'({xx:.5g},{yy:.7g})'for xx,yy in poly)+'} --cycle;')
bands+=['\\end{axis}\\end{tikzpicture}\\caption{PS6 Q4：$a=1$的Kronig--Penney模型，蓝区为允许能带，完整显示$0\\le\\lambda,\\sqrt{2E}\\le100$。边界由精确色散关系求根；横轴势垒增加使带变窄。}\\end{figure}']
(root/'chapters/figure-graduate-322-bands.tex').write_text('\n'.join(bands)+'\n')
