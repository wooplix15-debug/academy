schema_version: "1.1"
course_id: "C02"
chapter_id: "C02-CH13"
chapter_number: 13
chapter_title: "Creator API Integration"
filename: "C02_CH13_Creator_API_Integration_Student.md"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "partially_verified"
---
C02-CH13 — Creator API Integration
1. Chapter Orientation
1.1 Why this chapter matters
C02-CH11 introduced the Zoho CRM REST API. C02-CH12 explained OAuth, managed connections and credential security.
This chapter applies those ideas to Zoho Creator APIs.
A Creator application can be integrated in two directions:
External system → Creator API → Creator form or report
Creator function → external service → CRM or another application
For Nova Field Service, Creator owns operational records:
- Service requests.
- Jobs and visits.
- Inspection results.
- Dispatch state.
- Completion state.
- Synchronization status.
An external client may need to:
- Submit a service request.
- Read a report of requests.
- Update a synchronization result.
- Upload inspection evidence.
- Read field metadata.
- Delete test records in a controlled environment.
The Creator API provides these capabilities, but a safe integration must also understand:
- API V2.1 paths.
- Application, form and report link names.
- Creator account data centres.
- OAuth scopes.
- Development and stage environment headers.
- Form workflows and blueprints.
- Criteria syntax.
- Record limits and cursors.
- API response codes embedded in HTTP responses.
- Idempotency and duplicate prevention.
1.2 Learning outcomes
By the end of this chapter, you should be able to:
 1. Build a Creator API V2.1 URL from link names.
 2. Distinguish a form API from a report API.
 3. Use the correct Creator OAuth scope for a data operation.
 4. Retrieve Creator form field metadata.
 5. Add one or more records to a form.
 6. Fetch records displayed by a report.
 7. Update records using a report and criteria.
 8. Delete records safely in a test environment.
 9. Upload a file to a Creator record.
10. Control workflow execution during approved test calls.
11. Use environment headers for development or stage data.
12. Interpret Creator’s HTTP and JSON response codes.
13. Design an idempotent external request intake.
14. Create a Creator API collection and verification record.
15. Map Creator API records to the Nova operational model.
1.3 Prerequisites
You should already understand:
- Creator forms, reports and link names.
- Deluge maps and lists.
- Creator workflows and blueprints.
- CRM API V8 basics.
- OAuth connections.
- Correlation keys.
- Sync_Status, Request_Status and Job_Status.
The central Nova records remain:
NOV-CUST-001
NOV-REQ-001
NOV-VISIT-001
The examples use synthetic data and placeholder application identifiers. Replace placeholders only after verifying the target Creator account.
2. Creator API Boundary
2.1 Forms and reports have different roles
A Creator form is primarily a data-entry component.
A Creator report is a view of records. Creator API V2.1 uses the report endpoint to:
- Fetch records.
- Update records with criteria.
- Delete records with criteria.
- Upload files to a record displayed by the report.
Component	Typical API use
Form	Add records
Report	Fetch records
Report	Update records
Report	Delete records
Report	Upload files
Form metadata	Discover fields and link names
Application metadata	Discover application components
2.2 Nova ownership boundary
Operation	Owner
Accept a service request	Creator
Assign a technician	Creator
Update Request_Status	Creator
Update Job_Status	Creator
Record CRM Contact ID	Creator integration field
Resolve customer identity	CRM
Store customer email and phone	CRM
Expose a request intake endpoint	Creator API
Authenticate the external client	OAuth
Decide whether API-created records trigger workflows	Creator application owner
The Creator API is an access mechanism. It does not change the system-of-record decision.
2.3 Integration flow
flowchart LR
    A[External intake client] --> B[Creator API V2.1]
    B --> C[Service Requests form]
    C --> D[Creator validation]
    D --> E[Form workflows or blueprint]
    E --> F[Creator operational report]
    F --> G[CRM customer resolution]
    G --> H[Job and visit process]
    H --> I[Sync_Status and audit fields]
