# Produce reasoning tasks and trustworthy trajectories

A question with a teacher's answer, a question with a checkable reference, and a successful action trace are three different training products. They can share source material, but they supply different evidence. A beginner can learn the distinction with ten authored arithmetic tasks and a paper audit before downloading a large reasoning corpus or training a language model.

## Sequence distillation preserves a teacher response

In supervised sequence distillation, a teacher supplies an ordered output that a student is trained to imitate. The target may include reasoning text, code, tool calls or a final answer. Record the teacher model/version, generation settings, source question, response attempt, termination condition and any filtering. Never describe an unknown teacher as a source of verified truth merely because it writes a convincing explanation.

The [OpenThoughts paper, version 2](https://arxiv.org/html/2506.04178v2), examines question sources, teachers, repeated sampling and filtering through many controlled experiments. Its weak benefit from answer filtering in some supervised-training settings is a conditional finding. It is useful contrary evidence against assuming that a plausible filter always improves a student, but says little about whether a reward function is safe to optimize.

Counting the right unit changes the interpretation of a corpus. The [OpenThoughts3 card at revision 61bcf9d](https://huggingface.co/datasets/open-thoughts/OpenThoughts3-1.2M/blob/61bcf9d4eb38b30295efc2021227a63cc5bb34c8/README.md) describes 75,000 questions with 16 teacher responses apiece, producing 1.2 million rows. Repeated responses can expose useful variation, but they are not 1.2 million independent questions. Split by question and upstream source before sampling responses, then check for translated, paraphrased or shared-template relatives across splits.

A correct final answer does not prove every intermediate claim in the rationale is sound. Preserve separate fields for final-answer checks, step review, execution evidence and reviewer uncertainty. If a process label exists, specify whether it means locally valid reasoning, progress toward a solution, reviewer preference or something else. An answer-only check cannot silently authorize step-level supervision.

## Verifiable reinforcement learning begins with a task contract

For verifiable RL, the data product is a task plus a method of judging an attempted answer. A useful task record includes:

- The prompt and source provenance, including figure or document dependencies
- An answer schema, units and tolerance where meaningful
- A reference answer or hidden test suite, with evidence for its correctness
- Parser and verifier versions, resource limits and adjudication status
- Split/family identity, construction history and contamination checks
- Known ambiguity and counterexamples that attack the evaluator

The [Big-Math paper, version 1](https://arxiv.org/html/2502.17387v1), illustrates task production aimed at checkable closed-form answers. Filtering and reformulating questions changes the task distribution. A collection that excludes proofs, missing diagrams or ambiguous multipart tasks may be easier to score automatically while covering less of mathematical practice. The released verified data are tasks and answers, not a corpus of teacher rollouts. The model-specific solve-rate column should remain tied to its model and sampling procedure; it is not an intrinsic difficulty constant.

SFT and RL expose a verifier to different pressures. Filtering a fixed collection checks already generated outputs. An optimizing policy can repeatedly seek outputs that earn reward while exploiting a parser or incomplete test. This is a design inference, not a new experiment in this book. The practical response is to test the verifier itself before allowing a model to optimize against it.

## Write the adversarial test before the reward loop

Use an authored example such as “Return exactly one reduced fraction equal to one half, as numerator/denominator.” The allowed output contract must say whether `2/4`, a decimal, prose, multiple answers or extra text are acceptable. Mathematical equivalence and format compliance are separate judgments. Avoid a verifier that merely looks for the substring `1/2`; it may reward “The answer is not 1/2.” Avoid executing arbitrary answer text with `eval`.

A verifier test suite should include:

- Known correct forms allowed by the declared contract
- Known wrong answers one digit, sign, unit or inequality away
- Multiple competing answers and correct tokens embedded in incorrect prose
- Empty, malformed, excessively long and adversarially nested expressions
- Reference answers that are missing, inconsistent or ambiguous
- Timeouts and parser failures recorded distinctly from mathematical mistakes

Report false acceptance and false rejection with counts, denominators and the kinds of tasks tested. A perfect result on a small suite means that suite passed. It does not certify arbitrary mathematics. Keep challenge tests hidden from training when their secrecy is part of the evaluation design, and replace exposed holdouts rather than repeatedly tuning to them.

[Math-Verify 0.9.0, released January 2026](https://pypi.org/project/math-verify/0.9.0/), is a concrete versioned evaluator to investigate after the basic exercise. Its [official documentation](https://github.com/huggingface/Math-Verify) separates answer extraction from equivalence checking and documents asymmetric comparison behavior. Pin parser dependencies and settings as well as the top-level package. This book has not installed or benchmarked it; the citation establishes a research path, not a proof-checking guarantee.

## Distilling actions requires the state the student will see

The earlier text/tool-environment chapter defines reset state, observations, actions, results and termination. Use that common contract here, then decide which behavior the student should imitate: the next action, an entire continuation, a successful policy or a recovery after failure. These choices produce different targets. A complete logged trace is not automatically a well-formed next-action example.

Keep privileged teacher information separate from student-visible input. An expert may know a hidden simulator state that the deployed learner cannot observe. Providing it during training without a corresponding deployment channel changes the problem. In robot data, camera/action alignment and calibration matter; in CAD, an operation can reference geometry created earlier. Preserve the dependencies needed to replay or interpret the target.

Stepwise imitation accuracy can conceal a rollout problem: a student's early mistake takes it to states absent from expert demonstrations. The [DAgger paper, AISTATS 2011](https://proceedings.mlr.press/v15/ross11a.html) explicitly studies the induced-distribution issue in imitation learning. This motivates a later research exercise involving recovery states and rollout evaluation; it does not authorize automatic relabeling or assert that DAgger was run here. Human demonstrations also need not be optimal policies.

Retain failures according to the task contract. A timeout, malformed action, unauthorized action and unsuccessful plan are different events. For the existing text-training companion, the assistant-ending prefix and target-turn mask still apply. For a new robot or CAD adapter, specify the emitted representation and test its consumer before calling the trace ready for training.

## Choose a small acquisition route

Start with authored tasks and the public paper/card examples. OpenThoughts3's pinned card advertises Apache-2.0 but approximately 28.2 GB of download bytes; inspect its viewer before electing to stream a bounded sample or acquire shards. Keep any sampled rows tied to the pinned revision and question families. A streaming API limits materialization, not necessarily total transfer unless iteration is explicitly bounded.

[Big-Math-RL-Verified's public card](https://huggingface.co/datasets/SynthLabsAI/Big-Math-RL-Verified) is readable, but its files currently require login, conditions and contact-information sharing. That gate was not accepted in this research. It is unsuitable as an account-free beginner default. If access is later authorized, retain the accepted terms, immutable revision and file hashes; do not substitute the unverified variant under the same lesson title.

**Try it.** Write an answer contract and ten expected verifier outcomes before writing code. Include two mathematically equivalent forms, two incorrect near-matches and two cases that should go to adjudication. Then explain which failures a trained model could exploit. This exercise is proposed; the executed release lab elsewhere in the book does not claim to run a reasoning trainer or a math verifier.
