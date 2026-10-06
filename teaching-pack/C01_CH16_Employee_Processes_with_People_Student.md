schema_version: "1.1"
course_id: "C01"
chapter_id: "C01-CH16"
chapter_number: 16
chapter_title: "Employee Processes with People"
filename: "C01_CH16_Employee_Processes_with_People_Student.md"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "not_verified"
---
Employee Processes with People
1. What you will learn
Employee processes contain personal, employment and operational information. They need clear ownership, controlled access, approvals and evidence.
This chapter uses Zoho People as the candidate employee-process application for Meridian Supply. It covers stable process concepts and an implementation method. Exact current Zoho People screens, editions, modules, permissions and regional behavior must be verified before production use.
You will learn to:
- structure employee records;
- design onboarding processes;
- distinguish leave, attendance, shifts and timesheets;
- manage employee documents and employee cases;
- configure approvals and notifications;
- protect confidential employee information;
- define access for HR, managers, IT, facilities, payroll and employees;
- create and test an onboarding process;
- design a leave-approval process;
- recover from missing information, denied access and incomplete approvals.
The employee process is separate from the Meridian sales, finance and customer-service processes. A sales representative should not gain access to employee records merely because the person is also a Meridian user.
This chapter continues the project records from Chapter 15. The supplied continuity establishes:
- service records and employee records have separate access boundaries;
- CRM and Books records should not be used as substitutes for employee records;
- service teams may see limited CRM context but should not edit approved commercial values;
- no live product execution has been verified.
The employee records, onboarding rules and leave rules in this chapter are synthetic learning assumptions. They are not legal requirements, payroll rules, employment policies or universal HR practices.
2. Lessons
2.1 Employee records and confidential access
An employee record represents a person’s employment relationship with the organisation. It should have a stable employee ID and carefully defined fields.
Typical employee-record categories include:
- identity and contact;
- employment details;
- department and manager;
- work location;
- start and end dates;
- role or position;
- onboarding status;
- leave information;
- attendance and shift information;
- documents;
- employee cases.
Not every user should see every category.
Employee business ID
Use an organisation-owned employee ID such as:
MER-EMP-001
A product may generate another internal record ID. Preserve both separately if required. Do not use an email address as the permanent employee ID because email addresses can change.
Information sensitivity
A practical access classification is:
Information class	Example	Typical access
General employee information	Name, department, work email	Employee, manager and authorised HR
Operational information	Shift, onboarding task, attendance status	Employee, manager and responsible operations roles
Confidential information	Identity-document reference, payroll form status, employee case	HR and specifically authorised roles
Highly restricted information	Investigation notes or sensitive case details	Limited HR or authorised case roles
The labels in this table are design categories for the learning case. The organisation must define its own information classification and access policy.
Access should follow the task
A manager may need to know that an employee’s onboarding checklist is incomplete, but not see the employee’s identity document. IT may need the employee’s name, start date and technical setup task, but not salary information.
Check your understanding
Why should a manager see onboarding progress without automatically seeing identity documents?
Answer: Progress supports the manager’s operational responsibility. Identity documents are confidential and should be limited to roles that require them.
2.2 Employee onboarding
Onboarding is the controlled process of preparing an employee to begin and perform work.
A useful onboarding process defines:
- requestor;
- employee;
- manager;
- start date;
- department and role;
- required documents;
- required equipment;
- system-access tasks;
- orientation or induction;
- approval;
- readiness criteria;
- completion evidence;
- exception route.
A start date does not prove that onboarding is complete. The process must check the required evidence.
Synthetic Meridian onboarding rule
For this chapter, an onboarding case is complete only when all five conditions are recorded:
1. identity evidence verified;
2. employment document recorded as complete;
3. equipment ready;
4. required account access ready;
5. induction completed.
A missing value is not treated as complete.
Onboarding states
Requested
  → HR Review
  → Manager Approved
  → In Progress
  → Ready
  → Complete
