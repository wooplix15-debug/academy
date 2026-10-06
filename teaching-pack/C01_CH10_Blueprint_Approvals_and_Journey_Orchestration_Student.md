schema_version: "1.1"
course_id: "C01"
chapter_id: "C01-CH10"
chapter_number: 10
chapter_title: "Blueprint, Approvals and Journey Orchestration"
filename: "C01_CH10_Blueprint_Approvals_and_Journey_Orchestration_Student.md"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "not_verified"
---
Blueprint, Approvals and Journey Orchestration
1. What you will learn
A workflow can notify people, create tasks and update fields. It should not be the only control for a process that must move through authorised stages.
A Blueprint controls how a record moves between defined states. An approval process asks an authorised person to accept, reject or return a request. A journey orchestration connects several activities, waits, decisions and escalations across a longer business path.
In this chapter, you will learn to:
- define states and explain how they differ from ordinary fields;
- design transitions between states;
- specify entry criteria, exit criteria and mandatory information;
- distinguish a workflow notification from an approval decision;
- design approval and review routes;
- create escalation rules for waiting decisions;
- decide when a Blueprint, approval process, workflow or journey is appropriate;
- identify candidate CommandCenter scenarios and product dependencies;
- configure and test a controlled process with normal, denied, rejected, returned and escalated paths;
- recover from incomplete information, unauthorised actions and failed transitions.
The chapter continues the Meridian Supply scenario. The supplied continuity from Chapter 9 establishes that:
- MER-ENQ-001 is linked to MER-CUST-001 and MER-QUOTE-001;
- an email or field update does not prove that finance accepted a handoff;
- Finance Handoff Status = Ready is different from finance acceptance;
- workflows are used for notifications, tasks and field updates;
- workflow execution, edition limits and permissions have not been verified in a live Zoho environment.
No unprovided decisions from Chapters 2–8 are assumed. The new approval thresholds and state rules in this chapter are synthetic learning-case rules.
No coding is required. Product configuration requires suitable administrator or process-management access. Exact Zoho CRM, Blueprint and CommandCenter navigation, edition support and permission names must be checked in the current official documentation.
2. Lessons
2.1 What is a state?
A state describes the controlled phase of a record in a process. It answers:
Where is this record in its authorised lifecycle?
Examples include:
- Draft;
- Awaiting Approval;
- Approved;
- Sent to Customer;
- Customer Accepted;
- Ready for Finance;
- Returned for Correction;
- Closed.
A state is more than a label. It should define:
- what is true when the record enters;
- what information must exist;
- who may perform the next action;
- what transition is allowed;
- what evidence proves that the transition occurred;
- which paths are available when something goes wrong.
A free-text status such as “nearly done” is not a reliable controlled state. Different users may interpret it differently.
State versus field
Concept	Purpose	Meridian example
State	Controlled position in a process	Awaiting Approval
Field	Information about the record	Discount percentage
Transition	Authorised movement between states	Submit for approval
Approval outcome	Decision by an authorised reviewer	Approved or Rejected
Workflow action	Automated response to an event	Create a task for the sales manager
A record may have many fields but one active state within a particular Blueprint. A field such as Finance Handoff Status can provide supporting information, but it should not be used as a substitute for a controlled transition when the process requires permission and evidence.
Check your understanding
Why is Approved a stronger process state than a field containing the text “manager said okay”?
Answer: Approved can be tied to an authorised transition, approver, timestamp and decision evidence. Free text does not reliably identify who approved the record, what was approved or whether the decision remains valid.
2.2 Designing transitions
A transition is the controlled action that moves a record from one state to another.
A transition specification should identify:
1. the source state;
2. the target state;
3. who may perform it;
4. entry criteria;
5. mandatory information;
6. actions performed during the transition;
7. exit criteria;
8. the evidence produced;
9. the exception or recovery route.
For Meridian, the transition from Draft to Awaiting Approval could be:
A sales representative submits a quote for review when the quote has a customer, line items, currency, total and discount percentage.
The transition should not be available if the customer is unknown or currency is blank.
Entry and exit criteria
- Entry criteria determine whether a record may begin a transition.
- Exit criteria determine whether the transition has completed successfully.
Example:
Transition	Entry criteria	Exit criteria
Draft → Awaiting Approval	Quote has a customer, line items, currency and discount percentage	Approval request exists and state is Awaiting Approval
Awaiting Approval → Approved	Approver is authorised and approval decision is positive	Approval evidence is recorded and state is Approved
Approved → Sent	Required approval exists and customer-facing quote is complete	Quote sent timestamp is recorded
Customer Accepted → Ready for Finance	Customer acceptance and finance fields are complete	Finance handoff is marked Ready with an owner
Ready for Finance → Returned	Finance identifies missing or incorrect data	Return reason is recorded and owner receives correction task
A transition should not be considered complete merely because someone clicked its button. The resulting state and evidence must be verified.
Check your understanding
What is missing from a transition called “Send to Finance” if it has no required fields, receiving owner or acceptance evidence?
Answer: It has no defined data-quality gate, responsibility or proof of completion. It may only send a message without establishing that finance received or accepted a usable handoff.
2.3 Mandatory information and data quality
Mandatory information prevents a record from entering a state where the next team cannot work.
Mandatory information can be required:
- when a transition begins;
- before an approval is submitted;
- before a record enters a state;
- before a record leaves a state;
- only for a particular exception path.
For the Meridian quote process, the finance handoff requires:
- Meridian Customer ID;
- Meridian Quote ID;
- acceptance timestamp;
- currency;
- total;
- item lines;
- owner;
- recorded duplicate decision.
A field can be present but still invalid. For example:
- currency contains free text rather than an approved code;
- total does not equal the sum of line items;
- approval is recorded for a different quote version;
- a customer ID points to a duplicate record;
- the acceptance timestamp is earlier than the quote sent timestamp.
Mandatory fields and permissions
A field being mandatory does not automatically mean every user can supply it. If the person completing a transition cannot edit a mandatory field, the process must provide a correction route or assign the transition to a role that can complete it.
This creates a useful test:
Can the person who is required to complete the transition access and correct every mandatory field?
If the answer is no, the transition design is incomplete.
Check your understanding
A sales representative can submit a quote for approval but cannot edit the currency field. The currency is blank. What are two acceptable designs?
Answer: The process can prevent submission and direct the sales representative to an authorised data owner, or it can route the transition to a role that can supply and verify the currency. Allowing submission with missing currency is not acceptable when currency is mandatory for approval or finance.
2.4 Approval and review processes
An approval is an authorised decision about whether a request may proceed. A review may be broader: it can confirm information, classify a record or return it for correction without being a formal approval.
Use an approval when:
- a role must authorise a financial, contractual or operational decision;
- the decision must be traceable;
- the requester and approver should be separate;
- the outcome has allowed and rejected paths.
Use a review when:
- information needs validation;
- possible duplicates need classification;
- a specialist must confirm a condition;
- the reviewer may return the record without approving the business outcome.
Meridian approval rule
The following is a synthetic Meridian rule:
A quote with a discount greater than 10% requires sales manager approval before it can be sent to the customer.
A quote with a discount of 10% or less follows the standard route and does not require this approval. This is a case rule, not a universal commercial policy.
The approval design should define:
Decision item	Meridian design
Requester	Sales representative
Approver	Sales manager
Approval condition	Discount percentage greater than 10%
Required data	Customer, line items, currency, total, discount and quote version
Positive outcome	Approval recorded; quote may move to Approved
Negative outcome	Quote moves to Rejected or Returned for Correction
No response	Escalation to sales operations after one business day
Evidence	Approver, decision, timestamp, comment and quote version
Do not implement an approval only as a notification. A notification asks someone to look at a record; an approval process controls the permitted outcome.
Rejection versus return
These outcomes have different meanings:
- Rejected: The request should not proceed under the current proposal.
- Returned for correction: The request may proceed after identified information is corrected.
- Cancelled: The requester or owner intentionally stops the request.
- Expired: The request passed a defined validity period without completion.
If the product uses different labels, document the business meaning of each label.
Self-approval
A process should normally prevent the requester from approving their own request when separation of duties is required. If a small business permits self-approval for a specific low-risk case, record that as an explicit business rule rather than assuming it.
Check your understanding
Why is “send a notification to the manager” not equivalent to “require manager approval”?
Answer: A notification does not necessarily block the process, record a decision, prevent unauthorised progression or provide rejection and escalation evidence. An approval must control the permitted outcomes.
2.5 Escalations
An escalation occurs when a required action has not happened within a defined period or when an exception needs a higher level of attention.
An escalation needs:
1. a starting event;
2. a target duration;
3. a definition of incomplete;
4. a recipient or higher-level owner;
5. an escalation action;
6. a repeat or stop rule;
7. evidence of the escalation.
Meridian’s synthetic approval escalation rule is:
If a discount approval remains in Awaiting Approval for one business day, notify the sales operations owner and create an escalation task.
This rule requires a clear start event: the timestamp when the approval request entered Awaiting Approval.
A second synthetic rule is:
If a finance handoff remains Ready for Finance for one business day without finance acceptance or return, notify the finance team lead.
Do not infer that an escalation was unnecessary because a decision eventually happened. The elapsed time must be calculated from the defined start and observed decision time.
Escalation states
An escalation can be represented by:
- a separate escalation field;
- an escalation task;
- a state such as Escalated;
- an event in the approval history;
- a journey branch.
The design should prevent repeated escalations from creating unlimited tasks. For example:
Escalation Status = Not escalated
can change to First escalation sent. A second escalation should have a separate rule and owner.
Paused or cancelled escalations
Define what happens when:
- the record is returned for correction;
- the approval is rejected;
- the record is cancelled;
- the approver changes;
- the record is already escalated;
- the approval is completed before the timer expires.
The product’s exact timer and cancellation behavior must be tested. Do not assume that changing a state automatically cancels every scheduled escalation.
Check your understanding
An approval is completed after two business days, but the target was one business day. Was an escalation still required?
Answer: Yes, if the escalation rule started when the approval was submitted and no exception paused or cancelled it. Eventual completion does not erase the elapsed time.
2.6 Blueprint, workflow and CommandCenter journeys
These tools solve related but different problems.
Tool or concept	Best suited to	Example
Workflow	Automatic response to an event	Create a follow-up task after a quote is sent
Blueprint	Controlled movement through states	Prevent an unapproved quote from being sent
Approval	Authorised decision	Sales manager approves a discount above 10%
Journey or CommandCenter	Coordinated multi-step path with waits, conditions and actions	Coordinate enquiry, approval, finance handoff and service follow-up
A journey should not be used simply because it is more elaborate. Use the simplest control that accurately represents the business requirement.
Candidate CommandCenter scenarios
The following are candidate scenarios for Meridian that should be checked against the current edition and supported modules:
1. Enquiry-to-quote journey  
An enquiry enters the journey, receives an owner, waits for qualification, branches for duplicate review and proceeds to quote preparation.
2. Approval waiting and escalation  
A quote enters an approval stage, waits for a manager decision, escalates after the target period and branches to approved, returned or rejected.
3. Finance handoff journey  
An accepted quote moves through readiness validation, finance acceptance and correction or escalation routes.
4. Customer-service connection  
Installation or order information creates the context for a later service process, subject to supported connections and data ownership.
5. Employee onboarding journey  
A separate People process coordinates HR, IT and facilities tasks while restricting confidential employee information.
These are design scenarios, not claims that every CommandCenter node, module, connection or escalation is available in every Zoho edition.
A candidate scenario requires verification of:
- supported source module;
- supported target module;
- available state or stage controls;
- wait and timer behavior;
- approval support;
- notification and task support;
- connection or integration requirements;
- permissions;
- execution history;
- error and retry behavior.
Check your understanding
When should a Blueprint be preferred to a workflow field update?
Answer: Use a Blueprint when the record must move through authorised states and the transition needs entry criteria, mandatory information, permissions or evidence. Use a workflow field update when a state change does not require a controlled user decision and the automatic update is safe.
2.7 Configuring a controlled process
The following is an edition-neutral procedure for configuring a Blueprint and approval design. Exact navigation and feature availability must be confirmed in the current product edition.
Required access
You need permissions appropriate to the selected environment for:
- creating or editing fields and controlled values;
- creating or editing a Blueprint or equivalent state process;
- defining transitions and transition owners;
- creating or editing an approval process;
- configuring notifications, tasks and escalations;
- viewing process history and execution details;
- activating, deactivating or revising the process;
- testing with synthetic records.
A user who can edit a quote may not be allowed to define or activate a Blueprint. Test both configuration permission and record-transition permission.
Configuration sequence
1. Define the process boundary.  
State the module and the starting and ending business events.
Expected result: You can identify which records and actions belong to the controlled process.
2. Create or confirm states.  
Use controlled state values and define the meaning of each.
Expected result: Every state has a purpose and an owner.
3. Define transitions.  
Specify source state, target state, permitted role, entry criteria, mandatory fields and exit evidence.
Expected result: Every normal and exception path is represented.
4. Configure mandatory information.  
Apply required fields to the appropriate transition rather than making every field mandatory for every state.
Expected result: A record with missing information cannot pass the relevant transition.
5. Configure the approval process.  
Define requester, approver, condition, positive outcome, rejection or return behavior and escalation.
Expected result: The approval decision blocks or permits the intended next transition.
6. Connect workflows carefully.  
Use workflows for notifications, tasks and supporting field updates. Do not let a workflow bypass the controlled transition.
Expected result: Automated actions support the Blueprint instead of creating a second uncontrolled state path.
7. Configure escalation.  
Define the start timestamp, target, recipient and stop condition.
Expected result: An overdue test record produces one defined escalation.
8. Test permissions.  
Test a permitted user, an unauthorised user, the requester and the approver.
Expected result: Each user can perform only the actions assigned to the role.
9. Activate in a safe environment.  
Use a test or sandbox environment where available. If synthetic records must be used in a live environment, identify them clearly and use synthetic recipients.
Expected result: No real customer or employee receives a test notification.
10. Review evidence.  
Inspect state, approval decision, transition history, tasks, notifications and escalation status.
Expected result: The actual observation can be compared with the expected result.
11. Document recovery.  
Record what happens after rejection, return, missing data, permission denial, timeout or failed action.
Expected result: No exception path depends on an administrator guessing what to do.
3. Visual explanation
stateDiagram-v2
    [*] --> Draft
    Draft --> AwaitingApproval: Submit for approval
    Draft --> Sent: Send standard quote
    AwaitingApproval --> Approved: Manager approves
    AwaitingApproval --> Returned: Manager requests correction
    AwaitingApproval --> Rejected: Manager rejects
    AwaitingApproval --> Escalated: Approval overdue
    Returned --> Draft: Correct and resubmit
    Escalated --> AwaitingApproval: Review escalated request
    Approved --> Sent: Send approved quote
    Sent --> CustomerAccepted: Customer accepts
    Sent --> Draft: Customer requests change
    CustomerAccepted --> ReadyForFinance: Required handoff data complete
    CustomerAccepted --> Returned: Handoff data missing
    ReadyForFinance --> FinanceAccepted: Finance accepts
    ReadyForFinance --> Returned: Finance returns
    Returned --> CustomerAccepted: Correct returned information
    FinanceAccepted --> [*]
    Rejected --> [*]
