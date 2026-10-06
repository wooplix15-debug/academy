# ZDV-M09 Reliable synchronization
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Prevent duplicate business operations
- Design recoverable synchronization

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZDV-M08

Save this module evidence in the same course portfolio: Sync design and replay evidence.

## Explain the concept
Idempotency constrains a business effect. A unique key and reconciliation handle replay; version or ownership rules handle conflicting updates. Neither alone proves every side effect runs exactly once.

## Demonstration and sample input
The Python simulator receives create NOVA-D001 v1, replay v1, timeout-after-commit NOVA-D002 v1, update D001 v2 and stale D001 v1. Expected: two records, D001 v2 retained, timeout reconciled and stale write rejected.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Run the supplied synchronization simulator.
2. Trace the unique-key transaction.
3. Inject a timeout after commit.
4. Query by business key before retry.
5. Replay duplicates.
6. Attempt stale and conflicting versions.
7. Document where real Zoho behavior differs from this local model.

## Expected result
Two destination rows, one for each key; amount 1500 for D001 v2; no downgrade to v1; explicit unknown-outcome reconciliation. SQL uniqueness is a local teaching guarantee, not a Zoho API guarantee.

## Negative test
Submit the same key and version with a different amount. Expected conflict rather than silent overwrite.

## Recovery test
Read destination by key after timeout, then compare version and payload to decide whether replay is necessary.

## Independent practice
Simulate two workers and propose transaction or destination uniqueness control for their race.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Sync design and replay evidence.
- Replay does not create a second business record
- Retry has a bound
- Conflict ownership is documented

## Learner reflection
Does upsert alone guarantee exactly-once downstream effects?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S04, S05, S09, S10, S12, S13. Verify the Creator or CRM edition, event, API scope or quota used by this module. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
