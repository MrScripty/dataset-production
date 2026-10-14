# Physical fields and simulation

Choose this optional track after core chapter 8 and carry it through core chapters 9–15. You can complete the text, tabular and image projects without it. Its purpose is to answer a new question: when a model learns from numbers attached to places and times, what must we preserve so those numbers still mean the same thing?

We will use a complete two-by-two temperature example. No sensor, simulator, CAD program or dataset download is needed. The numbers are authored for teaching and follow a simple stated rule; they are not observations or validated physical predictions.

## A field is a value at each location

An ordinary table might contain one temperature for each machine. A **field** attaches values to positions across a region. Temperature is a **scalar field** because each position has one value. Velocity would need both size and direction and is usually stored using several components.

Imagine a square divided into four equal cells. The square is two metres wide and two metres high. We place the coordinate origin at its bottom-left corner; x increases to the right, y increases upward. Each stored value describes the centre of one cell.

| Cell centre (x, y) in metres | Temperature at time 0 |
| --- | --- |
| (0.5, 1.5) top left | 20 °C |
| (1.5, 1.5) top right | 22 °C |
| (0.5, 0.5) bottom left | 18 °C |
| (1.5, 0.5) bottom right | 21 °C |

We can store the same values as a small array, with rows written from top to bottom:

~~~text
20  22
18  21
~~~

The array alone does not tell a reader its units, physical size, row direction or whether values belong to cell centres or corners. If another program assumes the first row is the bottom row, it moves the hot and cold regions. The file can load successfully while describing the wrong spatial arrangement.

For this example, the representation therefore includes the values plus these facts: temperature in Celsius, position in metres, a two-by-two cell grid, cell-centre locations, top row first, and time measured in seconds. These are part of the data's meaning, not optional notes for a visualization.

## Make one input and one target

Suppose our teaching task is to predict the next temperature array. Define this deliberately simple rule: every cell becomes one degree Celsius warmer after one second. This is an authored arithmetic rule, not a heat-flow model.

~~~text
Input at 0 seconds      Target at 1 second
20  22                  21  23
18  21                  19  22
~~~

We now have an input/target pair just as we did for the helpdesk message. The input is structured differently, so the contract needs additional information:

| Field | Meaning in this example |
| --- | --- |
| values_at_t0 | The first array, in the stated spatial order |
| target_at_t1 | The second array under the one-degree rule |
| temperature_unit | Celsius for both arrays |
| time_step_seconds | 1 |
| grid | The cell centres and row/column convention defined above |
| source_rule | Add 1 °C to every cell; authored teaching rule |
| run_id | One identity shared by every time step from this sequence |

A **trajectory** is a sequence of such states over time. If we apply the rule again, the state at two seconds is another related frame from the same trajectory. Assign the whole run to one split before taking adjacent frame pairs. Otherwise training on the first pair and testing on the next can make a familiar sequence look like an independent new system.

Notice what we have not established. We have not shown that a neural model can learn the rule, that the rule resembles heat transfer, or that any hardware was measured. We have specified exactly what one training pair would mean.

## Check a representation error before blaming a model

A colleague returns this target while still claiming “top row first”:

~~~text
19  22
21  23
~~~

Those are the expected target's rows in reverse order. The values are individually plausible, but they are attached to the wrong places. A model trained on this pair would be penalized for making the spatially correct prediction.

There are two possible repairs. Put the rows back into the declared order, or change the coordinate mapping and transform all related fields consistently. Changing only the metadata to make one example appear valid is unsafe if the input, target or other channels still use the old convention.

Units can cause a similarly silent problem. A value of 20 °C describes the same temperature as 293.15 K. Writing 20 and changing the unit label to Kelvin does not perform that conversion. Keep the numerical transformation and the unit declaration together. A color picture can hide either error because its color scale may be rescaled automatically.

## Correct arithmetic is not physical validation

Two evidence questions matter when a numerical simulator supplies labels.

**Verification** asks whether the implementation and numerical solution do what the specified mathematical model requires. For our toy rule, checking that 20 becomes 21 and 18 becomes 19 verifies those example calculations. Real numerical solvers also need checks such as analytic test cases, convergence and sensitivity to resolution or tolerances.

**Physical validation** asks whether the model agrees with physical observations well enough for its intended use. Our one-degree rule has no such evidence. A perfectly implemented program can therefore produce targets that are perfectly consistent with the rule and physically inappropriate.

