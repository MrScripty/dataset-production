# Dataset Production: principles-first edition

Author: Puma

The 15 core chapters follow four milestones: one useful release; trustworthy evidence; a controlled improvement; and reliable delivery. Six optional modality tracks accompany the shared path after chapter 8. The opening and worked examples are hardware-free. Code is optional until a reader chooses the supplied standard-library CPU exercises.

The separate Training Your Own Models companion owns fitting implementations and architectures. This edition owns the data contract, evidence and consumer boundary. A tested educational text adapter is supported only for its named consumer, not automatically for the numeric companion.

The prior research manuscript is preserved in `editions/research-2026-10-02/manuscript.md`, with its original reader and downloads under `docs/research-edition/` and dated download names. The earlier `editions/next/` assembly is retained as a historical development draft.

Build the reviewed source with `python3 scripts/build_principles_edition.py`, then generate the reader and exact PDF/source release with `python3 scripts/build_book.py --release`. Run `npm run check` for supplied examples, structure, links and metadata. Start the local server, then run `python3 tests/browser_qa.py` and `python3 tests/book_qa.py` for separate browser/visual qualification. PDF generation needs Pandoc, ReportLab, Pillow and PyMuPDF; reader generation needs Pandoc. Actual browser QA additionally needs Playwright and Chromium in an environment with browser access. Neither is a reader runtime dependency.

Scientific sources are primary papers, official documentation or pinned public repositories. Authored illustrations, executed CPU fixtures, published results and source-inspected project receipts are visibly separated. No new project physics/model result or independent human annotation study is claimed.
