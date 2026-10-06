# ZDV-M07 Trainer answer guide
## Expected demonstration
An allowed read and denied write are evidenced separately. Credential values do not appear in screenshots, source code or learner submissions.
## Oral answer
Question: Why not solve every denial with full access?

The correct operation may be disallowed by design. Match permission to the reviewed contract.
## Failure diagnosis
Use the wrong organization or insufficient scope. Distinguish configuration failure from a data validation error.

Do not accept a happy-path screenshot as evidence for this case. Require its exact input, observed result and explanation.
## Recovery explanation
Reauthorize only after the owner confirms the required scope, then rerun the exact failed operation.
## Common misconception
Ask the learner to distinguish the business rule from the feature used to implement it, and a simulated result from a connected-product result.
## Independent task review
Design separate test and production connection names and prevent accidental cross-environment selection.

Check that the learner adapts the rule, preserves prior evidence and identifies affected tests. Several designs can pass; accept alternatives only with testable assumptions and evidence.
## Scoring
Apply the shared practical rubric. A critical access or unauthorized-write failure requires repair and reassessment, even when total points are at least 70.
