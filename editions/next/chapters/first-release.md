# Build your first release from supplied data

Your first result will be a directory of inspectable data and a report explaining how it was made. You need Python 3.10 or later, a terminal and the files supplied with this repository. You do not need a GPU, sensors, a model download, an account or a paid service. The model-training choices come after you can reproduce and explain the data.

The task is intentionally small: route fictional helpdesk messages into billing, access or technical categories. A few keyword rules will offer imperfect labels. Some messages make the rules disagree; some trigger no rule; some produce a confident-looking mistake. We keep those outcomes visible. A real support classifier would need a representative, permitted corpus and an independent evaluation far beyond these teaching records.

## Inspect the source before running a pipeline

Open `examples/first-release/data/records.jsonl`. JSONL is one JSON object per line. Each valid row names a record ID, source ID, family ID and text. A family says which examples are related strongly enough that they must remain together for this exercise. The source also includes deliberately malformed lines so that rejection can be tested rather than merely promised.

Open the separate `data/gold.json` only to understand the evaluation contract. It contains authored reference labels. It is not fed to the labeling rules or used to choose the split. In a real project, development labels help you design a rule, while a protected test set is held back for a final comparison. Here the complete public fixture is available for teaching; once you study it, it can no longer serve as unseen evidence about your own improvements.

Read two records with the same underlying message but different whitespace or character form. Should they count as two independent examples? Now look for related records whose text is different. Exact duplication and shared family membership are different relations. The release builder must respect both.

## Run the supplied builder

From the repository root, choose a new empty output path:

```sh
python3 examples/first-release/build.py --out /tmp/dataset-first-release
```

The command does not fetch anything. Its outputs include training records, provenance/lineage, a quarantine, an audit and a manifest. Read the [lab README](../../../examples/first-release/README.md) for the exact filenames and field definitions. Reusing a nonempty output directory is refused so that one experiment cannot silently overwrite another.

The builder performs a sequence of small decisions:

1. Preserve input bytes and their hashes, and parse each line with strict schema checks.
2. Keep invalid records in a quarantine with the raw evidence and rejection reason.
3. Make a documented normalization key and retain original text in lineage.
4. Collapse equal canonical text while preserving every source relationship.
5. Connect duplicates, shared sources and shared families before allocating whole components to train, development and test.
6. Run labeling functions that vote for a category or abstain. Agreement supplies a weak label; conflicts remain unresolved.
7. Compare predictions with the separate authored references and report counts and limitations.
8. Write immutable candidate files and their SHA-256 hashes into a manifest.

A hash identifies bytes; it does not certify that a label is correct or a source is permitted. A successful parse establishes that a record meets the schema; it does not establish that the record belongs in the intended application. The pipeline deliberately keeps these judgments separate.

## Read the failures as carefully as the successes

A rule that sees “password” may vote for access. If another rule sees “error,” the two may disagree. That conflict is different from an all-abstain message, for which no rule supplied evidence. Neither should be filled with an arbitrary class merely to obtain a complete column.

If several rules agree because they share the same dictionary, their agreement is not independent confirmation. If a duplicate group has inconsistent authored reference labels, there is no single trustworthy gold target for its accuracy calculation until someone resolves the disagreement. Count and exclude that ambiguity explicitly instead of choosing whichever label makes the rule look better.

The current executed fixture results are recorded in the lab evidence and [validation record](../validation.md). These measurements describe this exact fixture and recipe. They are not estimates of support-ticket accuracy in production and are not results from a trained model. Keep that sentence next to any number you copy into a report.

## Check the emitted bytes

Run the automated tests:

```sh
python3 -m unittest discover -s tests -p 'test_first_release.py' -v
```

Then build into a second empty directory and compare output hashes. Equal input bytes, recipe and runtime behavior should produce the same candidate. Reordering the input can change its byte hash and line-level provenance while leaving canonical examples and split allocation unchanged; those are different reproducibility claims. Read the tests to see which claim each assertion makes.

Inspect one training row and follow it back through lineage to all original source records. Check that its protected component occurs in exactly one split. Look at achieved component counts, not just nominal percentages. Splitting a large family to make a ratio look tidy would break the evaluation claim.

Finally, identify a quarantined row, an abstention, a conflict and a wrong weak label. Explain which would need a schema repair, a better rule, a new task definition or a human decision. This is the first practical success: you can account for the examples you made, including where their labels remain unreliable.

## What to try next

Choose one change using development material. Write its purpose before changing the program, and keep the previous candidate. Compare acceptance, error and coverage rather than celebrating a larger output count. Do not use the public fixture's final test results to tune repeatedly and then report the test as untouched.

After this chapter, follow the common spine on training claims, permissions, extraction, independence and measurement. Then choose a project track. Numeric examples can lead to a linear model, images to a small classifier or segmenter, and text to a simple bag-of-words baseline. The data contract determines what those models will actually learn. The separate training book covers fitting and inference; this book remains responsible for making the input evidence understandable and testable.
