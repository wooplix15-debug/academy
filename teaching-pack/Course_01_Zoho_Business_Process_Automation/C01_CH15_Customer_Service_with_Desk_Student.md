schema_version: "1.1"
course_id: "C01"
chapter_id: "C01-CH15"
chapter_number: 15
chapter_title: "Customer Service with Desk"
filename: "C01_CH15_Customer_Service_with_Desk_Student.md"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "not_verified"
---
Customer Service with Desk
1. What you will learn
A customer-service process must do more than collect messages. It must identify the customer, route the ticket, assign responsibility, measure response and resolution, protect internal information and provide a way to escalate overdue or high-risk work.
This chapter uses Zoho Desk as the candidate service application for Meridian Supply. It explains stable service-management concepts and a configuration method. Exact current Desk screens, editions, permissions and integration behavior must be verified before production use.
You will learn to:
- design ticket intake from email, web and other supported channels;
- distinguish departments, queues and individual assignment;
- define service-level targets with units, clocks and exclusions;
- configure escalation routes;
- send customer, agent and manager notifications;
- connect a ticket to CRM customer context;
- define knowledge-base ownership and publication control;
- create service reports with reproducible metric definitions;
- configure and test ticket routing;
- publish a synthetic support article;
- recover from missing customer context, incorrect routing, overdue tickets and permission problems.
This chapter continues the Meridian Supply project. The supplied continuity from Chapter 14 establishes:
- CRM and Books records have separate ownership;
- cross-application flows use mappings, connections, correlation IDs and explicit failure states;
- customer and finance references must remain traceable;
- failed handoffs require a named recovery owner;
- no live Zoho execution has been verified.
The service records and service-level rules in this chapter are new synthetic case assumptions. They are not universal customer-service targets, legal obligations or manufacturer instructions.
2. Lessons
2.1 Ticket intake
A ticket is one service case that can be assigned, worked, communicated about and closed with evidence.
A ticket should normally contain:
- ticket ID;
- customer;
- contact person;
- source channel;
- subject;
- description;
- category;
- product or service;
- severity or priority;
- department;
- queue or owner;
- status;
- timestamps;
- related CRM, quote or order reference;
- internal notes;
- customer-visible responses.
Intake channels
Possible channels include:
- support email;
- web form;
- telephone entry by an agent;
- chat or messaging, where supported;
- CRM-created service request;
- flow or webhook from another system.
Each channel must produce a consistent minimum record. A telephone ticket entered by an agent should not omit information required from a web form.
Customer context
A ticket should be associated with an existing customer when possible. A customer match can use:
- customer business ID;
- verified contact email;
- related quote or order reference;
- approved duplicate rules.
Do not create a new customer merely because an email address has changed. Route uncertain matches to a data-review queue.
Ticket status
A synthetic service status model may contain:
New
Assigned
In Progress
Pending Customer
Pending Internal
Resolved
Closed
Escalated
Resolved and Closed should have different meanings if the process needs a period for confirmation or quality review. Define what evidence is required for each.
Check your understanding
Why should an email subject alone not determine the customer on a ticket?
Answer: Subjects may be forwarded, reused or vague. Customer matching should use approved identifiers and supporting evidence, with uncertain matches sent to review.
2.2 Departments, queues and assignment
A department groups service work by organisational responsibility. A queue is a work list for a team or stage. An assignee is the person currently responsible for action.
These are related but not identical.
Concept	Example	Question answered
Department	Technical Support	Which service function owns this work?
Queue	Technical L1	Which work list should receive it?
Assignee	Jordan Lee	Which person is responsible now?
Escalation owner	Service Manager	Who acts when the target is missed?
A ticket can be in a department and queue without yet having an individual assignee. This is useful when work arrives outside business hours or when a team triages before assigning.
Meridian departments and queues
Department	Queue	Example ticket
Installation Support	Installation L1	Installation appointment or setup issue
Technical Support	Technical L1	Standard equipment question
Technical Support	Technical L2	High-severity equipment failure
Billing Questions	Billing L1	Invoice or payment question
Service Data Review	Unassigned Review	Missing customer or unusable context
Assignment criteria
Use criteria that are observable:
- category;
- severity;
- product;
- customer tier;
- installation status;
- location or region where explicitly supplied;
- language where supported and defined.
Avoid routing based on a free-text phrase unless the process has a review branch. A phrase such as “urgent” may not reliably mean High severity.
Assignment sequence
A safe sequence is:
1. identify the customer;
2. classify the category and severity;
3. select the department;
4. select the queue;
5. assign an agent;
6. notify the owner;
7. start or confirm the service clock.
Do not assign an individual before the ticket has enough context to determine the correct department.
Check your understanding
Why might a High equipment-failure ticket go to Technical L2 rather than Technical L1?
Answer: The synthetic Meridian rule routes High equipment failures to a more experienced queue because the severity requires a different capability and escalation path. This is a case rule, not a universal service-management rule.
2.3 Service-level targets and escalations
A service-level target defines the expected time for a service event. It must state:
- target event;
- starting event;
- unit;
- business calendar;
- exclusions or pauses;
- severity or customer tier;
- evidence of completion;
- escalation behavior.
For this chapter, Meridian uses the following synthetic targets:
Severity	First human response target	Resolution target
Standard	4 business hours	2 business days
High	1 business hour	1 business day
Synthetic business hours are Monday to Friday, 09:00–17:00 local time. There are 8 business hours in one full business day.
An automated receipt message is not a human response unless the business explicitly defines it as such. In this chapter, it is not.
Response calculation
If a Standard ticket is created Monday at 09:15 and receives its first human response at 11:15:
First response duration
= 11:15 − 09:15
= 2 business hours
The target is 4 business hours, so the expected result is within target.
For an after-hours ticket created Friday at 16:30 and answered Monday at 09:30:
Friday remaining time = 17:00 − 16:30 = 0.5 hours
Monday elapsed time = 09:30 − 09:00 = 0.5 hours

