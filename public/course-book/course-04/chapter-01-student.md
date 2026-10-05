# AI and Automation Literacy

## 1. What you will learn

A business request such as “automate our quotations” contains several different problems. Someone may be copying information between systems, checking required fields, interpreting an unclear enquiry or deciding which information to investigate next. These tasks do not necessarily need the same solution.

In this chapter, you will learn to distinguish four capabilities:

- Rules: apply predefined conditions and actions.
- Integrations: exchange information between systems.
- Generative assistance: produce or transform content for a defined purpose.
- Agents: use a model to choose steps and tools toward a goal within an agreed boundary.

By the end, you should be able to classify a business task, explain your classification, identify one practical limitation and describe where a person remains responsible. You will also recognise when process simplification is a better starting point than adding technology.

### What you need

You do not need coding skills or a product account. You need only the ability to describe a task: what starts it, what information it uses and what result is required. All exercise information is supplied in this chapter.

The fictional Meridian Supply management team is assessing its enquiry-to-quotation process. This scenario is synthetic. You may replace it with a permission-cleared company case, keeping facts and assumptions clearly separated.

### Your contribution to the course project

Your course project is a Business Automation Pilot Proposal. The final proposal will include an executive proposal, current-state and future-state maps, a baseline and assumptions register, solution options, a value/cost model, data and ownership requirements, a pilot design, an adoption plan and a leadership decision.

This chapter contributes your first Task Classification Register and Capability Brief. These explain what kind of help a process needs before you select a product or estimate returns.

The workshop develops your ability to assess and propose an opportunity. It does not establish production implementation competence or guarantee a financial return.

## 2. Lessons
### Lesson 1 — Distinguish a fixed decision from a connection between systems

A trigger is the event that starts work. A new enquiry, an approved quotation or a scheduled daily check can be a trigger. Microsoft’s Power Automate documentation uses this term for the event that starts a cloud flow.1

A rule states what should happen when a condition is met:

If quantity is missing, mark the enquiry “Needs clarification”.

Rules are useful when the condition and permitted action can be stated precisely. They can validate fields, calculate values, route records and flag exceptions. With the same validated inputs and rule version, a deterministic rule should produce the same result.

That consistency does not prove that the result is appropriate. An incorrect rule applies the wrong instruction consistently.

An integration connects systems so that information can be read, copied or updated. A connector is a packaged connection to a service. An API, or application programming interface, is a defined way for software to request information or actions from another system.

Integration solves a movement problem. It does not automatically solve a meaning problem. Copying an incorrect product code faithfully into another system still leaves an incorrect product code.

Worked demonstration: validation and record creation

For this demonstration, Meridian uses these synthetic rules:

- Quantity must be a positive whole number.
- The only recognised product code in the supplied catalogue is BF-10.
- A requested delivery date must be supplied.
- Missing or invalid values require clarification; they must not be guessed.

An enquiry contains product BF-10, quantity 0 and requested delivery date 2026-10-12.

The rule checks quantity and returns:

Needs clarification — provide a positive whole-number quantity.

It should not change 0 to 1. That would alter the customer’s request.

Now consider a valid enquiry:

| Source field | Supplied value | Intended destination field |
| --- | --- | --- |
| Business enquiry ID | MSP-ENQ-001 | External enquiry reference |
| Product code | BF-10 | Requested product |
| Quantity | 25 units | Requested quantity |
| Requested delivery date | 2026-10-12 | Customer requested date |

Copying these fields into a customer relationship management system, or CRM, is primarily an integration task. Validation rules may run before the transfer.

Suppose the destination creates illustrative record ID CRM-9001. That identifier belongs to the destination system. It is different from the business enquiry ID MSP-ENQ-001, the opportunity ID MSP-OPP-001 and any pilot ID.

A common mistake is to replace the business reference with the destination-generated ID. Keeping both allows you to reconcile records across systems and investigate duplicate transfers.

When to choose each

Choose rules when you can specify the decision. Choose integration when you need reliable movement between approved sources and destinations. Many practical solutions combine both.

Check L1: An enquiry has no quantity. Why is “default to one unit” a poor rule unless the process owner has explicitly authorised it?

### Lesson 2 — Use generative assistance for language work without confusing fluency with evidence

Generative AI produces content from instructions and context. A language model can draft a response, summarise an email, extract candidate fields or suggest questions.

These capabilities are valuable when wording varies. Customers do not always use the same format or vocabulary. A model may help turn a long message into a concise internal brief.

