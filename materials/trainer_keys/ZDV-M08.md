# ZDV-M08 Trainer answer guide
## Expected demonstration
The record key and returned ID are captured without secrets. The call estimate states assumptions and retry allowance. No fixed platform limit is invented.
## Oral answer
Question: Why can a batch HTTP success still require investigation?

Individual records may fail; reconciliation must examine each result.
## Failure diagnosis
Return a record validation error within a response. Route it to correction rather than retrying unchanged input.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Simulate quota exhaustion, pause work and resume according to observed platform signals and configured retry bounds.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Compare individual writes with a documented batch operation including partial failures.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
