#!/usr/bin/env python3
"""Reproduce required finite numerical experiments; no network or data downloads."""
import itertools,json,math,pathlib,hashlib
import numpy as np
R=pathlib.Path(__file__).resolve().parents[1];Q=R/'qa';F=R/'figures';Q.mkdir(exist_ok=True);F.mkdir(exist_ok=True)
result={'scope':'Finite numerical checks and requested plots; not a proof of general physical models','seed':851205}
def figure(name,curves,xlabel,ylabel,title,opts=''):
 s='\\begin{center}\\begin{tikzpicture}\\begin{axis}[width=11cm,height=5.7cm,xlabel={'+xlabel+'},ylabel={'+ylabel+'},title={'+title+'},'+opts+']\n'
 colors=['structurecolor','main','blue','gray','orange','teal','black']
 for i,(x,y,label) in enumerate(curves):
  s+='\\addplot[thick,color='+colors[i%len(colors)]+'] coordinates {'+' '.join(f'({a:.8g},{b:.8g})'for a,b in zip(x,y))+'};\n'
  if label:s+='\\addlegendentry{'+label+'}\n'
 s+='\\end{axis}\\end{tikzpicture}\\end{center}\n';(F/(name+'.tex')).write_text(s)
# Aluminum: plane-wave folding and independently obtained analytical splittings.
a=4.05;h2m=3.80998212;ec=14.399645;vol=a**3/4;q0=2*math.pi/a
V=lambda g:-4*math.pi*ec*3*math.cos(q0*np.linalg.norm(g)*.6)/((q0*np.linalg.norm(g))**2*vol)
v1,v2=V(np.ones(3)),V(np.array([2,0,0]));ef=h2m*(3*math.pi**2*3/vol)**(2/3)
result['aluminum']={'a_A':a,'V111_eV':v1,'V200_eV':v2,'X_splitting_eV':2*abs(v2),'L_splitting_eV':2*abs(v1),'W_offsets_eV':sorted([-v2,-v2,v2-2*v1,v2+2*v1]),'free_fermi_eV':ef}
gs=np.array([g for g in itertools.product(range(-4,5),repeat=3)if all(x%2==0 for x in g)or all(x%2!=0 for x in g)],float)
points=np.array([[0,0,0],[1,0,0],[1,.5,0],[.5,.5,.5],[0,0,0]])
x=[];bands=[[],[]]
for j in range(4):
 for t in np.linspace(0,1,61,endpoint=j==3):
  k=(1-t)*points[j]+t*points[j+1];e=np.sort(h2m*q0*q0*np.sum((gs+k)**2,axis=1));x.append(j+t)
  for n in range(2):bands[n].append(e[n])
figure('al-free',[(x,bands[0],'第一带'),(x,bands[1],'第二带')],'路径','能量/eV','Al自由电子折叠带',r'xtick={0,1,2,3,4},xticklabels={$\Gamma$,$X$,$W$,$L$,$\Gamma$},legend pos=north east')
# CuO2 constant-energy contours; filling from a full BZ grid.
k=np.linspace(-math.pi,math.pi,801,endpoint=False);s=(1-np.cos(k[:,None]))/2+(1-np.cos(k[None,:]))/2
cont=[];levels={}
for p in [0,.15,.3]:
 lev=float(np.quantile(s,(1-p)/2));levels[str(p)]=lev
 xx=np.linspace(-math.pi,math.pi,1201);cy=2-2*lev-np.cos(xx);ok=np.abs(cy)<=1;xx=xx[ok];yy=np.arccos(cy[ok]);cont.append((np.r_[xx,xx[::-1]],np.r_[yy,-yy[::-1]],f'$p={p:g}$'))
figure('cu-contours',cont,'$k_xa$','$k_ya$','CuO$_2$模型的费米面',r'axis equal image,xmin=-3.2,xmax=3.2,ymin=-3.2,ymax=3.2,legend pos=outer north east')
result['CuO2_filling']={'upper_band_electrons_per_cell':'1-p; two spin states','grid':801,'s_levels':levels}
# Hubbard dimer: Fock operators, independent of analytic singlet reduction.
def annihilate(state,i):
 if not state>>i&1:return None
 return state^(1<<i),(-1)**((state&((1<<i)-1)).bit_count())
