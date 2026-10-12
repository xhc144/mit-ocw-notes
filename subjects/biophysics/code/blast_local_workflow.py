"""Actual BLAST+/PSI-BLAST reproducible method task on a specified local public database.
Requires official BLAST+ binaries and an externally downloaded Swiss-Prot database.
Example: python code/blast_local_workflow.py --blast-bin /tmp/bio-blast/ncbi-blast-2.17.0+/bin --database /tmp/bio-blast/swissprot
The large third-party database/binaries are deliberately not bundled in this source ZIP.
"""
from pathlib import Path
import argparse,subprocess,json,hashlib,numpy as np
p=argparse.ArgumentParser();p.add_argument('--blast-bin',required=True);p.add_argument('--database',required=True);args=p.parse_args();B=Path(args.blast_bin);D=Path(__file__).resolve().parents[1];data=D/'data';qa=D/'qa';qa.mkdir(exist_ok=True)
rng=np.random.default_rng(20261012);letters='CMFILVWYAGTSQNEDHRKP';freq=np.array([1.660,2.370,4.100,5.810,9.430,6.580,1.240,3.190,7.580,6.840,5.670,7.130,3.970,4.440,6.360,5.270,2.240,5.160,5.940,4.920]);freq/=freq.sum();rows=[]
for length in [10,50,150,1500]:
 for rep in range(3):rows.append((f'random_{length}_rep{rep}', ''.join(rng.choice(list(letters),size=length,p=freq))))
rows.append(('periodic_hydrophobic_150',''.join(rng.choice(list(letters[:10]),p=freq[:10]/freq[:10].sum()) if i%4<2 else rng.choice(list(letters[10:]),p=freq[10:]/freq[10:].sum()) for i in range(150))))
base='MDETGKELVLALYDYQEKSPREVTMKKGDILTLLNSTNKDWWKVEVNDRQGYVPAAYVKKLD'
for constrained in [False,True]:
 for percent in [0,20,40,60,80,100]:
  a=list(base);pos=rng.choice(len(a),round(len(a)*percent/100),replace=False)
  for i in pos:
   group=letters[:10] if a[i] in letters[:10] else letters[10:];options=group if constrained else letters;a[i]=rng.choice([s for s in options if s!=a[i]])
  rows.append((f'SH3_{"class" if constrained else "all"}_{percent}', ''.join(a)))
query=data/'blast-local-queries.fasta';query.write_text(''.join('>'+n+'\n'+s+'\n' for n,s in rows));commands=[]
fmt='6 qseqid sseqid pident length evalue bitscore qcovs'
cmd=[str(B/'blastp'),'-query',str(query),'-db',args.database,'-out',str(data/'blast-local-results.tsv'),'-outfmt',fmt,'-evalue','0.01','-seg','yes','-comp_based_stats','2','-matrix','BLOSUM62','-max_target_seqs','10','-num_threads','2']
r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);commands.append({'argv':cmd,'exit_code':r.returncode,'messages':r.stdout});assert r.returncode==0;print('BLAST batch done',flush=True)
# PSI-BLAST accepts one query per job; run both mutation mechanisms across six rates.
for n,s in rows:
 if not n.startswith('SH3_'):continue
 q=Path('/tmp')/('mit-'+n+'.fasta');q.write_text('>'+n+'\n'+s+'\n');out=data/('psi-'+n+'.tsv')
 cmd=[str(B/'psiblast'),'-query',str(q),'-db',args.database,'-out',str(out),'-outfmt',fmt,'-evalue','0.01','-inclusion_ethresh','0.005','-num_iterations','3','-seg','yes','-comp_based_stats','2','-matrix','BLOSUM62','-max_target_seqs','10','-num_threads','2']
 r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);commands.append({'argv':cmd,'exit_code':r.returncode,'messages':r.stdout});assert r.returncode==0;print('PSI done',n,flush=True)
version=subprocess.check_output([str(B/'blastp'),'-version'],text=True);dbinfo=subprocess.check_output([str(B/'blastdbcmd'),'-db',args.database,'-info'],text=True)
def hits(f):
 out={}
 for s in f.read_text().splitlines():
  if not s or s.startswith('#'):continue
  a=s.split('\t');out.setdefault(a[0],[]).append({'subject':a[1],'identity_percent':float(a[2]),'aligned_length':int(a[3]),'evalue':float(a[4]),'bitscore':float(a[5]),'query_coverage_percent':float(a[6])})
 return out
bhits=hits(data/'blast-local-results.tsv');summary=[]
for n,s in rows:
 phits=hits(data/('psi-'+n+'.tsv')).get(n,[]) if n.startswith('SH3_') else None
 summary.append({'query':n,'length':len(s),'blast_hits_retained':len(bhits.get(n,[])),'blast_best':bhits.get(n,[None])[0],'psi_rows_over_up_to_3_iterations':len(phits) if phits is not None else None,'psi_best_across_returned_iterations':min(phits,key=lambda z:z['evalue']) if phits else None})
record={'kind':'actual computational database search; current curated Swiss-Prot, not historical 2011 nr','tool_version':version,'database_info':dbinfo,'parameters':{'evalue':.01,'PSI_inclusion_evalue':.005,'iterations_max':3,'matrix':'BLOSUM62','SEG':True,'composition_statistics':2},'query_sha256':hashlib.sha256(query.read_bytes()).hexdigest(),'queries':summary,'commands':commands,'limitations':['Swiss-Prot differs from nr and 2011 database','one mutation realization at each percentage; not universal threshold','retained targets truncated to10; PSI rows include rounds','matches do not prove function or genuine homology']}
(qa/'blast-local-analysis.json').write_text(json.dumps(record,ensure_ascii=False,indent=2));print('All local BLAST/PSI method tasks completed')
