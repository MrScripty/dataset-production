# Tabular and time series

A spreadsheet predicts tomorrow perfectly because one column contains tomorrow's answer. What information was really available when the prediction had to be made?

## Define time before calculating a score

Use this authored inspection table. At 09:00 each day, decide whether a machine's temperature at 10:00 will exceed 30 °C. Inputs are the machine ID and temperature observed at 09:00. The 10:00 temperature is the label source, unavailable at prediction time. These numbers are an illustration, not sensor observations.

| Machine | Day | 09:00 temperature °C | 10:00 temperature °C | Target exceeds 30 |
| --- | --- | --- | --- | --- |
| A | 1 | 24 | 28 | no |
| A | 2 | 29 | 32 | yes |
| B | 1 | 25 | 27 | no |
| B | 2 | missing | 31 | yes |

The prediction horizon is one hour. Distinguish event time, when a value describes the world, from availability time, when the consumer could read it. A maintenance report about 08:00 written at noon is still unavailable for a 09:00 decision. A corrected historical table can silently give an evaluator information that the live system did not have.

## Work one feature-timing failure

A proposed feature “daily maximum” is computed from both observations. Its values are 28, 32, 27 and 31. The threshold daily maximum >30 agrees with all four labels, because the feature includes the target measurement. The 4/4 agreement is authored arithmetic and leakage, not useful generalization evidence.

A permitted baseline is 09:00 temperature >27, abstaining on missing input. It predicts no, yes, no, abstain. Coverage is 3/4; conditional agreement on the three evaluated nonabstained rows is 3/3. Across all four rows, it has three correct decisions and one undecided case. Those denominators answer different questions. Missing is not zero: zero °C would describe a real cold measurement. An imputation policy must retain a missingness indicator and be fitted on training data only. Never use the later 10:00 value to repair the earlier input.

## Match the split to the question

For future days on known machines, allocate time with training before evaluation and prevent windows from overlapping across the boundary. Purging overlapping windows means removing examples whose feature or target intervals intersect protected evaluation intervals. A gap or embargo can help when dependence extends beyond the explicit window; its duration must follow the process, not a magic constant.

For unseen machines, keep A and B in different families. For both unseen machines and future periods, design both constraints together. This four-row table cannot provide a credible train/calibration/final-test experiment with broad coverage. State that limitation rather than fragmenting machines to fill every split. Repeated entities, shared maintenance events and common production batches can connect records even when their IDs differ.

Features have semantics as well as types: fixed column order, Celsius versus Kelvin, hourly versus cumulative counts, categorical vocabularies, absent versus unknown, clock/time-zone conventions and interval closure. A loader accepting four numbers does not establish that they match the companion's internally generated four-sensor project. That consumer must receive its exact feature meanings and units through a tested adapter.

## Carry this project through core 9–15

- Core 9: acquire independent missing-input cases and new machines under the intended claim; more adjacent rows do not establish entity diversity.
- Core 10: a unit conversion transforms every relevant value and threshold together. Random row shuffling is not a valid temporal augmentation.
- Core 11: a maintenance rule proposes labels, but post-outcome repairs and human overrides must retain their provenance.
- Core 12: generated rows need feasible joint constraints; independent column sampling can make impossible machines.
- Core 13: compare under the same prediction/availability cutoff; report machine and missingness slices, exposure and temporal shift.
- Core 14: freeze exact feature order, training-only preprocessing statistics and target horizon; test a row with swapped columns and a late report.
- Core 15: alert on changed units, unavailable features and missingness. Restore preprocessing and schema with data; compare total cost per accepted independent decision example.

## Exercises and worked answers

1. Why is daily maximum forbidden? It includes observations after the decision cutoff, including the label source.
2. If B's missing value becomes 0 and the baseline emits no, is its coverage now 4/4? It emits four decisions, but the change is an undocumented representation error. Apparent coverage does not justify the false interpretation; audit this as a policy failure.
3. What does 3/3 agreement establish? Only agreement of this authored baseline on these three evaluable rows. It excludes the abstention and supplies no uncertainty estimate over future machines.
4. Can a noon correction of a 09:00 value enter a retrospective input? Only if the claim is explicitly about a corrected archive. It cannot support a live 09:00 prediction claim.
5. Give one consumer edge fixture. Declare [temperature_C, elapsed_seconds], feed [60,20] instead of [20,60], and require rejection or a visible semantic check. Types alone cannot detect the swap.

Acceptance: all features must have an availability time, missingness policy and unit; protect the entity/time relationships implied by the claim. Inadequate independent examples require a narrower claim or more collection.

## Optional tools and primary reading

Paper and a spreadsheet suffice. Later, a dataframe library and temporal SQL query can implement “as of” joins, but check the join against a manually traced example. [WILDS](https://proceedings.mlr.press/v139/koh21a.html) provides concrete domain and temporal-shift evaluation examples; its protocols do not validate this toy table. The data contract comes before a predictive model.
