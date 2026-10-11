#!/usr/bin/env python3
"""Fetch only the already frozen source manifest; never infer a new selection."""
import argparse, concurrent.futures, hashlib, json, pathlib, subprocess
from urllib.request import urlopen
ROOT=pathlib.Path(__file__).resolve().parents[3]
MANIFEST=ROOT/'manifests/waves-and-optics-sources.json'
def collect(item, fetch):
    path=ROOT/item['path']
    if fetch or not path.exists():
        with urlopen(item['pdf_url'],timeout=60) as response:data=response.read()
        if not data.startswith(b'%PDF-'):raise ValueError(item['id']+' is not a PDF')
        digest=hashlib.sha256(data).hexdigest()
        if digest!=item['sha256']:raise ValueError(item['id']+' changed upstream; selection/review must be renewed')
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    data=path.read_bytes()
    assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'],item['id']
    info=subprocess.run(['pdfinfo',str(path)],capture_output=True,text=True,check=True).stdout
    assert f"Pages:           {item['pages']}" in info or int(next(x.split(':')[1] for x in info.splitlines() if x.startswith('Pages:')))==item['pages']
    text=ROOT/item['text_path'];text.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['pdftotext','-layout',str(path),str(text)],check=True)
    return {'id':item['id'],'sha256':item['sha256'],'pages':item['pages']}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--fetch',action='store_true',help='redownload frozen PDFs and require their existing hashes');args=ap.parse_args()
    manifest=json.loads(MANIFEST.read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:verified=list(pool.map(lambda x:collect(x,args.fetch),manifest['resources']))
    print(json.dumps({'verified_pdfs':len(verified),'source_pages':sum(x['pages'] for x in verified)},ensure_ascii=False))
if __name__=='__main__':main()
