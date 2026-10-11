# Represent physical systems and qualify simulation data

Physical data adds obligations that an ordinary row validator cannot satisfy. Coordinates, units, topology, boundary conditions, time and numerical assumptions all affect the meaning of an array. The first step can still be small: inspect one supplied schema or an authored geometric example. Buying a robot, collecting sensor readings or downloading terabytes is not a prerequisite for learning these contracts.

## Know which representation answers the question

A CAD construction program records editable operations and their order. A boundary representation, or B-rep, describes surfaces and their topological relationships. A surface mesh approximates a boundary with faces; a volume mesh also partitions the interior. A point cloud samples locations without necessarily preserving connectivity. A field attaches values to spatial positions or cells. A trajectory adds evolution over time. Synchronized sensor data combines measurements with clocks, calibration and coordinate relationships.

These are different kinds of evidence, even when they describe the same object. Triangulating a curved B-rep loses some exact geometric information. Sampling points from a mesh changes resolution and often drops topology. A rendered pressure image depends on camera, color scale and compositing; it is not the pressure field itself. A watertight surface does not automatically supply a suitable CFD volume mesh.

For each conversion, retain the parent ID, method/version, tolerances, coordinate frame, units and a mapping back to source elements when available. Check orientation, scale, degeneracies, disconnected components and missing boundaries. A task may require some properties and tolerate others; don't hide invalidity behind a generic “3D file loaded successfully” flag.