Total business time = 0.5 + 0.5 = 1 business hour
The target result depends on the severity.
Pending states
Define whether the service clock pauses while the ticket is:
- Pending Customer;
- Pending Internal;
- waiting for a supplier;
- waiting for a scheduled installation.
Do not assume that a status automatically pauses a target. The business rule and product behavior must both be verified.
Escalation
For Meridian:
- High tickets without a first human response after 1 business hour escalate to the service manager.
- Standard tickets without a first human response after 4 business hours escalate to the department lead.
- Tickets that pass the resolution target escalate to the department owner.
- An escalation creates a task and notification but does not falsely close or resolve the ticket.
Check your understanding
A High ticket is created Friday at 16:30 and receives its first human response Monday at 10:30. Was the one-business-hour target met?
Answer: No. The elapsed business time is 0.5 hours on Friday plus 1.5 hours on Monday, or 2 hours. The target was 1 hour, so the ticket should have escalated at approximately Monday 09:30 under the synthetic calendar.
2.4 Notifications and CRM context
Notifications should support the service process without exposing internal information.
Useful notifications include:
- customer receipt;
- assignment to a queue or agent;
- request for missing information;
- escalation to a manager;
- resolution message;
- internal exception notification.
A notification should identify:
- ticket ID;
- customer or contact;
- issue summary;
- current status;
- required action;
- target or due time where defined;
- safe contact information.
Do not include internal notes, confidential pricing or employee commentary in a customer-facing message.
CRM context
A Desk ticket may need context from CRM:
- customer ID;
- contact person;
- quote or order reference;
- products purchased;
- installation date or status;
- account owner;
- relevant commercial history.
The ticket should not copy every CRM field. Provide the minimum context that helps the service agent work correctly.
A common design is:
- CRM remains authoritative for customer and sales context;
- Desk remains authoritative for ticket status, assignment, response and resolution;
- a connection or flow supplies selected context;
- the service agent sees relevant CRM fields as read-only.
Check your understanding
Why should a service agent see the customer’s quote reference but not necessarily edit the quote amount?
Answer: The quote reference provides useful service context. Editing the commercial amount belongs to the controlled sales and approval process, so the service agent should use a correction or escalation route instead.
2.5 Knowledge-base ownership and publication
A knowledge base helps customers and agents find repeatable guidance. An article should have:
- article ID;
- title;
- audience;
- category;
- owner;
- reviewer;
- version;
- status;
- publication date;
- review date;
- content;
- escalation instructions;
- related product or service.
A useful article is not an unreviewed note. It needs ownership and a publication decision.
Article lifecycle
Draft
  → In Review
  → Published
  → Revision Required
  → Retired
The owner maintains accuracy. The reviewer confirms that the article is suitable for publication. A support agent may suggest an article without having permission to publish it.
Article content structure
A practical article can include:
1. problem statement;
2. symptoms;
3. prerequisites;
4. safe steps;
5. expected result;
6. stop condition;
7. escalation route;
8. last reviewed date.
The article should not expose customer-specific information or internal credentials.
Knowledge-base ownership
Responsibility	Role
Draft content	Subject-matter owner
Technical review	Service lead
Publication	Knowledge-base publisher
Accuracy review	Product or service owner
Retirement	Knowledge-base owner
Usage feedback	Support agents and service reporting owner
Check your understanding
Why should an article have a reviewer as well as an author?
Answer: The author knows the operational steps, while the reviewer checks accuracy, clarity, audience suitability and whether the content should be published.
2.6 Service reporting
Service reporting is meaningful only when the metric definition is clear.
Useful service measures include:
- tickets received;
- tickets by channel;
- tickets by department and queue;
- open backlog;
- first human response time;
- resolution time;
- target attainment;
- escalated tickets;
- returned or reopened tickets;
- knowledge article usage;
- tickets without customer context.
Metric definitions
Metric	Formula or definition	Important exclusion
Ticket count	Number of distinct ticket IDs received in period	Do not count repeated updates as tickets
Open backlog	Distinct tickets not in a terminal state at report time	Define terminal states
First response time	First human response timestamp minus ticket-created timestamp	Exclude automated acknowledgement
First-response attainment	Tickets meeting target / eligible tickets × 100	Define eligible tickets and pauses
Resolution time	Resolution timestamp minus start timestamp, adjusted by approved pauses	Do not assume closure means target met
Escalation count	Distinct tickets with an escalation event	Do not count repeated notifications as separate escalations
Reopen rate	Reopened tickets / resolved or closed tickets × 100	Define reopen event
Example:
Ticket	Eligible?	Met first-response target?
MER-TKT-301	Yes	Yes
MER-TKT-302	Yes	No
MER-TKT-303	No; missing valid customer	Excluded until corrected
MER-TKT-304	Yes	Yes
If two of three eligible tickets met the target:
First-response attainment
= 2 / 3 × 100
= 66.67%
The excluded ticket must be reported as an exception, not silently removed.
Check your understanding
Why should automated acknowledgements be separated from first human response time?
Answer: An automated message confirms receipt but does not demonstrate that a service agent reviewed or acted on the ticket. Combining them would make response performance appear faster than it was.
2.7 Configuring customer service with Desk
This procedure uses common service-management concepts and Zoho Desk terminology. Exact screens, editions, integrations and permission names must be verified.
Required access
You need access appropriate to:
- create or edit departments;
- create or edit ticket fields and layouts;
- configure channels and intake forms;
- configure assignment rules or queues;
- configure service-level targets and escalations;
- configure notifications;
- connect selected CRM customer context;
- create, review and publish knowledge articles;
- view ticket history and service reports;
- test with agent, manager, publisher and restricted roles.
Configuration sequence
 1. Define ticket fields and statuses.
