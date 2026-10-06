schema_version: "1.1"
course_id: "C02"
chapter_id: "C02-CH10"
chapter_number: 10
chapter_title: "Debugging and Maintainable Code"
filename: "C02_CH10_Debugging_and_Maintainable_Code_Student.md"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "partially_verified"
---
Debugging and Maintainable Code
1. What you will learn
An integration can fail even when every individual line looks reasonable. A missing field, wrong API name, expired connection, duplicate retry, recursive workflow or malformed response can produce the same user-facing symptom: “the sync did not work.”
Debugging is the disciplined process of finding the cause rather than changing code randomly. Maintainable code makes that process easier for the next person.
In this chapter, you will learn to:
- collect useful diagnostic information;
- distinguish symptoms from causes;
- trace a failure using business and correlation keys;
- use Deluge exceptions safely;
- separate configuration from code;
- add defensive checks;
- refactor repeated or tangled logic;
- design regression tests;
- review integration code;
- diagnose and refactor a broken integration.
The required practice is to diagnose and refactor a broken Nova Dispatch integration.
Contribution to the course project
This chapter improves the reliability and maintainability of the Chapter 9 integration:
- failures become searchable by business ID and correlation key;
- sensitive values are excluded from logs;
- connection and endpoint values are configurable;
- response classification is reusable;
- retry behavior is explicit;
- duplicate and recursion risks are reduced;
- regression cases protect the Chapter 1 contract.
Continuity from previous chapters
Item	Carried-forward decision
Customer ownership	CRM owns customer identity and service information
Creator ownership	Creator owns Requests, Jobs, inspections and completion workflow
Stable identifiers	NOV-CUST-001, NOV-REQ-001 and NOV-VISIT-001 remain business identifiers
External integration	Nova Dispatch Mock API v1 is fictional and was not executed
Idempotency	External request keys remain stable across retries
Correlation	Each attempt has a separate diagnostic correlation key
Sync states	Pending, Succeeded, Error and Retry Pending remain separate from business status
Access	Technician, Dispatcher, Service Manager and Administrator permissions remain distinct
Previous artifact	C02-CH09_Nova_Field_Service_External_Service_Integration_v0.1.md
2. Lessons
Lesson 1: Diagnose the symptom before changing code
A symptom is what someone observes. A cause is why it happened.
Example:
Symptom:
NOV-VISIT-050 remains in Sync Error.

Possible causes:
- endpoint URL is wrong;
- connection is expired;
- connection lacks permission;
- JSON body is invalid;
- external service returned 409;
- response was successful but parsing failed;
- Creator update failed after the external call;
- a retry created a duplicate.
Do not conclude “the API is down” from one failed record.
Diagnostic questions
Ask these questions in order:
 1. Which business record was being processed?
 2. Which operation was attempted?
 3. Which host and workflow event ran?
 4. Which configuration values were used?
 5. Which connection was selected?
 6. Which correlation key identifies the attempt?
 7. Did the request leave the host?
 8. What response code was received?
 9. Was the response body valid and expected?
