# Cross-Application Automation with Flow

1. What you will learn
A connected business process often crosses application boundaries. Sales may work in CRM, finance may work in Books and service may work in Desk. Someone must transfer the right information, identify the receiving record and recover when the transfer fails.
Flow is used in this chapter as a cross-application automation capability. A flow receives a trigger, performs actions, evaluates conditions, maps data and records an execution result.
You will learn to:
- distinguish event, polling, scheduled, email and webhook triggers;
- select a trigger that matches the source event;
- configure actions and conditions;
- design branches for success, missing data and failure;
- map records and fields between applications;
- configure connections with appropriate access;
- inspect execution history;
- distinguish data failure, permission failure and temporary connection failure;
- recover a failed handoff without creating duplicate customers, orders or invoices;
- build and test a CRM-to-Books handoff flow for Meridian Supply.
This chapter continues the finance handoff from Chapter 13. The supplied continuity establishes:
- CRM is the source for synthetic sales quotes and commercial approvals;
- Books is the source for finance customers, items, invoices, payments and receivables;
- MER-QUOTE-101 has an approved total of USD 5,984.00;
- the approved discount is USD 816.00;
- source and target business IDs must remain distinct;
- a missing discount mapping caused a previous invoice discrepancy;
- synchronisation states must distinguish Sent, Accepted, Failed and Reconciled.
No live Flow, CRM or Books execution has been verified. Exact trigger types, connector actions, supported modules, connection permissions, retry behavior and execution-history fields depend on the current product edition and configuration.
2. Lessons
2.1 What is a cross-application flow?
A cross-application flow connects an event in one application to actions in one or more applications.
A simple flow can be described as:
Trigger
  → retrieve source data
  → validate conditions
  → map fields
  → perform target action
  → record result
  → notify or recover when necessary
For Meridian:
CRM finance handoff becomes Ready
  → retrieve quote and line items
  → find Books customer and items
  → validate currency and totals
  → create or update finance order
  → write target reference back to CRM
  → notify finance
A flow is not just a connection. A connection supplies authenticated access; the flow defines what should happen with that access.
Flow versus workflow
Capability	Workflow	Cross-application flow
Main scope	Usually one application or module	Two or more applications or services
Example	Create a CRM task after a quote is sent	Send an accepted quote from CRM to Books
Main concern	Trigger, criteria and actions	Trigger, connections, mappings, target responses and failures
Failure evidence	Record or action history	Multi-step execution history
Recovery	Correct record or rule	Correct mapping, connection or target record, then retry safely
A flow should not duplicate a Blueprint, approval or finance process. It should transport and coordinate information while respecting the source and target controls.
Check your understanding
Why is a successful connection not proof that a flow is correctly configured?
Answer: A connection only provides access. The flow may still have incorrect triggers, mappings, criteria, permissions, duplicate behavior or target actions.
2.2 Trigger types
The trigger determines how a flow starts. Choose the trigger based on the source system’s behavior and the business requirement.
Event trigger
An event trigger starts when a source event occurs, such as:
- a record is created;
- a record is updated;
- a state changes;
- a payment is recorded;
- a webhook event is received.
Example:
Start when CRM Finance Handoff Status changes to Ready.
An event trigger is suitable when the source can reliably emit the relevant event.
Polling trigger
A polling trigger checks a source periodically for new or changed records.
Example:
Every 15 minutes, find Books payments created or changed since the last successful check.
Polling may be useful when the source does not provide the required event. It needs:
- a cursor or last-processed timestamp;
- a unique record or event ID;
- a way to avoid processing the same record repeatedly;
- a plan for records changed during the polling interval.
Polling frequency, limits and supported source operations must be verified.
Scheduled trigger
A scheduled trigger runs at a planned time rather than in response to one source record.
Examples:
- nightly reconciliation of CRM and Books totals;
- weekly search for failed handoffs;
- monthly review of records stuck in Sent.
A scheduled flow must define:
- time zone;
- schedule;
- population of records;
- processing order;
- overlap behavior;
- result summary;
- failure notification.
Email trigger
An email trigger starts when a monitored mailbox receives a message that meets defined conditions.
Possible uses include:
- receiving a structured remittance advice;
- capturing a supplier document;
- receiving a finance exception message.
Do not treat every email as trusted structured data. Validate:
- sender;
- subject or reference;
- required identifiers;
- amount and currency;
- attachment or message format;
- duplicate message ID.
An email trigger should send uncertain messages to review rather than creating an invoice or payment automatically.
Webhook trigger
A webhook trigger starts when another system sends an HTTP event to a configured endpoint.
Possible uses include:
- payment provider notification;
- delivery confirmation;
- external form submission;
- partner system status event.
A webhook design should address:
- event ID;
- source identity;
- authentication or signature verification where supported;
- timestamp;
- replay or duplicate delivery;
- payload validation;
- response behavior.
Do not mark a payment as settled merely because an unverified webhook contains the word “paid.”
Trigger comparison
Trigger	Best use	Main risk	Required control
Event	Immediate response to a reliable source event	Source event is too broad or not emitted	Specific event and criteria
Polling	Source has no suitable event	Duplicates or missed records	Cursor and idempotent processing
Scheduled	Periodic reconciliation or review	Overlapping runs or large populations	Run lock, scope and summary
Email	Structured messages from a controlled mailbox	Untrusted or inconsistent content	Sender, reference and field validation
Webhook	Near-real-time external events	Spoofed, duplicated or replayed events	Authentication, event ID and deduplication
Check your understanding
Meridian needs to send an accepted CRM quote to Books immediately after the handoff state changes. Which trigger is the first candidate?
Answer: An event trigger based on the specific CRM state change is the first candidate, provided the source and selected edition reliably support that event.
2.3 Actions, conditions and branching
A flow action performs work after the trigger.
Common actions include:
- find or retrieve a record;
- create a record;
- update a record;
- send an email;
- create a task;
- call a webhook;
- wait or delay where supported;
- write an execution or correlation reference;
- notify an exception owner.
A condition evaluates information. A branch chooses what happens next.
Meridian branch design
Is the finance handoff Ready?
  ├── No → do not process; record not eligible
  └── Yes
       Is customer mapping present?
         ├── No → blocked branch
         └── Yes
              Are all item mappings present?
                ├── No → failed-data branch
                └── Yes
                     Does target correlation ID already exist?
                       ├── Yes → update existing target
                       └── No → create target record
