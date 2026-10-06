# SDKs and Serverless Components

## What you will learn

By the end of this chapter, you will be able to:
- Choose between Deluge, a CRM Function, an external service, and an SDK-backed integration boundary.
- Explain how Java, Node.js, and Python CRM Functions receive input through basicIO.
- Use the Zoho Request Client, or ZRC, to call CRM APIs from a serverless Function.
- Distinguish a direct CRM call from a call made through an explicit Connection.
- Expose a Standalone Function as a REST endpoint with crmAPIRequest and crmAPIResponse.
- Separate reusable business logic from the platform-specific Function handler.
- Test SDK-backed logic locally with a fake client before attempting tenant execution.
- Design bounded, redacted responses for Nova Field Service.
- Account for deployment, runtime, response-size, credit, timeout, and package limits.
- Explain why serverless execution is not a replacement for a persistent queue or delivery ledger.
This chapter extends Chapter 18. The previous chapter used CRM Widgets and Queries to present contextual data. Here, you will move the data-access boundary into a reusable server-side component.
## Lessons

### Lesson 1 — Choose the execution boundary first

An integration can run in several places:
Boundary	Typical technology	Best use
CRM-native automation	Deluge Function	Small business rules, record updates, workflow actions
CRM-hosted general logic	Standalone Function	Reusable logic or an HTTP endpoint
CRM-hosted typed runtime	Node.js, Python, or Java Function	SDK-style requests, existing language skills, structured code
Creator-hosted logic	Deluge, custom functions, connections	Creator forms, reports, and Creator-owned workflows
External service	Node.js, Python, Java, or another runtime	Long-running processing, controlled deployment, durable queues
Client browser	Client Script or Widget	User interaction and presentation
The choice should follow the execution requirement.
A Button Function is suitable for a short interactive action. A Schedule Function can support longer batch work. A REST API Function is useful when another service needs a stable HTTP boundary. An external worker is more suitable when the process requires durable state, long retries, leases, or high-volume processing.
A serverless Function can call CRM APIs, but it does not automatically provide:
- A persistent queue.
- Exactly-once delivery.
- A durable retry schedule.
- A worker lease.
- A cross-system transaction.
- Unlimited runtime.
- Unlimited API capacity.
These must be designed separately when the business process requires them.
### Lesson 2 — Understand the current CRM Function language model

Current Zoho CRM Function documentation distinguishes Deluge from Java, Node.js, and Python:
Capability	Deluge	Java, Node.js, Python
Native CRM integration tasks	zoho.crm.v8.*	ZRC
Trigger input	Declared arguments and mappings	basicIO payload
CRM Function draft state	No separate draft/deploy flow	Save draft, then deploy
Logging	info	context.log
REST request context	crmAPIRequest map	request, records, user, organization, and related basicIO parameters
REST response	Return crmAPIResponse map	Write crmAPIResponse through basicIO
For Java, Node.js, and Python, the standard input/output mechanism is basicIO.
A Function can receive values such as:
- records
- user
- organization
- variables
- request
- module
- related_module
- related_records
The exact values depend on the trigger and execution context.
For a REST endpoint, the request object contains request-related data such as:
{
  "method": "POST",
  "headers": {},
  "params": {},
  "body": "{\"request_key\":\"NOV-REQ-801\"}",
  "auth_type": "oauth2"
}
A Node.js Function should treat request data as untrusted input. Validate it before constructing an API path or CRM payload.
### Lesson 3 — Use ZRC as the CRM Function request client

The Zoho Request Client, or ZRC, is the HTTP client documented for Java, Node.js, and Python CRM Functions.
A Node.js CRM call can use:
const { ZRC } = require("zrc");

