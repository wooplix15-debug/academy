# ZIM-M03 Trainer answer guide
## Expected demonstration
At least six allowed and six denied checks with tester, expected outcome and evidence. Screenshots must not contain credentials.
## Oral answer
Question: Why does hiding a field on a page not prove security?

UI visibility and underlying read or API permissions can differ. Test the relevant authorized access paths.
## Failure diagnosis
Try exporting records using the Sales East persona when export is denied by the proposed profile. A denial must be observable, not assumed.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Remove an accidental broad sharing rule and repeat every visibility test it could affect.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Design access for a temporary reviewer who needs read-only deal access for one department.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