A branch should have a defined outcome. Avoid a branch that simply ends without recording why.
Normal and exception branches
Branch	Condition	Action	Result
Success	All required records and mappings exist	Create or update target	Target reference written back
Missing customer	Customer mapping absent	Set sync status Blocked; notify owner	No target transaction created
Missing item	One or more item mappings absent	Set sync status Failed - Mapping; create exception	No partial target transaction
Duplicate target	Correlation ID already exists	Update or inspect existing target	No duplicate transaction
Permission failure	Connection cannot perform target action	Notify administrator; stop	No false success
Temporary failure	Connection or service unavailable	Record failure; retry according to policy	No uncontrolled repeat
A flow should fail safely. “Do nothing” is not a sufficient exception outcome when a finance handoff is waiting.
Check your understanding
What should happen when one of three quote line items has no Books item mapping?
Answer: The flow should hold or fail the handoff, identify the missing mapping and avoid creating a partial order or invoice. After the mapping is corrected, the same correlation ID can be retried safely.
2.4 Mapping records and fields
A mapping connects source data to target data. It may include transformation.
Mapping categories
- Direct mapping: CRM Quote ID → Books reference.
- Lookup mapping: CRM Customer ID → Books customer record found by business ID.
- Transformation: Numeric percentage 12 → formatted discount 12%, if the target requires that format.
- Default value: A known source value fills a target field only when the business rule permits it.
- Conditional mapping: Tax field is mapped only when the source contains an approved tax value.
- Aggregation: Several line values are combined into a subtotal.
- Validation mapping: A source value is checked before being sent.
Never use a default to conceal missing information. For example, assigning USD to every blank currency field is unsafe unless the business rule explicitly establishes USD as the only permitted currency and the source blank is impossible.
Meridian flow map
Source application	Source field	Target application	Target field	Rule
CRM	MER-QUOTE-101	Books	Transaction reference	Preserve quote ID
CRM	MER-CUST-101	Books	Customer code	Find mapped customer
CRM	Product ID	Books	Item code	Find every item mapping
CRM	Quantity	Books	Line quantity	Must be positive
CRM	Applied unit price	Books	Line rate	Preserve approved price
CRM	Discount amount	Books	Discount value	Map amount and basis
CRM	Currency	Books	Currency	Exact permitted code
Books	Target order ID	CRM	Finance reference	Write after success
Flow	Correlation ID	CRM and Books	Sync reference	Prevent duplicate creation
Flow	Error message	CRM	Sync error	Record actionable reason
Correlation IDs
A correlation ID links one business event across applications.
For the finance handoff:
Correlation ID = MER-HO-101
Source quote = MER-QUOTE-101
Target order = MER-ORDER-101
If the flow runs again, it should search for MER-HO-101 before creating a second order.
A correlation ID is different from a product-generated execution ID. The execution ID identifies one run; the correlation ID identifies the business event.
Check your understanding
Why should a retry search for an existing correlation ID before creating a new Books order?
Answer: The first run may have created the target record but failed before writing the target ID back to CRM. Searching by correlation ID prevents a retry from creating a duplicate order.
2.5 Connections and permissions
A connection authenticates a flow to an application or service. It should be owned and maintained by a responsible organisation role, not by an individual’s personal account without a support plan.
Connection design should define:
- application;
- connection owner;
- permitted operations;
- modules or records accessible;
- environment;
- credential renewal responsibility;
- deactivation process;
- test and production separation.
Least-privilege examples
Connection	Needed access	Unnecessary access
CRM source connection	Read quotes and customers; update sync fields	Delete customers
Books target connection	Search customers and items; create or update approved transaction	Delete invoices or change tax configuration
Email connection	Read a controlled mailbox; send internal exception notices	Read unrelated personal mailboxes
Webhook connection	Receive or call a defined endpoint	Access unrelated APIs
A connection can be valid while the action is not permitted. For example, a user may connect to Books but lack permission to create orders or update invoices.
Connection recovery
If a connection expires:
1. identify the affected flow and time period;
2. do not create a new connection with broader permissions just to make it run;
3. renew or replace it with the authorised owner;
4. identify records that arrived during the outage;
5. retry using correlation IDs;
6. inspect for partial target creation;
7. document the recovery.
Check your understanding
Why should a CRM-to-Books flow not use a connection that can delete invoices?
Answer: The flow does not need deletion capability. Excess permission increases the impact of a configuration error or compromised connection.
2.6 Execution history
Execution history shows what happened during a flow run. Useful information includes:
- execution or run ID;
- correlation ID;
- trigger time;
- completion time;
- status;
- step name;
- source record;
- target record;
- branch taken;
- mapped values;
- error message;
- retry count;
- connection used.
A successful run should still be inspected during testing. “Completed” may mean the flow reached its last step, not that the target record has the intended values.
Execution status
Status	Meaning
Received	Trigger was received
Running	Steps are being evaluated or executed
Completed	Configured actions finished according to the platform
Blocked	Business condition prevented processing
Failed	An action or connection failed
Retried	A later attempt was made
Reconciled	Source and target were compared and accepted
Do not place full payment credentials, sensitive personal data or confidential documents into an error message. Store only what is needed to diagnose the problem.
Failed-run categories
Failure type	Example	Recovery
Data	Missing customer or item mapping	Correct source or mapping, then retry
Permission	Connection cannot create target record	Correct connection role, then retry
Temporary	Target service unavailable	Retry after service recovery
Duplicate	Target record already exists	Search and update existing record
Transformation	Currency or amount has invalid format	Correct mapping and validate
Business rejection	Target refuses an invalid transaction	Follow target correction route
Configuration	Wrong branch or field	Fix flow, test new run, review affected records
A retry is safe only when the flow is idempotent or the target has been checked for partial completion.
Check your understanding
A flow run failed after creating a Books order but before updating CRM. What must happen before retrying?
Answer: Search Books using the correlation ID and source quote reference. If the order exists, update it or write the target reference back to CRM rather than creating a second order.
2.7 Configuring a cross-application flow
This is an edition-neutral procedure. Exact product screens, connector operations and action names must be verified.
Required access
You need:
- permission to create and activate flows;
- CRM read and sync-field update access;
- Books customer, item and transaction access;
- permission to create or manage connections;
- access to execution history;
- test records and synthetic recipients;
- authority to correct mappings or assign exceptions.
Procedure
 1. Define the business event.
