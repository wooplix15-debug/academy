# AAB-M04 Trainer answer guide
## Expected demonstration
Every chunk links back to a source. Restricted records are excluded before ranking and context assembly, not merely hidden in the final answer.
## Oral answer
Question: Why filter permissions before context assembly?

Once restricted text enters the model context, an output filter cannot reliably undo its exposure.
## Failure diagnosis
A highly relevant client-only document appears. Public retrieval must exclude it.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Withdraw a previously approved source and verify it no longer enters context.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Design source expiration and reviewer reminders for an API reference.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
