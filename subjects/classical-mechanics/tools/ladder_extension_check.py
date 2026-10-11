#!/usr/bin/env python3
"""Reproduce the uniform-ladder wall-release event and floor-only phase."""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[1]

def simulate(rtol,max_step):
    theta0=np.pi/3;ell=.5;g=1.;mass=1.
    def both(t,z):return [z[1],-1.5*g*np.cos(z[0])]
    def release(t,z):return np.sin(z[0])-2*np.sin(theta0)/3
    release.terminal=True;release.direction=-1
    first=solve_ivp(both,[0,10],[theta0,0],events=release,dense_output=True,rtol=rtol,atol=rtol/100,max_step=max_step)
    assert len(first.t_events[0])==1
    tr=first.t_events[0][0];theta,omega=first.y_events[0][0]
    x0=ell*np.cos(theta);vx=-ell*np.sin(theta)*omega
    def floor(t,z):
        q,w=z;den=np.cos(q)**2+1/3
        return [w,(np.sin(q)*np.cos(q)*w*w-(g/ell)*np.cos(q))/den]
    def reaches_floor(t,z):return z[0]
    reaches_floor.terminal=True;reaches_floor.direction=-1
    second=solve_ivp(floor,[tr,tr+10],[theta,omega],events=reaches_floor,dense_output=True,rtol=rtol,atol=rtol/100,max_step=max_step)
    assert len(second.t_events[0])==1
    tf=second.t_events[0][0];rows=[];drifts=[];gaps=[];normals=[]
    for phase,ts,solution in [(0,np.linspace(0,tr,201),first),(1,np.linspace(tr,tf,201),second)]:
        values=solution.sol(ts)
        for t,q,w in zip(ts,*values):
            if phase==0:
                x=ell*np.cos(q);xdot=-ell*np.sin(q)*w;acc=both(t,[q,w])[1]
                kinetic=mass*(2*ell)**2*w*w/6
            else:
                x=x0+vx*(t-tr);xdot=vx;acc=floor(t,[q,w])[1]
                kinetic=mass/2*(vx*vx+ell*ell*np.cos(q)**2*w*w)+mass*ell*ell*w*w/6
            energy=kinetic+mass*g*ell*np.sin(q)
            normal=mass*(g+ell*(-np.sin(q)*w*w+np.cos(q)*acc))
            gap=x-ell*np.cos(q)
            rows.append([t,q,w,x,2*ell*np.sin(q),gap,normal,phase])
            drifts.append(abs(energy-mass*g*ell*np.sin(theta0)))
            if phase: gaps.append(gap);normals.append(normal)
    return np.asarray(rows),{'length':1.,'mass':1.,'gravity':1.,'initial_angle':float(theta0),'initial_angular_velocity':0.,
        'release_time':float(tr),'release_angle':float(theta),'release_angular_velocity':float(omega),
        'floor_contact_time':float(tf),'minimum_postrelease_gap':float(min(gaps)),
        'minimum_floor_normal_force':float(min(normals)),'maximum_energy_error':float(max(drifts)),
        'rtol':rtol,'atol':rtol/100,'maximum_step':max_step}

def main():
    rows,report=simulate(2e-11,.005);_,fine=simulate(2e-12,.0025)
    report['refinement_difference']={k:abs(report[k]-fine[k]) for k in ['release_time','release_angle','floor_contact_time']}
    assert report['maximum_energy_error']<1e-8 and report['minimum_postrelease_gap']>-1e-8
    assert report['minimum_floor_normal_force']>0
    np.savetxt(ROOT/'figures/ladder-release.csv',rows,delimiter=',',header='t,theta,omega,x,top_height,wall_gap,floor_normal,phase',comments='',fmt='%.12g')
    text=(r'\begin{center}\begin{tikzpicture}\begin{axis}[width=.77\textwidth,height=4.8cm,xlabel={无量纲时间},ylabel={角度或高度},'
      r'xmin=0,ymin=0,legend pos=north east,legend style={font=\small},tick label style={font=\small}]'+'\n'+
      r'\addplot[blue,thick,no marks] table[x=t,y=theta,col sep=comma]{figures/ladder-release.csv};\addlegendentry{$\theta$}'+'\n'+
      r'\addplot[red!70!black,thick,no marks] table[x=t,y=top_height,col sep=comma]{figures/ladder-release.csv};\addlegendentry{梯顶高度}'+'\n'+
      r'\draw[dashed] (axis cs:'+f'{report["release_time"]:.10f},0'+r')--(axis cs:'+f'{report["release_time"]:.10f},.95'+r') node[above,font=\small]{离墙};'+'\n'+
      r'\end{axis}\end{tikzpicture}\end{center}'+'\n')
    (ROOT/'figures/ladder-release-plot.tex').write_text(text)
    report['scope']='Actual two-phase integration until theta=0; no impact or postimpact motion simulated. Dimensions fixed at L=M=g=1.'
    (ROOT/'qa/ladder-extension-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