10. Did the local update after the external call succeed?
11. Was the operation retried?
12. What state should recovery produce?
Reproduce with a controlled case
Use one synthetic record and one known expected result.
Reproduction field	Example
Business ID	NOV-VISIT-050
External key	EXT-JOB-5050
Environment	Development
Connection	nova_dispatch_oauth_connection_placeholder
Expected result	One external Job
Actual result	Sync Error
Correlation key	sync-NOV-VISIT-050-001
Do not reproduce a failure by repeatedly clicking a production action. A repeated create can become a real duplicate.
Five whys
For a failed sync:
1. Why is the Job in Sync Error?  
The response was classified as a failure.
2. Why was the response classified as a failure?  
The code expected 201, but the service returned 409.
3. Why did the service return 409?  
The external Job already existed.
4. Why did the code try to create it again?  
The previous timeout was treated as unsuccessful and a new idempotency key was generated.
5. Why was a new key generated?  
The code used the attempt key as the business idempotency key.
The root cause is an identity design error, not merely a network error.
Quick check
A user reports that “nothing happened.” Name three different pieces of evidence you would collect before changing the code.
Lesson 2: Log useful diagnostics without leaking data
A log should help you reconstruct what happened. It should not become a copy of customer records or credentials.
A useful diagnostic event includes:
- timestamp;
- host and event;
- business identifier;
- operation;
- correlation key;
- idempotency key or safe hash;
- target environment;
- response code;
- error category;
- retryable flag;
- outcome;
- safe external ID if returned.
Example safe diagnostic map:
diagnostic = Map();
diagnostic.put("business_id", "NOV-VISIT-050");
diagnostic.put("operation", "Create Dispatch Job");
diagnostic.put("correlation_key", "sync-NOV-VISIT-050-001");
diagnostic.put("response_code", 504);
diagnostic.put("category", "Transient Failure");
diagnostic.put("retryable", true);
diagnostic.put("environment", "development");
Avoid logging:
- access tokens;
- client secrets;
- Authorization headers;
- full customer contact details;
- internal notes;
- entire request bodies when they contain sensitive data;
- file contents;
- unredacted error responses that echo credentials.
Deluge diagnostic statements
During development, info can help inspect values and execution flow:
info diagnostic;
Use it carefully:
- log business IDs rather than entire records;
- use consistent labels;
- remove noisy temporary logs after diagnosis;
- preserve important operational outcomes in an audit or status record rather than relying only on transient console output.
Correlation keys
A correlation key links:
Creator record
→ Deluge execution
→ HTTP request
→ external response
→ local sync update
→ support investigation
Use a format that is readable:
sync-NOV-REQ-001-attempt-002
Do not use the same correlation key for unrelated records.
Logging levels
Even if the host does not expose formal logging levels, design them conceptually:
Level	Use
Debug	Temporary development details
Info	Normal state changes and successful operations
Warning	Recoverable abnormal condition
Error	Failed operation requiring correction or retry
Audit	Business decision or access-relevant event
Quick check
Which is safer to log?
Authorization: Bearer eyJ...
or:
connection=nova_dispatch_oauth_connection_placeholder
response_code=403
category=Permission
Explain why.
Lesson 3: Find the cause across boundaries
An integration has at least four boundaries:
1. source record and validation;
2. Deluge function;
3. external request and response;
4. local result update.
A failure at one boundary may appear at another.
Observation	Possible boundary
No correlation key exists	Function did not start or diagnostics are incomplete
Correlation key exists but no external request	Request construction or task execution failed
External service has the record but Creator says timeout	Response was lost or local update failed
Creator is Succeeded but no external ID exists	Response parsing or mapping defect
External record exists twice	Idempotency or reconciliation defect
Retry state never changes	Scheduled worker, claim state or local update defect
Compare before and after values
For updates, capture:
- old Sync Status;
- new Sync Status;
- old external ID;
- new external ID;
- actor or execution identity;
- reason.
A record that changes from Error to Retry Pending is not the same as one that changes from Error to Succeeded.
Inspect the actual request
When using Postman, browser tools or a service console, compare:
- final URL;
- HTTP method;
- query parameters;
- headers excluding secrets;
- JSON body;
- response code;
- response body;
- timing;
- redirect behavior.
A script may contain the correct URL template while the resolved environment value is wrong.
Error categories
Use a stable category rather than copying arbitrary messages:
Validation
Authentication
Permission
Not Found
Conflict
Rate Limit
Timeout
Service Unavailable
Malformed Response
Local Update Failure
Unknown
The category drives recovery. The raw message supports diagnosis.
Quick check
A service shows that DISPATCH-9001 exists, but the Creator Job has Sync_Status = Retry Pending. Which boundary should you inspect first?
Lesson 4: Separate configuration from code
Configuration changes between environments. Code expresses reusable behavior.
Move values such as these out of script logic:
- base URL;
- API version;
- connection name;
- timeout setting;
- retry limit;
- feature flag;
- mock versus production mode;
- module or field API names;
- notification recipient;
- environment label.
A configuration map can make dependencies visible:
config = Map();
config.put("base_url", "https://api.example.com");
config.put("api_version", "v1");
config.put(
    "connection",
    "nova_dispatch_oauth_connection_placeholder"
);
config.put("max_attempts", 3);
config.put("environment", "development");
In a production design, these values may come from approved application configuration rather than a hard-coded map. The code should not silently choose a production endpoint because a developer forgot to change one string.
Configuration validation
Validate configuration at startup or before processing:
configErrors = List();

if(isNull(config.get("base_url")) ||
   isBlank(config.get("base_url")))
{
    configErrors.add("base_url is required");
}

if(isNull(config.get("connection")) ||
   isBlank(config.get("connection")))
{
    configErrors.add("connection is required");
}

if(config.get("max_attempts") <= 0)
{
    configErrors.add("max_attempts must be positive");
}
Do not log a secret while reporting a missing or invalid connection.
Version configuration
A configuration value such as v1 is not proof that an external provider supports that version. It is only a selected contract identifier. The target service documentation must verify:
- current version;
- endpoint;
- required headers;
- scopes;
- request and response schema;
- deprecation status.
Quick check
Why is an environment-specific base URL configuration safer than editing the Deluge source before each deployment?
Lesson 5: Add defensive checks
Defensive programming checks assumptions before relying on them.
For an external response, check:
1. the response exists;
2. the status is available;
3. the status is in the expected category;
4. the body is present when required;
5. JSON parsing succeeds;
6. required fields exist;
7. values have expected types;
8. the local update can be made safely.
Example:
if(isNull(response))
{
    throw {
        "message" : "External service returned no response",
        "data" : {
            "business_id" : jobBusinessId
        }
    };
}

responseCode = response.get("responseCode");

