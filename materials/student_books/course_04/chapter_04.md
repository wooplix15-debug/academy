---
course_id: "C04"
chapter_id: "C04-CH04"
chapter_number: 4
chapter_title: "Data and Organisational Readiness"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "partially_verified"
---

# Data and Organisational Readiness

1. What you will learn
A promising opportunity can still be unsuitable for a pilot if its information is unreliable, access is unclear, a required licence is missing or nobody owns the result.
Readiness means that the essential conditions for a proposed change are sufficiently understood and controlled for the next decision. Readiness is not the same as technical possibility. A tool may be able to perform a task while the organisation is not ready to use it safely or consistently.
In this chapter, you will learn to:
- Assess source quality, completeness, timeliness and authority.
- Distinguish data ownership, process ownership, system ownership and support ownership.
- Check access, permissions and permitted uses.
- Identify integration, licence and usage dependencies.
- Assess process stability and exception frequency.
- Evaluate support and stakeholder readiness.
- Use an evidence-based readiness matrix with weights, sensitivity and limitations.
- Decide whether to proceed, revise or defer a candidate for further assessment.
Your required practice is to score one process for data ownership, access, integration, licences, process stability and support readiness. Stakeholder readiness and source quality are included so that the score reflects the full decision context.
Prerequisites and continuity
Chapter 1 introduced capability types. Chapter 2 showed how to map a process and separate facts from assumptions. Chapter 3 turned recurring issues into use-case cards.
Meridian Supply’s candidate opportunities remain:

| Opportunity ID | Candidate |
| --- | --- |
| MSP-OPP-001 | Improve required-field completeness and validity |
| MSP-OPP-002 | Reduce effort spent organising varied enquiry wording |
| MSP-OPP-003 | Investigate repeated entry of approved enquiry information |
The Chapter 2 discovery packet remains synthetic. It showed four completed quotations, two open cases and a 50% first-pass handoff measure within that small packet. It did not establish a typical company-wide rate.
The Chapter 3 preparation packet showed four selected cases with six preparation minutes per case. Those six minutes included organisation, source lookup and rekeying. No savings have been observed.
Pilot MSP-PILOT-001 remains proposed and unexecuted. This chapter adds readiness evidence and does not convert a proposal into an implementation.
Your contribution to the course project
You will produce:
- A Readiness Evidence Register.
- A Readiness Scorecard.
- A Readiness Decision Note.
These artifacts support the Business Automation Pilot Proposal by showing whether the proposed process has the information, ownership, permissions, interfaces, capacity and support needed for a credible pilot.
A low score is not a failure. It identifies what must be clarified before a responsible decision can be made.
2. Lessons
Lesson 1 — Assess data quality before assessing an AI or automation option
A system can process information quickly while still producing a bad result if the source is incomplete, outdated, inconsistent or unauthorised.
Useful source-quality questions include:
1. Accuracy: Does the value represent the real-world item?
2. Completeness: Are the required fields present?
3. Consistency: Do related sources use the same meaning and format?
4. Timeliness: Is the information current enough for the decision?
5. Authority: Is the source approved for this purpose?
6. Coverage: Does the source cover the cases you intend to handle?
7. Lineage: Can you identify where the value came from and when it changed?
A source can be strong on one dimension and weak on another. Meridian’s stock snapshot illustrates this:

| Dimension | Supplied assessment |
| --- | --- |
| Accuracy at snapshot time | The snapshot is a stated record of listed stock at that time |
| Completeness | Reservations and future availability are not supplied |
| Timeliness | It is dated 2026-10-05 08:45; later status is not established |
| Authority | It is an approved snapshot for investigation, not a delivery commitment |
| Coverage | It covers BF-10 in the synthetic packet, not the entire catalogue |
| Lineage | The snapshot date is supplied; update ownership is not yet established |
The correct conclusion is not “the stock data is useless”. It is:
The snapshot is useful evidence of a listed quantity at a stated time, but it cannot by itself establish current availability or a delivery promise.
Missing data is not zero
Suppose a record has no requested delivery date. Its value is missing, not zero and not “today”. Replacing missing data with a default can create a false impression of completeness.
Similarly:
- No matching receiving record means “not found in the supplied register”.
- No access approval means “not authorised for this use”.
- No source update time means “timeliness is unknown”.
- No observed result means “not tested”, not “successful”.
Source quality and use-case fit
A source may be adequate for one task and inadequate for another.

| Source | Suitable use | Unsuitable conclusion |
| --- | --- | --- |
| Dated stock snapshot | Investigate whether a request may exceed listed stock | Promise a delivery date |
| Approved product catalogue | Identify product description and code | Establish current price unless price is included |
| Customer email | Capture the customer’s request | Treat the request as an internal commitment |
| Obsolete sales note | Identify a statement requiring review | Use it as current operating guidance |
| Completed-case register | Calculate a completed-case measure | Infer the waiting time of unfinished cases |
Check L1: What is the difference between a source being relevant and a source being authoritative?
Lesson 2 — Name ownership at several levels
The word owner is used for different responsibilities. A readiness assessment should not assign every responsibility to one person.

