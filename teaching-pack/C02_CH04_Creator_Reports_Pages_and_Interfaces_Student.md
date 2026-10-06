schema_version: "1.1"
course_id: "C02"
chapter_id: "C02-CH04"
chapter_number: 4
chapter_title: "Creator Reports, Pages and Interfaces"
filename: "C02_CH04_Creator_Reports_Pages_and_Interfaces_Student.md"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "partially_verified"
---
Creator Reports, Pages and Interfaces
1. What you will learn
A data model stores information, but users work through screens. A Dispatcher does not think, “I need to open the Service Requests form, then the Jobs form, then the Sync Status report.” The Dispatcher thinks, “Which requests need attention, and which job should I assign next?”
This chapter teaches you to organize Creator screens around user tasks.
You will learn to:
- select an appropriate report type;
- use filters and criteria without hiding important exceptions;
- design safe record actions;
- create task-oriented Pages;
- organize dashboards around decisions;
- design navigation for different users;
- adapt screens for narrow mobile layouts;
- distinguish a useful interface from a collection of unrelated widgets.
The required practice is to build Dispatcher and Technician interfaces for Nova Field Service.
Contribution to the course project
This chapter turns the Chapter 3 forms into usable workspaces:
- a Dispatcher queue for intake, assignment and synchronization exceptions;
- a Technician screen for today’s assigned Jobs and inspection work;
- a Service Manager view for exceptions and workload;
- navigation that follows operational tasks;
- reports and actions that use the Chapter 3 relationships and lifecycle states.
Access security is introduced here as an interface design concern, but detailed users, roles, record access and portal behavior are covered in Chapter 5. Hiding a report or button is not a substitute for server-side permission enforcement.
Continuity from previous chapters
Item	Carried-forward decision
Customer form	Customer_Reference is a CRM-controlled reference, not a second customer master
Request form	Service_Requests contains Request_Business_ID, External_Request_Key, Customer, Priority, Request_Status and Sync_Status
Job form	Jobs contains Job_Business_ID, Request, Technician, schedule and Job_Status
Inspection data	Inspection_Items is a Job subform
Business IDs	NOV-CUST-001, NOV-REQ-001 and NOV-VISIT-001 remain stable business identifiers
Business roles	Dispatcher, Technician, Service Manager and Administrator remain scenario roles, not assumed native profiles
Failure behavior	Sync errors remain visible and retryable
Tooling	Chapter 2 validation and mock API artifacts are version-controlled
Product dependencies	Exact Creator report, Page and mobile options depend on the target environment and edition
2. Lessons
Lesson 1: Choose a report for the user’s question
A report is a view of stored records. It should answer a defined question for a defined user.
Start with the user’s question:
User question	Suitable report shape
Which requests need assignment?	Filtered list or table
Which Jobs are scheduled today?	Calendar or filtered list
Which Jobs are in each lifecycle state?	Kanban
How many requests exist by priority?	Summary or chart
Which customer requests are related?	List with lookup columns
Which records changed during a period?	Table filtered by date
Which exceptions require intervention?	Exception queue
Common Creator report choices include list or table, spreadsheet, calendar, summary, chart, pivot and Kanban views. The exact choices and configuration labels must be confirmed in the target environment.
A report should expose the fields needed for the task and omit distracting fields. A Dispatcher may need:
- Request Business ID;
- customer;
- priority;
- Request Status;
- Sync Status;
- preferred window;
- assigned Technician;
- last update time.
The Dispatcher probably does not need to see every technical CRM mapping field in the primary queue.
Report purpose statement
Write a purpose statement before creating a report:
The Dispatcher Queue shows Requests that are new, validated or ready for dispatch, with customer, priority, synchronization state and assignment information. It supports assignment and exception review.
This prevents a report from becoming a general-purpose dump of every column.
Filters and criteria
A filter limits which records appear. A criterion describes the rule used by the filter.
For the Dispatcher Queue:
Request_Status is one of:
New
Validated
Ready for Dispatch
A separate synchronization exception filter is:
Sync_Status is Error
Do not combine unrelated filters without checking their meaning. If you filter for:
Request_Status = "Ready for Dispatch"
AND Sync_Status = "Error"
you will see only records that satisfy both conditions. That may be useful for a focused exception queue, but it will not show all sync errors.
Use separate reports when users need different questions answered.
Empty results are meaningful
An empty report can mean:
- there are no matching records;
- the filter is too narrow;
- the user cannot access the records;
- the report has a date or timezone issue;
- the data has not been synchronized;
- the report points to the wrong form or field.
A user should not be told “there is no work” until the report’s criteria and access behavior are verified.
Quick check
1. Which report best answers “Which Jobs are in Scheduled, Started or Completed?”
2. Why is one report with every possible column usually a poor interface?
3. What are two possible meanings of an empty Technician report?
Lesson 2: Use actions carefully
An action changes data, opens a related screen or starts an approved operation.
Examples for Nova include:
- Assign Job;
- Start Job;
- Record Inspection;
- Mark No Show;
- Open Customer;
- Retry Synchronization;
- Cancel Request.
Actions should be named using a verb and an object. Update is less informative than Assign Job.
Action design
For each action, define:
Action design question	Example
Who can use it?	Dispatcher or Service Manager
Which records are eligible?	Jobs in Scheduled with no Technician
What fields change?	Technician and Job Status
What preconditions apply?	Technician is active
What happens on failure?	Keep the Job unchanged and show the reason
What audit evidence is needed?	Actor, time, old value and new value
A button that is hidden from a Technician improves usability, but it does not enforce security. The record update must still be rejected if the Technician calls the action through another route.
Idempotent and dangerous actions
Some actions are safe to repeat if they produce the same result. Others create a new side effect each time.
Examples:
- Opening a related Customer is read-only.
- Setting Job_Status to Started is usually repeat-safe if the transition is controlled.
- Sending a new emergency notification is not automatically repeat-safe.
- Retrying CRM synchronization must reuse the external request key.
An action should show a confirmation when the result is destructive or difficult to reverse. Confirmation is not a substitute for validation.
Actions and lifecycle
An action should move a record through a valid lifecycle transition rather than letting users edit a status arbitrarily.
For example:
Scheduled → Started
is valid when the Job has an assigned active Technician.
Scheduled → Completed
should be rejected because the Job has not started and the required completion evidence may be absent.
Quick check
1. What should an Assign Job action verify before changing a Job?
2. Why is hiding an action not enough to enforce access?
3. Give one Nova action that must be protected against duplicate execution.
Lesson 3: Build Pages around user tasks
A Page is a composed interface that can bring together reports, forms, panels, charts, text and navigation elements.
A Page should answer a user’s work question quickly. It should not simply place every component on one screen.
Dispatcher task model
A Dispatcher needs to:
1. see new and unassigned Requests;
2. identify high-priority work;
3. see missing customer or CRM synchronization exceptions;
4. assign an active Technician;
5. open the related Job or Customer;
6. confirm that the assignment was saved.
A Dispatcher Page can contain:
- a count of unassigned Jobs;
- a filtered Request Queue;
- a high-priority report;
- a Sync Exceptions report;
- an Assign Job action;
- a link to create a Request.
Technician task model
A Technician needs to:
1. see assigned Jobs for the current work period;
2. open one Job;
3. start the Job;
4. record notes;
5. complete required inspection items;
6. submit completion only when the evidence is valid.
A Technician Page should avoid:
- unrelated customer administration;
- configuration controls;
- all-company workload tables;
- technical synchronization fields that the Technician cannot resolve.
Manager task model
A Service Manager needs to:
- see workload by Job Status;
- review failed inspections;
- find overdue or unresolved exceptions when due data exists;
- reassign or escalate Jobs;
- inspect sync failures.
The Manager Page may use summary panels and charts, but each summary must link to the underlying record list. A number without a drill-down path is difficult to investigate.
Page component hierarchy
A useful Page has a visual hierarchy:
1. urgent exceptions;
2. primary work queue;
3. common actions;
4. secondary summaries;
5. help or explanatory text.
Do not put decorative charts above records that require immediate intervention.
Quick check
1. Why should the Dispatcher and Technician Pages not contain the same primary report?
2. What should a Manager chart provide besides a number?
3. Name one component that should not be prominent on a Technician Page.
Lesson 4: Use dashboards for decisions, not decoration
A dashboard combines reports, charts, totals and filters to help a user understand a situation and decide what to do.
A dashboard is useful when:
- the audience has a defined decision;
- the measures have a known denominator;
- the records behind a measure are accessible;
- the dashboard distinguishes open, completed and exception records;
- the refresh or synchronization timing is understood.
A dashboard is misleading when it shows:
- a completion percentage without defining completed and unfinished records;
- an average that excludes null values without saying so;
- a count of visible records as if it were a count of all records;
- a chart with categories that combine different lifecycles;
- a target presented as an observed result.
Example: Manager workload dashboard
Component	Definition	Action
Open Requests	Requests not in Completed or Cancelled	Open Request Queue
Unassigned Jobs	Jobs with no Technician and status not Cancelled	Open Assignment Queue
Failed inspections	Jobs with at least one required Fail result	Open Inspection Exceptions
Sync errors	Records with Sync_Status = Error	Open Sync Exceptions
Jobs by status	Count of Jobs grouped by Job_Status	Open Job Kanban
A dashboard measure must define its inclusion rule. For example:
\[
\text{Open Requests} =
\text{Requests where Status is not Completed and not Cancelled}
\]
If a request is still open, it belongs in the open count even if it has no due date.
Do not describe a request as overdue unless Due_At exists and the comparison rule has been defined.
Quick check
A dashboard shows “92% completed.” What questions must you ask before trusting the number?
Lesson 5: Design navigation around work
Navigation should help users move between related tasks.
Poor navigation mirrors the database:
Customer Reference
Service Requests
Technicians
Jobs
Inspection Items
Sync Log
Settings
This may be useful to an Administrator, but it forces a Dispatcher to understand the schema.
Task-oriented navigation is clearer:
Dispatcher Home
  New Request
  Requests to Assign
  Jobs
  Sync Exceptions

