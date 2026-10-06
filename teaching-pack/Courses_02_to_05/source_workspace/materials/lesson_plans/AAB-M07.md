# AAB-M07 Evaluation and adversarial cases
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Design realistic evaluation cases
- Measure task success and failure

## Prerequisite and capstone contribution
Use the previous module evidence as input: AAB-M06

Save this module evidence in the same course portfolio: Evaluation CSV and result report.

## Explain the concept
Evaluation should separate normal task quality from critical access failures. A high average cannot compensate for a leaked restricted document or unauthorized write.

## Demonstration and sample input
The supplied 20-case matrix contains supported, missing, stale, conflicting, restricted, injection, malformed and unavailable-tool scenarios. Each case has expected behavior and a critical flag; model actuals start blank.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Define evidence-support and task-completion rubrics.
2. Run the local retrieval subset.
3. Execute configured model cases only when available.
4. Record actual output, scorer and evidence.
5. Report category counts.
6. Investigate every critical failure.

## Expected result
Twenty designed cases are present. Only cases actually executed are scored; blank actuals are not passes. Release requires zero observed critical permission failures under the proposed policy.

## Negative test
Nineteen good outputs and one restricted-source leak. The critical gate fails despite 95 percent simple success.

## Recovery test
Repair source eligibility and rerun the failed case plus similar boundary cases.

## Independent practice
Add five cases from anonymized learner feedback after permission and review.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Evaluation CSV and result report.
- Cases include missing sources
- Permission violations are counted separately
- Scoring rules are reproducible

## Learner reflection
How should unexecuted cases affect the report?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S07, S08. Check model, retrieval and tool behavior in the approved environment. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
