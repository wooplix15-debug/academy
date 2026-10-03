# ZDV-M11 Capstone build and review
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Assemble the service application
- Improve code through review

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZDV-M10

Save this module evidence in the same course portfolio: Working training app and review log.

## Explain the concept
Integration assembly should reuse prior module artifacts. Code review examines behavior and supportability, including identity, field ownership and failure evidence.

## Demonstration and sample input
Trace CRM deal D001 to Creator request SR001 to work item W001. A technician closes W001; the approved status update returns to CRM without overwriting CRM-owned amount.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Assemble forms, validation and reviewed sync contract.
2. Walk one request through its lifecycle.
3. Ask a peer to inspect key and ownership handling.
4. Fix two recorded findings.
5. Run impacted regression cases.
6. Complete pending-sync support notes.

## Expected result
Core journey and a failed-handoff path are both demonstrated. Review notes identify the specific behavior changed and its evidence.

## Negative test
Destination response omits a required ID. Do not report completed synchronization.

## Recovery test
Mark the operation pending investigation and reconcile by business key.

## Independent practice
Add a cancellation path and identify affected fields, statuses and tests.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Working training app and review log.
- Core journey works end to end
- Failure paths are demonstrated
- Another developer can inspect the code

## Learner reflection
What should a peer review comment contain?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S04, S05, S09, S10, S12, S13. Verify the current edition, account metadata and API signature before a live product demonstration. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
