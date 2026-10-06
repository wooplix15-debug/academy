# Testing, Rollout and Administration

1. What you will learn
A configured process is not ready simply because its screens, workflows or reports exist. It must be tested with normal and exceptional cases, checked against role permissions, explained to users and assigned to support owners.
This chapter brings the Meridian Supply project together. You will learn to:
- plan functional, integration, data-quality, access and usability tests;
- test normal, invalid, missing-data, denied-action and failed-handoff scenarios;
- distinguish expected results from actual observations;
- prepare user acceptance evidence;
- assess release readiness;
- maintain configuration records and ownership;
- write task-based user instructions;
- route support requests;
- create and manage a controlled improvement backlog;
- prepare a launch pack for a connected business process.
The chapter continues the Meridian project. The supplied continuity from Chapter 17 establishes:
- CRM, Books, Desk and People have different source ownership;
- dashboard metrics require declared grain, formulas, exclusions and refresh information;
- employee data is separate from shared operations reporting;
- finance handoffs use mappings, correlation IDs and recovery evidence;
- no live product execution has been verified.
The launch and testing artifacts in this chapter are synthetic learning artifacts. They do not claim that Meridian or any Zoho product was actually configured, released or operated.
2. Lessons
2.1 What should be tested?
Testing asks whether the configured process behaves as intended under defined conditions.
A complete test case contains:
- test ID;
- objective;
- preconditions;
- input record;
- user role;
- steps;
- expected result;
- actual result;
- evidence reference;
- status;
- defect or follow-up.
Test types
Test type	Question	Meridian example
Functional	Does the feature perform the intended action?	A quote above 10% discount enters approval
Data quality	Are values complete, valid and correctly mapped?	Every CRM product has a Books item
Integration	Does information cross applications correctly?	A Ready handoff reaches Books once
Access	Can each role perform only permitted actions?	Sales cannot edit an invoice
Usability	Can the intended user complete the task?	Sales can submit a quote using the guided screen
Accessibility	Can users operate and understand the interface?	Keyboard focus and text errors work
Exception and recovery	Does failure produce a safe, owned route?	Missing item mapping blocks the handoff
Regression	Did a change break existing behavior?	A new discount rule does not break standard quotes
Reporting	Do metrics reconcile to source records?	Dashboard balance equals invoice-level calculation
A test can pass functionally but fail access testing. For example, the workflow may create the correct task, but an unauthorised user may be able to activate or change it.
Expected versus actual
Result label	Meaning
Expected	What should happen according to the requirement
Actual	What happened when the test was executed
Not executed	No product observation exists
Passed	Actual result agrees with expected result
Failed	Actual result differs from expected result
Blocked	Test could not proceed because a prerequisite was missing
Do not label a test Passed merely because the configuration looks correct.
Check your understanding
Why is a configuration screenshot not enough evidence that a workflow passed?
Answer: A screenshot shows configuration, not execution. The test needs an input, user role, event, actual outcome and evidence that the expected task, message, field change or state transition occurred.
2.2 Functional and access testing
Functional testing checks what the process does. Access testing checks who may do it.
Functional test structure
A useful functional test has:
Given the record and role are prepared,
when the user performs the action,
then the expected state, data and evidence should exist.
Example:
Given a quote with a 12% discount and complete line items,
when a sales representative submits it for approval,
then the quote enters Awaiting Approval and the sales representative cannot approve it.
Access test structure
Test both positive and negative actions.
Role	Positive test	Negative test
Sales representative	Submit quote for approval	Approve own quote
Sales manager	Approve a sales quote	Edit a finance payment
Finance processor	Accept a finance handoff	Edit HR identity documents
Service agent	Update assigned ticket	Change approved quote price
HR administrator	View confidential employee documents	Expose documents to sales
Employee	View own leave request	View another employee’s leave
A negative test is valuable evidence. “Access denied” is an expected result when the role should not perform the action.
Access test evidence
Record:
- user or role;
- record;
- action attempted;
- expected permission;
- actual result;
- message or evidence;
- correction if the result was wrong.
Do not use a system administrator for every test. An administrator may bypass the restrictions that ordinary users experience.
Check your understanding
Why should an access test use a sales user rather than an administrator when testing whether sales can edit an invoice?
Answer: An administrator may have broad permissions that hide the restriction. The test should use the role whose access is being evaluated.
2.3 User acceptance testing
User acceptance testing, or UAT, checks whether the configured process supports the real business task.
UAT is different from technical testing:
- technical testing checks whether a feature behaves according to configuration;
- UAT checks whether users can complete the business process and understand the result.
A UAT scenario should include:
- business role;
- realistic but safe record;
- starting condition;
- task;
- expected business result;
- exception route;
- user feedback;
- acceptance evidence.
Meridian UAT scenarios
Scenario	User	Expected business result
Submit a complete standard quote	Sales representative	Quote follows the standard route
Submit a quote above the discount threshold	Sales representative	Approval is requested
Approve a quote	Sales manager	Approval evidence is recorded
Submit accepted quote to finance	Sales representative	Complete handoff reaches Ready for Finance
Recover failed item mapping	Finance systems owner	Flow retries without duplicate target
Route a High service ticket	Service coordinator	Ticket reaches Technical L2
Correct missing employee evidence	HR administrator	Onboarding can be reassessed
Reconcile dashboard	Finance or operations owner	Dashboard matches source records
UAT evidence may include:
- completed scenario form;
- user comments;
- screenshots or record references;
- defect IDs;
- acceptance decision;
- unresolved questions.
Do not describe an unreviewed draft as accepted. If a user has not tested it, label the scenario Not Executed.
Check your understanding
What is the difference between a technically successful workflow and an accepted business process?
Answer: A technically successful workflow performs its configured action. An accepted business process also supports the user’s real task, produces the required business evidence and handles normal and exception cases understandably.
2.4 Release readiness
Release readiness is a decision based on evidence that the configured process can be introduced safely.
A release-readiness review should consider:
- functional tests;
- access tests;
- integration tests;
- data quality;
- dashboard and report reconciliation;
- user instructions;
- training or orientation;
- support ownership;
- configuration records;
- rollback or deactivation plan;
- known defects;
- unresolved assumptions;
- communication plan.
Readiness categories
Category	Evidence
Configuration	Component register, version and owner
Process	State model, workflow and transition tests
Data	Mapping, duplicate and required-field tests
Access	Role matrix and positive/negative tests
Integration	Successful and failed handoff tests
Reporting	Reconciled dashboard and refresh evidence
User adoption	User guide and UAT feedback
Support	Support route and escalation owner
Recovery	Failed-run, correction and rollback instructions
A release decision should state what is ready, what is not tested and what remains an explicit assumption.
Release states
A synthetic release register may use:
Draft
In Test
Ready for UAT
Ready for Controlled Release
Released
Paused
Rolled Back
Retired
Do not treat Ready for Controlled Release as proof that users have already adopted the process.
Check your understanding
Why should an unresolved High-severity duplicate-order defect affect release readiness?
Answer: It can create financial or operational duplicates. The release owner must either correct and retest it or explicitly hold the affected process.
2.5 Configuration records
A configuration record is the maintained description of what has been built.
It should contain:
- component ID;
- application;
- module;
- purpose;
- owner;
- environment;
- version;
- dependencies;
- fields;
- connections;
- active status;
- last tested date;
- support owner;
- change history.
Meridian configuration register
Component ID	Application	Component	Owner	Dependency
CFG-CRM-WF-01	CRM	Quote follow-up workflow	Sales operations	Quote fields
CFG-CRM-BP-01	CRM	Quote approval Blueprint	Sales systems owner	Approval route
CFG-CRM-GS-01	CRM	Finance handoff guided screen	Sales systems owner	Blueprint transition
CFG-BOOK-MAP-01	Books	Customer and item mapping	Finance systems owner	CRM IDs
CFG-FLOW-01	Flow	CRM-to-Books handoff	Integration owner	CRM and Books connections
CFG-DESK-01	Desk	Ticket routing and escalation	Service systems owner	Customer context
CFG-PEOPLE-01	People	Onboarding workflow	HR systems owner	Employee roles
CFG-AN-01	Analytics	Operations dashboard	Reporting owner	Source connectors
Never store passwords, access tokens or private secrets in a configuration register. Record the connection name and owner, not the secret.
Change history
Version	Date	Change	Reason
0.1	2026-12-01	Initial design	Course project
0.2	2026-12-03	Added missing-item branch	Failed handoff test
0.3	2026-12-05	Restricted employee document access	Access test
Check your understanding
Why should a configuration record include dependencies?
Answer: A change to one component may affect another. For example, changing a CRM field can affect a workflow, a Flow mapping and a dashboard formula.
2.6 Training and user guides
A user guide should answer:
- What task am I performing?
- Which record do I open?
- What information do I need?
- What action do I select?
- What result should I see?
- What should I do if an error appears?
- Who supports me?
Use task-based instructions instead of describing every available feature.
Example user guide: submit an accepted quote to finance
1. Open the accepted quote from the assigned sales work list.
2. Confirm the customer, quote ID, approval state and customer acceptance.
3. Review currency, customer ID, quote ID, total and line items.
4. Correct permitted missing information or choose Return for Correction.
5. Select Submit for Finance.
6. Confirm the message showing Ready for Finance.
7. Do not select or claim Finance Accepted; finance must complete that action.
8. If the flow reports a missing item mapping, record the error and contact the finance systems owner.
A good guide includes a normal example and at least one exception example.
Accessibility and comprehension
User instructions should:
- use plain language;
- identify buttons by their visible labels;
- avoid color-only directions;
- include error recovery;
- use readable headings;
- distinguish customer-facing and internal actions;
- state when a user should stop and ask for help.
Check your understanding
Why should a user guide explain what not to do?
Answer: It prevents users from taking actions that bypass approval, expose confidential information or create duplicate records.
2.7 Support routing and ownership
A support route tells users where to report a problem and tells support staff who owns the correction.
Support levels
Level	Responsibility	Meridian example
L1 process support	Explain normal user steps	Help sales submit a quote
L2 application support	Investigate configuration or permissions	Correct a Blueprint transition
L2 data support	Correct mappings or records	Add a missing Books item mapping
Integration support	Investigate Flow connections and failed runs	Recover a failed handoff
Reporting support	Investigate metrics, refresh and grain	Reconcile dashboard total
Process owner	Decide business rules	Approve a new discount threshold
Vendor or platform support	Investigate product behavior beyond local configuration	Confirm edition-dependent capability
A user should not need to know the technical cause. The intake route should collect:
- application;
- record ID;
- action attempted;
- time;
- error message;
- user role;
- business impact;
- whether a duplicate or incorrect record was created.
Support ownership
Every configuration component should have:
- business owner;
- technical owner;
- data owner;
- support route;
- escalation route;
- review date.
Check your understanding
Who should decide whether Meridian changes the discount approval threshold: an integration administrator or a process owner?
Answer: The process owner should decide the business rule. The administrator may implement it after approval and testing.
2.8 Controlled improvements
An improvement backlog captures proposed changes without changing live configuration immediately.
Classify requests:
- Defect: Configured behavior differs from the approved requirement.
- Data issue: Record or mapping is incorrect.
- Access issue: User can do too much or too little.
- Usability improvement: Task is confusing or inefficient.
- New requirement: Business need was not in the approved scope.
- Reporting issue: Metric, grain, filter or refresh is incorrect.
- Product limitation: Current edition or capability does not support the requirement.
Improvement backlog fields
Field	Purpose
Improvement ID	Stable reference
Date raised	Timing
Source	User, test, support or report
Problem	Observable issue
Impact	Business effect
Priority	Agreed urgency
Owner	Person responsible for analysis
Proposed change	Candidate response
Acceptance criteria	How success will be tested
Dependency	Related component or decision
Release	Planned controlled release
Status	New, Analysing, Approved, In Progress, Tested, Released, Rejected
Do not prioritise only by how often a person complains. Consider impact, risk, affected users, data integrity and dependency.
Controlled improvement lifecycle
Reported
  → Analysed
  → Approved
  → Designed
  → Tested
  → Released
  → Verified
