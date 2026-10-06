schema_version: "1.1"
course_id: "C02"
chapter_id: "C02-CH05"
chapter_number: 5
chapter_title: "Creator Access and Portals"
filename: "C02_CH05_Creator_Access_and_Portals_Student.md"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "partially_verified"
---
Creator Access and Portals
1. What you will learn
An interface can show the correct records and still be insecure if the underlying data operation does not enforce access. Access design must answer four different questions:
1. Who is the user?
2. Which application or component may the user open?
3. Which records may the user view or change?
4. Which fields and actions are allowed for that user?
In this chapter, you will learn to:
- distinguish authentication from authorization;
- distinguish business roles from Creator users, roles and permissions;
- design access at application, form, report, record and action levels;
- use ownership and criteria-based record access;
- separate internal users from external portal users;
- design controlled sharing;
- protect customer and Technician views;
- test normal, unauthorized and missing-mapping scenarios.
The required practice is to implement restricted customer and Technician views.
Continuity and scope clarification
Chapter 1 defined the first Nova release as internal request intake and placed a customer portal out of scope. The fixed course practice for this chapter requires a restricted customer view.
To preserve continuity, this chapter makes the following explicit scope change:
The customer-facing view is a future-release prototype created in a development or training environment. It is not silently added to the Chapter 1 internal-release baseline.
The Technician view remains part of the internal release design. The customer prototype demonstrates how a future portal boundary could be designed without claiming that the portal is approved for production.
Contribution to the course project
This chapter produces:
- a user and business-role mapping;
- an access matrix;
- internal Dispatcher, Technician, Service Manager and Administrator access rules;
- a restricted customer view prototype;
- record-level access tests;
- evidence that unauthorized users cannot view or change records through alternate paths.
The customer and Technician views must use the forms and reports from Chapters 3 and 4:
- Customer_Reference;
- Service_Requests;
- Technicians;
- Jobs;
- Inspection_Items;
- Requests to Assign;
- My Jobs;
- Inspection Exceptions;
- the role-based Pages.
Explicit product assumptions
Zoho’s official Creator quickstart describes managing users, roles and permissions from the product’s management area and assigning access to solutions. It also describes internal application users and a portal capability for external stakeholders.
Exact role names, permission controls, portal options, record-sharing behavior and edition dependencies must be checked in the target Creator environment. This chapter teaches the access method and completed design artifacts without claiming that a particular account configuration was executed.
2. Lessons
Lesson 1: Separate identity, authentication and authorization
An identity is the person or system account being represented. Authentication proves that the person controls that identity. Authorization determines what the authenticated identity may do.
These are different:
Question	Example
Who is this?	priya.nair@nova.example.com
Has the identity authenticated?	The account completed the approved sign-in process
Which business role applies?	Technician
Which records may be viewed?	Jobs assigned to TECH-001
Which fields may be changed?	Visit notes and inspection rows
Which actions may be executed?	Start assigned Job; submit inspection
A successful login does not grant access to every record.
Internal and external identities
An internal user is part of the organization’s application workforce. A portal user is an external stakeholder who receives a controlled view of selected application data.
For Nova:
- Dispatcher, Technician, Service Manager and Administrator are internal business roles.
- A customer contact such as maya.chen@northstar.example.com is an external customer identity for the future portal prototype.
- A customer portal account must not be treated as an internal Administrator or Dispatcher account.
- The customer’s CRM record and portal identity must be linked deliberately.
Do not use an email address alone as the business relationship. Email can change, be shared or be entered incorrectly. Use a controlled mapping to Customer_Business_ID.
Business role versus product role
A business role describes work responsibility:
Technician
A product role or permission set controls product behavior. They may have similar names, but they are not automatically equivalent.
The correct design process is:
1. list the business responsibilities;
2. identify the required actions and records;
3. map those needs to available product permissions;
4. test both allowed and denied operations;
5. record gaps or compensating controls.
A business role should not receive broad access merely because the product has a similarly named role.
Quick check
1. Does a successful login prove that a Technician may view every Job?
2. Why is Technician in the Nova scenario not automatically a native Creator permission?
3. Why should a customer portal identity be separate from an internal Dispatcher identity?
Lesson 2: Design permissions in layers
Access is easier to reason about when divided into layers.
Layer	Question	Nova example
Account or environment	May this identity use the environment?	User is admitted to the development application
Application	May the identity open Nova Field Service?	Customer prototype has limited application access
Component	May the identity open this form, report or Page?	Technician can open My Jobs but not configuration
Record	Which rows can the identity see or change?	Technician sees assigned Jobs
Field	Which fields are editable?	Technician cannot edit customer or priority
Action	Which operation may be executed?	Service Manager may reassign; Technician may start
Data operation	What happens when a direct request is made?	Unauthorized update is rejected
Not every product edition exposes every layer in the same way. If field-level controls are unavailable for a requirement, use a separate restricted form or action and enforce the rule in the server-side operation.
Least privilege
Least privilege means giving a user only the access needed for their task.
A Technician usually needs:
- read access to assigned Job details;
- edit access to visit notes;
- edit access to inspection rows;
- permission to start or submit an assigned Job;
- no access to application configuration;
- no access to another Technician’s Jobs;
- no permission to change customer, priority or assignment.
A Dispatcher usually needs:
- create and manage Requests;
- view customer reference information;
- create and assign Jobs;
- view operational exceptions;
- no permission to change CRM customer master data;
- no permission to manage users unless separately assigned.
A Service Manager needs broader operational visibility but still does not automatically own CRM administration.
Deny by default
A secure design starts with no access, then grants required access. This makes an untested new form or report less likely to expose every record.
A hidden navigation item is not the same as denied access. A user may still reach a record through:
- a related lookup;
- a direct record URL;
- an alternate report;
- an action;
- an API or integration;
- an exported file.
Test the operation at the data boundary.
Quick check
A Technician can open My Jobs, but can also find another Technician’s Job through a global search. Is the access design complete? Explain.
Lesson 3: Use ownership and criteria for record access
Record access answers which rows a user may view or modify. The common patterns are ownership, criteria and controlled sharing.
Ownership
A record owner is the user or responsibility holder associated with the record. Technical record ownership and business responsibility are not always identical.
For a Job:
- the assigned Technician is the operational worker;
- the Dispatcher may be the creator;
- the Service Manager may be the escalation owner;
- the product’s record owner may be one of these or a separate application owner.
Do not assume that assigning a Technician automatically changes every product ownership field. Define the relationship explicitly.
Criteria-based access
Criteria-based access derives visibility from record values or mappings.
Examples:
Technician may view Jobs where:
Job.Technician.Technician_Business_ID
matches
CurrentUser.Technician_Business_ID
Customer may view Requests where:
Request.Customer.Customer_Business_ID
matches
CurrentPortalUser.Customer_Business_ID
The exact expression and current-user reference depend on the product configuration. The design rule is the important part: use a stable mapping, not a display name.
Controlled sharing
Sharing grants a person or group access to selected records.
Examples:
- share one urgent Job with a Service Manager;
- share all operational records with the Dispatch team;
- share a customer’s own Requests with that customer portal identity;
- share an exception record with an Administrator.
Avoid broad sharing when a criteria rule is sufficient. Explicit sharing can become difficult to audit if records change ownership or the person leaves the organization.
Read and edit are separate
A user may need to read a value without changing it.
Role	Customer	Priority	Technician assignment	Visit notes
Dispatcher	Read	Edit before dispatch	Edit	Read
Technician	Read	Read	Read	Edit own Job
Service Manager	Read	Edit with reason	Edit	Read and support
Customer prototype	Read approved subset	Read	Read if exposed	Read approved summary
If the product cannot express a field-level restriction on one form, expose a separate form or action with only the fields the role is allowed to change.
Quick check
A Technician should see the customer name and service description but not change the customer lookup or priority. Which access layers are involved?
Lesson 4: Map users to business records safely
The application needs a reliable way to connect a signed-in user to a business record.
For Technicians, use a controlled mapping:
Application identity	Business role	Business record
priya.nair@nova.example.com	Technician	TECH-001
daniel.ortiz@nova.example.com	Technician	TECH-002
For customers:
Portal identity	Business role	Customer record
maya.chen@northstar.example.com	Customer contact	NOV-CUST-001
omar.khan@riverbend.example.com	Customer contact	NOV-CUST-002
The mapping must be:
- unique within the intended environment;
- created or approved by an authorized Administrator;
- protected from ordinary users;
- auditable;
- updated when a person changes role or organization;
- tested when the mapping is missing or duplicated.
Do not derive a customer ID from an email address at runtime. The email can be a login attribute, but the customer relationship should be an explicit mapping.
Multiple contacts
A customer may have more than one portal contact. Avoid forcing one customer record to contain one user identity if the business needs multiple contacts.
A separate mapping entity may contain:
- portal identity;
- Customer lookup;
- contact status;
- allowed view;
- start date;
- end date.
This allows one customer to have several approved contacts without duplicating the Customer Reference record.
Joiner, mover and leaver events
Access must change when a user:
- joins the organization;
- moves from Dispatcher to Service Manager;
- becomes inactive;
- changes employer;
- no longer represents a customer.
A user remaining in an old role after changing jobs is an access defect even if the application data is correct.
Quick check
What should happen when priya.nair@nova.example.com is removed from the Technician mapping? Should she continue to see old Jobs?
Lesson 5: Distinguish internal users and portal users
An internal application user is normally managed as part of the organization’s application access model. A portal user is an external identity with a limited purpose and controlled data boundary.
The distinction matters because:
- internal users may need operational reports and actions;
- customers should not see other customers’ records;
- portal users may need a different authentication and onboarding flow;
- portal users should not inherit internal roles;
- support and data-sharing obligations differ;
- a portal view must expose only the fields approved for external use.
Nova customer prototype
The Chapter 1 baseline excludes a customer portal. For the Chapter 5 practice, create a future-release prototype with this boundary:
Customer portal users may:
- view their own customer summary;
- create or view their own service requests if the future release approves intake;
- view approved Job status and scheduled window;
- view a customer-safe completion summary.
Customer portal users may not:
- view CRM technical IDs;
- view internal notes;
- view Technician contact details unless separately approved;
- change priority;
- assign a Technician;
- view other customer records;
- retry synchronization;
- manage users or configuration.
The prototype must be labelled:
Future Release — Customer View Prototype
Do not describe it as part of the current internal release.
Portal record boundary
The safest customer rule is:
Portal user → explicit Customer_Business_ID mapping
           → only records linked to that Customer Reference