However, a model can produce plausible statements that are unsupported or incorrect. This is often called a hallucination. Official guidance recommends grounding answers in supplied evidence, allowing uncertainty and checking important claims; these methods reduce errors but do not eliminate them.2

A useful distinction is:

- Generation: proposes wording or an interpretation.
- Validation: checks required fields, rules and source support.
- Approval: accepts responsibility for using or releasing the result.

A readable draft has passed only the first of these.

Worked demonstration: a facts-only enquiry brief

The following inputs are complete for this demonstration.

Customer message from buyer@example.com:

Please quote for 25 BF-10 fittings. We would like delivery on 12 October 2026. Please confirm whether that date is possible.

Approved synthetic sources:

| Source | Supplied fact | What it does not establish |
| --- | --- | --- |
| Catalogue extract | BF-10 is a 10 mm brass fitting | Price or delivery commitment |
| Stock snapshot | 40 units are listed at the snapshot time | Current reservation or future availability |
| Delivery note | Delivery requires Operations confirmation | A confirmed delivery date |

A suitable instruction is:

Prepare an internal enquiry brief using only the supplied message and sources.

Separate customer requests from confirmed facts.

Do not invent prices, stock reservations or delivery commitments.

Identify any information that still requires confirmation.

An illustrative acceptable brief is:

The customer requests 25 units of BF-10, a 10 mm brass fitting, with delivery requested for 12 October 2026. The supplied stock snapshot lists 40 units. Delivery on the requested date remains unconfirmed. Operations must check availability and delivery before Sales issues a quotation. No price was supplied.

This is a paper example of an acceptable output, not an observed model result.

The sentence “We can deliver on 12 October” would be a mistake. It converts a customer request into a company commitment without evidence.

Generative assistance is most useful here for organising language. A conventional rule can still check whether quantity is positive. An integration can retrieve approved source information. Sales remains responsible for the customer-facing quotation.

Check L2: A generated brief is grammatically excellent. What two things must you still check before relying on it?

### Lesson 3 — Recognise an agent by who chooses the next step

An agent, as used in this workshop, is a system in which a model chooses steps or tool use toward a goal, considers the returned information and decides what to do next.

A tool is a capability available to the system, such as reading a catalogue or looking up stock. Tool access must be configured; a model’s request to use a tool is not evidence that the operation succeeded. Official tool-use documentation distinguishes the model’s tool request from execution and the returned result.3

The key difference is not the number of steps. A workflow that always reads a catalogue, checks stock and creates a draft in that fixed order is still a predefined workflow. Anthropic’s architectural guidance distinguishes predefined workflows from agents that dynamically direct their processes and tool use.4 Product terminology may vary, so ask how the system actually behaves.

Worked demonstration: investigate an availability problem

Use these supplied facts:

- The customer requests 60 units of BF-10.
- The catalogue identifies BF-10 as a 10 mm brass fitting.
- The approved stock snapshot lists 40 units.
- The approved substitution guide states: “No approved substitute for BF-10.”
- Available tools are read-only catalogue, stock and substitution lookups.
- The system may make at most four lookups.
- It may prepare an internal brief, but cannot change records, promise delivery or send messages.

An illustrative agent sequence could be:

1. Read the catalogue to identify the item.
2. Choose a stock lookup because availability matters.
3. After finding only 40 units, choose the substitution guide.
4. After finding no approved substitute, stop and refer the shortage to Operations.

The important feature is the choice of the substitution lookup in response to the stock result. Another enquiry might not need that step.

The final brief should say that the requested quantity exceeds the supplied stock snapshot and that no approved substitute is listed. It should not invent a replenishment date.

Agents can help when investigation paths genuinely vary. Their limitations include incorrect tool choices, misinterpretation of results and compounded errors across steps. Additional calls can also add time and usage cost.

A boundary makes the proposal assessable: which goal, which tools, which data, which actions and which stopping condition? “Handle everything” is not a useful boundary.

Check L3: A system makes four model calls in a fixed sequence. Does that alone make it an agent? Explain.

### Lesson 4 — Match the capability to the problem before choosing technology

Classification describes how work might be performed. It does not prove that the task is worth automating.

Start by asking whether the process can be simplified. If Sales copies the same enquiry into two spreadsheets because nobody has agreed which record is authoritative, connecting both spreadsheets may preserve the duplication. Agreeing one record of origin may remove the work.

