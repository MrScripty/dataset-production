# 14 Freeze and test what the consumer reads

*Dataset Production · Puma*

## The question: why did a valid file teach the wrong thing?

A file has all expected columns and a loader accepts it. The producer assumes the release is ready. Later, a consumer interprets temperature as Fahrenheit instead of Celsius, swaps two features, or treats target ID 1 as access instead of billing. Valid syntax did not preserve the data contract.

The principle is **test emitted bytes through the actual named consumer**. Reproducibility connects inputs, transformations and outputs. Compatibility connects those outputs to one consumer's interpretation. Hashes detect byte changes; semantic tests detect mismatched meaning. Neither alone establishes rights, target quality or generalization.

You enter with a representation contract, protected splits and a bounded comparison. You leave with a frozen release, declared adapter, consumer test and reproducibility evidence. This is the end of Dataset Production's consumer handoff. Neural architectures and fitting are separate work in *Training Your Own Models*.

## A release and an export are different identities

A working collection changes. A **release** selects exact accepted revisions: source and canonical bytes, labels/ontology, permission basis, family graph, split map, recipe, exclusions and audit evidence. Correcting a label or changing a normalization creates another release; it should not overwrite the old name's bytes.

An **export** materializes one release for a declared consumer. Record adapter version, required fields, transformations, output layout/hashes, target encoding, supported split names, exclusions and consumer/version. Multiple exports may use the same canonical release without becoming competing sources of truth.

A useful release card names purpose, permitted/excluded uses, source composition, real/generated proportions, count of rows and independent families, annotation method, group rationale, evaluation exposure, known weaknesses and exact checks performed. A provenance metadata format can supplement it; it cannot certify quality or replace source-use records.

## Work an exact educational adapter

The supplied helpdesk release contains normalized `text`, canonical/group IDs, split, rule votes, weak label and label status. It is not the numeric input expected by the introductory training companion, which generates its own two-feature or sensor data. Assigning an integer to a department does not turn text into a supported numeric feature array.

Our delivered CPU path instead supports one small, documented consumer: `examples/consumer-contract/contract.py`, function `load_batch`, version `educational-text-routing-1`. This is an actual read-only educational consumer. It reads text and weak department targets; it performs no tokenization, fitting, inference or accuracy evaluation.

The adapter emits four files:

- `rows.jsonl`: accepted records with exactly `id`, `features`, `target`, `group_id`, `split`.
- `schema.json`: exact feature order/type/unit and target encoding.
- `exclusions.json`: canonical IDs omitted because their weak status is abstain or conflict.
- `manifest.json`: adapter/consumer versions, source release/manifest hashes, emitted hashes/byte counts and accepted/excluded counts.

A feature array has exactly one element: canonical text as a UTF-8 string. Its declared unit is `UTF-8 text, no tokenization`. Target IDs are `access=0`, `billing=1`, `technical=2`. Group/split/ID fields are provenance or selection fields, not model features. The adapter retains the source's family and split assignment. Labeled rows are retained; unresolved rows are excluded visibly rather than guessed. The target is still weak supervision, not a newly verified reference.

**Worked example.** A canonical row with text `please send my invoice.`, weak label billing, labeled status and its existing group/train assignment emits the same string in `features[0]`, target 1, and unchanged IDs/split. Decoding 1 as access would violate the exact declared target map even though 1 is a valid integer. Moving the group ID into `features[0]` would be a feature-order/type violation. Including reference gold would violate the canonical input schema and expose an evaluation target as construction data.

## Test two independent kinds of correctness

The adapter first verifies the source `release.jsonl` against its manifest. It accepts only the narrow canonical schema and rejects duplicate canonical IDs, unsupported labels/splits, unresolved rows with filled targets and cross-split protected groups. It writes a new or empty output directory and refuses overwrite.

The actual consumer then rereads emitted files. It verifies their hashes and byte counts, exact version/schema, feature order/unit, integer target encoding, row fields, unique IDs, split names, group isolation and accepted count. It can select one split and returns the decoded rows. Tests compare every text, target and group/split with the source canonical record.

Two failure tests distinguish integrity from meaning. Corrupt a file without changing the hash receipt: integrity fails. Change the schema's unit or target map and update the file's hash: byte integrity passes, but compatibility still fails because the named consumer does not support the new contract. A release needs both gates.

These checks have limits. The consumer cannot decide that a weak billing target should be technical; semantic label audits do that. An unsigned manifest can be replaced alongside files, so hashes do not authenticate authorship. The in-memory reader is not a hostile-input production parser. Its successful batch read is not a training-runtime result. A different consumer requires its own declared adapter and tests.

## Rebuild while retaining audit inputs

The first-release builder preserves original input bytes in `raw/records.jsonl` and, in recipe version 3, exact evaluation-reference bytes in `reference/gold.json`. The gold input is needed to reproduce `audit.json`; it is not included in canonical construction, grouping, splits or rule targets. Retaining an audit JSON without its reference input would leave a reproducibility hole.

