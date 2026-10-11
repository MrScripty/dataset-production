# Extract normalize and audit what changed

The first release lab starts with JSONL to make each decision visible. Larger pipelines encounter HTML, PDFs, tables, archives and multimedia containers. The central obligation is the same: be able to explain which source became which example, what was lost, and how often that loss changes the target.

## Keep the source and the comparison key distinct

A web page is not a ready-made training example. Extraction decides whether navigation, comments, tables, captions, footnotes, or code survive. Trafilatura’s 2021 evaluation measured retained content versus boilerplate on 500 documents; the paper also cautions that page styles and HTML diversity affect extraction. That result is evidence for a tool/version and benchmark, not a permanent ranking. [Trafilatura, ACL demo 2021](https://aclanthology.org/2021.acl-demo.15.pdf)

Keep three separate representations where justified: the source artifact, extracted content, and a normalization key used for comparison. NFC and NFKC are different choices. Unicode’s specification warns that compatibility normalization can remove meaningful distinctions. For example, converting a superscript into an ordinary digit may be acceptable in a search key but damaging in scientific training text. Do not overwrite the only copy. [Unicode Normalization, revision 57](https://www.unicode.org/reports/tr15/tr15-57.html)

A practical record contains source URI, acquisition time, source hash, parser/version/configuration, extracted-text hash, normalization version, language/script estimate, and parent record. Keep rejection reasons instead of an unexplained “clean” flag.

Audit fixed page families before and after a parser upgrade: news, forums, tables, code, scanned documents, short pages, and multiple scripts. Check missing content and inserted clutter, not just character count. Test accents, combining marks, nonbreaking spaces, indentation, decimal separators, and units. Missing text can create false labels downstream: a statement whose “not” disappears is a different example.

FineWeb2’s 2025 work shows why English-derived thresholds do not simply transfer across languages. Word segmentation and language-identification confidence interact with filtering. The pipeline was ablated on nine languages and evaluated on fourteen, despite much wider released coverage; bias and diversity were not measured by its chosen evaluation tasks. [FineWeb2, v1](https://arxiv.org/html/2506.20920v1)

## Detect related records before deciding what to keep

Exact hashes find byte-identical or normalized-identical records. Near-duplicate methods find substantial overlap; substring methods catch copied passages inside otherwise different documents. None proves that two examples mean the same thing. Lee et al. combine exact substring and approximate document matching, showing less memorized output and improved training efficiency in their studied language models. Their thresholds are experimental choices, not universal defaults. [Deduplicating Training Data, ACL 2022](https://aclanthology.org/2022.acl-long.577.pdf)

Separate three decisions: detecting related records, assigning related records to a split, and choosing their training weights. Deduplication is not always “keep one, forget the rest.” FineWeb2 retains original cluster sizes and uses filtering statistics to guide selective upsampling. In its experiments, moderate duplication can indicate useful content; enormous repeated clusters and completely unique material can have different quality profiles. [FineWeb2](https://arxiv.org/html/2506.20920v1)

Audit sampled duplicate pairs and near-threshold nonmatches. Check whether changing one date, number, or negation changes the task answer. Preserve conflicting labels for review. Retain cluster ID, match method, similarity, representative choice, and original multiplicity. Split by the relevant entity or document family before making derivatives, then verify cross-split similarity. A dataset with fewer rows is not necessarily a better dataset.

## Audit exposure to evaluation material

Deduplicating the training corpus does not establish separation from evaluation. Search training candidates against benchmark questions, answers, rationales, source documents, and transformed relatives where available. Version the benchmark exclusion list and record what matching can and cannot detect. Private holdouts still need access and release controls.

The 2025 Emperor’s New Clothes study evaluates twenty benchmark-update strategies with ten LLMs, five benchmarks, and two constructed contamination settings. It finds no strategy that consistently combines strong fidelity with resistance across its experiments. A reworded question can remain learnable from exposure, or become a different test. Its scope is updating existing benchmarks under controlled contamination; it does not show that every possible contamination defense fails. [ICML 2025 research, v1](https://arxiv.org/html/2503.16402v1)

Audit contamination claims at the example level. Report overlap rates, human-checked false matches, remaining uncertainty, and scores with suspected overlaps removed. Never convert “our detector found none” into “the corpus is contamination-free.”

## Turn a cleaning recipe into a measured change

Keep an immutable input manifest and run each recipe into a separate candidate release. Count records at every boundary: attempted, decoded, schema-valid, extracted, selected and emitted. Rejections need mutually intelligible reasons; a row can also carry several diagnostic flags. Preserve a quarantine that permits investigation without quietly returning rejected rows to training. Protect that quarantine with the same access rules as the source.

A minimal audit ledger contains the stage and recipe version; input/output counts and units; random-sample selection method; targeted failure slices; reviewed count; adjudicated error count; unresolved count; and reviewer guide version. Rate denominators must match the question. Extraction error over successfully decoded pages does not measure archive corruption; duplicate-pair precision does not measure missed duplicates; retained-row label precision does not measure coverage lost by filtering.

For a parser replacement, keep a fixed, manually inspectable regression set with tables, code, lists, short records and Unicode edge cases. Compare both extraction outputs against the source. Sample additional changed records and some unchanged records: a detector that only reviews differences can miss shared errors. Review length ratios as screening signals, never as final quality labels. Report exact sample counts and avoid claiming that a small zero-error sample proves no errors exist.

## The supplied lab and its deliberate limits

The first-release program actually runs a bounded audit: malformed rows, canonical duplicates, source-family components, weak-label coverage and separately supplied reference-label comparisons. It does not extract arbitrary websites, implement semantic deduplication or prove contamination absence. The distinction matters. A working exact-content check is a useful baseline with a known detection boundary, not a placeholder for an undocumented semantic detector.

A realistic follow-on should add a frozen set of near-duplicate pairs, including adversarial nonduplicates that differ in a number or negation. Measure precision and recall against that adjudicated set, then inspect samples near the selected threshold. Report residual undetected similarity as an uncertainty. Preserve original multiplicity even when only one training representative is emitted; it may be needed for source weighting and withdrawal later.

**Try it.** Compare case-preserving NFC text with a case-folded duplicate key. Invent a pair whose target changes under a normalization that would otherwise seem harmless. Record the collision instead of silently choosing the first label.
