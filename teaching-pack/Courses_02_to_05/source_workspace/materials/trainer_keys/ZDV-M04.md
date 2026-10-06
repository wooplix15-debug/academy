# ZDV-M04 Trainer answer guide
## Expected demonstration
Validation returns ok false with named reasons for bad inputs, and preserves zero when allowed. Debug notes show cause and evidence, not only final code.
## Oral answer
Question: Why rerun a previously passing case after a repair?

The repair may change behavior outside the original defect; regression cases detect that impact.
## Failure diagnosis
Supply an empty customer ID with otherwise valid fields. Validation must fail.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Inject a controlled exception, return a typed failure and preserve a correlation ID for support.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Extract a normalization function and define whether it mutates the original map.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
