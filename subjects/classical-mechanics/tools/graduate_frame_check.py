#!/usr/bin/env python3
"""Reproducible algebraic checks of the chosen Euler-angle frame and polar equations."""
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
# Non-coordinate polar frame [e_r,e_theta]=-e_theta/r and its equations.
t=s.symbols('t',real=True);mass=s.symbols('m',positive=True);rad=s.Function('r')(t);ang=s.Function('theta')(t)
wr=s.diff(rad,t);wt=rad*s.diff(ang,t)
# Poincare RHS_r=(omega_theta*pi_theta)/r, RHS_theta=-(omega_r*pi_theta)/r.
res_r=s.diff(mass*wr,t)-mass*wt**2/rad
res_theta=s.diff(mass*wt,t)+mass*wr*wt/rad
expected_r=mass*(s.diff(rad,t,2)-rad*s.diff(ang,t)**2)
expected_theta=mass*(rad*s.diff(ang,t,2)+2*s.diff(rad,t)*s.diff(ang,t))
assert s.simplify(res_r-expected_r)==0
assert s.simplify(res_theta-expected_theta)==0
r=Path(__file__).resolve().parents[1];p=r/'chapters/11-graduate-poincare.tex'
(r/'qa/graduate-frame-check.json').write_text(json.dumps({'status':'PASS','spatial_frame_brackets':'[ex,ey]=-ez and cyclic; exact symbolic simplification','polar_equations':{'radial_residual':str(s.simplify(res_r)),'angular_residual':str(s.simplify(res_theta)),'both_equal_coordinate_EL_exactly':True},'body_frame_euler':'derived with opposite structure constants; energy and lab angular momentum checked in prose','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'software':'SymPy '+s.__version__},indent=2)+'\n')
print('PASS: all9frame components and2polar EL equations')
