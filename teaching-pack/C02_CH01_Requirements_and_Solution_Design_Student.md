schema_version: "1.1"
course_id: "C02"
chapter_id: "C02-CH01"
chapter_number: 1
chapter_title: "Requirements and Solution Design"
filename: "C02_CH01_Requirements_and_Solution_Design_Student.md"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "partially_verified"
---
Requirements and Solution Design
1. What you will learn
A successful Zoho solution begins before you create a form or write Deluge. You first need to understand the work, agree on what the solution must do, decide where information belongs and record why you chose one design over another.
In this chapter, you will learn to:
- distinguish functional requirements from non-functional requirements;
- identify the people involved without confusing business roles with Zoho product profiles;
- write testable acceptance criteria;
- decide which system owns each type of data;
- identify constraints, assumptions and missing information;
- choose configuration or code deliberately;
- create an architecture decision record;
- produce a technical specification;
- draw and explain a solution diagram.
These skills contribute directly to the Nova Field Service course project. Your Chapter 1 evidence will be the first version of:
- the requirements register;
- the data ownership and access design;
- the configuration-versus-code decisions;
- the architecture decision records;
- the technical specification;
- the solution diagram.
Later chapters will build the Creator forms, reports, pages, workflows, Deluge functions, integrations and tests from these decisions. If the design is vague, later implementation will be difficult to test and maintain.
Scenario baseline
Nova Field Service is a fictional service company that handles service requests, dispatch, technician visits, inspections and completion. Its proposed Creator application will connect to CRM customer and service information.
No earlier chapter supplied schemas, field API names or integration contracts. Therefore, the following are explicit Chapter 1 assumptions:
Area	Chapter 1 assumption
Request intake	An internal Dispatcher enters requests in the first release. A customer-facing portal is out of scope for this chapter.
CRM ownership	CRM is the source of truth for customer identity and service information.
Creator ownership	Creator is the source of truth for service requests, visits, inspections and completion workflow.
Business identifiers	NOV-CUST-001, NOV-REQ-001 and NOV-VISIT-001 are business identifiers. They are separate from Zoho-generated record IDs.
Business roles	Dispatcher, Technician, Service Manager and Administrator are scenario roles. They are not assumed to be native Zoho profiles.
Product configuration	Exact field API names, API version, data centre and edition-specific menu labels must be confirmed before implementation.
Contact data	All example contact details are synthetic and use example.com.
Prerequisites
You should already understand CRM records, fields and workflows and have basic programming familiarity. Deluge is taught in later chapters, so this chapter explains where code may be needed without requiring you to write Deluge.
2. Lessons
Lesson 1: Turn a work story into requirements
A stakeholder usually describes a problem in work language:
“When a customer calls about a failed pump, the dispatcher needs to find the customer, record the problem, send someone and know whether the visit is complete.”
That sentence contains several possible requirements, but it is not precise enough to build or test. A requirement states a capability or quality that the solution must provide.
A functional requirement describes something the solution must do. Examples include creating a request, assigning a technician, recording inspection results and preventing a duplicate request.
A non-functional requirement describes how well, how safely or under what operational conditions the solution must work. Examples include access control, response time, auditability, recoverability and maintainability.
A useful requirement statement contains:
1. an identifier;
2. an actor or system;
3. an action or quality;
4. the data or condition involved;
5. an observable result.
For example:
FR-001: A Dispatcher must be able to create a service request for an existing CRM customer with a service description, priority and preferred visit window.
This is stronger than:
The app should handle requests.
Questions for discovery
Use questions that expose the start, end, rules and exceptions of a process.
Discovery area	Questions to ask
Start	What event creates a request? Who is allowed to create it?
Required information	What must be known before dispatch can begin? Which values may be unknown initially?
Decisions	How is priority chosen? Who can change it?
Ownership	Which team is accountable for the request, visit and final completion?
Completion	What evidence proves that a job is complete?
Exceptions	What happens if the customer cannot be found, the technician is unavailable or the inspection fails?
Timing	Is there a due time, a target response time or only a preferred window?
Reporting	Which records and measures must each role see?
Integration	Which system supplies customer and service information? What happens if it cannot be reached?
Security	Which users may view, create, edit or approve each record?
Evidence handling
Do not convert every stakeholder statement directly into a requirement. Record its source and whether it is confirmed.
Evidence ID	Source	Statement or observation	Type
E-001	Dispatcher interview	“I need the customer’s service plan before assigning a visit.”	Business need
E-002	Technician interview	“I should see my assigned visits and the inspection form.”	Access need
E-003	Existing spreadsheet	Requests have a preferred visit window but no due date.	Current-state fact
E-004	Service Manager	“A failed inspection must not be marked complete.”	Business rule
E-005	Implementation discussion	Duplicate protection may be needed during CRM retry.	Design concern
A useful evidence record preserves the original wording, source, date and confidence. If two people disagree, keep both statements visible until the decision is made. Do not silently choose a baseline.
Drawing a process map
Use a small set of consistent conventions:
- rectangles represent systems or stored data;
- rounded rectangles represent human activities;
- arrows show direction;
- arrow labels describe the data or decision;
- a solid arrow means a normal flow;
- a dashed arrow means a lookup, optional flow or exception;
- a boundary around a group shows system ownership;
- an explicit error path shows recovery rather than hiding failure.
The map is not decoration. It helps you ask where data is created, where it changes and which system must be trusted.
Quick check
1. Is “The application must be easy to use” functional or non-functional?
2. Rewrite “Dispatch should be faster” as an observable requirement without inventing a target.
3. Which evidence item above is not yet a confirmed requirement?
Lesson 2: Write acceptance criteria
Acceptance criteria define how someone can decide whether a requirement is satisfied. They are narrower than a general business goal.
A practical format is:
- Given a starting condition;
- When an action occurs;
- Then an observable result must occur.
Include a normal case and important negative cases.
For FR-001, a normal criterion could be:
Given an existing CRM customer and all required request information, when a Dispatcher submits the request, then Creator stores one new request with a business request identifier and status New.
A missing-data criterion could be:
Given that no CRM customer is selected, when the Dispatcher attempts to submit the request, then the request is not saved and the user is shown which customer information is required.
A permission criterion could be:
Given that a Technician is assigned to a different visit, when that Technician opens the visit, then the visit is not available for editing.
A recovery criterion could be:
Given that the CRM lookup times out, when the Dispatcher submits the request, then Creator keeps the request in Sync Pending or rejects it according to the approved contract, records the failure reason and does not create a second business request on retry.
Do not confuse an acceptance criterion with an implementation instruction. “Add a Deluge function called validateRequest” is an implementation detail. “A request with no customer cannot be submitted” is testable behavior.
Also distinguish completion from timeliness. If a record eventually reaches Completed, that proves only that it reached that state. It does not prove that a deadline was met. A deadline measure requires a due timestamp, a completion timestamp and an agreed rule for exclusions.
Requirement quality test
A requirement is ready for design review when it is:
- specific enough to understand;
- observable enough to test;
- assigned to an actor or system;
- linked to evidence;
- clear about missing and invalid values;
- clear about ownership;
- free from unexplained product jargon.
Quick check
For the statement “An inspection must pass before completion,” identify:
1. a normal acceptance criterion;
2. a failing inspection criterion;
3. the data needed to prove that a deadline was met, if a deadline is later introduced.
Lesson 3: Identify people, ownership and constraints
People involved
A solution has more participants than its logged-in users. Include people who provide information, make decisions, operate the process, support the system and receive results.
Participant	Responsibility in Nova Field Service	Information needed
Customer contact	Reports a service problem and confirms access details	Request status and visit information, subject to the selected release scope
Dispatcher	Enters and validates requests, assigns visits	Customer service information, request queue and technician availability
Technician	Performs the visit and records work and inspection evidence	Assigned visit, location, instructions and inspection form
Service Manager	Handles escalations, exceptions and service decisions	Workload, failed inspections and unresolved requests
Administrator	Maintains configuration, users and support settings	Configuration, audit information and operational diagnostics
Integration owner	Maintains the CRM connection and mapping	Connection status, mapping rules and failure records
Implementation engineer	Converts approved design into the application	Requirements, decisions, dependencies and test evidence
The role names above are business roles. They do not automatically create Zoho users, profiles, roles or permission sets. The implementation must map them to actual product access controls later.
Data ownership
Ownership answers “which system is authoritative when values disagree?” It is different from who happens to edit a record.
Data	Proposed owner	Consumer	Ownership rule
Customer identity	CRM	Creator and staff	Creator reads the approved CRM customer identity; it does not create a competing customer master
Service plan and entitlement	CRM	Dispatcher and Service Manager	CRM value is authoritative for the integration boundary
Service request	Creator	CRM, dispatch staff and managers	Creator owns the request lifecycle and business request identifier
Technician visit	Creator	Technician, Dispatcher and manager	Creator owns scheduling and visit status
Inspection result	Creator	Technician, manager and completion workflow	Creator owns inspection evidence and pass/fail outcome
Completion state	Creator	CRM and reports	Completion requires the stated evidence, not merely a date
OAuth connection	Zoho connection configuration	Integration process	The connection owner is an administrative responsibility, not a customer or technician
Product-generated record ID	Zoho product	Application and integration	Store and map it where needed, but do not use it as the business identifier
A source of truth is the system whose approved value wins. A data consumer may read or display the value without owning it.
Constraints
Constraints limit the design. Record them instead of discovering them after implementation.
Typical Nova constraints include:
- only synthetic data may be used for learning and testing;
- customer and service information must remain governed by CRM ownership;
- the first release has internal request intake;
- the business requires duplicate protection;
- a Technician must not see another Technician’s private work notes;
- integration failures must be visible and recoverable;
- exact product permissions depend on the selected Zoho edition and environment;
- the API version, regional endpoint and field API names must be confirmed before the integration is built;
- future chapters cover detailed API, OAuth and Deluge syntax.
An assumption is something you currently believe but have not verified. A constraint is a condition the design must respect. A decision is an approved choice. Label all three.
Quick check
A Dispatcher changes a customer’s legal name in Creator because the CRM lookup is unavailable. Is that an ownership decision, a recovery action or a design violation? Explain what the design should do instead.
Lesson 4: Decide between configuration and code
Configuration uses supported product settings such as forms, fields, lookups, reports, permissions, workflows and process stages. Code uses a script or program to express logic that configuration cannot safely or clearly provide.
A configuration-first approach is usually easier to inspect, explain and maintain. Code is appropriate when the rule is complex, reusable, cross-system or dependent on calculations and controlled recovery.
The official Zoho Creator quickstart describes applications built from forms, lookup relationships, workflows, reports, pages and process features. These are useful configuration candidates, but exact availability and labels can depend on the product edition and account environment. The design decision still belongs in your project record.
Need	Configuration-first choice	Code may be justified when
Required request fields	Mandatory fields and validation settings	The rule depends on several related records
Customer selection	Lookup or controlled integration mapping	A custom matching or reconciliation algorithm is required
Basic status display	Report filter or grouped report	A derived status depends on several systems
Simple notification	Workflow notification	Routing depends on complex ownership or escalation rules
Inspection completion gate	Process stage and validation	The gate needs reusable checks across several entry points
Duplicate protection	Unique or controlled business key where supported	Replay handling requires an idempotency record and cross-system check
CRM synchronization	Connection and mapped action	Retry, response interpretation and recovery require reusable logic
Audit detail	Product audit capability and explicit fields	A business event ledger or correlation ID is required
Calculation	Formula or supported expression	The calculation needs reusable functions, null handling or external data
Use these decision questions:
1. Can a supported configuration feature express the rule completely?
2. Can a user understand and change it safely?
3. Does it work for every path that can change the data?
4. Does it provide the required error and audit behavior?
5. Does it avoid creating a second source of truth?
6. Will the same rule be reused elsewhere?
7. Is a product limitation forcing code?
Do not write code merely because a rule is important. Important rules still need the simplest reliable implementation.
This chapter does not include Deluge code. When later chapters show Deluge, they must identify whether the script runs in a Creator form event, Creator function, CRM function or Flow step, its inputs, connection and return or failure shape.
Quick check
Choose configuration, code or a combination for each item:
1. Show only requests with status Ready for Dispatch.
2. On a CRM timeout, retry safely and preserve a correlation key.
3. Prevent a Technician from editing a visit assigned to another Technician.
4. Calculate a fixed priority from three controlled fields.
Give one reason for each choice.
Lesson 5: Record architecture decisions and specifications
An architecture decision record, or ADR, captures a significant choice, its context and its consequences. It prevents a later developer from reversing a decision accidentally.
A useful ADR contains:
Field	Purpose
ID and title	Identifies the decision
Status	Proposed, accepted, superseded or rejected
Context	Explains the problem
Options considered	Shows alternatives
Decision	States the selected option
Consequences	Describes benefits, costs and risks
Verification	States how the decision will be checked
Owner and date	Provides accountability
A technical specification turns the approved requirements into an implementable design. At minimum it should contain:
- scope and out-of-scope behavior;
- actors and access boundaries;
- functional and non-functional requirements;
- entities, business identifiers and lifecycle states;
- data ownership and mappings;
- configuration-versus-code choices;
- integration boundary and failure behavior;
- acceptance criteria;
- dependencies, assumptions and open questions;
- named diagrams and versioned artifacts.
A good specification is complete enough that another engineer can build a first testable version without asking what “done” means.
3. Visual explanation
Nova Field Service solution boundary
flowchart LR
    C[Customer contact] -. request information .-> D[Dispatcher]
    D -->|create and validate request| CF[Creator application]
    CF --> R[(Creator: Requests)]
    CF --> V[(Creator: Visits)]
    CF --> I[(Creator: Inspections)]
    CF -. read customer and service data .-> CRM[(CRM: Customer and Service data)]
    CRM -. mapped customer result .-> CF
    D -->|assign| V
    T[Technician] -->|visit notes and inspection| V
    T --> I
    I -->|pass or fail| G{Completion gate}
    G -->|pass| R
    G -->|fail| M[Service Manager exception queue]
    CF -->|approved summary and correlation key| CRM
    CRM -. timeout or permission error .-> E[Sync error state and recovery record]
    E --> CF
