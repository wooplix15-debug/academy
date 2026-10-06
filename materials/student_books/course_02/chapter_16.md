# CRM Server-Side Customisation

## What you will learn

By the end of this chapter, you will be able to:
- Choose the correct CRM Function category for a business requirement.
- Distinguish Workflow, Blueprint, Approval, Button, Schedule, Validation Rule, Related List, Signal, and Standalone contexts.
- Map Deluge arguments from CRM fields and understand how other runtimes receive trigger context.
- Use CRM v8 Deluge tasks to read, create, update, search, and upsert records.
- Design business rules that fail safely and avoid recursive updates.
- Separate blocking validation from asynchronous automation.
- Use custom buttons for short, user-visible actions.
- Use schedules for bounded batch processing.
- Use workflow and Blueprint Functions for side effects without assuming rollback.
- Understand CRM Function permissions, admin-level execution, connections, and caller identity.
- Apply current Function execution time, response, line, credit, and task limits.
- Test and recover server-side customizations without inventing live tenant outcomes.
This chapter uses an isolated CRM Account marker for learning. It does not alter the established Nova Creator lifecycle or implement the future CRM service-summary module.
## Lessons

### Lesson 1 — Choose the correct Function category

A CRM Function is server-side code associated with a trigger. The category determines where the Function can run, how it receives input, and what it returns.
Category	Typical trigger	Return behavior
Automation	Workflow, Blueprint, Approval, Command Center	Usually void; side effect runs asynchronously
Button	Custom button	String displayed in a CRM modal
Schedule	Time-based schedule	void; performs batch work
Validation Rule	Record save	Map used by validation context
Related List	Related-list rendering	XML or runtime-specific related-list response
Signals	Inbound external event that raises a CRM Signal	Signal-oriented response
Standalone	Other Functions, REST endpoint, ZDK	String or HTTP response
Serverless REST	Standalone Function exposed through REST	Controlled HTTP response
Choose the category from the execution contract rather than the implementation language.
Use Automation when the action should happen after a CRM event
Examples:
- A Deal reaches a target stage.
- A record is created or edited.
- An Approval is accepted.
- A Blueprint transition completes.
Automation Functions run asynchronously. The CRM record save is not held open waiting for the Function to return.
This makes Automation useful for:
- Notifications.
- Related-record updates.
- External synchronization.
- Post-save calculations.
- Audit stamps.
It also means Automation is the wrong place for a rule that must block the save. Use a Validation Rule or Blueprint transition criteria for that requirement.
Use a Button when a user requests a short action
A Button Function should:
- Complete quickly.
- Validate the current record again.
- Return a concise message.
- Avoid long-running loops.
- Avoid relying only on button visibility for authorization.
Button Functions can appear on:
- Record detail pages.
- List views.
- Create or edit pages.
The button can be limited to selected profiles. That improves the user interface, but the Function should still validate its target and caller-sensitive conditions.
Use a Schedule for batch work
A Schedule Function runs independently of a user action or record event.
Examples:
- Find stale training records.
- Reconcile a bounded set of integration results.
- Produce a daily exception report.
- Process a limited batch of records.
A Schedule Function normally has no record-trigger arguments. It must query CRM for its work.
Do not use a Button Function to process thousands of records. Do not use a Schedule Function when a user needs an immediate response.
Use a Validation Rule when the record must not be saved
Validation Rule Functions are intended to execute during record save and return a validation result. The exact map shape should be confirmed from the Function editor’s generated skeleton for the tenant.
Use this category for rules such as:
- A required pair of fields must be present together.
- A value must be within a business range.
- A transition requires a supporting field.
- A record cannot be saved when two fields conflict.
Do not use a post-save Workflow Function as a substitute for blocking validation. A failed asynchronous Function does not undo the original record save.
Use Standalone for reusable or HTTP-invoked logic
A Standalone Function can be:
- Called by another Function.
- Invoked by a Widget or Client Script through ZDK.
- Exposed as a REST endpoint.
- Used as a reusable service boundary.
A Standalone Function exposed through HTTP must validate its request, authentication context, input fields, and response contract. Its admin-level CRM access makes output filtering especially important.
Lesson check
1. Which category is appropriate for a rule that must block a save?
2. Which category returns a message in a CRM modal?
3. Why should large batches use a Schedule rather than a Button?
4. Does a Workflow Function return a message to the user who saved the record?
5. What category is normally used for a reusable REST endpoint?
### Lesson 2 — Pass arguments and understand execution identity