A change that affects invoices, approvals, employee access or dashboard definitions needs regression testing.
Check your understanding
Why should a new request be separated from a defect?
Answer: A defect means the system does not meet an approved requirement. A new request changes scope and needs a separate decision, design and approval.
2.9 Preparing the launch pack
A launch pack brings the evidence together.
It should include:
- process scope and owners;
- configuration register;
- test plan and results;
- access matrix;
- data and integration mapping;
- user guide;
- support routing;
- known issues;
- rollback or deactivation instructions;
- dashboard definitions;
- UAT evidence;
- controlled-improvement backlog;
- communication or release note.
A launch pack should make the process explainable to someone who did not build it.
Product administration procedure
 1. Inventory every configured component.
 2. Link components to business requirements.
 3. Confirm owners and dependencies.
 4. Execute functional and access tests.
 5. Reconcile data and dashboards.
 6. Run UAT scenarios.
 7. Review support and training materials.
 8. Record defects and approved exceptions.
 9. Decide release state.
10. Preserve the launch pack and change history.
Exact product administration screens and export options must be verified in the current editions.
3. Visual explanation
flowchart TD
    A[Configuration inventory] --> B[Functional tests]
    B --> C[Access and data tests]
    C --> D[Integration and recovery tests]
    D --> E[User acceptance]
    E --> F{Known high-impact issue?}
    F -- Yes --> G[Hold, correct and retest]
    F -- No --> H[Prepare launch pack]
    H --> I[Controlled release]
    I --> J[Support monitoring]
    J --> K[Improvement backlog]
    K --> L[Approved change]
    L --> B