The external client should not write directly to internal workflow state unless the operation is explicitly part of the API contract.
2.4 API-created records are still application events
By default, Creator API V2.1 can trigger associated workflows when records are added, updated or deleted.
That means an API request can cause:
- Notifications.
- Schedules.
- Form workflow actions.
- Blueprint transitions.
- Approval actions.
- Integration calls.
- Additional record writes.
The caller must decide whether the request is:
an ordinary business event
or:
a controlled data-loading or test operation
Do not use workflow-skipping parameters to bypass required business approvals in production.
3. API Version, Domain and Link Names
3.1 Verified API version
The official Creator documentation used in this chapter is labeled API V2.1.
The general API path is:
https://<base_url>/creator/v2.1/
The V2.1 documentation adds features such as:
- skip_workflow.
- record_cursor.
- field_config.
- fields.
- max_records.
- Revised response structures for lookups and multivalue fields.
Use V2.1 paths consistently. Do not mix a V2.1 path with assumptions from the older V2 response format.
3.2 Creator API domain
The Creator base URL is data-centre-specific.
Illustrative examples:
www.zohoapis.com
www.zohoapis.eu
www.zohoapis.in
The exact domain must match the Creator organization. The Creator OAuth documentation recommends using the api_domain returned in the access-token response.
Do not hardcode www.zohoapis.com for every organization.
3.3 URL components
A form endpoint has this shape:
https://<base_url>/creator/v2.1/data/<account_owner_name>/<app_link_name>/form/<form_link_name>
A report endpoint has this shape:
https://<base_url>/creator/v2.1/data/<account_owner_name>/<app_link_name>/report/<report_link_name>
A form metadata endpoint has this shape:
https://<base_url>/creator/v2.1/meta/<account_owner_name>/<app_link_name>/form/<form_link_name>/fields
Example using placeholders:
https://www.zohoapis.com/creator/v2.1/data/nova_owner/nova_field_service/form/Service_Requests
The values below are illustrative:
Component	Example
Base URL	www.zohoapis.com
Account owner	nova_owner
App link name	nova_field_service
Form link name	Service_Requests
Report link name	All_Service_Requests
The display name may be:
Nova Field Service
The link name may be:
nova_field_service
Use the link name in the API path.
3.4 Environment headers
Creator API requests default to production unless an environment header is supplied.
For a development request:
environment: development
For a stage request:
environment: stage
Some development environments also use:
demo_user_name: demouser_1
Use the environment header only when the target Creator account and API plan support the corresponding environment.
3.5 Common headers
Authorization: Zoho-oauthtoken {{access_token}}
Accept: application/json
Content-Type: application/json
environment: development
The environment header is not a substitute for a separate OAuth credential. Keep development and production credentials separate.
4. Authentication, Scopes and Metadata
4.1 OAuth scopes
Creator API V2.1 uses OAuth scopes such as:
Operation	Scope
Add records to a form	ZohoCreator.form.CREATE
Fetch report records	ZohoCreator.report.READ
Update report records	ZohoCreator.report.UPDATE
Delete report records	ZohoCreator.report.DELETE
Upload files to report records	ZohoCreator.report.CREATE
Read form field metadata	ZohoCreator.meta.form.READ
Read application metadata	ZohoCreator.meta.application.READ
Read application list	ZohoCreator.dashboard.READ
Request only the scopes required by the integration.
A customer intake service may need:
ZohoCreator.form.CREATE
A read-only dispatch dashboard may need:
ZohoCreator.report.READ
An integration that updates Sync_Status may need:
ZohoCreator.report.UPDATE
4.2 Metadata before data
The API uses Creator field link names rather than display labels.
Retrieve form field metadata:
GET https://<base_url>/creator/v2.1/meta/<account_owner_name>/<app_link_name>/form/<form_link_name>/fields
Example:
curl --request GET \
  --url "https://www.zohoapis.com/creator/v2.1/meta/nova_owner/nova_field_service/form/Service_Requests/fields" \
  --header "Authorization: Zoho-oauthtoken ${ACCESS_TOKEN}"
A response may include:
{
  "code": 3000,
  "fields": [
    {
      "display_name": "Request Key",
      "link_name": "Request_Key",
      "type": 1,
      "max_char": 100,
      "unique": true,
      "mandatory": true
    },
    {
      "display_name": "Email",
      "link_name": "Email",
      "type": 3,
      "mandatory": true
    },
    {
      "display_name": "Request Status",
      "link_name": "Request_Status",
      "type": 12,
      "choices": [
        {
          "value": "New",
          "key": "New"
        },
        {
          "value": "In Progress",
          "key": "In Progress"
        },
        {
          "value": "Closed",
          "key": "Closed"
        }
      ]
    }
  ]
}
The response above is a documentation-shaped example. It was not retrieved from a live Nova application.
4.3 Link names and field types
Some important Creator API V2.1 field values are:
Creator field	API behavior
Single line	String
Email	String with email validation
Phone	String with phone validation
Number	Numeric value subject to configured digit limit
Date	Application date format
Date-time	Application date-time format
Drop down	One configured choice
Multi select	Array of configured choices
Checkbox	Array of configured choices
Lookup	Valid Creator record ID
Name	Object containing name subfields
Address	Object containing address subfields
Subform	Array of sub-record objects
Formula	Read-only calculated value
Auto number	System-generated value
File upload	Use Upload File API
Image	Use URL or Upload File API, subject to field configuration
Do not send a value to a formula or auto-number field.
4.4 Metadata-driven mapping
Before writing a request payload:
1. Retrieve field metadata.
2. Confirm the link name.
3. Confirm whether the field is mandatory.
4. Confirm the field type.
5. Confirm configured choices.
6. Confirm unique-value behavior.
7. Confirm whether the field can be written through the API.
8. Record the result in the integration mapping document.
This avoids errors caused by:
- Renamed labels.
- Wrong link names.
- Invalid picklist values.
- Overlong text.
- Formula-field writes.
- Invalid lookup IDs.
5. Read Records and Criteria
5.1 Fetch a report
The Get Records endpoint reads records displayed by a report:
GET https://<base_url>/creator/v2.1/data/<account_owner_name>/<app_link_name>/report/<report_link_name>
Required scope:
ZohoCreator.report.READ
Example:
curl --get \
  --url "https://www.zohoapis.com/creator/v2.1/data/nova_owner/nova_field_service/report/All_Service_Requests" \
  --data-urlencode "field_config=custom" \
  --data-urlencode "fields=ID,Request_Key,Nova_Customer_Key,Request_Status,Sync_Status" \
  --data-urlencode "max_records=200" \
  --header "Authorization: Zoho-oauthtoken ${ACCESS_TOKEN}" \
  --header "Accept: application/json"
