# Deluge Data Operations

1. What you will learn
Chapter 7 taught you to calculate values and validate maps. This chapter applies those functions to real records.
You will learn to:
- distinguish native Creator record operations from integration tasks;
- query Creator records with criteria;
- search CRM records with Deluge integration tasks;
- create and update Creator records;
- create and update CRM records;
- work with lookup relationships;
- map business identifiers to product-generated record IDs;
- validate assignment and completion operations;
- handle partial failures;
- return useful per-record results;
- respect host-specific syntax, permissions, connections and limits.
The required practice is to build validated assignment and completion automation for Nova Field Service.
Contribution to the course project
This chapter implements two important operations:
1. assign a valid active Technician to a Job;
2. complete a Job only when required inspection evidence passes.
It also establishes the data-operation patterns needed for later chapters:
- Creator record tasks;
- CRM integration tasks;
- mapping and synchronization;
- partial-failure recovery;
- connection-aware operations;
- duplicate protection.
Continuity from previous chapters
Item	Carried-forward decision
Customer ownership	CRM owns customer identity and service information
Creator forms	Customer_Reference, Service_Requests, Technicians and Jobs
Inspection data	Inspection_Items remains a Job subform
Business identifiers	NOV-CUST-001, NOV-REQ-001 and NOV-VISIT-001 remain stable
Access	Technician sees assigned Jobs; Dispatcher or Service Manager assigns Jobs
Request lifecycle	New, Validated, Ready for Dispatch, Assigned, In Progress, Awaiting Inspection, Completed, Cancelled, Exception
Job lifecycle	Scheduled, Started, Completed, No Show, Cancelled
Sync lifecycle	Pending, Succeeded, Error, Retry Pending
Duplicate protection	External request key prevents repeated business actions
Deluge foundations	Maps, lists, null handling, reusable functions and host contexts from Chapter 7
Product and API assumptions
The exact Creator form link names, report link names, CRM module API names, CRM field API names, connection names, API versions, regional endpoints and scopes were not supplied by earlier continuity.
The code in this chapter uses clearly labelled placeholders where necessary. It is instructional code and has not been executed against a Zoho account.
2. Lessons
Lesson 1: Distinguish native Creator operations from integration tasks
Deluge can work with data in more than one way.
Native Creator record operations
Inside a Creator form workflow, you can use the application’s form and field context directly.
Host: Zoho Creator  
Example context: Jobs form, On Validate or On Success  
Input: input form record  
Connection: none for local record access  
Return shape: workflow behavior; no external response map required
Example query:
scheduledJobs = Jobs[Job_Status == "Scheduled"];
Example update of a related record:
jobRecord = Jobs[Job_Business_ID == "NOV-VISIT-001"];

if(jobRecord.count() > 0)
{
    jobRecord.Job_Status = "Started";
}
The exact field and form link names are proposed from Chapter 3 and must be confirmed.
Native Creator record operations are appropriate when the script runs inside the same application and needs to validate or update its records.
Creator integration tasks
zoho.creator.getRecords, zoho.creator.createRecord, zoho.creator.updateRecords and zoho.creator.updateRecord access Creator data through an integration task.
They require values such as:
- application owner;
- application link name;
- form or report link name;
- criteria;
- record values;
- pagination values;
- connection link name where required by the task and host.
Example shape:
response = zoho.creator.getRecords(
    "application_owner_placeholder",
    "nova_field_service",
    "All_Jobs",
    "Job_Status == \"Scheduled\"",
    1,
    200,
    "creator_oauth_connection_placeholder"
);
This is not the same operation as:
scheduledJobs = Jobs[Job_Status == "Scheduled"];
The first is an integration task that calls a Creator API boundary. The second is a native Creator form query.
The official Deluge documentation notes that Creator integration tasks can consume external-call or Developer API limits, and that actual executions are counted. Calling an integration task inside a loop can therefore produce one external call per iteration.
CRM integration tasks
CRM tasks use CRM module API names and field API names.
Example shape:
crmResponse = zoho.crm.searchRecords(
    "CRM_Module_API_Name_Placeholder",
    "(Customer_Business_ID:equals:NOV-CUST-001)"
);
The module and field names in this example are placeholders. Confirm them from CRM metadata before use.
The CRM task response is a map or list of maps. A successful response may contain records, while a failure response may contain an error code, message, details and status.
Flow context
In Flow, a Deluge step normally receives values from the trigger and previous actions. It does not automatically receive Creator’s input form object.
A Flow function should document:
- trigger fields;
- mapped inputs;
- connection used by the action;
- output fields;
- failure branch;
- whether the next step runs after success, failure or both.
Do not paste a Creator form script into Flow and expect input.Customer or cancel submit to work.
Quick check
1. Which operation is a native Creator form query?
2. Why does a zoho.creator.getRecords call need link names and pagination values?
3. Why should a CRM task not use a screen label as its module API name?
Lesson 2: Query records with criteria
A query should be as narrow as the business operation requires.
Native Creator criteria
Creator context: form workflow or custom function
errorRequests = Service_Requests[Sync_Status == "Error"];
A lookup criterion can traverse a related record:
northJobs = Jobs[Request.Customer.Customer_Business_ID == "NOV-CUST-001"];
The relationship path depends on the actual lookup link names. Confirm the names in the Creator reference page.
Check the result before using it:
technicians = Technicians[
    Technician_Business_ID == "TECH-001"
];

