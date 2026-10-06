schema_version: "1.1"
course_id: "C01"
chapter_id: "C01-CH11"
chapter_number: 11
chapter_title: "Guided Screens and User Actions"
filename: "C01_CH11_Guided_Screens_and_User_Actions_Student.md"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "not_verified"
---
Guided Screens and User Actions
1. What you will learn
A user may have permission to perform a task but still struggle to complete it correctly. Too many fields, unclear labels, missing context and poorly timed actions increase errors.
A guided screen presents the information and actions needed for one specific task. It should help the user complete valid work without hiding important controls or bypassing an approval process.
In this chapter, you will learn to:
- distinguish layouts, Canvas designs, wizards and Kiosk Studio interfaces;
- choose a screen type for a specific business task;
- design a screen around a user, goal, context, inputs and outcome;
- configure fields, sections, read-only information and validation;
- create guided actions that connect to controlled process transitions;
- use a wizard to collect information in a sensible sequence;
- use Canvas to present relevant record context;
- evaluate when Kiosk Studio may be suitable;
- apply usability and accessibility principles;
- test normal, missing-data, permission and recovery paths;
- create a guided sales task for Meridian Supply.
This chapter continues the controlled state and approval design from Chapter 10. The supplied continuity establishes:
- Blueprints control authorised movement between states;
- approvals and reviews must not be replaced by simple notifications;
- Ready for Finance is separate from Finance Accepted;
- a workflow must not bypass a controlled transition;
- current product edition, interface and permission behavior have not been verified.
The active Chapter 10 quote baseline includes MER-QUOTE-001 in an approval scenario. This chapter adds separate synthetic practice records rather than silently changing that baseline.
No coding is required. Product configuration requires access to the relevant Zoho CRM design and testing features. Exact current menus, feature availability and permission names must be checked in official product documentation.
2. Lessons
2.1 Which interface should you use?
Several interface types can help a user perform work. They solve different problems.
Interface	Main purpose	Best use	Limitation
Layout	Organise standard record fields and sections	Showing the right fields for a role or record type	May still expose more fields than a task requires
Canvas	Present a customised visual record view	Showing context, summaries and prominent actions	Presentation does not by itself enforce process transitions
Wizard	Lead a user through several screens or steps	Collecting information in a sequence with validation	Too many screens can slow simple work
Kiosk Studio	Provide a focused task-oriented entry point where supported	Helping a user start or complete a specific operation	Availability, supported modules and actions depend on product edition
Guided action	A named action that performs or starts a controlled task	Submit for approval, request correction or submit handoff	Must be connected to permissions and state rules
Layouts
A layout controls how fields and sections are presented on a normal record form. A layout can help you:
- group related fields;
- place important fields near the task they support;
- show or hide fields for a role or record type where supported;
- identify fields that are mandatory;
- make read-only information visible without allowing accidental edits.
A layout should not be used to hide a required business control from a user who needs to understand it. For example, a sales representative may not edit an approval decision, but the decision and its reason should remain visible.
Canvas
Canvas is a customised presentation surface for record information. It can arrange information as cards, panels, summaries or action areas. The exact supported modules and configuration options depend on the product edition.
A Canvas view might show:
- customer identity;
- quote total and discount;
- approval state;
- handoff readiness;
- next allowed action;
- recent activity;
- exception warning.
Canvas improves context and usability. It does not automatically prove that a user is authorised to perform an action. The action must still respect the Blueprint, approval and field permissions.
Wizards
A wizard divides one task into ordered screens. It is useful when the user must:
1. confirm the record;
2. enter or review information;
3. make a decision;
4. submit a controlled action.
A wizard should not divide a short task into unnecessary steps. Each screen should have a clear question or purpose.
Kiosk Studio
Kiosk Studio can be treated as a candidate focused interface for users who need a simple entry point for a particular operation. A kiosk may be useful when a user should begin with a task rather than browse the entire application.
Possible Meridian uses include:
- start a new enquiry;
- capture a service request;
- submit a quote for review;
- record a finance handoff exception.
Before selecting Kiosk Studio, verify:
- which modules it supports;
- whether it can create or update the required record;
- whether it can invoke the required guided action;
- whether role permissions are enforced;
- how it handles validation and errors;
- whether it supports the required accessibility behavior.
These capabilities are not claimed as verified in this chapter.
Check your understanding
A manager wants to see the quote, approval status, customer details and next action on one screen, but the process already has controlled approval transitions. Which interface is useful for the presentation, and what must still control the action?
Answer: Canvas may be useful for the presentation. The Blueprint and approval process must still control whether the manager can approve or move the quote.
2.2 Design a screen around a task
Begin with the task, not the visual design.
Write the task in this form:
As a role, I need to action for record so that outcome.
Example:
As a sales representative, I need to submit a customer-accepted quote for finance so that finance can review a complete handoff.
Then define:
- the user;
- the record;
- information the user must see;
- information the user may edit;
- information the user must not edit;
- decision or transition;
- success evidence;
- exception path;
- recovery action.
Task design worksheet
Design question	Meridian example
User	Sales representative
Record	Accepted quote
Task	Prepare and submit finance handoff
Context needed	Customer, enquiry, quote, approval state, acceptance date
Editable information	Finance-required fields that are still permitted to change
Read-only information	Quote ID, approval outcome, customer acceptance evidence
Controlled action	Submit for Finance
Success evidence	State becomes Ready for Finance
Exception	Currency, customer ID or line items missing
Recovery	Return for Correction with owner and reason
The screen should display enough context to prevent a wrong-record mistake. Showing only a large “Submit” button is not guidance.
Show the wider process context
A narrow task may belong to a wider process. A finance handoff screen should show that:
- the quote was approved where required;
- the customer accepted the quote;
- the duplicate review is complete;
- the handoff fields are complete;
- finance acceptance has not yet occurred.
This prevents a user from interpreting “Ready for Finance” as “Finance Accepted.”
Check your understanding
Why should a guided handoff screen show the approval state even if the sales user cannot edit it?
Answer: The approval state provides context and helps the user understand why an action is or is not available. Read-only information can prevent a user from attempting an invalid transition or believing that an approval has already occurred.
2.3 Layouts and field presentation
Use layouts to make the standard record form match the user’s work.
A useful layout groups fields by decision:
Section	Example fields	Presentation
Record context	Enquiry ID, Quote ID, Customer ID	Read-only and prominent
Customer	Company, contact, email	Read-only after customer acceptance where appropriate
Commercial data	Currency, line items, subtotal, discount, total	Read-only after approval unless correction route is used
Approval	Approval status, approver, decision time, reason	Read-only to requester
Finance handoff	Handoff readiness, finance status, finance reference	Editable only by permitted role
Next action	Owner, task, return reason	Editable according to role
Required fields should match the process
Do not make every field mandatory for every user and every state. A field may be:
- required when submitting for approval;
- required before sending a quote;
- required before finance handoff;
- optional while a record is in Draft;
- required only on a return or rejection path.
Making a field mandatory too early creates workarounds. Making it mandatory too late allows invalid records to progress.
Read-only versus hidden
A field that a user cannot edit may still need to be visible. Hide only information that is irrelevant or inappropriate for that role. Do not hide an approval rejection reason from the requester if the reason is necessary for correction.
Check your understanding
A quote total is locked after approval, but the sales representative needs to correct a missing currency. What is the safest design?
Answer: Do not unlock the approved quote silently. Use a controlled return or correction transition, record the reason and allow the permitted role to correct the data before resubmission.
2.4 Canvas for context and action
Canvas should answer the user’s immediate questions quickly:
- What record am I viewing?
- What has already happened?
- What is waiting?
- What can I do next?
- What will happen if I select the action?
- What information is missing?
Worked Canvas structure
For a Meridian quote, a Canvas view can contain:
1. Identity card
- Customer name;
- contact email;
- Meridian Enquiry ID;
- Meridian Quote ID.
2. Process card
- Current state;
- approval outcome;
- customer acceptance;
- finance handoff status.
3. Commercial card
- currency;
- subtotal;
- discount;
- total;
- line-item count.
4. Readiness card
- customer ID present;
- quote ID present;
- currency present;
- line items present;
- duplicate review complete.
5. Action card
- Submit for Finance;
- Return for Correction;
- View Approval;
- action explanation.
The action card should not display Submit for Finance as available if the Blueprint will deny it. If the product cannot dynamically hide the action, show a clear validation message before the attempt.
Canvas is not a second process engine
Do not build one state model into the Blueprint and another state model into Canvas buttons. A Canvas action should call or respect the controlled transition. Otherwise, users may see one state while the underlying record holds another.
Check your understanding
What is the risk of placing a custom “Finance Accepted” button on a Canvas page for sales users?
Answer: The button may bypass the finance acceptance transition and create false completion evidence. Sales should be able to submit a handoff, not record acceptance that belongs to finance.
2.5 Wizards for ordered work
A wizard is effective when the user must complete a sequence.
For the Meridian handoff task, an appropriate sequence is:
Screen	User question	Main content
1. Confirm record	Am I working on the correct quote?	Customer, enquiry, quote and acceptance
2. Confirm approval	Is the quote authorised to proceed?	Approval outcome, approver and decision time
3. Validate handoff	Is finance receiving complete data?	Customer ID, quote ID, currency, total and line items
4. Submit	Am I ready to send this controlled handoff?	Summary, warning and Submit for Finance action
Each screen should have:
- a meaningful title;
- short instructions;
- visible required fields;
- validation messages near the problem;
- Back and Next behavior where supported;
- a clear way to cancel or save without losing work;
- a final confirmation before an important transition.
Avoid a wizard that hides errors
Do not place all errors on the final screen if the user could have corrected them earlier. Validate at the point where the information is entered and again before the controlled transition.
Resume behavior
Define what happens if the user:
- closes the screen;
- loses connection;
- returns later;
- changes the record in another screen;
- opens the same record in two browser windows.
The user should not be encouraged to submit twice. A successful transition should change the state or display a confirmation that can be verified.
Check your understanding
Why should the wizard validate both on the data-entry screen and before the final transition?
Answer: Early validation helps the user correct a problem while its context is clear. Final validation protects the process from changes made after the earlier screen or by another user.
2.6 Kiosk Studio and guided actions
A guided action is a named action designed around a user decision. Good labels use a verb and describe the result:
- Submit for Approval;
- Return for Correction;
- Send Standard Quote;
- Submit for Finance;
- Accept Finance Handoff.
Avoid labels such as:
- Process;
- Continue;
- Update;
- Complete.
The user should know what will happen before selecting the action.
A guided action should define:
Element	Example
Label	Submit for Finance
User	Sales representative
Preconditions	State Customer Accepted; approval complete; required fields complete
Confirmation	“Submit this accepted quote to finance?”
Transition	Customer Accepted → Ready for Finance
Success evidence	State, timestamp and owner
Failure message	Identify the missing field or permission problem
Recovery	Return for Correction or ask an authorised role
Kiosk Studio may be suitable as a focused launch surface for the action. For example, a finance coordinator might start from a kiosk that asks for a quote ID and opens the permitted review task. That design must still enforce authentication, record access, field permissions and Blueprint transitions.
Do not treat Kiosk Studio as a way to bypass normal role controls. A simpler interface must not mean weaker control.
Check your understanding
Which is the better guided-action label?
A. Continue  
B. Submit for Finance
Answer: B. It tells the user the intended business outcome. The screen should still show the preconditions and expected result.
2.7 Usability and accessibility
A screen is usable when the intended user can complete the task accurately and efficiently. It is accessible when people with different abilities can perceive, understand and operate it.
Apply these principles:
- use plain, consistent labels;
- group related fields;
- place the primary action in a predictable location;
- do not rely on color alone;
- provide text for warnings and success states;
- use sufficient contrast;
- make focus visible;
- support keyboard navigation where the product allows it;
- provide labels for icons;
- keep error messages next to the relevant field;
- do not clear entered data after a validation error;
- avoid unnecessary time limits;
- identify required fields before submission;
- use readable text sizes;
- make the order of fields match the task;
- test with zoom and different screen sizes;
- protect confidential information from being displayed to unauthorised users.
Error message quality
Weak:
Invalid input.
Better:
Currency is required before submitting the finance handoff. Select a permitted currency or choose Return for Correction.
The better message explains:
1. what is wrong;
2. why it matters;
3. what the user can do.
Test with realistic users
Use at least:
- the person who performs the task frequently;
- a person who performs it occasionally;
- a person with the intended restricted role;
- a user who should be denied the action;
- a keyboard-only or zoomed test where possible.
Do not treat the designer’s successful test as proof that the screen is usable.
Check your understanding
Why is a red border around a missing field insufficient as the only error signal?
Answer: Some users may not distinguish the color, and assistive technology may not communicate the meaning. The screen should provide text explaining the missing field and required correction.
2.8 Configuration procedure
This procedure combines a layout, a visual record presentation, a wizard and a guided action. Exact product feature names and navigation must be verified.
Required access
You need suitable permissions for:
- creating or editing layouts;
- arranging fields and sections;
- creating a Canvas or equivalent record presentation;
- creating a wizard or multi-step interface;
- creating a Kiosk Studio entry point if selected;
- configuring or invoking Blueprint transitions;
- editing validation and action labels;
- testing with multiple roles;
- viewing process and action history.
Procedure
 1. Write the task statement.
