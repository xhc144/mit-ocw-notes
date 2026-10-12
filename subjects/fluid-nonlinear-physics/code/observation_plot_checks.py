"""Derive an informative delay display from existing actual PS6 observations.
No integration or previous accepted core computation is repeated.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[1]
def main():
    a=np.genfromtxt(ROOT/'data/ps6-rossler-time.csv',delimiter=',',names=True)
    dt=float(np.median(np.diff(a['t'])));tau=1.44;lag=round(tau/dt)
    assert np.max(abs(np.diff(a['t'])-dt))<1e-10 and abs(lag*dt-tau)<1e-9
    v=np.column_stack([a['x'][:-2*lag],a['x'][lag:-lag],a['x'][2*lag:]])
    np.savetxt(ROOT/'data/ps6-rossler-delay-tau144.csv',v,delimiter=',',header='x_now,x_delay,x_2delay',comments='')
    s=np.linalg.svd(v-v.mean(axis=0),compute_uv=False)
    # The previously saved mu20 table has dt=.1 and undersamples its fast jump.
    # Extend its actual final state by one period; retain adaptive solver nodes.
    vdp=np.genfromtxt(ROOT/'data/ps3-vdp-mu20-start0.csv',delimiter=',',names=True)
    initial=[float(vdp['x'][-1]),float(vdp['xdot'][-1])]
    sol=solve_ivp(lambda t,z:[z[1],20*(1-z[0]**2)*z[1]-z[0]],(0,40),initial,
                  method='Radau',rtol=1e-10,atol=1e-12,max_step=.04)
    assert sol.success and np.max(abs(sol.y[0]))>2
    np.savetxt(ROOT/'data/ps3-vdp-mu20-dense-phase.csv',np.c_[sol.t,sol.y.T],delimiter=',',header='t,x,xdot',comments='')
    report={'status':'PASS','data_source':'existing actual PS6 last60time observations, original provided initial condition',
            'no_integration_replay':True,'sample_dt':dt,'delay':lag*dt,'vectors':len(v),
            'singular_values':s.tolist(),'older_tau02_table_preserved':True,
            'purpose':'display a delay nearer quarter rotation period, not a proof of embedding or hidden equations',
            'vdp_visual_sampling_repair':{'reason':'saveddt.1 misses fast jump; one40time-unit extension from actual final state, not a full repeated scan',
            'initial':initial,'method':'Radau','rtol':1e-10,'atol':1e-12,'max_step':.04,'saved_nodes':len(sol.t)}}
    (ROOT/'qa/observation-plot-checks.json').write_text(json.dumps(report,indent=2));print('Actual-observation delay display PASS')
if __name__=='__main__':main()