if(technicians.count() == 0)
{
    info "Technician was not found";
}
else
{
    technician = technicians.get(0);
}
If the business rule requires exactly one result, treat zero and more than one as different errors:
if(technicians.count() == 0)
{
    errorMessage = "Technician not found";
}
else if(technicians.count() > 1)
{
    errorMessage = "Technician mapping is not unique";
}
CRM search criteria
Host: Creator, CRM function or another Zoho service  
Task: zoho.crm.searchRecords  
Inputs: CRM module API name, criteria string, optional page and page size, optional connection depending on host  
Output: response map or record list  
Failure shape: error map with code, message, details and status
Illustrative search:
criteria = "(Customer_Business_ID:equals:NOV-CUST-001)";

crmResponse = zoho.crm.searchRecords(
    "Customer_Module_API_Name_Placeholder",
    criteria
);
The accessed Deluge documentation describes supported search operators such as equals and starts_with for this task and provides optional paging parameters. The exact supported behavior should be checked against the target CRM API and task documentation.
Inspect the response before treating it as a match:
if(isNull(crmResponse))
{
    result.put("status", "No response");
}
else if(crmResponse.get("status") == "error")
{
    result.put("status", "CRM error");
    result.put("error", crmResponse);
}
else
{
    result.put("status", "Search completed");
    result.put("records", crmResponse);
}
Do not assume that an empty list means permission denied. Distinguish:
- no matching record;
- invalid module;
- invalid criteria;
- permission error;
- connection failure;
- malformed response.
Search by business identifier
The preferred Nova mapping is:
Creator Customer_Business_ID
→ CRM customer business identifier
→ CRM-generated record ID
Do not search by display name unless the business explicitly accepts ambiguity.
Quick check
A Creator query returns three Technician records for one Technician_Business_ID. Is that a successful lookup? Why?
Lesson 3: Create and update Creator records
Create a related Creator record
There are two common approaches:
1. create a record directly in the same Creator application using native form operations;
2. use zoho.creator.createRecord when the operation crosses an application or API boundary.
The integration-task form is explicit and easier to document:
Host: a Zoho service calling Creator  
Task: zoho.creator.createRecord  
Connection: creator_oauth_connection_placeholder  
Return: response map containing a code, message and created record ID
Illustrative code:
jobValues = Map();
jobValues.put("Job_Business_ID", "NOV-VISIT-020");
jobValues.put("Request", requestRecordId);
jobValues.put("Technician", technicianRecordId);
jobValues.put("Job_Status", "Assigned");

otherParams = Map();

createResponse = zoho.creator.createRecord(
    "application_owner_placeholder",
    "nova_field_service",
    "Jobs",
    jobValues,
    otherParams,
    "creator_oauth_connection_placeholder"
);
The Creator integration-task documentation describes single-record and list-based creation. It also documents a maximum batch size for that task. Confirm the current limit and target environment before building a bulk operation.
Inspect the response:
result = Map();

if(createResponse.get("code") == 3000)
{
    result.put("success", true);
    result.put("record_id", createResponse.get("data").get("ID"));
}
else
{
    result.put("success", false);
    result.put("error", createResponse);
}
The code 3000 is shown in the accessed Creator task documentation as a success response for the example task. Confirm current response codes in the target API documentation.
Update a Creator record by ID
Task: zoho.creator.updateRecord  
Inputs: owner, app link name, report link name, numeric record ID, new values, options map, connection  
Use when: the exact target record ID is known
updateValues = Map();
updateValues.put("Job_Status", "Started");

otherParams = Map();

updateResponse = zoho.creator.updateRecord(
    "application_owner_placeholder",
    "nova_field_service",
    "All_Jobs",
    creatorRecordId,
    updateValues,
    otherParams,
    "creator_oauth_connection_placeholder"
);
A business ID such as NOV-VISIT-020 is not necessarily the Creator record ID. Search or map the Creator record ID before calling an operation that requires it.
Update records by criteria
Task: zoho.creator.updateRecords  
Use when: multiple records should receive the same update and the criteria is tightly controlled
values = Map();
values.put("Sync_Status", "Retry Pending");

otherParams = Map();

response = zoho.creator.updateRecords(
    "application_owner_placeholder",
    "nova_field_service",
    "Sync_Exceptions",
    "Sync_Status == \"Error\"",
    values,
    otherParams,
    "creator_oauth_connection_placeholder"
);
Do not use a broad criterion accidentally. Updating all records is a destructive operation and must be explicitly approved.
Native Creator updates
Creator context: local form workflow
jobRecords = Jobs[Job_Business_ID == input.Job_Business_ID];

if(jobRecords.count() == 1)
{
    jobRecord = jobRecords.get(0);
    jobRecord.Job_Status = "Started";
}
This avoids a Creator API integration call when the script is already operating inside the same application. It still requires access, validation and lifecycle checks.
Quick check
1. Why must a Creator record ID be mapped separately from NOV-VISIT-020?
2. When is a criteria-based update dangerous?
3. Which update approach is more appropriate for a local Creator form workflow: a native record update or a cross-application Creator integration task?
Lesson 4: Create and update CRM records safely
CRM integration tasks use CRM module and field API names. Do not use unverified screen labels.
Create a CRM record
Host: Creator custom function or another Zoho service  
Task: zoho.crm.createRecord  
Input: module API name and field API-name map  
Connection: use the connection parameter where supported and required by the host  
Output: response map with record ID or error
Illustrative code:
crmValues = Map();
crmValues.put("Customer_Business_ID", "NOV-CUST-001");
crmValues.put("Service_Request_Business_ID", "NOV-REQ-020");
crmValues.put("Request_Status", "Ready for Dispatch");

