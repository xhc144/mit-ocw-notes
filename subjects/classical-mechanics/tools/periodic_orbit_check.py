#!/usr/bin/env python3
"""Shooting for local periodic islands of the undamped driven pendulum."""
import json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root
from nonlinear_check import ROOT,write_csv
T=2*np.pi/.7

def flow(q,a,dense=False):
 def f(t,z):
  th,w=z[:2];M=z[2:].reshape(2,2);J=np.array([[0.,1.],[-np.cos(th),0.]])
  return np.r_[w,-np.sin(th)-a*np.cos(.7*t),(J@M).reshape(-1)]
 return solve_ivp(f,[0,T],np.r_[q,np.eye(2).reshape(-1)],rtol=1e-10,atol=1e-12,max_step=T/100,dense_output=dense)

def shoot(a,guess):
 def fj(q):
  sol=flow(q,a);z=sol.y[:,-1];return z[:2]-q,z[2:].reshape(2,2)-np.eye(2)
 sol=root(fj,guess,jac=True,tol=1e-10)
 if np.linalg.norm(fj(sol.x)[0])>1e-8:return None
 z=flow(sol.x,a).y[:,-1];M=z[2:].reshape(2,2)
 return {'a':a,'initial_state':sol.x.tolist(),'closure_error':float(np.linalg.norm(z[:2]-sol.x)),'monodromy_trace':float(np.trace(M)),'monodromy_determinant':float(np.linalg.det(M)),'elliptic':bool(abs(np.trace(M))<2),'initial_guess':list(guess)}


# Reproduction entry point: periodic_orbit_scan.py.
