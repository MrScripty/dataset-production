# 15 Operate recover and account for cost

*Dataset Production · Puma*

## The question: can we use it safely tomorrow?

A build finished, the consumer read its files, and the release passed today's checks. Tomorrow a parser update drops a word, a source permission changes, or the working disk loses files. Which signal will detect a consequential change? Which earlier bundle can still be used? What does it cost to recover and keep the release useful?

The principle is **operate with explicit references, reversible choices and whole-pipeline accounting**. Monitoring needs stable checks and action criteria. Restart, rollback and independent backup restore solve different failures. A cheap candidate is not a cheap accepted, maintained release.

You enter with frozen inputs, contract/adapter/consumer evidence and known limitations. You leave with a tested toy recovery rehearsal, a matched-quality cost ledger and the core capstone. The recovery lab contains no trained model; model fitting and model acceptance remain separate companion work.

## Work the parser incident into a decision

**Authored incident, with an executed bounded CPU analogue below.** The request “Please do not refund this payment” has `not` inside an HTML span. Parser P1 preserves all paragraph text. Faulty P2 reads direct paragraph text only, emitting “Please do refund this payment.” The refund-intent target becomes true under a consumer that correctly follows the emitted text.

A source/format monitor can count extraction failures; a semantic regression checks that this saved source still retains `not` and produces false. Neither should merely alert “quality changed.” A useful alert names the check, affected version/family and first observed incorrect artifact. Frequency drift may trigger investigation without proving an error; stable averages can conceal a critical rare regression.

Set the response before seeing results: hold new outputs, mark affected releases, preserve faulty evidence where rights allow, verify the previous compatible bundle and contain harm through supported authorized controls. Reprocess affected descendants after repair and rerun both semantic and consumer gates. Review a sample beyond the known span case, because the same defect can drop words other than `not`.

A proposed repaired release is not automatically approved. If four saved regressions pass but two of twenty reviewed affected records remain unresolved, adjudicate them or exclude them under the policy and disclose coverage loss. A corrected dataset does not repair a previously fitted model. A production rollback must restore a compatible dataset/preprocessor/adapter/model/configuration bundle and then test actual selected behavior. The toy exercise has a parser and read-only consumer only.

## Three recovery verbs, three kinds of evidence

**Restart** resumes work from existing state. It needs intact inputs/checkpoints and an idempotent or reconciled job protocol. It does not undo a faulty recipe or recover deleted source bytes. Repeating a failed generation call can create duplicates or charges if the previous outcome is unknown; reconcile stable work/attempt IDs before retrying.

**Rollback** selects an earlier approved compatible bundle that still exists. Check hashes, versions, contract and behavior before switching, then verify the active selection. Reverting one dataset filename while keeping incompatible preprocessing or a model fitted from faulty inputs may not contain the incident. Rollback is unavailable if its earlier artifacts have been lost.

**Backup restore** reconstructs missing state from a separately retained copy. The copy must survive the failure being rehearsed. A checkpoint or another pointer in the same deleted working tree is not that backup. Verify restored hashes, versions and consumer behavior, then confirm the application selects the restored bundle. Backup without a tested restoration procedure is an assumption about recovery.

A production plan records recovery point, meaning how much recent work may be lost, and recovery time, meaning how long acceptable service can be unavailable. It also needs ownership, authorized access, external storage/dependencies, credential availability and rights/retention policy. The hardware-free exercise demonstrates the distinctions, not production durability.

## Execute an independent toy restore

The delivered `examples/recovery/recovery.py` creates two authored bundles. R1 uses `all-text-v1`; R2 uses faulty `direct-text-v2`; both declare `toy-refund-consumer-1`. The consumer recognizes exactly the two supplied fictional request strings, not unrestricted natural language. Each bundle stores HTML source bytes, the record, a release/parser/consumer/unit/target contract and hash manifest.

Run from the repository root with an absent or empty output directory:

```
python3 examples/recovery/recovery.py --out /tmp/dp-recovery-run
python3 -m unittest discover -s examples/recovery/tests -p 'test_*.py' -v
```

**Safety boundary.** The demo refuses a nonempty root and deliberately deletes only its own newly created `toy-working-files` directory. Do not point an exercise at valuable material. It needs only Python's standard library, no hardware, package download or service.

The rehearsal performs distinct checks:

1. Restart the interrupted R2 toy checkpoint; repeat restart idempotently if desired. The job finishes, but nested-negation regression still fails.
2. Verify existing R1's exact file hashes and compatible parser/consumer semantics; switch the active pointer; reread it to prove selection took effect.
3. Copy verified R1 into `independent-toy-backup`, outside the working tree. Record all R1 file hashes.
4. Remove the complete toy working tree, including both releases, job state and active pointer. Confirm it is absent.
5. Restore R1 from the independent copy, recreate the active selection, recheck hashes/versions/behavior and compare restored file hashes with the originals.

The generated `receipt.json` contains actual run evidence, including `working_tree_removed_before_restore=true` and `restored_hashes_match=true` when successful. It shows false for refund requested and `all-text-v1` for the restored parser. Tests reject hash corruption, incompatible rehashed contracts, missing/corrupt backup, backups inside the working tree and a nonempty demo root. Restart success is deliberately insufficient for semantic repair.

The sibling backup is independent of the deleted working tree, but shares a filesystem and physical machine. It does not survive whole-disk loss or establish remote durability, ransomware protection, authentication or production recovery time. Those require a separately authorized realistic implementation and rehearsal. No model has been rolled back, restored or evaluated here.

## Count the whole cost pipeline

The relevant unit may be an accepted independent request family, reviewed speech hour, verified trajectory or required quality improvement. Record total work, including rejected candidates and repeat runs, rather than divide only a generator's bill by accepted rows.

A complete ledger includes:

- Acquisition, rights/permission review and source preparation.
- Extraction, normalization and transformation/generation attempts, including rejected and uncertain attempts.
- Annotation, expert review, adjudication and retained references.
- Structural/semantic/executable verification, consumer tests and evaluation.
- All fitting: reference/proxy/teacher/student or other parameter estimation, regardless of whether an optimizer took gradient steps.
- Storage, copies/backups, indexes, serving/input processing and access costs.
- Repair, repeat builds/fitting, withdrawal, source/ontology changes and ongoing monitoring.

**Authored funnel, invented USD costs.** Generate 10,000 candidates at $0.02 each: $200. A structural screen passes 8,000. Verify those at $0.05: $400; half pass. Review the remaining 4,000 at $0.50: $2,000; 90% pass, yielding 3,600 accepted rows. Counted total is $2,600, or about $0.72 per accepted row. The two-cent generation price does not describe accepted production cost. This subtotal still excludes setup, structural-screen cost, acquisition, fitting, storage, serving and repair. Add them before comparing pipelines. If those rows belong to few families, cost per independent family is higher.

Acceptance rates are conditional on reaching a stage. Do not multiply unrelated unconditional rates as if filters were independent. For two order-independent filters A/B, expected cost A-first is `c_A + p_A*c_B`; B-first is `c_B + p_B*c_A`. Compare cost per expected rejection `c/(1-p)` only under the stated assumptions. Representation dependencies, correlated slice behavior, permission/privacy and legal ordering constraints can override a cheap-first schedule.

## Allocate review to the decision

Keep three budgets visible: learning a new source's failure profile, repairing likely consequential defects, and estimating release quality. A high-yield targeted repair queue does not replace a separately selected population audit. Critical slices may need a minimum checked sample even when their population weight is small.

For an optional stratified-audit calculation, let each stratum's weight be its share of the target population, its standard deviation describe variation in the measured outcome, and its review cost be cost per independently checked unit. Under independent sampling and a fixed total cost, a variance-minimizing allocation is proportional to `population weight × standard deviation / square root of review cost`. This is a planning result under assumptions, not an obligation to trust uncertain pilot estimates. For two equally weighted/equally variable strata costing one and four units to review, the cheaper stratum receives twice as many reviewed units. Use whole-number allocations, feasibility and coverage floors explicitly. Related examples need family-level sampling and uncertainty, not row-level imitation of the formula.

Repair prioritization asks a different question: probability of error, chance review can resolve it, consequence of leaving it wrong, and effort required. These are estimates, not intrinsic data values. A confident but common wrong target may deserve attention more than a permanently ambiguous request. Adding five votes without new evidence may not resolve ambiguity. Escalating only difficult items also makes repeated-annotation agreement describe that selected queue; retain an ordinary overlap sample if estimating general annotator reliability.

## Compare costs at matched quality

**Authored complete comparison; no vendor quotations or executed spending.** Two hypothetical pipelines each deliver 100 accepted independent request families meeting the same gates: correct source/contract, no family leakage, 90/100 agreement on the same supplied reference sheet and 4/4 critical negation cases. They use the same declared consumer, evaluation population and service period.

