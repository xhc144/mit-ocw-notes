"""Actual parameterized public oscillatory-pipe and film computations."""
from pathlib import Path
import json
import numpy as np
from scipy.special import jv
from scipy.linalg import solve_banded
from scipy.integrate import quad
ROOT=Path(__file__).resolve().parents[1]

def pipe_E(omega,D,N):
    dr=1/N;r=(np.arange(N)+.5)*dr;weight=2*r*dr
    z=np.sqrt(-1j*omega);W=1-jv(0,z*r)/jv(0,z)
    W/=np.dot(weight,W);Wp=W-np.dot(weight,W)
    lower=np.arange(N)/((np.arange(N)+.5)*dr*dr)
    upper=(np.arange(N)+1)/((np.arange(N)+.5)*dr*dr);upper[-1]=0
    diagonal=-(lower+upper)
    ab=np.zeros((3,N),complex);ab[0,1:]=-D*upper[:-1];ab[1]=1j*omega-D*diagonal;ab[2,:-1]=-D*lower[1:]
    chi=solve_banded((1,1),ab,Wp);E=.5*np.real(np.dot(weight,Wp*np.conj(chi)))
    # Discrete FV integration by parts uses shared face weights exactly.
    face=np.arange(1,N)*dr;diss=D*np.sum(face*np.abs(np.diff(chi)/dr)**2)*dr
    assert E>=-1e-14 and abs(E-diss)<1e-10
    return E,abs(np.dot(weight,chi)),float(abs(E-diss))

def film_coefficient(delta):
    k=omega=1.;nu=delta*delta/2;s=np.sqrt(k*k-1j*omega/nu);star=np.conj(s)
    bracket=-s/(4*k)+s*star/(k+star)**2+k*k/(s+k)**2-k*star/(s+star)**2
    I=.5*np.real(1j*star/abs(s-k)**2*bracket)
    # Amplitude squared is factored out: this is the perturbative coefficient.
    wall=.5*np.real(s);outer=wall-I/nu
    def F(d):
        W=(s*np.exp(-k*d)-k*np.exp(-s*d))/(s-k)
        Up=-1j*s/(s-k)*(-k*np.exp(-k*d)+s*np.exp(-s*d))
        return .5*np.real(W*np.conj(Up))
    # Integrate only the real decaying cross terms; the potential-potential
    # term has identically zero real part and can otherwise lose cancellation.
    def localized(d):
        value=1j*star/abs(s-k)**2*(s*star*np.exp(-(k+star)*d)+k*k*np.exp(-(s+k)*d)-k*star*np.exp(-(s+star)*d))
        return .5*np.real(value)
    assert max(abs(F(d)-localized(d)) for d in [delta/10,delta,3*delta,10*delta])<1e-9
    numeric=quad(lambda d:d*localized(d),0,max(40*delta,20),epsabs=1e-11,limit=500,points=[delta,2*delta,5*delta,10*delta])[0]
    assert abs(I-numeric)<1e-8
    return outer,float(abs(I-numeric))

def main():
    reports=[]
    for D,name in [(.1,'01'),(1.,'1'),(10.,'10')]:
        rows=[];difference=[]
        for omega in np.geomspace(1e-4,100,49):
            E,mean,res=pipe_E(omega,D,400);coarse,_,_=pipe_E(omega,D,200)
            rows.append([omega,E,E*D,mean,res]);difference.append(abs(E-coarse))
        assert abs(rows[0][2]-1/96)<2e-6
        np.savetxt(ROOT/'data'/f'osc-pipe-D{name}.csv',rows,delimiter=',',header='omega,E,normalized_E,corrector_mean_residual,energy_identity_residual',comments='')
        reports.append({'D':D,'a':1,'nu':1,'mean_velocity_amplitude':1,'frequency_points':49,'radial_cells':[200,400],'maximum_grid_difference_E':float(max(difference)),'low_frequency_normalized_E':rows[0][2],'expected_low_frequency':1/96})
    film=[]
    for delta in [.003,.01,.03,.1,.3,1.,3.]:
        c,res=film_coefficient(delta);film.append({'k_delta':delta,'outer_streaming_over_A2_omega_k':c,'film_drift_over_A2_omega_k':-c,'exponential_integral_check':res})
    assert abs(film[0]['outer_streaming_over_A2_omega_k']-.25)<.003
    report={'status':'PASS','pipe':reports,'film':film,'normalization':'all illustrative model parameters; no empirical observations','film_small_amplitude':'A is factored out; coefficient is the second-order perturbative limit before any thin-layer limit','physical_parameter_gaps':'Original pipe and artery assignments do not specify numerical material or wall parameters; symbolic solution and declared illustrative computation provided.'}
    (ROOT/'qa/oscillatory-task-checks.json').write_text(json.dumps(report,indent=2));print('Oscillatory public tasks PASS',flush=True)
if __name__=='__main__':main()