options = Map();
// Trigger behavior must be explicitly selected according to the approved contract.
// options.put("trigger", {"workflow"});

crmResponse = zoho.crm.createRecord(
    "CRM_Service_Module_API_Name_Placeholder",
    crmValues,
    options,
    "crm_connection_placeholder"
);
The exact module, field API names, options and connection behavior must be verified in the target CRM context. The accessed Deluge documentation describes optional trigger options and response maps.
Update a CRM record
crmValues = Map();
crmValues.put("Service_Request_Business_ID", "NOV-REQ-020");
crmValues.put("Request_Status", "Assigned");

crmResponse = zoho.crm.updateRecord(
    "CRM_Service_Module_API_Name_Placeholder",
    crmRecordId,
    crmValues,
    Map(),
    "crm_connection_placeholder"
);
Update only fields owned by the integration contract. Do not overwrite CRM-owned customer fields with Creator display values.
Upsert
An upsert creates or updates based on a unique identifier or supplied record ID. It is not automatically safe duplicate protection. The identifier and matching behavior must be explicitly confirmed.
crmValues = Map();
crmValues.put("Customer_Business_ID", "NOV-CUST-001");
crmValues.put("Service_Request_Business_ID", "NOV-REQ-020");

response = zoho.crm.upsert(
    "CRM_Service_Module_API_Name_Placeholder",
    crmValues,
    Map(),
    "crm_connection_placeholder"
);
If the unique field is not correctly configured or the input is ambiguous, an upsert can create an unintended record or update the wrong one. Validate the key and inspect the response.
Response categories
Classify response maps into:
success
validation_error
not_found
permission_error
duplicate_or_conflict
transient_error
unknown_error
Do not treat all non-success responses as retryable.
Quick check
Why is upsert not a complete substitute for an external request-key idempotency design?
Lesson 5: Map lookups and relationships
A Creator lookup is a relationship to another record. A CRM lookup may require a record ID or a lookup map containing an ID and display value, depending on the task and API.
Do not map this:
crmValues.put("Customer", "Northstar Facilities Ltd");
unless the target API explicitly accepts that value as a valid lookup representation.
Instead, map through a verified identifier:
customerMap = Map();
customerMap.put("id", crmCustomerRecordId);

crmValues.put("Customer", customerMap);
The exact CRM lookup structure must be checked in the current CRM API and module metadata.
Creator lookup assignment
Creator context: Jobs form On Validate or On Success
requestRecords = Service_Requests[
    Request_Business_ID == input.Request_Business_ID
];

if(requestRecords.count() == 1)
{
    requestRecord = requestRecords.get(0);
    newJob.Request = requestRecord.ID;
}
The use of the generated record ID for the lookup relationship is separate from the business ID used for support and integration.
Mapping table
Source	Destination	Mapping basis
Creator Customer_Business_ID	CRM customer business field	Stable business identifier
Creator Customer lookup	CRM lookup	Verified CRM record ID
Creator Request_Business_ID	CRM service request field	Stable business identifier
Creator Sync_Status	Integration status field	Controlled status mapping
Creator Job_Status	CRM summary status	Approved contract only
Keep a mapping specification with:
- source form and field link name;
- destination module and field API name;
- data type;
- transformation;
- null behavior;
- ownership;
- failure behavior.
Quick check
Why should a CRM lookup map use a verified CRM record ID instead of the display name?
Lesson 6: Handle partial failures
A partial failure occurs when a multi-record operation succeeds for some records and fails for others.
Example:
Five Jobs require assignment.
Two are assigned successfully.
One has an inactive Technician.
One has a missing Request.
One fails because the Creator operation times out.
Do not return only:
Assignment failed.
Return a per-record result.
results = List();

row = Map();
row.put("business_id", "NOV-VISIT-020");
row.put("success", true);
row.put("status", "Assigned");
results.add(row);

