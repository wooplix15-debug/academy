# AAB-M08 Operations and cost
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Measure usage and latency
- Plan bounded retries and cost limits

## Prerequisite and capstone contribution
Use the previous module evidence as input: AAB-M07

Save this module evidence in the same course portfolio: Usage log and operating limits.

## Explain the concept
Operations measure actual usage, latency, retries and quality. Token prices and model availability should be configured from current official information rather than buried in a lesson.

## Demonstration and sample input
Synthetic exercise: 10000 input tokens at configured USD 1 per million and 2000 output tokens at USD 4 per million gives USD 0.018. Rates are invented teaching inputs, not current vendor prices.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Record request ID, model, timestamps and usage.
2. Separate estimated from observed cost.
3. Configure a per-run token bound.
4. Simulate two retries and a timeout.
5. Calculate full workflow cost including retries.
6. Document stop and escalation rules.

## Expected result
Cost worksheet reproduces USD 0.018 for the example. Retry limits and request timeouts are recorded; no claim that the estimate is the actual billed cost.

## Negative test
Usage is missing in a failed response. Mark cost unknown or estimated rather than zero.

## Recovery test
Stop when the run budget is reached and preserve enough state for diagnosis.

## Independent practice
Compare two prompt versions using quality and reviewer time alongside cost.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Usage log and operating limits.
- Observed values are separated from estimates
- Retries are bounded
- Logs avoid sensitive content

## Learner reflection
Why is cheapest per-request output not necessarily cheapest per accepted lesson?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S07, S08. Check model, retrieval and tool behavior in the approved environment. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