Deluge argument mapping
For Deluge Functions, declare arguments in the Function signature or Arguments panel. Then map them to CRM merge variables when associating the Function.
Example Automation signature:
void automation.nova_ch16_automation_stamp(
	string account_id,
	string account_name,
	string description
)
{
	// implementation
}
A Workflow Rule can map:
Function argument	CRM merge variable
account_id	${Accounts.Account Id}
account_name	${Accounts.Account Name}
description	${Accounts.Description}
Workflow values are commonly passed as strings. Convert them only at the point where the CRM task requires a numeric ID.
For example:
account_id_long = account_id.toLong();
Use this conversion only inside the Deluge CRM task boundary. External JavaScript, Node.js, and JSON processing must preserve CRM IDs as exact opaque strings.
Other runtimes
Java, Node.js, and Python Functions use the basicIO context. The trigger context is provided as structured input rather than requiring the same manual merge-variable mapping used by Deluge.
For a multi-language Function, inspect the runtime-specific input contract before assuming that a Deluge argument name exists.
Direct CRM access and Connections
CRM Functions have two different access contexts:
1. Direct CRM operations
- Examples: zoho.crm.v8.getRecordById, zoho.crm.v8.updateRecord.
- Run with the Function’s system-level CRM execution access.
2. Operations made through a Connection
- Use the authorization and scopes of the Connection owner.
- May be more restricted than the Function’s direct CRM access.
This distinction matters:
Function execution permission
  is not the same as
Connection authorization
  is not the same as
business authorization
A Function can have the technical ability to update a record while the business rule still requires a marker check, role check, or ownership check.
Execution identity
Current CRM Function documentation exposes runtime values such as:
- zoho.loginuser: email of the user who triggered the Function.
- zoho.loginuserid: CRM user record ID of the triggering user.
- zoho.adminuser: email of the CRM super administrator.
- zoho.adminuserid: CRM super administrator record ID.
Do not use the administrator identity as the business owner of a record. The Function may execute with administrative access, but the event actor and business owner remain separate facts.
Example safe diagnostic:
info "code=STARTED";
info "actor_present=" + (zoho.loginuser != null);
Do not log the actual email, access token, Authorization header, or complete record map unless the evidence policy explicitly permits the field.
Caller checks
Button visibility is not sufficient for sensitive operations.
A Function that performs a sensitive action should independently check:
- Target marker or target ID.
- Allowed module.
- Current record state.
- Required ownership or role mapping.
- Whether the action is a replay.
- Whether the action is permitted in the current environment.
If the caller mapping is unavailable, fail closed.
Lesson check
1. Who maps Deluge arguments for a Workflow Function?
2. Why are CRM IDs passed as strings until the CRM task boundary?
3. Does a Connection necessarily have the same access as the Function?
4. Is the CRM administrator automatically the business owner?
5. Why should a Function validate a caller even when a button is profile-restricted?
### Lesson 3 — Implement business rules without recursion or accidental rollback assumptions

The Function should make business rules explicit.
A reliable server-side operation normally follows this pattern:
validate input
  -> re-read authoritative target
  -> verify identity and state
  -> apply one bounded change
  -> classify result
  -> log safe evidence
Re-read before sensitive updates
Arguments passed by a Workflow or Button can be stale by the time the Function executes.
For a sensitive update:
1. Receive the record ID.
2. Read the record by ID.
3. Confirm the marker, module, and expected fields.
4. Apply only the intended field changes.
5. Read back if the result matters.
Do not trust a display name or user-supplied ID without re-reading the target.
Avoid workflow recursion
If a Workflow Function updates the same module, the update may cause another workflow evaluation.
Use several defenses:
- Narrow workflow criteria.
- A processed marker or state transition.
- A Function guard that returns when the marker already exists.
- A maximum processing scope.
- Separate input and output fields when possible.
- An explicit recursion test.
Example:
Workflow condition:
  Account_Name == NOVCH16LAB901A
  AND Description does not contain |CH16_PROCESSED|

Function:
  Re-read Account
  If Description contains |CH16_PROCESSED|, stop
  Update Description with |CH16_PROCESSED|