The cycle does not end at release. Support evidence and user feedback create controlled improvements that return to testing.
4. Worked case: Meridian launch pack
4.1 Release scope
The synthetic release covers:
- CRM enquiry and quote automation;
- quote approval and controlled transitions;
- guided finance handoff;
- CRM-to-Books Flow;
- Desk ticket routing and escalation;
- People onboarding process;
- operations dashboard;
- user guides and support routing.
Out of scope for this release:
- new accounting policy;
- new employment policy;
- advanced API or Deluge development;
- unverified product features;
- production data migration not listed in the launch pack.
4.2 Functional test matrix
Test ID	Area	Scenario	Expected result
TST-001	CRM	Standard quote is sent	Quote follows standard route
TST-002	CRM	Quote discount is 12%	Approval required
TST-003	CRM	Sales tries to approve own quote	Action denied
TST-004	Guided screen	Complete accepted quote submitted	State becomes Ready for Finance
TST-005	Flow	Complete handoff reaches Books	One target transaction and CRM reference
TST-006	Flow	Missing item mapping	No partial target; error owner assigned
TST-007	Books	Invoice differs from approved quote	Reconciliation exception
TST-008	Desk	High equipment failure is created	Technical L2 and SLA target
TST-009	Desk	High ticket misses response target	Service manager escalation
TST-010	People	Missing onboarding identity evidence	Case blocked or returned
TST-011	People	Sales attempts to view employee record	Access denied
TST-012	Analytics	Dashboard total is compared to source	Difference is zero or explained
These results are deliberately labelled Not Executed. A launch pack cannot claim that the tests passed without actual product evidence.
4.3 Access test matrix
Test ID	Role	Action	Expected result
ACC-001	Sales representative	Submit quote for approval	Allowed
ACC-002	Sales representative	Approve own quote	Denied
ACC-003	Finance processor	Accept finance handoff	Allowed
ACC-004	Sales representative	Edit invoice	Denied
ACC-005	Service agent	Update assigned ticket	Allowed
ACC-006	Service agent	Edit approved quote price	Denied
ACC-007	HR administrator	View identity documents	Allowed
ACC-008	Sales representative	View employee identity documents	Denied
ACC-009	Employee	View own onboarding status	Allowed
ACC-010	Employee	View another employee’s leave	Denied
4.4 Configuration register
Component ID	Application	Owner	Dependency	Version	Test status
CFG-CRM-WF-01	CRM	Sales operations	Quote fields	0.1	Not Run
CFG-CRM-BP-01	CRM	Sales systems owner	Approval route	0.1	Not Run
CFG-CRM-GS-01	CRM	Sales systems owner	Blueprint transition	0.1	Not Run
CFG-BOOK-MAP-01	Books	Finance systems owner	Product mappings	0.1	Not Run
CFG-FLOW-01	Flow	Integration owner	CRM and Books connections	0.1	Not Run
CFG-DESK-01	Desk	Service systems owner	CRM customer context	0.1	Not Run
CFG-PEOPLE-01	People	HR systems owner	Employee role access	0.1	Not Run
CFG-AN-01	Analytics	Reporting owner	Source connectors	0.1	Not Run
4.5 User guide artifact
Submit an accepted quote to finance
Before you begin: Confirm that the quote is approved, accepted by the customer and linked to the correct customer.
1. Open the accepted quote.
2. Confirm the customer, enquiry ID and quote ID.
3. Review approval evidence and customer acceptance.
4. Check currency, customer ID, quote ID, total and line items.
5. If information is missing, choose Return for Correction.
6. If the information is complete, choose Submit for Finance.
7. Confirm that the state changes to Ready for Finance.
8. Do not record Finance Accepted. Finance must perform that action.
9. If a missing-item error appears, record the correlation ID and contact integration support.
Error guide
Message or symptom	User action
Currency is missing	Return for Correction
Item mapping is missing	Record the correlation ID and contact finance systems support
Approval is pending	Wait for the approver; do not send the quote
Finance reference is missing	Check whether finance accepted the handoff
Permission denied	Contact the support route; do not ask another user to share credentials
4.6 Support-routing artifact
Problem	First route	Escalation
User cannot complete a normal task	L1 process support	Application owner
Incorrect workflow or Blueprint	CRM administration	Process owner
Missing customer or item mapping	Data support	Finance systems owner
Failed CRM-to-Books run	Integration support	Integration owner
Incorrect service routing	Desk administration	Service process owner
Confidential People access issue	HR systems support	HR manager
Dashboard mismatch	Reporting support	Data owner and source-system owner
4.7 Improvement backlog
ID	Source	Problem	Type	Impact	Acceptance criterion
IMP-001	Flow test	Retry can create duplicate target if correlation check is skipped	Defect	High	Repeated run creates one target only
IMP-002	User feedback	Finance handoff screen does not show item-mapping owner	Usability	Medium	Error includes owner and recovery route
IMP-003	Dashboard review	Employee data should be separated from operations dashboard	Access issue	High	Non-HR users cannot see employee data
IMP-004	Finance review	Discount mapping requires an explicit amount and basis	Data issue	High	Invoice reconciliation identifies quote discount
IMP-005	Service review	High-ticket escalation recipient is unclear	Process issue	Medium	One named service-manager route exists
4.8 Mistake and correction
Mistake: The launch owner marks the release Ready because every configuration component exists and all tests have expected results.
Why it is wrong: Expected results are not actual observations. The tests are still Not Run.
Correction: Keep the release in a pre-release state, execute the tests, record actual evidence, resolve or accept defects through an explicit decision and update the launch pack.
5. Try it yourself — guided practice
Learning goal
Prepare a launch pack, a user guide and an improvement backlog for the Meridian release.
Complete configuration inputs
Component	Owner	Dependency	Current status
CRM quote workflow	Sales operations	Quote fields	Configured, not tested
CRM approval Blueprint	Sales systems owner	Discount approval	Configured, not tested
Guided finance screen	Sales systems owner	Blueprint transition	Configured, not tested
CRM-to-Books Flow	Integration owner	Item mapping	Configured, not tested
Desk routing	Service systems owner	Customer context	Configured, not tested
People onboarding	HR systems owner	Confidential access	Configured, not tested
Analytics dashboard	Reporting owner	Source refresh	Configured, not reconciled
Complete reported issues
Issue ID	Observation	Severity	Owner
ISSUE-001	A failed Flow retry may create a duplicate Books order	High	Integration owner
ISSUE-002	Sales guide does not explain missing item mapping	Medium	Sales systems owner
ISSUE-003	Dashboard source refresh time is not shown	Medium	Reporting owner
ISSUE-004	HR document access has not been tested with a sales role	High	HR systems owner
ISSUE-005	Desk escalation recipient is not documented	Medium	Service systems owner
Guided steps and expected results
Step 1: Create the launch scope
List included applications, components, users and exclusions.
Expected result: A reader can tell what the release covers and what it does not cover.
Step 2: Create the test register
Add functional, access, integration, reporting and UAT tests.
Expected result: Every high-impact component has at least one normal and one exception test.
Step 3: Create the access evidence plan
Use sales, manager, finance, service, HR and employee roles.
Expected result: Both allowed and denied actions are tested.
Step 4: Record actual status honestly
Mark unexecuted tests Not Run, not Passed.
Expected result: The launch pack distinguishes configuration from product observation.
Step 5: Write the user guide
Choose one task, such as submitting an accepted quote to finance, and write steps, expected result and errors.
Expected result: A user can complete the task without knowing the configuration details.
Step 6: Create the support route
Assign L1, application, data, integration, reporting and process owners.
Expected result: Every likely issue has a first route and escalation owner.
Step 7: Create the improvement backlog
Convert the five reported issues into backlog entries with acceptance criteria.
Expected result: Each item has type, impact, owner and status.
Step 8: Decide readiness
Use this synthetic decision rule:
The release cannot be marked Ready for Controlled Release while a High issue has no mitigation and a required access test has not been executed.
Expected result: The current launch pack remains not ready until ISSUE-001 and ISSUE-004 have a tested resolution or explicit approved mitigation.
Final artifact
Your launch pack should contain:
Artifact	Minimum content
Release scope	Included applications, users and exclusions
Configuration register	Component, owner, version and dependency
Test register	Functional, access, integration, UAT and reporting tests
UAT record	User, scenario, expected and actual result
User guide	Task steps and error recovery
Support matrix	First route and escalation
Improvement backlog	Problem, impact, owner and acceptance criteria
Readiness decision	Evidence-based state and unresolved issues
Safe cleanup
Use a copy of the launch pack for practice. Do not change production configuration while preparing a rollout document. Store no passwords or connection secrets in the pack.
Offline alternative
A document or spreadsheet can create the launch pack, test register and user guide. It cannot demonstrate actual application behavior, access denial, connector execution or user acceptance.
6. Independent challenge
Release candidate review
Meridian has prepared a release candidate with the following results.
Configuration register
Component	Owner	Version	Dependency
CRM approval Blueprint	Sales systems owner	1.1	Discount approval
CRM finance handoff screen	Sales systems owner	1.0	Blueprint
CRM-to-Books Flow	Integration owner	1.2	Item mappings
Desk routing	Service systems owner	1.0	CRM context
People onboarding	HR systems owner	1.0	Confidential access
Analytics dashboard	Reporting owner	1.1	CRM, Books and Desk refresh
Test results
Test ID	Type	Result	Evidence
RC-001	Functional quote approval	Pass	EVID-001
RC-002	Sales denied from invoice edit	Pass	EVID-002
RC-003	Flow normal handoff	Pass	EVID-003
RC-004	Flow retry after partial target creation	Fail: duplicate target created	EVID-004
RC-005	Desk High-ticket escalation	Pass	EVID-005
RC-006	People sales access denial	Not Run	Blank
RC-007	Dashboard reconciliation	Pass	EVID-007
RC-008	User acceptance: sales handoff	Pass with guide correction	EVID-008
Support inputs
Area	First support route	Escalation
CRM	Sales systems support	Process owner
Books mapping	Finance systems support	Finance systems owner
Flow	Integration support	Integration owner
Desk	Service systems support	Service process owner
People	HR systems support	HR manager
Analytics	Reporting support	Data owner
Deliverables
Prepare:
1. a launch decision;
2. a user guide correction;
3. a revised improvement backlog;
4. a test-recovery plan for RC-004;
5. an access-test plan for RC-006;
6. a support-routing matrix;
7. a configuration change record.
Synthetic readiness rule
For this exercise:
A release must not be marked Ready for Controlled Release while a High issue can create duplicate financial records or a required High-risk access test is Not Run.
Do not invent an alternative pass rule. Use the supplied rule.
7. Common problems and recovery
Symptom	Diagnosis	Correction	Verification
All tests are marked Passed before execution	Expected results were confused with actual observations	Mark tests Not Run until executed	Review evidence references
Only the normal path was tested	Exception and recovery paths were omitted	Add missing-data, denied-action, duplicate and failed-handoff tests	Execute each branch
A user can approve their own request	Access test was missing or used the wrong role	Correct permissions and retest	Record denied-action evidence
A release contains an unresolved duplicate-order defect	Business impact was not considered	Hold, correct idempotency and rerun integration tests	Confirm one target per correlation ID
Configuration ownership is unknown	Register lists features but not owners	Add business, technical and data owners	Ask who receives each support request
User guide describes menus rather than tasks	Guide was written for administrators	Rewrite using user goal, steps, result and recovery	Test with intended user
Support tickets go to the person who built the feature	Support ownership was not designed	Use L1, application, data, integration and process routes	Submit a sample support issue
Dashboard is released without source reconciliation	Report was trusted without comparison	Reconcile each KPI to source records	Record difference and reviewer
Employee data appears in shared reports	Sharing was based on dashboard layout only	Separate or restrict the model and test exports	Test a non-HR user
A change is made directly in production	Improvement control was bypassed	Record, approve, test and release the change	Compare configuration versions
Rollback instructions are missing	Deactivation and recovery were not planned	Document safe disablement and data correction	Run a rollback exercise on a test component
A failed integration run is retried blindly	Partial target creation was not checked	Search by correlation ID and inspect execution history	Retry without duplicate
UAT feedback is recorded but not linked to a decision	Acceptance evidence is incomplete	Record user, scenario, result and decision	Review UAT register
Training content exposes confidential data	Real examples were copied into the guide	Use synthetic, masked examples	Review guide as a restricted user
Improvement backlog has no acceptance criteria	Requests cannot be tested	Define observable success conditions	Link to a test case
8. Check your understanding
 1. What information belongs in a test case?
 2. Why are negative access tests necessary?
 3. What is the difference between functional testing and UAT?
 4. Why should a test be labelled Not Run rather than Passed when no product execution occurred?
 5. Name four areas to review before release.
 6. What should a configuration register contain?
 7. Why should a user guide be task-based?
 8. What information should a support request include?
 9. What is the difference between a defect and a new requirement?
