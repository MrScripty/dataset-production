# Produce reasoning tasks and trustworthy trajectories

This is an optional track after the shared lessons on labels, independence and audits. So far, many of our targets have been short labels such as billing or square. A model that solves a problem or takes actions needs a different kind of training example: a sequence, a task with a way to judge answers, or an ordered record of actions.

We will use one fraction question and a two-step navigation task. Both are fully supplied on this page. No language model, dataset or verification package is needed to understand the lesson.

## Copying a solution and checking an answer are different jobs

Consider this prompt:

~~~text
What fraction is equal to 0.5?
~~~

A teacher could supply this response:

~~~text
0.5 is five tenths. Dividing the numerator and denominator by five gives 1/2.
~~~

If we train a student model to reproduce responses like that, the response is a target sequence. **Sequence distillation** means learning from sequences produced by a teacher. The teacher is often another model, but recording its output does not make the output correct.

**Supervised fine-tuning**, or SFT, adapts an already trained model using examples of desired outputs. In a reasoning SFT example, the prompt is the input and the teacher's response is the target. We would preserve where the question came from, which teacher produced the response, and whether anyone checked it. Multiple responses to the same question remain related examples.

Now consider **reinforcement learning**, or RL. A learner produces an attempt and receives a reward, such as a score for meeting a task's requirements. Training uses that feedback to make rewarded behavior more likely. For this data-production track, our job is to supply tasks and a trustworthy scoring procedure. We are not running an RL trainer here.

A **verifier** is the program or procedure that checks an attempt. A weak verifier can reward an incorrect answer, so constructing the verifier is part of constructing the dataset.

## Write the answer contract before writing a checker

Let us make the fraction task precise:

~~~text
Return exactly one reduced fraction equal to 0.5.
Write integer numerator/denominator, with a positive denominator.
Use digits without plus signs or leading zeros.
Do not include an explanation or any other text.
~~~

A **reduced fraction** has no common divisor greater than one in its numerator and denominator. The valid target for this particular task is 1/2. We allow surrounding whitespace to be trimmed, but we do not allow decimals or extra prose.

Here are worked judgments under that contract. They are deductions from the stated rules, not results from a verifier program run in this chapter.

| Submitted response | Mathematical relationship | Format judgment | Task judgment |
| --- | --- | --- | --- |
| 1/2 | Equals 0.5 | Meets the contract | Accept |
| 2/4 | Equals 0.5 | Fraction is not reduced | Reject under this contract |
| 0.5 | Has the requested value | Decimal rather than fraction | Reject under this contract |
| 1/3 | Does not equal 0.5 | A reduced fraction | Reject: wrong value |
| 1/2 or 2/3 | Contains competing answers | Not exactly one answer | Reject: ambiguous submission |
| The answer is not 1/2. | Does not assert the requested answer | Extra prose | Reject |
| 1/2 because 1 + 1 = 3 | Contains the correct fraction | Extra prose | Reject; the explanation is also false |

A checker that searches only for the substring 1/2 would accept several of the bad submissions. It would reward finding a way to include the expected token rather than satisfying the task. A checker that first trims the permitted surrounding whitespace and then insists on the exact text 1/2 happens to fit this narrow contract, but it would be too restrictive for a different task that allows any equivalent mathematical expression.

This separates three questions:

1. **Format:** can we interpret the response in the form the task requires?
2. **Answer correctness:** does the interpreted answer satisfy the question?
3. **Reasoning correctness:** are the explanation's steps sound?

An answer-only response gives no reasoning steps to inspect. A correct final answer does not establish that an attached explanation is correct. If the training product needs process-level supervision, we need evidence about the process, not just the final number.

## Sometimes the problem is the task rather than the answer

Suppose a producer adds this question to the collection:

~~~text
What fraction of the items in the crate was sold?
~~~

No item counts are supplied. A reference file that simply says 1/2 does not repair the missing information. This task should be held for review or removed from the applicable collection. That status is different from a learner giving a wrong answer to a well-specified problem.

