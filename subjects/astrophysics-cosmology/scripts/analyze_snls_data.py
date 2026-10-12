"""Actual PS5 SNLS/SiFTO fit with frozen-weight iteration and curved distances.

Input is the unchanged official OCW TAR; originals are not bundled.
Requires numpy, scipy, matplotlib (only to extract computed contour curves).
"""
import argparse,hashlib,io,json,os,tarfile
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/mit-snls-mpl')
import numpy as np
from scipy.optimize import minimize_scalar
from numpy.polynomial.legendre import leggauss

C=299792.458;H0=71.
GX,GW=leggauss(48)
def luminosity_distance(z,m,l,order=48):
    z=np.asarray(z,float)
    gx,gw=(GX,GW) if order==48 else leggauss(order)
    zp=.5*z[:,None]*(gx+1);ok=1-m-l
    e2=m*(1+zp)**3+ok*(1+zp)**2+l
    if np.any(e2<=0):return np.full(z.shape,np.nan)
    chi=.5*z*np.sum(gw/np.sqrt(e2),axis=1)
    if abs(ok)<1e-9:transverse=chi
    elif ok>0:transverse=np.sinh(np.sqrt(ok)*chi)/np.sqrt(ok)
    else:transverse=np.sin(np.sqrt(-ok)*chi)/np.sqrt(-ok)
    d=(C/H0)*(1+z)*transverse
    return np.where(d>0,d,np.nan)

def mu(z,m,l):return 25+5*np.log10(luminosity_distance(z,m,l))
def read_table(archive):
    with tarfile.open(archive) as tar:
        raw=tar.extractfile('./table11.dat').read();readme=tar.extractfile('./ReadMe').read()
    ranges=[(7,14),(114,124),(125,135),(136,146),(147,157),(158,168),(169,179),(180,190),(191,201),(202,212)]
    rows=[];omitted=[]
    for line in raw.decode().splitlines():
        name=line[:6]
        try:values=[float(line[a:b]) for a,b in ranges]
        except ValueError:omitted.append({'name':name,'reason':'missing numeric SiFTO column'});continue
        if values[0]<=0 or any(v<=0 for v in [values[2],values[4],values[6]]):
            omitted.append({'name':name,'reason':'nonpositive redshift or reported statistical error'});continue
        rows.append((name,values))
    return np.asarray([r[1] for r in rows]),[r[0] for r in rows],omitted,raw,readme

