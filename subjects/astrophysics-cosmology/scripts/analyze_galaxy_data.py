"""Measure the real OCW PS1 FITS archive; never redistributes source images.

Usage: python scripts/analyze_galaxy_data.py ARCHIVE --response FILTER_FITS --out qa
Requires numpy, scipy, astropy. The optional response specifies a declared
response-weighted band-energy convention, not a unique bolometric correction.
"""
import argparse,hashlib,io,json,zipfile
from pathlib import Path
import numpy as np
from astropy.io import fits
from scipy.ndimage import gaussian_filter
from scipy.optimize import curve_fit
from scipy.special import gamma

C_KMS=299792.458
C_AAS=2.99792458e18
PIXEL=0.394
G_PC=4.30091727e-3
PC_CM=3.0856775814913673e18
LSUN=3.828e33

def read_image(z,name):
    raw=z.read(name)
    with fits.open(io.BytesIO(raw)) as hd:
        data=hd[0].data.astype(float);header=dict(hd[0].header)
    return data,header,hashlib.sha256(raw).hexdigest()

def refine_center(image,x,y):
    ix,iy=int(x),int(y)
    cut=image[iy-25:iy+25,ix-25:ix+25]
    my,mx=np.unravel_index(np.argmax(gaussian_filter(cut,2)),cut.shape)
    px,py=ix-25+mx,iy-25+my
    yy,xx=np.indices((15,15));xx=xx+px-7;yy=yy+py-7
    patch=image[py-7:py+8,px-7:px+8]
    def model(xy,b,A,xc,yc,wx,wy,angle):
        dx,dy=xy[0]-xc,xy[1]-yc
        u=dx*np.cos(angle)+dy*np.sin(angle);v=-dx*np.sin(angle)+dy*np.cos(angle)
        return b+A*np.exp(-.5*((u/wx)**2+(v/wy)**2))
    pars,_=curve_fit(model,(xx.ravel(),yy.ravel()),patch.ravel(),
        p0=[1095,patch.max()-1095,px,py,3,3,0],
        bounds=([1000,0,px-3,py-3,.5,.5,-np.pi],
                [1500,100000,px+3,py+3,15,15,np.pi]),maxfev=20000)
    return pars[2],pars[3]

