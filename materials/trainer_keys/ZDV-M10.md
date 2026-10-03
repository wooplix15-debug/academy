# ZDV-M10 Trainer answer guide
## Expected demonstration
Each case has input, expected, actual, environment and evidence. Mock passes never appear as live Creator or CRM certification evidence.
## Oral answer
Question: Why can restoring old code fail to restore the system?

New data or schema changes may be incompatible with the old version.
## Failure diagnosis
A release changes a field type while old records remain. Identify migration and backward-compatibility risk.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Restore the previous training version and reconcile records affected by the change.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Choose three regression cases for a change to duplicate-key handling and justify the selection.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
