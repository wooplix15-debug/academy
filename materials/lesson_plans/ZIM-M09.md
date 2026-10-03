# ZIM-M09 UAT and release
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Run acceptance tests against requirements
- Write a release and recovery plan

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZIM-M08

Save this module evidence in the same course portfolio: Signed style UAT template and release checklist.

## Explain the concept
User acceptance testing traces business requirements to observed outcomes. A checked box without inputs, tester and evidence cannot support a release decision.

## Demonstration and sample input
R01 routes a valid West lead to West Sales. UAT01 records L001, Sales West persona, expected owner, actual owner and screenshot reference. UAT02 tests missing region and expects review queue.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Select eight end-to-end scenarios from the requirement matrix.
2. Run them with relevant personas.
3. Compare expected to actual.
4. Classify defects by business consequence.
5. Rehearse recovery in training.
6. Write release recommendation and unresolved limitations.

## Expected result
Eight cases have explicit pass or fail and evidence. Any critical permission or unintended-write failure blocks the proposed release, even if the numerical score passes.

## Negative test
Seed a broad sharing defect and confirm the access case fails and blocks release.

## Recovery test
Fix the sharing defect, rerun impacted tests and keep original failure evidence.

## Independent practice
Add a scope change after UAT and choose the regression tests affected by it.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Signed style UAT template and release checklist.
- Each requirement has evidence
- Critical defects block release
- Rollback is rehearsed in the training environment

## Learner reflection
Who accepts a business requirement?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S06, S09, S11. Verify the current edition, account metadata and API signature before a live product demonstration. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