def spectral_line(w,f,err,mask,guess,window,absorption):
    # In historical spSpec, bit 30 identifies an emission line, not bad data.
    # Removing it would erase precisely the H-alpha feature being measured.
    acceptable=(mask.astype(np.int64)&~(1<<30))==0
    valid=(w>window[0])&(w<window[1])&(err>0)&np.isfinite(f)&acceptable
    x,y,e=w[valid],f[valid],err[valid]
    assert len(x)>8,'Insufficient actual line pixels for a five-parameter fit'
    sign=-1 if absorption else 1
    def model(lam,b,slope,A,center,width):
        return b+slope*(lam-guess)+sign*A*np.exp(-.5*((lam-center)/width)**2)
    amplitude=(np.median(y)-np.min(y)) if absorption else (np.max(y)-np.median(y))
    pars,cov=curve_fit(model,x,y,p0=[np.median(y),0,max(amplitude,1),guess,5 if absorption else 2],
        sigma=e,absolute_sigma=True,bounds=([-np.inf,-np.inf,0,guess-12,.3],
        [np.inf,np.inf,np.inf,guess+12,20]),maxfev=20000)
    chi2=np.sum(((y-model(x,*pars))/e)**2)
    return pars,cov,x,y,model,chi2/(len(x)-len(pars))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('archive',type=Path)
    ap.add_argument('--response',type=Path);ap.add_argument('--out',type=Path,default=Path('qa'))
    args=ap.parse_args();out=args.out;out.mkdir(parents=True,exist_ok=True)
    assert hashlib.sha256(args.archive.read_bytes()).hexdigest()=='920f11cc10ff2ef852924d0cb5d4d7d6af0e3639a1f35e34c7053c379e469adb'
    response=None
    if args.response:
        with fits.open(args.response) as hd:
            response=(np.asarray(hd['G'].data['wavelength'],float),
                      np.asarray(hd['G'].data['respt'],float))
    record={'archive_sha256':hashlib.sha256(args.archive.read_bytes()).hexdigest(),
      'input_images_redistributed':False,'pixel_scale_arcsec':PIXEL,
      'method':'core elliptical Gaussian centroid; sky median in 150–200 pixel annulus; one-pixel mean profile, two-arcsec median profile; log-intensity least squares on 3–31 arcsec; local Gaussian line with linear continuum and supplied error/mask, accepting the historical bit-30 EMLINE flag; no seeing deconvolution',
      'galaxies':[],'limits':'Circular medians and restricted radial fitting interval; statistical curve fit errors omit sky/centering/PSF/template systematics. Single fibers do not uniquely determine global spectral shape or precision band luminosity.'}
    with zipfile.ZipFile(args.archive) as z:
        for j,(sx,sy,c20,w0,rest,line_guess,window,absorp) in enumerate([
          (1831.5,636.5,2328.,3.5823,8545.,8741.,(8705,8775),True),
          (1346.,945.,2496.,3.5825,6563.,6679.,(6668,6691),False)],1):
            image,h,imsha=read_image(z,f'data/galaxy{j}.fit')
            x0,y0=refine_center(image,sx,sy)
            yy,xx=np.indices(image.shape);r=np.hypot(xx-x0,yy-y0)
            sky=float(np.median(image[(r>=150)&(r<200)]));signal=image-sky
            one=[]
            for n in range(150):
                v=signal[(r>=n)&(r<n+1)];mean=float(np.mean(v))
                if mean>0:one.append([(n+.5)*PIXEL,mean,np.log10(mean)])
            np.savetxt(out/f'ps1-galaxy{j}-onepixel.csv',one,delimiter=',',header='r_arcsec,dn_mean,log_dn',comments='')
            prof=[]
            for n in range(25):
                v=signal[(r*PIXEL>=2*n)&(r*PIXEL<2*n+2)]
                I=float(np.median(v))
                if I>0:prof.append([2*n+1,I,20-2.5*np.log10(I/(PIXEL**2*c20))])
            prof=np.asarray(prof);rf,I=prof[:,0],prof[:,1];good=(rf>=3)&(rf<=31)
            models={};curves=[]
            for name,power in [('exponential',1.),('de_vaucouleurs',.25)]:
                design=np.stack([np.ones(good.sum()),rf[good]**power],axis=1)
                inter,slope=np.linalg.lstsq(design,np.log(I[good]),rcond=None)[0]
                assert slope<0
                scale=-1/slope if power==1 else (-7.67/slope)**4
                fit=np.exp(inter+slope*rf**power)
                rms=float(np.sqrt(np.mean((np.log10(I[good])-np.log10(fit[good]))**2)))
                counts=2*np.pi*np.exp(inter)*scale**2/PIXEL**2 if power==1 else 8*np.pi*np.exp(inter)*scale**2*gamma(8)/(7.67**8*PIXEL**2)
                models[name]={'I0_DN_per_pixel':float(np.exp(inter)),'scale_arcsec':float(scale),'rms_log10_DN':rms,'model_counts_infinite':float(counts),'m_g':float(20-2.5*np.log10(counts/c20))}
                curves.append(fit)
            np.savetxt(out/f'ps1-galaxy{j}-profile.csv',np.column_stack([prof,*curves]),delimiter=',',
                header='r_arcsec,dn_median,mu_mag_arcsec2,fit_exp_dn,fit_dev_dn',comments='')
            spectrum,sh,spsha=read_image(z,f'data/galaxy{j}spec.fits')
            assert abs(float(sh['COEFF0'])-w0)<1e-10
            w=10**(w0+.0001*np.arange(spectrum.shape[1]));f=spectrum[0];err=spectrum[2];mask=spectrum[3]
            cont=f-spectrum[1];bins=np.arange(4000,9001,200)
            med=np.asarray([np.median(cont[(w>=v)&(w<v+200)]) for v in bins[:-1]])
            lam_peak=float(bins[:-1][np.argmax(med)]+100)
            p,cov,lam,line,fun,redchi=spectral_line(w,f,err,mask,line_guess,window,absorp)
            center,width=float(p[3]),float(p[4]);redshift=center/rest-1
            distance=C_KMS*redshift/71
            temperature=2.897771955e7/(lam_peak/(1+redshift))
            np.savetxt(out/f'ps1-galaxy{j}-continuum.csv',np.column_stack([bins[:-1]+100,med]),delimiter=',',header='wavelength_A,continuum_bin_median',comments='')
            grid=np.linspace(window[0],window[1],200)
            base=p[0]+p[1]*(grid-line_guess)
            np.savetxt(out/f'ps1-galaxy{j}-line-fit.csv',np.column_stack([grid,fun(grid,*p)/base]),delimiter=',',header='wavelength_A,normalized_fit',comments='')
            np.savetxt(out/f'ps1-galaxy{j}-line-measurements.csv',np.column_stack([lam,line/(p[0]+p[1]*(lam-line_guess))]),delimiter=',',header='wavelength_A,normalized_measurement',comments='')
            bandfactor=None
            if response:
                wl,R=response;R=R/R.max();fl=np.interp(wl,w,f)*1e-17
                # Photon-weighted AB mean: <Fnu> = integral(Flam R lambda dlambda)/(c integral(R/lambda dlambda)).
                fnu=np.trapezoid(fl*R*wl,wl)/(C_AAS*np.trapezoid(R/wl,wl))
                bandfactor=float(np.trapezoid(fl*R,wl)/fnu)
            for name,model in models.items():
                model['physical_scale_kpc']=model['scale_arcsec']/206265*distance*1000
                if bandfactor:
                    Fnu=3631e-23*10**(-.4*model['m_g']);Fband=Fnu*bandfactor
                    L=4*np.pi*(distance*1e6*PC_CM)**2*Fband
                    model['response_weighted_L_g_over_0p9_Lsun']=float(L/(.9*LSUN))
            result={'galaxy':j,'image_sha256':imsha,'spectrum_sha256':spsha,
              'center_zero_based':[float(x0),float(y0)],'center_FITS_one_based':[float(x0+1),float(y0+1)],
              'sky_DN':sky,'models':models,'better_profile':min(models,key=lambda n:models[n]['rms_log10_DN']),
              'continuum_peak_observed_A_200A_bins':lam_peak,'rough_Wien_temperature_K':temperature,
              'line_center_A':center,'line_center_stat_error_A':float(np.sqrt(cov[3,3])),
              'line_sigma_A':width,'line_sigma_stat_error_A':float(np.sqrt(cov[4,4])),
              'line_reduced_chi_square':float(redchi),'line_pixels_used':len(lam),
              'redshift_using_course_rest_wavelength':redshift,'cz_kms':C_KMS*redshift,
              'distance_Mpc_local_Hubble':distance,'response_band_energy_per_Fnu_Hz':bandfactor}
            if j==1:
                vobs=C_KMS*width/center
                result['observed_sigma_kms']=vobs
                assert vobs>95
                vs=float(np.sqrt(vobs*vobs-95**2));result['stellar_dispersion_kms']=vs
                re=models[result['better_profile']]['physical_scale_kpc']
                result['mass_C1_Msun']=vs**2*(1000*re)/G_PC
                result['mass_note']='M=C sigma_los^2 R/G; reported C=1 convention only, true C needs density and anisotropy. R chosen fitted characteristic radius.'
            record['galaxies'].append(result)
    if args.response:
        record['response_sha256']=hashlib.sha256(args.response.read_bytes()).hexdigest()
        record['band_luminosity_assumptions']='Historical SDSS g as AB; 2001 respt peak normalized to 1; central measured spectrum used as global spectral shape; constant-endpoint extrapolation below spectral blue limit; ignore extinction and cosmological K correction as course requests; solar response-band luminosity stipulated as 0.9 Lsun. Not a precision or convention-independent luminosity.'
    (out/'ps1-measurements.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(record,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