| Ownership type | Meaning | Meridian example |
| --- | --- | --- |
| Data owner | Accountable for whether a data set is appropriate, defined and governed | Operations Lead for availability information |
| Data steward | Maintains data quality and resolves specific data issues | A catalogue administrator checking product codes |
| Process owner | Accountable for how the work operates and what result it must produce | Sales Lead for enquiry intake and quotation preparation |
| System owner | Accountable for a system’s operation, configuration and access model | IT or the application owner |
| Decision owner | Accepts a business decision or commitment | Sales for a customer-facing quotation; Operations for availability confirmation |
| Support owner | Handles incidents, user questions, monitoring and maintenance | An agreed IT or process support owner |
A technical connection does not become the owner of the business result. IT may maintain a data transfer, but Sales still owns whether a customer-facing quotation is correct.
Worked example: assign ownership to a source
For the synthetic BF-10 information:

| Information | Data owner | Process owner using it | Decision owner | Open question |
| --- | --- | --- | --- | --- |
| Product description | Operations | Sales and Operations | Sales for description in a quotation | Who approves catalogue changes? |
| Stock snapshot | Operations | Operations | Operations for availability | How often is it refreshed? |
| Requested delivery date | Customer supplies it; Sales records it | Sales | Sales decides whether to communicate a commitment after Operations input | What evidence supports a confirmed date? |
| Source access permission | System or data owner according to the source | IT assesses connection; process team uses approved access | Named access approver is not yet supplied | Who grants and reviews access? |
A common mistake is to say, “IT owns the data because IT owns the system.” System administration and business meaning are different responsibilities.
Check L2: Who should decide whether a product can be promised for delivery: the person maintaining a data connection or the business owner of availability?
Lesson 3 — Treat access as a business control, not a technical convenience
Access answers whether a person or system is allowed to use a source for a defined purpose. It includes more than the ability to sign in.
Ask:
- Who or what is requesting access?
- Which records or fields can it read?
- Can it create, edit or delete anything?
- Is the intended use approved?
- Is the access limited to the minimum required?
- How is access reviewed or removed?
- What happens when access is denied or expires?
A user being able to open a file does not prove that an automation may copy its contents into another system. Read access does not imply write access. Write access does not imply permission to send customer communications.
Use least privilege as a design principle: provide only the access needed for the defined task. A read-only availability lookup may be enough for an internal brief. It does not need permission to change stock.
Worked example: access matrix

| Actor or system | Source | Read | Write | Permitted purpose | Status |
| --- | --- | --- | --- | --- | --- |
| Sales staff | Customer enquiry inbox | Yes | No | Read incoming requests | Supplied scenario condition |
| Sales intake record | Intake worksheet | Yes | Yes | Record and correct enquiry fields | Supplied scenario condition |
| Operations staff | Operations request application | Yes | Yes | Check and record operational results | Supplied scenario condition |
| Drafting assistant | Approved product extract | Proposed | No | Prepare an internal brief | Requires approval |
| Drafting assistant | Private staff notes | No | No | No permitted purpose | Prohibited |
| Integration connection | Operations request application | Proposed | Proposed | Transfer checked fields | Unconfirmed |
The final row is not a permission. It is a requirement to investigate.
The safest response to a denied access condition is to stop the affected action, preserve the case reference and refer the issue to the access owner. Do not use another person’s credentials or silently substitute an unapproved source.
If a product is used, its permission model and current configuration must be checked in the relevant official documentation and company environment. This chapter does not claim that a specific product grants any Meridian permission.
Check L3: Why can a read-only connection be suitable for a source-grounded brief but unsuitable for creating an Operations request?
Lesson 4 — Check integration, licence and usage dependencies
An integration dependency is a condition required for systems to exchange information or actions. Check:
- Source and destination systems.
- Trigger and action.
- Field mappings.
- Business identifier and destination identifier.
- Read and write permissions.
- Duplicate and retry behaviour.
- Error handling and reconciliation.
- API or connector availability.
- Monitoring and ownership.
Zoho Flow’s official FAQ describes a flow as a workflow in which an event triggers actions in other applications, and it describes one trigger with multiple sequential actions.1 This is a product-specific description, not a universal rule for every integration platform. Its same FAQ also notes that third-party API limits can affect executions.1
Microsoft’s Power Automate documentation describes connections as the means by which flows access data and actions in services, and explains that connections can be inspected, updated or deleted.2 The precise connection type, permissions and administration depend on the product, environment and organisation.
Identifiers and duplicate prevention
A safe handoff needs a stable business reference:
- Business enquiry ID: MSP-ENQ-401
- Opportunity ID: MSP-OPP-003
- Pilot ID: MSP-PILOT-001
- Destination-generated request ID: REQ-7401
Do not use REQ-7401 as a replacement for the business enquiry ID. If an acknowledgement is lost, reconcile by business reference before retrying. A matching record with matching fields may indicate that the first write succeeded.
Licence dependencies
A licence dependency is a required entitlement, subscription, credit, plan, connector, environment capability or usage allowance.
Assess at least:
- User or per-app access.
- Premium or custom connector requirements.
- Environment or tenant requirements.
- Storage and request capacity.
- AI or model usage allowance.
- Automation execution allowance.
- Development and test access.
- Support or service-level entitlement.
- Region, edition and contract restrictions.
Do not put a price in a business case until you know which edition, region, user count, volume and contract assumptions apply. Official licensing pages may change and may show list prices that do not apply to a particular organisation. For example, Microsoft’s current licensing FAQ describes multiple Power Apps, Power Automate and AI capacity models and directs readers to product-specific licensing material.3
A licence is not the same as permission. Someone may have a product licence but still lack access to a particular data source. Conversely, a data source may be accessible while the intended automation feature requires a separate entitlement.
Check L4: What information must be confirmed before a team claims that an integration is affordable and permitted?
Lesson 5 — Assess process stability, support readiness and stakeholder readiness
A process is stable enough for a pilot when its boundary, roles, inputs and expected outputs are sufficiently consistent to measure a change.
Stability does not mean that every case is identical. A stable process can have known exception routes. Instability appears when:
- Required fields change without an owner.
- Different teams use different meanings for the same field.
- The process boundary is disputed.
- The normal route changes every week.
- Exceptions are more common than routine cases.
- No one can state what a successful output looks like.
- A proposed change would be measured against a moving target.
A process with many exceptions may still be a good opportunity. It may require a narrower pilot or separate exception handling.
Support readiness
Support readiness asks whether the change can be operated after the initial demonstration:
- Who answers user questions?
- Who monitors failures?
- Who maintains rules, mappings, prompts or source documents?
- Who reviews access?
- Who records incidents?
- What is the manual fallback?
- How are users told about a process change?
- How often is performance reviewed?
A workflow without a support owner is not ready merely because it runs once.
Stakeholder readiness
Stakeholder readiness is the degree to which affected people understand the proposed change, agree on ownership and can participate in review.
A Sponsor’s enthusiasm is useful but insufficient. Readiness should include the people who:
- Supply source data.
- Perform the work.
- Receive exceptions.
- Approve customer or employee impact.
- Maintain systems.
- Validate costs and measures.
A stakeholder who disagrees may identify a missing requirement. Record the disagreement rather than treating it as resistance to be overcome.
Check L5: Why can a technically successful demonstration still be organisationally unready?
3. Visual explanation — Readiness is a chain of conditions
flowchart LR
    A[Useful business task] --> B[Source quality and authority]
    B --> C[Named owners]
    C --> D[Permitted access]
    D --> E[Interfaces and identifiers]
    E --> F[Licences and usage capacity]
    F --> G[Stable process boundary]
    G --> H[Support and stakeholder readiness]
    H --> I[Bounded pilot decision]
