#!/usr/bin/env python3
"""Recompute 2005 PS8 cold-wave plots at their own density and field values."""
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'chapters/historical-2005-cold-curves.tex'
QE = 1.602176634e-19
EPS = 8.8541878128e-12
ME = 9.1093837139e-31
MI = 2 * 1.67262192595e-27
B = 5.0
OI = QE * B / MI
OE = -QE * B / ME


def divide(a, b):
    return a / b if b else math.nan


def values(omega, density):
    pe = density * QE * QE / (EPS * ME)
    pi = density * QE * QE / (EPS * MI)
    rd = omega * (omega + OE) * (omega + OI)
    ld = omega * (omega - OE) * (omega - OI)
    rn = rd - pe * (omega + OI) - pi * (omega + OE)
    ln = ld - pe * (omega - OI) - pi * (omega - OE)
    return {'R': divide(rn, rd), 'L': divide(ln, ld),
            'O': 1 - (pe + pi) / omega**2,
            'X': divide(2 * rn * ln, rn * ld + ln * rd)}


def main():
    lines = []
    qa = []
    styles = {'R': 'thick,structurecolor', 'L': 'thick,orange',
              'O': 'thick,dashed,gray', 'X': 'thick,dotted,blue'}
    for density, title in [(1e20, '1'), (4e20, '4')]:
        curves = {name: [] for name in styles}
        counts = {name: 0 for name in styles}
        for i in range(1201):
            x = -2 + 6 * i / 1200
            for name, val in values(OI * 10**x, density).items():
                y = math.log10(val) if val > 0 else math.nan
                if not math.isfinite(y) or not -2 <= y <= 3:
                    y = math.nan
                else:
                    counts[name] += 1
                curves[name].append((x, y))
        lines.append(r'\begin{center}\begin{tikzpicture}\begin{axis}['
                     r'width=.77\textwidth,height=4.8cm,'
                     r'xlabel={$\log_{10}(\omega/\Omega_{ci})$},'
                     r'ylabel={$\log_{10}n_{\rm ref}^2$},'
                     r'xmin=-2,xmax=4,ymin=-2,ymax=3,unbounded coords=jump,'
                     r'title={$n_e=' + title + r'\times10^{20}\,\mathrm m^{-3},\ B=5\,\mathrm T$},'
                     r'legend style={font=\small,at={(1.02,1)},anchor=north west}]')
        for name, points in curves.items():
            coords = ' '.join(f'({x:.5f},{y:.7f})' if math.isfinite(y)
                              else f'({x:.5f},nan)' for x, y in points)
            lines.append(r'\addplot[' + styles[name] + '] coordinates {' + coords +
                         r'};\addlegendentry{' + name + '}')
        lines.append(r'\end{axis}\end{tikzpicture}\end{center}')
        qa.append({'electron_density_m_inv3': density,
                   'field_T': B, 'sample_count_per_branch': 1201,
                   'visible_positive_samples': counts})
    OUT.write_text('\n'.join(lines) + '\n')
    (ROOT / 'qa/historical-2005-cold-sampling.json').write_text(
        json.dumps({'sets': qa, 'negative_or_pole': 'not plotted',
                    'analytical_boundary': 'R/L/P/S equations in manuscript'}, indent=2) + '\n')
    print(OUT)


if __name__ == '__main__':
    main()