Plain-text explanation:
1. A customer contact gives information to a Dispatcher.
2. The Dispatcher uses Creator to create and validate a request.
3. Creator reads customer and service information from CRM; it does not become the customer master.
4. Creator stores the request, visit and inspection records because those records describe the operational service process.
5. A Technician records the visit and inspection.
6. A completion gate allows completion only after the required inspection evidence passes.
7. A failed inspection goes to a Service Manager exception path.
8. A CRM timeout or permission error creates a visible recovery state. It must not silently create a second request.
9. The business flow and the integration flow are related but separate. A request can remain operationally visible while its synchronization state is Pending or Error.
Design question	Answer in this diagram
Where is a request created?	Creator
Where is customer identity authoritative?	CRM
Who performs the work?	Technician
What proves completion?	Required inspection result and completion rule
What happens on integration failure?	Preserve the business record, store a sync state and provide recovery
Is a product-generated ID the business key?	No; use a stable business key and map product IDs separately
4. Worked case
Case inputs
The following evidence was collected for the first Nova design workshop.
Evidence ID	Source	Input
E-101	Dispatcher	“I need to search the customer before I schedule anything.”
E-102	Technician	“I need only my assigned visits, with instructions and a place for notes.”
E-103	Service Manager	“A failed inspection must be visible and must block completion.”
E-104	Administrator	“If CRM is unavailable, the team must know what failed and retry without creating another request.”
E-105	Existing process sheet	Customer, service type, description, priority and preferred visit window are captured. No due timestamp is present.
E-106	Implementation constraint	The first release is for internal users. A customer portal is not included.
Synthetic records used in the design:
Business ID	Record type	Values
NOV-CUST-001	CRM customer	Northstar Facilities Ltd; contact Maya Chen; maya.chen@northstar.example.com (mailto:maya.chen@northstar.example.com)
NOV-REQ-001	Creator request	Pump pressure low; High priority; preferred window 2026-10-07 09:00–12:00
NOV-VISIT-001	Creator visit	Assigned to TECH-001; scheduled for 2026-10-07 10:00
TECH-001	Business technician ID	Priya Nair; priya.nair@nova.example.com (mailto:priya.nair@nova.example.com)
No due timestamp is supplied. Therefore, this case cannot prove that a response deadline was met.
Step 1: Convert evidence into requirements
ID	Requirement
FR-001	A Dispatcher can create a request for an existing CRM customer with service type, description, priority and preferred visit window.
FR-002	The application prevents submission when the customer, description or priority is missing.
FR-003	A Dispatcher or authorized Service Manager can assign a request to a Technician and create a visit.
FR-004	An assigned Technician can view and update the assigned visit and record inspection evidence.
FR-005	A request cannot enter Completed unless the required inspection result is Pass.
FR-006	The application displays CRM customer and service information using a stable customer business identifier.
FR-007	A repeated submission with the same external request key does not create a second business request or duplicate CRM action.
FR-008	A synchronization failure is stored with a readable reason, correlation key and recovery state.
NFR-001	A Technician can access only assigned operational visits and permitted inspection information.
NFR-002	The system preserves an audit trail for assignment, inspection and completion changes.
NFR-003	The design uses configuration for simple rules and reusable code only where configuration cannot express the rule safely.
NFR-004	The request remains visible when an integration operation fails, unless the approved contract explicitly rejects the transaction.
Step 2: Define ownership and lifecycle
Entity	Owner	Business key	Lifecycle
Customer	CRM	NOV-CUST-001	Active, inactive
Service request	Creator	NOV-REQ-001	New, Validated, Ready for Dispatch, Assigned, In Progress, Awaiting Inspection, Completed, Cancelled
Technician visit	Creator	NOV-VISIT-001	Scheduled, Started, Completed, No Show, Cancelled
Inspection	Creator	Inspection business key linked to request and visit	Pending, Pass, Fail
Synchronization state	Creator integration record or controlled fields	External request key plus correlation key	Not Required, Pending, Succeeded, Error
Business status and synchronization status are separate. A request can be Assigned while its CRM summary is Sync Error.
Step 3: Define acceptance criteria
Requirement	Given	When	Then
FR-001	NOV-CUST-001 exists in CRM	A Dispatcher submits complete request data	One Creator request is stored with a new business request key
FR-002	The description is null	The Dispatcher submits the form	The request is rejected with a field-level error and no incomplete request is created
FR-004	NOV-VISIT-001 is assigned to TECH-001	TECH-001 opens the visit	The Technician can see and update that visit
FR-005	The inspection result is Fail	A user attempts completion	Completion is rejected and the request remains in an exception state
FR-007	A request with external key EXT-REQ-1001 already exists	The same key is submitted again	The existing request is returned or reported; no second request is created
FR-008	CRM returns a timeout	The synchronization action runs	The request remains visible, sync state is Error or Pending, and the failure is retryable
NFR-001	A Technician is assigned to NOV-VISIT-001 but not NOV-VISIT-002	The Technician requests NOV-VISIT-002	Access is denied or no record is returned according to the approved access design
Step 4: Configuration-versus-code decisions
Decision ID	Requirement	Decision	Reason
ADR-001	Required fields and controlled priority values	Configuration	Standard form validation is understandable and sufficient
ADR-002	Customer relationship	Configuration plus controlled mapping	A lookup expresses the relationship; integration mapping supplies the CRM value
ADR-003	Inspection completion gate	Configuration-first process rule	A clear state transition is easier to inspect and test
ADR-004	Duplicate protection across retries	Reusable code or integration logic	The rule must compare a business key across operation attempts and preserve recovery data
ADR-005	CRM failure recovery	Reusable integration logic	Response handling, correlation and retry behavior must be consistent
ADR-006	Technician access	Product access configuration plus record criteria	Access should be enforced by the platform and reviewed with negative tests
Step 5: Completed technical specification
Artifact: C02-CH01_Nova_Field_Service_Technical_Specification_v0.1.md
Scope
The first release supports internal request intake, customer lookup, dispatch, technician visits, inspection capture, completion control and a CRM synchronization boundary.
Out of scope
Customer self-service login, route optimization, payment processing, payroll, mobile device management and any unapproved modification of CRM customer master data are out of scope.
System responsibilities
- CRM owns customer identity and service information.
- Creator owns request, visit, inspection and completion workflow.
- The integration maps records using business identifiers and a stored correlation key.
- A product-generated record ID is retained only as a technical mapping value.
Access design
Business role	Request access	Visit access	Inspection access
Dispatcher	Create and manage operational requests	Schedule and assign	View results
Technician	View assigned requests	View and update assigned visits	Create or update assigned inspection
Service Manager	View all operational requests	Reassign and resolve exceptions	View all results and approve exceptions
Administrator	Support access subject to audit	Support access subject to audit	Support access subject to audit
The names in this table are business roles. The implementation must map them to actual Zoho access mechanisms and confirm whether record-level restrictions are available for the selected environment.
Integration contract
- Input from CRM: customer business ID, customer display name and approved service information.
- Input to Creator: a valid CRM mapping result or an explicit missing/invalid response.
- Output from Creator to CRM: approved request summary, Creator business request ID and external request key, only where the final integration contract authorizes the write.
- Duplicate key: external request key.
- Correlation key: one value per synchronization attempt.
- Failure outcomes: Invalid Customer, Permission Denied, Timeout, Duplicate, Validation Error or Unknown.
- Recovery: preserve the Creator request, store the failure state, expose the reason to an authorized operator and retry only with the same business key.
- Exact REST version, regional endpoint, scopes and field API names are intentionally implementation dependencies for the later CRM API and OAuth chapters. They must be confirmed before any live request is built.
Traceability
Requirement group	Design evidence
FR-001 to FR-002	Request form specification and validation criteria
FR-003 to FR-004	Visit entity, assignment rule and access matrix
FR-005	Inspection entity and completion gate
FR-006	CRM ownership rule and mapping contract
FR-007 to FR-008	External key, correlation key and recovery design
NFR-001	Access matrix and negative access tests
NFR-002	Audit fields and change history requirement
NFR-003	ADR register
NFR-004	Sync state and retry behavior
Mistake and correction
Mistake: The first draft says, “All Nova service data belongs in CRM because CRM contains the customer.”
Why it is wrong: Customer identity and operational service work are different data responsibilities. Moving visits and inspections into CRM without a business decision could create duplicate process ownership, unclear access and conflicting status values.
Correction: CRM owns customer identity and service information. Creator owns the operational request, visit and inspection lifecycle. The integration exchanges only the mapped data required by the approved contract.
A second mistake is to label Completed_At as proof that a service-level deadline was met. The correction is to add Due_At and define the calculation and exclusions before reporting on timeliness.
5. Try it yourself — guided practice
Learning goal
Produce a small technical specification and solution diagram from evidence. Your artifact must include requirements, acceptance criteria, ownership, constraints, configuration-versus-code decisions and recovery behavior.
Requirements and access
Use a Creator development or sandbox environment only if one is available to you. Do not use production customer data. If your account does not expose the required features, use the offline alternative at the end.
The official Zoho Creator quickstart demonstrates creating an application from the application builder, adding forms and lookup relationships, and using workflows, reports and pages. Product labels and availability can vary by edition. For this practice, you may create only a draft application shell and document the remaining configuration rather than publishing anything.
Sample inputs
Evidence:
ID	Source	Observation
G-001	Dispatcher	A request must identify a customer and service type before assignment.
G-002	Technician	A Technician needs only assigned visits and must record arrival and completion notes.
G-003	Service Manager	A failed inspection must return the request to an exception state.
G-004	Administrator	The same external key may be delivered twice after an integration retry.
G-005	Access review	A Technician must not edit another Technician’s visit.
Records:
business_id,record_type,customer_id,service_type,priority,external_key,assigned_technician,inspection_result
NOV-REQ-002,request,NOV-CUST-001,Boiler noise,Medium,EXT-REQ-2002,TECH-001,
NOV-REQ-003,request,NOV-CUST-002,Door access failure,High,EXT-REQ-2003,TECH-002,Fail
NOV-REQ-004,request,NOV-CUST-999,Air filter replacement,Low,EXT-REQ-2004,,
NOV-REQ-005,request,NOV-CUST-001,Boiler noise,Medium,EXT-REQ-2002,TECH-001,
Customer reference data:
customer_id,customer_name,contact_email,crm_lookup_status
NOV-CUST-001,Northstar Facilities Ltd,maya.chen@northstar.example.com,Found
NOV-CUST-002,Riverbend Clinics,omar.khan@riverbend.example.com,Found
NOV-CUST-999,Unknown customer,missing@example.com,Missing
The repeated EXT-REQ-2002 is intentional. NOV-CUST-999 is an intentional missing-data exception. A timeout case is supplied as a scenario rather than a record:
The CRM lookup for EXT-REQ-2004 times out after the request has been entered but before the synchronization result is stored.
Steps and expected intermediate results
1. Classify the evidence.  
Expected result: at least five evidence-backed requirements and one explicit constraint.
2. Write functional and non-functional requirements.  
Expected result: each requirement has an ID, actor or system, behavior or quality and source.
3. Define acceptance criteria.  
Include a normal request, a null or missing customer, a duplicate external key, a permission denial and a CRM timeout.  
Expected result: every scenario has a visible result and recovery choice.
4. Assign ownership.  
Decide who owns customer identity, requests, visits, inspections and synchronization state.  
Expected result: no item has two authoritative systems.
5. Make three architecture decisions.  
At least one must choose configuration, one must choose code or integration logic and one must address access.  
Expected result: each decision includes an alternative and consequence.
6. Create the technical specification.  
Use the following worksheet before writing the completed artifact.
Specification field	Column guidance
Scope	What this release does
Out of scope	What it deliberately does not do
Actors	Business participants and responsibilities
Functional requirements	IDs and observable behavior
Non-functional requirements	Security, reliability, audit or performance
Data entities	Owner, business key and lifecycle
Integration boundary	Inputs, outputs, duplicate key and failures
Access design	View, create, edit and exception access
Configuration decisions	Rules suitable for supported settings
Code decisions	Rules needing reusable logic
Open assumptions	Unverified facts
Acceptance evidence	What a tester will observe
7. Draw the solution.  
Show Dispatcher, Creator, CRM, Technician, inspection gate and failure recovery. Label arrows with the data or action being transferred.  
Expected result: the diagram clearly separates CRM ownership from Creator operational ownership.
8. Walk the four records.  
- NOV-REQ-002 should follow the normal path.
- NOV-REQ-003 should be blocked or returned by the failed inspection.
- NOV-REQ-004 should stop at missing customer mapping.
- NOV-REQ-005 should be recognized as a duplicate of NOV-REQ-002, not as a new business action.
Final artifact and cleanup
Your final artifact should contain:
- at least five functional requirements;
- at least three non-functional requirements;
- at least five acceptance criteria;
- an ownership table;
- an access table;
- three architecture decisions;
- a recovery state for missing data, permission denial, duplicate input and timeout;
- one complete Mermaid diagram and a text explanation.
If you created a draft application, remove only the draft records and application that you created, or leave it clearly named as a training draft. Do not alter production data or shared applications.
Offline alternative
Create the specification and Mermaid diagram in a Markdown file without opening Zoho Creator. This demonstrates requirements reasoning and architecture communication, but it cannot demonstrate actual product permissions, form behavior, lookup configuration or workflow execution.
6. Independent challenge
Changed constraints
Design a second release for emergency service requests with these constraints:
1. A Dispatcher can mark a request as Emergency.
2. An emergency request requires an incident description and a callback number.
3. A Service Manager may reassign an emergency visit.
4. A Technician may update an assigned visit but may not change its customer or priority.
5. Customer identity still belongs to CRM.
6. If CRM is unavailable, the emergency request must remain visible in Creator and show CRM Sync Pending.
7. A retry with the same external key must not create a second request or second emergency notification.
8. The first response target is a proposed business target of 30 minutes. It is not an observed result and must not be reported as achieved without timestamps.
9. The first release remains internal; do not add a customer portal.
Challenge data
external_key,customer_id,service_type,priority,incident_description,callback_number,assigned_technician,crm_status
EXT-EM-3001,NOV-CUST-001,Water leak,Emergency,Water entering electrical room,+1-555-010-0101,TECH-001,Found
EXT-EM-3002,NOV-CUST-002,Access failure,Emergency,,+1-555-010-0102,TECH-002,Found
EXT-EM-3003,NOV-CUST-003,Generator alarm,Emergency,Alarm active,+1-555-010-0103,TECH-001,Permission Denied
EXT-EM-3001,NOV-CUST-001,Water leak,Emergency,Water entering electrical room,+1-555-010-0101,TECH-001,Found
Customer reference:
customer_id,customer_name,contact_email
NOV-CUST-001,Northstar Facilities Ltd,maya.chen@northstar.example.com
NOV-CUST-002,Riverbend Clinics,omar.khan@riverbend.example.com
NOV-CUST-003,Harbor View Offices,li.wei@harborview.example.com
Deliverables
Produce:
- a scope statement and out-of-scope statement;
- six functional requirements and four non-functional requirements;
- acceptance criteria for a valid emergency, missing incident description, CRM permission denial and duplicate delivery;
- ownership and access tables;
- four ADRs;
- a complete technical specification;
- a diagram showing emergency notification, CRM synchronization and retry;
- a measurement definition for the proposed 30-minute response target.
Do not provide the solution in the challenge artifact. Use the supplied data only. In particular, treat the missing incident description and duplicate external key as test inputs, not as facts to hide.
Success criteria
Your design succeeds when another engineer can determine:
- why EXT-EM-3002 is rejected or held;
- why EXT-EM-3003 remains visible without inventing a successful CRM result;
- why the repeated EXT-EM-3001 does not produce another business action;
- which role may reassign the visit;
- how the 30-minute measure uses timestamps and excludes unfinished records.
7. Common problems and recovery
Symptom	Likely diagnosis	Correction
“The app should be flexible” appears as the only requirement	Quality is undefined	Specify the user, behavior, data and observable result
Two systems both edit customer names	Ownership is missing	Declare CRM authoritative and make Creator read-only for that value
A Technician can see every visit	Business role was confused with product access	Map the role to record-level access and test another Technician’s record
A duplicate retry creates two requests	No stable external key or idempotency rule	Store and compare the external key before creating the second action
A null customer becomes “Unknown customer” and is accepted	Missing data was converted into a misleading value	Keep the field null or route to an explicit exception state
CRM timeout deletes the Creator request	Integration failure was allowed to control business data	Preserve the request and store Sync Pending or Sync Error
A completed timestamp is used as SLA proof	No due time or start rule exists	Add Due_At, Started_At, Completed_At and an exclusion rule
Configuration is replaced by a large script	The design did not test simpler options	Revisit the configuration-versus-code ADR
An API field is named from its screen label	Display label was mistaken for field API name	Confirm the actual API name in the target environment before implementation
A draft diagram has arrows with no meaning	Flow direction and data are ambiguous	Label each arrow and separate normal and exception paths
8. Check your understanding
1. Classify each item as functional or non-functional:
- The Dispatcher can create a request for an existing customer.
- A Technician cannot edit another Technician’s visit.
- A failed synchronization remains visible and retryable.
- The application records who approved completion.
2. Rewrite this statement as a testable requirement: “Managers need better visibility.”
3. Which system owns customer identity in the worked case, and why does Creator still need a customer reference?
4. A request reaches Completed on October 8. No due timestamp exists. What can you conclude about timeliness?
5. Which is the safer design for a repeated integration delivery: use the display name as a match, or use an external request key? Explain.
6. A Technician has permission to use the application but is assigned to no visit. What should the access design test?
7. Choose configuration or code for a fixed list of priorities. Then choose configuration or code for safe duplicate prevention across retries.
8. Name the minimum recovery information you would store after a CRM permission error.
9. From the guided-practice data, what should happen to NOV-REQ-004 and NOV-REQ-005?
10. In the independent challenge, what timestamps are required to evaluate a 30-minute first-response target?
9. Solutions and explanations
Lesson quick checks
1. “The application must be easy to use” is non-functional because it describes a quality. It needs a measurable usability criterion before it can be tested.
2. “Dispatch should be faster” is incomplete without a target. A safe rewrite is: “The solution must display the request queue with priority, customer and current assignment so that a Dispatcher can select the next request without opening unrelated records.” This makes the needed capability observable without inventing a time measurement.
3. E-005 is a design concern and assumption, not a confirmed requirement. It must be validated through the integration contract.
For the acceptance-criteria check:
1. Normal: Given a valid request with a passing inspection, when an authorized user completes it, then the request enters Completed and retains the inspection evidence.
2. Failure: Given an inspection result of Fail, when an authorized user attempts completion, then the transition is rejected and the request enters or remains in an exception state.
3. Deadline evidence: a due timestamp, the event that starts the response clock, a completion or response timestamp, the unit of measurement and exclusion rules. A completion date alone is insufficient.
For the ownership check, changing a customer’s legal name in Creator is a design violation, not a valid recovery action. The Dispatcher should see an explicit CRM-unavailable state, use an approved temporary reference only if the business has defined one, or wait for recovery. Creator should not silently become a competing customer master.
For the configuration check:
1. A filtered request report is configuration.
2. Safe retry with a correlation key is integration logic or reusable code.
3. Technician record access uses product access configuration and record criteria.
4. A fixed priority calculation is configuration if supported by the selected feature; code is justified only if the rule is reusable or depends on complex data.
Guided-practice sample solution
A valid requirement set includes:
ID	Requirement
GFR-001	A Dispatcher can create a request for a CRM customer with service type and priority.
GFR-002	A request cannot be submitted without a customer, service type and priority.
GFR-003	A Technician can view and update only an assigned visit.
GFR-004	A failed inspection prevents completion and creates an exception state.
GFR-005	A repeated external key is recognized as an existing business request.
GFR-006	CRM permission or timeout failures are visible and retryable.
GNF-001	Customer identity remains CRM-owned.
GNF-002	Technician access is restricted by assignment.
GNF-003	The system retains an audit trail for assignment and inspection changes.
Valid acceptance results:
Input	Expected result
NOV-REQ-002	Valid request; create or retain one request and assign the visit to TECH-001
NOV-REQ-003	Inspection Fail blocks completion and routes the request to an exception state
NOV-REQ-004	Missing CRM customer mapping; do not create a valid downstream business action
NOV-REQ-005	Duplicate of EXT-REQ-2002; return or reference the existing request and do not create another
CRM timeout for EXT-REQ-2004	Preserve the request with Sync Pending or Sync Error, store the reason and retry with the same key
Completed guided-practice ADRs:
ADR	Decision	Consequence
G-ADR-001	Use Creator configuration for required fields and controlled priority values	Users can inspect and maintain the basic rules
G-ADR-002	Use an external key for duplicate protection	Retries can be recognized without matching unreliable display text
G-ADR-003	Use assignment-based access for Technician visits	Negative access tests are required for unassigned visits
G-ADR-004	Preserve requests during CRM timeout	Support needs a sync status and retry action
The guided diagram should contain these paths:
flowchart LR
    D[Dispatcher] -->|request data| C[Creator request]
    C -. customer lookup .-> CRM[(CRM customer data)]
    C --> V[Assigned visit]
    T[Technician] -->|visit and inspection| V
    V --> I{Inspection}
    I -->|Pass| Done[Complete]
    I -->|Fail| X[Exception]
    C -->|same external key| K[Duplicate check]
    CRM -. timeout or missing mapping .-> S[Sync Pending or Error]
    S -->|retry same key| C
