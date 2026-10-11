# Beginner to practical application

Author: Puma

A reader should finish a small, inspectable release before being asked to collect a large corpus, buy equipment or choose a neural architecture. Every track begins with supplied or openly accessible material. New sensors, microphones, robots and specialist hardware are optional collection projects, never entry requirements.

## The shared prerequisite spine

1. **Make one release.** Read ten records, find a mistake, run the authored fixture pipeline, inspect its quarantine and manifest, and reproduce its hashes.
2. **State a bounded learning claim.** Define input, target, unit, allowed use, failure cost and the conditions excluded from the claim.
3. **Keep evidence and independence.** Preserve source bytes, transformations, label origins, duplicate families and split assignments. Separate development feedback from final evaluation.
4. **Measure before improving.** Count rejected and retained records, inspect random and targeted samples, report denominators and uncertainty, and keep an honest baseline.
5. **Make one controlled change.** Compare a labeling rule, augmentation, acquisition source or selection policy while keeping the evaluation question and budget clear.
6. **Export and close the loop.** Test the actual consumer, version the release, observe failures, and rehearse a reversible rollback.

These ideas are revisited at greater depth rather than treated as a terminology exam before the first practical result. Readers can take a text, tabular or image route after the spine. Advanced material adds richer representations and more demanding evidence, not an obligation to run an expensive model.

## The reader journey

The outline is organized around outcomes rather than a required chapter count.

**First release and common foundations.** Build the supplied text release, define the training claim, establish permissions/lineage, then treat extraction, normalization, duplicate relationships and independent splits as one connected production problem. Learn annotation and audits once, using the same small examples.

**Improve supervision and coverage.** Add weak and semi-supervised labels, choose valid transformations, select useful examples, and compare mixtures or synthetic-generation recipes. Existing treatment of uncertainty, active learning, DoReMi, influence and synthetic verification remains part of this progression; these were already strengths of the delivered edition.

**Choose a representation track.** Apply the common contract to text/retrieval, reasoning and trajectories, vision, audio, and optional physical/3D data. A reader need not finish every track. Each asks what new evidence that representation requires instead of repeating the full release workflow.

**Evaluate and operate.** Debug failures, study the five retained published lab cases, account for economics, and combine freezing a release with monitoring, repair and rollback. The Tuldok application remains an optional closing case after the general methods.

The draft assembly moves existing sections and combines the overlapping extraction/split and release/monitoring material. All four existing appendices and the reference ledger remain available, especially the exact training-companion contracts. Further consolidation is an editorial option; preserving a chapter boundary is not a goal in itself.

## Optional project tracks

| Level | Track and candidate models | Data-production deliverable | Advancement gate |
| --- | --- | --- | --- |
| 0 | Fictional text routing; hand-written rules, then an optional bag-of-words linear or naive Bayes model | Supplied JSONL, canonical lineage, weak votes, split manifests and measured audit | Reproduce the release, explain an abstention and a wrong label, find zero protected-family overlap |
| 0–1 | Numeric classification/regression; linear/logistic models, small trees or an MLP | Authored numeric generators or attributed UCI Iris; units, feature order, missing policy, independent split rationale | A consumer loads the frozen bytes and preprocessing is fit only on training data |
| 1 | Shapes and masks; small CNN classifier, one-object detector or segmenter | Procedural images and aligned targets; geometry and target-preserving transforms | Decode actual image/mask pairs and test edge coordinates, empty targets and split-specific families |
| 1–2 | Retrieval, small text models and structured decisions | Document families, relevance judgments, turn boundaries and target masks | Test retrieval negatives or emitted tokens, and audit prompt/benchmark ancestry |
| 2 | Speech recognition and temporal labels | A small permitted public subset; segment/time/speaker metadata and uncertainty | Listening audit plus session/speaker independence; generation consent is a separate question |
| 2–3 | Reasoning SFT, sequence distillation and verifiable RL | Tasks, teacher/version metadata, independent answer evidence, verifier tests and failure traces | Attack the verifier and measure accepted wrong answers before any training |
| 3 | Scientific fields and 3D geometry; grid CNN/U-Net, neural operator or mesh GNN comparisons | Coordinates, topology, units, boundary conditions, solver settings and scenario splits | Numerical verification and held-out-regime checks; empirical physical validation where required |
| 3 | Robot/agent trajectories and multimodal time series | Episode boundaries, clocks, calibration, actions, observations and reset semantics | Synchronization, whole-episode/site splits and executable environment checks |

