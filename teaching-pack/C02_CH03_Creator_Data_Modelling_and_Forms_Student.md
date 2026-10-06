schema_version: "1.1"
course_id: "C02"
chapter_id: "C02-CH03"
chapter_number: 3
chapter_title: "Creator Data Modelling and Forms"
filename: "C02_CH03_Creator_Data_Modelling_and_Forms_Student.md"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "partially_verified"
---
Creator Data Modelling and Forms
1. What you will learn
A Creator application becomes dependable when its data model reflects the real work. Forms are the entry point for records, but the important design decisions come first:
- what counts as an entity;
- which fields describe it;
- which records are related;
- which identifiers are stable;
- which values may be null;
- which record owns a lifecycle;
- which rules belong in field configuration, validation or later workflow logic.
In this chapter, you will learn to:
- model entities and relationships for a Creator application;
- use lookup fields to connect records;
- decide when a subform is appropriate;
- separate business identifiers from product-generated record IDs;
- design validation for required, invalid and missing values;
- define record lifecycles;
- plan safe schema changes;
- build Customer Reference, Request, Technician and Job forms.
The required practice is to build the four forms and their relationships for Nova Field Service.
Contribution to the course project
This chapter produces the data foundation for:
- request intake;
- technician assignment;
- scheduled jobs and visits;
- inspection evidence;
- later reports, pages, workflows and integrations.
The Chapter 1 specification says CRM owns customer identity and service information, while Creator owns requests, visits, inspections and completion workflow. This chapter implements that boundary as a Creator data model.
Continuity from Chapters 1 and 2
Item	Carried-forward decision
CRM customer ownership	CRM remains authoritative for customer identity and service information
Creator ownership	Creator owns requests, visits, inspections and completion workflow
Stable identifiers	NOV-CUST-001, NOV-REQ-001 and NOV-VISIT-001 remain business identifiers
Duplicate protection	External request keys prevent duplicate business actions
Failure handling	CRM lookup or synchronization failure remains visible and recoverable
Business roles	Dispatcher, Technician, Service Manager and Administrator remain scenario roles
Tooling	The Chapter 2 validation module, Git repository and mock API collection are versioned artifacts
API status	Zoho API versions, data-centre endpoints, field API names and OAuth scopes remain unverified implementation dependencies
Explicit Chapter 3 assumptions
No earlier chapter supplied a final Creator form schema or field link names. The link names and field API names in this chapter are proposed implementation names. They must be checked in the target Creator environment before integration or deployment.
This chapter uses a Customer_Reference form in Creator. It is a controlled reference or synchronized projection of CRM customer data, not a second customer master. If the final integration can query CRM directly at every lookup point, the form may later be replaced by an approved integration design. The ownership rule does not change.
A Creator form normally captures records and can have an associated report. Zoho’s official quickstart also demonstrates creating relationships with lookup fields, setting fields as mandatory and importing data into forms. Exact interface labels and feature availability can vary by account edition and environment.
Prerequisites
You should understand:
- the Nova requirements and ownership decisions from Chapter 1;
- basic JavaScript types, JSON and Git from Chapter 2;
- the difference between a business identifier and a product-generated record ID.
Deluge is not required in this chapter. The form design will identify where later validation or workflow logic may be needed without inventing host-specific Deluge syntax.
2. Lessons
Lesson 1: Model entities before building forms
An entity is a type of thing about which the business needs to store information. A record is one instance of that entity. A field is one property of a record.
For Nova Field Service:
- Customer is an entity;
- NOV-CUST-001 is one Customer record;
- Request is an entity;
- NOV-REQ-001 is one Request record;
- Job is an entity;
- NOV-VISIT-001 is one Job record representing a scheduled technician visit.
A form is a product component used to capture or manage records. It should not be used to hide a poor data model.
Entity test
Ask these questions:
1. Does the item have its own identity?
2. Does it have its own lifecycle?
3. Can it occur more than once for another record?
4. Does it need its own access or report?
5. Can it change independently?
6. Would storing it repeatedly create inconsistent copies?
If the answer to several questions is yes, the item may deserve its own entity.
For example, a request can have multiple technician jobs. Each job has its own assigned Technician, schedule and status. Therefore, Job should not be stored as one text field on Request.
Attributes and controlled values
Fields should represent one meaningful value. Avoid a single field such as:
"Priya Nair | 2026-10-07 10:00 | In Progress | Pump room"
That value cannot be reliably filtered, validated or updated. Use separate fields:
Field	Value
Technician	TECH-001
Scheduled start	2026-10-07 10:00
Job status	In Progress
Location instructions	Pump room
Use controlled values for fields with a known set of options, such as Priority, Request_Status and Job_Status. A controlled choice prevents small spelling differences from producing separate report categories.
Model the stable business identity
The business identifier for a request is NOV-REQ-001. It should be stored in a text field with a clear rule:
- required;
- not silently changed after creation;
- unique within the intended business scope;
- included in integrations and support messages.
The Creator-generated record ID is a separate technical identifier. Store it or map it when an integration requires it, but do not display it as the business request number unless the business has approved that choice.
Quick check
1. Should a scheduled Technician visit be a text field on Request or a related Job record?
2. Why should Priority use controlled values?
3. Give two reasons why a Creator-generated record ID should not automatically replace NOV-REQ-001.
Lesson 2: Use relationships and lookup fields
A relationship describes how records are connected.
The main relationship patterns for Nova are:
Relationship	Meaning
One customer to many requests	One customer can report multiple service requests
One request to many jobs	A request may require multiple visits
One Technician to many jobs	A Technician can be assigned to multiple jobs
One job to many inspection items	A job can contain several checklist observations
A lookup field connects one form to another. In Creator, the lookup normally lets a user select a record from a related form. The stored relationship should point to the related record, while the displayed value may be the selected record’s name or another display field.
Lookup design
For the Service_Requests form:
- Customer is a lookup to Customer_Reference;
- the lookup display can show Customer_Name;
- the relationship should retain the referenced customer record;
- the business key Customer_Business_ID remains available for integration mapping.
For the Jobs form:
- Request is a lookup to Service_Requests;
- Technician is a lookup to Technicians;
- the job stores the relationships rather than copying all request and Technician fields.
A lookup is not a replacement for ownership. A Technician lookup identifies the assigned worker; it does not automatically prove that the logged-in user is allowed to edit the record. Access must be designed and tested separately in later chapters.
One-to-many and many-to-many
A one-to-many relationship can be represented by placing a lookup on the many side:
Customer_Reference 1 ---- many Service_Requests
Service_Requests 1 ---- many Jobs
Technicians 1 ---- many Jobs
For a many-to-many relationship, use a junction entity. For example, if a job can require several skills and a Technician can have several skills, do not store a comma-separated list in each record. Use:
Technicians
Technician_Skills
Skills
The junction record can contain:
- Technician;
- Skill;
- proficiency;
- valid-from date;
- active status.
Display field versus key
Suppose the lookup displays Northstar Facilities Ltd. That display value is useful to a human, but it is not a reliable integration key. Names can change or be duplicated.
Use:
- Customer_Name for display;
- Customer_Business_ID for business mapping;
- the Creator record reference for the relationship;
- a CRM record ID only as a technical mapping value when verified.
Missing related records
A request with a missing customer must not silently use a text value such as Unknown customer and proceed as normal. Choose an explicit behavior:
- prevent submission;
- save the request in an exception state;
- allow a temporary intake record only if the business has approved that process.
The choice must be consistent with the Chapter 1 ownership design.
Quick check
1. Which form should contain the lookup from a Request to a Customer?
2. Why is a customer name a poor integration key?
3. If a job needs three skills, should you store "electrical, plumbing, HVAC" in one field?
Lesson 3: Use subforms for bounded child data
A subform is a group of child fields entered within a parent form. It is suitable when the child rows belong tightly to one parent and do not need an independent lifecycle.
An inspection checklist is a good candidate:
Job
  Inspection_Items
    - Pump pressure: Pass
    - Electrical enclosure: Fail
    - Safety label: Pass