Expected result: The task names a role, record, action and outcome.
 2. Map the process state.
Expected result: The guided action points to an existing permitted transition rather than a new uncontrolled state.
 3. List read-only and editable information.
Expected result: Users cannot accidentally edit approval or finance-acceptance evidence.
 4. Create or update the layout.
Expected result: The standard record form presents fields in task order.
 5. Create the Canvas presentation if needed.
Expected result: Context, state, readiness and next action are visible together.
 6. Create wizard screens or steps.
Expected result: Each screen has one purpose and validates its own inputs.
 7. Configure the guided action.
Expected result: The action has a clear label, role, preconditions, confirmation and success evidence.
 8. Connect the action to the controlled transition.
Expected result: The action cannot mark a record as complete without satisfying Blueprint and approval requirements.
 9. Test normal, missing-data and denied cases.
Expected result: The user sees a useful correction or permission message rather than an unexplained failure.
10. Test accessibility and usability.
Expected result: The task can be understood and completed without relying on color, hidden instructions or designer knowledge.
11. Activate and document.
Expected result: The screen’s owner, purpose, fields, action, support route and rollback or deactivation method are recorded.
3. Visual explanation
flowchart TD
    A[Open accepted quote] --> B[Canvas summary]
    B --> C[Wizard 1: confirm customer and quote]
    C --> D[Wizard 2: confirm approval and acceptance]
    D --> E[Wizard 3: validate finance fields]
    E --> F{All mandatory information present?}
    F -- No --> G[Show field error or Return for Correction]
    F -- Yes --> H[Wizard 4: confirm submission]
    H --> I{Blueprint transition permitted?}
    I -- No --> J[Show state or permission explanation]
    I -- Yes --> K[Customer Accepted to Ready for Finance]
    K --> L[Show success evidence and next owner]
