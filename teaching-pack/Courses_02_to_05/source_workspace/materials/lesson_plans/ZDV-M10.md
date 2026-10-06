# ZDV-M10 Testing and release
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Create meaningful positive and failure tests
- Plan versioned deployment

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZDV-M09

Save this module evidence in the same course portfolio: Test log and deployment notes.

## Explain the concept
A useful test suite includes the business success path, invalid input, authorization, replay, partial failure and recovery. Deployment rollback must consider changed data as well as code.

## Demonstration and sample input
A ten-case release suite covers required field, lookup, permission, connection failure, duplicate key, lost response, malformed body, quota, conflict and reconciliation.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Create fixtures and expected outcomes for all ten cases.
2. Execute local mocks and label them as such.
3. Run available sandbox equivalents separately.
4. Record defects and impact.
5. Write code rollback and data recovery steps.
6. Rehearse one repair.

## Expected result
Each case has input, expected, actual, environment and evidence. Mock passes never appear as live Creator or CRM certification evidence.

## Negative test
A release changes a field type while old records remain. Identify migration and backward-compatibility risk.

## Recovery test
Restore the previous training version and reconcile records affected by the change.

## Independent practice
Choose three regression cases for a change to duplicate-key handling and justify the selection.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Test log and deployment notes.
- Ten scenarios have expected outcomes
- Known defects are recorded
- Rollback includes data impact

## Learner reflection
Why can restoring old code fail to restore the system?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S04, S05, S09, S10, S12, S13. Verify the Creator or CRM edition, event, API scope or quota used by this module. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