Likewise, a parser timeout means the scoring program did not finish; it is not evidence that the mathematical answer was false. Keep wrong answer, invalid format, ambiguous task and verifier failure distinct in the audit, even if a later reward policy assigns some of them the same numerical score.

Never evaluate arbitrary submitted code or expressions with unrestricted execution. A real verifier needs bounded parsing, resource limits and, for executable code tasks, an appropriately isolated environment. Those implementation choices are beyond this paper exercise.

## A short trajectory makes another kind of target

A **trajectory** is an ordered record of observations, actions and their results. Imagine a character on a row of three cells, with a goal at the rightmost cell:

~~~text
Start:   [agent] [empty] [goal]
Finish:  [empty] [empty] [agent]
~~~

An expert supplies this two-step trace:

| Step | Observation available before acting | Action | Result |
| --- | --- | --- | --- |
| 1 | Position 0; goal at 2; cell 1 is free | Move right | Position becomes 1 |
| 2 | Position 1; goal at 2; cell 2 is free | Move right | Position becomes 2; goal reached |

For next-action imitation, each observation/action pair is an example. The second input must include the state after the first move; simply attaching both actions to the initial state would describe a different training task. Preserve order, the starting state, the action meanings and the condition for ending the episode. Both steps belong to the same source episode for splitting.

Now imagine that a student moves left on the first step in a larger environment. Its next observation differs from the expert's second observation. High accuracy on the expert's recorded steps does not necessarily mean the student recovers when it visits unfamiliar states. The [DAgger paper](https://proceedings.mlr.press/v15/ross11a.html) studies this learner-induced state-distribution problem. Here it gives us a reason to evaluate complete rollouts and recovery behavior later, rather than treating stepwise imitation as the whole task.

A teacher may also have information the student will not receive. A navigation expert with a full hidden map should not be represented as if its decisions depended only on a small camera view. Record what the learner actually observes, and distinguish it from privileged teacher information.

## What larger research collections add

The same distinctions matter at scale. [OpenThoughts](https://arxiv.org/html/2506.04178v2) studies teacher-generated reasoning sequences and the choices used to make them. Its [OpenThoughts3 card](https://huggingface.co/datasets/open-thoughts/OpenThoughts3-1.2M/blob/61bcf9d4eb38b30295efc2021227a63cc5bb34c8/README.md) describes 75,000 questions with repeated responses, not 1.2 million independent questions. Count questions and response attempts separately.

[Big-Math](https://arxiv.org/html/2502.17387v1) instead illustrates production of tasks with checkable answers for RL. Choosing automatically checkable tasks also narrows what kinds of reasoning the collection represents. Its public verified release contains tasks and answers rather than teacher rollouts. These collections answer different production needs.

For a later implementation, [Math-Verify 0.9.0](https://pypi.org/project/math-verify/0.9.0/) is one evaluator to investigate. Its [documentation](https://github.com/huggingface/Math-Verify) distinguishes extraction and equivalence checking; it is not a universal proof checker. No installation is needed for this chapter. Large-corpus acquisition details, version pins and current access restrictions are in the separate research register. In particular, Big-Math's current file gate requires account/terms/contact steps, so it is not a prerequisite here.

## Exercise test the specification on paper

Nothing runs in this exercise. The prompt, candidate answers and two-step trace above are all the supplied material. No download is required.

First, change the fraction contract to allow any reduced or unreduced fraction, while still requiring exactly one fraction and no prose. Which row changes? 2/4 becomes acceptable; 0.5, competing answers and explanations remain outside the format. This shows that a verifier's judgment depends on the declared task, not merely on an answer string.

Next, invent one response that fools a substring checker but violates the contract. “Do not answer 1/2” is one example. Explain which check catches it. Finally, write the second navigation example as an observation/action pair and state why it belongs to the same episode as the first.

**What you have learned.** You can tell apart imitation targets, reward-bearing tasks and action trajectories. You can judge format, answer and reasoning separately, and identify a task whose reference answer is not supported. Implementing a general math verifier, generating teacher rollouts or training an RL model is an optional later project, not an implied completion of this lesson.
