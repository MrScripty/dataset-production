# Extract normalize and audit what changed

The first lesson turned two differently written invoice messages into one example. That was safe only because we decided that case and spacing did not change the routing task. Now we will follow the same question further: when a source contains useful information mixed with clutter, how do we clean it without changing what it says?

There are three distinct operations. **Extraction** selects the content we intend to use. **Normalization** puts selected content into a consistent form. **Deduplication** finds repeated examples. A mistake at any stage can survive every later step, so “the file loaded successfully” is not a sufficient check.

## Extract the request rather than the entire page

Suppose a helpdesk exports this small page. Everything needed for the example is shown here; there is no website to visit.

```html
<nav>Pricing | Invoice help | Contact</nav>
<article>
  <h1>Customer request</h1>
  <p>I cannot reset my password.</p>
</article>
```

Our intended input is the customer's request. A crude extractor that joins all visible text might produce:

```text
Pricing Invoice help Contact Customer request I cannot reset my password.
```

The words “Invoice help” came from navigation, not the customer. They could mislead our billing rule or a later classifier. A task-aware extraction produces:

```text
I cannot reset my password.
```

The output is shorter, but shortness is not the goal. The goal is to retain the intended content and exclude irrelevant material. If the customer had written “The Invoice help page is broken,” those words would belong in the request and must stay. An extractor cannot safely solve the problem by deleting every occurrence of “invoice.”

Repeated navigation and footer material is often called **boilerplate**. Real webpages place content in many structures, so a rule that works on this tiny example needs testing on other page types. Trafilatura's [published extraction study](https://aclanthology.org/2021.acl-demo.15.pdf) evaluates that problem on actual webpages. It is a useful tool study, not evidence that any parser will identify your intended training content automatically.

## Keep three versions for three jobs

Consider the invoice record again:

| Representation | Value | Why keep it? |
| --- | --- | --- |
| Original source | `  PLEASE\tSEND my invoice.  ` | Evidence of what arrived |
| Extracted message | `  PLEASE\tSEND my invoice.  ` | The selected message, without unrelated source fields |
| Comparison form | `please send my invoice.` | A consistent key for this task's duplicate check |

Extraction changes nothing here because the JSONL field already identifies the message. That is an advantage of a clearly structured source. The original is still valuable: when the comparison policy is wrong, we can rebuild from it.

The supplied lab also uses the comparison form as its model-facing text. That is a deliberate simplification for case-insensitive helpdesk routing. Other tasks should keep a separate training representation. In code, `US` and `us` might name different things. In mathematics, `x²` and `x2` do not necessarily mean the same expression.

**Unicode** is the system used to represent written characters. Some visually similar characters have different encodings. NFC normalization brings canonically equivalent ways of writing a character, such as an accented letter or that letter plus a combining accent, into a common form. NFKC goes further and also merges certain compatibility forms, such as fullwidth letters. The lab uses NFKC; case folding removes case distinctions. A second normalization brings any new character combinations introduced by case folding back into a consistent form. Then the lab collapses whitespace. You do not need to memorize those names to understand the decision: this recipe intentionally treats some different strings as equivalent.

Unicode's [normalization specification](https://www.unicode.org/reports/tr15/tr15-57.html) warns that compatibility normalization can remove meaningful distinctions. That is why we preserve the original and explain the policy rather than simply naming it “clean text.” The tested lab includes a combining-mark regression because a superficially reasonable normalization recipe was initially unstable when applied twice.

## Decide whether a match is truly a duplicate

For our routing task, these two inputs can share one example:

```text
Please send my invoice.
PLEASE SEND MY INVOICE.
```

These cannot be collapsed merely because most words match:

```text
Please refund this payment.
Please do not refund this payment.
```

The extra “not” changes the requested action. **Exact matching** compares the chosen representation for equality. **Near-duplicate matching** looks for substantial similarity, such as shared phrases. It can find repeats that exact matching misses, but it can also nominate distinct examples like the refund pair.

A duplicate detector therefore supplies evidence for a decision. It does not decide the target's meaning. Keep the relation and the originals long enough to inspect disputed matches. The next sections of the assembled book explain how these relations also protect independent splits.

Deduplication can improve language-model training in specific experiments, as [Lee et al.](https://aclanthology.org/2022.acl-long.577.pdf) show. It does not follow that removing every similar record is always helpful. FineWeb2 studies both filtering and selective repetition; its [version-1 paper](https://arxiv.org/html/2506.20920v1) also shows why language-specific processing matters. Those findings motivate measured choices rather than a universal “remove more” rule.

## Audit a change by checking the source

An **audit** checks a sample of outputs against the evidence needed to judge them. Here is a completely worked, invented audit of three extracted requests. It illustrates how to count errors; it is not a run of a webpage extractor.

| Intended request in the source | Extractor output | Judgment |
| --- | --- | --- |
| I cannot reset my password. | Invoice help I cannot reset my password. | Wrong: navigation was added |
| Do not refund this payment. | Refund this payment. | Wrong: negation was lost |
| Please send my invoice. | Please send my invoice. | Correct for this task |

One of three outputs preserves the intended request. There are two different failure types: added clutter and lost meaning. A revised extractor must address both. Checking only the output length might find the first problem while missing the second, because the shortened second output looks tidy.

To evaluate a real change, save the old and new outputs for the same sources. Review ordinary cases as well as cases the program flags as suspicious. Record how the sample was chosen and count errors over all reviewed cases. If you deliberately select the three worst pages, their error rate describes that selection, not the entire source population. The existing audit chapter develops the sampling and uncertainty details.

**Contamination** is a different danger: evaluation material, or close relatives of it, enters the training-production process. Cleaning a corpus internally does not prove separation from a test set. Rewording benchmark questions is not a dependable cure either; [a 2025 study of benchmark updates](https://arxiv.org/html/2503.16402v1) finds important tradeoffs between preserving a test and resisting prior exposure. Keep the source relationships and evaluation exclusions visible rather than declaring a corpus contamination-free because one matcher found nothing.

## Exercise make one defensible cleaning decision

This exercise runs no code and requires no downloads. The source strings and expected reasoning are on this page.

1. Copy the password-reset HTML example. Mark which words belong to the request and which come from the surrounding page.
2. For the invoice pair, write one comparison form and retain both originals.
3. For the refund pair, explain why the records must remain distinct even though they are similar.
4. Add one row to the audit table in which a shorter output is worse.

Your expected result is a small before/after record with a reason for every change. If you cannot determine whether content belongs in the input, the missing piece is the task definition or source evidence, not necessarily a more elaborate cleaning tool.

For an optional executable check, reuse the first lesson's supplied builder and inspect `lineage.jsonl` and `quarantine.jsonl`; no new files or packages are required. It demonstrates normalization and exact deduplication of JSONL, not webpage extraction or semantic similarity. After this lesson, you should be able to explain what was preserved, what was changed and how you would notice a harmful change. The following independence sections use those source relationships to decide what can safely be held out for evaluation.