The diagram shows several important controls:
- A quote cannot move from Awaiting Approval directly to Sent unless the approval route permits it.
- Returned is a correction path, not a hidden failure.
- Escalated records that the approval target was missed.
- Finance acceptance is separate from Ready for Finance.
- The same record may return to an earlier state after a correction, but that movement should be authorised and evidenced.
A workflow can notify the approver when the record enters Awaiting Approval. The Blueprint controls whether the record may leave that state. The approval process records the manager’s decision. These controls work together but are not interchangeable.
4. Worked case: Meridian Supply quote approval and finance handoff
4.1 Scenario rules
The following rules are specific to this worked case:
- A quote discount greater than 10% requires sales manager approval.
- A discount of 10% or less does not require this approval.
- A quote cannot be sent to the customer while required approval is pending.
- A quote must contain a customer, line items, currency, total and discount percentage before approval submission.
- A customer acceptance can be recorded only after the quote is approved and sent.
- Finance handoff requires the Chapter 1 fields and a completed duplicate decision.
- Finance acceptance is a separate state from Ready for Finance.
- An approval remaining in Awaiting Approval for one business day is escalated to sales operations.
- A finance handoff remaining in Ready for Finance for one business day is escalated to the finance team lead.
- These are synthetic case rules and are not universal commercial or accounting policies.
4.2 Supplied records
Quote ID	Enquiry ID	Customer ID	Discount	Currency	Line items	Current state	Approval
MER-QUOTE-001	MER-ENQ-001	MER-CUST-001	12%	USD	Complete	Awaiting Approval	Pending
MER-QUOTE-002	MER-ENQ-004	MER-CUST-002	8%	Blank	Complete	Customer Accepted	Not required
MER-QUOTE-003	MER-ENQ-002	Blank	15%	USD	Incomplete	Draft	Not submitted
MER-QUOTE-004	MER-ENQ-003	Blank	14%	USD	Complete	Duplicate Review	Not submitted
Synthetic contacts:
- maya@acme.example.com
- omar@northstar.example.com
- lina@cedar.example.com
4.3 State design
State	Meaning	Entry requirements	Mandatory information
Draft	Quote is being prepared	New or returned quote	Customer, line items, currency, total and discount when submitting
Awaiting Approval	Approval is pending	Discount greater than 10% and complete quote	Approval requester and quote version
Approved	Required approval exists	Positive approval decision	Approver, decision timestamp and comment
Sent	Approved quote was sent to customer	Standard quote or approved quote	Sent timestamp and recipient
Customer Accepted	Customer accepted the current quote	Quote has been sent	Acceptance timestamp and evidence
Ready for Finance	Complete handoff is ready for finance	Accepted quote and complete handoff fields	Customer ID, quote ID, currency, total, line items and duplicate decision
Finance Accepted	Finance accepted the handoff	Finance acceptance event	Finance reference and acceptance evidence
Returned	Receiving party found a correctable problem	Return reason exists	Return reason and owner
Duplicate Review	Possible duplicate requires decision	Duplicate indicator or review request	Match evidence and reviewer
Rejected	Approval denied	Negative approval decision	Rejection reason
Escalated	Target was missed	Approval or finance target expired	Escalation owner and timestamp
4.4 Transition design
Transition	Permitted role	Entry criteria	Mandatory information
Submit for approval	Sales representative	Discount greater than 10%; quote complete	Customer, line items, currency, total, discount, quote version
Send standard quote	Sales representative	Discount 10% or less; quote complete	Customer, line items, currency, total
Approve quote	Sales manager	Approval is pending; approver is authorised	Decision and comment
Return quote	Sales manager	Approval or finance review identifies correction	Return reason
Send approved quote	Sales representative	Approval is positive	Approval evidence and recipient
Record customer acceptance	Sales representative	Quote is in Sent	Acceptance evidence and timestamp
Submit finance handoff	Sales representative	Customer Accepted; all handoff fields complete	Customer ID, quote ID, currency, total, line items and duplicate decision
Accept finance handoff	Finance processor	State is Ready for Finance	Finance reference and acceptance comment
Escalate approval	System or authorised operations role	Approval target expired	Escalation owner and timestamp
4.5 Applying the model to the records
MER-QUOTE-001
- Discount is 12%, so approval is required.
- Customer, currency and line items are present.
- The record is correctly in Awaiting Approval.
- A sales manager may approve, return or reject it.
- It must not be sent to the customer while approval is pending.
MER-QUOTE-002
- Discount is 8%, so the synthetic approval rule does not apply.
- Currency is missing.
- Although the quote is marked Customer Accepted, it cannot move to Ready for Finance.
- The correct route is Returned for currency correction.
MER-QUOTE-003
- Customer ID and line items are incomplete.
- The record cannot be submitted for approval.
- It remains Draft until the missing information is corrected.
MER-QUOTE-004
- The enquiry is in Duplicate Review.
- The quote cannot proceed to customer acceptance or finance handoff until the duplicate decision is complete.
4.6 Approval and escalation configuration
The approval process for MER-QUOTE-001 should contain:
Configuration item	Value
Request condition	Discount percentage greater than 10%
Requester	Sales representative
Approver	Sales manager
Required submission data	Customer, line items, currency, total, discount and quote version
Positive outcome	State may move to Approved
Negative outcome	Rejected or Returned with reason
Escalation target	One business day
Escalation recipient	Sales operations
Stop condition	Approval decision recorded or request returned
The finance escalation should contain:
Configuration item	Value
Start event	State enters Ready for Finance
Target	One business day
Escalation recipient	Finance team lead
Stop condition	Finance Accepted or Returned
Escalation evidence	Escalation timestamp, owner and reason
4.7 Test cases
These are expected simulated results, not actual product observations.
Test ID	Scenario	Expected result
B-01	Manager approves MER-QUOTE-001	State becomes Approved; sales can send it
B-02	Sales attempts to send MER-QUOTE-001 while approval is pending	Transition is denied
B-03	MER-QUOTE-002 attempts finance handoff with blank currency	Transition is denied or returned with missing-currency reason
B-04	MER-QUOTE-003 attempts approval submission with no customer ID	Submission is denied; missing field is shown
B-05	MER-QUOTE-004 attempts to proceed while duplicate review is pending	Transition is denied; duplicate review remains open
B-06	Approval remains pending beyond one business day	Escalation notification and task are created
B-07	Finance returns a handoff	State becomes Returned; reason and correction owner are recorded
B-08	Sales representative attempts to approve their own quote	Action is denied if separation of duties is configured
4.8 Mistake and correction
Mistake: A workflow changes Status directly from Awaiting Approval to Approved when the quote is submitted.
Why it is wrong: Submission is a request for approval, not a positive approval decision. The workflow bypasses the approver.
Correction: The workflow may notify the sales manager and create an approval task, but only the approval outcome or authorised Blueprint transition may move the record to Approved.
A second mistake is treating Ready for Finance as Finance Accepted. The correction is to maintain separate states and require finance evidence before entering Finance Accepted.
5. Try it yourself — guided practice
Learning goal
Implement and test a controlled quote process with an approval route and exception paths.
Required access
You need:
- permission to create or edit fields;
- permission to configure a Blueprint or equivalent controlled process;
- permission to configure an approval route;
- permission to create tasks, notifications and escalations;
- test records and synthetic recipients;
- access to process or record history.
Complete sample inputs
Quote ID	Customer ID	Discount	Currency	Line items	Total	Current state	Approval	Handoff ready
MER-QUOTE-101	MER-CUST-101	12%	USD	Complete	6400.00	Draft	Not submitted	Yes
MER-QUOTE-102	MER-CUST-102	8%	USD	Complete	2800.00	Draft	Not required	Yes
MER-QUOTE-103	Blank	15%	USD	Incomplete	5100.00	Draft	Not submitted	No
MER-QUOTE-104	MER-CUST-104	14%	USD	Complete	7200.00	Awaiting Approval	Pending	Yes
MER-QUOTE-105	MER-CUST-105	9%	Blank	Complete	3900.00	Customer Accepted	Not required	No
Synthetic roles:
- Sales representative: Jordan
- Sales manager: sales-manager@example.com
- Sales operations: sales-operations@example.com
- Finance team lead: finance-lead@example.com
Practice rules
1. Quotes with a discount greater than 10% require manager approval.
2. Quotes with a discount of 10% or less may bypass manager approval only when all quote fields are complete.
3. Currency, customer ID, line items and total are mandatory before approval submission or sending.
4. A quote cannot be sent while approval is pending.
5. Finance handoff requires customer ID, quote ID, currency, total, line items and duplicate decision.
6. Approval overdue after one business day escalates to sales operations.
7. Finance handoff overdue after one business day escalates to the finance team lead.
8. Rejected or returned quotes need a reason and correction owner.
Guided steps and expected results
Step 1: Define states
Create a state list containing at least:
Draft
Awaiting Approval
Approved
Sent
Customer Accepted
Ready for Finance
Finance Accepted
Returned
Rejected
Escalated
Expected result: Every supplied record can be placed in one state.
Step 2: Define transitions
Create a transition table with source, target, permitted role, criteria, mandatory fields and evidence.
Expected result: Sending a quote while approval is pending is not an available permitted transition.
Step 3: Configure mandatory information
Set the required information for approval submission and finance handoff.
Expected result: MER-QUOTE-103 cannot be submitted because the customer ID and line items are incomplete. MER-QUOTE-105 cannot move to finance because currency is blank.
Step 4: Configure approval
Configure approval for discounts greater than 10%.
Expected result: MER-QUOTE-101 and MER-QUOTE-104 require approval. MER-QUOTE-102 and MER-QUOTE-105 do not require this approval.
Step 5: Configure escalation
Use the request or state-entry timestamp as the escalation anchor.
Expected result: MER-QUOTE-104, submitted at 2026-10-10 09:00, is overdue after one business day if no decision is recorded.
Step 6: Test permissions
Test Jordan attempting to approve MER-QUOTE-101.
Expected result: The action is denied if only sales managers may approve.
Step 7: Test return and recovery
Return MER-QUOTE-105 for missing currency. Add the currency, record the correction owner and resubmit.
Expected result: The record cannot move to Ready for Finance before correction and can proceed after the required information is present.
Safe cleanup
Deactivate or remove only synthetic practice rules and records after recording the test result. Do not delete live Blueprints, approvals or business records. If shared test fields were created, document whether they are needed by another learner before removing them.
Offline alternative
Use a spreadsheet to evaluate state and transition rules, but recognize its limit: it cannot prove that a Zoho user was denied a transition, that an approval was recorded in product history or that an escalation executed.
6. Independent challenge
Controlled service-credit approval process
Meridian sometimes offers a service credit after an installation or support issue. Design a separate controlled process for approving that credit. This is a learning scenario and does not establish a universal customer-compensation policy.
Scenario rules
- A service credit request starts in Draft.
- A credit greater than 5% of the related order value requires service manager approval.
- A credit of 5% or less requires service lead review.
- The request must include customer ID, related quote or order reference, issue summary, requested percentage, order value and evidence reference.
- A request cannot be approved by its requester.
- A request returned for correction must include a reason and owner.
- A request pending for two business days is escalated to the service operations lead.
- Approved credits are sent to finance for recording; finance acceptance is a separate state.
- The service-credit process is separate from the HR process.
Complete input data
Credit ID	Customer ID	Quote/order reference	Requested credit	Order value	Evidence reference	Current state	Requester
MER-CREDIT-201	MER-CUST-001	MER-QUOTE-001	4%	4820.00	Installation note INST-201	Draft	Service Agent A
MER-CREDIT-202	MER-CUST-002	MER-QUOTE-002	8%	3900.00	Ticket note TCK-202	Draft	Service Manager
MER-CREDIT-203	Blank	MER-QUOTE-003	3%	2500.00	Blank	Draft	Service Agent B
MER-CREDIT-204	MER-CUST-004	MER-QUOTE-004	7%	6200.00	Ticket note TCK-204	Awaiting Approval	Service Agent C
MER-CREDIT-205	MER-CUST-005	MER-QUOTE-005	4%	3000.00	Installation note INST-205	Returned	Service Agent D
Deliverables
Create:
1. a state model;
2. a transition matrix;
3. an approval and review design;
4. mandatory information rules;
5. a two-business-day escalation rule;
6. an access matrix;
7. test cases for normal approval, service-lead review, missing data, self-approval, rejection, return and finance acceptance;
8. expected results without claiming actual product execution.
Success criteria
Your design should:
- route requests above 5% to service manager approval;
- route requests at or below 5% to service lead review;
- prevent MER-CREDIT-203 from being submitted because customer ID and evidence are missing;
- prevent the requester from approving their own request;
- identify the escalation for MER-CREDIT-204;
- keep finance acceptance separate from service approval;
- provide a correction route for MER-CREDIT-205.
7. Common problems and recovery
Symptom	Diagnosis	Correction	Verification
Users can move a quote directly from Draft to Sent	The Blueprint has an unguarded transition or workflow bypass	Remove the direct path or require the correct approval state	Test a high-discount quote
Approval is requested with missing customer or currency	Mandatory information is applied too late	Require fields before approval submission	Submit an incomplete test quote
The requester can approve their own quote	Approver eligibility is not separated from requester identity	Configure an authorised approver rule or manual review	Test with the same requester and approver
A rejection has no reason	Rejection transition lacks mandatory explanation	Require rejection reason and next owner	Reject a test record and inspect evidence
Returned records cannot be corrected	The return state has no transition back to an editable state	Add a correction route and owner	Correct and resubmit a returned record
Approval escalation repeats continuously	Escalation has no sent marker or stop condition	Add escalation state, timestamp or maximum escalation rule	Leave a test approval overdue and count escalation actions
Finance accepts a record that was never approved	Finance transition does not check prior state or approval evidence	Require Approved, Sent and Customer Accepted prerequisites	Attempt the transition from Draft
Workflow field update bypasses the Blueprint	Workflow and controlled states write to the same field	Limit workflow to notifications/tasks or invoke only permitted transitions	Edit a record and inspect state history
A user can see a transition but receives a permission error	Transition visibility and transition permission differ	Review role, profile and field permissions	Test the action with each role
Escalation occurs after the request was rejected	Timer is not cancelled or the execution guard is absent	Cancel or guard the escalation after terminal outcomes	Reject before the due time
A product feature is assumed to support a journey	Edition or module support was not verified	Record it as a candidate and verify official documentation	Complete a capability check before design approval
Approval history does not identify the quote version	Quote data can change while approval is pending	Lock relevant fields or record a version at submission	Change the discount after submission and test
Finance return is treated as rejection	Return and rejection meanings were not separated	Define each state and recovery route	Test both outcomes with different reasons
When recovering from an incorrect transition, preserve the original decision evidence. Add a correction or reversal rather than deleting history.
8. Check your understanding
 1. What is the difference between a state and a field?
 2. What information should a transition specification contain?
 3. Why should Ready for Finance and Finance Accepted be separate states?
 4. Which Meridian quotes require manager approval under the synthetic 10% rule?
 5. Why is a return different from a rejection?
 6. What event should start the approval escalation timer?
 7. How can a workflow bypass a Blueprint?
 8. What should happen when the requester and approver are the same person?
 9. Why must a returned record have a correction owner?