| Cost component, USD | Pipeline A | Pipeline B |
|---|---:|---:|
| Acquisition and rights preparation | 200 | 100 |
| Generation/transformation, all attempts | 100 | 50 |
| Annotation/adjudication | 300 | 200 |
| Verification/export/evaluation checks | 200 | 100 |
| Fitting, including repeats/proxies | 400 | 800 |
| Storage and backup for the stated period | 50 | 50 |
| Serving/input processing for that period | 100 | 100 |
| Repair and repeated work allowance | 150 | 200 |
| Total | 1500 | 1600 |

Cost per accepted independent family is $15 versus $16. B is cheaper at candidate generation but more expensive overall. This decision is meaningful only at the matched quality, coverage, independent-unit and service assumptions. If B supplies more quality or a different rare-slice capability, first compare at an agreed operating point rather than treat totals as interchangeable. The invented four-case gate cannot establish zero future risk.

Separate fixed setup, marginal attempt cost and ongoing maintenance. Use measured quantities where available; label uncertain forecasts. Fast generation can simply grow an expert-review queue. Measure age, rework and accepted-output latency, not only requests per second. A clearer guide or more reliable source may reduce cost more than a faster teacher.

For large releases, separate authoritative manifest from convenient shards/caches. Shard size affects startup, parallelism, retries and wasted reads. Sampling only between domain-ordered shards can alter exposure. Cache dependencies include source, model/tokenizer, normalization, rubric and rights status; identical bytes do not guarantee unchanged permitted use. Lineage supports correct partial rebuilds, not unconditional cache reuse.

## Controlled exercise and acceptance check

**Evidence labels: executed authored fixture for the recovery demo; authored illustration for cost tables; proposed production controls.** Unit: one toy nested-negation request for recovery; 100 assumed independent accepted families for the cost comparison. Source hashes/version evidence are in run manifests/receipt, not implied by a screenshot.

1. Explain why a completed restart leaves P2's semantic error intact.
2. Run the demo, inspect the receipt and prove the working tree was removed before restoration. Identify which independent files supplied recovery.
3. In the tests, observe that changing a contract and rehashing it still fails compatibility. Explain why a hash match is insufficient.
4. Calculate funnel subtotal and complete matched-quality totals. Include rejected candidates and repeated fitting, and mark forecasts.
5. Defend the production recovery plan: owner, stable checks, action criteria, compatible bundle, independent backup, permitted retention and realistic recovery objectives.

Pass the toy rehearsal only if restart/rollback/restore are distinguished, missing state is reconstructed from the backup and restored consumer behavior agrees with the declared contract. Pass an economics conclusion only when matched quality/coverage and all relevant cost stages are stated. Do not call restart a verified backup restore or a cheap generated token a useful independent example.

Worked answers: restart uses R2's remaining files and only changes job completion state. Rollback verifies/selects the existing R1. After complete toy loss, the sibling `independent-toy-backup/R1` supplies source/record/contract/manifest bytes. Matching hashes plus `refund_requested=false`, correct parser/consumer versions and active reread establish this bounded restore. The funnel subtotal is $2,600/3,600 ≈ $0.72; complete hypothetical totals are $1,500 and $1,600, or $15/$16 per accepted family. A $50 difference in generation cost alone cannot settle the decision.

## Core capstone: deliver a release another reader can defend

Choose one modality and keep a small, inspectable project. Deliver:

1. A bounded claim, input/target/decision unit, population, permitted/excluded use and important failure cost.
2. A semantic contract: schema, units, axes/time/order, missing-value/target conventions and exact supported consumer.
3. Source/rights evidence and traceable lineage through transformations, annotations and accepted/rejected decisions.
4. Protected-family graph, split rationale and evaluation-exposure ledger.
5. An audit with all eligible, labeled, missing, conflicting and evaluable denominators, sample design and uncertainty limits.
6. One controlled improvement, expected mechanism, comparison/budget, failures and defensible acceptance decision.
7. A frozen release with retained raw/reference inputs, hashes, versions, actual emitted-byte consumer test and known limitations.
8. Stable monitoring references/action criteria, demonstrated recovery and a whole-pipeline matched-quality cost ledger.

A hardware-free text capstone can use the supplied helpdesk builder, educational adapter and separate refund-parser recovery fixture. Explicitly name the two different tasks/consumers; do not imply refund-intent behavior is tested by department-routing labels. A nontext capstone must deliver its own actual tested consumer, not borrow the text consumer's pass.

