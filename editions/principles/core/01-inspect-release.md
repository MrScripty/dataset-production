# 1 Inspect and reproduce a small release

*Dataset Production · Puma · Part 1: A first useful release*

## A beginner's question: what have we actually made?

A helpdesk receives “Please send my invoice.” Someone puts it in a file beside the word “billing.” Is that a dataset? It could be the beginning of one. But a second person still needs to know what the word means, where the message came from, whether it was copied, and how the answer was obtained. If those decisions disappear, the file can teach the wrong lesson while looking perfectly tidy.

This chapter is a guided preview. You will follow one message through a small release and inspect an error. You do not need to understand every production technique yet. Chapters 2–8 explain the decisions you encounter here. No model, GPU, account, sensor, paid service, or downloaded dataset is needed. You can complete the main path on paper.

The supplied fictional helpdesk has three queues: **billing** for money and billing documents, **access** for getting into an account, and **technical** for concrete software/interface failures. These are task conventions for a teaching collection. They are not universal rules for every company. Our eventual **input** is the message a consumer reads; our **target** is the queue the task says should own its reported problem.

## The principle: a release is decisions plus evidence

A **source record** is what arrived. An **example** is a task-specific interpretation of source material. A **label** is an answer supplied under some procedure. A **release** is a fixed selection of examples and supporting files that another person can inspect or consume. These distinctions matter even in a folder containing only a few dozen messages.

Keep the source, the interpretation, the judgment, and the evidence distinct. Then a mistaken judgment can be corrected without pretending the original source said something different. A file's existence proves little; an understandable record of how it was produced gives the reader something to check.

### Evidence labels used throughout this book

Every result needs a status. Use these labels when doing the exercises:

- **Authored illustration:** invented values, messages, diagrams, or arithmetic used to explain a method. They are not observations of real customers or systems.
- **Executed fixture:** output recorded from running a supplied teaching program on its supplied inputs. It establishes those checks for those inputs and recipe.
- **Independently reviewed reference:** a judgment with a documented independent review process. This status requires evidence of the review; a filename such as “gold” does not confer it.
- **Reproduced experiment:** a new run of a declared experiment with its inputs, versions, procedure, and outputs retained. Record departures from the original experiment.
- **Published result:** a result reported by a cited primary source, bounded by its setup and assumptions.
- **Proposed work:** a suggested change or experiment that has not established an outcome.
- **Unrun work:** a described procedure or code path that has not been executed in the reported evidence.

The lab's `gold.json` contains **separately authored references**, not independently reviewed references. Both its messages and references are teaching material. Its audit is an executed fixture. When you calculate a fraction from that audit, identify the input counts and call your calculation descriptive fixture arithmetic. When you rerun the lab, keep your own run evidence before calling it a reproduction.

## Follow the invoice message

**Authored fixture source.** Record r01 contains “Please send my invoice.” Record r02 contains the same request in capitals, with extra spaces and a tab: “  PLEASE\tSEND my invoice.  ” Here `\t` describes the tab; it is not a word in the request.

For this task, the builder intentionally ignores case and repeated whitespace. It creates a **comparison form**, `please send my invoice.` Both records share that form. It therefore emits one distinct example. This is **deduplication**: identifying repeats and deciding how to represent them. It keeps both original records in **lineage**, the history connecting an output to its sources.

The comparison form is also the model-facing text in this simplified lab. That choice would be inappropriate for some other tasks; chapter 3 will explain the contract, and chapter 5 will examine what normalization erases.

A fixed rule sees the whole word “invoice” and proposes billing. This is a **weak label**, meaning a fallible procedure supplied a candidate answer. No classifier has learned anything. A present weak label does not mean a person approved it.

The example receives a **split**, a role in later learning and checking. Training material may teach a model. Development material may influence choices. Test material is reserved for a final check under a stated protocol. Related sources stay together: r01 matches r02, while r02 shares a declared family with r03, “Please email a receipt.” All three source records belong to one protected group. You do not need the grouping algorithm yet; the important idea is that a familiar relative should not masquerade as a new test.

Finally, a **manifest** records the recipe and file fingerprints. A hash is a compact fingerprint of bytes. It helps notice a change. It does not prove the bytes are correct, lawful, or written by a particular author.

## Inspect three failures rather than hiding them

The supplied rules are deliberately limited.

1. “I was charged twice for renewal.” receives no vote because the billing rule recognizes “charge,” not “charged.” This is an **abstention**.
2. “The login animation crashes.” attracts access and technical votes. This is a **conflict**; the aggregate supplies no answer.
3. “The charge indicator stays at zero.” receives billing because of “charge,” while its authored reference is technical. This is a labeled mistake.

