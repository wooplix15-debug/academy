# ZDV-M03 Trainer answer guide
## Expected demonstration
Two valid numeric transformations, two explicit amount errors, and one normalized email example. Log only synthetic identifiers and error codes.
## Oral answer
Question: Should a missing amount default to zero?

Only if an approved business rule permits it; otherwise the default hides a data-quality failure.
## Failure diagnosis
Replace a missing-value check with a truthiness check and show how it wrongly rejects zero.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Correct the check and rerun all five cases, including a zero-value boundary.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Normalize an optional date using an explicit expected format and reject an invalid date.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
