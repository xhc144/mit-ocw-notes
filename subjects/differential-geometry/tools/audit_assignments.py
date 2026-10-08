#!/usr/bin/env python3
"""Check frozen official inventory against manuscript structure, not mathematics."""
import argparse
import hashlib
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    inv_path = ROOT / 'assignment-inventory.json'
    inv = json.loads(inv_path.read_text())
    errors, rows, found = [], [], []
    for h in inv['homeworks']:
        path = ROOT / 'chapters' / f"ps{h['homework']:02}.tex"
        source = path.read_text()
        matches = list(re.finditer(r'\\begin\{exercise\}.*?\\label\{ps:(\d+)-(\d+)\}', source, re.S))
        expected = [p['id'] for p in h['problems']]
        actual = [f'PS{m[1]}.{m[2]}' for m in matches]
        if actual != expected:
            errors.append(f'{path.name}: expected {expected}, found {actual}')
        found += actual
        for j, m in enumerate(matches):
            pid = actual[j]
            block = source[m.start():matches[j+1].start() if j+1 < len(matches) else len(source)]
            problem = next(p for p in h['problems'] if p['id'] == pid)
            solutions = re.findall(r'\\begin\{solution\}(.*?)\\end\{solution\}', block, re.S)
            expected_solutions = 0 if pid == 'PS9.4' else 1
            if len(solutions) != expected_solutions:
                errors.append(f'{pid}: expected {expected_solutions} solution blocks, found {len(solutions)}')
            if solutions and len(re.sub(r'\\[A-Za-z]+|\W', '', solutions[0])) < 40:
                errors.append(f'{pid}: suspiciously empty solution block')
            status = ('source_statement_unavailable' if pid == 'PS9.4' else
                      'partial_answer_missing_final_reference' if pid == 'PS3.3' else
                      'original_false_statement_analyzed_and_corrected' if pid in {'PS7.2', 'PS10.2'} else
                      'independent_complete_answer')
            rows.append({'id': pid, 'chapter_source': path.relative_to(ROOT).as_posix(),
                         'chapter_sha256': sha(path), 'source_pdf_sha256': h['pdf']['sha256'],
                         'official_points': problem['points_as_printed'],
                         'source_statement_status': problem['statement_status'],
                         'labeled_subparts': problem['labeled_subparts'],
                         'unlabeled_requests_zh': problem['unlabeled_requests_zh'],
                         'answer_disposition': status, 'solution_environment_count': len(solutions)})
    if len(found) != len(set(found)) or len(found) != inv['totals']['top_level_problem_count']:
        errors.append('question labels are duplicated or differ from frozen total')
    result = {'schema_version': 1, 'inventory_sha256': sha(inv_path),
              'top_level_questions': len(rows),
              'explicit_labeled_subparts': sum(len(r['labeled_subparts']) for r in rows),
              'fully_addressed_top_level_questions': sum(r['answer_disposition'] not in
                {'source_statement_unavailable', 'partial_answer_missing_final_reference'} for r in rows),
              'partial_top_level_questions': 1, 'source_statement_unavailable_questions': 1,
              'source_gaps': ['PS3.3: final referenced Proposition 6.3 unavailable',
                              'PS9.4: referenced Lemma 28.3 statement unavailable'],
              'problems': rows, 'errors': errors,
              'structural_status': 'PASS_WITH_DISCLOSED_SOURCE_GAPS' if not errors else 'FAIL',
              'limits': ['Structure and inventory matching only.',
                         'Givens, each subrequest and mathematics are checked in three independent Sol reports.',
                         'False original claims are answered by counterexample and explicitly corrected versions.',
                         '32 top-level questions and 10 labeled subparts are not additive.']}
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'problems'}, ensure_ascii=False))
    raise SystemExit(bool(errors))
if __name__ == '__main__':
    main()
