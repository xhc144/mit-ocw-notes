#!/usr/bin/env python3
"""Independent PS10/11 computations; Python 3 stdlib, no downloaded code.
Run from the subject directory: python3 tools/ps10_11_numerics.py.
Writes qa/ps10_11-numerics.json and chapters/numerical-data.tex.
"""
import json, math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
G, C, MSUN = 6.67430e-8, 2.99792458e10, 1.98847e33
GAMMA = 5/3
DENS = G/C**2*1e10
PRES = G/C**4*1e10
KCONV = PRES/DENS**GAMMA
K = 5.38e9*KCONV
MSUN_KM = G*MSUN/C**2/1e5

def rk4(fun,x,y,h):
    k1=fun(x,y)
    k2=fun(x+h/2,[a+h*b/2 for a,b in zip(y,k1)])
    k3=fun(x+h/2,[a+h*b/2 for a,b in zip(y,k2)])
    k4=fun(x+h,[a+h*b for a,b in zip(y,k3)])
    return [a+h*(b+2*c+2*d+e)/6 for a,b,c,d,e in zip(y,k1,k2,k3,k4)]

def eos(h):
    if h<=0:return 0.,0.,0.
    rho0=((GAMMA-1)/(GAMMA*K)*math.expm1(h))**(1/(GAMMA-1))
    p=K*rho0**GAMMA
    return rho0,rho0+p/(GAMMA-1),p

def tov(rho0_c_cgs,step=.0025):
    rho0=rho0_c_cgs*DENS; pc=K*rho0**GAMMA; rho=rho0+pc/(GAMMA-1)
    hc=math.log1p(GAMMA/(GAMMA-1)*K*rho0**(GAMMA-1))
    r=min(1e-5,step/100)
    m=4*math.pi*rho*r**3/3
    y=[hc-2*math.pi*(rho/3+pc)*r*r,m,m]
    def f(r,y):
        h,m,mp=y
        _,e,p=eos(h)
        if r<=2*m:raise ArithmeticError('TOV integration crossed trapped surface')
        return [-(m+4*math.pi*r**3*p)/(r*(r-2*m)),4*math.pi*e*r*r,4*math.pi*e*r*r/math.sqrt(1-2*m/r)]
    count=0
    while r<100:
        yn=rk4(f,r,y,step);count+=1
        if yn[0]<=0:
            lo,hi=0.,step
            for _ in range(45):
                mid=(lo+hi)/2
                if rk4(f,r,y,mid)[0]>0:lo=mid
                else:hi=mid
            delta=(lo+hi)/2
            y=rk4(f,r,y,delta);r+=delta
            break
        r+=step;y=yn
    else:raise ArithmeticError('No surface before 100 km')
    m,mp=y[1:]
    return {'rho0_c_cgs':rho0_c_cgs,'rho_c_cgs':rho/DENS,'R_km':r,'M_km':m,'M_solar':m/MSUN_KM,'Mp_km':mp,'binding_fraction':(mp-m)/m,'z_original':1-1/math.sqrt(1-2*m/r),'z_conventional':1/math.sqrt(1-2*m/r)-1,'steps':count}

def maximize_mass(step):
    # First mass maximum on sequence. Golden search on log10 central density.
    a,b=14.,17.; ratio=(math.sqrt(5)-1)/2
    c=b-ratio*(b-a);d=a+ratio*(b-a)
    fc=tov(10**c,step)['M_km'];fd=tov(10**d,step)['M_km']
    for _ in range(34):
        if fc<fd:a,c,fc=c,d,fd;d=a+ratio*(b-a);fd=tov(10**d,step)['M_km']
        else:b,d,fd=d,c,fc;c=b-ratio*(b-a);fc=tov(10**c,step)['M_km']
    result=tov(10**((a+b)/2),step)
    result['bracket_log10_rho0']=[a,b]
    return result

def potential(r,L):return (1-2/r)*(1+L*L/r**2)

