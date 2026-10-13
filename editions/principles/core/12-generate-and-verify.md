# 12 Generate candidates and verify the claim

*Dataset Production · Puma*

## The question: what did the checker actually prove?

A generator answers “What fraction equals 0.5?” with “The answer is not 1/2.” A checker finds the substring `1/2` and accepts it. The output passed an implemented test, yet it did not satisfy the intended task.

The principle is **separate proposal, verification and acceptance**. Generation creates candidates. A verifier checks defined properties under a specification. Acceptance combines those checks with source, relevance, rights, independence and review gates. Passing an incomplete checker cannot establish broad correctness.

You enter with protected families, audit methods, target-valid transformation rules and supervision provenance. You leave with a bounded generator/verifier plan, explicit rejected candidates, and a statement of what remains unsupported. Generating teacher responses or supplying reward-bearing tasks belongs here at the data-contract level; architectures and fitting implementations belong in the companion.

## Work a fraction contract before building a verifier

**Authored illustration.** The task is: return exactly one reduced fraction equal to 0.5, written as integer numerator/positive denominator with ordinary digits, no plus signs or leading zeros, and no explanation. Surrounding whitespace may be trimmed. “Reduced” means numerator and denominator have no common divisor greater than one.

| Candidate | Mathematical value | Format/process issue | Decision |
|---|---|---|---|
| `1/2` | correct | meets exact contract | accept |
| `2/4` | correct | not reduced | reject |
| `0.5` | correct | not a fraction | reject |
| `1/3` | wrong | otherwise interpretable | reject |
| `1/2 or 2/3` | competing answers | not exactly one fraction | reject |
| `The answer is not 1/2.` | does not assert required answer | extra prose | reject |
| `1/2 because 1 + 1 = 3` | fraction correct | extra prose and false reasoning | reject |

An exact trimmed-string check for `1/2` happens to suffice for this narrow task. It does not generalize to arbitrary fractions or allowed equivalent expressions. A general verifier would need bounded parsing, denominator/domain checks, equivalence and format checks. Never evaluate untrusted expressions with unrestricted code execution.

Now change the contract to allow unreduced fractions. `2/4` becomes acceptable. The verifier should change because the task changed. A checker cannot be correct independently of the specification it implements.

Separate **format**, **answer correctness** and **reasoning correctness**. An answer-only response offers no steps to review. A correct final answer does not certify an attached explanation. A process label identifies a property of a step under available evidence, rather than merely the terminal answer.

## Verify one synthetic helpdesk record

The fraction task changes modality to expose checker scope. Return now to our running helpdesk.

**Authored illustration.** A generator proposes:

```
source: authored-device-example-1
text: The charge indicator stays at zero.
target: billing
parent_family: device-indicators-1
```

A structural checker can establish that the record has the expected fields and permitted target string. It cannot establish that billing owns the problem. A semantic check under our routing guide identifies a device indicator failure and proposes technical. Another keyword-based judge may agree with billing because it shares the generator's `charge` shortcut. Agreement between similar systems is evidence of shared decisions, not independent truth.

Accept a corrected record only after the guide and context support it. Record the initial candidate, rejection reason, revised target and review evidence. The source is authored; it is not a real customer's message, and the derivative does not add a new independent family. “Verified” must identify the property and checker, not become an unqualified badge.

A synthetic four-cell field illustrates another limit. If values are 1, 2, 3, 4 in a declared axis order, a sum checker confirms 10. Reversing the order still gives 10, so that check cannot certify spatial alignment. Conservation-like checks can detect some numerical defects while leaving unit, boundary, resolution and physical-validation claims unanswered. The optional physical track explores those limits further.

## Choose generation for the missing evidence

Several strategies change different pieces of the task:

- **Grounded transformation** starts with permitted source evidence, then extracts, translates, paraphrases or recaptions it. Verify against the source and Chapter 10's target policy.
- **Seed expansion** uses a few examples to propose new tasks. The seeds shape the output distribution; keep seed ancestry and reserve evaluation families before expansion.
- **Controlled evolution** adds constraints, reasoning steps or broader topics. Longer prompts are not automatically coherent, solvable or useful.
- **Model-prior sampling** uses a teacher's learned task distribution. It can reduce manual seed work while still inheriting the teacher/template's biases.
- **Factorized generation** samples a structured scenario, then realizes it. Record requested and verified factors separately; asking for two objects does not prove two appear.
- **Environment-backed rollout** records actions and actual observations in a controlled executable environment. It supports claims about that environment and tests, not an unexecuted production service.

A real image with a generated caption, a rendered image with a simulator mask and a fully invented conversation have different evidence chains. Preserve which parts are observed, generated, mechanically checked and human-reviewed. Permission to use a seed is also not unlimited permission to reuse every third-party fragment a generator reproduces.

## A verifier changes both quality and composition

**Authored production funnel.** Imagine 10,000 candidates, 60% correct under one binary reference. A verifier accepts 95% of correct candidates and 10% of wrong ones. It accepts 6,000×0.95 = 5,700 correct and 4,000×0.10 = 400 wrong candidates. Accepted precision is 5,700/6,100 ≈ 93.4%; acceptance is 6,100/10,000 = 61%.

The false-accept rate among wrong candidates is 10%, while error among accepted candidates is 400/6,100 ≈ 6.6%. They are different denominators. If the generator's starting quality falls, the same verifier can leave a worse accepted collection.

