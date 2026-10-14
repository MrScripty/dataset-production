# 8 Audit quality and establish a baseline

*Dataset Production · Puma · Part 2: Evidence you can trust*

## A beginner's question: 100% of what?

A report says the test set has 100% accuracy. Another line says it scored four predictions. A third line says there are seven test examples. Which claim does the number support? Without the denominators, exclusions, reference process, and split/exposure record, “100%” can mislead more than it explains.

After chapters 6–7, you can group related examples and distinguish reference states. Here you will reconstruct a descriptive baseline, separate random audit from targeted diagnosis, and explain why many correlated rows do not create precise evidence. You will finish Part 2 with a split rationale and audit report that another person can reconstruct.

## The principle: measure the stated population, not just the convenient subset

An **audit** compares a defined collection or sample with the evidence and protocol needed to judge it. An **estimand** is the exact quantity sought, such as error per canonical row, fraction of families containing any error, or coverage of accepted examples. The word matters less than the discipline: name the unit, population, and denominator before calculating.

Coverage, reference agreement, and generalization are different quantities. Random sampling can estimate population properties under its assumptions. Targeted review can efficiently locate defects. Neither can establish what its evidence does not address. A baseline is useful precisely because its procedure and limitations are explicit enough for a later controlled comparison.

## Worked fixture accounting: reconstruct every denominator

**Executed fixture snapshot, with descriptive arithmetic.** The audit retained at `examples/first-release/expected/audit.json` reports these counts for the authored helpdesk fixture and fixed keyword rules. The source increment and expected-audit hash are recorded in chapter 1. The unit changes between raw records, canonical examples, and protected groups, so each is named.

| Accounting question | Count and unit |
|---|---|
| Arriving input | 30 raw lines |
| Accepted / quarantined | 28 / 2 raw lines |
| Distinct normalized examples | 24 canonical examples |
| Duplicate records collapsed | 4 accepted raw records beyond the canonical count |
| Protected split groups | 21 connected components |
| Labeled / abstained / conflicted proposals | 14 / 5 / 5 canonical examples |
| Resolved / missing / conflicting references | 21 / 2 / 1 canonical examples |
| Scored aggregate predictions | 13 canonical examples |
| Matching / nonmatching scored predictions | 10 / 3 canonical examples |

Check the totals before interpreting percentages: 28 + 2 = 30; 28 − 4 = 24; 14 + 5 + 5 = 24; 21 + 2 + 1 = 24; 10 + 3 = 13. None of these equations equates raw records with independent groups.

The reference/status relationship explains the scoring subset:

| Aggregate proposal status | Resolved reference | Missing reference | Conflicting reference | Total |
|---|---:|---:|---:|---:|
| Labeled | 13 | 0 | 1 | 14 |
| Abstain | 3 | 2 | 0 | 5 |
| Conflict | 5 | 0 | 0 | 5 |
| Total | 21 | 2 | 1 | 24 |

This cross-accounting follows the authored fixture references and the retained audit. r12/r20 are the two missing references and both abstain. The canonical r27/r28 invoice example is labeled but has conflicting references. Thus one of the 14 labels is unscorable, leaving 13. The other eight resolved references have no aggregate prediction: three abstentions and five conflicts. A reference conflict is different from a rule-vote conflict.

Coverage is 14/24 ≈ 58.3%. Aggregate agreement is 10/13 ≈ 76.9%. Nonagreement among scored predictions is 3/13 ≈ 23.1%. Confirmed matching predictions cover 10/24 ≈ 41.7% of all canonical examples, but the remaining examples are not all known errors: some are unpredicted or unresolved. Naming that fraction “overall accuracy” would obscure its meaning.

The baseline is the fixed aggregation of three keyword rules: no votes → abstain; mutually consistent nonabstaining votes → a label; differing categories → conflict and no label. It is not a trained classifier, probabilistic confidence, or learned label model.

### Per-rule and aggregate results have different denominators

The billing rule votes on 9 of 24 examples; 8 votes have resolved references and 4 match. Its coverage is 9/24 = 37.5% and agreement is 4/8 = 50%. The access rule votes on 7/24 and matches 4/7. The failure rule votes on 8/24 and matches 7/8. A rule's individual votes can be scored even when another rule causes aggregate conflict. Therefore per-rule scored counts need not add to the aggregate count, and summing them counts some examples more than once.

The fixture's development and test subsets happen to have agreement 3/3 and 4/4 on scored aggregate predictions. Development contains five canonical examples and four groups; test contains seven canonical examples and five groups. Those 100% conditional fractions omit unpredicted examples, rely on authored references, and are tiny. All three scored aggregate mistakes happen to fall in training under this seed. Moving them around or trying seeds until test looks good would not improve the data; it would select on evaluation exposure.

The mistakes are useful evidence: “charge indicator” is misread as billing; “login button opens a blank page” as access; “help article contains the word invoice” as billing. Their sources and ownership reasons are more informative than a headline fraction. Keep them in the report so a future proposed repair can be tested against its actual mechanism.

