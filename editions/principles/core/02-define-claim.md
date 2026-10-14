# 2 Define the question and the claim

*Dataset Production · Puma · Part 1: A first useful release*

## A beginner's question: what should this answer mean?

A message contains “refund.” Does its correct answer have to be “billing”? The helpdesk may ask which department should handle the message, whether the customer requests a refund, or which span expresses a requested action. These are different questions about the same source. A label can be perfectly consistent with one and wrong for another.

After chapter 1, you can inspect the release's parts. Here you will specify its purpose. You will finish with a bounded claim, a decision unit, a proposed baseline and measurement, and a clear account of what success would not establish. No fitting or model implementation is needed.

## The principle: state the decision before measuring success

Name five things before choosing labels or scores:

1. **Input:** the evidence available at decision time.
2. **Target:** the answer or behavior sought under a stated convention.
3. **Decision unit:** what receives one answer, such as a message, conversation, image, or one-second field transition.
4. **Population:** the set of situations to which the claim is meant to apply.
5. **Failure cost:** what goes wrong when an answer is wrong, missing, or late.

The **claim** connects them: what a result would establish, for which population, under which conditions. A benchmark score supports only the evaluation conditions actually measured. “Works on our data” is not a population definition.

For a deployed router, the input might be the latest message alone, or the whole conversation up to the decision time. If the target requires earlier context but the input omits it, a wrong label may actually expose a broken task. The input must exclude evidence available only after the decision, such as the queue assigned by an agent later. That would make an impressive score answer an easier and unintended question.

## A small worked comparison

**Authored illustration.** Consider these requests under two tasks:

| Message | Department routing | Explicit refund intent |
|---|---|---|
| Please refund this payment. | billing | refund requested |
| Please do not refund this payment. | billing | refund not requested |
| The invoice link returns an error. | technical | refund not requested |
| Password reset says error. | access | refund not requested |

For routing, both refund messages concern payment handling, even though they request opposite actions. For intent extraction, negation changes the target. The broken invoice link belongs to technical under this fixture's concrete-interface-failure policy. The password-reset error remains access because the message reports an unsuccessful account-recovery operation without a specific interface fault. Another organization could choose other owners, but it must document that policy.

Notice the cost of a vague label called “refund.” Does it mean the word occurs, a refund is requested, a refund is allowed, or a refund has happened? Those are not interchangeable. A router's billing output is not permission to move money. Define permitted use so a downstream consumer cannot turn a triage label into an authorization.

A bounded teaching claim is: “Given one fictional English helpdesk message, our fixed keyword rules propose one of the three routing queues or explicitly abstain/conflict under guide version 1. We describe their coverage and reference agreement on the supplied fixture.” A future claim might concern unseen customer conversations, but it would need new acquisition, rights, independent references, and appropriate evaluation. It remains proposed work here.

## The theory: a target is not the same as a measurement

A **construct** is the idea we want to learn about, such as useful routing or factual helpfulness. An **operationalization** is the procedure we use to observe it: a queue guide, rating scale, or reference review. Jacobs and Wallach explain why reliable measurement can still fail to capture its intended construct [R01]. Two people may reliably rate politeness while the project claims to measure correctness.

For this fixture, a department guide operationalizes “who should handle this problem.” Agreement with authored references measures conformity to that guide as represented by those references. It does not measure customer satisfaction, resolution time, or real department capacity. We have not observed those outcomes.

Use a **quality profile**, because several failure questions are separate:

- **Integrity:** are the records readable, complete, and traceable?
- **Target validity:** does the label answer the intended question?
- **Label fidelity:** does the recorded judgment agree with qualified review or verifiable evidence?
- **Coverage:** are relevant conditions represented, with enough independent examples?
- **Independence:** does evaluation avoid related or previously exposed material?
- **Usability and permitted use:** can the consumer interpret and lawfully use the release?
- **Downstream utility:** does it improve the actual behavior under a controlled comparison?

Some are acceptance constraints. Unsupported rights or known evaluation leakage cannot be compensated for by better average agreement. Other dimensions involve tradeoffs. Removing all ambiguous requests may improve agreement while excluding the requests the helpdesk most needs to handle.

### Choose a baseline and a metric together

