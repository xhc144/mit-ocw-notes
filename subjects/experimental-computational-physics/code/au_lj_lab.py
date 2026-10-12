"""Actual static subproblems with the public Au LJ coefficients and 40 A cutoff.

Unshifted pair potential; full periodic perfect lattice, periodic *unrelaxed*
vacancy arrays, and unrelaxed (100) slabs. This is not a GULP or EAM run.
"""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import minimize_scalar
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'data';Q=ROOT/'qa';O.mkdir(exist_ok=True);Q.mkdir(exist_ok=True)
A,B,rc=214180.2,625.482,40.
cells=np.array(np.meshgrid(*([np.arange(-15,16)]*3),indexing='ij')).reshape(3,-1).T
basis=np.array([[0,0,0],[0,.5,.5],[.5,0,.5],[.5,.5,0]])
vectors=(cells[:,None,:]+basis[None,:,:]).reshape(-1,3)
norm=np.linalg.norm(vectors,axis=1);mask=norm>1e-12;vectors=vectors[mask];norm=norm[mask]
def pair(r):return A/r**12-B/r**6
def per_atom(a):
    r=a*norm;return float(.5*pair(r[r<rc]).sum())
fit=minimize_scalar(per_atom,bounds=(3.9,4.3),method='bounded',options={'xatol':1e-10})
a=float(fit.x);e=per_atom(a)
scan=np.array([[x,per_atom(x)] for x in np.linspace(a-.12,a+.12,49)])
np.savetxt(O/'au-lj-static-lattice.csv',scan,delimiter=',',header='a_A,E_eV_per_atom',comments='')
vac=[]
for n in [2,3,4,5,6,8]:
    d=np.linalg.norm(cells,axis=1)*n*a;vimage=float(pair(d[(d>0)&(d<rc)]).sum())
    Ef=-e+.5*vimage
    vac.append([n,4*n**3,Ef,Ef/(-e)])
np.savetxt(O/'au-lj-unrelaxed-vacancy.csv',vac,delimiter=',',header='cells_per_axis,N_sites,Ef_eV,Ef_over_cohesive_magnitude',comments='')
r=a*norm;active=r<rc;zlayer=np.round(2*vectors[active,2]).astype(int);v=pair(r[active]);positive=zlayer>0
layers=zlayer[positive];values=v[positive];area_density=2/a**2
surface=[]
for M in [2,4,8,12,16,20,24,32]:
    gamma=float(-.5*area_density*np.sum(np.minimum(layers,M)*values))
    surface.append([M,gamma,gamma*16.02176634])
np.savetxt(O/'au-lj-unrelaxed-surface.csv',surface,delimiter=',',header='atomic_layers,gamma_eV_per_A2,gamma_J_per_m2',comments='')
# Local expansion bulk modulus, per atom V=a^3/4.
v0=a**3/4;dv=v0*1e-3
EV=lambda volume:per_atom((4*volume)**(1/3))
curvature=(EV(v0+dv)-2*EV(v0)+EV(v0-dv))/dv**2
out={'kind':'actually executed static pair-model subproblems; original GULP/EAM not run','potential':{'A_eV_A12':A,'B_eV_A6':B,'cutoff_A':rc,'shift':'none'},'perfect_FCC':{'a_A':a,'energy_eV_per_atom':e,'cohesive_energy_magnitude_eV':-e,'volume_per_atom_A3':v0,'local_bulk_modulus_eV_per_A3':v0*curvature},'vacancies':{'condition':'fixed cell and all remaining atoms fixed, periodic vacancy images retained','rows':vac,'formula':'Ef=-e_bulk+0.5*sum_nonzero_vacancy_images v(R)'},'surface_100':{'condition':'unrelaxed planar slabs, two equivalent faces, vacuum isolation implicit in removing inter-slab bonds','rows':surface,'formula':'gamma_M=-(rho_layer/2)*sum_{n>0}min(n,M)*w_n','rho_layer_per_A2':area_density},'not_executed':['atomic and cell relaxation of defective GULP cells','EAM tasks: original referenced potential input not included in retrieved materials','relaxed surface structures and optional EAM elastic constants']}
(Q/'au-lj-public-lab-analysis.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