The condition and the code guard are both required. Do not rely on only one layer.
Do not assume coordinated rollback
A CRM Automation Function can:
- Update another CRM record.
- Call an external API.
- Send an email.
- Create a related record.
If a later operation fails, earlier operations are not automatically rolled back across all systems.
For example:
1. Function updates CRM Account.
2. Function calls external service.
3. External service fails.
The Account update does not automatically revert.
Use a deliberate compensation or reconciliation design when required. Do not report “transaction rolled back” unless the specific transaction contract proves it.
Deluge CRM tasks
The current CRM Deluge guide documents v8 tasks such as:
record = zoho.crm.v8.getRecordById("Accounts", account_id_long);
response = zoho.crm.v8.updateRecord(
	"Accounts",
	account_id_long,
	update_map
);
records = zoho.crm.v8.searchRecords(
	"Accounts",
	"(Account_Name:equals:NOVCH16LAB901A)"
);
response = zoho.crm.v8.upsert(
	"Accounts",
	record_map,
	options_map
);
Use Field API names rather than display labels.
A CRM Function can use direct v8 tasks without a Connection when operating inside CRM. Use a Connection when calling another service or when you intentionally require explicit scope control.
Safe error handling
Use try and catch around operations that can fail:
try
{
	account = zoho.crm.v8.getRecordById("Accounts", account_id_long);
}
catch (e)
{
	info "code=READ_FAILED";
	return;
}
Avoid:
info e;
in a production Function if the exception may include a URL, request body, token, or confidential response.
Log:
- Safe result code.
- Function name or version.
- Target module.
- Target ID presence.
- Attempt number.
- Actual actor presence.
- Timestamp.
- Error class or provider code after redaction.
Lesson check
1. Why should a Function re-read a record before updating it?
2. What prevents a same-module Workflow from recursively firing?
3. Does a failed external call roll back an earlier CRM update?
4. Why should CRM Field API names be used in code?
5. What information is safe to include in a failure log?
### Lesson 4 — Respect execution limits and choose the right trigger

Function limits affect architecture.
The current Function platform documentation lists these limits:
Limit	Current documented value
Response size	10 MB
Executed lines per invocation	200,000
Button timeout	10 seconds
Related List timeout	10 seconds
Validation Rule timeout	10 seconds
REST Function timeout	10 seconds
Automation timeout	30 seconds
Schedule timeout	15 minutes
Deluge execution credit	1 credit per execution
sendMail daily quota	50,000 per organization
SMS daily quota	1,000,000 per organization
invokeurl daily quota	5,000,000 per organization
These are current documentation values, not a substitute for checking the tenant’s current plan and usage.
Design within the timeout
A Button Function should not:
- Iterate through thousands of records.
- Make many external calls.
- Wait for a long-running Bulk API job.
- Send a large batch of emails.
- Run reconciliation across an entire module.
A Button Function can:
- Validate one record.
- Read one target.
- Make one bounded update.
- Return a concise result.
An Automation Function has a longer timeout but is still not a queue worker. Use it for one event and bounded side effects.
A Schedule Function is appropriate for:
- Paginated reconciliation.
- Stale-record scans.
- Bounded cleanup.
- Retry processing.
Even a Schedule Function needs a page limit and a resume checkpoint.
Credits
Every Deluge Function execution consumes a credit. Java, Node.js, and Python Functions use execution-time-based credit accounting in the current documentation.
A Workflow rule that fires for 1,000 records can consume 1,000 Function executions. A Function that is called by another Function creates additional execution usage.
Before enabling a broad Workflow:
1. Estimate record volume.
2. Estimate executions per record.
3. Estimate retries.
4. Estimate scheduled runs.
5. Confirm available credits.
6. Test with a bounded marker.
Function revisions
The current documentation describes revision history. Deluge saves update the live Function immediately; Deluge does not use the same draft/deploy workflow as Java, Node.js, or Python Functions.
Therefore:
- Make a safe revision before changing an associated Function.
- Record the revision or change description.
- Test the guard path before the write path.
- Use Sandbox for Functions that can modify production records.
- Review associations before deleting a Function.
Lesson check
1. Which category has the longest documented timeout?
2. Why is a Button Function unsuitable for a large reconciliation?
3. What happens to credit usage when a Workflow triggers once per record?
4. Does saving a Deluge Function necessarily create a production-safe draft?
5. Why should Functions be tested in Sandbox?
### Lesson 5 — Associate Workflows, Buttons, Blueprints, and Schedules