const response = await ZRC.get("/crm/v8/Accounts");
For an internal CRM call:
- No baseUrl is required.
- No explicit Connection is required for normal direct CRM access.
- CRM resolves the appropriate service route.
- Authentication is handled by the Function runtime.
A ZRC response has the general shape:
{
  status: 200,
  headers: {},
  data: {}
}
For an external service or a service requiring an explicit Connection, use a request configuration:
const response = await ZRC.get("/v1/accounts", {
  baseUrl: "https://api.example.test",
  connection: "nova_external_api",
  responseType: "JSON"
});
Use a Connection when:
- The target is another Zoho service.
- The target is an external API.
- You need the scopes of a specifically authorized user.
- You need explicit scope separation from the Function’s direct CRM access.
A direct CRM operation inside a CRM Function has system-level access behavior. A call made through an explicit Connection is governed by the authorized identity and scopes of that Connection. Treat these as different security contexts.
### Lesson 4 — Separate the core logic from the platform handler

A maintainable Function has two layers:
HTTP/basicIO handler
    |
    +-- Parse and validate input
    |
    +-- Call reusable application logic
              |
              +-- Call injected CRM client
              |
              +-- Select and normalize output
The core logic should not depend directly on basicIO, context, or the global ZRC object.
That separation provides three benefits:
1. The core logic can be tested locally with a fake CRM client.
2. The handler remains small and easy to audit.
3. A future external worker can reuse the same application logic with another client adapter.
The platform handler is an adapter. It translates between the Function runtime and the application contract.
### Lesson 5 — Expose a Standalone Function carefully

A Standalone Function is the recommended category for a reusable REST endpoint.
The current CRM Function REST model supports:
- API Key authentication.
- OAuth 2.0 authentication.
- crmAPIRequest input.
- crmAPIResponse output.
- External calls through curl, Postman, or an application HTTP client.
For production integrations, OAuth 2.0 is the safer default when the caller needs authenticated access.
An API-key endpoint is URL-based. The generated URL or API key must be treated as a secret. Do not place it in browser JavaScript, Widget source, public repositories, or screenshots. Regenerating the API key can invalidate the previous key for all Function endpoints in the organization.
A Node.js Function can set a response like this:
basicIO.write({
  crmAPIResponse: {
    status_code: 200,
    body: JSON.stringify({
      status: "ok"
    }),
    "content-type": "application/json;charset=utf-8",
    headers: {}
  }
});
Use explicit status codes for validation failures, missing records, upstream failures, and successful results.
### Lesson 6 — Respect runtime and deployment limits

Current CRM Function documentation describes several limits relevant to this chapter:
- REST API Functions have a 10-second category timeout.
- Automation Functions have a 30-second category timeout.
- Schedule Functions have a 15-minute category timeout.
- Function response size is limited to 10 MB.
- A single invocation has a maximum lines-of-execution limit.
- Java, Node.js, and Python Function credit usage is based on execution time.
- A Node.js Function package can be uploaded as a ZIP package.
- The ZIP package has a documented maximum size of 10 MB.
- The Function name, ZIP name, and main source file name must match exactly for Node.js packages.
- The current language guide documents the Node.js editor runtime as Node.js 8.11.
The runtime version matters. Avoid copying code that depends on a newer Node.js runtime unless the current tenant documentation confirms support.
For Java, Node.js, and Python:
1. Save the Function as a draft.
2. Test the draft.
3. Review logs and response behavior.
4. Deploy explicitly.
5. Associate or expose the deployed version.
Deluge Functions have different save behavior. The current Deluge guide documents no separate draft/deploy workflow; saving an associated Deluge Function can change the live version.
### Lesson 7 — Design logs as operational evidence

Logs should help an operator answer:
- Which operation ran?
- Which business key was involved?
- Which result category occurred?
- Was the failure local, authentication-related, validation-related, or upstream?
- What should be retried?
Logs should not contain:
- Access tokens.
- Refresh tokens.
- Client secrets.
- Authorization headers.
- API keys.
- Full CRM responses.
- Unnecessary customer data.
- Raw exception messages that may contain request details.
Use a stable business identifier and a classification:
request_key=NOV-REQ-801 result=CRM_READ_OK marker=NOVCH19LAB901A
For Node.js, use the platform logging methods:
context.log.INFO("request_key=NOV-REQ-801 result=CRM_READ_OK");
Do not write the entire exception object to a production log. Record a safe error category and retain detailed diagnostics only in a controlled development environment.
## Visual explanation

