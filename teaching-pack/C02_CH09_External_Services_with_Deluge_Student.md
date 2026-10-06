schema_version: "1.1"
course_id: "C02"
chapter_id: "C02-CH09"
chapter_number: 9
chapter_title: "External Services with Deluge"
filename: "C02_CH09_External_Services_with_Deluge_Student.md"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "partially_verified"
---
External Services with Deluge
1. What you will learn
A Creator application often needs to communicate with another service. Nova Field Service must exchange approved information with CRM and may later connect to dispatch, messaging, document or field-service systems.
An external call is more than a URL. It includes:
- authentication;
- endpoint and HTTP method;
- path and query parameters;
- headers;
- request body;
- JSON or file encoding;
- timeout behavior;
- response-code interpretation;
- retry and duplicate protection;
- logging and recovery.
In this chapter, you will learn to:
- use connections for authenticated services;
- construct an invokeurl request;
- distinguish headers, query parameters, form data and JSON bodies;
- parse JSON responses;
- handle files conceptually and safely;
- classify HTTP response codes;
- catch runtime exceptions;
- design retryable and non-retryable failures;
- respect execution and response-size limits.
The required practice is to integrate an external service and document failure handling.
Contribution to the course project
This chapter extends the Chapter 8 local data operations into an external synchronization boundary:
Creator Job or Request
        ↓
Deluge integration function
        ↓
External service
        ↓
Response classification
        ↓
Sync status, audit result and recovery
The design preserves the Chapter 1 rules:
- Creator owns operational Requests and Jobs;
- CRM owns customer identity and service information;
- external calls must not create duplicate business actions;
- integration failures remain visible and recoverable.
External-service accuracy boundary
The external API examples in this chapter use a fictional service:
Nova Dispatch Mock API v1
Base URL: https://api.example.com
This is a teaching contract. It is not a Zoho API, has not been executed and does not define a real vendor’s version, scope, data centre or quota.
For actual Zoho CRM and Creator APIs, confirm the current official API documentation, regional endpoint, module and field API names, OAuth scopes and connection requirements before implementation. Those product-specific contracts are covered in later API chapters.
2. Lessons
Lesson 1: Use connections instead of embedding credentials
A connection stores authorization details so a Deluge script can call another service without placing a token or secret in source code.
The official Deluge connection documentation describes connections for Zoho and third-party services and supports authentication patterns such as API key, Basic authentication and OAuth 2, depending on the service.
A connection has:
- a service definition;
- an authentication type;
- credentials or authorization state;
- scopes or permissions;
- a link name used by Deluge;
- an owner or administration process;
- a lifecycle for renewal and revocation.
Use a descriptive placeholder:
nova_dispatch_oauth_connection_placeholder
The placeholder is not a secret and does not authenticate anything.
Connection design
Design item	Nova question
Service	Which external dispatch service is being called?
Environment	Is this mock, development, test or production?
Authentication	API key, OAuth 2 or another supported method?
Scope	What minimum operations are needed?
Owner	Which Administrator owns renewal and revocation?
Region	Which regional endpoint applies?
Secret storage	Where is the credential stored?
Failure	What happens when the connection expires or lacks permission?
Use the minimum scope required. A Job-status update connection should not automatically receive permission to delete customer records.
Connection ownership
A connection may be technically used by a scheduled function but owned by an Administrator or integration service identity.
Document:
- who created it;
- who can edit it;
- where it is used;
- which environments use it;
- how it is rotated;
- what happens when it is revoked.
Do not copy access tokens into:
- Deluge source;
- screenshots;
- Postman collections;
- Git;
- error messages;
- customer-visible notifications.
Quick check
1. Why is connection: "nova_dispatch_oauth_connection_placeholder" safer than placing an access token in a script?
2. What should happen if a connection has permission to read but not update a Job?
3. Who should own a production integration connection?
Lesson 2: Construct an invokeurl request
invokeurl is the Deluge task used to call a web service when a built-in integration task is not sufficient.
Host: Creator custom function, Creator workflow, CRM function or Flow Deluge action  
Input: URL, method, headers, parameters or body and connection  
Connection: approved connection link name where supported  
Return: text, map, file or detailed response depending on the task options and endpoint
Illustrative syntax:
headers = Map();
headers.put("Content-Type", "application/json");
headers.put("Accept", "application/json");

requestBody = Map();
requestBody.put("external_request_key", "EXT-REQ-1001");
requestBody.put("job_business_id", "NOV-VISIT-001");
requestBody.put("job_status", "Started");

response = invokeurl
[
    url : "https://api.example.com/v1/jobs"
    type : POST
    headers : headers
    body : requestBody.toString()
    connection : "nova_dispatch_oauth_connection_placeholder"
    detailed : true
];
This is illustrative Deluge for a Creator custom function. The fictional endpoint is not live. Confirm the exact invokeurl options supported by the target editor before execution.
Request anatomy
Part	Example	Purpose
URL	https://api.example.com/v1/jobs	Resource endpoint
Method	POST	Requested operation
Headers	Content-Type, Accept	Format and behavior metadata
Query parameters	?region=North	Filters or options in the URL
Body	JSON text	Data sent to the service
Connection	Named connection	Authentication
Detailed response	true	Access response status and headers
Do not use a request body for values that belong in query parameters according to the external contract. Do not put sensitive values in query strings unless the service explicitly requires it and the risk is accepted.
GET example
headers = Map();
headers.put("Accept", "application/json");