10. What makes a CommandCenter scenario a candidate rather than a confirmed supported configuration?
11. Can MER-QUOTE-002 move to Finance Accepted if its currency is blank?
12. What evidence should exist after a finance acceptance?
13. Why should escalation have a stop condition?
14. Which tool is most appropriate for preventing an unapproved quote from being sent: a notification, a Blueprint transition or an unrelated field update? Explain.
15. How should an actual test result be labelled if the product was not executed?
9. Solutions and explanations
9.1 Answers to the checks
 1. A state is a controlled phase in a process. A field stores information about the record. A state should have defined transitions and permissions; a field may support those decisions.
 2. It should contain source state, target state, permitted role, entry criteria, mandatory information, actions, exit criteria, evidence and exception route.
 3. Ready for Finance means sales has prepared a complete handoff. Finance Accepted means the receiving finance role accepted it. Combining them would make a transfer attempt look like a completed handoff.
 4. MER-QUOTE-001 at 12% and MER-QUOTE-003 at 15% require manager approval. MER-QUOTE-002 at 8% does not require this approval, although its missing currency blocks later progress. MER-QUOTE-004 at 14% requires approval but is first blocked by duplicate review.
 5. A return means the request may proceed after correction. A rejection means the current proposal should not proceed. They need different reasons, evidence and recovery paths.
 6. The timer should start when the approval request enters Awaiting Approval, using the recorded state-entry or submission timestamp.
 7. A workflow can directly update the state field or trigger an uncontrolled action that makes a later state appear valid. Restrict workflow actions and require controlled transitions for state movement.
 8. The action should be denied if separation of duties is required. The request should be routed to an authorised approver.
 9. Without a correction owner, the record can remain returned indefinitely and no one is responsible for resolving it.
