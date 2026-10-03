# AAB-M07 Trainer answer guide
## Expected demonstration
Twenty designed cases are present. Only cases actually executed are scored; blank actuals are not passes. Release requires zero observed critical permission failures under the proposed policy.
## Oral answer
Question: How should unexecuted cases affect the report?

Show them as not run, with a separate denominator. Do not count them as passing.
## Failure diagnosis
Nineteen good outputs and one restricted-source leak. The critical gate fails despite 95 percent simple success.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Repair source eligibility and rerun the failed case plus similar boundary cases.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Add five cases from anonymized learner feedback after permission and review.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