Technician Home
  My Jobs
  Start Job
  Inspection
  Completed Jobs

Manager Home
  Exceptions
  Workload
  Failed Inspections
  Sync Health
The underlying reports can still be based on the four forms from Chapter 3.
Navigation principles
- Put the most frequent task first.
- Use business language rather than internal form names where appropriate.
- Keep related tasks together.
- Make exception paths visible.
- Do not create navigation items the user cannot use.
- Do not treat hidden navigation as access control.
- Provide a way back to the user’s main work queue.
- Preserve the record context when opening a related view.
A user should understand what a navigation item does without reading implementation documentation.
Quick check
Why is Requests to Assign often better navigation text than Service_Requests_Report for a Dispatcher?
Lesson 6: Design mobile layouts for field work
A Technician often works on a narrow screen, possibly in a location where scrolling and typing are difficult. A mobile layout is not simply a desktop Page made narrower.
Mobile design should prioritize:
- one primary task per screen;
- short labels;
- important fields first;
- readable status and schedule;
- touch-friendly actions;
- limited horizontal scrolling;
- concise validation messages;
- saving or recovery behavior when connectivity is uncertain.
A Technician Job screen may display:
1. Job Business ID;
2. customer name and location;
3. scheduled window;
4. service description;
5. Start Job;
6. visit notes;
7. inspection checklist;
8. Complete Job.
A wide report with ten columns is unsuitable as the primary mobile screen. Use a compact list to select a Job, then a detail screen for the selected record.
Mobile state and incomplete work
A field worker may open a Job and have incomplete inspection data. The interface must distinguish:
- draft notes;
- submitted inspection results;
- saved Job;
- completed Job.
Do not show a green “complete” indicator because the form was opened or because one inspection item passed.
If offline behavior is not implemented and verified, do not imply that the application can continue operating without connectivity. Show the actual supported failure behavior, such as an error with retry instructions.
Quick check
1. Why should the Technician first see a compact Job list and then a detail screen?
2. What must the mobile interface show when an inspection item is blank?
3. Does a responsive layout automatically prove that offline work is supported?
3. Visual explanation
Task-oriented interface structure
flowchart TD
    H[Role task home] --> Q[Primary queue]
    H --> X[Exceptions]
    H --> A[Common action]
    Q --> D[Record detail]
    D -->|valid transition| N[Next lifecycle state]
    D -->|missing or invalid data| E[Visible validation]
    D -->|integration problem| S[Sync exception]
    X --> D
    A --> D
    S --> R[Retry or support action]
