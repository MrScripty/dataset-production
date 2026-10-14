# Vision and video

A shape moves correctly in an image, but its mask stays behind. A perfect learner would now be punished for finding the actual shape. This is a representation failure we can expose before any training.

## Work an authored image and mask

Use a four-column, three-row grid. Coordinates are integer pixel indices (x,y), origin at top-left; x grows right and y down. The authored foreground occupies (1,1) and (2,1). Both image and binary mask are 1 at those positions and 0 elsewhere. Foreground is 1; background is 0; no value means ignore in this toy contract.

| Row y | x=0 | x=1 | x=2 | x=3 |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 1 | 0 |
| 2 | 0 | 0 | 0 | 0 |

Translate right by one pixel. Image and mask must now be 1 at (2,1) and (3,1). The exclusive-maximum bounding box changes from [1,1,3,2] to [2,1,4,2]. The right edge 4 is permitted for a width-four image because it denotes a boundary, not a pixel index. A mask left at its original coordinates has intersection one and union three with the correct translated mask, giving IoU 1/3. This is authored arithmetic, not a model score.

A crop to x=0,1,2 removes the rightmost foreground pixel after translation. The target must change with the crop. A caption saying “two visible foreground pixels” would become false. For a visible-mask task, do not invent the cropped pixel; for an amodal task, specify separately what hidden extent is being labelled.

## Carry this project through core 9–15

- Core 9: add empty scenes, last-column objects and occlusion events that a random batch may miss.
- Core 10: apply the joint translation; compare with the deliberately broken image-only transform.
- Core 11: review a proposed mask without treating acceptance as independent double annotation.
- Core 12: a renderer supplies scene-relative labels; verify realized visibility and reserve independent scenes before generating derivatives.
- Core 13: diagnose localization and identity separately; reserve complete recording/object/session families under the stated claim.
- Core 14: cold-read empty masks, holes, last-pixel boxes and orientation metadata; test foreground/ignore semantics, interpolation and target conventions.
- Core 15: preserve source image, accepted mask, mapping and adapter in a recovery bundle; include correction/verification time in costs.

## Exercises and worked answers

1. Write the shifted foreground coordinates. (2,1) and (3,1); the new exclusive box is [2,1,4,2].
2. Why is resizing a class-ID mask with unconstrained linear interpolation unsafe? It can create values that are not valid classes; use a label-preserving policy and check the consumer's semantics.
3. Three adjacent frames depict the same object disappearing and reappearing. Are they three independent unseen-object trials? No; retain object/recording identity and define continuity across occlusion.
4. Does a plausible generated image inherit the requested caption automatically? No. The prompt specifies intent; the accepted caption describes verified pixels.

Acceptance: image, geometry/mask, caption and family metadata must describe the same transformed example. Audit small and boundary objects, not only attractive overlays.

Visual datasets contain geometry as well as appearance. A label can be semantically correct and still be unusable because it refers to the wrong orientation, crop, pixel convention, frame, or object identity. Production should preserve the original image or video, the coordinate system of each annotation, and the transforms that produce the model input.

## Collect variation that could change the decision

Start from the deployment conditions: devices, distance, resolution, motion, illumination, background, occlusion, object state, and the prevalence of empty or confusing scenes. Collect independent physical objects and sessions where the generalization claim requires them. Hundreds of adjacent frames may improve temporal coverage without supplying hundreds of independent scenes.

A capture protocol should identify which properties are deliberately varied and which remain fixed. For an object classifier, changing backgrounds can test whether the model relies on the object. For a geometry model, varied viewpoint and partial visibility matter. For a defect detector, pristine examples alone cannot establish the boundary between normal variation and the defect of interest.

Preserve negatives with a precise meaning. An empty detection scene is a reviewed statement that no target object is present under the guide, not an unlabeled image. A background class in classification is a defined category, not a universal container for every unknown object. Ignore regions, unknown classes, and occluded parts need their own semantics.

## Choose annotation units before choosing drawing tools

A class label, axis-aligned box, rotated box, keypoint set, polygon, semantic mask, instance mask, and track answer different questions. A polygon around an object's extent can include occluded material; a visible-pixel mask excludes it. The guide must say which is intended.

Store object or instance identity separately from class identity. In video, also preserve track identity and rules for disappearance, re-entry, splitting, merging, and uncertain identity. Do not quietly assign a new ID every time an object is occluded if the task requires continuity.

Image transformations need label-aware transforms. Rotating or resizing the image without its mask is an obvious error; subtler errors come from interpolation, rounding, padding, and exclusive versus inclusive bounds. Masks containing discrete class IDs generally need label-preserving resampling rather than interpolation that creates new class values. A value of 255 can mean foreground in one binary format and ignore in another. The consumer contract decides.

Use tiny boundary fixtures to test conversions: a one-pixel region on the last row/column, an empty mask, a hole, a partially visible object, and a rotated image with orientation metadata. A large attractive overlay can conceal an off-by-one error. The exact corner-versus-box and binary-mask contracts of the training companion are retained in the appendix as concrete examples.