### Capstone rubric and worked reviewer guidance

**Pass** requires traceable sources with supported rights, no protected-family overlap, correct audit denominators, tested consumer semantics and demonstrated bounded recovery. **Revise** when evidence is missing or a narrower claim is needed. **Block acceptance** for leakage, unsupported rights/compatibility or misleading evaluation. Unsupported future physical or model performance is not repaired by confident prose.

For the supplied fixture, a worked submission can claim an authored reproducible weak-routing release with documented errors and a supported educational text reader. It cannot claim real-customer generalization, numeric-companion training compatibility or independent human ground truth. The parser rehearsal separately demonstrates toy recovery of one authored refund request after working-file loss. A reviewer checks exact reference-input retention, exclusions, group identity, decoded feature/target mapping and restoration receipt rather than accept a “ready” badge.

A check-by-check worked review for the supplied teaching path is:

1. Claim: department routing under the authored guide, with one canonical request as the decision unit. The source collection is fictional English messages; it does not represent a sampled customer population. Refund authorization is excluded.
2. Contract: the educational text consumer reads one UTF-8 text feature and integer weak department target, with the exact access/billing/technical map from Chapter 14. Units and target conventions are explicit; no numeric training-companion input is claimed.
3. Origin and rights: trace the invoice example through r01/r02, raw bytes and lineage. Authored sources are identified, but the repository supplies no declared distribution license. Local inspection/reproduction under applicable permission is a narrower activity; an external/distributable capstone remains blocked until its permission basis is supplied. Fictionality is not a redistribution grant.
4. Independence: reconstruct the 21 protected groups from source/family/canonical relations. Verify each group stays in one split. Record that inspecting all fixture outcomes makes them teaching/development evidence; they cannot later become an untouched real-population holdout.
5. Audit: 24 canonical examples, 14 labeled, five abstentions and five conflicts. Thirteen aggregate predictions have resolved references and ten agree. Preserve unresolved/missing-reference exclusions and the supplied references' authored status; do not call them independent human ground truth.
6. Controlled improvement: a suitable data-production change is retaining the exact gold input for repeatable reference audits or adding the declared consumer export. Show baseline/candidate artifact differences and test the expected reproducibility/compatibility mechanism. Acceptance can support that bounded data property; a learned-performance gain remains unrun without a matched fitting experiment. If the comparison itself was not run, record revise rather than borrow another lab's pass.
7. Freeze and consumer: keep recipe version 3's raw/reference inputs, implementation/environment identity and manifests. Decode the invoice feature/target and record actual consumer tests, including rejection of rehashed incompatible contracts. An observed loader pass supports this educational consumer only.
8. Recovery and cost: the separate refund-task toy receipt demonstrates restart's remaining failure, existing R1 rollback and backup restoration after deliberate working-tree loss. Its task/consumer boundary and same-filesystem durability limit stay explicit. Use the complete cost ledger with actual quantities where measured and forecasts where not; the invented USD table is arithmetic practice, not spending evidence.

This review can pass the executed local teaching checks while marking an external distribution or real-model claim blocked or unfinished. Missing authority or evidence must not be papered over by the complete-looking artifact list.

Have an independent reader reconstruct the artifacts and explain limits in ordinary language. Then have a technical reviewer check computations/versioned files and an evidence reviewer challenge each executed/published/proposed label. Successful data handoff identifies exactly which consumer is supported. Any later model fitting, rollout or deployment needs its own evidence and approval under the companion's contract.

## Optional tools and primary reading

Versioned storage, job ledgers and monitoring services can implement these controls once scale warrants them. Choose by failure domain and workload, not tool popularity. Read the official [Hugging Face Datasets cache/fingerprint documentation](https://huggingface.co/docs/datasets/about_cache) [legacy R59], [DVC lock files](https://dvc.org/doc/user-guide/project-structure/dvcyaml-files) [R76] and [lakeFS retention documentation](https://docs.lakefs.io/data-retention/) [R06]. None independently proves backup durability, rights or semantic correctness.

Sambasivan et al., [Data Cascades in High-Stakes AI](https://storage.googleapis.com/gweb-research2023-media/pubtools/5936.pdf) [R58], connects upstream data problems to technical/organizational handoffs in a qualitative practitioner study. Its sample findings are not population prevalence. The transferable lesson is to budget documentation, responsibility, domain communication and repair alongside software and fitting. Production readiness is an evidence chain that can be used, monitored and recovered.