Example: CRM finance handoff changes to Ready.
Expected result: The flow has one unambiguous starting event.
 2. Create or confirm connections.
Use separate test connections where possible.
Expected result: Each connection has an owner and only the required permissions.
 3. Choose the trigger.
Select event, polling, scheduled, email or webhook based on the source behavior.
Expected result: The trigger has a scope, source and deduplication method.
 4. Retrieve source records.
Obtain customer, quote, line items, currency, discount, totals and correlation ID.
Expected result: The flow has all required source information before target creation.
 5. Validate conditions.
Check state, required fields, mappings, currency and approval.
Expected result: Invalid records follow an explicit blocked branch.
 6. Map fields and records.
Use business IDs and controlled transformations.
Expected result: Every target field has a source, transformation or documented reason for being blank.
 7. Check for an existing target.
Search by correlation ID or source reference.
Expected result: Retry cannot create a duplicate target transaction.
 8. Create or update the target.
Perform the Books action only after validation.
Expected result: The target record is created or updated with the expected amount and references.
 9. Update the source.
Write target reference and sync status back to CRM.
Expected result: Sales can see whether the handoff is sent, accepted, blocked or failed.
10. Notify or escalate.
Send success or exception information to the correct owner.
Expected result: No failure ends without an owner.
11. Test execution history.
Run normal, missing-data, duplicate, permission and failed-action tests.
Expected result: Each run has an identifiable outcome.
12. Activate and document.
Record flow owner, connections, mappings, retry policy and support route.
Expected result: A future administrator can diagnose and safely change the flow.
3. Visual explanation
flowchart TD
    A[CRM handoff event] --> B[Retrieve quote, customer and line items]
    B --> C{Handoff state and approval valid?}
    C -- No --> D[Block and record business exception]
    C -- Yes --> E[Find customer and item mappings]
    E --> F{All mappings present?}
    F -- No --> G[Failed-data branch and correction task]
    F -- Yes --> H[Search target by correlation ID]
    H --> I{Target already exists?}
    I -- Yes --> J[Update or reconcile existing target]
    I -- No --> K[Create Books transaction]
    K --> L{Target action successful?}
    L -- No --> M[Record failed run and recovery owner]
    L -- Yes --> N[Write target reference to CRM]
    N --> O[Notify finance and record sent status]