A baseline describes current performance using evidence: completed volume, staff effort, rework, elapsed time or another relevant measure. Staff effort is time spent working. Elapsed time includes waiting. Reducing typing does not necessarily remove an Operations queue.

Compare plausible options against the actual problem:

| Problem | Plausible first option | Important remaining limitation |
| --- | --- | --- |
| Required fields are often absent | Simplify intake and use validation rules | Customers may still need help clarifying requests |
| Staff rekey approved data | Establish one source and integrate it with the destination | Field mappings, permissions and duplicate handling still matter |
| Enquiries use varied language | Use a template or source-grounded generative brief | A person must verify meaning and unsupported claims |
| Investigation paths vary | Consider a bounded agent after simpler options | Tool choices and stopping behaviour need evaluation |

This is a qualitative comparison, not a scored ranking. It identifies questions to investigate rather than manufacturing a precise-looking winner.

A solution’s business cost extends beyond initial setup. Depending on the option, assess implementation, licences, model usage, human review, support and maintenance. Someone must update rules and mappings when products or processes change.

Released capacity means staff time becomes available for other work. Cash savings means an actual expense decreases. Saving an hour of typing does not automatically reduce payroll by an hour.

A pilot is a bounded test of a proposed change. It needs an owner, a baseline, representative cases, measures, success criteria and stop criteria. A useful result supports a proceed, revise or defer decision. Chapter 8 develops this design in detail; here you need enough literacy to recognise what a credible test would contain.

Check L4: If an opportunity removes some enquiry preparation work, why should you avoid claiming that it saves all the time spent on the enquiry-to-quotation process?

## 3. Visual explanation — How capabilities can work together

The diagram shows a proposed assistance pattern. It is a conceptual design, not a configured product workflow.

Transition map — each row is one arrow in the supplied flowchart.

| From | Route or condition | To |
| --- | --- | --- |
| Customer enquiry | Continue | Permission and required-field checks: rules |
| Permission and required-field checks: rules | Missing, invalid or not permitted | Exception for a person |
| Permission and required-field checks: rules | Permitted and valid | Read approved sources: integration |
| Read approved sources: integration | Continue | Prepare internal brief: generative assistance |
| Prepare internal brief: generative assistance | Continue | Sales reviews against sources |
| Sales reviews against sources | Correction needed | Exception for a person |
| Sales reviews against sources | Accepted | Continue the human-owned quotation process |

In plain language, the system first checks whether it may use the information and whether required fields are valid. Exceptions go to a person. Valid cases can use approved connections to obtain source facts. Generative assistance then organises those facts into a brief, which Sales checks.

The diagram explains why these labels are not mutually exclusive. Rules, integrations and generative assistance can contribute to one workflow.

An agent would change how some steps are selected—for example, choosing which approved source to investigate next. It would not remove the need for permission checks, reliable sources or decision ownership.

## 4. Worked case — Meridian’s first capability assessment

Case inputs and evidence

Meridian’s synthetic process begins with a customer enquiry. Sales records the request, Operations checks product and availability information, and Sales prepares and issues the quotation. Missing information returns to Sales or the customer for clarification.

The following sample figures are supplied as scenario evidence, not measurements from a real company:

| Baseline item | Supplied value | Evidence represented in the scenario |
| --- | --- | --- |
| Completed enquiries in one reference week | 120 enquiries | Completed-case register |
| Initial handling effort | 18 staff minutes per completed enquiry | Combined Sales and Operations time log |
| Preparation component within initial handling | 6 of the 18 minutes | Time spent organising and checking enquiry information |
| Additional rework | 24 enquiries × 6 staff minutes | Correction log, separate from initial handling |
| Rework categories | 14 missing quantity/date; 6 copied-code errors; 4 outdated-stock checks | Categorised correction records |
| Handoffs | Sales → Operations → Sales | Supplied process description |

The 120 figure describes completed cases. Arrivals, unfinished records and waiting durations are not supplied. You cannot derive incoming demand or response time from this baseline.

Initial effort:

120 enquiries/week × 18 minutes/enquiry = 2,160 staff minutes/week

Additional rework:

24 reworked enquiries/week × 6 minutes/reworked enquiry = 144 staff minutes/week

Total:

(2,160 + 144) minutes/week ÷ 60 minutes/hour = 38.4 staff hours/week

The preparation component is already inside the 18 minutes. Adding it again would double count effort.

Small reference packet