SDK-backed serverless request
Trusted server-to-server caller
             |
             | OAuth 2.0 request
             v
+-----------------------------+
| CRM Standalone Function     |
| nova_ch19_context_sdk       |
+-----------------------------+
             |
             | basicIO.getParameter("request")
             v
+-----------------------------+
| Request validator           |
| - request_key               |
| - crm_account_id            |
| - field allowlist           |
+-----------------------------+
             |
             | application client interface
             v
+-----------------------------+
| ZRC adapter                 |
| ZRC.get("/crm/v8/Accounts")|
+-----------------------------+
             |
             v
+-----------------------------+
| Zoho CRM v8 Accounts API    |
+-----------------------------+
             |
             v
+-----------------------------+
| Redacted crmAPIResponse     |
| - selected fields only      |
| - safe status               |
| - no raw response           |
+-----------------------------+
Direct CRM call versus Connection call
Direct ZRC CRM call
    Function runtime
        |
        +-- ZRC.get("/crm/v8/Accounts")
        |
        +-- CRM runtime authentication
        |
        +-- system-level Function access behavior

Connection-backed call
    Function runtime
        |
        +-- ZRC.get(path, { connection: "name", ... })
        |
        +-- Connection authorization
        |
        +-- authorized user scopes and permissions
The second path may be preferable when you need a narrower authorization boundary.
## Worked case

Scenario
Nova’s Chapter 18 Widget displays contextual Account information. The Widget must not contain an access token, a refresh token, an API key, or a broad CRM response.
The team decides to create a read-only CRM Standalone Function:
Function name: nova_ch19_context_sdk
Category: Standalone
Language: Node.js
Purpose: Return a small, approved Account context object
The request contract is:
{
  "request_key": "NOV-REQ-801",
  "crm_account_id": "NOVCH19-CRM-ACCOUNT-901"
}
The Function will:
1. Parse the request body.
2. Validate both values as non-empty strings.
3. Preserve the Account ID as an opaque string.
4. URL-encode the ID before placing it in a path.
5. Call CRM through ZRC.
6. Select only approved fields.
7. Return a stable response shape.
8. Avoid creating, updating, or deleting records.
9. Avoid logging the complete CRM response.
The Function does not implement the future Nova delivery ledger. It is a read-only context service.
Core application module
Save this logic as nova_ch19_core.js:
"use strict";

var LAB_MARKER = "NOVCH19LAB901A";

function failure(statusCode, code, message) {
  return {
    statusCode: statusCode,
    body: {
      status: "error",
      code: code,
      message: message,
      lab_marker: LAB_MARKER
    }
  };
}

function validOpaqueString(value) {
  return typeof value === "string" &&
    value.length > 0 &&
    value.trim() === value;
}

function validateInput(input) {
  if (!input || typeof input !== "object") {
    return failure(400, "INVALID_BODY", "Request body must be an object.");
  }

  if (!validOpaqueString(input.request_key)) {
    return failure(400, "INVALID_REQUEST_KEY", "request_key must be a non-empty string.");
  }

  if (!validOpaqueString(input.crm_account_id)) {
    return failure(400, "INVALID_CRM_ACCOUNT_ID", "crm_account_id must be a non-empty string.");
  }

  return null;
}

