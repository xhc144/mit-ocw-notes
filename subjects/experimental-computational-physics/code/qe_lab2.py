"""Execute the actual public Lab2 diamond input family with a supplied pw.x.

The named C.pz-vbc.UPF is fetched from the official QE library only when absent.
UPF/binaries are not redistributed; provenance hashes and real run output are kept.
"""
from pathlib import Path
import argparse,concurrent.futures,json,hashlib,os,re,subprocess,time,urllib.request
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
URL='https://pseudopotentials.quantum-espresso.org/upf_files/C.pz-vbc.UPF'
def main(args):
    scratch=Path(args.scratch).resolve();scratch.mkdir(parents=True,exist_ok=True)
    pseudo=Path(args.pseudo).resolve()
    if not pseudo.exists():
        pseudo.parent.mkdir(parents=True,exist_ok=True);urllib.request.urlretrieve(URL,pseudo)
    output=ROOT/'data';qa=ROOT/'qa';inputs=ROOT/'code/inputs/qe-lab2';output.mkdir(exist_ok=True);qa.mkdir(exist_ok=True);inputs.mkdir(parents=True,exist_ok=True)
    groups={
        'energy_cutoff':[(6.6,float(c),4,0.) for c in range(10,151,10)],
        'energy_kgrid':[(6.6,100.,k,0.) for k in range(2,13)],
        'force_cutoff':[(6.6,float(c),4,.05) for c in range(30,111,5)],
        'force_kgrid':[(6.6,100.,k,.05) for k in range(2,13)],
        'difference_cutoff':[(a,float(c),8,0.) for c in range(20,121,10) for a in [6.70,6.74]],
        'equilibrium':[(float(a),100.,8,0.) for a in np.linspace(6.55,6.8,11)]}
    if args.smoke:groups={'smoke':[(6.6,40.,4,0.)]}
    all_specs=sorted(set(x for values in groups.values() for x in values));results={};started=time.time()
    def run(spec):
        a,cut,k,z=spec;tag=f'a{a:.5f}-c{cut:.1f}-k{k}-z{z:.2f}';folder=scratch/tag;folder.mkdir(exist_ok=True)
        source=f"""&CONTROL
 calculation='scf',restart_mode='from_scratch',prefix='diamond',
 pseudo_dir='{pseudo.parent}',outdir='{folder/'tmp'}',tprnfor=.true.,tstress=.true.
/
&SYSTEM
 ibrav=2,celldm(1)={a:.10f},nat=2,ntyp=1,ecutwfc={cut},
/
&ELECTRONS
 diagonalization='david',mixing_mode='plain',mixing_beta=.7,conv_thr=1.d-9,
/
ATOMIC_SPECIES
 C 12.011 {pseudo.name}
ATOMIC_POSITIONS alat
 C 0 0 0
 C .25 .25 {(.25+z):.10f}
K_POINTS automatic
 {k} {k} {k} 0 0 0
"""
        infile=folder/'pw.in';logfile=folder/'pw.out';infile.write_text(source)
        env=os.environ.copy();env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
        with logfile.open('w') as stream:
            proc=subprocess.run([args.pw,'-in',str(infile)],cwd=folder,env=env,stdout=stream,stderr=subprocess.STDOUT)
        text=logfile.read_text();energy=re.findall(r'!\s+total energy\s+=\s+([-+\d.eE]+)\s+Ry',text)
        forces=re.findall(r'atom\s+(\d+)\s+type\s+\d+\s+force\s*=\s*([-+\d.eE]+)\s+([-+\d.eE]+)\s+([-+\d.eE]+)',text)
        nk=re.findall(r'number of k points\s*=\s*(\d+)',text)
        result={'a_bohr':a,'ecut_Ry':cut,'k_grid':k,'z_displacement_alat':z,'exit_code':proc.returncode,'converged':bool(energy and 'convergence has been achieved' in text and 'JOB DONE' in text),'input_sha256':hashlib.sha256(infile.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(logfile.read_bytes()).hexdigest(),'working_output':str(logfile),'unique_k_points':int(nk[-1]) if nk else None,'energy_Ry_per_primitive_cell':float(energy[-1]) if energy else None,'forces_Ry_per_bohr':[[int(v[0]),*map(float,v[1:])] for v in forces[-2:]]}
        # Portable exact input: replace only task-specific directory locations.
        portable=source.replace(str(pseudo.parent),'./pseudo').replace(str(folder/'tmp'),'./tmp-'+tag)
        (inputs/(tag+'.in')).write_text(portable)
        print(tag,'converged',result['converged'],'seconds',round(time.time()-started,1),flush=True)
        return spec,result
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for spec,result in pool.map(run,all_specs):results[spec]=result
    failed=[r for r in results.values() if not r['converged']]
    # Retain failed computations with their actual status; do not fill missing data.
    for name,specs in groups.items():
        rows=[]
        for spec in specs:
            r=results[spec]
            if not r['converged']:continue
            force_z=r['forces_Ry_per_bohr'][-1][-1] if r['forces_Ry_per_bohr'] else np.nan
            rows.append([r['a_bohr'],r['ecut_Ry'],r['k_grid'],r['z_displacement_alat'],r['unique_k_points'],r['energy_Ry_per_primitive_cell'],r['energy_Ry_per_primitive_cell']/2,force_z])
        np.savetxt(output/('qe-lab2-'+name+'.csv'),rows,delimiter=',',header='a_bohr,ecut_Ry,k_grid,z_displacement_alat,unique_k,E_Ry_per_cell,E_Ry_per_atom,force_z_Ry_per_bohr',comments='')
    version=next((line.strip() for r in results.values() for line in Path(r['working_output']).read_text().splitlines() if 'Program PWSCF' in line),'unknown')
    report={'kind':'real PWSCF execution of original Lab2 input family, current official named pseudopotential copy; not toy plane-wave Hamiltonian','source_handout':'MIT3.320 Spring2005 pwscf_handout.pdf','original_handout_software_version':'2.1.2','actual_software_version':version,'pseudo':{'filename':pseudo.name,'official_url':URL,'sha256':hashlib.sha256(pseudo.read_bytes()).hexdigest(),'bytes':pseudo.stat().st_size,'current_UPF_conversion_not_proven_byte_identical_to_2005_file':True,'file_not_redistributed':True},'parameters':{'K_point_offset':[0,0,0],'coordinates':'alat Cartesian axes, atom2 z=.25+.05 for force tasks','nat_primitive':2,'convergence_threshold_Ry':1e-9,'energy_Ry_to_eV':13.605693122994,'bohr_to_A':.529177210903},'groups':{k:[results[s] for s in specs] for k,specs in groups.items()},'executed_unique_jobs':len(results),'failed_jobs':failed,'workers':args.workers,'wall_seconds':time.time()-started}
    (qa/'qe-lab2-actual-runs.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    if failed:print('Actual failed jobs',len(failed),flush=True)
    print('PWSCF Lab2 complete',len(results),'jobs',flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--pw',required=True);ap.add_argument('--pseudo',required=True);ap.add_argument('--scratch',required=True);ap.add_argument('--workers',type=int,default=2);ap.add_argument('--smoke',action='store_true');main(ap.parse_args())
