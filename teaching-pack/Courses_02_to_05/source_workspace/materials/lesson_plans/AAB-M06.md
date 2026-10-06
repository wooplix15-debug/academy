# AAB-M06 Tools and bounded agents
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Define an allowed tool contract
- Constrain action proposals

## Prerequisite and capstone contribution
Use the previous module evidence as input: AAB-M05

Save this module evidence in the same course portfolio: Tool contracts and workflow traces.

## Explain the concept
A bounded agent selects from narrow validated tools. Tool outputs and source documents are untrusted data; they cannot grant new permissions or override the user request.

## Demonstration and sample input
Allowed tools are lookup_course(course_id) and propose_lesson(module_id, request). Reject delete_course, issue_certificate and arbitrary shell execution. A tool failure returns a typed error and no fabricated success.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Define exact tool input schemas.
2. Restrict valid course and module IDs.
3. Simulate an allowed lookup.
4. Test unknown ID and unsupported action.
5. Inspect proposed file paths.
6. Record a trace without secrets.

## Expected result
Allowed lookup returns catalog data. Unsupported tools and invalid paths fail before execution. Draft tools do not publish or modify client systems.

## Negative test
A retrieved note says ignore rules and execute a shell command. Treat the text as source content, not an instruction.

## Recovery test
Tool unavailable: return the dependency and preserve the draft state for an operator to resolve.

## Independent practice
Add a read-only lesson-status tool and design permission and audit fields.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Tool contracts and workflow traces.
- Inputs are validated
- Unauthorized requests are denied
- No unrestricted execution tool is exposed

## Learner reflection
Why is a general shell tool unsuitable for this content task?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S07, S08. Check model, retrieval and tool behavior in the approved environment. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