Do not expose a general Request report and assume that a filter alone will protect it. The record access rule must be applied to every customer-facing entry point.
Quick check
Why should a customer portal not reuse the Dispatcher Queue with one extra filter?
Lesson 6: Design access tests
An access requirement is incomplete until it has an observable test.
Use four test categories:
1. allowed access;
2. denied access;
3. missing or invalid mapping;
4. alternate path.
Access test structure
Test field	Example
Identity	technician.one@nova.example.com
Mapped business record	TECH-001
Resource	NOV-VISIT-001
Operation	View or edit
Expected result	Allowed
Evidence	Screen result, response, audit entry or error
Cleanup	Remove test user or sample record
Alternate-path testing is important. If a Technician cannot see a Job in My Jobs, also test:
- direct Job report;
- related Request;
- lookup search;
- action URL;
- export or download;
- API or integration route when applicable.
Access test matrix
Test ID	User	Target	Operation
AT-001	Dispatcher	New Request	Create
AT-002	Technician TECH-001	Job NOV-VISIT-001	View
AT-003	Technician TECH-001	Job assigned to TECH-002	View
AT-004	Technician TECH-001	Own Job	Change priority
AT-005	Service Manager	Any operational Job	Reassign
AT-006	Customer NOV-CUST-001	Own Request	View approved fields
AT-007	Customer NOV-CUST-001	Customer NOV-CUST-002 Request	View
AT-008	Unmapped user	Any Job	View
AT-009	Technician	Sync Exception	Retry
AT-010	Customer portal user	User management	Open
Negative tests are evidence
A test that proves a permitted user can open a record does not prove that another user cannot. Both sides are required.
Do not use a production user to test a denial if that could affect real data. Use synthetic identities and development records.
Quick check
What alternate path should you test if a customer cannot see another customer’s Request in the Customer Requests report?
3. Visual explanation
Access decision flow
flowchart TD
    U[Authenticated identity] --> M{Identity mapping exists?}
    M -->|No| D[Reject and record access exception]
    M -->|Yes| R{Business role allowed?}
    R -->|No| D
    R -->|Yes| C{Record matches access criteria?}
    C -->|No| D
    C -->|Yes| O{Operation permitted?}
    O -->|No| D
    O -->|Yes| F{Field or action preconditions pass?}
    F -->|No| V[Show validation or transition error]
    F -->|Yes| A[Allow operation and audit result]