## Random audit and targeted diagnosis answer different questions

Maintain two queues with separate sampling records.

A **random audit queue** samples a frozen population with known inclusion probabilities. It can estimate a stated population property if the sample and review process support that inference. Retain population identity/count, selected IDs, sampling procedure/seed, reviewers and guide, outcomes, exclusions, and uncertainty method. A convenient sample of the first six rows is not automatically random.

A **targeted queue** uses suspicious content, disagreements, rare slices, failed checks, or model scores to find defects. Report confirmed issues per reviewed candidate and failure types. Its yield measures that selected queue, not the whole release's error rate. It can miss confident systematic errors and unexplored regions.

**Authored illustration.** From a frozen population of 60 independent one-record families, a genuinely random sample of six has one confirmed error. Its descriptive sample rate is 1/6, very imprecise evidence about that population. A separate suspicious-candidate queue reviews six and finds four errors. Its yield is 4/6. Combining them into 5/12 and calling it a random population rate loses the selection information. Reviewing the four targeted errors can still be valuable for repair.

### Stratified sampling needs population weights

**Authored arithmetic, preserved from the research edition.** A release has 8,000 ordinary examples and 2,000 difficult-condition examples. A probability audit independently samples 200 from each stratum and finds 2 and 12 errors. Here a **stratum** is a defined population subset sampled separately.

Within-stratum error estimates are 2/200 = 1% and 12/200 = 6%. The sample's unweighted error fraction is 14/400 = 3.5%. But difficult examples are 20% of the population and 50% of the audit. The population-weighted estimate is (8,000/10,000) × 1% + (2,000/10,000) × 6% = 2%.

This calculation assumes the declared population counts are correct, selection is random within strata, the review protocol can resolve the relevant target, and the independent unit matches the estimand. If difficult examples are many crops from a few scenes, counting each crop as an independent observation overstates precision. If rights-unknown or unlabeled records are excluded, declare whether the population is all acquired data or only the accepted release.

For optional planning, let w be a stratum's population fraction, p its estimated error fraction, and n its independent audited count. Add w²p(1−p)/n across strata, then take the square root, to obtain an approximate standard error under the simplified independent-binomial model. The example gives about 0.66 percentage points. A rough normal interval would be about 0.7% to 3.3%; two observed errors in the ordinary stratum make that approximation fragile. This is illustrative uncertainty arithmetic, not a prescribed confidence interval for every real audit. Finite-population corrections and an appropriate stratified/group-aware interval may be needed. Expose counts so a reviewer can assess assumptions.

## Uncertainty follows the independent observation unit

An uncertainty interval does not fix a biased sample or unreliable references. Even a perfect calculation can describe the wrong population. With related examples, assess dependence before choosing the calculation.

If the goal is fraction of families with any error, review and score whole sampled families. A four-row family with one error and a one-row family with none give row error 1/5 = 20% but error-containing-family fraction 1/2 = 50%. These estimands ask different questions; neither should be substituted for the other. For row-weighted error when families differ in size, the sampling and weights must recover the row population rather than silently treating all families as equally sized.

When using resampling, sample whole protected components with all their descendants, preserving the declared weighting and design. Do not bootstrap individual frames of the same video and call the result a new-video interval. If components still share seeds or regimes relevant to the claim, the independent unit may be larger. Report uncertainty limits rather than manufacturing a precise effective sample size from row counts.

### No observed errors is not no risk

**Authored probability illustration.** Under n independent Bernoulli observations of a fixed error probability p, the chance of zero observed errors is (1−p)^n. A one-sided 95% upper confidence bound after zero failures solves (1−p)^n = 0.05. With n = 300, p is approximately 0.00994, or 1%. The “rule of three” approximates that upper bound as 3/n.

Here n is the number of independent trials, not arbitrary rows, and p is the population failure probability under the sampling assumptions. The bound does not establish safety of every rare slice or a changed deployment distribution. Three hundred correlated frames are not the required 300 independent trials. To have a 95% chance of seeing at least one error if the true independent rate were 1%, solve 1−0.99^n ≥ 0.95; n = 299 suffices. Detecting an error's existence differs from estimating its rate precisely or meeting a release threshold.

Do not put a deployment confidence interval around this deliberately authored fixture as if it were a random customer sample. Its counts are descriptive; a statistical generalization claim would need additional evidence.

## Controlled exercise: reconstruct an audit and defend a claim

**Evidence status:** descriptive calculation from the retained executed fixture, plus authored sampling illustrations. **Units and denominators:** explicitly stated in each step. No model fitting or new customer study is performed.

