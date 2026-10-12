"""Run the original MIT Lab3 Ba/Ti/O potential family in modern PWSCF.

The external potentials are obtained from the MIT Lab3 archive; neither the
potentials nor binaries are redistributed. All output here is computation.
"""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,os,re,subprocess,time
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def main(args):
    scratch=Path(args.scratch).resolve();scratch.mkdir(parents=True,exist_ok=True)
    pseudo=Path(args.pseudo).resolve()
    for p in ['Ba.UPF','Ti.UPF','O.UPF']:assert (pseudo/p).is_file()
    inputs=ROOT/'code/inputs/qe-lab3-batio3';inputs.mkdir(parents=True,exist_ok=True)
    started=time.time();rows=[]
    def run(name,a,d=0.,mode='scf'):
        folder=scratch/name;folder.mkdir(exist_ok=True)
        flags='0 0 0' if mode=='oxygen_relax' else '1 1 1'
        ti='0 0 0' if mode=='oxygen_relax' else '1 1 1'
        calc='relax' if mode!='scf' else 'scf'
        ions="&IONS\n ion_dynamics='bfgs'\n/\n" if calc=='relax' else ''
        text=f"""&CONTROL
 calculation='{calc}',prefix='batio3',restart_mode='from_scratch',
 pseudo_dir='{pseudo}',outdir='{folder/'tmp'}',tstress=.true.,tprnfor=.true.,
 forc_conv_thr=1.d-5,etot_conv_thr=1.d-7,nstep=100,
/
&SYSTEM
 ibrav=1,celldm(1)={a:.12f},nat=5,ntyp=3,ecutwfc=30,ecutrho=240,
/
&ELECTRONS
 diagonalization='cg',mixing_mode='plain',mixing_beta=.7,conv_thr=1.d-8,electron_maxstep=200,
/
{ions}ATOMIC_SPECIES
 Ba 137.327 Ba.UPF
 Ti 47.88 Ti.UPF
 O 15.9994 O.UPF
ATOMIC_POSITIONS crystal
 Ba 0 0 0 0 0 0
 Ti .5 .5 {0.5+d:.12f} {ti}
 O .5 .5 0 1 1 1
 O .5 0 .5 1 1 1
 O 0 .5 .5 1 1 1
K_POINTS automatic
 4 4 4 1 1 1
"""
        infile=folder/'pw.in';log=folder/'pw.out'
        cached=infile.exists() and infile.read_text()==text and log.exists() and 'JOB DONE' in log.read_text()
        infile.write_text(text)
        if not cached:
            env=os.environ.copy();env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
            with log.open('w') as f:p=subprocess.run([args.pw,'-in',str(infile)],cwd=folder,env=env,stdout=f,stderr=subprocess.STDOUT)
            status=p.returncode
        else:status=0
        out=log.read_text();E=re.findall(r'!\s+total energy\s+=\s+([-+\d.eE]+)\s+Ry',out)
        P=re.findall(r'P=\s*([-+\d.eE]+)',out);F=re.findall(r'Total force\s*=\s*([-+\d.eE]+)',out)
        blocks=re.findall(r'ATOMIC_POSITIONS \(crystal\)\s*\n((?:.*\n){5})',out)
        coords=[]
        if blocks:
            for line in blocks[-1].splitlines():
                vals=line.split();coords.append({'element':vals[0],'xyz':[float(x) for x in vals[1:4]]})
        row={'name':name,'a_bohr':a,'Ti_displacement_fractional':d,'mode':mode,'exit_code':status,'SCF_converged':bool(E and 'JOB DONE' in out and 'convergence NOT achieved' not in out),'ionic_converged':calc=='scf' or 'bfgs converged' in out,'E_Ry_per_5_atom_cell':float(E[-1]) if E else None,'pressure_GPa':float(P[-1])/10 if P else None,'total_force_Ry_bohr':float(F[-1]) if F else None,'final_positions':coords,'input_sha256':hashlib.sha256(infile.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'working_output':str(log),'identical_input_completed_output_reused':cached}
        (inputs/(name+'.in')).write_text(text.replace(str(pseudo),'./pseudo').replace(str(folder/'tmp'),'./tmp-'+name))
        print(name,row['SCF_converged'],row['ionic_converged'],row['E_Ry_per_5_atom_cell'],'seconds',round(time.time()-started,1),flush=True)
        return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        rows.extend(pool.map(lambda a:run(f'cubic-a{a:.3f}',a),[7.40,7.44,7.48,7.50,7.52,7.54,7.56,7.60,7.64,7.68]))
    good=[r for r in rows if r['SCF_converged']];assert len(good)==10
    agrid=np.array([r['a_bohr'] for r in good]);energy=np.array([r['E_Ry_per_5_atom_cell'] for r in good]);coef=np.polyfit(agrid-7.52,energy,4)
    roots=np.roots(np.polyder(coef));candidates=[7.52+float(v.real) for v in roots if abs(v.imag)<1e-8 and 7.4<7.52+v.real<7.68 and np.polyval(np.polyder(coef,2),v.real)>0];assert candidates
    afit=min(candidates,key=lambda a:np.polyval(coef,a-7.52))
    # Keep the original scan lattice a=7.52 for direct comparison, rather
    # than silently replacing it with the modern fitted value.
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        rows.extend(pool.map(lambda d:run(f'oxygen-relax-d{d:.3f}',7.52,d,'oxygen_relax'),[0.,.002,.004,.006,.008,.010,.012,.014,.016,.018,.020]))
    rows.append(run('full-Ti-O-relax',7.52,.015,'full_relax'))
    for mode in ['scf','oxygen_relax']:
        group=[r for r in rows if r['mode']==mode and r['SCF_converged']]
        np.savetxt(ROOT/'data'/f'qe-batio3-{mode}.csv',[[r['a_bohr'],r['Ti_displacement_fractional'],r['E_Ry_per_5_atom_cell'],r['pressure_GPa'],r['total_force_Ry_bohr'] or 0] for r in group],delimiter=',',header='a_bohr,d_Ti_fractional,E_Ry_cell,P_GPa,total_force_Ry_bohr',comments='')
    report={'executed_jobs':len(rows),'original_archive':'https://ocw.mit.edu/courses/3-320-atomistic-computer-modeling-of-materials-sma-5107-spring-2005/d8f0936c291ffeb28cb051a169ccbb23_3320_lab3.zip','pseudopotentials':[{'file':p,'sha256':hashlib.sha256((pseudo/p).read_bytes()).hexdigest(),'not_redistributed':True} for p in ['Ba.UPF','Ti.UPF','O.UPF']],'parameters':{'ecut_Ry':30,'ecutrho_Ry':240,'k_grid':[4,4,4],'k_offset':[1,1,1],'SCF_threshold_Ry':1e-8,'force_threshold_Ry_bohr':1e-5},'cubic_fitted_a_bohr':afit,'scan_a_bohr':7.52,'original_displacement_audit':'Original scripts scan Ti z=0.502 through 0.520 in steps .002. The official answer 0.08*a0 conflicts with its final fractional coordinates; retain that printed statement as ambiguous, do not change input to .08.','rows':rows,'failed_jobs':[r for r in rows if not r['SCF_converged'] or not r['ionic_converged']],'wall_seconds':time.time()-started}
    (ROOT/'qa/qe-batio3-lab3-actual-runs.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    assert not report['failed_jobs'],report['failed_jobs']

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--pw',required=True);ap.add_argument('--pseudo',required=True);ap.add_argument('--scratch',required=True);ap.add_argument('--workers',type=int,default=2);main(ap.parse_args())