row = Map();
row.put("business_id", "NOV-VISIT-021");
row.put("success", false);
row.put("error_category", "Inactive Technician");
row.put("retryable", false);
results.add(row);
A useful result shape is:
{
  "success": false,
  "processed": 5,
  "succeeded": 2,
  "failed": 3,
  "results": [
    {
      "business_id": "NOV-VISIT-020",
      "success": true,
      "status": "Assigned"
    },
    {
      "business_id": "NOV-VISIT-021",
      "success": false,
      "error_category": "Inactive Technician",
      "retryable": false
    }
  ]
}
Failure handling rules
Failure	Retry?	Recovery
Missing customer	No automatic retry	Correct mapping
Invalid field value	No automatic retry	Correct input
Duplicate external key	No new create	Reference existing record
Permission denied	No blind retry	Correct approved permission
Timeout	Maybe	Retry with same key and claim state
Temporary service unavailable	Maybe	Backoff and retry
Unknown response	No blind retry	Record and investigate
Transactions and boundaries
A native Creator On Validate event can cancel a form submission. The official Creator cancel submit documentation states that applicable tasks in that validation section are rolled back, with specified exceptions. That behavior does not mean that every integration call elsewhere in a process automatically rolls back a previously saved record.
For a workflow that saves a Request and then calls CRM:
1. save or preserve the Creator Request;
2. set Sync_Status = Pending;
3. call CRM;
4. record success or error;
5. retry safely if permitted.
Do not assume a remote CRM create can be undone by a Creator field update.
Quick check
A batch assigns five Jobs and two fail. Should the automation undo the three successful assignments automatically? What additional business rule would be required before choosing that behavior?
Lesson 7: Use context-specific syntax and connections
Creator form context
Host: Creator  
Event: Jobs form On Validate  
Inputs: input, related lookups and subform rows  
Connection: not required for native local operations  
Outcome: allow or cancel form submission
if(isNull(input.Technician))
{
    alert "An active Technician is required";
    cancel submit;
}
Creator integration context
Host: Creator custom function or workflow calling another Creator application  
Task: zoho.creator.getRecords, createRecord, updateRecord  
Inputs: owner, app link name, report/form link name, criteria or values  
Connection: approved Creator OAuth connection placeholder  
Outcome: response map with code and data or error
CRM context
Host: Creator custom function or CRM function  
Task: zoho.crm.searchRecords, createRecord, updateRecord, upsert  
Inputs: CRM module API names, field API-name map, CRM record IDs  
Connection: verify whether the host requires the connection parameter  
Outcome: CRM response map
Flow context
Host: Zoho Flow custom function or action  
Inputs: trigger payload and mapped step values  
Connection: selected in Flow or task configuration  
Outcome: map or fields passed to later steps  
Important: no automatic Creator input object
A connection placeholder is not a credential:
crm_connection_placeholder
creator_oauth_connection_placeholder
The real connection must be created, scoped, owned and tested in the target environment. Do not hard-code access tokens or client secrets.
Quick check
Why must the same business logic be separated from the Creator adapter before it is reused in Flow?
3. Visual explanation
Creator-to-CRM assignment flow
flowchart TD
    E[Creator workflow event] --> V[Validate input and access]
    V -->|invalid| X[Return field or business error]
    V -->|valid| Q[Query Creator records]
    Q --> M[Map business IDs to record IDs]
    M --> A[Create or update Creator Job]
    A --> C[Optional CRM integration task]
    C -->|success| S[Mark Sync Succeeded]
    C -->|duplicate| D[Reference existing CRM action]
    C -->|permission or validation| P[Mark non-retryable error]
    C -->|timeout or unavailable| R[Mark Retry Pending]
    A --> O[Return per-record result]
    S --> O
    D --> O
    P --> O
    R --> O
Plain-text explanation:
1. The workflow receives a host-specific event.
2. It validates the user, data and current lifecycle.
3. It queries Creator records using the appropriate local or integration syntax.
4. It maps business identifiers to product record IDs.
5. It creates or updates the Creator Job.
6. If the approved contract requires CRM synchronization, it calls a CRM integration task.
7. The response is classified as success, duplicate, non-retryable failure or retryable failure.
8. The result preserves a per-record outcome.
Operation	Native Creator form query	Creator integration task	CRM integration task
Search	Form[criteria]	zoho.creator.getRecords	zoho.crm.searchRecords
Create	Native form record operation or local workflow	zoho.creator.createRecord	zoho.crm.createRecord
Update one	Direct record object in Creator	zoho.creator.updateRecord	zoho.crm.updateRecord
Update many	Controlled Creator record operation	zoho.creator.updateRecords	CRM bulk or loop, subject to limits
Key names	Creator field link names	Creator app/form/report link names	CRM module and field API names
Identity	Creator record ID and business ID	Creator record ID and link names	CRM record ID and business key
Failure output	Host validation or record context	Response map with code/data	Response map with status/error details
4. Worked case
Case inputs
Technicians:
technician_business_id,technician_name,active
TECH-001,Priya Nair,true
TECH-002,Daniel Ortiz,true
TECH-003,Leah Stone,false
Requests:
request_business_id,customer_business_id,priority,request_status,sync_status
NOV-REQ-020,NOV-CUST-001,High,Ready for Dispatch,Succeeded
NOV-REQ-021,NOV-CUST-002,Medium,Ready for Dispatch,Succeeded
NOV-REQ-022,NOV-CUST-001,High,Ready for Dispatch,Succeeded
Jobs to assign:
job_business_id,request_business_id,technician_business_id,job_status,expected_result
NOV-VISIT-020,NOV-REQ-020,TECH-001,Scheduled,valid
NOV-VISIT-021,NOV-REQ-021,TECH-003,Scheduled,inactive_technician
NOV-VISIT-022,NOV-REQ-022,,Scheduled,missing_technician
NOV-VISIT-023,NOV-REQ-020,TECH-002,Scheduled,valid
Inspection rows:
job_business_id,check_name,required,result
NOV-VISIT-020,Pump pressure,true,Pass
NOV-VISIT-020,Electrical enclosure,true,Pass
NOV-VISIT-023,Pump pressure,true,Pass
NOV-VISIT-023,Electrical enclosure,true,Fail
Step 1: Validate an assignment
Host: Creator Jobs form, On Validate  
Input: current Job form record  
Record operation: native Creator Technician lookup  
Output: allow save or cancel submit
Illustrative Creator code:
errors = List();

if(isNull(input.Request))
{
    errors.add("Request is required");
}

if(isNull(input.Technician))
{
    errors.add("Technician is required");
}
else if(input.Technician.Active != true)
{
    errors.add("Selected Technician is inactive");
}

if(isNull(input.Scheduled_Start) || isNull(input.Scheduled_End))
{
    errors.add("Schedule is required");
}
else if(input.Scheduled_End <= input.Scheduled_Start)
{
    errors.add("Scheduled end must be after scheduled start");
}

if(errors.size() > 0)
{
    alert errors.toString();
    cancel submit;
}
This code is Creator-specific because it uses input, form lookup fields, alert and cancel submit.
Expected results:
Job	Result
NOV-VISIT-020	Valid
NOV-VISIT-021	Rejected because TECH-003 is inactive
NOV-VISIT-022	Rejected because Technician is missing
NOV-VISIT-023	Valid
Step 2: Validate completion
Host: Creator Jobs form, On Validate  
Input: Job fields and Inspection_Items subform  
Record operation: local validation only  
Output: allow or cancel submit
Illustrative code:
errors = List();

