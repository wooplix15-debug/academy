# ZIM-M06 Data migration
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Reconcile source and target records
- Prepare a reversible migration procedure

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZIM-M05

Save this module evidence in the same course portfolio: Migration checklist and reconciliation report.

## Explain the concept
Migration is a controlled transformation with evidence. A source count alone is not enough: rejected and intentionally excluded rows need separate reasons and stable source identifiers.

## Demonstration and sample input
The new leads_50.csv fixture has 50 rows. Lab policy requires name, company and syntactically valid email. Rows 43-47 are invalid and rows 48-50 duplicate emails 1-3. Keep the first valid email occurrence: 42 accepted, 5 rejected, 3 excluded.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Preserve the source file and record its hash.
2. Map fields and normalize email case and whitespace.
3. Run the offline validator before a trial import.
4. Import only the accepted file into a training organization.
5. Reconcile source IDs to target IDs.
6. Rehearse removal using the migration batch identifier.

## Expected result
50 = 42 accepted + 5 rejected + 3 excluded. Offline accepted is not proof of 42 successful Zoho imports; record target success and failures separately after the actual trial.

## Negative test
Change one accepted row to an existing destination email. Predict the chosen import duplicate behavior and reconcile its actual result.

## Recovery test
Rollback only records created by the trial batch. Restore separately any existing record the import changed.

## Independent practice
Change policy to permit a blank company, rerun classification and explain the count difference.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Migration checklist and reconciliation report.
- Source equals imported plus rejected plus intentionally excluded
- Rejected records have reasons
- Rollback steps are documented

## Learner reflection
Why preserve a migration batch ID?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S06, S09, S11. Verify the current edition, account metadata and API signature before a live product demonstration. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
