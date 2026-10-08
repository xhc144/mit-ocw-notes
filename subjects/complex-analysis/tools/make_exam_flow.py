#!/usr/bin/env python3
"""Regenerate Pex2.11 TikZ curves by normalized RK4 of conjugate(Phi').

This is a numerical illustration; the proof and singularity analysis are in TeX.
No screenshots or third-party image are used.
"""
import cmath
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = (-4.0, 4.0, -3.0, 3.0)
SOURCES = (1j, -1j)

def derivative(z):
    return (z + 1) ** 2 / (z * z + 1)

def velocity(z):
    v = derivative(z).conjugate()
    return v / abs(v) if abs(v) > 1e-12 else 0j

def trace(seed, direction=1):
    z = seed
    points = [z]
    h = 0.025 * direction
    for k in range(1600):
        if not (BOX[0] <= z.real <= BOX[1] and BOX[2] <= z.imag <= BOX[3]):
            break
        if min(abs(z - a) for a in SOURCES) < .075 or abs(z + 1) < .022:
            break
        k1 = velocity(z)
        k2 = velocity(z + h * k1 / 2)
        k3 = velocity(z + h * k2 / 2)
        k4 = velocity(z + h * k3)
        z = z + h * (k1 + 2*k2 + 2*k3 + k4) / 6
        if k % 4 == 0:
            points.append(z)
    return points

paths = []
for a in SOURCES:
    for k in range(12):
        paths.append(trace(a + .12 * cmath.exp(2j * cmath.pi * k / 12)))
for k in range(15):
    paths.append(trace(complex(-3.95, -2.8 + .4*k)))

lines = [r'\begin{center}\begin{tikzpicture}[xscale=1.35,yscale=1.25,>=Stealth]',
         r'\clip (-4.3,-3.3) rectangle (4.7,3.4);']
for points in paths:
    if len(points) < 3:
        continue
    coords = ' '.join(f'({z.real:.4f},{z.imag:.4f})' for z in points)
    lines.append(r'\draw[main!65,line width=.35pt] plot[smooth] coordinates {' + coords + '};')
lines += [r'\draw[->,gray](-4.1,0)--(4.45,0) node[right]{$x$};',
          r'\draw[->,gray](0,-3.1)--(0,3.15) node[above]{$y$};',
          r'\fill (0,1)circle(2pt) node[above right,fill=white,inner sep=1pt]{源 $\ii$};',
          r'\fill (0,-1)circle(2pt) node[below right,fill=white,inner sep=1pt]{源 $-\ii$};',
          r'\fill (-1,0)circle(2pt) node[below left,fill=white,inner sep=1pt]{$-1$};',
          ]
for start, length in [(3+2.6j,.55),(3-2.6j,.55),(.22+1j,.30),(.22-1j,.30)]:
    end = start + length*velocity(start)
    lines.append(f'\\draw[->,thick]({start.real:.4f},{start.imag:.4f})--({end.real:.4f},{end.imag:.4f});')
lines.append(r'\end{tikzpicture}\qedhere\end{center}')
(ROOT/'chapters/assessments/exam-flow.tex').write_text('\n'.join(lines)+'\n')
errors = []
for z in [complex(x,y) for x in (-3,-2,-.5,.5,2,3) for y in (-2,-.5,.5,2)]:
    errors.append(abs((derivative(z)*velocity(z)).imag))
(ROOT/'qa/assessment-review/exam-flow-numeric-check.json').write_text(json.dumps({
    'method':'normalized RK4, step=0.025; 39 streamlines; clipping avoids sources and double stagnation point',
    'flow_equation':'dz/dt = conjugate(Phi_prime(z))/abs(Phi_prime(z))',
    'sampled_streamfunction_direction_residual_max':max(errors),
    'numerical_plot_is_not_a_proof':True,
    'tikz_final_pdf_visual_review':'pending'},indent=2)+'\n')
print('Generated',len(paths),'curves; max direction residual',max(errors))
