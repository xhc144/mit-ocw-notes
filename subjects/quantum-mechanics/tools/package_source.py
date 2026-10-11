#!/usr/bin/env python3
"""Package complete standalone XeLaTeX source with deterministic ZIP members."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    paths=[ROOT/'main.tex',ROOT/'course-info.tex',ROOT/'BUILDING.md',ROOT/'LICENSE-NOTICE.md',
           *sorted((ROOT/'chapters').glob('*.tex')),
           *[ROOT/'tools'/n for n in ('build.py','check_pdf.py','assessment_numerics.py','addition_numerics.py')],
           ROOT/'qa/assessment-numerics.json',ROOT/'qa/addition-numerics.json']
    readme="""# 量子力学中文学习册独立源码

所有 TeX 输入、数值图坐标和固定适配类均在本 ZIP 内；字体和 TeX Live 为运行环境依赖。
在本目录执行：

    python tools/build.py --out build
    python tools/check_pdf.py build/main.pdf --out build/pdf-links.json

完整依赖与限制见 BUILDING.md。

本册是 MIT OCW Barton Zwiebach 8.04 Spring 2016、8.05 Fall 2013、8.06 Spring 2018 的非官方中文改编。新增推导与答案为 AI 独立整理，没有取得官方答案。原件另署 Sarah Geller、Andrew Turner 的转录信用在来源附录保留。CC BY-NC-SA 4.0；商业教材未打包，纯教材题号不编造题面。课程入口与逐项资源链接均在 PDF 来源附录。

图文件为自主数值计算生成；普通编译不需要 SciPy 或网络。可选重算图形依赖 NumPy/SciPy，输出的采样不能替代解析证明。
"""
    members={'SOURCE-README.md':readme.encode()}
    members.update({str(p.relative_to(ROOT)):p.read_bytes()for p in paths})
    out=ROOT/'quantum-mechanics-source.zip'
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9)as z:
        for name,b in sorted(members.items()):
            i=zipfile.ZipInfo(name,(2026,10,11,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16
            z.writestr(i,b)
    record={'zip':out.name,'sha256':sha(out.read_bytes()),'bytes':out.stat().st_size,'entries':len(members),
       'members':[{'path':n,'sha256':sha(b),'bytes':len(b)}for n,b in sorted(members.items())],
       'scope':'All manuscript TeX inputs, generated figure coordinates, builder/link checker, numerical generators and receipts. Fonts/TeX Live and archived OCW PDFs are runtime/repository resources, not ZIP dependencies.'}
    (ROOT/'qa/source-zip.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print(out)
if __name__=='__main__':main()
