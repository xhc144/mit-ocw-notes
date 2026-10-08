#!/usr/bin/env python3
"""Package only the Chinese book's resolved inputs and build dependencies."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys
import zipfile

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=root / 'complex-analysis-source.zip')
args = parser.parse_args()
scripts = root / 'vendor/math-latex-typesetting/scripts'
sys.path.insert(0, str(scripts))
from tex_project import expand_project

# The same resolver as the validator follows every actual nested TeX input.
# This edition has no external image/PDF inputs; do not silently grow its scope.
project = expand_project(root / 'main.tex')
if '\\includegraphics' in project.text or '\\includepdf' in project.text:
    raise SystemExit('External image/PDF dependency requires an explicit packaging review')
selected = {p.relative_to(root).as_posix(): p for p in project.files}

# Follow the validator's local import closure, including optional diagnostics.
# Unrelated skill prose, tests, review snapshots and archive-verification tools
# are not compilation dependencies and remain in the repository.
pending = [scripts / 'validate.py']
visited = set()
while pending:
    path = pending.pop()
    if path in visited:
        continue
    visited.add(path)
    selected[path.relative_to(root).as_posix()] = path
    for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
        if isinstance(node, ast.Import):
            modules = [item.name for item in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules = [node.module]
        else:
            modules = []
        for module in modules:
            dependency = scripts / (module.split('.')[0] + '.py')
            if dependency.is_file():
                pending.append(dependency)

for name in [
    'LICENSE.md', 'SOURCES.md',
    'tools/build.sh', 'tools/bootstrap_tex.py', 'tools/audit_pdf.py',
    'vendor/math-latex-typesetting/SOURCE.json',
    'vendor/math-latex-typesetting/requirements.txt',
    'vendor/math-latex-typesetting/templates/wangzhe_baiti_style.tex',
]:
    selected[name] = root / name
selected['README.md'] = root / 'SOURCE-PACKAGE.md'
members = []
for name, path in sorted(selected.items()):
    if path.is_symlink() or not path.resolve().is_relative_to(root):
        raise SystemExit(f'Non-project file not packaged: {path}')
    members.append((name, path.read_bytes()))
inventory = [{'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for name, data in members]
with zipfile.ZipFile(args.output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    contents = json.dumps({'format': 2, 'scope': 'Chinese compilation inputs only; original OCW archive retained separately in the repository', 'tex_input_files': len(project.files), 'validator_modules': len(visited), 'members': inventory}, ensure_ascii=False, indent=2) + '\n'
    for name, data in members + [('ZIP-CONTENTS.json', contents.encode('utf-8'))]:
        info = zipfile.ZipInfo(name, date_time=(2026,10,8,0,0,0))
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, data)
print(json.dumps({'zip': str(args.output), 'members': len(members)+1, 'bytes': args.output.stat().st_size, 'sha256': hashlib.sha256(args.output.read_bytes()).hexdigest()}))
