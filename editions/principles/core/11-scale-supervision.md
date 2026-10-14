# 11 Scale supervision with honest uncertainty

*Dataset Production · Puma*

## The question: who supplied this answer?

Our helpdesk has more messages than reviewers can label. A producer writes three keyword rules; another proposes accepting every model prediction above 90% confidence. Both can fill a target column cheaply. Neither creates independent truth merely by writing a value.

The principle is **preserve the source and uncertainty of supervision**. A rule vote, a model prediction, an adjudicated reference and a missing target are different observations. The release must keep those distinctions available to construction, audit and consumers.

You enter with a label guide, protected families, an augmentation policy and an audit baseline. You leave able to distinguish abstention, conflict, coverage, reference agreement and calibration, and to propose a controlled supervision comparison. Teacher/student fitting stays in the training companion; the supplied CPU exercise runs rules only.

## Work the rule votes before combining them

A **labeling function** proposes a label or abstains. The first-release builder has three fixed whole-word rules: billing terms such as invoice/refund/charge/payment; access terms such as password/login/locked; failure terms such as crash/crashes/error/frozen.

**Authored examples from the teaching fixture.** A dash means abstention.

| Message | Billing | Access | Failure | Combined decision |
|---|---|---|---|---|
| Please send my invoice. | billing | — | — | billing |
| I was charged twice for renewal. | — | — | — | abstain |
| The login animation crashes. | — | access | technical | conflict |
| The charge indicator stays at zero. | billing | — | — | billing, although its routing reference is technical |

The whole-word `charge` rule does not match `charged`. That is a coverage defect, not an erroneous prediction. In the animation case, two incompatible categories are proposed. That is a conflict, not absence of evidence. In the indicator case, the rule proposes the wrong category because the same word has different meanings.

The transparent combined policy accepts a category when the distinct non-abstaining categories agree; it records conflict when they differ and abstains when none vote. It is not a fitted label model. Copying the billing rule into three separately named functions adds no independent evidence: all copies use the same clue and can make the same error.

## Coverage and agreement have different denominators

**Executed fixture, not generalization evidence.** Running the supplied first-release builder yields 24 canonical examples, of which 14 are labeled, five abstain and five conflict. Aggregate coverage is 14/24 ≈ 58.3%. There are 13 labeled examples with resolved references; ten agree, so reference agreement is 10/13 ≈ 76.9%. One labeled example has conflicting reference annotations and is not scorable. These are descriptive results on an authored collection, not performance on future customer messages.

Coverage asks “on how many eligible examples did this policy provide a target?” Agreement asks “on how many scorable predictions did it match the specified references?” Report the excluded references and nonpredictions beside the metrics. A policy cannot improve its coverage merely by removing abstentions from the eligibility denominator. It cannot claim a population accuracy from agreement on a selected subset without stating what remains unmeasured.

A per-rule vote can be scorable even when the aggregate has a conflict. Accordingly, a per-rule agreement denominator differs from the aggregate denominator. Recompute from the actual audit's documented policies; do not compare percentages that quietly score different sets.

## A model supplies pseudo-labels under a policy

A **pseudo-label** is a model prediction reused as a target. A teacher proposes it; a student learns from selected proposals alongside checked labels. In **self-training**, the student may become the next teacher. **Semi-supervised learning** is the broader use of labeled and unlabeled training examples; self-training is one approach within it.

**Authored score sheet, not model output.** These four rows are a calibration teaching set C. The “reference” column is supplied with the illustration, not independently reviewed experimental evidence.

| Previously unlabeled input | Teacher label | Score | Supplied reference |
|---|---|---:|---|
| Please email my invoice. | billing | 0.97 | billing |
| My account is locked. | access | 0.94 | access |
| The charge indicator stays at zero. | billing | 0.98 | technical |
| Where is the export button? | technical | 0.61 | technical |

At a 0.90 cutoff, three rows are retained and two agree. The most confident retained row is wrong. At 0.95, two remain and only one agrees. At 0.60, all four remain and three agree. Increasing a confidence threshold need not improve observed precision on a small or shifted collection.

A confidence score has an interpretation only under evidence. **Calibration** asks whether predictions assigned similar confidence have similar observed success frequencies in a relevant checked population. A ranking score need not be a probability. Even calibrated average confidence can conceal category-specific or source-specific failures. A tiny score sheet cannot establish calibration; it can only expose why a threshold needs independent justification.

## Keep calibration and final references in different roles

Use checked development or calibration references to design rules, estimate operating points and choose thresholds. Reserve separately governed final audit references A. Once their judgments influence a rule, cutoff, prompt or selection policy, log that exposure and change their status. A renamed row or re-shuffled split does not restore independence.

