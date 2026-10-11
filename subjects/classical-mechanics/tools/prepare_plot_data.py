#!/usr/bin/env python3
"""Extract deterministic actual-data subsets for memory-bounded vector plots.
Full computed CSVs are retained. Every original parameter grid point is retained;
only the number of late-time samples per parameter is reduced for printing.
"""
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
for name,nparams,keep in [('rlc-bifurcation',301,8),('pendulum-wide-bifurcation',301,8),('pendulum-small-bifurcation',301,8),('logistic-bifurcation',501,8),('cosine-map',501,6),('cubic-map',501,6),('exponential-map',501,2)]:
 p=ROOT/'figures'/f'{name}.csv';header=p.read_text().splitlines()[0];data=np.loadtxt(p,delimiter=',',skiprows=1)
 ns=len(data)//nparams
 inds=np.unique(np.linspace(0,ns-1,keep).round().astype(int))
 out=data.reshape(ns,nparams,2)[inds].reshape(-1,2)
 np.savetxt(p.with_name(name+'-plot.csv'),out,delimiter=',',header=header,comments='',fmt='%.10g')

# Logarithmic plots require positive data; zero/floor points cannot be placed.
data=np.loadtxt(ROOT/"figures/map-sensitivity.csv",delimiter=",",skiprows=1)
for label,r in [("periodic",3.2),("chaotic",4.)]:
 selected=data[np.isclose(data[:,0],r)&(data[:,2]>=1e-17)]
 np.savetxt(ROOT/"figures"/f"map-sensitivity-{label}.csv",selected,delimiter=",",header="r,n,delta",comments="",fmt="%.10g")
import json
q0=json.loads((ROOT/"qa/periodic-orbit-check.json").read_text())["selected"]["initial_state"][0]
data=np.loadtxt(ROOT/"figures/pendulum-periodic-island.csv",delimiter=",",skiprows=1)
data[:,0]-=q0
np.savetxt(ROOT/"figures/pendulum-periodic-island-offset.csv",data,delimiter=",",header="theta_offset,w",comments="",fmt="%.10g")
