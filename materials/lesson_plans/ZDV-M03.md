# ZDV-M03 Deluge language essentials
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Use variables lists maps and conditions
- Trace a script with sample values

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZDV-M02

Save this module evidence in the same course portfolio: Commented script and expected outputs.

## Explain the concept
Normalization needs explicit type and missing-value rules. Do not confuse zero with missing, or silently convert malformed text to a valid amount.

## Demonstration and sample input
Five payloads: amount 0 remains valid; amount "1250" becomes numeric 1250; absent amount fails validation; amount "twelve" fails parsing; email " A@Example.Test " becomes "a@example.test".

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Write a five-row input-output table.
2. Build Deluge maps and lists in the training editor.
3. Trace conditional branches for each payload.
4. Handle missing and malformed amounts separately.
5. Compare every output to the table.

## Expected result
Two valid numeric transformations, two explicit amount errors, and one normalized email example. Log only synthetic identifiers and error codes.

## Negative test
Replace a missing-value check with a truthiness check and show how it wrongly rejects zero.

## Recovery test
Correct the check and rerun all five cases, including a zero-value boundary.

## Independent practice
Normalize an optional date using an explicit expected format and reject an invalid date.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Commented script and expected outputs.
- Null values are handled
- Each output matches the input rule
- Learner explains the control flow

## Learner reflection
Should a missing amount default to zero?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S04, S05, S09, S10, S12, S13. Verify the current edition, account metadata and API signature before a live product demonstration. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.

## Code demonstration files
Use materials/code_examples/README.md and the matching Deluge starter. These have not been executed in a connected editor. Record the actual product, version, observed result and trainer correction before using them in class.
