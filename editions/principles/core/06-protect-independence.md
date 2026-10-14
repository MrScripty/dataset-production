# 6 Protect independence and evaluation

*Dataset Production · Puma · Part 2: Evidence you can trust*

## A beginner's failure: the exam contains a relative of the practice question

A student practices “Please send my invoice,” then answers the same request in capitals on an exam. The answer may be correct, but it tells us little about a new request. A dataset can create this illusion without exact duplicate rows: one crop from an image is in training and another crop is in test; one step of a trajectory is in training and the next is in test.

After chapters 2 and 5, you know what the claim is and which source relations cleanup can reveal. Here you will choose split units that match the claim, connect overlapping relationships, and record how evaluation has been exposed. Your goal is defensible independence, not an attractive split percentage.

## The principle: separate the information the claim says must be new

**Independence** is relative to a generalization claim. If the claim concerns new messages from familiar customers, customer identity may be permitted across splits while duplicate message families are not. If the claim concerns new customers, hold out customers. For new recording sessions, hold out sessions; for new speakers, hold out speakers. A source reused in retrieval may be intentionally searchable while query judgments remain held out. Name the allowable shared information.

A **split unit** is the group assigned as a whole to one role. A protected relationship says two records must not cross split roles for the chosen claim. Some relationships describe source identity, some derived ancestry, and some shared experimental conditions. A row is often too small a unit.

Store semantic roles: training, development/model selection, calibration when needed, and final evaluation. An adapter may rename these `train`, `dev`, `validation`, or `test` for a consumer. A convenient filename does not decide its epistemic role. If data influence construction choices, they are development evidence regardless of their name.

## A small worked connected-family example

**Authored fixture source with executed grouping snapshot.** r01 has family-01 and the ordinary invoice request. r02 has family-02 and its case/spacing variant. r03 also has family-02 and asks for a receipt. r01 and r02 share canonical text; r02 and r03 share a declared family.

Draw an edge r01–r02 and another edge r02–r03. All three are connected. A **connected component** is the set reached by following any protected edge, even if its outer records have no direct link. Therefore r01 and r03 must share the split. Comparing only the surviving canonical example's chosen family ID would lose r02's bridging relationship.

Another fixture chain connects r04 and r05 by source ID, and r04 and r06 by canonical text. Both chains illustrate why grouping must retain every accepted origin before final split assignment. One declared family field is not sufficient when different relations overlap.

The builder connects shared canonical IDs, source IDs, and family IDs transitively. Its recorded snapshot has 21 leakage groups. Under the supplied seed it assigns 12 groups to training, 4 to development, and 5 to test, containing respectively 12, 5, and 7 canonical examples. Group proportions are not guaranteed row or class proportions. The code does not use gold to allocate groups.

The snapshot's quantities are executed-fixture descriptions from the source increment identified in chapter 1. They do not prove that human-declared families captured all unknown relationships. A new run requires its own manifest. A tiny test with five declared groups cannot establish broad customer generalization, particularly when its public answers have been studied.

## The theory: constraints can overlap transitively

**Authored illustration.** Book A appears in sessions 1 and 2. Book B appears in session 2. A claim requiring both new-book and new-session independence must keep all those examples together. Grouping only by book would break session independence; grouping only by session would break book independence.

Construct a graph: nodes are source records or their stable examples; edges are protected relations under the contract. Components are indivisible split units. Descendants inherit the component assignment before crops, paraphrases, frame pairs, or segments are expanded. A shared class such as “English” is not automatically a protected edge, or it would merge the whole dataset. The contract determines which relations matter and why.

Sometimes the graph produces one large component. Then a requested 80/10/10 split may be impossible without leakage. Accept a different ratio, narrow the claim, or acquire more independent components. Do not delete edges simply to improve the percentages. Report group counts, row counts, and coverage by split separately.

### Four holdout questions

- **Entity holdout:** can the release support new people, customers, objects, sites, or documents? Group the chosen entity and its descendants.
- **Temporal holdout:** can it support later decisions using information available at the time? Train on earlier periods and evaluate later ones, respecting feature availability and overlapping windows. A random timestamped split is not a future-use test.
- **Seed holdout:** can a generated or simulated procedure handle fresh randomness or initial states? Keep descendants of the same seed or generated parent together; record exactly what the seed controls.
- **Regime holdout:** can it handle a different condition, such as an operating range, boundary rule, sensor, or source domain? Holding out a condition tests that declared condition, not every unseen regime.

These can be combined. A fresh seed under familiar physics is not a new-physics test. Different filenames may still share an initial state. A later frame may reuse earlier trajectory information. Adjacent video frames, related conversations, trajectory steps, and repeated seeds require a claim-specific relationship record.