if(isNull(responseCode))
{
    throw {
        "message" : "External response has no response code",
        "data" : {
            "business_id" : jobBusinessId
        }
    };
}
Do not use a defensive check to hide a contract failure:
externalId = ifNull(responseData.getJSON("external_job_id"), "");
If the external ID is required for reconciliation, an empty fallback is dangerous. Return an explicit malformed-response error instead.
Guard local updates
Before updating a Creator record:
- confirm the record still exists;
- confirm its Sync Status is the state expected by this attempt;
- confirm the external key matches;
- confirm the response belongs to this record;
- prevent a stale retry from overwriting a newer success.
A safe update condition is conceptually:
Update only when:
Current Sync_Status = Retry Pending
AND Current External_Request_Key = attempt idempotency key
AND Attempt version is current
Quick check
Why is returning an empty external ID less safe than returning an explicit malformed-response error?
Lesson 6: Refactor for maintainability
Refactoring changes code structure without changing intended behavior.
Signs that refactoring is needed:
- the same response classifier appears in several scripts;
- one function validates, calls a service, updates records and sends emails;
- configuration is repeated in every function;
- errors have inconsistent categories;
- a loop contains a large nested condition;
- tests require real external calls;
- the same business rule is implemented differently in Creator and Flow.
Separate responsibilities
A maintainable integration may use:
Function	Responsibility
validateSyncInput	Validate the local Job map
buildDispatchPayload	Create the request body
buildDispatchHeaders	Create safe headers and keys
classifyDispatchResponse	Categorize status and body
syncOneJob	Execute one external operation
processSyncBatch	Process several Jobs and return per-record results
applySyncResult	Update Creator Sync Status
writeDiagnostic	Store safe diagnostic information
The function names are illustrative; the responsibility boundaries are the important point.
Refactoring sequence
1. Capture current behavior with tests.
2. Identify duplicated or tangled logic.
3. Extract one small function.
4. Run regression tests.
5. Compare outputs.
6. Extract the next responsibility.
7. Keep the change small enough to review.
8. Update documentation and configuration notes.
Do not refactor and change business rules in the same unreviewed change unless the change is explicitly documented.
Example: classifier
map classifyDispatchResponse(number statusCode)
{
    result = Map();

    if(statusCode >= 200 && statusCode < 300)
    {
        result.put("category", "Success");
        result.put("retryable", false);
    }
    else if(statusCode == 409)
    {
        result.put("category", "Conflict");
        result.put("retryable", false);
    }
    else if(statusCode == 401 || statusCode == 403)
    {
        result.put("category", "Permission");
        result.put("retryable", false);
    }
    else if(statusCode == 429 ||
            statusCode == 500 ||
            statusCode == 502 ||
            statusCode == 503 ||
            statusCode == 504)
    {
        result.put("category", "Transient");
        result.put("retryable", true);
    }
    else
    {
        result.put("category", "Non-Retryable");
        result.put("retryable", false);
    }

    return result;
}
This function can be tested without a connection.
Quick check
What is the benefit of extracting response classification into a pure function?
Lesson 7: Use regression and code review
A regression is a previously working behavior that fails after a change.
Regression tests for Nova should cover:
- valid creation;
- duplicate external key;
- 400 invalid request;
- 401 or 403 connection problem;
- 409 existing external action;
- 429 rate limit;
- 503 or 504 transient failure;
- malformed success body;
- local update failure;
- retry after error;
- replay after success;
- authorization and field protection.
A test should identify:
- input;
- setup;
- action;
- expected result;
- observed result;
- cleanup;
- evidence.
Code review checklist
Review the following:
Area	Review question
Contract	Does the payload match the approved external schema?
Identity	Are business, external and product IDs distinct?
Secrets	Are credentials kept in a connection or secret store?
Logging	Are correlation keys present and sensitive values excluded?
Errors	Are status and response shape both checked?
Retry	Is the operation safe to repeat?
State	Can a stale attempt overwrite a newer success?
Limits	Are loops and response sizes bounded?
Access	Does the execution identity have only required permission?
Tests	Are normal and failure paths covered?
Configuration	Are endpoints and connection names environment-specific?
Maintainability	Can another engineer understand and change the logic?
Review comment example
Weak:
This integration is unreliable.
Useful:
The catch block marks every exception as Retry Pending, including missing module and permission errors. Please classify the error first. A 403 should remain Error until permission is corrected, while a timeout may become Retry Pending. Add tests for both paths.
Quick check
Why should a refactor be protected by regression tests even when the intended business behavior has not changed?
3. Visual explanation
From symptom to safe repair
flowchart TD
    S[Observed symptom] --> I[Collect business ID and correlation key]
    I --> B[Check boundary: input, request, response, local update]
    B --> C[Classify cause]
    C -->|configuration| CF[Correct environment configuration]
    C -->|data| DF[Correct validation or mapping]
    C -->|permission| PF[Correct approved connection scope]
    C -->|transient| RF[Use controlled retry]
    C -->|code design| RR[Refactor and add regression test]
    CF --> T[Run regression cases]
    DF --> T
    PF --> T
    RF --> T
    RR --> T
    T --> V[Verify state, logs and duplicate behavior]
