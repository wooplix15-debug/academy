schema_version: "1.1"
course_id: "C02"
chapter_id: "C02-CH02"
chapter_number: 2
chapter_title: "Programming and Developer Tooling"
filename: "C02_CH02_Programming_and_Developer_Tooling_Student.md"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "partially_verified"
---
Programming and Developer Tooling
1. What you will learn
In Chapter 1, you converted Nova Field Service's work into requirements, ownership rules, acceptance criteria and a technical specification. This chapter gives you the programming and tooling foundation needed to implement and test that design.
You will learn to:
- choose suitable types and collections for business data;
- write small JavaScript functions with clear inputs and outputs;
- understand JavaScript scope, nulls, equality and control flow;
- describe HTTP requests and responses;
- distinguish REST resources, methods, status codes and JSON payloads;
- use Postman variables, environments, scripts and collections;
- use browser developer tools to inspect a failing request;
- use Git to create a version-controlled exercise;
- review code for correctness, access safety, maintainability and testability;
- separate environment configuration from source code and secrets.
The required practice is to create a small version-controlled request-validation exercise and an API collection. The collection uses a fictional mock API so that no unverified Zoho endpoint, API version, data centre or OAuth scope is presented as real.
Continuity from Chapter 1
The following Chapter 1 decisions remain in force:
Item	Previous decision
Customer identity	CRM is authoritative
Operational records	Creator owns requests, visits, inspections and completion workflow
Stable records	NOV-CUST-001, NOV-REQ-001 and NOV-VISIT-001 are business identifiers
Business roles	Dispatcher, Technician, Service Manager and Administrator are scenario roles
Duplicate key	An external business key prevents repeated business actions
Failure behavior	A CRM failure remains visible and retryable
First release	Internal request intake; customer portal is out of scope
Chapter 1 artifacts	Technical specification, solution diagram and ADR register
Prerequisites
You should understand the Nova Field Service requirements from Chapter 1 and have basic programming familiarity. You do not need prior JavaScript, Postman or Git expertise.
This chapter uses JavaScript in three clearly identified contexts:
1. a small standalone module for validation;
2. Postman’s JavaScript scripting environment;
3. browser developer tools.
These examples are not Deluge. Deluge runs inside a Zoho host context such as Creator, CRM or Flow and has host-specific tasks, inputs and limits. Do not paste a Node.js or browser example into a Deluge editor. Deluge syntax and host contexts are covered in later chapters.
2. Lessons
Lesson 1: Types and collections describe business data
A type describes what kind of value a variable holds. A collection holds multiple values or named values.
In JavaScript, common primitive values are:
Type	Example	Nova Field Service use
String	"NOV-REQ-001"	Business ID, description or status
Number	30	A count or duration in minutes
Boolean	true	Whether inspection passed
null	null	A known empty value
undefined	undefined	A value that was not supplied or found
Object	{ status: "Assigned" }	One structured record
Array	["New", "Assigned"]	An ordered list of values
A business identifier should usually be treated as a string even if it contains digits. Converting NOV-REQ-001 to a number would lose its meaning. A phone number should also usually remain a string because leading zeros, spaces and country prefixes matter.
Objects and arrays
An object stores named properties:
const request = {
  businessId: "NOV-REQ-001",
  customerId: "NOV-CUST-001",
  priority: "High",
  status: "New",
  inspectionResult: null,
};
An array stores an ordered collection:
const allowedPriorities = ["Low", "Medium", "High"];
You can access object properties with dot notation:
request.priority; // "High"
Use bracket notation when the property name comes from a variable:
const propertyName = "status";
request[propertyName]; // "New"
Useful array operations include:
const requests = [
  { businessId: "NOV-REQ-001", priority: "High", status: "New" },
  { businessId: "NOV-REQ-002", priority: "Low", status: "Completed" },
];