function selectAccount(input, response) {
  if (!response || typeof response.status !== "number") {
    return failure(502, "INVALID_CRM_RESPONSE", "CRM response was not usable.");
  }

  if (response.status === 404) {
    return failure(404, "CRM_ACCOUNT_NOT_FOUND", "CRM Account was not found.");
  }

  if (response.status < 200 || response.status >= 300) {
    return failure(502, "CRM_READ_FAILED", "CRM Account read failed.");
  }

  var responseData = response.data && response.data.data;

  if (!Array.isArray(responseData) || responseData.length === 0) {
    return failure(404, "CRM_ACCOUNT_NOT_FOUND", "CRM Account was not returned.");
  }

  var row = responseData[0];

  if (!row || typeof row.id !== "string") {
    return failure(502, "CRM_ID_NOT_STRING", "CRM returned an unusable identifier.");
  }

  return {
    statusCode: 200,
    body: {
      status: "ok",
      source: "CRM",
      request_key: input.request_key,
      crm_account_id: input.crm_account_id,
      account: {
        id: row.id,
        name: typeof row.Account_Name === "string"
          ? row.Account_Name
          : "",
        segment: typeof row.Segment === "string"
          ? row.Segment
          : ""
      },
      lab_marker: LAB_MARKER
    }
  };
}

async function run(input, crmClient) {
  var validationFailure = validateInput(input);

  if (validationFailure) {
    return validationFailure;
  }

  if (!crmClient || typeof crmClient.get !== "function") {
    return failure(500, "CLIENT_NOT_CONFIGURED", "CRM client is not configured.");
  }

  var path = "/crm/v8/Accounts/" +
    encodeURIComponent(input.crm_account_id);

  var response;

  try {
    response = await crmClient.get(path);
  } catch (error) {
    return failure(502, "CRM_CLIENT_ERROR", "CRM client could not complete the read.");
  }

  return selectAccount(input, response);
}

module.exports = {
  run: run
};
Important design details:
- The ID remains a string.
- The ID is encoded before being placed in a URL path.
- The module does not convert an ID with Number, parseInt, or toLong.
- The module returns only an approved subset of fields.
- The module does not expose response.data directly.
- The module classifies errors instead of returning raw exceptions.
- The application logic can be tested without the ZRC package.
CRM Function handler
Save this as nova_ch19_context_sdk.js:
"use strict";

var ZRC = require("zrc").ZRC;
var core = require("./nova_ch19_core");

function objectFrom(value, label) {
  if (value === null || value === undefined || value === "") {
    return {};
  }

  if (typeof value === "string") {
    try {
      return JSON.parse(value);
    } catch (error) {
      throw new Error(label + "_MALFORMED");
    }
  }

  if (typeof value === "object") {
    return value;
  }

  throw new Error(label + "_INVALID");
}

function writeResponse(basicIO, result) {
  basicIO.write({
    crmAPIResponse: {
      status_code: result.statusCode,
      body: JSON.stringify(result.body),
      "content-type": "application/json;charset=utf-8",
      headers: {}
    }
  });
}

module.exports = async function(context, basicIO) {
  var result;

  try {
    var request = objectFrom(
      basicIO.getParameter("request"),
      "REQUEST"
    );

    var body = objectFrom(request.body, "BODY");

    result = await core.run(body, {
      get: function(path) {
        return ZRC.get(path);
      }
    });

    if (result.statusCode === 200) {
      context.log.INFO(
        "request_key=" + body.request_key +
        " result=CRM_READ_OK marker=NOVCH19LAB901A"
      );
    } else {
      context.log.WARNING(
        "result=" + result.body.code +
        " marker=NOVCH19LAB901A"
      );
    }
  } catch (error) {
    context.log.SEVERE(
      "result=HANDLER_ERROR marker=NOVCH19LAB901A"
    );

    result = {
      statusCode: 400,
      body: {
        status: "error",
        code: "INVALID_REQUEST",
        message: "Request could not be processed.",
        lab_marker: "NOVCH19LAB901A"
      }
    };
  }

  writeResponse(basicIO, result);
  context.close();
};
This handler uses ZRC only at the platform boundary. The core module does not know whether the CRM client is ZRC, a fake test client, or a future external adapter.
Local fake-client test
The following test demonstrates the application logic without making a Zoho request:
"use strict";