[NASA/NPARC's guidance](https://www.grc.nasa.gov/WWW/wind/valid/tutorial/overview.html) makes this distinction explicit. Its [verification assessment](https://www.grc.nasa.gov/www/wind/valid/tutorial/verassess.html) describes several kinds of numerical evidence. Agreement with a simulator, a small solver residual or a convincing animation cannot alone establish agreement with reality. A **residual** measures how much a proposed numerical solution fails to satisfy the equations being solved; it does not measure whether those equations describe the intended physical situation.

For a real simulation-generated example, retain the equations or model name, material properties, initial state, boundary conditions and solver settings. A **boundary condition** specifies behavior at the edges of the simulated region, such as holding a wall at a fixed temperature. Changing that condition changes the problem even if the interior grid is unchanged.

## Exercise repair the four-cell record

This is a paper exercise. Nothing runs, and all arrays and coordinates are supplied above. There is no physical-data download or sensor requirement.

1. Restore the reversed-row target to the declared top-first order. You should obtain 21 23 on the top row and 19 22 on the bottom row.
2. State the location of the value 23 °C. It is at (1.5, 1.5) metres, not simply “array entry two” without a coordinate convention.
3. Explain what happens if the target's unit label changes to Kelvin but its numbers do not. The represented temperatures change; the physical quantity has not been converted correctly.
4. Write one supported claim and one unsupported claim. Supported: the target follows the authored one-degree rule. Unsupported: the rule accurately predicts a heated real object.

If you cannot place a value in space and time or explain its units, the data contract is incomplete. That is the problem to fix before comparing model architectures. After this exercise, you should be able to read a field sample without confusing its array layout, visualization and physical meaning.

## Optional branches after the field example

These are directions to investigate, not additional exercises that must be downloaded or run now. Detailed sizes, licenses and acquisition routes remain in the research register.

**Scientific simulation trajectories.** The [Well paper](https://arxiv.org/html/2412.00568v1) and [format documentation](https://polymathic-ai.org/the_well/data_format/) extend the field idea to much larger systems. Begin by reading one sample's coordinate, time and field descriptions. Data and loader-code licenses differ, and some releases have correction notices. Obtaining a large collection does not replace checking those details or validating the physical use case.

**Geometry instead of a fixed grid.** A CAD program stores construction operations. A boundary representation, or B-rep, stores surfaces and how they connect. A mesh approximates a surface or volume with small elements; a point cloud samples positions without necessarily retaining those connections. These formats preserve different information. [Fusion360 Gallery's reconstruction specification](https://github.com/AutodeskAILab/Fusion360GalleryDataset/blob/master/docs/reconstruction.md) provides concrete examples, but its data have noncommercial-research restrictions. Reading the schema is enough for an initial comparison; no corpus download is required here.

**Measured action sequences.** Robot recordings add cameras, actions and clocks. Two streams with timestamps still need a known timing relationship and **calibration**, the measurements that connect camera coordinates to the robot or world. [DROID's 2025 revision](https://arxiv.org/html/2403.12945v2) illustrates that richer contract. The optional starting point is its public documentation or visualizer, not reproducing the robot hardware collection.

## Staggered fields do not share one set of locations

The four-cell temperature is cell-centered. In a staggered fluid grid, pressure can be at cell centers while each velocity component sits on faces normal to its axis. On a two-by-two 2D grid, cell pressure has four entries, horizontal face velocity has three columns by two rows, and vertical face velocity has two columns by three rows. Even equal-length flat arrays would not establish equal coordinate meaning. Record component shape, physical offset, flattening order and units. A renderer that centers everything can hide the mistake.

A pressure gauge fixes the arbitrary reference in problems that determine pressure differences. Comparing two gauge-equivalent fields without the declared alignment can show a large pressure error even when their gradients agree. Never remove a real offset for a task where absolute pressure is specified. Unit conversion, gauge alignment and spatial rearrangement are different transformations.

## Carry the four-cell project through core 9–15

Core 9 adds independently specified starting fields and boundary/regime cases, not adjacent frames masquerading as independent systems. Core 10 tests coordinate and unit transformations jointly. Core 11 records a numerical-solver label's tolerances and failure/abstention state. Core 12 separates generated candidates, numerical verification and evidence against observations. Core 13 reports errors by trajectory/regime and resolution, tracks seed exposure, and narrows claims where new holdouts are unavailable. Core 14 cold-reads arrays with units, cell/face axes, time, gauge and boundary conditions. Core 15 restores input fields, solver/adapter versions and accepted outputs as a bundle; include generation, failed candidates, review, fitting and repeat evaluation in economics.

## Additional exercises and worked answers

1. How many horizontal face values exist on the stated two-by-two 2D grid? Six, arranged as two rows by three columns; they are not the four pressure locations.
2. Can a small divergence residual validate a real fluid scene? No. It checks a property of the discretized numerical state; physical validation needs relevant observations and a use-specific error budget.
3. A frame from the same simulation seed is renamed and moved to final test. Is it fresh independent evidence? No. Preserve its trajectory/initial-condition family and earlier exposure.
4. What remains unproved by the Celsius-to-Kelvin exercise? The correctness of a physical heat model, real measurement validity and any fitted predictor's generalization.

Acceptance: locate values in space and time, preserve units and boundary/field semantics, distinguish arithmetic/numerical verification from physical validation and defend the independence unit. Optional larger field, geometry and robotics projects inherit this same standard. The [Rheon case](#case-01-rheon) now uses pinned published run artifacts rather than the old future-pressure proposal. Its fixed-box modal fit must not be generalized to new physical regimes.