Two verifiers with those rates and conditional independence would accept 6,000×0.95² = 5,415 correct and 4,000×0.10² = 40 wrong candidates, about 99.3% precision. If both pass the same wrong subset, the squared-error calculation is unjustified. The numbers are constructed assumptions, not measured model capabilities.

Audit false rejection too. A filter can produce excellent retained precision by deleting a useful rare condition. Report funnel counts, accepted family counts and coverage shifts by relevant slice. Maximum embedding distance can select nonsense, and diverse wording can still restate one fact. Useful diversity concerns task conditions and independent sources, not visual novelty alone.

## Keep roles and failures visible

Name generator, grounder, verifier, judge, refiner and reviewer. A single teacher can do several jobs, but its feedback is dependent. A deterministic specification, actual environment observation or qualified review may add evidence unavailable in another prompt to that same teacher.

A judge needs a rubric, reference-based checks where possible, order swaps or blind identity to investigate bias, ties/uncertainty, and qualified-review calibration by slice. Fluent verbosity can influence preference without improving factual correctness. Selecting the highest judge score among many candidates may exploit a proxy's weaknesses.

Refinement is another candidate proposal. Save the original, critique, revision and recheck. Compare an extra critique/rewrite call with another same-budget candidate judged by the same checker. Set a stopping rule: verified success, exhausted budget, repeated failure or unresolved ambiguity. A final attractive output is not the whole cost record.

For executable verification, version environment/dependencies, starting state, random seeds, test suite and resource/time limits. Separate wrong answer, malformed candidate, insufficient task evidence, verifier timeout and environment failure. A crate-fraction task with no counts is invalid even if a reference file says `1/2`. A timeout does not prove the candidate mathematically wrong.

## Controlled exercise and Part 3 assessment

**Evidence label: authored illustration; verifier execution and downstream utility remain unrun work.** Unit: candidate attempt, with parent problem/family as the independence unit.

1. Observe and classify the seven fraction candidates by format, answer and process properties.
2. Calculate both funnel precisions. Write the independence assumption needed for the second.
3. Check the synthetic helpdesk record with a structural rule and the routing guide. Name what each check establishes and cannot establish.
4. Make one controlled change: revise a failing candidate, verifier rule or acquisition policy. Keep ancestry, rejected attempts, seed exposure and evaluation roles in the record.
5. Defend one improvement from Chapters 9–12 under a fixed comparison plan. Submit baseline, expected mechanism, changed artifacts, acceptance gates, full attempted/accepted counts, costs and observed failures. Test a paper-visible property or a supplied CPU data check; label model effects as proposed until fitting/evaluation evidence exists.

The Part 3 assessment needs one controlled change in practice, not a collection of method names. A data-validity result can support acceptance of a better contract or corrected label. An asserted performance improvement requires a fair learned-consumer experiment and independent evaluation. Do not convert the supplied invented score sheets into executed evidence.

## Acceptance check and worked reviewer answer

Pass when every accepted record is traceable to its source/seed, the verifier's scope is explicit, rejected candidates remain counted, final references stayed out of construction, and the controlled change meets the predeclared gates without unsupported claims.

Worked answers: only `1/2` passes the original fraction contract. Under the relaxed unreduced-fraction contract, `2/4` also passes. A substring check fails on negated answers and prose. The helpdesk structure is valid while its proposed target is unsupported; the routing guide points to technical. The sum 10 cannot detect axis reversal. One verifier gives 93.4% accepted precision; the hypothetical independent pair gives about 99.3%. Independence must be justified, not inferred from different names.

Reviewer guidance: challenge the verifier with plausible wrong answers, missing information, schema-valid invalid IDs and hard-coded visible test responses. Demand source and environment evidence for an execution claim. Count seed families separately from response attempts. A correct answer with unreviewed reasoning supports only an outcome claim. An unresolved judge disagreement calls for evidence or abstention, not invented certainty.

## Optional deeper methods and primary reading

Retain the original research edition's source trail: Wang et al., [Self-Instruct](https://arxiv.org/abs/2212.10560) [R18]; Xu et al., [WizardLM/Evol-Instruct](https://arxiv.org/abs/2304.12244) [R19]; Xu et al., [Magpie](https://arxiv.org/abs/2406.08464) [R20]. These strategies motivate candidate distributions rather than replace release verification.

For process versus outcome evidence, read Lightman et al., [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) [R21]. Preserve its comparison and generator/selection setting rather than treating step labels as a universal guarantee. Madaan et al., [Self-Refine](https://arxiv.org/abs/2303.17651v2) [R22], and Huang et al., [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798) [R23], examine different feedback/stop conditions; neither supplies a timeless verdict on every teacher. Zheng et al., [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) [R24], and Gao et al., [Reward Model Overoptimization](https://arxiv.org/abs/2210.10760) [R25], motivate proxy and bias audits.

Recursive replacement and accumulation are different retention experiments. Losing a rare category in an empirical-resampling toy process can remove its future support, while retaining earlier sources changes the process and cost. Read Shumailov et al. [R26] together with the [2025 correction](https://www.nature.com/articles/s41586-025-08905-3) [R27], and Gerstgrasser et al., [Is Model Collapse Inevitable?](https://arxiv.org/abs/2404.01413) [R28]. Do not derive a universal safe synthetic percentage. The optional reasoning track retains full trajectory and learner-state examples; fitting/reward optimization remains in the companion.
