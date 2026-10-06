# ZIM-M02 Solution and data design
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Map requirements to configuration
- Design field and relationship choices

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZIM-M01

Save this module evidence in the same course portfolio: Diagram and configuration decision log.

## Explain the concept
Store a business fact once and connect records through relationships. Repeated customer names are not a reliable identity rule; people can share names and names can change.

## Demonstration and sample input
Nova has account A001, contacts C001 and C002, and deals D001 and D002. Both deals reference A001; a delivery request references D001. Updating the account name must not require editing four copies.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Identify Accounts, Contacts, Deals and Delivery Requests.
2. Assign a stable key and data owner to each.
3. Draw one-to-many relationships and mark optional lookups.
4. Map all eight requirements to a field, configuration feature or explicit gap.

## Expected result
A dictionary with field type, API name to verify, required rule, owner and sample value. Deal amount uses INR in this exercise and cannot be a free text string.

## Negative test
Create two customers called Nova Services. The design must keep their identifiers distinct rather than merging by display name.

## Recovery test
Rename account A001 and show that linked deals still reference the same identity.

## Independent practice
Add a recurring service renewal without duplicating the original account; explain the new entity or field decision.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Diagram and configuration decision log.
- Every entity has an identifier
- Required fields have a business reason
- Each requirement maps to a feature or gap

## Learner reflection
When should a new module be created?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S06, S09, S11. Verify the CRM feature, edition, profile or sandbox behavior used by this module. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