Plain-text explanation:
- Start with evidence instead of editing code.
- Use business and correlation keys to locate one operation.
- Inspect each boundary in order.
- Classify the cause as configuration, data, permission, transient or code design.
- Make the smallest safe correction.
- Run normal, failure and replay tests.
- Verify the final local state and diagnostics.
Diagnostic evidence	Meaning
No correlation key	Execution did not reach diagnostic boundary
Request key present, no response code	Transport or runtime failure
403 with valid request	Permission or connection scope issue
409 with external ID	Existing action; reconcile
201 with no external ID	Response contract or parser issue
External success, local Error	Local update or state transition issue
Repeated external IDs	Idempotency or reconciliation defect
4. Worked case
Broken integration
The following script is intended to synchronize assigned Jobs with the Nova Dispatch Mock API.
Host: Creator scheduled workflow  
Input: all Jobs with Job_Status = "Assigned"  
Connection: nova_dispatch_oauth_connection_placeholder  
Expected result: update each Job’s Sync_Status
jobs = Jobs[Job_Status == "Assigned"];

for each job in jobs
{
    payload = Map();
    payload.put("job_business_id", job.Job_Business_ID);
    payload.put("customer_business_id", job.Request.Customer.Customer_Business_ID);
    payload.put("status", job.Job_Status);

    response = invokeurl
    [
        url : "https://api.example.com/v1/jobs"
        type : POST
        body : payload
        connection : "nova_dispatch_oauth_connection_placeholder"
    ];

    if(response.get("responseCode") == 201)
    {
        job.Sync_Status = "Succeeded";
    }
    else
    {
        job.Sync_Status = "Retry Pending";
    }
}
Step 1: Identify the symptoms
Observed outcomes:
Job	Observation
NOV-VISIT-070	External Job created twice
NOV-VISIT-071	Sync_Status says Retry Pending after a 403
NOV-VISIT-072	Function stopped after one malformed response
NOV-VISIT-073	Job was updated to Succeeded but no external ID was stored
Step 2: Diagnose the defects
Defect	Cause	Risk
No idempotency header or stable action key	Replay cannot be reconciled	Duplicate external Jobs
body format is not documented	API may interpret map incorrectly	Invalid payload
No Content-Type header	Server may not parse JSON	Request failure
Every non-201 becomes Retry Pending	Permission and validation errors are retried	Repeated failure and noisy logs
No try-catch	One runtime or parsing error stops the batch	Later Jobs remain unprocessed
No response-body validation	201 without ID is treated as success	Cannot reconcile or support
No correlation key	Attempts cannot be traced	Slow diagnosis
Hard-coded URL	Environment changes require source edits	Wrong environment risk
No claim state	Two schedules can process the same Job	Concurrent duplicates
Direct Sync Status update	Workflow may retrigger itself	Recursion
No per-record result	Batch outcome is invisible	Partial success is hidden
No external ID field update	Local record cannot map to external Job	Future updates are unsafe
Step 3: Define configuration
config = Map();
config.put("base_url", "https://api.example.com");
config.put("api_version", "v1");
config.put(
    "connection",
    "nova_dispatch_oauth_connection_placeholder"
);
config.put("max_records", 50);
config.put("environment", "development");
In production, these values should come from approved environment configuration rather than a hard-coded map.
Step 4: Extract response classification
map classifyResponse(number responseCode)
{
    result = Map();

    if(responseCode >= 200 && responseCode < 300)
    {
        result.put("category", "Success Candidate");
        result.put("retryable", false);
    }
    else if(responseCode == 400)
    {
        result.put("category", "Invalid Request");
        result.put("retryable", false);
    }
    else if(responseCode == 401 || responseCode == 403)
    {
        result.put("category", "Permission");
        result.put("retryable", false);
    }
    else if(responseCode == 409)
    {
        result.put("category", "Conflict");
        result.put("retryable", false);
    }
    else if(responseCode == 429 ||
            responseCode == 500 ||
            responseCode == 502 ||
            responseCode == 503 ||
            responseCode == 504)
    {
        result.put("category", "Transient");
        result.put("retryable", true);
    }
    else
    {
        result.put("category", "Unknown");
        result.put("retryable", false);
    }

    return result;
}
Step 5: Refactor one-record processing
Host: Creator custom function called by a scheduled workflow  
Input: a safe Job map and configuration map  
Connection: named configuration value  
Return: per-record result map
map syncOneAssignedJob(map job, map config)
{
    result = Map();

    businessId = job.get("job_business_id");
    idempotencyKey = job.get("external_request_key");
    attemptNumber = ifNull(job.get("attempt_number"), 1);
    correlationKey = "sync-" + businessId + "-" + attemptNumber;

    if(isNull(businessId) || isBlank(businessId))
    {
        result.put("success", false);
        result.put("category", "Validation");
        result.put("retryable", false);
        result.put("message", "Job business ID is required");
        return result;
    }

    if(isNull(idempotencyKey) || isBlank(idempotencyKey))
    {
        result.put("success", false);
        result.put("category", "Validation");
        result.put("retryable", false);
        result.put("message", "External request key is required");
        return result;
    }

    headers = Map();
    headers.put("Content-Type", "application/json");
    headers.put("Accept", "application/json");
    headers.put("X-Correlation-Key", correlationKey);
    headers.put("Idempotency-Key", idempotencyKey);

    payload = Map();
    payload.put("external_request_key", idempotencyKey);
    payload.put("job_business_id", businessId);
    payload.put("customer_business_id", job.get("customer_business_id"));
    payload.put("status", job.get("job_status"));

    try
    {
        response = invokeurl
        [
            url : config.get("base_url") + "/" + config.get("api_version") + "/jobs"
            type : POST
            headers : headers
            body : payload.toString()
            connection : config.get("connection")
            detailed : true
        ];

        responseCode = response.get("responseCode");
        classification = classifyResponse(responseCode);

        result.put("business_id", businessId);
        result.put("correlation_key", correlationKey);
        result.put("response_code", responseCode);
        result.put("category", classification.get("category"));
        result.put("retryable", classification.get("retryable"));

        if(responseCode == 201)
        {
            responseText = response.get("responseText");
            responseData = responseText.getJSON("data");

            if(isNull(responseData) ||
               isNull(responseData.getJSON("external_job_id")))
            {
                result.put("success", false);
                result.put("category", "Malformed Success");
                result.put("retryable", false);
            }
            else
            {
                result.put("success", true);
                result.put(
                    "external_job_id",
                    responseData.getJSON("external_job_id")
                );
            }
        }
        else if(responseCode == 409)
        {
            responseText = response.get("responseText");
            conflictData = responseText.getJSON("error");

            if(isNull(conflictData) ||
               isNull(conflictData.getJSON("existing_external_job_id")))
            {
                result.put("success", false);
                result.put("category", "Unresolved Conflict");
                result.put("retryable", false);
            }
            else
            {
                result.put("success", true);
                result.put("category", "Reconciled");
                result.put(
                    "external_job_id",
                    conflictData.getJSON("existing_external_job_id")
                );
            }
        }
        else
        {
            result.put("success", false);
        }
    }
    catch(e)
    {
        result.put("success", false);
        result.put("category", "Runtime Exception");
        result.put("retryable", true);
        result.put("correlation_key", correlationKey);
        result.put("error_type", e.type);
        result.put("error_message", e.message);
        result.put("error_line", e.lineNo);
    }

    return result;
}
This code is illustrative and not executed. A production implementation must verify the current invokeurl syntax, response representation, JSON conversion methods and configuration source.
Step 6: Refactor the batch wrapper
map processAssignedJobs(list jobs, map config)
{
    results = List();
    succeeded = 0;
    failed = 0;

    for each job in jobs
    {
        result = syncOneAssignedJob(job, config);
        results.add(result);

        if(result.get("success") == true)
        {
            succeeded = succeeded + 1;
        }
        else
        {
            failed = failed + 1;
        }
    }

    summary = Map();
    summary.put("processed", jobs.size());
    summary.put("succeeded", succeeded);
    summary.put("failed", failed);
    summary.put("results", results);
    return summary;
}
The wrapper does not decide how to update Creator records. That is a separate host operation that can:
- set Sync_Status;
- store External_Job_ID;
- store Last_Correlation_Key;
- store Last_Sync_Error;
- set Retry_Eligible.
Mistake and correction
Mistake: The refactored function returns success = true for every 2xx response.
Why it is wrong: A 202 or 204 may have a different business meaning, and a 201 without an external ID cannot support reconciliation.
Correction: Classify the expected status for the operation and validate the body required by that status.
Mistake: The function updates Sync_Status inside the same workflow that runs whenever Sync_Status changes.
Correction: Separate the result function from the state-update adapter and guard the workflow by source, state change or processing key.
5. Try it yourself — guided practice
Learning goal
Diagnose the broken integration, refactor it into reusable functions and demonstrate that replay, permission and transient failures behave differently.
Host and access requirements
Use Creator development or sandbox. Use the fictional API contract from Chapter 9. Do not send requests to a real external service.
Create these artifacts:
- configuration map or configuration record;
- response classifier;
- single-record sync function;
- batch wrapper;
- per-record result shape;
- diagnostic map;
- regression test table.
Broken-code inputs
Use these mocked results:
job_business_id,external_request_key,response_code,response_body,expected_category
NOV-VISIT-070,EXT-JOB-7070,201,valid external_job_id,Success
NOV-VISIT-071,EXT-JOB-7071,403,permission error,Permission
NOV-VISIT-072,EXT-JOB-7072,504,no complete response,Transient
NOV-VISIT-073,EXT-JOB-7073,201,missing external_job_id,Malformed Success
NOV-VISIT-074,EXT-JOB-7074,409,existing external_job_id,Reconciled
Steps and expected intermediate results
1. Read the broken script and list every assumption it makes.  
Expected result: at least ten defects or risks are documented.
2. Identify the boundary for each defect.  
Expected result: defects are assigned to input, configuration, request, response, local update, retry or maintainability.
3. Extract configuration values.  
Expected result: URL, API version, connection name and retry settings are not embedded in the core function.
4. Write a response classifier.  
Expected result: 403 is non-retryable, 504 is retryable, and 409 is reconciled rather than recreated.
5. Write a single-record function.  
Expected result: it returns a stable result map for every normal or failure path.
6. Add correlation and idempotency keys.  
Expected result: attempts can be traced while the business action remains stable.
7. Add response-body validation.  
Expected result: the malformed 201 becomes an error.
8. Add a batch wrapper.  
Expected result: one failed record does not hide successful records.
 9. Add regression cases.  
