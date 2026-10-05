---
course_id: "C04"
chapter_id: "C04-CH03"
chapter_number: 3
chapter_title: "Opportunity Identification"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "partially_verified"
---

# Opportunity Identification

1. What you will learn
A recurring problem is a starting point, not yet an automation proposal. “We spend too much time on enquiries” could refer to missing information, repeated data entry, document searches, unclear wording or unresolved availability decisions. Each issue suggests different work and different possible solutions.
In this chapter, you will learn to:
- Identify useful opportunities across Sales, Service, Finance, HR and Operations.
- Recognise document handling, knowledge retrieval, decision support and cross-app work.
- Turn a recurring issue into a bounded use-case card.
- Specify the affected team, task, trigger and expected result.
- Connect a proposed opportunity to evidence, ownership and exceptions.
- Compare simpler alternatives before assuming that AI is necessary.
Your required practice is to create use-case cards from supplied recurring issues. All information needed for the exercises is included.
Prerequisites and continuity
Chapter 1 introduced rules, integrations, generative assistance and agents. Chapter 2 taught you to map the current process and distinguish facts, assumptions and unknowns.
Meridian Supply’s existing candidates remain:

| Opportunity ID | Established candidate |
| --- | --- |
| MSP-OPP-001 | Improve required-field completeness and validity |
| MSP-OPP-002 | Reduce effort spent organising varied enquiry wording |
| MSP-OPP-003 | Investigate repeated entry of approved enquiry information |
The Chapter 2 discovery packet did not establish that drafting is the main cause of quotation delay. It showed information-correction returns, internal queues, customer clarification waiting and separate access and availability exceptions.
Pilot MSP-PILOT-001 remains proposed and unexecuted. This chapter develops candidate descriptions; it does not establish a selected production solution or a financial return.
Your contribution to the course project
You will produce a Use-Case Card Set and an Opportunity Backlog for the Business Automation Pilot Proposal.
These artifacts connect the current-state problem to a specific piece of work. Chapter 4 assesses readiness, Chapter 5 develops value and costs, and Chapter 6 compares and prioritises solution options.
The Meridian scenario is synthetic. You may substitute a permission-cleared company case while preserving the distinction between evidence and assumptions.
2. Lessons
Lesson 1 — Turn a recurring issue into a bounded use case
A use case describes how a person or system performs a particular task in response to a trigger and produces a useful result.
An opportunity is a candidate improvement. It may involve changing the process, using an existing feature, connecting systems or introducing AI assistance.
A useful use-case statement follows this pattern:
When trigger occurs, help affected team perform task, producing expected result.
Compare these descriptions:

| Description | What it tells you |
| --- | --- |
| “Use AI in Sales” | A technology preference and a department |
| “Automate quotations” | A broad process, with unclear boundaries |
| “When an enquiry arrives, help Sales identify missing required fields before the Operations handoff” | A trigger, team, task and point in the process |
| “Produce either a checked enquiry record or a specific clarification request” | An observable result |
The expected result should describe an output or state that someone can inspect. “Improve efficiency” is a business aspiration. “Create a draft brief with product, quantity, requested date and unresolved questions” is an inspectable result.
Look across business functions
The following examples are separate synthetic demonstrations. They do not expand Meridian’s enquiry-to-quotation project boundary.

| Function | Supplied situation | Bounded opportunity and demonstration |
| --- | --- | --- |
| Sales | An email asks for 25 BF-10 units for 15 October; approved delivery confirmation is absent | Extract the request into an internal brief, separating the requested date from confirmed delivery |
| Service | Customers repeatedly ask how to request returns; an approved guide exists | Retrieve the current guide and prepare a draft explanation for Service review, rather than decide individual eligibility |
| Finance | Invoice INV-17 references approved purchase order PO-88, but receiving evidence is absent | Produce a missing-evidence exception for Finance; do not treat the absence as proof that goods were not received |
| HR | A role-specific induction guide exists, but a new starter’s date is missing | Draft the role checklist and flag the missing scheduling input; do not invent the start date |
| Operations | A customer requests 60 units against a 40-unit stock snapshot | Prepare an availability exception brief for Operations; do not promise replenishment or substitution |
Each opportunity has a useful result even when the case cannot proceed normally. A clarification request or missing-evidence flag can be the correct output.
Why recurrence matters
A single inconvenience may reveal a real issue, but it does not establish volume or value. Look for repeated task patterns in records, interviews and process maps.
Meridian’s supplied weekly correction log includes 14 missing-quantity/date cases, six copied-code errors and four outdated-stock checks. Those counts support investigation of recurring information problems. They do not prove that one solution can remove every problem.
A common mistake is to combine unrelated issues into one impressive-sounding proposal. Missing quantity, outdated stock information and denied source access require different explanations and may have different owners.
Check L1: Rewrite “Buy a chatbot for Service” as a use-case statement. Assume the trigger is a new returns-information enquiry and the task is to use an approved guide to prepare a draft answer.
Lesson 2 — Distinguish document handling from knowledge retrieval
Document handling works on information already supplied in a document or message. It can include sorting, naming, extracting fields, checking completeness and preparing summaries.
Knowledge retrieval finds relevant information in an approved collection of sources. It may use exact words or search by meaning. Searching by meaning is often called semantic search.
The distinction is practical:
- “Find the quantity in this enquiry” is extraction from a supplied document.
- “Find the current return guide” is retrieval.
- “Draft an explanation using that guide” is generation.
- “Approve this return” is a business decision.
A solution may combine these tasks, but they should remain visible in the use-case description.
As one product example, OpenAI’s official file-search documentation describes semantic and keyword search over previously uploaded files in configured knowledge bases.1 That supports the idea of searching a defined source collection. It does not establish that every company document is connected, current or authorised for a particular user.
Worked demonstration: extract without inventing
The supplied message is:
Please quote BF-10 for delivery on 15 October 2026. Send the quotation to buyer@example.com.
A document-handling output could be:

| Field | Extracted value | Status |
| --- | --- | --- |
| Product | BF-10 | Supplied |
| Quantity | Not supplied | Clarification required |
| Requested delivery date | 2026-10-15 | Customer request |
| Contact | buyer@example.com (mailto:buyer@example.com) | Supplied |
The output should preserve the missing quantity. A blank field is not an invitation to guess.
If a structured form can collect these fields directly, it may remove extraction work. Generative assistance is more relevant when the business must accept varied language and formats.
Worked demonstration: retrieve the right evidence
Suppose a search returns these two documents:

| Source | Status and content |
| --- | --- |
| Current Operations note | Approved; delivery requires Operations confirmation |
| Old sales note | Obsolete; says “BF-10 can always be delivered next day” |
The obsolete note may match the customer’s question closely. Relevance is not authority.
A useful retrieval opportunity must therefore identify:
- Which source collection is permitted.
- Who owns the content.
- Which version or status is authoritative.
- What happens when no suitable source is found.
- Who checks the resulting explanation.
Retrieval can help a model use evidence, but it does not guarantee that the answer preserves the source accurately. Official guidance recommends grounding claims, allowing uncertainty and checking important information; those methods reduce rather than eliminate unsupported output.2
A common mistake is to describe retrieval as “the assistant knows our business”. A better description is “the assistant can search this approved collection and show the sources used”.
Check L2: A retrieved document is highly relevant but marked obsolete. What does its relevance establish, and what should happen before its content is used?
Lesson 3 — Separate decision support from decision ownership, and recognise cross-app work
Decision support organises evidence, applies known criteria or presents options to help a person decide. It does not automatically transfer responsibility for the decision.
For Meridian, an internal brief might compare requested quantity with a supplied stock snapshot:
60 requested units − 40 snapshot units = 20 units beyond the snapshot quantity
This calculation identifies a discrepancy. It does not establish the current shortage, because the snapshot may not reflect current reservations or replenishment. It also does not identify a permitted delivery commitment.
A useful decision-support output is:
The request is for 60 units. The supplied snapshot lists 40. Operations must confirm current availability and any delivery option. No approved substitute or replenishment date is supplied.
The important business decision remains with Operations and Sales.
Cross-app work
Cross-app work reads or moves information across applications. It often appears as rekeying, copying attachments, checking statuses or reconciling identifiers.
Meridian may have a Sales intake worksheet and an Operations request application. The repeated task is not “think about the enquiry”. It is “carry these approved fields accurately from one place to another”.
A proposed transfer needs a clear mapping:

| Business information | Source | Intended destination |
| --- | --- | --- |
| Enquiry reference | Sales business enquiry ID | External enquiry reference |
| Product | Checked product code | Requested product |
| Quantity | Checked whole-number quantity | Requested quantity |
| Requested date | Customer requested date | Requested date, not promised date |
If the destination assigns record ID REQ-7401 to enquiry MSP-ENQ-401, retain both. REQ-7401 is an illustrative destination-generated identifier. It must not replace the business enquiry or opportunity ID.
An integration is a plausible mechanism. However, removing the second entry may be simpler if both teams can work from one appropriate record. Investigate that option before connecting a duplication that has no business purpose.
Fixed work does not require an agent
A predefined sequence—validate fields, copy them, and flag a mismatch—is a rules-and-integration workflow.
An agent becomes relevant only when model-selected investigation is genuinely needed. “It touches three systems” is not sufficient justification.
Cross-app opportunities also depend on permissions and available interfaces. At this stage, describe the desired transfer and its owner. Do not assume that a connection is available or that read access includes write access.
Check L3: Why does an availability brief support a decision without authorising a delivery promise?
Lesson 4 — Make a use-case card testable without pretending it is a business case
A use-case card is a compact record of one candidate improvement. Its four essential fields are:
1. Affected team.
2. Task.
3. Trigger.
4. Expected result.
For a course-project card, add enough context to make those fields meaningful:

