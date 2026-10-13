# Write rules and learn from unlabeled examples

We now know how to define labels and how to change an input without accidentally changing its target. The next problem is cost: what if we have many messages but only a small number of checked labels?

There are two different ways to use that material. We can write rules that propose labels, or we can let an already trained model propose labels for additional examples. Both can reduce repetitive labeling work. Both can also repeat the same mistake thousands of times. This lesson follows a few messages closely enough to see the difference.

## Let a rule vote without pretending it knows everything

A **labeling function** is a small program that proposes a label or declines to answer. Declining is called **abstaining**. The supplied release lab has three functions:

| Function | Clue it recognizes | Proposed label |
| --- | --- | --- |
| Billing rule | Whole words such as invoice, refund, charge or payment | billing |
| Access rule | Whole words password, login or locked | access |
| Failure rule | Whole words crash, crashes, error or frozen | technical |

A whole-word match means `charge` does not match `charged`. These are deliberately simple rules. They do not understand what the message is asking, and they have no learned parameters.

Apply them to four supplied records. A dash means that the function abstains.

| Message | Billing vote | Access vote | Failure vote | Combined result |
| --- | --- | --- | --- | --- |
| Please send my invoice. | billing | — | — | billing |
| I was charged twice for renewal. | — | — | — | abstain |
| The login animation crashes. | — | access | technical | conflict |
| The charge indicator stays at zero. | billing | — | — | billing, but the reference says technical |

The combination rule is intentionally transparent: if all non-abstaining functions agree on a category, use it; if none vote, abstain; if categories disagree, keep a conflict. It does not give a special authority to the first rule or fill unresolved cases with a guess.

The last row explains why a filled label is not necessarily a trustworthy label. The routing policy concerns the reported problem. Here “charge” describes a device indicator, not a payment. A rule has supplied a **weak label**, meaning an uncertain piece of supervision rather than a verified answer.

## Measure reach separately from correctness

A rule can be precise when it fires but cover very few examples, or cover many examples while frequently being wrong. **Coverage** measures how often it offers an answer. Agreement with separately supplied reference labels measures how often a scorable answer matches those references.

In the executed first-release fixture, the combined rules label 14 of 24 distinct examples. Coverage is therefore 14/24, about 58.3%. Only 13 of those predictions can be scored because one has conflicting reference labels; 10 match, giving 10/13 agreement. Five other examples are abstentions and five are conflicts. The rules do not get credit for those unresolved cases.

Suppose we copy the billing keyword list into three functions with different names. Three matching votes would look more impressive, but all three could make the same “charge indicator” mistake. Their errors are **correlated**: they depend on the same clue. Agreement is useful evidence only when we understand how it was produced.

**Programmatic weak supervision** uses such noisy labeling sources systematically. [Snorkel](https://www.vldb.org/pvldb/vol11/p269-ratner.pdf) is a research example that models relationships among labeling functions to produce probabilistic training labels. It then trains a separate predictive model. The supplied lab does not implement that learned label model; it lets you inspect the simpler voting baseline first. Even Snorkel's original setup retains checked development and held-out test data. Automating training-label production does not remove the need for independent checking.

## A model can also propose a label

Now imagine that we trained a small classifier on checked examples. Call that model the **teacher** because it supplies proposed answers to a later learner. A label predicted by a model and reused as a training target is a **pseudo-label**. The later learner is the **student**; it may be a new version of the same model rather than a different architecture.

The following table is an invented teaching example, not output from a model run:

| Previously unlabeled message | Teacher's proposed label | Reported confidence | Manual review for this example |
| --- | --- | --- | --- |
| Please email my invoice. | billing | 0.97 | billing |
| My account is locked. | access | 0.94 | access |
| The charge indicator stays at zero. | billing | 0.98 | technical |
| Where is the export button? | technical | 0.61 | technical |

If we keep only predictions with confidence at least 0.90, we keep the first three. Two of the three agree with the manual review, and the most confident one is wrong. The cutoff selected confident predictions; it did not prove their correctness. The fourth prediction is correct in this illustration but would be rejected by that cutoff.

**Self-training** repeats this process: train a teacher from available labels, propose pseudo-labels, select some, and train a student using the original checked labels plus the selected pseudo-labels. A student can learn beyond individual keyword rules, but it can also reinforce a teacher's error. Save the teacher version and selection decision with each pseudo-label so you can trace that error back.

**Semi-supervised learning** is the broader category of methods that use both labeled and unlabeled training examples. Self-training is one route within it. The unlabeled examples must still fit the task: a weather forecast is not automatically a billing, access or technical request just because a model confidently chooses one of those three labels.

## Consistency adds a second kind of evidence

The augmentation lesson showed a square moved within an image. For a category task, we expect the same answer before and after the move. **Consistency training** encourages a model to produce compatible predictions for such valid variations.

One approach, [FixMatch](https://proceedings.neurips.cc/paper/2020/file/06964dce9addb1c5cb5d6e3d9838f733-Paper.pdf), first predicts a category from a gently changed image. If that prediction meets its confidence criterion, it trains using a more strongly changed version with the proposed category as target. “Weak” and “strong” augmentation describe how much the image is changed here; they do not mean that the resulting label has been independently verified. Both versions must still support the category.

Imagine the teacher calls the complete square a square, then the strong crop removes most of it. Consistency would now encourage agreement across an invalid or ambiguous transformation. We must evaluate the augmentation policy and the pseudo-label policy together. This is why learning the augmentation idea first matters.

## What would a real comparison need?

Keep a supervised baseline: a model trained only on the trusted labels. Compare it with the method that also uses the unlabeled pool, under a stated training budget. Use development labels to choose rules and thresholds; keep final-test labels out of those decisions. Check accepted pseudo-labels and rejected ones by category, so a good overall average does not hide a class receiving almost no supervision.

Research cautions reinforce this plan. [Oliver et al.](https://papers.nips.cc/paper/7585-realistic-evaluation-of-deep-semi-supervised-learning-algorithms.pdf) show problems when unlabeled data do not match the task. A [2025 segmentation study](https://arxiv.org/html/2509.16704v1) examines failures of high-confidence selection. [SEVAL's June 2026 revision](https://arxiv.org/html/2407.05370v3) studies learning refinements and class-specific thresholds from held-out labeled training data. These are methods to investigate after the basic experiment is understood, not dependencies required for this lesson.

## Exercise inspect the votes before changing the method

For the core exercise, nothing runs and nothing must be downloaded. Use the four-row voting table and the invented teacher table above.

1. Explain why an abstention is different from a conflict. Expected answer: one has no proposed category; the other has incompatible proposed categories.
2. Add a fourth rule that copies the billing rule. Explain why its extra agreement supplies no independent evidence.
3. Apply a 0.90 confidence threshold to the teacher table. You should retain three examples, two of which agree with the manual review.
4. Write one question you would ask before trusting the unlabeled pool. For example: do these records actually belong to the three-category helpdesk task?

For an optional code inspection, reuse the supplied first-release builder; it needs no new packages or data. Run `python3 examples/first-release/build.py --out run-weak-labels` from the repository root, then inspect `audit.json` and the `rule_votes` fields in `release.jsonl`. Expect the measured 14/24 coverage and 10/13 agreement described above. Use a fresh output directory. This program executes rule voting only; it does not train a teacher, student, Snorkel model or FixMatch model.

**What you have learned.** You can explain who supplied a label, how it was selected, why it might be wrong, and what independent evidence would be needed to trust it. A larger model or a more elaborate labeling method can now be evaluated against a baseline you understand.
