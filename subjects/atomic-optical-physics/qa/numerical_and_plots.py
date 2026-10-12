"""Reproducible numerical checks and original vector figures; no source PDF backgrounds."""
from pathlib import Path
import math,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];F=ROOT/'figures';F.mkdir(exist_ok=True)
report={}
h=6.62607015e-34;hb=h/(2*math.pi);e=1.602176634e-19;ep=8.8541878128e-12;c=299792458;me=9.1093837139e-31;kB=1.380649e-23;a0=5.29177210903e-11;Eh=4.359744722206e-18
w0=2*math.pi*c/590e-9;d2=hb*e*e/(2*me*w0);Gam=w0**3*d2/(3*math.pi*ep*hb*c**3)
report['Na_effective_lifetime_s']=1/Gam;report['Na_Is_W_m2']=math.pi*h*c*Gam/(3*(590e-9)**3)
for label,wl in [('yellow',w0-2*math.pi*1.7e9),('IR',2*math.pi*c/985e-9)]:
 alpha=e*e/(me*(w0*w0-wl*wl));I=2*ep*c*kB*10e-6/alpha;P=I*math.pi*(6e-6)**2/2
 R=wl**3*alpha**2*(2*I/(ep*c))/(12*math.pi*ep*hb*c**3)
 report[label]={'power_W':P,'scatter_s-1':R}
W=3*Eh/(8*hb);alpha=e*e/(4*math.pi*ep*hb*c);rate=2*alpha**2*a0**4*W**5/(9*math.pi*c**4);report['single_2P_model_2S_lifetime_s']=1/rate
f=Eh/h/50**3;L=c/math.sqrt(2)/f;g=2500*e*a0*math.sqrt(hb*2*math.pi*f/(2*ep*(L**3/4)))/hb;report['rydberg']={'f_Hz':f,'cube_m':L,'vacuum_Rabi_Hz':g/math.pi}
report['quenching']={}
for label,om in [('unresolved',0),('Lamb',2*math.pi*1.06e9)]:
 V=math.sqrt(1e6*(om*om+(6.3e8/2)**2)/6.3e8);report['quenching'][label]=V*hb/(3*e*a0)/100
# Q plots are normalised Q=<z|rho|z> (the density with respect to dx dy is Q/pi).
def q_from_fock(z,coef):
 amp=np.zeros_like(z,dtype=complex);term=np.ones_like(z,dtype=complex)
 for n,cn in enumerate(coef):
  if n:term*=z.conj()/math.sqrt(n)
  amp+=cn*term
 return np.exp(-np.abs(z)**2)*np.abs(amp)**2
panels=[]
for theta,phi in [(math.pi/2,0),(math.pi/2,math.pi/4),(math.pi,0)]:
 coef=np.zeros(13,complex);coef[0]=math.cos(theta/2);coef[12]=np.exp(1j*phi)*math.sin(theta/2)
 panels.append((f'$\\theta={theta/math.pi:g}\\pi,\\ \\phi={phi/math.pi:g}\\pi$',lambda z,cc=coef:q_from_fock(z,cc),5,False))
def cat(z):return np.exp(-np.abs(z)**2-9)*np.abs(np.exp(3*z.conj())+np.exp(-3*z.conj()))**2/(2*(1+np.exp(-18)))
phase=np.zeros(11,complex);phase[1:]=np.exp(1j*np.arange(1,11)*math.pi/4)/math.sqrt(10)
panels+=[('even cat, $\\alpha=3$',cat,5,True),('phase sum, $N=10$',lambda z:q_from_fock(z,phase),5,False)]
for r in [.2,1.2,4]:panels.append((f'squeezed vacuum, $r={r}$',lambda z,r=r:np.exp(-np.abs(z)**2+math.tanh(r)*np.real(z.conj()**2))/math.cosh(r),max(4,math.exp(r)*1.2),False))
for t in [0,16,32,64,128]:
 n=np.arange(121);co=np.empty(121,complex);co[0]=math.exp(-8)
 for j in range(1,121):co[j]=co[j-1]*4/math.sqrt(j)
 co*=np.exp(1j*math.pi/128*n*(n-1)*t)
 panels.append((f'Kerr, $t={t}$',lambda z,cc=co:q_from_fock(z,cc),9,True))
for batch in range(4):
 group=panels[batch*4:batch*4+4]
 fig,ax=plt.subplots(1,1,figsize=(4,3.8),squeeze=False) if len(group)==1 else plt.subplots(2,2,figsize=(8,7),squeeze=False)
 for unused in ax.flat:unused.set_visible(False)
 for a,(title,fn,lim,log) in zip(ax.flat,group):
  a.set_visible(True)
  x=np.linspace(-lim,lim,220);xx,yy=np.meshgrid(x,x);val=fn(xx+1j*yy)
  if log:val=np.log10(np.maximum(val,1e-12));a.contourf(xx,yy,val,levels=np.linspace(-9,0,30),cmap='viridis')
  else:a.contourf(xx,yy,val,levels=24,cmap='viridis')
  a.set_aspect('equal');a.set_xlabel(r'$\Re z$');a.set_ylabel(r'$\Im z$');a.set_title(title,fontsize=10)
 fig.tight_layout();fig.savefig(F/f'quantum-states-{batch+1}.pdf');plt.close(fig)
# Fixed threshold rank is not a monotone.
rs=np.linspace(.001,6,1000);counts=[]
for r in rs:
 if 1/math.cosh(r)<=.01:counts.append(0)
 else:counts.append(math.ceil(math.log(.01*math.cosh(r))/math.log(math.tanh(r))))
fig,ax=plt.subplots(figsize=(6,3));ax.plot(rs,counts);ax.set(xlabel='r',ylabel=r'number of $\lambda_k>0.01$');fig.tight_layout();fig.savefig(F/'schmidt-threshold.pdf');plt.close(fig)
report['plot_cases']=len(panels);report['figure_origin']='original numerical contours, vector PDF';(ROOT/'qa/numerical-results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
