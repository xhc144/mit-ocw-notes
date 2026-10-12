"""Reproduce the independent numerical audit and vector review plots.
Run with NumPy, SciPy and Matplotlib available. Writes next to this script.
"""
import json
import numpy as np
from scipy.optimize import brentq
import midterm_reference as mid
import final_reference as fin

OUT=mid.OUT

def additional_checks():
    d=json.loads((OUT/'midterm_75.json').read_text());b=d['beta0']
    v=np.array([d[k] for k in ['l0','C0','sigma0','kappa0','delta0']])
    conv=[]
    for nr,nm in [(48,128),(72,192),(128,512),(192,1024)]:
        vv=mid.solve(b,v,weights='cos',lam=.2,nr=nr,nm=nm)
        p,*_=mid.performance(b,vv,lam=.2,nr=nr,nm=nm)
        conv.append(dict(nr=nr,nm=nm,parameter_change_max=float(max(abs(vv-v))),beta=p['beta'],fB=p['fB'],qmin=p['qmin'],rho_qmin=p['rho_qmin']))
    r,mu,w=mid.mesh(100,256);l,C,sig,kap,d0=v
    def quantities(z,t):
        sh=mid.shape(z,t,sig,kap,d0);ss=1+mid.EPS*sh[0];gp=mid.flux(z,.2)[1]
        return gp*sh[7]/(sh[6]*ss),-gp*sh[8]/(sh[6]*ss),sh,ss
    P,Q,sh,s=quantities(r,mu);hh=1e-6
    Lp=s/sh[6]*((quantities(r+hh,mu)[0]-quantities(r-hh,mu)[0])/(2*hh)+(quantities(r,mu+hh)[1]-quantities(r,mu-hh)[1])/(2*hh))
    p,gp=mid.flux(r,.2);h,hp,f,fp=mid.profile(p)
    src=2*b/l**2*(s*s-1)*hp+2*C*fp
    rel=np.sqrt(np.sum(w*sh[6]*(Lp+src)**2)/np.sum(w*sh[6]*src**2))
    psib=d['I_MA']*1e6*mid.MU0*mid.R0*l/(4*np.pi)
    integ=-psib/(mid.MU0*mid.R0)*np.sum(w*sh[6]*src/s)
    report=dict(midterm_convergence=conv,relative_area_weighted_strong_GS_RMS=float(rel),source_current_MA=float(integ/1e6),Ampere_current_MA=d['I_MA'])
    assert abs(integ/1e6-d['I_MA'])<1e-8
    rows=[]
    for z,a in [(1.1,.6),(1.25,.5),(1.4,.3),(1.05,fin.alpha_sep(1.05)*.98)]:
        r=[]
        for nth in [128,256,512,1024]:
            e,_=fin.eq(z,a,nth);r.append(dict(nth=nth,area_hat=e['area_hat'],qa=e['qa'],beta_over_epsilon=e['beta_over_epsilon'],minimum=fin.min_eigen(e)[0]))
        rows.append(dict(zeta1=z,alpha=a,convergence=r))
    report['final_quadrature_convergence']=rows
    report['final_fast_matrix_checks_count']=45
    report['final_fast_matrix_max_error']=float(max(np.max(np.abs(fin.fast_fluid(m,n,q)-fin.fluid_matrix(m,n,q,96,128))) for m in range(2,17) for n,q in [(.2,1.1),(.7,1.4),(.95,1.7)]))
    assert report['final_fast_matrix_max_error']<1e-10
    (OUT/'verification.json').write_text(json.dumps(report,indent=2))