| Additional field | Why it matters |
| --- | --- |
| Evidence and current problem | Connects the proposal to an observed or supplied issue |
| Owner and review point | Makes responsibility explicit |
| Work pattern and candidate mechanism | Distinguishes the task from a preferred product |
| Exceptions and action boundary | Describes what happens when normal processing is not possible |
| Plausible alternatives | Keeps simpler options visible |
| Proposed measure | Makes the expected result inspectable |
| Unknowns | Prevents assumptions from becoming hidden promises |
A proposed measure is not an observed result. “Record whether each brief preserves quantity” is a measurement idea. “All briefs are accurate” requires test evidence.
Likewise, a card is not a financial justification. Released capacity, cash savings, implementation costs, licences, model usage, review effort and maintenance belong in the later value/cost model.
Worked example: improve an overbroad card
Weak card:
Automate all enquiry work with AI to save time.
Improved card:
When Sales receives an enquiry, check product, quantity and requested date before the Operations handoff. Produce either a checked request or a clarification list. Sales owns the intake rules. Compare a clearer intake form with validation in the existing record. Measure missing-field handoffs and clarification effort. Access and availability exceptions remain separately identified.
The improved version is narrower but more useful. You can inspect the output and explain what evidence would support its value.
Check L4: Why is “reduce effort” insufficient as the only expected-result field on a use-case card?
3. Visual explanation — From problem evidence to a candidate opportunity
flowchart TD
    A[Recurring issue in records or process map] --> B[Identify affected team and task]
    B --> C[Define trigger and bounded output]
    C --> D[Identify work pattern]
    D --> E[Compare simplification, rules, integration and AI assistance]
    E --> F[Name owner, exceptions and proposed measure]
    F --> G[Record candidate use-case card]
    G --> H[Assess readiness, value and priority in later chapters]
The diagram shows a reasoning sequence. You begin with an issue and its evidence, then define the work. Technology comparison follows that definition.
The last step is assessment, not automatic implementation. A well-written card may still be deferred because its data is unavailable, its ownership is unclear or its costs exceed its value.
The four work patterns describe what the business task concerns:
- Documents and messages.
- Finding knowledge.
- Supporting a decision.
- Working across applications.
Rules, integrations, generative assistance and agents describe how a proposed solution might perform that task. These are different classification questions.
4. Worked case — Meridian’s first use-case card set
New synthetic evidence
The following sources extend the case explicitly.

| Source ID | Supplied information |
| --- | --- |
| MSP-OBS-001 | Restatement of the weekly correction categories: 14 missing-quantity/date cases, six copied-code errors and four outdated-stock checks |
| MSP-OBS-002 | Four selected standard enquiries with the preparation breakdown below |
| MSP-OBS-003 | Approved knowledge extracts and one obsolete note |
| MSP-OBS-004 | Observation that Sales manually copies checked fields from its intake worksheet into the Operations request application for the four selected cases |
These are separate from the Chapter 2 timing packet and the proposed pilot reference packet. They are synthetic scenario records, not real product observations.
The new process detail is explicit: the selected cases include a manual transfer between a Sales intake worksheet and an Operations request application. No automated connection has been established.
Complete preparation packet
All four enquiries use BF-10, have permitted access and contain valid quantities and requested dates.

| Enquiry ID | Quantity | Requested date | Organise/check enquiry | Find source extracts | Rekey checked fields |
| --- | --- | --- | --- | --- | --- |
| MSP-ENQ-401 | 20 units | 2026-10-15 | 2 staff minutes | 2 staff minutes | 2 staff minutes |
| MSP-ENQ-402 | 10 units | 2026-10-15 | 2 staff minutes | 2 staff minutes | 2 staff minutes |
| MSP-ENQ-403 | 15 units | 2026-10-16 | 2 staff minutes | 2 staff minutes | 2 staff minutes |
| MSP-ENQ-404 | 5 units | 2026-10-16 | 2 staff minutes | 2 staff minutes | 2 staff minutes |
For these selected cases, the six preparation minutes are inside the 18 initial handling minutes. The remaining initial handling component is 12 minutes per case.
Preparation per case = 2 + 2 + 2 = 6 staff minutes
Packet preparation = 4 cases × 6 minutes/case = 24 staff minutes
Packet initial handling = 4 × 18 = 72 staff minutes
Reconciliation:
24 preparation minutes + 48 other initial minutes = 72 minutes
These figures describe current task coverage. They do not establish savings.
Knowledge packet
All source identifiers below are business labels for the synthetic case, not provider-generated file IDs.

