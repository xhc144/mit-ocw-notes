from pathlib import Path
import urllib.request, re, html, hashlib,json,fitz,zipfile,io
root=Path(__file__).resolve().parents[3]; out=root/'sources/abstract-algebra'; records=[]
base='https://ocw.mit.edu'
courses=[('18-703-modern-algebra-spring-2013','lecture-notes','18.703'),('res-18-011-algebra-i-student-notes-fall-2021','student-notes','RES.18-011'),('res-18-012-algebra-ii-student-notes-spring-2022','student-notes','RES.18-012')]
def links_from(h):
    s=h.decode('utf-8') if isinstance(h,bytes) else h
    return [(html.unescape(a), html.unescape(re.sub('<[^>]+>', '',t))) for a,t in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>',s,re.S)]
def download(url,path):
    data=urllib.request.urlopen(url,timeout=90).read();path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);return data
for slug,page,code in courses:
    course=f'{base}/courses/{slug}/'; pageurl=course+f'pages/{page}/'
    download(course,out/'html'/f'{code}-course.html')
    h=download(pageurl,out/'html'/f'{code}-index.html')
    links=[]
    for href,title in links_from(h):
        selected=('/resources/' in href and (code=='18.703' or any(k in href for k in ['full_lec','lec_w_img'])))
        if selected:
            url=base+href if href.startswith('/') else href
            if url not in [x[0] for x in links]:links.append((url,title))
    if code!='18.703':links=links[:2]
    print(code,len(links),flush=True)
    for i,(res,title) in enumerate(links,1):
        rh=download(res,out/'html'/f'{code}-{i:02}.html')
        candidates=[href for href,title in links_from(rh) if href.split('?')[0].endswith(('.pdf','.zip'))]
        url=candidates[0];url=base+url if url.startswith('/') else url
        ext=Path(url).suffix;filename=f'{code}-{i:02}{ext}'; path=out/('pdf' if ext=='.pdf' else 'tex')/filename
        data=download(url,path);text='';pages=None
        if ext=='.pdf':
            doc=fitz.open(stream=data,filetype='pdf');pages=len(doc);text='\n\f\n'.join(p.get_text() for p in doc)
            (out/'text'/f'{code}-{i:02}.txt').write_text(text)
            print(filename,pages,text[:150].replace('\n',' '),flush=True)
        else:
            z=zipfile.ZipFile(io.BytesIO(data)); names=z.namelist()
            texts=[(n,z.read(n).decode('utf-8',errors='replace')) for n in names if n.endswith(('.tex','.txt','.md'))]
            text='\n'.join(n+'\n'+t for n,t in texts)
            (out/'text'/f'{code}-{i:02}-zip.txt').write_text(text)
            print(filename,len(names),'members',flush=True)
        rights=[l.strip() for l in text.splitlines() if any(k in l.lower() for k in ['copyright','courtesy','permission','rights reserved','©','creativecommons','notetaker','typed by','lecturer','author'])]
        records.append(dict(id=f'{code}-{i:02}',course=code,title=title,resource_url=res,url=url,path=str(path.relative_to(root)),pages=pages,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),rights_hits=rights[:100],role='primary' if code=='18.703' else 'student supplement; not faculty checked',license='CC BY-NC-SA 4.0 default, subject to item exceptions',review_status='pending manual review'))
download(base+'/pages/privacy-and-terms-of-use/',out/'html'/'terms.html')
(out/'source-manifest.json').write_text(json.dumps({'access_date':'2026-10-08','files':records},ensure_ascii=False,indent=2))
