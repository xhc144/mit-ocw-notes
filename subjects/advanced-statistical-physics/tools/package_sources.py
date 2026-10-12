#!/usr/bin/env python3
"""Make a source-only ZIP; never include fetched originals, fonts or build output."""
import hashlib,json,pathlib,zipfile
root=pathlib.Path(__file__).resolve().parents[1]
name=root.name+'-source.zip';out=root/name
excluded={'build','renders','release','__pycache__'}
allowed={'.tex','.py','.md','.json','.sha256'}
files=sorted(p for p in root.rglob('*') if p.is_file() and p.suffix in allowed and not excluded.intersection(p.relative_to(root).parts) and p.name not in {'progress.json','remote-validation.json','archive-validation.json'})
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files:
  i=zipfile.ZipInfo(str(pathlib.Path(root.name)/p.relative_to(root)),date_time=(2026,10,12,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;z.writestr(i,p.read_bytes())
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
print(json.dumps({'zip':str(out),'files':len(files),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