The team also supplies six independent synthetic cases for an offline concept test. The same 40-unit stock snapshot applies separately to each case; these cases do not reserve or consume stock.

The catalogue and substitution facts from the lessons remain unchanged. No price or confirmed delivery date is supplied.

| Enquiry ID | Product | Quantity | Requested date | Source access permitted? | Manual preparation effort |
| --- | --- | --- | --- | --- | --- |
| MSP-ENQ-001 | BF-10 | 25 units | 2026-10-12 | Yes | 6 minutes |
| MSP-ENQ-002 | BF-10 | 10 units | 2026-10-13 | Yes | 5 minutes |
| MSP-ENQ-003 | BF-10 | Missing | 2026-10-12 | Yes | 7 minutes |
| MSP-ENQ-004 | XX-99 | 8 units | 2026-10-12 | Yes | 8 minutes |
| MSP-ENQ-005 | BF-10 | 4 units | 2026-10-12 | No | 4 minutes |
| MSP-ENQ-006 | BF-10 | 60 units | 2026-10-12 | Yes | 6 minutes |

For case 005, the operational source is not authorised for use. Knowing the request fields does not authorise source enrichment. Treat the denied access as an exception.

The packet’s manual effort is:

6 + 5 + 7 + 8 + 4 + 6 = 36 staff minutes

36 minutes ÷ 6 cases = 6 staff minutes/case

This small packet is deliberately exception-rich. Its results must not be extrapolated to the weekly cohort without examining case mix.

### Step 1: separate the problems

The team identifies three preliminary opportunities:

| Opportunity ID | Problem | Candidate capability | Why |
| --- | --- | --- | --- |
| MSP-OPP-001 | Missing or invalid required fields | Rules and clearer intake | The acceptance conditions can be stated explicitly |
| MSP-OPP-002 | Time spent organising varied enquiry wording | Generative assistance or a standard template | The work concerns language and structure |
| MSP-OPP-003 | Repeated entry of approved enquiry fields | Process simplification, then integration if needed | The work concerns duplication and data movement |

These are discovery candidates, not approved implementation projects.

### Step 2: complete the reference outcomes

| Enquiry ID | Correct reference outcome | Reason |
| --- | --- | --- |
| MSP-ENQ-001 | Prepare a facts-only brief for Sales review | Recognised product and valid request; delivery remains unconfirmed |
| MSP-ENQ-002 | Prepare a facts-only brief for Sales review | Same conditions, with a different quantity and requested date |
| MSP-ENQ-003 | Request quantity clarification | A required value is missing |
| MSP-ENQ-004 | Ask Sales to verify the product code | XX-99 is not in the supplied catalogue |
| MSP-ENQ-005 | Stop source enrichment and refer access to IT | Source use is not permitted |
| MSP-ENQ-006 | Refer availability to Operations | Requested quantity exceeds the snapshot; no approved substitute exists |

These outcomes are constructed reference answers. They are not observed automated performance.

### Step 3: record the capability decision

Completed artifact: MSP_Capability_Brief_v0_1.md

Assess intake simplification and validation first under MSP-OPP-001. Explore a standard template and source-grounded internal drafting under MSP-OPP-002. Investigate duplicated entry under MSP-OPP-003 before selecting an integration. The currently specified brief-preparation path does not require model-selected investigation, so an agent is not justified for this initial concept test. Sales owns brief acceptance and customer commitments; Operations owns availability confirmation; IT owns connection and access verification.

Finance validates effort and cost assumptions. The Sponsor owns the later investment decision. IT’s responsibility for a connection does not transfer Sales’ responsibility for quotation accuracy.

### Step 4: make the proposed test bounded

Illustrative preliminary test brief: MSP-PILOT-001 — proposed, not executed

| Element | Supplied preliminary design |
| --- | --- |
| Boundary | One offline round using the six-case packet; internal brief preparation only; no live writes, prices or customer messages |
| Owners | Sales Lead accountable; Operations supplies source facts; IT checks access requirements; Finance checks effort recording; Sponsor owns the decision |
| Baseline | Manual packet effort of 36 minutes; the six reference outcomes above define correctness |
| Cases | Two valid requests, missing quantity, unknown product, denied access and stock shortage |
| Measures | Correct outcome per case; unsupported statements per output; total staff effort including review and correction; completion of review and feedback by two proposed sales reviewers |
| Success criteria | Six of six correct outcomes; zero unsupported price/delivery claims or prohibited actions; total staff effort at most 30 minutes; both reviewers complete review and feedback |
| Stop criteria | Any attempted prohibited access/action, or any unsupported price/delivery commitment in a proposed brief |
| Decision rule | Proceed to broader pilot design if all criteria pass; revise if correctness and controls pass but effort/adoption targets fail; defer if a stop condition occurs until its cause is resolved |
| Result status | No candidate outputs or post-change timings have been observed |

