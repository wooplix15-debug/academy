# ZDV-M06 Trainer answer guide
## Expected demonstration
The mapped request preserves its external key and numeric amount. Empty data yields no fabricated record. Pagination stops on the documented condition or a configured safety limit.
## Oral answer
Question: What are two layers of API success?

The transport status and the operation result in the response body must both be checked.
## Failure diagnosis
Receive HTTP success with a record-level error. Do not treat transport success as business success.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Record the failing page and resume only from a supported cursor or page strategy after diagnosis.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Add an optional currency field and a contract version compatibility note.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
