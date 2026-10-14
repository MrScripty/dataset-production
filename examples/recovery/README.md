# Rehearse three different recovery operations

Run from the repository root with Python's standard library. No model, GPU, data download or external service is involved:

```
python3 examples/recovery/recovery.py --out /tmp/dp-recovery-demo
python3 -m unittest discover -s examples/recovery/tests -p 'test_*.py' -v
```

Use an absent or empty demo directory. The script refuses a nonempty root and deliberately removes only its own newly created `toy-working-files` tree. Never use valuable files as this exercise's output directory. `receipt.json` is the executed evidence from your run, not a prewritten performance claim.

The authored HTML has a nested `not`: `<p>Please do <span>not</span> refund this payment.</p>`. The P1 parser (`all-text-v1`) preserves it. The faulty P2 (`direct-text-v2`) drops nested text. The bounded consumer supports exactly two fictional request strings, with a boolean `refund_requested` target. It is not a general natural-language intent classifier and makes no training-companion compatibility claim. Each bundle includes source bytes, parser/consumer/release contract, record and hash manifest.

The demo starts with a deliberately simulated R2 incident. Restart resumes an interrupted checkpoint to completion, idempotently, using the existing R2 files. It leaves the nested-negation error intact. Rollback verifies the existing earlier R1 bundle, including its exact versions, file hashes and actual consumer behavior, then changes the active pointer. Backup copies verified R1 bytes outside the working tree into a sibling directory. The demo records hashes, removes the entire toy working tree including both releases and the active pointer, then reconstructs a working tree from the independent backup. Restoration rechecks source/record/contract hashes, release and parser/consumer compatibility, consumer behavior, and identical restored file bytes. A corrupt backup blocks restoration.

Independence here means the backup is outside the deleted working tree. Both directories remain on one filesystem: this teaches separation of failure domains but does not protect against disk loss, theft, ransomware, permission changes or cloud-service failure. Production needs authorized separate storage, tested credentials, retention/rights policy, compatible dependencies, recovery-time and recovery-point objectives, and a rehearsal under realistic failure. The toy parser handles its supplied grammar only. The hash manifest is unsigned and is not an authenticity mechanism. There is no production application or trained model in this lab.

Tests distinguish byte integrity from semantic compatibility, verify restart idempotence and remaining failure, verify safe refusal of nonempty output, exercise independent restoration after complete toy loss and reject missing/corrupt backups. The minimal checkpoint models a finished-output state, not a transactional distributed job system. No inference or fitting claim follows from passing it.
