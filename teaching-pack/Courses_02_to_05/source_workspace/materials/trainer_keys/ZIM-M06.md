# ZIM-M06 Trainer answer guide
## Expected demonstration
50 = 42 accepted + 5 rejected + 3 excluded. Offline accepted is not proof of 42 successful Zoho imports; record target success and failures separately after the actual trial.
## Oral answer
Question: Why preserve a migration batch ID?

It links evidence to a specific run and limits rollback scope; record counts alone cannot identify affected records.
## Failure diagnosis
Change one accepted row to an existing destination email. Predict the chosen import duplicate behavior and reconcile its actual result.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Rollback only records created by the trial batch. Restore separately any existing record the import changed.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Change policy to permit a blank company, rerun classification and explain the count difference.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