The diagram shows why a flow should validate before creating a target record. It also shows why retry logic needs a duplicate check.
4. Worked case: CRM-to-Books handoff flow
4.1 Scenario assumptions
The following rules are new for this chapter:
- The flow starts when a CRM finance handoff changes to Ready.
- The source record contains correlation ID MER-HO-101.
- The flow must not set Finance Accepted. It may set Flow Sync Status = Sent after the target action succeeds.
- A target order is created only after customer and item mappings are valid.
- A retry searches for the correlation ID before creating a new target.
- A missing mapping is a data failure, not a connection failure.
- All amounts are in USD and tax is excluded.
- The flow uses internal synthetic notifications.
- These are design assumptions; no live flow execution is claimed.
4.2 Source record
Field	Value
CRM quote	MER-QUOTE-101
CRM customer	MER-CUST-101
Correlation ID	MER-HO-101
Finance handoff status	Ready
Flow sync status	Not started
Currency	USD
Approved total	5,984.00
Approval	Approved
Customer acceptance	Recorded
Duplicate review	Not a duplicate
Target order reference	Blank
Line items:
Product ID	Quantity	Applied unit price	Discount
MER-PROD-WS-001	10	520.00	0%
MER-PROD-INST-001	1	1,200.00	0%
MER-PROD-SUP-001	1	400.00	0%
Quote discount:
6,800.00 × 0.12 = USD 816.00
Approved total:
6,800.00 − 816.00 = USD 5,984.00
4.3 Flow design
Step	Action	Expected result
1	Receive CRM handoff event	Flow receives MER-HO-101
2	Retrieve quote and line items	All three lines and approved total are available
3	Validate state and approval	Record is eligible
4	Find CRM customer mapping	MER-CUST-101 maps to MER-BOOK-CUST-101
5	Find item mappings	All three products map to Books items
6	Search by correlation ID	No duplicate target is found in the isolated test run
7	Create or update Books order	Target amount is USD 5,984.00
8	Write target reference to CRM	Flow Sync Status becomes Sent; target reference is stored
9	Notify finance	Finance receives an internal handoff message
10	Record execution result	Run ID, correlation ID and target ID are available
4.4 Failed handoff case
A second synthetic handoff contains:
Field	Value
CRM quote	MER-QUOTE-FLOW-102
Correlation ID	MER-HO-102
Customer	MER-CUST-102
Product lines	Workstation and docking station
Finance handoff status	Ready
Flow sync status	Not started
Currency	USD
Approved total	2,700.00
Docking-station mapping	Missing
Expected flow result:
Run status: Failed - Missing Item Mapping
Error code: ITEM_MAPPING_MISSING
Target order created: No
CRM flow status: Blocked
Recovery owner: Commercial systems administrator
The flow must not create an order containing only the workstation line.
4.5 Recovery procedure
1. Identify the failed run using MER-HO-102.
2. Confirm that the customer exists and that the only missing value is the docking-station item mapping.
3. Create or approve the mapping from MER-PROD-DOCK-001 to MER-ITEM-DOCK-001.
4. Confirm that the item is active and has the correct USD price.
5. Search Books using MER-HO-102 to confirm that no partial order exists.
6. Retry the flow using the same correlation ID.
7. Confirm that the complete order is created once.
8. Write the target reference back to CRM.
9. Record the retry and final result.
A valid alternative is to route the record to manual finance processing if the target connector cannot safely retry line items. The alternative must still preserve the source quote and failure evidence.
4.6 Mistake and correction
Mistake: The flow creates the Books order first, then checks whether every line item is mapped.
Why it is wrong: A partial finance transaction may be created. A later retry could create a duplicate or require manual deletion.
Correction: Perform customer, item, currency, approval and total validation before the target creation action. Then search for an existing correlation ID before creating.
5. Try it yourself — guided practice
Learning goal
Build and test a CRM-to-Books handoff flow with success, missing-data, duplicate and permission branches.
Required access
You need:
- flow creation and activation permission;
- a CRM connection that can read quote and customer data and update sync fields;
- a Books connection that can search customers and items and create or update a test order;
- access to execution history;
- synthetic test records;
- permission to create or correct item mappings.
Complete handoff inputs
Handoff ID	CRM quote	Customer	Currency	Total	Handoff status	Flow status	Correlation ID
MER-HO-201	MER-QUOTE-301	MER-CUST-301	USD	4,153.60	Ready	Not started	MER-HO-201
MER-HO-202	MER-QUOTE-302	MER-CUST-302	USD	2,700.00	Ready	Not started	MER-HO-202
MER-HO-203	MER-QUOTE-303	MER-CUST-303	USD	3,900.00	Ready	Not started	MER-HO-203
MER-HO-204	MER-QUOTE-304	MER-CUST-304	Blank	4,500.00	Ready	Not started	MER-HO-204
Mapping inputs:
CRM record	Books record	Status
MER-CUST-301	MER-BOOK-CUST-301	Mapped
MER-CUST-302	MER-BOOK-CUST-302	Mapped
MER-CUST-303	MER-BOOK-CUST-303	Mapped
MER-CUST-304	MER-BOOK-CUST-304	Mapped
MER-PROD-WS-001	MER-ITEM-WS-001	Mapped
MER-PROD-INST-001	MER-ITEM-INST-001	Mapped
MER-PROD-SUP-001	MER-ITEM-SUP-001	Mapped
MER-PROD-DOCK-001	Blank	Missing
Flow requirements
 1. Start when a handoff is Ready and flow status is Not started.
 2. Retrieve quote, customer, line items, currency and total.
 3. Stop if the currency is blank.
 4. Stop if any item mapping is missing.
 5. Search for an existing target using the correlation ID.
 6. Update the existing target rather than creating a duplicate.
 7. Create a new Books order only when no target exists.
 8. Update CRM with target reference and flow status.
 9. Notify finance after a successful target action.