## Simulation provides known scene state

A procedural scene can expose object identity, pose, depth, camera parameters, visible masks, optical flow, and other targets that would be expensive to annotate manually. The renderer knows the scene state; that makes some labels exact relative to the simulation. It does not make the simulated world representative of the real deployment.

Kubric joins a scene description, a physics simulator, rendering, and export. Its published pipeline supports annotations including segmentation, flow, depth, normals, trajectories, collision events, and camera parameters. This illustrates the advantage of generating inputs and targets from shared structured state rather than asking an image model to invent both independently. Asset provenance, renderer versions, and simulation assumptions still matter. [R29]

An original scene recipe for a tabletop task might sample object type, pose, distractor count, camera distance, light direction, and material. Validate physical plausibility and target visibility before rendering an expensive high-resolution frame. Save the sampled factors and realized measurements, such as visible area or actual occlusion fraction. A requested occlusion level is not a measured one.

Separate errors in the renderer, simulator, asset metadata, and target extraction. Transparent or reflective objects can make visible boundaries ambiguous. Motion blur complicates the definition of a per-pixel target. Collision meshes may differ from rendered geometry. A perfect mask of an unrealistic scene can teach the wrong deployment behavior.

## Domain randomization is a transfer hypothesis

Domain randomization varies nuisance factors so that a learner cannot rely on one synthetic appearance. Tobin and colleagues randomized textures, objects, camera properties, and lighting in a simulated localization task and demonstrated transfer in their real-world setup. This is evidence that photorealism is not always necessary for useful transfer, not proof that arbitrary randomization covers every real environment. [R30]

Choose ranges from observed deployment conditions and plausible uncertainty. Broad randomization can improve robustness, but physically impossible combinations waste capacity or teach artifacts. Too little variation encourages shortcuts. If a factor changes the target rather than merely its appearance, update the target accordingly.

Evaluate on real held-out captures that were not used to tune the recipe. Compare real-only, synthetic-only, and mixed training where the budget permits, and include an equal-compute or equal-example baseline. A synthetic validation set generated by the same renderer mostly measures consistency with that renderer. Inspect which real slices benefit and which regress.

Simulation assets also carry rights and coverage limitations. A diverse texture library does not guarantee diverse object shapes or behaviors. Changing random seeds without changing the underlying asset set may add appearance variety while preserving a narrow shape distribution.

## Model assisted masks need temporal quality checks

Interactive segmentation can reduce drawing effort: propose a mask, correct it, propagate it, and inspect failures. Record the model, prompt/clicks, human corrections, and accepted revision. Review missed objects and disputed boundaries rather than only whether the suggested region looks plausible.

Video propagation introduces drift, identity swaps, lost objects, and failures at occlusion or re-entry. Sample both routine frames and event boundaries, and inspect the complete trajectory at a speed that reveals temporal discontinuities. A high mask overlap on selected frames can coexist with incorrect identity association.

The HOTA metric formalizes the need to account for detection, association, and localization rather than only per-frame detection. Its decomposition provides a useful debugging vocabulary even when a project uses a different task-specific metric. A tracker can find the right boxes while attaching them to the wrong object histories. [R31]

A video review guide should define interpolation and propagation policies, annotation frame rate, how unreviewed frames are marked, and whether a model-filled interval counts as accepted supervision. Use actual media timestamps where frame timing is irregular. Split at the independent recording/session or object level required by the claim, not by random neighboring frames.

## Captions for image generation

For image-generation training, keep image, caption or conditioning, rights, quality checks, and transform history. Store the original caption and recaptioned revisions. An accurate simple caption can be more useful than a richly detailed false one. Ground nouns, counts, colors, composition, text, and style claims in the actual image.

DALL-E 3 research is evidence that descriptive generated captions can improve prompt following under its studied setup. It does not establish a universal preference for longer captions or publish the full image corpus. A production team should compare caption policies using a fixed evaluation rather than adopt verbosity as a quality metric. [R32]

A generation prompt is a request, not a verified description of the result. Keep original prompts, image-conditioned caption revisions, and accepted captions separate. Check nouns, counts, relationships, visible text, and style claims against the image after every crop or transform. A crop can remove the object that justified the caption. Compare caption policies through held-out prompt following and image quality, not caption length alone.

For a captioning audit, stratify by caption origin and difficult visual attributes. Let the reviewer mark supported, wrong, omitted, and unverifiable spans. Retain a simple accurate caption when the alternative adds unsupported detail. If the intended task needs only a class token or a short subject description, do not force a long scene narrative merely because another training recipe used one.

## Optional tools

A drawn grid is sufficient. Image editors, segmentation assistants and video review tools can reduce labor after the guide and boundary fixtures are established. Freeze their versions and exported conventions; their availability does not establish mask quality. The SAM 2 case below separates proposal speed from verified temporal quality.
