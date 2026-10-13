# 5 Extract cleanly without erasing evidence

*Dataset Production · Puma · Part 2: Evidence you can trust*

## A beginner's failure: the clean sentence says the opposite

A page contains “I do not want you to refund this payment.” The extracted record says “I want you to refund this payment.” It is shorter, grammatically plausible, and valid text. The intended meaning has been reversed. No later hash, split, or model can recover the lost “not” from the cleaned sentence alone.

Chapters 3–4 established representation and origin. Here you will preserve meaning while extracting and normalizing records, find the first incorrect representation in a chain, and retain disputed material for review. You will also distinguish repeated record identifiers from duplicate text. The main exercise uses supplied strings; running code is optional.

## The principle: cleanup is a task-dependent transformation

**Extraction** selects the content intended as input. **Normalization** gives selected content a consistent form. **Deduplication** identifies repeated examples and decides how they are represented. Each can change what a future consumer sees. “Clean” is not a universal property: a transformation is defensible when its changes preserve the task's relevant distinctions or deliberately alter them under a documented contract.

Preserve source evidence and transformation reasons. A normalized output usually cannot reconstruct the original spacing, letter forms, or surrounding context. **Reversible lineage** means retaining enough origin and recipe information to reconstruct or reconsider a derived record, not claiming that every lossy transformation has a mathematical inverse.

## Small worked example: find the first wrong representation

**Authored illustration.** The task is to route the customer's request, not classify a webpage's navigation. The source is:

~~~html
<nav>Pricing | Invoice help | Contact</nav>
<article>
  <h1>Customer request</h1>
  <p>I do <strong>not</strong> want you to refund this payment.</p>
</article>
~~~

A broken extractor selects only direct text nodes of the paragraph and loses the nested `strong` element. Its output is “I do want you to refund this payment.” A later normalizer lowercases and collapses spaces. A later rule proposes billing.

Where did the first error occur? At extraction. The source contained the negation; the extracted message did not. Normalization did not cause that loss, and billing might still be the same routing owner for both sentences. An intent task would expose the opposite target. This is why an audit must check source meaning under the task, not merely whether the final routing label changed.

Another crude extractor joins all visible text, yielding “Pricing Invoice help Contact Customer request I do not want you to refund this payment.” It keeps negation but adds irrelevant navigation. Removing every occurrence of “invoice” is not an appropriate repair: a customer may actually report a broken invoice page. Select content using source structure and task evidence, then inspect failure cases.

A before/after record should retain the raw page, extracted request, comparison text, recipe/version, and reasons. If source structure is ambiguous, quarantine or flag the record rather than inventing a confident interpretation.

## Normalization deliberately creates equivalence classes

A recipe groups strings it treats as interchangeable. The set of strings sharing one comparison form is an **equivalence class** under that recipe. For routing, the fixture treats case, some Unicode forms, and whitespace differences as irrelevant. Thus r01 and r02 share `please send my invoice.`

The lab's documented sequence is:

1. Unicode NFKC compatibility normalization.
2. Unicode case folding.
3. NFKC again.
4. Collapse whitespace runs to one ordinary space and strip outside whitespace.

Unicode encodes written characters. NFC joins canonically equivalent ways of writing a character, such as an accented letter versus a letter plus combining accent. NFKC additionally merges some compatibility forms, such as fullwidth Latin letters. Case folding removes case distinctions. The second NFKC step normalizes combinations introduced by folding. The original remains important because those operations lose information.

**Authored illustration.** A fullwidth “Ｐｌｅａｓｅ” can normalize to “please.” Composed `é` and `e` plus a combining acute accent should converge under appropriate canonical normalization. But changing a mathematical superscript or case-sensitive program identifier may erase a distinction the task needs. `US` and `us` can have different meanings; a chemical symbol or identifier may depend on case. Unicode's [normalization specification](https://www.unicode.org/reports/tr15/tr15-57.html) explicitly distinguishes canonical and compatibility forms. Naming a standard is not enough; state why its mergers are acceptable for your task.

### Test stability without confusing it with validity

Let N(x) mean the normalized form of source string x. **Idempotence** means N(N(x)) = N(x): normalizing an already normalized value changes nothing. Explain x as the input string and N as the recipe before using the equation. This property matters when pipelines normalize more than once; an unstable key can create different IDs or duplicate decisions at different stages.

Idempotence is necessary for this comparison policy, but not proof of semantic safety. A recipe deleting every occurrence of “not” could be perfectly idempotent and profoundly wrong. Pair the stability test with preservation tests for punctuation, negation, meaningful symbols, and task-specific distinctions.

For the invoice pair, N(x) is `please send my invoice.` and applying N again leaves it unchanged. For the refund pair, “Please refund this payment” and “Please do not refund this payment” remain distinct because the recipe keeps negation. Similarity does not justify collapsing them.

## Two different duplicate problems

**Duplicate text** can be legitimate repeated acquisition. Different IDs can describe the same normalized message; the builder emits one canonical example while preserving every accepted origin and relationship.