This is a learning-scale test design. Chapter 8 will address representative sampling and stronger measurement.

A mistake and its correction

Mistake: “The assistant will save 38.4 hours each week.”

Correction: 38.4 hours is the total supplied weekly effort, including work outside brief preparation. The effect of a change is unknown. Even the 30-minute packet target is a target, not an observed result or cash saving.

Completed assumptions artifact: MSP_Case_Assumptions_v0_1.md

| Assumption ID | Statement | Status or next evidence needed |
| --- | --- | --- |
| MSP-A-001 | Weekly figures describe the supplied synthetic completed-case cohort | Scenario input; replace with company evidence when adapting |
| MSP-A-002 | Required product connections and write permissions are available | Unconfirmed; IT must assess in Chapter 4 |
| MSP-A-003 | A template or generated brief can reduce total effort including review | Untested; no savings claimed |
| MSP-A-004 | The six-case packet reflects the wider process mix | Not established; broader sampling is required |

## 5. Try it yourself — Guided practice

Learning goal

Classify sample business tasks by their primary capability and record one meaningful limitation for each.

Requirements and access

Use paper or a local worksheet. All inputs are synthetic. No product access is required. This exercise demonstrates business reasoning; it cannot demonstrate connector behaviour, model reliability or live permissions.

You may work individually. In a group, take the Sponsor, Sales Lead, Finance Lead, Operations Lead and IT Lead perspectives. Individually, consider those same perspectives when assigning ownership.

Complete task inputs

Classify the mechanism described, rather than guessing a different implementation.

| Task ID | Requested task |
| --- | --- |
| MSP-TASK-001 | In the existing enquiry record, flag quantity as invalid when it is missing, zero, negative or not a whole number |
| MSP-TASK-002 | Copy a validated enquiry’s business ID, product, quantity and requested date from an intake system into a CRM draft record |
| MSP-TASK-003 | Turn a supplied customer email and approved source extracts into a concise internal brief; do not select or operate tools |
| MSP-TASK-004 | Investigate an availability exception by choosing among approved catalogue, stock and substitution lookups in response to their results; stop after four lookups |
| MSP-TASK-005 | Set an internal reminder flag when the supplied “business days since response” field exceeds two; the example field value is three |
| MSP-TASK-006 | Copy an approved quotation PDF from document storage to the matching CRM record using the business quotation ID |
| MSP-TASK-007 | Suggest a clarification question from the supplied message “Need fittings for next week”; do not retrieve information or send the question |
| MSP-TASK-008 | Investigate conflicting internal status reports by choosing which approved read-only source to consult next, then produce an exception brief for a person |

Additional exception inputs

After classifying the tasks, write the permitted next action for each exception:

| Exception | Supplied condition |
| --- | --- |
| E1 — Invalid quantity | A new request contains quantity 0; no authorised default quantity exists |
| E2 — Missing product | A request says “Need fittings for next week”; no product code is supplied and the catalogue contains only BF-10 |
| E3 — Permission | Someone asks the drafting assistant to include private staff notes; those notes are not approved or supplied |
| E4 — Uncertain transfer | For task 002, the acknowledgement is lost. An authorised destination lookup finds CRM-9001 already linked to MSP-ENQ-001, with all transferred fields matching. The permitted recovery is to reconcile a matching existing record; creating a second record is not permitted |

Learner worksheet

Enter one primary capability. You may mention supporting capabilities in your explanation.

| Task ID | Primary capability | Why this mechanism fits | One specific limitation | Responsible role and boundary |
| --- | --- | --- | --- | --- |
| MSP-TASK-001 |  |  |  |  |
| MSP-TASK-002 |  |  |  |  |
| MSP-TASK-003 |  |  |  |  |
| MSP-TASK-004 |  |  |  |  |
| MSP-TASK-005 |  |  |  |  |
| MSP-TASK-006 |  |  |  |  |
| MSP-TASK-007 |  |  |  |  |
| MSP-TASK-008 |  |  |  |  |

Guided steps and expected intermediate results

