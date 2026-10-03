# ZDV-M05 Trainer answer guide
## Expected demonstration
Invalid hours create no accepted request. A failed external handoff leaves a persisted request with retry ownership and error evidence.
## Oral answer
Question: Why is a post-submit validation message too late?

The record may already exist. Validate the rule at the supported pre-persistence stage.
## Failure diagnosis
Simulate a failed post-submit call and ensure the user sees pending status rather than a false completion message.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Retry the pending handoff by its stable request key and reconcile destination state.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Decide how an edit to a completed request is handled and document the event limitations.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
