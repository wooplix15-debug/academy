# ZDV-M06 REST and JSON contracts
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Read an API request and response
- Map payloads to application fields

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZDV-M05

Save this module evidence in the same course portfolio: Contract and mapping table.

## Explain the concept
An API contract describes types, required fields, pagination and error handling independently of a particular transport library. API names must be verified against the actual organization metadata.

## Demonstration and sample input
Mock response data contains record id 1001, External_Request_Key NOVA-D001 and Amount 1250; info.more_records is true. Map only approved fields and request the next page deliberately.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Create a source-to-target mapping table.
2. Parse the mock success response.
3. Handle empty data and absent optional fields.
4. Add pagination stop conditions.
5. Test malformed JSON and non-success status.
6. Record metadata and API version to verify.

## Expected result
The mapped request preserves its external key and numeric amount. Empty data yields no fabricated record. Pagination stops on the documented condition or a configured safety limit.

## Negative test
Receive HTTP success with a record-level error. Do not treat transport success as business success.

## Recovery test
Record the failing page and resume only from a supported cursor or page strategy after diagnosis.

## Independent practice
Add an optional currency field and a contract version compatibility note.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Contract and mapping table.
- Required fields are explicit
- Pagination is considered
- Malformed JSON has a handled failure path

## Learner reflection
What are two layers of API success?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S04, S05, S09, S10, S12, S13. Verify the current edition, account metadata and API signature before a live product demonstration. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
