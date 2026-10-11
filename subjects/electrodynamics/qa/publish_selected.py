#!/usr/bin/env python3
"""Publish a frozen electrodynamics batch via ordinary Git to the authorized public repo.
The repository uploader is private-only; it is left unchanged. No force or token creation.
"""
import subprocess,json,hashlib,sys,shutil,fcntl
from pathlib import Path
ROOT=Path('/workspace/mit-ocw-notes')
m=json.loads(Path(sys.argv[1]).read_text()); assert m['repo']=='xhc144/mit-ocw-notes' and m['branch']=='main'
for e in m['files']:
 assert e['path'].startswith(('subjects/electrodynamics/','sources/electrodynamics/')) or e['path']=='manifests/electrodynamics-sources.json'
 assert '..' not in Path(e['path']).parts
 assert hashlib.sha256((ROOT/e['source']).read_bytes()).hexdigest()==e['sha256']
def run(args,cwd=None): return subprocess.check_output(args,cwd=cwd,stderr=subprocess.STDOUT)
lock=open('/tmp/mit-ocw-native-publication.lock','w');fcntl.flock(lock,fcntl.LOCK_EX)
head=run(['git','ls-remote','https://github.com/'+m['repo']+'.git','refs/heads/main']).decode().split()[0]
assert head==m['expected_head'],f'HEAD moved before publication: {head}'
w=Path('/tmp/electrodynamics-publish-'+m['expected_head'][:10]+'-'+Path(sys.argv[1]).stem)
assert not w.exists(),'isolated publication checkout already exists; inspect it before retry'
run(['git','clone','--shared','--no-checkout',str(ROOT),str(w)])
run(['git','remote','set-url','origin','https://github.com/'+m['repo']+'.git'],w)
run(['git','fetch','origin','main'],w);run(['git','checkout','-B','main','origin/main'],w)
assert run(['git','rev-parse','HEAD'],w).decode().strip()==head
for e in m['files']:
 dst=w/e['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/e['source'],dst)
run(['git','add','--']+[e['path'] for e in m['files']],w)
changed=run(['git','diff','--cached','--name-only'],w).decode().splitlines();assert set(changed)<=set(e['path'] for e in m['files'])
if changed:
 run(['git','-c','user.name=MIT OCW Notes','-c','user.email=ocw-notes@users.noreply.github.com','commit','-m',sys.argv[2]],w)
 commit=run(['git','rev-parse','HEAD'],w).decode().strip()
 print(run(['git','push','origin','main'],w).decode())
else: commit=head
run(['git','fetch','origin','main'],w)
remote=run(['git','rev-parse','origin/main'],w).decode().strip();assert remote==commit
for e in m['files']:
 b=run(['git','show','origin/main:'+e['path']],w);assert hashlib.sha256(b).hexdigest()==e['sha256'],e['path']
receipt={'status':'PUBLISHED_VERIFIED' if changed else 'NOOP_VERIFIED','commit':commit,'url':'https://github.com/'+m['repo']+'/commit/'+commit,'verified_files':len(m['files']),'changed_files':len(changed),'expected_parent':head,'manifest_sha256':hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest()}
out=Path(sys.argv[1]).with_name(Path(sys.argv[1]).stem.replace('manifest','receipt')+'.json');out.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
