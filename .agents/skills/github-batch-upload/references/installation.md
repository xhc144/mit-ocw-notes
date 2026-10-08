# Installation

Requires Python 3.11+. Download and extract `github-batch-upload.zip`, preserving the complete `github-batch-upload/` folder. This repository is private; download with the user's existing authorized GitHub session or use the delivered Library file.

```bash
python3 github-batch-upload/scripts/install.py --repo /absolute/current-repo
```

PowerShell also supports `python ... --repo C:\path\repo`. Installation uses portable Python filesystem operations; it does not edit account, authentication, security, network, root README or AGENTS settings. It installs exactly one folder under the repo's `.agents/skills`. An identical rerun reports `ALREADY_INSTALLED`. A modified existing package stops rather than discarding edits. Other skills and AGENTS are retained.

The package index `install-manifest.json` verifies every copied file. `dist/` ZIPs and Python caches are not installed. Before intentionally upgrading an existing installation, compare changes; a clean installation carrying its prior package index can be atomically replaced with rollback on copy failure.

The native uploader uses POSIX secure file descriptors/process groups and Git/gh. It is validated on Linux (MIT saved cloud environment), not natively on Windows. Windows can install/read the skill and use a POSIX runtime such as an existing WSL environment, or the authorized connected-app workflow when native execution is unavailable. No claim of universal runtime testing or automatic dependency installation is made.

A repo folder installation is not a personal-skill install. Initializing a personal-skills checkout, publishing a personal skill, restarting agents, or installing in other saved environments are separate operations. Each actual environment must be opened and checked by its operator. Repo commits alone do not prove skill discovery by an already running agent.

Verification after installation (avoid bytecode cache changes):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 .agents/skills/github-batch-upload/scripts/batch_upload.py --help
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s .agents/skills/github-batch-upload/tests -p 'test_*.py' -v
```