def final_scan():
    rows=[];roots=[];jumps=[];unresolved=[];best=None
    for z in np.linspace(1.00001,fin.zcrit()-1e-5,101):
        prev=None
        for tf in np.linspace(.002,.99999,151):
            al=fin.alpha_sep(z)*tf;e,_=fin.eq(z,al,nth=256);lam,m=fin.min_eigen(e)
            rows.append([z,al,e['inv_qstar'],e['beta_over_epsilon'],lam,m,e['qcore'],e['qa']])
            if lam>=0 and (best is None or e['beta_over_epsilon']>best['beta_over_epsilon']):best=e|dict(lowest_eigenvalue=lam,worst_m=m)
            if prev and prev[1]*lam<0:
                for nq in [256,512,1024,2048,4096]:
                    aa=brentq(lambda a:fin.min_eigen(fin.eq(z,a,nth=nq)[0])[0],prev[0],al,xtol=2e-13)
                    er,_=fin.eq(z,aa,nth=nq*2);lr,mr=fin.min_eigen(er)
                    row=[z,aa,er['inv_qstar'],er['beta_over_epsilon'],lr,mr,er['qcore'],er['qa']]
                    distance=min(np.min(abs(er['qcore']-np.arange(1,11))),np.min(abs(er['qa']-np.arange(1,11))))
                    if abs(lr)<1e-7:roots.append(row);break
                    if distance<1e-6:jumps.append(row);break
                else:unresolved.append(row)
            prev=(al,lam)
    header='zeta1,alpha,invqstar,beta_over_epsilon,lambda_min,worst_m,qcore,qa'
    for name,data in [('final_scan',rows),('final_marginal',roots),('final_branch_jumps',jumps),('final_unresolved',unresolved)]:
        np.savetxt(OUT/(name+'.csv'),data,delimiter=',',header=header,comments='')
    (OUT/'final_grid_best.json').write_text(json.dumps(best,indent=2))
    nuc=brentq(lambda n:fin.qprime_of(n)/np.sqrt(1-n*n)-3,.7,.95);seq=[]
    for gap in [.1,.03,.01,.003,.001,.0003,.0001,.00003,.00001]:
        alpha=1-gap;nu=nuc-.2*gap
        z=brentq(lambda z:fin.nu_of(z,alpha)-nu,1+1e-14,2-alpha-1e-14,xtol=1e-14)
        e,_=fin.eq(z,alpha,512);lm,m=fin.min_eigen(e,range(2,17))
        seq.append(e|dict(lowest_eigenvalue=lm,worst_m=m))
    (OUT/'final_thin_shell_sequence.json').write_text(json.dumps(seq,indent=2))

