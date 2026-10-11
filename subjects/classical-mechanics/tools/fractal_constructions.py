#!/usr/bin/env python3
"""Export finite Cantor/Koch constructions; geometric iteration is deterministic."""
from pathlib import Path
import cmath
import json

ROOT=Path(__file__).resolve().parents[1]

def main():
    lines=[r'\begin{center}',r'\begin{tikzpicture}[x=7cm,y=.48cm]']
    intervals=[(0.,1.)];checks=[]
    for level in range(4):
        lines.append(r'\node[anchor=east,font=\small] at (-.04,'+str(-level)+r') {$n='+str(level)+r'$};')
        for left,right in intervals:
            lines.append(r'\draw[blue!65!black,line width=2pt] ('+f'{left:.10f},{-level})--({right:.10f},{-level});')
        checks.append({'construction':'cantor','level':level,'segments':len(intervals),'total_length':sum(b-a for a,b in intervals)})
        intervals=[part for a,b in intervals for part in [(a,a+(b-a)/3),(b-(b-a)/3,b)]]
    lines.extend([r'\node[font=\small] at (.5,.8) {Cantor构造};',r'\end{tikzpicture}',r'\hfill',r'\begin{tikzpicture}[x=7cm,y=7cm]'])
    points=[0j,1+0j]
    for level in range(4):
        offset=-.30*level
        coords='--'.join(f'({p.real:.10f},{p.imag+offset:.10f})' for p in points)
        lines.append(r'\draw[blue!65!black,thin] '+coords+';')
        lines.append(r'\node[anchor=east,font=\small] at (-.04,'+f'{offset:.10f}'+r') {$n='+str(level)+r'$};')
        length=sum(abs(b-a) for a,b in zip(points[:-1],points[1:]))
        assert abs(length-(4/3)**level)<1e-12
        checks.append({'construction':'koch','level':level,'segments':len(points)-1,'total_length':length})
        updated=[]
        for a,b in zip(points[:-1],points[1:]):
            delta=(b-a)/3
            updated.extend([a,a+delta,a+delta+delta*cmath.exp(1j*cmath.pi/3),a+2*delta])
        points=updated+[points[-1]]
    lines.extend([r'\node[font=\small] at (.5,.23) {Koch曲线构造};',r'\end{tikzpicture}',r'\end{center}'])
    # Side-by-side width would exceed the text width, so the two plots form rows.
    lines=[r'\par\smallskip' if x==r'\hfill' else x for x in lines]
    (ROOT/'figures/fractal-constructions.tex').write_text('\n'.join(lines)+'\n')
    (ROOT/'qa/fractal-construction-check.json').write_text(json.dumps({'finite_levels':checks,'scope':'Exact deterministic finite iterates; no dynamics or dimension proof from sampling.'},ensure_ascii=False,indent=2)+'\n')
    print('Finite constructions verified: Cantor and Koch levels 0–3')

if __name__=='__main__':main()
