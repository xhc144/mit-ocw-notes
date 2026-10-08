"""Package Chinese editable sources and reproducible experiment dependencies.

The fixed class is embedded in main.tex. English originals remain in repository
sources/; no originals, HTML, extracted text caches, or review reports are copied.
An explicit list prevents post-publication QA/history files from entering the ZIP.
The numerical checker in qa/ is executable experiment code, not a review report.
"""
from pathlib import Path
import hashlib
import zipfile

SUB = Path(__file__).resolve().parents[1]
files = {}
for name in [
    'main.tex', 'build.sh', 'README.md', 'LICENSE.md',
    'source-coverage.json', 'source-manifest.json',
    'experiments/assessment-summation.pdf',
    'experiments/nla_experiments.jl',
    'experiments/assessment_checks.jl',
    'experiments/assessment_checks.py',
    'experiments/julia-results/base-experiments.txt',
    'experiments/julia-results/checks.txt',
    'experiments/julia-results/newton.csv',
    'experiments/julia-results/qr.txt',
    'experiments/julia-results/summation.csv',
    'qa/check_numerical_examples.py',
    'qa/numerical-example-checks.json',
    'qa/assessment-numerical-checks.json',
    'tools/package_source.py',
]:
    if not (SUB / name).is_file():
        raise FileNotFoundError(name)
    files[name] = SUB / name
for folder in ['chapters', 'assessments']:
    for path in (SUB / folder).glob('*.tex'):
        files[str(path.relative_to(SUB))] = path
archive = SUB / 'dist/source.zip'
archive.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for name, path in sorted(files.items()):
        info = zipfile.ZipInfo(name, date_time=(2026, 10, 8, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = (0o100644 << 16)
        z.writestr(info, path.read_bytes())
print(f'{len(files)} files; sha256={hashlib.sha256(archive.read_bytes()).hexdigest()}')