The sequence separates presentation from control:
- Canvas gives the user context.
- The wizard collects and validates information.
- The guided action asks for confirmation.
- The Blueprint decides whether the transition is permitted.
- The success screen shows evidence rather than merely displaying a green message.
4. Worked case: Meridian guided finance handoff
4.1 Scenario and inputs
This chapter introduces the following synthetic test copy:
Field	Value
Quote ID	MER-QUOTE-101
Enquiry ID	MER-ENQ-101
Customer ID	MER-CUST-101
Contact	Aisha Green
Email	aisha@greenfield.example.com
Current state	Customer Accepted
Approval outcome	Approved
Approval timestamp	2026-10-14 11:30
Customer acceptance	2026-10-15 14:10
Duplicate review	Not a duplicate
Currency	USD
Owner	Jordan
Finance handoff status	Not started
Commercial calculation:
Line item	Quantity	Unit price	Calculation
Office workstation	10	520.00	10 × 520.00
Installation	1	1,200.00	1 × 1,200.00
Support plan	1	400.00	1 × 400.00
Subtotal	 	 	5,200 + 1,200 + 400
Discount at 12%	 	 	6,800 × 0.12
Total	 	 	6,800 - 816
The 12% discount means the quote required approval under the Chapter 10 synthetic rule. The supplied approval outcome is Approved, so the guided screen may support the finance handoff. It must not approve the quote or record finance acceptance.
4.2 Completed screen specification
Screen	Purpose	Read-only information	Editable or confirmable information	Expected result
1. Confirm quote	Prevent wrong-record submission	Customer, enquiry ID, quote ID, current state	User confirms “This is the correct quote”	User proceeds only after confirmation
2. Confirm approval	Show why submission is permitted	Approval result, approver, approval time, acceptance time	User confirms customer acceptance evidence	User sees that approval and acceptance are complete
3. Validate handoff	Check finance requirements	Quote total, line-item summary, duplicate result	Currency, owner and permitted handoff fields	Missing data is shown before submission
4. Submit handoff	Confirm controlled action	Full summary and next owner	Confirmation of Submit for Finance	Blueprint transition is requested
5. Success	Show evidence	New state and timestamp	None	State is Ready for Finance; finance is next owner
4.3 Completed Canvas design
The Canvas summary for MER-QUOTE-101 contains:
CUSTOMER
Greenfield Office Services
aisha@greenfield.example.com
Customer ID: MER-CUST-101