Plain-text explanation:
1. The system identifies the authenticated account.
2. It checks whether the account has a controlled business mapping.
3. It checks the assigned business role.
4. It checks whether the target record belongs to the allowed scope.
5. It checks whether the requested operation is permitted.
6. It checks field and lifecycle conditions.
7. It either allows the operation or returns a controlled denial or validation result.
Access concept	Nova example
Identity	technician.one@nova.example.com
Mapping	TECH-001
Role	Technician
Record criterion	Job.Technician = TECH-001
Operation	View and update visit notes
Denied operation	Change customer or priority
Audit result	Allowed or denied with time and actor
4. Worked case
Scope decision
The first release from Chapter 1 remains internal. The following customer view is a future-release prototype:
C02-CH05-SCOPE-001
Future Release — Customer View Prototype
This scope label is part of the artifact. It prevents the prototype from being mistaken for an approved production commitment.
Case inputs
Users:
identity,identity_type,business_role,business_record_id,active
dispatcher.one@nova.example.com,internal,Dispatcher,,true
technician.one@nova.example.com,internal,Technician,TECH-001,true
technician.two@nova.example.com,internal,Technician,TECH-002,true
manager.one@nova.example.com,internal,Service Manager,,true
admin.one@nova.example.com,internal,Administrator,,true
maya.chen@northstar.example.com,future_portal,Customer,NOV-CUST-001,true
omar.khan@riverbend.example.com,future_portal,Customer,NOV-CUST-002,true
unmapped.user@nova.example.com,internal,Unmapped,,true
Records:
request_business_id,customer_business_id,priority,request_status,sync_status,assigned_technician
NOV-REQ-001,NOV-CUST-001,High,Assigned,Succeeded,TECH-001
NOV-REQ-002,NOV-CUST-002,Medium,New,Pending,
NOV-REQ-005,NOV-CUST-001,High,Assigned,Error,TECH-002
NOV-REQ-006,NOV-CUST-002,Low,Completed,Succeeded,TECH-002
job_business_id,request_business_id,technician_business_id,job_status,visit_notes
NOV-VISIT-001,NOV-REQ-001,TECH-001,Started,Pressure inspection in progress
NOV-VISIT-002,NOV-REQ-002,,Scheduled,
NOV-VISIT-005,NOV-REQ-005,TECH-002,Assigned,
NOV-VISIT-006,NOV-REQ-006,TECH-002,Completed,Door mechanism repaired
Step 1: Complete access matrix
Role	Component	View	Create	Edit
Dispatcher	Service Requests	Operational requests	Yes	Operational fields
Dispatcher	Jobs	All operational Jobs	Yes	Assignment and schedule
Technician	My Jobs	Assigned Jobs	No	Notes and inspection rows
Service Manager	Jobs and Requests	All operational records	Limited	Reassign and resolve exceptions
Administrator	Configuration	Support scope	As approved	Configuration and access
Customer prototype	Own Requests and approved Jobs	Own customer-linked records	Future scope only	Approved customer fields only
Step 2: Apply record criteria
Technician TECH-001:
Allow Job view when:
Jobs.Technician.Technician_Business_ID = TECH-001
Customer NOV-CUST-001:
Allow Request view when:
Service_Requests.Customer.Customer_Business_ID = NOV-CUST-001
Service Manager:
Allow operational Request and Job view across the approved Nova application
Unmapped user:
No operational record access
The exact Creator configuration that expresses these criteria must be verified in the target environment. These are completed access rules, not claims about a particular menu or syntax.
Step 3: Evaluate records
Identity	Target	Expected result	Reason
Technician TECH-001	NOV-VISIT-001	Allowed	Assigned Technician matches
Technician TECH-001	NOV-VISIT-005	Denied	Assigned to TECH-002
Technician TECH-002	NOV-VISIT-005	Allowed	Assigned Technician matches
Technician TECH-002	NOV-REQ-005 priority	Denied edit	Priority is not Technician-editable
Customer NOV-CUST-001	NOV-REQ-001	Allowed in prototype	Customer mapping matches
Customer NOV-CUST-001	NOV-REQ-002	Denied	Different customer
Customer NOV-CUST-002	NOV-REQ-006	Allowed in prototype	Customer mapping matches
Unmapped user	Any Job	Denied	No business record mapping
Technician TECH-001	Retry NOV-REQ-005 sync	Denied	Sync recovery is not a Technician action
Step 4: Field restrictions
A Technician may update:
- Visit_Notes;
- permitted inspection subform fields;
- a controlled start or completion action.
A Technician may not update:
- Customer;
- Priority;
- Request_Status directly;
- Technician;
- Sync_Status;
- External_Request_Key;
- CRM technical mapping fields.
The Customer prototype may view:
- Customer Name;
- Request Business ID;
- Request Status;
- scheduled window;
- approved completion summary.
It may not view:
- CRM Record ID;
- internal notes;
- synchronization error details;
- other customers’ records;
- internal Technician contact information unless approved.
Mistake and correction
Mistake: The implementation creates a “Technician” role with access to the entire Jobs report and hides the Assign and Retry buttons.
Why it is wrong: The user can still see other Technicians’ records, and hidden actions do not protect direct updates or alternate reports.
Correction: Restrict record visibility to the mapped Technician business ID, limit editable fields and enforce the same rule on every Job update path.
A second mistake is mapping customer access by email text inside each Request. The correction is to link the portal identity to Customer_Business_ID through a controlled mapping record and filter records through the Customer lookup.
Completed artifact
Artifact: C02-CH05_Nova_Field_Service_Access_Design_v0.1.md
The artifact contains:
1. user-to-role mapping;
2. role-to-component access;
3. role-to-record criteria;
4. editable field list;
5. action preconditions;
6. allowed and denied test matrix;
7. future-release customer scope label;
8. joiner, mover and leaver procedure.
5. Try it yourself — guided practice
Learning goal
Implement restricted Technician access and a clearly labelled future-release customer view prototype using the Chapter 3 forms and Chapter 4 Pages.
Product access and safety
Use a Creator development or sandbox environment. Use synthetic identities under example.com. Do not use production data or real customer credentials.
The official Creator quickstart describes adding users from the management area and assigning access to solutions. Use the available product controls in your environment, but do not assume that the visible business role names are native product profiles.
Sample inputs
Create or map these identities:
identity,scenario_role,business_record_id,view_scope
dispatcher.one@nova.example.com,Dispatcher,,All operational requests and jobs
technician.one@nova.example.com,Technician,TECH-001,Assigned jobs only
technician.two@nova.example.com,Technician,TECH-002,Assigned jobs only
manager.one@nova.example.com,Service Manager,,All operational exceptions
maya.chen@northstar.example.com,Customer,NOV-CUST-001,Future prototype own records
unmapped.user@nova.example.com,Unmapped,,No operational access
Use these records:
job_business_id,request_business_id,customer_business_id,technician_business_id,job_status
NOV-VISIT-001,NOV-REQ-001,NOV-CUST-001,TECH-001,Started
NOV-VISIT-005,NOV-REQ-005,NOV-CUST-001,TECH-002,Assigned
NOV-VISIT-006,NOV-REQ-006,NOV-CUST-002,TECH-002,Completed
Steps and expected intermediate results
 1. Create the synthetic internal users or document the user setup if your account cannot add them.  
