#!/usr/bin/env python3
"""Physical PDF checks, never keyword-based content censorship."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def audit(path: Path,page_size: tuple[float,float]=(612,792)) -> dict:
    import fitz
    issues=[]; warnings=[]
    with fitz.open(path) as doc:
        if doc.needs_pass or not len(doc): raise ValueError('Encrypted or empty PDF')
        for i,page in enumerate(doc,1):
            if abs(page.rect.width-page_size[0])>1.5 or abs(page.rect.height-page_size[1])>1.5:
                issues.append(f'Page {i}: paper size differs from the selected template ({page_size}).')
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    for span in line.get('spans',[]):
                        r=fitz.Rect(span['bbox'])
                        if r.x0 < -1 or r.y0 < -1 or r.x1 > page.rect.width+1 or r.y1 > page.rect.height+1:
                            issues.append(f'Page {i}: text lies outside physical page: {span["text"][:60]}')
            if 1<i<len(doc):
                boxes=[b for b in page.get_text('blocks') if b[6]==0 and str(b[4]).strip() and 92 <= (b[1]+b[3])/2 <= 737]
                has_art=bool(page.get_images()) or len(page.get_drawings())>1
                if boxes and not has_art and max(b[3] for b in boxes)-min(b[1] for b in boxes)<190:
                    warnings.append(f'Page {i}: sparse text; inspect whether the whitespace is intentional.')
        return {'pages':len(doc),'issues':issues,'warnings':warnings,
                'mathematical_verification':False,'visual_review':'not_performed'}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('pdf',type=Path); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    try: r=audit(a.pdf)
    except (OSError,ValueError,RuntimeError,ImportError) as exc: print('INPUT ERROR:',exc); return 2
    print(json.dumps(r,ensure_ascii=False,indent=2)); return int(bool(r['issues']))
if __name__=='__main__': raise SystemExit(main())
