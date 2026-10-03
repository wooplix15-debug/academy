# ZIM-M02 Trainer answer guide
## Expected demonstration
A dictionary with field type, API name to verify, required rule, owner and sample value. Deal amount uses INR in this exercise and cannot be a free text string.
## Oral answer
Question: When should a new module be created?

When a distinct entity has its own lifecycle or repeated records and cannot be represented clearly by existing relationships. Document the tradeoff.
## Failure diagnosis
Create two customers called Nova Services. The design must keep their identifiers distinct rather than merging by display name.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Rename account A001 and show that linked deals still reference the same identity.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Add a recurring service renewal without duplicating the original account; explain the new entity or field decision.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