var assert = require("assert");
var core = require("./nova_ch19_core");

var accountId = "NOVCH19-CRM-ACCOUNT-901";

var fakeCrm = {
  get: async function(path) {
    assert.strictEqual(
      path,
      "/crm/v8/Accounts/NOVCH19-CRM-ACCOUNT-901"
    );

    return {
      status: 200,
      data: {
        data: [
          {
            id: accountId,
            Account_Name: "Nova Training Account",
            Segment: "Training",
            Internal_Notes: "This field must not be returned."
          }
        ]
      }
    };
  }
};

async function main() {
  var result = await core.run(
    {
      request_key: "NOV-REQ-801",
      crm_account_id: accountId
    },
    fakeCrm
  );

  assert.strictEqual(result.statusCode, 200);
  assert.strictEqual(result.body.status, "ok");
  assert.strictEqual(result.body.account.id, accountId);
  assert.strictEqual(
    result.body.account.name,
    "Nova Training Account"
  );
  assert.strictEqual(
    result.body.account.Internal_Notes,
    undefined
  );

  console.log("happy path passed");
}

main().catch(function(error) {
  console.error("test failed");
  process.exitCode = 1;
});
Expected local result:
happy path passed
This is a local test result. It does not prove that:
- The CRM Function exists.
- The Function is deployed.
- The OAuth client is configured.
- The Connection exists.
- The CRM Account exists in a tenant.
- The endpoint is reachable.
- The tenant has the required edition or permission.
Those require separate tenant evidence.
Expected failure cases
Input or fake response	Expected status	Expected code
Missing body	400	INVALID_BODY
Numeric crm_account_id	400	INVALID_CRM_ACCOUNT_ID
Empty request_key	400	INVALID_REQUEST_KEY
CRM status 404	404	CRM_ACCOUNT_NOT_FOUND
CRM status 401	502	CRM_READ_FAILED
Client throws an exception	502	CRM_CLIENT_ERROR
CRM response has no data array	404	CRM_ACCOUNT_NOT_FOUND
CRM returns numeric id	502	CRM_ID_NOT_STRING
The response deliberately does not include the upstream CRM error body. The caller receives a stable integration error category, while operators can correlate the invocation through safe logs and the request key.
Deployment package
A simple package can have this layout:
nova_ch19_context_sdk/
├── config.json
├── nova_ch19_context_sdk.js
└── nova_ch19_core.js
Before uploading:
- Use the current CRM Function editor or current language guide for the config.json schema.
- Keep the package under the documented size limit.
- Match the Function name, ZIP name, and main JavaScript filename exactly, including case.
- Avoid hidden macOS files such as .DS_Store and __MACOSX.
- Do not include .env files, OAuth secrets, access tokens, or refresh tokens.
- Use the documented Node.js runtime syntax.
- Save and test the draft before deployment.
## Try it yourself — guided practice

