# AAB-M05 Retrieval and cited answers
Version 0.2 | Team review required | Synthetic teaching case

## Purpose
- Retrieve relevant context
- Explain when the assistant should abstain

## Prerequisite and capstone contribution
Use the previous module evidence as input: AAB-M04

Save this module evidence in the same course portfolio: Answers with source identifiers and retrieval notes.

## Explain the concept
Retrieval finds candidate evidence; generation uses it to answer. A citation is useful only when it supports the exact claim. Missing or conflicting evidence needs an explicit response.

## Demonstration and sample input
The local lexical retriever answers certificate issuer using approved K1. It abstains for job guarantee, excludes client-only K3 and does not treat a document instruction as a command. It uses word overlap, not embeddings or model inference.

## Live teaching sequence
- Retrieve prior learning: 15 minutes
- Explain and predict: 30 minutes
- Trainer demonstration: 35 minutes
- Guided build: 75 minutes
- Break: 15 minutes
- Failure and recovery tests: 40 minutes
- Evidence review and exit check: 30 minutes

## Guided lab
1. Run the retrieval exercise.
2. Inspect eligible records before scoring.
3. Ask five supported and unsupported questions.
4. Cite record ID plus supporting statement.
5. Mark conflicts.
6. Compare lexical matching with a proposed semantic retriever.

## Expected result
Supported answer cites K1. Unsupported questions abstain. Evidence-only simulation results are labeled separately from live model evaluation.

## Negative test
Ask a question whose only matching source is a draft. Do not promote draft content to fact.

## Recovery test
Add an approved source, rebuild the eligible set and rerun the original unanswered case.

## Independent practice
Create a paraphrase that lexical overlap misses and explain what semantic retrieval might improve.

Budget: 120 minutes. Use 15 minutes planning, 75 building and testing, 30 documenting.

## Submit and assess
Answers with source identifiers and retrieval notes.
- Citations support the answer
- Missing evidence causes abstention
- Conflicting sources are surfaced

## Learner reflection
Why is the highest scoring result not automatically enough?

Describe one failed input, your correction and evidence that the correction worked.

## Source verification
Official reference IDs: S07, S08. Verify the current edition, account metadata and API signature before a live product demonstration. Examples and thresholds are proposed lab rules.

## Trainer preparation
Use the separate trainer key. Rehearse the positive, negative and recovery case. Provide a mock equivalent if required product access is unavailable; label the evidence accordingly.