QUOTE
Quote ID: MER-QUOTE-101
Enquiry ID: MER-ENQ-101
Total: USD 5,984.00
Discount: 12%

CONTROL STATUS
Approval: Approved
Customer acceptance: Recorded
Duplicate review: Not a duplicate
Finance handoff: Not started

NEXT PERMITTED ACTION
Submit for Finance

NOT PERMITTED
Approve quote
Record Finance Accepted
Change approved pricing without Return for Correction
The final three lines are important. A guided interface should make the boundary clear.
4.4 Completed guided-action specification
Element	Completed design
Label	Submit for Finance
User	Sales representative
Source state	Customer Accepted
Target state	Ready for Finance
Preconditions	Approval complete, customer acceptance recorded, duplicate review complete, mandatory finance fields complete
Confirmation text	“Submit quote MER-QUOTE-101 to finance for review?”
Success evidence	State, timestamp and finance owner
Failure message	Identify the missing field, state restriction or permission problem
Recovery	Correct permitted fields or choose Return for Correction
Prohibited result	Finance Accepted
4.5 Test cases
These are expected simulated results, not actual product observations.
Test ID	Test event	Expected result
U-01	Jordan opens MER-QUOTE-101	Canvas shows correct customer, quote, approval and handoff context
U-02	Jordan proceeds with all mandatory fields present	Wizard reaches confirmation
U-03	Jordan selects Submit for Finance	Blueprint transition is requested
U-04	Transition succeeds	State becomes Ready for Finance; next owner is finance
U-05	Currency is removed in a test copy	Wizard shows a currency error and prevents submission
U-06	Jordan attempts to approve the quote	Action is hidden or denied; approval remains unchanged
U-07	Finance user opens the record	Finance can review and accept or return according to the controlled process
U-08	Record state changes in another browser window before submission	Final validation prevents stale submission or displays a state-change message
4.6 Mistake and correction
Mistake: The wizard includes a final action called Approve and Send to Finance and makes it available to the sales representative.
Why it is wrong: It combines two controlled decisions and allows a user to bypass the manager approval route.
Correction: Use separate actions:
- Submit for Approval from Draft;
- Send Quote after approval;
- Submit for Finance after customer acceptance;
- Accept Finance Handoff for finance only.
The screen should show the current state and the next permitted action, not every possible action.
5. Try it yourself — guided practice
Learning goal
Create a guided sales task that leads a user through quote submission for approval. Use a layout, a context view, a multi-step wizard and a controlled action.
Required access
You need access to:
- quote or equivalent CRM records;
- layouts and field configuration;
- a Canvas or similar presentation feature, if available;
- wizard or multi-step screen creation, if available;
- Blueprint transition configuration;
- at least two test roles: sales representative and sales manager;
- synthetic notification recipients.
Complete sample input data
Quote ID	Enquiry ID	Customer ID	Contact	Email	Discount	Currency	Line items	State
MER-QUOTE-201	MER-ENQ-201	MER-CUST-201	Nia Patel	nia@atlas.example.com (mailto:nia@atlas.example.com)	12%	USD	Complete	Draft
MER-QUOTE-202	MER-ENQ-202	MER-CUST-202	Leo Martin	leo@quietlake.example.com (mailto:leo@quietlake.example.com)	8%	USD	Complete	Draft
MER-QUOTE-203	MER-ENQ-203	Blank	Sam Rivera	sam@riverbend.example.com (mailto:sam@riverbend.example.com)	15%	USD	Incomplete	Draft
MER-QUOTE-204	MER-ENQ-204	MER-CUST-204	Priya Shah	priya@northstar.example.com (mailto:priya@northstar.example.com)	14%	USD	Complete	Awaiting Approval
Practice rules
- A quote above 10% discount must use Submit for Approval.
- A quote at or below 10% may use Send Standard Quote when complete.
- A quote with missing customer or line items cannot be submitted.
- Sales representatives cannot approve quotes.
- The guided screen must show approval status and customer context.
- The guided screen must not offer Finance Accepted.
- Returned records must show a correction reason and owner.
Guided steps and expected results
Step 1: Create the layout
Create sections for:
1. quote context;
2. customer;
3. commercial information;
4. approval;
5. next action.
Expected result: MER-QUOTE-201 shows the information needed for approval submission without placing unrelated employee or finance fields in the sales form.
Step 2: Create the context view
Create a Canvas or equivalent record presentation showing:
- quote ID;
- customer;
- discount;
- total;
- current state;
- approval state;
- next permitted action.
Expected result: A user can identify the record and action without opening unrelated sections.
Step 3: Create the wizard
Use these screens:
Screen	Purpose
1. Confirm customer	Check customer and quote identity
2. Review commercial data	Confirm discount, currency, line items and total
3. Review approval route	Explain whether approval is required
4. Submit	Request the permitted transition
Expected result: MER-QUOTE-201 is routed to approval; MER-QUOTE-202 is routed to the standard send path.
Step 4: Configure actions
Create:
- Submit for Approval;
- Send Standard Quote;
- Return for Correction.
Expected result: Sales cannot see or execute Approve Quote.
Step 5: Test missing data
Open MER-QUOTE-203.
Expected result: The wizard identifies the missing customer and incomplete line items before submission.
Step 6: Test pending approval
Open MER-QUOTE-204 as Jordan.
Expected result: The screen shows that approval is pending and does not offer an approval or send action to Jordan.
Step 7: Test permission
Open MER-QUOTE-201 as a sales manager and as a sales representative.
Expected result: The manager can review or approve according to the approval process. The sales representative can submit but cannot approve.
Step 8: Test state change recovery
Open a quote in two test sessions. Change its state in the first session, then attempt the old action in the second.
Expected result: The second action is denied or revalidated. The user receives an explanation rather than creating a duplicate transition.
Final artifact
Your practice submission should contain:
Artifact	Minimum content
Screen map	Screen name, purpose, user and expected result
Layout design	Sections, fields, read-only values and required fields
Canvas or context design	Record summary, state, readiness and permitted action
Guided-action register	Label, source state, target state, role and error route
Test matrix	Normal, missing-data, approval-pending, permission and stale-state tests
User instruction	Five to eight steps for the sales representative
Safe cleanup
Use synthetic records and recipients. Deactivate practice screens or actions after recording the test results. Do not remove shared layouts or production transitions without confirming ownership.
Offline alternative
You can draw the screen map and create a spreadsheet-based wizard script. This can test sequence, labels and missing-data logic, but it cannot demonstrate actual Canvas rendering, product permissions, keyboard behavior or Blueprint enforcement.
6. Independent challenge
Guided service-triage task
Design a guided screen for a service coordinator who receives an installation or support issue. The detailed Desk configuration belongs to a later chapter, so this challenge focuses on screen design, guided actions, state control and usability.
Scenario rules
- The service coordinator must identify the customer and related quote or order.
- A service case cannot move to Ready for Assignment without an issue summary, category, severity and preferred contact method.
- High-severity cases require impact information and an escalation owner.
- A service coordinator may submit a case but cannot close it.
- A customer-facing action must not expose internal escalation notes.
- A case returned for missing information must show the missing field and correction owner.
- The screen must support keyboard navigation and must not use color as the only indicator.
- An unauthorised user must not see confidential internal notes.
Complete input data
Case ID	Customer ID	Related quote	Contact	Email	Category	Severity	Issue summary	Preferred contact
MER-SVC-301	MER-CUST-301	MER-QUOTE-301	Elena Cruz	elena@oakridge.example.com (mailto:elena@oakridge.example.com)	Installation	Medium	Installer did not leave setup guide	Email
MER-SVC-302	MER-CUST-302	MER-QUOTE-302	Daniel Wu	daniel@brightline.example.com (mailto:daniel@brightline.example.com)	Equipment failure	High	Main device stops after startup	Phone
MER-SVC-303	Blank	MER-QUOTE-303	Noor Ali	noor@westfield.example.com (mailto:noor@westfield.example.com)	Support	Low	User cannot find login instructions	Email
MER-SVC-304	MER-CUST-304	MER-QUOTE-304	Grace Kim	grace@harborview.example.com (mailto:grace@harborview.example.com)	Installation	Medium	Customer requests a revised visit time	Phone
Deliverables
Create:
1. a layout or Canvas context design;
2. a three- or four-screen wizard;
3. guided actions for Submit for Assignment and Return for Correction;
4. high-severity validation;
5. an access distinction between service coordinator and service manager;
6. an accessibility checklist;
7. test results for normal, missing-customer, high-severity, returned and permission cases.
Success criteria
Your design should:
- allow MER-SVC-301 to proceed when required information is complete;
- prevent MER-SVC-302 from proceeding until impact and escalation owner are supplied;
- return MER-SVC-303 for missing customer information;
- show the correction route for MER-SVC-304;
- prevent a service coordinator from closing a case;
- keep internal notes hidden from an unauthorised user;
- explain all errors using text and not color alone.
7. Common problems and recovery
Symptom	Diagnosis	Correction	Verification
The screen displays every available field	The design began with the data model rather than the task	Remove irrelevant fields and group the remainder by decision	A user can describe the task without opening unrelated sections
A guided action bypasses approval	The action writes a state directly or uses the wrong transition	Connect it to the controlled transition and enforce approval prerequisites	Attempt the action before and after approval
A user cannot understand why an action is unavailable	The state, missing field or permission reason is hidden	Show current state, required information and a useful message	Test with a denied user
A wizard loses entered data after an error	Validation is late or recovery behavior is undefined	Validate earlier and preserve entered values where supported	Submit with one missing field
The screen relies on color to indicate error	Accessibility was not considered	Add text, labels, icons with text and visible focus	Test grayscale, zoom and keyboard use
A Canvas button records Finance Accepted	Presentation has become a second process engine	Remove the button or connect it to the finance-only transition	Test as sales and finance roles
A returned record cannot be corrected	No correction owner or editable route exists	Add Return for Correction with owner and reason	Return and resubmit a synthetic record
A user opens the wrong customer record	Context is hidden or identifiers are too small	Display customer, enquiry and quote IDs prominently	Test two similar customer names
A user can edit an approved quote price	Field permissions and state rules are not aligned	Lock the field after approval or require a controlled correction route	Edit as sales representative after approval
A screen works for the designer but not for keyboard use	Focus order or action labels are unclear	Test keyboard navigation and make focus visible	Complete the task without a mouse
A stale screen submits an old state	Final validation is missing	Recheck state and permissions immediately before transition	Change state in a second test session
Kiosk users can access too much data	The focused interface was given excessive record scope	Restrict records and fields according to role	Test with a limited user
A screen hides an approval rejection reason	The design prioritised simplicity over recovery	Display the reason and next permitted action	Reject a test quote and correct it
Product capability is assumed from a feature name	Current edition or module support was not confirmed	Verify supported feature, module and permission before implementation	Record a capability check
8. Check your understanding
 1. What is the difference between a layout and a Canvas presentation?
 2. When is a wizard more useful than a standard record form?
 3. Why must a guided action respect the Blueprint?
 4. What information should be read-only on a finance handoff screen?
 5. Why should a rejected quote show a reason?
 6. What is the purpose of a final validation before a transition?
 7. Which Meridian screen should show approval status but not allow the sales user to change it?
 8. What is the risk of using Complete as a generic action label?
 9. How should a high-severity service case differ from a low-severity case?
