# AAB-M04 Knowledge preparation
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Classify usable source material
- Keep source and permission metadata

## Prerequisite and capstone contribution
Use the previous module evidence as input: AAB-M03

Save this module evidence in the same course portfolio: Knowledge manifest and cleaned records.

## Explain the concept
Knowledge records need identity, status, permission, version and provenance. Chunking preserves relevant context, but an index must also respect access and source lifecycle.

## Demonstration and sample input
K1 is approved public guidance; K2 is an older draft; K3 is client-only; K4 contains a malicious instruction. Public retrieval considers approved public current records only; K4 is data, never authority to change instructions.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Clean three synthetic notes without losing qualifiers.
2. Assign source and chunk IDs.
3. Record owner, version and permission.
4. Exclude restricted and obsolete records.
5. Add a text-instruction attack to a test record.
6. Inspect the resulting manifest.

## Expected result
Every chunk links back to a source. Restricted records are excluded before ranking and context assembly, not merely hidden in the final answer.

## Negative test
A highly relevant client-only document appears. Public retrieval must exclude it.

## Recovery test
Withdraw a previously approved source and verify it no longer enters context.

## Independent practice
Design source expiration and reviewer reminders for an API reference.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Knowledge manifest and cleaned records.
- Each record has an owner and date
- Confidential content is excluded
- Draft and approved sources are distinguished

## Learner reflection
Why filter permissions before context assembly?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S07, S08. Check model, retrieval and tool behavior in the approved environment. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
