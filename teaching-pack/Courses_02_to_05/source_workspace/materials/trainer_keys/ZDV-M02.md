# ZDV-M02 Trainer answer guide
## Expected demonstration
Open report contains SR001 and SR003 only. Each work item resolves to the intended request. Export the dictionary with proposed API names for later verification.
## Oral answer
Question: Why avoid a text field for a relationship?

Text does not enforce record identity and can become stale or ambiguous.
## Failure diagnosis
Select an invalid or missing request reference. Validation must reject it or require a documented correction route.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Change SR003 to Closed and verify the filtered report now contains one row.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Add a technician-specific open-work report and test another technician persona.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