10. It is a candidate until the current edition, module, permissions, wait behavior, actions, connections and execution history are verified.
11. No. Currency is mandatory for the finance handoff, so the record should be returned or blocked before finance acceptance.
12. Evidence may include finance approver, finance acceptance timestamp, finance reference, acceptance comment and the state transition history.
13. Without a stop condition, a completed, rejected or returned request can continue generating escalation tasks and notifications.
14. A Blueprint transition is most appropriate because it can control who may move the record and what information must exist. A notification only informs someone, and a field update alone does not establish authorised movement.
15. It should be labelled Not executed, Expected simulated result or Actual observation only when the product test was really performed.
9.2 Guided practice sample solution
State model
Draft
  ├── discount > 10% → Awaiting Approval
  ├── discount <= 10% and complete → Sent
  └── incomplete → remains Draft

Awaiting Approval
  ├── approved → Approved
  ├── returned → Returned
  ├── rejected → Rejected
  └── overdue → Escalated

Approved → Sent
Sent → Customer Accepted
Customer Accepted
  ├── complete → Ready for Finance
  └── incomplete → Returned

Ready for Finance
  ├── finance accepts → Finance Accepted
  ├── finance returns → Returned
  └── overdue → Escalated
Transition register
Transition	Role	Conditions	Mandatory information
Submit for approval	Sales representative	Discount greater than 10%; quote complete	Customer, currency, line items, total, discount and version
Send standard quote	Sales representative	Discount 10% or less; quote complete	Customer, currency, line items and total
Approve	Sales manager	Pending approval; requester and approver are different	Decision and comment
Return	Sales manager or finance processor	Correction needed	Reason and correction owner
Record acceptance	Sales representative	State Sent	Acceptance evidence and timestamp
Submit finance handoff	Sales representative	State Customer Accepted; all handoff fields complete	Customer ID, quote ID, currency, total, line items and duplicate decision
Accept finance handoff	Finance processor	State Ready for Finance	Finance reference and acceptance comment
Applying the rules to the practice data
Quote	Expected route	Explanation
MER-QUOTE-101	Awaiting Approval	Discount is 12%; the quote is complete
MER-QUOTE-102	Sent	Discount is 8% and the quote is complete
MER-QUOTE-103	Remains Draft	Customer ID and line items are missing
MER-QUOTE-104	Escalated if no decision after one business day	Approval has been pending since 2026-10-10 09:00
MER-QUOTE-105	Returned	Currency is missing despite customer acceptance
Escalation calculation
For MER-QUOTE-104:
Approval submitted: 2026-10-10 09:00
Target: one business day
Expected escalation: after the defined one-business-day period
The exact clock time depends on the organisation’s business calendar and time-zone configuration. The design must record those settings before claiming an actual due time.
Permission test
Jordan is the sales representative and cannot approve MER-QUOTE-101. The expected result is a denied approval action. A sales manager must approve, return or reject the quote.
Correction route for MER-QUOTE-105
1. Return the quote with reason Currency missing.
2. Assign the correction to the quote owner.
3. Add the correct currency.
4. Revalidate the quote.
5. Resubmit or move through the permitted standard path.
6. Record the new transition evidence.
9.3 Independent challenge sample solution
State model
Draft
  ├── complete and <= 5% → Awaiting Service Lead Review
  ├── complete and > 5% → Awaiting Service Manager Approval
  └── incomplete → Returned for Correction