[Autodesk Fusion360 Gallery's reconstruction specification](https://github.com/AutodeskAILab/Fusion360GalleryDataset/blob/master/docs/reconstruction.md) is a useful concrete bridge. It describes construction JSON, B-rep files, triangulated OBJ and thumbnails, with mesh faces related to source B-rep faces. The stated units are centimetres and radians, and the supplied meshes are not manifold. Point clouds and voxels are possible derivatives, not included ground truth. Record the release and exact conversion used rather than assuming every modality is present.

## Attach physical meaning to fields

A field tensor needs axis names and order; location conventions; units; grid or mesh coordinates; scalar/vector/tensor interpretation; time values; and masks or missing-value rules. A velocity on cell faces is not interchangeable with a velocity at cell centres. Pressure differences may be meaningful while absolute pressure is defined only up to an additive gauge. For a rotated coordinate frame, vector components and tensor components must be transformed consistently, not merely relabeled.

A simulation record should also identify governing equations, material parameters, initial and boundary conditions, numerical method, solver tolerances, discretization and convergence diagnostics. Preserve failed solves with clear status in the production audit. Silently deleting difficult cases can make the dataset appear accurate while removing the conditions in which the intended model is most likely to fail.

[The Well's version-1 paper](https://arxiv.org/html/2412.00568v1) presents a broad collection of simulation trajectories, not direct physical observations. Its [format documentation](https://polymathic-ai.org/the_well/data_format/) illustrates coordinates, time, scalar/vector/tensor fields and boundary metadata in HDF5. The data are stated as CC BY 4.0; the loader code has a separate BSD-3-Clause license. A package version does not pin the dataset payload or prove that an upstream processing correction has been applied.

## Verification and physical validation answer different questions

[NASA/NPARC's guidance](https://www.grc.nasa.gov/WWW/wind/valid/tutorial/overview.html) distinguishes verification of a mathematical/numerical implementation from validation against physical reality for the intended use. This distinction is essential when simulation supplies training targets. A student can accurately imitate a numerical approximation while inheriting its model mismatch or numerical error.

Build an evidence ladder:

1. **Implementation checks:** units, shapes, boundaries, analytic or manufactured cases, and invariants applicable to the equations.
2. **Numerical-solution checks:** residual and convergence criteria, discretization/refinement studies, and sensitivity to tolerances.
3. **Surrogate checks:** error against independently checked numerical targets on held-out conditions, plus constraint and rollout behavior.
4. **Physical validation:** comparison with relevant measurements and their uncertainty, within the use domain of the physical model.

These stages are complementary. Matching two solvers is useful evidence but can share errors. A small residual does not by itself establish fine enough spatial resolution, and grid convergence does not by itself establish correct physical assumptions. An attractive animation measures neither. See [NASA's verification assessment](https://www.grc.nasa.gov/www/wind/valid/tutorial/verassess.html) for the distinct checks; do not interpret its historical statements about standards as a current standards survey.

Split whole simulations and geometry/parameter families before creating windows or frames. Adjacent snapshots from one run can be nearly identical. A random frame split may answer whether a model interpolates within a familiar run while being presented as evidence for new conditions. Name which extrapolation is attempted: new initial state, forcing, geometry, material, resolution or physical regime. Treat each as a separate claim.

## Synchronized recordings require more than timestamps

[DROID's April 2025 paper revision](https://arxiv.org/html/2403.12945v2) describes robot demonstrations with camera streams, actions and calibration. Its calibration discussion includes quality measures and difficult cases. A common recording clock does not establish correct geometric registration, exposure timing, action delay or absence of dropped frames.

A useful episode contract names clock domains, timestamp units, frame/action rates, calibration versions, camera poses, reset semantics, termination and missing data. Audit synchronization with events visible in more than one stream. Test whether interpolation or resampling changes the supervision target. Keep a scene/session/operator split when those relationships matter, rather than placing consecutive frames in different partitions. Existing recordings can teach these checks without reproducing the original hardware collection.

## Graduated acquisition paths

- **The Well:** begin with the [official visualizer and access documentation](https://polymathic-ai.org/the_well/). The documented selective command is `the-well-download --base-path PATH --dataset active_matter --split train`; omitting selectors can request the whole collection. Active matter's full listed subset is 51.3 GB, so even this is an advanced acquisition choice, not a tiny exercise. Decide on a bounded file/trajectory and budget before downloading. Check the [repository's correction notice](https://github.com/PolymathicAI/the_well) for `viscoelastic_instability_v2`; the older name is deprecated for processing errors.
- **Fusion360 Gallery:** read the [release index](https://github.com/AutodeskAILab/Fusion360GalleryDataset) and schema first. Reconstruction `r1.0.1` is a 2.0 GB release, with a smaller 41 MB face-extrusion supplement that does not contain every modality. The [dataset terms](https://github.com/AutodeskAILab/Fusion360GalleryDataset/blob/master/LICENSE.md) limit use to noncommercial research and restrict redistribution. Commercial learners should use their own authored CAD examples or choose separately permitted data.
- **DROID:** start with the [visualizer or sample-loading notebook](https://droid-dataset.github.io/droid/the-droid-dataset). The documented 100-episode RLDS subset is `gs://gresearch/robotics/droid_100`, approximately 2 GB. Full RLDS and raw collections are much larger. The documentation still reports missing raw episodes while calling RLDS complete; inspect the actual manifest instead of assuming an old promised fix occurred. Pin object generations/checksums on acquisition and retain the stated CC BY 4.0 attribution.

No payload from these collections was downloaded for this draft. Published sizes and terms are dated acquisition planning evidence, not a completed rights or file-integrity audit.

## A bounded Rheon pressure-surrogate project

Rheon is a future design case here. Its [public fixed-box comparison description at revision 34235d3](https://github.com/MrScripty/Rheon/blob/34235d33c886aa05b5bdf95d920b863d1fb2ad6f/README.md) describes bounded 3D solver work, which does not supply a qualified general solver or a ready-made training corpus. A useful first research question is whether a learned initial guess can reduce the work of an existing pressure solver while preserving its acceptance criterion.

Begin with one fixed three-dimensional box/grid, density, timestep and boundary-condition family. Record the actual pressure operator, right-hand side, consistent pressure gauge, pre-correction velocity and reference pressure/diagnostics. Vary smooth genuinely three-dimensional forcing within a declared range. A small grid CNN/U-Net can be compared with simple nonlearned initial guesses; a graph network is not required merely because the problem is physical. Instrumentation and qualified data generation must come before model training.

Use the prediction as a warm start for the numerical solve, retaining residual-based stopping and fallback. Compare total time for inference, conversion, checks and cleanup iterations with the existing numerical baselines at matched achieved tolerance. Report pressure error after gauge handling, full residual, corrected-velocity divergence, boundary compliance and self-fed rollout behavior. Split complete scenarios/forcing families, never adjacent fields. No speedup or training budget is established by this proposal.

Pressure prediction in a conventional fluid pipeline has precedent in [Tompson et al., ICML 2017](https://proceedings.mlr.press/v70/tompson17a.html). That precedent does not validate Rheon's implementation or establish engineering CFD accuracy. Qualification still needs independent numerical checks and, for claims about physical reality, suitable experimental validation. The Well, CAD sequences and robot demonstrations provide useful production lessons; none automatically supplies the required Rheon operator–right-hand-side–pressure pairs.

**Try it.** Write a schema for one pressure sample without generating it. State the grid locations, axes, units, gauge, boundary representation, solver status and family ID. Then identify exactly which physical claim the stored evidence cannot establish.
