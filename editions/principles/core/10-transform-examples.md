# 10 Transform examples without changing the task

*Dataset Production · Puma*

## The question: is a changed input still the same lesson?

A producer moves a square to create another image and keeps the label `square`. Another producer moves the image but leaves its segmentation mask in place. Both used the same image operation. One may teach the intended task; the other teaches that the object is somewhere it is not.

The principle is **justify the target transformation before increasing volume**. Some tasks should keep their answer when an input changes. Others must change their answer consistently. A third possibility is that the changed input no longer supports any accepted answer. A library's operation name cannot choose among these cases for you.

You already have a contract, label guide, family split and measured gap. This chapter produces an augmentation policy and validity audit. A valid derivative is not yet evidence of a better model.

## Work one square through two tasks

**Authored illustration.** Number rows and columns from zero at the upper left. These character grids are explanatory drawings, not executable PNG files. `#` marks foreground and `.` marks background.

```
Original       Shifted right
.....          .....
.##..          ..##.
.##..          ..##.
.....          .....
.....          .....
```

For “classify the visible shape,” the complete shifted foreground is still a square. Its category stays `square`. This is **invariance**: an intended input change leaves the target unchanged.

For “mark the foreground pixels,” the original target is cells (1,1), (1,2), (2,1), (2,2), written as (row,column). After the move the target is (1,2), (1,3), (2,2), (2,3). This is **equivariance**: the answer changes in the same relevant way as the input. For an exclusive-maximum box in pixel coordinates, the original is `(x_min=1,y_min=1,x_max=3,y_max=3)` and the moved box is `(2,1,4,3)`. Writing x and y explicitly prevents row/column confusion. A normalized box would divide x values by width and y values by height under its declared contract.

If the pixels move but the mask stays, the files may have identical dimensions and valid integer values. Schema checks pass while semantic alignment fails. Overlaying the decoded emitted mask on the decoded emitted image makes the failure visible. Inspect what the consumer reads, not only what an editor preview displayed.

## Cropping can change the question

Crop the original to columns 0 and 1:

```
..
.#
.#
..
..
```

For “classify the visible shape,” the foreground is now a narrow rectangle. Keeping `square` is unsupported. For “identify the original object despite occlusion,” `square` may be intended, but the visible evidence may not distinguish it from a rectangle. That task requires an occlusion policy, perhaps an uncertain target. For visible-foreground segmentation, retain only the two surviving foreground pixels and update shape/coordinates. For a caption saying “a complete square,” revise or reject the caption.

A crop can also remove all foreground. A segmentation contract may permit an empty mask for a negative image. An object-identity contract may require a minimum visible fraction. State the policy rather than guessing a target from the parent's category. Hidden versus absent objects, visible versus full-object masks, and clipped versus unclipped boxes are distinct conventions.

## Text, sound and fields have the same dependency

**Authored illustration.** “Please refund this payment” becomes “Please do not refund this payment.” Department routing may remain billing, but refund-action extraction changes from requested to not requested. Lexical overlap is high while action meaning reverses. A polite paraphrase of an invoice request may preserve routing; a rewrite that deletes a condition may not.

For audio, bounded volume changes may preserve a transcript, but clipping can erase phonetic evidence. Cropping a segment requires synchronized transcript and timing updates. Changing sample-rate metadata without resampling changes interpreted time and pitch. For a physical field, reordering cells may be valid only when axes, boundary conditions and targets move consistently. A unit conversion must change values and metadata together. For a tool trajectory, deleting an observation can remove the evidence needed for the next action.

These cases do not require software to recognize. They require the task definition from Chapter 2 and the representation contract from Chapter 3. A transformation is safe relative to those definitions, not safe in general.

## Separate validity from utility

An augmentation has at least three questions:

1. Does the derivative meet the declared semantic and representation contract?
2. Does it resemble a condition relevant to intended use, rather than an arbitrary disturbance?
3. Does using it improve a controlled downstream comparison without unacceptable regressions?

The first is a data-validity gate. The second is a relevance hypothesis. The third requires a fitting/evaluation experiment. Passing one does not settle the others. A realistic noisy input can be invalid if its target is stale. A perfectly valid shift can be useless if the original collection already covers position adequately.

