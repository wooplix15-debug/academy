# ZDV-M04 Deluge functions and debugging
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Write reusable functions
- Diagnose failure from controlled logs

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZDV-M03

Save this module evidence in the same course portfolio: Function and debugging notes.

## Explain the concept
A reusable function exposes an input-output contract. Debugging is a controlled experiment: reproduce, isolate, repair and regress using the smallest relevant input.

## Demonstration and sample input
Seeded defects: treating zero as absent; comparing number 10 to string "10" without normalization; returning success before checking required customer ID. Each gets a failing input and expected output.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Define validate_request input keys and output ok plus errors.
2. Reproduce all three defects.
3. Add one failing case per defect.
4. Repair one defect at a time.
5. Rerun valid and invalid cases.
6. Replace sensitive logs with request ID and error code.

## Expected result
Validation returns ok false with named reasons for bad inputs, and preserves zero when allowed. Debug notes show cause and evidence, not only final code.

## Negative test
Supply an empty customer ID with otherwise valid fields. Validation must fail.

## Recovery test
Inject a controlled exception, return a typed failure and preserve a correlation ID for support.

## Independent practice
Extract a normalization function and define whether it mutates the original map.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Function and debugging notes.
- Inputs have a contract
- Logs omit tokens and personal data
- Each defect has a reproducible test

## Learner reflection
Why rerun a previously passing case after a repair?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S04, S05, S09, S10, S12, S13. Verify the Creator or CRM edition, event, API scope or quota used by this module. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.

## Code demonstration files
Use materials/code_examples/README.md and the matching Deluge starter. These have not been executed in a connected editor. Record the actual product, version, observed result and trainer correction before using them in class.
