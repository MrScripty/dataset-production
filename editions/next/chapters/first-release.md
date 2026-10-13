# Build your first release from supplied data

Imagine a small helpdesk with three queues. Questions about invoices go to **billing**, questions about getting into an account go to **access**, and reports of broken software go to **technical support**. We want a future model to read a message and choose a queue.

Before training that model, we need to decide what examples will teach it. A training example has an **input**, the information the model receives, and a **target**, the answer we want it to learn. For our task, one example could be:

| Input message | Target queue |
| --- | --- |
| Please send my invoice. | billing |

A folder full of messages is only source material. A dataset for this task must connect messages to labels, explain uncertain labels, and keep some examples aside to check what a model has learned. This chapter builds that small data product. You can understand the whole lesson from the examples on this page. Running the supplied program is an optional final step.

## Decide which team should own a request

A label is a decision under a policy, not a fact supplied by a keyword. For this fictional helpdesk, use the following ownership rules:

- **Billing** handles money and billing documents: charges, payments, refunds, invoice amounts and receipt requests.
- **Access** handles getting into an account: credentials, password resets and account locks. An unspecified error during password reset stays with this team.
- **Technical** handles concrete application/interface failures, such as crashes, frozen screens, blank pages and broken links. Reports about help-article content also go here for triage, even if their wording does not yet state a clear fault.

When a message mentions several topics, identify the reported problem. “The invoice link returns an error” reports a broken link, so its supplied reference is technical. “Password reset says error” reports an unsuccessful account-recovery operation without a specific interface fault, so its reference is access. “The login button opens a blank page” names a concrete interface failure and goes to technical. Another organization could choose different owners; its guide and labels should reflect that choice consistently.

These are conventions for an authored fixture, not universal customer-service categories. The deliberately contradictory reference labels discussed below are defects to detect, not additional routing rules.

## Follow one message from source to example

The supplied fictional collection contains these two records:

| Record | Original text |
| --- | --- |
| r01 | `Please send my invoice.` |
| r02 | `  PLEASE\tSEND my invoice.  ` |

Here `\t` represents a tab. For routing a request, those differences in capitalization and spacing should not change the answer. The program makes a comparison form by standardizing the characters, ignoring case and collapsing whitespace. Both become:

```text
please send my invoice.
```

That comparison form is called **normalized text**. Because the normalized texts are exactly equal, the builder emits one example instead of counting the same message twice. This step is **deduplication**: identifying repeated examples and deciding how to represent them.

We still keep both originals. A separate record says that the emitted example came from r01 and r02. That history is **lineage**. It lets us answer “Where did this come from?” later, rather than losing the second source when we remove a duplicate. The normalization chapter will explain why this particular cleanup policy is appropriate for our toy task but unsafe for some other tasks.

Now give the example a label. A simple rule says, “If the message contains the whole word invoice, propose billing.” It produces:

```text
text:         please send my invoice.
weak_label:   billing
label_status: labeled
```

It is a **weak label** because a fallible rule supplied it. Nothing has learned from data yet. The program is preparing examples, not training a classifier.

## Keep the cases the rule cannot explain

Consider three more messages from the same supplied collection:

| Message | What the rules do | What that means |
| --- | --- | --- |
| I was charged twice for renewal. | No vote | The billing rule recognizes `charge`, but not `charged` |
| The login animation crashes. | Access and technical votes disagree | Two rules see different clues |
| The charge indicator stays at zero. | Billing vote | The word `charge` is about a device indicator here; the supplied reference says technical |

The first case is an **abstention**: the rules decline to propose a label. The second is a **conflict**: they propose incompatible labels. The third is a mistake that would look ordinary if we checked only whether a label was present.

We record all three outcomes. Filling every empty label with a guess would make the file look more complete while hiding what we do not know. Deleting every difficult message would make the task easier while shrinking its coverage. Later chapters teach ways to improve these labels and measure the tradeoffs.

To count mistakes, we need answers that do not simply repeat the rules. The supplied `gold.json` file contains separately authored reference labels. “Gold” is a conventional filename, not a promise that the labels are infallible. One duplicate pair deliberately has conflicting reference labels, and two examples have none. The audit reports those limitations instead of forcing an answer. This is authored teaching material, not an independent human annotation study.

## Keep learning examples separate from checking examples

Suppose a student practices one exam question and then receives the same question with different spacing on the exam. A correct answer tells us little about handling a new problem. The same issue affects models.

We therefore divide the examples into three **splits**, or assigned groups:

- **Training:** material a later model may learn from
- **Development:** material used to choose rules or improve the method
- **Test:** material reserved for the final check