10. Record failed runs with an error reason and owner.
Guided steps and expected results
Step 1: Create connections
Configure separate test connections for CRM and Books.
Expected result: Each connection has the minimum required permissions and a named owner.
Step 2: Define the trigger
Use the CRM handoff event or the closest supported event that identifies Ready.
Expected result: A draft flow does not respond to unrelated CRM edits.
Step 3: Retrieve source data
Map the quote, customer, line items, amount, currency and correlation ID.
Expected result: The flow has all required values before target creation.
Step 4: Validate
Create branches for blank currency, missing item mapping and invalid handoff status.
Expected result:
- MER-HO-201 passes validation.
- MER-HO-202 is blocked if its quote contains the unmapped docking station.
- MER-HO-203 reaches the duplicate-target branch.
- MER-HO-204 is blocked for missing currency.
Step 5: Add duplicate protection
Search Books by correlation ID before creating an order.
Expected result: MER-HO-203 updates or reconciles MER-ORDER-203 instead of creating another order.
Step 6: Add target action
Create or update the Books test order and map the source total, currency and line items.
Expected result: The target amount agrees with the approved source amount.
Step 7: Add CRM update and notification
Write the target reference and flow status back to CRM. Notify finance-operations@example.com.
Expected result: Finance receives a message only after the target action succeeds.
Step 8: Test permission denial
Use a Books connection that can search records but cannot create orders.
Expected result: The flow records a permission failure and does not mark the handoff as successful.
Step 9: Recover MER-HO-202
Create the missing docking-station mapping, verify the item, search for any partial target and retry.
Expected result: The retry creates one complete order using MER-HO-202.
Final artifact
Your submission should contain:
Artifact	Minimum content
Flow design	Trigger, actions, conditions and branches
Connection register	Application, owner, permissions and environment
Mapping register	Source, target, transformation and required status
Correlation strategy	Business event ID and duplicate behavior
Test matrix	Success, missing currency, missing item, duplicate and permission tests
Execution evidence	Run ID, status, branch, error and retry
Recovery record	Correction, retry and final result
Safe cleanup
Deactivate the test flow after recording results if it is not needed by another learner. Remove only synthetic test orders or records through the permitted finance process. Do not delete target records to conceal a duplicate test.
Offline alternative
Use a spreadsheet to simulate branches and mappings. This can test logic and duplicate protection but cannot demonstrate actual connections, Flow execution history, connector permissions or target-application creation.
6. Independent challenge
Payment-status and reconciliation flow
Design a flow that updates CRM after Books records a payment. The flow must distinguish a fully matched payment from a discrepancy.
Scenario rules
- Books is the source of payment status.
- CRM stores the related finance reference and payment status for sales visibility.
- A payment may update CRM only when invoice ID, customer ID, currency and amount are present.
- The flow must compare the payment with the expected invoice balance.
- A matching payment sets CRM payment status to Paid or the approved equivalent.
- A partial or excessive payment creates a reconciliation exception and must not be marked fully paid.
- A repeated event ID must not create a second payment or second notification.
- If an event trigger is unavailable, you may propose polling or a scheduled check, but explain the duplicate-control method.
- A payment discrepancy notification must go to finance, not directly to the customer.
Complete input data
Payment event	Books payment	Invoice	Customer	Currency	Payment amount	Expected invoice balance
PAY-EVT-401	MER-PAY-401	MER-INVOICE-401	MER-CUST-401	USD	8,017.10	8,017.10
PAY-EVT-402	MER-PAY-402	MER-INVOICE-402	MER-CUST-402	USD	5,800.00	5,984.00
PAY-EVT-403	MER-PAY-403	MER-INVOICE-403	MER-CUST-403	USD	4,000.00	4,000.00
PAY-EVT-404	MER-PAY-404	Blank	MER-CUST-404	USD	2,000.00	Blank
CRM records:
CRM quote	Customer	Expected finance reference	Current payment status
MER-QUOTE-401	MER-CUST-401	MER-INVOICE-401	Awaiting Payment
MER-QUOTE-402	MER-CUST-402	MER-INVOICE-402	Awaiting Payment
MER-QUOTE-403	MER-CUST-403	MER-INVOICE-403	Awaiting Payment
MER-QUOTE-404	MER-CUST-404	Blank	Awaiting Payment
Deliverables
Create:
1. a trigger choice and justification;
2. a payment-to-CRM mapping;
3. conditions and branches;
4. duplicate event handling;
5. success and discrepancy actions;
6. execution-history fields;
7. a failed-run recovery plan;
8. expected results for all four events.
Success criteria
Your design should:
- mark MER-PAY-401 as matched;
- create an exception for MER-PAY-402;
- identify MER-PAY-403 as a duplicate event ID rather than a new payment for the CRM process;
- block MER-PAY-404 because invoice ID and expected balance are missing;
- never mark a missing or mismatched payment as fully paid;
- identify an owner for each exception.
7. Common problems and recovery
Symptom	Diagnosis	Correction	Verification
The flow starts for every CRM edit	Trigger is too broad	Use the specific handoff event and criteria	Edit an unrelated field
A polling flow processes the same record repeatedly	No cursor or event-ID control	Store the last successful position and processed IDs	Run two polling cycles
A webhook creates duplicate payments	Duplicate event handling is absent	Use source event ID and idempotent update behavior	Send the same test event twice
A scheduled reconciliation overlaps with the prior run	Run duration and schedule were not considered	Add a run lock, period boundary or overlap policy	Start two test runs
An email flow parses the wrong amount	Message format or sender was not validated	Require trusted sender, reference and amount pattern	Test a malformed email
A target order is created twice after retry	Retry did not search by correlation ID	Search before create and update existing target	Retry after simulated partial success
Flow status says successful but target record is wrong	Completion was checked only at action level	Inspect target values and reconcile	Compare source and target fields
Connection works for reads but not writes	Target permission is insufficient	Use an authorised connection or route to manual action	Test create and update separately
A failed mapping is retried without correction	Data failure was treated as temporary	Correct the source or mapping first	Retry only after validation passes
A webhook payload is accepted without verification	Source identity or signature was not checked	Use supported verification and reject invalid payloads	Send a malformed or unknown event
An email-triggered flow treats arbitrary text as structured data	Email content is not a controlled schema	Route uncertain messages to manual review	Test missing reference and amount
A flow marks Finance Accepted after creating an order	Source and target states were conflated	Set only Sent or target-created status until receiving acceptance exists	Inspect both state histories
Error messages expose sensitive data	Full payloads are stored in execution logs	Mask or omit unnecessary confidential values	Review the run history
A missing currency is filled with a default	Default concealed a data-quality problem	Block the flow and correct currency	Test a blank currency
Manual correction creates a second target	Original target was not searched	Search by correlation ID before correction	Compare target record count
8. Check your understanding
 1. What is the difference between an event trigger and a scheduled trigger?
 2. When might polling be appropriate?
 3. What control prevents a repeated webhook from creating a duplicate record?
 4. What is the purpose of a correlation ID?
 5. Why should a flow validate all item mappings before creating a Books order?
 6. What is the difference between a connection and a flow?
 7. Name three fields that should appear in execution history.
 8. What should happen after a target record is created but the source update fails?
 9. Why should Sent and Accepted remain separate?
