# Dataset Production next edition

Author: Puma

Working edition begun 11 October 2026. The delivered 2 October book remains in `docs/book/manuscript.md`; its published reader and downloads are not replaced by this draft.

## Start here

Read [the progression and project tracks](progression.md), then [the first release chapter](chapters/first-release.md). Run the supplied CPU lab from the repository root:

```sh
python3 examples/first-release/build.py --out /tmp/dataset-first-release
python3 -m unittest discover -s tests -p 'test_first_release.py' -v
```

The new chapters and retained chapters are assembled in a deliberate reading order with:

```sh
python3 scripts/build_next_edition.py --out /tmp/dataset-next-edition
```

This produces a review manuscript and HTML outside the published website. [The research register](research-register.md) records primary evidence, versions, limitations and open work. [The validation record](validation.md) distinguishes executed checks from designs that still need experiments.

## New sections ready to read

- [First release from supplied data](chapters/first-release.md)
- [Extraction normalization and measured audits](chapters/extraction-audits.md)
- [Weak and semi-supervised labels](chapters/weak-semisupervised.md)
- [Target-valid augmentation](chapters/augmentation.md)
- [Reasoning tasks verifiers and trajectories](chapters/reasoning-trajectories.md)
- [Physical systems and simulation evidence](chapters/physical-systems.md)
- [Monitoring repair and rollback](chapters/monitoring.md)

## Scope of this draft

The first increment supplies a hardware-free opening, a measured release lab, and new methods chapters on operational cleaning, weak and semi-supervised labels, augmentation, verified reasoning and trajectories, physical representations, and production monitoring. It reuses every substantive chapter and appendix of the delivered book, including active learning, uncertainty, mixture methods, influence and five published lab cases. Retained claims keep their original evidence date; newly researched claims carry their own source versions.

The assembly changes chapter order without changing the delivered sources. Application-specific Tuldok material remains the closing optional application, after methods. The existing companion contract appendix is retained and supplemented, not replaced by an assumed universal loader.

This is an initial next-edition draft, not a claim that all proposed projects have been implemented. The small release pipeline is executed; larger training experiments, model comparisons, physical validation, full companion compatibility and an audience-ready PDF remain future gates. Original illustrative calculations and `not_run` experiments in retained material remain illustrative or unrun.

## Publication boundary

No merge, Pages deployment, release download replacement or new blanket license is part of this increment. Fixture data are authored educational material with no real customers or third-party personal data. Existing repository rights remain unchanged. Open external datasets retain their own terms; acquisition checks are part of each track.