Expected result: Category, severity, customer, contact, department, queue and status have controlled meanings.
 2. Configure intake channels.
Expected result: Email, web or manual tickets create the minimum required fields.
 3. Create departments and queues.
Expected result: Each supported category has a receiving work list.
 4. Configure assignment rules.
Expected result: A ticket can be routed by category, severity or another approved criterion.
 5. Configure service-level targets.
Expected result: The target has a calendar, starting event, completion event and pause definition.
 6. Configure escalations.
Expected result: Overdue or high-severity tickets notify the correct owner and create a task or escalation state.
 7. Configure notifications.
Expected result: Customer-facing and internal messages are separated.
 8. Connect CRM context.
Expected result: Service users can identify the customer and relevant commercial context without gaining unwanted edit access.
 9. Configure knowledge-base ownership.
Expected result: Draft, review, publication and retirement responsibilities are clear.
10. Test reports.
Expected result: Metrics use distinct ticket IDs, defined timestamps and declared exclusions.
11. Activate and document support ownership.
Expected result: A user knows where to report incorrect routing, missing context, target errors or article problems.
3. Visual explanation
flowchart TD
    A[Customer email or web intake] --> B[Create ticket]
    B --> C{Customer context valid?}
    C -- No --> D[Data Review queue]
    C -- Yes --> E[Classify category and severity]
    E --> F[Select department and queue]
    F --> G[Assign agent]
    G --> H[Start service target]
    H --> I{Response within target?}
    I -- Yes --> J[Work ticket]
    I -- No --> K[Escalate]
    J --> L{Resolution complete?}
    L -- No --> M[Pending Customer or Pending Internal]
    M --> J
    L -- Yes --> N[Resolve and notify customer]
    N --> O[Close after defined confirmation]
The diagram shows that customer validation and assignment occur before normal service work. A ticket without a valid customer should not disappear; it follows a data-review route.
4. Worked case: Meridian installation support
4.1 Scenario rules
The following rules are synthetic Meridian service rules:
- Departments are Installation Support, Technical Support, Billing Questions and Service Data Review.
- Installation tickets go to Installation L1.
- Standard equipment issues go to Technical L1.
- High equipment failures go to Technical L2.
- Billing questions go to Billing L1.
- Tickets without a valid customer go to Service Data Review.
- Standard tickets have a first human response target of 4 business hours and a resolution target of 2 business days.
- High tickets have a first human response target of 1 business hour and a resolution target of 1 business day.
- Business hours are Monday to Friday, 09:00–17:00 local time.
- Automated acknowledgements do not count as human responses.
- A Pending Customer pause begins only after the status and reason are recorded.
- High tickets without a first human response escalate to the service manager.
- These rules are learning assumptions, not universal service obligations.
4.2 Input tickets
Ticket ID	Customer	Contact	Channel	Category	Severity	Created	First human response
MER-TKT-301	MER-CUST-301	Ava Ross	Email	Installation	Standard	2026-11-03 09:15	2026-11-03 11:15
MER-TKT-302	MER-CUST-302	Daniel Wu	Web	Equipment Failure	High	2026-11-03 16:30	2026-11-04 10:30
MER-TKT-303	Blank	Noor Ali	Email	Support	Standard	2026-11-03 10:00	Blank
MER-TKT-304	MER-CUST-304	Grace Kim	Phone	Installation	Standard	2026-11-03 13:00	2026-11-03 14:00
4.3 Routing results
Ticket	Department	Queue	Reason
MER-TKT-301	Installation Support	Installation L1	Installation category
MER-TKT-302	Technical Support	Technical L2	High equipment failure
MER-TKT-303	Service Data Review	Unassigned Review	Customer context missing
MER-TKT-304	Installation Support	Installation L1	Installation category
4.4 Service-time calculations
MER-TKT-301
Created: 09:15
First human response: 11:15