const openRequests = requests.filter((item) => item.status !== "Completed");
const requestIds = requests.map((item) => item.businessId);
const firstHighRequest = requests.find((item) => item.priority === "High");
filter returns all matching items. map transforms every item. find returns the first matching item or undefined.
Null and undefined
null and undefined are not interchangeable business meanings.
- null can mean that a field is deliberately empty.
- undefined can mean that a property was not supplied or does not exist.
- an empty string "" is a supplied string with no characters;
- 0 is a number and must not be treated as missing;
- false is a value and must not be treated as missing.
This mistake is unsafe:
if (!request.priority) {
  // Treats "", 0, false, null, and undefined as missing.
}
If the field must be a non-empty string, state that rule directly:
function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}
If a field may be null but must not be undefined, test that explicitly:
const inspectionIsKnown = request.inspectionResult !== undefined;
When checking a required field, specify the accepted values rather than relying on truthiness.
Quick check
1. Should NOV-VISIT-001 be stored as a number or string?
2. What is the difference between inspectionResult: null and an object with no inspectionResult property?
3. Which array operation returns all open requests: map, filter or find?
Lesson 2: Functions make rules reusable
A function is a named operation that accepts inputs and returns a result. Small functions are easier to test and review than one large procedure.
This function validates the required request fields:
function validateRequest(request) {
  const errors = [];

  if (!request || typeof request !== "object") {
    return {
      valid: false,
      errors: ["Request must be an object"],
    };
  }

  if (!isNonEmptyString(request.customerId)) {
    errors.push("customerId is required");
  }

  if (!isNonEmptyString(request.description)) {
    errors.push("description is required");
  }

  const allowedPriorities = ["Low", "Medium", "High"];
  if (!allowedPriorities.includes(request.priority)) {
    errors.push("priority must be Low, Medium, or High");
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
The function has a stable return shape:
{
  valid: true,
  errors: []
}
or:
{
  valid: false,
  errors: ["customerId is required"]
}
A stable return shape helps callers handle success and failure consistently.
The function uses isNonEmptyString, which must be defined before use:
function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}
Use const for values that will not be reassigned and let for values that will change. Prefer block scope and avoid undeclared variables.
const maximumRetries = 3;
let retryCount = 0;

while (retryCount < maximumRetries) {
  retryCount += 1;
}
A function should normally do one coherent job. A function called validateRequestAndSendEmailAndUpdateCRMAndWriteLog is difficult to test because it mixes validation, communication, data mutation and logging. Separate those responsibilities.
Pure and side-effecting functions
A pure function returns a result based only on its inputs and does not change external state:
function classifyPriority(priority) {
  if (priority === "High") return "Urgent queue";
  if (priority === "Medium") return "Standard queue";
  return "Planned queue";
}
A function that sends an HTTP request, writes a record or changes a browser page has a side effect. Side effects are sometimes required, but keep them at a clear boundary.
A good design separates:
1. validation;
2. transformation;
3. transport;
4. response handling.
For example:
function buildCreatePayload(request) {
  return {
    external_request_key: request.externalRequestKey,
    customer_business_id: request.customerId,
    description: request.description.trim(),
    priority: request.priority,
  };
}
This function does not call CRM or Creator. It transforms an internal object into an API payload. A separate transport function can send that payload later.
JavaScript context matters
The following code uses the browser or Node.js standard fetch function:
async function createRequest(baseUrl, payload) {
  const response = await fetch(`${baseUrl}/v1/requests`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const body = await response.json();

  return {
    status: response.status,
    body,
  };
}
This is a JavaScript example for a browser or a compatible JavaScript runtime. It is not a Deluge invokeurl example. A later chapter will show the correct host-specific approach for Deluge.
Quick check
1. Why is buildCreatePayload easier to test than a function that also sends the request?
2. What should validateRequest return when request is null?
3. Which keyword should normally be used for maximumRetries?
Lesson 3: JavaScript foundations for implementation work
JavaScript is case-sensitive. requestId, requestID and RequestId are different identifiers.
Use strict equality:
priority === "High"
rather than relying on automatic conversion:
priority == "High"
Automatic conversion can produce surprising results:
"37" + 7; // "377"
"37" - 7; // 30
The first expression performs string concatenation. The second converts the string to a number. Explicit conversion makes intent clearer:
const quantity = Number("37");
const total = quantity + 7; // 44
Conditions
Use conditions to express business rules:
function completionDecision(request) {
  if (request.status !== "Awaiting Inspection") {
    return { allowed: false, reason: "Request is not awaiting inspection" };
  }

  if (request.inspectionResult !== "Pass") {
    return { allowed: false, reason: "Inspection must pass" };
  }

  return { allowed: true, reason: "Completion allowed" };
}
This handles a normal case and a blocked case. It does not infer that a request met a deadline just because it reached completion.
Loops and collections
Use a loop when each item must be inspected or transformed:
function duplicateKeys(requests) {
  const seen = new Set();
  const duplicates = new Set();

  for (const request of requests) {
    if (seen.has(request.externalRequestKey)) {
      duplicates.add(request.externalRequestKey);
    }
    seen.add(request.externalRequestKey);
  }

  return [...duplicates];
}
Set is useful for unique values. Map is useful when a key must point to a value:
const requestByKey = new Map();

requestByKey.set("EXT-REQ-1001", {
  businessId: "NOV-REQ-001",
  status: "New",
});

requestByKey.get("EXT-REQ-1001");
Do not choose a collection only because it is available. Choose one that communicates the rule:
Need	Suitable collection
Ordered list of requests	Array
Unique external keys	Set
Key-to-record lookup	Map
One record with named fields	Object
Quick check
A request with priority: 0 is received. Why should a generic if (!request.priority) check not be used to identify a missing priority?
Lesson 4: HTTP, REST and JSON
HTTP is a client-server protocol. A client sends a request and a server returns a response. A browser, Postman, a Zoho function or a JavaScript program can act as a client.
An HTTP request contains:
- a method;
- a URL;
- optional query parameters;
- headers;
- an optional body.
An HTTP response contains:
- a status code;
- headers;
- an optional body.
The examples in this lesson use the fictional Nova Mock API v1. This is a teaching contract, not a Zoho endpoint. It uses api.example.com, does not execute against a real server and does not define a Zoho API version or OAuth scope.
REST resources and methods
REST organizes data as resources. In the mock contract, /v1/requests represents service requests.
Method	Mock operation	Typical result
GET	Read a request or collection	200 OK
POST	Create a new request or trigger a creation action	201 Created or 409 Conflict
PATCH	Update selected fields	200 OK
DELETE	Remove a resource where permitted	204 No Content
Whether a method is safe to repeat depends on the operation contract. A repeated POST can create two records unless the API or application uses an external idempotency key.
Example request
POST https://api.example.com/v1/requests
Content-Type: application/json
X-Correlation-Key: test-2026-001

{
  "external_request_key": "EXT-REQ-1001",
  "customer_business_id": "NOV-CUST-001",
  "description": "Pump pressure low",
  "priority": "High"
}
Expected mocked response:
HTTP/1.1 201 Created
Content-Type: application/json

{
  "data": {
    "business_id": "NOV-REQ-001",
    "external_request_key": "EXT-REQ-1001",
    "status": "New"
  },
  "meta": {
    "correlation_key": "test-2026-001"
  }
}
The body is JSON. JSON is a text format with objects, arrays, strings, numbers, booleans and null. JSON property names use double quotes. Comments, undefined and trailing commas are not valid JSON.
Valid JSON:
{
  "business_id": "NOV-REQ-001",
  "inspection_result": null,
  "priority": "High"
}
Invalid JSON:
{
  "business_id": "NOV-REQ-001",
  "inspection_result": undefined,
}
JavaScript converts between objects and JSON text with JSON.stringify and JSON.parse:
const payload = {
  external_request_key: "EXT-REQ-1001",
  priority: "High",
};

const requestBody = JSON.stringify(payload);
const objectAgain = JSON.parse(requestBody);
A JSON null is not the same as an omitted property. The receiving API contract must define whether omission means “leave unchanged,” while null means “clear the value.”
Status codes and failures
Status codes help separate failure categories.
Status	Meaning in this exercise	Client response
200	Read or update succeeded	Parse and validate the response
201	Resource created	Store the returned business ID and correlation data
204	Succeeded with no body	Do not attempt to parse an empty body as JSON
400	Request shape or value is invalid	Correct the payload; do not blindly retry
401	Authentication is missing or invalid	Check the connection or token process
403	Identity exists but lacks permission	Do not bypass access; request approved permission
404	Resource or path was not found	Check the identifier, path and environment
409	Conflict, often duplicate business key	Find the existing record and avoid a second action
429	Rate limit or quota condition	Follow the approved delay or retry policy
500	Server-side failure	Record the failure and retry only when safe
503 or 504	Service unavailable or gateway timeout	Preserve the business action and use controlled recovery
A successful HTTP response is not automatically a successful business operation. A 200 response with an unexpected body can still violate the contract. Always validate both the status and the response shape.
REST boundary for Nova
The Chapter 1 design says:
- CRM owns customer identity and service information;
- Creator owns service requests and operational workflow;
- an integration maps business identifiers;
- duplicate external keys must not create duplicate actions.
This chapter does not claim the current Zoho CRM or Creator API version, regional endpoint or OAuth scope. Those values are environment-specific and are covered in C02-CH11 through C02-CH13. The mock collection teaches the request structure and testing method without inventing product details.
Quick check
1. Which status should the mock API return for a repeated external_request_key?
2. Why should a client not retry every 400 response?
3. Why is a 200 response not sufficient evidence that an update succeeded?
Lesson 5: Use Postman for repeatable API work
Postman is an API client and collaboration platform for designing, sending, testing and documenting requests. Its documentation describes requests, variables, environments, response inspection, scripts and collections.
A collection is a named group of related requests. A variable allows one value to be reused without copying it into every URL or body.
The mock collection uses these variables:
Variable	Example value	Purpose
baseUrl	https://api.example.com	Keeps the host replaceable
apiVersion	v1	Identifies the mock contract version
customerId	NOV-CUST-001	Reuses the sample customer
externalRequestKey	EXT-REQ-1001	Tests duplicate protection
correlationKey	postman-run-001	Traces one request attempt
accessToken	blank	Placeholder only; no secret is supplied
Postman variables are strings. If you store an object or array, serialize it with JSON.stringify and parse it when retrieving it. Use the narrowest appropriate variable scope. Do not place a real token in a committed collection file.
Environment setup procedure
 1. Create a Postman environment named Nova Mock - Local.
 2. Add the variables in the table above.
 3. Keep accessToken blank unless you are working with an approved mock server.
 4. Select the environment.
 5. Import the collection JSON supplied in the practice solution.
 6. Inspect the resolved URL before sending a request.
 7. Run the request with the normal sample input.
 8. Run the duplicate, invalid and permission scenarios using the supplied values.
 9. Review the response body and Postman test results.
10. Open the Postman Console if the request cannot be sent or a variable is unresolved.
The collection is a complete artifact, but its api.example.com host is illustrative. Expected responses in this chapter are mocked outputs, not observed execution results.
Postman scripts
Postman supports JavaScript scripts before a request and after a response. A post-response test can check the status and body:
pm.test("response is a successful creation", function () {
  pm.response.to.have.status(201);
});

const body = pm.response.json();

pm.test("created request has a business ID", function () {
  pm.expect(body.data.business_id).to.match(/^NOV-REQ-\d{3}$/);
});
A duplicate test should expect a conflict:
pm.test("duplicate key is rejected as a conflict", function () {
  pm.response.to.have.status(409);
});

const body = pm.response.json();

pm.test("conflict identifies the existing request", function () {
  pm.expect(body.error.code).to.eql("DUPLICATE_EXTERNAL_KEY");
});
These tests run in the Postman Sandbox. They are not Creator Deluge scripts and do not prove that a Zoho endpoint behaves this way.
Quick check
1. Which variable should change when moving from a mock server to a test server?
2. Why should accessToken not be committed in a collection?
3. What should a duplicate test verify besides the status code?
Lesson 6: Use browser developer tools to inspect behavior
Browser developer tools help you observe what a browser actually sends and receives. They do not replace server-side authorization or tests.
The most useful areas for implementation work are:
Tool area	Use
Console	Inspect JavaScript errors, values and debug messages
Network	Inspect URL, method, headers, payload, status, timing and response
Application or Storage	Inspect local storage, cookies and other client-side state
Sources or Debugger	Set breakpoints and inspect execution
Elements	Inspect rendered HTML and client-side changes
For a failing request:
 1. Open the Network panel.
 2. Enable “Preserve log” before reproducing a navigation or redirect issue.
 3. Reproduce the action once.
 4. Select the request.
 5. Check the final URL and method.
 6. Inspect query parameters and request payload.
 7. Check request headers without copying secrets into a ticket.
 8. Check the status code and response body.
 9. Compare the browser request with the Postman request.
10. Use the Console for the JavaScript stack trace.
Common interpretations:
- no request appears: the handler may not run;
- request has an unexpected URL: configuration or variable resolution is wrong;
- request is blocked before reaching the server: browser policy, network or CORS may be involved;
- response is 403: the server recognized the identity but denied access;
- response is 500: inspect the correlation key and server logs;
- request succeeds in Postman but fails in the browser: compare origin, cookies, headers, CORS and browser credentials behavior.
Never treat a hidden button as security. A user can call an endpoint directly. Authorization must be enforced by the server or host product.
Quick check
A browser shows a request with the correct JSON body but returns 403, while Postman returns 200 using an administrator credential. What is the most likely category of problem?
Lesson 7: Use Git to make changes traceable
Git records snapshots of a project. A repository contains the project files and the .git history directory.
A practical sequence is:
git init
git status
git add .
git commit -m "Create request validation exercise"
git log --oneline
The staging area lets you choose what enters the next commit. git status shows tracked, modified, staged and untracked files.
For a feature branch:
git switch -c feature/request-validation
After editing:
git diff
git diff --staged
git add src/request-tools.js test/request-tools.test.js
git commit -m "Validate required Nova request fields"
Use .gitignore to exclude local secrets, generated files and temporary output:
.env
.env.*
!.env.example
node_modules/
coverage/
*.log
The .env.example file documents required configuration without containing secret values.
A commit should represent a coherent change. “Fix everything” is not a useful commit message. Prefer messages such as:
- Add request validation rules
- Add duplicate-key test
- Document mock API collection
Git records files, not the intent behind them. A good README, commit message and test result make the history useful to the next developer.
Quick check
1. What does git diff --staged show?
2. Why is .env.example allowed while .env is ignored?
3. Why should a validation change and an unrelated dashboard redesign normally be separate commits?
Lesson 8: Review code and configure environments safely
A code review checks whether a change is correct, understandable, secure and maintainable. A reviewer should be able to connect the code to a requirement and a test.
Use this review order:
1. Behavior: Does the code satisfy the requirement?
2. Data: Does it handle nulls, duplicates, wrong types and unexpected response shapes?
3. Access: Does it preserve server-side permission boundaries?
4. Failures: Does it distinguish validation, authentication, permission, conflict and transient errors?
5. Maintainability: Are names, functions and return shapes clear?
6. Tests: Do tests prove both successful and rejected paths?
7. Configuration: Are environment values outside the source code?
8. Scope: Does the change avoid unrelated edits?
Environment configuration
Configuration changes between environments. Code should not need to change merely because the mock host, test host or production host changes.
A safe pattern is:
src/
  request-tools.js
test/
  request-tools.test.js
postman/
  Nova-Mock-API.postman_collection.json
.env.example
.gitignore
README.md
Example .env.example:
API_BASE_URL=https://api.example.com
API_VERSION=v1
ZOHO_REGION=replace-after-verification
CRM_MODULE_API_NAME=replace-after-verification
CREATOR_APP_LINK_NAME=replace-after-verification
The last three values are placeholders because Chapter 1 did not supply them and this chapter does not verify them. A placeholder is safer than an invented API name.
Separate configuration into:
- safe shared configuration: mock host, API version, feature flags;
- environment-specific configuration: test host, data centre, module names;
- secrets: access tokens, client secrets and private credentials.
Secrets belong in an approved secret store or local untracked configuration. They should not be pasted into source, screenshots, Postman collections or review comments.
Review comment example
Weak comment:
This is wrong.
Useful comment:
The duplicate path returns 409, but the caller treats every non-2xx response as a retryable failure. Please classify 409 as an existing business action, return the existing request reference and add a test proving that no second notification is sent.
Quick check
A reviewer sees this code:
const response = await fetch(url);
if (!response.ok) {
  throw new Error("Request failed");
}
Name two important questions the reviewer should ask.
3. Visual explanation
From source code to a tested API action
flowchart LR
    R[Requirement: create one request] --> F[Pure validation function]
    F -->|valid| P[Build JSON payload]
    F -->|invalid| U[Readable validation errors]
    P --> H[HTTP request]
    H --> S{HTTP response}
    S -->|201| C[Store business ID]
    S -->|409| D[Use existing request]
    S -->|401 or 403| A[Stop and diagnose access]
    S -->|429, 500, 503, 504| E[Controlled recovery]
    S -->|400| V[Correct input]
    C --> T[Postman and automated tests]
    D --> T
    A --> T
    E --> T
    V --> T
    T --> G[Git commit and review]
Plain-text explanation:
1. A requirement becomes a small validation function.
2. Valid input becomes a JSON payload.
3. The payload crosses an HTTP boundary.
4. The response status determines the next path.
5. A creation response stores the returned business identifier.
6. A duplicate response refers to an existing action instead of repeating it.
7. Authentication and permission failures stop the operation for diagnosis.
8. Transient failures use controlled recovery.
9. Tests prove the paths, and Git records the change.
Layer	Main question	Example evidence
Requirement	What must happen?	FR-007 duplicate protection
Function	Does the input satisfy local rules?	validateRequest result
Payload	Is the contract shape correct?	JSON body
Transport	What did the server return?	Method, URL and status
Recovery	What is safe to retry?	409 versus 503 decision
Review	Is the change maintainable and safe?	Diff, tests and review comments
Version control	Can the change be understood or restored?	Commit and branch history
4. Worked case
Case input
The Dispatcher submits this request:
{
  "businessId": "NOV-REQ-001",
  "customerId": "NOV-CUST-001",
  "description": "Pump pressure low",
  "priority": "High",
  "externalRequestKey": "EXT-REQ-1001",
  "inspectionResult": null
}
The local validation rules are:
1. the input must be an object;
2. customerId, description and externalRequestKey must be non-empty strings;
3. priority must be Low, Medium or High;
4. inspectionResult may be null while the request is not yet inspected;
5. duplicate detection uses externalRequestKey.
Step 1: Validate locally
function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function validateRequest(request) {
  const errors = [];

  if (!request || typeof request !== "object") {
    return { valid: false, errors: ["Request must be an object"] };
  }

  if (!isNonEmptyString(request.customerId)) {
    errors.push("customerId is required");
  }

  if (!isNonEmptyString(request.description)) {
    errors.push("description is required");
  }

  if (!isNonEmptyString(request.externalRequestKey)) {
    errors.push("externalRequestKey is required");
  }

  if (!["Low", "Medium", "High"].includes(request.priority)) {
    errors.push("priority must be Low, Medium, or High");
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
Expected result for the supplied input:
{
  "valid": true,
  "errors": []
}
inspectionResult: null is accepted because inspection has not happened yet. It must not be confused with an inspection that passed.
Step 2: Build the API payload
function buildCreatePayload(request) {
  return {
    external_request_key: request.externalRequestKey,
    customer_business_id: request.customerId,
    description: request.description.trim(),
    priority: request.priority,
  };
}
Expected payload:
{
  "external_request_key": "EXT-REQ-1001",
  "customer_business_id": "NOV-CUST-001",
  "description": "Pump pressure low",
  "priority": "High"
}
The payload does not include inspectionResult because the creation contract does not require it. Leaving it out is different from sending null; the API contract must define that distinction.
Step 3: Interpret mocked responses
Normal mocked result:
{
  "httpStatus": 201,
  "body": {
    "data": {
      "business_id": "NOV-REQ-001",
      "external_request_key": "EXT-REQ-1001",
      "status": "New"
    },
    "meta": {
      "correlation_key": "postman-run-001"
    }
  }
}
Interpretation: one request was created. Store the returned business ID and correlation key.
Duplicate mocked result:
{
  "httpStatus": 409,
  "body": {
    "error": {
      "code": "DUPLICATE_EXTERNAL_KEY",
      "message": "External request key already exists",
      "existing_business_id": "NOV-REQ-001"
    }
  }
}
Interpretation: do not retry as a new create. Reference NOV-REQ-001.
Permission mocked result:
{
  "httpStatus": 403,
  "body": {
    "error": {
      "code": "FORBIDDEN",
      "message": "The integration identity cannot create requests"
    }
  }
}
Interpretation: stop and correct the approved permission or connection. Do not lower security or use an administrator credential casually.
Transient mocked result:
{
  "httpStatus": 504,
  "body": {
    "error": {
      "code": "UPSTREAM_TIMEOUT",
      "message": "The service did not respond in time",
      "correlation_key": "postman-run-001"
    }
  }
}
Interpretation: preserve the business action and retry only under the agreed recovery rule. Reuse the external key.
Mistake and correction
Mistake: A developer writes this:
if (!response.ok) {
  await createRequestAgain(payload);
}
This retries 400, 401, 403 and 409 as if they were temporary failures. A duplicate 409 could cause repeated work or notifications.
Correction: Classify the status:
function classifyResponse(status) {
  if (status >= 200 && status < 300) return "success";
  if (status === 400) return "invalid_input";
  if (status === 401) return "authentication_error";
  if (status === 403) return "permission_error";
  if (status === 409) return "duplicate";
  if ([429, 500, 502, 503, 504].includes(status)) {
    return "transient_failure";
  }
  return "unexpected";
}
The classification is not a complete retry policy, but it creates a safe decision boundary.
5. Try it yourself — guided practice
Learning goal
Create a small Git repository containing a request-validation module, tests, environment documentation and a Postman collection for the Nova Mock API v1 contract.
Files and sample inputs
Use this repository layout:
nova-tooling-exercise/
  src/
    request-tools.js
  test/
    request-tools.test.js
  postman/
    Nova-Mock-API.postman_collection.json
  .env.example
  .gitignore
  README.md
Use these records:
external_request_key,customer_business_id,description,priority,expected_result
EXT-REQ-1001,NOV-CUST-001,Pump pressure low,High,valid
EXT-REQ-1002,NOV-CUST-002,Door access failure,Medium,valid
EXT-REQ-1003,,Generator alarm,High,invalid_missing_customer
EXT-REQ-1004,NOV-CUST-001,,Low,invalid_missing_description
EXT-REQ-1001,NOV-CUST-001,Pump pressure low,High,duplicate_key
EXT-REQ-1005,NOV-CUST-001,Filter replacement,Urgent,invalid_priority
Steps
1. Create a directory and initialize Git:
mkdir nova-tooling-exercise
cd nova-tooling-exercise
git init
git switch -c feature/request-validation
Expected intermediate result: git status identifies an empty repository on the feature branch.
2. Create the directory structure and .gitignore.
Expected intermediate result: git status --short shows the new files as untracked.
3. Implement isNonEmptyString, validateRequest, buildCreatePayload and duplicateKeys.
Expected intermediate result: each function has one clear purpose and a documented return shape.
4. Add tests for:
- a valid high-priority request;
- a missing customer;
- a missing description;
- an invalid priority;
- a duplicate external key;
- inspectionResult: null.
Expected intermediate result: the test names describe behavior rather than implementation.
5. Add .env.example with a mock base URL and placeholder Zoho configuration values.
Expected intermediate result: no token or client secret appears in the repository.
6. Import the supplied Postman collection from the solution section, or create equivalent requests:
- get customer;
- create request;
- repeat the same create;
- get the created request.
Expected intermediate result: every request uses variables rather than duplicated host values.
7. Add post-response tests for the expected statuses and response fields.
Expected intermediate result: the normal request checks 201; the repeated request checks 409.
8. Inspect and commit the work:
git status
git diff
git add .
git diff --staged
git commit -m "Create Nova request validation exercise"
git log --oneline
Expected intermediate result: the commit includes source, tests, collection, configuration template and README, but no .env.
Required final artifact
Your repository must:
- validate all supplied input cases;
- distinguish missing data from duplicate data;
- preserve null as an intentional value;
- use the external request key for duplicate detection;
- include a mock API collection;
- include tests for success and failure;
- include environment configuration without secrets;
- have at least one meaningful Git commit;
- explain that the API host and outputs are mocked.
Cleanup
Do not send requests to a real Zoho organization from this exercise. If you create a Postman environment, delete any temporary token values after practice. You may delete the local repository after reviewing its history.
Offline alternative
If Git or Postman is unavailable, create the same files in a folder and record the commands and expected outputs in README.md. This demonstrates the design and artifact structure but cannot demonstrate actual Git history, Postman variable resolution or Postman test execution.
6. Independent challenge
Changed input and constraints
Create a second branch called feature/emergency-request-validation.
Emergency requests have these additional rules:
1. priority must be exactly Emergency.
2. incidentDescription and callbackNumber are required.
3. customerBusinessId must still identify a CRM customer.
4. A repeated externalRequestKey must not create a second emergency notification.
5. A 403 response is a permission failure, not a retryable network failure.
6. A 504 response may be retried with the same external key.
7. The response body may omit inspectionResult; omission must not be treated as a passed inspection.
8. The first-response target of 30 minutes is not part of the API payload unless timestamps are supplied.
Input data:
external_request_key,customer_business_id,incident_description,callback_number,priority,expected_result
EXT-EM-3001,NOV-CUST-001,Water entering electrical room,+1-555-010-0101,Emergency,valid
EXT-EM-3002,NOV-CUST-002,,+1-555-010-0102,Emergency,invalid_missing_description
EXT-EM-3003,NOV-CUST-003,Alarm active,+1-555-010-0103,Emergency,permission_failure
EXT-EM-3001,NOV-CUST-001,Water entering electrical room,+1-555-010-0101,Emergency,duplicate_key
EXT-EM-3004,NOV-CUST-001,Alarm active,+1-555-010-0104,Emergency,transient_timeout
Deliverables
Create:
- an emergency validation function;
- tests for all five input cases;
- a Postman collection folder with normal, duplicate, permission and timeout requests;
- an updated .env.example;
- a README with the retry decision table;
- two commits: one for validation and tests, one for the API collection and documentation.
Observable success criteria
A reviewer must be able to see that:
- EXT-EM-3002 fails before transport because the description is missing;
- EXT-EM-3003 stops on 403;
- the repeated EXT-EM-3001 is treated as an existing action;
- EXT-EM-3004 may be retried with the same key;
- the code never treats an omitted inspection result as Pass;
- no real secret is committed;
- the Git history separates code from collection documentation.
7. Common problems and recovery
Symptom	Diagnosis	Correction
NOV-REQ-001 is converted to a number	Identifier type was chosen from its digits	Keep business IDs as strings
null, false and 0 are rejected together	Truthiness was used as validation	Check each allowed value explicitly
JSON fails to parse	JavaScript object syntax was confused with JSON	Use double-quoted keys and values; remove comments and trailing commas
Every non-2xx response is retried	Status categories are not distinguished	Separate invalid, permission, duplicate and transient failures
Postman URL contains {{baseUrl}} literally	Variable is missing or wrong environment is selected	Select the intended environment and inspect resolved variables
Postman test expects 201 for a duplicate	Test describes the happy path only	Add a separate duplicate request and expect 409
Browser request differs from Postman	Cookies, origin, headers or browser policy differ	Compare requests in Network and Postman Console
A secret appears in Git history	.gitignore was added after the secret was staged	Remove the secret, rotate it if real and keep only a placeholder
git diff appears empty before commit	Changes were staged or the wrong directory is open	Use git status, git diff --staged and verify the repository root
A function validates and sends data in one step	Responsibilities are coupled	Separate validation, payload construction and transport
A 403 is treated as a missing record	Permission and existence were conflated	Preserve the access failure category
A missing inspection result passes completion	Omitted, null and Pass were treated alike	Require explicit inspectionResult === "Pass"
8. Check your understanding
1. Choose the most suitable JavaScript collection for each need:
- an ordered list of visits;
- a unique set of external request keys;
- a lookup from external key to request record.
2. What should this expression return?
"37" + 7
3. Why should request.inspectionResult === "Pass" be used for the completion gate instead of if (request.inspectionResult)?
4. In the mock contract, which status represents a duplicate external key?
5. A 504 is returned after a create request. State two pieces of information that must be preserved before retrying.
6. What is the difference between a Postman collection variable and an environment variable in this exercise?
7. A browser request succeeds in Postman with an administrator credential but returns 403 in the browser. Give two investigation steps and one security rule.
8. What does git add do, and why should you inspect git diff --staged before committing?
 9. Identify the problem with this function:
function processRequest(request) {
  if (!request.customerId) {
    throw new Error("Invalid");
  }
  const response = fetch("/requests", {
    method: "POST",
    body: JSON.stringify(request),
  });
  console.log(response);
  return response;
}
10. Which values are safe to commit in .env.example, and which values must remain secret?
9. Solutions and explanations
Lesson quick checks
1. NOV-VISIT-001 should be a string because the prefix and formatting are part of the identifier.
2. inspectionResult: null explicitly represents an empty value. A missing property is undefined when read. The application must define whether those states have the same business meaning.
3. filter returns all matching requests.
For the function checks:
1. buildCreatePayload can be tested with an object and an expected object. It does not require a network, credential or mock server.
2. A null input should return a stable invalid result such as { valid: false, errors: ["Request must be an object"] }.
3. maximumRetries should normally be declared with const.
For the JavaScript foundation check, 0 is a valid number and is falsy in JavaScript. A generic falsy test would confuse a valid zero with missing data.
For HTTP:
1. A repeated external key should produce 409 Conflict in the mock contract.
2. A 400 usually means the input is invalid. Retrying unchanged input repeats the same mistake and may create noise or consume a quota.
3. A 200 only describes the transport-level status. The body may be malformed, incomplete or inconsistent with the expected business result.
For browser tools, the likely category is access or credential difference. Compare the browser request’s identity, cookies, authorization headers and target environment with Postman. Do not solve the problem by exposing administrator credentials or weakening server-side authorization.
For Git:
1. git diff --staged shows the exact changes currently selected for the next commit.
2. .env.example contains names and safe placeholders; .env may contain local secrets and is ignored.
3. Separate commits make review, rollback and history easier.
For the fetch review, ask at least:
- Does the function await the asynchronous response?
- Does it validate the input beyond customerId?
- Does it set Content-Type: application/json?
- Does it classify status codes and handle duplicate or permission responses?
- Does it parse and validate the response body?
- Does it preserve a correlation key?
- Is /requests environment configuration rather than a hard-coded production path?
Guided-practice sample solution
A complete validation module can be:
const ALLOWED_PRIORITIES = new Set(["Low", "Medium", "High"]);

export function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

export function validateRequest(request) {
  const errors = [];

  if (!request || typeof request !== "object") {
    return {
      valid: false,
      errors: ["Request must be an object"],
    };
  }

  if (!isNonEmptyString(request.externalRequestKey)) {
    errors.push("externalRequestKey is required");
  }

  if (!isNonEmptyString(request.customerBusinessId)) {
    errors.push("customerBusinessId is required");
  }

  if (!isNonEmptyString(request.description)) {
    errors.push("description is required");
  }

  if (!ALLOWED_PRIORITIES.has(request.priority)) {
    errors.push("priority must be Low, Medium, or High");
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

export function buildCreatePayload(request) {
  return {
    external_request_key: request.externalRequestKey,
    customer_business_id: request.customerBusinessId,
    description: request.description.trim(),
    priority: request.priority,
  };
}

export function duplicateKeys(requests) {
  const seen = new Set();
  const duplicates = new Set();

  for (const request of requests) {
    const key = request.externalRequestKey;

    if (seen.has(key)) {
      duplicates.add(key);
    }

    seen.add(key);
  }

  return [...duplicates];
}
A dependency-free test file using a modern Node runtime with the built-in test module is:
import test from "node:test";
import assert from "node:assert/strict";

import {
  buildCreatePayload,
  duplicateKeys,
  validateRequest,
} from "../src/request-tools.js";

test("accepts a complete request", () => {
  const result = validateRequest({
    externalRequestKey: "EXT-REQ-1001",
    customerBusinessId: "NOV-CUST-001",
    description: "Pump pressure low",
    priority: "High",
    inspectionResult: null,
  });

  assert.deepEqual(result, {
    valid: true,
    errors: [],
  });
});

test("rejects a missing customer", () => {
  const result = validateRequest({
    externalRequestKey: "EXT-REQ-1003",
    customerBusinessId: null,
    description: "Generator alarm",
    priority: "High",
  });

  assert.equal(result.valid, false);
  assert.deepEqual(result.errors, ["customerBusinessId is required"]);
});

test("rejects a missing description", () => {
  const result = validateRequest({
    externalRequestKey: "EXT-REQ-1004",
    customerBusinessId: "NOV-CUST-001",
    description: "",
    priority: "Low",
  });

  assert.equal(result.valid, false);
  assert.deepEqual(result.errors, ["description is required"]);
});

test("rejects an unsupported priority", () => {
  const result = validateRequest({
    externalRequestKey: "EXT-REQ-1005",
    customerBusinessId: "NOV-CUST-001",
    description: "Filter replacement",
    priority: "Urgent",
  });

  assert.equal(result.valid, false);
  assert.deepEqual(result.errors, [
    "priority must be Low, Medium, or High",
  ]);
});

test("builds the API payload with mapped names", () => {
  const payload = buildCreatePayload({
    externalRequestKey: "EXT-REQ-1001",
    customerBusinessId: "NOV-CUST-001",
    description: "  Pump pressure low ",
    priority: "High",
  });

  assert.deepEqual(payload, {
    external_request_key: "EXT-REQ-1001",
    customer_business_id: "NOV-CUST-001",
    description: "Pump pressure low",
    priority: "High",
  });
});

test("finds repeated external keys", () => {
  const duplicates = duplicateKeys([
    { externalRequestKey: "EXT-REQ-1001" },
    { externalRequestKey: "EXT-REQ-1002" },
    { externalRequestKey: "EXT-REQ-1001" },
  ]);

  assert.deepEqual(duplicates, ["EXT-REQ-1001"]);
});
Expected test interpretation:
Input	Result
Complete request	Valid
Null customer	Invalid; no transport
Empty description	Invalid; no transport
Urgent priority	Invalid; no transport
Repeated external key	Duplicate identified
inspectionResult: null	Accepted by request validation; completion remains blocked elsewhere
A safe .env.example is:
API_BASE_URL=https://api.example.com
API_VERSION=v1
ZOHO_REGION=replace-after-verification
CRM_MODULE_API_NAME=replace-after-verification
CREATOR_APP_LINK_NAME=replace-after-verification
A matching .gitignore is:
.env
.env.*
!.env.example
node_modules/
coverage/
*.log
A suitable README must state that the mock host is illustrative, the outputs are expected mocked results and no Zoho call was executed.
Complete mock API collection
The following collection is importable in Postman-compatible tooling, but the api.example.com host is not a live Nova service. The tests describe the intended mock contract.
{
  "info": {
    "name": "Nova Field Service - Mock API v1",
    "description": "Teaching collection for C02-CH02. This collection uses a fictional host and does not call Zoho.",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "baseUrl",
      "value": "https://api.example.com"
    },
    {
      "key": "apiVersion",
      "value": "v1"
    },
    {
      "key": "customerId",
      "value": "NOV-CUST-001"
    },
    {
      "key": "externalRequestKey",
      "value": "EXT-REQ-1001"
    },
    {
      "key": "correlationKey",
      "value": "postman-run-001"
    }
  ],
  "item": [
    {
      "name": "Get customer",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Accept",
            "value": "application/json"
          }
        ],
        "url": {
          "raw": "{{baseUrl}}/{{apiVersion}}/customers/{{customerId}}",
          "host": [
            "{{baseUrl}}"
          ],
          "path": [
            "{{apiVersion}}",
            "customers",
            "{{customerId}}"
          ]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test(\"customer lookup returns 200\", function () {",
              "  pm.response.to.have.status(200);",
              "});",
              "",
              "const body = pm.response.json();",
              "pm.test(\"customer has a business ID\", function () {",
              "  pm.expect(body.data.business_id).to.eql(pm.environment.get(\"customerId\") || pm.collectionVariables.get(\"customerId\"));",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "Create request - normal",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          },
          {
            "key": "X-Correlation-Key",
            "value": "{{correlationKey}}"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"external_request_key\": \"{{externalRequestKey}}\",\n  \"customer_business_id\": \"{{customerId}}\",\n  \"description\": \"Pump pressure low\",\n  \"priority\": \"High\"\n}"
        },
        "url": {
          "raw": "{{baseUrl}}/{{apiVersion}}/requests",
          "host": [
            "{{baseUrl}}"
          ],
          "path": [
            "{{apiVersion}}",
            "requests"
          ]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test(\"normal create returns 201\", function () {",
              "  pm.response.to.have.status(201);",
              "});",
              "",
              "const body = pm.response.json();",
              "pm.test(\"response contains a business request ID\", function () {",
              "  pm.expect(body.data.business_id).to.match(/^NOV-REQ-\\\\d{3}$/);",
              "});",
              "",
              "pm.collectionVariables.set(\"createdRequestId\", body.data.business_id);"
            ]
          }
        }
      ]
    },
    {
      "name": "Create request - duplicate",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          },
          {
            "key": "X-Correlation-Key",
            "value": "{{correlationKey}}-replay"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"external_request_key\": \"{{externalRequestKey}}\",\n  \"customer_business_id\": \"{{customerId}}\",\n  \"description\": \"Pump pressure low\",\n  \"priority\": \"High\"\n}"
        },
        "url": {
          "raw": "{{baseUrl}}/{{apiVersion}}/requests",
          "host": [
            "{{baseUrl}}"
          ],
          "path": [
            "{{apiVersion}}",
            "requests"
          ]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test(\"duplicate returns 409\", function () {",
              "  pm.response.to.have.status(409);",
              "});",
              "",
              "const body = pm.response.json();",
              "pm.test(\"duplicate identifies the existing request\", function () {",
              "  pm.expect(body.error.code).to.eql(\"DUPLICATE_EXTERNAL_KEY\");",
              "  pm.expect(body.error.existing_business_id).to.match(/^NOV-REQ-\\\\d{3}$/);",
              "});"
            ]
          }
        }
      ]
    },
    {
      "name": "Get request",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Accept",
            "value": "application/json"
          }
        ],
        "url": {
          "raw": "{{baseUrl}}/{{apiVersion}}/requests/{{createdRequestId}}",
          "host": [
            "{{baseUrl}}"
          ],
          "path": [
            "{{apiVersion}}",
            "requests",
            "{{createdRequestId}}"
          ]
        }
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test(\"request lookup returns 200\", function () {",
              "  pm.response.to.have.status(200);",
              "});",
              "",
              "const body = pm.response.json();",
              "pm.test(\"request status is present\", function () {",
              "  pm.expect(body.data.status).to.be.a(\"string\");",
              "});"
            ]
          }
        }
      ]
    }
  ]
}
Independent-challenge sample solution
A suitable emergency validator is:
const EMERGENCY = "Emergency";