Awaiting Service Lead Review
  ├── approve → Approved
  ├── return → Returned for Correction
  └── overdue → Escalated

Awaiting Service Manager Approval
  ├── approve → Approved
  ├── reject → Rejected
  ├── return → Returned for Correction
  └── overdue → Escalated

Approved → Ready for Finance
Ready for Finance
  ├── finance accepts → Finance Accepted
  ├── finance returns → Returned for Correction
  └── overdue → Escalated
Applying the challenge data
Credit ID	Expected route	Explanation
MER-CREDIT-201	Awaiting Service Lead Review	Credit is 4%, at or below 5%; required fields are present
MER-CREDIT-202	Awaiting Service Manager Approval	Credit is 8%, above 5%
MER-CREDIT-203	Remains Draft or moves to Returned for Correction	Customer ID and evidence reference are missing
MER-CREDIT-204	Escalated if no decision after two business days	Manager approval has been pending
MER-CREDIT-205	Returned for Correction	It already has a correction-required outcome
Access matrix
Role	Create request	Edit own draft	Review or approve	View confidential evidence
Service agent	Yes	Yes	No	View required service evidence
Service lead	Yes	Yes	Review credits up to 5%	Yes for assigned cases
Service manager	Yes	Yes	Approve credits above 5%	Yes
Service operations lead	Yes	Limited correction	Escalation review	Yes for escalated cases
Finance processor	No	No	No	View finance-required evidence
Sales representative	No	No	No	No access to service-credit records
Mandatory information
The request cannot enter a review state without:
- customer ID;
- quote or order reference;
- issue summary;
- requested percentage;
- order value;
- evidence reference;
- requester;
- correction owner when returned.
The requester must not be the approving role. A service manager may approve a request submitted by a service agent, but not their own request if separation of duties is required.
Escalation
MER-CREDIT-204 is in Awaiting Service Manager Approval. Its escalation starts when that state was entered. If the state remains unchanged for two business days, the service operations lead receives an escalation and task.
If the request is rejected before the timer expires, the escalation should stop. If the request is returned for correction, the organisation must decide whether the timer restarts after resubmission or continues from the original request. That decision should be documented and tested.
Finance handoff
An approved credit should enter Ready for Finance, not Finance Accepted. Finance must independently accept the handoff and provide a finance reference. A notification or field update is not sufficient evidence of finance acceptance.
10. Chapter recap and next step
A controlled process needs more than labels and notifications. It needs states, authorised transitions, mandatory information, approval outcomes and recovery paths.
You should now be able to:
- define the meaning of every process state;
- distinguish a state from a supporting field;
- specify source state, target state, role, criteria and evidence for a transition;
- define mandatory information at the correct transition;
- separate approval, review, rejection and return outcomes;
- prevent self-approval where separation of duties is required;
- create an escalation with a start event, target, owner and stop condition;
- distinguish workflow, Blueprint, approval and journey responsibilities;
- identify CommandCenter scenarios that require edition and capability verification;
- test permitted, denied, incomplete, rejected, returned and escalated routes;
- preserve a separate finance acceptance state;
- document expected results without presenting them as actual observations.
For the Meridian Supply project, this chapter produces:
C01_CH10_Meridian_Controlled_Process_State_Model
C01_CH10_Meridian_Transition_and_Approval_Register
C01_CH10_Meridian_Escalation_and_Exception_Matrix
C01_CH10_Meridian_Blueprint_Test_Evidence
The next chapter builds on these controlled states by examining guided screens, layouts, wizards, Kiosk Studio and user actions. A guided screen should help a user complete a valid transition; it should not hide the mandatory information or bypass the approval route.
11. Glossary and further reading
Glossary
Term	Definition
Approval	An authorised decision that permits, rejects or returns a request
Blueprint	A controlled process model that restricts movement between defined states
CommandCenter	A Zoho orchestration capability used to coordinate stages, actions, waits and conditions where supported
Entry criteria	Conditions that must be true before a transition or state entry can begin
Escalation	A higher-level action taken when a required decision or task is overdue
Exit criteria	Conditions and evidence required for a transition to complete
Journey orchestration	Coordination of multiple activities, waits, conditions and outcomes across a longer process
Mandatory information	Data that must be present and valid before a transition can proceed
Review	Examination or classification of a record that may produce approval, return or another outcome
State	A controlled phase of a record’s lifecycle
Transition	An authorised movement from one state to another
Workflow	Conditional automation that performs actions when a trigger and criteria are satisfied
Further reading
Check the current edition, product permissions and supported modules before implementing a Blueprint, approval, escalation or CommandCenter journey:
- Zoho CRM Help (https://help.zoho.com/portal/en/kb/crm)
- Zoho CRM automation help (https://help.zoho.com/portal/en/kb/crm/automate-business-processes)
- Zoho CRM process-management help (https://help.zoho.com/portal/en/kb/crm/automate-business-processes)
- Zoho CRM developer documentation (https://www.zoho.com/crm/developer/docs/)
- Zoho CommandCenter information (https://www.zoho.com/commandcenter/)
This chapter has not verified current product screens, edition limits, CommandCenter capability, timer behavior or permission names. Treat the test results as expected simulated results until the configured product environment records actual observations.
continuity:
  previous_continuity:
    supplied: "C01-CH09"
    source_artifacts:
      - "C01_CH09_Meridian_Workflow_Register_and_Test_Matrix"
      - "C01_CH09_Meridian_Field_and_Action_Dictionary"
      - "C01_CH09_Meridian_Exception_Recovery_Record"
    note: "Continuity from C01-CH02 through C01-CH08 was not supplied; no decisions from those chapters are assumed."
  record_ids:
    inherited:
      - MER-ENQ-001
      - MER-CUST-001
      - MER-QUOTE-001
      - MER-ENQ-002
      - MER-ENQ-003
      - MER-ENQ-004
      - MER-CUST-002
      - MER-QUOTE-002
      - MER-ENQ-101
      - MER-ENQ-102
      - MER-ENQ-103
      - MER-ENQ-104
      - MER-ENQ-105
      - MER-ENQ-201
      - MER-ENQ-202
      - MER-ENQ-203
      - MER-ENQ-204
      - MER-ENQ-205
    added_for_blueprint_practice:
      - MER-QUOTE-003
      - MER-QUOTE-004
      - MER-QUOTE-101
      - MER-QUOTE-102
      - MER-QUOTE-103
      - MER-QUOTE-104
      - MER-QUOTE-105
      - MER-CREDIT-201
      - MER-CREDIT-202
      - MER-CREDIT-203
      - MER-CREDIT-204
      - MER-CREDIT-205
  case_decisions:
    - "A workflow may notify, create tasks or update supporting fields, but it must not bypass a controlled approval transition."
    - "A discount greater than 10% requires synthetic sales manager approval."
    - "A quote cannot be sent while required approval is pending."
    - "Ready for Finance is separate from Finance Accepted."
    - "Finance acceptance requires receiving evidence and a finance reference."
    - "An approval overdue after one business day escalates to sales operations."
    - "A finance handoff overdue after one business day escalates to the finance team lead."
    - "Returned and rejected outcomes have different meanings and recovery paths."
    - "CommandCenter scenarios and product support remain subject to current edition and permission verification."
  artifacts:
    - "C01_CH10_Meridian_Controlled_Process_State_Model"
    - "C01_CH10_Meridian_Transition_and_Approval_Register"
    - "C01_CH10_Meridian_Escalation_and_Exception_Matrix"
    - "C01_CH10_Meridian_Blueprint_Test_Evidence"
  open_case_assumptions_next_chapter:
    - "The exact current Zoho CRM Blueprint, approval and CommandCenter capabilities have not been verified."
    - "The next chapter should use these state and transition rules when designing guided screens and user actions."
    - "The finance acceptance event, finance reference and approval history must remain separate from automated notifications."
    - "Any journey timer, cancellation behavior, escalation limit or cross-application connection must be tested in the selected edition."
END OF C01-CH10
