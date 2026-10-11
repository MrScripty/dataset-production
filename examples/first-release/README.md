# First release: a tiny, auditable text dataset

Build a dataset release on an ordinary CPU, with Python 3.10+ and **only the standard library**. No account, download, model, GPU, package installation, sensor, or paid service is involved.

This is a production-*process* exercise, not a production-quality training corpus. You will preserve raw inputs, validate records, inspect quarantine, deduplicate, prevent known grouping leaks, generate imperfect weak labels, evaluate against separately authored reference labels, and hash a reproducible release.

## Run it

From the repository root, using a new output directory:

```sh
python3 -B examples/first-release/build.py --out /tmp/dataset-first-release-v1
python3 -B -m unittest discover -s tests -p 'test_first_release.py' -v
```

The first command prints measured counts. If that output directory already contains anything, choose a new directory. The builder refuses to overwrite it. It can also use an existing **empty** directory. `-B` suppresses Python cache files; it does not change the release.

To inspect the evidence:

```sh
python3 -m json.tool /tmp/dataset-first-release-v1/audit.json
python3 -m json.tool /tmp/dataset-first-release-v1/manifest.json
```

To reproduce with an explicitly recorded seed:

```sh
python3 -B examples/first-release/build.py \
  --records examples/first-release/data/records.jsonl \
  --gold examples/first-release/data/gold.json \
  --seed first-release-v1 \
  --out /tmp/dataset-first-release-v2
```

The default and explicit commands use the same inputs and seed. On the same Python Unicode database version, every output byte, including the manifest, is identical. `--records`, `--gold`, `--seed`, and `--out` are the complete CLI. No network access occurs.

## 1. Acquisition and purpose

`data/records.jsonl` contains fictional, newly authored helpdesk messages. It is the acquisition artifact for this exercise, not a scrape or export from a real helpdesk. There are no people, addresses, credentials, or other personal records in the fixture. `source_id` identifies an authored source artifact; `family_id` identifies related formulations or cases. IDs are **globally scoped**, so reuse deliberately creates a relation.

Each valid record has exactly four fields:

```json
{"id":"r01","source_id":"src-01","family_id":"family-01","text":"Please send my invoice."}
```

The hypothetical task is to route a request to `billing`, `access`, or `technical`. This exercise stops at the dataset release. It does not train or deploy a classifier.

Reference annotations in `data/gold.json` were authored separately from labeling-function outputs. They are an illustrative annotation pass, **not** an independent human annotation study. The deliberately inconsistent `r27`/`r28` pair demonstrates a gold-data defect. `r12` and `r20` are deliberately unannotated. “Gold” names the reference file; it does not promise infallibility.

This repository has no declared license at the time of this lab. Authored fictional data avoids third-party acquisition dependencies, but this README does not grant an open-source or dataset license. Decide and document rights before redistribution or outside use.

## 2. Validate and preserve the original

`build.py` validates UTF-8 JSON Lines. Every valid object must have exactly the four required fields. IDs must contain 1–80 ASCII letters, numbers, periods, underscores, or hyphens, starting with a letter or number. Text must be a string that does not become empty after normalization.

Malformed JSON, blank lines, duplicate JSON keys, nonfinite numbers, unknown/missing fields, invalid IDs, invalid UTF-8, unpaired surrogate characters, and invalid text are quarantined. If an ID appears twice, **all** its occurrences are quarantined; the first row never wins by accident. This fixture intentionally includes two bad lines.

`raw/records.jsonl` is a byte-for-byte copy of the acquisition input. `lineage.jsonl` preserves each accepted record's original text, source/family IDs, original line number, raw-text hash, raw-line hash, and base64-encoded raw line including its line ending. `quarantine.jsonl` preserves bad-line bytes and rejection reasons. Every input line is accounted for.

Quarantine is observable evidence, not permission to ignore a defect. A zero exit code means the build finished, not that a real dataset is safe or good enough to publish. This code is not a personal-data detector or sanitizer. Do not replace the fixture with private messages and assume the outputs are safe to share.