Exception states:
Returned for Correction
Blocked
Cancelled
Each transition should have an owner. For example, HR may complete the review, the manager may approve the request, IT may complete the account task and the employee may confirm induction.
Onboarding checklist
Checklist item	Owner	Completion evidence
Identity evidence	HR	Verification status and document reference
Employment document	HR	Signed or recorded document status
Equipment	Facilities or IT	Equipment-ready confirmation
Account access	IT	Account-ready confirmation
Induction	HR or manager	Attendance or completion record
Check your understanding
Why should an onboarding case not be marked Complete merely because the employee’s start date has passed?
Answer: A date does not prove that identity, documents, equipment, access and induction are complete. Completion requires the defined evidence.
2.3 Leave processes
A leave process records a request, checks the applicable balance or eligibility, routes an approval and updates the approved result.
A leave request should contain:
- employee ID;
- leave type;
- start date;
- end date;
- calculated working days;
- approver;
- balance or availability where applicable;
- reason or supporting information, with appropriate confidentiality;
- current state;
- approval and cancellation history.
The exact leave types, balances, carryover and approval rules must come from the organisation’s approved policy. This chapter uses a synthetic Planned Leave type.
Working-day calculation
For the practice case:
- working days are Monday to Friday;
- no holidays are supplied;
- dates are inclusive.
For 2026-12-14 through 2026-12-16:
Monday 14 December = 1 day
Tuesday 15 December = 1 day
Wednesday 16 December = 1 day

Working days = 3
For 2026-12-18 through 2026-12-28:
Friday 18 December = 1
Monday 21 December = 1
Tuesday 22 December = 1
Wednesday 23 December = 1
Thursday 24 December = 1
Friday 25 December = 1
Monday 28 December = 1