First response duration
= 11:15 − 09:15
= 2 business hours
The Standard target is 4 business hours, so the expected result is within target.
Resolution calculation:
Business hours on 2026-11-03
= 17:00 − 09:15
= 7.75 hours

Business hours on 2026-11-04
= 15:00 − 09:00
= 6 hours

Total active business time
= 7.75 + 6
= 13.75 hours

Business-day equivalent
= 13.75 / 8
= 1.71875 business days
The synthetic resolution target is 2 business days, so the expected result is within target.
MER-TKT-302
Friday-equivalent first period:
2026-11-03 16:30–17:00 = 0.5 business hours

Next day:
2026-11-04 09:00–10:30 = 1.5 business hours

Total
= 0.5 + 1.5
= 2 business hours
The High target is 1 business hour. The ticket should have escalated at approximately 2026-11-04 09:30 under the synthetic calendar. The first response at 10:30 is late.
4.5 Notification design
Notification	Recipient	Trigger	Content
Receipt	Customer contact	Ticket created with valid contact	Ticket ID and safe summary
Assignment	Queue or agent	Department and queue assigned	Ticket ID, category, severity and action
High escalation	Service manager	High target missed	Ticket ID, target, current owner and next action
Missing context	Service data review	Customer or contact missing	Required correction and owner
Resolution	Customer contact	Ticket resolved	Resolution summary and support route
Internal notes and escalation commentary must not appear in the customer receipt or resolution message.
4.6 Knowledge-base artifact
Field	Value
Article ID	MER-KB-001
Title	Workstation: confirming readiness after installation
Audience	Meridian customers and support agents
Owner	Service Enablement
Reviewer	Installation Support Lead
Version	1.0
Status	Published after review
Related product	MER-PROD-WS-001
Last reviewed	2026-11-02
Synthetic article content:
Purpose: Confirm that a Meridian workstation is ready after installation.  
Before starting: Keep the workstation, monitor and supplied cables available.  
Steps:  
1. Confirm that the power cable is connected to the workstation and an available outlet.  
2. Confirm that the power indicator responds when the workstation is turned on.  
3. Confirm that the monitor cable is connected to the workstation and monitor.  
4. Confirm that the monitor input matches the connected cable.  
5. Sign in using the customer’s approved account.  
Expected result: The workstation starts, displays an image and reaches the normal sign-in screen.  
Stop condition: If the workstation does not power on or displays an error, stop and contact Meridian Support with the ticket ID.  
Internal note: Do not include customer credentials in a ticket or article.
This is synthetic Meridian guidance, not manufacturer documentation.
4.7 Mistake and correction
Mistake: The system sends every installation ticket to Technical L1 because the assignment rule checks only whether a product is present.
Why it is wrong: Product presence does not identify the type of service work. Installation issues need the Installation Support department.
Correction: Use category as the first routing condition, then severity for technical escalation. Route missing customer context to Service Data Review rather than assigning it to a random agent.
A second mistake is counting the automated receipt as the first human response. The correction is to record a separate human-response timestamp.
5. Try it yourself — guided practice
Learning goal
Configure ticket routing and escalation, then publish a synthetic knowledge-base article.
Required access
You need:
- Desk administration or service-configuration access;
- permission to create departments, queues and assignment rules;
- permission to configure service targets and escalations;
- permission to create and publish knowledge articles;
- CRM context access;
- agent, manager and publisher test roles;
- synthetic tickets and contacts.
Complete sample tickets
Ticket ID	Customer	Contact email	Channel	Category	Severity	Created	Customer context
MER-TKT-401	MER-CUST-401	ava@ridgeway.example.com (mailto:ava@ridgeway.example.com)	Email	Installation	Standard	2026-12-01 09:00	Valid
MER-TKT-402	MER-CUST-402	daniel@brightline.example.com (mailto:daniel@brightline.example.com)	Web	Equipment Failure	High	2026-12-01 15:30	Valid
MER-TKT-403	MER-CUST-403	noor@westfield.example.com (mailto:noor@westfield.example.com)	Email	Billing	Standard	2026-12-01 10:00	Valid
MER-TKT-404	Blank	unknown@harborview.example.com (mailto:unknown@harborview.example.com)	Email	Installation	Standard	2026-12-01 11:00	Missing
MER-TKT-405	MER-CUST-405	grace@oakridge.example.com (mailto:grace@oakridge.example.com)	Phone	Equipment Failure	High	2026-12-01 10:00	Valid
Routing and escalation requirements
- Installation → Installation Support → Installation L1.
- Standard equipment failure → Technical Support → Technical L1.
- High equipment failure → Technical Support → Technical L2.
- Billing → Billing Questions → Billing L1.
- Missing customer → Service Data Review → Unassigned Review.
- Standard response target: 4 business hours.
- High response target: 1 business hour.
- High escalation: service manager after one business hour without human response.
- Resolution escalation: department owner after the resolution target is missed.
- Automated receipt does not count as first human response.
Guided steps and expected results
Step 1: Create departments and queues
Create the four departments and queues in the routing table.
Expected result: Every valid category has a queue, and missing customer context has a review queue.
Step 2: Configure assignment rules
Use category first and severity second.
Expected result:
- MER-TKT-401 → Installation L1.
- MER-TKT-402 → Technical L2.
- MER-TKT-403 → Billing L1.
- MER-TKT-404 → Unassigned Review.
- MER-TKT-405 → Technical L2.
Step 3: Configure service targets
Use the synthetic calendar and targets.
Expected result: The target starts at ticket creation and first response stops at the first human response.
Step 4: Configure escalations
Escalate High tickets without first response after one business hour.
Expected result: MER-TKT-402 is due for escalation at approximately 2026-12-02 09:30 if no response is recorded. MER-TKT-405 has a response after 30 minutes and should not escalate.
Step 5: Configure CRM context
Display customer, contact and related commercial reference to the service agent without allowing quote-price edits.
Expected result: An agent can identify the customer and related sale while the sales approval boundary remains intact.
Step 6: Create the article draft
Use the supplied article input:
Field	Value
Article ID	MER-KB-101
Title	Workstation setup: check power and display
Audience	Customers and Installation Support agents
Owner	Service Enablement
Reviewer	Installation Support Lead
Category	Installation
Related product	MER-PROD-WS-001
Version	1.0
Status	Draft
Content:
Check that the workstation power cable is connected, the monitor cable is connected and the monitor input matches the cable. Confirm that the workstation reaches the sign-in screen. If the workstation does not power on or displays an error, stop and contact Meridian Support with the ticket ID. Do not include passwords in the ticket.
Step 7: Review and publish
Have the reviewer check the title, steps, stop condition, audience and internal-information boundary.
Expected result: The article moves from Draft to In Review and then Published only after the reviewer’s decision.
Step 8: Test access
Test a customer-facing view, service agent view and article publisher view.
Expected result: Customers see approved article content; internal notes and unpublished drafts remain restricted.
Final artifact
Your submission should contain:
Artifact	Minimum content
Ticket intake design	Channels, fields and customer matching
Department and queue matrix	Category, severity and destination
Service target register	Start, stop, unit, calendar and exclusions
Escalation matrix	Trigger, recipient, action and stop condition
CRM context design	Visible fields and edit restrictions
Knowledge article	Owner, reviewer, version, content and publication status
Test evidence	Routing, SLA, escalation, permission and article tests
User instructions	How an agent handles a new, high-severity and missing-context ticket
Safe cleanup
Use synthetic tickets and article content. Deactivate practice routing and escalation rules after recording results if they are not shared. Do not delete live service tickets or published knowledge articles.
Offline alternative
You can produce the routing, target, escalation and article artifacts in a spreadsheet. You cannot demonstrate actual Desk intake, timer execution, role permissions or article publication behavior without product access.
6. Independent challenge
After-hours service routing and reporting
Design a service configuration for tickets received near the end of the business day.
Scenario rules
- Business hours remain Monday to Friday, 09:00–17:00.
- Standard first response target is 4 business hours.
- High first response target is 1 business hour.
- High tickets escalate to the service manager after the target is missed.
- Pending Customer pauses resolution only after a human response and a recorded reason.
- The customer receipt does not count as a human response.
- Tickets with missing customer context go to Service Data Review.
- Published articles require an owner, reviewer, version and review date.
Complete ticket data
Ticket ID	Category	Severity	Created	First human response	Pending Customer	Resolved
MER-TKT-501	Installation	Standard	2026-12-04 16:30	2026-12-07 09:30	No	2026-12-07 14:00
MER-TKT-502	Equipment Failure	High	2026-12-04 16:30	2026-12-07 10:30	No	Blank
MER-TKT-503	Installation	Standard	2026-12-07 09:00	2026-12-07 10:00	2026-12-07 10:30–15:05	2026-12-08 11:00
MER-TKT-504	Billing	Standard	2026-12-07 11:00	Blank	No	Blank
MER-TKT-505	Equipment Failure	High	2026-12-07 13:00	2026-12-07 13:30	No	2026-12-07 16:00
Article input
Field	Value
Article ID	MER-KB-201
Title	What to include when reporting an equipment failure
Owner	Technical Support Lead
Reviewer	Service Manager
Audience	Customers and Technical Support agents
Version	1.0
Status	Draft
Required content	Symptoms, device identifier, time of failure, visible error, safe stop condition and contact route
Deliverables
Create:
1. routing rules and queue assignments;
2. first-response calculations;
3. escalation results;
4. resolution-pause treatment for MER-TKT-503;
5. missing-context route for MER-TKT-504;
6. a service-reporting table;
7. the completed knowledge article;
8. a test plan for after-hours, high severity, pending customer and permission cases.
Success criteria
Your design should:
- calculate the after-hours target correctly;
- escalate MER-TKT-502;
- avoid escalating MER-TKT-505;
- pause only the defined portion of MER-TKT-503;
- exclude or separately report MER-TKT-504;
- keep the draft article unpublished until reviewed;
- define the owner of every exception.
7. Common problems and recovery
Symptom	Diagnosis	Correction	Verification
Tickets go to the wrong department	Routing checks a broad or ambiguous field	Use controlled category and severity values	Test one ticket for each category
A missing-customer ticket is assigned to an agent	Customer validation happens after assignment	Route missing context to Service Data Review first	Submit a ticket without customer ID
A receipt is counted as a human response	Response event is not defined	Store a separate first human response timestamp	Test automated and human messages
High tickets do not escalate	Target, calendar or escalation recipient is missing	Define the target and escalation owner	Create a high ticket near closing time
An escalation repeats every few minutes	No escalation marker or stop condition	Record escalation state and stop after required action	Leave a test ticket overdue
Pending Customer pauses the clock immediately	Pause rule lacks a human-response prerequisite	Start pause only after the defined event and reason	Test pending status before first response
Agents cannot see the related quote	CRM context mapping is incomplete	Map customer, contact and permitted commercial references	Open a linked test ticket
Agents can edit quote prices from the service screen	Context fields have excessive permissions	Make sales fields read-only and route corrections to sales	Test service-agent role
Customer receives an internal escalation note	Notification audiences are mixed	Separate customer and internal templates	Trigger an escalation and inspect both messages
A knowledge article contains customer information	Article was copied from a ticket without review	Remove identifiers and send for review	Search the published article for private data
An article is published with no owner	Publication control is missing	Require owner, reviewer and version	Attempt to publish incomplete metadata
Backlog report counts updates as tickets	Report grain is incorrect	Count distinct ticket IDs	Reconcile report count to source records
First-response percentage is inflated	Excluded or unfinished tickets were silently removed	Define denominator and report exceptions	Recalculate from case-level flags
Service target is claimed as met from final closure	Start or target evidence is missing	Preserve timestamps and target definition	Reproduce the calculation
A ticket is closed without resolution evidence	Closing transition is uncontrolled	Require resolution note and authorised role	Attempt closure with no note
8. Check your understanding
 1. What is the difference between a department, queue and assignee?
 2. What information should a ticket contain before normal routing?
 3. Why should missing customer context have a separate route?
 4. What is the synthetic Standard first-response target?
 5. Does an automated receipt count as a human response in this chapter?
 6. How is a High equipment-failure ticket routed?
 7. What starts a Pending Customer pause under the synthetic rules?
 8. Why should CRM quote amounts be read-only to service agents?
 9. What evidence should a published knowledge article contain?