## 3. Normalize and deduplicate

The exact policy is:

1. Apply Unicode NFKC compatibility normalization.
2. Apply Unicode case folding.
3. Apply NFKC again, because case folding can introduce decomposed combining marks.
4. Replace runs of Unicode whitespace with one ASCII space and strip outside whitespace.
5. Keep punctuation, negation, and all other remaining content.

Recipe version 2 records this exact **NFKC → casefold → NFKC** sequence. The final normalization makes case-equivalent Greek combining-mark forms converge and keeps normalization idempotent; for example, capital iota plus combining dialytika-tonos and the corresponding lowercase forms share one canonical text. Without the final NFKC pass, equivalent spellings can get different hashes and leak across splits.

Thus fullwidth letters and case/spacing variants can become equal. This is appropriate for demonstrating a case-insensitive helpdesk routing task; it would lose meaningful distinctions for some code, identifier, transcription, or language tasks. No normalization parameters are learned from any split.

Deduplication uses **exact normalized-text equality**, represented by full SHA-256 canonical IDs. It does not detect paraphrases, semantic similarity, or fuzzy near-duplicates. Only one normalized example is exported per canonical ID. Every originating record remains in lineage, including duplicates with different source or family IDs.

## 4. Group before splitting

The builder first connects raw records when they share **any** of:

- The same canonical text ID
- The same `source_id`
- The same `family_id`

It then takes the transitive connected components of all three relations. For example, `r01` duplicates `r02`, and `r02` shares a family with `r03`; all three must stay together. Another fixture relationship links `r04` and `r05` by source and `r04` and `r06` by duplicate text. Deduplicating first and throwing away the extra IDs would miss those relationships.

Only then are whole components assigned to `train`, `dev`, and `test`. Components are ordered by SHA-256 of the seed, a newline, and their content-derived group ID. The first floor(60%) go to train, the next floor(20%) to dev, and the remainder to test. Train and dev each get at least one component; fewer than three components is a hard error.

These are **group-count proportions**, not guaranteed example-count or class proportions. There is no gold-based stratification. The supplied seed produces 12/4/5 groups and 12/5/7 canonical examples in train/dev/test. Known relations never cross a split. Undeclared relationships and semantic near-duplicates can still leak; family quality remains a human responsibility. A changed dataset can change component ordering and assignments: this is a reproducible release, not an append-stable split service.

## 5. Weak labels with visible failure modes

Three short regex labeling functions are defined in `RULES`:

| Function | Votes for | Whole words |
| --- | --- | --- |
| `billing_terms` | billing | invoice, refund, charge, payment |
| `access_terms` | access | password, login, locked |
| `failure_terms` | technical | crash, crashes, error, frozen |

Each function either votes for its category or abstains (`null`). If every non-abstaining vote agrees, the release records that weak label. No votes means `abstain`; different categories mean `conflict` and no weak label. The aggregation is a transparent fixed rule. It is **not** a learned label model, calibrated probability, or implementation of Snorkel's generative label model.

The rules intentionally miss context:

- “The charge indicator stays at zero.” incorrectly triggers billing.
- “The login button opens a blank page.” incorrectly triggers access.
- “The login animation crashes.” creates a conflict.
- “I was charged twice for renewal.” abstains because `charged` is not `charge`.

Inspect these mistakes before suggesting richer rules. Do not tune rules against the test split. For a real experiment, define annotation guidelines, reserve an independently annotated test set, use development data for revisions, and keep the final test untouched until the evaluation plan is fixed. This tiny authored fixture is too small and too curated to establish generalization.

## 6. Evaluate without leaking gold

Release construction, grouping, split assignment, and predictions happen before `gold.json` is read. The release-construction function cannot accept gold as an argument. Tests change all gold labels and verify that exported examples, predictions, lineage assignments, and splits remain identical.

Evaluation maps raw-record annotations onto canonical examples:

- One consistent reference label becomes that example's reference.
- Missing annotations are allowed and counted explicitly.
- Conflicting reference labels for a duplicate are reported and excluded from accuracy denominators. Neither majority voting nor the weak prediction resolves the disagreement.
- An unknown or quarantined record ID, invalid label, or malformed gold file fails the build before output is written.

