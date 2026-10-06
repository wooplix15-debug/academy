# ZDV-M02 Creator forms and reports
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Build related forms
- Create appropriate views for users

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZDV-M01

Save this module evidence in the same course portfolio: App screenshots and data dictionary.

## Explain the concept
Form fields capture validated data; reports present a specific user task. A lookup must preserve identity, and a report filter must be stated explicitly.

## Demonstration and sample input
Requests SR001 Open, SR002 Closed and SR003 Open should produce two rows in the open-request report. Work item W001 selects SR001 by lookup, not a copied customer name.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Create customer, request and work-item forms.
2. Choose lookup and numeric types.
3. Add a request-status allowed set.
4. Create an Open-only report.
5. Enter three requests and two work items.
6. Verify links and counts.

## Expected result
Open report contains SR001 and SR003 only. Each work item resolves to the intended request. Export the dictionary with proposed API names for later verification.

## Negative test
Select an invalid or missing request reference. Validation must reject it or require a documented correction route.

## Recovery test
Change SR003 to Closed and verify the filtered report now contains one row.

## Independent practice
Add a technician-specific open-work report and test another technician persona.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
App screenshots and data dictionary.
- Lookups connect intended records
- Validation catches bad input
- Report filters match user tasks

## Learner reflection
Why avoid a text field for a relationship?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S04, S05, S09, S10, S12, S13. Verify the Creator or CRM edition, event, API scope or quota used by this module. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