The response may contain:
{
  "code": 3000,
  "data": [
    {
      "ID": "5725767000000100001",
      "Request_Key": "NOV-REQ-001",
      "Nova_Customer_Key": "NOV-CUST-001",
      "Request_Status": "New",
      "Sync_Status": "Pending"
    }
  ]
}
5.2 Select fields
The field_config parameter controls the fields returned:
Value	Meaning
quick_view	Fields included in the report quick view
detail_view	Fields included in the report detail view
custom	Fields supplied through fields
all	Fields from both quick and detail views
Use:
field_config=custom
when the integration needs a stable and narrow response:
fields=ID,Request_Key,CRM_Contact_ID,Sync_Status
Do not retrieve every visible field when the integration requires only four values.
5.3 Criteria syntax
Creator criteria uses field link names.
String values require double quotes:
Request_Status == "New"
Multiple conditions use:
&&
||
Examples:
Request_Key == "NOV-REQ-001"
Request_Status == "New" && Sync_Status == "Pending"
Request_Status == "New" || Request_Status == "Retry Pending"
For dates, use the application’s configured date format and single quotes:
Scheduled_Date >= '06-Oct-2026'
For lookup fields, use the related record ID:
CRM_Contact_ID == 5725767000000100001
Always URL-encode criteria when building a request.
5.4 Fetch limit and record cursor
The Creator API documentation states:
- A maximum of 1,000 records can be fetched per request.
- max_records accepts 200, 500 or 1,000.
- A record_cursor can fetch the next consecutive batch of 1,000 records.
- The cursor is returned in the response headers when more records exist.
Example first request:
GET /report/All_Service_Requests?max_records=1000
If the response header provides:
record_cursor: abc123
send that cursor in the next request:
record_cursor: abc123
Do not treat a cursor as a permanent bookmark. Store it only for the current retrieval process.
5.5 Read pattern for reconciliation
request report
→ inspect HTTP status
→ inspect JSON code
→ inspect data
→ inspect record_cursor
→ process current records
→ request next batch if cursor exists
→ stop when no cursor is returned
A no-record response is a valid business result for a lookup. It is different from an authentication or component-not-found failure.
6. Add, Update and Delete Records
6.1 Add records to a form
The Add Records endpoint is:
POST https://<base_url>/creator/v2.1/data/<account_owner_name>/<app_link_name>/form/<form_link_name>
Required scope:
ZohoCreator.form.CREATE
The API supports up to 200 records per request.
Example payload for one Nova request:
{
  "data": {
    "Request_Key": "NOV-REQ-001",
    "Nova_Customer_Key": "NOV-CUST-001",
    "Customer_Name": {
      "first_name": "Maya",
      "last_name": "Rivera"
    },
    "Email": "maya.rivera@example.com",
    "Phone": "+1-555-010-0111",
    "Request_Status": "New",
    "Job_Status": "Not Created",
    "Sync_Status": "Pending"
  },
  "skip_workflow": [
    "schedules",
    "form_workflow"
  ],
  "result": {
    "fields": [
      "Request_Key",
      "ID",
      "Sync_Status"
    ],
    "message": true
  }
}
The skip_workflow property is shown for a controlled test. In production, removing it allows the associated form workflows and schedules to run.
Blueprints and approvals cannot necessarily be skipped through this parameter. The application’s configured behavior remains authoritative.
6.2 Add multiple records
For multiple records:
{
  "data": [
    {
      "Request_Key": "NOV-REQ-001",
      "Email": "maya.rivera@example.com",
      "Request_Status": "New"
    },
    {
      "Request_Key": "NOV-REQ-002",
      "Email": "sam.chen@example.com",
      "Request_Status": "New"
    }
  ],
  "result": {
    "fields": [
      "ID",
      "Request_Key"
    ],
    "message": true
  }
}
A successful response may contain:
{
  "result": [
    {
      "code": 3000,
      "data": {
        "ID": "5725767000000100001",
        "Request_Key": "NOV-REQ-001"
      },
      "message": "Data Added Successfully!"
    },
    {
      "code": 3000,
      "data": {
        "ID": "5725767000000100002",
        "Request_Key": "NOV-REQ-002"
      },
      "message": "Data Added Successfully!"
    }
  ],
  "code": 3000
}
Process each result independently. Do not assume that a multi-record request has one all-or-nothing outcome.
6.3 Creator-side idempotency
The Nova Request_Key should be unique in the Creator form.
A safe intake sequence is:
search for Request_Key
→ one match: return existing record
→ no match: add record
→ multiple matches: stop and investigate
If the external client times out after the add request, it must search again before repeating the create.
A unique Creator field is a useful guard, but it does not replace reconciliation logic.
6.4 Update records through a report
The Update Records endpoint is:
PATCH https://<base_url>/creator/v2.1/data/<account_owner_name>/<app_link_name>/report/<report_link_name>
Required scope:
ZohoCreator.report.UPDATE
The request requires a criteria property.
Example:
{
  "criteria": "Request_Key == \"NOV-REQ-001\"",
  "data": {
    "CRM_Contact_ID": "5725767000001234567",
    "Sync_Status": "Resolved"
  },
  "skip_workflow": [
    "form_workflow"
  ],
  "result": {
    "fields": [
      "ID",
      "Request_Key",
      "CRM_Contact_ID",
      "Sync_Status"
    ],
    "message": true
  }
}
The criteria protects against accidentally updating every matching record.
If more than 200 records match, the request must use:
process_until_limit=true
The response then indicates whether more records remain. Continue until more_records is false.
6.5 Delete records through a report
The Delete Records endpoint uses:
DELETE https://<base_url>/creator/v2.1/data/<account_owner_name>/<app_link_name>/report/<report_link_name>
Required scope:
ZohoCreator.report.DELETE
The request requires criteria:
{
  "criteria": "Request_Key == \"TEST-NOV-REQ-001\"",
  "skip_workflow": [
    "form_workflow"
  ],
  "result": {
    "message": true
  }
}
Never use a broad delete criterion in production without review.
A delete request can trigger workflows and blueprints according to application configuration. Use a synthetic test key for cleanup.
6.6 Record IDs
Creator record IDs are generated by Creator:
5725767000000100001
They are different from:
NOV-REQ-001
NOV-CUST-001
NOV-VISIT-001
Store both when necessary:
Field	Value
Request_Key	NOV-REQ-001
Creator ID	5725767000000100001
CRM Contact ID	5725767000001234567
7. Workflows, Files and Environment Safety
7.1 Workflow behavior
By default, Creator API V2.1 can trigger associated workflows.
Operation	skip_workflow behavior
Add	Can skip form_workflow, schedules or all
Update	Can skip form_workflow, schedules or all
Delete	Can skip form_workflow
File upload	Can skip form_workflow, schedules or all
Only permitted administrators and developers can skip certain workflows. Blueprints and approvals may still execute.
7.2 Workflow decision table
Scenario	Skip workflows?	Reason
Production customer request intake	Usually no	The request is a real business event
Sandbox fixture creation	Often yes	Avoid notifications and downstream side effects
Backfill from an approved migration	Depends	Migration owner decides
Update Sync_Status after CRM resolution	Usually controlled	Avoid recursive integration loops
Upload inspection evidence	Depends	Evidence may require workflow review
Test cleanup	Usually yes	Avoid sending notifications for test deletion
7.3 Preventing integration loops
A loop can occur when:
Creator API add
→ form workflow calls CRM
→ CRM workflow calls Creator
→ Creator workflow adds or updates the same form
→ cycle repeats
Use these protections:
- External_Request_Key.
- Correlation_Key.
- Sync_Status.
- Source-system marker.
- Workflow guard condition.
- Separate integration-only update path.
- Maximum loop count.
- Safe retry limit.
Example guard:
if Sync_Status == "Integration Update":
    do not launch customer-resolution workflow
