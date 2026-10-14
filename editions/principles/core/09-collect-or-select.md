# 9 Collect or select the next useful examples

*Dataset Production · Puma*

## The question: would another hundred messages help?

Suppose the release from Chapter 8 already contains many invoice requests, but the baseline still confuses device charging problems with payments. A producer proposes collecting a hundred more invoice messages because they are easy to find. The file becomes larger, yet the observed confusion may remain.

The principle is **acquire evidence for a stated gap**. More rows can repeat the same evidence. A useful next batch adds a missing condition, resolves a consequential uncertainty, or tests an explanation of failure. None of those benefits follows from a row count alone.

You enter this chapter with a source/rights worksheet and a baseline audit. You leave with an acquisition plan, a fair budget comparison, and an honest account of what the acquired examples establish. No fitting implementation is required. If you later test model utility, use the separate training companion and a compatible consumer.

## Work a small acquisition decision

**Authored illustration.** Imagine a pool of 40 independently sourced fictional requests: 30 familiar billing requests, six account requests and four device-indicator requests. The intended population includes all three. The error investigation nominated device terminology, not billing in general, as the gap. Our budget is eight reviewer decisions.

Two policies are proposed before seeing labels:

- A documented random draw selects six familiar billing requests, one account request and one device request.
- A targeted draw selects the four device requests, two account requests and two familiar billing requests, each from a different family.

These are supplied draws, not a claim that a random draw always has this composition. On review, the random batch yields eight resolved targets. In the targeted batch, one device request is outside the supported product and another has insufficient context, so six targets are resolved. One resolved random target and two resolved targeted targets address the nominated device-indicator gap. The targeted batch has greater gap coverage but fewer immediately usable labels.

If each review costs two minutes and pool scoring costs the targeted policy four additional minutes, random acquisition costs 16 minutes and targeted acquisition costs 20. Cost per accepted target is 16/8 = 2 minutes versus 20/6 ≈ 3.33 minutes. Cost per accepted *gap example* is 16/1 = 16 versus 20/2 = 10 minutes. Neither measure proves downstream improvement. They expose the tradeoff we would otherwise hide behind “eight labels each.”

The unresolved device request is evidence that the guide or available source context is inadequate. Counting it as a correct label because a reviewer spent time on it would obscure a bottleneck. The out-of-scope request should be excluded from this task, with its reason retained, rather than force-labeled into one of the three queues.

## Four different ways to change a collection

**Acquisition** obtains new source evidence or new labels. **Review** checks existing labels. **Pruning** excludes retained material from a particular view. **Sampling** changes how often a consumer sees retained material. They have different mechanisms and costs. None requires erasing the canonical source history.

For the indicator failure, acquiring device requests tests a coverage explanation; reviewing existing indicator targets tests a label-error explanation. Pruning all device requests might raise a convenient development score by making the task easier while removing a required population. Sampling existing device requests more often changes exposure without adding independent information. State which intervention you mean.

Start with random or stratified random acquisition as a baseline. Stratification gives known conditions a minimum share. Keep some exploration even in a targeted policy: a selector built from current failures can miss a confidently wrong category it has never recognized. An initial seed collection should cover the task's known categories and source families before trusting model-based acquisition scores.

## Why uncertainty and diversity are signals

A model's **uncertainty** describes its current predictions. Low maximum probability, a small margin between the leading classes, entropy spread over classes, or disagreement among models offer different ways to find hesitation. A tied two-class decision and uncertainty spread over ten classes need not identify the same examples.

Hesitation is not the same as learning value. A permanently unreadable request can remain uncertain after ten labels. A confidently wrong device request can look uninteresting to an uncertainty selector. Disagreement is also conditional on the committee: several models with shared sources and objectives can share the same blind spot.

**Diversity** asks what the batch adds collectively. Eight adjacent frames of one incident may be eight files but one family of evidence. Embeddings can help locate redundancy, yet distance in an embedding space is a measurement chosen by a model. If that space organizes background color rather than the small object that matters, excellent geometric coverage may still miss the decision boundary. Inspect actual selected examples and retain domain-based coverage checks.

A **hard example** is hard for a particular model or objective. High loss can indicate a valuable rare condition, a bad target, an extraction error or an impossible task. Review the failure before increasing its weight. In retrieval, a highly ranked supposed negative may be another valid answer. High similarity does not establish nonrelevance; retain multiple positives and unresolved judgments.

## Mixture weights count something specific

After acquisition, a release says what is available. A mixture says how much of it a fitting process sees. Always name the weighting unit: rows, source families, audio seconds, all tokens, or supervised target tokens.

**Authored illustration.** Source A has 10,000 answers of 20 target tokens; B has 1,000 answers of 400 target tokens. A has ten times as many rows, but B has twice as many target tokens: 200,000 versus 400,000. Equal numbers of A and B rows place 400/(400+20) ≈ 95.2% of supervised tokens in B, if each token receives equal loss weight. Per-example normalization changes that conclusion. Tokenization, packing, truncation and target masks belong in the declared recipe.

