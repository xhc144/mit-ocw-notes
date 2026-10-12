"""Read original MIT supplied coordinates and derive dihedrals/contact summaries."""
from pathlib import Path
import json,numpy as np,urllib.request,hashlib,fitz,re
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'data/public'
# Third-party MJ original is read transiently; original table and 400 values are NOT redistributed.
url='https://ocw.mit.edu/courses/8-592j-statistical-physics-in-biology-spring-2011/1b821d36380d4de6f2270eb875336417_mj_table3.pdf'
b=urllib.request.urlopen(url,timeout=45).read();text=''.join(p.get_text() for p in fitz.open(stream=b,filetype='pdf'))
labels=['Cys','Met','Phe','Ile','Leu','Val','Trp','Tyr','Ala','Gly','Thr','Ser','Asn','Gln','Asp','Glu','His','Arg','Lys','Pro'];rows=[]
# Text extraction may be line-by-line or entire row; use matching between successive labels.
for lab in labels:
 pattern=rf'{lab}\s+((?:-?\d+\.\d+\s+){{20}}){lab}'
 m=re.search(pattern,text)
 if not m:raise ValueError('MJ text row not found: '+lab)
 rows.append([float(v) for v in m.group(1).split()])
raw=np.array(rows);U=np.triu(raw)+np.triu(raw,1).T;mean=float(U.mean());variance=float(U.var());g=1.85
result={'MJ':{'url':url,'input_sha256':hashlib.sha256(b).hexdigest(),'choice':'e_ij upper triangle plus diagonal, symmetrized; lower e_prime is a different table','weights':'uniform amino acid probability 1/20; ordered pairs include diagonals','mean_in_RT_units':mean,'variance_in_RT_squared_units':variance,'Tc_over_energy_reference_T0_at_n_over_N_2':float(np.sqrt(variance/np.log(g))),'Ec_over_N_at_n_over_N_2':float(2*mean-2*np.sqrt(variance*np.log(g))),'original_table_included':False},'proteins':{}}
AA={s.upper():i for i,s in enumerate(labels)}
def angle(p0,p1,p2,p3):
 b0=-(p1-p0);b1=p2-p1;b2=p3-p2;b1/=np.linalg.norm(b1)
 v=b0-np.dot(b0,b1)*b1;w=b2-np.dot(b2,b1)*b1
 return float(np.degrees(np.arctan2(np.dot(np.cross(b1,v),w),np.dot(v,w))))
for name in ['1TEN.PDB','4HHB_A.PDB']:
 lines=(P/name).read_text().splitlines();res={};lig=[];ranges=[]
 for s in lines:
  if s.startswith('HELIX '):ranges.append(('H',s[19],int(s[21:25]),int(s[33:37])))
  if s.startswith('SHEET '):ranges.append(('S',s[21],int(s[22:26]),int(s[33:37])))
  if s.startswith(('ATOM  ','HETATM')) and s[16] in [' ','A']:
   atom=s[12:16].strip();aa=s[17:20];key=(s[21],int(s[22:26]),s[26]);xyz=np.array([float(s[30:38]),float(s[38:46]),float(s[46:54])])
   if s.startswith('HETATM'):
    if aa not in ['HOH','WAT'] and not atom.startswith('H'):lig.append(xyz)
   elif aa in AA:res.setdefault(key,{'aa':aa,'atoms':{}})['atoms'][atom]=xyz
 keys=sorted(res);data=[];contacts=[];energy=0
 for i in range(1,len(keys)-1):
  k=keys[i];prev=res[keys[i-1]];cur=res[k];nextres=res[keys[i+1]]
  if keys[i-1][0]!=k[0] or keys[i+1][0]!=k[0]:continue
  if not all(a in cur['atoms'] for a in ['N','CA','C']) or 'C' not in prev['atoms'] or 'N' not in nextres['atoms']:continue
  if np.linalg.norm(prev['atoms']['C']-cur['atoms']['N'])>1.8 or np.linalg.norm(cur['atoms']['C']-nextres['atoms']['N'])>1.8:continue
  phi=angle(prev['atoms']['C'],cur['atoms']['N'],cur['atoms']['CA'],cur['atoms']['C']);psi=angle(cur['atoms']['N'],cur['atoms']['CA'],cur['atoms']['C'],nextres['atoms']['N'])
  kind=next((typ for typ,chain,start,end in ranges if chain==k[0] and start<=k[1]<=end),'C')
  dist=float(min(np.linalg.norm(cur['atoms']['CA']-v) for v in lig)) if lig else None
  data.append({'chain':k[0],'residue':k[1],'aa':cur['aa'],'phi':phi,'psi':psi,'secondary':kind,'nearest_nonwater_ligand_CA_distance_A':dist})
 cas=[(k,r) for k,r in res.items() if 'CA' in r['atoms']]
 for i,(ki,ri) in enumerate(cas):
  for kj,rj in cas[i+1:]:
   if ki[0]!=kj[0] or abs(ki[1]-kj[1])<=2:continue
   if np.linalg.norm(ri['atoms']['CA']-rj['atoms']['CA'])<8:
    contacts.append([ki[1],kj[1]]);energy+=U[AA[ri['aa']],AA[rj['aa']]]
 n=len(contacts);N=len(cas);ec=n*mean-np.sqrt(2*n*variance*N*np.log(g))
 out=ROOT/'data'/('ramachandran-'+name.split('.')[0]+'.csv')
 out.write_text('phi,psi,secondary,aa,residue\n'+'\n'.join(f"{r['phi']:.6f},{r['psi']:.6f},{r['secondary']},{r['aa']},{r['residue']}" for r in data)+'\n')
 positive=[r for r in data if r['phi']>0];result['proteins'][name]={'residues_with_CA':N,'torsions_count':len(data),'positive_phi':positive,'secondary_counts':{k:sum(r['secondary']==k for r in data) for k in ['H','S','C']},'nonwater_ligand_atoms':len(lig),'CA_contacts_cutoff_8A_sequence_exclusion_2':n,'native_contact_energy_RT':float(energy),'REM_Ec_RT_using_actual_contact_count':float(ec),'EN_over_Ec':float(energy/ec),'all_dihedrals':data,'contact_definition_is_author_model':True}
(ROOT/'qa/structure-analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print('MJ aggregate facts and actual coordinate dihedrals:',{k:(v['torsions_count'],len(v['positive_phi']),v['native_contact_energy_RT'],v['EN_over_Ec']) for k,v in result['proteins'].items()})