10. Why should a failed Flow retry be checked for partial target creation?
11. What synthetic rule prevents release in the independent challenge?
12. What should happen when a dashboard has not been reconciled?
13. Why should employee data be tested separately from shared operational reporting?
14. Who decides whether a business rule should change?
15. What evidence should a UAT decision contain?
9. Solutions and explanations
9.1 Answers to the checks
 1. Test ID, objective, preconditions, input record, user role, steps, expected result, actual result, evidence, status and defect or follow-up.
 2. They prove that users who should not perform an action are actually denied and that confidential or financial controls work.
 3. Functional testing checks configured behavior. UAT checks whether users can complete the real business task and accept the outcome.
 4. There is no actual observation to compare with the expected result.
 5. Functional behavior, access, integrations, data quality, reporting, user instructions, support ownership and recovery.
 6. Component ID, application, purpose, owner, environment, version, dependencies, active status, test status, support route and change history.
 7. Users need to know how to complete a task, what result to expect and how to recover from errors. They do not need a catalog of every administrator option.
 8. Application, record ID, action, time, user role, error, business impact and whether a duplicate or incorrect record was created.
 9. A defect violates an approved requirement. A new requirement changes scope and needs a separate decision.
10. The first attempt may have created the target before failing. Retrying without checking can create a duplicate.
11. A High issue that can create duplicate financial records or a required High-risk access test that is Not Run prevents release.
12. Keep the dashboard out of the release or mark the relevant report unverified until source reconciliation is complete.
13. Employee data has different confidentiality and access requirements.
14. The process owner or authorised business owner decides the rule. An administrator implements it after approval and testing.
15. User, scenario, expected result, actual result, evidence, feedback and acceptance or follow-up decision.
9.2 Guided practice sample solution
Readiness decision
The synthetic launch pack is not ready for controlled release because:
- ISSUE-001 is a High integration risk involving duplicate Books orders;
- ISSUE-004 is a High access issue and its HR access test has not been executed.
The other components may continue through testing, but they do not remove these blockers.
Revised improvement backlog
ID	Type	Impact	Owner	Acceptance criterion
ISSUE-001	Defect	High	Integration owner	Repeated Flow retry finds the existing target by correlation ID and creates no duplicate
ISSUE-002	Usability improvement	Medium	Sales systems owner	Guide explains missing item mapping and support owner
ISSUE-003	Reporting issue	Medium	Reporting owner	Dashboard shows last successful refresh timestamp
ISSUE-004	Access test	High	HR systems owner	Sales cannot view employee records or identity documents
ISSUE-005	Support documentation	Medium	Service systems owner	High-ticket escalation has a named recipient and route
RC-004 recovery plan
 1. Preserve the failed run and duplicate target IDs.
 2. Identify the correlation ID.
 3. Decide which target record is authoritative.
 4. Prevent another retry while the duplicate is investigated.
 5. Correct the Flow’s duplicate-search or update behavior.
 6. Test with a new synthetic handoff and repeat the same event.
 7. Confirm that one correlation ID produces one target record.
 8. Reconcile the duplicate records and document any authorised cleanup.
 9. Retest the normal and failed-retry scenarios.
