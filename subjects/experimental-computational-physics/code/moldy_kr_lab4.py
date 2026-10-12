"""Actual modern Moldy runs using public Lab4 Kr.in and Kr_SL.in.

No physical measurement is performed. Executables and potential archives remain
external dependencies. Only generated controls, numeric output and hashes are
published. Cluster scripts containing broad move operations are never executed.
"""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,re,shutil,subprocess,time
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def main(args):
    scratch=Path(args.scratch).resolve();scratch.mkdir(parents=True,exist_ok=True)
    original=Path(args.inputs).resolve();start=time.time()
    controls=ROOT/'code/inputs/moldy-kr';controls.mkdir(parents=True,exist_ok=True)
    specs=[('NPE-crystal',T) for T in [80,100,110,120,130,140,150,160]]+[('NVE-prepared-two-phase-v2',T) for T in [100,130,140]]
    def run(spec):
        mode,T=spec;name=f'{mode}-T{T}';d=scratch/name;d.mkdir(exist_ok=True)
        f='Kr.in' if mode=='NPE-crystal' else 'Kr_SL.in';shutil.copyfile(original/f,d/f)
        # 7.5 ps preparation, 42.5 ps production. Fixed absolute times.
        text=f'''title=public Lab4 Kr {name}
sys-spec-file={f}
step=.005
nsteps=10000
begin-average=1501
average-interval=500
temperature={T}
scale-interval=100
scale-end=1500
scale-options=4
lattice-start=1
begin-dump=1501
dump-interval=50
dump-level=3
ndumps=250
dump-file=Kr-dump
save-file=Kr-save
backup-file=
print-interval=50
roll-interval=100
page-length=200
page-width=150
cutoff=10
strict-cutoff=1
begin-rdf=1501
rdf-interval=20
rdf-limit=10
nbins=200
rdf-out=8500
'''
        if mode=='NPE-crystal':text+='const-pressure=1\nw=1000\npressure=0\nstrain-mask=238\n'
        startstep=0
        if mode!='NPE-crystal':
            assert args.prepared_restart, 'Prepare the original overlapping liquid initial coordinates first.'
            shutil.copyfile(args.prepared_restart,d/'prepared.restart')
            text=text.replace('sys-spec-file=Kr_SL.in','restart-file=prepared.restart').replace('lattice-start=1','lattice-start=0')
            # Moldy treats nsteps and window offsets on restart as NEW-run
            # relative quantities, and adds the stored initial step itself.
            startstep=5000
        text+='end\n'
        cached=(d/'control.in').exists() and (d/'control.in').read_text()==text and (d/'moldy.out').exists() and 'Run used' in (d/'moldy.out').read_text()
        (d/'control.in').write_text(text);(controls/(name+'.in')).write_text(text)
        if not cached:
            with (d/'moldy.out').open('w') as fobj:p=subprocess.run([args.moldy,'control.in'],cwd=d,stdout=fobj,stderr=subprocess.STDOUT)
            status=p.returncode
        else:status=0
        out=(d/'moldy.out').read_text();samples=[]
        for match in re.finditer(r'=+ Timestep\s+(\d+)\s+Current values[^\n]*\n\s*([^\n]+)',out):
            v=[float(x) for x in match[2].split()];assert len(v)>=10
            samples.append([int(match[1]),*v[:10]])
        samples=np.array(samples);assert samples.ndim==2 and len(samples)==200
        np.savetxt(ROOT/'data'/f'moldy-{name}.csv',samples,delimiter=',',header='step,K_trans_kJ_mol,K_rot_kJ_mol,U_kJ_mol,E_ext_kJ_mol,T_trans_K,T_rot_K,T_K,hxx_A,hyx_A,hzx_A',comments='')
        production=samples[samples[:,0]>startstep+1500];n=256 if mode=='NPE-crystal' else 1024
        row={'name':name,'ensemble':mode,'T_initial_K':T,'N_atoms':n,'exit_code':status,'number_of_printed_samples':len(samples),'production_T_K_mean':float(production[:,7].mean()),'production_T_K_std':float(production[:,7].std(ddof=1)),'production_U_kJ_mol_atom_mean':float(production[:,3].mean()/n),'production_extended_E_kJ_mol_atom_drift_linear_per_ps':float(np.polyfit(production[:,0]*.005,production[:,4]/n,1)[0]),'control_sha256':hashlib.sha256(text.encode()).hexdigest(),'input_sha256':hashlib.sha256((d/('Kr.in' if mode=='NPE-crystal' else 'Kr_SL.in')).read_bytes()).hexdigest(),'output_sha256':hashlib.sha256((d/'moldy.out').read_bytes()).hexdigest(),'working_output':str(d/'moldy.out'),'dump_files':[str(v) for v in sorted(d.glob('Kr-dump*'))],'identical_completed_run_reused':cached,'initial_step':startstep,'interpretation':'Initial T is not final T after rescaling stops. Melting requires structural/diffusive analysis; this thermodynamic mean alone does not establish a melting point.'}
        assert status==0
        print(name,row['production_T_K_mean'],'seconds',round(time.time()-start,1),flush=True);return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:rows=list(pool.map(run,specs))
    np.savetxt(ROOT/'data/moldy-kr-summary.csv',[[r['T_initial_K'],r['N_atoms'],r['production_T_K_mean'],r['production_T_K_std'],r['production_U_kJ_mol_atom_mean'],r['production_extended_E_kJ_mol_atom_drift_linear_per_ps']] for r in rows],delimiter=',',header='T_initial_K,N_atoms,T_mean_K,T_std_K,U_kJ_mol_atom,E_drift_kJ_mol_atom_ps',comments='')
    report={'kind':'actual MD computation with modern Moldy and original public Kr files; not observed krypton data','Moldy_source':'https://github.com/krefson/Moldy','parameters':{'dt_ps':.005,'equilibration_steps':1500,'production_steps':8500,'total_ps':50,'cutoff_A':10,'strict_cutoff':True,'tail_correction':'Moldy default distant potential/pressure correction retained and printed in raw output','epsilon_convention':'5.4516 kJ/mol multiplies (sigma/r)^12-(sigma/r)^6; well depth is one quarter','sigma_A':3.83,'mass_amu':83.8},'rows':rows,'wall_seconds':time.time()-start}
    (ROOT/'qa/moldy-kr-actual-runs.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--moldy',required=True);ap.add_argument('--inputs',required=True);ap.add_argument('--scratch',required=True);ap.add_argument('--prepared-restart');ap.add_argument('--workers',type=int,default=3);main(ap.parse_args())