7.4 Upload files
Creator V2.1 uses the Upload File API for file, image, audio, video and signature fields.
The endpoint is:
POST https://<base_url>/creator/v2.1/data/<account_owner_name>/<app_link_name>/report/<report_link_name>/<record_ID>/<field_link_name>/upload
Required scope:
ZohoCreator.report.CREATE
Example:
curl --request POST \
  --url "https://www.zohoapis.com/creator/v2.1/data/nova_owner/nova_field_service/report/All_Service_Requests/5725767000000100001/Inspection_Photo/upload" \
  --header "Authorization: Zoho-oauthtoken ${ACCESS_TOKEN}" \
  --form "file=@./fixtures/inspection-photo.jpg"
Documented limits include:
- Image and signature fields: up to 10 MB.
- File upload, audio and video fields: up to 50 MB.
- Each file must be uploaded in a separate call when multiple uploads are enabled.
- Uploads consume Creator storage.
7.5 Development and stage data
A development request can include:
environment: development
demo_user_name: demouser_1
Use a development or stage environment for:
- API collection tests.
- Workflow-skip experiments.
- Invalid payload tests.
- File upload tests.
- Delete tests.
- Criteria experiments.
Never use environment: development and assume that the request succeeded against production. Confirm the environment in the test record and response evidence.
8. Errors, Limits and Observability
8.1 Creator response model
Creator may return an HTTP success status while placing the operation result in a JSON code.
A successful response commonly uses:
{
  "code": 3000,
  "result": [
    {
      "code": 3000,
      "data": {
        "ID": "5725767000000100001"
      },
      "message": "Data Added Successfully!"
    }
  ]
}
Inspect both:
HTTP status
JSON top-level code
record-level result code
8.2 Important status codes
HTTP/code	Meaning	Recovery
HTTP 200, code 3000	Operation succeeded	Persist result
Code 3100	No records found for criteria	Treat as a business no-match
Code 3090	Missing or invalid criteria	Correct field link name or expression
Code 3190	Record ID not found	Re-read or correct ID
Code 2902	Invalid field choice or value	Use metadata and configured choices
Code 2893	Form not found	Verify form link name
Code 2894	Report not found	Verify report link name
Code 2899	Permission denied to add	Repair Creator permission
Code 2898	Permission denied to view	Repair report permission
Code 2897	Permission denied to update	Repair report permission
Code 2896	Permission denied to delete	Repair report permission
Code 1130	API access disabled	Enable API access for permission set
Code 1030	Access token invalid or expired	Refresh or reauthorize
Code 1000	Missing or repeated mandatory parameter	Correct request
Code 3020	Request body missing or incomplete	Send valid JSON body
Code 3050	Formula or file field written incorrectly	Use calculated value or upload API
Code 3950	More than 200 records added	Split the request
Code 3960	More than 200 records processed	Use process_until_limit and loop
Code 3970	More than 200 records fetched under older mode	Use supported pagination/cursor
Code 4000	Daily Developer API limit reached	Review usage or wait
HTTP 429, code 2955	Per-minute or simultaneous-call limit reached	Backoff and reduce concurrency
HTTP 404	Invalid URL or component	Verify base URL and link names
HTTP 405	Invalid method	Use documented HTTP method
8.3 API limits
The Creator documentation states:
- API requests are limited to 50 calls per minute per API endpoint per public IP address.
- Daily Developer API usage depends on the Creator subscription.
- A maximum of 200 records can be added, updated or deleted per request.
- Some API responses use code 2955 for too many requests.
- A simultaneous-call limit may also be reached.
Design the integration to:
- Batch when safe.
- Avoid metadata calls inside every record loop.
- Cache verified link names and field mappings.
- Limit concurrent requests.
- Backoff on 429 responses.
- Track daily usage.
- Queue work that cannot be completed immediately.
8.4 Safe diagnostic record
correlation_key: "C02-CH13-NOV-REQ-001"
environment: "development"
api_version: "v2.1"
operation: "creator_add_service_request"
app_link_name: "nova_field_service"
form_link_name: "Service_Requests"
request_key: "NOV-REQ-001"
http_status: 200
creator_code: 3090
record_level_code: null
retryable: false
token_logged: false
payload_logged: false
next_action: "Correct criteria or field link name"
8.5 Deluge wrapper pattern
A Deluge function using a managed Creator connection can follow this pattern:
payload = Map();
recordData = Map();
recordData.put("Request_Key","NOV-REQ-001");
recordData.put("Nova_Customer_Key","NOV-CUST-001");
recordData.put("Email","maya.rivera@example.com");
recordData.put("Request_Status","New");
recordData.put("Job_Status","Not Created");
recordData.put("Sync_Status","Pending");