response = invokeurl
[
    url : "https://api.example.com/v1/jobs/NOV-VISIT-001"
    type : GET
    headers : headers
    connection : "nova_dispatch_oauth_connection_placeholder"
    detailed : true
];
A GET request should not create a new business action.
POST example
response = invokeurl
[
    url : "https://api.example.com/v1/jobs"
    type : POST
    headers : headers
    body : requestBody.toString()
    connection : "nova_dispatch_oauth_connection_placeholder"
    detailed : true
];
A POST may create a resource or business action. Use an external request or idempotency key when replay is possible.
PUT and PATCH
Use the method required by the external API contract:
- PUT commonly replaces a resource representation;
- PATCH commonly changes selected fields.
Do not choose a method because it “sounds right.” Follow the verified external contract.
Quick check
1. What does the Accept header communicate?
2. Why must a POST operation use a duplicate-protection key in Nova?
3. What is the difference between a query parameter and a JSON body field?
Lesson 3: Use headers, parameters and bodies correctly
Headers
Headers describe the request and may carry authorization or correlation information.
Useful headers include:
headers = Map();
headers.put("Content-Type", "application/json");
headers.put("Accept", "application/json");
headers.put("X-Correlation-Key", "sync-NOV-REQ-001-001");
headers.put("Idempotency-Key", "EXT-REQ-1001");
Whether an external service supports Idempotency-Key is a contract question. Do not add a header and assume the server will enforce it.
Do not log authorization headers or secrets.
Query parameters
A query parameter changes retrieval or processing options:
GET /v1/jobs?region=North&status=Scheduled
When building a URL, encode values according to the service contract. A customer description containing spaces, & or ? must not accidentally alter the query.
Form parameters
Some services require URL-encoded form data:
Content-Type: application/x-www-form-urlencoded
The exact body and header requirements belong to the service documentation.
JSON bodies
For a JSON body:
{
  "external_request_key": "EXT-REQ-1001",
  "job_business_id": "NOV-VISIT-001",
  "job_status": "Started"
}
Keep the payload limited to fields the external service needs. Do not send CRM record IDs, internal notes or customer data without a contract and purpose.
Correlation and idempotency
Use two different concepts:
- Correlation key: tracks one attempt or message across logs.
- Idempotency key: identifies the business action that must not repeat.
Example:
Business action: EXT-REQ-1001
Attempt 1: sync-EXT-REQ-1001-001
Attempt 2: sync-EXT-REQ-1001-002
The attempt key can change for each retry. The idempotency key remains the same.
Quick check
Why should the correlation key change between attempts while the idempotency key remains stable?
Lesson 4: Parse JSON and validate the response
An HTTP response can have:
- a transport status;
- response headers;
- response text;
- JSON data;
- an error body;
- an empty body;
- invalid JSON.
Do not parse before checking whether a body exists and whether the response format is expected.
A response may be represented by a detailed map such as:
{
  "responseCode": 201,
  "responseHeader": {
    "content-type": "application/json"
  },
  "responseText": "{\"data\":{\"job_id\":\"EXT-JOB-001\",\"status\":\"accepted\"}}"
}
Illustrative parsing:
statusCode = response.get("responseCode");
responseText = response.get("responseText");

if(statusCode >= 200 && statusCode < 300)
{
    body = responseText.getJSON("data");
    externalJobId = body.getJSON("job_id");
}
Deluge provides JSON-related functions such as getJSON and toJSONList. If a JSON array is returned, convert it to a list before looping:
itemsText = responseText.getJSON("items");
items = itemsText.toJSONList();

for each item in items
{
    itemId = item.getJSON("id");
    info itemId;
}
The exact response representation depends on the invokeurl options and target service. Inspect the value before assuming it is already a map.
Validate shape, not only status
This is unsafe:
if(statusCode == 200)
{
    syncStatus = "Succeeded";
}
A successful transport response may still omit the expected business result.
Use:
if(statusCode >= 200 && statusCode < 300)
{
    if(isNull(responseText) || isBlank(responseText))
    {
        syncStatus = "Error";
        errorCategory = "Missing response body";
    }
    else
    {
        responseData = responseText.getJSON("data");

        if(isNull(responseData) ||
           isNull(responseData.getJSON("job_id")))
        {
            syncStatus = "Error";
            errorCategory = "Unexpected response shape";
        }
        else
        {
            syncStatus = "Succeeded";
        }
    }
}
Quick check
Why can a 200 response still be a synchronization failure?
Lesson 5: Classify response codes and failures
Use response codes and body details to decide what to do.
Response	Category	Nova behavior
200 or 201	Success candidate	Validate body and store external ID
204	Success with no body	Mark success only if the operation contract expects no body
400	Invalid request	Correct payload; do not retry unchanged
401	Authentication failure	Check connection or token state
403	Permission failure	Request approved scope or permission
404	Not found	Verify endpoint or external ID
409	Duplicate or conflict	Find existing business action; do not create a second
413	Payload too large	Reduce or split payload
429	Rate limit	Retry according to Retry-After or approved backoff
500	Server error	Record failure; retry only if safe
502, 503, 504	Gateway or availability failure	Retry with same idempotency key
Invalid JSON	Contract or service failure	Store raw-safe diagnostic and mark error
A retry decision depends on both the status and the business operation.
For example:
POST create job + 504:
retry may be safe only with the same idempotency key.