Model names are options to motivate contracts, not evidence that the draft implements or benchmarks them. At each level a smaller baseline should be allowed to win. A fixed regular grid may justify a small convolutional model without introducing a graph network first.

## Exact beginner acquisition paths

### A Supplied text release

Everything required for the first executable lab is in `examples/first-release/`. Read `data/records.jsonl` and the separately maintained `data/gold.json`. Run `python3 examples/first-release/build.py --out /tmp/dataset-first-release` from the repository root. Python 3.10+ and its standard library are the only runtime requirements. There is no account, network fetch, sensor, model checkpoint or paid API in that command. The local files are authored fictional fixtures, not sampled customer messages or a population-quality benchmark. The manifest records their exact bytes and recipe.

### B Small open tabular data

Open the [official UCI Iris page](https://archive.ics.uci.edu/dataset/53/iris), use its Download button, and extract `iris.data` together with `iris.names`. The linked archive is [iris.zip](https://archive.ics.uci.edu/static/public/53/iris.zip). UCI lists 150 examples, four measurements in centimetres, three classes and CC BY 4.0. Retain attribution to Fisher and UCI, DOI `10.24432/C56C76`, retrieval date, filename and a locally computed SHA-256. The page flags historical discrepancies in two rows: record the version you actually use rather than silently blending variants. This small, heavily studied dataset is for plumbing and comparison practice, not a claim of general botanical performance. The card was inspected; this draft has not downloaded or trained on its files.

### C Existing hardware-free companion examples

The separate [BC+AI training companion at pinned revision fb895e1](https://github.com/bc-ai-ecosystem/training-your-own-models/tree/fb895e1a3e08fac86738106e6122bdcafb124e65) is publicly readable but archived as checked on 11 October 2026. No active public successor has been verified. Obtain [training-models-companion.zip at that revision](https://github.com/bc-ai-ecosystem/training-your-own-models/blob/fb895e1a3e08fac86738106e6122bdcafb124e65/docs/downloads/training-models-companion.zip) with GitHub's download control. Its published checksum is `e924589b152f68bb15d89b8f95e3b52005bbe4a9f7770f2d0550b5422d3a11d6` and size is 806,494 bytes. Compare against the [pinned checksum manifest](https://github.com/bc-ai-ecosystem/training-your-own-models/blob/fb895e1a3e08fac86738106e6122bdcafb124e65/docs/downloads/checksums.json) before extracting.

Inside the extracted companion, run from `examples/first-model/`: `python3 train.py --output run`. It generates its two features and labels internally. Chapter 4's four-sensor project also internally generates educational measurements; the reader does not need sensors. The numeric scripts currently lack an external CSV/JSONL loader, so the first text release in this book is not a drop-in input to them.

For images, the companion includes `examples/tiny-ml/make_classification_data.py`. From that directory, after using its documented CPU dependencies, run `python3 make_classification_data.py --out data/shapes-classification --train 24 --val 8 --test 8`. This creates circle/square/triangle fixtures and uses no real camera. NumPy and Pillow are required for generation; neural training is a later optional dependency. The companion's own verification record, not this draft, describes earlier execution. This edition has not rerun those scripts or established runtime compatibility.

A public repository is not automatically openly licensed. The companion does not grant a blanket license; preserve its attribution and consult its reuse notice. This acquisition path is a reference to its supplied educational material, not a new redistribution license.

## Coordinating the two books

Dataset Production teaches where examples come from, what their labels mean, how independence is preserved, and how a release is measured and maintained. Training Your Own Models teaches fitting, model architecture, inference and experimental comparison. The boundary is a concrete contract: schema, feature order, units, target conventions, split roles, provenance, adapter version and a loader test.

The existing Appendix A is the starting contract ledger. Preserve its distinctions: internally generated numeric examples are not external-data consumers; the detector reads image/mask pairs rather than arbitrary boxes; segmentation masks are 0/255; language supervision depends on the actual tokenizer and target turn. A new exporter is compatible only after its emitted files pass the relevant consumer tests. A link between books is not that test.

## Advanced acquisition is a choice

The Well, Fusion360 Gallery, DROID and large reasoning corpora belong after the shared spine. Their cards specify different licenses, download sizes and access steps. A small metadata inspection or an authored analogue can teach the contract before a reader elects to fetch data. Neither a gated dataset nor a noncommercial corpus should be described as an unrestricted default download. See the physical-systems and reasoning chapters and research register for exact routes and current caveats.