def plots():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    def save(fig,name):
        fig.tight_layout();fig.savefig(OUT/(name+'.pdf'));fig.savefig(OUT/(name+'.png'),dpi=150);plt.close(fig)
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    d=json.loads((OUT/'midterm_75.json').read_text())
    surf=np.genfromtxt(OUT/'midterm_flux_surfaces.csv',delimiter=',',skip_header=1)
    fig,ax=plt.subplots(figsize=(4.5,6))
    for rr in np.unique(surf[:,0]):
        pts=surf[surf[:,0]==rr];ax.plot(pts[:,1],pts[:,2],lw=1)
    ax.plot(d['sigma0'],0,'ko',ms=4);ax.set(xlabel=r'$x=(R-R_0)/a$',ylabel=r'$y=Z/a$',title=r'Midterm: $f_B=0.75$, $\lambda=0.2$');ax.set_aspect('equal');save(fig,'midterm_flux')
    data=json.loads((OUT/'midterm_scan.json').read_text())
    fig,ax=plt.subplots(figsize=(6,4));ax.plot([v['beta']*100 for v in data],[v['fB'] for v in data]);ax.axhline(.75,color='.5',ls='--');ax.plot(d['beta']*100,.75,'o');ax.set(xlabel=r'$\beta$ (%)',ylabel=r'$f_B$',title='Midterm: independently solved moment model');save(fig,'midterm_bootstrap')
    pro=np.genfromtxt(OUT/'midterm_q_bootstrap.csv',delimiter=',',skip_header=1)
    cur=np.genfromtxt(OUT/'midterm_currents.csv',delimiter=',',skip_header=1)
    fig,axes=plt.subplots(2,1,figsize=(6,7));axes[0].plot(pro[:,0],pro[:,1]);axes[0].plot(d['rho_qmin'],2,'o');axes[0].set(xlabel=r'$\rho$',ylabel=r'$q$',ylim=(1.8,None));axes[1].plot(cur[:,0],cur[:,2]/1e6,label=r'$J_B$');axes[1].plot(cur[:,0],cur[:,3]/1e6,label=r'$J_{tot}=-\langle J_\varphi\rangle$');axes[1].set(xlabel=r'$\rho$',ylabel=r'$J$ (MA/m$^2$)');axes[1].legend();save(fig,'midterm_profiles')
    scan=np.genfromtxt(OUT/'final_scan.csv',delimiter=',',skip_header=1)
    roots=np.genfromtxt(OUT/'final_marginal.csv',delimiter=',',skip_header=1)
    jumps=np.genfromtxt(OUT/'final_branch_jumps.csv',delimiter=',',skip_header=1)
    fig,ax=plt.subplots(figsize=(7,5))
    for sign,color,label in [(True,'#247b91','sampled stable'),(False,'#d69778','sampled unstable')]:
        use=(scan[:,4]>=0)==sign;ax.scatter(scan[use,2],scan[use,3],s=3,c=color,label=label,rasterized=False)
    ax.scatter(roots[:,2],roots[:,3],s=10,c='k',label='zero eigenvalue')
    ax.scatter(jumps[:,2],jumps[:,3],s=9,facecolors='none',edgecolors='#ab1616',label='wall branch switch')
    nu=np.linspace(0,1,501);qp=fin.qprime_of(nu);ax.plot(1/qp,nu/qp**2,'k',lw=1.5,label='core = outer boundary')
    env=[]
    for z in np.linspace(1.00001,fin.zcrit()-1e-5,201):
        e,_=fin.eq(z,fin.alpha_sep(z),1024);env.append([e['inv_qstar'],e['beta_over_epsilon']])
    env=np.array(env);np.savetxt(OUT/'final_equilibrium_envelope.csv',env,delimiter=',',header='invqstar,beta_over_epsilon',comments='')
    ax.plot(env[:,0],env[:,1],'k--',lw=1.5,label='separatrix boundary')
    xx=np.linspace(0,1,100);ax.plot(xx,.14*xx,':',color='.3',label='Troyon (circular)')
    ax.set(xlabel=r'$1/q^*$',ylabel=r'$\beta_t/\epsilon$',xlim=(0,1),ylim=(0,.37));ax.legend(fontsize=10,loc='upper left');save(fig,'final_stability_space')
    e,(theta,rb)=fin.eq(1.1,.6,1024);nu=e['nuprime']
    x=np.linspace(-2.1,2.1,500);y=np.linspace(-2.1,2.1,500);X,Y=np.meshgrid(x,y);r2=X*X+Y*Y
    chi=np.where(r2<=1,.5*(r2-1)*(1+nu*X),np.log(np.sqrt(np.maximum(r2,1e-12)))+nu/2*(1-1/np.maximum(r2,1e-12))*X)
    fig,ax=plt.subplots(figsize=(6,6));ax.contour(X,Y,chi,levels=np.linspace(np.min(chi),e['chi_edge'],14)[1:],linewidths=.8)
    tt=np.linspace(0,2*np.pi,721);ax.plot(np.cos(tt),np.sin(tt),'k--',label='core');ax.plot(rb*np.cos(theta),rb*np.sin(theta),'k',lw=1.5,label='outer plasma');ax.set_aspect('equal');ax.set(xlabel=r'$x/a^{\prime}$',ylabel=r'$y/a^{\prime}$',title=r'Final equilibrium: $\zeta_1=1.1$, $\alpha=0.6$');ax.legend();save(fig,'final_flux')

if __name__=='__main__':
    mid.main();fin.main();additional_checks();final_scan();plots()
