#!/usr/bin/env python3
"""Rehearse restart, compatible rollback, and independent toy backup restore."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil

SOURCE = '<p>Please do <span>not</span> refund this payment.</p>'
EXPECTED_TEXT = 'Please do not refund this payment.'
VERSION = 'toy-refund-consumer-1'


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode('utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


class ParagraphText(HTMLParser):
    def __init__(self, direct_only=False):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.parts = []
        self.direct_only = direct_only
    def handle_starttag(self, tag, attrs):
        if tag == 'p' or self.depth: self.depth += 1
    def handle_endtag(self, tag):
        if self.depth: self.depth -= 1
    def handle_data(self, data):
        if self.depth and (not self.direct_only or self.depth == 1): self.parts.append(data)


def extract(source, parser):
    if parser not in ('all-text-v1', 'direct-text-v2'):
        raise ValueError('unknown parser version')
    p = ParagraphText(parser == 'direct-text-v2')
    p.feed(source)
    return ' '.join(''.join(p.parts).split())


def consume(text, version=VERSION):
    if version != VERSION: raise ValueError('unknown consumer version')
    # Intentionally bounded authored grammar, not a general intent classifier.
    if text == EXPECTED_TEXT: return {'refund_requested': False}
    if text == 'Please do refund this payment.': return {'refund_requested': True}
    raise ValueError('outside toy consumer grammar')


def make_bundle(root, release, parser):
    root.mkdir(parents=True, exist_ok=False)
    text = extract(SOURCE, parser)
    outputs = {'source.html': SOURCE.encode(), 'record.json': encode({'text': text, **consume(text)}),
               'contract.json': encode({'consumer': VERSION, 'parser': parser, 'release': release,
                                         'unit': 'one authored request', 'target': 'refund_requested boolean'})}
    manifest = {'release': release, 'outputs': {name: {'sha256': digest(content), 'bytes': len(content)}
                                               for name, content in outputs.items()},
                'toy': True, 'manifest_self_hash': 'excluded'}
    for name, content in outputs.items(): (root / name).write_bytes(content)
    (root / 'manifest.json').write_bytes(encode(manifest))


def verify_bundle(root, expected_release=None, require_regression=True):
    root = Path(root)
    manifest = json.loads((root / 'manifest.json').read_text())
    if set(manifest['outputs']) != {'source.html', 'record.json', 'contract.json'}:
        raise ValueError('unexpected bundle layout')
    if expected_release is not None and manifest['release'] != expected_release:
        raise ValueError('wrong release')
    for name, receipt in manifest['outputs'].items():
        path = root / name
        if path.is_symlink(): raise ValueError('symlink is not a toy bundle file')
        content = path.read_bytes()
        if digest(content) != receipt['sha256'] or len(content) != receipt['bytes']:
            raise ValueError('hash mismatch: ' + name)
    contract = json.loads((root / 'contract.json').read_text())
    if contract['release'] != manifest['release'] or contract['consumer'] != VERSION:
        raise ValueError('incompatible bundle')
    if contract['unit'] != 'one authored request' or contract['target'] != 'refund_requested boolean':
        raise ValueError('semantic contract mismatch')
    text = extract((root / 'source.html').read_text(), contract['parser'])
    record = json.loads((root / 'record.json').read_text())
    if record != {'text': text, **consume(text, contract['consumer'])}:
        raise ValueError('consumer/record mismatch')
    if require_regression and (text != EXPECTED_TEXT or record['refund_requested'] is not False):
        raise ValueError('nested-negation regression failed')
    return {'release': manifest['release'], 'parser': contract['parser'], 'consumer': contract['consumer'],
            'text': text, 'refund_requested': record['refund_requested'], 'hashes_verified': len(manifest['outputs'])}


def restart_job(work):
    """Resume existing state; a finished job is idempotently left finished."""
    work = Path(work)
    state = json.loads((work / 'job.json').read_text())
    if state['status'] not in ('interrupted', 'complete') or state['job'] != 'toy-build-R2':
        raise ValueError('unsupported checkpoint')
    verify_bundle(work / 'R2', 'R2', require_regression=False)
    was_interrupted = state['status'] == 'interrupted'
    state['status'] = 'complete'
    if was_interrupted: state['resumes'] += 1
    (work / 'job.json').write_bytes(encode(state))
    return state


def select_bundle(work, release):
    if release not in ('R1', 'R2'): raise ValueError('unsupported release')
    result = verify_bundle(Path(work) / release, release)
    # Commit pointer only after compatibility, hashes and behavior have passed.
    (Path(work) / 'active.json').write_bytes(encode({'release': release}))
    return result


def read_active(work):
    active = json.loads((Path(work) / 'active.json').read_text())['release']
    if active not in ('R1', 'R2'): raise ValueError('unsupported active pointer')
    return verify_bundle(Path(work) / active, active)


def backup_bundle(work, backup):
    work, backup = Path(work).resolve(), Path(backup).resolve()
    if work == backup or work in backup.parents or backup in work.parents:
        raise ValueError('backup must be outside the working tree')
    verify_bundle(work / 'R1', 'R1')
    backup.mkdir(parents=True, exist_ok=False)
    shutil.copytree(work / 'R1', backup / 'R1')
    return verify_bundle(backup / 'R1', 'R1')


def restore_bundle(backup, work):
    backup, work = Path(backup), Path(work)
    if work.exists(): raise ValueError('restore destination must be absent')
    verify_bundle(backup / 'R1', 'R1')
    work.mkdir()
    shutil.copytree(backup / 'R1', work / 'R1')
    select_bundle(work, 'R1')
    return read_active(work)


def demo(root):
    root = Path(root)
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        raise ValueError('demo root must be nonexistent or empty')
    root.mkdir(parents=True, exist_ok=True)
    work, backup = root / 'toy-working-files', root / 'independent-toy-backup'
    work.mkdir()
    make_bundle(work / 'R1', 'R1', 'all-text-v1')
    make_bundle(work / 'R2', 'R2', 'direct-text-v2')
    # An incident is simulated by an existing bad active pointer, not by approval of R2.
    (work / 'active.json').write_bytes(encode({'release': 'R2'}))
    (work / 'job.json').write_bytes(encode({'job': 'toy-build-R2', 'status': 'interrupted', 'resumes': 0}))
    restarted = restart_job(work)
    try:
        read_active(work)
    except ValueError as exc:
        restart_regression = str(exc)
    else:
        raise AssertionError('restart incorrectly repaired the semantic defect')
    rolled_back = select_bundle(work, 'R1')
    if read_active(work) != rolled_back: raise AssertionError('rollback pointer did not take effect')
    copied = backup_bundle(work, backup)
    before = {p.name: digest(p.read_bytes()) for p in (work / 'R1').iterdir()}
    # Deliberate loss is confined to files this invocation created in its fresh toy root.
    shutil.rmtree(work)
    if work.exists(): raise AssertionError('toy loss was not complete')
    restored = restore_bundle(backup, work)
    after = {p.name: digest(p.read_bytes()) for p in (work / 'R1').iterdir()}
    if before != after: raise AssertionError('restored bytes differ')
    receipt = {'evidence_label': 'executed authored CPU fixture', 'unit': 'one authored nested-negation request',
               'restart': restarted, 'restart_did_not_repair': restart_regression,
               'rollback': rolled_back, 'independent_backup': copied, 'restore': restored,
               'working_tree_removed_before_restore': True, 'restored_hashes_match': before == after,
               'limits': 'Toy sibling-directory backup only; no model, remote durability, credentials or production recovery guarantee'}
    (root / 'receipt.json').write_bytes(encode(receipt))
    return receipt


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(demo(args.out), sort_keys=True))

if __name__ == '__main__': main()