Goal
Build and test a read-only CRM Account context adapter using a fake client first.
Part 1 — Define the contract
Use these exact lab values:
request_key: "NOV-REQ-801"
crm_account_id: "NOVCH19-CRM-ACCOUNT-901"
lab_marker: "NOVCH19LAB901A"
function_name: "nova_ch19_context_sdk"
crm_path: "/crm/v8/Accounts/{crm_account_id}"
live_execution: false
The output must include:
{
  "status": "ok",
  "source": "CRM",
  "request_key": "NOV-REQ-801",
  "crm_account_id": "NOVCH19-CRM-ACCOUNT-901",
  "account": {
    "id": "NOVCH19-CRM-ACCOUNT-901",
    "name": "Nova Training Account",
    "segment": "Training"
  }
}
Do not include Internal_Notes.
Part 2 — Implement the client seam
Create a client object with one method:
{
  get: async function(path) {
    // return a controlled fake response
  }
}
Test that the path is exactly:
/crm/v8/Accounts/NOVCH19-CRM-ACCOUNT-901
Part 3 — Add validation tests
Add cases for:
1. A missing request_key.
2. A numeric crm_account_id.
3. Leading whitespace in the Account ID.
4. A CRM 404.
5. A CRM 500.
6. A client exception.
7. A valid CRM response containing an extra confidential field.
8. A valid response with a string identifier containing leading zeroes.
The last case must remain unchanged:
"000901"
Part 4 — Add the platform handler
Use basicIO.getParameter("request") and parse the request body.
Return all responses through crmAPIResponse.
The handler must:
- Return JSON.
- Set an explicit status code.
- Avoid returning the full CRM response.
- Avoid logging the request body.
- Log only the request key or safe result category.
- Close the Function execution.
Part 5 — Inspect the deployment boundary
Before deployment, answer:
- Is the Function category Standalone?
- Is Node.js supported in the target tenant?
- Is the current runtime compatible with the code?
- Does the package contain only required files?
- Are Function and package names identical?
- Is OAuth 2.0 enabled for the endpoint?
- Is API Key authentication disabled if it is not needed?
- Does the Function have the required Manage Extensibility permission?
- Is the Function being tested in a Sandbox or another safe environment?
- Are the response fields approved for external callers?
Part 6 — Record evidence
Create a small evidence table:
Evidence item	Result
Core happy-path test	Pass or fail
Validation tests	Pass or fail
Fake 404 behavior	Pass or fail
Fake upstream error behavior	Pass or fail
Confidential field excluded	Pass or fail
Exact opaque ID preserved	Pass or fail
Live tenant execution	Not attempted
Endpoint deployment	Not attempted unless separately configured
## Independent challenge

Build a second version called:
nova_ch19_request_summary_sdk
It should accept:
{
  "request_key": "NOV-REQ-801",
  "crm_account_id": "NOVCH19-CRM-ACCOUNT-901",
  "event_key": "NOV-REQ-801:completed:v1"
}
The Function must:
 1. Validate all three values.
 2. Read the Account through an injected CRM client.
 3. Return only:
- request_key
- event_key
- crm_account_id
- Account id
- Account name
- Account segment
 4. Return 404 when no Account is found.
 5. Return 502 for an upstream CRM failure.
 6. Return 400 for invalid input.
 7. Preserve all identifiers as strings.
 8. Avoid record creation and updates.
 9. Avoid returning raw CRM data.
10. Include a safe lab marker in the local test response.
11. Add a test showing repeated reads do not create a second business record.
12. Write one paragraph explaining why this Function is not a delivery ledger.
For an advanced variation, replace the direct CRM call with an explicit Connection and explain how the authorization boundary changes.
## Common problems and recovery

