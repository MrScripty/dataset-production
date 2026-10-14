# Tuldok as a production lifecycle case

A corrected label should improve the next release without rewriting the evidence used to judge the previous one. A restarted application should not silently repeat a job whose earlier response was lost. These are data-production principles, whatever interface implements them.

Evidence status: source, versioned contracts and public lifecycle receipts were inspected on 13 October 2026 at Tuldok main 6a1d799f916e5882856ae66f261fb2ad81061cec. No application, model or browser workflow was executed for this edition. The public receipts below record actual upstream executions on authored fixtures. They establish bounded workflow behavior, not model quality on user data. Earlier chapter 16's 2fc4a46 snapshot and 7d7e6e6 integration branch remain historical; their capabilities must not be presented as current limits.

## One versioned source review release and consumer

Use the bounded text workflow as the compact chain. The [clean-source visual receipt](https://github.com/MrScripty/Tuldok/blob/6a1d799f916e5882856ae66f261fb2ad81061cec/docs/images/workspaces-m3-text/manifest.json) identifies qualification source a10f2cb9296e1070683352cd6e5b544729219738, dirty=false, and 18 explicitly authored independently grouped text fixtures imported through Data controls. Human label review is explicit. “Authored independent fixtures” describes that test design, not a statistical audit of a naturally occurring population.

Source meaning precedes the interface. Imported original text has its own source hash; the canonical asset uses NFC and LF. The frozen text export does not contain the original pre-normalization bytes, so its source hash cannot reconstruct them. Keep original source evidence separately when it is needed to reproduce an audit. Review establishes eligibility under the guide, not proof that every class reflects an external truth.

The [text-classification contract](https://github.com/MrScripty/Tuldok/blob/6a1d799f916e5882856ae66f261fb2ad81061cec/docs/contracts/workspace-text-training.md) freezes exact text assets, labels and sorted class indices, source/annotation revisions, rights/provenance and protected-family snapshots. Connected families include unselected bridges and retained deleted lineage. Unknown lineage and protected-family crossings refuse rather than being repaired by random assignment. The frozen ZIP carries manifest, assets and separate train/validation/test JSONL views. Every label must be represented in all three protected splits; missing coverage blocks release without dropping or reassigning examples.

The [M3 qualification report](https://github.com/MrScripty/Tuldok/blob/6a1d799f916e5882856ae66f261fb2ad81061cec/docs/plans/dataset-centered-workspaces/reports/m3-text.md) records actual run 78bd09fe80164b8abb5eff3efc2c7e1a and frozen release 46b8f6e9740632303866479536e57b64dfb557d822737fb57e257d389605747d. These identify that original fixture execution, not a new run at the later main head.

## What the actual consumer checks

The implemented v1 consumer is a bounded TF-IDF/Multinomial Naive Bayes CPU classifier. It accepts 6–512 reviewed records and 2–8 exact labels under the frozen split/byte bounds. It is not a general language-model trainer. [The inspected implementation](https://github.com/MrScripty/Tuldok/blob/6a1d799f916e5882856ae66f261fb2ad81061cec/text_training.py) fits vocabulary, feature selection, document frequencies/IDF and coefficients using train records only; validation/test transform through those saved statistics.

The classifier has one fit pass. Its shared history envelope's epoch=1 does not mean iterative neural training. Its data-only JSON model has a checked cold reader; a readable JSON object alone would be insufficient without validating source identity, dimensions, class mapping and prediction behavior. Runs publishes hashed model/metric/prediction artifacts and verifies their consistency. These controls connect core 3's semantic contract to core 14's actual emitted data.

The selected recipe is a fixed five-stage release→validate→train→evaluate→publish graph, with bounded parameters and typed edges. The existence of editable Pipeline controls does not authorize arbitrary graph execution. Stale graph/release validation fails before admission. Hardware/runtime availability is a declared prerequisite of this optional consumer, not a prerequisite of the book's paper examples.

## Correction and evaluation exposure

The public text receipt records a correction that creates a new reviewed annotation and release while retaining the old release bytes and frozen predictions. A result link opens the current editable source, but the result continues to cite the old frozen revision. This is the transferable invariant: current truth can change without falsifying historical evidence.

Validation is the default result view. Test access requires a durable exposure reason. Exposure follows record identity or canonical content hash; reimporting the same normalized text under a different filename cannot create a fresh holdout. The [Runs contract](https://github.com/MrScripty/Tuldok/blob/6a1d799f916e5882856ae66f261fb2ad81061cec/docs/contracts/workspace-runs.md) and text receipt record retained test exposure across later releases and application restart. The software detects some identity/byte reuse; it cannot prove semantic independence of every paraphrase or previously inspected related family. Continue the scientific exposure ledger outside those exact-match checks.

## Observe a failure and test the boundary

The clean text fixture deliberately tests stale validation, disconnected graphs and a lost committed response. Its receipt records explicit reconciliation returning the same single run. A lost response does not establish that the request stopped or failed before commit. Use the saved operation identity and verified result to distinguish no admission from an admission whose acknowledgement was lost; automatic blind retry can duplicate work or distort costs.

A separate historical [grounded-reopen CI diagnosis](https://github.com/MrScripty/Tuldok/blob/6a1d799f916e5882856ae66f261fb2ad81061cec/docs/plans/image-caption-exports/reports/grounded-reopen-ci-failure.md) documents a browser failure after reload: the fixture waited for text already present in the old document, then immediately asserted rejected state. The navigation-race explanation is an inference because the exact failed event interleaving was not captured. The test correction waits for a changed main-frame loader and that loader's own load event, then compares retained API decisions. This is a lesson in diagnosing the first wrong observation boundary rather than declaring stored decisions corrupt. It is a distinct fixture/version, not a failure in the text run above.

## Restart is different from restoring an independent backup

The text receipt demonstrates application restart with the existing catalog/artifacts and no job replay. That is useful persistence evidence. It is not an independent backup restoration experiment.

Tuldok's [local storage contract](https://github.com/MrScripty/Tuldok/blob/6a1d799f916e5882856ae66f261fb2ad81061cec/docs/contracts/local-storage.md) makes PostgreSQL the metadata authority while local files hold original assets and frozen releases. Dataset identity includes the persistent manifest; a directory of images alone is not a complete catalog. Backup needs all cooperating writers stopped, metadata plus filesystem artifacts, exact hashes and a compatible schema/application. An old SQLite copy cannot recover later PostgreSQL writes. A version rollback and a data restore must agree on that contract.

Actual independent restoration evidence is separate. The [PostgreSQL verification report](https://github.com/MrScripty/Tuldok/blob/6a1d799f916e5882856ae66f261fb2ad81061cec/docs/plans/dataset-centered-workspaces/reports/postgres-verification.md) records a separate-server restore retaining source catalog, dataset identity, reviewed text/history and frozen release hash 7065adc765c7d66cd775b5ded85f2baabbc3654cc924f0291b5e3e60a09f6852, followed by cold-process reopen. A later [retained-run restoration receipt](https://github.com/MrScripty/Tuldok/blob/6a1d799f916e5882856ae66f261fb2ad81061cec/docs/images/workspaces-exports-20261013/integrated-retained-runs.json) records a real schema-3 mesh integrity run retained through schema-4 upgrade, schema-4 restore and schema-3 restore followed by upgrade. Its release ZIP hash remains 39272bdc66acf5e536e0896bb44bdb8b0f8f5278d18276b0294a76f40880239a and the original backups remain unchanged.

Do not stitch these separate catalogs into a claim that the named text run above underwent every restoration path. They provide distinct scoped evidence for the same recovery principle. This edition has not repeated either restoration. A new release's recovery acceptance still requires its own complete-bundle rehearsal, ideally after deliberate loss of disposable working state, with hashes, history, exposure and consumer behavior checked.

## Implemented behavior and proposed interfaces

Data/Pipeline/Runs, these bounded classifiers, frozen reviewed releases and durable exposure are implemented at the inspected head. The old research edition's generalized overview/readiness/recipe screens and additive task expansions were design proposals; a screenshot concept is not an implementation receipt. Match each capability to its actual versioned contract.

A current example of the distinction is Rheon producer v2. The [corrected readiness audit](https://github.com/MrScripty/Tuldok/blob/6a1d799f916e5882856ae66f261fb2ad81061cec/docs/plans/rheon-v2-consumer/reports/readiness-20261013.md) identifies an actual producer packet and corrects an earlier inference that no packet existed. Current Tuldok still admits its bounded two-file v1 path; its three-file v2 reader/storage/release workflow remains planned at this head. Missing locally materialized packet bytes do not prove the producer never emitted them, and a consumer plan does not prove interoperability. ASR, general 3D training and other later paths require their own product/consumer evidence.

## Hardware-free transfer exercise and worked answer

Write three authored records on paper: R1 source version 1, reviewed target billing, frozen in release A; R1 source version 1, target corrected to accounts at annotation version 2, frozen in release B; result E that evaluated A. E must continue to cite A and the old reviewed target, while a correction view may link to current R1. A test inspection event for R1 remains exposure after the label correction. Changing the label does not make the input independent.

Next, classify three recovery descriptions. Reopening the existing catalog is restart. Selecting old compatible source/adapter/data together is rollback. Copying a verified complete backup to a new destination after working-state loss is restoration. The correct acceptance evidence for the last is not a running server but reconstructed identity, bytes, metadata/history and correct consumer interpretation.

Acceptance: trace one source through review, freeze, actual consumer, correction and exposure; keep fixture failures distinct from production incidents; demonstrate the recovery claim actually made. Product setup is optional and versioned separately.