Workflow Rule
Use a Workflow Function for asynchronous post-save work.
Association pattern:
Setup
  -> Automation
  -> Workflow Rules
  -> module and trigger condition
  -> Instant Action
  -> Function
  -> argument mapping
The Workflow must be active before it can run.
For Nova-related CRM training, an isolated rule can use:
Module: Accounts
Condition:
  Account_Name equals NOVCH16LAB901A
  AND Description does not contain |CH16_PROCESSED|
Action:
  nova_ch16_automation_stamp
This rule is a lab-only rule. It is not a production Nova lifecycle rule.
Button
Association pattern:
Setup
  -> Customization
  -> Modules and Fields
  -> Accounts
  -> Links and Buttons
  -> Create New Button
  -> Writing a Function
Configure:
- Button location.
- Function.
- Argument mappings.
- Profiles allowed to view the button.
Use a Button Function for the isolated preview:
Button label: CH16 Scratch Preview
Module: Accounts
Visible to: administrator or controlled training profile
Function: nova_ch16_preview
Action: read-only
The function should return a string such as:
READY: NOVCH16LAB901A; CRM record verified; no write performed.
or:
BLOCKED: target marker mismatch; no write performed.
Blueprint
Blueprint Functions are attached to a transition.
Use a Blueprint when the operation is a process transition:
Assigned -> In Progress
In Progress -> Completed
Do not use a Blueprint Function as the only completion validator if the transition must be blocked. Add transition criteria or validation rules for blocking conditions.
The Function can perform a side effect after the transition, but a Function failure must not be described as a coordinated rollback of the transition and external systems.
Approval
Approval Functions can run on approval lifecycle actions, such as submit, approve, or reject. Use them for:
- Notifications.
- Escalation.
- Related-record updates.
- Audit actions.
Do not make a failing notification Function change an approval decision unless the approval process explicitly defines that behavior.
Schedule
Association pattern:
Setup
  -> Developer Hub
  -> Functions
  -> Schedule category Function
  -> Schedules
  -> frequency, start time, optional end time
A Schedule Function has no natural record-trigger argument. It must query a bounded set.
Use:
marker prefix: NOVCH16
page: 1
maximum records: 200
for the training reconciliation. Stop after the bounded page and report whether additional records remain.
## Visual explanation

flowchart TD
    A[CRM requirement] --> B{Must block save?}
    B -->|Yes| C[Validation Rule or Blueprint criteria]
    B -->|No| D{User clicks action?}
    D -->|Yes| E[Button Function]
    D -->|No| F{Record event?}
    F -->|Yes| G[Automation Function]
    F -->|No| H{Time based?}
    H -->|Yes| I[Schedule Function]
    H -->|No| J[Standalone Function]
    G --> K[CRM direct task or Connection]
    E --> K
    I --> K
    J --> K
Plain-text explanation:
- Blocking business rules belong before or during save.
- User-requested short actions belong in Buttons.
- Post-save reactions belong in Automation.
- Batch and reconciliation work belongs in Schedules.
- Reusable or externally invoked logic belongs in Standalone Functions.
- Every category still needs input validation, permission design, safe logging, and bounded execution.
## Worked case