if(isNull(input.Technician))
{
    errors.add("Technician is required before completion");
}

if(isNull(input.Visit_Notes) || isBlank(input.Visit_Notes))
{
    errors.add("Visit notes are required before completion");
}

if(input.Job_Status == "Completed")
{
    for each inspectionItem in input.Inspection_Items
    {
        if(inspectionItem.Required == true &&
           inspectionItem.Result != "Pass")
        {
            errors.add(
                inspectionItem.Check_Name + " must be Pass before completion"
            );
        }
    }
}

if(errors.size() > 0)
{
    alert errors.toString();
    cancel submit;
}
Expected results:
- NOV-VISIT-020 may complete if notes exist.
- NOV-VISIT-023 cannot complete because Electrical enclosure is Fail.
- A required inspection row with a blank result also blocks completion.
- The code does not call CRM or create a follow-up Job. That is a separate process decision.
Step 3: Map a Creator Customer to CRM
Host: Creator custom function or approved Creator workflow  
Task: CRM search integration task  
Module: placeholder because no CRM module API name was supplied  
Connection: crm_connection_placeholder where supported and required  
Return: map with mapping status
Illustrative code:
result = Map();
customerBusinessId = "NOV-CUST-001";

criteria = "(Customer_Business_ID:equals:" + customerBusinessId + ")";

crmResponse = zoho.crm.searchRecords(
    "CRM_Customer_Module_API_Name_Placeholder",
    criteria
);

if(isNull(crmResponse))
{
    result.put("status", "No Response");
}
else if(crmResponse.get("status") == "error")
{
    result.put("status", "CRM Error");
    result.put("error", crmResponse);
}
else if(crmResponse.size() == 0)
{
    result.put("status", "Not Found");
}
else if(crmResponse.size() > 1)
{
    result.put("status", "Not Unique");
}
else
{
    crmRecord = crmResponse.get(0);
    result.put("status", "Mapped");
    result.put("crm_record_id", crmRecord.get("id"));
    result.put("customer_business_id", customerBusinessId);
}

return result;
This code is illustrative. The exact response shape and criteria syntax must be confirmed for the target CRM task and module.
Step 4: Partial assignment result
A batch assignment result might be:
{
  "success": false,
  "processed": 4,
  "succeeded": 2,
  "failed": 2,
  "results": [
    {
      "job_business_id": "NOV-VISIT-020",
      "success": true,
      "status": "Assigned"
    },
    {
      "job_business_id": "NOV-VISIT-021",
      "success": false,
      "error_category": "Inactive Technician",
      "retryable": false
    },
    {
      "job_business_id": "NOV-VISIT-022",
      "success": false,
      "error_category": "Missing Technician",
      "retryable": false
    },
    {
      "job_business_id": "NOV-VISIT-023",
      "success": true,
      "status": "Assigned"
    }
  ]
}
The two valid assignments remain assigned. The two invalid Jobs remain available for correction. The process does not silently roll back valid work or retry non-retryable errors.
Mistake and correction
Mistake: The developer loops through Jobs and calls a CRM search once for each Job, even though several Jobs share the same Customer.
Why it is wrong: It creates unnecessary external calls and increases the chance of inconsistent results or partial failure.
Correction:
1. collect distinct Customer business IDs;
2. resolve each Customer once;
3. cache the mapping;
4. use the mapping for all related Jobs;
5. record per-Job failures when a mapping is missing.
A second mistake is using zoho.creator.updateRecords with a broad criterion such as:
Job_Status != "Completed"
The correction is to select exact record IDs or a tightly bounded, approved criterion. Broad updates can alter records belonging to different users or lifecycles.
5. Try it yourself — guided practice
Learning goal
Build validated assignment and completion automation for Creator Jobs.
Host and access requirements
Use a Creator development or sandbox environment. You need:
- access to the Technicians and Jobs forms;
- permission to create a Creator custom function or form workflow;
- synthetic records only;
- no CRM connection for the local validation portion;
- a placeholder CRM connection only if you perform the mapping extension.
Sample inputs
Technicians:
technician_business_id,technician_name,active
TECH-001,Priya Nair,true
TECH-002,Daniel Ortiz,true
TECH-003,Leah Stone,false
Jobs:
job_business_id,request_business_id,technician_business_id,scheduled_start,scheduled_end,job_status
NOV-VISIT-030,NOV-REQ-030,TECH-001,2026-10-10T09:00:00Z,2026-10-10T11:00:00Z,Scheduled
NOV-VISIT-031,NOV-REQ-031,TECH-003,2026-10-10T10:00:00Z,2026-10-10T11:00:00Z,Scheduled
NOV-VISIT-032,NOV-REQ-032,,2026-10-10T12:00:00Z,2026-10-10T13:00:00Z,Scheduled
NOV-VISIT-033,NOV-REQ-033,TECH-002,2026-10-10T14:00:00Z,2026-10-10T13:00:00Z,Scheduled
Inspection rows:
job_business_id,check_name,required,result,notes
NOV-VISIT-030,Pump pressure,true,Pass,Stable
NOV-VISIT-030,Electrical enclosure,true,Pass,Safe
NOV-VISIT-033,Door operation,true,Pass,Working
NOV-VISIT-033,Access safety,true,,Missing result
Steps and expected intermediate results
1. Create or verify the Technicians and Jobs forms using the Chapter 3 schema.  
Expected result: Jobs have Technician, Request, schedule and status fields.
2. Implement assignment validation in the Jobs form’s On Validate event.  
Expected result: the validation can reject a missing or inactive Technician before save.
3. Test NOV-VISIT-030.  
Expected result: assignment is accepted.
4. Test NOV-VISIT-031.  
Expected result: assignment is rejected because TECH-003 is inactive.
5. Test NOV-VISIT-032.  
Expected result: assignment is rejected because no Technician is selected.
 6. Test NOV-VISIT-033.  
