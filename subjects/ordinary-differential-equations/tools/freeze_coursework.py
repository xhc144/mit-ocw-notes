#!/usr/bin/env python3
"""Normalize the reviewed original IDs without treating repeated tasks as new questions."""
import collections
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
registry = {x['id']: x for x in json.loads((root/'source-manifest.json').read_text())['sources']}
groups = ['bank01-03', 'bank04-07', 'ps01-05', 'ps06-09', 'recitations', 'exams']
records, bindings = [], []
all_tex = '\n'.join(p.read_text() for p in (root/'coursework').glob('*.tex'))
labels = re.findall(r'\\label\{([^}]+)\}', all_tex)
assert len(labels) == len(set(labels)), 'Duplicate coursework labels'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def source(sid, pages, expected=None):
    x = registry[sid]
    assert x['archive_allowed'] and x['status'] == 'archived-verified', sid
    assert all(1 <= p <= x['pages'] for p in pages), (sid, pages)
    if expected:
        assert expected == x['sha256'], sid
    return {'id': sid, 'pdf_pages': pages, 'sha256': x['sha256'], 'official_url': x['resource_url']}

def add(group, identifier, label, leaves, src, basis, refs=(), unavailable=(), raw=None):
    if label:
        assert label in labels, label
    assert leaves and len(leaves) == len(set(leaves)), identifier
    rows = []
    for leaf in leaves:
        missing = leaf in unavailable or 'external-textbook-statement-unavailable' in str(basis)
        match = re.search(r'Notes-?([1-7][A-I]-\d+)(?:\.?([a-z].*))?', leaf)
        target = 'cw:bank-'+match.group(1) if match else None
        if target:
            assert target in labels, target
        ep = None
        if missing:
            m = re.search(r'EP-?(\d+\.\d+)[.-](\d+)', leaf)
            assert m, leaf
            ep = 'EP6:'+m.group(1)+':'+m.group(2)
        rows.append({'original_selector': leaf,
            'status': 'external-statement-unavailable' if missing else 'public-bank-reference' if target else 'statement-and-solution-in-Chinese',
            'bank_target': target, 'bank_selector': match.group(2) if match else None,
            'external_locator_key': ep})
    records.append({'group': group, 'original_id': identifier, 'tex_label': label,
        'source': src, 'answer_basis': basis, 'reference_targets': list(refs),
        'leaves': rows, 'original_schema_record': raw})

for group in groups:
    inventory = root/'research'/f'{group}-coverage.json'
    data = json.loads(inventory.read_text())
    tex = root/'coursework'/f'{group}.tex'
    reviewed = root/'review'/f'{group}-independent-review.md'
    text = reviewed.read_text()
    tex_sha = digest(tex)
    assert tex_sha in text, f'Independent review does not bind final source: {group}'
    bindings.append({'group': group, 'tex': str(tex.relative_to(root)), 'tex_sha256': tex_sha,
        'coverage': str(inventory.relative_to(root)), 'coverage_sha256': digest(inventory),
        'independent_review': str(reviewed.relative_to(root)), 'review_sha256': digest(reviewed),
        'mathematical_review': 'independent-second-reader-closed',
        'review_kind': 'Separate AI agent; not external human or MIT approval'})
    if group.startswith('bank'):
        for x in data['problems']:
            pid = x.get('id', x.get('problem_id'))
            add(group, pid, x.get('label', 'cw:bank-'+pid), x['leaf_subparts'],
                source(x.get('source_id', x.get('exercise_source')), x.get('source_pdf_pages', x.get('source_pages'))),
                x['solution_basis'], [x['duplicate_of']] if x.get('duplicate_of') else [], raw=x)
    elif group == 'ps01-05':
        for x in data['entries']:
            m = re.match(r'(PS\d+)-(I|II)-', x['id'])
            parent = m.group(1)+'-'+m.group(2)+'-'+str(x['original_main_number'])
            # Early coverage is leaf-based; the body groups its original tasks.
            candidates = ['cw:'+parent.lower(), 'cw:'+parent.replace('PS','ps')]
            label = next((a for a in candidates if a in labels), None)
            add(group, x['id'], label, x['leaf_subparts'],
                source(x['source_pdf'], x['source_pdf_pages'], x['source_sha256']),
                x['answer_basis'], ([x['bank_target']] if x.get('bank_target') else [])+x.get('duplicates', []), raw=x)
    elif group == 'ps06-09':
        for x in data['problems']:
            add(group, x['id'], x['label'], x['leaf_subparts'],
                source(x['source_id'], x['sourcepages'], x['source_sha']),
                x['answerbasis'], x['duplication_refs'], x['external_statement_unavailable'], raw=x)
    elif group == 'recitations':
        for x in data['entries']:
            add(group, x['id'], x['tex_label'], x['leaf_subparts'],
                source(x['source_id'], x['sourcepages'], x['source_sha256']),
                x['solution_basis'], x['duplicate_refs'], raw=x)
    else:
        for paper in data['papers']:
            for x in paper['problems']:
                add(group, x['id'], x['id'], x['leaf_subparts'],
                    source(paper['source_id'], x['sourcepages'], x['source_sha']),
                    x['answerbasis'], x['duplicate_refs'], raw={'paper': paper['id'], **x})

external = collections.defaultdict(list)
bank_refs = []
for x in records:
    for leaf in x['leaves']:
        if leaf['external_locator_key']:
            external[leaf['external_locator_key']].append({'original_id': x['original_id'], 'selector': leaf['original_selector']})
        if leaf['bank_target']:
            bank_refs.append({'original_id': x['original_id'], **leaf})
assert sum(len(x['leaves']) for x in records) == 1094
assert sum(len(v) for v in external.values()) == 40
summary = {g: {'schema_records': sum(x['group']==g for x in records),
    'terminal_records': sum(len(x['leaves']) for x in records if x['group']==g)} for g in groups}
result = {'schema_version': 2, 'frozen_on': '2026-10-08',
    'scope': 'All publicly supplied 18.03 Spring 2010 course problem statements and task locators',
    'counting_boundary': '1094 terminal records retain group-specific original task conventions; they include repeated bank tasks and 40 unavailable textbook locators. This is not a count of distinct solved questions.',
    'group_counts': summary, 'source_registry': 'source-manifest.json', 'bindings': bindings,
    'external_textbook_reference_records': 40, 'distinct_external_textbook_locators': len(external),
    'external_locator_map': dict(external), 'bank_reference_map': bank_refs,
    'unavailable_recitation_numbers': [6,12,20,26],
    'answer_boundary': '2010 final has no official answer. The linked 2008 practice-final answer is matched by actual conditions, never by filename alone. Missing and erroneous source answers are annotated locally.',
    'records': records}
(root/'research/coursework-coverage.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'group_counts': summary, 'external_records':40, 'distinct_external_locators':len(external), 'bank_reference_records':len(bank_refs)}, ensure_ascii=False))