Final references must not enter pseudo-label construction, source selection or acceptance decisions while serving as untouched confirmation. If no new independent references are available, report development agreement honestly and narrow the claim. That is preferable to disguising adaptive tuning as final evaluation.

For every accepted proposal, preserve input/source revision, teacher/checkpoint or rule version, score, threshold version, predicted label, selection reason, parent family and later review. Retain rejected proposals and abstentions with enough detail to measure who is losing supervision. A class can have high accepted precision while receiving almost no coverage.

A weather report is not a valid helpdesk input just because a three-class model confidently assigns billing. Check unlabeled-pool membership and source permissions before scoring. A teacher trained on a narrow initial pool can be confidently wrong on a new regime. Random exploration and checked slice audits help reveal that problem but do not eliminate it automatically.

## Consistency does not create independent truth

Consistency training encourages compatible predictions on task-valid variants. From Chapter 10, moving a complete square can preserve its category; cropping most of it away may not. A weakly changed image can supply a confident pseudo-label for a more strongly changed version, but both must support that target under the guide.

A repeated teacher mistake is **confirmation bias**: selected predictions become training evidence that makes the same mistaken belief easier to reproduce. Consistency across two invalidly labeled views reinforces the problem. Independence can come from separately acquired observations, a checked specification, qualified review or a different source of evidence. Two prompts, two names or two models do not guarantee it.

## Controlled exercise: audit the operating point

**Evidence labels: authored illustration for the score sheet; executed fixture only when the builder is run.** Units: canonical requests for the rule audit; four supplied examples for threshold arithmetic. Neither denominator estimates generalization.

1. Observe the difference between “charged twice” and “charge indicator.” Identify absence of a vote versus a wrong vote.
2. Calculate retained count, coverage and agreement at thresholds 0.60, 0.90, 0.95 and 0.99. What does agreement mean when nothing is retained?
3. Classify an added copy of the billing rule. Does extra agreement count as an independent reference?
4. Make one controlled proposal: add a reviewed word-form rule or change the cutoff using C. Record what C influenced and reserve A for a final audit.
5. Defend the proposal against a supervised-only baseline, meaning a learner using checked labels without pseudo-label additions. Declare matching of fitting budget, source coverage and evaluation roles. This model comparison is proposed, not executed here.

Optional CPU check, using a fresh output directory:

```
python3 examples/first-release/build.py --out /tmp/dp-weak-run
```

Inspect `rule_votes`, `label_status` and `weak_label` in `release.jsonl`, and recompute the audit's labeled, conflicting, abstained and evaluable counts. This command fits no teacher, student, Snorkel or consistency model. Modifying a rule is development work and changes implementation hashes; preserve the old release and compare the new one explicitly.

## Acceptance check and worked answer

A supervision policy passes its data gate when it names who or what supplied every target, what abstention/conflict mean, which references influenced construction, and which separately governed references support the stated audit. Its threshold report includes coverage, agreement, exclusions and sensitivity by relevant category/source where evidence permits. Missing final references means revise the claimed independence, not fill them with teacher votes.

The score-sheet answers are: 0.60 retains 4/4 and agrees on 3/4; 0.90 retains 3/4 and agrees on 2/3; 0.95 retains 2/4 and agrees on 1/2; 0.99 retains 0/4, so agreement is undefined rather than zero or 100%. The copied rule shares errors. Neither `labeled` status nor high confidence proves correctness. The first-release 14/24 coverage and 10/13 agreement use different denominators for documented reasons.

Reviewer guidance: inspect accepted and rejected proposals, class-specific coverage, unresolved references, off-task inputs and shared teacher ancestry. Ask whether higher agreement came from better targets or excluding harder classes. Reject any claim that rule votes were independently reviewed when the “review” was another keyword match. Accept a small transparent baseline before requiring a complex label model.

## Optional models and primary reading

Ratner et al., [Snorkel: Rapid Training Data Creation with Weak Supervision](https://www.vldb.org/pvldb/vol11/p269-ratner.pdf), models noisy labeling sources and their relationships before training a predictive model. The core lab deliberately uses a simpler fixed voting baseline. A learned label model's assumptions and independence limits still require checked evaluation.

Sohn et al., [FixMatch](https://arxiv.org/abs/2001.07685), combines confidence-selected proposals with weak/strong augmentation in its studied image settings. Oliver et al., [Realistic Evaluation of Deep Semi-Supervised Learning Algorithms](https://arxiv.org/abs/1804.09170), motivates checking unlabeled-pool/task mismatch and realistic comparisons. These papers are optional conceptual extensions, not dependencies or reproduced results.

Later class-specific threshold or calibration methods should be tested against this same accounting. Their names cannot establish a universal safe cutoff. Recheck the operating point after teacher, rubric, domain or augmentation changes. Tool installation and teacher/student optimization are outside this book's core consumer boundary.