Expected result: assignment is rejected because the end time precedes the start time.
 7. Implement the completion gate.  
Expected result: completion checks all required inspection rows, not only the first row.
 8. Test completion for NOV-VISIT-030.  
Expected result: completion is allowed if visit notes exist.
 9. Test completion for NOV-VISIT-033.  
Expected result: completion is rejected because Access safety is blank.
10. Return a structured result from a reusable validation function.  
Expected result: the form adapter displays an error, while the function itself remains independent of the UI.
11. Add a partial-failure result table for all four Jobs.  
Expected result: two invalid Jobs are reported without hiding the valid one.
Final artifact
Create:
- C02-CH08_Nova_Field_Service_Data_Operations_v0.1.md;
- assignment validation function;
- completion validation function;
- Creator On Validate adapters;
- result table for all sample Jobs;
- partial-failure handling note;
- optional CRM mapping function with placeholder module and connection names.
Cleanup
Remove or disable test workflows and custom functions created only for the practice. Delete synthetic records if they are not needed for later chapters.
Offline alternative
Write the Creator-specific scripts and expected record results in Markdown. Simulate form inputs with the supplied CSV data. This demonstrates logic and mapping but cannot demonstrate Creator record operations or response behavior.
6. Independent challenge
Changed constraints
Nova now supports batch assignment from the Dispatcher Page:
 1. A Dispatcher submits up to four Jobs for assignment.
 2. Each Job must have an active Technician.
 3. A Technician may not receive overlapping Jobs.
 4. All Jobs must belong to a Request that is Ready for Dispatch.
 5. A valid assignment updates the Job to Assigned.
 6. An invalid Job must not prevent other valid Jobs from being processed.
 7. The result must identify each success and failure.
 8. CRM synchronization is not performed by this batch operation.
 9. A later process may synchronize successful assignments.
10. The operation must not assign the same Job twice if the batch is replayed.
Challenge data
Technicians:
technician_business_id,technician_name,active
TECH-001,Priya Nair,true
TECH-002,Daniel Ortiz,true
TECH-003,Leah Stone,true
TECH-004,Sam Rivera,false
Requests:
request_business_id,request_status
NOV-REQ-040,Ready for Dispatch
NOV-REQ-041,Ready for Dispatch
NOV-REQ-042,In Progress
NOV-REQ-043,Ready for Dispatch
NOV-REQ-044,Ready for Dispatch
Existing Jobs:
job_business_id,request_business_id,technician_business_id,scheduled_start,scheduled_end,job_status
NOV-VISIT-040,NOV-REQ-040,TECH-001,2026-10-10T09:00:00Z,2026-10-10T11:00:00Z,Assigned
NOV-VISIT-041,NOV-REQ-041,TECH-002,2026-10-10T13:00:00Z,2026-10-10T14:00:00Z,Assigned
Assignment batch:
job_business_id,request_business_id,technician_business_id,scheduled_start,scheduled_end,replay_key
NOV-VISIT-045,NOV-REQ-040,TECH-001,2026-10-10T10:00:00Z,2026-10-10T12:00:00Z,BATCH-001
NOV-VISIT-046,NOV-REQ-041,TECH-003,2026-10-10T13:00:00Z,2026-10-10T14:00:00Z,BATCH-002
NOV-VISIT-047,NOV-REQ-042,TECH-002,2026-10-10T15:00:00Z,2026-10-10T16:00:00Z,BATCH-003
NOV-VISIT-048,NOV-REQ-043,TECH-004,2026-10-10T16:00:00Z,2026-10-10T17:00:00Z,BATCH-004
Deliverables
Produce:
- a reusable batch-assignment function;
- overlap-detection logic;
- Request-state validation;
- active-Technician validation;
- replay protection;
- per-record result shape;
- all expected results for the four batch rows;
- a recovery rule for a partial failure;
- a note identifying which operations are native Creator operations and which would be integration tasks.
Success criteria
Your solution succeeds when:
- NOV-VISIT-045 is rejected because it overlaps TECH-001’s existing Job;
- NOV-VISIT-046 is assigned to TECH-003;
- NOV-VISIT-047 is rejected because the Request is not Ready for Dispatch;
- NOV-VISIT-048 is rejected because TECH-004 is inactive;
- the batch returns four individual outcomes;
- replaying BATCH-002 does not assign NOV-VISIT-046 a second time;
- one failure does not erase the successful assignment;
- no CRM call is made by the local assignment operation.
7. Common problems and recovery
Symptom	Diagnosis	Correction
Creator query finds no record	Form or field link name is wrong, or criteria value is mismatched	Verify link names and normalize the comparison value
Multiple records match one business ID	Uniqueness rule was not enforced	Treat as data-quality failure and stop mapping
CRM search returns an error map	Module name, criteria, permission or connection is wrong	Classify error before using records
Lookup display text is written to a CRM lookup	Relationship mapping used a label instead of an ID	Map the verified CRM record ID
Broad update changes unrelated records	Criteria was too broad	Use exact IDs or approved bounded criteria
A create call runs inside a loop for every child row	External calls were not bounded	Cache mappings, batch where supported and record call counts
Partial batch failure hides successful records	Function returns one Boolean	Return per-record result maps
Failed CRM write causes duplicate retry	No external key or attempt state	Reuse business key and store retry state
Creator record ID is confused with business ID	Technical and business identities were mixed	Store and map both explicitly
CRM task uses screen labels	API names were not verified	Confirm module and field API names
Creator integration task is used for local record update	Wrong task boundary	Use native Creator record operation where appropriate
Flow script expects input.Customer	Creator context was copied into Flow	Map Flow trigger fields explicitly
Connection placeholder is hard-coded as a secret	Configuration and credentials were mixed	Use named connection configuration
Successful record update triggers unexpected workflow	Task trigger options were not documented	Define which workflows, approvals or Blueprints run
One error cancels an entire valid batch	Atomicity assumption was not specified	Choose per-record recovery or approved all-or-nothing behavior
8. Check your understanding
1. What is the difference between Jobs[Job_Status == "Scheduled"] and zoho.creator.getRecords(...)?
2. Why should a Creator integration task use application and report link names?
3. What must be checked before using the first record returned from a business-key query?
4. Why is NOV-VISIT-020 not necessarily a valid record_id argument?
5. What is the difference between updating one Creator record by ID and updating records by criteria?
6. Why should a CRM lookup use a verified record ID?
7. A batch contains four Jobs and one assignment fails. What should the function return?
8. Which error categories may be retryable?
9. Why should the CRM search response be inspected before using .get("id")?
10. What is the correct host context for cancel submit;?
11. Why should a Creator record update and CRM update not be treated as one automatically atomic transaction?
12. What should happen when the same batch replay key is processed twice?
9. Solutions and explanations
Lesson quick checks
 1. Jobs[criteria] is a native Creator form query that returns a Creator record collection. zoho.creator.getRecords is an integration task that crosses a Creator API boundary and requires application, report and pagination parameters.
 2. Link names identify the application and report in the integration task contract. Display labels are not reliable identifiers.
 3. Check zero, one and multiple matches. Zero means not found; multiple means the business key is not unique and mapping must stop.
 4. NOV-VISIT-020 is a business identifier. The Creator update-by-ID task requires the product-generated numeric record ID.
 5. Update-by-ID targets one known record. Criteria update can affect every matching record and therefore needs carefully bounded criteria.
 6. A display name can change or be duplicated. A verified product record ID identifies the intended lookup target.
 7. Return a batch summary and one result per Job, including success, failure category, retryability and business ID.
 8. Timeouts, temporary unavailability and some rate-limit responses may be retryable. Missing data, invalid input, permission errors and duplicate conflicts should not be blindly retried.
 9. A search can return an error map, an empty result or several records. Inspect status and cardinality first.
