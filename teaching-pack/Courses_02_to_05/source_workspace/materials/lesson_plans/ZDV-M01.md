# ZDV-M01 Application requirements and model
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Design entities for a service workflow
- Identify data ownership

## Prerequisite and capstone contribution
Start the course capstone evidence folder and record the training environment.

Save this module evidence in the same course portfolio: Entity diagram and six user stories.

## Explain the concept
A stable business key identifies the operation across systems. A transport event ID identifies a delivery attempt. Keeping these separate prevents a replay from becoming a new business request.

## Demonstration and sample input
Customer C001 has request SR001 with business key NOVA-D001 and work items W001 and W002. CRM owns deal amount; Creator owns technician assignment and completion status.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Write six user stories for request capture, assignment and closure.
2. Draw Customer to Request to Work Item relationships.
3. Define unique request key.
4. Assign ownership for each shared field.
5. Add a duplicate-request acceptance test.

## Expected result
Three entities, explicit cardinalities and a field-owner table. Two deliveries with different event IDs but the same request key represent one business request.

## Negative test
Send EVT001 and EVT002 for NOVA-D001. Do not create two requests merely because event IDs differ.

## Recovery test
Repair an incorrect lookup using recorded source and target IDs without deleting unrelated work items.

## Independent practice
Model a request that contains multiple visits and explain where visit history belongs.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Entity diagram and six user stories.
- Relationships match requirements
- Uniqueness rule is defined
- Ownership of shared fields is explicit

## Learner reflection
Why is an event ID not always an idempotency key?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S04, S05, S09, S10, S12, S13. Verify the Creator or CRM edition, event, API scope or quota used by this module. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