| Source ID | Status | Supplied content |
| --- | --- | --- |
| MSP-KNOW-001 | Approved catalogue extract | BF-10 is a 10 mm brass fitting |
| MSP-KNOW-002 | Approved snapshot extract | 40 units listed at 2026-10-05 08:45; no reservation or future availability established |
| MSP-KNOW-003 | Approved substitution extract | No approved substitute for BF-10 |
| MSP-KNOW-004 | Obsolete sales note | “BF-10 can always be delivered next day” |
| MSP-KNOW-005 | Approved Operations note | Delivery requires Operations confirmation; no commitment supplied |
The packet contains no price. A brief cannot become a complete quotation merely by sounding complete.
Step 1: identify the recurring task families
The evidence suggests three related but distinct opportunities:
- Required-field problems can create unusable handoffs.
- Organising varied messages and finding source extracts consumes preparation effort.
- Rekeying checked fields creates repeated work and an opportunity for copying errors.
The knowledge extracts also show why source authority matters. The obsolete next-day note must not become a delivery promise.
Step 2: complete the use-case cards
Completed artifact: MSP_Use_Case_Cards_v0_1.md
MSP-OPP-001 — Required-field completeness and validity

| Field | Completed card |
| --- | --- |
| Affected team | Sales; Operations receives the handoff |
| Trigger | A new customer enquiry becomes available |
| Task | Check product code, positive whole-number quantity and requested date before handoff |
| Expected result | A checked request or a specific clarification list; no guessed values |
| Evidence | MSP-OBS-001 missing-information cases; Chapter 2 information-correction returns |
| Work pattern and mechanism | Document handling; clearer intake and rules are plausible |
| Owner and review | Sales Lead owns required-field rules; Sales resolves customer clarification |
| Exceptions and boundary | Unknown product, missing/invalid quantity or date; stop normal handoff until clarified |
| Alternatives | Simplified intake form; checklist; native validation if available |
| Proposed measure | Missing/invalid-field handoffs and staff clarification effort |
| Unknowns | Wider case mix and whether earlier checks reduce total effort |
MSP-OPP-002 — Organise enquiry wording into a source-grounded brief

| Field | Completed card |
| --- | --- |
| Affected team | Sales; Operations confirms availability facts |
| Trigger | A usable enquiry needs an internal preparation brief |
| Task | Organise the request and relevant approved source extracts |
| Expected result | Brief containing product, quantity, requested date, source references and unresolved questions |
| Evidence | MSP-OBS-002 organisation and lookup components; MSP-OBS-003 source packet |
| Work pattern and mechanism | Document handling and knowledge retrieval; template or generative assistance |
| Owner and review | Sales Lead owns acceptance; Operations owns availability confirmation |
| Exceptions and boundary | Missing authoritative evidence is labelled unknown; no price, delivery promise or customer sending |
| Alternatives | Standard template with source links; source-grounded drafting assistance |
| Proposed measure | Field preservation, unsupported claims, source correctness and total preparation/review effort |
| Unknowns | Whether varied wording justifies AI and whether review offsets time released |
MSP-OPP-003 — Reduce repeated entry of checked information

| Field | Completed card |
| --- | --- |
| Affected team | Sales and Operations |
| Trigger | Sales has a checked request ready for the Operations handoff |
| Task | Make the checked fields available to Operations without unnecessary rekeying |
| Expected result | One accurately linked request with matching business reference, product, quantity and requested date |
| Evidence | MSP-OBS-004 manual copying; MSP-OBS-002 two-minute rekey component |
| Work pattern and mechanism | Cross-app work; process simplification or integration |
| Owner and review | Sales and Operations agree field meaning; IT assesses connection and permissions |
| Exceptions and boundary | Unmatched reference or unapproved access requires an exception; do not create an unlinked duplicate |
| Alternatives | One appropriate shared record; native sharing/transfer if available; configured integration |
| Proposed measure | Rekey effort, field mismatches and duplicate/unlinked requests |
| Unknowns | Destination interface, licences, write permission and suitability of a shared record |
These cards preserve the original opportunity IDs. They refine the task description without claiming that the candidates have been selected or implemented.
Step 3: compare plausible starting points