10. Which branch should handle a blank currency?
11. What is a safe response to a permission failure?
12. Why should an email trigger validate sender and reference?
13. Calculate the difference when the expected invoice is USD 5,984 and the observed payment is USD 5,800.
14. In the independent challenge, what should happen to PAY-EVT-403 if BANK-EVT-401 was already processed?
15. What should a scheduled reconciliation flow compare?
9. Solutions and explanations
9.1 Answers to the checks
 1. An event trigger responds to a source event. A scheduled trigger runs at a defined time or interval regardless of one immediate source event.
 2. Polling is appropriate when the source does not provide a reliable event trigger. It requires a cursor, event ID or other duplicate-control method.
 3. Store and compare the source event ID before processing. A repeated event should be ignored or reconciled with the existing result.
 4. It links one business event across applications and allows a retry to find an existing target instead of creating a duplicate.
 5. Otherwise the target may contain only some line items or an incomplete amount, creating a finance discrepancy.
 6. A connection provides authenticated access. A flow defines the trigger, actions, mappings, branches and recovery behavior using that access.
 7. Examples include execution ID, correlation ID, trigger time, step, status, target record, branch and error message.
 8. Search the target using the correlation ID, then update the source with the existing target reference. Do not create another target.
 9. Sent means a transfer or target action occurred. Accepted means the receiving process accepted it. They require different evidence.
