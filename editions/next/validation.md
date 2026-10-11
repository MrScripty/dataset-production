# Validation and evidence boundaries

Checked 11 October 2026 against the initial next-edition draft. Author credit remains Puma. The delivered manuscript and all published `docs/` artifacts are unchanged by this increment.

## Initial executed checks at commit 416408d

Environment: Python 3.12.14, Unicode database 15.0.0, Node.js 24.19.0 and Pandoc 3.1.11.1. No packages, model checkpoints or external dataset payloads were installed/downloaded for these checks.

| Check | Result |
| --- | --- |
| `python3 -B -m unittest discover -s tests -p 'test_*.py' -v` | 28 tests pass: 22 release-lab tests and 6 edition-assembly tests |
| `npm test` | All 15 existing JavaScript tests pass |
| First-release CLI with recipe version 2 | Successful build into a fresh output directory |
| Repeated release builds at distinct output paths | Byte-identical outputs; manifest hashes checked in tests |
| Reordered input | Canonical examples, split files and audit unchanged; raw byte/line provenance correctly changes |
| Gold-isolation test | Changing gold labels cannot alter examples, votes, grouping or splits |
| Unicode regression | Greek combining-mark equivalents share a stable canonical form and protected family component |
| Next-edition builder | Markdown, HTML, metadata and copied SVG figures generated successfully outside `docs/` |
| Edition integrity | All retained chapters/appendices included once; legacy citation labels resolve; figures exist; author credit present |
| Protected output and overwrite checks | Both builders refuse nonempty targets; review builder refuses published `docs/` paths |
| `git diff --check` | Pass |

The source manuscript was checked against Git blob `8f10a4bc9adc5325974fa0e3cdba1a97127d3fdf` at audited base commit `93613d638d6c6bb05c997b55033234a6147b63c3`. Its SHA-256 is `81d59106d3e3eea9b438125f51e39bc0b1c27cac916b8bf980fd9f372b0718fa`. The review builder records both retained-source and assembled-manuscript hashes on every run.

## Measured fixture result

Thirty input lines produce 28 accepted raw records, two quarantined lines, 24 canonical examples and 21 protected components. Four duplicate records are collapsed without dropping their lineage. The fixed rules yield 14 labels, five abstentions and five conflicts. Of the 13 predictions with resolved reference labels, ten agree and three disagree. One duplicate has conflicting reference labels and is excluded from accuracy; two canonical examples lack reference labels.

These are executed descriptive measurements on authored fictional fixtures. They do not estimate production accuracy or generalization. No model is trained. The separately authored reference file is not an independent human annotation study. The complete audit is [checked in beside the lab](../../examples/first-release/expected/audit.json), with denominators and known mistakes.

Input record SHA-256: `6f5c21ce6e70abb56712fa0e5b6058cc678579564d9a36e22d6898af0d79071e`.

Reference-label SHA-256: `203a8bb1ed213d2a61520717adc04fdfab654dc5b6eabd3a4de63337b9c76176`.

An independent review identified a real normalization defect in the first implementation: case folding could leave a non-idempotent Unicode form. Recipe version 2 applies NFKC, casefold, a second NFKC and whitespace collapse. Regression tests cover the collision and its effect on family splitting. Existing ASCII-fixture results remain unchanged.

## Reader QA follow-up

A subsequent cloud-browser review of exact commit `416408db8adaa7eeb1edbd5b80637c64bd7fd062` identified three reader defects: an unbroken revision link widened a 390-pixel viewport, contents entries were plain text, and citation markers lacked reference links. Desktop layout, images and code wrapping were reported sound. That review separately ran a 22-test subset; it is not a replacement for the original 28-Python/15-JavaScript result above. Forty-six external links succeeded, while 96 were blocked by the browsing proxy and remain unverified. The blocked links were not retried.

The narrow follow-up adds wrapping for long text/links, manifest-owned stable chapter anchors, linked contents with return navigation, and bibliography-derived citation destinations. Citation groups and ranges preserve the exact visible marker text; unknown labels remain unlinked. Existing links, code, attributes and reference-entry text are not relinked. Duplicate destination labels/IDs fail rather than silently point somewhere ambiguous.

The updated full checks pass: **35 Python tests** (22 release-lab plus 13 assembly/navigation tests), **15 JavaScript tests**, draft assembly and `git diff --check`. New regressions verify long-link wrapping CSS, stable anchors after chapter reordering, all in-page destinations, group/range and unknown-reference handling, visible citation-text preservation, protected markup and duplicate-anchor rejection. These are structural and behavioral checks. The three changes await the requested browser recheck at their newly published commit; no new visual-pass claim is made here.

## Beginner lesson revision

The seven new chapters were rewritten after reader feedback that the earlier prose resembled implementation guidance rather than lessons. They now explain the problem and mechanism through visible examples before presenting optional tools. The opening includes the routing policy, an actual record-to-label walkthrough and coverage versus reference-agreement denominators. Augmentation is taught before semi-supervised consistency methods. The physical-data lesson centres on a supplied four-cell field; larger CAD, robotics and Rheon work is optional research.

The subsequent full suite passes **42 Python tests**: the unchanged 22 release-lab tests, 13 reader/assembly tests and 7 new worked-example checks. All **15 JavaScript tests** pass. Draft assembly, local-link checks, stable internal destinations and `git diff --check` pass. Worked-example checks verify the displayed shape move/crop, temperature update and reversed rows, fraction format/value judgments, confidence-cutoff arithmetic, actual fixture denominators, chapter ordering and the illustrated loss of nested text.

These added checks validate the consistency of the teaching examples. They do not turn the invented pseudo-label scores, fraction judgments, temperature rule or monitoring incident into trained-model, verifier-library, scientific-simulation or deployed-service results. The executable first-release fixture and its data are unchanged. The revised pages still need visual review at their new commit; prior browser findings should not be treated as a fresh layout pass on new prose.

## Checks not completed

The original local browser visual-QA attempt was made on the cloud workspace. Playwright's bundled Chromium was absent; the installed Chromium could not launch because the environment forbids a required process socket, including the permitted escalation attempt. HTML generation and structural checks passed. The later separate browser review is recorded above; a full corrected mobile-layout pass is still pending. A visual review is required before calling the new reader audience-ready.

No final PDF/export package has been produced. The existing published reader/PDF was not regenerated or deployed. No new GPU/CPU model-training comparison, neural memory measurement, external-dataset download, Math-Verify execution, companion trainer-loader integration, robot/sensor capture, Rheon run or physical validation was performed. Those tasks remain explicit research/implementation gates. Retained illustrative calculations and earlier `not_run` experiments keep their original status.

Research register entries identify paper revisions, inspected sections and acquisition limitations. Published numerical findings are attributed to their sources; source inspection is not independent reproduction. No talks or videos were watched in this pass.