10. Creator form On Validate. It is not a general CRM or Flow command.
11. They are separate systems and task calls. A Creator save can succeed while a CRM call fails. Use sync state and recovery instead of assuming rollback.
12. The second run should detect the replay key or existing assignment and return an existing-result status without applying a second business action.
Worked-case results
Job	Result	Reason
NOV-VISIT-020	Assignment valid	Active TECH-001 and valid schedule
NOV-VISIT-021	Assignment rejected	TECH-003 is inactive
NOV-VISIT-022	Assignment rejected	Technician missing
NOV-VISIT-023	Assignment valid	Active TECH-002 and valid schedule
NOV-VISIT-020 completion	Allowed if notes exist	All required checks pass
NOV-VISIT-023 completion	Rejected	Electrical enclosure failed
The Creator On Validate adapter is appropriate for blocking invalid local records. A separate Creator custom function or workflow can perform CRM mapping. The two contexts must not be mixed.
Guided-practice sample solution
Expected assignment results:
Job	Result
NOV-VISIT-030	Valid
NOV-VISIT-031	Invalid: inactive Technician
NOV-VISIT-032	Invalid: missing Technician
NOV-VISIT-033	Invalid: end before start
Expected completion results:
Job	Result
NOV-VISIT-030	Completion allowed if visit notes are present
NOV-VISIT-033	Completion rejected because Access safety is blank
A reusable assignment result can be:
map validateAssignment(map assignment)
{
    errors = List();

    if(isNull(assignment.get("job_business_id")) ||
       isBlank(assignment.get("job_business_id")))
    {
        errors.add("job_business_id is required");
    }

    if(isNull(assignment.get("request_status")) ||
       assignment.get("request_status") != "Ready for Dispatch")
    {
        errors.add("Request is not Ready for Dispatch");
    }

    if(isNull(assignment.get("technician_business_id")) ||
       isBlank(assignment.get("technician_business_id")))
    {
        errors.add("Technician is required");
    }

    if(assignment.get("technician_active") != true)
    {
        errors.add("Technician is inactive");
    }

    if(isNull(assignment.get("scheduled_start")) ||
       isNull(assignment.get("scheduled_end")))
    {
        errors.add("Schedule is required");
    }

    result = Map();
    result.put("valid", errors.size() == 0);
    result.put("errors", errors);
    return result;
}
A completion result can be:
map validateCompletion(map job)
{
    errors = List();
    inspectionItems = job.get("inspection_items");

    if(isNull(job.get("technician_business_id")))
    {
        errors.add("Technician is required");
    }

    if(isNull(job.get("visit_notes")) ||
       isBlank(job.get("visit_notes")))
    {
        errors.add("Visit notes are required");
    }

    if(isNull(inspectionItems) || inspectionItems.size() == 0)
    {
        errors.add("Inspection items are required");
    }
    else
    {
        for each item in inspectionItems
        {
            if(item.get("required") == true &&
               item.get("result") != "Pass")
            {
                errors.add(
                    item.get("check_name") + " must be Pass"
                );
            }
        }
    }

    result = Map();
    result.put("valid", errors.size() == 0);
    result.put("errors", errors);
    return result;
}
These functions are reusable because they receive maps rather than Creator form objects. The Creator adapter is responsible for converting input and related records into those maps.
Independent-challenge sample solution
Overlap rule:
\[
\text{Start}{new} < \text{End}{existing}
\quad\text{and}\quad
\text{End}{new} > \text{Start}{existing}
\]
Expected results:
Job	Result	Reason
NOV-VISIT-045	Rejected	Overlaps TECH-001’s NOV-VISIT-040
NOV-VISIT-046	Assigned	Request ready, TECH-003 active, no overlap
NOV-VISIT-047	Rejected	Parent Request is In Progress
NOV-VISIT-048	Rejected	TECH-004 is inactive
Expected batch result:
{
  "success": false,
  "processed": 4,
  "succeeded": 1,
  "failed": 3,
  "results": [
    {
      "job_business_id": "NOV-VISIT-045",
      "success": false,
      "error_category": "Overlap",
      "retryable": false
    },
    {
      "job_business_id": "NOV-VISIT-046",
      "success": true,
      "status": "Assigned",
      "replay_key": "BATCH-002"
    },
    {
      "job_business_id": "NOV-VISIT-047",
      "success": false,
      "error_category": "Request Not Ready",
      "retryable": false
    },
    {
      "job_business_id": "NOV-VISIT-048",
      "success": false,
      "error_category": "Inactive Technician",
      "retryable": false
    }
  ]
}
Replay behavior:
If replay_key BATCH-002 already has a successful result:
return Already Processed
do not update NOV-VISIT-046 again
do not send a second notification
The batch operation performs only local Creator validation and assignment. CRM synchronization is a separate later process. This separation reduces external calls and makes partial failure easier to understand.
10. Chapter recap and next step
You should now be able to:
- distinguish native Creator record access from integration tasks;
- query Creator records with criteria;
- use Creator and CRM integration task shapes;
- create and update records with explicit link names and API names;
- map business identifiers to product-generated IDs;
- assign lookup relationships safely;
- classify integration responses;
- process partial failures without hiding successful work;
- use connections without exposing credentials;
- separate Creator, CRM and Flow execution contexts;
- build validated assignment and completion automation.
Your project artifact from this chapter is:
C02-CH08_Nova_Field_Service_Data_Operations_v0.1.md
It should contain the assignment validator, completion gate, mapping notes, partial-failure result shape and context-specific operation examples.
Chapter 9 builds external-service integrations with Deluge. It will cover connections, invokeurl, headers, parameters, request bodies, JSON parsing, files, response codes, timeouts and execution limits.
11. Glossary and further reading
Glossary
Business identifier  
A stable identifier meaningful to the business, such as NOV-VISIT-020.
Connection  
A configured authorization object used by a supported integration task or external call.
Criteria  
A condition used to select records for retrieval or update.
Integration task  
A Deluge task that calls a Zoho service or API boundary.
Link name  
A product identifier for an application, form, report or field used by integrations.
Mapping  
The controlled conversion between source and destination fields, identifiers or record references.
Native record operation  
A record query or update performed within the current Creator form or application context.
Partial failure  
A multi-record operation in which some items succeed and others fail.
Product-generated record ID  
An identifier assigned by Creator or CRM to one stored record.
Record collection  
A group of records returned by a criteria query.
Retryable error  
An error that may be safely attempted again under an explicit recovery rule.
Upsert  
An operation that creates or updates based on matching logic, provided the matching identifier and behavior are correctly defined.
Further reading
- Deluge Integration Tasks for Zoho Services (https://www.zoho.com/deluge/help/integration-tasks.html) — official overview of integration-task structure, external calls and limits.
- Zoho Creator Integration Tasks (https://www.zoho.com/deluge/help/creator-tasks.html) — official Creator Get, Create and Update task index.
- Get Records from Zoho Creator (https://www.zoho.com/deluge/help/creator/get-records.html) — official criteria, pagination, link-name and response reference.
- Create Record in Zoho Creator (https://www.zoho.com/deluge/help/creator/create-record.html) — official Creator record-creation syntax and response examples.
- Update Records in Zoho Creator (https://www.zoho.com/deluge/help/creator/update-records.html) — official criteria-based update reference.
- Update Record in Zoho Creator (https://www.zoho.com/deluge/help/creator/update-record.html) — official update-by-ID reference.
- Zoho CRM Integration Tasks (https://www.zoho.com/deluge/help/crm-tasks.html) — official CRM task index.
- Search Records in Zoho CRM (https://www.zoho.com/deluge/help/crm/search-records.html) — official CRM search criteria, pagination and response reference.
- Create Record in Zoho CRM (https://www.zoho.com/deluge/help/crm/create-record.html) — official CRM creation syntax and error response examples.
- Update Record in Zoho CRM (https://www.zoho.com/deluge/help/crm/update-record.html) — official CRM update syntax.
- Upsert in Zoho CRM (https://www.zoho.com/deluge/help/crm/upsert-record.html) — official upsert behavior and response reference.
- Zoho Creator API Reference (https://creator.zoho.com/api/reference) — official location for application, form, report and field link names.
