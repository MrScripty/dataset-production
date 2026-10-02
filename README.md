# Dataset Production

A public fieldbook and interactive dataset-production workbench, built as a dependency-free static site for GitHub Pages.

## Read and explore

- Site: https://mrscripty.github.io/dataset-production/
- Current book: the delivered **Dataset Production**, research edition, 2 October 2026 (16 chapters, four appendices, 80-page PDF)
- General hands-on labs: geometry, split families, synthetic review, lineage, and frozen releases
- Application concept: proposed Tuldok workspaces, clearly separate from the actual Tuldok application

The site contains no backend, analytics tracker, provider calls, user accounts, or private datasets. Lab state is stored in the visitor’s browser and can be reset or exported. No actual Tuldok repository changes are implied.

## Local development

Requirements: Node.js 20+ for unit tests; Python 3 for serving and rendering; Pandoc only when rebuilding book HTML.

```sh
npm test
npm run build
npm run serve
# open http://localhost:8094
```

The optional browser QA script needs Python Playwright and Chromium already installed:

```sh
python tests/browser_qa.py
```

`docs/` is the complete publishable site. GitHub Pages is configured to deploy from `main` → `/docs`, with `.nojekyll`. No CI action or bundling is required for publication.

## Updating the book

Only publish a reviewed, delivered manuscript. Replace `docs/book/manuscript.md`, copy the corresponding original diagrams to `docs/book/figures/`, replace the PDF/source downloads, then run `npm run build`. When the title, chapter count, page count, or edition changes, update the explicit edition text in `scripts/build_book.py`, `docs/app.js`, `docs/about.html`, and this README as well. Keep version claims aligned across reader, download, and landing page; never mix in unfinished research tranches.

The source bundle contains only the delivered manuscript and its original diagrams. Raw source caches, internal research notes, local credentials, and tool receipts are not included.

## Educational boundaries

The lab PNG is a real 8-bit grayscale 0/255 mask. The frozen release is an educational JSON manifest, not a complete or loader-tested training bundle. The synthetic candidate checker verifies only narrowly defined fixture properties; its illustrative judge scores have no acceptance authority. The provenance exercise records a conceptual crop/review relationship and does not silently transform the independent geometry exercise. The static Tuldok application screen is a proposal.

The book’s external-method findings are attributed to primary sources. Repository observations are pinned to inspected commits. No model-training or Tuldok-runtime test is claimed by this site.

## Reuse and privacy

No distribution license has been selected for the book or repository. Public visibility does not automatically confer a reuse license. Lab records and images are original procedural fixtures, with no third-party personal data. Referenced projects and datasets retain their own licenses and terms. See `docs/about.html` for fixture scope, privacy, and limitations.
