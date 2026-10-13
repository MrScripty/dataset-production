# 3 Represent meaning with a data contract

*Dataset Production · Puma · Part 1: A first useful release*

## A beginner's failure: the file loads, but the meaning moves

A four-cell temperature file loads without an error. It contains exactly four numbers. A second program reads its first row as the bottom of the square, though the writer meant the top. Every value has the right type and the wrong location. A validator that checks only “four numbers” cannot catch the mistake.

After chapter 2, you have a task and a claim. Here you will decide how each value carries that task's meaning. You will compare a table row, a tiny mask, and a four-cell field, then deliberately expose a unit or row-order mismatch. Everything needed is printed below.

## The principle: representations preserve some information and discard other information

A **representation** is a way to store or describe something. A **schema** describes structural requirements: fields, types, shapes, and allowed values. A **data contract** adds how a consumer must interpret them: units, coordinate order, time, missingness, labels, task scope, and versioned transformations. Structural correctness is necessary, but it cannot alone establish semantic correctness.

Keeping “billing” as a string preserves the category name. It does not preserve the ownership guide unless the guide is linked and versioned. Reducing a conversation to its last message discards earlier context. Turning a photo into four corners preserves a quadrilateral, not every visible pixel. A representation is good for a task when its retained information and declared conventions are sufficient for the intended decision.

### One source can support several targets

A photograph of a book might support an object-present category, four named corners, a visible-paper mask, or a caption. The image may be shared, but the targets are separate example revisions. A four-corner polygon is not automatically a pixel-perfect segmentation. A prompt used to generate an image is not automatically a verified description of its output. Keep the source asset, task, annotation revision, release, and consumer export separate so a convenient format does not silently redefine the target.

## Worked example 1: a table row

**Authored illustration.** A row says:

| message_id | message | queue |
|---|---|---|
| t01 | Please do not refund this payment. | billing |

The contract specifies one message per decision, text as received or transformed under a named recipe, and a queue under routing guide version 1. Here “billing” identifies an owner; it does not mean “refund requested.” The ID links evidence and should not become a predictor of the queue. The target is a proposal, an adjudicated reference, or an accepted training target only if its status says so.

Missing queue values need a convention. An empty string could mean no annotation was attempted, insufficient evidence, abstention, conflict, or a technical failure. Those states need separate fields or an explicit status vocabulary. The fixture uses `label_status` with `labeled`, `abstain`, or `conflict`; a missing reference is a separate audit state. Replacing every missing value with “billing” would invent information.

For time-dependent tables, also state when each feature becomes available. A value recorded after an outcome may be unsuitable as an input for predicting that outcome. Storing a timestamp does not, by itself, establish availability at decision time.

## Worked example 2: an image mask

**Authored illustration.** Imagine a two-by-two image and a matching mask:

~~~text
Image cells              Visible-object mask
book   background        1  0
book   background        1  0
~~~

A **mask** assigns a label to each spatial cell or pixel. Our mask uses 1 for visible book and 0 for background, with top row first, columns left to right, and the same two-by-two grid as the image. The contract prohibits filling an invisible occluded region. It states that this is a binary visible-object mask, not a class-ID palette or an instance-ID map.

If an adapter resizes the image, it must transform the mask consistently. If it swaps 0 and 1, the same byte values acquire the opposite meaning. If it rotates only the image, the input and target no longer align. The consumer must declare its expected orientation, geometry, label codes, and resizing policy. A loader accepting the file proves none of those meanings automatically.

## Worked example 3: a four-cell field

**Authored illustration.** A field attaches a quantity to positions. This scalar field gives one temperature per cell in a two-metre by two-metre square. The origin is bottom left; x increases rightward and y upward. Values describe cell centres. Stored rows run from top to bottom.

| Cell centre in metres | Temperature at 0 seconds |
|---|---|
| (0.5, 1.5), top left | 20 °C |
| (1.5, 1.5), top right | 22 °C |
| (0.5, 0.5), bottom left | 18 °C |
| (1.5, 0.5), bottom right | 21 °C |

The corresponding input array is:

~~~text
20  22
18  21
~~~

The authored target rule adds 1 °C to every cell after one second. The target is:

~~~text
21  23
19  22
~~~

This is an arithmetic teaching rule, not a heat-transfer model or a physical observation. The target at (1.5, 1.5) is 23 °C. If a file instead gives first row `19 22` and second row `21 23` while still declaring top-first order, it attaches the correct numbers to the wrong places.

Units are equally consequential. The same temperature as 20 °C is 293.15 K. Converting from Celsius to Kelvin adds 273.15 to the numerical value; changing the unit label alone does not convert it. A one-degree Celsius difference is a one-kelvin difference, but the absolute values differ. Thus the top-left input and target are 293.15 K and 294.15 K after consistent conversion.