Working days = 7
If holidays, part-time schedules or regional calendars apply, the calculation must use the approved calendar rather than this simplified example.
Approval routes
The synthetic rules for the independent challenge are:
- up to 5 working days: manager approval;
- more than 5 working days: manager approval followed by HR review;
- insufficient balance: return or deny according to the defined process;
- overlap with an already approved request in the same team: exception review;
- missing manager: block the request until corrected.
These rules are not employment-policy requirements.
Check your understanding
Why should a pending leave request not immediately reduce an employee’s approved balance?
Answer: A pending request has not yet been approved. The process should define whether a pending request is reserved, but it should not silently treat it as approved.
2.4 Attendance, shifts and timesheets
These records are related but different.
Record	Meaning	Example
Shift	Planned working schedule	Monday 09:00–17:00
Attendance	Evidence of presence or attendance event	Check-in at 08:58
Timesheet	Work effort recorded against a task, project or activity	3 hours on installation planning
Leave	Approved or requested absence	Planned Leave for 3 working days
Do not infer one from another:
- A timesheet does not prove physical attendance.
- Attendance does not explain which project received the time.
- A scheduled shift does not prove that the employee worked.
- An approved leave request does not prove that the employee’s attendance record was updated.
Time calculation
Suppose a shift is 09:00–17:00 with a 1-hour unpaid break:
Elapsed time = 17:00 − 09:00 = 8 hours
Work time = 8 − 1 break hour = 7 hours
The organisation must define whether breaks, overtime, travel and rounding are included. Do not invent payroll calculations from a timesheet alone.
Attendance exceptions
Examples include:
- missing check-in;
- duplicate check-in;
- check-out before check-in;
- attendance outside the assigned shift;
- approved leave but attendance recorded;
- shift changed without approval.
An exception should be assigned to an owner rather than silently corrected.
Check your understanding
Why should a timesheet entry not automatically create an attendance record?
Answer: A timesheet records claimed work against an activity. Attendance records presence or attendance events. They have different meanings and may require different evidence.
2.5 Documents and employee cases
Employee documents
Documents may include:
- identity evidence;
- employment documents;
- policy acknowledgements;
- training records;
- certifications;
- equipment acknowledgements;
- leave supporting information.
A document process should define:
- document type;
- employee association;
- owner;
- status;
- version;
- submission date;
- review date;
- access;
- correction route;
- retention or deletion responsibility according to approved policy.
Do not store confidential documents in a broadly accessible shared folder merely because it is convenient.
Employee cases
An employee case is a controlled record for an HR issue or request. Examples may include:
- onboarding exception;
- missing document;
- attendance correction;
- leave dispute;
- employee query;
- confidential review.
The case should have:
- case ID;
- employee;
- category;
- owner;
- state;
- priority;
- notes;
- evidence;
- access restriction;
- resolution;
- closure authority.
A manager may be able to see that a case exists without seeing its confidential notes.
Check your understanding
Why should an employee case have its own access design instead of inheriting the access of the employee’s department?
Answer: A case may contain more sensitive information than ordinary department data. Access should be based on the case responsibility and confidentiality, not only the employee’s department.
2.6 Approvals, notifications and employee access
Employee processes often require several approvals:
- manager approval for onboarding request;
- HR review for confidential documents;
- manager approval for leave;
- HR review for exceptions;
- payroll or finance confirmation for relevant outputs.
Approval design should specify:
- requester;
- approver;
- decision;
- mandatory information;
- rejection or return reason;
- escalation;
- evidence;
- access to the decision.
Notifications should not expose confidential information. A manager’s notification can say:
Leave request MER-LEAVE-201 requires your decision for employee MER-EMP-201.
It does not need to include confidential medical or identity details.
An employee should be able to see their own request status where appropriate, but not other employees’ records.
Escalation
An approval escalation may notify an HR manager when a request has been pending beyond a synthetic target. Do not use escalation to force approval. It should highlight waiting work and assign responsibility.
Check your understanding
What should a manager receive when a confidential employee case requires review?
Answer: The manager should receive only the information necessary to perform the permitted review, such as the case ID, employee and required action. Confidential notes should remain restricted.
2.7 Configuring employee processes with People
This procedure uses common employee-process concepts and Zoho People terminology. Exact screens, editions, modules, regional features and permission names must be verified.
Required access
You need suitable access to:
- create and update employee records;
- configure onboarding or employee workflows;
- configure leave types, calendars and approval routes;
- configure attendance, shifts and timesheets;
- manage documents;
- create and manage employee cases where supported;
- define role and field access;
- configure notifications and escalations;
- test as employee, manager, HR, IT and restricted sales user.
Procedure
1. Define the employee process boundary.
Example: manager request received through onboarding complete or exception.
Expected result: The process does not accidentally include customer-service or sales records.
2. Create or confirm employee fields.
Expected result: Employee ID, manager, department, start date and role have defined ownership.
3. Define states and checklist items.
Expected result: Each onboarding or leave state has entry, exit and evidence rules.
4. Configure approval routes.
Expected result: The requester cannot approve their own request where separation is required.
5. Configure confidential fields and documents.
Expected result: HR-only information is inaccessible to sales and unauthorised roles.
6. Configure notifications and escalations.
Expected result: The right role receives the next action without seeing unnecessary confidential information.
7. Test attendance, shifts and timesheets separately.
Expected result: Each record type retains its own meaning and evidence.
8. Test normal and exception cases.
Expected result: Missing documents, missing managers, insufficient leave and denied access have clear recovery routes.
9. Activate and document support ownership.
Expected result: Employees know where to ask about a request, and administrators know who owns configuration.
3. Visual explanation
flowchart TD
    A[Manager submits employee request] --> B[HR reviews employee information]
    B --> C{Required information complete?}
    C -- No --> D[Return for correction]
    C -- Yes --> E[Manager approval]
    E -- Rejected --> F[Close with reason]
    E -- Approved --> G[Create onboarding checklist]
    G --> H[HR documents]
    G --> I[IT account]
    G --> J[Equipment]
    G --> K[Induction]
    H --> L{All readiness evidence complete?}
    I --> L
    J --> L
    K --> L
    L -- No --> M[Exception owner follows up]
    L -- Yes --> N[Onboarding Complete]