Related examples must travel together. In our fixture, r01 and r02 are duplicates. Record r03, “Please email a receipt,” belongs to the same declared family as r02. That connects all three originals, even though r03 has different words. Putting r03 in a test set while its close relatives are used for training would not test a genuinely independent family.

The builder joins these relationships before assigning splits. It does not consult the reference labels to choose where a record goes. The resulting files have 12 training examples, 5 development examples and 7 test examples. These are small teaching sets, not enough evidence to estimate a real helpdesk model's reliability. Because every example and its answers are public in this lesson, they also cease to be an unseen test once you study them.

## What the finished release contains

A **release** is a named, fixed set of files that someone else can inspect or use. Its contents should not silently change while keeping the same identity. Our release contains cleaned examples, the original records, their lineage, rejected records, an audit and a manifest.

The **audit** is a report of what happened. Here are the results actually produced by the supplied builder:

| Question | Measured answer |
| --- | --- |
| How many lines arrived? | 30 |
| How many were valid records? | 28 |
| How many were rejected and kept aside? | 2 |
| How many distinct normalized examples remain? | 24 |
| How many get a weak label? | 14 |
| How many have no vote or conflicting votes? | 5 with no vote; 5 with conflicts |
| How many scored weak labels agree with the reference? | 10 of 13 |

**Coverage and correctness answer different questions.** The rules provide labels for 14 of 24 examples, or about 58.3% coverage. They agree with the usable references on 10 of 13 scored predictions, or about 76.9% agreement. The first denominator asks how much of the collection received a label; the second asks how often a scorable prediction agrees. Neither includes the other by implication.

Why 13 rather than 14 in the last row? One labeled example has conflicting reference labels, so we cannot fairly score it against a single answer. Two other examples have missing reference labels, but both are abstentions here, so neither was among the 14 predictions to begin with. Ten of the remaining thirteen agree. This is about 76.9%, but it describes only the predictions that can be scored in this deliberately tiny fixture. It does not say that 76.9% of all real helpdesk messages will be routed correctly.

The **manifest** describes the files and the recipe that produced them. It records a **hash**, a compact fingerprint of bytes, for each output. If the bytes change, the fingerprint is overwhelmingly likely to change too. A hash helps detect changes; it does not establish correctness, permission or authorship.

The two rejected lines are preserved in **quarantine**, a separate file for investigation. One line is broken JSON; the other lacks a required family ID. They are expected faults in this fixture. The useful result is that the builder finds them and explains the rejection, rather than crashing or silently losing them.

## Optional exercise run the supplied release builder

**What you need.** Python 3.10 or later and this repository's files. If you are reading on GitHub without a local copy, open the [draft branch](https://github.com/MrScripty/dataset-production/tree/edition/beginner-practical-2026-10), select that branch rather than main, and choose Code → Download ZIP. Extract it and open a terminal in the folder containing the top-level README. The data and program are already included. No dataset, model weights, Python package, sensor, account or paid service must be fetched separately.

The program you will run is `examples/first-release/build.py`. It reads the supplied `data/records.jsonl` and `data/gold.json` beside it. JSONL means one JSON record per line; JSON is the key-and-value format used in these files. You do not need to write either file for this exercise.

From the repository root, run:

```sh
python3 examples/first-release/build.py --out run-first-release
python3 -m json.tool run-first-release/audit.json
```

The first command creates a new `run-first-release` directory. The second displays its audit in a readable form. Expect the counts in the table above. Open `quarantine.jsonl` to see the two rejected lines, and `lineage.jsonl` to follow the invoice example back to r01 and r02.

If Python is not found, the runtime is not installed or uses a different command name on your system. If `examples/first-release/build.py` is not found, check that your terminal is in the repository root. If the output directory is nonempty, choose a new name such as `run-first-release-2`; refusal to overwrite an earlier release is intentional. If your counts differ, compare your input files and recipe with the supplied version before interpreting the result as an improvement.

For the automated checks, run:

```sh
python3 -m unittest discover -s tests -p 'test_first_release.py' -v
```

A passing test means the specified behavior passed its checks. It does not turn the weak labels into trusted answers. The [lab README](../../../examples/first-release/README.md) explains each emitted field when you want implementation detail.

**What you have learned.** You can now distinguish source records, training examples, proposed labels and reference labels. You can follow an example's origin, recognize an abstention or conflict, and explain the denominator in an audit. That is enough to begin the shared chapters on defining the task, source permissions and independent evaluation. You do not need to choose a neural network yet.
