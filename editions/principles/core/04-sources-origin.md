# 4 Choose sources and preserve their origin

*Dataset Production · Puma · Part 1: A first useful release*

## A beginner's question: where did this example come from, and may we use it?

You can read a webpage without logging in. Does that make its contents yours to redistribute in a training dataset? No. Public access and permission to reuse are separate questions. Equally, a dataset assembled with an openly licensed tool does not inherit that tool's license for every imported source.

After chapters 2–3, you know the task and representation. Here you will explain source selection, preserve a path to original bytes, and document the permission basis for the intended use. The main exercise uses the authored helpdesk fixture. An external-source worksheet can remain a document-reading exercise without downloading or processing any data.

## The principle: selection shapes coverage; provenance makes decisions traceable

A source is not a neutral bag of rows. Choosing one channel, language, device, institution, or time period selects some parts of the intended population and misses others. A clear task should therefore guide acquisition before a large collection makes the omission expensive.

**Provenance** records where material originated and how it reached an example. **Lineage** describes its transformations and dependencies. Neither grants permission. A perfect hash of an unauthorized source still identifies unauthorized bytes. A permission record without source identity may not tell you which bytes it covers. Preserve both evidence paths.

For this teaching release, messages are fictional and newly authored. That avoids pretending a real helpdesk or its customers supplied them. It also limits the claim: fictional coverage is not measured deployment coverage. The source README states that the repository has no declared license at the time of the lab. This chapter does not grant a license, establish ownership, or authorize redistribution. Document rights for the actual use before sharing a release externally.

## A small worked source-to-output trace

**Authored fixture material with executed release structure.** r02 comes from an input line containing its ID, source ID, family ID, and original text. Its text is normalized to the same comparison form as r01. The canonical example refers through lineage to both origins.

To trace it back, preserve:

1. The acquired input bytes and a source locator or local filename.
2. The line number and exact raw line, including its line ending.
3. The original text and source/family IDs.
4. The normalization recipe and runtime-dependent character version.
5. The canonical example ID and its release/split assignment.
6. The source and release rights records, with the use they cover.

The lab's raw snapshot copies the acquisition file byte for byte. Its lineage retains hashes and an encoding of the raw line. If a reader disputes the normalization, these records let them compare the output with what actually arrived. Keeping just “please send my invoice” would not reveal the tab, spacing, or second origin.

The recorded fixture input has SHA-256 `6f5c21ce6e70abb56712fa0e5b6058cc678579564d9a36e22d6898af0d79071e`. The separately authored references have SHA-256 `203a8bb1ed213d2a61520717adc04fdfab654dc5b6eabd3a4de63337b9c76176`. Source increment `416c4b12ad2b9649c2c38bad4d2c7ed5f77eac5f` identifies the lesson's source evidence. Retain your run's manifest as well; source identification is not a claim that every later copy or modified recipe has been executed.

## The theory: rights have several dimensions

A worksheet should separate the intended operations rather than reducing them to one checkbox:

| Question | Evidence to retain |
|---|---|
| Who supplied or owns the source, and under what basis? | Source, author/provider identity where appropriate, exact terms or permission record, date/version |
| May it be used for the proposed training or evaluation task? | Scope of permitted purpose, relevant restrictions |
| May it be transformed? | Permission for derivatives, annotation, resizing, extraction, or translation as relevant |
| May bytes or excerpts go to an external processor? | Recipient, purpose, retention terms, approved data scope |
| May the release redistribute source or derived records? | Distribution scope, attribution, downstream conditions |
| What retention or withdrawal obligations apply? | Retention period, correction/deletion process, dependencies |
| Does it contain identifiable or sensitive material? | Necessary privacy review and safeguards; avoid collecting unnecessary details |

Source licensing, software licensing, model licensing, endpoint terms, and release licensing answer different questions. A model provider allowing an API call does not automatically authorize every input upload or every downstream use of its output. A dataset's name and an unchecked summary card are not substitutes for the actual governing terms.

Use explicit states such as `cleared_for_this_use`, `restricted`, `unresolved`, or `blocked`, with supporting evidence and reviewer. “Unknown” is not “allowed.” Material with unresolved rights remains outside a distributable release until the intended use is resolved. For sensitive, contractual, regulated, or high-impact situations, obtain appropriate organizational or legal review. These are operational practices, not legal advice.

An external-processing preview should name which bytes leave the system, the recipient, purpose, and permission basis. Credentials never belong in dataset payloads, examples, exports, or provenance logs. A source contract may be traceable without storing unnecessary personal information.

### Keep distinct objects so corrections can travel

A compact data system can be understood without a database product:

- An **asset** identifies source or derived bytes, their modality and dimensions/duration.
- A **task contract** defines input, target, guide, and validation.
- An **example revision** selects inputs and a target under that contract.
- An **annotation event** records who or what proposed, edited, accepted, or rejected a judgment.
- A **verification run** records checks, versions, inputs, and outcomes.
- A **family relation** links sources that must remain together for a stated claim.
- A **recipe run** records frozen inputs, settings, outputs, and failures.
- A **release** freezes selected revisions, splits, hashes, and reports.
- An **export** adapts a release to one exact consumer, with tests and version.

A nonempty target is not evidence of review. A resized mask in an export should not overwrite its source annotation. A second task can share an asset while creating a separate example revision. These distinctions make later corrections possible.

If a source label changes, descendants can be rebuilt under new revisions while old releases remain identifiable. A rights withdrawal may require stronger action, including restrictions or deletion across retained sources, exports, indexes, caches, and backups according to the applicable obligations. Previously downloaded files and trained weights do not disappear when a local row is removed. State what the system can enforce and what remediation remains outside it. Do not promise global erasure from a local action.

Versioned storage makes logical deletion and physical removal different. The legacy bibliography's [lakeFS retention guide](https://docs.lakefs.io/data-retention/) [R06] illustrates this distinction; moving documentation describes a product at a checked version, not a verified implementation for this project.

## Controlled exercise: an acquisition and rights worksheet

**Evidence status:** authored fixture inspection; proposed work for any optional external acquisition. **Unit:** the source collection and one traced output example. No download, upload, redistribution, or license acceptance is part of this paper exercise.

Complete these fields for the helpdesk fixture: source locator, bytes identity, acquisition method, population represented, known omissions, intended use, transformation permission basis, redistribution basis, external-processing basis, retention plan, rights state, and unresolved questions. Trace the invoice example to r01 and r02. Do not infer a grant from the fictionality of its messages.

Optionally choose one primary dataset or source documentation already listed in the book's references. Read its stated terms and format and complete the same worksheet for a proposed use. If terms, authority, or scope are not available, write unresolved and identify what evidence would be needed. Choosing an optional source does not authorize acquiring or sharing it.

### Acceptance check

Pass when a reviewer can locate the exact source bytes, reproduce the trace, identify the permission basis or unresolved issue for each intended operation, and explain one coverage omission. Unknown permissions must block external distribution. Reject “public website,” “fictional,” or “open-source tool” used alone as a sufficient redistribution grant.

### Worked answer and reviewer guidance

For the fixture, the locator is `examples/first-release/data/records.jsonl`, with the hash above; acquisition is authored teaching JSONL, not scraping. The represented population is the fictional messages, not a sampled customer base. Important omissions include languages, real conversational context, and measured operational outcomes. Normalization follows the recorded recipe, and r01/r02 remain available in raw/lineage evidence.

The intended use in this lesson is inspectable teaching and local reproduction under the permissions actually applicable to the repository. The README supplies no declared license. Redistribution, an external provider upload, or a commercial deployment therefore cannot be marked cleared merely from this lesson; record the missing grant and seek the appropriate permission. Retention includes source bytes needed for reconstruction and authored references needed for audit, subject to the resolved rights. For real private sources, retention requires a justified scope rather than copying everything indefinitely.

For an optional external source, there is no universal worked “allowed” answer. A complete unresolved worksheet is better evidence than an invented grant. Reviewers should inspect the governing source and the learner's use description, not assume that research access covers commercial redistribution.

## Part 1 assessment: a one-page release card

Submit one page covering the chapter 2 claim and unit, chapter 3 contract, this chapter's source and rights, permitted use, proposed baseline and metric, and one known weakness. State which fields describe the executed fixture and which describe proposed work. Include a lineage trace for one example.

**Worked card.** “Authored English helpdesk messages; one message is the routing decision unit. Fixed keyword rules propose billing/access/technical or abstain/conflict under the fixture guide. Case/spacing-normalized text is the consumer input; weak labels are proposals, and reference judgments remain evaluation-only. Source: the identified JSONL and separately authored reference file. No independently reviewed customer study is claimed. Local teaching/reproduction is the purpose; external redistribution rights require an explicit basis. The fixed rules provide a descriptive baseline: 14/24 coverage and 10/13 agreement on scorable predictions in the retained executed fixture. New real conversations, other languages, refund authorization, and model reliability are outside the claim. Known weakness: keyword context can misroute ‘charge indicator’.”

**Reviewer guidance.** Pass if a reader can explain each sentence in ordinary language and identify the missing evidence for deployment or redistribution. Revise a card that hides the unsupported rights or replaces the denominator with a headline percent. Reject an invented experiment. No model choice is needed to pass this part.
