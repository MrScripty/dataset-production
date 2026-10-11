# Monitor repair and roll back a production release

A release can pass its original checks and become unsuitable later. A source changes format, a labeling guide is revised, new operating conditions appear, or a downstream loader interprets a field differently. Production maintenance needs a reversible process for noticing, diagnosing and correcting such changes. This chapter proposes an operational protocol; it does not claim that a deployed service was monitored for this edition.

## Monitor the contract before interpreting model scores

Separate four observation layers. Pipeline health asks whether sources can be fetched, decoded and processed. Data health asks whether schemas, units, missingness, duplicate rates, source balance and label routes changed. Model behavior asks about errors, calibration, abstention and important slices. Outcome health asks whether the application still achieves its real purpose. One dashboard number cannot represent all four.

An increase in quarantine rate after a source change may expose a correct validator doing its job. A stable model score can coexist with a broken source if the sampled evaluation never reaches that source. Feature drift alone does not prove a model is failing; it is a reason to investigate. Conversely, harmful label or target changes may occur without conspicuous feature drift. Pair automatic signals with delayed outcome labels and routine random review where those are available and permitted.

Every monitored measure needs an owner, unit, denominator, baseline window, review cadence, threshold rationale and response. Choose windows that reflect the application's rate and consequences; do not prescribe one universal percentage. Report independent families or time blocks when row-level counts would exaggerate evidence. Repeatedly testing the same stream creates multiple-comparison and dependence issues, so an alert is a diagnostic prompt rather than an automatic causal explanation.

## A minimal incident record

Record what changed, when it was first observed, which sources/releases/models may be affected, and which downstream products consumed them. Link the source revision, extraction/normalization recipe, annotation guide, verifier and export adapter. Preserve representative failures and a privacy-aware sample of apparently normal cases. Compare the emitted data, not just a screenshot of the source platform.

Classify the suspected cause before choosing a repair. A parsing failure suggests fixing extraction and rebuilding descendants. An annotation-policy change may require relabeling and a new target version. A novel input population may require new coverage and a revised deployment boundary. A training regression can occur even when the dataset bytes are unchanged. More generated data is not a universal incident response.

Keep an audit trail of decisions and unresolved questions. A diagnosis can change as evidence arrives. Separate observed facts from hypotheses, and keep failed repair attempts available so the same mistake is not repeatedly rediscovered.

## Candidate releases and reversible promotion

A safe repair is a new immutable candidate, not an in-place replacement of the bytes behind an old release name. Re-run the loader, lineage, split, rights and targeted regression checks that apply to the change. Also retain a random audit to detect regressions outside the incident slice. If downstream evaluation uses a protected final holdout, do not repeatedly tune to it; use development material for repair and obtain a fresh holdout when exposure invalidates the original test.

A release registry can record `candidate`, `approved`, `active`, `superseded` and `withdrawn` states with reasons. Keep the mapping from a deployed model to dataset release, preprocessing, training configuration and model artifact. An active pointer is a convenience for deployment; it must resolve to immutable identities. Make promotion conditional on predeclared acceptance checks and authorized review, not the mere presence of output files.

Where the application permits it, a shadow comparison or limited rollout can reveal compatibility and distribution problems before broad use. Its population, duration and stopping conditions must be justified by risk and traffic, not chosen after seeing favorable results. High-impact applications need their own domain controls and expert review beyond this educational protocol.

## Rehearse rollback rather than only documenting it

Before relying on a rollback plan, test that the previous approved artifacts can still be located and loaded. Check schema and feature compatibility with the current application, dependency versions, cache invalidation, permissions and routing. A dataset rollback may require a model and preprocessing rollback too. A model trained on a problematic release does not forget it when a dataset pointer changes.

Define triggers and authority: who can stop ingestion, suspend a candidate, revert the active bundle, or withdraw a release? Record the evidence that led to the action and the checks that show it took effect. Preserve the faulty candidate for investigation where retention and permissions allow, but prevent accidental reuse by marking its status and descendants. Withdrawal and deletion may have different legal, technical and recovery implications.

For the first-release lab, a simple rehearsal can stay entirely local. Build two candidates into separate empty directories, verify their manifests, keep the first intact, and switch a small consumer's chosen path back after a failed check in the second. This is a proposed exercise until that consumer and switching test exist; the current executable lab builds and verifies a candidate, not a deployment system.

## Close an incident with evidence

A repair is complete when the corrected release passes the relevant gates, affected downstream products are accounted for, the operational state is verified, and unresolved risks have an owner. Add the failure to the regression set without silently converting every production example into training material. Revisit the coverage and monitoring plan if the incident exposed a blind spot.

**Try it.** Write a one-page response plan for an extraction update that drops negation from one document format. Name the detection sample, the stop condition, affected descendants, repair test and rollback bundle. Explain why deleting the offending source rows alone cannot establish that a previously trained model is unaffected.