**Duplicate record IDs** are an integrity ambiguity. An ID is supposed to name one source record. If the same ID names different text or origins, choosing the first or last occurrence makes input order determine which evidence survives.

The policy for this edition is **quarantine the whole duplicate-ID family**: every occurrence carrying the repeated identifiable ID stays out of accepted examples, with raw bytes, line numbers, and reasons retained. This does not mean automatically quarantining all semantically related messages or every member of the split component. It means all occurrences of the ambiguous identifier. Investigate related lineage as needed; do not invent a winner.

The corrected lab's safe-ID rule reserves a valid, unambiguous ID in a strictly decoded object even if another field is invalid. Suppose a valid row has ID `q01`, and another strictly decoded object also has ID `q01` but lacks a family field. The invalid object still creates identifier ambiguity, so both are quarantined. Undecodable input or an object with duplicate JSON keys has no safely identifiable ID for this purpose; its raw bytes are quarantined without guessing an identity. An invalid ID string likewise cannot become a trusted record identity. Gold referencing an unknown or quarantined record must fail the build rather than be silently reassigned.

**Authored policy test.** Put two records with ID q01 in either order: one otherwise valid, one missing `family_id`. The expected result is no accepted q01 occurrence. Put two valid records with different IDs but equal normalized text in either order: the expected result is one canonical example with both origins. These paper expectations are policy tests; call them executed results only after retaining a test run from the corrected implementation.

## Deduplication is evidence, not a universal removal rule

Raw-byte hashes find identical encodings. A canonical text key finds equivalence under its declared normalization. Decoded-media hashes, perceptual similarity, text shingles, and embedding similarity find other relations, with different false matches and missed matches. The fixture implements exact normalized-text equality only; it does not implement semantic or fuzzy similarity.

A near-duplicate candidate needs a decision: same example, same protected family, related but distinct, or unrelated under the claim. Counterfactuals can be almost identical yet require opposite labels. An exact-text duplicate with conflicting references is a reference problem to expose, not a cue to let a weak predictor choose the answer.

Lee and colleagues' primary [deduplication study](https://aclanthology.org/2022.acl-long.577.pdf) reports benefits under particular language-model experiments. It motivates checking duplicates, not indiscriminate deletion in every modality. The optional extraction study by [Trafilatura's author](https://aclanthology.org/2021.acl-demo.15.pdf) examines actual web content extraction; our nested-negation example is an authored diagnostic, not a reproduced extractor benchmark.

## Controlled exercise: preserve a disputed change

**Evidence status:** authored illustration and paper policy tests. **Units:** one source page per extraction judgment; one raw record per identifier check; one canonical message per text duplicate. No webpage extractor or model is run.

1. Record source, broken extraction, and normalized output for the nested-negation example. Mark the first lost evidence.
2. Write a correct extracted request and explain why navigation is excluded.
3. Compare a composed accented character with its decomposed variant, and fullwidth versus ordinary Latin letters. State which equivalences the routing recipe intends and one task where a merger is unsafe.
4. Test idempotence on the invoice comparison form. State why that test cannot establish meaning preservation by itself.
5. Classify the two duplicate cases above. Record accepted/quarantined status and retained evidence under both input orders.
6. Add a negation preservation check and a duplicate-ID check to your release worksheet.

### Acceptance check

Pass if source evidence survives, the first incorrect stage is identified, intentional equivalences are justified, and the whole duplicate-ID family is quarantined regardless of order. Revise a policy that names a normalization tool without its semantic scope. Reject first-row-wins or last-row-wins for ambiguous record IDs, or a claim that exact-text matching finds all semantic leakage.

### Worked answer and reviewer guidance

The nested “not” disappears at extraction; a correct extractor retains the paragraph's nested text as “I do not want you to refund this payment.” Navigation has a different source role and is outside the message input. Normalization may change case and whitespace, but retains negation. The invoice comparison form is unchanged by a second normalization. A code task is a valid counterexample to blanket case folding, and a symbol-sensitive mathematics task is a valid counterexample to compatibility mergers.

Both q01 occurrences are quarantined because two safely identified objects claim the ID. Raw bytes, reasons, and line numbers remain, including the otherwise valid row. Different valid IDs with equal normalized text may contribute to one canonical example, while their individual origins stay traceable. Undecodable bytes are preserved but not used to guess an ID. The reviewer should reverse record order and ask whether the decision changes; it must not.

## Optional technical checks

Run the supplied first-release tests and retain the implementation hash and results. Inspect the duplicate-ID regression covering an invalid sibling, Unicode combining marks, and gold independence. An implementation that has not passed the documented edge policy does not earn a publishable-release claim because its ordinary fixture counts happen to match. For a real extraction audit, sample ordinary pages as well as flagged failures and compare outputs with source evidence. Chapter 8 explains why a targeted three-page error hunt cannot estimate the error rate of every page.