An adapter is a versioned transformation from the release representation to a specific consumer's expected representation. Its contract might say: “adapter v1 emits four features in top-left, top-right, bottom-left, bottom-right order, in Celsius; target time is input time plus one second.” Adapter v2 could emit Kelvin, but it must update every relevant input, target, unit declaration, and test. Merely calling a file “compatible” is insufficient.

## The theory: make the interpretation reconstructible

A minimal semantic contract answers these questions:

- What is one example, and what source/time does it describe?
- Which fields are inputs, targets, metadata, or review evidence?
- What are the units and permitted numerical range, if meaningful?
- What do axes, row/column order, coordinates, sampling rate, and origin mean?
- What is the time reference, step, horizon, or interval? Are endpoints included?
- Which codes mean background, absence, unknown, abstention, or conflict?
- Which label guide and revision define the target?
- Which transformations occurred, and which adapter version emits the consumer's files?

Some of these are irrelevant to a particular modality; mark them not applicable rather than silently leaving them unknown. For a mask, time may be absent. For an audio segment, time and sample rate are essential. For a field sequence, cell centre versus corner location and boundary conditions can change the problem. Boundary conditions describe behavior at the edges, such as a held temperature; this toy addition rule does not claim any physical boundary model.

A contract needs both successful and failing examples. A test should identify the known location of 23 °C, not just assert that an array has shape two by two. A mask test should check that a known object cell remains object after decoding. Chapter 14 will apply that idea to the actual consumer's emitted bytes.

### Verification is narrower than physical validation

Checking that each cell increases by one verifies arithmetic against our authored rule. **Physical validation** would ask whether that rule represents observations well enough for the intended physical use. No such evidence exists here. NASA/NPARC distinguishes mathematical/numerical verification from validation against reality in its [overview](https://www.grc.nasa.gov/WWW/wind/valid/tutorial/overview.html). A low residual or attractive animation cannot close the missing observational step. A residual measures mismatch with specified equations, not whether those equations describe the relevant world.

This is a general lesson: checking file syntax, label consistency, and consumer interpretation establishes different properties. State which property each test checks.

## Controlled exercise: repair the contract, then the values

**Evidence status:** authored illustration, with paper arithmetic. **Unit:** one table decision, one mask cell, and one spatial field cell at a declared time. No model or physical experiment is run.

1. Write the table row's target semantics and distinguish a missing target from “refund not requested.”
2. State what 0 and 1 mean in the mask, its axis order, and one unsupported use of it.
3. Repair the reversed-row field target. Locate 23 °C in coordinates and time.
4. Convert the input top-left and target top-left to Kelvin. Explain why keeping 20 and 21 while changing the unit label fails.
5. Write an adapter declaration containing feature order, units, input/target times, missing-value policy, guide or rule version, and one semantic test.

### Acceptance check

Pass when another person can place every field value, interpret every mask code, and distinguish metadata from features without guessing. The paper adapter must have a semantic test that would fail the deliberate mismatch. Revise unknown axis, unit, time, or missingness conventions. Reject a physical prediction claim based only on the four-cell arithmetic.

### Worked answer and reviewer guidance

The table target is owning queue under routing guide v1. A missing routing target supplies no refund-intent judgment. The mask is binary visible-book segmentation, top-first and left-to-right, with 1 object and 0 background; it does not identify an occluded extent or distinct book instances.

The repaired target is top row 21, 23 and bottom row 19, 22. The 23 °C value is at (1.5, 1.5) metres at one second. Kelvin top-left values are 293.15 and 294.15. A valid adapter example flattens those Celsius arrays in top-left, top-right, bottom-left, bottom-right order, rejects missing cells rather than imputing unknown temperatures, names addition-rule v1, and tests that output position two equals the top-right target 23. Other consistent representations are acceptable if all values and metadata transform together.

The reviewer should read only the learner's contract and try to reconstruct the arrays. If reconstruction requires looking up an unstated convention, the contract needs revision. Do not reward a long schema that still leaves feature order ambiguous.

## Optional technical details and reading

For implementation, a machine-readable schema can validate types and shapes, while small authored tests check semantics. Retain both. Exact companion formats remain in the preserved training-contract appendix; these teaching arrays do not assert a new supported adapter. The optional physical track expands units, trajectories, boundaries, and numerical evidence after chapter 8. NASA/NPARC's [verification assessment](https://www.grc.nasa.gov/www/wind/valid/tutorial/verassess.html) is primary guidance for the verification distinction. It supports the scope of the concept, not the realism of this toy field.
