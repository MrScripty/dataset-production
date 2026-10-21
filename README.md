# Dataset Production

A principles-first fieldbook by Puma on turning raw examples into a dataset someone else can trust and use. Start with one inspectable text release, then work through source choice, labels, independence, controlled improvement, consumer contracts and recovery.

**[Read the book](https://mrscripty.github.io/dataset-production/book/)** · **[Download the PDF](https://mrscripty.github.io/dataset-production/downloads/dataset-production.pdf)** · [Source and exercises](https://mrscripty.github.io/dataset-production/downloads/dataset-production-source.zip)

The 13 October 2026 edition has 15 core chapters, six optional modality tracks and four appendices. Paper exercises come first; optional CPU labs need no GPU, paid service, account or dataset download. The browser workbench runs locally in the visitor's browser with no backend or provider calls.

## Try the first lab

Python 3.10+ and its standard library are enough. From the repository root, choose a new output directory:

```sh
python3 -B examples/first-release/build.py --out /tmp/dp-release
```

Inspect the source bytes, lineage, quarantine, labels, audit and manifest. Continue with the [first-release guide](examples/first-release/README.md), [consumer-contract exercise](examples/consumer-contract/README.md) and [recovery lab](examples/recovery/README.md).

## What the book covers

- Define the question, evidence and data contract before selecting a model
- Protect evaluation independence and treat labels as measurements
- Compare changes against a baseline and diagnose what failed
- Release bytes a named consumer can verify, then account for operation and recovery

The Rheon and Tuldok cases are pinned evidence studies. The browser Tuldok interface is an educational proposal. Authored examples, executed fixtures and published project results are labelled separately. The companion *Training Your Own Models* owns fitting and architectures; this book ends at data and consumer contracts.

## Contribute or reproduce the edition

Readers need only a browser or PDF reader. [Contributor instructions](https://github.com/MrScripty/dataset-production/blob/main/CONTRIBUTING.md) cover source layout, book/PDF builds, checks and publication. The [edition source guide](editions/principles/README.md) is included in source downloads for offline build instructions. The publishable site is checked in under `docs/`.

The [previous research edition](https://mrscripty.github.io/dataset-production/research-edition/) remains available with its original evidence boundary.

No distribution license has been selected. Public visibility alone does not grant reuse rights; referenced projects and datasets retain their own terms.