1. Identify the required result. Is it a flag, a transferred record, drafted content or an investigation?
  **Expected result:** eight short descriptions of the intended output.
2. Identify how the result is obtained. Look for fixed conditions, data movement, content generation or model-selected steps.
  **Expected result:** one primary classification for every row, with supporting capabilities noted where useful.
3. State a limitation that could affect this task.
  **Expected result:** eight specific limitations. “Technology can fail” is too vague.
4. Assign ownership and an action boundary.
  **Expected result:** every row names a business owner or relevant operational role and a limit on action.
5. Resolve E1–E4.
  **Expected result:** four exception notes that preserve the request, respect access and prevent duplicate action.
Your final artifact is C04_CH01_Task_Classification_Register.md, containing the completed table and four exception notes.

Keep the synthetic final worksheet for your project. You can discard scratch copies after transferring your reasoning. No account or system cleanup is required.

## 6. Independent challenge

Use these changed conditions. They are exercise variants and do not overwrite Meridian’s main case records.

| Challenge ID | Complete changed input |
| --- | --- |
| MSP-CHAL-01 | Replace task 004 with a fixed path: read catalogue, read stock, then flag shortage if requested quantity exceeds the stock figure. No model chooses steps. Product is BF-10, quantity is 60 and stock is 40. |
| MSP-CHAL-02 | An enquiry contains BF-10, quantity 0 and requested date 2026-10-12. Source access is permitted. No default or quantity correction is authorised. |
| MSP-CHAL-03 | An enquiry requests 20 BF-10 units for 2026-10-09 and asks, “Can you promise that date?” The catalogue description is available, but the stock source is temporarily unavailable. No delivery confirmation or approved substitute is supplied. A person may investigate or prepare an internal brief stating the uncertainty. |

Deliverables

For each challenge, record:

1. A suitable primary capability for the next useful task.
2. Your reason and one limitation.
3. The permitted next action.
4. A statement that must not appear in the output.

Then write a short recommendation comparing a standard internal template with generative assistance for this initial scope. Include one unresolved assumption.

Observable success criteria

Your work should distinguish a fixed path from agentic choice, preserve missing or invalid values as exceptions, avoid unsupported promises and connect the recommendation to the specified work.

More than one classification can be valid if you define a different task boundary clearly. A different label is not enough; the explanation must show a different mechanism.

## 7. Common problems and recovery

| Symptom | Likely diagnosis | Correction | Verification |
| --- | --- | --- | --- |
| Every task is labelled “AI” | The desired outcome has been confused with the mechanism | Ask what performs the work: condition, connection, generation or model-selected investigation | Explain what would still function without a language model |
| A fluent brief changes a requested date into a promise | Customer wording has been treated as company evidence | Separate requested, confirmed and unknown information | Trace every commitment to an approved source |
| A required field receives a guessed value | Completion has been prioritised over accuracy | Retain the exception and request clarification | Confirm that no unauthorised default was introduced |
| A connection fails and staff immediately repeat the write | Failure to receive confirmation has been treated as proof that nothing happened | Check the destination using the business reference before an authorised retry | Confirm one matching record and reconcile its status |
| An assistant requests an unavailable or unauthorised source | Tool availability or permission has been assumed | Stop that lookup; refer access questions to IT and the data owner | Confirm authorisation before future use |
| An agent keeps investigating | The goal or stopping condition is unclear | Use a defined lookup limit and escalation condition | Confirm that the unresolved issue is handed to the named owner |
| Savings increase when the same activity appears in two worksheets | Overlapping effort has been counted twice | Mark which components are already included in baseline effort | Recalculate using non-overlapping activities |

Recovery does not always mean completing the task immediately. A correctly identified exception can be the correct output.

## 8. Check your understanding

1. A rule flags enquiries with a missing requested date. A model drafts a polite request for that date. What is the primary capability of each task?
2. A generated brief correctly repeats quantity but promises next-day delivery. The supplied sources contain no delivery commitment. What should happen, and why?
3. IT confirms that a connection can read CRM records but cannot create them. Can Meridian claim that task 002 is ready? Explain.
4. The weekly baseline contains 18 initial minutes per enquiry, including six preparation minutes. What is wrong with calculating initial effort as 120 × (18 + 6)?
5. What can the supplied 120 completed enquiries tell you, and what can they not tell you about arrivals and customer waiting?
6. Who should own acceptance of a customer-facing quotation, and what responsibilities remain with Operations, IT, Finance and the Sponsor?