The missing customer is an exception because the required authoritative record cannot be found. The repeated external key is not a missing-data case; it is a replay case. These cases require different explanations and recovery actions.
Independent-challenge sample solution
A coherent requirement set is:
ID	Requirement
EM-FR-001	A Dispatcher can create an emergency request with customer, service type, incident description and callback number.
EM-FR-002	The application marks the request as Emergency and routes it to the emergency queue.
EM-FR-003	A Service Manager can reassign an emergency visit.
EM-FR-004	A Technician can update an assigned emergency visit but cannot change its customer or priority.
EM-FR-005	A CRM permission failure leaves the request visible with CRM Sync Pending or CRM Sync Error.
EM-FR-006	A repeated external key produces no second request or emergency notification.
EM-NFR-001	CRM remains authoritative for customer identity.
EM-NFR-002	Emergency assignment and notification actions are auditable.
EM-NFR-003	Recovery uses the same external key and correlation information.
EM-NFR-004	The proposed 30-minute target is measured only when the required timestamps exist.
Acceptance results:
- EXT-EM-3001 is valid and may enter the emergency queue.
- EXT-EM-3002 is held or rejected because the incident description is null. The callback number alone does not satisfy the requirement.
- EXT-EM-3003 has a CRM permission failure. The request may remain visible in Creator, but the design must not claim that CRM synchronization succeeded. The error is recorded for an authorized retry or correction.
- The second EXT-EM-3001 is a replay. It must reference the existing request and must not send a second emergency notification.
Completed access design:
Role	Emergency request	Assignment	Priority	Customer
Dispatcher	Create and view operational records	View assignment	Set at creation	Select from CRM mapping
Technician	View assigned visit	Cannot reassign	Cannot change	Read-only
Service Manager	View all emergency records	Reassign	Approve changes	Read-only from CRM
Administrator	Support access with audit	Support access	Support access	No master-data ownership
The 30-minute measure is:
\[
\text{First-response duration} =
\text{First\_Response\_At} - \text{Emergency\_Created\_At}
\]
For each record, record:
- Emergency_Created_At;
- First_Response_At;
- timezone or normalized timestamp rule;
- whether the record was cancelled or invalid;
- whether unfinished records are excluded or counted as open;
- the proposed target of 30 minutes.
The challenge data contains no timestamps, so it cannot demonstrate that the target was met. It can demonstrate that the design correctly identifies the missing measurement inputs.
A complete challenge diagram could be:
flowchart LR
    D[Dispatcher] -->|emergency request| C[Creator emergency queue]
    C -->|customer lookup| CRM[(CRM customer master)]
    C -->|authorized notification| N[Emergency notification]
    C --> V[Emergency visit]
    M[Service Manager] -->|reassign| V
    T[Technician] -->|assigned visit update| V
    CRM -. permission error .-> P[CRM Sync Pending or Error]
    P -->|retry using same external key| C
    C --> K{Duplicate key check}
    K -->|new key| N
    K -->|existing key| R[Reference existing action]