The inspection rows belong to the Job. They should not be reused as independent records by another Job.
A subform is less suitable when each child item:
- must be scheduled independently;
- has its own permissions;
- needs a separate report or integration;
- can be reassigned;
- has a lifecycle independent of the parent;
- may be shared by several parents.
For example, Technician visits should not be a subform inside Request if each visit has its own schedule, status and assigned person. Use a separate Job form with a Request lookup.
Subform rules
Define the parent and row behavior:
Parent	Child row	Required rule
Job	Inspection item	Each required checklist item must have an outcome
Job	Inspection item	A blank outcome is not a pass
Job	Inspection item	A failed required item blocks completion
Job	Inspection item	Notes may be required for a failed item
A subform row can be empty or partially completed while a user is entering a form. The final save or completion transition must enforce the required rule. Do not rely only on the visible row layout.
Nulls in inspection data
These values have different meanings:
Value	Meaning
Pass	The check was performed and passed
Fail	The check was performed and failed
null or blank	No result recorded
Not Applicable	The item was deliberately excluded under an approved rule
Only Pass should satisfy a pass gate. Blank, null and Not Applicable require a separately defined rule.
Quick check
A Job has three required inspection rows. Two are Pass and one has no result. Can the Job be marked complete? Why?
Lesson 4: Design identifiers and field names
Creator provides product-generated record identifiers. Your business design also needs stable identifiers that users and external systems can understand.
Use a separate field for each identity purpose.
Identifier	Example	Purpose
Business customer ID	NOV-CUST-001	Business and integration reference
Business request ID	NOV-REQ-001	Human-readable request identity
Business visit ID	NOV-VISIT-001	Human-readable job or visit identity
External request key	EXT-REQ-1001	Replay and duplicate protection
Creator record ID	Product-generated value	Technical record mapping
CRM record ID	Product-generated value	Technical cross-system mapping
Do not generate a new business ID every time a retry occurs. The same business action must retain the same external key.
Field display names and link names
A display name is what a user sees. A link name or API name is what configuration, scripts or APIs may use. They are related but not always identical.
Proposed examples:
Display name	Proposed link name	Status
Customer Business ID	Customer_Business_ID	Proposed
Request Business ID	Request_Business_ID	Proposed
External Request Key	External_Request_Key	Proposed
Scheduled Start	Scheduled_Start	Proposed
Inspection Items	Inspection_Items	Proposed
Do not claim that these are verified Zoho API names. Before integration, inspect the actual target form metadata and record the confirmed names in the project mapping specification.
A stable field link name should not be changed casually after integrations, scripts or reports depend on it.
Naming rules
Use names that:
- identify one concept;
- avoid unexplained abbreviations;
- distinguish business IDs from product IDs;
- use one consistent casing convention;
- do not change meaning over time.
Avoid reusing Status for different lifecycles. Use Request_Status, Job_Status and Sync_Status when the states belong to different processes.
Quick check
1. Which identifier should a retry reuse?
2. Why should Request_Status and Sync_Status be separate?
3. What must you do before using a proposed field link name in an API mapping?
Lesson 5: Apply validation at the correct level
Validation protects data quality. Use the simplest layer that can enforce the rule reliably, then verify important rules at the point where the business action occurs.
Field-level validation
Use field configuration for rules such as:
- required value;
- allowed choices;
- text length;
- date format;
- numeric range;
- email format where appropriate.
The Creator quickstart demonstrates marking a lookup field as mandatory and using controlled choice fields. These are configuration-level rules.
Record-level validation
Use record-level validation when a rule depends on several fields:
- Scheduled_End must be after Scheduled_Start;
- Job_Status cannot be Completed unless a Technician is assigned;
- an emergency request requires a callback number;
- a failed inspection requires a note.
Cross-record validation
Use cross-record logic when the rule depends on other records:
- the selected customer must be an active CRM reference;
- the Technician must be active;
- the external request key must not already exist;
- a Technician cannot be assigned to overlapping jobs if that constraint is approved.
Cross-record rules may require a workflow or reusable function in later chapters. Do not pretend that a mandatory field alone can enforce them.
Validation and access
Validation answers “is this data or transition allowed?” Access answers “is this user allowed to attempt it?” Both are necessary.
For example:
- a Technician may have a valid Scheduled_End;
- but only a Dispatcher or Service Manager may change the schedule;
- the server-side access rule must still reject the Technician’s update.
Validation matrix
Rule	Data condition	Invalid result
Customer required	Customer is null	Cannot submit a normal request
Priority controlled	Value is not Low, Medium or High	Show a validation error
Job time order	End is before start	Cannot save or schedule
Technician active	Selected Technician is inactive	Cannot assign
Duplicate request	External key already exists	Reference existing request
Inspection gate	Any required result is blank or Fail	Cannot complete
CRM mapping	Customer is not found or permission denied	Exception or sync state
Quick check
Which validation category applies to each rule?
1. Priority must be one of three values.
2. Scheduled_End must be after Scheduled_Start.
3. A Technician cannot edit another Technician’s Job.
4. The external key must not already exist.
Lesson 6: Model record lifecycles
A lifecycle is the sequence of meaningful states through which a record moves.
Request lifecycle
New → Validated → Ready for Dispatch → Assigned → In Progress
    → Awaiting Inspection → Completed
