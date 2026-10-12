"""Finite checks for revised AMO formulas and pulse sequences, not precision QED/many-body validation."""
from pathlib import Path
import numpy as np,json,math
ROOT=Path(__file__).resolve().parents[1];out={}
# Fixed complex B/P convention: coherent second port has positive sin.
B=np.array([[1,-1j],[-1j,1]],complex)/math.sqrt(2);checks=[]
for phi in [0,.3,1,math.pi]:
 U=B.conj().T@np.diag([np.exp(-1j*phi),1])@B
 expected=np.exp(-1j*phi/2)*np.array([math.cos(phi/2),math.sin(phi/2)])
 err=float(np.max(abs(U[:,0]-expected)));assert err<1e-12
 checks.append({'phi':phi,'first_input_column_residual':err})
out['Yurke_fixed_B_P_coherent_ports']=checks
out['strict_threshold_boundary']={'r_exact':math.acosh(100),'lambda0':1/math.cosh(math.acosh(100)),
 'all_coefficients_le_epsilon':True,'strictly_greater_count':0,'operator_parameter_for_given_series':2*math.acosh(100)}
assert abs(out['strict_threshold_boundary']['lambda0']-.01)<1e-15
# Bogoliubov integral: rationalized expression avoids high-q cancellation.
t=np.linspace(1e-9,1-1e-9,400001);q=t/(1-t);D=q*np.sqrt(q*q+2)
integrand=q*q/(2*D*(q*q+1+D))/(1-t)**2
integ=float(np.trapezoid(integrand,t));expected=1/(3*math.sqrt(2));assert abs(integ-expected)<1e-6
out['Bogoliubov_depletion_integral']={'numeric':integ,'analytic':expected,'residual':abs(integ-expected)}
x=math.sqrt(2)-1;tip=x*(1-x)/(x+1);out['Mott_MF_n1_tip_zJ_over_U']=tip;assert abs(tip-(math.sqrt(2)-1)**2)<1e-12
out['evaporation_example']={'eta':8,'kappa_approx':1,'alpha':2,'fixed_omega_efficiency':5,'fixed_omega_elastic_N_exponent':-1,
 'lowered_optical_omega_T_power':.5,'optical_efficiency':2,'optical_elastic_N_exponent':2}
# Cirac-Zoller control red pi, target auxiliary red 2pi, inverse control pi.
def ix(c,t,n):return c*6+t*2+n
Uc=np.eye(12,dtype=complex);Ut=np.eye(12,dtype=complex)
for t0 in range(3):
 pair=[ix(1,t0,0),ix(0,t0,1)];Uc[np.ix_(pair,pair)]=np.array([[0,-1j],[-1j,0]])
for c0 in range(2):
 pair=[ix(c0,1,1),ix(c0,2,0)];Ut[np.ix_(pair,pair)]=-np.eye(2)
U=Uc.conj().T@Ut@Uc
logical=[ix(c,t0,0) for c in range(2) for t0 in range(2)]
err=float(np.max(abs(U[np.ix_(logical,logical)]-np.diag([1,1,1,-1]))))
leak=float(np.max(abs(U[np.ix_([i for i in range(12) if i not in logical],logical)])))
assert err<1e-12 and leak<1e-12
out['Cirac_Zoller']={'CZ_residual':err,'motion_or_aux_leakage_amplitude':leak}
# Four strong-drive Mollow dressed transition magnitudes.
plus=np.array([1,1])/math.sqrt(2);minus=np.array([1,-1])/math.sqrt(2);lower=np.array([[0,0],[1,0]])
weights=[float(abs(a@lower@b)**2) for a in [plus,minus] for b in [plus,minus]]
assert max(abs(v-.25) for v in weights)<1e-12
out['Mollow_resonant_dressed_transition_weights']=weights
# Exact transverse hyperfine coupling table for S=I=1/2.
X2=np.array([[0,1],[1,0]],complex);Y2=np.array([[0,-1j],[1j,0]]);Z2=np.diag([1,-1]);I2=np.eye(2)
out['hyperfine_transverse_coupling_table']=[]
for field in [0,.1,1,10]:
 gS=2;gI=.07;delta=(gS-gI)*field;theta=.5*math.atan2(1,delta);co=math.cos(theta);si=math.sin(theta)
 u=np.array([0,co,si,0]);v=np.array([0,-si,co,0]);ends=np.eye(4)[[0,3]]
 Hp=(gS*np.kron(X2,I2)+gI*np.kron(I2,X2))/2
 got=ends@Hp@np.array([u,v]).T
 want=np.array([[gI*co+gS*si,gS*co-gI*si],[gS*co+gI*si,gI*co-gS*si]])/2
 err=float(np.max(abs(got-want)));assert err<1e-12
 Hhf=(np.kron(X2,X2)+np.kron(Y2,Y2)+np.kron(Z2,Z2))/4+field*(gS*np.kron(Z2,I2)+gI*np.kron(I2,Z2))/2
 en=[-.25+math.sqrt(1+delta*delta)/2,-.25-math.sqrt(1+delta*delta)/2]
 er2=max(float(np.max(abs(Hhf@state-E*state))) for state,E in zip([u,v],en));assert er2<1e-12
 out['hyperfine_transverse_coupling_table'].append({'B_units':field,'matrix_residual':err,'mixed_eigenstate_residual':er2})
out['scope']='Finite pulse/mode checks and explicit-model scalar integrals; not independent proof of full QED, exact many-body phase diagram, or experimental accuracy.'
(ROOT/'qa/revision-math-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2))