## 9. Solutions and explanations

Lesson checks

L1: Defaulting to one changes the customer’s request without evidence. A technically valid quantity may still be commercially incorrect. The permitted result is a missing-data exception unless an authorised business rule establishes a default.

L2: Check that the brief preserves the customer’s meaning and that factual claims are supported by approved sources. Also apply the required-field rules. Grammar does not establish factual correctness or permission to make commitments.

L3: No. A fixed sequence remains a predefined workflow even if it contains several model calls. Under this chapter’s definition, agentic behaviour involves model-selected steps or tool use in response to results.

L4: The baseline includes activities outside preparation. The change may also introduce review and correction effort. Only measured, non-overlapping reductions can support a time-saving claim, and released time is not automatically cash saving.

### Guided practice — Completed classification register

| Task ID | Primary capability | Why this mechanism fits | One specific limitation | Responsible role and boundary |
| --- | --- | --- | --- | --- |
| MSP-TASK-001 | Rules | Explicit conditions determine the flag | Validating quantity does not confirm that the customer intended it | Sales owns intake rules; flag rather than alter the request |
| MSP-TASK-002 | Integrations | Fields move between two systems | A wrong mapping or duplicate transfer can create an incorrect record | IT owns connection reliability; Sales owns field meaning |
| MSP-TASK-003 | Generative assistance | Supplied content is transformed into a brief | It can omit an important request or add an unsupported statement | Sales checks the brief; no customer sending |
| MSP-TASK-004 | Agents | The model chooses subsequent lookups from returned results | It can select an inappropriate source or misread availability | Operations owns availability interpretation; read-only and four-lookups maximum |
| MSP-TASK-005 | Rules | A supplied numeric field is compared with a fixed threshold | An incorrect business-day field causes an incorrect flag | Sales owns the reminder condition; internal flag only |
| MSP-TASK-006 | Integrations | A document moves between approved systems using an identifier | An incorrect business-ID match can attach the wrong document | IT owns transfer controls; Sales confirms the approved document |
| MSP-TASK-007 | Generative assistance | The task proposes wording from supplied text | It cannot establish which fitting the customer means from that message alone | Sales reviews and sends any clarification |
| MSP-TASK-008 | Agents | The model chooses sources to investigate a conflict | Choosing one source does not prove that it is authoritative | Operations owns resolution; read-only investigation and human acceptance |

Supporting rules can validate IDs during integration. Generative assistance can produce an agent’s final brief. Those supporting capabilities do not change the main mechanism described in the task.

For task 005, three business days exceeds the two-day threshold, so the expected rule result is reminder flag set. No timestamp calculation is needed because the elapsed business-day field is supplied.

Exception notes

- E1: Mark the quantity invalid and ask for a positive whole number. Do not substitute one or another value.
- E2: Ask the customer to identify the fitting or product code. The catalogue containing only BF-10 does not prove that BF-10 is the intended item.
- E3: Exclude the private notes and do not attempt to retrieve them. Drafting can use the approved customer message. Refer any proposed access change to the appropriate owner.
- E4: Reconcile the transfer with existing destination record CRM-9001. Preserve its link to MSP-ENQ-001; do not create a duplicate. The supplied lookup establishes that the matching write already occurred.

### Independent challenge — Completed example

| Challenge ID | Primary capability and reason | Limitation | Permitted next action | Statement to exclude |
| --- | --- | --- | --- | --- |
| MSP-CHAL-01 | Rules, supported by integrations: the path and shortage condition are predefined | The stock snapshot may not establish current availability | Flag shortage because 60 exceeds 40; refer to Operations | “An agent autonomously resolved availability” |
| MSP-CHAL-02 | Rules: quantity zero fails the explicit validation condition | Validation cannot supply the customer’s intended quantity | Request quantity clarification | “Quantity corrected to one” |
| MSP-CHAL-03 | Generative assistance for an internal uncertainty brief | Available sources cannot confirm stock or delivery | State the request and catalogue fact; mark stock and delivery unconfirmed; refer to Operations | “Delivery on 9 October is guaranteed” |

For challenge 01, integration is also an acceptable primary label if your defined task is the catalogue/stock transfer rather than the shortage decision. Calling it an agent is not supported because no model chooses the path.

For challenge 03, a standard template is equally acceptable if you define the task as filling known fields and uncertainty flags. An agent is unnecessary merely because a source is unavailable.

Completed recommendation:

Start with a standard internal template and explicit validation for the current limited scope. This keeps required fields and uncertainty visible. Compare generative assistance where variable wording creates meaningful preparation work, while retaining Sales review. Do not propose an agent solely to handle the supplied stock-source outage; the permitted response is already clear. An unresolved assumption is whether drafting reduces total effort after review and correction. Test that assumption against the manual reference packet before claiming value.

Understanding questions

1. Missing-date flag: rules. Polite request draft: generative assistance. The first applies an explicit condition; the second produces wording.
2. Reject or correct the unsupported promise before acceptance. Keep the requested quantity if supported, but mark delivery unconfirmed. Correct content elsewhere does not validate the delivery claim.
3. No. Task 002 requires creation in the destination. Read permission does not establish write permission. IT must assess the required authorised capability.
4. The six preparation minutes are counted twice. Correct initial effort is 120 × 18 = 2,160 minutes, not 2,880 minutes. Additional supplied rework brings the total to 2,304 minutes, or 38.4 hours.
5. The figure establishes supplied completed-case volume for the reference week. It does not establish arrivals, backlog or waiting duration. Unfinished cases could contain long waits that are absent from completed-case measures.
6. Sales owns customer-facing quotation acceptance in this scenario. Operations confirms availability; IT owns technical access and connection assessment; Finance checks value/cost assumptions; the Sponsor owns the investment decision. Technical operation and commercial accountability are different responsibilities.

## 10. Chapter recap and next step

You can now distinguish a specified decision, information movement, generated content and model-directed investigation. A process may combine these capabilities, but each should solve an identified problem.

The first useful decision is often to simplify the process or clarify its rules. The value of a proposed capability remains an evidence question: what work changes, what new effort appears and what results can be measured?

“I can…” checklist

- I can classify a task and explain its primary mechanism.
- I can give a limitation specific to that task.
- I can distinguish a generated draft from a verified fact or successful action.
- I can identify a fixed workflow that does not require an agent.
- I can preserve missing data and permission issues as exceptions.
- I can distinguish released capacity from cash savings.
- I can name the person responsible for the business result.

Your project evidence from this chapter is the completed Task Classification Register, Capability Brief and initial assumptions register. The worked test brief is a proposed example, not a pilot result.

Chapter 2, Process Discovery and Problem Framing, builds on these classifications. You will examine triggers, roles, handoffs, decisions, queues, rework, exceptions and customer impact, marking facts separately from assumptions.

## 11. Glossary and further reading

Glossary

| Term | Meaning |
| --- | --- |
| Agent | A system in which a model selects steps or tools toward a goal within a defined boundary |
| API | A defined interface through which software requests information or actions |
| Baseline | Evidence describing performance before a proposed change |
| Cash saving | An actual reduction in expenditure |
| Connector | A packaged connection to a service or system |
| CRM | Customer relationship management system |
| Deterministic rule | A specified instruction that gives the same result for the same validated inputs and rule version |
| Generative assistance | Model-produced content or transformation used for a defined task |
| Hallucination | Plausible model output that is incorrect or unsupported |
| Integration | A connection that exchanges information or actions between systems |
| Released capacity | Staff time made available for other work |
| Tool | A capability available to a system, such as an approved lookup |
| Trigger | An event that starts work |
| Workflow | An organised sequence of tasks, conditions and actions |

Further reading

The official pages below were accessed for the concepts cited in this chapter. No product was executed. Meridian’s particular connectors, editions, licences, model/tool availability, permissions and deployment-region dependencies remain unverified.

1. Microsoft Learn — Triggers in Power Automate. Explains event, manual and scheduled triggers. Useful for recognising how automation starts.

https://learn.microsoft.com/en-us/power-automate/triggers-introduction

2. Anthropic documentation — Reduce hallucinations. Explains uncertainty, grounding and verification, including why mitigation does not eliminate errors.

https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations

3. Anthropic documentation — Tool use with Claude. Explains model tool requests, execution and returned results. Useful for distinguishing requested actions from completed actions.

https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview

4. Anthropic — Building effective agents. Provides the architectural distinction between predefined workflows and dynamically directed agents. Use it for conceptual comparison rather than as a current product configuration checklist.

https://www.anthropic.com/engineering/building-effective-agents

[1]: https://learn.microsoft.com/en-us/power-automate/triggers-introduction

[2]: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations

[3]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview

[4]: https://www.anthropic.com/engineering/building-effective-agents
