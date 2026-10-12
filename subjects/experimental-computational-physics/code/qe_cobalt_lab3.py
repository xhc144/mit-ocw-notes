"""Actual public Lab3 cobalt input family with the named official US pseudopotential."""
from pathlib import Path
import argparse,concurrent.futures,json,hashlib,os,re,subprocess,time,urllib.request
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
URL='https://pseudopotentials.quantum-espresso.org/upf_files/Co.pz-nd-rrkjus.UPF'
def main(args):
    scratch=Path(args.scratch).resolve();scratch.mkdir(parents=True,exist_ok=True)
    pseudo=Path(args.pseudo).resolve()
    if not pseudo.exists():pseudo.parent.mkdir(parents=True,exist_ok=True);urllib.request.urlretrieve(URL,pseudo)
    data=ROOT/'data';qa=ROOT/'qa';inputs=ROOT/'code/inputs/qe-lab3-cobalt';inputs.mkdir(parents=True,exist_ok=True)
    groups={};specs=[]
    def add(group,name,a,c,k,structure='hcp',mag=.7):
        spec={'name':name,'a_bohr':float(a),'c_bohr':float(c),'k':list(k),'structure':structure,'starting_magnetization':mag}
        specs.append(spec);groups.setdefault(group,[]).append(name)
    for k in [4,6,8,10,12,14,16]:add('FCC_k_convergence',f'fcc-k{k}',6.483,0,(k,k,k),'fcc')
    for k in [4,6,8,10,12]:add('HCP_k_convergence',f'hcp-k{k}',4.58,7.438,(k,k,max(1,k//2)))
    for kz in [2,3,4,5,6,8]:add('HCP_c_k_convergence',f'hcp-c-k{kz}',4.58,7.438,(9,9,kz))
    for a in np.arange(6.39,6.601,.03):add('FCC_lattice_scan',f'fcc-a{a:.3f}',a,0,(16,16,16),'fcc')
    for a in np.arange(4.48,4.661,.03):add('HCP_ideal_ca_scan',f'hcp-ideal-a{a:.3f}',a,a*np.sqrt(8/3),(12,12,6))
    for a in [4.54,4.56,4.58,4.60,4.62]:
        for c in [7.36,7.40,7.44,7.48,7.52]:add('HCP_a_c_scan',f'hcp-a{a:.2f}-c{c:.2f}',a,c,(12,12,6))
    ahex=6.483/np.sqrt(2);add('FCC_hex_check','fcc-hex',ahex,ahex*np.sqrt(6),(12,12,4),'hex-fcc')
    for n in [3,5,7,9]:add('HCP_stacking_fault',f'fault-{n}',4.58,n*7.438/2,(8,8,max(1,round(12/n))),f'fault-{n}')
    for structure,alist in [('hcp',[4.10,4.25,4.40,4.58,4.75]),('fcc',[5.80,6.,6.20,6.40,6.483,6.70])]:
        for a in alist:
            for mag in [.7,0.]:add('pressure_moment_scan',f'pressure-{structure}-a{a:.3f}-m{mag}',a,a*7.438/4.58 if structure=='hcp' else 0,(12,12,6) if structure=='hcp' else (16,16,16),structure,mag)
    def run(spec):
        name=spec['name'];structure=spec['structure'];folder=scratch/name;folder.mkdir(exist_ok=True)
        if structure=='fcc':ibrav=2;coords=[(0.,0.,0.)]
        elif structure=='hcp':ibrav=4;coords=[(1/3,2/3,.25),(2/3,1/3,.75)]
        elif structure=='hex-fcc':ibrav=4;coords=[(1/3,2/3,0.),(2/3,1/3,1/3),(0.,0.,2/3)]
        else:
            ibrav=4;n=int(structure.split('-')[1]);coords=[]
            for i in range(n):
                xy=(1/3,2/3) if i==0 or (i>=3 and i%2) else ((2/3,1/3) if i==1 else (0.,0.))
                coords.append((*xy,(i+.5)/n))
        pos='\n'.join(' Co '+ ' '.join(f'{v:.10f}' for v in xyz) for xyz in coords)
        ca=f",celldm(3)={spec['c_bohr']/spec['a_bohr']:.12f}" if ibrav==4 else ''
        k=spec['k'];text=f"""&CONTROL
 calculation='scf',prefix='cobalt',restart_mode='from_scratch',pseudo_dir='{pseudo.parent}',outdir='{folder/'tmp'}',tprnfor=.true.,tstress=.true.
/
&SYSTEM
 ibrav={ibrav},celldm(1)={spec['a_bohr']:.12f}{ca},nat={len(coords)},ntyp=1,
 ecutwfc=30,ecutrho=250,nspin=2,starting_magnetization(1)={spec['starting_magnetization']},
 occupations='smearing',smearing='cold',degauss=.03,
/
&ELECTRONS
 mixing_beta=.7,conv_thr=1.d-9,electron_maxstep=200,
/
ATOMIC_SPECIES
 Co 58.933 {pseudo.name}
ATOMIC_POSITIONS crystal
{pos}
K_POINTS automatic
 {k[0]} {k[1]} {k[2]} 0 0 0
"""
        infile=folder/'pw.in';infile.write_text(text);log=folder/'pw.out';env=os.environ.copy();env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
        with log.open('w') as stream:p=subprocess.run([args.pw,'-in',str(infile)],cwd=folder,env=env,stdout=stream,stderr=subprocess.STDOUT)
        out=log.read_text();E=re.findall(r'!\s+total energy\s+=\s+([-+\d.eE]+)\s+Ry',out);M=re.findall(r'total magnetization\s*=\s*([-+\d.eE]+)',out);P=re.findall(r'P=\s*([-+\d.eE]+)',out);K=re.findall(r'number of k points\s*=\s*(\d+)',out)
        row={**spec,'nat':len(coords),'exit_code':p.returncode,'converged':bool(E and 'convergence has been achieved' in out and 'JOB DONE' in out),'energy_Ry_per_cell':float(E[-1]) if E else None,'energy_Ry_per_atom':float(E[-1])/len(coords) if E else None,'total_magnetization_muB':float(M[-1]) if M else None,'magnetization_muB_per_atom':float(M[-1])/len(coords) if M else None,'pressure_GPa':float(P[-1])/10 if P else None,'unique_k':int(K[-1]) if K else None,'input_sha256':hashlib.sha256(infile.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'working_output':str(log)}
        (inputs/(name+'.in')).write_text(text.replace(str(pseudo.parent),'./pseudo').replace(str(folder/'tmp'),'./tmp-'+name))
        print(name,'converged',row['converged'],'seconds',round(time.time()-started,1),flush=True);return row
    started=time.time();rows=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for row in pool.map(run,specs):rows.append(row)
    lookup={r['name']:r for r in rows};numeric=[]
    for r in rows:
        if r['converged']:numeric.append([r['a_bohr'],r['c_bohr'],r['nat'],r['k'][0],r['k'][2],r['energy_Ry_per_atom'],r['magnetization_muB_per_atom'],r['pressure_GPa']])
    np.savetxt(data/'qe-cobalt-all.csv',numeric,delimiter=',',header='a_bohr,c_bohr,nat,k_ab,k_c,E_Ry_per_atom,M_muB_per_atom,P_GPa',comments='')
    for group,names in groups.items():
        numeric=[]
        for name in names:
            r=lookup[name]
            if r['converged']:numeric.append([r['a_bohr'],r['c_bohr'],r['nat'],r['k'][0],r['k'][2],r['energy_Ry_per_atom'],r['magnetization_muB_per_atom'],r['pressure_GPa'],r['starting_magnetization']])
        np.savetxt(data/('qe-cobalt-'+group+'.csv'),numeric,delimiter=',',header='a_bohr,c_bohr,nat,k_ab,k_c,E_Ry_per_atom,M_muB_per_atom,P_GPa,starting_magnetization',comments='')
    report={'kind':'real modern PWSCF execution of specified public Lab3 Co model/input family','pseudo':{'url':URL,'filename':pseudo.name,'sha256':hashlib.sha256(pseudo.read_bytes()).hexdigest(),'current_official_copy_not_proven_byte_identical_to_2005':True,'not_redistributed':True},'parameters':{'ecut_Ry':30,'ecutrho_Ry':250,'nspin':2,'smearing':'cold','degauss_Ry':.03,'original_handout_k_offset':[0,0,0]},'groups':{k:[lookup[n] for n in names] for k,names in groups.items()},'failed_jobs':[r for r in rows if not r['converged']],'executed_jobs':len(rows),'pressure_scan_limit':'shape held at specified c/a; pressure is mean stress, not a full variable-shape enthalpy optimization; competing magnetic starts retained','stacking_fault_limit':'original up-to10-layer bound retained; finite-layer and k-c convergence reported','wall_seconds':time.time()-started}
    (qa/'qe-cobalt-lab3-actual-runs.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('Co tasks finished',len(rows),'failed',len(report['failed_jobs']),flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--pw',required=True);ap.add_argument('--pseudo',required=True);ap.add_argument('--scratch',required=True);ap.add_argument('--workers',type=int,default=2);main(ap.parse_args())
