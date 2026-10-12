#!/usr/bin/env python3
"""Package all static TeX inputs and standalone build tools; exclude fonts/cache."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    paths=[ROOT/n for n in ['main.tex','course-info.tex','BUILDING.md','LICENSE-NOTICE.md','coverage.json']]
    paths+=sorted((ROOT/'chapters').glob('*.tex'))
    paths+=[ROOT/'tools'/n for n in ['build.py','check_pdf.py','formula_spotchecks.py']]
    members={str(p.relative_to(ROOT)):p.read_bytes()for p in paths}
    members['SOURCE-README.md']=('独立源码：在本目录运行 python tools/build.py --out build，再运行 python tools/check_pdf.py build/main.pdf --out build/pdf-links.json。需要XeLaTeX及BUILDING.md列出的中文宏包和字体。TeX/TikZ输入均在包内；不依赖网络、原英文PDF或其他学科。MIT OCW 8.323 Spring2023与8.324 Fall2010非官方中文重编，CC BY-NC-SA4.0，署名与具体缺口见LICENSE-NOTICE.md和coverage.json。\n').encode()
    out=ROOT/'quantum-field-theory-source.zip'
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
        for name,b in sorted(members.items()):
            i=zipfile.ZipInfo(name,(2026,10,12,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;z.writestr(i,b)
    record={'date':'2026-10-12','zip':out.name,'sha256':sha(out.read_bytes()),'bytes':out.stat().st_size,'members':[{'path':n,'sha256':sha(b),'bytes':len(b)}for n,b in sorted(members.items())],'exclusions':'Fonts, original OCW PDFs, rendering images, build caches and logs; all are absent from the ZIP. Runtime TeX dependencies documented separately.'}
    (ROOT/'qa/source-zip.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n');print(out)
if __name__=='__main__':main()