Expected result: each supplied row has expected category, retryability and local state.
10. Write a code review summary.  
Expected result: the review identifies remaining product-specific values that must be verified before deployment.
Final artifact
Create:
- C02-CH10_Nova_Field_Service_Debugging_and_Refactor_v0.1.md;
- broken-code diagnosis;
- refactored function set;
- failure taxonomy;
- diagnostic logging specification;
- regression table;
- code review checklist;
- configuration dependency list;
- recovery runbook.
Cleanup
Do not leave a scheduled test workflow enabled. Remove temporary debug output that contains sample payloads or response bodies unless it is intentionally retained in a safe test artifact.
Offline alternative
Perform the diagnosis and refactor on paper or in a Markdown file using the supplied response table. This demonstrates debugging and maintainability but cannot demonstrate actual Deluge execution history or external calls.
6. Independent challenge
Changed constraints
The external service now supports a second operation: updating a Job after a Technician submits inspection results.
 1. A completed Job may be sent only once.
 2. A Job with a failed inspection must not be sent as completed.
 3. A 409 response may indicate an earlier successful update.
 4. A 503 response is retryable.
 5. A 400 response is not retryable until the payload is corrected.
 6. The service returns a successful response with external_job_id but may omit updated_at.
 7. The local Creator update may fail after the external update succeeds.
 8. The next retry must reconcile the external state before sending another update.
 9. The code must support both development and production endpoints through configuration.