CH16 isolated CRM training operation
Create one disposable CRM Account:
Account_Name: NOVCH16LAB901A
Description: CH16 scratch account
The actual CRM record ID is generated by the training organization.
Record it as:
artifact,module,marker,record_id,organization,observed
CH16 scratch Account,Accounts,NOVCH16LAB901A,<captured ID>,training CRM,NOT_YET_RUN
Do not use a production customer Account.
Function 1 — Button preview
Host: CRM Button Function
Function: nova_ch16_preview
Input: account_id string mapped from the Account record ID
Connection: none for direct CRM read
Supported task: Verify one disposable Account and return a safe message
Return contract: String shown in a CRM modal
Side effects: none
string button.nova_ch16_preview(string account_id)
{
	if(account_id == null || account_id.trim() == "")
	{
		return "BLOCKED: account ID missing; no write performed.";
	}

	try
	{
		account = zoho.crm.v8.getRecordById(
			"Accounts",
			account_id.toLong()
		);

		if(account == null)
		{
			return "BLOCKED: Account not found; no write performed.";
		}

		account_name = account.get("Account_Name");

		if(account_name != "NOVCH16LAB901A")
		{
			return "BLOCKED: scratch marker mismatch; no write performed.";
		}

		return "READY: NOVCH16LAB901A verified; no write performed.";
	}
	catch (e)
	{
		info "code=PREVIEW_READ_FAILED";
		return "BLOCKED: read failed; inspect Function logs.";
	}
}
The Function does not return the Account contents. It returns only a safe status.
Expected result:
READY: NOVCH16LAB901A verified; no write performed.
This is an expected result. It becomes an actual result only after the learner runs it in the tenant.
Function 2 — Automation stamp
Host: CRM Automation Function
Function: nova_ch16_automation_stamp
Trigger: Isolated Accounts Workflow Rule
Inputs: Account ID, Account Name, Description
Connection: none for direct CRM operation
Supported task: Add one idempotent training marker to the disposable Account Description
Return contract: void
Side effects: One guarded update to the scratch Account
void automation.nova_ch16_automation_stamp(
	string account_id,
	string account_name,
	string description
)
{
	if(account_id == null || account_id.trim() == "")
	{
		info "code=BLOCKED_ID_MISSING";
		return;
	}

	if(account_name != "NOVCH16LAB901A")
	{
		info "code=BLOCKED_MARKER_MISMATCH";
		return;
	}

	try
	{
		account = zoho.crm.v8.getRecordById(
			"Accounts",
			account_id.toLong()
		);

		if(account == null)
		{
			info "code=BLOCKED_ACCOUNT_NOT_FOUND";
			return;
		}

		actual_name = account.get("Account_Name");
		actual_description = account.get("Description");

		if(actual_name != "NOVCH16LAB901A")
		{
			info "code=BLOCKED_RE_READ_MARKER_MISMATCH";
			return;
		}

		if(actual_description == null)
		{
			actual_description = "";
		}

		if(actual_description.toString().contains("|CH16_PROCESSED|"))
		{
			info "code=ALREADY_PROCESSED";
			return;
		}

		update_map = Map();
		update_map.put(
			"Description",
			"CH16|CH16_PROCESSED|Account=NOVCH16LAB901A"
		);

		update_response = zoho.crm.v8.updateRecord(
			"Accounts",
			account_id.toLong(),
			update_map
		);

		response_code = update_response.get("code");

		if(response_code == null || response_code == "SUCCESS")
		{
			info "code=UPDATED";
		}
		else
		{
			info "code=UPDATE_REJECTED";
		}
	}
	catch (e)
	{
		info "code=UPDATE_EXCEPTION";
	}
}
The workflow condition should also include:
Account_Name equals NOVCH16LAB901A
AND Description does not contain |CH16_PROCESSED|
The condition reduces unnecessary invocations. The Function guard protects against stale arguments, manual invocation, and recursion.
Function behavior
Input condition	Expected result
Wrong Account marker	No write
Missing ID	No write
Account not found	No write
Already processed	No write
Correct marker and unprocessed	One update
CRM update error	Safe failure log
Lost response	Target requires read-back
The Function does not claim that the CRM update and Workflow execution form one distributed transaction.
Function 3 — Scheduled scratch reconciliation
Host: CRM Schedule Function
Function: nova_ch16_reconcile_scratch
Inputs: none
Connection: none for direct CRM read
Supported task: Read one bounded page of CH16 scratch Accounts and report safe counts
Return contract: void
Side effects: none
void schedule.nova_ch16_reconcile_scratch()
{
	try
	{
		records = zoho.crm.v8.searchRecords(
			"Accounts",
			"(Account_Name:starts_with:NOVCH16)",
			1,
			200
		);

		if(records == null)
		{
			info "code=NO_RECORDS";
			return;
		}

		total = records.size();
		processed = 0;
		unprocessed = 0;

		for each record in records
		{
			name_value = record.get("Account_Name");
			description_value = record.get("Description");

			if(name_value == "NOVCH16LAB901A")
			{
				if(description_value != null &&
				   description_value.toString().contains("|CH16_PROCESSED|"))
				{
					processed = processed + 1;
				}
				else
				{
					unprocessed = unprocessed + 1;
				}
			}
		}

		info "code=RECONCILE_COMPLETE";
		info "total=" + total;
		info "processed=" + processed;
		info "unprocessed=" + unprocessed;
	}
	catch (e)
	{
		info "code=RECONCILE_FAILED";
	}
}
This Function deliberately processes only one bounded page and one exact marker. It is not a general production reconciliation worker.
## Try it yourself — guided practice

