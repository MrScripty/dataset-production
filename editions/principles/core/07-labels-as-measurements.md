# 7 Treat labels as measurements

*Dataset Production · Puma · Part 2: Evidence you can trust*

## A beginner's question: why do two reasonable labels disagree?

“The invoice link returns an error.” One reviewer chooses billing because the message mentions an invoice. Another chooses technical because the link is broken. Both may be following their instructions faithfully. Taking a majority vote without inspecting the guide can hide the disagreement's cause.

After chapters 2–3 and 6, you have a target, representation, and evaluation boundary. Here you will write a label protocol, distinguish missing and conflicting references, preserve original judgments, and adjudicate an ambiguity with reasons. You need only a few paper messages, not a labeling platform or a learned model.

## The principle: annotation observes a target through a protocol

An **annotation** is an observation or judgment obtained under instructions, evidence, and working conditions. Labels can depend on the guide, context shown, reviewer expertise, interface, time budget, and whether uncertainty is allowed. Record these when they affect meaning. Consistency can indicate a reliable protocol; it does not show that the protocol measures the intended construct or that its judgments are correct.

A **reference label** is the judgment used as comparison evidence under a declared process. It is not automatically truth. A label proposed by a heuristic or model is another kind of judgment. Keep its source and status. A nonempty target cannot stand in for acceptance, and a filename called “gold” cannot stand in for independent review.

## Small worked example: two instructions, two measurements

**Authored illustration.** Compare instruction A, “Route any invoice or refund mention to billing; otherwise any login or password mention to access; otherwise an error/crash report to technical,” with instruction B, the fixture's ownership guide:

- Billing owns money and billing-document requests.
- Access owns account recovery and access problems unless a concrete interface fault is described.
- Technical owns concrete application/interface failures, including broken links, blank pages, and frozen screens. Help-article content is sent here for triage.

The authored answers under those instructions are:

| Message | Instruction A | Instruction B | Reason under B |
|---|---|---|---|
| The invoice link returns an error. | billing | technical | Broken link is the reported fault |
| Password reset says error. | access | access | Unspecified account-recovery failure |
| The login button opens a blank page. | access | technical | Concrete interface fault |
| Please refund this payment. | billing | billing | Money request |

They match on two of four messages. That is 50% agreement between these two authored policies on this constructed selection. It is not a measured human reliability study or a random estimate of customer-label ambiguity. The disagreements reveal a policy difference: topic versus problem ownership. If the project intended B, faithfully following A is still the wrong measurement for this task.

An adjudication for the first message can say: “Under routing guide B v1, the observed problem is a link error, so technical owns it; ‘invoice’ is context. Preserve both original judgments and record that this resolves a guide convention, not a factual dispute about whether the link actually failed.” Without real system evidence, the annotation concerns what the message reports, not an independently verified incident.

## The theory: disagreement has several causes

Do not apply one repair to every disagreement.

1. **Ordinary mistake:** a reviewer missed a word, selected the wrong option, or drew the wrong boundary. Recheck source evidence and correct the judgment.
2. **Missing evidence:** the message omits context, a word is inaudible, or the object is obscured. Preserve uncertainty, obtain evidence if permitted, or narrow the task.
3. **Unclear task definition:** the guide fails to specify ownership, visible versus occluded shape, or relevant transcript conventions. Revise the guide and test fresh judgments.
4. **Legitimate boundary ambiguity:** several categories reasonably fit under the current ontology. Define a convention, allow multiple labels, or retain an unresolved case depending on the task.
5. **Stable perspective difference:** people legitimately prefer different styles or interpretations. A distribution of judgments may represent the target better than forced consensus.

The same raw mismatch could arise from any of these. Written reasons and retained judgments help distinguish them. An adjudication is a new event, not a retroactive rewrite of independent agreement. If reviewers discuss their answers first, their later agreement has a different provenance.

Davani, Díaz, and Prabhakaran [R03] study preserving annotator-specific judgments in subjective language tasks. Their findings support considering disagreement as information, with privacy and sparse-data limits. They do not require every dataset to model each annotator or claim that every disagreement is equally valid.

### Pilot the guide before scaling the labels

A useful **pilot** is a small trial designed to expose the protocol's weaknesses. Include ordinary cases, boundary cases, known counterexamples, and inputs with insufficient evidence. Ask reviewers to give reasons for some choices and record needed context or controls. Maximizing quick agreement is not the purpose.

Specify the annotation unit, label definitions, hierarchical or multi-label rules, coordinate/time conventions, normalization, permitted external evidence, uncertainty states, and escalation path. Distinguish directly observed fields from policy judgments. In a tool trace, the API response is an observation; “the best next action” is a judgment under a task. For masks, the guide must state whether only visible regions count. For transcription, punctuation and normalization policy can alter literal match without altering spoken meaning.

Use specialist review where judgment depends on domain knowledge, language, subtle sound, or fine-grained taxonomy. A generalist can flag uncertainty without guessing. Reviewer quality should not be measured only by conformity to a majority; a careful dissenter may expose the guide's systematic error.

After a guide change, repeat independent labeling on fresh material under the new version. Reusing adjudicated examples is useful for teaching but cannot measure unprompted agreement on new cases. Keep any final evaluation reference process separate from construction and calibration choices.

