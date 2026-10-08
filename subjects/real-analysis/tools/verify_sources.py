#!/usr/bin/env python3
"""Verify every explicitly listed archived original; no network mutations."""
from pathlib import Path
import argparse
import hashlib
import json
import fitz

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir',type=Path)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    project=Path(__file__).resolve().parents[1]
    source=args.source_dir or project.parents[1]/'sources/real-analysis'
    if not source.is_dir(): source=project/'sources-original'
    manifest=json.loads((source/'source-manifest.json').read_text())
    results=[]
    for item in manifest['records']:
        path=source/'originals'/item['filename']
        data=path.read_bytes()
        with fitz.open(path) as doc:
            pages=len(doc)
            images=sum(len(page.get_images()) for page in doc)
            text='\n'.join(page.get_text() for page in doc)
        digest=hashlib.sha256(data).hexdigest()
        ok=(len(data)==item['bytes'] and pages==item['pages'] and digest==item['sha256'])
        results.append({'file':item['filename'],'bytes':len(data),'pages':pages,'sha256':digest,
                        'image_objects':images,'text_extracted':bool(text.strip()),'matches_manifest':ok})
    report={'status':'PASS' if all(x['matches_manifest'] for x in results) else 'FAIL',
            'files':len(results),'pages':sum(x['pages'] for x in results),'records':results,
            'rights_review':'This hash/page check does not replace the source readers rights review.'}
    output=args.out or project/'qa/source-integrity.json'
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='records'},ensure_ascii=False))
    if report['status']!='PASS':raise SystemExit(1)

if __name__=='__main__':main()