Practice A — Create the disposable Account
Create:
Account_Name: NOVCH16LAB901A
Description: CH16 scratch account
Capture:
step,operation,marker,record_id,expected,observed,status
1,create Account,NOVCH16LAB901A,<fill>,one record,<fill>,NOT_YET_RUN
2,read Account,NOVCH16LAB901A,<fill>,exact marker,<fill>,NOT_YET_RUN
Do not place a live access token or full CRM response in the worksheet.
Practice B — Run the Button Function
1. Create nova_ch16_preview.
2. Add account_id as a string argument.
3. Add a Button Function to Accounts.
4. Map account_id to the CRM Account ID.
5. Limit the button to the controlled training profile.
6. Click it on the disposable Account.
7. Record the returned modal message.
Run negative tests:
- Click the button on another Account.
- Pass a missing ID through editor testing.
- Use an invalid record ID.
- Use a deleted or unavailable record if the tenant permits safe testing.
Expected result:
case,target,expected_message,write_count,observed
valid,scratch Account,READY,0,NOT_YET_RUN
wrong marker,other Account,BLOCKED,0,NOT_YET_RUN
missing ID,null,BLOCKED,0,NOT_YET_RUN
Practice C — Test Workflow argument mapping
 1. Create the Automation Function.
 2. Create a Workflow Rule on Accounts.
 3. Limit the rule to NOVCH16LAB901A.
 4. Add the Description does not contain |CH16_PROCESSED| condition.
 5. Map the three arguments.
 6. Save and activate the rule.
 7. Edit the scratch Account.
 8. Inspect Function execution logs.
 9. Read the Account after the asynchronous execution.
10. Confirm the processed marker appears once.
Expected result:
Initial Description:
CH16 scratch account

After one successful execution:
CH16|CH16_PROCESSED|Account=NOVCH16LAB901A

After replay:
same Description; no second update
The values are expected results, not live observations.
Practice D — Test Schedule bounds
1. Create the Schedule Function.
2. Configure a short development schedule or use editor execution.
3. Confirm that it receives no record argument.
4. Run it against the bounded NOVCH16 search.
5. Record counts.
6. Add a second scratch record only if cleanup is controlled.
7. Confirm that the Function does not scan outside the marker boundary.
Evidence:
run_key,matched_records,processed_count,unprocessed_count,additional_pages,observed
CH16-SCHED-901,<fill>,<fill>,<fill>,<fill>,NOT_YET_RUN
Practice E — Test the failure path
Force one safe failure:
- Disable the Function’s required CRM permission.
- Use a non-existent record ID in editor testing.
- Remove the scratch Account before the Function runs.
- Use an invalid API field only in a disposable test.
Record:
failure,expected_code,record_state_after,log_contains_secret,observed
missing record,BLOCKED_ACCOUNT_NOT_FOUND,unchanged,false,NOT_YET_RUN
wrong marker,BLOCKED_MARKER_MISMATCH,unchanged,false,NOT_YET_RUN
already processed,ALREADY_PROCESSED,unchanged,false,NOT_YET_RUN
Do not deliberately break a production Function.
## Independent challenge