10. Logs must not contain internal inspection notes.
Challenge data
job_business_id,external_job_id,job_status,inspection_result,sync_status,attempt_number,response_code,response_shape
NOV-VISIT-080,DISPATCH-9080,Completed,Pass,Succeeded,1,200,complete
NOV-VISIT-081,DISPATCH-9081,Completed,Fail,Pending,1,,not_sent
NOV-VISIT-082,DISPATCH-9082,Completed,Pass,Error,1,503,service_unavailable
NOV-VISIT-083,DISPATCH-9083,Completed,Pass,Error,1,409,existing_state
NOV-VISIT-084,DISPATCH-9084,Completed,Pass,Error,1,400,invalid_payload
NOV-VISIT-085,DISPATCH-9085,Completed,Pass,Error,1,200,missing_updated_at
Deliverables
Produce:
- a diagnosis of the existing update function;
- a refactored updateExternalJob function;
- a reconciliation path for 409;
- a local-update-failure recovery path;
- configuration for development and production;
- safe logging fields;
- regression cases for all six Jobs;
- a review note identifying which failures are retryable.
Success criteria
Your solution succeeds when:
- NOV-VISIT-080 remains successful;
- NOV-VISIT-081 is blocked before external call;
- NOV-VISIT-082 becomes Retry Pending;
- NOV-VISIT-083 is reconciled;
- NOV-VISIT-084 becomes a non-retryable Error;
- NOV-VISIT-085 is treated as a malformed response;
- a local update failure does not cause a duplicate external update;
- configuration selects the endpoint without code changes;
- logs exclude internal inspection notes.
7. Common problems and recovery
Symptom	Diagnosis	Correction
Logs contain full request bodies	Diagnostic scope is too broad	Log safe identifiers and response metadata
Every error is Retry Pending	Error taxonomy is missing	Classify validation, permission, conflict and transient errors
A malformed success is accepted	Status-only checking	Validate required response fields
The same external Job appears twice	New idempotency key on retry	Keep business key stable
Refactor changes business behavior	Refactor and rule change were combined	Add regression tests before extraction
Production URL is in source	Configuration is hard-coded	Move endpoint to environment configuration
Debugging changes are committed permanently	Temporary logging was not removed or documented	Remove or classify logging
A local update failure causes duplicate external update	External and local state are not reconciled	Query or reconcile before retry
try-catch hides all exceptions	Catch block discards context	Return or store category, line, message and correlation key
A stale retry overwrites a newer success	No expected-state check	Require current sync state and attempt version
Large batch exceeds limits	Unbounded loop or call count	Bound batch, page records and schedule remaining work
Code review checks style but not recovery	Review checklist is incomplete	Review identity, state, retry and limits
Reusable function depends on global fields	Hidden context coupling	Pass explicit map and config arguments
Error message exposes connection name or token	Safe diagnostic mapping is missing	Redact sensitive values
8. Check your understanding
 1. What is the difference between a symptom and a root cause?
 2. Which fields should identify one external-call attempt?
 3. Why should a response classifier be a reusable function?
 4. What is wrong with marking all non-201 responses as Retry Pending?
 5. Why should malformed success responses be treated as errors?
 6. What is the benefit of passing configuration into a function?
 7. Why should an older retry not overwrite a newer successful state?
 8. What should a catch block preserve for diagnosis?
 9. Why are regression tests needed after a refactor that “does not change behavior”?