POST create job + 400:
do not retry unchanged.

POST create job + 409:
look for the existing external job.

GET status + 504:
retry may be safe because GET is read-oriented, subject to limits.
Try-catch
Deluge supports try-catch for runtime exceptions.
Host: Creator custom function  
Connection: approved connection placeholder  
Return: structured result map
result = Map();

try
{
    response = invokeurl
    [
        url : "https://api.example.com/v1/jobs/NOV-VISIT-001"
        type : GET
        headers : {"Accept":"application/json"}
        connection : "nova_dispatch_oauth_connection_placeholder"
        detailed : true
    ];

    result.put("success", true);
    result.put("response", response);
}
catch(e)
{
    result.put("success", false);
    result.put("error_type", e.type);
    result.put("error_message", e.message);
    result.put("error_line", e.lineNo);
}

return result;
Use try-catch for runtime failures such as invalid data, parsing errors or task exceptions. It does not make a business operation safe to retry automatically.
Throw business errors
Use throw when a business rule should stop processing:
if(isNull(jobId))
{
    throw {
        "message" : "Job ID is required",
        "data" : {
            "business_id" : jobBusinessId
        }
    };
}
Catch the exception at the host boundary and decide whether to alert, store an error, return a failure map or retry.
Quick check
Which of these should normally be retried without changing the request: 400, 403, 409 or 504? Explain the exception for a 409.
Lesson 6: Handle files safely
External services may accept or return:
- inspection photographs;
- completion documents;
- CSV exports;
- PDF reports;
- JSON metadata with a file URL.
Files require additional decisions:
- file type;
- maximum size;
- filename;
- content type;
- sensitivity;
- retention;
- access permission;
- retry behavior;
- whether the external service returns a file ID or URL.
File upload context
Host: Creator Job form On Success or Creator custom function  
Input: approved Creator File Upload field  
Connection: external-service connection placeholder  
Output: external file ID or structured error
The exact multipart syntax depends on the current invokeurl task and target service. A clearly labelled illustrative shape is:
PSEUDOCODE — verify exact file parameter syntax in the target Deluge editor

fileHeaders = Map();
fileHeaders.put("Accept", "application/json");

fileResponse = invokeurl
[
    url : "https://api.example.com/v1/jobs/NOV-VISIT-001/attachments"
    type : POST
    headers : fileHeaders
    files : {"inspection_photo" : input.Inspection_Photo}
    connection : "nova_dispatch_oauth_connection_placeholder"
    detailed : true
];
This is pseudocode because the target service’s multipart field name and current task syntax must be verified. Do not claim that this file call was executed.
File download
A file response should not be parsed as JSON unless the endpoint returns JSON metadata. Store or hand off the file using a supported file operation and record:
- external file ID;
- filename;
- content type;
- size;
- source Job ID;
- upload status;
- retry status.
Do not expose an internal file URL to a customer without checking its access and lifetime.
File failure
If an attachment upload fails after the Job is saved:
Job remains saved.
Attachment_Status = Error.
Attachment_Retry_Eligible = true or false.
The external file action is retried with the same business attachment key.
Do not mark the Job complete merely because the text fields were saved if the inspection photo is a required completion artifact.
Quick check
Why should a file upload have its own status instead of being represented only by Job_Status?
Lesson 7: Respect timeouts and execution limits
External calls are slow compared with local variable operations. A script may fail because of:
- network delay;
- service timeout;
- response size;
- too many statements;
- too many external calls;
- loops that make one call per record;
- oversized file;
- expired connection;
- service rate limit.
The official Deluge limitations documentation states that limits can change and should be verified. It currently documents examples including:
- maximum statements executed in one function;
- recursive function-call limits;
- daily email, webhook and integration-task limits;
- an invokeurl response-size limit;
- file and attachment constraints in related tasks.
Treat published limits as environment-dependent operational constraints, not as a reason to build an unbounded loop.
Safe external-call pattern
 1. Validate locally.
 2. Select a bounded set of records.
 3. Mark a record as in progress.
 4. Build one request.
 5. Call the service.
 6. Capture status and correlation key.
 7. Parse and validate the response.
 8. Update success or failure state.
 9. Release the claim.
10. Continue or stop according to the failure policy.
Avoid:
for every inspection row:
    call external service
