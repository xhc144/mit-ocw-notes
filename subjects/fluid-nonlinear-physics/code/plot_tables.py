"""Display-only subsampling; full numerical and observed tables are retained."""
from pathlib import Path
import re, json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def main():
    out=ROOT/'data/plots';out.mkdir(exist_ok=True);report=[]
    for p in sorted((ROOT/'chapters').glob('2[2-5]*.tex')):
        s=p.read_text()
        for f in sorted(set(re.findall(r'\{(data/(?:plots/)?[^}]+\.csv)\}',s))):
            original=ROOT/'data'/Path(f).name
            a=np.genfromtxt(original,delimiter=',',names=True);n=len(a)
            if n<450:continue
            if 'ps8-r166' in f and 'maxima' in f:
                # Event maxima are small enough to retain every return pair.
                b=a
            elif 'ps8-r166' in f and '-X.csv' in f:
                # Retain 0.04 trace spacing; coarse thinning hides fast peaks.
                b=a[::2]
            elif 'vdp-mu20' in f:
                # Uniform time thinning misses stiff fast jumps in phase space.
                # Sample by normalized trajectory arc length, retaining full input.
                xyz=np.column_stack([a[k] for k in a.dtype.names]);scale=np.ptp(xyz,axis=0)
                scale[scale==0]=1
                arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(xyz/scale,axis=0),axis=1))]
                ids=np.unique(np.searchsorted(arc,np.linspace(0,arc[-1],700)))
                b=a[ids]
            elif 'bifurcation' in f:
                mus=np.unique(a['mu']);chosen=mus[::8]
                band=(mus>=2.5)&(mus<=2.75) if 'ricker' in f else (mus>=.94)&(mus<=.975)
                chosen=np.unique(np.r_[chosen,mus[band]])
                # Keep all 32 tail values for each displayed parameter: taking
                # every fourth tail value would erase period-two/four branches.
                b=a[np.isin(a['mu'],chosen)]
            elif 'spectrum' in f or 'spectra' in f:
                b=a[np.unique(np.geomspace(1,n,450).astype(int)-1)]
            else:b=a[np.arange(0,n,max(1,n//450))]
            dst=out/original.name
            np.savetxt(dst,np.column_stack([b[k] for k in a.dtype.names]),delimiter=',',header=','.join(a.dtype.names),comments='')
            report.append({'input':original.relative_to(ROOT).as_posix(),'input_rows':n,'display':dst.relative_to(ROOT).as_posix(),'display_rows':len(b),'changes_to_full_input':False})
    (ROOT/'qa/display-tables.json').write_text(json.dumps(report,indent=2))
if __name__=='__main__':main()