Problem 1 — Cannot find module 'zrc'
Possible causes:
- The code is being run locally rather than inside the CRM Function runtime.
- The Function package or runtime is not configured as expected.
- The code is being tested with the wrong execution environment.
Recovery:
- Test core logic locally with a fake client.
- Import ZRC only in the CRM Function handler.
- Run the handler only in the supported CRM Function environment.
- Do not install an arbitrary package with a similar name without verifying the official runtime contract.
Problem 2 — The CRM path contains the wrong identifier
Cause:
- The ID was converted to a number.
- A display label was used instead of an API identifier.
- A request value was copied from a user-facing name.
Recovery:
- Treat IDs as opaque strings.
- Validate type and non-empty content.
- Use encodeURIComponent when placing a value in a URL path.
- Record the source of the identifier in the contract.
Problem 3 — The Function returns a successful HTTP status with an error body
Cause:
- crmAPIResponse was not used.
- The response body was returned as a JavaScript object instead of a JSON string.
- A catch block logged the error but never set a failure status.
Recovery:
- Create one response helper.
- Set status_code.
- Serialize the response body with JSON.stringify.
- Test the 400, 404, and 502 paths.
Problem 4 — The Function works in the editor but fails through HTTP
Possible causes:
- Editor execution has no real crmAPIRequest data.
- The request body is malformed.
- Authentication differs between editor execution and endpoint invocation.
- basicIO parameters were read using the wrong shape.
- The deployed version is different from the saved draft.
Recovery:
1. Test pure application logic with a fake client.
2. Test the Function draft with controlled input.
3. Test the external HTTP request in a non-production environment.
4. Confirm authentication mode.
5. Confirm deployment state.
6. Inspect safe execution logs.
Problem 5 — A Connection call has less access than a direct CRM call
Cause:
- A Connection uses the authorized user’s scopes and permissions.
- Direct Function CRM operations and Connection-backed calls have different access contexts.
Recovery:
- Document the required Connection owner and scopes.
- Confirm the authorized user can perform the operation.
- Avoid replacing a narrow Connection with broad direct access merely to make a test pass.
- Return a safe authorization error category.
Problem 6 — A Node.js package fails after upload
Possible causes:
- The ZIP contains hidden system files.
- The Function, ZIP, and main file names do not match.
- The package exceeds the documented size limit.
- A dependency requires a newer runtime than the CRM Function environment.
- The entry-point configuration is incorrect.
Recovery:
- Rebuild the ZIP from a clean directory.
- Exclude hidden macOS files.
- Match names exactly.
- Minimize dependencies.
- Verify runtime compatibility.
- Test a minimal package before adding libraries.
Problem 7 — A serverless Function becomes a hidden queue
Cause:
- A Function was asked to retry indefinitely.
- The caller assumes the Function stores failed work.
- A timeout is treated as proof that no downstream action occurred.
- The Function mutates records without an idempotency key.
Recovery:
- Keep the Chapter 19 Function read-only.
- Return a classified failure.
- Add durable queue and ledger components outside the Function when required.
- Use the Nova Event_Key for future write operations.
- Reconcile independently when the downstream result is uncertain.
Problem 8 — Logs expose confidential information
Cause:
- The complete exception object was written to logs.
- The full CRM response was logged.
- Headers or request bodies were printed for debugging.
Recovery:
- Replace raw diagnostics with stable error categories.
- Log only a safe request key, result class, and lab marker.
- Remove temporary verbose logging before deployment.
- Use controlled local debugging for detailed fake responses.
## Check your understanding

 1. What is the primary request client documented for Java, Node.js, and Python CRM Functions?
 2. Which basicIO parameter contains HTTP request details for a REST-exposed Function?
 3. When is a baseUrl normally unnecessary for a ZRC CRM request?
 4. Why should the core application logic be separated from the Function handler?
 5. What is the recommended Function category for a reusable REST endpoint?
 6. What is the security difference between a direct CRM Function call and a call made through a Connection?
 7. Why should a CRM Account ID remain a string?
 8. What does crmAPIResponse control?
 9. Why is a local fake-client test valuable even when the final integration uses ZRC?
10. Why is nova_ch19_context_sdk not a reliable delivery queue?
## Solutions and explanations

