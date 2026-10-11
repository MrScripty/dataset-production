# Write rules and learn from unlabeled examples

Two routes can reduce the number of labels that people must supply. Programmatic rules offer noisy evidence about a label; semi-supervised methods learn from both trusted labels and unlabeled examples. Neither route permits us to spend our final test set while designing the method.

## Begin with rules that can abstain

A labeling function is a small program that returns a proposed label or abstains. For support tickets, one function might vote “billing” when it sees “charged twice”; another might use an account-event record; a third might use a legacy classifier. Abstention matters: a rule that recognizes billing should not silently label every other ticket “technical.”

Snorkel combines overlapping, conflicting labeling-function outputs into probabilistic training labels, then trains a separate predictive model. Its label model and its final classifier have different jobs. Crucially, the original setup still assumes a labeled development set and a blind held-out test set. “No hand-labeled training set” does not mean “no human-checked evidence.” [Snorkel, PVLDB 2017](https://www.vldb.org/pvldb/vol11/p269-ratner.pdf)

Three regexes derived from the same keyword list are not three independent witnesses. Agreement can represent shared mistakes. Coverage also differs from quality: a rule labeling almost everything can be consistently wrong on one subgroup. The original paper examines when majority voting is sufficient and when modeling source dependencies helps; its empirical results do not guarantee recovery from arbitrary, correlated heuristics. [Snorkel](https://www.vldb.org/pvldb/vol11/p269-ratner.pdf)

Audit each function’s coverage, class balance, conflicts, and estimated precision on an independently labeled sample. Record the rule version and upstream model or dictionary. Review cases where all functions agree, as well as disagreements and complete abstentions. Compare majority vote, the label model, and the trained classifier on the same untouched test set. The last comparison establishes whether training generalizes beyond the rules.

## Predictions as targets

Weak supervision supplies imperfect labels from outside rules or sources. Semi-supervised learning uses labeled and unlabeled examples together. In self-training, a teacher predicts labels for unlabeled examples and a student learns from selected predictions; the roles may be successive versions of the same model. Those predictions are pseudo-labels, not verified annotations.

Consistency training asks predictions to agree across suitable versions of an input. FixMatch combines the ideas: predict on a weakly augmented image, retain a sufficiently confident hard pseudo-label, then train on a strongly augmented version. The confidence cutoff controls a quality–quantity trade-off. Its famous small-label image results are benchmark findings, not a promise that the same recipe works for arbitrary text or production traffic. [FixMatch, NeurIPS 2020](https://proceedings.neurips.cc/paper/2020/file/06964dce9addb1c5cb5d6e3d9838f733-Paper.pdf)

A displayed confidence of 0.95 does not establish 95% correctness. Suppose 100 accepted examples contain 15 mistakes: their measured precision is 85%, regardless of the cutoff. In the 2025 CSL segmentation study, correct and incorrect pixels could both occupy high-confidence regions. Its remedy considers more of the probability distribution and contextual supervision; that evidence is specific to semantic segmentation. [When Confidence Fails, v1](https://arxiv.org/html/2509.16704v1)

SEVAL’s June 2026 revision provides a useful update: learn class-specific pseudo-label refinement and thresholds using a held-out portion of labeled training data. Its analysis favors estimating selected-label precision over trusting raw confidence. However, its theoretical criteria use assumptions, including smoothness approximations; the experiments largely target balanced test performance. It is not a universal guarantee under arbitrary domain shift. [SEVAL, v3](https://arxiv.org/html/2407.05370v3)

Audit accepted-label precision and acceptance rate separately for each class, source, and important slice. A rising average can hide a minority class receiving almost no supervision. Sample rejected examples too. Keep the teacher checkpoint, threshold, confidence, and round attached to every pseudo-label. Compare against a well-tuned supervised/transfer baseline and deliberately test out-of-class unlabeled examples: Oliver et al. found that adding mismatched unlabeled classes can degrade SSL performance. [Realistic Evaluation, NeurIPS 2018](https://papers.nips.cc/paper/7585-realistic-evaluation-of-deep-semi-supervised-learning-algorithms.pdf)

## A small experiment before a larger model

Use the first-release fixture to inspect each rule separately. Its consensus is deliberately simple: agreement emits a weak label; conflicting votes and total abstention remain unresolved. This is not the probabilistic label model in Snorkel. Keep the separately authored reference file out of the rule inputs and the exported training features. A student trained on these votes would require an additional experiment; this lab does not claim that it generalizes.

For a later self-training experiment, first freeze source families and splits. Reserve labeled training data for fitting, a separate labeled development portion for threshold selection, and a final untouched evaluation. Treat the unlabeled pool as training-only material. Train a supervised baseline, save its checkpoint, generate pseudo-labels, and retain teacher version, round, score and selection reason. Compare the next model with the baseline at a stated data/compute budget. Report both acceptance rate and independently audited accepted-label precision. A second round is a new selection intervention, not an automatic improvement.

Deliberately add a small out-of-task challenge pool. If a billing/technical classifier confidently labels a weather forecast, its confidence is not proof the forecast belongs in either class. Quarantine unfamiliar sources until the task and label space apply. Review class coverage after every round, including accepted labels from classes the teacher rarely predicts. Do not balance classes by overwriting unfamiliar cases with desired labels.

**Try it.** Explain why an all-abstain row is different from a conflict. Identify two correlated rules. Write one new rule using only development material, record the examples that motivated it, and leave the disclosed final fixture audit out of tuning. For a real experiment, obtain a new unseen test set once the supplied test examples have become familiar.