Design a CRM server-side customization for the following requirement:
When a disposable Nova training Account is edited, validate its marker, stamp a processing marker once, expose a read-only user button, and run a daily bounded reconciliation.
Complete this design sheet:
Design item	Your answer
Blocking or post-save?
Function categories
Workflow condition
Button profile scope
Schedule boundary
Arguments
Direct CRM tasks
Connection required?
Re-entry guard
Target marker
Maximum records per run
Failure code for marker mismatch
Failure code for missing record
Read-back requirement
Cleanup plan
Create these failure fixtures.
Failure fixture 1 — Workflow Function expected to block save
A developer expects a Workflow Function to reject an invalid Account before the record is saved.
Expected analysis:
- Workflow Functions run asynchronously after the record operation.
- Their failure does not provide a blocking validation result.
- Use a Validation Rule or Blueprint transition criteria for a save-blocking requirement.
- Keep post-save side effects separate from pre-save validation.
Failure fixture 2 — Button updates the wrong Account
A user clicks the Button on an Account whose name resembles the training marker.
Expected analysis:
- Re-read the Account by ID.
- Require exact marker equality.
- Do not use a partial match.
- Return a blocked modal message.
- Perform zero writes.
Failure fixture 3 — Recursive Workflow
The Workflow updates the same field that causes its own trigger.
Expected analysis:
- Add a narrow Workflow condition.
- Add an idempotent processed marker.
- Re-read the record in the Function.
- Exit if already processed.
- Test one initial edit and one replay.
- Inspect logs for repeated invocation.
Failure fixture 4 — Connection owner lacks permission
The Function uses a Connection authorized by a limited CRM user and the external call returns a permission failure.
Expected analysis:
- Distinguish direct Function CRM access from Connection access.
- Do not silently substitute the administrator identity.
- Reauthorize or change the Connection deliberately.
- Record the actual Connection owner and required scopes.
- Do not expose the returned token or raw response.
## Common problems and recovery

Symptom	Likely cause	Recovery
Function does not appear in a trigger list	Wrong Function category	Create the Function with the category required by the trigger
Workflow Function returns no user message	Automation Functions are asynchronous and return void	Use logs for diagnosis or a Button for immediate feedback
Button times out	Too much work for the interactive timeout	Reduce scope or move work to Automation or Schedule
Schedule has no record ID	Schedules have no natural record context	Query a bounded set of records
Arguments are empty	Deluge arguments were not mapped to merge variables	Review the trigger association mapping
JavaScript or Python expects Deluge arguments	Runtime input model differs	Read basicIO or runtime request context
Function updates the wrong record	Caller-provided ID was not re-read and checked	Validate exact module, marker, and record ID
Function runs repeatedly	Same-module update retriggers the Workflow	Add trigger narrowing and a processed-state guard
Function failure did not undo the record save	Workflow execution is asynchronous	Use Validation Rule or Blueprint criteria for blocking behavior
Direct CRM task can read restricted data	Function executes with system-level CRM access	Filter fields and avoid logging sensitive values
Connection call is denied	Connection owner lacks permission or scope	Reauthorize the Connection; do not assume Function admin access applies
Function exceeds line limit	Large loops or child calls	Page work, reduce scope, and use Schedule checkpoints
Function exceeds timeout	Category unsuitable for workload	Move long work to Schedule or external queue
info log exposes a secret	Entire Map, exception, or response was logged	Replace raw logging with allowlisted fields
Function was changed immediately in production	Deluge saves are live	Use Sandbox, revision history, and controlled deployment
Deleted Function breaks a button	Associations or references remained	Review associations and dependencies before deletion
Workflow consumes too many credits	High-volume trigger or repeated recursion	Narrow the rule, add guards, and estimate execution volume
Button is hidden but endpoint still works	UI visibility is not endpoint security	Configure endpoint authentication and server-side authorization
Reconciliation scans too many records	No marker or page bound	Use an exact marker, page limit, and checkpoint
## Check your understanding

 1. What determines where a CRM Function can be associated?
 2. Which Function category is appropriate for a post-save update?
 3. Which category should block an invalid record save?
 4. How are Deluge Workflow arguments supplied?
 5. What does a Button Function return?
 6. Why should a Function re-read a record?
 7. What is the difference between direct CRM access and Connection access?
 8. What is the documented timeout for a Schedule Function?
 9. What protects a same-module Workflow from repeated updates?
10. Does a Workflow Function failure roll back the record save?
11. Why should a schedule process a bounded marker set?
12. What permission controls Function management?
13. Can a Function’s system-level access be used as proof that a business user is authorized?
14. What should be recorded when a Connection call fails?
15. What evidence is needed before claiming that a live Function worked?
## Solutions and explanations

 1. The Function category determines eligible trigger contexts, return type, and execution behavior.
 2. Use an Automation Function for asynchronous post-save work.
 3. Use a Validation Rule or Blueprint transition criteria for a blocking rule.
 4. Declare the arguments in the Deluge Function and map them to CRM merge variables when associating the trigger.
 5. A Button Function returns a string displayed in a CRM modal.
 6. Trigger arguments may be stale, incomplete, or manipulated by an incorrect association. A re-read verifies the current authoritative target.
 7. Direct CRM tasks run with Function system-level access. A Connection uses the authorization and scopes of its authorized user.
 8. The current platform documentation lists 15 minutes for Schedule Functions.
 9. Narrow Workflow criteria plus an idempotent state or processed marker in the Function.
