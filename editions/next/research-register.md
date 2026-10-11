# Research register for the next edition

Checked 11 October 2026. This register adds evidence for identified gaps; it does not replace or renumber the delivered book’s existing 85 public-source entries. No new source is included solely to reach a reference count. Research findings below describe their authors’ experiments or documentation, not experiments rerun for this edition. No talk/video was watched in this pass.

## Labeling and corpus methods


Stable proceedings URLs identify the cited publication; arXiv URLs pin the exact revision. “Read” below means inspected relevant full-text sections, not reproduced results or audited proofs.

1. Ratner et al., Snorkel, PVLDB 2017: architecture, development/test assumptions, labeling functions, modeling trade-offs. [Published PDF](https://www.vldb.org/pvldb/vol11/p269-ratner.pdf)
2. Sohn et al., FixMatch, NeurIPS 2020: objective, threshold and augmentation ablations; noted single-split ablation scope. [Published PDF](https://proceedings.neurips.cc/paper/2020/file/06964dce9addb1c5cb5d6e3d9838f733-Paper.pdf)
3. Oliver et al., Realistic Evaluation, NeurIPS 2018: evaluation principles, class-mismatch design, discussion/recommendations. [Published PDF](https://papers.nips.cc/paper/7585-realistic-evaluation-of-deep-semi-supervised-learning-algorithms.pdf)
4. Xie et al., UDA, NeurIPS 2020: §§2.1–2.3, augmentation assumptions and objective. [Published PDF](https://proceedings.neurips.cc/paper/2020/file/44feb0096faa8326192570788b38c1d1-Paper.pdf)
5. Lowell et al., EMNLP 2021: augmentation/sequence alignment, §4 results, conclusion. [Published PDF](https://aclanthology.org/2021.emnlp-main.408.pdf)
6. Liu and Liu, When Confidence Fails, 2025: introduction, §§3.1–3.2, stated benchmark scope. [arXiv v1](https://arxiv.org/html/2509.16704v1)
7. Li et al., SEVAL, TMLR-accepted 2026 revision of a 2024 preprint: §§3–4, §5 setup, grouping/held-out limitations, appendix implementation notes. [arXiv v3, June 12, 2026](https://arxiv.org/html/2407.05370v3)
8. Barbaresi, Trafilatura, ACL-IJCNLP 2021: §4 evaluation, Table 1, conclusion. [Published PDF](https://aclanthology.org/2021.acl-demo.15.pdf)
9. Unicode Consortium, UAX #15: canonical/compatibility distinctions, normalization caution, stability, revision metadata. [Revision 57 / Unicode 17.0.0](https://www.unicode.org/reports/tr15/tr15-57.html)
10. Lee et al., Deduplicating Training Data, ACL 2022: exact/near dedup methods, memorization experiment scope, reported outcomes. [Published PDF](https://aclanthology.org/2022.acl-long.577.pdf)
11. Penedo et al., FineWeb2, 2025: §§2–6, language thresholds, deduplication, rehydration, evaluation and limitations. [arXiv v1](https://arxiv.org/html/2506.20920v1)
12. Sun et al., Emperor’s New Clothes, 2025: §§1–3, experimental pipeline, qualitative failures, conclusion. [arXiv v1](https://arxiv.org/html/2503.16402v1)


## Reasoning and physical systems


### 1. OpenThoughts research recipe

[OpenThoughts, arXiv:2506.04178v2, 5 June 2025](https://arxiv.org/html/2506.04178v2), paper text inspected, especially sections 3–5 and the experiment design. This is supervised sequence distillation: collect questions, choose/filter sources, generate teacher responses, and package question–reasoning–answer sequences. The paper studies over 1,000 controlled experiments. Its findings about teacher choice, repeated sampling, and answer filtering are conditional on its experimental setting; they do not establish universal production rules. In particular, its weak gains from answer filtering in SFT are not an argument for omitting an RL reward verifier. The paper separates development benchmarks from held-out evaluations, an important distinction to teach before presenting leaderboard scores.

### 2. OpenThoughts3 acquisition and counting

[Official dataset card](https://huggingface.co/datasets/open-thoughts/OpenThoughts3-1.2M/blob/main/README.md), pinned by [repository revision 61bcf9d4eb38b30295efc2021227a63cc5bb34c8](https://huggingface.co/datasets/open-thoughts/OpenThoughts3-1.2M/commit/61bcf9d4eb38b30295efc2021227a63cc5bb34c8). The advertised Apache-2.0 dataset has 1,200,000 training rows: 850k math, 250k code, 100k science. Crucially, the recipe downsamples to 75k questions and annotates each 16 times with QwQ-32B. These are not 1.2 million independent questions. Files are Parquet under `data/train-*`; metadata reports 28,188,197,544 download bytes and 59,763,369,750 logical dataset bytes. Fields include `difficulty`, `source`, `domain`, and `conversations`. Beginner route: inspect the card and web viewer, then a deliberately bounded streaming sample if separately requested. Advanced route: acquire pinned Parquet shards through Hugging Face Datasets with the revision recorded. Keep repeated responses grouped by source question across splits.

### 3. Big-Math's task-production method

[Big-Math, arXiv:2502.17387v1, 24 February 2025](https://arxiv.org/html/2502.17387v1), paper sections 2.1–2.3 inspected. Its target is open-ended problems with a uniquely checkable closed-form answer. The pipeline applies source-specific cleaning, exact/semantic deduplication, decontamination, and human-reviewed filters. It also reformulates multiple-choice questions into open-ended tasks. Its filter-quality measurements are evidence about the tested filters, not proof that every retained answer is correct. A useful classroom comparison is which task types disappear: proof requests, ambiguous or multipart questions, and problems depending on missing figures. Explain the tradeoff: automatic reward coverage improves, but the resulting dataset represents a narrower slice of mathematical reasoning.

### 4. Big-Math files, gates, and licenses

[Official Big-Math-RL-Verified card](https://huggingface.co/datasets/SynthLabsAI/Big-Math-RL-Verified) lists 251,122 problems, including 47,010 reformulated examples, and 33.2 MB total file size. Its advertised data license is Apache-2.0. The [official production-code repository](https://github.com/SynthLabsAI/big-math) is MIT and explicitly says the dataset contains no rollouts. Columns are `problem`, `answer`, `source`, `domain`, and `llama8b_solve_rate`; the last is model-specific success frequency over 64 attempts, not intrinsic difficulty.

Current acquisition caveat: the public card is readable, but file access requires Hugging Face login, accepting conditions, and contact-information sharing. That gate was not accepted. Beginner route: read the paper's examples and public schema. After authorized access, the exact dataset ID is `SynthLabsAI/Big-Math-RL-Verified`, with Parquet in its `data` directory. No immutable dataset revision was obtainable in this read-only pass; require a revision/file manifest before reproducible ingestion. Do not silently substitute `Big-Math-RL-UNVERIFIED`.

### 5. A concrete 2026 verifier update

[Hugging Face Math-Verify](https://github.com/huggingface/Math-Verify), README and changelog inspected; [PyPI release 0.9.0](https://pypi.org/project/math-verify/0.9.0/) is dated 10 January 2026. It is Apache-2.0, requires Python 3.10+, and distinguishes extraction from equivalence checking. The documented call order is `verify(gold, answer)`; comparison is intentionally asymmetric in some cases. The README discusses LaTeX/plain-expression extraction, numeric precision, and timeout handling. Pin the evaluator and parser dependencies, not merely a dataset filename. The 0.9.0 source distribution is 60.3 kB; its SHA-256 is `45ac6c61344ba056b9e99a660a4bc8d044ed408f730aed68c60435aa5eec4645`. Beginner exercise: review expected outcomes for equivalent fractions, intervals, malformed answers, and multiple boxed answers. Do not describe this library as a proof checker or an infallible truth oracle.

### 6. NASA: numerical verification versus physical validation

[NASA/NPARC overview](https://www.grc.nasa.gov/WWW/wind/valid/tutorial/overview.html) and [verification assessment](https://www.grc.nasa.gov/www/wind/valid/tutorial/verassess.html), last-updated date 10 February 2021, inspected as technical guidance. Verification asks whether implementation and numerical solution correctly realize the mathematical model. Validation asks whether the simulation agrees with physical reality for an intended use. Code review, analytic comparisons, conservation checks, and spatial/temporal convergence supply different evidence. Matching another solver alone is weaker than independent convergent evidence; errors can cancel. This is guidance, not a downloadable labeled corpus. Do not repeat the historical page's claim about the absence of standards as a current industry fact.

### 7. The Well's scientific scope and data license

[The Well, arXiv:2412.00568v1, 30 November 2024](https://arxiv.org/html/2412.00568v1), main description and datasheet distribution section inspected. The original release advertises 16 physics datasets totaling approximately 15 TB, spanning distinct dynamical systems. Its datasheet declares CC-BY-4.0 for data. These are numerical simulations and temporally sampled fields, not direct experimental measurements or general ground truth about reality. The paper provides provenance and simulation context; the production lesson is to retain equations, numerical method, initial/boundary conditions, and parameter coverage alongside arrays. A paper describing a broad collection does not make each constituent dataset appropriate for a particular pressure-prediction use case.

### 8. The Well's practical access and maintenance

[Official access documentation](https://polymathic-ai.org/the_well/), [format](https://polymathic-ai.org/the_well/data_format/), and [dataset-size overview](https://polymathic-ai.org/the_well/datasets_overview/) inspected. HDF5 stores fp32 fields, coordinates, time, parameters, and boundary metadata; scalar, vector, and tensor fields have distinct semantics. The documented selective command is `the-well-download --base-path PATH --dataset active_matter --split train`. Omitting dataset/split downloads everything. The documented streaming base is `hf://datasets/polymathic-ai/` with `WellDataset`. Published full-subset sizes include active matter 51.3 GB and turbulent radiative layer 2D 6.9 GB; neither is a tiny classroom sample. Start with the visualizer or one explicitly bounded file/trajectory.

[The repository](https://github.com/PolymathicAI/the_well) flags `viscoelastic_instability` as deprecated due to processing errors and recommends `viscoelastic_instability_v2`. Its code [license](https://github.com/PolymathicAI/the_well/blob/master/LICENSE) is BSD-3-Clause, distinct from the data license. [Package 1.2.0](https://pypi.org/project/the-well/1.2.0/) was released 1 December 2025. A package pin is not a data-content pin; record constituent IDs, hashes, and correction status independently.

### 9. Fusion360 Gallery: acquisition and permission boundaries

[Autodesk's official release index](https://github.com/AutodeskAILab/Fusion360GalleryDataset) lists reconstruction `r1.0.1`: 8,625 sequences, 2.0 GB; segmentation `s2.0.1`: 35,680 parts, 3.1 GB; and joint subset `j1.0.0`: 32,148 joints/23,029 parts, 2.8 GB. Smaller supplementary archives include face-extrusion sequences, 41 MB, and extrude volumes, 152 MB. The reconstruction file is `https://fusion-360-gallery-dataset.s3.us-west-2.amazonaws.com/reconstruction/r1.0.1/r1.0.1.zip`; the 41 MB supplement is `r1.0.1_regraph_05.zip` in that directory. The supplement is derived data, not a complete small replica of every modality.

The [dataset license, updated November 2021](https://github.com/AutodeskAILab/Fusion360GalleryDataset/blob/master/LICENSE.md), permits only noncommercial research and prohibits redistributing the whole corpus. Modified subsets have downstream restrictions; re-identifying creators is prohibited. Access for a commercial product pipeline must not be assumed from public availability. The no-download route is the illustrated schema documentation; commercial learners can practice on their own synthetic CAD examples.

### 10. Fusion360 Gallery's representation bridge

[Official reconstruction specification](https://github.com/AutodeskAILab/Fusion360GalleryDataset/blob/master/docs/reconstruction.md), full format sections inspected. Data includes construction JSON, B-rep in SMT and STEP, triangulated OBJ, and thumbnails. JSON records sketch/extrude operations and their timeline; sketches use points, curves, and profiles. OBJ triangles retain B-rep face IDs, allowing connections to modeling operations. Important caveats: supplied meshes are not manifold; length units are centimeters and angles radians. Point clouds and voxels are possible derived representations but are not included. Teaching opportunity: the same final shape can be viewed as geometry, topology, an operation sequence, or sampled observations. Preserve correspondence and conversion provenance rather than treating these formats as interchangeable encodings.

### 11. DROID's synchronized demonstrations and 2025 revision

[DROID, arXiv:2403.12945v2, 22 April 2025](https://arxiv.org/html/2403.12945v2), collection setup and calibration appendix inspected. This version reports 76k trajectories, 350 hours, 564 scenes, and 86 tasks; earlier summaries say 84, so attach the count to the version. The paper states CC-BY-4.0 for the dataset. Collection uses a Franka arm, gripper, three synchronized stereo-camera streams, and teleoperation, recording actions at 15 Hz. Its calibration appendix is a useful 2025 update: it supplies post-hoc calibration and quality metrics while acknowledging false positives and difficult scenes. A synchronized recording still requires calibration and alignment checks. Replicating this collection is an advanced robotics project involving hardware, trained operators, privacy, and physical safety, not a beginner software exercise.

### 12. DROID's graduated acquisition paths

[Official dataset documentation](https://droid-dataset.github.io/droid/the-droid-dataset) provides a browser visualizer and sample-loading Colab as starting points. For a manageable but still substantial download, `gsutil -m cp -r gs://gresearch/robotics/droid_100 TARGET` obtains 100 RLDS episodes, advertised as 2 GB. Full RLDS is `gs://gresearch/robotics/droid`, 1.7 TB; raw stereo-HD data is `gs://gresearch/robotics/droid_raw`, 8.7 TB. Raw folders include metadata JSON, `trajectory.h5`, MP4s and SVO recordings. RLDS packages language instructions, per-step observations/actions, boundaries, reward and discount.

The documentation still warns that 20% of raw episodes were missed during face-blurring/copying, while stating RLDS is complete. Its promised short fix window is not evidence that repair happened; verify the bucket manifest before publishing a completeness claim. Bucket paths are mutable; record object generations/checksums when acquisition is actually authorized.



## Additional primary acquisition evidence

- UCI Iris: official [dataset card](https://archive.ics.uci.edu/dataset/53/iris), DOI 10.24432/C56C76, inspected 11 October 2026. Card/schema/license and documented row discrepancies read; data bytes not downloaded. Use a content hash at acquisition.
- BC+AI training companion: [public revision fb895e1](https://github.com/bc-ai-ecosystem/training-your-own-models/tree/fb895e1a3e08fac86738106e6122bdcafb124e65), README and published checksum manifest inspected. Archived; no verified active public successor. Original companion contract evidence remains in Appendix A. No new training run or private-material inspection.

- Tompson et al., ICML 2017: [published paper landing page and abstract](https://proceedings.mlr.press/v70/tompson17a.html) inspected in this pass for the bounded fluid-surrogate precedent. No independent reproduction; do not treat this as validation of Rheon.

- Rheon: [README at revision 34235d3](https://github.com/MrScripty/Rheon/blob/34235d33c886aa05b5bdf95d920b863d1fb2ad6f/README.md), fixed-box comparison and transport evidence boundaries inspected 11 October 2026. No source build, solver run or independent physical validation performed for this edition. The pressure-surrogate section is a design proposal.

- Ross, Gordon and Bagnell, AISTATS 2011: [DAgger paper landing page and abstract](https://proceedings.mlr.press/v15/ross11a.html) inspected for the learner-induced state-distribution issue. Used as a limited conceptual precedent, not a reproduced algorithm or newly executed trajectory experiment.

## Questions still requiring research or execution

1. Evaluate weak-label models against majority/abstaining rules and a supervised baseline on an appropriately licensed, independently annotated corpus. The authored fixture only tests plumbing.
2. Compare pseudo-label thresholds, class coverage and mismatch sensitivity under a fixed budget, including 2026 SEVAL-style held-out threshold learning. No reproduced improvement is claimed.
3. Build extraction and near-duplicate gold audits across scripts, page types and answer-changing small edits; exact hashes alone do not answer this.
4. Benchmark reasoning verifiers on false acceptance, false rejection, ambiguous references and resource limits. Pin Math-Verify plus dependencies; do not infer process correctness from final-answer success.
5. Materialize a bounded permitted field/geometry/trajectory sample, record payload hashes and validate its actual loader. No large dataset payload was downloaded here.
6. Qualify the bounded Rheon pressure experiment with source instrumentation, numerical reference checks and whole-scenario holdouts before calling it a training corpus. Any physical-accuracy claim needs separate validation evidence.
7. Compare release candidates under a deployment-like audit, rehearse rollback, and establish a fresh unseen evaluation set after the public teaching fixture has been studied.

## Reading limits

Version-pinned paper links identify the inspected text; selected methods/results/limitations were read rather than every proof independently checked. Publisher documentation is a dated snapshot when no immutable revision is available. OpenReview’s later OpenThoughts conference copy was inaccessible in this pass, so only the pinned arXiv text is cited. Current web access and a publisher’s license declaration do not constitute a rights audit of every upstream example.
