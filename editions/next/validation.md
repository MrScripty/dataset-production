# Validation and evidence boundaries

Checked 11 October 2026 against the initial next-edition draft. Author credit remains Puma. The delivered manuscript and all published `docs/` artifacts are unchanged by this increment.

## Executed checks

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

## Checks not completed

Browser visual QA was attempted on the cloud workspace. Playwright's bundled Chromium was absent; the installed Chromium could not launch because the environment forbids a required process socket, including the permitted escalation attempt. HTML generation and structural checks passed, but no screenshot-based or mobile-layout pass is claimed. A visual review is required before calling the new reader audience-ready.

No final PDF/export package has been produced. The existing published reader/PDF was not regenerated or deployed. No new GPU/CPU model-training comparison, neural memory measurement, external-dataset download, Math-Verify execution, companion trainer-loader integration, robot/sensor capture, Rheon run or physical validation was performed. Those tasks remain explicit research/implementation gates. Retained illustrative calculations and earlier `not_run` experiments keep their original status.

Research register entries identify paper revisions, inspected sections and acquisition limitations. Published numerical findings are attributed to their sources; source inspection is not independent reproduction. No talks or videos were watched in this pass.