payload.put("data",recordData);
payload.put("skip_workflow",{"schedules","form_workflow"});

resultConfig = Map();
resultConfig.put("fields",{"ID","Request_Key","Sync_Status"});
resultConfig.put("message",true);
payload.put("result",resultConfig);

response = invokeurl
[
    url: "https://www.zohoapis.com/creator/v2.1/data/nova_owner/nova_field_service/form/Service_Requests"
    type: POST
    parameters: payload.toString()
    connection: "creator_api_connection_dev"
];

safeResult = Map();
safeResult.put("correlation_key","C02-CH13-NOV-REQ-001");
safeResult.put("response_present",response != null);
info safeResult;
The application must replace:
- Account owner.
- App link name.
- Form link name.
- Connection name.
- Field link names.
Do not copy this payload into production without checking metadata and workflow behavior.
9. Guided Practice — Build a Creator API Collection
9.1 Practice objective
Create a test-ready collection for a development or stage Creator application.
The collection must:
1. Retrieve field metadata.
2. Add one synthetic service request.
3. Fetch the request through a report.
4. Update Sync_Status.
5. Upload a synthetic inspection file.
6. Delete the synthetic request after review.
7. Record HTTP status and Creator JSON codes.
8. Avoid logging access tokens.
9.2 Environment variables
base_url: "www.zohoapis.com"
account_owner_name: "replace_with_verified_owner"
app_link_name: "replace_with_verified_app_link"
form_link_name: "Service_Requests"
report_link_name: "All_Service_Requests"
access_token: "secret_current_value_only"
environment: "development"
demo_user_name: "demouser_1"
request_key: "TEST-NOV-REQ-001"
nova_customer_key: "NOV-CUST-001"
creator_record_id: ""
Use example.com for all test email values.
9.3 Request 1 — Get form fields
curl --request GET \
  --url "https://{{base_url}}/creator/v2.1/meta/{{account_owner_name}}/{{app_link_name}}/form/{{form_link_name}}/fields" \
  --header "Authorization: Zoho-oauthtoken {{access_token}}" \
  --header "environment: {{environment}}"
Expected checks:
- HTTP status is successful.
- Top-level code is successful.
- fields is an array.
- Request_Key exists.
- Sync_Status exists.
- The required choice values are present.
9.4 Request 2 — Add a synthetic request
curl --request POST \
  --url "https://{{base_url}}/creator/v2.1/data/{{account_owner_name}}/{{app_link_name}}/form/{{form_link_name}}" \
  --header "Authorization: Zoho-oauthtoken {{access_token}}" \
  --header "Content-Type: application/json" \
  --header "environment: {{environment}}" \
  --data '{
    "data": {
      "Request_Key": "{{request_key}}",
      "Nova_Customer_Key": "{{nova_customer_key}}",
      "Customer_Name": {
        "first_name": "Maya",
        "last_name": "Rivera"
      },
      "Email": "nova-c02-ch13@example.com",
      "Phone": "+1-555-010-0121",
      "Request_Status": "New",
      "Job_Status": "Not Created",
      "Sync_Status": "Pending"
    },
    "skip_workflow": [
      "schedules",
      "form_workflow"
    ],
    "result": {
      "fields": [
        "ID",
        "Request_Key",
        "Sync_Status"
      ],
      "message": true
    }
  }'
