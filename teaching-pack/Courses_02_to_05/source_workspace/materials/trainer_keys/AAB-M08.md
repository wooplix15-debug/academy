# AAB-M08 Trainer answer guide
## Expected demonstration
Cost worksheet reproduces USD 0.018 for the example. Retry limits and request timeouts are recorded; no claim that the estimate is the actual billed cost.
## Oral answer
Question: Why is cheapest per-request output not necessarily cheapest per accepted lesson?

Retries, correction time and rejection rate can increase the total cost.
## Failure diagnosis
Usage is missing in a failed response. Mark cost unknown or estimated rather than zero.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Stop when the run budget is reached and preserve enough state for diagnosis.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Compare two prompt versions using quality and reviewer time alongside cost.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
