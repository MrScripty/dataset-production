# Choose transformations that preserve the target

An augmentation changes the input while preserving the intended label, or transforms the label in a known way. The same edit can be safe for one task and destructive for another. Lowercasing may preserve a document’s topic but destroy an entity distinction. An image flip may preserve an object category but reverse a left/right label. Cropping a detection image requires updating boxes and checking whether objects remain visible.

UDA motivates consistency learning with diverse, useful transformations, including back-translation for text. Its supervised formulation explicitly requires label-preserving transformations. This is an assumption to check, not a property conferred by the name of an algorithm. [UDA, NeurIPS 2020](https://proceedings.neurips.cc/paper/2020/file/44feb0096faa8326192570788b38c1d1-Paper.pdf)

Contrary evidence improves the lesson. Lowell et al. found naive word replacement competitive with more elaborate augmentation in several NLP experiments; consistency on labeled data alone also helped. Back-translation hurt biomedical evidence inference by 7.5 F1 with the full unlabeled set. The authors suggest domain mismatch as an explanation, not a proven universal mechanism. Some imperfect transformations can help regularization, so fluent paraphrases are neither necessary nor sufficient evidence of usefulness. [EMNLP 2021 study](https://aclanthology.org/2021.emnlp-main.408.pdf)

Audit a stratified original–transformed sample with reviewers labeling both versions independently. Count label flips, changed negation/numbers/entities, lost evidence, and broken span alignment. Store parent IDs and put all derivatives in the parent’s split. Evaluate on unaugmented production-like data; use a separate robustness suite to measure the intended invariance.

## Choose the method by the failure it should address

Begin with a failure hypothesis: the model relies on background color, fails under a plausible recording gain, or cannot handle harmless spelling variants. A transformation should resemble a variation the application may encounter. More severe or more visually impressive changes are not necessarily better training examples. Compare a baseline without the change, the proposed policy, and an equally sized alternative at a stated training budget. If a stochastic policy makes several changes, keep the sampled parameters so an accepted example can be inspected again.

| Intended variation | Candidate operation | Target obligation | Example of a failed assumption |
| --- | --- | --- | --- |
| Camera position | Crop or resize | Transform boxes, masks and landmarks together; record truncation | A caption names an object removed by the crop |
| Image orientation | Rotation or reflection | Rotate coordinates and directional labels | A left-handed part becomes right-handed |
| Recording gain | Bounded amplitude change | Avoid clipping; retain transcript only if speech remains intelligible | A quiet phoneme disappears below the noise |
| Writing variation | Spelling or paraphrase edits | Recheck entities, numbers, negation and answer evidence | “Not approved” becomes “approved” |
| Sensor/reference frames | Coordinate transformation | Transform vectors, tensors, boundary conditions and units consistently | Positions rotate but velocity labels do not |
| Numeric measurement noise | Plausible noise model | Preserve a target only when its definition permits it | Noise crosses the actual decision threshold |

The table is a design checklist, not a validated menu of defaults. Mixing two examples, deleting spans, or generating counterfactuals can require a new target rather than an inherited one. Some methods intentionally train on soft or mixed labels; document that objective instead of calling the new example an unchanged observation.

## Audit the transformation itself

Freeze a small sample before tuning the policy. Stratify by class and vulnerable cases, then retain every parent–child pair, operation version, parameters and target revision. Count transformation failures over attempted transforms, not only over accepted children. If a reviewer rejects one in ten children, report that denominator alongside any downstream gain. Check the cases that passed automatic validity tests as well as obvious failures.

A geometric check can establish that a transformed box lies inside the image without establishing that it encloses the right object. A text parser can establish valid JSON while missing a changed factual answer. Mechanical validity, semantic validity and downstream utility need separate measurements. Keep augmented derivatives in the parent split; never augment first and randomly split the children.

**Try it.** Take a provided shape image, crop it until part of the shape disappears, and write three target contracts: classify the original shape, classify what remains visible, and segment visible pixels. Which targets survive the crop without reannotation? The exercise is about the definition of the label, not finding one universal answer.
