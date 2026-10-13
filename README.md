# Dataset Production

Author: Puma

A principles-first fieldbook and dependency-free dataset-production workbench for GitHub Pages.

- Read: https://mrscripty.github.io/dataset-production/book/
- Current edition: 13 October 2026, 15 core chapters in four parts, six optional modality tracks, four reference appendices, 152-page PDF
- Start with one hardware-free, inspectable text release; learn the reason and theory before workflows
- Progress through paper exercises, optional standard-library CPU labs, controlled improvements and a defended capstone
- Pinned Rheon and Tuldok cases teach transferable evidence and operational principles
- Previous research reader: https://mrscripty.github.io/dataset-production/research-edition/

The browser site has no backend, analytics tracker, provider calls, accounts or private datasets. Browser lab state stays in the visitor’s browser. Its Tuldok interface is an educational proposal, distinct from the actual current Tuldok application described in the book’s pinned case.

## Reproduce the examples

Python 3.10+ and its standard library suffice. No account, GPU, sensors, paid service, dataset download or model is required. Choose new or empty output directories:

```sh
python3 -B examples/first-release/build.py --out /tmp/dp-release
python3 examples/consumer-contract/contract.py --release /tmp/dp-release --out /tmp/dp-consumer
python3 examples/consumer-contract/contract.py --read --out /tmp/dp-consumer
python3 examples/recovery/recovery.py --out /tmp/dp-recovery
python3 -B -m unittest discover -s tests -v
```

The first lab retains source bytes, exact reference input, lineage, quarantine, known leakage groups, imperfect weak labels, audit and manifest. The consumer checks emitted bytes against exactly `educational-text-routing-1`; it is not a text adapter for the numeric training companion. Recovery demonstrates restart, rollback and restoration from a separate toy backup after complete working-tree loss, with its one-filesystem limitation explicit.

## Build and qualify the book

Node.js 20+ runs browser-lab unit tests. Python and Pandoc assemble/render the book. Generating PDF additionally needs ReportLab, Pillow and PyMuPDF; browser QA needs Playwright and Chromium in an environment with browser access. Readers need none of these tools.

```sh
npm run build
npm run release
npm run check
npm run serve
# In another shell after the server starts:
python3 tests/browser_qa.py
python3 tests/book_qa.py
```

`docs/` is the complete publishable site. GitHub Pages deploys `main` → `/docs`; no CI workflow is needed. Publication still requires independent pedagogy/technical/evidence review, all applicable checks and visual inspection of the exact web/PDF candidate. Do not substitute a draft or unchanged old review for the rewritten edition’s qualification.

## Source and migration

`editions/principles/` contains the modular source and edition metadata. `scripts/build_principles_edition.py` assembles it into `docs/book/manuscript.md`. `scripts/build_book.py --release` renders the reader, produces its actual PDF, records the real page count, packages public source/exercises and hashes the release. The source bundle contains no private notes, source caches, credentials or execution receipts unrelated to the public book.

The original research manuscript remains in `editions/research-2026-10-02/manuscript.md`, its original reader under `docs/research-edition/`, and its exact PDF/source downloads use dated names. Earlier `editions/next/` modules remain a historical development draft. Section migration is accounted for in `editions/principles/migration.json` and the writers’ topic maps. The preserved research edition retains its original evidence boundary.

## Evidence, companion and rights boundaries

Authored illustrations, executed CPU fixtures, published results and source-inspected project receipts are separately labeled. The authored reference file is not an independent human annotation study. Many frames from a few trajectories are not independent trials. Numerical verification is different from physical validation. Project timings are bounded by their measured interval; they do not stand for the total data-production cost.

Training Your Own Models remains a separate companion for fitting implementations, architectures and neural training. This book ends at data and consumer contracts. A hash establishes byte identity, not correctness, authenticity, permission or compatibility.

No distribution license has been selected for this repository or book. Public visibility does not automatically confer reuse rights. Supplied fictional fixtures contain no third-party personal data; referenced projects and datasets retain their own licenses and terms.