Expected response shape:
{
  "code": 3000,
  "result": [
    {
      "code": 3000,
      "data": {
        "ID": "replace_with_returned_id",
        "Request_Key": "TEST-NOV-REQ-001",
        "Sync_Status": "Pending"
      }
    }
  ]
}
Save the returned Creator record ID in the local environment only.
9.5 Request 3 — Fetch the request
curl --get \
  --url "https://{{base_url}}/creator/v2.1/data/{{account_owner_name}}/{{app_link_name}}/report/{{report_link_name}}" \
  --data-urlencode "criteria=Request_Key == \"{{request_key}}\"" \
  --data-urlencode "field_config=custom" \
  --data-urlencode "fields=ID,Request_Key,Nova_Customer_Key,Request_Status,Job_Status,Sync_Status" \
  --data-urlencode "max_records=200" \
  --header "Authorization: Zoho-oauthtoken {{access_token}}" \
  --header "environment: {{environment}}"
Expected checks:
- One record matches.
- Request_Key equals the test key.
- Sync_Status equals Pending.
- The ID equals the saved creator_record_id.
9.6 Request 4 — Update synchronization status
curl --request PATCH \
  --url "https://{{base_url}}/creator/v2.1/data/{{account_owner_name}}/{{app_link_name}}/report/{{report_link_name}}" \
  --header "Authorization: Zoho-oauthtoken {{access_token}}" \
  --header "Content-Type: application/json" \
  --header "environment: {{environment}}" \
  --data '{
    "criteria": "Request_Key == \"{{request_key}}\"",
    "data": {
      "Sync_Status": "Resolved",
      "CRM_Contact_ID": "5725767000001234567"
    },
    "skip_workflow": [
      "form_workflow"
    ],
    "result": {
      "fields": [
        "ID",
        "Request_Key",
        "Sync_Status",
        "CRM_Contact_ID"
      ],
      "message": true
    }
  }'
The CRM Contact ID is illustrative. Replace it with a verified test ID only in a test organization.
9.7 Request 5 — Upload a synthetic file
curl --request POST \
  --url "https://{{base_url}}/creator/v2.1/data/{{account_owner_name}}/{{app_link_name}}/report/{{report_link_name}}/{{creator_record_id}}/Inspection_Photo/upload" \
  --header "Authorization: Zoho-oauthtoken {{access_token}}" \
  --header "environment: {{environment}}" \
  --form "file=@./fixtures/nova-test-inspection.jpg"
Only use this request if:
- Inspection_Photo is verified as a file or image field.
- The test file is synthetic.
- The field link name was retrieved from metadata.
- The file size is within the documented limit.
9.8 Request 6 — Delete the test record
Run only after checking the record ID:
curl --request DELETE \
  --url "https://{{base_url}}/creator/v2.1/data/{{account_owner_name}}/{{app_link_name}}/report/{{report_link_name}}" \
  --header "Authorization: Zoho-oauthtoken {{access_token}}" \
  --header "Content-Type: application/json" \
  --header "environment: {{environment}}" \
  --data '{
    "criteria": "Request_Key == \"{{request_key}}\"",
    "skip_workflow": [
      "form_workflow"
    ],
    "result": {
      "message": true
    }
  }'
Do not replace the specific test criterion with:
ID != null
unless the operation is an approved, controlled bulk deletion.
9.9 Verification record
Check	Expected	Actual	Evidence
API version	/creator/v2.1/	 	URL
Domain	Matches Creator organization	 	Environment
Metadata	Link names verified	 	Fields response
Add	Code 3000 and record ID	 	Response
Read	One matching request	 	Report response
Update	Sync_Status becomes Resolved	 	Response and reread
Upload	Synthetic file accepted	 	Upload response
Delete	Only test key removed	 	Delete response
Workflow behavior	Expected test behavior	 	Workflow review
Secret handling	No token in collection export	 	Collection inspection
9.10 Guided-practice questions
1. Why is the add request sent to a form while the update request is sent to a report?
2. Why does the update request require criteria?
3. What can happen if skip_workflow is omitted?
4. Why must a file upload use the report and record ID?
5. Which scope is needed to retrieve fields?
6. Which response values must be checked besides HTTP status?
7. Why is Request_Key better than a display name for cleanup?
10. Independent Practice — Creator API Contract and Mapping
10.1 Scenario
An external scheduling service submits a new request:
{
  "external_request_key": "EXT-2026-1001",
  "customer_key": "NOV-CUST-001",
  "customer_name": "Maya Rivera",
  "email": "maya.rivera@example.com",
  "phone": "+1-555-010-0111",
  "service_type": "Annual HVAC inspection",
  "requested_date": "2026-10-12",
  "notes": "Customer prefers an afternoon appointment."
}
Create a Creator API contract that:
- Prevents duplicate requests.
- Creates a Creator request.
- Does not create a Job yet.
- Keeps customer identity separate from operational status.
- Allows later CRM resolution.
- Records the external correlation key.
- Returns a safe response to the scheduling service.
10.2 Creator form mapping
Assume the verified Creator form link name is:
Service_Requests
The following field link names are illustrative and must be verified through metadata.
External property	Creator field link name	Transform	Validation	Owner
external_request_key	External_Request_Key	Trim	Required and unique	Integration
customer_key	Nova_Customer_Key	Preserve	Required	CRM identity
customer_name	Customer_Name	Split into Name object	Required last name	CRM/Creator intake
email	Email	Lowercase comparison	Valid email	CRM
phone	Phone	Preserve country code	Valid phone	CRM
service_type	Service_Type	Exact choice	Must match configured choice	Creator
requested_date	Requested_Date	Convert to app date format	Valid date	Creator
notes	Request_Notes	Preserve text	Max field length	Creator
Generated	Request_Status	Set New	Controlled choice	Creator
Generated	Job_Status	Set Not Created	Controlled choice	Creator
Generated	Sync_Status	Set Pending	Controlled choice	Creator
Generated	Correlation_Key	Generate	Required for diagnostics	Integration
10.3 Contract request
{
  "data": {
    "External_Request_Key": "EXT-2026-1001",
    "Nova_Customer_Key": "NOV-CUST-001",
    "Customer_Name": {
      "first_name": "Maya",
      "last_name": "Rivera"
    },
    "Email": "maya.rivera@example.com",
    "Phone": "+1-555-010-0111",
    "Service_Type": "Annual HVAC inspection",
    "Requested_Date": "12-Oct-2026",
    "Request_Notes": "Customer prefers an afternoon appointment.",
    "Request_Status": "New",
    "Job_Status": "Not Created",
    "Sync_Status": "Pending",
    "Correlation_Key": "C02-CH13-EXT-2026-1001"
  },
  "skip_workflow": [
    "schedules"
  ],
  "result": {
    "fields": [
      "ID",
      "External_Request_Key",
      "Request_Status",
      "Job_Status",
      "Sync_Status"
    ],
    "message": false
  }
}
Whether form_workflow should be skipped depends on the approved Nova process. If a form workflow creates the CRM resolution task, do not skip it.
10.4 Contract response
Return a response that does not expose unnecessary Creator fields:
{
  "accepted": true,
  "resolution": "created",
  "external_request_key": "EXT-2026-1001",
  "creator_record_id": "5725767000000100001",
  "request_status": "New",
  "job_status": "Not Created",
  "sync_status": "Pending",
  "correlation_key": "C02-CH13-EXT-2026-1001"
}
For a duplicate:
{
  "accepted": true,
  "resolution": "already_exists",
  "external_request_key": "EXT-2026-1001",
  "creator_record_id": "5725767000000100001",
  "correlation_key": "C02-CH13-EXT-2026-1001"
}
For validation failure:
{
  "accepted": false,
  "resolution": "rejected",
  "error_class": "validation",
  "external_request_key": "EXT-2026-1001",
  "correlation_key": "C02-CH13-EXT-2026-1001",
  "retryable": false
}
10.5 Idempotent intake algorithm
receive external request
→ validate required properties
→ create correlation key
→ search Creator by External_Request_Key
→ if exactly one match:
       return already_exists