Expected result: each identity has a documented role and mapping.
 2. Create an internal access mapping record or approved configuration table.  
Expected result: technician.one@nova.example.com maps only to TECH-001; no user maps to both Technicians.
 3. Grant the Dispatcher, Technician, Service Manager and Administrator the minimum application and component access needed for the Chapter 4 Pages.  
Expected result: a Technician can open the Technician Page but cannot open configuration components.
 4. Configure the Technician’s My Jobs report using the approved current-user-to-Technician mapping.  
Expected result: TECH-001 sees NOV-VISIT-001, while TECH-002 sees NOV-VISIT-005 and NOV-VISIT-006.
 5. Restrict Technician edits to visit notes and inspection fields.  
Expected result: a Technician can save notes on an assigned Job but cannot change customer, priority or Technician assignment.
 6. Configure the future-release Customer View Prototype.  
Expected result: the Page is labelled as a future-release prototype and displays only approved customer fields.
 7. Configure the prototype customer criteria.  
Expected result: maya.chen@northstar.example.com sees records linked to NOV-CUST-001 and not records linked to NOV-CUST-002.
 8. Test the unmapped identity.  
Expected result: unmapped.user@nova.example.com cannot open operational records.
 9. Test alternate paths.  
Attempt to access:
- the other Technician’s Job from a direct report;
- a related Request;
- a lookup;
- a hidden action;
- the Sync Exceptions report.
Expected result: the denial is consistent across paths.
10. Record results in the access test matrix.  
Expected result: every allowed and denied case has evidence and cleanup information.
Final artifact
Produce:
- C02-CH05_Nova_Field_Service_Access_Design_v0.1.md;
- user and mapping table;
- role and permission matrix;
- record criteria;
- restricted Technician Page;
- future-release Customer View Prototype;
- access test results;
- joiner, mover and leaver notes.
Cleanup
Remove synthetic users, mappings and sample records created for the practice, or clearly mark them as training identities. Remove the future-release prototype if it is not retained for later chapters.
Offline alternative
Create a complete access design and test matrix using the supplied data. Draw the access decision flow and describe how each role would be configured. This demonstrates access reasoning but cannot demonstrate actual Creator user, portal or record-sharing behavior.
6. Independent challenge
Changed constraints
Nova now allows a Service Manager to support two regions:
1. TECH-001 belongs to the North region.
2. TECH-002 belongs to the South region.
3. Dispatchers may view all operational Requests but may assign only active Technicians.
4. A regional Service Manager may view all Jobs in their region.
5. The Administrator may support both regions.
6. Customers still view only their own records.
7. A Technician must not see Jobs in another region, even if the Technician is temporarily unassigned.
8. A Job with Sync_Status = Error is visible to the Service Manager but not to the customer.
9. Customer portal scope remains a future-release prototype.
Challenge data
identity,identity_type,scenario_role,business_record_id,region,active
dispatcher.north@nova.example.com,internal,Dispatcher,,North,true
manager.north@nova.example.com,internal,Service Manager,,North,true
manager.south@nova.example.com,internal,Service Manager,,South,true
technician.one@nova.example.com,internal,Technician,TECH-001,North,true
technician.two@nova.example.com,internal,Technician,TECH-002,South,true
maya.chen@northstar.example.com,future_portal,Customer,NOV-CUST-001,North,true
omar.khan@riverbend.example.com,future_portal,Customer,NOV-CUST-002,South,true
job_business_id,request_business_id,customer_business_id,technician_business_id,region,job_status,sync_status
NOV-VISIT-020,NOV-REQ-020,NOV-CUST-001,TECH-001,North,Assigned,Succeeded
NOV-VISIT-021,NOV-REQ-021,NOV-CUST-002,TECH-002,South,Started,Succeeded
NOV-VISIT-022,NOV-REQ-022,NOV-CUST-001,,North,Scheduled,Error
NOV-VISIT-023,NOV-REQ-023,NOV-CUST-002,,South,Scheduled,Succeeded
Deliverables
Produce:
- a regional access matrix;
- Technician record criteria;
- North and South Manager criteria;
- Dispatcher assignment rules;
- customer prototype criteria;
- Sync Error visibility rules;
- at least ten access tests;
- normal, denied, unmapped and inactive-user cases;
- a note explaining how the future-release scope remains separate from the internal baseline.
Success criteria
Your design succeeds when:
- manager.north@nova.example.com can view North Jobs but not South Jobs;
- manager.south@nova.example.com can view South Jobs but not North Jobs;
- technician.one@nova.example.com cannot view NOV-VISIT-021;
- the Dispatcher can view operational records but cannot assign an inactive Technician;
- NOV-VISIT-022 is visible to the North Manager but not to maya.chen@northstar.example.com;
- each customer sees only the Customer-linked records;
- an inactive or unmapped identity is denied;
- the design does not convert the customer prototype into an approved internal-release feature.
7. Common problems and recovery
Symptom	Diagnosis	Correction
A Technician sees every Job	Component access was mistaken for record access	Add assignment-based record criteria
A customer sees another customer’s Request	Customer filter is missing or applied only to navigation	Enforce the customer relationship at every record path
A hidden action still works through another route	UI hiding was treated as authorization	Enforce operation permission at the data boundary
A user has two Technician mappings	Identity mapping is not unique	Correct the mapping and add an administrative validation
A departed Technician retains access	Leaver process is missing	Disable application access and remove or expire mapping
A Service Manager cannot investigate an exception	Manager scope is narrower than operational responsibility	Add approved regional or organization-wide exception access
Portal users can see CRM technical IDs	Internal and external field views were mixed	Create a customer-safe field projection
Customer portal is presented as production	Scope extension was not documented	Label it as future-release prototype and update continuity
A Technician can edit priority	Field restrictions are absent	Use restricted form/action and server-side validation
A customer cannot see their own record	Portal mapping is missing, stale or wrong	Verify the identity-to-customer mapping
An unmapped user sees a default report	Default access is too broad	Deny access until mapping and role exist
Shared records remain visible after reassignment	Explicit sharing was not expired	Review sharing and ownership on reassignment
Access differs between Page and report	Rules were configured in only one component	Apply and test the record boundary consistently
Admin credential is used for every action	Least privilege was bypassed	Create an approved service or role-specific path
8. Check your understanding
 1. What is the difference between authentication and authorization?
 2. A Technician can open the application but cannot view a Job assigned to another Technician. Which access layer is doing the work?
 3. Why should Customer_Business_ID be part of a customer portal mapping?
 4. Is a hidden Retry Sync button sufficient to prevent a Technician from retrying synchronization?
 5. A Customer portal user has access to a Request report with a customer filter. What additional test should you perform?
 6. What should happen to a Technician’s record mapping when the Technician leaves Nova?
 7. Distinguish the following:
- Technician business role;
- Creator application access;
- Job record criteria;
- editable fields.
 8. Why is the Customer View Prototype labelled as a scope change?
 9. A Service Manager can see a failed sync record but the customer cannot. Is that necessarily a defect?
10. A user has no business-role mapping but can open the Dispatcher Home Page. What is the likely access defect?
9. Solutions and explanations
Lesson quick checks
1. A successful login proves authentication, not authorization. The Technician must still be restricted to permitted Jobs and actions.
2. The scenario name Technician does not automatically create a native Creator permission. The role must be mapped to product capabilities.
3. A customer portal identity must be separate because customers should not inherit internal operational access.
For layered access:
- the Technician may have application access;
- the Job record criterion restricts rows to assigned Jobs;
- field permissions restrict editable values;
- action permissions restrict operations such as reassigning or retrying synchronization.
If a Technician can find another Job through global search, the record access boundary is incomplete even if My Jobs is correct.
For the mapping check, remove or expire the mapping. Whether historical records remain visible is a business decision, but ongoing access to operational records should not continue automatically after the user leaves. If support requires historical access, grant it through an approved support role rather than leaving the old Technician mapping active.
A customer portal should not reuse the Dispatcher Queue because the report contains operational fields, exception details, assignment data and potentially records belonging to other customers. A customer-safe view needs its own scope and fields.
Worked-case access results
User	Operation	Expected result
Dispatcher	View NOV-REQ-002	Allowed
Dispatcher	Assign NOV-VISIT-002 to active TECH-001	Allowed if other preconditions pass
Technician TECH-001	View NOV-VISIT-001	Allowed
Technician TECH-001	View NOV-VISIT-005	Denied
Technician TECH-001	Edit Priority on own Request	Denied
Technician TECH-001	Edit own visit notes	Allowed
Technician TECH-001	Retry NOV-REQ-005 synchronization	Denied
Service Manager	Reassign NOV-VISIT-005	Allowed
Customer NOV-CUST-001	View NOV-REQ-001 in prototype	Allowed
Customer NOV-CUST-001	View NOV-REQ-002	Denied
Unmapped user	View any operational Job	Denied
Independent-challenge sample solution
Regional record criteria:
North Manager:
Job.Region = North

