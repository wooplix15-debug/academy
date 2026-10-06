# ZDV-M08 Deluge integrations
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Use documented integration tasks
- Handle external call limits deliberately

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZDV-M07

Save this module evidence in the same course portfolio: Integration code and response log.

## Explain the concept
A Deluge integration wrapper still calls a versioned product API and consumes limits. Treat each response as evidence and plan batching or scheduling from observed operation costs.

## Demonstration and sample input
Plan ten records with one lookup and one write each: estimated 20 operations before retries. This is an exercise estimate; current CRM credits and concurrency depend on operation, edition and organization.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Locate the official wrapper signature for the chosen API version.
2. Verify parameter order and connection name.
3. Build a sample request with synthetic values.
4. Execute in training or use the mock contract.
5. Check body-level success.
6. Estimate calls and record actual usage when available.

## Expected result
The record key and returned ID are captured without secrets. The call estimate states assumptions and retry allowance. No fixed platform limit is invented.

## Negative test
Return a record validation error within a response. Route it to correction rather than retrying unchanged input.

## Recovery test
Simulate quota exhaustion, pause work and resume according to observed platform signals and configured retry bounds.

## Independent practice
Compare individual writes with a documented batch operation including partial failures.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Integration code and response log.
- API version is recorded
- Response success is checked
- External call consumption is estimated

## Learner reflection
Why can a batch HTTP success still require investigation?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S04, S05, S09, S10, S12, S13. Verify the Creator or CRM edition, event, API scope or quota used by this module. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.

## Code demonstration files
Use materials/code_examples/README.md and the matching Deluge starter. These have not been executed in a connected editor. Record the actual product, version, observed result and trainer correction before using them in class.