Keep a record of parent revision, operation/version, parameters, randomness, output hash, target policy, checks and decision. Derivatives inherit the parent's protected family and split. Ten crops do not create ten independent acquisition units. Transform only allowed training material for training; never expand a final-test family into training and count it as newly independent.

When augmentation is sampled on the fly, freeze its policy, distribution and seeds for the reproducibility claim you need. Exact bitwise replay may require environment/version pins. A statement that training uses “random crops” is insufficient to reconstruct which shapes are legal or how labels change.

## Controlled exercise: audit six derivatives

**Evidence label: authored illustration; no model or image program executed.** Unit: a proposed derivative of one authored parent. Use the grids and requests above. Each decision must name the task, not just the operation.

1. Shift the original square down one row. Write the category and foreground coordinates.
2. Shift its pixels right while keeping the original mask. Accept or reject for segmentation?
3. Keep “a complete square” after the two-column crop. Accept or reject for visible-image captioning?
4. Add `not` to the refund request. Supply targets for both routing and refund-action extraction.
5. Mirror an image containing text to be transcribed. Can the old ordinary transcription be silently retained?
6. Put a derivative in test while its parent remains in train. Explain why a correct target does not repair the evaluation problem.

Then make one controlled change: revise the risky crop policy to reject crops below a declared evidence threshold, or explicitly support negative/occluded cases with the corresponding targets. Record attempted, accepted, rejected and unresolved candidates. If four of six are rejected, report six attempts and two acceptances; do not present the retained pair as evidence that the original recipe was perfectly valid.

For an optional CPU reproduction, implement the five-by-five arrays and a joint image/mask shift using the standard library. Assertions should compare all foreground coordinates, count pixels, reject out-of-bounds shifts under your chosen policy and verify inherited family identity. This implementation is **proposed work**, not a delivered augmentation program. No package or model download is needed for the paper exercise.

## Acceptance check and worked answer

A valid policy names the relevant gap, supported task, target update, prohibited/uncertain cases, lineage, family inheritance and checks on emitted data. A reviewer should be able to explain a counterexample in which a familiar operation fails. Utility acceptance is a separate decision under Chapter 13's controlled comparison.

Worked answers: the down-shifted category remains `square`; foreground rows become 2 and 3, columns remain 1 and 2. The unshifted mask is rejected because it marks wrong locations. The complete-square caption is rejected because the crop cannot support it. Routing remains billing under our guide; refund requested becomes false. Mirroring a sign requires a transcription policy and fresh verification; silently retaining the old transcription is unsupported. The split derivative leaks a parent family even if its pixels and target are otherwise correct.

Reviewer guidance: do not accept “the model should learn robustness” as a label-validity argument. Ask to see the transformed target and its interpretation. Check axes after rotation, exclusive maxima at image edges, empty masks, color/label encodings, clipping, time alignment, negation and conditional statements. An apparently small operation may erase the only task-relevant evidence.

## Optional consistency methods, tools and reading

A consistency objective encourages compatible predictions across valid versions of an input. It inherits the augmentation policy's assumptions. If a strong crop makes the category ambiguous, asking the learner to agree confidently can amplify an unsupported target. Training mechanics belong in the companion.

Read Xie et al., [Unsupervised Data Augmentation for Consistency Training](https://proceedings.neurips.cc/paper/2020/hash/44feb0096faa8326192570788b38c1d1-Abstract.html), for augmentation as part of a consistency method. Read Lowell et al., [Unsupervised Data Augmentation with Naive Augmentation and without Unlabeled Data](https://aclanthology.org/2021.emnlp-main.408/). Their empirical study finds that simple perturbations can match or exceed more elaborate ones in the examined NLP settings. No universal improvement follows from a transformation name.

An image/mask tool can reduce bookkeeping, but choose one only after specifying joint operations and export tests. Audio tools must expose sample rate, segment boundaries and resampling. Text generators must preserve source spans and support semantic review. None of these tools is required for the shared lesson or supplies an independent validity guarantee.