The diagram shows that an employee record can exist before onboarding is complete. Each checklist item has a separate owner and evidence. The final state depends on all required evidence, not only the start date.
4. Worked case: Meridian onboarding
4.1 Scenario rules
The following rules are synthetic:
- HR owns employee identity and confidential documents.
- The manager owns the request and confirms role, department and start date.
- IT owns account setup.
- Facilities owns equipment readiness.
- HR or the manager owns induction evidence.
- Onboarding is complete only when identity, employment document, equipment, account and induction are complete.
- The manager sees progress but not identity-document contents.
- Sales has no access to employee records.
- A missing value causes a return or exception, not an assumption of completion.
4.2 Employee records
Employee ID	Name	Email	Department	Role	Manager
MER-EMP-001	Amina Rahman	amina.rahman@example.com (mailto:amina.rahman@example.com)	Operations	Service Coordinator	MER-MGR-001
MER-EMP-002	Jordan Lee	jordan.lee@example.com (mailto:jordan.lee@example.com)	Sales	Account Executive	MER-MGR-002
MER-EMP-003	Priya Shah	priya.shah@example.com (mailto:priya.shah@example.com)	Technical Support	Support Specialist	MER-MGR-003
4.3 Checklist evidence
Employee	Identity	Employment document	Equipment	Account
MER-EMP-001	Verified, MER-DOC-001	Complete, MER-DOC-002	Ready, MER-TASK-001	Ready, MER-TASK-002
MER-EMP-002	Verified, MER-DOC-003	Complete, MER-DOC-004	Ready, MER-TASK-003	Ready, MER-TASK-004
MER-EMP-003	Missing	Complete, MER-DOC-005	Not started	Not started
4.4 Expected state results
Employee	Result	Explanation
MER-EMP-001	Not complete	Induction is not complete
MER-EMP-002	Complete or Ready for final closure	All five required items have evidence
MER-EMP-003	Returned or Blocked	Identity evidence is missing and downstream tasks have not started
MER-EMP-001 has a start date of 2026-12-01, but that date does not prove completion.
4.5 Access matrix
Role	Employee general data	Confidential documents	Onboarding tasks	Leave records
Employee	Own record	Own permitted documents	Own checklist	Own requests
Manager	Team progress	No document contents	Team tasks and approval	Team requests
HR administrator	View and edit	View and edit	View and edit	View and edit
HR manager	View and edit	View, edit and approve	Approve exceptions	Approve exceptions
IT	Required technical fields	No access	Edit account task	No access
Facilities	Required equipment fields	No access	Edit equipment task	No access
Payroll or finance	Required approved outputs	Only fields required for work	No onboarding edit	Approved leave output as permitted
Sales representative	No access	No access	No access	No access
4.6 Mistake and correction
Mistake: A manager marks MER-EMP-001 complete because the employee started work and the equipment and account are ready.
Why it is wrong: The induction evidence is still missing. The completion rule requires all five checklist items.
Correction: Keep the case In Progress, assign the induction task to its owner and mark the onboarding exception if the induction cannot be completed. Do not backdate completion.
5. Try it yourself — guided practice
Learning goal
Build and test an employee-onboarding process with confidential access and exception routes.
Required access
You need:
- employee-process administration access;
- permission to create employee fields and onboarding states;
- permission to configure approval routes;
- permission to manage documents and tasks;
- HR, manager, IT, employee and sales test roles;
- synthetic employee records.
Complete sample inputs
Employee ID	Name	Email	Department	Manager	Start date	Identity	Contract	Equipment
MER-EMP-101	Aisha Green	aisha.green@example.com (mailto:aisha.green@example.com)	Operations	MER-MGR-OPS	2026-12-07	Complete	Complete	Pending
MER-EMP-102	Bruno Silva	bruno.silva@example.com (mailto:bruno.silva@example.com)	Sales	MER-MGR-SALES	2026-12-14	Complete	Complete	Complete
MER-EMP-103	Chen Li	chen.li@example.com (mailto:chen.li@example.com)	Technical Support	MER-MGR-TECH	2026-12-01	Missing	Complete	Complete
Onboarding requirements
1. Manager submits the employee request.
2. HR checks employee, manager, department and start date.
3. Manager approves the request.
4. HR, IT and facilities complete their checklist items.
5. HR records induction evidence.
6. Onboarding becomes Complete only when all five evidence values are complete.
7. Missing identity evidence routes to HR correction.
8. A sales user cannot view employee records.
9. Managers see team progress but not confidential document contents.
Guided steps and expected results
Step 1: Define states
Create:
Requested
HR Review
Manager Approval
In Progress
Ready
Complete
Returned for Correction
Blocked
Expected result: Every sample employee can be placed in one state.
Step 2: Create employee fields
Define employee ID, manager, department, role, start date, document statuses, equipment status, account status and induction status.
Expected result: Each field has an owner and confidentiality level.
Step 3: Create the onboarding checklist
Create five checklist items with owners and completion evidence.
Expected result: HR, IT, facilities and the manager can identify their responsibilities.
Step 4: Configure approval
Require manager approval after HR review.
Expected result: HR can review, but the manager makes the approval decision.
Step 5: Configure completion control
Require all five evidence fields before Complete.
Expected result:
- MER-EMP-101 remains In Progress.
- MER-EMP-102 can reach Complete.
- MER-EMP-103 is returned or blocked because identity evidence is missing.
Step 6: Test confidential access
Test HR, manager, IT, employee and sales roles.
Expected result: Sales has no employee access; IT and facilities see only their task information; HR can see confidential documents.
Step 7: Test recovery
Supply identity evidence for MER-EMP-103 through the HR correction route.
Expected result: The case can be reassessed after the evidence is recorded. The earlier missing-data exception remains traceable.
Final artifact
Your submission should contain:
Artifact	Minimum content
Employee field dictionary	Meaning, owner, sensitivity and format
Onboarding state model	States, transitions, owners and evidence
Checklist	Task, owner, status and completion proof
Access matrix	Role and permitted information
Approval design	Requester, approver, outcome and escalation
Test evidence	Complete, incomplete, denied-access and recovery tests
User instructions	Employee, manager and HR steps
Safe cleanup
Use only synthetic employee records and documents. Deactivate practice workflows and remove test documents through the permitted HR process. Do not delete shared employee fields or live onboarding records.
Offline alternative
A spreadsheet can model onboarding states, checklist completion and access decisions. It cannot demonstrate actual People permissions, document privacy, employee self-service or approval history.
6. Independent challenge
Planned-leave approval process
Design a leave-approval process using the following synthetic rules:
- working days are Monday to Friday;
- no holidays are supplied;
- dates are inclusive;
- requests up to 5 working days require manager approval;
- requests above 5 working days require manager approval followed by HR review;
- insufficient balance is returned for correction;
- overlap with an already approved request in the same team requires exception review;
- approved leave reduces available balance;
- pending leave does not reduce approved balance;
- confidential reasons are visible to HR but not necessarily to the manager;
- missing manager blocks approval.
Complete employee data
Employee ID	Name	Department	Manager	Available planned-leave days
MER-EMP-201	Nia Patel	Operations	MER-MGR-OPS	8
MER-EMP-202	Leo Martin	Operations	MER-MGR-OPS	10
MER-EMP-203	Sam Rivera	Technical Support	MER-MGR-TECH	2
MER-EMP-204	Priya Shah	Operations	MER-MGR-OPS	5
MER-EMP-205	Noor Ali	Sales	Blank	5
Complete leave requests
Leave ID	Employee	Leave type	Start	End	Current state
MER-LEAVE-201	MER-EMP-201	Planned Leave	2026-12-14	2026-12-16	Approved
MER-LEAVE-202	MER-EMP-202	Planned Leave	2026-12-18	2026-12-28	Submitted
MER-LEAVE-203	MER-EMP-203	Planned Leave	2026-12-22	2026-12-24	Submitted
MER-LEAVE-204	MER-EMP-204	Planned Leave	2026-12-15	2026-12-17	Submitted
MER-LEAVE-205	MER-EMP-205	Planned Leave	2026-12-21	2026-12-21	Submitted
Deliverables
Create:
1. a leave-request state model;
2. a working-day calculation for every request;
3. manager and HR approval routes;
4. balance and overlap validation;
5. confidential-reason access rules;
6. approval and escalation notifications;
7. an access matrix;
8. expected results and recovery paths.
Success criteria
Your design should:
- calculate the working days correctly;
- route MER-LEAVE-202 to manager approval followed by HR review;
- return MER-LEAVE-203 because balance is insufficient;
- route MER-LEAVE-204 to overlap exception review;
- block MER-LEAVE-205 because the manager is missing;
- avoid reducing balance for pending requests;
- keep confidential reasons restricted.
7. Common problems and recovery
Symptom	Diagnosis	Correction	Verification
A sales user can view employee records	Employee access was inherited from a broad organisation role	Restrict employee modules and fields	Test sales login
An employee is marked onboarded because the start date passed	Completion evidence is missing	Require the checklist gate	Test an incomplete employee
A manager sees identity documents	Confidential fields are not restricted	Separate progress access from document access	Open the record as manager
IT can edit payroll fields	Access is based on convenience rather than task	Limit IT to technical onboarding fields	Test IT role
A pending leave request reduces balance	Pending and approved states are mixed	Reduce balance only after approval	Compare balance before and after approval
Leave days are calculated incorrectly over a weekend	Calendar logic is missing	Count inclusive weekdays using the defined calendar	Recalculate a Friday-to-Monday request
An HR review is skipped for a long request	Approval criteria use dates but not working-day count	Branch on calculated working days	Test a request above 5 days
Overlapping leave is automatically denied without review	Exception policy is missing	Route to manager or HR coverage review	Submit overlapping requests
A leave reason appears in a manager notification	Confidential data is included in the template	Send only request ID and action; restrict reason	Inspect manager and HR messages
A document is replaced without preserving version	Document control is incomplete	Record version, owner and review evidence	Upload a revised synthetic document
An employee case is visible to the whole department	Case access inherited from department	Restrict by case role and sensitivity	Test employee, manager and sales roles
An attendance event is treated as a timesheet entry	Record meanings were combined	Keep attendance, shifts and timesheets separate	Compare one shift and one timesheet
A leave approval has no manager	Employee record is incomplete	Block or route to HR correction	Test a request with blank manager
An onboarding exception has no owner	Exception route was omitted	Assign HR or manager owner and due action	Return a test case
A workflow exposes confidential data in an email	Notification audience was not reviewed	Use minimal fields and separate internal templates	Trigger each notification
8. Check your understanding
 1. What is the purpose of a stable employee ID?
 2. Name three types of information that may require confidential access.
 3. What evidence is required for onboarding completion in the worked case?
 4. Why should IT see an account task but not payroll details?
 5. What is the difference between leave, attendance, shifts and timesheets?
 6. Calculate the working days from 2026-12-14 through 2026-12-16.
 7. Calculate the working days from 2026-12-18 through 2026-12-28 using the supplied calendar.
 8. Why should a pending leave request not automatically reduce approved balance?
 9. Which independent-challenge request requires HR review after manager approval?
