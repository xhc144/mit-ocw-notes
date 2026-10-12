"""Real band and elastic extensions of completed original Lab2 diamond SCF."""
from pathlib import Path
import argparse,concurrent.futures,json,hashlib,os,re,subprocess,time,xml.etree.ElementTree as ET
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def main(args):
    scratch=Path(args.scratch).resolve();scratch.mkdir(parents=True,exist_ok=True);pseudo=Path(args.pseudo).resolve();data=ROOT/'data';qa=ROOT/'qa';inputs=ROOT/'code/inputs/qe-diamond-extras';inputs.mkdir(parents=True,exist_ok=True)
    fit=json.loads((qa/'qe-lab2-equilibrium-fit.json').read_text());a=fit['a_bohr'];V0=a**3/4
    lattice=a/2*np.array([[-1.,0,1],[0,1,1],[-1,1,0]])
    env=os.environ.copy();env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1');started=time.time()
    def execute(tag,text,kind):
        folder=scratch/tag;folder.mkdir(exist_ok=True);infile=folder/'pw.in';log=folder/'pw.out'
        cached=infile.exists() and log.exists() and infile.read_text()==text and 'JOB DONE' in log.read_text()
        infile.write_text(text)
        if cached:
            exit_code=0
        else:
            with log.open('w') as stream:p=subprocess.run([args.pw,'-in',str(infile)],cwd=folder,env=env,stdout=stream,stderr=subprocess.STDOUT)
            exit_code=p.returncode
        out=log.read_text();energies=re.findall(r'!\s+total energy\s+=\s+([-+\d.eE]+)\s+Ry',out)
        good=bool(exit_code==0 and 'JOB DONE' in out and ('End of band structure calculation' in out if kind=='bands' else ('convergence has been achieved' in out and energies)))
        if kind=='relax':good=good and ('End of BFGS Geometry Optimization' in out or 'bfgs converged' in out)
        row={'name':tag,'kind':kind,'converged':good,'exit_code':exit_code,'reused_identical_already_executed_input':cached,'energy_Ry_per_cell':float(energies[-1]) if energies else None,'input_sha256':hashlib.sha256(infile.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'working_output':str(log)}
        (inputs/(tag+'.in')).write_text(text.replace(str(pseudo.parent),'./pseudo').replace(str(scratch),'./scratch'))
        print(tag,'converged',good,'seconds',round(time.time()-started,1),flush=True);return row
    base=f"""&CONTROL
 calculation='scf',prefix='diamond',pseudo_dir='{pseudo.parent}',outdir='{scratch/'bands-tmp'}',tprnfor=.true.,tstress=.true.
/
&SYSTEM
 ibrav=2,celldm(1)={a},nat=2,ntyp=1,ecutwfc=100,
/
&ELECTRONS
 mixing_beta=.7,conv_thr=1.d-10,
/
ATOMIC_SPECIES
 C 12.011 {pseudo.name}
ATOMIC_POSITIONS alat
 C 0 0 0
 C .25 .25 .25
K_POINTS automatic
 8 8 8 0 0 0
"""
    results=[execute('band-ground-scf',base,'scf')]
    points=np.array([[0,0,0],[0,1,0],[.5,1,0],[.75,.75,0],[0,0,0],[.5,.5,.5],[.25,1,.25],[.5,1,0],[.5,.5,.5],[.75,.75,0]])
    ks=[];distance=[];s=0.;ticks=[0.]
    for i in range(len(points)-1):
        length=np.linalg.norm(points[i+1]-points[i])
        for t in np.linspace(0,1,16,endpoint=False):ks.append((1-t)*points[i]+t*points[i+1]);distance.append(s+t*length)
        s+=length;ticks.append(s)
    ks.append(points[-1]);distance.append(s)
    band=base.replace("calculation='scf'","calculation='bands'").replace('ntyp=1,ecutwfc=100,','ntyp=1,ecutwfc=100,nbnd=8,')
    band=band[:band.index('K_POINTS')]+f'K_POINTS tpiba\n{len(ks)}\n'+'\n'.join(' '.join(map(str,k))+' 1.0' for k in ks)+'\n'
    br=execute('diamond-bands',band,'bands');results.append(br)
    # Low-verbosity PWSCF suppresses printed eigenvalues for >100 k points.
    # Its actual schema output retains all eigenvalues in Hartree units.
    xml=scratch/'bands-tmp/diamond.save/data-file-schema.xml';tree=ET.parse(xml);matches=[]
    for node in tree.iter():
        if node.tag.rsplit('}',1)[-1]=='ks_energies':
            eig=next(child for child in node if child.tag.rsplit('}',1)[-1]=='eigenvalues')
            matches.append([float(x) for x in eig.text.split()])
    eigen=np.array(matches)*27.211386245988
    assert len(eigen)==len(ks),(len(eigen),len(ks))
    vbm=float(eigen[:,:4].max());cbm=float(eigen[:,4:].min());eigen-=vbm
    np.savetxt(data/'diamond-eight-bands.csv',np.column_stack([distance,eigen]),delimiter=',',header='s,'+','.join('band'+str(i) for i in range(1,9)),comments='')
    (qa/'diamond-band-path.json').write_text(json.dumps({'labels':['Gamma','X','W','K','Gamma','L','U','W','L','K'],'cartesian_k_in_2pi_over_a':points.tolist(),'distance_ticks':ticks,'k_points':len(ks),'bands':8,'energy_reference':'maximum of four valence bands on displayed path','path_KS_gap_eV':cbm-vbm,'not_experimental_quasiparticle_gap':True},indent=2))
    tasks=[]
    for mode in ['uniaxial','orthorhombic','shear_clamped','shear_relaxed']:
        for delta in [-.008,-.004,0.,.004,.008]:tasks.append((mode,delta))
    def elastic(task):
        mode,delta=task;F=np.eye(3)
        if mode=='uniaxial':F[0,0]=1+delta
        elif mode=='orthorhombic':F=np.diag([1+delta,1-delta,1/(1-delta*delta)])
        else:F[0,1]=F[1,0]=delta;F[2,2]=1/(1-delta*delta)
        cell=lattice@F.T;atom=F@(np.ones(3)*a/4);tag=mode+f'-d{delta:+.4f}';folder=scratch/tag
        kind='relax' if mode=='shear_relaxed' else 'scf'
        text=f"""&CONTROL
 calculation='{kind}',prefix='diamond',pseudo_dir='{pseudo.parent}',outdir='{folder/'tmp'}',tprnfor=.true.,tstress=.true.,forc_conv_thr=5.d-6,nstep=100,
/
&SYSTEM
 ibrav=0,nat=2,ntyp=1,ecutwfc=100,
/
&ELECTRONS
 mixing_beta=.7,conv_thr=1.d-10,
/
"""
        if kind=='relax':text+="&IONS\n ion_dynamics='bfgs',\n/\n"
        text+=f'ATOMIC_SPECIES\n C 12.011 {pseudo.name}\nCELL_PARAMETERS bohr\n'+'\n'.join(' '.join(map(str,r)) for r in cell)+'\nATOMIC_POSITIONS bohr\n C 0 0 0\n C '+' '.join(map(str,atom))+'\nK_POINTS automatic\n 8 8 8 0 0 0\n'
        row=execute(tag,text,kind);row.update(mode=mode,delta=delta,cell_volume_bohr3=float(abs(np.linalg.det(cell))));return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:er=list(pool.map(elastic,tasks))
    results+=er;constants={};curves=[]
    for mode in ['uniaxial','orthorhombic','shear_clamped','shear_relaxed']:
        rr=[r for r in er if r['mode']==mode and r['converged']];x=np.array([r['delta'] for r in rr]);E=np.array([r['energy_Ry_per_cell'] for r in rr]);coef=np.polyfit(x,E-E.min(),2);k=coef[0]/V0
        constants[mode]={'energy_density_delta_squared_coefficient_Ry_bohr3':float(k),'actual_points':len(rr),'quadratic_fit_with_linear_stress_term':True}
        curves.extend([[mode,r['delta'],r['energy_Ry_per_cell']] for r in rr])
    C11=2*constants['uniaxial']['energy_density_delta_squared_coefficient_Ry_bohr3'];C12=C11-constants['orthorhombic']['energy_density_delta_squared_coefficient_Ry_bohr3'];C44c=constants['shear_clamped']['energy_density_delta_squared_coefficient_Ry_bohr3']/2;C44r=constants['shear_relaxed']['energy_density_delta_squared_coefficient_Ry_bohr3']/2
    (data/'diamond-elastic-curves.csv').write_text('mode,delta,E_Ry_per_cell\n'+'\n'.join(f'{m},{d},{e}' for m,d,e in curves)+'\n')
    report={'kind':'actual diamond band and elastic extra tasks, current public named PP and modern PWSCF','a_reference_bohr':a,'ecut_Ry':100,'k_grid':[8,8,8],'rows':results,'failed':[r for r in results if not r['converged']],'elastic_coefficients':constants,'elastic_GPa':dict(C11=float(C11*14710.5079),C12=float(C12*14710.5079),C44_clamped=float(C44c*14710.5079),C44_relaxed=float(C44r*14710.5079)),'limits':['small finite strains and one cutoff/k mesh, further convergence is independently testable','normal-strain diamond internal forces vanish by symmetry in these patterns; shear relaxed separately','band gap is a path-sampled Kohn-Sham gap, not experimental gap'],'wall_seconds':time.time()-started}
    (qa/'qe-diamond-extra-actual-runs.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('Diamond extra tasks complete',report['elastic_GPa'],flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--pw',required=True);ap.add_argument('--pseudo',required=True);ap.add_argument('--scratch',required=True);ap.add_argument('--workers',type=int,default=2);main(ap.parse_args())