The diagram shows a dependency chain. If the source is not authoritative, a connection only moves unreliable information faster. If access is not permitted, technical feasibility does not create permission. If a licence is missing, the design may not be deployable. If nobody supports the change, a successful test may not survive normal use.
The chain is not strictly linear in every project. Some checks can occur in parallel. The learning point is that a missing condition should be made visible before a proceed decision.
Plain-text explanation:
Define the task, confirm the source, name the owners, verify access, check the systems and identifiers, confirm licences and capacity, assess process stability, assign support and engage stakeholders. Then decide whether the next step is a bounded pilot, more discovery or deferral.
4. Worked case — Meridian’s readiness assessment
New synthetic readiness evidence
The following records are added to Meridian’s case:

| Record ID | Supplied content |
| --- | --- |
| MSP-READ-001 | Data source register |
| MSP-READ-002 | Access and ownership register |
| MSP-READ-003 | Integration and identifier assessment |
| MSP-READ-004 | Licence and usage assessment |
| MSP-READ-005 | Stakeholder and support notes |
These records are synthetic. They are not observed company records.
Source register

| Source ID | Source | Owner | Sample or status | Quality observation |
| --- | --- | --- | --- | --- |
| MSP-SRC-001 | Sales enquiry messages | Sales Lead | Six discovery cases | Product and quantity issues appear in the supplied packet; coverage beyond it is unknown |
| MSP-SRC-002 | Product catalogue extract | Operations Lead | BF-10 entry supplied | Product description is available; wider catalogue freshness is not established |
| MSP-SRC-003 | Stock snapshot | Operations Lead | 40 BF-10 units at 2026-10-05 08:45 | Dated snapshot; reservations and future availability absent |
| MSP-SRC-004 | Operations request application | Operations Lead | Four selected cases | Destination fields are present; mapping governance is not established |
| MSP-SRC-005 | Sales intake worksheet | Sales Lead | Four selected cases | Manual rekeying is confirmed; one stable business reference is present in the supplied packet |
| MSP-SRC-006 | Approved substitution extract | Operations Lead | BF-10 has no approved substitute | Coverage outside BF-10 is unknown |
| MSP-SRC-007 | Obsolete sales note | Unconfirmed | Marked obsolete | Must not be used as current delivery authority |
The data is sufficient for a narrow, internal concept test about field preservation and exception handling. It is not sufficient for a live quotation or delivery commitment.
Ownership and access register

| Area | Current supplied condition | Readiness observation |
| --- | --- | --- |
| Sales intake | Sales can record and correct enquiry fields | Process owner is named |
| Operations request application | Operations can review and update requests | Business owner is named |
| Product and availability information | Operations owns business meaning | Refresh and quality review cadence remain open |
| IT access administration | IT Lead investigates access exceptions | Approval path and review schedule are not supplied |
| Customer communication | Sales owns customer-facing quotation acceptance | No proposed automation may send a quotation without further decision |
| Private staff notes | Not in the approved packet | Excluded from the opportunity |
Integration assessment
The intended field map for MSP-OPP-003 is:

| Source field | Destination field | Transformation | Identifier |
| --- | --- | --- | --- |
| Business enquiry ID | External enquiry reference | None | MSP-ENQ-401 |
| Product code | Requested product | None after validation | BF-10 |
| Quantity | Requested quantity | Whole-number validation | 20 |
| Requested date | Requested date | Preserve as request, not promise | 2026-10-15 |
The supplied assessment records:
- No live connection has been configured.
- The business field mapping is drafted for four fields.
- Destination-generated IDs must be retained alongside business IDs.
- Duplicate and retry handling is not yet tested.
- Read and write permissions for a proposed connection are unconfirmed.
- A shared record may remove the need for a second entry, but this alternative has not been assessed.
Licence and usage assessment
The supplied licence register says:
- Current entitlements for the proposed connection are not inventoried.
- Any connector, environment or premium-feature requirement is unconfirmed.
- Model or AI usage allowance is not relevant to a rules-only field transfer but would be relevant to MSP-OPP-002.
- Development and test access is not confirmed.
- Contract, region and edition are not supplied.
- No current price should be inserted into the case.
This is enough to assign a low readiness score for licensing. It is not enough to calculate a purchase cost.
Support and stakeholder notes

| Role | Supplied position |
| --- | --- |
| Sponsor | Supports investigating quotation preparation and handoff delay |
| Sales Lead | Will review intake and quotation outputs |
| Operations Lead | Will confirm availability information and exceptions |
| Finance Lead | Requires distinct effort, usage and cash-cost assumptions |
| IT Lead | Will assess access, interfaces and support requirements |
| Support rota | No named operational support rota exists yet |
| Maintenance owner | No owner is assigned for field mapping or rule changes |
| Stakeholder disagreement | Sales prefers one shared record; Operations currently uses a separate request application |
The disagreement is a readiness issue, not a reason to assign blame.
Step 1: choose a defined assessment scope
The scorecard assesses:
A proposed transfer of checked enquiry fields from the Sales intake worksheet to the Operations request application under MSP-OPP-003.
It does not score the whole enquiry-to-quotation process, a customer-facing quotation automation or an AI agent.
Step 2: use an explicit scoring scale
Use this scale for each criterion:

| Score | Meaning |
| --- | --- |
| 0 | Unknown, unavailable or not permitted |
| 1 | Weak: material gap blocks the next responsible step |
| 2 | Partial: evidence exists, but a dependency or control remains |
| 3 | Ready for the defined next step |
A score is not a probability of success. It is a structured description of readiness for the stated scope.
Step 3: apply criteria and weights
The following weights sum to 100%.

| Criterion | Weight | What a high score requires |
| --- | --- | --- |
| Data quality and ownership | 20% | Required data is sufficiently accurate, current, defined and owned |
| Access and permission | 15% | Required read/write permissions and permitted use are confirmed |
| Integration and identifiers | 15% | Interfaces, mappings, identifiers and retry handling are understood |
| Licences and usage capacity | 10% | Required entitlements and capacity are confirmed |
| Process stability | 15% | Boundary, fields, roles and exception routes are stable enough to measure |
| Support readiness | 15% | Monitoring, maintenance, fallback and incident ownership are assigned |
| Stakeholder readiness | 10% | Affected roles agree on the task, owner and review process |
Calculate:
\[
\text{Readiness percentage}
=
\sum
\left(
\frac{\text{criterion score}}{3}
\times
\text{criterion weight}
\right)
\]
Step 4: complete the weighted score

| Criterion | Weight | Score | Calculation | Weighted points |
| --- | --- | --- | --- | --- |
| Data quality and ownership | 20% | 2 | 2 ÷ 3 × 20 | 13.33 |
| Access and permission | 15% | 1 | 1 ÷ 3 × 15 | 5.00 |
| Integration and identifiers | 15% | 1 | 1 ÷ 3 × 15 | 5.00 |
| Licences and usage capacity | 10% | 0 | 0 ÷ 3 × 10 | 0.00 |
| Process stability | 15% | 2 | 2 ÷ 3 × 15 | 10.00 |
| Support readiness | 15% | 1 | 1 ÷ 3 × 15 | 5.00 |
| Stakeholder readiness | 10% | 2 | 2 ÷ 3 × 10 | 6.67 |
| Total | 100% |  |  | 45.00% |
The score is 45.00%.
The calculation is reproducible:
\[
13.33 + 5 + 5 + 0 + 10 + 5 + 6.67 = 45.00
\]
Step 5: examine sensitivity
A weighted score can hide important dependencies. Test what happens if one criterion improves by one point.