Alternative terminal or exception paths:
New → Cancelled
Any operational state → Exception
Awaiting Inspection → In Progress
A status is useful when it describes a real business state. Do not add statuses merely because a report needs another color.
Job lifecycle
Scheduled → Started → Completed
Scheduled → Cancelled
Scheduled → No Show
A Job can be completed only when the completion evidence is present. A Request can remain In Progress if another Job is required.
Synchronization lifecycle
Keep synchronization separate:
Not Required → Pending → Succeeded
                     ↘ Error → Retry Pending → Succeeded
A request can be Assigned with Sync_Status = Error. Combining the two statuses creates confusing states such as Assigned but CRM Error in one field.
State transition rules
For each transition, define:
- current state;
- allowed next state;
- authorized role;
- required fields;
- side effects;
- failure behavior.
Example:
Current	Next	Actor	Required data
New	Validated	Dispatcher	Customer, description and priority
Validated	Ready for Dispatch	Dispatcher	Valid customer mapping
Ready for Dispatch	Assigned	Dispatcher or Service Manager	Active Technician
In Progress	Awaiting Inspection	Technician	Visit notes
Awaiting Inspection	Completed	Authorized role	All required inspection items are Pass
A user editing a status field directly can bypass lifecycle rules. Later workflow chapters will show how to enforce transitions. In this chapter, model the states and rules clearly first.
Quick check
Why is Sync_Status not a suitable replacement for Request_Status? Give one example of a request whose business work is complete while synchronization is still pending.
Lesson 7: Plan schema changes safely
A schema change changes forms, fields, relationships, validation or lifecycle states after data already exists.
Classify changes before applying them.
Change	Typical risk	Safer approach
Add an optional field	Low to medium	Add it, document null behavior and test reports
Add a required field to existing records	High	Backfill or create an exception path before enforcing
Rename a display label	Medium	Check user instructions and reports
Rename a link/API name	High	Map dependencies and migrate consumers
Change field type	High	Create a migration plan and test conversion
Remove a field	High	Archive or migrate values; confirm no dependency
Add a lifecycle state	Medium to high	Define transitions and update reports and tests
Change lookup target	High	Map existing relationships before changing the relationship
Change subform structure	Medium to high	Preserve row meaning and test old records
Do not treat an imported spreadsheet as the final schema. Import headers may contain spaces, inconsistent types or repeated values. Review mapping and data types before accepting the import.
Backward-compatible field addition
Suppose Nova needs Due_At to measure response performance. Adding it as optional is safer than making it required immediately because older requests do not have a value.
The transition plan is:
1. add Due_At as nullable;
2. document that old records have unknown due time;
3. populate new records where a due rule exists;
4. report missing values as Not Measured;
5. backfill only from reliable evidence;
6. make it required only after the business confirms that every new request has a due rule.
Never infer a deadline from the completion time.
Schema change record
Record:
- change ID;
- reason;
- affected forms and fields;
- old and new behavior;
- migration or backfill;
- null and invalid-data behavior;
- integration impact;
- rollback or recovery;
- tests.
3. Visual explanation
Nova Creator data model
erDiagram
    CUSTOMER_REFERENCE ||--o{ SERVICE_REQUEST : "has"
    SERVICE_REQUEST ||--o{ JOB : "requires"
    TECHNICIAN ||--o{ JOB : "assigned to"
    JOB ||--o{ INSPECTION_ITEM : "contains"

    CUSTOMER_REFERENCE {
        string Customer_Business_ID
        string Customer_Name
        string CRM_Record_ID
        string Sync_Status
    }

    SERVICE_REQUEST {
        string Request_Business_ID
        string External_Request_Key
        string Customer
        string Description
        string Priority
        string Request_Status
        string Sync_Status
    }

    TECHNICIAN {
        string Technician_Business_ID
        string Technician_Name
        string Email
        boolean Active
    }

    JOB {
        string Job_Business_ID
        string Request
        string Technician
        datetime Scheduled_Start
        datetime Scheduled_End
        string Job_Status
    }

    INSPECTION_ITEM {
        string Check_Name
        boolean Required
        string Result
        string Notes
    }
Plain-text explanation:
- Customer_Reference is a Creator reference to CRM-owned customer information.
- One customer can have many service requests.
- One request can require many Jobs or visits.
- One Technician can be assigned to many Jobs.
- A Job contains inspection rows because the rows belong to that Job and do not need an independent lifecycle.
- Sync_Status is separate from operational status.
- Business IDs are stored explicitly and do not replace Creator-generated record IDs.
Modeling choice	Why it fits Nova
Separate Job form	Visits have independent schedules, assignments and statuses
Customer lookup	Requests must refer to an authoritative customer record
Technician lookup	Jobs need an assigned operational resource
Inspection subform	Checklist rows belong tightly to one Job
External key field	Retry and duplicate protection need a stable value
Separate sync state	Integration failure must not erase business status
4. Worked case
Case inputs
The following synthetic records are available:
customer_business_id,customer_name,contact_email,crm_record_id,sync_status
NOV-CUST-001,Northstar Facilities Ltd,maya.chen@northstar.example.com,CRM-MOCK-001,Succeeded
NOV-CUST-002,Riverbend Clinics,omar.khan@riverbend.example.com,CRM-MOCK-002,Succeeded
request_business_id,external_request_key,customer_business_id,description,priority,request_status,sync_status
NOV-REQ-001,EXT-REQ-1001,NOV-CUST-001,Pump pressure low,High,Assigned,Succeeded
NOV-REQ-002,EXT-REQ-1002,NOV-CUST-002,Door access failure,Medium,New,Pending
technician_business_id,technician_name,email,active
TECH-001,Priya Nair,priya.nair@nova.example.com,true
TECH-002,Daniel Ortiz,daniel.ortiz@nova.example.com,true
TECH-003,Leah Stone,leah.stone@nova.example.com,false
job_business_id,request_business_id,technician_business_id,scheduled_start,scheduled_end,job_status
NOV-VISIT-001,NOV-REQ-001,TECH-001,2026-10-07T10:00:00Z,2026-10-07T12:00:00Z,Started
NOV-VISIT-002,NOV-REQ-002,,2026-10-08T13:00:00Z,2026-10-08T14:00:00Z,Scheduled
Inspection items for NOV-VISIT-001:
check_name,required,result,notes
Pump pressure, true, Pass, Pressure restored
Electrical enclosure, true, null,
Safety label, true, Pass, Label readable
The null inspection result is intentional missing data. It is not a pass.
Step 1: Identify entities
The data contains five modeling concepts:
1. Customer Reference;
2. Service Request;
3. Technician;
4. Job;
5. Inspection Item as a Job subform.
The CRM customer records remain authoritative. The Creator Customer Reference form stores the mapped business key, display values and synchronization state required by the application.
Step 2: Define the forms
Customer Reference form
Display field	Proposed link name	Type	Required	Rule
Customer Business ID	Customer_Business_ID	Single line	Yes	Must match the CRM business ID
Customer Name	Customer_Name	Single line	Yes	Display value from CRM
Contact Email	Contact_Email	Email	No	Synthetic example data only
CRM Record ID	CRM_Record_ID	Single line	No	Technical mapping, not business identity
Sync Status	Sync_Status	Choice	Yes	Pending, Succeeded, Error
Last Sync At	Last_Sync_At	Date-time	No	Set by synchronization process
This form is not allowed to create a competing customer master. A later synchronization process may update the display fields according to the approved contract.
Service Requests form
Display field	Proposed link name	Type	Required	Rule
Request Business ID	Request_Business_ID	Single line	Yes	Stable value such as NOV-REQ-001
External Request Key	External_Request_Key	Single line	Yes	Duplicate protection
Customer	Customer	Lookup	Yes	Lookup to Customer Reference
Description	Description	Multi-line	Yes	Cannot be blank
Priority	Priority	Choice	Yes	Low, Medium, High
Request Status	Request_Status	Choice	Yes	Controlled lifecycle values
Sync Status	Sync_Status	Choice	Yes	Separate integration lifecycle
Created At	Created_At	Date-time	Yes	Product or application timestamp
Due At	Due_At	Date-time	No	Null means no approved due rule
Technicians form
Display field	Proposed link name	Type	Required	Rule
Technician Business ID	Technician_Business_ID	Single line	Yes	Stable business resource ID
Technician Name	Technician_Name	Single line	Yes	Display name
Email	Email	Email	Yes	Synthetic example data
Active	Active	Boolean	Yes	Inactive workers cannot receive new Jobs
Skill Code	Skill_Code	Choice or lookup	No	Use a separate skill model if many-to-many grows
This form describes operational resources. It does not create native Zoho users or profiles. User access is designed in a later chapter.
Jobs form
Display field	Proposed link name	Type	Required	Rule
Job Business ID	Job_Business_ID	Single line	Yes	NOV-VISIT-001 is retained
Request	Request	Lookup	Yes	Lookup to Service Requests
Technician	Technician	Lookup	No at schedule draft	Required before Assigned or Started
Scheduled Start	Scheduled_Start	Date-time	Yes	Must precede end
Scheduled End	Scheduled_End	Date-time	Yes	Must follow start
Job Status	Job_Status	Choice	Yes	Scheduled, Started, Completed, No Show, Cancelled
Visit Notes	Visit_Notes	Multi-line	No at schedule	Required before completion
Inspection Items	Inspection_Items	Subform	Required before completion	Required rows must have a valid result
Step 3: Apply the relationships
The completed relationship design is:
Parent form	Child form	Relationship field	Result
Customer Reference	Service Requests	Service_Requests.Customer	One customer can have many requests
Service Requests	Jobs	Jobs.Request	One request can have many jobs
Technicians	Jobs	Jobs.Technician	One active Technician can have many jobs
Jobs	Inspection Items	Jobs.Inspection_Items	One Job can have many checklist rows
NOV-VISIT-001 is stored as the Job business ID. The word “Visit” remains part of the business language, while the form is named Jobs to match the required practice artifact.
Step 4: Apply validation
- NOV-REQ-001 is valid because its customer exists and its required request fields are present.
- NOV-VISIT-001 is valid for Started because an active Technician is assigned and the schedule is ordered.
- NOV-VISIT-002 is valid as a draft scheduled Job but is not ready to start because no Technician is assigned.
- TECH-003 cannot be selected for a new Job because it is inactive.
- NOV-VISIT-001 cannot be completed because Electrical enclosure has a null result.
- NOV-REQ-002 can remain New while its Sync_Status is Pending.
Mistake and correction
Mistake: The first draft stores the assigned Technician, schedule and status inside the Request form as text fields.
Why it is wrong: A Request may require multiple Jobs. Text fields cannot safely represent separate schedules, assignments or job lifecycles. A later visit would overwrite the first visit or create a difficult-to-parse string.
Correction: Create a separate Jobs form. Link each Job to its Request and Technician with lookups. Keep inspection checklist rows as a subform because they belong to one Job.
A second mistake is using Northstar Facilities Ltd as the lookup or integration key. The correction is to use the Customer Reference record and retain NOV-CUST-001 as the business mapping key.
5. Try it yourself — guided practice
Learning goal
Build the Customer Reference, Service Requests, Technicians and Jobs forms in a Creator development environment or produce their complete offline specification.
Product access and safety
Use a Creator development or sandbox environment if available. Do not use a production application or real customer data.
Zoho’s official Creator quickstart shows a workflow of creating an application from scratch, creating forms, adding lookup fields, marking fields mandatory and reviewing imported data. The following procedure follows that learning flow, but exact menu labels may differ in your edition.
Sample inputs
Use these datasets:
customer_business_id,customer_name,contact_email,crm_record_id,sync_status
NOV-CUST-001,Northstar Facilities Ltd,maya.chen@northstar.example.com,CRM-MOCK-001,Succeeded
NOV-CUST-002,Riverbend Clinics,omar.khan@riverbend.example.com,CRM-MOCK-002,Succeeded
NOV-CUST-999,Unknown customer,missing@example.com,,Error
request_business_id,external_request_key,customer_business_id,description,priority,request_status,sync_status
NOV-REQ-001,EXT-REQ-1001,NOV-CUST-001,Pump pressure low,High,Assigned,Succeeded
NOV-REQ-003,EXT-REQ-1003,NOV-CUST-002,Door access failure,Medium,New,Pending
NOV-REQ-004,EXT-REQ-1004,NOV-CUST-999,Generator alarm,High,Exception,Error
NOV-REQ-005,EXT-REQ-1001,NOV-CUST-001,Pump pressure low,High,Exception,Error
technician_business_id,technician_name,email,active
TECH-001,Priya Nair,priya.nair@nova.example.com,true
TECH-002,Daniel Ortiz,daniel.ortiz@nova.example.com,true
TECH-003,Leah Stone,leah.stone@nova.example.com,false
job_business_id,request_business_id,technician_business_id,scheduled_start,scheduled_end,job_status
NOV-VISIT-001,NOV-REQ-001,TECH-001,2026-10-07T10:00:00Z,2026-10-07T12:00:00Z,Started
NOV-VISIT-002,NOV-REQ-003,,2026-10-08T13:00:00Z,2026-10-08T14:00:00Z,Scheduled
NOV-VISIT-003,NOV-REQ-003,TECH-003,2026-10-09T09:00:00Z,2026-10-09T10:00:00Z,Scheduled
NOV-CUST-999 is an intentional missing CRM mapping. NOV-REQ-005 is an intentional duplicate external request key. TECH-003 is inactive.
Steps and expected intermediate results
1. Create a draft application named Nova Field Service from scratch.  
Expected result: a draft application exists; no production data has been changed.
2. Create the Customer_Reference form and add the fields in the worked case.  
Expected result: the form can represent a CRM business ID, display name, technical CRM mapping and sync state.
3. Import or enter the Customer Reference sample records. Review each field mapping before accepting it.  
Expected result: two records have Succeeded; NOV-CUST-999 is visibly an error condition rather than a valid customer.
4. Create the Technicians form and enter the three Technician records.  
Expected result: TECH-001 and TECH-002 are active; TECH-003 is inactive.
5. Create the Service_Requests form. Add a lookup from Customer to Customer_Reference. Make customer, external key, description and priority mandatory.  
Expected result: a request can reference a customer record rather than storing only a customer name.
6. Configure controlled values for Priority, Request_Status and Sync_Status.  
Expected result: invalid spelling such as urgent is not accepted as a priority.
 7. Create the Jobs form. Add lookups to Service_Requests and Technicians. Add schedule, status, notes and the Inspection_Items subform.  
Expected result: a Job has independent schedule and assignment fields.
 8. Add inspection subform fields Check_Name, Required, Result and Notes.  
Expected result: a Job can contain multiple checklist rows, and a blank result remains distinguishable from Pass.
 9. Enter the Job sample data.  
Expected result:
- NOV-VISIT-001 is assigned to an active Technician;
- NOV-VISIT-002 remains unassigned;
- NOV-VISIT-003 identifies an inactive Technician and is an exception.
10. Review the data model against the lifecycle.  
Expected result: a user cannot reasonably mark a Job complete without an assigned Technician, visit notes and valid required inspection results.
Learner worksheet
Form	Field	Type	Required?	Related form	Validation or lifecycle rule
 	 	 	 	 	 
 	 	 	 	 	 
 	 	 	 	 	 
 	 	 	 	 	 
 	 	 	 	 	 
Final artifact
Produce:
- four form definitions;
- a relationship diagram;
- a field and validation table;
- at least one normal record;
- one missing-data exception;
- one duplicate-key exception;
- one inactive-Technician exception;
- a lifecycle table;
- a schema-change note for adding Due_At.
Cleanup
Delete only the draft records and draft application created for this practice, or clearly mark them as training data. Do not modify shared or production forms.
Offline alternative
Create the four form schemas and relationship diagram in Markdown and validate the supplied CSV rows manually. This demonstrates data modeling but cannot demonstrate Creator lookup behavior, form validation or imported-record mapping.
6. Independent challenge
Changed constraints
Nova now supports a multi-visit repair process:
1. One Request may require multiple Jobs.
2. A Job may be assigned to only one Technician at a time.
3. A Technician can have several Jobs, but overlapping assignments must be reported as an exception.
4. A failed inspection requires a follow-up Job rather than reopening the original completed Job.
5. Customer identity remains CRM-owned.
6. A Technician may enter inspection rows but cannot change the customer or priority.
7. A Job may require more than one inspection checklist item.
8. An old request may have no Due_At; the absence must be visible and must not be interpreted as “on time.”
9. The external request key remains unique.
Challenge data
request_business_id,external_request_key,customer_business_id,description,priority,request_status,due_at
NOV-REQ-010,EXT-REQ-2010,NOV-CUST-001,Recurring pump fault,High,In Progress,2026-10-12T17:00:00Z
NOV-REQ-011,EXT-REQ-2011,NOV-CUST-002,Door access failure,Medium,In Progress,
NOV-REQ-012,EXT-REQ-2012,NOV-CUST-001,Generator alarm,High,Awaiting Inspection,2026-10-11T12:00:00Z
job_business_id,request_business_id,technician_business_id,scheduled_start,scheduled_end,job_status
NOV-VISIT-010,NOV-REQ-010,TECH-001,2026-10-10T09:00:00Z,2026-10-10T11:00:00Z,Completed
NOV-VISIT-011,NOV-REQ-010,TECH-002,2026-10-11T09:00:00Z,2026-10-11T11:00:00Z,Scheduled
NOV-VISIT-012,NOV-REQ-011,TECH-001,2026-10-10T10:30:00Z,2026-10-10T12:00:00Z,Scheduled
NOV-VISIT-013,NOV-REQ-012,TECH-001,2026-10-11T13:00:00Z,2026-10-11T14:00:00Z,Scheduled
Inspection rows:
job_business_id,check_name,required,result,notes
NOV-VISIT-010,Pump pressure,true,Pass,Pressure stable after repair
NOV-VISIT-010,Electrical enclosure,true,Pass,No exposed conductors
NOV-VISIT-013,Alarm reset,true,,
NOV-VISIT-013,Generator start,true,Pass,Started after reset
Deliverables
Produce:
- an updated Request, Technician and Job schema;
- an inspection subform design;
- a rule for overlapping Jobs;
- a rule for follow-up Jobs after failed inspection;
- access rules for Technician and Service Manager;
- a relationship diagram;
- acceptance criteria for missing Due_At, overlapping Jobs and blank inspection result;
- a migration note explaining how the existing Chapter 1 records remain valid.
Do not solve the challenge in the task section. Use the supplied data only.
Success criteria
Your model succeeds when another engineer can determine:
- why NOV-VISIT-010 and NOV-VISIT-011 are allowed for the same Request;
- why NOV-VISIT-012 is an overlap exception;
- why NOV-VISIT-013 cannot complete;
- why a failed inspection would create a new follow-up Job;
- why NOV-REQ-011 has an unknown due time rather than a successful timeliness result.
7. Common problems and recovery
Symptom	Diagnosis	Correction
Customer names are copied into every Request	Relationship was modeled as text	Use a Customer lookup and retain the business key
Two requests use the same external key	Uniqueness and duplicate behavior were not designed	Add a controlled uniqueness rule or exception workflow
A Job is stored inside Request text	Independent lifecycle was missed	Create a separate Jobs form
A blank inspection item allows completion	Blank was treated as pass	Require explicit Pass for required rows
An inactive Technician appears in the assignment list	Active status is not part of assignment validation	Filter or validate the Technician selection
A required field is added to old records	Schema change ignored existing nulls	Backfill, provide an exception or keep it optional
A link name is changed after integration work	Display name and API dependency were confused	Record dependencies and migrate deliberately
Sync error is placed in Request Status	Two lifecycles were combined	Add Sync_Status separately
A subform is used for independently scheduled visits	Child data has its own lifecycle	Use a separate Job form
Imported dates become text	Import mapping was not reviewed	Confirm field type and sample values before acceptance
A customer reference form creates new customer masters	Projection and ownership were confused	Make the form read-only or controlled by CRM synchronization
A Technician can edit priority through the form	Access and validation were not separated	Restrict editable fields and enforce the rule server-side
8. Check your understanding
1. Identify the entities in this sentence: “Northstar reported a pump problem, and two technicians visited on separate days.”
2. Which relationship is represented by a lookup on Jobs.Request?
3. Why should inspection checklist rows be a subform while technician visits are separate Job records?
4. What is the difference between NOV-REQ-001, a Creator record ID and EXT-REQ-1001?
5. The Customer Reference record exists, but its Sync_Status is Error. Should a normal Request be allowed to proceed? State an acceptable design choice and its consequence.
 6. In the worked case, which data prevents NOV-VISIT-001 from completing?
 7. Classify each rule as field-level, record-level, cross-record or access validation:
- Priority must be one of three choices.
- End time must follow start time.
- The selected Technician must be active.
- A Technician cannot edit a Job assigned to someone else.
 8. Why should Due_At be nullable when first added to an existing application?
 9. In the guided practice, what should happen to NOV-VISIT-003?
10. In the independent challenge, why are NOV-VISIT-010 and NOV-VISIT-011 valid even though they belong to the same Request?
9. Solutions and explanations
Lesson quick checks
1. A scheduled visit should be a related Job record because it has its own identity, schedule, Technician and lifecycle.
2. Controlled values make filtering, validation and reporting consistent.
3. A product-generated ID is technical and may not be meaningful to operations; a business ID is stable and usable in support and integration; the product ID may vary by environment or be difficult for users to communicate.
For lookup questions:
1. The lookup from Request to Customer belongs on the Request form.
2. A customer name can change or be duplicated, so it is not a stable integration key.
3. Three skills should not be stored as comma-separated text if the relationship must be searched, validated or reused. Use a separate skill or junction model.
For subforms, a Job with two passing rows and one blank required row cannot be completed. A blank result means the check has not produced a valid outcome.
For identifier questions:
1. A retry reuses the same external request key.
2. Request_Status describes business work; Sync_Status describes an integration operation. A Request can be Completed while its CRM summary is still Pending.
3. Confirm the actual link name in the target form metadata and record it in the integration mapping specification.
For validation categories:
1. Priority choice: field-level validation.
2. End after start: record-level validation.
3. Technician is active: cross-record validation.
4. Technician cannot edit another user’s Job: access validation.
Guided-practice sample solution
Completed form definitions:
Form	Field	Type	Required	Relationship	Rule
Customer Reference	Customer_Business_ID	Single line	Yes	None	CRM business key
Customer Reference	Customer_Name	Single line	Yes	None	CRM display value
Customer Reference	CRM_Record_ID	Single line	No	None	Technical mapping
Customer Reference	Sync_Status	Choice	Yes	None	Pending, Succeeded, Error
Service Requests	Request_Business_ID	Single line	Yes	None	Stable request ID
Service Requests	External_Request_Key	Single line	Yes	None	Duplicate protection
Service Requests	Customer	Lookup	Yes	Customer Reference	Existing valid customer
Service Requests	Description	Multi-line	Yes	None	Non-blank
Service Requests	Priority	Choice	Yes	None	Low, Medium, High
Service Requests	Request_Status	Choice	Yes	None	Controlled lifecycle
Service Requests	Sync_Status	Choice	Yes	None	Separate integration lifecycle
Technicians	Technician_Business_ID	Single line	Yes	None	Stable resource ID
Technicians	Technician_Name	Single line	Yes	None	Display name
Technicians	Email	Email	Yes	None	Synthetic address
Technicians	Active	Boolean	Yes	None	Inactive cannot receive new Jobs
Jobs	Job_Business_ID	Single line	Yes	None	Stores NOV-VISIT-*
Jobs	Request	Lookup	Yes	Service Requests	Parent Request
Jobs	Technician	Lookup	No at draft	Technicians	Required before assignment
Jobs	Scheduled_Start	Date-time	Yes	None	Before end
Jobs	Scheduled_End	Date-time	Yes	None	After start
Jobs	Job_Status	Choice	Yes	None	Scheduled, Started, Completed, No Show, Cancelled
Jobs	Visit_Notes	Multi-line	No at schedule	None	Required before completion
Jobs	Inspection_Items	Subform	No at draft	Child rows	Required before completion
Guided-practice results:
Record	Result	Reason
NOV-CUST-001	Valid reference	CRM mapping succeeded
NOV-CUST-002	Valid reference	CRM mapping succeeded
NOV-CUST-999	Exception	CRM mapping is missing or failed
NOV-REQ-001	Valid existing Request	Unique external key and valid customer
NOV-REQ-003	Valid new Request	Valid customer and unique external key
NOV-REQ-004	Exception	Customer reference is not valid
NOV-REQ-005	Duplicate exception	EXT-REQ-1001 already belongs to NOV-REQ-001
NOV-VISIT-001	Valid active Job	Active Technician and ordered schedule
NOV-VISIT-002	Draft schedule	No Technician assigned yet
NOV-VISIT-003	Assignment exception	TECH-003 is inactive
A suitable lifecycle table is:
Entity	Initial state	Normal next state	Exception
Request	New	Validated	Exception or Cancelled
Request	Validated	Ready for Dispatch	Exception
Request	Ready for Dispatch	Assigned	Exception
Job	Scheduled	Started	No Show or Cancelled
Job	Started	Completed	Exception if inspection fails
Sync	Pending	Succeeded	Error and Retry Pending
The Due_At schema note should say that it is added as nullable, older records remain Not Measured, new records receive a value only when a due rule exists and no completion timestamp alone proves timeliness.
Independent-challenge sample solution
A valid model preserves the four existing forms and adds these rules:
Rule	Design
Multiple visits for one Request	Keep Jobs.Request as a one-to-many lookup
One Technician per Job	Use a single Technician lookup on Job
Overlap detection	Compare a new Job’s interval with other active Jobs for the same Technician
Failed inspection	Keep the original Job’s evidence and create a new follow-up Job linked to the same Request
Technician restrictions	Technician may update visit notes and inspection rows but not customer, priority or assignment
Missing due time	Leave Due_At null and report the Request as Not Measured for deadline analysis
External key	Keep it on Request and reject or reference duplicate input
The overlap calculation is based on intervals. Two Jobs overlap when:
\[
\text{Start}_A < \text{End}_B
\quad\text{and}\quad
\text{End}A > \text{Start}B
\]
For NOV-VISIT-012:
- existing NOV-VISIT-010 is 09:00–11:00;
- NOV-VISIT-012 is 10:30–12:00;
- both are assigned to TECH-001;
- 10:30 < 11:00 and 12:00 > 09:00;
- therefore, the intervals overlap and the new Job is an exception.
NOV-VISIT-010 and NOV-VISIT-011 are allowed because they are assigned to different Technicians, even though they belong to the same Request.
NOV-VISIT-013 cannot complete because Alarm reset has a blank result. The Generator start pass does not compensate for the missing required row.
A failed inspection should create a new follow-up Job rather than changing a completed Job back to an earlier state. This preserves the original work evidence and gives the follow-up visit its own schedule, assignment and result.
Completed challenge relationship diagram:
erDiagram
    CUSTOMER_REFERENCE ||--o{ SERVICE_REQUEST : "identifies"
    SERVICE_REQUEST ||--o{ JOB : "has visits"
    TECHNICIAN ||--o{ JOB : "performs"
    JOB ||--o{ INSPECTION_ITEM : "records"
    JOB ||--o{ JOB : "follow-up of"

    SERVICE_REQUEST {
        string Request_Business_ID
        string External_Request_Key
        string Due_At
        string Request_Status
    }

    JOB {
        string Job_Business_ID
        string Request
        string Technician
        datetime Scheduled_Start
        datetime Scheduled_End
        string Job_Status
        string Follow_Up_Reason
    }
The self-reference JOB ||--o{ JOB represents a follow-up relationship. If the product model or reporting requirements make self-reference difficult, use an explicit Parent_Job lookup or a separate Follow-Up entity. The business rule is more important than the visual implementation choice.
10. Chapter recap and next step
You should now be able to:
- distinguish entities, records, forms and fields;
- model one-to-many and many-to-many relationships;
- use lookup fields for relationships;
- choose a subform for tightly owned child rows;
- keep independently scheduled visits in a separate Job form;
- distinguish business, external, Creator and CRM identifiers;
- design field, record, cross-record and access validation;
- model operational and synchronization lifecycles separately;
- plan schema changes without losing existing data;
- build the four Nova Field Service forms from a documented schema.
Your project artifacts from this chapter are:
- Customer_Reference form definition;
- Service_Requests form definition;
- Technicians form definition;
- Jobs form definition;
- Inspection_Items subform definition;
- C02-CH03_Nova_Field_Service_Data_Model_v0.1.md;
- C02-CH03_Nova_Field_Service_Schema_Change_Record_v0.1.md.
Chapter 4 builds reports, pages and interfaces around these records. It will use the relationships, statuses, assignments and role boundaries established here.
11. Glossary and further reading
Glossary
Business identifier  
A stable identifier used by the business, such as NOV-REQ-001.
Entity  
A type of business object about which the application stores information.
Field  
One named property of a record.
Form  
A Creator component used to capture or manage records.
Junction entity  
A separate entity used to represent a many-to-many relationship.
Lifecycle  
The meaningful states and transitions through which a record moves.
Lookup field  
A field that connects a record to a record in another form.
Null  
An explicitly empty or unknown value.
Product-generated record ID  
An identifier automatically supplied by the product for a particular record.
Schema  
The defined structure of forms, fields, relationships, types and rules.
Schema migration  
A controlled change to existing data structures and records.
Subform  
A group of child rows entered within a parent form.
System of record  
The system that owns the authoritative lifecycle and value for a record type.
Further reading
- Zoho Creator Resource Center (https://www.zoho.com/creator/help/) — official Creator documentation entry point.
- Zoho Creator Quickstart Guide (https://www.zoho.com/creator/help/new-quickstart-guide.html) — official walkthrough covering applications, forms, lookup relationships, mandatory fields, workflows and imported data.
- Zoho Creator Forms (https://www.zoho.com/creator/newhelp/forms/understand-forms.html) — official form concepts and configuration reference.
- Zoho Creator Field Types (https://www.zoho.com/creator/newhelp/forms/fields/understand-fields.html) — official field-type reference.
- Zoho Creator Lookup Relationships (https://www.zoho.com/creator/newhelp/forms/fields/lookup/relationship-between-forms.html) — official lookup relationship reference.
- Zoho Creator Environments (https://help.zoho.com/portal/en/kb/creator/developer-guide/environments) — official environment documentation for later development and deployment work.
continuity:
  record_ids:
    customer: "NOV-CUST-001"
    request: "NOV-REQ-001"
    visit: "NOV-VISIT-001"
  carried_forward_decisions:
    - "CRM remains authoritative for customer identity and service information."
    - "Creator owns requests, jobs or visits, inspections and completion workflow."
    - "Business identifiers remain distinct from Creator and CRM-generated record IDs."
    - "External request keys are used for duplicate protection."
    - "Integration failures remain visible through a separate synchronization state."
    - "The first release uses internal request intake."
  proposed_form_artifacts:
    - "Customer_Reference"
    - "Service_Requests"
    - "Technicians"
    - "Jobs"
    - "Inspection_Items subform"
    - "C02-CH03_Nova_Field_Service_Data_Model_v0.1.md"
    - "C02-CH03_Nova_Field_Service_Schema_Change_Record_v0.1.md"
  proposed_relationships:
    - "Customer_Reference one-to-many Service_Requests"
    - "Service_Requests one-to-many Jobs"
    - "Technicians one-to-many Jobs"
    - "Jobs one-to-many Inspection_Items"
  open_case_assumptions:
    - "Proposed Creator form link names and field API names require verification in the target environment."
    - "Customer_Reference is a controlled reference or synchronized projection, not a second CRM customer master."
    - "The exact Creator subform limits, validation behavior and edition dependencies have not been verified for a target account."
    - "The mapping of business roles to native Zoho access controls remains open for the access chapter."
END OF C02-CH03