Prefer:
collect all approved inspection data
build one bounded request
call external service once
record one response
Timeout recovery
A timeout does not prove that the external service did nothing. The request may have reached the service even though the response did not return.
Therefore:
- reuse the same idempotency key;
- check for an existing external action before creating another;
- do not blindly create a second resource;
- preserve the first attempt key;
- classify the result as Unknown Outcome until reconciled.
Quick check
Why is a timeout during a create request more dangerous than a timeout during a read request?
3. Visual explanation
External-call decision flow
flowchart TD
    S[Saved Creator record] --> V[Validate local data]
    V -->|invalid| E[Store validation error]
    V -->|valid| C[Claim sync attempt]
    C --> B[Build URL headers and body]
    B --> A[Invoke external service]
    A --> T{Transport result}
    T -->|runtime exception| X[Catch and store retryable error]
    T -->|4xx validation or permission| N[Non-retryable error]
    T -->|409 conflict| D[Find existing external action]
    T -->|429 5xx timeout| R[Retry pending with same key]
    T -->|2xx| J[Validate JSON response]
    J -->|expected| Y[Store external ID and success]
    J -->|unexpected| U[Store response-shape error]
Plain-text explanation:
- The local record is validated before any external call.
- A claim prevents concurrent processing.
- The request includes a stable idempotency key and a per-attempt correlation key.
- Runtime exceptions and HTTP responses are handled separately.
- A conflict leads to reconciliation, not a second create.
- A timeout produces an unknown-outcome or retry state.
- A success status still requires response-shape validation.
- Every path stores a useful result for support and later reconciliation.
Failure layer	Example	Recovery
Local validation	Missing Job ID	Correct data; no call
Authentication	Expired OAuth connection	Renew or replace connection
Authorization	Insufficient service scope	Request approved scope
Transport	Timeout	Retry or reconcile with same key
HTTP contract	400	Correct request
Business conflict	409	Find existing action
Response contract	Missing external ID	Mark error and investigate
Limit	Response or file too large	Split, reduce or redesign
4. Worked case
Case inputs
Nova sends an assigned Job to the fictional Nova Dispatch Mock API.
Mock request contract:
Method: POST
URL: https://api.example.com/v1/jobs
Mock contract version: v1
Authentication: connection placeholder only
Request body: JSON
Required fields:
  external_request_key
  job_business_id
  customer_business_id
  status
  scheduled_start
The mock service returns these expected responses:
Normal response:
{
  "responseCode": 201,
  "responseText": "{\"data\":{\"external_job_id\":\"DISPATCH-9001\",\"status\":\"accepted\"}}"
}
Duplicate response:
{
  "responseCode": 409,
  "responseText": "{\"error\":{\"code\":\"DUPLICATE_KEY\",\"existing_external_job_id\":\"DISPATCH-9001\"}}"
}
Permission response:
{
  "responseCode": 403,
  "responseText": "{\"error\":{\"code\":\"FORBIDDEN\",\"message\":\"Connection cannot create jobs\"}}"
}
Timeout result:
No complete response is received.
The mock outputs are expected examples, not observed results.
Step 1: Build the request
Host: Creator custom function  
Input: a map containing a Creator Request and Job mapping  
Connection: nova_dispatch_oauth_connection_placeholder  
Supported tasks: map/list functions, invokeurl, try-catch  
Return: result map with success, category, external ID and diagnostics
map syncJobToDispatch(map job)
{
    result = Map();
    attemptKey = "sync-" + job.get("job_business_id") + "-001";
    idempotencyKey = job.get("external_request_key");

    headers = Map();
    headers.put("Content-Type", "application/json");
    headers.put("Accept", "application/json");
    headers.put("X-Correlation-Key", attemptKey);
    headers.put("Idempotency-Key", idempotencyKey);

    requestBody = Map();
    requestBody.put("external_request_key", idempotencyKey);
    requestBody.put("job_business_id", job.get("job_business_id"));
    requestBody.put("customer_business_id", job.get("customer_business_id"));
    requestBody.put("status", job.get("job_status"));
    requestBody.put("scheduled_start", job.get("scheduled_start"));

    try
    {
        response = invokeurl
        [
            url : "https://api.example.com/v1/jobs"
            type : POST
            headers : headers
            body : requestBody.toString()
            connection : "nova_dispatch_oauth_connection_placeholder"
            detailed : true
        ];

        result.put("attempt_key", attemptKey);
        result.put("idempotency_key", idempotencyKey);
        result.put("raw_response_available", true);
        result.put("response", response);
    }
    catch(e)
    {
        result.put("success", false);
        result.put("category", "Runtime Exception");
        result.put("retryable", true);
        result.put("attempt_key", attemptKey);
        result.put("error_message", e.message);
        result.put("error_line", e.lineNo);
        return result;
    }

    responseCode = response.get("responseCode");
    responseText = response.get("responseText");

    result.put("response_code", responseCode);

    if(responseCode == 201)
    {
        responseData = responseText.getJSON("data");

        if(isNull(responseData) ||
           isNull(responseData.getJSON("external_job_id")))
        {
            result.put("success", false);
            result.put("category", "Unexpected Response");
            result.put("retryable", false);
        }
        else
        {
            result.put("success", true);
            result.put("category", "Created");
            result.put("retryable", false);
            result.put(
                "external_job_id",
                responseData.getJSON("external_job_id")
            );
        }
    }
    else if(responseCode == 409)
    {
        conflictData = responseText.getJSON("error");

        result.put("success", true);
        result.put("category", "Already Exists");
        result.put("retryable", false);
        result.put(
            "external_job_id",
            conflictData.getJSON("existing_external_job_id")
        );
    }
    else if(responseCode == 401 || responseCode == 403)
    {
        result.put("success", false);
        result.put("category", "Authentication or Permission");
        result.put("retryable", false);
    }
    else if(responseCode == 429 ||
            responseCode == 500 ||
            responseCode == 502 ||
            responseCode == 503 ||
            responseCode == 504)
    {
        result.put("success", false);
        result.put("category", "Transient Failure");
        result.put("retryable", true);
    }
    else
    {
        result.put("success", false);
        result.put("category", "Non-Retryable HTTP Failure");
        result.put("retryable", false);
    }

    return result;
}
This code is illustrative and was not executed. The exact detailed-response fields and JSON conversion behavior must be verified in the target Deluge editor.
Step 2: Interpret the results
Mock result	Function category	Creator state
201 with external ID	Created	Sync_Status = Succeeded
409 with existing ID	Already Exists	Sync_Status = Succeeded or Reconciled
403	Authentication or Permission	Sync_Status = Error; support required
504 or runtime timeout	Transient Failure	Sync_Status = Retry Pending
201 without external ID	Unexpected Response	Sync_Status = Error
400	Non-Retryable HTTP Failure	Sync_Status = Error
A 409 is treated as a successful reconciliation only because the response identifies the existing external Job. If the conflict body does not identify the existing action, mark it as unresolved rather than assuming success.
Step 3: Update Creator state
After the function returns, a Creator workflow can update local fields:
syncResult = syncJobToDispatch(jobMap);

