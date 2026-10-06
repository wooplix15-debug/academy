# ZIM-M03 Permissions and environment
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Test a role based access model
- Plan separated test and production work

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZIM-M02

Save this module evidence in the same course portfolio: Access matrix and test evidence.

## Explain the concept
A profile controls allowed operations; role and sharing choices affect record visibility. Test both with actual training personas, because a diagram alone does not prove access.

## Demonstration and sample input
Sales West can edit assigned West leads; Sales East cannot read West-only records; the manager can review both regions; the integration persona receives only the operations needed by its contract.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Create an operation-by-persona matrix.
2. Configure three training users or simulate unavailable roles on paper.
3. Test own-region read and edit.
4. Test other-region read, export and administrative changes.
5. Record edition, sharing rules and observed results.

## Expected result
At least six allowed and six denied checks with tester, expected outcome and evidence. Screenshots must not contain credentials.

## Negative test
Try exporting records using the Sales East persona when export is denied by the proposed profile. A denial must be observable, not assumed.

## Recovery test
Remove an accidental broad sharing rule and repeat every visibility test it could affect.

## Independent practice
Design access for a temporary reviewer who needs read-only deal access for one department.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Access matrix and test evidence.
- Sales access meets scope
- Manager visibility is tested
- Admin privileges are not given to all learners

## Learner reflection
Why does hiding a field on a page not prove security?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S06, S09, S11. Verify the CRM feature, edition, profile or sandbox behavior used by this module. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
