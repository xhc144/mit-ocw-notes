#!/usr/bin/env python3
"""Verify locally frozen downloaded files against their recorded SHA-256."""
import hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
    entries=json.loads((ROOT/'sources/manifest.json').read_text())
    issues=[]
    for e in entries:
        p=ROOT/'sources'/e['file']
        if not p.is_file():issues.append({'file':e['file'],'issue':'missing'});continue
        got=hashlib.sha256(p.read_bytes()).hexdigest()
        if got!=e['sha256']:issues.append({'file':e['file'],'issue':'sha256 mismatch','actual':got})
        if p.suffix=='.pdf' and not p.read_bytes().startswith(b'%PDF-'):issues.append({'file':e['file'],'issue':'not a PDF'})
    record={'entries':len(entries),'issues':issues,'status':'PASS' if not issues else 'FAIL','scope':'Recorded local bytes; remote permanent availability and legal interpretation not certified.'}
    (ROOT/'qa/source-integrity.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print(record)
    if issues:raise SystemExit(1)
if __name__=='__main__':main()