if(syncResult.get("success") == true)
{
    jobRecord.Sync_Status = "Succeeded";
    jobRecord.External_Job_ID = syncResult.get("external_job_id");
}
else if(syncResult.get("retryable") == true)
{
    jobRecord.Sync_Status = "Retry Pending";
    jobRecord.Last_Sync_Error = syncResult.get("category");
}
else
{
    jobRecord.Sync_Status = "Error";
    jobRecord.Last_Sync_Error = syncResult.get("category");
}
The local update must also include the attempt key and timestamp in a production design.
Step 4: File attachment design
Suppose a required inspection photograph must be sent after Job completion.
Required mapping:
Creator value	External value
Job Business ID	External job reference
File Upload field	Multipart attachment
File name	External file name
Content type	MIME type
Inspection result	Attachment metadata
Correlation key	Upload attempt identifier
The file operation needs its own state:
Attachment_Status:
Not Required
Pending
Uploaded
Error
Retry Pending
A failed file upload does not automatically mean the Job itself is invalid, unless the business completion rule says that the photograph is mandatory.
Mistake and correction
Mistake: A timeout occurs after the POST request. The developer sends another POST with a new idempotency key.
Why it is wrong: The first request may have succeeded even though the response was lost. A second key may create a duplicate external Job.
Correction: Keep the original idempotency key, reconcile with a GET or idempotent retry, and use the same key for the next attempt.
A second mistake is logging the full Authorization header and JSON body, including customer data, to diagnose a failure.
Correction: Log only:
- business ID;
- attempt key;
- response code;
- safe error category;
- external ID if returned;
- redacted diagnostic values.
5. Try it yourself — guided practice
Learning goal
Implement and document a Deluge function that sends a Creator Job to the Nova Dispatch Mock API and handles normal, duplicate, permission, timeout and malformed-response cases.
Host and access requirements
Use a Creator development or sandbox environment. The external endpoint is fictional and should not be treated as live.
Create or document:
- a custom connection named nova_dispatch_oauth_connection_placeholder;
- mock contract version v1;
- no production secret;
- no real customer data;
- an audit or sync result field on the test Job if available.
Sample inputs
job_business_id,external_request_key,customer_business_id,job_status,scheduled_start,expected_scenario
NOV-VISIT-050,EXT-JOB-5050,NOV-CUST-001,Assigned,2026-10-12T09:00:00Z,created
NOV-VISIT-051,EXT-JOB-5051,NOV-CUST-002,Assigned,2026-10-12T10:00:00Z,duplicate
NOV-VISIT-052,EXT-JOB-5052,NOV-CUST-001,Assigned,2026-10-12T11:00:00Z,permission_denied
NOV-VISIT-053,EXT-JOB-5053,NOV-CUST-002,Assigned,2026-10-12T12:00:00Z,timeout
NOV-VISIT-054,EXT-JOB-5054,NOV-CUST-001,Assigned,2026-10-12T13:00:00Z,malformed_success
Expected mock responses:
job_business_id,response_code,response_body_shape,expected_category,retryable
NOV-VISIT-050,201,data.external_job_id,Created,false
NOV-VISIT-051,409,error.existing_external_job_id,Already Exists,false
NOV-VISIT-052,403,error.code,Authentication or Permission,false
NOV-VISIT-053,504,error.code or no response,Transient Failure,true
NOV-VISIT-054,201,data missing external_job_id,Unexpected Response,false
Steps and expected intermediate results
 1. Write the mock contract into the integration artifact.  
