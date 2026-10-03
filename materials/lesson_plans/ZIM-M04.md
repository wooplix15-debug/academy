# ZIM-M04 Workflow configuration
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Build and test conditional automations
- Identify duplicate execution risk

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZIM-M03

Save this module evidence in the same course portfolio: Two workflows and trigger test matrix.

## Explain the concept
Automation is an event plus a condition plus an action. A rule that works on creation may produce repeated tasks on later edits unless its event and duplicate behavior are deliberate.

## Demonstration and sample input
For valid West leads, assignment selects West Sales. A follow-up task uses a proposed business key lead_id plus follow_up_type. L001 edited twice must still have one intended follow-up task.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Write a trigger-condition-action table before configuring.
2. Build region assignment and follow-up in the training organization.
3. Test creation then two unrelated edits.
4. Test missing region.
5. Record when each action is eligible to fire.

## Expected result
West lead routes to West Sales; missing region routes to review; repeat edits do not create unintended duplicate tasks. If a platform feature cannot enforce the proposed key, record a customization or monitoring gap.

## Negative test
An update changes only a phone number. Demonstrate whether the follow-up rule fires again and explain the configuration.

## Recovery test
Disable an incorrect rule, remove only its identified training tasks, then replay one input and reconcile counts.

## Independent practice
Introduce a product-family condition and revise the trigger matrix without breaking missing-region handling.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Two workflows and trigger test matrix.
- Positive and negative cases pass
- Repeated events are considered
- Automation ownership is recorded

## Learner reflection
Why is a successful first run insufficient?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S06, S09, S11. Verify the current edition, account metadata and API signature before a live product demonstration. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
