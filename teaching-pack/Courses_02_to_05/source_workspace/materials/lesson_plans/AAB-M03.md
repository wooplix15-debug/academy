# AAB-M03 Business workflows
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Separate proposal from execution
- Map exception and review paths

## Prerequisite and capstone contribution
Use the previous module evidence as input: AAB-M02

Save this module evidence in the same course portfolio: Workflow diagram and decision rules.

## Explain the concept
A workflow can separate retrieval, generation, validation, review and publication. Make rejection and retry states explicit so draft completion cannot silently become approval.

## Demonstration and sample input
States are Requested, Drafted, Checked, Review Required, Approved and Released. A changed file hash after approval invalidates that approval and returns the item to review.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Draw states and owners.
2. Define input and output for each stage.
3. Add invalid-output and reviewer-rejection branches.
4. Separate local approval from external publication.
5. Simulate a changed draft after review.

## Expected result
The workflow produces a reviewable artifact with identified changes. Publication requires the actual publishing authorization and configured destination.

## Negative test
Try to release a draft with failed validation. The workflow blocks or returns it for correction.

## Recovery test
Correct the draft, rerun checks and request review for the new version.

## Independent practice
Add a technical reviewer for product-specific lessons without removing editorial review.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Workflow diagram and decision rules.
- Each stage has an owner
- Failures have a recovery path
- Publication is a separate action

## Learner reflection
Why should approval bind to a version or hash?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S07, S08. Check model, retrieval and tool behavior in the approved environment. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
