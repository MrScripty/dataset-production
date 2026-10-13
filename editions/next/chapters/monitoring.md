# Monitor repair and roll back a production release

The release chapter showed how to freeze a set of examples and check what a consumer will read. A new problem appears once that release is in use: sources and processing code can change. How do we discover a bad change before treating its output as a new improvement?

We will follow one lost word through an entire incident. This is an invented operational walkthrough, not a report of a deployed service. It supplies the inputs, observations and decisions on this page. No monitoring platform, application or rollback program has to be installed.

## Start with the behavior that must remain correct

Our helpdesk now has a second task. Instead of merely choosing a department, a future assistant must extract whether the customer is requesting a refund. This is a different target: adding “not” may leave the department as billing while reversing the requested action.

For this walkthrough, the source is:

~~~html
<p>Please do <span>not</span> refund this payment.</p>
~~~

The intended extracted request is:

~~~text
Please do not refund this payment.
~~~

The target is “refund not requested.” An earlier parser, version P1, keeps all the text inside the paragraph. A proposed parser, P2, accidentally keeps only direct paragraph text and drops text inside the span. It produces:

~~~text
Please do refund this payment.
~~~

The output is valid text. It has the expected field and can pass a JSON schema check. It is nevertheless the wrong example, because the source's meaning changed.

## Use a small known case to notice the change

A **monitor** repeatedly checks a property whose change may require attention. Some monitors check job completion or missing fields; others check whether known examples still have the intended meaning. A **regression case** is a saved example that should continue to behave correctly after an update.

Our small regression set contains four requests:

| Source request | Expected meaning | P2 extraction preserves it? |
| --- | --- | --- |
| Please refund this payment. | Refund requested | Yes |
| Please do NOT refund this payment, with “not” inside a span | Refund not requested | No |
| Refund the duplicate charge. | Refund requested | Yes |
| Do not refund the duplicate charge, all in ordinary paragraph text | Refund not requested | Yes |

P1 passed all four. P2 passes three of four. These are invented walkthrough counts, not measurements from the supplied JSONL lab. They are enough to reveal a specific regression, but far too few to estimate an entire parser's quality.

The alert should say what changed: the nested-negation case failed after the P2 update. “Data quality dropped” would be less useful. It might send us toward the model, labeling rules or source population before we inspect the precise transformation that lost the word.

## Diagnose the first incorrect representation

Follow the record through its stages:

~~~text
Source S07:     Please do not refund this payment.
P2 extraction:  Please do refund this payment.
Label L07:      refund requested
Release R2:     contains the incorrect extracted example and label
Model M2:       trained using R2
~~~

The source is correct. The first wrong representation is P2's extracted text. Merely changing L07 to “refund not requested” while leaving the input as “Please do refund” would create a contradictory training pair. We need to repair the extraction and rebuild the dependent outputs.

A **descendant** is an artifact made from an earlier artifact. Here the label, exported example, release and model are descendants of the extracted request. The lineage we preserved in the early lessons tells us where to look. If an index or an embedding was also made from the faulty text, it belongs in the impact check too.

Search for other sources with the same structure, then review some ordinary records as well. The bug may affect more than the word “not,” and checking only the known failure can miss a shared problem. Keep actual observations separate from hypotheses: the failed example proves a nested-text loss, not yet how common that loss is.

## Contain the problem before preparing a repair

Suppose the faulty R2/M2 bundle is already active. An **active bundle** is the particular dataset history, preprocessing and model version selected for use. A **rollback** returns that selection to an earlier approved bundle.

In this scenario, the previous approved bundle is R1/P1/M1. Reverting only the dataset pointer does not make M2 forget the faulty examples it learned from. Reverting only the model while continuing to drop negation in live inputs also leaves a problem. The chosen bundle must be compatible as a whole.

Before relying on the old bundle, check that its files exist and can still be loaded by the current application. Record who can authorize the switch and how success will be checked. For this task, a meaningful post-switch check includes sending the saved nested-negation input through the selected preprocessing path and confirming that the word survives.

