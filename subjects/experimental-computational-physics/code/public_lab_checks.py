"""New public-manual tasks only; existing independently passed MD/MC kept intact."""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad
ROOT=Path(__file__).resolve().parents[1];(ROOT/'qa').mkdir(exist_ok=True)
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
R=lambda P,t:expm(-.5j*t*P)
RH=lambda P,t:np.kron(R(P,t),I)
RC=lambda P,t:np.kron(I,R(P,t))
UJ=expm(-.25j*np.pi*np.kron(Z,Z))
near=RC(Y,-np.pi/2)@UJ@RC(X,np.pi/2)
CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
proper=near@RH(Z,np.pi/2)@RC(Z,-np.pi/2)
global_phase=np.exp(-.25j*np.pi)
error=float(np.linalg.norm(proper-global_phase*CNOT));assert error<1e-12
xy=RC(Y,-np.pi/2)@UJ@RC(Y,np.pi/2)@RC(X,np.pi/2)@RH(X,-np.pi/2)@RH(Y,-np.pi/2)@RH(X,np.pi/2)
assert np.linalg.norm(xy-global_phase*CNOT)<1e-12
n=np.array([.3,-.4,.7]);norm=np.linalg.norm(n);P=n[0]*X+n[1]*Y+n[2]*Z
pauli_error=float(np.linalg.norm(expm(1j*P)-(np.cos(norm)*I+1j*np.sin(norm)*P/norm)))
assert pauli_error<1e-12
def readout(diagonal):
    a,b,c,d=diagonal;return [float(a-c),float(b-d),float(a-b),float(c-d)]
thermal=np.eye(4)/4+1e-4*np.diag([5,3,-3,-5]);initial=np.diag(thermal)
ct=CNOT@thermal@CNOT.conj().T;nt=near@thermal@near.conj().T
assert np.allclose(ct,nt)
A=RH(Y,np.pi/2)@RC(Y,-np.pi/2);B=RH(Y,-np.pi/2)@RC(Y,np.pi/2)
oracles=[np.eye(4),np.kron(I,X),CNOT,np.kron(I,X)@CNOT]
oracle_results=[]
for name,F in zip(['0','1','x','1-x'],oracles):
    U=B@F@A;psi=U[:,0];pzero=float(np.sum(np.abs(psi[:2])**2));oracle_results.append({'f':name,'DJ_unitary_real':np.round(U.real,12).tolist(),'input_x_zero_probability':pzero})
assert np.allclose([r['input_x_zero_probability'] for r in oracle_results],[1,1,0,0])
T2=.1;delta=17.;phi=.4
numerical=quad(lambda t:np.exp(-t/T2)*np.cos(phi-delta*t),0,np.inf)[0]+1j*quad(lambda t:np.exp(-t/T2)*np.sin(phi-delta*t),0,np.inf)[0]
analytic=np.exp(1j*phi)/(1/T2+1j*delta);assert abs(numerical-analytic)<1e-9
kappa,ukappa,dV,udV=41.6,1.3,7.6,.03
wavelength=2*kappa*dV;uncertainty=np.hypot(2*dV*ukappa,2*kappa*udV)
# Walsh cluster basis: orthogonal Gram matrix and exact full-basis reconstruction.
spins=np.array([[1 if (state>>i)&1 else -1 for i in range(4)] for state in range(16)])
Phi=np.array([[np.prod(s[[i for i in range(4) if (mask>>i)&1]]) if mask else 1 for mask in range(16)] for s in spins],float)
assert np.allclose(Phi.T@Phi/16,np.eye(16))
coeff=np.arange(16,dtype=float)/7
energies=Phi@coeff
cluster_error=float(np.max(np.abs(Phi.T@energies/16-coeff)))
assert cluster_error<1e-12
out={'kind':'actual calculation of specified mathematical and simulated-readout examples; no physical measurements fabricated','basis_order':'H left, C right:00,01,10,11','near_CNOT_phase_corrected_error':error,'XY_sequence_CNOT_error':float(np.linalg.norm(xy-global_phase*CNOT)),'Pauli_exponential_error':pauli_error,'cluster_full_basis_reconstruction_error':cluster_error,'pure_population_peak_integrals':[readout(v) for v in np.eye(4)],'thermal_peak_integrals':readout(initial),'CNOT_thermal_peak_integrals':readout(np.diag(ct).real),'near_CNOT_same_diagonal_thermal_spectrum':True,'oracle_results':oracle_results,'one_sided_FID':{'T2':T2,'delta_angular_frequency':delta,'phase':phi,'complex_quadrature_error':float(abs(numerical-analytic))},'PZT_example':{'calibration_kind':'manual illustrative tag, not calibrated project apparatus','nm_per_V':kappa,'standard_uncertainty_nm_per_V':ukappa,'voltage_interval_kind':'author specified simulated same-phase interval','deltaV':dV,'u_deltaV':udV,'wavelength_nm':wavelength,'u_wavelength_nm':float(uncertainty)}}
(ROOT/'qa/public-lab-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('New public lab tasks: Pauli/CNOT pulse sequences/oracles/FID and PZT uncertainty checked.')