→ if more than one match:
       stop and escalate data integrity issue
→ if no match:
       add one Creator request
→ if add succeeds:
       return created with Creator ID
→ if add times out:
       search again by External_Request_Key
→ if field validation fails:
       return non-retryable rejection
→ if rate limit occurs:
       queue for bounded retry
10.6 Self-study solution
The key design decisions are:
- External_Request_Key must be unique.
- Request_Key or external key must be used for reconciliation.
- Request_Status, Job_Status and Sync_Status are separate fields.
- The API must not create a Job as a side effect of request intake unless that behavior is explicitly approved.
- Customer identity is resolved through CRM after the Creator request exists.
- The Creator record ID is returned only after a successful add.
- A timeout triggers reconciliation, not an immediate duplicate create.
- A validation error is not retried unchanged.
- A rate-limit error is retried with backoff.
- The response to the external service should contain only the fields required for integration.
10.7 Independent challenge
Extend the contract to support a Sync_Status update after CRM resolution.
Required behavior:
1. Find the Creator record by External_Request_Key.
2. Update:
- CRM_Contact_ID.
- Sync_Status.
- CRM_Last_Read_At.
- Correlation_Key.
3. Preserve:
- Request_Status.
- Job_Status.
4. Return the updated Creator ID.
5. Return Needs Review when CRM returns multiple matches.
6. Do not update the Creator record if CRM authentication fails.
Expected update payload:
{
  "criteria": "External_Request_Key == \"EXT-2026-1001\"",
  "data": {
    "CRM_Contact_ID": "5725767000001234567",
    "Sync_Status": "Resolved",
    "CRM_Last_Read_At": "06-Oct-2026 14:30:00",
    "Correlation_Key": "C02-CH13-EXT-2026-1001"
  },
  "result": {
    "fields": [
      "ID",
      "External_Request_Key",
      "CRM_Contact_ID",
      "Sync_Status",
      "CRM_Last_Read_At"
    ],
    "message": false
  }
}
11. Checks, Recap and Glossary
11.1 Knowledge check
Question 1
Which Creator API version is used in this chapter?
Question 2
What is the difference between a form endpoint and a report endpoint?
Question 3
Which endpoint is used to retrieve form field metadata?
Question 4
What is the maximum number of records the Add Records API accepts in one request?
Question 5
What is the purpose of skip_workflow?
Question 6
Why does Update Records require a criteria property?
Question 7
What should be used to fetch more Creator records after the first batch?
Question 8
Which scope is required to fetch records from a report?
Question 9
A Creator response has HTTP 200 but a record-level code of 2902. Should the integration mark the operation successful?
Question 10
Which Nova field prevents an external request from being created twice?
11.2 Answers
Answer 1
Creator API V2.1.
Answer 2
A form endpoint is used to add records. A report endpoint is used to fetch, update or delete records displayed by the report.
Answer 3
GET /creator/v2.1/meta/<owner>/<app>/form/<form>/fields
with ZohoCreator.meta.form.READ.
Answer 4
200 records.
Answer 5
It controls whether eligible schedules and form workflows are skipped. It should be used only when the operation is approved for that behavior.
Answer 6
Criteria prevents an update from accidentally changing every matching record or a broad set of records.
Answer 7
Use the record_cursor response header for the next consecutive batch.
Answer 8
ZohoCreator.report.READ
Answer 9
No. Code 2902 indicates invalid field data, such as an invalid choice. The integration must classify the operation as failed and correct the payload.
Answer 10
A unique external request key, such as External_Request_Key or Request_Key.
11.3 Chapter recap
A reliable Creator API integration follows this sequence:
verify Creator data centre and API version
→ discover application, form, report and field link names
→ configure minimum OAuth scopes
→ select development or stage environment
→ validate external request
→ search by unique external key
→ add through the form endpoint
→ read through the report endpoint
→ update with narrow criteria
→ upload files through the upload endpoint
→ inspect HTTP and JSON codes
→ apply bounded retries and reconciliation
→ preserve Nova source-of-truth boundaries
Remember:
 1. Creator API V2.1 uses link names, not display labels.
 2. Forms and reports have different API responsibilities.
 3. Creator API requests can trigger workflows.
 4. skip_workflow is a controlled behavior, not a default production shortcut.
 5. Add, update and delete operations have record limits.
 6. Criteria protects update and delete operations.
 7. record_cursor supports continued retrieval.
 8. API errors may be represented inside HTTP 200 responses.
 9. Metadata should be retrieved before building custom payloads.