Plain-text explanation:
- A user starts from a role-specific home screen.
- The primary queue contains records that need attention.
- An exception report is separate so unusual cases are not lost in normal work.
- A common action opens or updates a record.
- The record detail screen shows the data required for the next valid transition.
- Missing data produces validation feedback.
- Integration failures produce a visible synchronization exception.
- A retry or support action is available only to an authorized role.
Screen design layer	Nova example
Role home	Dispatcher Home or Technician Home
Primary queue	Requests to Assign or My Jobs
Detail	Request Detail or Job Detail
Action	Assign Job, Start Job or Record Inspection
Exception	CRM Sync Errors or Failed Inspections
Recovery	Retry Sync or Escalate to Manager
The interface is successful when the user can identify the next action without understanding the internal database structure.
4. Worked case
Case inputs
The following synthetic records are available for a Dispatcher and Technician interface.
request_business_id,customer_business_id,priority,request_status,sync_status,assigned_technician,due_at
NOV-REQ-001,NOV-CUST-001,High,In Progress,Succeeded,TECH-001,2026-10-08T17:00:00Z
NOV-REQ-002,NOV-CUST-002,Medium,New,Pending,, 
NOV-REQ-003,NOV-CUST-001,High,Ready for Dispatch,Succeeded,,
NOV-REQ-004,NOV-CUST-002,Low,Cancelled,Succeeded,,
NOV-REQ-005,NOV-CUST-001,High,Assigned,Error,TECH-002,
job_business_id,request_business_id,technician_business_id,scheduled_start,scheduled_end,job_status
NOV-VISIT-001,NOV-REQ-001,TECH-001,2026-10-07T10:00:00Z,2026-10-07T12:00:00Z,Started
NOV-VISIT-002,NOV-REQ-002,,2026-10-08T13:00:00Z,2026-10-08T14:00:00Z,Scheduled
NOV-VISIT-003,NOV-REQ-003,,2026-10-08T15:00:00Z,2026-10-08T17:00:00Z,Scheduled
NOV-VISIT-004,NOV-REQ-005,TECH-002,2026-10-07T08:00:00Z,2026-10-07T09:00:00Z,No Show
Inspection results:
job_business_id,check_name,required,result,notes
NOV-VISIT-001,Pump pressure,true,Pass,Pressure restored
NOV-VISIT-001,Electrical enclosure,true,, 
NOV-VISIT-004,Site access,true,Fail,Customer contact unavailable
No current observation is supplied for NOV-REQ-002 or NOV-REQ-003 beyond the timestamps and statuses. Do not infer that either request met a deadline.
Step 1: Define report purposes
Completed report registry:
Report name	Source	Purpose	Criteria
Requests to Assign	Service_Requests	Show requests needing dispatch attention	Status is New, Validated or Ready for Dispatch
Sync Exceptions	Service_Requests	Show failed CRM synchronization	Sync_Status = Error
Unassigned Jobs	Jobs	Show Jobs without a Technician	Technician is empty and Job Status is not Cancelled
Job Status Board	Jobs	Show operational work by state	All permitted Jobs
My Jobs	Jobs	Show a Technician’s assigned Jobs	Technician matches the current user mapping
Inspection Exceptions	Jobs with subform	Show Jobs with blank or failed required checks	Any required result is blank or Fail
The phrase “matches the current user mapping” is a design requirement. The exact Creator user-to-Technician mapping and criteria mechanism must be confirmed when access is implemented.
Step 2: Define actions
Action	Eligible record	Actor	Preconditions
Assign Job	Unassigned Job in a dispatchable state	Dispatcher or Service Manager	Active Technician selected
Start Job	Assigned Job in Scheduled state	Assigned Technician	Current user is assigned; start data available
Record Inspection	Started or inspection-ready Job	Assigned Technician	Job is assigned
Complete Job	Job with all required checks Pass	Authorized role	Notes and inspection evidence complete
Retry Sync	Request with Sync_Status = Error or Pending	Administrator or Service Manager	Same external key and approved connection
Mark No Show	Scheduled Job with no visit completed	Dispatcher or Service Manager	Reason is entered
Step 3: Build Page layouts
Dispatcher Home
Region	Component	Purpose
Top	Count of Requests to Assign	Shows immediate workload
Top	Count of Sync Exceptions	Makes integration failures visible
Main	Requests to Assign report	Supports triage and assignment
Main	Unassigned Jobs report	Shows scheduled work with no Technician
Side	High-priority Requests report	Brings urgent work forward
Side	New Request action	Starts request intake
Side	Retry Sync action	Opens an authorized recovery path
Technician Home
Region	Component	Purpose
Top	My Jobs for current work period	Shows assigned work
Main	Compact My Jobs list	Allows Job selection
Detail	Job information	Provides customer, schedule and instructions
Detail	Start Job action	Moves the Job into work
Detail	Inspection subform	Captures required evidence
Bottom	Complete Job action	Available only after validation
Service Manager Home
Region	Component	Purpose
Top	Open Requests count	Shows unresolved work
Top	Failed Inspections count	Shows quality exceptions
Main	Job Status Board	Shows workload by state
Main	Inspection Exceptions report	Supports intervention
Side	Sync Exceptions report	Supports recovery
Side	Workload chart	Shows distribution, not completion proof
Step 4: Interpret the case through the reports
- NOV-REQ-002 appears in Requests to Assign because it is New.
- NOV-REQ-003 appears in Requests to Assign because it is Ready for Dispatch.
- NOV-REQ-005 appears in Sync Exceptions because its sync state is Error, even though it is assigned.
- NOV-VISIT-002 and NOV-VISIT-003 appear in Unassigned Jobs.
- NOV-VISIT-001 appears in My Jobs for TECH-001.
- NOV-VISIT-001 appears in Inspection Exceptions because Electrical enclosure is blank.
- NOV-VISIT-004 appears in Inspection Exceptions because the required check failed.
- NOV-REQ-004 does not appear in open queues because it is Cancelled.
Mistake and correction
Mistake: The first Page shows a chart labelled “Requests completed on time” using every request with a completion timestamp.
Why it is wrong: The dataset has no due timestamp for some records. A completion timestamp does not prove that a target was met.
Correction: Show a neutral count such as “Completed Requests,” or define a measured subset:
On-time records:
Due_At is not empty
AND Completed_At is not empty
AND Completed_At <= Due_At
Label records without Due_At as Not Measured. Do not place them in the denominator for an on-time percentage.
A second mistake is putting every form report on the Technician Home page. The correction is to show a compact assigned-Job queue and open the Job detail only when the Technician selects a record.
5. Try it yourself — guided practice
Learning goal
Create a Dispatcher Home, Technician Home and Service Manager exception view using the Chapter 3 forms and sample data.
Product access and safety
Use a Creator development or sandbox environment. Do not use production data.
The official Creator quickstart demonstrates creating reports from an application, creating a Kanban report, creating a blank Page, embedding reports and forms on a Page and adding panels and charts. Use those documented product patterns, while treating exact labels as environment-dependent.
Sample inputs
Use the worked-case records from this chapter. Add this user-to-Technician mapping for the exercise:
application_user,scenario_role,technician_business_id
dispatcher.one@nova.example.com,Dispatcher,
technician.one@nova.example.com,Technician,TECH-001
manager.one@nova.example.com,Service Manager,
admin.one@nova.example.com,Administrator,
The mapping is synthetic. It is an exercise input, not a claim about native Creator profiles.
Steps and expected intermediate results
 1. Create a list report named Requests to Assign.  