10. A blocked or missing-data branch should identify the blank currency and assign a correction owner.
11. Stop the affected action, record the permission failure, correct the authorised connection or route the record to an administrator, then retry safely.
12. Without validation, an untrusted or malformed message may create an incorrect payment or transaction.
13. 5,984 − 5,800 = USD 184 remains unmatched or outstanding, depending on the invoice and payment allocation.
14. It should be identified as a duplicate event ID and not create a second CRM payment update or notification.
15. It should compare source and target IDs, amounts, currencies, statuses, mappings and unresolved exceptions.
9.2 Guided practice sample solution
Flow design
Step	Configuration	Expected result
1	Trigger on CRM handoff Ready and Flow status Not started	Only eligible handoffs start
2	Retrieve quote, customer, line items, currency and correlation ID	Complete source payload
3	Check customer and item mappings	Missing mappings branch before target creation
4	Search Books by correlation ID	Existing target is found on retry
5	Create or update Books order	Target uses approved total and lines
6	Update CRM target reference and flow status	Sales can see the handoff result
7	Notify finance	Notification occurs after target action succeeds
8	Write execution result	Run is traceable by run and correlation ID
Expected record routes
Handoff	Expected route	Explanation
MER-HO-201	Success	Customer, item mappings, currency and target data are complete
MER-HO-202	Failed - missing item mapping	Docking-station mapping is absent
MER-HO-203	Duplicate-target branch	Existing MER-ORDER-203 is found
MER-HO-204	Blocked - missing currency	Currency is required before target creation
Duplicate behavior
For MER-HO-203, the flow should:
1. receive the event;
2. retrieve the correlation ID;
3. search Books for MER-HO-203;
4. find MER-ORDER-203;
5. compare amount and source reference;
6. update the CRM target reference if needed;
7. avoid creating another order.
Permission failure
If the Books connection can read but not create:
Flow status: Failed - Permission
Target order: Not created
CRM status: Blocked
Owner: Flow administrator or finance systems owner
The connection should be corrected or replaced with an authorised least-privilege connection. The flow should then be retried using the same correlation ID.
Recovery of MER-HO-202
The missing mapping is:
MER-PROD-DOCK-001 → MER-ITEM-DOCK-001
After the mapping is created and verified:
1. search for an existing target using MER-HO-202;
2. confirm none exists;
3. retry;
4. create one complete target order;
5. write the target ID to CRM;
6. notify finance;
7. record the successful retry.
9.3 Independent challenge sample solution
Trigger choice
An event trigger from Books payment creation or payment-status update is the preferred candidate if supported. It provides near-real-time processing and identifies the payment event directly.
A polling trigger is an alternative if the payment source cannot emit the required event. It must store the last successful timestamp or source event ID.
A scheduled reconciliation flow is useful as a secondary control, even when event processing exists. It can find missed or failed events.
An email trigger is appropriate only for controlled remittance messages, not as the primary source of payment truth.
Payment mapping
Source field	CRM target field	Rule
Books payment ID	Finance payment reference	Preserve business ID
Invoice ID	Finance invoice reference	Required
Customer ID	CRM customer reference	Match existing customer
Payment amount	Applied payment amount	Numeric and currency-specific
Currency	Payment currency	Must match invoice or include conversion
Event ID	Processed event ID	Deduplicate
Payment date	Payment date	Preserve source date
Payment status	CRM payment status	Map to controlled value
Branch design
Invoice reference present?
  ├── No → Blocked - Missing Invoice