10. Calculate the first response time for a ticket created at 09:15 and answered at 11:15.
11. A ticket is created Friday at 16:30 and answered Monday at 10:30. How many business hours elapsed?
12. Why should service reports count distinct ticket IDs?
13. What should happen when an article has no reviewer?
14. Which ticket in the worked case requires escalation?
15. What should be excluded or separately reported when calculating first-response attainment?
9. Solutions and explanations
9.1 Answers to the checks
 1. A department is an organisational service function. A queue is a work list within a function. An assignee is the person responsible for the current action.
 2. It should contain a ticket ID, customer or review state, contact, subject, description, category, severity, channel and creation timestamp.
 3. Assigning an invalid ticket to a random agent hides a data-quality problem and can delay service. A review queue gives the problem an owner.
 4. Four business hours.
 5. No. It confirms receipt but is not a human response under the chapter’s rule.
 6. It goes to Technical Support and Technical L2.
 7. A human response followed by the recorded Pending Customer state and reason starts the pause.
 8. Quote amounts belong to the controlled sales and approval process. Service agents need context but should not bypass commercial controls.
 9. Article ID, title, owner, reviewer, version, audience, status, content and review date.
10. Two business hours.
11. Friday 16:30–17:00 is 0.5 hours, and Monday 09:00–10:30 is 1.5 hours. Total is 2 business hours.
12. Updates, messages and assignments are not new tickets. Distinct ticket IDs represent the actual service cases.
13. Keep it in Draft or In Review. Do not publish until a reviewer is assigned and completes the review.
14. MER-TKT-302, because it is High and its first response took two business hours against a one-hour target.
15. Exclude tickets without valid eligibility evidence, such as missing customer context, but report them separately as exceptions.
9.2 Guided practice sample solution
Routing results
Ticket	Department	Queue	Expected result
MER-TKT-401	Installation Support	Installation L1	Correctly routed
MER-TKT-402	Technical Support	Technical L2	High-severity route
MER-TKT-403	Billing Questions	Billing L1	Correctly routed
MER-TKT-404	Service Data Review	Unassigned Review	Customer context must be corrected
MER-TKT-405	Technical Support	Technical L2	High-severity route
Escalation calculations
For MER-TKT-402:
Created: 2026-12-01 15:30
Remaining business time: 15:30–17:00 = 1.5 hours
High target: 1 hour

