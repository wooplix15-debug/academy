# ZDV-M09 Trainer answer guide
## Expected demonstration
Two destination rows, one for each key; amount 1500 for D001 v2; no downgrade to v1; explicit unknown-outcome reconciliation. SQL uniqueness is a local teaching guarantee, not a Zoho API guarantee.
## Oral answer
Question: Does upsert alone guarantee exactly-once downstream effects?

No. It can prevent duplicate records under the chosen key, while workflow actions and other effects still need separate replay analysis.
## Failure diagnosis
Submit the same key and version with a different amount. Expected conflict rather than silent overwrite.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Read destination by key after timeout, then compare version and payload to decide whether replay is necessary.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Simulate two workers and propose transaction or destination uniqueness control for their race.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