def orbit(r,v,L,tau_end,step,keep=1200):
    E=math.sqrt(v*v+potential(r,L));y=[r,v,0.,0.];tau=0
    err=0.;rmin=r;rmax=r;hold=None;turns=[];points=[]
    stride=max(1,int(tau_end/step/keep));n=0;last_phi=0.;last_r=r
    def f(t,y):
        r,v,phi,tt=y
        return [v,-1/r**2+L*L/r**3-3*L*L/r**4,L/r**2,E/(1-2/r)]
    while tau<tau_end and 2.025<y[0]<250:
        if n%stride==0 or (keep>=1 and (abs(y[2]-last_phi)>.035 or abs(y[0]-last_r)>.015*max(1,y[0]))):
            points.append([y[0]*math.cos(y[2]),y[0]*math.sin(y[2])]);last_phi=y[2];last_r=y[0]
        h=min(step,tau_end-tau);yn=rk4(f,tau,y,h)
        if y[1]*yn[1]<0:turns.append({'tau':tau+h/2,'r':(y[0]+yn[0])/2,'phi':(y[2]+yn[2])/2,'kind':'peri' if y[1]<0 else 'apo'})
        tau+=h;n+=1;y=yn
        err=max(err,abs(y[1]**2+potential(y[0],L)-E*E))
        rmin=min(rmin,y[0]);rmax=max(rmax,y[0])
        if hold is None and abs(y[0]-r)>1e-3:hold=tau
    points.append([y[0]*math.cos(y[2]),y[0]*math.sin(y[2])])
    return {'E':E,'L':L,'initial_r':r,'initial_v':v,'step':step,'tau_final':tau,'r_final':y[0],'r_min':rmin,'r_max':rmax,'max_energy_residual':err,'hold_to_1e_minus_3':hold,'turns':turns,'points':points}

def run():
    conversions={'density_km_minus2_per_g_cm3':DENS,'pressure_km_minus2_per_dyn_cm2':PRES,'K_km4_3_per_cgs':KCONV,'K_km4_3':K,'solar_mass_km':MSUN_KM,'ten_solar_mass_length_km':10*MSUN_KM,'ten_solar_mass_time_seconds':10*G*MSUN/C**3}
    models=[tov(10**n) for n in range(14,19)]
    central_checks=[dict(step_km=h,**tov(1e15,h)) for h in [.01,.005,.0025,.00125]]
    maximum_checks=[dict(step_km=h,**maximize_mass(h)) for h in [.005,.0025,.00125]]
    sequence=[tov(10**(14+i/15),.005) for i in range(61)]
    unbound=orbit(100,-math.sqrt(1.05**2-potential(100,4.5)),4.5,600,.02)
    Ec=1.05; rcrit=(3*Ec*Ec-4+math.sqrt((3*Ec*Ec-4)**2+16*(Ec*Ec-1)))/(2*(Ec*Ec-1)); Lcrit=math.sqrt(rcrit*rcrit/(rcrit-3))
    near=orbit(100,-math.sqrt(Ec*Ec-potential(100,Lcrit*(1+1e-5))),Lcrit*(1+1e-5),600,.01)
    rp,ra=4.1,100.;ecc=(ra-rp)/(ra+rp);p=2*ra*rp/(ra+rp);Lb=p/math.sqrt(p-3-ecc*ecc)
    bound=orbit(ra,0,Lb,7000,.02)
    stable=orbit(8.,0.,math.sqrt(64/5),1000,.02)
    Lu=math.sqrt(3.5**2/(3.5-3))
    unstable=orbit(3.5,0.,Lu,500,.02)
    inward=orbit(3.5-1e-6,0.,Lu,500,.02)
    outward=orbit(3.5+1e-6,0.,Lu,500,.02)
    checks=[]
    for name,r,v,L,T in [('unbound',100,unbound['initial_v'],4.5,600),('bound',100,0,Lb,7000),('inward',3.5-1e-6,0,Lu,500),('outward',3.5+1e-6,0,Lu,500)]:
        checks.append({'name':name,'runs':[orbit(r,v,L,T,h,0.0001) for h in [.02,.01]]})
    # Additional background quantities in PS09 and PS11, using constants supplied.
    photon_u_mev=math.pi**2/15*1e18**4/(6.6e-22**3*C**3)
    lam=8*math.pi*G*photon_u_mev*1.6e-12/C**2
    H=math.sqrt(lam/3);alpha=1201*2.73*8.6e-11/1e18
    expN=1+(2*(math.sqrt(1201)-1)-1+alpha)/alpha
    Ne=math.log(expN);chi=math.asin(math.sqrt(2/5));eta_cross=math.acos(4/5-1);eta_birth=eta_cross-chi;R0=math.sqrt(125/2)
    background={'inflation_Lambda_s_minus2':lam,'inflation_H_s_minus1':H,'efolds':Ne,'expansion_factor':expN,'inflation_t2_seconds':Ne/H,'horizon_ratio_no_inflation':1/(2*(math.sqrt(1201)-1)),'OS_chi':chi,'OS_eta_cross':eta_cross,'OS_eta_birth':eta_birth,'OS_tau_birth_in_GM':R0/2*(eta_birth+math.sin(eta_birth)),'OS_tau_cross_in_GM':R0/2*(eta_cross+math.sin(eta_cross)),'OS_tau_singularity_in_GM':math.pi*R0/2}
    out={'method':'stdlib RK4 in r with log enthalpy and bisection surface; RK4 proper-time geodesics','constants_cgs':{'G':G,'c':C,'M_sun':MSUN},'conversions':conversions,'tov_models':models,'tov_central_convergence':central_checks,'tov_maximum_convergence':maximum_checks,'tov_sequence':sequence,'orbits':{'unbound':unbound,'near_critical':near,'bound':bound,'stable':stable,'unstable_exact':unstable,'unstable_inward':inward,'unstable_outward':outward},'orbit_convergence':checks,'critical_unbound':{'E':Ec,'r':rcrit,'L':Lcrit},'background':background}
    (ROOT/'qa/ps10_11-numerics.json').write_text(json.dumps(out,indent=2))
    render_tex(out)
    # A concise stdout without raw trajectory arrays.
    print(json.dumps({'conversions':conversions,'models':models,'central_convergence':central_checks,'maximum_convergence':maximum_checks,'orbits':{k:{a:b for a,b in v.items() if a not in ['points','turns']} for k,v in out['orbits'].items()},'bound_turns':bound['turns'],'critical':out['critical_unbound'],'background':background},indent=2))