| Candidate | Simpler option to investigate | More capable option to investigate | Decision still needed |
| --- | --- | --- | --- |
| MSP-OPP-001 | Clearer form and checklist | Validation in the existing process | Can the intake process collect required fields consistently? |
| MSP-OPP-002 | Standard brief template and source links | Source-grounded generative drafting | Does varied language justify the additional review and upkeep? |
| MSP-OPP-003 | Remove duplicate entry through one record | Integration between approved applications | Is the second record necessary, and can transfer be authorised? |
This is an option comparison, not a scored ranking. Readiness and realistic costs are not yet established.
Step 4: correct a double-counting mistake
Suppose someone claims:
- Opportunity 001 saves two minutes of organisation/checking.
- Opportunity 002 saves four minutes of organisation and lookup.
- Opportunity 003 saves two minutes of rekeying.
Adding these gives:
2 + 4 + 2 = 8 claimed minutes/case
But the supplied preparation component is only six minutes. Opportunities 001 and 002 overlap on the two-minute organisation/checking activity.
Across four cases:
8 × 4 = 32 claimed minutes, against 24 distinct preparation minutes.
The correction is not “therefore we save six minutes”. Six minutes is the covered baseline activity, not proven removable effort. Review, clarification, connection maintenance and source upkeep may remain or increase.
Record combined value only after separating overlapping activities and measuring the changed work.
Step 5: complete the backlog
Completed artifact: MSP_Opportunity_Backlog_v0_1.md

| Opportunity ID | Status | Current rationale | Next assessment |
| --- | --- | --- | --- |
| MSP-OPP-001 | Candidate for readiness assessment | Required-field problems recur in the supplied correction evidence | Ownership, intake stability and available validation |
| MSP-OPP-002 | Candidate for readiness assessment | Preparation includes wording and source work | Source quality, access, review effort and template comparison |
| MSP-OPP-003 | Candidate for readiness assessment | Manual rekeying is confirmed in the selected packet | Shared-record suitability, interfaces and permissions |
The backlog is a record of candidates. It is not an approval list.
5. Try it yourself — Guided practice
Learning goal and access
Turn three recurring issues into complete use-case cards.
Use paper or a local document. No product account is required. The exercise demonstrates opportunity definition; it cannot demonstrate model accuracy, connector behaviour or actual savings.
You may work individually. In a group, consider business ownership, operational exceptions, costs and access from the Sponsor, process lead, Finance and IT perspectives.
The following examples are outside Meridian’s main project boundary.
Complete issue inputs

| Evidence ID | Affected area and recurring issue | Supplied packet |
| --- | --- | --- |
| EX-EV-SVC-001 | Service repeatedly searches for returns guidance | Eight enquiries: five standard-item information questions, two bespoke-item questions and one with item type missing |
| EX-EV-FIN-001 | Finance repeatedly checks receiving evidence before payment review | Ten invoices: eight have matching receiving entries; two do not. Example INV-17 references approved PO-88, with no receiving entry found |
| EX-EV-HR-001 | HR repeatedly prepares role induction checklists | Four requests: three contain start dates; one does not. The missing-date request is for a warehouse coordinator |
No staff timings or post-change results are supplied. Do not estimate savings from these counts.
Approved source inputs
Service guide EX-DOC-SVC-001, current and approved for this exercise:
Requests to return unopened standard items may be submitted within 14 calendar days. Service reviews the request before confirming eligibility. Bespoke items require specialist review. If item type is missing, ask the customer to identify it.
This is a fictional company rule for the exercise, not a legal entitlement.
Finance records EX-DOC-FIN-001:
- INV-17 references PO-88.
- PO-88 is recorded as approved.
- The permission-cleared receiving register contains no matching entry for PO-88.
- Finance owns payment review.
- The exercise permits reading these records, not approving payment or changing supplier details.
“No matching entry” does not establish whether goods arrived.
HR guide EX-DOC-HR-001, approved for this exercise:
The warehouse coordinator induction checklist contains:
1. General orientation.
2. Role training.
3. Equipment request.
4. Safety briefing.
The exercise permits use of role, supplied start date and this guide. Personal health notes are not approved or supplied. HR owns checklist acceptance and scheduling.
A separate old induction note is marked obsolete. It must not be treated as current guidance.
Learner worksheet
Complete one card for each issue. Use IDs EX-OPP-SVC-001, EX-OPP-FIN-001 and EX-OPP-HR-001.