Freeze builder bytes, input bytes, seed, rule/normalization/split recipes, Python and Unicode database version, output ordering and serialization policy. The manifest's own hash is excluded from its output map to avoid recursive self-hashing; identify the manifest separately in an external release receipt. Store permission/annotation-guide evidence alongside the manifest because hashes alone cannot represent changed interpretation or allowed use.

On the same relevant environment, identical input bytes and recipe produce identical outputs. Reordered raw input can leave canonical content unchanged while changing raw bytes, line-number provenance and manifest identity. A gold-only change should leave construction unaffected while changing audit/reference evidence. A code change can alter the implementation receipt even when canonical rows happen to remain equal. State which equality you tested.

Archive equality is another contract. Stable JSONL/media hashes do not prove a ZIP archive has identical bytes if timestamps differ. Distinguish identical logical records, identical individual files and identical complete archive. Test the level you promise.

## Controlled exercise: build, export, read and challenge

**Executed authored CPU fixture.** This supplied path needs only Python's standard library, no GPU, external data or service. Use fresh paths; substitute new names if the examples already exist.

```
python3 examples/first-release/build.py --out /tmp/dp-release-a
python3 examples/first-release/build.py --out /tmp/dp-release-b
python3 examples/consumer-contract/contract.py --release /tmp/dp-release-a --out /tmp/dp-export-a
python3 examples/consumer-contract/contract.py --read --out /tmp/dp-export-a
python3 -m unittest discover -s examples/consumer-contract/tests -p 'test_*.py' -v
```

1. Observe: inspect one decoded invoice row and identify its feature, target and provenance fields.
2. Calculate: compare the two releases' file hashes and explain why audit/reference files belong in the retained input set.
3. Run: read the actual export and inspect accepted versus excluded counts. The authored fixture exports 14 labeled rows and excludes ten unresolved rows; this is a selection count, not 14 correct answers.
4. Make one controlled fault: in an expendable copy, alter the schema's target map and update its file hash. The supplied test performs this safely. Confirm the actual consumer rejects the semantic mismatch.
5. Defend: write a compatibility statement naming precisely this consumer/version and limitations. Do not claim numeric companion compatibility.

The suite also tests deterministic export and relocation to another directory, corruption, bad targets, unexpected gold fields, overwrite refusal and duplicate JSON keys. For your own modality, add representative boundary cases from its contract. A consumer assertion on an ordinary row is not enough to cover the full supported domain.

## Acceptance check and worked reviewer answer

Pass the release handoff when another reader can reconstruct accepted source revisions, reproduce the audit from retained input/reference bytes, identify adapter/consumer versions and read the emitted bytes with the actual consumer. Required gates cover schema, feature order, units, target conventions, splits, provenance and exact source/output integrity. Missing execution evidence means revise a supported-compatibility claim.

Worked answer: the invoice text stays the sole feature; target is 1 for billing; IDs and group/split remain metadata. The adapter keeps 14 labeled examples from 24 canonical rows and records ten abstentions/conflicts as exclusions. Its targets remain weak and known imperfect. The reader supports text-routing only. Corrupt bytes fail hash verification; a rehashed incompatible unit/map fails the consumer's schema check. Both failures should prevent handoff. Gold bytes are retained for reference-audit reconstruction while excluded from construction and model features.

Reviewer guidance: inspect actual emitted rows, test a fresh relocated directory, check known errors as well as accepted examples, and distinguish executed CPU data checks from source inspection, GPU/model tests or independently reviewed references. If a package or consumer version changes, rerun its relevant checks before retaining the compatibility claim. Check source permissions even when hashes are stable.

## Optional tools, boundary fixtures and primary reading

For media and structured tasks, keep the inherited release chapter's boundary cases: EXIF rotations, one-pixel edge boxes, crossed polygons, hidden corners, empty masks, mismatched dimensions, 0/1 versus required 0/255 masks, rectangular 90-degree rotations, short/long clips, synthetic-fixture flags, stale/missing media, empty class folders, missing option IDs, prompt-only chats, truncated answers and retrieval positives altered by preprocessing. They are optional consumer-specific tests, not capabilities of the text adapter.

A versioning tool can record dependencies and hashes; an interchange descriptor can make schema/provenance portable. Read the official [DVC lock-file documentation](https://dvc.org/doc/user-guide/project-structure/dvcyaml-files) [legacy R76] and [Croissant format documentation](https://docs.mlcommons.org/croissant/) [R78]. They complement, rather than replace, the tested contract. Avoid installation before a measured workload justifies it.

Exact training-companion contracts remain in the updated appendix: class folders, binary masks and mask-based detection, UTF-8 language data, retrieval corpus/query/pairs, typed option decisions, image-caption metadata, consented aligned ASR and fixed waveforms. They require their actual consumer tests. A schema sketch or repository read is not successful runtime compatibility. The introductory numeric examples generate their own data, and this helpdesk export is not a supported input to them.
