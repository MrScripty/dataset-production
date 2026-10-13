#!/usr/bin/env python3
"""A narrow text-routing educational adapter and actual read-only consumer."""
import argparse
import hashlib
import json
from pathlib import Path

VERSION = 'educational-text-routing-1'
LABEL_IDS = {'access': 0, 'billing': 1, 'technical': 2}
SCHEMA = {'version': VERSION, 'features': [{'name': 'text', 'type': 'string', 'unit': 'UTF-8 text, no tokenization'}],
          'target': {'name': 'department', 'type': 'integer', 'labels': LABEL_IDS},
          'splits': ['train', 'dev', 'test'], 'target_status': 'weak, not independently verified'}
FIELDS = {'id', 'features', 'target', 'group_id', 'split'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def strict_load(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key: ' + key)
            result[key] = value
        return result
    def constant(value):
        raise ValueError('nonfinite JSON: ' + value)
    return json.loads(data.decode('utf-8'), object_pairs_hook=pairs, parse_constant=constant)


def rows(data):
    return [strict_load(line) for line in data.splitlines()]


def verify_files(root, manifest):
    for name, receipt in manifest['outputs'].items():
        target = root / name
        if target.is_symlink() or target.resolve().parent != root.resolve():
            raise ValueError('unsafe path: ' + name)
        content = target.read_bytes()
        if digest(content) != receipt['sha256'] or len(content) != receipt['bytes']:
            raise ValueError('hash or byte count mismatch: ' + name)


def materialize(source, out):
    source, out = Path(source), Path(out)
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError('output must be new or empty')
    release_bytes = (source / 'release.jsonl').read_bytes()
    source_manifest_bytes = (source / 'manifest.json').read_bytes()
    source_manifest = strict_load(source_manifest_bytes)
    expected = source_manifest['outputs']['release.jsonl']
    if digest(release_bytes) != expected['sha256'] or len(release_bytes) != expected['bytes']:
        raise ValueError('source release hash mismatch')
    source_rows = rows(release_bytes)
    accepted, excluded, seen, splits = [], [], set(), {}
    required = {'canonical_id', 'text', 'group_id', 'split', 'rule_votes', 'weak_label', 'label_status'}
    for row in source_rows:
        if not isinstance(row, dict) or set(row) != required:
            raise ValueError('unsupported canonical schema, including any gold fields')
        for field in ('canonical_id', 'text', 'group_id'):
            if not isinstance(row[field], str) or not row[field]:
                raise ValueError('empty or nonstring ' + field)
        if row['canonical_id'] in seen:
            raise ValueError('duplicate canonical ID')
        seen.add(row['canonical_id'])
        split = row['split']
        if split not in SCHEMA['splits']:
            raise ValueError('unsupported split')
        if row['group_id'] in splits and splits[row['group_id']] != split:
            raise ValueError('protected group crosses splits')
        splits[row['group_id']] = split
        if row['label_status'] in ('abstain', 'conflict'):
            if row['weak_label'] is not None:
                raise ValueError('unresolved row has a target')
            excluded.append({'id': row['canonical_id'], 'reason': row['label_status']})
            continue
        if row['label_status'] != 'labeled' or row['weak_label'] not in LABEL_IDS:
            raise ValueError('unsupported label/status')
        accepted.append({'id': row['canonical_id'], 'features': [row['text']],
                         'target': LABEL_IDS[row['weak_label']], 'group_id': row['group_id'], 'split': split})
    accepted.sort(key=lambda row: row['id'])
    payload = b''.join((json.dumps(row, sort_keys=True, ensure_ascii=False) + '\n').encode() for row in accepted)
    outputs = {'rows.jsonl': payload, 'schema.json': encode(SCHEMA), 'exclusions.json': encode(excluded)}
    manifest = {'adapter': VERSION, 'consumer': VERSION, 'source_manifest_sha256': digest(source_manifest_bytes),
                'source_release_sha256': digest(release_bytes), 'accepted': len(accepted), 'excluded': len(excluded),
                'outputs': {name: {'sha256': digest(content), 'bytes': len(content)} for name, content in outputs.items()},
                'compatibility': 'Only contract.py load_batch; no Training Your Own Models compatibility'}
    out.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        (out / name).write_bytes(content)
    (out / 'manifest.json').write_bytes(encode(manifest))
    load_batch(out)  # Test the actual consumer against emitted bytes, not in-memory objects.
    return manifest


def load_batch(root, split=None):
    root = Path(root)
    manifest = strict_load((root / 'manifest.json').read_bytes())
    if manifest.get('adapter') != VERSION or manifest.get('consumer') != VERSION:
        raise ValueError('unsupported version')
    if set(manifest['outputs']) != {'rows.jsonl', 'schema.json', 'exclusions.json'}:
        raise ValueError('unsupported output layout')
    verify_files(root, manifest)
    schema = strict_load((root / 'schema.json').read_bytes())
    if schema != SCHEMA:
        raise ValueError('feature order, units, targets or schema version differ')
    if split is not None and split not in SCHEMA['splits']:
        raise ValueError('unsupported requested split')
    result, seen, groups = [], set(), {}
    for row in rows((root / 'rows.jsonl').read_bytes()):
        if not isinstance(row, dict) or set(row) != FIELDS:
            raise ValueError('consumer row schema mismatch')
        if not isinstance(row['features'], list) or len(row['features']) != 1 or not isinstance(row['features'][0], str) or not row['features'][0]:
            raise ValueError('consumer needs one nonempty text feature')
        if type(row['target']) is not int or row['target'] not in LABEL_IDS.values():
            raise ValueError('target encoding mismatch')
        if any(not isinstance(row[k], str) or not row[k] for k in ('id', 'group_id')) or row['id'] in seen:
            raise ValueError('ID mismatch')
        seen.add(row['id'])
        if row['split'] not in SCHEMA['splits']:
            raise ValueError('split mismatch')
        if row['group_id'] in groups and groups[row['group_id']] != row['split']:
            raise ValueError('group overlap')
        groups[row['group_id']] = row['split']
        if split is None or row['split'] == split:
            result.append(row)
    if len(seen) != manifest['accepted']:
        raise ValueError('accepted count mismatch')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--read', action='store_true')
    args = parser.parse_args()
    if args.read:
        print(json.dumps({'consumer': VERSION, 'rows_read': len(load_batch(args.out))}, sort_keys=True))
    elif args.release:
        print(json.dumps(materialize(args.release, args.out), sort_keys=True))
    else:
        parser.error('--release is required unless --read')

if __name__ == '__main__':
    main()
