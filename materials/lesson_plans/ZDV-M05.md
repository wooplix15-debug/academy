# ZDV-M05 Form events and workflow behavior
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Choose the correct form event
- Test validation before persistence

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZDV-M04

Save this module evidence in the same course portfolio: Event matrix and four case log.

## Explain the concept
Choose an event according to whether persistence has occurred. Validation should block invalid input before a write; downstream actions need a separate recoverable stage.

## Demonstration and sample input
Negative hours must fail before submission. A valid request persists once, then proposes a CRM handoff. If the handoff fails, the saved request remains visible as Pending Sync instead of disappearing.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Map load, input, validation and post-submit actions.
2. Verify supported events in current Creator documentation.
3. Configure hours validation.
4. Add a post-submit sync marker.
5. Test valid, invalid, edited and failed-handoff cases.

## Expected result
Invalid hours create no accepted request. A failed external handoff leaves a persisted request with retry ownership and error evidence.

## Negative test
Simulate a failed post-submit call and ensure the user sees pending status rather than a false completion message.

## Recovery test
Retry the pending handoff by its stable request key and reconcile destination state.

## Independent practice
Decide how an edit to a completed request is handled and document the event limitations.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Event matrix and four case log.
- Invalid requests are rejected
- Actions occur at the intended stage
- Edition and event limitations are documented

## Learner reflection
Why is a post-submit validation message too late?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S04, S05, S09, S10, S12, S13. Verify the current edition, account metadata and API signature before a live product demonstration. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
