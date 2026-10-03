# ZIM-M07 Integration planning
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Define a minimal integration contract
- Test authentication and failure behavior

## Prerequisite and capstone contribution
Use the previous module evidence as input: ZIM-M06

Save this module evidence in the same course portfolio: Contract, sample payload and failure log.

## Explain the concept
An integration contract states identity, field ownership, accepted payloads, responses and recovery. A timeout does not reveal whether the destination already committed.

## Demonstration and sample input
Deal D001 emits event EVT001 with request key NOVA-D001. The destination stores that key uniquely. If its response is lost after committing, querying the key must find the existing request before any retry decision.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Write source-to-destination field mappings.
2. Define request key and version ownership.
3. Describe allowed OAuth scopes and training environment.
4. Walk through success, denied authorization and ambiguous timeout.
5. Link the contract to the synchronization simulator.

## Expected result
One destination business record for NOVA-D001 even after replay; an unresolved timeout is marked unknown until reconciled. Real API behavior still needs a connected sandbox test.

## Negative test
Return a permission denial. Do not repeatedly retry the same operation using broader access.

## Recovery test
Lose the success response after commit, query by stable key and reconcile before replay.

## Independent practice
Add a destination-maintained delivery date and explain why the CRM writer must not overwrite it.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Contract, sample payload and failure log.
- Credentials are not in artifacts
- Duplicate event behavior is specified
- Environment specific authorization is respected

## Learner reflection
Can an HTTP timeout be treated as a failed write?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S02, S03, S06, S09, S11. Verify the current edition, account metadata and API signature before a live product demonstration. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