10. Which request must be blocked because the manager is missing?
11. What should happen when identity evidence is missing?
12. Why should employee cases have separate access rules?
13. What should a manager notification contain for a confidential leave request?
14. Why should a passed start date not prove onboarding completion?
15. What is the difference between a document owner and a document reviewer?
9. Solutions and explanations
9.1 Answers to the checks
 1. It provides a stable organisation-owned reference that remains meaningful even if an email address or product-generated ID changes.
 2. Identity documents, payroll details, employee-case notes and sensitive supporting documents may require confidential access.
 3. Identity evidence, employment document, equipment, account access and induction must all be complete.
 4. IT needs technical information to complete its task. Payroll details are unrelated to that task and should remain restricted.
 5. Leave records absence approval; attendance records presence events; shifts record planned schedules; timesheets record work effort against tasks or projects.
 6. Three working days.
 7. Seven working days.
 8. The request is not yet approved. The process must distinguish requested, approved and cancelled states.
 9. MER-LEAVE-202, because it covers seven working days, which is above the synthetic five-day threshold.
10. MER-LEAVE-205.
11. The onboarding case should be returned or blocked, assigned to HR and corrected with evidence. It should not be marked complete.
12. Cases may contain more sensitive information than general employee records. Access should follow case responsibility and sensitivity.
13. It should contain the request ID, employee, decision required and due action. It should not include confidential reasons unless the manager is authorised to see them.
14. Dates show planned timing, not completion evidence.
15. The owner maintains the document or process. The reviewer checks whether it is accurate and suitable for approval or publication.
9.2 Guided practice sample solution
State model
Requested
  → HR Review
  → Manager Approval
  → In Progress
  → Ready
  → Complete