South Manager:
Job.Region = South

TECH-001:
Job.Technician.Technician_Business_ID = TECH-001

TECH-002:
Job.Technician.Technician_Business_ID = TECH-002

Customer NOV-CUST-001:
Job.Request.Customer.Customer_Business_ID = NOV-CUST-001

Customer NOV-CUST-002:
Job.Request.Customer.Customer_Business_ID = NOV-CUST-002
Expected regional results:
User	Visible Job IDs
North Manager	NOV-VISIT-020, NOV-VISIT-022
South Manager	NOV-VISIT-021, NOV-VISIT-023
TECH-001	NOV-VISIT-020
TECH-002	NOV-VISIT-021
North customer	Only customer-approved records linked to NOV-CUST-001
South customer	Only customer-approved records linked to NOV-CUST-002
Dispatcher North	Operational records according to Dispatcher scope; assignment still requires active Technician
Administrator	Approved support scope for both regions
NOV-VISIT-022 is visible to the North Manager because it is a North Job with Sync_Status = Error. It is not visible to the customer because synchronization details are internal operational information.
A complete access test set includes:
Test ID	Identity	Target	Expected
REG-001	North Manager	NOV-VISIT-020	Allow
REG-002	North Manager	NOV-VISIT-021	Deny
REG-003	South Manager	NOV-VISIT-021	Allow
REG-004	South Manager	NOV-VISIT-020	Deny
REG-005	TECH-001	NOV-VISIT-020	Allow
REG-006	TECH-001	NOV-VISIT-021	Deny
REG-007	North customer	NOV-VISIT-022	Deny internal sync details
REG-008	South customer	NOV-VISIT-023	Allow approved customer-safe data
REG-009	Dispatcher North	assign to inactive Technician	Deny
REG-010	unmapped identity	any Job	Deny
REG-011	inactive user	any operational record	Deny
REG-012	Technician	change priority	Deny
Check-your-understanding answers
 1. Authentication proves who the identity is. Authorization decides what the identity may view or do.
 2. Record-level access is restricting the Job rows.
 3. The stable customer business ID connects the portal identity to the authoritative Customer Reference record without relying on a changeable display name or email text.
 4. No. The server-side operation must reject unauthorized retries even if the button is hidden.
 5. Test a direct record URL, related Request, lookup search, export and any alternate action. A filter on one report is not enough evidence.
 6. Disable or expire the mapping and remove application access where appropriate. Preserve historical records through an approved support process if needed.
 7. The Technician business role describes work responsibility. Application access allows entry to the app. Job record criteria restricts visible rows. Editable fields define which values the user may change.
 8. Chapter 1 explicitly placed the customer portal out of scope. The fixed practice requires a customer view, so the prototype is labelled as a future-release scope extension rather than silently changing the earlier baseline.
 9. No. A Service Manager may need internal synchronization details that are not appropriate for an external customer.