def fit_flat(a,variance_intrinsic):
    z,mb,emb,s,es,col,ec,cms,cmc,csc=a.T
    design=np.column_stack([s,-col,-np.ones(len(z))])
    def var(alpha,beta):return emb**2+alpha**2*es**2+beta**2*ec**2+2*alpha*cms-2*beta*cmc-2*alpha*beta*csc
    pars=np.array([1.,1.,-20.,.3]);history=[]
    for iteration in range(250):
        v=var(pars[0],pars[1]);assert np.all(v>0)
        weight=1/np.sqrt(v+variance_intrinsic)
        def solve(m):
            target=mu(z,m,1-m)-mb
            p=np.linalg.lstsq(design*weight[:,None],target*weight,rcond=None)[0]
            residual=(design@p-target)*weight
            return float(residual@residual),p
        op=minimize_scalar(lambda m:solve(m)[0],bounds=(.001,1.4),method='bounded',options={'xatol':1e-11})
        chi,p=solve(op.x);new=np.array([*p,op.x]);change=float(np.max(np.abs(new-pars)))
        history.append([iteration+1,*new,chi,change]);pars=new
        if change<2e-8:break
    else:raise RuntimeError('Frozen-weight iteration did not converge')
    v=var(pars[0],pars[1]);mi=mb-pars[2]+pars[0]*s-pars[1]*col
    chi=float(np.sum((mi-mu(z,pars[3],1-pars[3]))**2/(v+variance_intrinsic)))
    return {'alpha':float(pars[0]),'beta':float(pars[1]),'M_course_convention':float(pars[2]),
      'Omega_m_flat':float(pars[3]),'Omega_lambda_flat':float(1-pars[3]),'chi_square':chi,
      'degrees_of_freedom':len(z)-4,'iterations':len(history),'intrinsic_variance_mag2':variance_intrinsic},mi,v,np.asarray(history)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('archive',type=Path);ap.add_argument('--out',type=Path,default=Path('qa'))
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    digest=hashlib.sha256(args.archive.read_bytes()).hexdigest();assert digest=='9221f60b4bc5cad1d6ce2259aed121e578a78d90b1d559de2820bab94719f860'
    a,names,omit,raw,readme=read_table(args.archive);z=a[:,0]
    result,mi,var,history=fit_flat(a,.10)
    comparison,_,_,_=fit_flat(a,.01)
    np.savetxt(args.out/'snls-fit-iterations.csv',history,delimiter=',',header='iteration,alpha,beta,M,Omega_m,chi_square,max_parameter_change',comments='')
    np.savetxt(args.out/'snls-hubble-measurements.csv',np.column_stack([z,mi,np.sqrt(var),np.sqrt(var+.1)]),delimiter=',',header='z,mu,err_mu,err_total',comments='')
    zz=np.linspace(.005,1.12,240);m=result['Omega_m_flat']
    np.savetxt(args.out/'snls-hubble-models.csv',np.column_stack([zz,mu(zz,m,1-m),mu(zz,m-.2,1-m+.2),mu(zz,m+.2,1-m-.2)]),delimiter=',',header='z,best_mu,Omega_m_minus_0p2_mu,Omega_m_plus_0p2_mu',comments='')
    # PS5.2(A): every specified model, both the z<=1 and z<=5 plot from same data.
    z5=np.linspace(.005,5,400);cosmos=[(1,0),(0,1),(.3,.7),(1.2,0),(.3,0)]
    curves=np.column_stack([z5]+[luminosity_distance(z5,*p) for p in cosmos])
    np.savetxt(args.out/'ps5-distance-models.csv',curves,delimiter=',',header='z,matter_flat,Lambda_flat,model_0p3_0p7,matter_closed,matter_open',comments='')
    exact_errors=[]
    for pars in cosmos:
        d=luminosity_distance(z5,*pars);other=luminosity_distance(z5,*pars,order=96)
        err=float(np.max(np.abs(d-other)/other));assert err<1e-8;exact_errors.append({'parameters':pars,'max_relative_48_vs_96_point_error':err})
    dEdS=2*C/H0*(1+z5)*(1-(1+z5)**-.5)
    assert np.max(np.abs(curves[:,1]-dEdS)/dEdS)<1e-10
    assert np.max(np.abs(curves[:,2]-(C/H0)*(1+z5)*z5)/curves[:,2])<1e-10
    # Grid holds the converged nuisance parameters and their errors fixed.
    ms=np.linspace(0,2.2,221);ls=np.linspace(-.6,2.6,257)
    grid=np.full((len(ls),len(ms)),np.nan);weights=1/(var+.1)
    for iy,l in enumerate(ls):
        for ix,om in enumerate(ms):
            prediction=mu(z,om,l)
            if np.all(np.isfinite(prediction)):grid[iy,ix]=np.sum((mi-prediction)**2*weights)
    iy,ix=np.unravel_index(np.nanargmin(grid),grid.shape);minimum=float(grid[iy,ix])
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots();cs=ax.contour(ms,ls,grid-minimum,levels=[2.3,6.2,11.8]);segments=[]
    for level,curves_level in zip(cs.levels,cs.allsegs):
        rows=[]
        for curve in curves_level:
            if len(curve)>1:
                if rows:rows.append([np.nan,np.nan])
                rows.extend(curve.tolist())
        name='snls-contour-'+str(level).replace('.','p')+'.csv'
        np.savetxt(args.out/name,rows,delimiter=',',header='Omega_m,Omega_lambda',comments='')
        segments.append({'delta_chi_square':float(level),'file':name,'segments':len(curves_level),
                         'touches_grid_edge':any(np.any(np.isclose(c[:,0],ms[0])|np.isclose(c[:,0],ms[-1])|np.isclose(c[:,1],ls[0])|np.isclose(c[:,1],ls[-1])) for c in curves_level if len(c)>0)})
    plt.close(fig)
    record={'archive_sha256':digest,'table11_sha256':hashlib.sha256(raw).hexdigest(),
      'table_readme_sha256':hashlib.sha256(readme).hexdigest(),'valid_SiFTO_rows':len(a),'omitted_rows':omit,
      'primary_fit':result,'alternative_interpretation_sigma_intrinsic_0p10_mag':comparison,
      'primary_intrinsic_interpretation':'Literal original sigma_int^2=0.10 used as variance in mag^2. Alternative sigma_int=0.10, variance=0.01 reported separately.',
      'curved_grid':{'Omega_m_limits':[float(ms[0]),float(ms[-1])],'Omega_lambda_limits':[float(ls[0]),float(ls[-1])],
        'shape':list(grid.shape),'minimum_Omega_m':float(ms[ix]),'minimum_Omega_lambda':float(ls[iy]),'minimum_chi_square':minimum,'contours':segments,
        'nuisance_parameters':'fixed to primary flat fit, as original exercise directs; errors also fixed'},
      'checks':{'distance_quadrature':exact_errors,'EdS_and_pure_Lambda_analytic_distance_checks':True},
      'scope':'Actual public Table11 SiFTO analysis; all numeric valid rows with positive reported errors; no undocumented outlier rejection or published-author fit claim. H0=71; original heliocentric redshifts, no peculiar-velocity, host-mass, selection or correlated systematic covariance corrections; frozen-weight exercise chi-square is not a full likelihood.'}
    (args.out/'snls-results.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(record,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
