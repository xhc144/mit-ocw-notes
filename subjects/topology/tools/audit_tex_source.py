#!/usr/bin/env python3
"""Check fixed style, source structure, and literal reference targets without building.

Uses the user's original skill scanner. Mathematical correctness and final PDF
link/page rendering remain separate checks. Dynamic TeX is not interpreted.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import re
import sys

VENDOR = Path(__file__).resolve().parents[1] / 'vendor/math-latex-typesetting/scripts'
sys.path.insert(0, str(VENDOR))
from check_style import check  # noqa: E402
from content_style_lint import lint  # noqa: E402
from tex_project import expand_project  # noqa: E402
from tex_scan import commands, document_body  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('main', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    project = expand_project(args.main)
    style_errors = check(project.text)
    found, metrics = lint(project.text)
    findings = []
    for item in found:
        record = asdict(item)
        record['file'], record['line'] = project.location(item.line)
        findings.append(record)
    body, offset = document_body(project.text)

    def location(position: int) -> dict:
        combined_line = project.text.count('\n', 0, offset + position) + 1
        file, line = project.location(combined_line)
        return {'file': file, 'line': line}

    labels, bibliography, references, citations = {}, {}, [], []
    problems = []
    for _, target, position, _ in commands(body, ('label',)):
        labels.setdefault(target.strip(), []).append(location(position))
    for _, target, position, _ in commands(body, ('bibitem',)):
        bibliography.setdefault(target.strip(), []).append(location(position))
    for command, target, position, _ in commands(body, ('ref', 'eqref', 'pageref', 'autoref', 'cref', 'Cref')):
        for name in target.split(','):
            references.append({'command': command, 'target': name.strip(), **location(position)})
    for match in re.finditer(r'\\hyperref\s*\[([^\]]+)\]', body):
        references.append({'command': 'hyperref', 'target': match.group(1).strip(), **location(match.start())})
    for command, target, position, _ in commands(body, ('cite', 'nocite')):
        for name in target.split(','):
            if command == 'nocite' and name.strip() == '*':
                continue
            citations.append({'command': command, 'target': name.strip(), **location(position)})
    for name, places in labels.items():
        if len(places) > 1:
            problems.append({'kind': 'duplicate_label', 'target': name, 'locations': places})
    for name, places in bibliography.items():
        if len(places) > 1:
            problems.append({'kind': 'duplicate_bibliography_key', 'target': name, 'locations': places})
    for record in references:
        if record['target'] not in labels:
            problems.append({'kind': 'unresolved_literal_reference', **record})
    for record in citations:
        if record['target'] not in bibliography:
            problems.append({'kind': 'unresolved_literal_citation', **record})
    errors = style_errors + [item for item in findings if item['level'] == 'ERROR'] + problems
    report = {
        'source': str(args.main.resolve()),
        'automated_static_status': 'PASS' if not errors else 'FAIL',
        'input_bindings': [
            {'path': str(path.relative_to(project.root)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in project.files
        ],
        'fixed_style_errors': style_errors,
        'layout_findings': findings,
        'layout_metrics': metrics,
        'labels': labels,
        'references': references,
        'bibliography_keys': bibliography,
        'citations': citations,
        'reference_problems': problems,
        'mathematical_verification': False,
        'compile': 'not_requested',
        'pdf_links': 'not_checked_by_source_audit',
        'visual_review': 'not_performed',
        'scope': 'reachable static inputs and literal commands; not a full TeX interpreter',
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({
        'status': report['automated_static_status'], 'inputs': len(project.files),
        'labels': len(labels), 'references': len(references),
        'bibliography_keys': len(bibliography), 'citations': len(citations),
        'errors': len(errors), 'warnings': sum(item['level'] == 'WARNING' for item in findings),
    }, ensure_ascii=False))
    for item in findings:
        print(f"{item['level']} {item['file']}:{item['line']} {item['kind']}: {item['detail']}")
    for item in problems:
        print(json.dumps(item, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