| Field | What to enter |
| --- | --- |
| Opportunity ID | Supplied stable card ID |
| Affected team | Team doing the task and any receiving team |
| Trigger | Event that starts this bounded task |
| Task | Specific work to perform |
| Expected result | Inspectable output, including uncertainty where relevant |
| Evidence | Supplied evidence and document IDs |
| Work pattern and mechanism | Business task pattern and plausible way to perform it |
| Owner and review | Who accepts the result |
| Exception and boundary | Missing data, permission limits and actions excluded |
| Alternatives | At least two plausible approaches |
| Proposed measure | What you would inspect or record |
| Unknowns | Information not established by the packet |
Steps and expected intermediate results
1. Write one recurring issue per card.
- Expected result: three distinct issues, supported by the supplied packets.
2. Specify trigger, team, task and result.
- Expected result: four essential fields on every card.
3. Separate information work from final decisions.
- Expected result: Service eligibility, payment review and HR acceptance remain with named owners.
4. Describe the relevant exception.
- Expected result: bespoke/missing item type, missing receiving evidence and missing start date are handled explicitly.
5. Compare two plausible approaches.
- Expected result: alternatives linked to the task, such as a template/checklist and appropriate retrieval or integration assistance.
6. Add measures and unknowns.
- Expected result: measurable outputs without invented timings, costs or benefits.
Your final artifact is C04_CH03_Use_Case_Cards_Practice.md, containing the three cards.
Retain the synthetic final artifact. No system cleanup is required.
6. Independent challenge
The Sponsor asks you to expand Meridian’s brief opportunity into “automatic complete quotations”.
Use this permission-cleared exercise variant:

| Input | Supplied value or constraint |
| --- | --- |
| Parent opportunity | MSP-OPP-002 |
| Variant label | CH03-C1 |
| Enquiry | MSP-ENQ-451: 25 BF-10 units, delivery requested for 2026-10-16 |
| Contact | buyer@example.com (mailto:buyer@example.com) |
| Available approved source | MSP-KNOW-001: BF-10 is a 10 mm brass fitting |
| Other available source | MSP-KNOW-004: obsolete next-day sales note |
| Missing from the permitted packet | Approved stock extract, price and delivery confirmation |
| Destination permission | Read permitted; write not permitted |
| Business owner | Sales Lead; Operations owns availability confirmation |
| Proposed claim | “Automatically issue a complete quotation and guarantee the requested date” |
The earlier main-case stock snapshot remains part of the main case. It is not available as authoritative evidence within this variant’s permitted packet.
Deliverables
1. Write a revised variant card, retaining the parent opportunity ID and variant label.
2. Define a useful output that can be produced from the permitted inputs.
3. Compare a standard internal template with generative assistance.
4. Explain why automatic quotation issuance is not supported.
5. Identify two evidence or readiness questions.
Success criteria
Your card must preserve the request, identify unknown stock/price/delivery, reject the obsolete promise as authority and respect the lack of write permission.
You must not turn the exercise variant into an approved change to the main case.
7. Common problems and recovery

| Symptom | Diagnosis | Correction | Verification |
| --- | --- | --- | --- |
| The card names only a product | Technology has replaced task definition | Write trigger, team, task and output first | A reader can understand the opportunity without the product name |
| “Expected result” says only “save time” | A business aspiration is being used as an output | Define the record, brief, flag or state produced | Someone can inspect whether it exists and is correct |
| Retrieval finds an obsolete answer | Relevance has been confused with authority | Check status and owner; use approved evidence or mark unknown | Every factual claim has a suitable source |
| A missing record becomes a negative conclusion | Absence of evidence has been overinterpreted | Report “not found in the supplied register” | The output does not claim an event never occurred |
| The card cannot name an owner | Responsibility is unresolved | Record the gap and seek an accountable owner | The card remains a candidate until ownership is established |
| Claimed savings exceed baseline activity | Overlapping tasks have been added twice | Map each proposal to distinct baseline activities | Covered minutes do not exceed the non-overlapping baseline |
| A broad card contains several triggers | Multiple use cases have been combined | Split tasks by trigger, output and owner where appropriate | Each resulting card has a coherent boundary |
Recovery in opportunity identification often means narrowing the task, recording an unknown or improving the evidence. It does not require inventing a technical solution.
8. Check your understanding
1. How do the four work patterns differ from rules, integrations, generative assistance and agents?
2. Why might a structured intake form be preferable to extracting fields from emails?
3. What is wrong with treating “no receiving entry found” as “goods were not received”?
4. Why should Meridian compare a standard brief template with generative assistance?
5. In the worked packet, why is an eight-minute combined saving claim invalid?
6. What is the difference between an opportunity backlog entry and an implementation approval?
9. Solutions and explanations
Lesson checks
L1: A suitable statement is:
When a returns-information enquiry arrives, help Service retrieve the current approved guide and prepare a draft answer for review.
An expected result could be a source-linked draft that distinguishes standard, bespoke and missing-item-type cases. Individual eligibility remains a Service decision.
L2: Relevance establishes that the document may address the topic. It does not establish current authority. Check status and ownership; do not use the obsolete statement as a commitment.
L3: The brief organises supplied evidence and identifies a discrepancy. It does not establish current availability or confirmed delivery. Operations must confirm availability, and Sales owns the customer-facing commitment.
L4: “Reduce effort” does not identify the output or show whether the task succeeded. A card needs an inspectable result, with effort recorded as a later measure.
Guided practice — Completed Service card

