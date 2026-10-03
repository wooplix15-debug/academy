# ZDV-M07 OAuth and connections
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Explain delegated authorization
- Configure minimum required access

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZDV-M06

Save this module evidence in the same course portfolio: Setup guide with redacted evidence.

## Explain the concept
OAuth delegates permission; a connection stores authorized access for tasks. Scopes, data center, organization and environment are part of the configuration, not strings to copy blindly.

## Demonstration and sample input
A read-only CRM connection should read the intended training module. An attempted create must fail if the required operation is outside its granted access. Use placeholders in notes, never a live token.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. List exactly which module operations the app needs.
2. Record training organization and region endpoint.
3. Create or inspect an authorized connection.
4. Run an allowed read.
5. Run a deliberately denied operation.
6. Save redacted setup and revocation steps.

## Expected result
An allowed read and denied write are evidenced separately. Credential values do not appear in screenshots, source code or learner submissions.

## Negative test
Use the wrong organization or insufficient scope. Distinguish configuration failure from a data validation error.

## Recovery test
Reauthorize only after the owner confirms the required scope, then rerun the exact failed operation.

## Independent practice
Design separate test and production connection names and prevent accidental cross-environment selection.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Setup guide with redacted evidence.
- No secret is submitted
- Scopes match the lab
- Test and production environments are distinguished

## Learner reflection
Why not solve every denial with full access?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S04, S05, S09, S10, S12, S13. Verify the current edition, account metadata and API signature before a live product demonstration. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