Abstention, conflict, and incorrect prediction are different outcomes. Deleting all difficult messages would conceal a coverage problem. Guessing labels for all of them would conceal uncertainty. Retaining them makes the weakness inspectable.

The reference file has its own problems: r27 and r28 collapse to one example but have contradictory reference categories, while r12 and r20 have no references. The audit excludes unresolved references from agreement scoring and reports them. It does not let the weak rule settle the reference dispute.

## The theory, in ordinary counts

**Executed fixture snapshot.** The retained audit at `examples/first-release/expected/audit.json` reports 30 input lines, 28 accepted raw records, and 2 quarantined lines. Quarantine holds rejected material and reasons rather than silently dropping it. One line has broken JSON; another lacks the required family ID. The 28 accepted records become 24 distinct normalized examples because four repeated records collapse.

Of those 24 examples, 14 receive a weak label, 5 abstain, and 5 conflict. The accounting check is 14 + 5 + 5 = 24. Label **coverage** asks how much receives an answer: 14 / 24 ≈ 58.3%. Agreement asks whether scorable supplied answers match references. Only 13 of the 14 predictions have a resolved reference; 10 match. Agreement is 10 / 13 ≈ 76.9%.

Those quantities have different **denominators**, the totals below each fraction. Coverage concerns all eligible examples. Agreement concerns only predictions that can be scored. Neither describes reliable routing of future real customers. The collection is small, authored, and publicly inspected. Its test split is exposed teaching material after you study it.

The recorded source increment is `416c4b12ad2b9649c2c38bad4d2c7ed5f77eac5f`, merged in `ac62387a3a9760e3f1e9f8b8290552cb2dc13471`. The expected audit's SHA-256 is `96fa6e02cf575fe5aa768cf61275b204a8fc68d8cbddbe7169086269e09bee54`. These identify the evidence snapshot used for the lesson. A changed implementation needs its own run record; these identifiers are not a receipt for untested rewritten instructions.

## Controlled exercise: trace, classify, explain

**Evidence status:** paper inspection of authored fixture material and descriptive calculation from the executed fixture snapshot. **Observation unit:** a raw source record when tracing origin; a canonical example when counting labels. **Requires no execution:** all six steps below.

1. Draw the path r01 and r02 → one comparison form → one billing proposal. Write where both originals remain.
2. Explain why r03 must share the split even though its words differ.
3. Classify the three failure examples as abstention, conflict, or wrong label.
4. Account for all 30 arriving lines and all 24 canonical examples.
5. Calculate coverage and agreement, naming each denominator.
6. Write one supported claim and one claim the fixture cannot establish.

### Acceptance check

Pass when another reader can recover both invoice originals, tell a proposal from a reference, account for every line and example, and explain why 10/13 differs from 14/24. Revise if any difficult case disappears without a reason. Reject a claim of real-world model accuracy: no such model or independent customer sample has been measured.

### Worked answer and reviewer guidance

The originals remain in raw input and accepted lineage. r01 ↔ r02 ↔ r03 is a connected relationship, so splitting r03 away would expose family information across splits. The three failures are respectively abstention, conflict, and a labeled error. Raw accounting is 28 + 2 = 30; canonical status accounting is 14 + 5 + 5 = 24. One predicted example has conflicting references, leaving 13 evaluated predictions. Ten agree.

A supported claim is “this fixture's fixed rules label 14 of 24 canonical examples.” An unsupported claim is “the future helpdesk model routes 76.9% of real messages correctly.” A reviewer should ask the learner to explain both fractions without using the vague word “quality.” Exact terminology matters less than preserving the distinction.

## Optional CPU reproduction and deeper reading

From the repository root, with Python 3.10 or later, run:

~~~sh
python3 -B examples/first-release/build.py --out run-first-release
python3 -m json.tool run-first-release/audit.json
python3 -B -m unittest discover -s tests -p 'test_first_release.py' -v
~~~

Choose a new or empty output directory. The program refuses to overwrite existing contents. No package download is required. Retain the audit, manifest, command, input hashes, runtime/Unicode version, and test output. If counts differ, compare versions and inputs before interpreting the difference. A passing suite checks specified behavior, not all possible data errors.

Inspect `raw/records.jsonl`, `lineage.jsonl`, `quarantine.jsonl`, and `manifest.json` in the resulting release. The [lab README](../../../examples/first-release/README.md) describes fields and limitations. Measurement's distinction between a construct and its operationalization is developed in Jacobs and Wallach, [Measurement and Fairness](https://arxiv.org/html/1912.05511v3) [R01]. Chapter 2 makes that idea usable before any model choice.