10. Which data must not appear in a normal diagnostic log?
11. A local Creator update fails after the external service returns success. What should the next retry do first?
12. What is one design response to Deluge statement and task limits?
9. Solutions and explanations
Lesson quick checks
1. Collect the business ID, correlation key, response code, operation, environment and local Sync Status before changing code.
2. The safe diagnostic form is:
connection=placeholder
response_code=403
category=Permission
It does not expose a token or customer payload.
3. Inspect the local record’s external ID and correlation history, then query or reconcile the external service before retrying. The external operation may have succeeded even though the local response was lost.
For configuration:
- endpoint and connection values vary by environment;
- source code should express behavior, not deployment-specific addresses;
- configuration validation can fail early without exposing secrets.
For defensive checks, an empty external ID prevents reconciliation. A named malformed-response failure is safer than silently storing an empty value.
For refactoring, a pure classifier can be tested with status codes and does not need a live connection. This reduces test cost and makes behavior explicit.
For regression, structure can change in ways that alter null handling, retry categories or response parsing even if the business requirement remains the same.
Worked-case diagnosis
The broken integration contains these major defects:
 1. no connection or environment configuration;
 2. no Content-Type header;
 3. no Accept header;
 4. no correlation key;
 5. no idempotency key;
 6. no input validation;
 7. no try-catch;
 8. no response-body validation;
 9. no conflict reconciliation;
10. all failures marked Retry Pending;
11. no local expected-state check;
12. no per-record result;
13. possible workflow recursion after Sync Status update;
14. no bounded batch size;
15. no safe diagnostic record;
16. no separate configuration and code;
17. no protection from concurrent schedules;
18. no external ID mapping.
Expected mock results:
Job	Category	Retryable	Local state
NOV-VISIT-070	Success	No	Succeeded
NOV-VISIT-071	Permission	No	Error
NOV-VISIT-072	Transient	Yes	Retry Pending
NOV-VISIT-073	Malformed Success	No	Error
NOV-VISIT-074	Reconciled	No	Succeeded or Reconciled
Guided-practice sample solution
A suitable refactoring boundary is:
validateSyncInput
classifyResponse
buildPayload
syncOneJob
processSyncBatch
applySyncResult
The batch result should preserve successful items:
{
  "processed": 5,
  "succeeded": 2,
  "failed": 3,
  "results": [
    {
      "business_id": "NOV-VISIT-070",
      "category": "Success",
      "retryable": false
    },
    {
      "business_id": "NOV-VISIT-071",
      "category": "Permission",
      "retryable": false
    },
    {
      "business_id": "NOV-VISIT-072",
      "category": "Transient",
      "retryable": true
    },
    {
      "business_id": "NOV-VISIT-073",
      "category": "Malformed Success",
      "retryable": false
    },
    {
      "business_id": "NOV-VISIT-074",
      "category": "Reconciled",
      "retryable": false
    }
  ]
}
Safe review findings:
- configuration values should not be hard-coded;
- response classification should be centralized;
- 409 must reconcile;
- 504 can be Retry Pending;
- 403 must remain Error;
- malformed success must not update external ID;
- correlation key and attempt number must be stored;
- local state updates need recursion and stale-attempt guards.
Independent-challenge sample solution
Expected results:
Job	Result	Reason
NOV-VISIT-080	Succeeded	Complete successful response
NOV-VISIT-081	Blocked before call	Inspection failed
NOV-VISIT-082	Retry Pending	503 is transient
NOV-VISIT-083	Reconciled	409 identifies an existing external state
NOV-VISIT-084	Error	400 requires payload correction
NOV-VISIT-085	Error	Required updated_at is missing
For NOV-VISIT-082, the next attempt uses:
- the same external Job ID;
- the same business action key;
- a new correlation key;
- an incremented attempt number.
For NOV-VISIT-083, the function should first retrieve or inspect the existing external state. It must not issue another update simply because the local record says Error.
For a local update failure after external success:
1. record the external ID and response evidence in a recovery record if possible;
2. set local state to Reconciliation Required;
3. on retry, query the external service or use the idempotent update operation;
4. update local state from the known external result;
5. do not create a new external action.
A safe configuration structure is:
development:
  base_url: https://api.example.com
  api_version: v1
  connection: nova_dispatch_dev_connection_placeholder