Guided practice solution
A valid implementation has these properties:
- The request contract uses exact opaque strings.
- The CRM path is built from the encoded Account ID.
- The fake client verifies the exact path.
- The core module does not import ZRC.
- The handler imports ZRC and adapts it to the core client interface.
- Only approved fields are returned.
- Extra fields such as Internal_Notes are discarded.
- A CRM 404 becomes a stable CRM_ACCOUNT_NOT_FOUND response.
- A CRM 500 or client exception becomes a stable upstream failure.
- No access token, response header, or raw exception is returned.
- Repeating the read does not create a new CRM record.
A valid local test result proves the pure application behavior against the fake response. It does not prove tenant configuration or live endpoint availability.
Independent challenge solution
The second Function should preserve the event_key without using it as a reason to write a new record. The read-only operation is naturally replay-safe because repeated reads do not create business state.
A suitable response is:
{
  "status": "ok",
  "request_key": "NOV-REQ-801",
  "event_key": "NOV-REQ-801:completed:v1",
  "crm_account_id": "NOVCH19-CRM-ACCOUNT-901",
  "account": {
    "id": "NOVCH19-CRM-ACCOUNT-901",
    "name": "Nova Training Account",
    "segment": "Training"
  }
}
The Function is not a delivery ledger because it does not persist:
- An event record.
- A delivery state.
- Attempt count.
- Next retry time.
- Worker ownership.
- Destination response.
- Reconciliation status.
If a future implementation writes a CRM summary after Creator completion, it must use the previously established Event_Key and a durable state model.
Check-your-understanding answers
 1. ZRC, the Zoho Request Client.
 2. The request parameter.
 3. For normal direct CRM calls, the CRM runtime resolves the CRM route and authentication.
 4. It allows local testing with a fake client and keeps platform-specific code small.
 5. Standalone.
 6. Direct CRM operations use the Function’s CRM execution context; Connection calls use the authorized identity and scopes of the Connection.
 7. CRM IDs are opaque identifiers. Numeric conversion can lose precision or remove leading zeroes.
 8. It controls the HTTP status code, body, headers, and content type.
 9. It verifies validation, field selection, path construction, and error mapping without tenant access.
10. It has no durable queue, retry ledger, worker lease, or persistent delivery state.
## Chapter recap and next step

This chapter introduced the server-side SDK boundary for CRM Functions.
You learned that:
- Deluge uses native CRM tasks.
- Java, Node.js, and Python CRM Functions use basicIO and ZRC.
- Direct CRM calls and Connection-backed calls have different authorization behavior.
- Standalone Functions can provide reusable REST endpoints.
- crmAPIRequest and crmAPIResponse define the HTTP boundary.
- Core application logic should be separated from the platform handler.
- A fake client makes the core logic locally testable.
- Runtime, package, timeout, credit, and response limits influence architecture.
- A Function is not automatically a durable queue.
- Nova’s future reliable delivery design still requires durable state outside this read-only context Function.
In the next chapter, you will build reusable extensions and package the integration boundary for broader reuse.
## Glossary and further reading

Glossary
Application adapter
Code that translates between a platform interface and reusable application logic.
basicIO
The standard input/output mechanism documented for Java, Node.js, and Python CRM Functions.
Connection
A securely configured authorization reference used by a Function to call another Zoho service or external API.
crmAPIRequest
The request context supplied to a CRM Function exposed as a REST endpoint.
crmAPIResponse
The response object used to control HTTP status, body, headers, and content type from a REST-exposed Function.
Direct CRM call
A CRM API request made through the Function runtime without an explicit Connection.
Function category
The CRM Function type that determines how a Function is triggered and what context it receives.
Opaque identifier
An identifier that must be preserved as a string without assuming that it represents a numeric value.
Standalone Function
A general-purpose CRM Function that can be invoked programmatically or exposed as a REST endpoint.
ZRC
Zoho Request Client, the request client documented for Java, Node.js, and Python CRM Functions.
Further reading
- Zoho CRM Functions — An Overview (https://www.zoho.com/crm/developer/docs/functions/)
- Java, Node.js, Python Functions Guide (https://www.zoho.com/crm/developer/docs/functions/language-guide/multi-language.html)
- Zoho Request Client (https://www.zoho.com/crm/developer/docs/functions/language-guide/zrc.html)
- Exposing Functions as REST APIs (https://www.zoho.com/crm/developer/docs/functions/serverless.html)
- Create Serverless Functions (https://www.zoho.com/crm/developer/docs/functions/getting-started/quickstart/create-serverless.html)
- Function Categories (https://www.zoho.com/crm/developer/docs/functions/getting-started/categories.html)
- Platform Limits and Quotas (https://www.zoho.com/crm/developer/docs/functions/limits-quotas.html)
- Function Security (https://www.zoho.com/crm/developer/docs/functions/security.html)
- Zoho CRM v8 APIs (https://www.zoho.com/crm/developer/docs/api/v8/)