Expected balance present?
  ├── No → Blocked - Missing Expected Amount

Event ID already processed?
  ├── Yes → Duplicate branch; no new update

Payment amount equals expected balance?
  ├── Yes → Set CRM payment status Paid; notify owner
  └── No → Create reconciliation exception; do not set Paid
Expected results
Event	Expected result	Explanation
PAY-EVT-401	Mark matched or Paid	USD 8,017.10 equals expected USD 8,017.10
PAY-EVT-402	Reconciliation exception	USD 5,800 is USD 184 below expected USD 5,984
PAY-EVT-403	Duplicate event branch	BANK-EVT-401 was already processed; do not create a second update
PAY-EVT-404	Blocked - missing invoice and expected amount	Required comparison fields are absent
Recovery for PAY-EVT-402
Expected invoice balance = USD 5,984.00
Payment received = USD 5,800.00
Difference = USD 184.00
The flow should create an exception for finance. It should not mark CRM as fully paid. Finance may later record another payment, an authorised adjustment or a correction, but the flow should not choose that accounting outcome automatically.
Recovery for PAY-EVT-404
The missing invoice reference must be supplied or matched by an authorised finance user. The event should remain blocked until the invoice and expected balance are known. Retrying without those values would produce an untraceable payment update.
10. Chapter recap and next step
Cross-application automation succeeds when it moves reliable information through controlled connections and records what happened.
You should now be able to:
- distinguish event, polling, scheduled, email and webhook triggers;
- select a trigger based on source behavior;
- create actions, conditions and explicit branches;
- map records, fields, transformations and correlation IDs;
- configure least-privilege connections;
- inspect execution history;
- classify data, permission, duplicate, configuration and temporary failures;
- retry safely without creating duplicate target records;
- separate Sent, Accepted, Failed and Reconciled states;
- recover a missing item mapping;
- design a payment-status flow that does not mark mismatched payments as paid.
For the Meridian Supply project, this chapter produces:
C01_CH14_Meridian_CRM_to_Books_Flow_Design
C01_CH14_Meridian_Flow_Mapping_and_Connection_Register
C01_CH14_Meridian_Execution_History_Test_Evidence
C01_CH14_Meridian_Failed_Handoff_Recovery_Record
C01_CH14_Meridian_Payment_Status_Flow_Design
The next chapter applies connected process principles to customer service with Desk. It builds on customer mappings, service context, failed handoffs and cross-application ownership.
11. Glossary and further reading
Glossary
Term	Definition
Action	Work performed by a flow after a trigger and conditions are satisfied
Branch	A conditional path selected according to record values
Connection	Authenticated access from a flow to an application or service
Correlation ID	Business-event identifier used to link source and target records
Event trigger	Trigger caused by a source event such as record creation or update
Execution history	Record of flow runs, steps, statuses, values and errors
Flow	Cross-application automation containing triggers, actions, conditions and mappings
Idempotent processing	Repeating a flow does not create an unwanted duplicate result
Mapping	Definition of how source records or fields correspond to target records or fields
Polling	Repeatedly checking a source for new or changed records
Scheduled trigger	Trigger that starts at a defined time or interval
Webhook	Event message sent to or from a configured endpoint
Further reading
Check current product editions, supported connectors, trigger types, connections, retry behavior and execution history before configuring a production flow:
- Zoho Flow Help (https://help.zoho.com/portal/en/kb/flow)
- Zoho Flow documentation (https://www.zoho.com/flow/help/)
- Zoho CRM Help (https://help.zoho.com/portal/en/kb/crm)
- Zoho Books Help (https://help.zoho.com/portal/en/kb/books)
- Zoho CRM developer documentation (https://www.zoho.com/crm/developer/docs/)
- Zoho Books API documentation (https://www.zoho.com/books/api/v3/)
This chapter has not verified current Zoho Flow screens, connector actions, trigger availability, connection permissions, retry behavior or execution-history fields in a live environment. Synthetic flow results are expected learning outputs, not product execution observations.