10. The default application or Page access is too broad, or the role-to-user mapping is missing. Access should be denied until the identity has an approved business mapping.
10. Chapter recap and next step
You should now be able to:
- distinguish identity, authentication and authorization;
- map business roles to product permissions deliberately;
- design application, component, record, field and action access;
- use ownership, criteria and controlled sharing;
- map internal users and future portal users to stable business records;
- design restricted Technician views;
- design customer-safe future-release views;
- test allowed, denied, unmapped and alternate access paths;
- separate interface visibility from real authorization;
- document scope changes instead of silently rewriting earlier decisions.
Your project artifacts from this chapter are:
- C02-CH05_Nova_Field_Service_Access_Design_v0.1.md;
- user and business-role mapping;
- role and permission matrix;
- Technician record criteria;
- future-release Customer View Prototype;
- access test matrix;
- joiner, mover and leaver procedure.
Chapter 6 builds workflows and process control. It will use the access boundaries from this chapter to decide who may validate, approve, transition, schedule, notify and recover each record.
11. Glossary and further reading
Glossary
Authentication  
The process of proving control of an identity.
Authorization  
The process of deciding what an authenticated identity may view or do.
Business role  
A responsibility in the organization, such as Dispatcher or Technician.
Criteria-based access  
Record visibility or operation permission derived from record values and user mappings.
Identity mapping  
A controlled link between an authenticated account and a business record or role.
Internal user  
An organizational user who works inside the application.
Least privilege  
Giving an identity only the access needed for its approved tasks.
Portal user  
An external stakeholder with a controlled application view.
Record owner  
The user or responsibility holder associated with a record; it may differ from operational assignment.
Role  
A grouping of permissions or responsibilities. A business role must be mapped deliberately to product permissions.
Sharing  
An explicit grant that allows another user or group to access selected records or components.
Scope extension  
A documented change that adds behavior or users beyond an earlier approved boundary.
Further reading
- Zoho Creator Resource Center (https://www.zoho.com/creator/help/) — official Creator documentation entry point.
- Zoho Creator Quickstart Guide (https://www.zoho.com/creator/help/new-quickstart-guide.html) — official examples of users, roles, permissions, reports and application components.
- Zoho Creator Users (https://help.zoho.com/portal/en/kb/creator/developer-guide/users) — official user-management documentation entry point.
- Zoho Creator Portal Documentation (https://help.zoho.com/portal/en/kb/creator/developer-guide/portal/understand-portal/articles/understand-portal) — official portal concepts and external-user documentation.
- Zoho Creator Add Users (https://www.zoho.com/creator/help/manage/users/add-users.html) — official user-management reference.
- Zoho Creator Share Applications with Users (https://www.zoho.com/creator/help/manage/users/add-to-application-as-user.html) — official application-access reference.
- Zoho Creator Reports and Pages (https://www.zoho.com/creator/help/new-quickstart-guide.html) — official examples used by the previous chapter.
continuity:
  record_ids:
    customer: "NOV-CUST-001"
    request: "NOV-REQ-001"
    visit: "NOV-VISIT-001"
  carried_forward_decisions:
    - "CRM remains authoritative for customer identity and service information."
    - "Creator owns requests, jobs or visits, inspections and completion workflow."
    - "Customer_Reference is a controlled reference or synchronized projection, not a second customer master."
    - "Service_Requests, Technicians and Jobs remain the core Creator forms."
    - "Inspection_Items remains a Job subform."
    - "Request_Status and Sync_Status remain separate lifecycles."
    - "Business roles are scenario roles and are not assumed to be native Zoho profiles."
    - "Hidden interface actions do not replace server-side authorization."
  chapter_5_artifacts:
    - "C02-CH05_Nova_Field_Service_Access_Design_v0.1.md"
    - "User and business-role mapping"
    - "Role and permission matrix"
    - "Technician record criteria"
    - "Future-release Customer View Prototype"
    - "Access test matrix"
    - "Joiner, mover and leaver procedure"
  access_mappings:
    - "technician.one@nova.example.com -> TECH-001"
    - "technician.two@nova.example.com -> TECH-002"
    - "maya.chen@northstar.example.com -> NOV-CUST-001 in future-release prototype"
    - "omar.khan@riverbend.example.com -> NOV-CUST-002 in future-release prototype"
  scope_changes:
    - "C02-CH05-SCOPE-001 records the customer-facing view as a future-release prototype."
    - "The Chapter 1 internal-release baseline remains unchanged."
  open_case_assumptions:
    - "Exact Creator user, role, portal, sharing, record-access and field-access controls require confirmation in the target edition and environment."
    - "The identity-to-Technician and identity-to-customer mapping mechanism remains an implementation decision."
    - "The customer prototype has not been approved as a production portal."
    - "Access denial must be verified through direct, related, report, action and integration paths."
END OF C02-CH05
