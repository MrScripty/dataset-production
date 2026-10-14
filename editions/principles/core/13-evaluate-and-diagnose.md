# 13 Evaluate change and diagnose failure

*Dataset Production · Puma*

## The question: did the change help, and why?

A producer fixes some messages and sees a higher score. Was the gain caused by better labels, extra training, easier evaluation examples, or chance? A headline number cannot answer all those questions.

The principle is **separate measured change, explanation and generalization**. A fair comparison states what changed, what stayed fixed, what population was measured and which results influenced selection. An ablation removes or varies a proposed mechanism to test its explanation. A final evaluation supports only its stated independence and regime.

You enter with an audit baseline and one controlled improvement from Part 3. You leave with an experiment record, failure trace and evaluation-exposure ledger. If no fitting experiment is run, your justified result can still be a corrected data artifact or a narrower claim. This book does not require a model to demonstrate that a parser erased evidence.

## Find the first wrong artifact

**Authored incident illustration, executable toy analogue in Chapter 15.** The source is:

```
<p>Please do <span>not</span> refund this payment.</p>
```

Under refund-action extraction, the intended text preserves `not` and the target is `refund_requested=false`. A faulty parser drops nested text and emits “Please do refund this payment.” A later labeler assigns true. The labeler appears to contradict the source, but it answers the corrupted input consistently. The first incorrect representation is extraction.

Relabeling that emitted text as false while leaving its wording unchanged would create an unsupported input/target pair. The repair starts with the parser, then invalidates or rebuilds descendants: canonical text, labels, derivatives, exports, indexes/embeddings and any consumers whose behavior depends on them. A fitted model does not forget faulty data merely because a dataset pointer changes; model repair/evaluation is a separate task.

Begin diagnosis by decoding what the consumer actually received. For images, overlay emitted geometry on emitted pixels; for audio, inspect the exact segment and timing; for conversations, inspect template tokens and loss masks; for decisions, check option-ID remapping; for retrieval, compare query positives with the emitted corpus. A correct editor preview is not proof of a correct exported batch.

Save a failure record with release/source/example revisions, adapter, model/inference recipe if present, expected target, actual output, metric decision and environment state. Label hypotheses provisionally: target defect, missing evidence, extraction/representation error, unsupported task, uncovered condition, shortcut suspicion, environment mismatch or evaluation defect. Several may contribute. Inspect some randomly selected successes as well: correct answers can rely on accidental shortcuts.

## Work a paired comparison without exaggerating it

**Authored score sheet, no trained model run.** Ten independent fictional request families are evaluated under the same refund-intent task. Four are negated requests; six are ordinary requests. Baseline A gets two of four negated families and four of six ordinary families correct. Candidate B gets four of four negated and four of six ordinary families correct.

A is correct on 6/10, B on 8/10: a 20-percentage-point difference on this sheet. The candidate repairs two baseline errors and introduces no observed regression in the supplied families. The negation slice changes from 2/4 to 4/4; the ordinary slice stays 4/6. Four clean slice examples are enough to describe those examples, not to establish a precise future error rate or zero risk.

Pairing means the comparison uses the same evaluation families for both releases. Preserve individual outcomes, not only totals. If B's eight successes included newly introduced failures offset by fixes, the same headline score would conceal a different release decision. Report regressions on consequential slices even when the average improves.

A controlled model comparison also fixes task, consumer contract, reference policy, fitting implementation, inference configuration and the budget that matters: steps, tokens, examples, wall time or compute. State unavoidable differences. Removing records changes exposure; filling the saved budget with repeats is another intervention. Equal file size alone does not make a comparison fair.

## Test the explanation with a separate intervention

Suppose label review nominates 200 suspect records in a 10,000-example collection. Compare:

1. Baseline unchanged release.
2. Removal of 200 records under a matched random policy.
3. Removal of the 200 nominated records.
4. Correction of only confirmed wrong targets among the nominated records, retaining useful inputs.

This is a **proposed experiment**, not a delivered result. If targeted removal beats baseline but not random removal, the evidence does not establish that nomination located uniquely harmful records. If correction beats both removal variants, keeping inputs with better labels may be preferable. If rare-slice results worsen, acceptance is a tradeoff under the declared quality requirements.

Ablate only what the explanation requires. To test whether preserving nested text matters, compare parsers on a frozen source set with the same label guide and consumer. To test whether more examples matter, compare against a same-budget random addition. To test curriculum order, hold exposures comparable. To test source mixtures, examine interactions: A may help only when B is retained. Individual gains need not sum.

Repeated fitting seeds describe training variability; resampling independent evaluation families describes evaluation-sampling uncertainty. They answer different questions. A frame-level confidence interval treats related frames as independent and can overstate precision. Use the protection unit from Chapter 6 and report how many units remain. If the available sample/budget cannot distinguish a small gain from noise, say the result is inconclusive.

## Slices and regimes bound the claim

A **slice** is a meaningful condition: nested markup, device terminology, overlapping speech, occlusion, long tool traces, source organization or resolution. Declare important slices from intended use before examining outcomes. Add failure-discovered slices as development hypotheses, then confirm them on fresh material if possible.

A camera-associated failure may actually be caused by lighting or class mix. A language-associated failure may come from transcript normalization or vocabulary. Association directs investigation; it does not establish the cause. A challenge set that changes only an irrelevant background can probe a shortcut hypothesis, but its artificially constructed error frequency is not a deployment prevalence estimate.