1. Rebuild the three count partitions and the status/reference table. Explain why 13 predictions are evaluable rather than 14 or 21.
2. Calculate aggregate coverage/agreement and billing-rule coverage/agreement. Explain why per-rule counts cannot simply be summed.
3. Report the test's 4/4 fraction with its exclusions, group/row counts, and exposure caveat.
4. Compare the random 1/6 and targeted 4/6 queues. Write a permitted conclusion for each.
5. Recompute the weighted stratified example. Name its population and assumptions.
6. Explain how uncertainty changes for eight adjacent frames from each trajectory. Do not invent a confidence interval without a sampling design and independent units.

### Acceptance check

Pass when every numerator can be traced to an outcome and every denominator to a defined eligible set, exclusions are counted, the fixed baseline is specified, and descriptive/targeted/random evidence remain distinct. Reject a generalization claim from exposed fixture data, a pooled random/targeted rate without design correction, or independent-frame uncertainty for related trajectories. Revise undefined zero denominators; use “not estimable,” not a fabricated percent.

### Worked answer and reviewer guidance

The count equations and table above are the worked reconstruction. Aggregate coverage is 14/24 and agreement 10/13; billing coverage is 9/24 and agreement 4/8. Predictions with missing/conflicting references are not scorable, and resolved references without predictions do not enter conditional aggregate agreement. Individual rules can vote on overlapping examples.

A correct test sentence is: “Four aggregate predictions with resolved authored references match in this exposed teaching test; its seven examples form five known groups, and the other three examples have no aggregate prediction. This does not establish real-world or new-family model performance.” Random 1/6 describes a probability sample with large uncertainty; targeted 4/6 describes confirmed-issue yield among selected suspicious candidates. The weighted illustrative population error is 2%, not 3.5%. Eight adjacent frames add within-trajectory observations, not eight independent new trajectories; use trajectory or larger protected units and report design limitations.

The reviewer should ask the learner to explain one denominator without reading the formula. Then deliberately remove a reference or add a conflicting reference and ask which counts change. A good response changes reference/evaluable counts and keeps construction predictions unchanged, because references are evaluation-only.

## Part 2 assessment: split rationale and audit report

Deliver a report with (a) the generalization claim; (b) protected relations, components, and split allocation; (c) canonical/raw/group counts; (d) label/reference states and scoring exclusions; (e) baseline procedure, coverage, agreement, and known errors; (f) sampling/uncertainty plan; and (g) evaluation exposure ledger.

**Worked miniature report.** “This is a teaching-process claim on an authored collection. Shared canonical text, source ID, and family ID are protected and joined transitively. The retained fixture has 21 components allocated 12/4/5 and 24 canonical examples allocated 12/5/7. No known protected edge crosses splits. Twenty-eight raw records are accepted and two lines quarantined. Aggregate labels partition 14/5/5; references partition 21/2/1. One labeled canonical example has conflicting references, leaving 13 scored predictions; 10 match. Fixed keyword aggregation is the baseline. ‘Charge indicator,’ blank login page, and help-article context expose errors. No random deployment audit or population interval is claimed. All public fixture inputs/references have been exposed for teaching. A future new-customer claim requires new independent customer families, supported rights, and independently reviewed references under a frozen protocol.”

**Reviewer gate.** Reconstruct the grouping chain for r01–r02–r03 and verify every protected relationship against emitted assignments if running the lab. Reject any crossing. Require the learner to justify the grouping from the claim, not merely repeat an algorithm name. Check raw/canonical/group distinctions and all exclusions. Missing source, group, or denominator evidence means revise. A numeric pass without a bounded generalization claim does not pass the assessment.

## Optional technical review and primary reading

For the CPU lab, retain `reference/gold.json` with the frozen raw input and manifest so a later reader can reproduce the reference audit. It is evaluation-only: the construction procedure receives no gold; labels, groups, and splits must remain unchanged if references change. Verify that property with the supplied regression tests. Gold references to quarantined/unknown IDs fail rather than quietly vanish. Retaining reference bytes is subject to the source's actual rights and privacy obligations.

A model can nominate likely label problems, but nomination is not adjudication. Confident Learning [R04] uses out-of-sample probabilities and a class-conditional noise framework with explicit assumptions. Family-aware cross-fitting avoids fitting on the same or related record being scored; otherwise memorization can masquerade as reassuring evidence. Low assigned-label probability may reflect a true label error, a rare valid case, shift, missing input evidence, or model inadequacy. Source review decides the next action.

Northcutt, Athalye, and Mueller's benchmark-label study [R05] motivates separately auditing evaluation references. Its nomination can miss errors, and its corrections are imperfect. Its ordinary correction/removal comparisons did not generally reverse rankings; the paper's instability experiment increased the proportion of originally mislabeled cases. Do not inflate a published result into a universal claim. Freeze review criteria and avoid choosing corrections to favor a preferred procedure.

Read [Confident Learning](https://arxiv.org/pdf/1911.00068) [R04] and [Pervasive Label Errors in Test Sets](https://arxiv.org/html/2103.14749v4) [R05] as optional research, not prerequisites for the paper report. You now have enough shared foundations to choose a modality and one controlled improvement in Part 3.