10. What should happen when a user without permission selects a guided action?
11. Why should internal notes be separated from customer-facing information?
12. Which record in the guided practice cannot be submitted for approval, and why?
13. What does a successful finance handoff screen prove, and what does it not prove?
14. Name two accessibility checks for a guided screen.
15. What evidence should be saved after testing a screen?
9. Solutions and explanations
9.1 Answers to the checks
 1. A layout organises standard fields and sections. A Canvas presentation creates a customised view that emphasises context, summaries and actions.
 2. A wizard is useful when the user must complete an ordered task with validation or different screens for different decisions.
 3. The Blueprint controls authorised state movement. If the action bypasses it, the record may appear complete without satisfying approval, permissions or mandatory information.
 4. Approval outcome, approver, approval timestamp, customer acceptance and approved commercial values should generally be read-only to a sales user after approval. Exact permissions depend on the design.
 5. A rejection reason tells the requester why the quote cannot proceed and supports an appropriate correction or closure path.
 6. It protects against missing data, permission changes or a state change that occurred after the user began the task.
 7. The approval-review screen should show the approval status as read-only to the sales user.
 8. Complete does not explain what will happen. The user may not know whether it submits, closes, approves or sends the record.
 9. A high-severity case should require impact information and an escalation owner before it can be submitted. A low-severity case may not require those additional fields.
