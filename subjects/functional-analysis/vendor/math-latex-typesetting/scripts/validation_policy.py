"""Explicit thresholds and occurrence-specific review notes, never blanket waivers."""
from __future__ import annotations
import json,math
from pathlib import Path
from build_utils import sha256
from tex_project import safe_path

DEFAULTS={'title_soft_limit':20,'inline_warning_ratio':.5,'overflow_tolerance_pt':.5,
          'page_size':[612,792],'reviewed_warnings':[]}

def load_policy(path: Path|None) -> dict:
    result=dict(DEFAULTS)
    if path:
        value=json.loads(path.read_text(encoding='utf-8-sig'))
        if not isinstance(value,dict): raise ValueError('Policy must be a JSON object')
        unknown=set(value)-set(DEFAULTS)
        if unknown: raise ValueError('Unknown policy field(s): '+', '.join(sorted(unknown)))
        result.update(value)
    for key in ('title_soft_limit','inline_warning_ratio','overflow_tolerance_pt'):
        x=result[key]
        if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or x<0:
            raise ValueError('Invalid numeric policy field: '+key)
    if not result['title_soft_limit'] or not 0<result['inline_warning_ratio']<=1:
        raise ValueError('Invalid title/inline diagnostic threshold')
    size=result['page_size']
    if not isinstance(size,list) or len(size)!=2 or any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or x<=0 for x in size):
        raise ValueError('page_size must be two positive finite numbers')
    notes=result['reviewed_warnings']
    if not isinstance(notes,list): raise ValueError('reviewed_warnings must be an array')
    for item in notes:
        if not isinstance(item,dict) or set(item)!={'file','line','kind','sha256','reason'}:
            raise ValueError('Review note needs exactly file, line, kind, sha256, reason')
        if not all(isinstance(item[k],str) and item[k].strip() for k in ('file','kind','sha256','reason')) or not isinstance(item['line'],int) or isinstance(item['line'],bool) or item['line']<1:
            raise ValueError('Invalid review note')
    return result

def annotate_warnings(rows: list[dict],policy: dict,root: Path) -> list[str]:
    messages=[]
    for note in policy['reviewed_warnings']:
        try:
            p=safe_path(root,note['file'])
            if sha256(p)!=note['sha256']: raise ValueError('source hash changed')
        except (OSError,ValueError) as exc:
            messages.append('Unused/stale review note for '+note['file']+': '+str(exc)); continue
        matches=[r for r in rows if r['level']=='WARNING' and all(r.get(k)==note[k] for k in ('file','line','kind'))]
        if not matches: messages.append('No matching warning for review note: '+note['file']); continue
        for r in matches: r['reviewed']=True; r['review_reason']=note['reason']
    return messages