def render_tex(out):
    models=out['tov_models'];sequence=out['tov_sequence'];orbits=out['orbits']
    def scientific(v,digits=4):
        exp=int(math.floor(math.log10(v)));mant=v/10**exp
        return (f"10^{{{exp}}}" if abs(mant-1)<1e-12 else f"{mant:.{digits}f}\\times10^{{{exp}}}")
    tex=['% Automatically generated by tools/ps10_11_numerics.py; actual numerical data.',
         '\\begin{center}\\begin{tabular}{rrrr}',
         '\\toprule','$\\rho_{0,c}\\;(\\mathrm{g/cm^3})$ & $\\rho_c\\;(\\mathrm{g/cm^3})$ & $R_*\\;(\\mathrm{km})$ & $M_*/M_\\odot$\\\\\\midrule']
    for a in models:
        tex.append('$'+scientific(a['rho0_c_cgs'])+'$ & $'+scientific(a['rho_c_cgs'])+f"$ & {a['R_km']:.5f} & {a['M_solar']:.6f}\\\\")
    tex+=['\\bottomrule\\end{tabular}\\end{center}',
          '\\begin{center}\\begin{tikzpicture}\\begin{semilogxaxis}[width=.82\\textwidth,height=6cm,xlabel={$\\rho_c\\;(\\mathrm{g/cm^3})$},ylabel={$M_*/M_\\odot$},grid=major]',
          '\\addplot[thick] coordinates {']
    tex+=['('+format(a['rho_c_cgs'],'.8e')+','+format(a['M_solar'],'.8f')+')' for a in sequence]
    tex+=['};\\end{semilogxaxis}\\end{tikzpicture}\\end{center}']
    captions={'unbound':'非束缚散射轨道, $\\hat E=1.05$, $\\hat L=4.5$.',
              'bound':'近分离线的束缚轨道, $r_{\\rm p}=4.1$, $r_{\\rm a}=100$.',
              'inward':'不稳定圆轨道的向内扰动, $r(0)=3.5-10^{-6}$.',
              'outward':'不稳定圆轨道的向外扰动, $r(0)=3.5+10^{-6}$. '}
    for name,key,zoom in [('unbound','unbound',12),('bound','bound',8),
                          ('inward','unstable_inward',None),('outward','unstable_outward',6)]:
        data=orbits[key]
        if name=='inward':tex.append('\\clearpage')
        tex+=['\\begin{figure}[htbp]\\centering']
        options=[('', 'width=.42\\textwidth,height=5.8cm,title={全轨道}')]
        if zoom is not None:
            options.append((f',xmin=-{zoom},xmax={zoom},ymin=-{zoom},ymax={zoom}',
                            'width=.42\\textwidth,height=5.8cm,title={近黑洞区域}'))
        else:options=[('','width=.62\\textwidth,height=5.8cm')]
        for bounds,dimensions in options:
            tex+=['\\begin{tikzpicture}\\begin{axis}[axis equal image,'+dimensions+',xlabel={$x/(GM)$},ylabel={$y/(GM)$},grid=major'+bounds+']',
                  '\\addplot[thick] coordinates {']
            tex+=['('+format(x,'.7f')+','+format(y,'.7f')+')' for x,y in data['points']]
            tex+=['};\\addplot[domain=0:360,samples=100,dashed] ({2*cos(x)},{2*sin(x)});\\end{axis}\\end{tikzpicture}']
        tex+=['\\caption{'+captions[name]+' 虚线圆为 $r=2$.}\\label{fig:ps11-'+name+'}\\end{figure}']
    (ROOT/'chapters/numerical-data.tex').write_text('\n'.join(tex)+'\n')

if __name__=='__main__':
    import sys
    if '--render-only' in sys.argv:
        render_tex(json.loads((ROOT/'qa/ps10_11-numerics.json').read_text()))
    else:run()
