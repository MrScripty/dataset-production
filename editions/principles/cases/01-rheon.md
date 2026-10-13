# Rheon as a physical data evidence chain

A pressure replacement agrees closely with a simulator and makes one rollout faster. What exactly has been learned, which examples supplied the evidence, and which part of the cost was timed? These questions transfer to any simulation-generated dataset.

Evidence status: the public source and preserved run receipts were inspected at rheon-surrogate-lab revision e8a90bfef6b2955c502008ccc62443e29dd9f2ec on 13 October 2026. The timing arithmetic and freeze hash were checked for this edition. No new fitting, physics run, physical observation or independent full-field replay was performed. The upstream verification is a published project receipt, not a fresh reproduction here. The laboratory experiment's Rheon source is 2209012bc5f902693d0f695ec1c2d854126af317; the subsequently observed Rheon main c7e88d8dfd58969e6020d089a11fb96795f0f5e3 does not replace that run identity.

## Start from the supported question

The recorded trajectory-v2 experiment asks whether a fitted pressure response can replace iterative pressure solving in one 32³ uniform sealed cube, with prescribed forcing and a passive tracer. It excludes a free liquid surface, viscosity, obstacles and moving boundaries. An analytic spectral inverse exists for this operator; the experiment does not establish an advantage over it. Agreement with this discretized flow is a numerical comparison, not physical validation or evidence for a new regime. These exclusions are explicit in the [pinned experiment description](https://github.com/MrScripty/rheon-surrogate-lab/blob/e8a90bfef6b2955c502008ccc62443e29dd9f2ec/experiments/trajectory-v2/README.md).

Keep this scope separate from Rheon's other pressure, material, obstacle and transport developments. A project name is not one physical model or one dataset contract.

## Generation and the actual independence units

The [generation driver](https://github.com/MrScripty/rheon-surrogate-lab/blob/e8a90bfef6b2955c502008ccc62443e29dd9f2ec/scripts/trajectory_experiment.py) uses training seeds 100–111. It captures eight frames from each of 12 training trajectories: 12×8=96 frames. Validation seeds are 500 and 501; final comparison seeds are 900–903. Adjacent frames share an evolving state, and all these trajectories share the same operator and forcing family. Treating the 96 frames as 96 independent systems would exaggerate evidence. Distinct seed IDs separate recorded paths; they do not demonstrate diversity of boundaries, geometry, density or physical regimes.

The native probe has a one-unit-wide cubic grid, spacing 1/32, step duration 1/60 second and density 1.25. The [probe source](https://github.com/MrScripty/rheon-surrogate-lab/blob/e8a90bfef6b2955c502008ccc62443e29dd9f2ec/probes/trajectory/src/main.rs) binds these values and verifies accepted numerical states. An audit must still preserve their physical interpretation. Pressure is cell-centered; u, v and w are on faces normal to their own axes. The documented pressure-data convention is x-fast flattening, i+nx(j+ny k), or [z,y,x] after a Python reshape; pressure is Pa, pressure offset [0.5,0.5,0.5], and each MAC component has zero offset along its own axis. The documented operator-scaled RHS/residual unit is m³/s², not simply “pressure”. These conventions are stated in the [pinned laboratory data contract](https://github.com/MrScripty/rheon-surrogate-lab/blob/e8a90bfef6b2955c502008ccc62443e29dd9f2ec/README.md). That contract and the trajectory stream are distinct versioned representations; do not claim the small stream header alone contains the full release manifest.

For a transferable release, require original fields, component shapes and offsets, axes, units, accepted time, density, forcing and boundary definitions, pressure gauge, source/binary versions and every relevant hash. A plausible rendered picture cannot validate those meanings.

## What fitting actually changes

The actual fit is supervised modal least squares, not iterative neural-network training. The [model implementation](https://github.com/MrScripty/rheon-surrogate-lab/blob/e8a90bfef6b2955c502008ccc62443e29dd9f2ec/scripts/trajectory_model.py) transforms each training RHS and reference pressure into an orthonormal cosine basis. For each nonconstant mode it fits a gain using the sum of input×target coefficients divided by the sum of squared input coefficients. The constant mode is excluded and pressure is gauge-aligned. The basis encodes geometry; the response gains are learned from the supplied pressure labels.

On a 32³ grid this fits 32³−1=32,767 modal gains with zero optimizer steps. Zero optimizer steps does not mean zero learned parameters or zero fitting work. The [freeze](https://github.com/MrScripty/rheon-surrogate-lab/blob/e8a90bfef6b2955c502008ccc62443e29dd9f2ec/experiments/trajectory-v2/freeze.json) records method supervised_modal_least_squares, fitted_parameters 32767 and optimizer_steps 0. Its 0.1953-second training_wall_s measures the fit call after generated arrays exist; it is not total acquisition, generation, review, model startup or project labor cost.

A hardware-free miniature illustrates the statistic. One modal input coefficient is [1,2] and its target coefficient is [3,6]. The fitted gain is (1×3+2×6)/(1²+2²)=15/5=3. Applying it to input 4 predicts 12 under this authored relationship. No gradient steps are needed, yet the gain was estimated from data. If both input coefficients are zero, the denominator is zero and the mode is unexcited; refuse rather than invent a fitted response. This miniature explains the data requirement without implementing the real model or claiming physical validity.

## Review freeze rollout and exposure

The actual driver generates and fits training data, uses validation for accuracy/runtime qualification, checks an untrained-gain ablation, then saves pre-test conditions and checkpoint/input hashes. Preserve that order; the recorded freeze is after fitting and validation, not evidence of an earlier immutable training release. Its checkpoint SHA-256 is 25533a2fbaa5ab0f5fb574dc6307a2b8d6a686deb7db867d0d03338d4d70d5a9; the training-data hash is 3ca87734e4ebe41320328b130908dc88b85967dcc745f80f8c207cf29b539184. Numerical gates and upstream verification are evidence channels, not independent human annotation of every frame.

Final evaluation then compares complete 120-frame rollouts, representing two simulated seconds, for four seeds. Once those outputs informed reports or were inspected, the seeds became exposed. Replaying seeds 900–903, using a new output filename or drawing later frames from those trajectories does not create a fresh holdout. Distinguish unseen seeds within this fixed family from genuinely unseen regimes. Independent holdout claims require new protected initial-condition/trajectory families reserved before the new selection process; use a narrower claim if those are unavailable.

## Verify the actual timing claim

The [actual result artifact](https://github.com/MrScripty/rheon-surrogate-lab/blob/e8a90bfef6b2955c502008ccc62443e29dd9f2ec/experiments/trajectory-v2/result.json) has 60 timing entries: three methods×four seeds×five repetitions, each with 120 frames. Recomputed medians are 22.0055 s Jacobi, 19.0796 s SGS and 5.1761 s fitted response. Ratios are 4.2513× and 3.6861×. The 7,200 timed frames are operational repetitions over four seeded cases, not 7,200 independent scientific trials. The recorded environment is Pumas-managed PyTorch 2.14.0+cu132 on an RTX 5090 Laptop GPU. These first native comparisons are single-threaded; a separate later parallel comparison has a different receipt and must not be silently combined with them.

The timing scope includes native startup/teardown, all simulation kernels, inference, transfers, numerical gates and report parsing with a resident model. It excludes capture/rendering, Python/model initialization and explicit warmup. Therefore this is neither model-only latency nor a complete cold-start user pipeline. The separately recorded fresh-process startup check uses a different sampling design. Quote each only with its boundary, hardware/runtime and comparator quality conditions.

The upstream [verification receipt](https://github.com/MrScripty/rheon-surrogate-lab/blob/e8a90bfef6b2955c502008ccc62443e29dd9f2ec/experiments/trajectory-v2/verification.json) reports independent full-field error recomputation, frame qualification and hash checks: maximum velocity relative L2 error 8.8857e−8 and tracer relative L2 error 5.8869e−8 in the first comparison. Those small differences measure agreement with the reference discretization. The bulk full fields were not materialized/replayed for this edition, so the independent-replay claim belongs to that published receipt.

## Numerical checks physical checks and total economics

Numerical qualification should cover finite fields, residual/divergence, accepted clocks, gauge, boundary compatibility, conservation/work ledgers where applicable, and sensitivity to grid resolution/tolerances. These ask whether the specified numerical model is implemented and solved acceptably. Physical validation asks whether relevant observations agree sufficiently for the intended use. [NASA/NPARC's verification and validation guidance](https://www.grc.nasa.gov/WWW/wind/valid/tutorial/overview.html) makes that distinction explicit. Neither a small simulator-to-surrogate error nor a convincing animation supplies physical observations.

For a production cost comparison, collect all source generation attempts, refusals, fitting, validation, repeated timing/evaluation, review, storage/transfer, consumer integration and incident repair. Compare cost per accepted record or accepted independent trajectory at matched numerical quality. The preserved resident timing does not identify those missing costs. A residual gate can catch an unacceptable fitted pressure, but a negative-path cleanup bug still affects reliable operation: the experiment description records a buffered-pipe cleanup race and a corrected close-time BrokenPipeError handler. The frozen timed driver is retained separately; the repair did not justify replacing historical timings.

## Exercises and worked answers

1. What was learned with zero optimizer steps? 32,767 modal response gains from supervised pressure labels.
2. What is the training denominator? 96 frames, grouped into 12 seeded trajectories in one operator/forcing family; frame-level independent uncertainty is unjustified.
3. Can the fit-call 0.1953 s be compared with whole-release collection cost? No. The scopes differ and generated arrays already exist before that timer starts.
4. What does a replay of seeds 900–903 establish now? Reproducibility/compatibility within exposed cases, not fresh model-selection evidence.
5. What evidence is still required for a different boundary or physically realistic liquid claim? A revised source/representation contract, protected new regimes, numerical qualification and use-relevant physical observations. None is supplied by this fixed-box receipt.

Acceptance: trace the data, fit and numerical consumer; keep denominators and timing scopes honest; mark missing independent replay, physical observations and total cost as missing. The beginner four-cell example remains sufficient for the track's paper milestone.