A **baseline** is the declared starting procedure for comparison. It must be simple enough to understand and specified before using evaluation feedback to improve it. The fixture's fixed keyword rules are a measured data-production baseline, not a trained model. For an imagined deployed router, always choosing the most common queue is another proposed baseline. The two answer different questions.

A **metric** is a defined calculation. For agreement, let C be the number of correct comparable predictions and E the number of predictions with resolved references. Agreement is C/E when E > 0. For coverage, let L be the number given labels and N the eligible example count. Coverage is L/N when N > 0. If a denominator is zero, report “not estimable” and the count, not 0% or 100%.

A majority-queue baseline can perform well when one queue dominates while never finding a rare queue. Inspect per-category behavior and important failure slices. A failure **slice** is a specified subset, such as messages describing concrete login interface faults. A score without a population and denominator cannot show whether that subset is protected.

### Three distributions can legitimately differ

The deployment population might contain mostly ordinary requests. Training may deliberately oversample rare failures. Evaluation may sample rare failures heavily to inspect them. These are the deployment, training-exposure, and evaluation-sampling distributions. Do not silently substitute one for another.

**Authored arithmetic.** If expected deployment is 80% ordinary and 20% difficult requests, and a procedure's measured errors under suitable independent sampling are 1% and 6%, deployment-weighted error is 0.8 × 0.01 + 0.2 × 0.06 = 0.02, or 2%. This is an illustration, not this fixture's error rate. The weights, sample design, and meaning of “difficult” need evidence before that calculation supports a real claim. Chapter 8 returns to this example.

A coverage table is useful but incomplete. Having examples with negation and examples with software crashes does not show coverage of negated crash reports. Mark impossible combinations, excluded regimes, unobserved cells, and cells with few independent groups. Leave room to discover failures outside the initial table.

## Controlled exercise: write two task cards

**Evidence status:** authored illustration and proposed work. **Decision unit:** one message in the four-row table. **Denominator:** all four messages for paper classification; a future metric's denominator must be declared separately. No model is run.

Write one card for routing and one for explicit refund intent. Each card must include input, target, decision unit, population, permitted use, excluded conditions, proposed baseline, proposed metric and denominator, and an important failure cost. Classify all four messages. Then add this question: “Could the output authorize a refund?” Explain your answer from the contract, rather than from the presence of a word.

### Acceptance check

Pass when the cards produce different targets for the negated refund request, state what evidence is available, and separate proposed success criteria from observed results. A reviewer must be able to tell what future evidence could refute the claim. Revise a card whose metric omits abstentions without reporting coverage. Reject a refund-authorization claim: neither task supplies permission or verifies entitlement.

### Worked answer and reviewer guidance

Routing card: input is one message; target is an owning queue under the stated guide; unit is a message; population is the authored English teaching collection. Permitted use is teaching/triage illustration subject to source rights; refund execution and real deployment are excluded. The fixed keyword rules are a baseline already measured on the supplied fixture; a change to them is proposed work. Agreement uses predictions with resolved references, while coverage uses all eligible canonical examples. A key failure is sending an interface fault to access or billing because of a keyword.

Intent card: input is one message; target is whether an explicit refund is requested; unit is a message; population is the four authored examples for this exercise. A proposed baseline recognizes explicit requests and negation under a stated rule. A proposed exact-match metric would use all four independently resolved paper targets, with uncertain cases separately counted if added. A key failure is treating “do not refund” as a positive request. No intent-baseline execution or future accuracy is claimed.

The targets are those shown in the table. Both cards prohibit financial action. Reviewers should accept reasonable alternative baselines if they are fully specified and have no invented results. Ask the learner to change the population from fictional messages to new real customer conversations. A correct answer identifies missing evidence rather than merely changing the card's title.

## Optional deeper reading and companion boundary

Jacobs and Wallach, [Measurement and Fairness](https://arxiv.org/html/1912.05511v3) [R01], supply the measurement framework. Their discussion motivates explicit assumptions; it does not offer a universal quality score. Fitting choices, architectures, and neural training belong to the separate *Training Your Own Models* companion. Here a proposed baseline is enough to specify what the data must support. Dataset Production ends at a verified data and consumer contract; a text release does not automatically fit the companion's numeric examples.