Expected escalation time:
Next business day begins at 09:00
One remaining target hour is reached at 09:30
No first response is supplied, so the expected result is an escalation at approximately 2026-12-02 09:30.
For MER-TKT-405:
Created: 10:00
First human response: 10:30
Elapsed time: 0.5 business hours
The High target is one business hour, so it should not escalate.
Article artifact
Field	Completed value
Article ID	MER-KB-101
Title	Workstation setup: check power and display
Owner	Service Enablement
Reviewer	Installation Support Lead
Audience	Customers and Installation Support agents
Status	Published only after review
Version	1.0
Related product	MER-PROD-WS-001
Completed article:
Check that the workstation power cable is connected to the workstation and an available outlet. Check that the monitor cable is connected at both ends and that the monitor input matches the cable. Confirm that the workstation reaches the sign-in screen. If the workstation does not power on or displays an error, stop and contact Meridian Support with the ticket ID. Do not include passwords in the ticket.
Permission result
A service agent may view the related CRM customer and quote reference but cannot change the quote price or approve a discount. A sales or finance correction route is required.
9.3 Independent challenge sample solution
Routing
Ticket	Department	Queue	Reason
MER-TKT-501	Installation Support	Installation L1	Installation category
MER-TKT-502	Technical Support	Technical L2	High equipment failure
MER-TKT-503	Installation Support	Installation L1	Installation category
MER-TKT-504	Service Data Review	Unassigned Review	Missing customer
MER-TKT-505	Technical Support	Technical L2	High equipment failure
First-response calculations
MER-TKT-501:
Friday: 16:30–17:00 = 0.5 hours
Monday: 09:00–09:30 = 0.5 hours
Total = 1 business hour
The Standard target is 4 hours, so it is within target.
MER-TKT-502:
Friday: 16:30–17:00 = 0.5 hours
Monday: 09:00–10:30 = 1.5 hours
Total = 2 business hours
The High target is 1 hour, so it breached and should have escalated at approximately Monday 09:30.
MER-TKT-505:
Created: 13:00
First response: 13:30
Elapsed: 0.5 business hours
It is within the High target and should not escalate.
Pending-customer treatment for MER-TKT-503
The supplied pause is:
Pending Customer: 10:30–15:05
The service report should exclude that period from active resolution time if the synthetic pause rule has been correctly recorded. The ticket should retain:
- first human response at 10:00;
- pause start at 10:30;
- customer reply or resume at 15:05;
- resolution at 11:00 on the next business day.
The report must state whether the pause is excluded from resolution time. It must not silently remove the ticket from the report.
Missing-context treatment for MER-TKT-504
The ticket is routed to Service Data Review. It should not be counted as a normal routed ticket until the customer is identified or the case is closed with an exception reason.
Completed article
Field	Completed value
Article ID	MER-KB-201
Title	What to include when reporting an equipment failure
Owner	Technical Support Lead
Reviewer	Service Manager
Version	1.0
Status	In Review until approved
Audience	Customers and Technical Support agents
Article content:
Include these details when reporting an equipment failure:  
- device or workstation identifier;  
- time the problem began;  
- visible error message;  
- whether the device powers on;  
- whether the problem affects one user or several users;  
- preferred contact method.  