| Change | Score effect |
| --- | --- |
| Data quality and ownership: 2 to 3 | +6.67 percentage points |
| Access: 1 to 2 | +5.00 points |
| Integration: 1 to 2 | +5.00 points |
| Licences: 0 to 1 | +3.33 points |
| Process stability: 2 to 3 | +5.00 points |
| Support: 1 to 2 | +5.00 points |
| Stakeholder readiness: 2 to 3 | +3.33 points |
If licensing improves from 0 to 3, the score rises by:
\[
\frac{3}{3} \times 10 = 10 \text{ points}
\]
The result would be 55.00%, but that still does not resolve access, integration or support gaps.
This demonstrates a limitation of weighted scoring: a high total can conceal a critical zero. Meridian should treat licence and access as gates for any live transfer, regardless of the total.
Step 6: make a readiness decision
Completed artifact: MSP_Readiness_Decision_v0_1.md
Decision: revise before live transfer assessment.  
The proposed Sales-to-Operations transfer scores 45.00% under the supplied weights. Data ownership is partly established and the business field mapping is drafted, but access, interface behaviour, licensing and support ownership remain incomplete. Assess a shared-record alternative, confirm permissions and entitlements, test duplicate handling and name a maintenance owner. The six-case internal concept packet may remain a learning exercise, but it is not evidence that a live integration is ready. MSP-PILOT-001 remains proposed and unexecuted.
Why this decision is appropriate
The decision is not based on a universal pass mark. The most important gaps are specific:
- No confirmed connection permissions.
- No tested retry or duplicate behaviour.
- No licence inventory.
- No support or maintenance owner.
- A stakeholder disagreement about whether two records are necessary.
A solution may later be feasible. The current evidence does not support treating it as ready.
Limitations of the scorecard
The scorecard has several limitations:
1. The 0–3 scores are ordinal judgements, not precise measurements.
2. Weights reflect the workshop’s stated priorities and may change.
3. A high total can conceal a zero in a critical criterion.
4. The score does not measure business value, cost, risk severity or model accuracy.
5. Evidence quality affects the score; missing records may lower readiness without proving that the underlying condition is poor.
6. A score for one process boundary cannot be reused for a different opportunity.
7. Readiness can change when systems, owners, licences or process rules change.
The score is a conversation and decision aid, not an approval certificate.
5. Try it yourself — Guided practice
Learning goal and access
Score MSP-OPP-002, the opportunity to organise varied enquiry wording into a source-grounded internal brief.
You will assess data quality and ownership, access, integration, licences, process stability, support readiness and stakeholder readiness. No product account is required. All data is supplied below.
You may work individually. In a group, use the Sponsor, Sales, Operations, Finance and IT perspectives. The individual alternative is to write one sentence explaining what each role would challenge.
Practice evidence packet
This packet is synthetic and separate from the worked score for MSP-OPP-003.
Source-quality sample
enquiry_id,product_present,quantity_present,requested_date_present,approved_source_found,source_date_known,reviewer
MSP-ENQ-501,yes,yes,yes,yes,yes,Sales-01
MSP-ENQ-502,yes,yes,no,yes,yes,Sales-01
MSP-ENQ-503,yes,no,yes,yes,yes,Sales-02
MSP-ENQ-504,yes,yes,yes,no,no,Sales-02
MSP-ENQ-505,yes,yes,yes,yes,yes,Sales-01
MSP-ENQ-506,no,yes,yes,yes,yes,Sales-02
MSP-ENQ-507,yes,yes,yes,yes,yes,Sales-01
MSP-ENQ-508,yes,yes,yes,yes,yes,Sales-02
The eight cases are a sample for this exercise. They do not represent a weekly or monthly population.
Ownership and access facts
- Sales Lead owns the internal brief process.
- Operations Lead owns availability confirmation.
- The approved catalogue and Operations note have named business owners.
- Sales may read the enquiry packet.
- Operations may read the approved source extracts.
- No permission is supplied for a drafting assistant to access private staff notes.
- Sales review is required before any customer-facing use.
- IT has not confirmed whether the proposed drafting service may access the approved source folder.
- The company has not recorded a maintenance owner for source indexing or prompt/template updates.
Integration and licence facts
- The initial brief can be prepared offline without writing to another system.
- No live integration is required for the guided practice.
- If a later design retrieves sources automatically, source permissions and an interface must be checked.
- A standard document template is available.
- Licence status for a proposed generative assistance feature is unknown.
- Model usage volume and regional/edition requirements are unknown.
- Finance has asked for a usage and review-cost estimate before approval.
Process and stakeholder facts
- The brief boundary is agreed: internal preparation only.
- The normal input is a customer enquiry plus approved sources.
- Missing values and unavailable sources have explicit exception routes.
- Source review is required before use.
- Sales supports a trial template.
- Operations supports an internal brief but requires clear availability ownership.
- IT has not reviewed the proposed source access.
- Finance wants the cost model before supporting additional usage.
Scoring rubric
Use the same 0–3 scale and weights as the worked case.

| Score | Interpretation |
| --- | --- |
| 0 | Unknown, unavailable or not permitted |
| 1 | Material gap prevents the next responsible step |
| 2 | Partial evidence or control; targeted work remains |
| 3 | Ready for the stated next step |
Learner worksheet