Expected result: the endpoint, mock version, request fields, response shapes and non-execution status are clear.
 2. Build a request map from the Job input.  
Expected result: the payload contains only approved fields.
 3. Add X-Correlation-Key and Idempotency-Key.  
Expected result: the attempt key and business key are distinct.
 4. Add a named connection placeholder.  
Expected result: no secret or token appears in the script.
 5. Add try-catch.  
Expected result: runtime failures return a structured retryable result.
 6. Inspect the response code before parsing the body.  
Expected result: a 403 is not parsed as a successful Job.
 7. Validate the response shape for 201.  
Expected result: a 201 without external_job_id is an error.
 8. Handle 409 by storing the existing external ID.  
Expected result: a duplicate is reconciled rather than recreated.
 9. Update local Sync_Status according to the result.  
Expected result:
- Created → Succeeded;
- Already Exists → Reconciled;
- Permission → Error;
- Timeout → Retry Pending;
- Malformed response → Error.
10. Add a file-attachment design note.  
Expected result: file status, size, type, retry behavior and customer visibility are documented.
11. Add execution-limit and call-volume notes.  
Expected result: no unbounded loop or large response is assumed safe.
Final artifact
Create:
- C02-CH09_Nova_Field_Service_External_Service_Integration_v0.1.md;
- Deluge integration function;
- mock request and response contract;
- connection record;
- response classification table;
- retry and reconciliation design;
- file-handling note;
- execution-limit note;
- five scenario results.
Cleanup
Disable or delete any training connection, workflow or test function that is not needed later. Remove synthetic credentials and temporary files.
Offline alternative
Write the integration function, mock responses and failure-handling matrix without calling a service. This demonstrates request construction and recovery reasoning but cannot demonstrate real network behavior, connection authorization or file transfer.
6. Independent challenge
Changed constraints
Nova now sends completion summaries to a fictional customer-notification service:
1. Only completed Jobs may be sent.
2. A completed Job must have all required inspection results equal to Pass.
3. The summary must contain Job Business ID, Customer Business ID, completion time, outcome and a correlation key.
4. Internal CRM record IDs and internal notes must not be included.
5. The notification service may return:
- 202 accepted;
- 400 invalid payload;
- 401 expired connection;
- 409 already notified;
- 429 rate limited;
- 503 unavailable.
6. A repeated notification must not create a second customer message.
7. A 202 response without a notification ID is an unexpected response.
8. A file attachment is optional unless attachment_required = true.
9. The customer must not receive internal synchronization error details.
Challenge data
job_business_id,customer_business_id,job_status,completion_time,outcome,required_checks_passed,attachment_required,external_notification_key
NOV-VISIT-060,NOV-CUST-001,Completed,2026-10-12T11:00:00Z,Pump repaired,true,false,NOTIFY-NOV-VISIT-060
NOV-VISIT-061,NOV-CUST-002,Completed,2026-10-12T12:00:00Z,Door repaired,false,false,NOTIFY-NOV-VISIT-061
NOV-VISIT-062,NOV-CUST-001,In Progress,,Repair underway,true,false,NOTIFY-NOV-VISIT-062
NOV-VISIT-063,NOV-CUST-002,Completed,2026-10-12T13:00:00Z,Generator repaired,true,true,NOTIFY-NOV-VISIT-063
NOV-VISIT-064,NOV-CUST-001,Completed,2026-10-12T14:00:00Z,Pump repaired,true,false,NOTIFY-NOV-VISIT-064
Mock responses:
job_business_id,response_code,response_body_shape,expected_result
NOV-VISIT-060,202,data.notification_id,accepted
NOV-VISIT-061,,not_sent,blocked_before_call
NOV-VISIT-062,,not_sent,blocked_before_call
NOV-VISIT-063,503,error.code,retry_pending
NOV-VISIT-064,409,error.existing_notification_id,reconciled
Deliverables
Produce:
- a Deluge notification function;
- local eligibility validation;
- JSON request body;
- response classification;
- idempotency and duplicate handling;
- optional file-attachment behavior;
- safe customer-facing message mapping;
- at least eight tests;
- a connection and scope record;
- timeout, rate-limit and expired-connection recovery steps.
Success criteria
Your solution succeeds when:
- NOV-VISIT-060 sends one valid completion summary;
- NOV-VISIT-061 is blocked because inspection evidence failed;
- NOV-VISIT-062 is blocked because the Job is not completed;
- NOV-VISIT-063 becomes Retry Pending;
- NOV-VISIT-064 is reconciled using the existing notification ID;
- NOV-VISIT-063 does not expose internal error details to the customer;
- the optional attachment is required only for NOV-VISIT-063;
- the request excludes CRM technical IDs and internal notes.
7. Common problems and recovery
Symptom	Diagnosis	Correction
Connection name is hard-coded incorrectly	Link name or environment is wrong	Verify the connection link name and environment
Access token is stored in source	Credential handling is unsafe	Move authentication to a connection
Content-Type does not match body	Server parses the body incorrectly	Use the contract’s content type and encoding
JSON body is treated as form data	parameters and body were confused	Use the documented body mode for JSON
201 is marked success without an external ID	Response shape was not validated	Require the expected ID
409 creates another resource	Conflict was treated as retryable create	Reconcile using the existing ID
Timeout creates duplicate records	New idempotency key was generated	Reuse the original key
Full response is logged	Sensitive or oversized data was captured	Log safe metadata only
File upload is retried without file identity	Attachment has no stable key	Store attachment key and attempt key
A 429 is retried immediately	Backoff or retry header was ignored	Delay according to contract
401 is retried repeatedly	Connection is invalid or expired	Renew or replace connection
403 is treated as a timeout	Permission and transport errors are mixed	Mark non-retryable permission error
Large response causes runtime failure	Response-size limit was exceeded	Request smaller pages or fields
External call runs once per inspection row	Call boundary is too fine-grained	Aggregate data and call once where possible
Customer sees internal error text	Internal and external messages share a template	Map to safe customer language
8. Check your understanding
 1. What is the purpose of a Deluge connection?
 2. Which two keys should Nova include for replay-safe external processing?
 3. Why is a 409 response not always a failure?
 4. What should happen when a successful response lacks the expected external ID?
 5. What is the difference between a correlation key and an idempotency key?
 6. Why should Content-Type match the request body?
 7. Which errors are generally non-retryable: 400, 403, 409 or 504?
 8. Why does a timeout during a create operation require reconciliation?
 9. What should the local Creator record store after a 503 response?