Safe stop condition: Do not open equipment covers or attempt electrical repairs. Contact Meridian Support with the ticket ID and the information above.
This is synthetic Meridian support content. The article should not be published until the Technical Support Lead and Service Manager complete the defined review.
10. Chapter recap and next step
A service process is reliable when every ticket has a clear intake, owner, target, escalation route, customer context and resolution record.
You should now be able to:
- design ticket intake from supported channels;
- distinguish departments, queues and assignees;
- route tickets using category, severity and customer context;
- define service targets with calendars, units and exclusions;
- calculate first-response and resolution times;
- configure escalation conditions and owners;
- separate customer notifications from internal notes;
- display CRM context without bypassing sales permissions;
- assign knowledge-base ownership and publication review;
- create reproducible service metrics;
- test missing customer context, overdue response, permission and article-publication cases.
For the Meridian Supply project, this chapter produces:
C01_CH15_Meridian_Desk_Intake_and_Routing_Design
C01_CH15_Meridian_Department_Queue_and_Assignment_Matrix
C01_CH15_Meridian_Service_Target_and_Escalation_Register
C01_CH15_Meridian_CRM_Service_Context_Design
C01_CH15_Meridian_Knowledge_Base_Ownership_and_Article
C01_CH15_Meridian_Service_Test_and_Reporting_Evidence
The next chapter applies similar process controls to employee processes with People. The employee process remains separate from customer service and requires stricter confidentiality boundaries.
11. Glossary and further reading
Glossary
Term	Definition
Assignee	Person currently responsible for acting on a ticket
Department	Organisational service function responsible for a type of work
Escalation	Action taken when a service target or risk condition requires higher attention
First human response	First response from a service agent, excluding an automated acknowledgement
Knowledge base	Collection of reviewed support articles for agents or customers
Queue	Work list from which tickets are assigned or processed
Resolution time	Time from ticket start to resolution, using the declared pause rules
Service-level target	Defined expected time for a service event
Ticket	One service case with customer, issue, status, ownership and evidence
Ticket intake	Process by which a customer request becomes a service ticket
Ticket routing	Selection of department, queue and assignee
Unassigned review	Queue for tickets that cannot yet be routed safely
Further reading
Check the current Zoho Desk edition, channel support, departments, assignment rules, service targets, escalations, CRM context, knowledge base and reporting behavior before implementation:
- Zoho Desk Help (https://help.zoho.com/portal/en/kb/desk)
- Zoho Desk documentation (https://www.zoho.com/desk/help/)
- Zoho Desk automation help (https://help.zoho.com/portal/en/kb/desk/automate-business-processes)
- Zoho CRM Help (https://help.zoho.com/portal/en/kb/crm)
- Zoho Flow Help (https://help.zoho.com/portal/en/kb/flow)
This chapter has not verified current Zoho Desk screens, service-level behavior, channel support, CRM integration, article permissions or reporting definitions in a live environment. Synthetic service targets and ticket results are expected learning outputs, not product execution observations.
continuity:
  previous_continuity:
    supplied: "C01-CH14"
    source_artifacts:
      - "C01_CH14_Meridian_CRM_to_Books_Flow_Design"
      - "C01_CH14_Meridian_Flow_Mapping_and_Connection_Register"
      - "C01_CH14_Meridian_Execution_History_Test_Evidence"
      - "C01_CH14_Meridian_Failed_Handoff_Recovery_Record"
      - "C01_CH14_Meridian_Payment_Status_Flow_Design"
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
      - MER-QUOTE-003
      - MER-QUOTE-004
      - MER-QUOTE-101
      - MER-QUOTE-102
      - MER-QUOTE-103
      - MER-QUOTE-104
      - MER-QUOTE-105
      - MER-CUST-101
      - MER-QUOTE-201
      - MER-QUOTE-202
      - MER-QUOTE-203
      - MER-QUOTE-204
      - MER-SVC-301
      - MER-SVC-302
      - MER-SVC-303
      - MER-SVC-304
      - MER-PROD-WS-001
      - MER-PROD-INST-001
      - MER-PROD-SUP-001
      - MER-PROD-DOCK-001
      - MER-PROD-MON-001
      - MER-PB-STD-2026
      - MER-PB-PARTNER-2026
      - MER-QUOTE-301
      - MER-QUOTE-302
      - MER-QUOTE-303
      - MER-QUOTE-304
      - MER-CUST-301
      - MER-CUST-302
      - MER-CUST-303
      - MER-CUST-304
      - MER-QUOTE-401
      - MER-QUOTE-402
      - MER-QUOTE-403
      - MER-QUOTE-404
      - MER-CUST-401
      - MER-CUST-402
      - MER-CUST-403
      - MER-CUST-404
      - MER-BOOK-CUST-101
      - MER-BOOK-CONTACT-101
      - MER-BOOK-QUOTE-101
      - MER-ITEM-WS-001
      - MER-ITEM-INST-001
      - MER-ITEM-SUP-001
      - MER-ORDER-101
      - MER-INVOICE-101
      - MER-PAY-101
      - MER-ADJ-101
      - MER-BOOK-CUST-301
      - MER-BOOK-CONTACT-301
      - MER-ORDER-301
      - MER-INVOICE-301
      - MER-PAY-301
      - MER-ADJ-301
      - MER-BOOK-CUST-401
      - MER-ORDER-401
      - MER-INVOICE-401
      - MER-PAY-401
      - MER-HO-101
      - MER-HO-102
      - MER-QUOTE-FLOW-102
      - MER-HO-201
      - MER-HO-202
      - MER-HO-203
      - MER-HO-204
      - MER-ORDER-203
      - MER-ITEM-DOCK-001
      - MER-PAY-402
      - MER-PAY-403
      - MER-PAY-404
      - MER-INVOICE-402
      - MER-INVOICE-403
      - MER-INVOICE-404
    added_for_service_practice:
      - MER-TKT-301
      - MER-TKT-302
      - MER-TKT-303
      - MER-TKT-304
      - MER-TKT-401
      - MER-TKT-402
      - MER-TKT-403
      - MER-TKT-404
      - MER-TKT-405
      - MER-TKT-501
      - MER-TKT-502
      - MER-TKT-503
      - MER-TKT-504
      - MER-TKT-505
      - MER-KB-001
      - MER-KB-101
      - MER-KB-201
  case_decisions:
    - "Meridian service departments are Installation Support, Technical Support, Billing Questions and Service Data Review."
    - "Installation tickets route to Installation L1; High equipment failures route to Technical L2; billing tickets route to Billing L1."
    - "Tickets with missing customer context route to Service Data Review."
    - "Synthetic Standard targets are 4 business hours for first human response and 2 business days for resolution."
    - "Synthetic High targets are 1 business hour for first human response and 1 business day for resolution."
    - "Business hours are Monday to Friday, 09:00–17:00 local time."
    - "Automated acknowledgements do not count as human responses."
    - "Knowledge articles require an owner, reviewer, version and publication status."
    - "Desk service context may display CRM customer and commercial references without allowing service agents to edit approved quote values."
  artifacts:
    - "C01_CH15_Meridian_Desk_Intake_and_Routing_Design"
    - "C01_CH15_Meridian_Department_Queue_and_Assignment_Matrix"
    - "C01_CH15_Meridian_Service_Target_and_Escalation_Register"
    - "C01_CH15_Meridian_CRM_Service_Context_Design"
    - "C01_CH15_Meridian_Knowledge_Base_Ownership_and_Article"
    - "C01_CH15_Meridian_Service_Test_and_Reporting_Evidence"
  open_case_assumptions_next_chapter:
    - "The exact current Zoho Desk channels, assignment behavior, service targets, escalations, CRM context and knowledge-base permissions must be verified."
    - "The next chapter must keep employee records and customer-service records in separate access boundaries."
    - "Service reporting must preserve ticket-level timestamps and exclusions before being combined with broader course dashboards."
    - "Any service-to-CRM or service-to-Flow connection must preserve customer identity and failure-recovery evidence."
END OF C01-CH15
