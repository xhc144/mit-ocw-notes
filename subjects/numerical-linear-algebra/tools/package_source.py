"""Create the stable, editable source archive; never bundle fonts or held notebooks.

Run within the complete repository after PDF/QA verification. Official assessment
originals appear under originals/assessments in the ZIP; their manifest retains
the repository-relative original paths and source URLs.
"""
from pathlib import Path
import hashlib
import zipfile

SUB = Path(__file__).resolve().parents[1]
REPO = SUB.parents[1]
SOURCE = REPO / 'sources/18.335j-spring-2019/assessments'
files = {}
for name in ['main.tex', 'build.sh', 'README.md', 'LICENSE.md',
             'source-coverage.json', 'source-manifest.json']:
    files[name] = SUB / name
for folder in ['chapters', 'assessments', 'experiments', 'tools', 'qa']:
    for path in (SUB / folder).rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts and path.suffix not in ['.pyc', '.ipynb']:
            files[str(path.relative_to(SUB))] = path
for path in SOURCE.iterdir():
    if path.is_file() and path.suffix in ['.pdf', '.txt', '.json']:
        files['originals/assessments/' + path.name] = path
archive = SUB / 'dist/source.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for name, path in sorted(files.items()):
        info = zipfile.ZipInfo(name, date_time=(2026, 10, 8, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = (0o100644 << 16)
        z.writestr(info, path.read_bytes())
print(f'{len(files)} files; sha256={hashlib.sha256(archive.read_bytes()).hexdigest()}')