### Missing, conflicting, and resolved references are different states

A canonical example has a **resolved reference** when its available applicable judgments consistently identify one answer or an adjudication resolves them under a documented protocol. **Missing reference** means no applicable judgment is available. **Conflicting reference** means available judgments disagree and no resolution has been accepted.

The fixture maps separately authored raw-record labels to canonical examples. r01 and r02 agree on billing, so their canonical reference is resolved. r27 and r28 normalize to the same message but their authored references disagree, billing versus technical. The audit records the conflict and excludes it from single-answer scoring. r12 and r20 lack reference labels, so their canonical references are missing. It does not infer their answers from weak votes.

The executed snapshot has 21 resolved, 2 missing, and 1 conflicting canonical reference, totaling 24 examples. Those counts describe a teaching annotation pass, not independently reviewed truth. A duplicate family's conflict could result from an annotation mistake or unsafe normalization; investigate both source and protocol before choosing a remedy. For the authored r27/r28 example, the conflict is deliberate teaching material.

Three valid outcomes are an adjudicated single target under an operational convention, a distribution/multi-label target where the task permits it, or an unresolved record retained but excluded from a particular supervised export. Choose from the objective and evidence, not because a CSV column prefers one string.

## Agreement measures consistency, with assumptions

For categorical labels, **raw agreement** is matching judgments divided by comparable judgments. State how missingness, abstention, and multiple labels are treated. Two reviewers matching on three comparable items out of four have 75% raw agreement on that set. If an additional fifth item has no judgment from one reviewer, it does not become an agreement or disagreement automatically; count the missingness separately.

Prevalence can make agreement misleading. **Authored illustration:** two reviewers label 100 items. Both say negative on 90; on five only reviewer A says positive; on five only B does. They agree on 90% overall but never jointly identify a positive. Each reviewer's positive fraction is 0.05. A chance-agreement term based on their marginal rates is 0.05² + 0.95² = 0.905. Cohen's kappa, defined here as (observed agreement − that chance term)/(1 − that chance term), is (0.90 − 0.905)/(1 − 0.905) ≈ −0.053. This is arithmetic illustrating a prevalence effect, not a claim that one coefficient settles validity.

Show the contingency counts, per-label behavior, sampling composition, and missingness beside any coefficient. Krippendorff's alpha [R02] generalizes reliability as 1 − observed disagreement/expected disagreement, with a stated distance between labels and handling of missing ratings. A nominal distance treats any different category as disagreement; an ordinal distance can recognize ordered severity. Choosing the distance encodes what differences matter. Reliability cannot prove unbiased reviewers or a valid target.

For geometry and time, a category coefficient misses boundary errors. Measure appropriate mask overlap, boundary displacement, timing tolerance, and missed instances. For preferences, preserve ties and criterion-specific reasons. Do not import a universal “good agreement” threshold without a decision-specific rationale.

## Controlled exercise: label, adjudicate, retain

**Evidence status:** authored paper exercise. If two people actually label independently, record that as your own small annotation exercise, not a population study. **Unit:** one message. **Denominator:** four comparable paired judgments; missing and unresolved states are reported separately.

1. Label the four messages under A and B before reading the worked answer, retaining both columns and instruction versions.
2. Identify whether each mismatch is a guide difference, evidence gap, ordinary error, or another cause. Explain uncertainty in the cause.
3. Write an adjudication reason for the invoice-link message under guide B.
4. Construct a reference-state sheet for r01/r02, r27/r28, r12, and r20. Do not replace a missing or conflicting reference with the weak prediction.
5. Add “The renewal thing is wrong” and decide whether your guide can support a single routing target from that input alone.

### Acceptance check

Pass when original judgments remain available, each accepted answer names its guide, and missing/conflicting/resolved states remain distinct. A reviewer must reconstruct the adjudication reason and identify what evidence was unavailable. Revise a reference claimed independent merely because it was stored separately. Reject conflict resolution chosen only to match the evaluated procedure.

### Worked answer and reviewer guidance

The table supplies the authored A/B results: two matches and two policy-driven differences. The invoice-link adjudication chooses technical under B because the failure is the link, with the guide-convention reason retained. r01/r02 produce a resolved billing reference; r27/r28 remain conflicting; r12 and r20 remain missing. “The renewal thing is wrong” lacks enough detail to distinguish billing, access, or an interface fault, so retain uncertainty or seek context under the allowed process. Do not invent a specific incident.

Reviewers should accept a justified alternative ontology if the learner explicitly changes the task rather than mixing policies invisibly. Ask what consensus would and would not prove. A good answer says it may establish shared application of the guide, while source factuality, target validity, and downstream utility still need other evidence.

## Optional deeper primary reading

Read [Krippendorff's computational note](https://www.asc.upenn.edu/sites/default/files/2021-03/Computing%20Krippendorff's%20Alpha-Reliability.pdf) [R02] for reliability assumptions and [Dealing with Disagreements](https://aclanthology.org/2022.tacl-1.6.pdf) [R03] for subjective judgments. These are deeper concepts, not required software exercises. The next chapter measures a release using these reference states and explicit denominators.