| Field | Completed example |
| --- | --- |
| Opportunity ID | EX-OPP-SVC-001 |
| Affected team | Service; specialist reviewer for bespoke cases |
| Trigger | A new returns-information enquiry |
| Task | Find current guidance and prepare an information response |
| Expected result | Source-linked draft or an explicit specialist/clarification route |
| Evidence | EX-EV-SVC-001; EX-DOC-SVC-001 |
| Work pattern and mechanism | Knowledge retrieval and document handling; approved FAQ/template or retrieval-assisted drafting |
| Owner and review | Service Lead reviews customer-facing content |
| Exception and boundary | Bespoke items go to specialist review; missing item type requires clarification; no automatic eligibility decision |
| Alternatives | Current FAQ with standard response templates; source-grounded retrieval and drafting assistance |
| Proposed measure | Correct guide use, correct routing, unsupported claims and total handling/review effort |
| Unknowns | Handling time, guide upkeep effort and whether assistance improves the overall task |
A response may explain how to submit a standard-item request. It must not confirm eligibility without the required review.
Guided practice — Completed Finance card

| Field | Completed example |
| --- | --- |
| Opportunity ID | EX-OPP-FIN-001 |
| Affected team | Finance; receiving team may supply missing evidence |
| Trigger | An invoice reaches evidence checking |
| Task | Match its purchase-order reference to approval and receiving records |
| Expected result | Matched evidence summary or a specific missing-evidence exception |
| Evidence | EX-EV-FIN-001; EX-DOC-FIN-001 |
| Work pattern and mechanism | Document handling and cross-app lookup; checklist/rules or approved integration |
| Owner and review | Finance Lead owns payment review |
| Exception and boundary | Missing receiving entry is reported as missing evidence; no payment approval or supplier changes |
| Alternatives | Standard evidence checklist with source links; automated matching across authorised records |
| Proposed measure | Correct reference matches, correctly identified exceptions and total checking effort |
| Unknowns | Interface availability, complete record quality and time/cost effects |
For INV-17, the correct output is:
PO-88 is recorded as approved. No matching receiving entry was found in the supplied register. Finance must resolve the evidence gap before completing payment review.
It should not say that delivery never occurred.
Guided practice — Completed HR card

| Field | Completed example |
| --- | --- |
| Opportunity ID | EX-OPP-HR-001 |
| Affected team | HR and the role manager |
| Trigger | A role induction request arrives |
| Task | Prepare the approved role checklist and identify missing scheduling inputs |
| Expected result | Draft checklist containing orientation, role training, equipment request and safety briefing; missing start date flagged |
| Evidence | EX-EV-HR-001; EX-DOC-HR-001 |
| Work pattern and mechanism | Document handling and knowledge retrieval; role template or approved-guide drafting assistance |
| Owner and review | HR accepts the checklist and confirms scheduling |
| Exception and boundary | Missing date requires clarification; obsolete guidance and unapproved personal notes are excluded |
| Alternatives | Role-specific template; source-grounded checklist drafting |
| Proposed measure | Correct checklist items, missing-input detection, obsolete-source use and review effort |
| Unknowns | Wider role coverage, guide maintenance and actual preparation effort |
The draft can be useful without a start date. It cannot establish a schedule by guessing.
These examples are not the only valid cards. A purely rules-based Finance check or a non-AI HR template is acceptable when its task and boundary are clear.
Independent challenge — Completed variant card

| Field | Completed example |
| --- | --- |
| Parent opportunity and variant | MSP-OPP-002; CH03-C1 |
| Affected team | Sales; Operations for availability confirmation |
| Trigger | Enquiry MSP-ENQ-451 requires an internal brief |
| Task | Organise the request and available approved catalogue fact |
| Expected result | Brief preserving 25 BF-10 units and requested date, with stock, price and delivery marked unconfirmed |
| Evidence | Enquiry input and approved MSP-KNOW-001 |
| Owner and review | Sales Lead accepts the brief; Operations supplies availability confirmation |
| Boundary | Internal output only; no destination write or customer quotation issuance |
| Exception | Missing approved stock, price and delivery evidence; obsolete note cannot supply a promise |
| Proposed measure | Request preservation, explicit unknowns, source correctness and review effort |
| Readiness questions | Can approved current stock/pricing/delivery evidence be supplied? Can any required write action be authorised and owned? |
An acceptable brief is:
The customer requests 25 BF-10 units for delivery on 16 October 2026. The approved catalogue identifies BF-10 as a 10 mm brass fitting. Current stock, price and delivery confirmation are not supplied in the permitted packet. Sales and Operations must resolve these points before a customer-facing quotation is accepted.
Option comparison

