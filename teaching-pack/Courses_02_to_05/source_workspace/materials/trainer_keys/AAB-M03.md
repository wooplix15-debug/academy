# AAB-M03 Trainer answer guide
## Expected demonstration
The workflow produces a reviewable artifact with identified changes. Publication requires the actual publishing authorization and configured destination.
## Oral answer
Question: Why should approval bind to a version or hash?

Otherwise a changed artifact can inherit approval intended for different content.
## Failure diagnosis
Try to release a draft with failed validation. The workflow blocks or returns it for correction.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Correct the draft, rerun checks and request review for the new version.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Add a technical reviewer for product-specific lessons without removing editorial review.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
