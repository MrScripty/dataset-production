# Choose transformations that preserve the target

Suppose we have only a few labeled pictures of a square. We would like a future classifier to recognize the square in different positions rather than memorize one arrangement of pixels. One way to create practice examples is to move the square within the image while keeping its category label.

This is **data augmentation**: making a changed version of an example for training. The important question is whether the old target still answers the question we are teaching. The transformation may require changing the target too. We will work through that decision before considering any augmentation library.

## Move a shape and follow its labels

Here is a complete five-by-five image represented as characters. `#` is a foreground pixel; `.` is background. This is an on-page illustration, not a file you must download.

```text
Original            Moved one column right
.....               .....
.##..               ..##.
.##..               ..##.
.....               .....
.....               .....
```

For a **classifier**, which chooses a category for the image, the input changed but the target can stay `square`. The object is still completely visible and has the same shape. This teaches an intended **invariance**: position should not change this particular answer.

For a **localization model**, the target is where the square is. Number columns and rows from zero, starting at the top left. The original square occupies columns 1 and 2, and rows 1 and 2. After moving it, it occupies columns 2 and 3. Its location target must move too.

| Task | Original target | Target after the move |
| --- | --- | --- |
| Classify the visible shape | square | square |
| Identify foreground columns | 1 and 2 | 2 and 3 |
| Mark foreground pixels | The four original `#` cells | The four moved `#` cells |

A **segmentation mask** marks which pixels belong to the object. For this example, the foreground pattern shown above is also the mask. Moving the image without moving its mask would teach the model that the object is somewhere it is not. The symbol diagram is not a PNG encoding; the existing companion's executable mask contract uses 0 and 255, as explained in its appendix.

This example shows two valid augmentation policies. Classification can keep the label. Localization or segmentation must transform the label together with the input. The correct policy depends on the task, not merely on the image operation.

## A plausible change can destroy the lesson

Now crop the original image so that only columns 0 and 1 remain:

```text
Cropped view
..
.#
.#
..
..
```

The visible foreground is now a narrow rectangle. If the task is “classify the visible shape,” keeping `square` would be wrong. If the task instead identifies an original object despite occlusion, `square` might remain the intended target, but the cropped evidence may not be sufficient to distinguish it from another object. That is a different task specification. The crop command cannot decide which one you meant.

For segmentation of visible foreground, the cropped mask is straightforward: keep only the surviving foreground cells. For a caption that said “a complete square,” the caption is no longer accurate. One source can support several targets, and a single transformation can affect them differently.

Text has the same problem. Compare these two changes to a fictional request:

| Original | Changed version | Is the old request meaning preserved? |
| --- | --- | --- |
| Please send my invoice. | Could you send my invoice, please? | Yes for routing to billing |
| Please refund this payment. | Please do not refund this payment. | No: the requested action changed |

The second pair shares almost every word. Similarity alone does not establish that a transformation is safe. For a task that only routes messages by department, both may still go to billing; for a task that decides whether to issue a refund, their targets must differ. Always name the answer before deciding which variations should leave it unchanged.

## Choose a change for a reason

Start with a problem you want to address. If a classifier fails when an object moves, position changes are relevant. If a speech system fails at ordinary recording volumes, bounded gain changes may be relevant. Randomly adding every available transformation does not establish that the new inputs resemble the application.

Record the original example, the operation and its settings, the resulting input, and the target decision. Keeping the original ID with its derivatives also prevents a subtle evaluation error: a training image and its shifted copy should not be placed in different splits and counted as independent evidence.

There are two separate checks. First, did the transformation preserve or correctly update the target? Second, did training on the changed examples improve performance on the intended application? The first is a data check. The second requires a controlled model experiment. A valid transformation need not be useful, and a useful average effect does not excuse wrong labels in an important slice.

## Work through a small audit

Here is an invented four-example review. We are checking data validity, not reporting a training run.

| Candidate | Target policy | Decision |
| --- | --- | --- |
| Move the complete square right | Keep category `square` | Accept |
| Move the image but leave its mask behind | Segment visible foreground | Reject: image and target no longer align |
| Crop half the square and retain “a complete square” | Caption what is visible | Reject: caption claims missing evidence |
| Rephrase the invoice request politely | Route by requested service | Accept |

Two of four candidates are acceptable under the stated policies. Do not report “100% valid” after deleting the two failures without mentioning that four were attempted. The rejection rate helps estimate review effort and reveals which operation is risky. For a real audit, inspect ordinary and difficult examples, and record how they were selected.

Research supports taking this task-specific view. [UDA](https://proceedings.neurips.cc/paper/2020/file/44feb0096faa8326192570788b38c1d1-Paper.pdf) uses augmentations to encourage consistent predictions and depends on their label-preserving behavior. That premise can fail in practice: [Lowell et al.](https://aclanthology.org/2021.emnlp-main.408.pdf) found that elaborate text augmentation was not consistently better than simpler alternatives, with a harmful back-translation result in biomedical evidence inference. The lesson is to test the policy for the task, rather than assume a named method supplies validity.

## Exercise decide what must change

Nothing is installed or run in this exercise. The two shape diagrams and the text pairs above are all the supplied material; no image file or companion download is needed.

For each of the following, write the changed input, the new target if needed, and one sentence explaining your decision:

1. Move the original square down by one row, keeping it fully visible. The category should remain square; the foreground rows should move from 1–2 to 2–3.
2. Mirror a sign whose text must be transcribed. The visual category “sign” may survive, but you must not silently keep an ordinary left-to-right transcription if the transformed image no longer supports it.
3. Add “not” to the refund request. Department routing and refund-action prediction need different target decisions.

If two reasonable answers disagree, check whether they describe the same task. If they do, the annotation guide needs clarification before the policy is used at scale.

**What you have learned.** You can distinguish an input change that preserves the target from one that requires a new target or should be rejected. This lets us discuss **consistency training** in the next lesson: asking a model to make compatible predictions on suitable versions of an example. No image-generation or model-training experiment has been run in this chapter.
