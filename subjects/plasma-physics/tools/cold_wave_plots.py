#!/usr/bin/env python3
"""Sample signed cold-plasma branches; never plot abs(n^2) or join poles."""
from pathlib import Path
import math,json,argparse
ROOT=Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=ROOT/'chapters/cold-curves.tex');a=ap.parse_args()
 q=1.602176634e-19;eps=8.8541878128e-12;me=9.1093837015e-31;mi=2*1.67262192369e-27;B=5.5;oi=q*B/mi;oe=-q*B/me
 lines=[];counts=[]
 for ne in [2e20,5e20]:
  pe=ne*q*q/(eps*me);pi=ne*q*q/(eps*mi);curves={k:[] for k in ['R','L','O','X']};positive={k:0 for k in curves}
  for i in range(2401):
   x=-2+6*i/2400;w=oi*10**x
   # Rational products give the finite X limit at bare cyclotron poles.
   rd=w*(w+oe)*(w+oi);ld=w*(w-oe)*(w-oi)
   rn=rd-pe*(w+oi)-pi*(w+oe);ln=ld-pe*(w-oi)-pi*(w-oe)
   div=lambda a,b:a/b if b else float('nan')
   vals=dict(R=div(rn,rd),L=div(ln,ld),O=1-(pe+pi)/w**2,X=div(2*rn*ln,rn*ld+ln*rd))
   for k,v in vals.items():
    y=math.log10(v) if v>0 else float('nan')
    if not math.isfinite(y) or not -2<=y<=3:y=float('nan')
    if math.isfinite(y):positive[k]+=1
    curves[k].append((x,y))
  lines.append(r'\begin{center}\begin{tikzpicture}\begin{axis}[width=.82\textwidth,height=5cm,xlabel={$\log_{10}(\omega/\Omega_{ci})$},ylabel={$\log_{10}n_{\rm ref}^2$},xmin=-2,xmax=4,ymin=-2,ymax=3,unbounded coords=jump,title={$n_e='+('2'if ne==2e20 else'5')+r'\times10^{20}\,\mathrm m^{-3}$},legend style={font=\small,at={(1.02,1)},anchor=north west}]')
  styles={'R':'thick,structurecolor','L':'thick,orange','O':'thick,dashed,gray','X':'thick,dotted,blue'}
  for k,pts in curves.items():
   lines.append(r'\addplot['+styles[k]+'] coordinates {'+' '.join(f'({x:.5f},{y:.7f})'if math.isfinite(y) else f'({x:.5f},nan)'for x,y in pts)+'};'+r'\addlegendentry{'+k+'}')
  lines.append(r'\end{axis}\end{tikzpicture}\end{center}');counts.append({'density_m_inv3':ne,'samples':2401,'visible_positive_samples':positive})
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text('\n'.join(lines)+'\n');print(a.out)
 (ROOT/'qa/cold-wave-sampling.json').write_text(json.dumps({'field_T':B,'ion':'D, mass 2mp','branches':counts,'negative_values':'excluded; no absolute value used','cutoffs_and_resonances':'analytical definitions in manuscript; finite sample is visualization only'},indent=2)+'\n')
if __name__=='__main__':main()