production:
  base_url: verified-production-endpoint
  api_version: verified-version
  connection: nova_dispatch_prod_connection_placeholder
The exact production values must be verified before deployment.
10. Chapter recap and next step
You should now be able to:
- distinguish symptoms from root causes;
- trace an operation using business and correlation keys;
- log useful diagnostics without exposing secrets;
- classify errors consistently;
- separate configuration from reusable code;
- add defensive response and state checks;
- use try-catch without hiding the cause;
- refactor a large integration into testable functions;
- preserve successful records during partial failure;
- design stale-attempt and recursion protection;
- use regression tests and code review to preserve behavior;
- diagnose and refactor a broken integration.
Your project artifact from this chapter is:
C02-CH10_Nova_Field_Service_Debugging_and_Refactor_v0.1.md
It should contain the broken-code diagnosis, refactored function set, diagnostic fields, configuration dependencies, regression cases, code review checklist and recovery runbook.
Chapter 11 moves from Deluge integration tasks to CRM REST API foundations. It will cover current API versions, module and field API names, metadata, CRUD, search, related records, attachments, pagination, API credits, concurrency limits and error interpretation.
11. Glossary and further reading
Glossary
Correlation key  
An identifier that links one execution attempt to its request, response, logs and recovery record.
Defensive check  
A validation that confirms an assumption before code relies on it.
Diagnostic event  
A structured record of an operation, its inputs, outcome and useful investigation metadata.
Malformed response  
A response that has an expected transport result but does not contain the required business fields or structure.
Refactoring  
Changing code structure while preserving intended behavior.
Regression  
A previously working behavior that fails after a change.
Root cause  
The underlying condition that produced a symptom.
Stale attempt  
An older operation result that arrives after a newer attempt has already changed the record.
Structured logging  
Recording diagnostics as named fields rather than unstructured text.
Transient failure  
A failure that may resolve after time or controlled retry.
Further reading
- Zoho Deluge Try-Catch (https://www.zoho.com/deluge/help/misc-statements/try-catch.html) — official exception handling and exception attributes.
- Zoho Deluge Throw (https://www.zoho.com/deluge/help/misc-statements/throw.html) — official user-defined errors and propagation.
- Zoho Deluge Limitations (https://www.zoho.com/deluge/help/limitations.html) — official statement, task, response and recursion limitations.
- Zoho Deluge Connections (https://www.zoho.com/deluge/help/deluge-connections.html) — official connection and authentication reference.
- Zoho Deluge Integration Tasks (https://www.zoho.com/deluge/help/integration-tasks.html) — official integration boundaries and call behavior.
- Zoho Creator Resource Center (https://www.zoho.com/creator/help/) — official operations, environments, Deluge and application documentation.
- Zoho Creator Environments (https://help.zoho.com/portal/en/kb/creator/developer-guide/environments) — official environment documentation for safe development and testing.
continuity:
  record_ids:
    customer: "NOV-CUST-001"
    request: "NOV-REQ-001"
    visit: "NOV-VISIT-001"
  carried_forward_decisions:
    - "CRM remains authoritative for customer identity and service information."
    - "Creator owns requests, jobs or visits, inspections and completion workflow."
    - "Customer_Reference, Service_Requests, Technicians and Jobs remain the core Creator forms."
    - "Inspection_Items remains a Job subform."
    - "Request_Status, Job_Status and Sync_Status remain separate lifecycles."
    - "Technician access is restricted to assigned Jobs."
    - "External request keys prevent duplicate business actions."
    - "Correlation keys identify individual attempts."
    - "Timeouts and remote failures preserve local business records and produce recoverable states."
  chapter_10_artifacts:
    - "C02-CH10_Nova_Field_Service_Debugging_and_Refactor_v0.1.md"
    - "Broken-code diagnosis"
    - "Refactored function set"
    - "Diagnostic logging specification"
    - "Configuration dependency list"
    - "Regression test table"
    - "Code review checklist"
    - "Recovery runbook"
  refactoring_boundaries:
    - "validateSyncInput"
    - "classifyDispatchResponse"
    - "buildDispatchPayload"
    - "buildDispatchHeaders"
    - "syncOneJob"
    - "processSyncBatch"
    - "applySyncResult"
    - "writeSafeDiagnostic"
  open_case_assumptions:
    - "The external service remains the fictional Nova Dispatch Mock API v1 and no external call has been executed."
    - "Exact runtime logging, operations-history and environment-management views depend on the target Creator environment."
    - "Actual Deluge limits can change and must be checked against current official documentation before release."
    - "Production endpoint, connection, API version, scopes and response contract remain implementation dependencies."
    - "A local update failure after remote success requires reconciliation before another remote write."
END OF C02-CH10