10. External_Request_Key provides the basis for idempotent intake.
11. A timeout requires reconciliation.
12. Creator record IDs, CRM IDs and Nova business IDs must remain distinct.
11.4 Glossary
Term	Meaning
App link name	Machine-facing name of a Creator application
Base URL	Data-centre-specific Creator API host
Criteria	Expression used to filter Creator report records
Creator record ID	System-generated identifier for one Creator record
Data API	Creator API used to add, fetch, update or delete data
Environment header	Header selecting production, development or stage data
External request key	Idempotency key supplied by an external system
Field link name	Machine-facing name of a Creator field
Form endpoint	API path used to add records
Form workflow	Workflow associated with a Creator form
Metadata API	API used to retrieve application or field definitions
more_records	Response indicator that more records require processing
Report endpoint	API path used to fetch, update or delete displayed records
record_cursor	Header value used to fetch the next batch of records
skip_workflow	V2.1 request property controlling eligible workflow execution
Sync_Status	Creator field describing integration state
V2.1	Current Creator API version documented for this chapter
11.5 Further reading
Official documentation used for this chapter:
- Zoho Creator API V2.1 Overview (https://www.zoho.com/creator/help/api/v2.1/)
- Zoho Creator API V2.1 OAuth Authentication (https://www.zoho.com/creator/help/api/v2.1/oauth-overview.html)
- Zoho Creator API V2.1 Add Records (https://www.zoho.com/creator/help/api/v2.1/add-records.html)
- Zoho Creator API V2.1 Get Records (https://www.zoho.com/creator/help/api/v2.1/get-records.html)
- Zoho Creator API V2.1 Update Records (https://www.zoho.com/creator/help/api/v2.1/update-records.html)
- Zoho Creator API V2.1 Delete Records (https://www.zoho.com/creator/help/api/v2.1/delete-records.html)
- Zoho Creator API V2.1 Get Fields (https://www.zoho.com/creator/help/api/v2.1/get-fields.html)
- Zoho Creator API V2.1 Upload File (https://www.zoho.com/creator/help/api/v2.1/upload-file.html)
- Zoho Creator API V2.1 Things to Know (https://www.zoho.com/creator/help/api/v2.1/things-to-know.html)
- Zoho Creator API Status Codes (https://www.zoho.com/creator/help/api/v2/status-codes.html)
- Zoho OAuth 2.0 Scopes (https://www.zoho.com/accounts/protocol/oauth/scope.html)
continuity:
  course_id: "C02"
  chapter_id: "C02-CH13"
  chapter_title: "Creator API Integration"
  previous_chapter: "C02-CH12"
  next_chapter: "C02-CH14"
  project: "Nova Field Service"
  source_of_truth:
    crm:
      - "Customer identity"
      - "Customer email and phone"
      - "CRM-generated customer record ID"
    creator:
      - "Service requests"
      - "Jobs and visits"
      - "Inspections"
      - "Request_Status"
      - "Job_Status"
      - "Sync_Status"
      - "Assigned_Technician"
  stable_ids:
    customer_key: "NOV-CUST-001"
    request_key: "NOV-REQ-001"
    visit_key: "NOV-VISIT-001"
  api:
    creator_version: "v2.1"
    crm_version: "v8"
    api_domain: "Resolve from organization data centre and OAuth response"
    live_execution: false
    external_request_key: "EXT-2026-1001"
  artifacts:
    - "C02_CH13_Creator_API_Integration_Student.md"
    - "C02-CH13_Nova_Creator_API_Contract_v0.1.md"
    - "Nova Creator API development collection"
    - "Nova Creator API verification record"
  security:
    oauth: "Managed connection"
    token_logging: false
    development_and_production_data: "Separate"
  deferred_topics:
    - "COQL, Bulk, upsert, Composite and GraphQL: C02-CH14"
END OF C02-CH13