10. No. Workflow Functions run asynchronously and do not provide a coordinated rollback of the original record save.
11. To stay within execution time, API, line, and credit limits and to make progress resumable.
12. The current security documentation identifies the profile-level Manage Extensibility permission under Developer Permissions.
13. No. Technical execution access and business authorization are separate decisions.
14. Record a safe error code, Connection link name, operation, target module, and whether the failure was permission, authentication, transport, or business validation. Do not record tokens or raw confidential responses.
15. Actual tenant evidence should include the tenant and environment, Function category and revision, trigger configuration, safe inputs, execution log result, target read-back, and a statement that no secret-bearing data was exported.
## Chapter recap and next step

CRM server-side customisation is a trigger and contract design problem.
Use:
- Validation Rule for blocking save-time business rules.
- Automation for asynchronous post-save or transition side effects.
- Button for short user-requested actions with modal results.
- Schedule for bounded batch and reconciliation work.
- Standalone for reusable logic, REST endpoints, or ZDK calls.
- Related List for lightweight page-rendered data.
- Signals for inbound events that should raise CRM notifications.
Always define:
- Input arguments.
- Argument mapping.
- Return behavior.
- Caller and connection identity.
- Target marker or record identity.
- Re-entry guard.
- Error and retry behavior.
- Execution bounds.
- Safe logs.
- Read-back evidence.
- Cleanup.
The Nova business lifecycle remains unchanged. A CRM Function does not authorize a Creator completion, does not replace Creator ownership rules, and does not make an external side effect transactional.
The next chapter is:
C02-CH17 — CRM Client Script
## Glossary and further reading

Glossary
Automation Function
A Function associated with Workflow Rules, Blueprints, Approvals, or similar CRM automation.
Button Function
A Function invoked by a user through a CRM custom button and returning a modal string.
Connection
A secure credential configuration used by a Function to call another service or to apply explicit API scopes.
Function category
The execution context selected when a Function is created.
Function revision
A saved version of Function logic retained by the CRM Function management system.
Manage Extensibility
The CRM profile permission that allows users to create and manage Functions.
Merge variable
A CRM field value mapped into a Deluge Function argument during trigger configuration.
Re-entry guard
A condition that prevents a Function’s own update from causing an unintended repeated invocation.
Schedule Function
A Function invoked according to a configured time interval rather than a record event.
Standalone Function
A reusable Function that can be invoked by another Function, REST endpoint, Widget, or Client Script.
Validation Rule Function
A Function used to evaluate record data before save and return validation information.
Further reading
- Functions overview (https://www.zoho.com/crm/developer/docs/functions/)
- Function categories (https://www.zoho.com/crm/developer/docs/functions/getting-started/categories.html)
- Associating Functions with CRM (https://www.zoho.com/crm/developer/docs/functions/getting-started/associate-with-crm.html)
- Triggers and associations (https://www.zoho.com/crm/developer/docs/functions/triggers-and-associations.html)
- Functions platform limits and quotas (https://www.zoho.com/crm/developer/docs/functions/limits-quotas.html)
- Functions security (https://www.zoho.com/crm/developer/docs/functions/security.html)
- Managing Functions (https://www.zoho.com/crm/developer/docs/functions/management.html)
- Deluge CRM Function guide (https://www.zoho.com/crm/developer/docs/functions/language-guide/deluge.html)
- Create Function API (https://www.zoho.com/crm/developer/docs/api/v8/create-function.html)
- Serverless Functions (https://www.zoho.com/crm/developer/docs/functions/serverless.html)
- CRM v8 Records API (https://www.zoho.com/crm/developer/docs/api/v8/get-records.html)
- CRM v8 Upsert Records (https://www.zoho.com/crm/developer/docs/api/v8/upsert-records.html)
- CRM v8 Field Metadata (https://www.zoho.com/crm/developer/docs/api/v8/field-meta.html)
