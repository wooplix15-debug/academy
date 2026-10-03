# AAB-M02 Prompt design and structured output
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Write an input and output contract
- Test a prompt against examples

## Prerequisite and capstone contribution
Use the previous module evidence as input: AAB-M01

Save this module evidence in the same course portfolio: Prompt, schema and five trial outputs.

## Explain the concept
Structured output enforces shape, while factual checks evaluate meaning. A schema-valid lesson can still contain unsupported product behavior or an impossible duration.

## Demonstration and sample input
Required lesson fields are module_id, outcomes, activity_minutes, source_ids and review_notes. A response claiming ten 30-minute activities for a two-hour class is structurally valid but fails the duration check.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Write the lesson output schema.
2. Supply one approved topic and two examples.
3. Test missing module ID, extra fields and invalid duration.
4. Check each factual claim against source text.
5. Record prompt version and assumptions.

## Expected result
Five trial outputs have schema and content results recorded separately. Activity minutes fit the available teaching time.

## Negative test
A source ID exists but does not support the quoted claim. Fail evidence support even if the JSON validates.

## Recovery test
Ask for a narrower correction using the failed field and repeat the original checks.

## Independent practice
Add an accessibility field and design a compatible schema update.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Prompt, schema and five trial outputs.
- Required fields appear
- Assumptions are labeled
- Unsupported details are marked for review

## Learner reflection
What does schema success prove?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S07, S08. Verify the current edition, account metadata and API signature before a live product demonstration. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