Per-rule coverage is `voted_examples / eligible_examples`, measured over all canonical examples. Per-rule accuracy counts only that rule's non-abstaining predictions with resolved gold, even when another rule disagrees. Aggregate weak-label accuracy excludes aggregate abstentions/conflicts and missing/conflicting gold. All accuracy fields include `correct` and `evaluated_predictions`; zero denominators produce `null`, never a fabricated 0% or 100%.

The supplied fixture measures:

| Check | Result |
| --- | --- |
| Input / accepted / quarantined | 30 / 28 / 2 lines |
| Canonical examples / duplicates collapsed | 24 / 4 |
| Leakage groups | 21 |
| Weak labeled / abstain / conflict | 14 / 5 / 5 |
| Resolved / missing / conflicting canonical gold | 21 / 2 / 1 |
| Billing rule coverage; accuracy | 9/24; 4/8 |
| Access rule coverage; accuracy | 7/24; 4/7 |
| Failure rule coverage; accuracy | 8/24; 7/8 |
| Aggregate weak-label accuracy | 10/13, about 76.9% |

The aggregate predicts on only 14/24 examples, and one prediction has conflicting gold. Those denominators matter more than the headline percentage. The tiny dev and test subsets happen to score 3/3 and 4/4; **this is not evidence of a perfect model or successful generalization**. The three observed aggregate mistakes all happen to fall in train under this seed. The full measured snapshot is in [`expected/audit.json`](expected/audit.json).

## 7. Inspect the release contract

The output directory contains:

- `raw/records.jsonl`: original input bytes
- `release.jsonl`: all canonical examples, in canonical-ID order
- `train.jsonl`, `dev.jsonl`, `test.jsonl`: disjoint component-preserving subsets
- `lineage.jsonl`: all accepted originals and their final assignments
- `quarantine.jsonl`: every rejected raw line and reason
- `audit.json`: counts, coverage, accuracy denominators, gold conflicts, mistakes, and split diagnostics
- `manifest.json`: input, implementation, recipe, and output hashes

The canonical release schema is `canonical_id`, `text`, `group_id`, `split`, `rule_votes`, `weak_label`, and `label_status`. **There are no gold labels in any training, development, test, or canonical release row.** Evaluation-only gold appears in the separate audit. If later training a weakly supervised model, use `text` as input, `weak_label` as the noisy target for `label_status == "labeled"`, and keep IDs, votes, split flags, lineage, and audit fields out of model features. Model evaluation needs the separately governed reference annotations, not its own weak targets.

The manifest records the input byte hashes, builder-code hash, seed, normalization, Python Unicode database version, split recipe, regexes, gold policy, serialization policy, and each output's SHA-256 and byte count. It intentionally excludes its own hash to avoid recursive self-hashing. Hashes detect changes; they do not authenticate authorship, prove rights, or establish quality.

There are no timestamps, generated random IDs, or absolute paths in the output contract. An identical recipe and identical input bytes produce identical outputs on the same Unicode database version. Reordering input lines preserves canonical data, votes, component membership, split files, and the audit. It correctly changes the raw-input hash, raw snapshot, line-number provenance, and manifest. Different Python Unicode databases can change normalization behavior; the manifest makes that dependency visible.

## Tests and next decisions

The test suite exercises malformed rows, Unicode normalization, duplicate IDs, full raw preservation, transitive unions, split overlap, conflicting/missing/unknown gold, gold independence, input reordering, reproducibility, exact hashes, measured coverage, nonempty-directory refusal, and the actual CLI.

This in-memory lab does not implement streaming, adversarial file-size limits, cryptographic signatures, immutable remote storage, annotation UI, adjudication workflow, near-duplicate retrieval, class balancing, model training, privacy review, or deployment. Before using the process on real data, choose lawful sources and rights, write annotation guidelines, review quarantine and disagreements, audit distribution and privacy risks, and set explicit release gates appropriate to the intended use.