10. The action should be denied or unavailable, with a message explaining the required permission or role.
11. Internal notes may contain operational or confidential information that should not be exposed to customers or unauthorised roles.
12. MER-QUOTE-203 cannot be submitted because the customer ID and line items are incomplete.
13. It proves that the controlled transition to Ready for Finance succeeded. It does not prove that finance accepted or processed the handoff.
14. Examples include keyboard navigation, visible focus, text-based error messages, sufficient contrast, non-color indicators and readable labels.
15. Save the test record, user role, input values, expected result, actual observation, timestamp, error message and recovery action.
9.2 Guided practice sample solution
Screen map
Screen	User	Purpose	Expected result
Confirm customer	Sales representative	Check quote, customer and enquiry IDs	Correct record confirmed
Review commercial data	Sales representative	Check discount, currency, line items and total	Quote is classified as approval-required or standard
Review approval route	Sales representative	Explain why approval is or is not required	Correct next action is shown
Submit	Sales representative	Confirm and invoke the permitted transition	Quote enters Awaiting Approval or Sent
Correction	Sales representative	Identify missing or invalid information	Record remains Draft with owner and correction reason
Expected routes
Quote	Expected route	Explanation
MER-QUOTE-201	Draft → Awaiting Approval	Discount is 12% and required data is complete
MER-QUOTE-202	Draft → Sent	Discount is 8% and required data is complete
MER-QUOTE-203	Remains Draft	Customer and line items are missing
MER-QUOTE-204	Remains Awaiting Approval	Approval is pending; sales cannot send or approve
Guided-action register
Action	User	Source state	Target state	Preconditions
Submit for Approval	Sales representative	Draft	Awaiting Approval	Discount greater than 10%; quote complete
Send Standard Quote	Sales representative	Draft	Sent	Discount 10% or less; quote complete
Approve Quote	Sales manager	Awaiting Approval	Approved	Authorised approver; decision recorded
Return for Correction	Sales manager	Awaiting Approval	Returned	Reason and correction owner
Submit for Finance	Sales representative	Customer Accepted	Ready for Finance	Approval, acceptance and handoff data complete
Missing-data result
For MER-QUOTE-203, the screen should identify:
Customer ID is required.
Line items are incomplete.
Approval submission is unavailable.
Next action: provide missing information or request correction support.
The message is better than a generic “Cannot continue” because it gives the user a recovery path.
Permission result
Jordan may submit MER-QUOTE-201 for approval but cannot approve it. The sales manager can review the approval. The screen should show the relevant action to each role or deny the action with a clear explanation.
9.3 Independent challenge sample solution
Service screen map
Screen	Purpose	Required content
1. Identify case	Confirm customer and related quote	Customer ID, quote ID, contact, email
2. Describe issue	Capture the problem	Category, severity, summary, preferred contact
3. Assess impact	Apply severity-specific rules	Impact and escalation owner for High
4. Submit or return	Choose the permitted action	Submit for Assignment or Return for Correction
Expected results
Case	Expected route	Explanation
MER-SVC-301	Submit for Assignment	Customer, category, severity, summary, contact method and impact are present
MER-SVC-302	Correction required	High severity requires impact and escalation owner
MER-SVC-303	Correction required	Customer ID is missing
MER-SVC-304	Return for Correction	The case is already returned and should display the correction route
Guided actions
Action	User	Preconditions	Result
Submit for Assignment	Service coordinator	Customer, category, severity, summary and preferred contact present; high severity also has impact and escalation owner	State becomes Ready for Assignment
Return for Correction	Service manager or authorised coordinator	Missing information or invalid state	State remains or becomes Returned; reason and owner required
Close Case	Service manager or authorised closing role	Resolution note and required closure evidence	Service coordinator cannot perform this action
Access design
Role	Customer and contact	Internal notes	Submit case	Close case
Service coordinator	View and edit permitted fields	No access or limited access	Yes	No
Service manager	View and edit	View and edit	Yes	Yes
Customer-facing user	View permitted customer information	No access	No	No
System administrator	Administrative access as assigned	Administrative access as assigned	Administrative access as assigned	Administrative access as assigned
Accessibility checklist
The completed design should:
- label every field;
- provide text for high-severity warnings;
- show focus when moving through the wizard with a keyboard;
- avoid using red alone to identify missing information;
- keep action labels descriptive;
- preserve entered data when validation fails;
- use readable contrast and text size;
- keep internal notes out of the customer-facing screen.
Permission and recovery tests
For a service coordinator attempting to close MER-SVC-301, the expected result is denial with an explanation that closure requires an authorised role.
For MER-SVC-302, the user must supply impact and escalation owner. If the action fails because the case state changed while the screen was open, the user should reload the record, inspect its current state and continue from the permitted action. The user should not submit repeatedly.
10. Chapter recap and next step
A guided screen should make the correct task easier without weakening process control.
You should now be able to:
- choose between a layout, Canvas, wizard, Kiosk Studio entry point and guided action;
- design a screen around a role, task, record and outcome;
- distinguish editable, read-only and confidential information;
- create an ordered wizard with meaningful screens;
- connect a guided action to a controlled transition;
- keep approvals and finance acceptance outside the authority of the wrong role;
- provide useful validation and recovery messages;
- test missing data, permission denial and stale-record behavior;
- apply keyboard, contrast, focus, labeling and non-color accessibility checks;
- document expected and actual screen-test results.
For the Meridian Supply project, this chapter produces:
C01_CH11_Meridian_Guided_Finance_Handoff_Screen
C01_CH11_Meridian_Layout_and_Canvas_Design
C01_CH11_Meridian_Wizard_and_Guided_Action_Register
C01_CH11_Meridian_Usability_Accessibility_and_Test_Evidence
The next chapter examines products, pricing and commercial records. The guided sales task from this chapter provides the user experience; the next chapter supplies deeper rules for products, price books, quote lines, discounts and commercial approvals.
11. Glossary and further reading
Glossary
Term	Definition
Accessibility	Designing an interface so people with different abilities can perceive, understand and operate it
Canvas	A customised visual presentation of record information and actions where supported
Guided action	A named, task-specific action with defined preconditions, outcome and recovery
Kiosk Studio	A focused interface capability for task-oriented interaction where supported
Layout	Arrangement of fields and sections on a standard record form
Read-only field	Information a user can see but cannot edit in the current context
Screen flow	Ordered sequence of screens used to complete a task
Usability	How effectively, efficiently and clearly a user can complete a task
Validation	Check that required information and conditions are satisfied
Wizard	A multi-step interface that guides a user through an ordered task
Further reading
Check the current edition, product permissions and supported modules before implementing these interfaces:
- Zoho CRM Help (https://help.zoho.com/portal/en/kb/crm)
- Zoho CRM customization help (https://help.zoho.com/portal/en/kb/crm/customize-crm-account)
- Zoho CRM automation help (https://help.zoho.com/portal/en/kb/crm/automate-business-processes)
- Zoho CRM developer documentation (https://www.zoho.com/crm/developer/docs/)
- Zoho CommandCenter information (https://www.zoho.com/commandcenter/)
This chapter has not verified current Canvas, wizard, Kiosk Studio, layout, permission or accessibility behavior in a live Zoho environment. The design and test results are expected learning outputs, not product execution observations.
continuity:
  previous_continuity:
    supplied: "C01-CH10"
    source_artifacts:
      - "C01_CH10_Meridian_Controlled_Process_State_Model"
      - "C01_CH10_Meridian_Transition_and_Approval_Register"
      - "C01_CH10_Meridian_Escalation_and_Exception_Matrix"
      - "C01_CH10_Meridian_Blueprint_Test_Evidence"
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
    added_for_guided_screen_practice:
      - MER-CUST-101
      - MER-QUOTE-201
      - MER-QUOTE-202
      - MER-QUOTE-203
      - MER-QUOTE-204
      - MER-SVC-301
      - MER-SVC-302
      - MER-SVC-303
      - MER-SVC-304
  case_decisions:
    - "A guided screen assists a task but does not replace the Blueprint, approval or permission controls."
    - "The finance handoff action is Submit for Finance; it must not record Finance Accepted."
    - "Approved commercial values are read-only to the sales user unless a controlled correction route is used."
    - "A wizard should validate information during entry and again before the controlled transition."
    - "Canvas is used for context and presentation, not as a second process engine."
    - "Kiosk Studio scenarios and supported modules require current edition and permission verification."
    - "A service coordinator may submit a service case but may not close it in the independent challenge."
  artifacts:
    - "C01_CH11_Meridian_Guided_Finance_Handoff_Screen"
    - "C01_CH11_Meridian_Layout_and_Canvas_Design"
    - "C01_CH11_Meridian_Wizard_and_Guided_Action_Register"
    - "C01_CH11_Meridian_Usability_Accessibility_and_Test_Evidence"
  open_case_assumptions_next_chapter:
    - "The exact current Zoho CRM support for Canvas, Wizards, Kiosk Studio and guided actions has not been verified."
    - "The next chapter should use the guided sales task while defining products, price books, quote lines, discounts and commercial approval controls."
    - "Any screen action that changes a commercial record must continue to respect the controlled state and approval rules."
    - "Accessibility and usability results must be confirmed with actual users and the selected product interface."
END OF C01-CH11