def create(state,i):
 if state>>i&1:return None
 return state^(1<<i),(-1)**((state&((1<<i)-1)).bit_count())
U,t=7.,1.3;sector={}
for n in range(1,5):
 states=[i for i in range(16)if i.bit_count()==n];M=np.zeros((len(states),len(states)));ix={s:i for i,s in enumerate(states)}
 for j,state in enumerate(states):
  M[j,j]=U*((state&3==3)+((state>>2)&3==3))
  for i,b in [(0,2),(2,0),(1,3),(3,1)]:
   first=annihilate(state,b)
   if first:
    second=create(first[0],i)
    if second:M[ix[second[0]],j]+=t*first[1]*second[1]
 e,vec=np.linalg.eigh(M);sector[str(n)]={'basis_occupied_orbital_bits':states,'matrix':M.tolist(),'eigenvalues':e.tolist(),'eigenvectors_columns':vec.tolist()}
expected=sorted([0,0,0,U,(U-math.sqrt(U*U+16*t*t))/2,(U+math.sqrt(U*U+16*t*t))/2]);err=max(abs(np.array(expected)-sector['2']['eigenvalues']));assert err<1e-10
result['hubbard']={'U':U,'t':t,'analytic_error':err,'sectors':sector}
# Anderson/Thouless experiments, positive and signed curvatures both retained.
rng=np.random.default_rng(851205)
def ring(M,onsite,phi):
 H=np.diag(onsite.astype(complex))
 for j in range(M-1):H[j,j+1]=H[j+1,j]=1
 H[M-1,0]=np.exp(1j*phi);H[0,M-1]=np.exp(-1j*phi);return H
phi=np.linspace(-math.pi,math.pi,81);onsite=rng.uniform(-2,2,19);base=np.linalg.eigvalsh(ring(19,onsite,0));ind=np.argsort(abs(base))[:10];ind=np.sort(ind);energies=np.array([np.linalg.eigvalsh(ring(19,onsite,p))[ind]for p in phi]);figure('anderson-levels',[(phi,energies[:,j],None)for j in range(10)],'$\phi$','$E/t$','一维无序环：$N=20$，10个能级')
records=[]
for M in [19,39,79,139]:
 absvals=[];signed=[];spacing=[];steps=[]
 for sample in range(40):
  onsite=rng.uniform(-2,2,M);e0=np.linalg.eigvalsh(ring(M,onsite,0));i=np.sort(np.argsort(abs(e0))[:10]);sp=(e0[i[-1]]-e0[i[0]])/9
  cur=[]
  for step in [.002,.001]:
   ep=np.linalg.eigvalsh(ring(M,onsite,step));em=np.linalg.eigvalsh(ring(M,onsite,-step));cur.append((ep[i]+em[i]-2*e0[i])/step**2)
  absvals.append(np.mean(abs(cur[1])));signed.append(np.mean(cur[1]));spacing.append(sp);steps.append(float(np.max(abs(cur[1]-cur[0]))))
 records.append({'N_source':M+1,'independent_sites':M,'samples':40,'mean_abs_curvature':float(np.mean(absvals)),'mean_signed_curvature':float(np.mean(signed)),'mean_spacing':float(np.mean(spacing)),'g':float(np.mean(absvals)/np.mean(spacing)),'max_step_difference':max(steps)})
result['anderson_1D']=records;figure('anderson-g',[(np.array([x['N_source']for x in records]),np.array([x['g']for x in records]),'$W/t=2$')],'$N$','$g$','有限样本Thouless电导尺度',r'ymode=log,mark=*')
def square(L,W,phi,onsite):
 H=np.diag(onsite.astype(complex))
 for y in range(L):
  for x in range(L):
   i=y*L+x;j=y*L+(x+1)%L;v=np.exp(1j*phi)if x==L-1 else 1.;H[i,j]+=v;H[j,i]+=np.conj(v)
   j=((y+1)%L)*L+x;H[i,j]+=1;H[j,i]+=1
 return H