10. Update the launch decision.
RC-006 access-test plan
Test as:
- sales representative;
- HR administrator;
- manager;
- employee.
Expected outcomes:
- sales representative: no employee-record access;
- HR administrator: permitted confidential access;
- manager: team status, no identity-document contents;
- employee: own record and permitted own requests.
Record the actual product result and evidence reference. Until this is executed, the test remains Not Run.
User-guide correction
Add the missing error route:
If the finance handoff displays a missing item mapping, do not retry repeatedly. Copy the correlation ID, record the missing product, and contact Finance Systems Support. The support owner will correct the mapping and confirm when a retry is safe.
Configuration change record
Field	Value
Change ID	CHG-018-001
Component	CFG-FLOW-01
Change	Add correlation-ID duplicate protection before target creation
Reason	RC-004 duplicate target defect
Owner	Integration owner
Test required	Normal handoff, partial-target retry and duplicate event
Release state	Held until retested
9.3 Independent challenge sample solution
Launch decision
Under the supplied synthetic readiness rule, the release is not ready for Controlled Release.
Reasons:
1. RC-004 failed with a High-severity duplicate-target defect.
2. RC-006 is a High-risk access test and remains Not Run.
The passing functional, service and reporting tests do not override those conditions.
RC-004 recovery
Expected recovery:
- inspect execution history;
- identify the source correlation ID;
- locate both target records;
- determine whether one is a duplicate;
- correct the Flow to search before create;
- test a new handoff and a repeated retry;
- reconcile and document the duplicate target;
- update the configuration register and change history.
The test is not complete until the repeated event produces one target result.
RC-006 access plan
User	Test	Expected result
Sales representative	Open People employee record	Denied
Sales representative	View identity document	Denied
Manager	View team onboarding status	Allowed
Manager	View identity document contents	Denied
HR administrator	View and manage confidential fields	Allowed
Employee	View own onboarding status	Allowed
Employee	View another employee’s record	Denied
Updated user guide
The guide correction should explain:
- what the user sees;
- which action is safe;
- which information to record;
- which support route to use;
- that repeated retries may create duplicates if the Flow is not corrected.
Revised backlog
The high-risk items remain open until tested. Medium items can be scheduled according to the process owner’s decision, but they should not obscure the high-risk release blockers.
10. Chapter recap and next step
Testing, rollout and administration turn configuration into an explainable and supportable process.
You should now be able to:
- write functional, access, integration, data-quality, usability and UAT tests;
- test normal and exception paths;
- distinguish expected results from actual observations;
- prepare an evidence-based release-readiness decision;
- maintain configuration records, ownership and dependencies;
- write role-based user guides;
- route support issues to the correct owner;
- maintain a controlled improvement backlog;
- recover failed handoffs without creating duplicates;
- reconcile reports before release;
- protect employee and finance information during rollout.
For the Meridian Supply project, this chapter produces the final administration and rollout evidence:
C01_CH18_Meridian_Launch_Pack
C01_CH18_Meridian_Functional_and_Access_Test_Register
C01_CH18_Meridian_UAT_Evidence
C01_CH18_Meridian_User_Instructions
C01_CH18_Meridian_Support_Routing_Matrix
C01_CH18_Meridian_Configuration_Register
C01_CH18_Meridian_Improvement_Backlog
The completed course project should show:
- current-state and future-state maps;
- application map, data dictionary and access matrix;
- CRM pipeline, lead capture, assignment and controlled transitions;
- follow-up automation and one guided user experience;
- Books handoff with verified mappings;
- Flow integration and Desk service process;
- separate People operational exercise;
- dashboard reconciled to source records;
- demonstration of a duplicate, denied action or failed handoff;
- user acceptance evidence;
- user instructions;
- support ownership;
- each learner’s explanation of their own configuration and evidence.
The course does not end with a configuration screen. It ends with a process that users can operate, support owners can maintain and business evidence can explain.
11. Glossary and further reading
Glossary
Term	Definition
Access test	Test that confirms what a role may and may not do
Configuration register	Maintained inventory of configured components, owners, dependencies and versions
Defect	Behavior that differs from an approved requirement
Launch pack	Collection of release, test, access, user, support and recovery evidence
Release readiness	Evidence-based assessment of whether a process may be introduced
Regression test	Test that checks whether a change broke existing behavior
Support route	Defined path for reporting and resolving an issue
User acceptance testing	Business-user testing of whether a process supports the intended task
User guide	Role-based instructions for completing a task
Improvement backlog	Controlled list of proposed defects, changes and enhancements
Configuration owner	Person responsible for maintaining a component
Actual observation	Result recorded after a real test execution
Expected result	Result that should occur according to the requirement
Further reading
Check the current product editions, permissions, export features, audit history and administration options before rollout:
- Zoho CRM Help (https://help.zoho.com/portal/en/kb/crm)
- Zoho Books Help (https://help.zoho.com/portal/en/kb/books)
- Zoho Flow Help (https://help.zoho.com/portal/en/kb/flow)
- Zoho Desk Help (https://help.zoho.com/portal/en/kb/desk)
- Zoho People Help (https://help.zoho.com/portal/en/kb/people)
- Zoho Analytics Help (https://help.zoho.com/portal/en/kb/analytics)
This chapter has not verified current product administration screens, audit behavior, release controls, permissions or export options in a live environment. Synthetic test statuses and launch decisions are learning artifacts, not product execution observations.