Likewise, spending 50 million tokens on a 10-million-token source creates five corpus-equivalent exposures; spending 50 million on a one-million-token source creates fifty. Equal mixture weight does not mean equal unique evidence. Repetition can help fitting, but repeated exposure does not add independent source coverage. Ordering examples in a curriculum also changes a fitting path. To test order itself, hold total exposure as close as feasible; otherwise an apparent curriculum gain may come from changed weights.

## Controlled exercise: spend the same review budget

**Evidence label: authored illustration; proposed utility experiment.** Use the eight-review example above. The unit is an independently sourced request family. These counts are not outputs from the CPU lab.

1. Observe: identify the missing population and why more invoice messages may not address it.
2. Calculate: report resolved targets, accepted gap targets and total minutes for both policies. Keep unresolved and out-of-scope attempts in the denominator of attempted acquisition.
3. Classify: decide whether each alternative is acquisition, review, pruning or sampling.
4. Make one controlled change: propose a stratified-random batch with a device coverage floor. Fix the pool, family rules, annotation guide and budget before drawing it.
5. Defend: describe the evidence needed to accept the batch as useful. If no model runs, make the narrower claim “adds reviewed coverage of the stated condition,” not “improves generalization.”

An optional CPU exercise is to inspect `lineage.jsonl` and `audit.json` from the first-release lab. Count canonical rows and protected groups separately. Do not inject the final gold references into an acquisition rule while continuing to call their audit independent. The fixture cannot estimate the value of a real acquisition policy because its entire tiny population is authored and inspectable.

## Acceptance check and worked answer

Pass the acquisition plan when another reader can reconstruct the candidate pool, permission basis, inclusion policy, protected families, review budget, accepted/rejected/unresolved counts, and the measured gap that motivated it. A reviewer should reject a utility claim supported only by confidence, embedding distance or row count.

The worked arithmetic is random: 8 resolved, 1 gap example, 16 minutes; targeted: 6 resolved, 2 gap examples, 20 minutes. Device-indicator requests are the nominated missing condition. Both batches address it to different degrees. The targeted result supports better measured gap yield in this illustration, with lower total accepted-label yield. It does not demonstrate a learned model's improvement. A model comparison would freeze release differences, fitting budget and development metrics, repeat where feasible, and use a genuinely independent final check as described in Chapter 13.

Reviewer questions include: was the unresolved label quietly counted as accepted? Did source scoring or repeated training consume hidden budget? Did the policy remove a critical rare condition? Does the acquisition estimate describe its selected queue or the deployment population? A targeted queue's error average is not a population risk estimate without a sampling design and appropriate weights.

## Optional methods, tools and primary reading

The shared lesson does not require an active-learning package. Specialist methods refine the signals after the simple experiment is understood:

- Core-set selection covers a chosen representation space using a center-covering objective; its assumptions and distance do not establish all semantic coverage. Read Sener and Savarese, [Active Learning for Convolutional Neural Networks: A Core-Set Approach](https://arxiv.org/abs/1708.00489), sections 4.2–4.4 [legacy R08].
- BADGE combines uncertainty and batch diversity with gradient embeddings based on predicted labels. Those proxy labels are not references. Read Ash et al., [Deep Batch Active Learning by Diverse Uncertain Gradient Lower Bounds](https://arxiv.org/abs/1906.03671), algorithm 1 [R09].
- GraNd/EL2N nomination depends on scoring checkpoint and implementation. Preserve the [corrected Data Diet paper](https://arxiv.org/abs/2107.07075v2) and [Kirsch's reproduction](https://arxiv.org/abs/2303.14753) [R10–R11]; the initialization-time GraNd conclusion was retracted after a software bug. Do not repeat the old conclusion.
- Active testing estimates a fixed model's risk; active learning acquires training supervision. They need different estimators. Read Kossen et al., [Active Testing](https://proceedings.mlr.press/v139/kossen21a.html) [R12].
- DoReMi learns source proportions with a smaller proxy relative to a reference, then resamples data for a larger model. High raw loss and learnable headroom are different. Proxy transfer and its extra fitting cost need validation. Read Xie et al., [DoReMi](https://arxiv.org/abs/2305.10429v4) [R13]. Fitting recipes remain in the companion.
- Data Shapley averages a record's marginal utility over subset/order contexts; it is conditional on learner, metric, population and approximation. Two substitute records can each have zero leave-one-out effect yet share Shapley value equally. Read Ghorbani and Zou, [Data Shapley](https://proceedings.mlr.press/v97/ghorbani19c.html) [R17]. This is not ownership, consent or a price.

For repetition and curriculum assumptions, retain Muennighoff et al., [Scaling Data-Constrained Language Models](https://arxiv.org/abs/2305.16264) [R14], Bengio et al., [Curriculum Learning](https://ronan.collobert.com/pub/2009_curriculum_icml.pdf) [R15], and Hacohen and Weinshall's [curriculum study](https://proceedings.mlr.press/v97/hacohen19a.html) [R16]. Published results stay results of their stated settings; no selector or mixture has been reproduced here.