rec2=[]
for W in [4.,9.]:
 for L in [4,6,8]:
  cur=[];sp=[]
  for sample in range(24):
   site=rng.uniform(-W,W,L*L);e0=np.linalg.eigvalsh(square(L,W,0,site));ii=np.sort(np.argsort(abs(e0))[:10]);ep=np.linalg.eigvalsh(square(L,W,.001,site));em=np.linalg.eigvalsh(square(L,W,-.001,site));cur.append(np.mean(abs((ep[ii]+em[ii]-2*e0[ii])/1e-6)));sp.append((e0[ii[-1]]-e0[ii[0]])/9)
  rec2.append({'W':W,'L':L,'samples':24,'g':float(np.mean(cur)/np.mean(sp))})
result['anderson_2D_optional']=rec2
figure('anderson-2d',[(np.array([r['L']for r in rec2 if r['W']==W]),np.array([r['g']for r in rec2 if r['W']==W]),f'$W/t={W:g}$')for W in [4.,9.]],'$L$','$g$','二维有限尺寸对照',r'ymode=log,mark=*')
# Mattis-Bardeen: sin^2 substitution removes endpoint singularities.
def mb(w,n):
 if w<=2:return 0.
 a,b=np.polynomial.legendre.leggauss(n);theta=(a+1)*math.pi/4;d=w-2;s=np.sin(theta)**2;c=1-s;E=1+d*s;E2=1+d*c
 return float(np.sum(b*2*(E*E2-1)/np.sqrt((2+d*s)*(2+d*c)))*math.pi/4/w)
w=np.r_[np.linspace(0,1.9,12),np.linspace(2,8,101),np.linspace(8.5,20,24)];vals=np.array([mb(x,120)for x in w]);mb_err=max(abs(mb(x,120)-mb(x,240))for x in [2.001,2.1,3,5,10,20]);assert mb_err<1e-9
result['Mattis_Bardeen']={'quadrature_error':mb_err,'values':[[float(x),float(y)]for x,y in zip(w,vals)]};figure('mattis-bardeen',[(w,vals,None)],'$\omega/\Delta$','$\sigma_1/\sigma_N$','零温脏极限光吸收',r'xmin=0,ymin=0,ymax=1.05')
# 3D AII mass constraints in an independent full real matrix basis.
s0=np.eye(2);s1=np.array([[0.,1],[1,0]]);s3=np.diag([1.,-1]);eps=np.array([[0.,1],[-1,0]])
kron=lambda a,b,c:np.kron(np.kron(a,b),c)
gam=[kron(s0,s1,s3),kron(eps,eps,s3),kron(s0,s3,s3)];charge=kron(eps,s0,s0);time=kron(s3,eps,s0)
basis=[kron(a,b,c)for a,b,c in itertools.product([s0,s1,s3,eps],repeat=3)]
constraints=np.stack([np.concatenate([(M+M.T).ravel(),(M@charge-charge@M).ravel(),*[(M@g+g@M).ravel()for g in gam+[time]]])for M in basis],axis=1)
rank=int(np.linalg.matrix_rank(constraints,tol=1e-10));assert rank==63
mass=kron(eps,s0,s1);resid=max(np.linalg.norm(mass@g+g@mass)for g in gam+[time]);assert resid<1e-12
result['3d_mass']={'constraint_rank':rank,'nullity':64-rank,'residual':float(resid),'mass_square_error':float(np.linalg.norm(mass@mass+np.eye(8)))}
# Open Majorana spectra versus independently solved boundary equation.
majorana={}
for ratio in [0,.3,.7,1.,1.3]:
 L=20;D=np.diag(np.full(L,ratio))-np.diag(np.ones(L-1),-1);sv=np.sort(2*np.linalg.svd(D,compute_uv=False));majorana[str(ratio)]={'L':L,'energies':sv.tolist(),'edge_estimate':2*(1-ratio*ratio)*ratio**L if ratio<1 else None}
result['open_Majorana']=majorana
result['generated_figures']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in F.glob('*.tex')}
(Q/'numerical-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('Generated',len(result['generated_figures']),'vector figures; numeric checks saved.')
