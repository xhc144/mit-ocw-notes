#!/usr/bin/env python3
"""Check the Stokes radial equations and export actual sphere streamlines."""
from pathlib import Path
import json
import numpy as np
import sympy as sp
from scipy.optimize import brentq

SUBJECT = Path(__file__).resolve().parents[1]

def main():
    r, a = sp.symbols('r a', positive=True)
    C = sp.Rational(-3, 2)
    f = 1 + C*a/(2*r) + C*a**3/(6*r**3)
    k = C*a/(2*r**3)*(1-a**2/r**2)
    residuals = [sp.simplify(sp.diff(f,r)+r**2*sp.diff(k,r)+4*r*k),
                 sp.simplify(sp.diff(k,r,2)+6*sp.diff(k,r)/r+3*C*a/r**5),
                 sp.simplify(sp.diff(f,r,2)+2*sp.diff(f,r)/r+2*k-C*a/r**3)]
    assert residuals == [0,0,0]
    assert f.subs(r,a)==0 and k.subs(r,a)==0 and sp.limit(f,r,sp.oo)==1
    assert sp.limit(r**2*k,r,sp.oo)==0
    plots=[];checks=[]
    for model in ['ideal','stokes']:
        curves=[]
        for index,b in enumerate([.2,.5,1.,1.5]):
            target=b*b/2
            def psi(x,y):
                radius=np.hypot(x,y)
                factor=1-radius**-3 if model=='ideal' else 1-1.5/radius+.5/radius**3
                return .5*y*y*factor
            rows=[]
            for x in np.linspace(-4,4,161):
                lower=max(0.,np.sqrt(max(0.,1-x*x)))
                y=brentq(lambda y:psi(x,y)-target,lower+1e-12,b+3.,xtol=2e-13)
                assert np.hypot(x,y)>1
                rows.append([x,y])
            rows=np.asarray(rows);name=f'sphere-{model}-{index}.csv'
            np.savetxt(SUBJECT/'figures'/name,rows,delimiter=',',header='x,y',comments='',fmt='%.12g')
            error=max(abs(psi(x,y)-target) for x,y in rows)
            checks.append({'file':name,'upstream_streamline_label':b,'psi':target,'rows':len(rows),'maximum_contour_residual':float(error)})
            curves.append(r'\addplot[blue!65!black,no marks,thin] table[x=x,y=y,col sep=comma]{figures/'+name+'};')
            curves.append(r'\addplot[blue!65!black,no marks,thin] table[x=x,y expr=-\thisrow{y},col sep=comma]{figures/'+name+'};')
        title='理想位势流' if model=='ideal' else 'Stokes黏性流'
        axis=(r'\begin{tikzpicture}\begin{axis}[width=.46\textwidth,height=5cm,axis equal image,'
              r'xmin=-4,xmax=4,ymin=-2.6,ymax=2.6,xtick={-4,-2,0,2,4},ytick={-2,0,2},'
              r'xlabel={$z/a$},ylabel={$s/a$},title={'+title+r'},tick label style={font=\scriptsize},title style={font=\small}]')
        plots.append('\n'.join([axis,*curves,
          r'\addplot[black,fill=gray!20,domain=0:360,samples=73] ({cos(x)},{sin(x)});',
          r'\draw[->,thick] (axis cs:-3.7,2.0)--(axis cs:-2.7,2.0) node[midway,above] {$\vect u$};',
          r'\end{axis}\end{tikzpicture}']))
    (SUBJECT/'figures/sphere-flow-plots.tex').write_text('\\begin{center}\n'+ '\\hfill\n'.join(plots)+'\n\\end{center}\n')
    result={'stokes_radial_equation_residuals':list(map(str,residuals)),
            'boundary_conditions':'f(a)=k(a)=0; f(infinity)=1; r²k(infinity)=0 verified symbolically',
            'curves':checks,'model':'a=U=1; meridional half-plane contour roots, mirrored for display',
            'not_a_proof':'The plotted contour samples illustrate the analytic fields; drag is calculated from stress, not from the image.'}
    (SUBJECT/'qa/flow-extension-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'radial_residuals':result['stokes_radial_equation_residuals'],'streamline_files':len(checks),'max_contour_error':max(x['maximum_contour_residual'] for x in checks)}))

if __name__=='__main__': main()
