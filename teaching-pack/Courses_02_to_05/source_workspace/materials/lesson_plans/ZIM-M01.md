# ZIM-M01 Discovery and scope
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Write testable requirements
- Separate scope assumptions and exclusions

## Prerequisite and capstone contribution
Start the course capstone evidence folder and record the training environment.

Save this module evidence in the same course portfolio: Discovery brief and scope statement.

## Explain the concept
A requirement describes observable business behavior. A preference such as faster follow up needs a clock, a responsible person and an exception path before it can be tested.

## Demonstration and sample input
Manager says new West-region leads should go to West Sales. Rewrite as R01: when a new valid West lead arrives, assign West Sales and record assignment time; missing region goes to the review queue. The proposed first-response target is four business hours, not a claim about Nova performance.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Role-play manager, sales representative and administrator.
2. Capture eight requirements with IDs and owners.
3. Separate a requirement from the feature chosen to implement it.
4. Add one normal and one exception acceptance case to each requirement.

## Expected result
Eight requirements, sixteen acceptance cases and a scope section. R01 must include the missing-region path. Keep unresolved working-hours and holiday definitions visible.

## Negative test
The manager asks for guaranteed revenue improvement. Do not convert this into an acceptance test without evidence and an agreed measurement design.

## Recovery test
The sponsor changes region ownership. Revise R01, identify affected routing and access tests, and keep its previous version.

## Independent practice
Interview a support-team persona and create four additional requirements without using the sales examples.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Discovery brief and scope statement.
- Every requirement has an owner
- Acceptance criteria can be tested
- Unanswered questions remain visible

## Learner reflection
Why is assign leads quickly not testable?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S06, S09, S11. Verify the CRM feature, edition, profile or sandbox behavior used by this module. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