The diagram makes the duplicate check occur before a second notification. It also keeps the operational request visible when CRM access fails.
Check-your-understanding answers
1. - Dispatcher can create a request: functional.
- Technician cannot edit another visit: non-functional security requirement, expressed through observable access behavior.
- Failed synchronization remains visible and retryable: non-functional reliability requirement.
- Application records who approved completion: non-functional auditability requirement.
2. A testable version is: “A Service Manager can view a report containing all requests in New, In Progress, Awaiting Inspection and Exception states, with customer, priority, assigned Technician and last status-change time.”
3. CRM owns customer identity because it is the authoritative customer master. Creator still needs a customer reference to associate operational requests with the correct CRM customer and to display approved customer information.
4. You can conclude only that the request reached Completed on October 8. You cannot conclude that it met a deadline because no due timestamp or response-time rule exists.
5. Use the external request key. Display names can change or be shared by multiple customers. A stable external key supports replay detection and mapping.
6. Test that the Technician cannot view or edit another Technician’s visit, cannot discover it through a report or search, and cannot update it through an alternate action or integration path.
7. Fixed priorities are configuration when a supported choice field is sufficient. Safe duplicate prevention across retries requires an external key and usually reusable integration logic because it must coordinate attempts and recovery.
8. Store the business key, correlation key, operation, timestamp, failure category, readable message, retry state and the identity of the authorized operator or process that handled it.
9. NOV-REQ-004 should enter a missing-customer exception because NOV-CUST-999 is not found in CRM. NOV-REQ-005 should be recognized as a duplicate of NOV-REQ-002 because both use EXT-REQ-2002.
10. At minimum, measure the emergency creation timestamp and first-response timestamp. Also define timezone handling, which event starts the clock, which event stops it and whether cancelled, invalid or unfinished records are excluded.
10. Chapter recap and next step
Requirements and solution design connect business work to implementation.
You should now be able to:
- write functional requirements that describe observable behavior;
- write non-functional requirements for access, reliability, audit and maintainability;
- use evidence instead of assumptions;
- define acceptance criteria with normal, invalid, permission and recovery cases;
- distinguish business roles from product permissions;
- assign a system of record for each important data group;
- identify constraints and open assumptions;
- choose configuration before code when it is sufficient;
- record architecture choices and consequences;
- produce a technical specification and solution diagram;
- design duplicate protection and recovery without hiding failures.
Your project artifact from this chapter is:
C02-CH01_Nova_Field_Service_Technical_Specification_v0.1.md
The next chapter builds the programming and developer-tooling foundation needed to implement and test the design. It will cover types, collections, functions, JavaScript, HTTP, REST, JSON, Postman, browser tools, Git, code review and environment configuration. It will use the identifiers and ownership decisions recorded here rather than inventing a new baseline.
11. Glossary and further reading
Glossary
Acceptance criterion  
A testable condition that defines when a requirement is satisfied.
Architecture decision record (ADR)  
A short record of an important design choice, the alternatives considered and its consequences.
Business identifier  
A stable identifier meaningful to the business, such as NOV-REQ-001.
Configuration  
Supported product settings used to express behavior without writing custom program logic.
Constraint  
A condition that limits the possible design.
Correlation key  
An identifier used to connect one operation attempt, log entry or integration response to a business action.
Functional requirement  
A capability or behavior that the solution must provide.
Idempotency  
The property that repeating the same operation does not create additional unintended business effects.
Non-functional requirement  
A quality, boundary or operational condition such as security, reliability or auditability.
Source of truth  
The system whose approved value is authoritative when systems disagree.
System of record  
The system that owns the lifecycle and authoritative storage of a particular record type.
Technical specification  
An implementable description of scope, behavior, data, access, integrations, decisions and verification.
Further reading
- Zoho Creator Quickstart Guide (https://www.zoho.com/creator/help/new-quickstart-guide.html) — official examples of Creator applications, forms, lookup relationships, workflows, reports and pages.
- Zoho Creator Resource Center (https://www.zoho.com/creator/help/) — official product documentation and links for application development, users, environments and APIs.
- Zoho CRM API and SDK Library (https://www.zoho.com/crm/developer/api.html) — official overview of CRM REST, Bulk, Notification and Query API families.
- Zoho CRM Sandbox (https://www.zoho.com/crm/developer/sandbox.html) — official overview of testing and controlled deployment environments.
continuity:
  record_ids:
    customer: "NOV-CUST-001"
    request: "NOV-REQ-001"
    visit: "NOV-VISIT-001"
  case_decisions:
    - "CRM is authoritative for customer identity and service information."
    - "Creator is authoritative for requests, visits, inspections and completion workflow."
    - "Business identifiers remain distinct from Zoho-generated record IDs."
    - "The first release uses internal request intake; a customer portal is out of scope."
    - "Technician access is restricted to assigned operational records."
    - "Duplicate protection uses an external business key and preserves the original request during integration failure."
  artifact_names:
    - "C02-CH01_Nova_Field_Service_Technical_Specification_v0.1.md"
    - "C02-CH01_Nova_Field_Service_Solution_Diagram_v0.1.mmd"
    - "C02-CH01_Nova_Field_Service_ADR_Register_v0.1.md"
  open_case_assumptions:
    - "Creator form names and field API names have not yet been verified in a target environment."
    - "The CRM REST API version, regional endpoint and OAuth scopes are implementation dependencies for later chapters."
    - "No response deadline is established for NOV-REQ-001 because no due timestamp was supplied."
    - "The mapping of business roles to native Zoho permissions remains to be confirmed."
END OF C02-CH01