| Criterion | Weight | Score | Evidence and reasoning | Weighted points |
| --- | --- | --- | --- | --- |
| Data quality and ownership | 20% |  |  |  |
| Access and permission | 15% |  |  |  |
| Integration and identifiers | 15% |  |  |  |
| Licences and usage capacity | 10% |  |  |  |
| Process stability | 15% |  |  |  |
| Support readiness | 15% |  |  |  |
| Stakeholder readiness | 10% |  |  |  |
| Total | 100% |  |  |  |
Guided steps and expected intermediate results
1. Assess the source sample.
- Expected result: you identify missing quantity, missing date, absent approved source and missing source-date evidence.
2. Separate ownership from access.
- Expected result: business owners are named, but drafting-service access and maintenance ownership remain unresolved.
3. Assess the current boundary.
- Expected result: the offline internal brief has a clear boundary and no live integration dependency.
4. Score each criterion.
- Expected result: each score cites at least one supplied fact.
5. Calculate the weighted total.
- Expected result: all weighted points sum to the total.
6. Write a decision.
- Expected result: the decision states whether to proceed with a bounded offline template exercise, revise the live generative design or defer it.
Your final artifact is MSP_OPP_002_Readiness_Scorecard_Practice.md.
A score alone is incomplete. Include the critical gaps, the next evidence requests and one limitation of the matrix.
No system access or cleanup is required.
6. Independent challenge
Assess a changed version of MSP-OPP-001, the required-field validation opportunity.
Challenge scope
The proposed process is:
When a Sales enquiry is recorded, validate product code, quantity and requested date, then either allow a handoff or produce a clarification exception.
The proposed first step uses rules in the existing intake record. It does not use generative AI and does not send customer messages.
Complete challenge packet
Data quality and ownership
- A 12-record sample contains 10 recognised product codes.
- Nine records contain positive whole-number quantities.
- Ten records contain requested dates.
- The Sales Lead owns the intake fields.
- The Operations Lead owns the product catalogue.
- One catalogue field is labelled “Requested date”; the intake field is labelled “Customer date”.
- Both owners have agreed that these fields mean the same thing for this scope.
- A weekly catalogue review is scheduled, but the first review has not yet occurred.
Access and permission
- Sales can read and update intake records.
- Operations can maintain the product catalogue.
- The proposed rules run inside the existing intake record.
- No customer email or private staff note is accessed.
- IT has not yet reviewed whether the rules can be changed by Sales administrators.
Integration and identifiers
- No cross-app transfer is needed for the first validation step.
- A later Operations handoff still uses the business enquiry ID.
- No automated retry or duplicate test is needed for the rules-only first step.
- The future handoff mapping is not part of this score.
Licence and usage
- The existing intake record includes the required validation capability under the supplied challenge assumptions.
- No model or usage allowance is required for the rules-only step.
- Training or support material may require ordinary business effort, but no new product licence is identified.
Process stability
- Product, quantity and requested date are agreed required fields.
- The clarification route is defined.
- The process still has separate access and availability exceptions.
- The proposed step does not decide availability or send a quotation.
Support and stakeholders
- Sales Lead owns rule content.
- IT Lead will review any rule change.
- Operations Lead owns catalogue meaning.
- Finance supports the rules-only approach but wants later value evidence.
- No named monthly review date for the rules has been supplied.
- Sponsor, Sales and Operations support testing the narrow validation step.
Deliverables
1. Complete a weighted readiness score.
2. Identify the lowest-scoring criterion or criteria.
3. State whether the rules-only validation step should proceed, be revised or be deferred.
4. List two controls that should remain outside the rules.
5. Explain one limitation of your score.
Success criteria
Your work should:
- Use only the supplied challenge facts.
- Keep the rules-only scope separate from the later handoff.
- Preserve the access and availability exceptions.
- Show calculations with units and weights.
- Name a decision owner and next evidence request.
7. Common problems and recovery

| Symptom | Diagnosis | Correction | Verification |
| --- | --- | --- | --- |
| A source is scored ready because it is easy to open | Accessibility has been confused with quality and authority | Check owner, status, date, coverage and permitted use | The score cites evidence beyond “I can access it” |
| IT is listed as owner of every data issue | System ownership has replaced business ownership | Name data, process, decision and support owners separately | Each owner has a distinct responsibility |
| Read access is treated as write permission | Permissions are being inferred | Record read, create, update and send capabilities separately | The proposed action is allowed by the stated access |
| A licence is assumed because a user can sign in | Product access and feature entitlement differ | Confirm feature, connector, environment and usage requirements | The licence register names the dependency and source |
| The readiness score is high despite a critical zero | Weighted averaging has hidden a gate | Apply explicit critical-criterion gates | A zero in access or permission prevents live use |
| A stable normal path hides frequent exceptions | Stability has been assessed only from the happy path | Count and define exception routes | The pilot boundary states which exceptions are included |
| A demonstration has no support owner | One-time success is being mistaken for operational readiness | Assign maintenance, monitoring, incident and fallback owners | A user knows who handles a failure |
| Stakeholder disagreement is removed from the record | Disagreement has been treated as a communication problem | Record the different requirements and resolve the decision | The final owner and decision are explicit |
Recovery example: an unknown licence
If the licence status is unknown, do not assign a guessed price or mark the capability ready. Record:
Required entitlement and usage capacity not confirmed. Finance and IT to identify the relevant edition, connector, environment, volume and regional terms.
The next responsible action is evidence collection, not purchase.
8. Check your understanding
1. Why is an approved but dated stock snapshot useful and limited at the same time?
2. Who is responsible for the meaning of availability information, and who may be responsible for maintaining a connection to it?
3. Why is a licence check needed even when the proposed process appears technically simple?
4. What is the difference between an integration dependency and a support dependency?
5. Why should a scorecard include both a total and critical-criterion gates?
6. What evidence would show that a process is stable enough for a bounded pilot?
7. Why should a stakeholder disagreement appear in the readiness register?
9. Solutions and explanations
Lesson checks
L1: Relevance means that a source concerns the topic. Authority means that the source is approved, current enough and owned for the decision being made. An obsolete document may be relevant but not authoritative.
L2: The business owner of availability should decide whether the evidence supports a delivery commitment. A connection maintainer may operate the technical transfer but does not automatically own the business decision.
L3: A read-only connection can supply facts for an internal brief. Creating an Operations request requires permission to write, a mapping, duplicate handling and an owner for the destination record.
L4: Confirm the source and destination systems, required actions, field mappings, identifiers, access, connector or API availability, licences, usage limits, implementation effort, support and failure handling. A connection that works in a demonstration may still be unaffordable or unapproved.
L5: A demonstration may work with test data but lack an owner, support path, maintenance process or user agreement. Operational readiness includes what happens after the demonstration.
Guided practice — Completed scorecard
A reasonable scorecard is:

| Criterion | Weight | Score | Evidence and reasoning | Weighted points |
| --- | --- | --- | --- | --- |
| Data quality and ownership | 20% | 2 | Owners are named and the sample is usable for a narrow brief, but missing fields and source coverage remain | 13.33 |
| Access and permission | 15% | 1 | Sales and Operations access is described, but drafting-service access to the source folder is unconfirmed | 5.00 |
| Integration and identifiers | 15% | 2 | No integration is needed for the offline brief; future retrieval/interface details remain open | 10.00 |
| Licences and usage capacity | 10% | 0 | Proposed generative-feature entitlement, volume and edition are unknown | 0.00 |
| Process stability | 15% | 2 | Boundary, exception routes and review requirement are defined; source variation remains | 10.00 |
| Support readiness | 15% | 1 | No maintenance owner for indexing or template/prompt updates is supplied | 5.00 |
| Stakeholder readiness | 10% | 2 | Sales and Operations support a controlled exercise; IT and Finance still require evidence | 6.67 |
| Total | 100% |  |  | 50.00% |
Calculation:
\[
13.33 + 5 + 10 + 0 + 10 + 5 + 6.67 = 50.00\%
\]
A suitable decision is:
Proceed with a bounded offline template comparison using the supplied sample and approved sources. Revise the live generative-assistance design before requesting live source access. Confirm licensing, source permission, maintenance ownership and total review effort. Do not send customer messages or claim savings.
This decision separates two scopes:
- The offline exercise can proceed as a learning and evaluation activity because it does not require live integration or unconfirmed model access.
- The live design is not ready because access, licensing and support gaps remain.
Possible next evidence requests:
1. Confirm whether the proposed assistance feature may read the approved source folder.
2. Identify the relevant licence, usage allowance and maintenance owner.
A limitation statement could be:
The score is based on an eight-record exercise sample and supplied role descriptions; it does not establish wider source quality, production reliability or financial value.
Valid alternative scores are possible if the reasoning is tied to the supplied facts. For example, a learner may score data quality as 1 because two required fields are absent and one source is unavailable. The score must then explain why a narrow internal brief cannot yet use those exceptions safely.
Independent challenge — Completed scorecard
A reasonable challenge scorecard is:

| Criterion | Weight | Score | Calculation | Weighted points |
| --- | --- | --- | --- | --- |
| Data quality and ownership | 20% | 2 | 2 ÷ 3 × 20 | 13.33 |
| Access and permission | 15% | 2 | 2 ÷ 3 × 15 | 10.00 |
| Integration and identifiers | 15% | 3 | 3 ÷ 3 × 15 | 15.00 |
| Licences and usage capacity | 10% | 3 | 3 ÷ 3 × 10 | 10.00 |
| Process stability | 15% | 3 | 3 ÷ 3 × 15 | 15.00 |
| Support readiness | 15% | 2 | 2 ÷ 3 × 15 | 10.00 |
| Stakeholder readiness | 10% | 3 | 3 ÷ 3 × 10 | 10.00 |
| Total | 100% |  |  | 73.33% |
Calculation:
\[
13.33 + 10 + 15 + 10 + 15 + 10 + 10 = 73.33\%
\]
The lower data score reflects the supplied sample: 10 of 12 product codes, nine of 12 quantities and ten of 12 dates are complete or recognised. The exercise does not establish why the four gaps occurred or whether the sample is representative.
The lower access score reflects the unconfirmed authority for Sales administrators to change rule content. The rules themselves operate in the existing intake record under the challenge assumptions.
A suitable decision is:
Proceed with a bounded rules-only validation test after IT confirms change permissions and a maintenance review date is assigned. Keep availability decisions, access exceptions and customer communication outside the rules. Do not extend this score to the later cross-app handoff.
Two controls that remain outside the rules:
1. Availability confirmation: Operations decides whether a requested delivery can be supported.
2. Customer communication: Sales reviews and accepts any customer-facing quotation or promise.
Other acceptable controls include source-access review, exception logging and a manual fallback when a rule cannot evaluate a record.
A suitable limitation statement is:
The score reflects a 12-record sample and the narrow validation scope. It does not establish the rate of future exceptions, the effect on customer waiting or the readiness of the later Operations handoff.
Understanding questions
1. It is useful because it records listed stock at a stated time and may identify a quantity discrepancy. It is limited because reservations, later changes, source coverage and delivery confirmation are absent.
2. Operations owns the business meaning of availability. IT or a system owner may maintain the connection or access configuration. These responsibilities must not be collapsed.
3. Even a simple change may require a feature entitlement, connector, environment access, usage capacity or support arrangement. Signing in is not evidence that all dependencies are met.
4. An integration dependency concerns the ability to exchange information or actions. A support dependency concerns what happens when users need help, a rule changes or a transfer fails.
5. A total summarises several dimensions, while a gate prevents a critical missing condition from being hidden by strengths elsewhere.
6. Evidence may include a stable boundary, agreed field definitions, repeatable roles, known exception routes, consistent inputs and a measure that can be collected before and after the change.
7. The disagreement may reveal a different process requirement, such as one shared record versus two applications. Recording it makes the decision and affected owners visible.
10. Chapter recap and next step
Readiness asks whether the proposed next step has the conditions needed to be understood, permitted, measured and supported.
The main lessons are:
- Source quality includes authority, completeness, timeliness and coverage.
- Ownership must be divided by data, process, system, decision and support responsibility.
- Access is purpose-specific and must distinguish read, write and send actions.
- Integrations require mappings, identifiers, permissions, retries and reconciliation.
- Licences and usage capacity are dependencies, not afterthoughts.
- Stable processes can still have exceptions, but the exceptions must be explicit.
- A support owner and stakeholder agreement are part of readiness.
- A weighted score helps structure judgement but cannot replace critical gates or evidence.
“I can…” checklist
- I can assess whether a source is accurate, complete, current and authoritative enough for a task.
- I can name data, process, system, decision and support owners.
- I can distinguish read permission from write or send permission.
- I can identify integration and licence dependencies.
- I can assess process stability and exception handling.
- I can identify support and stakeholder gaps.
- I can calculate a weighted readiness score with units and assumptions.
- I can test score sensitivity and explain limitations.
- I can make a proceed, revise or defer recommendation without hiding critical gaps.
Your project artifacts are:
- MSP_Readiness_Evidence_Register_v0_1.md
- MSP_Readiness_Scorecard_v0_1.md
- MSP_Readiness_Decision_v0_1.md
- MSP_Case_Assumptions_v0_4.md
For assumptions version 0.4, retain MSP-A-001 through MSP-A-010 and add:

| Assumption ID | Added assumption | Status |
| --- | --- | --- |
| MSP-A-011 | The supplied source owners can approve use of their records for the stated pilot scope | Unconfirmed |
| MSP-A-012 | The proposed connection or assistance feature has an available entitlement | Unconfirmed |
| MSP-A-013 | A shared record may remove the need for a separate Operations request application | Untested |
| MSP-A-014 | A named support and maintenance owner can be assigned before a live pilot | Unconfirmed |
Chapter 5, Value, Costs and Business Case, will use these readiness gaps when estimating implementation, licence, model-usage, review and support costs. It will also distinguish released capacity from actual cash savings.
11. Glossary and further reading
Glossary

| Term | Meaning |
| --- | --- |
| Access | Permission to use a source or perform an action for a defined purpose |
| Data owner | Person accountable for the meaning, suitability and governance of a data set |
| Data quality | Fitness of information for its intended use, including accuracy and completeness |
| Data steward | Person who maintains or improves data quality in practice |
| Integration dependency | Condition required for systems to exchange information or actions |
| Licence dependency | Required product, feature, connector, capacity or usage entitlement |
| Least privilege | Giving only the access needed for the defined task |
| Process owner | Person accountable for how a process operates and what result it produces |
| Readiness | Evidence that the conditions for a defined next step are sufficiently understood and controlled |
| Support owner | Person or team responsible for user help, incidents, monitoring and maintenance |
| System owner | Person accountable for a system’s operation, configuration and access model |
| Weighted score | A combined score in which criteria contribute according to stated weights |
Further reading
The following official sources were accessed for product concepts. Product names, editions, permissions, usage limits, pricing and licensing terms can vary by region, plan, environment and date. No Meridian product connection or product execution is claimed.
1. Zoho Flow FAQ — Flow, triggers, actions, connections and execution considerations. Describes Zoho Flow’s product-specific trigger/action model, connections and some execution and third-party API considerations.  
https://www.zoho.com/flow/help/faq.html
2. Microsoft Learn — Manage connections in Power Automate. Explains how Power Automate connections provide access to data and actions, and discusses connection management and troubleshooting.  
https://learn.microsoft.com/en-us/power-automate/add-manage-connections
3. Microsoft Learn — Power Platform licensing FAQs. Describes licensing categories and directs readers to current product-specific licensing material. It should be checked for the relevant product, region, edition and contract before any cost model is prepared.  
https://learn.microsoft.com/en-us/power-platform/admin/powerapps-flow-licensing-faq
[1]: https://www.zoho.com/flow/help/faq.html
[2]: https://learn.microsoft.com/en-us/power-automate/add-manage-connections
[3]: https://learn.microsoft.com/en-us/power-platform/admin/powerapps-flow-licensing-faq
