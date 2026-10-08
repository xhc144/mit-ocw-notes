#!/usr/bin/env python3
"""Prepare a frozen connector upload plan without Git or network access."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import tempfile
import batch_upload as batch


def prepare(manifest, root, checkpoint, emit_blob=None):
    m = batch.load_manifest(manifest, validate_branch_git=False)
    root = Path(root).resolve(strict=False)
    key = hashlib.sha256((m['repo'].casefold() + '|github.com').encode()).hexdigest()
    lock_root = Path(tempfile.gettempdir()) / ('github-batch-upload-locks-' + str(os.getuid()))
    with batch.process_lock(lock_root, key), batch.process_lock(checkpoint, 'checkpoint.lock'):
        cp = batch.Checkpoint(checkpoint, m, root, None)
        reused = cp.freeze(m, root, 2)
        if emit_blob is not None and not 0 <= emit_blob < len(m['files']):
            raise batch.Stop('INVALID_BLOB_INDEX')
        entries = []
        for index, f in enumerate(m['files']):
            digest = hashlib.sha1(('blob ' + str(f['size']) + '\0').encode())
            with f['snapshot'].open('rb') as stream:
                first = stream.read(1024)
                if first.startswith(b'version https://git-lfs.github.com/spec/v1\n'):
                    raise batch.Stop('LFS_POINTER_INPUT_REQUIRES_SEPARATE_WORKFLOW')
                digest.update(first)
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
            entries.append({'index': index, 'path': f['path'], 'sha256': f['sha256'],
                            'size': f['size'], 'expected_blob_sha': digest.hexdigest(),
                            'snapshot': str(f['snapshot'])})
        plan = {'status': 'FROZEN_PLAN_ONLY', 'manifest_id': cp.digest, 'repo': m['repo'],
                'branch': m['branch'], 'expected_head': m['expected_head'],
                'reused_snapshots': reused, 'entries': entries, 'remote_write_attempted': False,
                'verified_files': 0}
        if emit_blob is not None:
            plan['blob_input'] = {'repository_full_name': m['repo'], 'encoding': 'base64',
                                  'content': base64.b64encode(m['files'][emit_blob]['snapshot'].read_bytes()).decode()}
        cp.save(connector_plan={k: v for k, v in plan.items() if k != 'blob_input'})
        return plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--source-root', required=True, type=Path)
    parser.add_argument('--checkpoint', required=True, type=Path)
    parser.add_argument('--emit-blob', type=int, help='Generate input for one connected create_blob tool, not an upload')
    args = parser.parse_args()
    try:
        print(json.dumps(prepare(args.manifest, args.source_root, args.checkpoint, args.emit_blob), ensure_ascii=False, indent=2))
        return 0
    except batch.Stop as error:
        print(json.dumps({'status': 'STOPPED', 'code': error.code, **error.details}))
        return 2
    except (OSError, ValueError, KeyError, TypeError):
        print(json.dumps({'status': 'STOPPED', 'code': 'LOCAL_INPUT_OR_IO_ERROR'}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