10. Why should a file upload have its own status?
11. What should be logged when an external call fails?
12. Why is an external call inside a large loop a performance and reliability concern?
9. Solutions and explanations
Lesson quick checks
 1. A connection centralizes authentication so source code does not contain credentials and the integration can be authorized, renewed or revoked separately.
 2. A stable idempotency key identifies the business action; a correlation key identifies the attempt.
 3. A 409 may mean the business action already exists. If the response identifies the existing external record, the correct result is reconciliation rather than a second create.
 4. Mark the result as an unexpected response or contract failure. Do not claim success without the identifier needed for mapping.
 5. The idempotency key remains stable across retries. The correlation key can change for each attempt.
 6. The service uses the content type to parse the body. A JSON body sent as form data may be rejected or misinterpreted.
 7. 400 and 403 are normally non-retryable without correction. 409 requires reconciliation. 504 may be retryable.
 8. The server may have created the resource even though the client did not receive the response. A new key could create a duplicate.
 9. Store Sync_Status = Retry Pending or an equivalent state, the attempt key, error category and retry eligibility.
10. An attachment can fail independently from the parent Job and may need its own retry, identity, size and permission behavior.
11. Log business ID, attempt key, response code, safe error category, external ID if present and timestamp. Do not log tokens or unnecessary private data.
12. It can consume call limits, increase execution time and create inconsistent partial results.
Worked-case results
Mock response	Expected result
201 with DISPATCH-9001	Succeeded; store external ID
409 with DISPATCH-9001	Reconciled; store existing external ID
403	Error; permission correction required
504 or no response	Retry Pending; same idempotency key
201 without external ID	Error; unexpected response
The timeout path must not generate a new idempotency key. It should preserve the original action identity and either:
1. query the service for the existing action;
2. retry the same idempotent request;
3. place the record in a reconciliation queue.
Guided-practice sample solution
A valid result classification is:
map classifyExternalResponse(map response)
{
    result = Map();
    statusCode = response.get("response_code");

    if(statusCode == 201)
    {
        result.put("category", "Created");
        result.put("retryable", false);
    }
    else if(statusCode == 409)
    {
        result.put("category", "Already Exists");
        result.put("retryable", false);
    }
    else if(statusCode == 401 || statusCode == 403)
    {
        result.put("category", "Authentication or Permission");
        result.put("retryable", false);
    }
    else if(statusCode == 429 ||
            statusCode == 500 ||
            statusCode == 502 ||
            statusCode == 503 ||
            statusCode == 504)
    {
        result.put("category", "Transient Failure");
        result.put("retryable", true);
    }
    else
    {
        result.put("category", "Non-Retryable Failure");
        result.put("retryable", false);
    }

    return result;
}
Expected guided results:
Job	Category	Local state
NOV-VISIT-050	Created	Succeeded
NOV-VISIT-051	Already Exists	Reconciled
NOV-VISIT-052	Authentication or Permission	Error
NOV-VISIT-053	Transient Failure	Retry Pending
NOV-VISIT-054	Unexpected Response	Error
The integration artifact must state that the endpoint is fictional, the outputs are mocked and no service call was executed.
Independent-challenge sample solution
Eligibility results:
Job	Result	Reason
NOV-VISIT-060	Eligible	Completed and all required checks passed
NOV-VISIT-061	Blocked	Required inspection evidence failed
NOV-VISIT-062	Blocked	Job is not Completed
NOV-VISIT-063	Eligible	Completed and checks passed; attachment required
NOV-VISIT-064	Eligible and reconciled	Existing notification conflict
Response results:
Job	Response	Local result
NOV-VISIT-060	202 with notification ID	Notification Accepted
NOV-VISIT-063	503	Retry Pending
NOV-VISIT-064	409 with existing notification ID	Reconciled
NOV-VISIT-061	No external call	Inspection Exception
NOV-VISIT-062	No external call	Job Not Complete
Safe customer message for NOV-VISIT-063:
Your completion update is being processed. We will provide confirmation when it is available.
Do not send:
Notification service returned 503.
Connection expired.
Retry attempt 2.
The completion summary body should contain only:
{
  "notification_key": "NOTIFY-NOV-VISIT-060",
  "customer_business_id": "NOV-CUST-001",
  "job_business_id": "NOV-VISIT-060",
  "completed_at": "2026-10-12T11:00:00Z",
  "outcome": "Pump repaired"
}
It should exclude:
- CRM record IDs;
- internal notes;
- connection names;
- OAuth details;
- internal error categories.
10. Chapter recap and next step
You should now be able to:
- configure and document a connection;
- construct an invokeurl request;
- use methods, URLs, headers, parameters and bodies correctly;
- send and parse JSON;
- distinguish response status from response business data;
- classify authentication, permission, validation, conflict and transient errors;
- use try-catch and throw;
- design file upload and file-status handling;
- preserve idempotency across retries;
- use correlation keys for diagnostics;
- respect response-size, call-count and execution constraints;
- write external-service failure and recovery documentation.
Your project artifact from this chapter is:
C02-CH09_Nova_Field_Service_External_Service_Integration_v0.1.md
It should contain the connection record, mock or verified API contract, Deluge integration function, response classification, retry and reconciliation design, file-handling note and execution-limit note.
Chapter 10 focuses on debugging and maintainable code. It will use the failure categories and correlation information from this chapter to diagnose broken integrations, refactor reusable logic, manage configuration and prevent regressions.
11. Glossary and further reading
Glossary
Authentication  
The process of proving the identity used to call a service.
Connection  
A configured authentication object used by Deluge integration tasks or external calls.
Correlation key  
An identifier that links one request attempt to logs, responses and recovery records.
External service  
A system outside the current Zoho application or host.
Idempotency key  
A stable identifier that tells a service repeated requests represent one business action.
Invoke URL  
A Deluge task used to perform an HTTP request to a web service.
Multipart upload  
A request format used to send files and fields together.
Response shape  
The expected structure of an external response body.
Retryable failure  
A failure that may be safely attempted again under an explicit policy.
Scope  
A permission granted to a connection or application.
Timeout  
A condition where the expected response does not arrive within the permitted interval.
Further reading
- Zoho Deluge Connections (https://www.zoho.com/deluge/help/deluge-connections.html) — official connection types, authentication and custom-service configuration.
- Zoho Deluge Integration Tasks (https://www.zoho.com/deluge/help/integration-tasks.html) — official integration-task structure and external-call behavior.
- Zoho Deluge Try-Catch (https://www.zoho.com/deluge/help/misc-statements/try-catch.html) — official runtime exception handling.
- Zoho Deluge Throw (https://www.zoho.com/deluge/help/misc-statements/throw.html) — official user-defined exception handling.
- Zoho Deluge Limitations (https://www.zoho.com/deluge/help/limitations.html) — official statement, task, response and execution limitations.
- Zoho Deluge Post URL (https://www.zoho.com/deluge/help/web-data/posturl.html) — official HTTP POST reference and deprecation notice directing users to invokeurl.
- Zoho Deluge Get URL (https://www.zoho.com/deluge/help/web-data/geturl.html) — official HTTP GET reference and response examples.
- Zoho CRM Integration Tasks (https://www.zoho.com/deluge/help/crm-tasks.html) — official CRM task index for later integration work.
- Zoho Creator Integration Tasks (https://www.zoho.com/deluge/help/creator-tasks.html) — official Creator task index.
- Zoho CRM API Documentation (https://www.zoho.com/crm/developer/docs/api/v8/) — current CRM API documentation entry point for later chapters.
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
    - "Integration failures preserve the Creator business record and produce a recoverable sync state."
  chapter_9_artifacts:
    - "C02-CH09_Nova_Field_Service_External_Service_Integration_v0.1.md"
    - "Connection record"
    - "Mock or verified API contract"
    - "Deluge external-service function"
    - "Response classification table"
    - "Retry and reconciliation design"
    - "File-handling note"
    - "Execution-limit note"
  mock_service:
    name: "Nova Dispatch Mock API"
    version: "v1"
    base_url: "https://api.example.com"
    execution_status: "mocked_only_not_executed"
    connection_placeholder: "nova_dispatch_oauth_connection_placeholder"
  open_case_assumptions:
    - "The mock endpoint is fictional and is not a Zoho or vendor service."
    - "Actual external API versions, regional endpoints, scopes, connection requirements and response shapes require verification before implementation."
    - "The exact current invokeurl file-upload syntax must be confirmed in the target Deluge editor and external-service contract."
    - "No access token, client secret or private credential belongs in source or learning artifacts."
    - "A timeout after a create request is an unknown-outcome case and requires reconciliation with the original idempotency key."
END OF C02-CH09
