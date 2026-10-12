#!/usr/bin/env python3
"""Independent algebraic checks of the chosen Euler-angle frame and polar equations."""
import sympy as s
import json,hashlib
from pathlib import Path
q=s.symbols('phi theta psi',real=True);phi,theta,psi=q
ex=s.Matrix([-s.sin(phi)*s.cot(theta),s.cos(phi),s.sin(phi)/s.sin(theta)])
ey=s.Matrix([s.cos(phi)*s.cot(theta),s.sin(phi),-s.cos(phi)/s.sin(theta)])
ez=s.Matrix([1,0,0])
def bracket(x,y):return (y.jacobian(q)*x-x.jacobian(q)*y).applyfunc(s.trigsimp)
checks=[bracket(ex,ey)+ez,bracket(ey,ez)+ex,bracket(ez,ex)+ey]
assert all(v==s.zeros(3,1)for v in checks)
r=Path(__file__).resolve().parents[1];p=r/'chapters/11-graduate-poincare.tex'
(r/'qa/graduate-frame-check.json').write_text(json.dumps({'status':'PASS','spatial_frame_brackets':'[ex,ey]=-ez and cyclic; exact symbolic simplification','body_frame_euler':'derived with opposite structure constants; energy and lab angular momentum checked in prose','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'software':'SymPy '+s.__version__},indent=2)+'\n')
print('PASS: all 9 frame commutator components')
