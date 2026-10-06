# ZIM-M05 Blueprint and approval design
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Represent controlled stages and transitions
- Explain approval and exception handling

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZIM-M04

Save this module evidence in the same course portfolio: Blueprint diagram and transition evidence.

## Explain the concept
A workflow reacts to events. A controlled transition represents a permitted move between business states with required inputs. Approval is a separate business decision that needs an owner and rejection route.

## Demonstration and sample input
Synthetic quote policy: amount greater than INR 50000 requires manager review. INR 50000 takes the normal route; INR 50001 needs approval. Proposed states are Draft, Review, Approved, Sent and Rejected.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Draw permitted transitions before opening Blueprint.
2. Add required quote amount and review evidence.
3. Configure the available training features or simulate unavailable approval behavior.
4. Test boundary values 49999, 50000 and 50001.
5. Test rejection and resubmission.

## Expected result
A quote requiring approval cannot be sent through the normal route. Rejected quotes return for correction with their history intact. Record the edition and exact feature used.

## Negative test
Attempt Draft to Sent for INR 50001 with no approval. Expected outcome is a blocked transition under the proposed policy.

## Recovery test
Reject then revise the amount and resubmit. Record whether prior approval is invalidated by the policy.

## Independent practice
Add a discount-above-15-percent review rule and write all boundary tests before configuration.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Blueprint diagram and transition evidence.
- Invalid progression is blocked
- Rejection path is usable
- Feature availability is checked in the training edition

## Learner reflection
Does a Blueprint automatically implement every approval requirement?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S06, S09, S11. Verify the CRM feature, edition, profile or sandbox behavior used by this module. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