This is a design walkthrough. The repository's first-release lab builds data files; it does not contain this hypothetical application, M1/M2 models or an active-bundle switch. There is no rollback command to run for this chapter.

## Build a corrected candidate without erasing the evidence

Repair the parser as P3, and keep P2's faulty outputs available for investigation where retention and permissions allow. Build a new **candidate release**, R3, rather than replacing the bytes behind the old name R2. A candidate is a proposed replacement that has not yet passed its acceptance checks.

Reprocess the affected sources, revise their dependent labels and exports, and rerun the consumer's loading checks. The intended corrected example is:

~~~text
Source S07:     Please do not refund this payment.
P3 extraction:  Please do not refund this payment.
Rebuilt label:  refund not requested
Candidate R3:  preserves the source meaning
~~~

Now evaluate the candidate against a declared acceptance plan. Here is a worked example of the results:

| Check | Walkthrough result | Interpretation |
| --- | --- | --- |
| Original four regression cases | 4/4 pass | The known failures are repaired in these cases |
| Additional review of 20 affected sources | 18 correct; 2 unresolved | More evidence or clarification is still needed |
| File/schema/loader checks | Pass | The consumer can read the files; this does not settle meaning |
| Old approved bundle remains available | Yes | Keeping R3 on hold need not force use of R2 |

R3 is not ready just because its headline regression score returned to 4/4. The two unresolved sources must be adjudicated, meaning reviewed to a justified decision, or excluded with the resulting coverage change documented. A final decision should use the acceptance plan and the application's consequences, not a threshold invented after seeing these results.

Passing these data gates approves R3 as a dataset candidate; it does not repair or approve M2. In this walkthrough, the next step would be to train a replacement model M3 from the corrected data and evaluate it separately against the model acceptance plan, including the refund-negation behavior. That training and evaluation have not been implemented or run here. A different model decision would need its own evidence; silently retaining M2 is not a repair. Only an approved R3/P3/M3 bundle, with compatible preprocessing and separately accepted model behavior, could replace the restored R1/P1/M1 bundle.

The important separation is between **repairing the known bug** and **establishing that the replacement is ready**. Both matter. A successful file check cannot substitute for a semantic audit, and a small clean audit cannot prove every unseen case is correct.

## Turn the incident into a better next release

When both the corrected data and replacement model meet their respective gates and the authorized owner selects R3/P3/M3, verify that the application actually uses those exact artifacts. Keep a record of affected releases and downstream products. Mark faulty artifacts so they are not selected accidentally in another experiment.

Add the nested-text case to the regression set, but avoid repeatedly using a protected final model test set to tune the parser. Development cases are for repair. A final evaluation whose examples have become part of the repair process no longer supports the same untouched-test claim.

Monitoring also needs limits. A change in word frequencies is a signal to investigate, not proof of failure. A stable average model score is not proof that a rare but important source format is safe. Choose checks that address the failure modes and consequences of the specific application.

## Exercise complete the incident decision

This exercise is a design exercise on paper. Nothing runs, no external data or service is required, and all evidence is supplied above.

Write a short incident record answering these questions:

1. Where does the first error appear? Expected answer: P2 extraction loses the nested “not”; the original source is intact.
2. Why is relabeling L07 alone insufficient? The model-facing text would still ask for a refund and conflict with the repaired target.
3. Which prior bundle could be restored? R1/P1/M1, after checking compatibility and availability.
4. Is R3 ready in the displayed results? No. The two unresolved source reviews still need a decision under the acceptance plan.
5. What proves a switch took effect? Checking the selected artifact identities and the actual preprocessing behavior, not merely editing a release name in a document.

If the previous bundle is unavailable, rollback is not presently possible; stop claiming it as a safety net and choose a containment action the application actually supports. If a source is ambiguous, preserve that uncertainty instead of declaring the repair complete.

**What you have learned.** You can trace an alert to a source transformation, identify affected descendants, distinguish a corrected candidate from an approved replacement, and describe what a rollback must restore. Implementing the deployment controls is a later engineering project. The reasoning about evidence and reversibility can be practiced now.
