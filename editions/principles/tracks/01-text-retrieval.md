# Text and retrieval

A search result contains the right words but leaves out the condition that makes the answer true. How do we preserve evidence rather than merely collect similar strings?

After core 8, start with these two authored notes. D1: “Refunds are available within 30 days. Opened custom items are excluded.” D2: “An exchange is available for damaged custom items.” Query Q1: “Can I refund an opened custom item after 10 days?” The reference answer is no under D1. The fact that 10 is within 30 does not remove the exception. This is an authored illustration, not a real merchant policy.

## Work one retrieval example

Treat each whole note as its source family. Make D1-a from the first sentence and D1-b from the second, retaining ordered offsets and D1 as parent. A retrieval record needs query ID, corpus snapshot, candidate chunk IDs and relevance judgments. D1-a alone is insufficient evidence for Q1. D1-b is necessary; D1-a plus D1-b supplies the scope and exception. D2 shares a topic but answers a different question. Mark a merely unjudged chunk as unjudged, not negative.

A lexical baseline matching “refund” can rank D1-a first and still lead to a wrong answer. For the tiny audit, define success as retrieving sufficient evidence within the first two results. Rank [D1-a,D2] fails; [D1-a,D1-b] passes. That is one authored query judgment, not a population recall estimate. A controlled improvement adds section-aware neighboring context. It is justified if it repairs missing exceptions without exceeding the declared context budget or merging unrelated sections.

The theory is conditional relevance. A passage is relevant to a query in a fixed corpus under an answerability guide; semantic similarity is only a signal. Chunking changes what evidence a consumer can see, and selection changes the denominator of any reported retrieval metric. Keep answer spans, insufficient evidence, multiple positives and disputed relevance distinct.

## Carry this project through core 9–15

- Core 9: collect independently authored queries about exceptions, with the same review budget as a random alternative.
- Core 10: a paraphrase preserves the answer only if it preserves the opened/custom/10-day conditions. Dropping “opened” changes the question.
- Core 11: use a keyword rule as a weak proposal; audit against resolved relevance references and retain abstention.
- Core 12: generate candidate questions only from held-in notes; check every answer against the complete source. Reserve other document/query families first.
- Core 13: compare sufficient-evidence retrieval under a fixed corpus, result budget and query guide; log every inspected query family.
- Core 14: freeze corpus/chunks/queries/judgments and test ID resolution, offsets, order and the neighboring-context policy with the actual retriever.
- Core 15: a chunker change that loses exclusions is an incident. Restore the source, chunker version and index together; a running search process is not a recovered compatible release.

## Exercises and worked answers

1. Can D1-a support “all custom items qualify within 30 days”? No. The full source contains an exclusion, and the universal claim is unsupported.
2. May D1-a be training and D1-b final evaluation for unseen documents? No. Both descend from D1; keep the document family together. A known-corpus/new-query claim needs a different explicit split rationale.
3. Two answers use the same context: A says “No, opened custom items are excluded”; B says “Yes, 10 days is within 30.” Which is chosen for correctness? A. Do not generalize that correctness judgment into a style preference without a rubric.
4. A typed choice has IDs refund, exchange, clarify. Display order changes. What must stay stable? Target ID and evidence, followed by a checked ID-to-index mapping; the old display index is unsafe.

Acceptance: preserve the complete condition and answer provenance, correctly distinguish related from relevant, and show that a changed chunking policy actually supplies the necessary evidence. Model training is optional.

Text records can look valid while carrying the wrong supervision. The same string can be context in one objective, a target in another, and an evaluation-only reference in a third. Keep source evidence, canonical roles, target semantics, and rendered model input separate.

## Documents conversations and preferences are different units

Continued pretraining consumes document text under a next-token objective. Instruction tuning consumes a context and desired response, often with only selected assistant tokens receiving loss. Retrieval training consumes relevance relationships. Preference training consumes comparative judgments under shared context. Typed decisions consume state, candidate options, and a target choice or distribution.

A document extraction pipeline should retain page/section anchors and ordered structure, including tables or code where relevant. Inspect OCR and cleanup on representative layouts. A classifier that prefers textbook-like prose may be appropriate for one pretraining objective and erase the informal language needed for another.

For style examples, separate facts from presentation. A teacher can rewrite a response fluently while changing a commitment or number. Review both factual preservation and style, and vary topic independently from voice. For preferences, preserve ties, both-bad, uncertainty, rubric, and candidate provenance before mapping to a binary chosen/rejected export.

For typed decisions, stable candidate IDs matter more than display order. Preserve constraints and evidence, distinguish infeasible options from less-preferred feasible ones, and define abstention where the application permits it. A calibrated probability is a prediction under a population and protocol; it is not permission to execute the chosen action. The Jev/Kev/CLM/Laya studies and original option-pointer exercise remain distinct in the companion appendix.

## Retrieval supervision and negative mining

A retrieval example links a query to one or more relevant passages in a specific corpus snapshot. Keep relevance separate from similarity. A high-scoring neighbor can be a hard negative, a duplicate of the positive, another valid answer, or an ambiguous partial answer. Unjudged is not synonymous with irrelevant.

A sound process registers a rights-cleared corpus, generates or collects queries from held-in material, verifies positive evidence spans, retrieves candidate negatives, removes related positive families, and has a qualified reviewer or validated scorer judge the remaining candidates. Preserve multiple positives and uncertainty. Record the miner and scorer versions, ranks, scores, and query-generation conditions.

Qwen3 Embedding describes synthetic weak supervision followed by labeled data and filtered synthetic pairs. Its query-generation dimensions include role, type, length, difficulty, and language. NVIDIA's public embedding recipe explicitly addresses false negatives and uses margin filtering, but its numeric thresholds are recipe-specific. Neither is a reason to label all nearest neighbors negative. [R37] [R38]

## Preference judgments and pair construction

Preserve the shared context, all candidates, display order, judge identity/version, criteria, decision, confidence when meaningful, and rationale or evidence. Allow ties, both-bad, and uncertain. Only a later pair-construction policy maps eligible judgments to chosen/rejected records for a particular trainer.

Blind and randomize A/B display when possible. Keep factual correctness separate from style and brevity. A shorter answer is not automatically better, and a rejected response is not a classification negative. Hard comparisons should include plausible alternatives; artificially broken responses can make preference learning look easy without teaching useful distinctions.

Argilla's curated UltraFeedback documentation describes cases where numeric scores contradicted strongly negative critiques. This is a concrete warning to audit judge output parsing and pair ordering, not merely trust that a model returned valid JSON. Check duplicate candidates, inverted ordering, rubric contradictions, and accidental prompt differences. [R39]

## Optional tools and deeper path

A text editor and ordered IDs suffice for this example. Later, a corpus loader, search index and review interface can implement the same contract. Test the actual tokenizer, chat template, truncation policy and assistant loss mask before calling an SFT export supported. Tool environments continue in the reasoning track. The five published production cases explain why filtering rubrics and generated preferences need independent checks.
