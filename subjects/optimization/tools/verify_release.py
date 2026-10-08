"""Verify an exact remote commit's artifact bytes against the local release manifest."""
from pathlib import Path
from urllib.request import urlopen,Request
import json, hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
def sha(data): return hashlib.sha256(data).hexdigest()
def main():
    if len(sys.argv)!=2: raise SystemExit('Usage: python tools/verify_release.py COMMIT_SHA')
    commit=sys.argv[1]
    if len(commit)!=40 or any(c not in '0123456789abcdef' for c in commit):raise SystemExit('Exact commit SHA required')
    release=json.loads((ROOT/'release-manifest.json').read_text()); results=[]
    targets=release['artifacts']+[{'path':'release-manifest.json','sha256':sha((ROOT/'release-manifest.json').read_bytes())}]
    for record in targets:
        url=f"https://raw.githubusercontent.com/xhc144/mit-ocw-notes/{commit}/subjects/optimization/{record['path']}"
        with urlopen(Request(url,headers={'User-Agent':'MIT-OCW-notes artifact verifier'}),timeout=90) as r: data=r.read()
        actual=sha(data);match=actual==record['sha256'];results.append({'path':record['path'],'url':url,'bytes':len(data),'sha256':actual,'matches_local':match})
        if not match:raise SystemExit('Remote checksum mismatch: '+record['path'])
    report={'commit':commit,'status':'verified','remote_artifacts':results}
    (ROOT/'review/remote-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