Criteria: Request_Status is New, Validated or Ready for Dispatch.  
Expected result: NOV-REQ-002 and NOV-REQ-003 appear; NOV-REQ-004 does not.
 2. Create a list report named Sync Exceptions.  
Criteria: Sync_Status = Error.  
Expected result: NOV-REQ-005 appears.
 3. Create a list report named Unassigned Jobs.  
Criteria: Technician is empty and Job Status is not Cancelled.  
Expected result: NOV-VISIT-002 and NOV-VISIT-003 appear.
 4. Create a Kanban report named Job Status Board, grouped by Job_Status.  
Expected result: Jobs appear in Started, Scheduled and No Show columns.
 5. Create a Technician report named My Jobs.  
Use the approved user-to-Technician mapping concept.  
Expected result for TECH-001: NOV-VISIT-001 appears, while the other Jobs do not appear in the primary work list.
 6. Create a report named Inspection Exceptions.  
Include Jobs where any required inspection result is blank or Fail.  
Expected result: NOV-VISIT-001 and NOV-VISIT-004 appear.
 7. Create a blank Page named Dispatcher Home. Add:
- a count panel for Requests to Assign;
- a count panel for Sync Exceptions;
- the Requests to Assign report;
- the Unassigned Jobs report;
- a link or action for New Request.
Expected result: a Dispatcher can see the queue and exceptions from one screen.
 8. Create a blank Page named Technician Home. Add:
- the compact My Jobs report;
- a Job detail entry point;
- inspection access;
- a completion action or explanation.
Expected result: the Technician’s primary path is assigned Job to inspection to completion.
 9. Create a Service Manager view with:
- Job Status Board;
- Inspection Exceptions;
- Sync Exceptions;
- a chart or count summary.
Expected result: the Manager can identify a specific record behind every exception count.
10. Review the pages at a narrow width.  
Expected result: the primary task remains visible without requiring a wide table or horizontal scrolling for essential data.
Final artifact
Create:
- C02-CH04_Nova_Field_Service_Reports_and_Pages_v0.1.md;
- a report registry;
- a Page component registry;
- a navigation map;
- an action precondition table;
- a mobile layout note;
- screenshots or descriptions of expected outputs if screenshots are not available.
Cleanup
Delete only draft reports, pages and sample records created for this practice, or label them as training components. Do not change shared production reports.
Offline alternative
Create a Markdown interface specification and Mermaid navigation diagram. Build wireframes with text boxes if no Creator environment is available. This demonstrates task and layout reasoning but cannot demonstrate actual report filtering, Page rendering or mobile behavior.
6. Independent challenge
Changed constraints
Nova now has an after-hours support queue:
1. Emergency Requests must be visible separately from normal Requests.
2. The Dispatcher must see an Emergency Queue and an Unassigned Emergency Jobs report.
3. A Service Manager needs a dashboard showing emergency workload and failed inspection count.
4. A Technician must see only assigned Jobs, including emergency priority.
5. A Job with Job_Status = No Show must be visible to the Manager but not in the Technician’s active queue.
6. A Request with Sync_Status = Error must remain visible in the emergency exception view.
7. A proposed 30-minute first-response target must not be shown as achieved without Created_At and First_Response_At.
8. The first release remains internal. Do not create a customer-facing portal.
Challenge data
request_business_id,customer_business_id,priority,request_status,sync_status,assigned_technician,created_at,first_response_at,due_at
NOV-REQ-010,NOV-CUST-001,Emergency,Assigned,Succeeded,TECH-001,2026-10-10T08:00:00Z,2026-10-10T08:18:00Z,2026-10-10T08:30:00Z
NOV-REQ-011,NOV-CUST-002,Emergency,Ready for Dispatch,Pending,,2026-10-10T08:05:00Z,,
NOV-REQ-012,NOV-CUST-001,High,In Progress,Error,TECH-002,2026-10-10T07:45:00Z,2026-10-10T08:20:00Z,
NOV-REQ-013,NOV-CUST-002,Emergency,Completed,Succeeded,TECH-001,2026-10-09T18:00:00Z,2026-10-09T18:45:00Z,2026-10-09T18:30:00Z
job_business_id,request_business_id,technician_business_id,scheduled_start,scheduled_end,job_status
NOV-VISIT-010,NOV-REQ-010,TECH-001,2026-10-10T09:00:00Z,2026-10-10T10:00:00Z,Started
NOV-VISIT-011,NOV-REQ-011,,2026-10-10T09:30:00Z,2026-10-10T10:30:00Z,Scheduled
NOV-VISIT-012,NOV-REQ-012,TECH-002,2026-10-10T08:30:00Z,2026-10-10T09:30:00Z,No Show
NOV-VISIT-013,NOV-REQ-013,TECH-001,2026-10-09T19:00:00Z,2026-10-09T20:00:00Z,Completed
Inspection data:
job_business_id,check_name,required,result,notes
NOV-VISIT-010,Emergency isolation,true,Pass,Area isolated
NOV-VISIT-010,Pressure check,true,Pass,Pressure stable
NOV-VISIT-012,Site access,true,Fail,Technician could not enter
NOV-VISIT-013,Door mechanism,true,Pass,Repaired
Deliverables
Produce:
- an Emergency Queue report;
- an Unassigned Emergency Jobs report;
- a Technician Active Jobs report;
- a Manager Emergency Dashboard specification;
- a No Show Manager Exceptions report;
- an emergency navigation map;
- a mobile layout for the Technician;
- definitions for the 30-minute first-response measure;
- acceptance criteria for missing timestamps, sync errors and no-show Jobs.
Success criteria
Your design succeeds when:
- NOV-REQ-010 appears in emergency operational work;
- NOV-REQ-011 appears in the emergency assignment queue and remains visible while sync is pending;
- NOV-REQ-012 appears in the emergency or integration exception view even though it is not an active Technician Job;
- NOV-REQ-013 is not incorrectly counted as meeting the 30-minute target;
- NOV-VISIT-011 is visible to the Dispatcher because it is unassigned;
- NOV-VISIT-012 is visible to the Manager but not the Technician’s active queue;
- every dashboard measure has a definition and drill-down path.
7. Common problems and recovery
Symptom	Diagnosis	Correction
A report shows every record	No task-specific filter was defined	Write the user question and add explicit criteria
A high-priority record disappears	Filters use the wrong status or an unintended AND condition	Inspect each criterion and test with known records
A count differs from the underlying list	Dashboard and report use different criteria or access	Compare source, filters, date range and permissions
A chart says “on time” without due timestamps	Target and observation were confused	Rename it or require due and response timestamps
A Technician sees every Job	The report is filtered by a display name or no user mapping	Use an approved user-to-Technician mapping and enforce access separately
A Kanban drag changes status without required evidence	UI action bypasses lifecycle validation	Enforce transition rules at the server or workflow layer
A Page contains too many components	The Page was designed around entities rather than tasks	Remove secondary fields and split by role
Mobile users must scroll across many columns	Desktop table was reused unchanged	Use a compact list and detail screen
Retry action is available on successful sync	Eligibility criteria are too broad	Filter for Pending or Error only
No Show Jobs vanish from all work views	Exception state was excluded everywhere	Create a Manager exception report
A hidden button is treated as security	Interface visibility was confused with authorization	Enforce access on the record operation
Page shows stale data as live	Synchronization timing is unknown	Display last refresh or sync state where relevant
A report uses an internal field name as its title	Database structure was exposed to users	Use task language in navigation and titles
8. Check your understanding
 1. Which report type is most suitable for comparing Jobs by Job_Status?
 2. A Dispatcher Queue is filtered with:
Request_Status = "Ready for Dispatch"
AND Sync_Status = "Error"
What records will it show, and what important records may it hide?
 3. Why should a dashboard number link to an underlying report?
 4. What should an Assign Job action verify before saving?
 5. Why should Sync Exceptions be a separate report from normal assignment work?
 6. A Technician’s active queue contains a No Show Job. Which design rule has probably been missed?
 7. A dashboard reports 3 completed Jobs out of 4 total Jobs. One Job has no Due_At. Can you calculate an on-time percentage? Explain.
 8. Give two changes needed when adapting a wide desktop report for a mobile Technician screen.
 9. Is hiding Retry Sync from a Technician sufficient to prevent unauthorized synchronization?
10. Which records from the worked case should appear in Inspection Exceptions?
9. Solutions and explanations
Lesson quick checks
1. A Kanban report grouped by Job_Status best answers which Jobs are in each lifecycle state.
2. A report containing every column is hard to use because it mixes task fields, technical fields and unrelated data. Users must interpret the schema instead of acting on a work queue.
3. An empty report may mean there are no matching records, the filter is wrong, the user lacks access, the date range is wrong or synchronization has not completed.
For action checks:
1. Assign Job should verify that the Job is eligible, the selected Technician is active, the schedule is valid and the actor is authorized.
2. Hiding an action changes the interface only. A user may still call another action or endpoint, so the update operation must enforce authorization.
3. Retry Sync must be protected against duplicate execution and should reuse the original external request key.
For dashboard checks, ask:
- What records are included?
- Are cancelled and unfinished records excluded?
- Is there a due timestamp?
- What is the denominator?
- Are visible records limited by access?
- When was the data last synchronized?
- Can the user open the underlying records?
Worked-case report results
Report	Expected records
Requests to Assign	NOV-REQ-002, NOV-REQ-003
Sync Exceptions	NOV-REQ-005
Unassigned Jobs	NOV-VISIT-002, NOV-VISIT-003
My Jobs for TECH-001	NOV-VISIT-001
Inspection Exceptions	NOV-VISIT-001, NOV-VISIT-004
Cancelled records in active queues	None from NOV-REQ-004
For the two-condition Dispatcher filter, only records that are both Ready for Dispatch and Sync_Status = Error appear. It hides new or assigned records with sync errors and all ready records whose sync succeeded. That filter may be useful for a narrow report, but it should not replace separate assignment and sync exception reports.
The Assign Job action must check:
- the Job is not cancelled or completed;
- the selected Technician is active;
- required Request and schedule fields exist;
- the actor has the Dispatcher or Service Manager permission;
- the update is recorded with an audit result.
Sync Exceptions is separate because a record can be operationally assigned while its CRM synchronization has failed. Combining both concerns makes either assignment or recovery invisible.
A No Show Job should be excluded from the Technician’s active queue and included in a Manager exception view.
The worked case cannot calculate an on-time percentage for all records because some records have no Due_At. A valid measured subset would be:
\[
\text{On-time percentage} =
\frac{\text{records with Due\_At and Completed\_At where Completed\_At} \leq \text{Due\_At}}
{\text{records with Due\_At and Completed\_At}}
\times 100
\]
Any record without a due timestamp is Not Measured, not automatically on time or late.
Guided-practice sample solution
Completed report registry:
Report	Source	Criteria	Primary user
Requests to Assign	Service Requests	Status is New, Validated or Ready for Dispatch	Dispatcher
Sync Exceptions	Service Requests	Sync Status is Error	Dispatcher, Service Manager
Unassigned Jobs	Jobs	Technician is empty and status is not Cancelled	Dispatcher
Job Status Board	Jobs	All permitted Jobs	Service Manager
My Jobs	Jobs	Technician matches approved current-user mapping	Technician
Inspection Exceptions	Jobs and inspection rows	Required result is blank or Fail	Service Manager, Technician for own Jobs
Completed Dispatcher Page:
Dispatcher Home
├── Requests to Assign count
├── Sync Exceptions count
├── Requests to Assign report
├── Unassigned Jobs report
├── High-priority Requests report
└── New Request and Assign Job actions
Completed Technician Page:
Technician Home
├── My active Jobs
├── Job detail
│   ├── Customer and service details
│   ├── Schedule and instructions
│   ├── Start Job
│   ├── Visit Notes
│   ├── Inspection Items
│   └── Complete Job
└── Completed Jobs
Completed Manager Page:
Service Manager Home
├── Open Requests count
├── Unassigned Jobs count
├── Failed Inspections count
├── Job Status Board
├── Inspection Exceptions
├── Sync Exceptions
└── Workload chart with drill-down
Mobile design correction:
- use a compact Job list with Job ID, priority, schedule and status;
- open a single Job detail screen;
- keep Start Job, inspection and completion actions near the relevant data;
- do not require horizontal scrolling for customer, schedule or status;
- display a clear error if the action cannot save;
- do not claim offline support unless it has been implemented and tested.
Independent-challenge sample solution
Emergency report definitions:
Report	Criteria
Emergency Queue	Priority is Emergency and Request Status is not Completed or Cancelled
Unassigned Emergency Jobs	Priority through Request is Emergency, Technician is empty, Job Status is not Cancelled
Emergency Sync Exceptions	Priority is Emergency and Sync Status is Error or Pending
Technician Active Jobs	Technician matches current user and Job Status is Scheduled or Started
No Show Manager Exceptions	Job Status is No Show
Emergency Inspection Exceptions	Emergency Job has blank or failed required inspection row
Expected records:
Record	Expected view
NOV-REQ-010	Emergency Queue; assigned operational work
NOV-REQ-011	Emergency Queue; Unassigned Emergency Jobs; Sync or pending exception view
NOV-REQ-012	Emergency Sync Exceptions; not an active Technician Job because its Job is No Show
NOV-REQ-013	Not an active emergency record; historical completed record
NOV-VISIT-010	Active Jobs for TECH-001
NOV-VISIT-011	Unassigned Emergency Jobs
NOV-VISIT-012	No Show Manager Exceptions; excluded from active Technician queue
The 30-minute first-response target can be calculated only when both timestamps exist:
\[
\text{First-response duration} =
\text{First\_Response\_At} - \text{Created\_At}
\]
For NOV-REQ-010:
- Created at 08:00;
- first response at 08:18;
- duration is 18 minutes;
- the proposed 30-minute target is met for this synthetic example.
For NOV-REQ-011, First_Response_At is missing. It is not possible to state whether the target was met.
For NOV-REQ-012, the timestamps show a response at 08:20 after creation at 07:45, which is 35 minutes. If the 30-minute rule is approved and timestamps are comparable, the target is not met. The request still has a synchronization error and requires operational recovery.
For NOV-REQ-013, creation at 18:00 and first response at 18:45 is 45 minutes, which exceeds the proposed 30-minute target. Its Due_At also indicates 18:30, but the first-response rule must still be stated separately from the due-time rule.
The Manager dashboard should show:
- Emergency Open count;
- Emergency Unassigned count;
- Emergency Sync Error count;
- No Show count;
- Failed Inspection count;
- measured First Response target result only for records with both timestamps;
- a link from every number to a filtered report.
10. Chapter recap and next step
You should now be able to:
- choose a report type based on a user question;
- define report purpose and criteria;
- separate normal queues from exception queues;
- design actions with preconditions and recovery behavior;
- organize Creator Pages around user tasks;
- design Dispatcher, Technician and Service Manager workspaces;
- use dashboards with reproducible definitions;
- create navigation that hides schema complexity without hiding security;
- adapt layouts for narrow screens;
- distinguish measured results from targets and missing data.
Your project artifacts from this chapter are:
- C02-CH04_Nova_Field_Service_Reports_and_Pages_v0.1.md;
- Dispatcher Home specification;
- Technician Home specification;
- Service Manager exception view;
- report registry;
- navigation map;
- mobile layout note.
Chapter 5 applies access design to these reports, Pages and actions. It will define users, roles, record access, internal versus portal users, sharing and ownership. The business role names in this chapter will be mapped to actual product permissions only after that design is reviewed.
11. Glossary and further reading
Glossary
Action  
A user-invoked operation that opens, changes or processes a record.
Dashboard  
A collection of summaries, charts and reports used to understand a situation and make decisions.
Drill-down  
A path from a summary or chart to the underlying records.
Filter  
A rule that limits the records shown in a report.
Kanban report  
A report that groups records into columns, commonly by lifecycle state.
Navigation  
The links, menus or buttons that help a user move between application tasks.
Page  
A composed Creator screen containing reports, forms, panels, charts, text or other interface elements.
Report  
A view of records arranged for a particular question or task.
Responsive layout  
A layout that adapts to different screen widths.
Task-oriented interface  
An interface organized around what a user needs to accomplish rather than around database entities.
Work queue  
A filtered list of records that require attention or action.
Further reading
- Zoho Creator Resource Center (https://www.zoho.com/creator/help/) — official Creator documentation entry point.
- Zoho Creator Quickstart Guide (https://www.zoho.com/creator/help/new-quickstart-guide.html) — official examples of reports, Kanban reports, Pages, panels, charts and embedded reports.
- Zoho Creator Reports (https://www.zoho.com/creator/newhelp/reports/understand-reports.html) — official report concepts and configuration reference.
- Zoho Creator Kanban Reports (https://www.zoho.com/creator/newhelp/reports/kanban/browser/understand-kanban-report.html) — official Kanban report reference.
- Zoho Creator Pages (https://www.zoho.com/creator/newhelp/pages/understand_pages.html) — official Page-building reference.
- Zoho Creator Mobile (https://help.zoho.com/portal/en/kb/creator/developer-guide/mobile) — official mobile documentation entry point.
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
    - "A hidden interface action does not replace server-side access enforcement."
  chapter_4_artifacts:
    - "C02-CH04_Nova_Field_Service_Reports_and_Pages_v0.1.md"
    - "Dispatcher Home specification"
    - "Technician Home specification"
    - "Service Manager exception view"
    - "Report registry"
    - "Navigation map"
    - "Mobile layout note"
  report_definitions:
    - "Requests to Assign"
    - "Sync Exceptions"
    - "Unassigned Jobs"
    - "Job Status Board"
    - "My Jobs"
    - "Inspection Exceptions"
  open_case_assumptions:
    - "Exact Creator report types, Page components, mobile layout options and menu labels require confirmation in the target edition and environment."
    - "The mapping between application users and Technician business IDs remains open for the access chapter."
    - "No offline Technician workflow is claimed unless separately implemented and tested."
    - "The 30-minute first-response value is a proposed target and must not be reported as achieved when timestamps are missing."
END OF C02-CH04