HR Review
  └── missing information → Returned for Correction

In Progress
  └── blocked task → Blocked

Manager Approval
  └── rejected → Returned for Correction
Expected employee results
Employee	Expected state	Explanation
MER-EMP-101	In Progress	Equipment, account and induction are incomplete
MER-EMP-102	Ready or Complete	All required evidence is complete
MER-EMP-103	Returned for Correction or Blocked	Identity evidence is missing
Access result
Role	Expected result
HR	Can view and manage all supplied onboarding fields and confidential documents
Manager	Can see team progress and approval actions but not identity-document contents
IT	Can update account task only
Employee	Can see own onboarding checklist
Sales	Cannot view employee records
Correction for MER-EMP-103
1. HR assigns the missing identity-evidence task.
2. HR records the document reference and verification status.
3. The case is reassessed.
4. If all other evidence is complete, the case can move to Ready.
5. Completion remains separate from the date of the correction.
9.3 Independent challenge sample solution
Working-day calculations
MER-LEAVE-201:
2026-12-14 Monday = 1
2026-12-15 Tuesday = 1
2026-12-16 Wednesday = 1

Total = 3 working days
MER-LEAVE-202:
2026-12-18 Friday = 1
2026-12-21 Monday = 1
2026-12-22 Tuesday = 1
2026-12-23 Wednesday = 1
2026-12-24 Thursday = 1
2026-12-25 Friday = 1
2026-12-28 Monday = 1

