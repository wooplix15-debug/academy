# ZDV-M01 Trainer answer guide
## Expected demonstration
Three entities, explicit cardinalities and a field-owner table. Two deliveries with different event IDs but the same request key represent one business request.
## Oral answer
Question: Why is an event ID not always an idempotency key?

Distinct events can refer to the same business operation. Choose a key that matches the operation being made unique.
## Failure diagnosis
Send EVT001 and EVT002 for NOVA-D001. Do not create two requests merely because event IDs differ.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Repair an incorrect lookup using recorded source and target IDs without deleting unrelated work items.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Model a request that contains multiple visits and explain where visit history belongs.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
