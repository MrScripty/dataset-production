# A tested educational consumer contract

This standard-library CPU exercise supports exactly `contract.py:load_batch`, version `educational-text-routing-1`. It does not train anything. It does not adapt helpdesk text to the numeric training companion, whose introductory examples generate their own numbers. No GPU, download, credentials, service or package installation is needed.

From the repository root, use new or empty output directories:

```
python3 examples/first-release/build.py --out /tmp/dp-first-release
python3 examples/consumer-contract/contract.py --release /tmp/dp-first-release --out /tmp/dp-consumer
python3 examples/consumer-contract/contract.py --read --out /tmp/dp-consumer
python3 -m unittest discover -s examples/consumer-contract/tests -p 'test_*.py' -v
```

The adapter accepts only the exact first-release canonical schema. It verifies `release.jsonl` against the source manifest, rejects reused canonical IDs, unexpected fields (including gold), bad split names and protected-family crossing, and materializes labeled rows only. Abstentions and conflicts remain in `exclusions.json` with their reasons. Targets remain weak labels; this exercise does not establish their correctness.

Emitted layout: `rows.jsonl`, `schema.json`, `exclusions.json`, `manifest.json`. Every row has exactly `id`, `features`, `target`, `group_id`, `split`. Features have exactly one element, the canonical text, interpreted as a UTF-8 string without tokenization. The unit is recorded literally as `UTF-8 text, no tokenization`. IDs and split fields are provenance/selection fields, not model features. Target encoding is `access:0, billing:1, technical:2`. Splits retain the original train/dev/test assignment and group identity. The manifest pins source release and manifest hashes, emitted hashes and byte counts, adapter/consumer versions and accepted/excluded counts. It intentionally does not recursively hash itself. Hashes are integrity checks, not authentication or permission evidence.

The actual consumer verifies emitted hashes, version, exact schema/feature order/units/target mapping, row types, unique IDs, split/group constraints and counts, then returns the requested split's rows. It rereads files, rather than trusting adapter memory. Tests compare every decoded text and target with its canonical source, test relocation/reproducibility, refuse overwrite, reject corrupt bytes and reject semantic schema changes even when their hashes have been updated. This distinguishes byte integrity from contract compatibility. The consumer has no tokenizer, fitting, model inference, accuracy metric or deployment claim. A future trainer needs a different, declared and tested adapter.

Limits: this in-memory teaching consumer is not a production parser for hostile inputs, a cryptographically authenticated release format or an independently reviewed label audit. It verifies source release bytes only; preserve the complete source release and its gold input separately when reproducing audits.