export function validateEmergencyRequest(request) {
  const errors = [];

  if (!request || typeof request !== "object") {
    return {
      valid: false,
      errors: ["Request must be an object"],
    };
  }

  if (request.priority !== EMERGENCY) {
    errors.push("priority must be Emergency");
  }

  if (
    typeof request.customerBusinessId !== "string" ||
    request.customerBusinessId.trim() === ""
  ) {
    errors.push("customerBusinessId is required");
  }

  if (
    typeof request.incidentDescription !== "string" ||
    request.incidentDescription.trim() === ""
  ) {
    errors.push("incidentDescription is required");
  }

  if (
    typeof request.callbackNumber !== "string" ||
    request.callbackNumber.trim() === ""
  ) {
    errors.push("callbackNumber is required");
  }

  if (
    typeof request.externalRequestKey !== "string" ||
    request.externalRequestKey.trim() === ""
  ) {
    errors.push("externalRequestKey is required");
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

export function classifyEmergencyResponse(status) {
  if (status >= 200 && status < 300) return "success";
  if (status === 400) return "invalid_input";
  if (status === 401) return "authentication_error";
  if (status === 403) return "permission_error";
  if (status === 409) return "duplicate";
  if ([429, 500, 502, 503, 504].includes(status)) {
    return "retryable_transient";
  }
  return "unexpected";
}
Expected challenge decisions:
Input	Decision
EXT-EM-3001	Validate and send
EXT-EM-3002	Reject before transport because the incident description is missing
EXT-EM-3003 with 403	Stop as a permission failure; do not retry unchanged
Repeated EXT-EM-3001 with 409	Reference the existing action; no second notification
EXT-EM-3004 with 504	Preserve the key and correlation data, then retry according to policy
A reviewable commit sequence is:
1a2b3c4 Add emergency request validation and tests
5d6e7f8 Add emergency Postman scenarios and retry documentation
These commit IDs are illustrative expected examples, not actual observed Git output.
10. Chapter recap and next step
You now have the foundations for turning a Chapter 1 design into a traceable implementation.
You should be able to:
- choose types that preserve business meaning;
- use arrays, sets, maps and objects appropriately;
- distinguish null, undefined, empty strings, zero and false;
- write small functions with stable return shapes;
- separate validation, transformation, transport and response handling;
- describe HTTP requests and responses;
- use REST methods and status categories safely;
- create and inspect valid JSON;
- use Postman variables, environments, scripts and collections;
- investigate browser requests with developer tools;
- create commits and inspect staged changes with Git;
- review behavior, data, access, failure handling and configuration;
- keep environment values and secrets separate from source.
Your project artifact from this chapter is:
C02-CH02_Nova_Field_Service_Tooling_Exercise
It should contain a version-controlled request-validation exercise and an API collection that reflects the Chapter 1 duplicate and recovery requirements.
Chapter 3 builds the Creator data model and forms from the business identifiers and ownership boundaries defined in Chapters 1 and 2. It will introduce entities, relationships, lookups, subforms, identifiers, validation and lifecycle design. The exact Zoho API names remain an implementation dependency until the later API chapters verify them.
11. Glossary and further reading
Glossary
API collection  
A grouped set of requests, variables, scripts and tests used to exercise an API contract.
Array  
An ordered JavaScript collection.
Environment variable  
A configuration value selected for a particular environment, such as mock, test or production.
Function  
A reusable unit of logic that accepts inputs and returns a result.
HTTP  
The client-server protocol used to exchange requests and responses on the web.
JSON  
A text format for objects, arrays, strings, numbers, booleans and null.
Map  
A collection that associates keys with values.
Mock API  
A simulated API used for learning or testing. Its responses must not be represented as observations from a real product.
Postman Sandbox  
The JavaScript environment in which Postman request scripts and tests run.
REST  
An architectural style commonly used to expose resources through HTTP methods and representations.
Set  
A collection of unique values.
Staging area  
The Git area containing changes selected for the next commit.
Status code  
The numeric result in an HTTP response that describes the broad outcome of a request.
Type  
A category of value, such as string, number, boolean, object or array.
Further reading
- MDN: Grammar and types (https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types) — JavaScript declarations, scope, values and collections.
- MDN: Overview of HTTP (https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) — HTTP clients, servers, messages, methods and responses.
- MDN: JSON (https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON) — JSON syntax and parse and stringify.
- Postman API Platform (https://www.postman.com/product/) — official overview of API clients, collections, environments and testing.
- Postman variables (https://learning.postman.com/docs/sending-requests/variables/variables/) — variable scopes, environments and reusable values.
- Postman scripts and tests (https://learning.postman.com/docs/tests-and-scripts/write-scripts/intro-to-scripts/) — pre-request and post-response JavaScript.
- Postman request troubleshooting (https://learning.postman.com/docs/sending-requests/response-data/troubleshooting-api-requests/) — Console-based diagnosis and request inspection.
- Git: Getting a Git Repository (https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository) — initialization and cloning.
- Git: Recording Changes (https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository) — status, staging, diffs, commits and .gitignore.
- Zoho CRM Developer Platform (https://www.zoho.com/crm/developer/) — official product entry point for later CRM API and customization work.
- Zoho Creator Resource Center (https://www.zoho.com/creator/help/) — official Creator documentation for later application and Deluge work.
continuity:
  record_ids:
    customer: "NOV-CUST-001"
    request: "NOV-REQ-001"
    visit: "NOV-VISIT-001"
  carried_forward_decisions:
    - "CRM is authoritative for customer identity and service information."
    - "Creator owns requests, visits, inspections and completion workflow."
    - "Business identifiers are distinct from Zoho-generated record IDs."
    - "External request keys prevent duplicate business actions."
    - "CRM failures remain visible and recoverable."
    - "The first release uses internal request intake and excludes a customer portal."
  chapter_2_artifacts:
    - "C02-CH02_Nova_Field_Service_Tooling_Exercise"
    - "src/request-tools.js"
    - "test/request-tools.test.js"
    - "postman/Nova-Mock-API.postman_collection.json"
    - ".env.example"
    - ".gitignore"
    - "README.md"
  open_case_assumptions:
    - "The API collection uses a fictional mock host and has not been executed against Zoho."
    - "Zoho CRM and Creator API versions, regional endpoints, field API names and OAuth scopes remain unverified."
    - "The JavaScript examples are not Deluge and must not be pasted into Creator, CRM or Flow script editors."
    - "The mapping of Dispatcher, Technician, Service Manager and Administrator to native Zoho access controls remains to be verified."
END OF C02-CH02