### Counting rows does not count new evidence

Suppose 12 independent trajectories yield eight frames each. There are 96 frames and at most 12 trajectory units, possibly fewer if trajectories share protected seeds or conditions. Ninety-six is the row count, not the count of independent new trajectories. This is an authored counting illustration, not a Rheon result; project-specific quantities require pinned run evidence.

For uncertainty, resample or aggregate meaningful groups rather than treating frames as independent. A simplified equal-group design effect can illustrate the risk: with m rows per group and within-group error correlation rho, D ≈ 1 + (m − 1)rho. Here D is the approximate variance inflation relative to independent rows. For 1,000 rows in groups of five and rho = 0.3, D = 2.2, yielding an illustrative effective size near 1,000/2.2 ≈ 455. This model assumes an equal-group correlation structure; it does not magically determine the real dataset's effective sample size. Group-aware evidence is preferable to plugging guessed values into a formula.

## Protect evaluation from the whole production process

Leakage includes more than training rows. Final-test source documents used to generate new questions, known answers copied into rule design, and detailed evaluation feedback used repeatedly to select releases all expose the test. A benchmark decontamination matcher that finds no string overlap cannot prove the absence of these paths.

Keep an **evaluation exposure ledger**: evaluation identity/version, protected families, who or what saw inputs or references, when, which summaries or failures were inspected, and what decisions they influenced. Aggregate feedback can still influence selection. If developers use it to choose a recipe, record that fact.

The remedy is not renaming `test` to `test-new` or reshuffling inspected families. Reserve genuinely new independent material before a fresh final claim, freeze the procedure, and apply it once under the declared protocol. If new material is unavailable, narrow the result to descriptive performance on exposed data. This fixture is deliberately exposed; treat its split check as a demonstration of known grouping, not a private final exam.

Primary Tülu 3 material [R07] discusses practical lexical decontamination and the limits of embedding similarity. The transferable lesson is to combine source relationships, explicit benchmark/version checks, and reviewed match evidence, not to call every semantically similar pair a leaked paraphrase.

## Controlled exercise: assign whole components

**Evidence status:** authored graph exercise, using the fixture's documented relationships. **Unit:** a connected protected component. **Denominator:** component counts for allocations; canonical-example counts are reported separately. No model is fit.

Use these invented records: A and B share normalized text; B and C share source; C and D share family; E and F share trajectory; F and G share seed; H has no declared relation. All named relations are protected for this exercise.

1. List components and assign them to training, development, and test without overlap.
2. Explain why A and D cannot be split apart even though they share no direct edge.
3. Suppose H was inspected to select your rule. Record its current evaluation role.
4. Describe a new entity holdout, a temporal holdout, and a new-seed holdout in ordinary language. State what each cannot establish.
5. Add eight frames to each trajectory record E and F. Explain why that expansion does not create sixteen independent trajectories.

### Acceptance check

Pass if every protected edge and its transitive component stay in one split, the generalization claim matches the chosen unit, and exposure is honestly recorded. Reject any protected family crossing splits. Revise claims inferred from row percentages without group counts. If H influenced selection, it cannot remain an untouched final holdout.

### Worked answer and reviewer guidance

The components are {A,B,C,D}, {E,F,G}, and {H}. One valid paper allocation is training, development, and test respectively. Many assignments are possible, but there are only three independent components under these constraints, making any performance estimate extremely limited. A–B–C–D is a connected chain, so A and D must move together.

After inspecting H to select a rule, H becomes development/exposed evaluation material. A new untouched holdout must come from an independent component absent from the selection loop. Entity holdout supports the chosen new-entity claim under its measured conditions; temporal holdout supports later-time conditions observed, not arbitrary future drift; fresh-seed holdout tests the same generator/regime with new randomness, not a new regime. Extra E/F frames remain related by their trajectory and seed component.

A reviewer should draw each edge, check the components, and ask the learner to describe what information the future consumer may already know. A technically valid component algorithm cannot rescue the wrong generalization claim or incomplete ancestry records.

## Optional technical details and reading

An implementation may use union–find to compute components, but the paper graph is the core idea. Test every protected relation against final emitted split files, not just an intermediate graph. Changing or adding sources can change a content-derived component ID and allocation; reproducibility of one frozen release is different from an append-stable split service. The supplied lab is reproducible, not append-stable. Read [Tülu 3](https://arxiv.org/html/2411.15124v1) [R07] for the published production example, keeping its reported experimental scope separate from this exercise.