| Option | Fit to the supplied scope | Limitation |
| --- | --- | --- |
| Standard internal template | Strong starting point for a short, predictable set of fields and unknowns | A person must populate and check it |
| Generative assistance | May help if incoming wording varies substantially | Needs review and cannot supply missing commercial facts |
Automatic quotation issuance is unsupported because essential information is absent and destination write permission is not granted. The obsolete note cannot justify the requested-date guarantee.
This is a variant recommendation, not a change to the main-case decision.
Understanding questions
1. Work patterns describe the business task. Mechanisms describe how a solution performs it. Document handling may use rules or generative assistance; cross-app work may use integration.
2. A form may collect structured required fields directly, removing interpretation and extraction work. Its suitability depends on customer behaviour and the intake process.
3. The register may be incomplete or delayed. The evidence supports “no matching entry found”, not a conclusion about whether goods arrived.
4. A template may solve predictable structure with less complexity. AI should demonstrate useful improvement in variable-language work after review effort is included.
5. The claim overlaps the two-minute organisation/checking activity in opportunities 001 and 002. Eight claimed minutes exceed the six distinct baseline preparation minutes, and no savings have been observed.
6. A backlog entry records a candidate and its next assessment. Implementation approval requires a justified choice, readiness, ownership, costs and an appropriate leadership decision.
10. Chapter recap and next step
Opportunity identification turns a recurring issue into a specific task with a trigger, team and inspectable result. It keeps evidence, ownership and uncertainty visible.
Document handling, retrieval, decision support and cross-app work can appear together. Their presence does not automatically justify AI or an agent. A simpler process, template or shared record may be the stronger option.
“I can…” checklist
- I can turn a recurring issue into a bounded use-case statement.
- I can name the affected team, task, trigger and expected result.
- I can distinguish document handling, retrieval, decision support and cross-app work.
- I can preserve missing evidence as an exception.
- I can compare simpler alternatives with AI assistance.
- I can identify overlapping baseline activities.
- I can record a candidate without presenting it as approved.
Your project artifacts are:
- MSP_Use_Case_Cards_v0_1.md
- MSP_Opportunity_Backlog_v0_1.md
- MSP_Case_Assumptions_v0_3.md
For assumptions version 0.3, retain MSP-A-001 through MSP-A-007 and add:

| Assumption ID | Added assumption | Status |
| --- | --- | --- |
| MSP-A-008 | The selected four-case preparation breakdown represents the weekly mix | Unconfirmed |
| MSP-A-009 | Combined changes can remove the entire six-minute preparation component | Untested; review and remaining work must be measured |
| MSP-A-010 | The small knowledge packet covers the wider product catalogue | Unconfirmed; it only supplies BF-10 facts |
Chapter 4, Data and Organisational Readiness, will examine source quality, ownership, access, integrations, licences, process stability, support and stakeholder readiness for these candidates.
11. Glossary and further reading
Glossary

| Term | Meaning |
| --- | --- |
| Cross-app work | Reading or moving information across applications |
| Decision support | Organising evidence or options to help a responsible person decide |
| Document handling | Extracting, checking, sorting or transforming supplied documents and messages |
| Expected result | An output or state that can be inspected |
| Knowledge retrieval | Finding relevant information in a defined source collection |
| Opportunity | A candidate improvement requiring further assessment |
| Opportunity backlog | A record of candidate improvements and their status |
| Semantic search | Searching by meaning rather than only exact words |
| Source authority | The status, ownership and suitability that make a source appropriate for a claim |
| Use-case card | A compact description of a triggered task, affected team and expected result |
Further reading
Official documentation was accessed for the retrieval and grounding concepts cited here. The business examples are synthetic, and no product execution is claimed. Meridian’s particular source connections, tool availability, licences, permissions and deployment requirements remain unverified.
1. OpenAI documentation — File search. Describes semantic and keyword search over configured knowledge bases of uploaded files. Useful for understanding a concrete retrieval capability without assuming that all organisational content is connected.  
https://developers.openai.com/api/docs/guides/tools-file-search
2. Anthropic documentation — Reduce hallucinations. Explains grounding, uncertainty and verification, including why these measures do not eliminate unsupported output.  
https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
[1]: https://developers.openai.com/api/docs/guides/tools-file-search
[2]: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