Total = 7 working days
MER-LEAVE-203:
2026-12-22 Tuesday = 1
2026-12-23 Wednesday = 1
2026-12-24 Thursday = 1

Total = 3 working days
Available balance = 2 days
MER-LEAVE-204:
2026-12-15 Tuesday = 1
2026-12-16 Wednesday = 1
2026-12-17 Thursday = 1

Total = 3 working days
MER-LEAVE-205:
2026-12-21 Monday = 1 working day
Expected routes
Leave request	Expected route	Explanation
MER-LEAVE-201	Existing approved request	Three days and sufficient balance
MER-LEAVE-202	Manager approval → HR review	Seven days exceeds the five-day threshold
MER-LEAVE-203	Returned or denied for correction	Three days exceeds available balance of two
MER-LEAVE-204	Overlap exception review	Overlaps an already approved request in the same team
MER-LEAVE-205	Blocked	Manager is missing
Balance treatment
For MER-LEAVE-201, after approval:
Initial balance = 8 days
Approved leave = 3 days
Remaining balance = 8 − 3 = 5 days
For MER-LEAVE-202, its seven-day request is pending, so the supplied balance remains 10 until the request is approved under the synthetic rules.
Confidential access
The manager may see:
Leave ID: MER-LEAVE-201
Employee: Nia Patel
Dates: 2026-12-14 to 2026-12-16
Working days: 3
Decision required: Yes
The manager should not automatically see a confidential reason field. HR may see the reason if required for its task.
Overlap recovery
MER-LEAVE-204 overlaps the approved dates of MER-LEAVE-201. The process should not silently approve or deny it. A manager or HR reviewer should assess coverage, record the decision and either approve, return or reject it according to the synthetic process.
10. Chapter recap and next step
Employee processes require clear lifecycle stages, role-based access, evidence and confidentiality.
You should now be able to:
- define a stable employee record and ID;
- separate general, operational and confidential information;
- design onboarding states, checklist items and completion gates;
- define leave requests, working-day calculations and approval routes;
- distinguish attendance, shifts and timesheets;
- control employee documents and cases;
- define role-based access for HR, managers, employees, IT and facilities;
- prevent pending leave from being treated as approved;
- route missing information and approval exceptions;
- test confidential access and denied actions.
For the Meridian Supply project, this chapter produces:
C01_CH16_Meridian_Employee_Record_and_Access_Design
C01_CH16_Meridian_Onboarding_State_and_Checklist
C01_CH16_Meridian_Employee_Document_and_Case_Register
C01_CH16_Meridian_Leave_Approval_and_Exception_Design
C01_CH16_Meridian_People_Test_and_Confidentiality_Evidence
The next chapter examines reporting and Zoho Analytics. It builds on the need for defined record grain, source ownership, calculated measures, access and reconciliation.
11. Glossary and further reading
Glossary
Term	Definition
Attendance	Record of presence or attendance events
Employee case	Controlled record for an HR issue, request or exception
Employee record	Record representing a person’s employment relationship
Employee ID	Stable organisation-owned identifier for an employee
Employee document	File or evidence associated with an employee process
Leave balance	Available amount of a defined leave type under an approved rule
Leave request	Request for an employee absence over defined dates
Onboarding	Process of preparing an employee to begin and perform work
Shift	Planned working schedule
Timesheet	Record of work effort against a task, project or activity
Confidential field	Information limited to authorised roles
Approval route	Sequence of authorised review and decision steps
Checklist	Required tasks and evidence for a process
Further reading
Check the current edition, regional features, employee modules, leave calendars, attendance, shifts, timesheets, documents, cases and permissions before implementation:
- Zoho People Help (https://help.zoho.com/portal/en/kb/people)
- Zoho People documentation (https://www.zoho.com/people/help/)
- Zoho People automation help (https://help.zoho.com/portal/en/kb/people/automation)
- Zoho CRM Help (https://help.zoho.com/portal/en/kb/crm)
- Zoho Flow Help (https://help.zoho.com/portal/en/kb/flow)
This chapter has not verified current Zoho People screens, employee self-service, leave behavior, document permissions, attendance calculations or regional settings in a live environment. Synthetic employee records and policies are learning examples, not employment or legal requirements.
continuity:
  previous_continuity:
    supplied: "C01-CH15"
    source_artifacts:
      - "C01_CH15_Meridian_Desk_Intake_and_Routing_Design"
      - "C01_CH15_Meridian_Department_Queue_and_Assignment_Matrix"
      - "C01_CH15_Meridian_Service_Target_and_Escalation_Register"
      - "C01_CH15_Meridian_CRM_Service_Context_Design"
      - "C01_CH15_Meridian_Knowledge_Base_Ownership_and_Article"
      - "C01_CH15_Meridian_Service_Test_and_Reporting_Evidence"
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
    added_for_employee_practice:
      - MER-EMP-001
      - MER-EMP-002
      - MER-EMP-003
      - MER-MGR-001
      - MER-MGR-002
      - MER-MGR-003
      - MER-DOC-001
      - MER-DOC-002
      - MER-DOC-003
      - MER-DOC-004
      - MER-DOC-005
      - MER-TASK-001
      - MER-TASK-002
      - MER-TASK-003
      - MER-TASK-004
      - MER-TRAIN-002
      - MER-EMP-101
      - MER-EMP-102
      - MER-EMP-103
      - MER-MGR-OPS
      - MER-MGR-SALES
      - MER-MGR-TECH
      - MER-LEAVE-201
      - MER-LEAVE-202
      - MER-LEAVE-203
      - MER-LEAVE-204
      - MER-LEAVE-205
      - MER-EMP-201
      - MER-EMP-202
      - MER-EMP-203
      - MER-EMP-204
      - MER-EMP-205
  case_decisions:
    - "Employee processes are separate from Meridian sales, finance and customer-service processes."
    - "HR owns identity and confidential employee documents."
    - "Managers see team progress but not confidential document contents."
    - "IT and facilities receive only the onboarding fields required for their tasks."
    - "Onboarding is complete only when identity evidence, employment document, equipment, account and induction are complete."
    - "Pending leave does not automatically reduce approved balance."
    - "Synthetic leave rules use inclusive Monday-to-Friday working days with no supplied holidays."
    - "Leave requests above five working days require manager approval followed by HR review."
    - "Confidential employee-case information is restricted by role and case sensitivity."
  artifacts:
    - "C01_CH16_Meridian_Employee_Record_and_Access_Design"
    - "C01_CH16_Meridian_Onboarding_State_and_Checklist"
    - "C01_CH16_Meridian_Employee_Document_and_Case_Register"
    - "C01_CH16_Meridian_Leave_Approval_and_Exception_Design"
    - "C01_CH16_Meridian_People_Test_and_Confidentiality_Evidence"
  open_case_assumptions_next_chapter:
    - "The exact current Zoho People modules, permissions, leave behavior, document access and reporting capabilities must be verified."
    - "The next chapter should keep employee data separate when combining reports with CRM, Books and Desk data."
    - "Employee metrics must define record grain, confidentiality and permitted dashboard audiences."
    - "Any cross-application employee update must use minimum necessary fields and an approved connection."
END OF C01-CH16