A **regime holdout** asks about a new condition, such as future time, unseen organization, device or physical boundary setting. A random holdout from known sources answers a different question. If the intended use is new queries over a fixed corpus, say so; do not claim unseen-corpus transfer. If every seed trajectory shares one initial-condition family, many frames do not establish new-regime performance.

Underspecification is a further limit: fitting objectives can permit several predictors with similar ordinary scores but different stress-test behavior. Some failures require a better objective, inference rule, system constraint or specification rather than another data cleanup. Keep alternative explanations visible.

## Keep an exposure ledger

Record evaluation asset ID/hash and protected family, its original role, date/source revision, who or what inspected its results, the decision influenced and its resulting role. Exposure includes using aggregate results to choose a source or threshold, reading individual failures, generating near copies, and selecting a favored seed.

Freeze the pipeline before final evaluation: source rules, transformations, target policy, split map, selected improvement, adapter and fitting/inference recipe when used. Once final results influence a revision, their status changes. Obtain a genuinely new holdout from independent families to support a new final claim. A renamed, shuffled, re-encoded or paraphrased inspected family is not new evidence.

If independent data is unavailable, report the observed development/challenge result and narrow the conclusion. “The corrected parser preserves nested negation on the inspected cases” is useful. “The system is robust to all real requests” is unsupported. Honest limitations preserve the next reader's ability to make a safe decision.

## Controlled exercise: defend one release difference

**Evidence label: authored score sheet; proposed fitting comparison.** Unit: ten independent authored families; denominator: 10 overall, 4 negated, 6 ordinary. Source is this on-page construction, not the helpdesk CPU audit.

1. Observe the source→extraction→label chain and identify the first incorrect artifact.
2. Calculate paired overall and slice results for A/B. List what the sheet cannot establish.
3. Classify the proposed targeted-removal and correction conditions by their mechanism and budget changes.
4. Make one controlled repair, using the supplied recovery parser in Chapter 15 or a paper-visible transform from Chapter 10. Retain the old artifact and record the difference.
5. Defend its claim with an exposure ledger. Explain which inspected cases are now development regression cases and what fresh family evidence would be required for final generalization.

Without model fitting, inspect an emitted record and test its contract/meaning. That is a data repair result. With a later fitting implementation, record every seed/run, exact consumer and reference roles; do not report only the best seed.

## Acceptance check and worked reviewer answer

Pass when the release comparison isolates the stated change as far as the design allows, shows budgets and individual/slice outcomes, traces failures to intermediate artifacts, and states evaluation exposure and remaining uncertainty. Reject a causal conclusion supported only by an average gain, or an independence claim contradicted by the exposure ledger.

The worked source-chain answer is extraction, because the original still contains nested `not`. The paired sheet is 60% versus 80% overall, 50% versus 100% on four negated families, and approximately 66.7% for both on six ordinary families. This supports the supplied descriptive difference; it is not an executed experiment or precise population estimate. After using those failures to select a repair, all ten inspected families belong in the exposure record. New names do not undo that use.

Reviewer guidance: verify reference labels before treating model disagreement as error. Check whether a removed subset changed class balance or effective fitting exposure. Ask what random correction/removal baseline would show. A negative result can still be valuable: the suspected source was not the cause, the gain did not repeat, or current evidence cannot distinguish explanations.

## Optional diagnostic methods and primary reading

Automated slice discovery proposes hypotheses. [Domino](https://arxiv.org/abs/2203.14960v3) [R42] uses embeddings and error information; inspect cluster members/nonmembers and confirm a frozen definition on new evidence. Searching many candidate slices creates selection effects, and an attractive cluster description is not a causal mechanism.

[Dataset Cartography](https://arxiv.org/abs/2009.10795v2) [R43] records target probabilities across training checkpoints. In an authored four-checkpoint example, probabilities 0.1, 0.2, 0.8, 0.9 average 0.5 with substantial variability, while four values of 0.5 average the same with zero variability. The first changes over fitting; the second remains uncertain. Neither pattern alone diagnoses a wrong label. The scoring run has a cost and must be versioned.

[Influence functions](https://proceedings.mlr.press/v70/koh17a.html) [R44] approximate the test-loss effect of a small training weight change near a fitted optimum. They combine test gradient, inverse loss curvature and training-example gradient; upweighting and removal have different signs. Smoothness/convexity assumptions do not automatically hold for a neural learner. [Basu et al.](https://arxiv.org/abs/2006.14651v2) [R45] and [Epifano et al.](https://arxiv.org/abs/2303.12922) [R46] disagree in part about validation/retraining interpretations, so validate against the exact intended intervention. [TracIn](https://papers.neurips.cc/paper/2020/hash/e6385d39ec9394f2f3a354d9d2b88eec-Abstract.html) [R47] uses checkpoint gradient alignment along a training path, a different quantity from leave-one-out retraining. Influence does not establish ownership, consent or memorization. Use scores to nominate review, compare with cheap loss/disagreement/nearest-neighbor baselines, then perform a bounded intervention.

For generalization boundaries, read [WILDS](https://proceedings.mlr.press/v139/koh21a.html) [R48] and [Underspecification](https://jmlr.org/papers/v23/20-1335.html) [R49]. Their concrete shifted/stress evaluations motivate declared regimes rather than a universal robustness claim. Published system cases are optional tracks; project-specific run findings require their own pinned evidence.
