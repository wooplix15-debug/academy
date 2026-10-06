# Advanced CRM Data APIs

## What you will learn

By the end of this chapter, you will be able to:
- Use CRM Object Query Language (COQL) for filtered, joined, grouped, and aggregate retrieval.
- Query related CRM records through lookup paths.
- Use external IDs and duplicate-check fields safely.
- Distinguish ordinary record APIs from asynchronous Bulk Read and Bulk Write jobs.
- Interpret per-record results, 207 Multi-Status, job states, result files, and replay risks.
- Use Upsert for bounded insert-or-update operations.
- Use Composite API references and rollback settings deliberately.
- Evaluate whether a GraphQL retrieval contract is actually published and available before implementing it.
- Protect CRM record IDs, external IDs, tokens, and confidential responses.
- Apply these APIs to a controlled Nova Field Service training dataset.
This chapter does not build the production delivery ledger, queue, retry scheduler, or reliable event consumer. It uses a disposable CRM training organization and bounded markers.
## Lessons

### Lesson 1 — Use COQL for relational retrieval

The ordinary CRM Records API is useful when you already know a module and need records or a specific record ID. COQL is useful when your question crosses lookup relationships or needs grouping and aggregates.
COQL uses a POST request:
POST {api_domain}/crm/v8/coql
Authorization: Zoho-oauthtoken <access_token>
Content-Type: application/json
The body contains a select_query:
{
  "select_query": "select Account_Name, Description, id from Accounts where Account_Name = 'NOVCH11LAB901A' limit 0, 200"
}
Use CRM field and module API names, not display labels.
A query can include:
- SELECT
- FROM
- WHERE
- ORDER BY
- GROUP BY
- LIMIT
The main documented COQL boundaries are:
Contract	Documented value
Selected field API names	Up to 500 in the overview
Criteria in WHERE	Up to 25
Joins in one query	Up to 2
GROUP BY fields	Up to 4
Aggregate fields	Up to 5
ORDER BY fields	Up to 10
Values in IN or NOT IN	Up to 100
Pagination	Up to 100,000 records for one criteria pattern
COQL scope	ZohoCRM.coql.READ plus module read access
The detailed COQL page contains a limit-error section that refers to a maximum result limit of 200, while the overview documents LIMIT values up to 2,000. Treat this as a documentation inconsistency. Use a conservative LIMIT 0, 200 for the lab, verify the current tenant behavior, and do not claim a 2,000-row result without actual execution evidence.
A simple COQL query
curl "https://www.zohoapis.eu/crm/v8/coql" \
  -X POST \
  -H "Authorization: Zoho-oauthtoken ${CRM_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{
    "select_query":
      "select Account_Name, Description, Modified_Time, id
       from Accounts
       where Account_Name = '\''NOVCH11LAB901A'\''
       order by id asc
       limit 0, 200"
  }'
Expected response shape:
{
  "data": [
    {
      "Account_Name": "NOVCH11LAB901A",
      "Description": "NOV-CH11-901|updated",
      "Modified_Time": "2026-10-05T13:10:00+00:00",
      "id": "5725767000001000001"
    }
  ],
  "info": {
    "count": 1,
    "more_records": false
  }
}
The values above are an expected fixture shape. The ID and timestamp are not claimed as live observations.
COQL lookup paths
Suppose Contacts.Account_Name is the lookup from Contacts to Accounts. You can retrieve the Account name through the lookup path:
{
  "select_query":
    "select Last_Name, Email, Account_Name, Account_Name.Account_Name
     from Contacts
     where Account_Name.Account_Name = 'NOVCH11LAB901A'
     limit 0, 200"
}
The response can contain both:
{
  "Last_Name": "Training Contact",
  "Email": null,
  "Account_Name": {
    "id": "5725767000001000001"
  },
  "Account_Name.Account_Name": "NOVCH11LAB901A",
  "id": "5725767000003000001"
}
An optional customer email does not mean that the CRM Account has an email field. The authoritative Contact mapping remains unresolved until the tenant’s Contacts fields and relationship are verified.
Two joins
A COQL lookup path can continue through a second lookup:
Contacts
  -> Account_Name
     -> Parent_Account
Example:
{
  "select_query":
    "select Last_Name,
            Account_Name.Parent_Account,
            Account_Name.Parent_Account.Account_Name
     from Contacts
     where Last_Name is not null
       and Account_Name.Parent_Account.Account_Name is not null
     limit 0, 200"
}
Do not add a third lookup path merely because the data model contains one. The documented COQL limit is two joins.
Lesson check
1. Why does COQL use POST when it retrieves data?
2. Which names must appear in the query?
3. What is the maximum documented number of joins?
4. What should you do when two official sections document different result limits?
5. Does an Account lookup prove that the related Contact has an email address?
### Lesson 2 — Use aggregates, external IDs, and pagination carefully

Aggregate queries
COQL supports:
- SUM
- MIN
- MAX
- AVG
- COUNT
Aggregate functions are case-sensitive. When an aggregate is used with non-aggregate fields, include GROUP BY.
This query counts Accounts by owner:
{
  "select_query":
    "select COUNT(Owner), Owner
     from Accounts
     where Account_Name like 'NOVCH14%'
     group by Owner
     limit 0, 200"
}
Expected response shape:
{
  "data": [
    {
      "COUNT(Owner)": 2,
      "Owner": {
        "id": "5725767000001190199"
      }
    }
  ],
  "info": {
    "count": 1,
    "more_records": false
  }
}
This result counts records; it does not prove that the owner is the intended Morgan user. Identity mapping still requires the CRM Users API and a confirmed active user.
A grouped aggregate is useful for questions such as:
- How many training Accounts are assigned to each owner?
- What is the total value of a group of Deals?
- Which service-related records have the latest completion time?
- How many Contacts are associated with each scratch Account?
Do not use aggregate output as an authorization decision. It is a retrieval result, not an access-control proof.
External IDs
An external ID is an organization-defined CRM field that stores an identifier from another system. A useful external ID field should be:
- The correct CRM field API name.
- Configured as an external or unique field according to the tenant setup.
- Mapped to one authoritative source.
- Preserved as an exact string.
- Validated before being used for upsert or lookup.
The actual external field API name for the Nova Customer mapping is not established. Do not invent External_Account_ID as a production field name.
Use metadata first:
GET {api_domain}/crm/v8/settings/fields?module=Accounts
Authorization: Zoho-oauthtoken <access_token>
Find a field whose metadata confirms the relevant external or unique behavior. Record its actual API name:
module,field_label,field_api_name,external,unique,api_create,api_update,observed
Accounts,<tenant label>,<verified field name>,<fill>,<fill>,<fill>,<fill>,NOT_YET_RUN
COQL can use an external field in SELECT and WHERE:
{
  "select_query":
    "select Account_Name, <verified_external_field_api_name>
     from Accounts
     where <verified_external_field_api_name> = 'NOV-CH14-EXT-901'
     limit 0, 200"
}
Replace the placeholder only after metadata verification.
Pagination
COQL supports LIMIT offset, limit.
Example:
limit 0, 200
means “start at offset zero and return up to 200 records.”
For a large, stable result set:
1. Order by a deterministic field and ID.
2. Record the last row’s ordering values.
3. Use the next offset for the documented range.
4. After the documented 100,000-record range, use Bulk Read instead.
5. Do not treat more_records: true as proof that the next page has not changed.
Example ordered query:
{
  "select_query":
    "select Account_Name, Modified_Time, id
     from Accounts
     where Account_Name like 'NOVCH14%'
     order by Modified_Time asc, id asc
     limit 0, 200"
}
For ordinary Get Records pagination, CRM permits:
- Up to 200 records per request.
- Pages 1 through 10 without a page token, or up to 2,000 records.
- Page tokens for later pages.
- Up to 100,000 records through page-token pagination.
- A page token that is user-specific and parameter-bound.
- A page-token expiry shown in the response.
Do not change fields, filters, sorting, or other bound parameters while using a page token.
Lesson check
1. When is GROUP BY required?
2. Why must the actual external field API name come from metadata?
3. What does more_records: true tell you?
4. Why should an ordered query include a stable tie-breaker such as id?
5. When should Bulk Read replace ordinary COQL pagination?
### Lesson 3 — Use Bulk Read and Bulk Write as asynchronous jobs

Bulk Read
Bulk Read is appropriate for a large export or backup. It is asynchronous.
Create a job:
POST {api_domain}/crm/bulk/v8/read
Authorization: Zoho-oauthtoken <access_token>
Content-Type: application/json
Required scope:
ZohoCRM.bulk.read
The caller also needs read access to the selected module.
Example:
{
  "query": {
    "module": {
      "api_name": "Accounts"
    },
    "fields": [
      "Account_Name",
      "Description",
      "Modified_Time",
      "Owner"
    ],
    "criteria": {
      "field": {
        "api_name": "Account_Name"
      },
      "comparator": "starts_with",
      "value": "NOVCH14"
    },
    "page": 1
  }
}
The create response returns a job ID and an initial state such as ADDED.
Check job status:
GET {api_domain}/crm/bulk/v8/read/{job_id}
Authorization: Zoho-oauthtoken <access_token>
Possible states include:
- ADDED
- QUEUED
- IN PROGRESS
- COMPLETED
- FAILURE
A completed result includes a download_url. The download is a ZIP containing a CSV file.
Documented Bulk Read boundaries include:
- Up to 200,000 records per export page.
- Additional pages use a page value or a returned page token.
- The file is available for one day after completion.
- Download requests are rate-limited.
- Sorting and GROUP BY are not supported in the Bulk Read endpoint.
- Notes, Attachments, Emails, and related or cross modules are excluded from this API.
- Up to 200 selected fields can be supplied to Bulk Read.
- A maximum page value of 500 is documented.
- External fields are not supported in Bulk Read.
- Criteria are limited to 25, including criteria inherited from a view.
- IN and NOT IN accept up to 20 values in this endpoint.
Bulk Read creation proves only that the job was accepted. It does not prove that the export completed or that the file was downloaded.
Bulk Write
Bulk Write inserts, updates, or upserts large datasets asynchronously.
The process is:
1. Prepare a CSV file.
2. Compress the CSV into a ZIP file.
3. Upload the ZIP.
4. Capture the returned file_id.
5. Create a Bulk Write job.
6. Poll or receive a callback.
7. Download and inspect the result ZIP.
The upload endpoint is separate from the normal CRM API domain:
POST https://upload.zoho.com/crm/v8/upload
Authorization: Zoho-oauthtoken <access_token>
X-CRM-ORG: <zgid>
feature: bulk-write
Required upload scope:
ZohoFiles.files.ALL
The ZIP file must contain CSV data. The documented file-size limit is 25 MB. A single CSV can contain up to 25,000 records.
Example CSV:
Account_Name,Description
NOVCH14-BULK-001,CH14 bulk fixture one
NOVCH14-BULK-002,CH14 bulk fixture two
Create an upsert job:
POST {api_domain}/crm/bulk/v8/write
Authorization: Zoho-oauthtoken <access_token>
Content-Type: application/json
Example:
{
  "operation": "upsert",
  "ignore_empty": true,
  "resource": [
    {
      "type": "data",
      "module": {
        "api_name": "Accounts"
      },
      "file_id": "<captured_file_id>",
      "file_names": [
        "nova_ch14_accounts.csv"
      ],
      "find_by": "Account_Name",
      "field_mappings": [
        {
          "api_name": "Account_Name",
          "index": 0
        },
        {
          "api_name": "Description",
          "index": 1
        }
      ]
    }
  ]
}
find_by is mandatory for Bulk Write update and upsert operations. It can use an ID, unique field, external field, or another documented lookup resolution.
Check the job:
GET {api_domain}/crm/bulk/v8/write/{job_id}
Authorization: Zoho-oauthtoken <access_token>
The result file contains status information. Inspect at least:
- STATUS
- RECORD_ID
- ERRORS
Possible row outcomes include:
- Added.
- Updated.
- Skipped.
- Unprocessed.
The result file is documented as available for up to seven days. A completed job with skipped rows is not an all-success result.
Parent and child data
Subforms and multi-select lookup relationships use separate modules or linking modules in Bulk Write.
For parent-child imports:
- Put the parent resource first.
- Include separate CSV files.
- Use field mappings.
- Map children through Parent_Id or the appropriate parent-column index.
- Do not assume the parent and child write is a general cross-system transaction.
Lesson check
1. Why is a Bulk Read job not complete when its create call succeeds?
2. What file format does Bulk Write require?
3. Which header identifies the CRM organization during file upload?
4. What does the Bulk Write result file tell you?
5. Can a skipped row be counted as a successful update?
### Lesson 4 — Use Upsert and partial results for bounded writes

The Upsert API inserts or updates records based on duplicate-check fields.
Endpoint:
POST {api_domain}/crm/v8/Accounts/upsert
Authorization: Zoho-oauthtoken <access_token>
Content-Type: application/json
A single call can process up to 100 records.
Example using the system-defined Account duplicate field:
{
  "data": [
    {
      "Account_Name": "NOVCH14-UP-001",
      "Description": "CH14 upsert fixture"
    }
  ],
  "duplicate_check_fields": [
    "Account_Name"
  ],
  "trigger": [],
  "skip_feature_execution": [
    {
      "name": "cadences",
      "action": "insert"
    },
    {
      "name": "cadences",
      "action": "update"
    }
  ]
}
For Accounts, Account_Name is a system-defined duplicate-check field. A user-defined unique field or verified external field can also be used.
The response identifies the action:
{
  "data": [
    {
      "code": "SUCCESS",
      "duplicate_field": "Account_Name",
      "action": "update",
      "details": {
        "id": "5725767000004000001"
      },
      "message": "record updated",
      "status": "success"
    }
  ]
}
or:
{
  "data": [
    {
      "code": "SUCCESS",
      "duplicate_field": null,
      "action": "insert",
      "details": {
        "id": "5725767000004000002"
      },
      "message": "record added",
      "status": "success"
    }
  ]
}
Do not infer the action from whether an ID appears. Read the explicit action value.
Upsert and business identity
For a future Nova service summary, the intended logical identity is:
Request_Key
The actual CRM summary module and its field API names remain unresolved. Do not use the Accounts module as a substitute for that production module.
For this chapter, use the Accounts module only for disposable training records. If you want to model a real external ID, first verify an actual CRM field and its uniqueness. Then use:
{
  "data": [
    {
      "<verified_external_field_api_name>": "NOV-CH14-EXT-901",
      "Account_Name": "NOVCH14-EXT-901",
      "Description": "External ID fixture"
    }
  ],
  "duplicate_check_fields": [
    "<verified_external_field_api_name>"
  ]
}
This is a template, not a ready-to-run payload.
Partial results
When multiple records are inserted, updated, or upserted, CRM preserves response order. A response can have HTTP status 207 when some records succeed and others fail.
Example input:
{
  "data": [
    {
      "Account_Name": "NOVCH14-UP-001",
      "Description": "valid fixture"
    },
    {
      "Account_Name": "",
      "Description": "missing required value"
    }
  ]
}
The result at index zero belongs to input record zero. The result at index one belongs to input record one.
Do not retry the entire batch without examining the individual results. A full retry can update already-successful records or create duplicates if the operation is changed from upsert to insert.
Automation controls
CRM record APIs can trigger workflows, approvals, blueprints, pathfinder, and orchestration features depending on the operation and input.
An empty trigger list disables the standard trigger set for the request. skip_feature_execution can skip Cadences for the specified action. These controls are not a universal bypass of every CRM rule.
Use the same trigger policy on every replay attempt. Record it in the evidence.
Lesson check
1. What determines whether Upsert inserts or updates?
2. What is the maximum number of records per Upsert request?
3. How should a client map a 207 response to input records?
4. Why is Account_Name not an acceptable substitute for the future Nova summary identity?
5. Does trigger: [] mean that every CRM control is bypassed?
### Lesson 5 — Compose CRM requests and verify GraphQL availability

Composite API
Composite API combines up to five CRM subrequests:
POST {api_domain}/crm/v8/__composite_requests
Authorization: Zoho-oauthtoken <access_token>
Content-Type: application/json
The composite scope is:
ZohoCRM.composite_requests.CUSTOM
The caller also needs the scope required by every subrequest.
A dependent two-step example:
{
  "rollback_on_fail": true,
  "parallel_execution": false,
  "__composite_requests": [
    {
      "sub_request_id": "upsert1",
      "method": "POST",
      "uri": "/crm/v8/Accounts/upsert",
      "body": {
        "data": [
          {
            "Account_Name": "NOVCH14-COMP-001",
            "Description": "Composite fixture"
          }
        ],
        "duplicate_check_fields": [
          "Account_Name"
        ],
        "trigger": []
      }
    },
    {
      "sub_request_id": "read1",
      "method": "GET",
      "uri": "/crm/v8/Accounts/@{upsert1:$.data[0].details.id}",
      "params": {
        "fields": "Account_Name,Description,Modified_Time"
      }
    }
  ]
}
Use parallel_execution: false when a later request references an earlier response. Use parallel_execution: true only when requests are independent or the references are valid under the documented execution rules.
Important Composite behavior:
- Maximum five subrequests.
- Delete operations require an ID in the URL.
- Create, update, upsert, and delete subrequests are limited to one record.
- Search, Get Records, and COQL subrequests are limited to 25 records.
- rollback_on_fail and parallel_execution cannot both be true.
- With rollback enabled, a failed subrequest can cause CRM changes in the composite to be rolled back.
- With rollback disabled, some subrequests can succeed while others fail.
- The outer HTTP response does not replace inspection of each subrequest.
- A 200 composite response can still contain subrequest-level errors.
- A 207 response can indicate that only some subrequests were triggered.
Composite rollback applies to the supported CRM subrequests in that composite. It does not roll back an email, webhook, external service call, Creator write, or other side effect outside that CRM transaction.
GraphQL retrieval boundary
GraphQL retrieval is included in this chapter because it is a possible advanced retrieval style. The current public CRM v8 documentation reviewed for this chapter does not provide a verifiable GraphQL endpoint, schema, scope, supported-module list, or limit contract.
Therefore, do not invent a URL such as:
https://<api_domain>/crm/v8/graphql
and do not invent a scope such as:
ZohoCRM.graphql.READ
Before using GraphQL in a tenant, record:
item,value,source,observed
endpoint,<fill>,current official tenant/API documentation,NOT_YET_VERIFIED
version,<fill>,current official tenant/API documentation,NOT_YET_VERIFIED
scope,<fill>,current official tenant/API documentation,NOT_YET_VERIFIED
schema URL,<fill>,current official tenant/API documentation,NOT_YET_VERIFIED
supported modules,<fill>,current official tenant/API documentation,NOT_YET_VERIFIED
pagination contract,<fill>,current official tenant/API documentation,NOT_YET_VERIFIED
limits,<fill>,current official tenant/API documentation,NOT_YET_VERIFIED
Until these values are verified, use CRM v8 Records, COQL, or Bulk Read. A generic GraphQL query shape is not a CRM API contract.
Lesson check
1. How many subrequests can a Composite call contain?
2. When should parallel_execution be false?
3. Can an outer 200 response hide a subrequest error?
4. What does Composite rollback not cover?
5. Why is a GraphQL endpoint not included as an executable example here?
## Visual explanation

flowchart TD
    A[Nova integration question] --> B{Bounded record read?}
    B -->|Known module and IDs| C[Records API]
    B -->|Lookup joins or aggregate| D[COQL]
    B -->|More than normal page range| E[Bulk Read job]
    B -->|Large insert/update/upsert| F[Bulk Write job]
    B -->|Small insert-or-update| G[Upsert]
    B -->|Up to five CRM subrequests| H[Composite]
    B -->|GraphQL requested| I[Verify published tenant contract]
    I -->|Verified| J[Use documented GraphQL client]
    I -->|Not verified| D
Plain-text explanation:
- Use the simplest API that answers the question.
- COQL is a query language, not a write API.
- Bulk APIs are asynchronous jobs, not enlarged synchronous requests.
- Upsert is a bounded write keyed by duplicate-check fields.
- Composite reduces round trips but does not make external systems transactional.
- GraphQL must be treated as a documented capability, not a guessed endpoint.
## Worked case

Nova advanced retrieval and disposable CRM update
The goal is to inspect a completed Nova visit, identify its CRM customer Account, and update only a disposable training Account.
This case does not create the future CRM service-summary module.
Inputs
Input	Value
CRM API version	v8
Creator API version	v2.1
CRM scratch Account marker	NOVCH11LAB901A
Synthetic Cedar Account ID	"5725767000001000001"
Synthetic Beacon Account ID	"5725767000001000002"
Synthetic Product ID	"5725767000002000001"
Nova Request key	NOV-REQ-801
Nova Visit key	NOV-VISIT-801
Event key	NOV-REQ-801:completed:v1
Owner target	Actual active CRM user must be resolved
CRM environment	Dedicated training organization
CRM API domain	Use the token’s returned api_domain
The synthetic IDs are examples only. They must not be sent to a live organization.
Step 1 — Retrieve the scratch Account with COQL
{
  "select_query":
    "select Account_Name, Description, Owner, Modified_Time, id
     from Accounts
     where Account_Name = 'NOVCH11LAB901A'
     limit 0, 200"
}
Expected logical result:
Account_Name,Description,Owner,id
NOVCH11LAB901A,NOV-CH11-901|updated,<owner object>,<captured account id>
Capture the Account ID only after:
- The Account name exactly matches the marker.
- The organization and API domain match the lab.
- The response contains exactly one matching record.
Step 2 — Retrieve related Contacts
{
  "select_query":
    "select Last_Name, Email, Account_Name, Account_Name.Account_Name
     from Contacts
     where Account_Name.Account_Name = 'NOVCH11LAB901A'
     limit 0, 200"
}
Possible expected results:
- Zero Contacts because the scratch Account has no Contact.
- One or more Contacts with nullable Email.
- A query error if the tenant’s fields or relationship differ.
Do not convert zero Contacts into a missing CRM Account. These are separate facts.
Step 3 — Count scratch Accounts by owner
{
  "select_query":
    "select COUNT(Owner), Owner
     from Accounts
     where Account_Name like 'NOVCH14%'
     group by Owner
     limit 0, 200"
}
This is a reporting query. It does not establish that a specific user can own the future summary.
Step 4 — Upsert two disposable records
Use two records to demonstrate ordered results:
{
  "data": [
    {
      "Account_Name": "NOVCH14-UP-001",
      "Description": "CH14 upsert record one"
    },
    {
      "Account_Name": "NOVCH14-UP-002",
      "Description": "CH14 upsert record two"
    }
  ],
  "duplicate_check_fields": [
    "Account_Name"
  ],
  "trigger": []
}
Expected result:
input_position,expected_action,expected_marker
0,insert_or_update,NOVCH14-UP-001
1,insert_or_update,NOVCH14-UP-002
The action must be read from each returned result. On a replay, the expected action will usually change from insert to update.
Step 5 — Use a Composite read-back
After capturing the Account ID returned by Upsert, use a bounded Composite request:
{
  "rollback_on_fail": false,
  "parallel_execution": false,
  "__composite_requests": [
    {
      "sub_request_id": "readScratch",
      "method": "GET",
      "uri": "/crm/v8/Accounts/<captured_account_id>",
      "params": {
        "fields": "Account_Name,Description,Modified_Time"
      }
    },
    {
      "sub_request_id": "readProduct",
      "method": "GET",
      "uri": "/crm/v8/Products/5725767000002000001",
      "params": {
        "fields": "Product_Name,id"
      }
    }
  ]
}
These reads are independent, so parallel execution could be appropriate. The example keeps sequential execution to make evidence ordering simpler.
Step 6 — Cleanup
Delete only records whose names begin with:
NOVCH14-
Before deleting:
1. Read the record.
2. Confirm its marker.
3. Record its ID.
4. Delete by exact ID.
5. Read or search to confirm the intended cleanup.
6. Do not delete the Chapter 11 scratch Account unless the Chapter 11 cleanup plan permits it.
Evidence worksheet
step,operation,resource,marker_or_id,expected_result,observed_result,status
1,COQL read,Accounts,NOVCH11LAB901A,one exact scratch Account,<fill>,NOT_YET_RUN
2,COQL join,Contacts,NOVCH11LAB901A,zero or more related Contacts,<fill>,NOT_YET_RUN
3,COQL aggregate,Accounts,NOVCH14%,grouped owner count,<fill>,NOT_YET_RUN
4,Upsert,Accounts,NOVCH14-UP-001,ordered record result,<fill>,NOT_YET_RUN
5,Upsert,Accounts,NOVCH14-UP-002,ordered record result,<fill>,NOT_YET_RUN
6,Composite read-back,captured IDs,NOVCH14-,per-subrequest status,<fill>,NOT_YET_RUN
7,Cleanup,Accounts,NOVCH14-,only lab records removed,<fill>,NOT_YET_RUN
## Try it yourself — guided practice

Practice A — Write and validate a COQL query
Dependencies
- Dedicated CRM training organization.
- CRM v8 access token.
- ZohoCRM.coql.READ.
- Read permission for Accounts and Contacts.
- Actual captured scratch Account marker.
Task
Write three queries:
1. Exact Account retrieval.
2. Contact-to-Account lookup retrieval.
3. Grouped owner count.
For each query, record:
- Query text.
- Selected fields.
- Criteria count.
- Join count.
- Expected row count.
- Actual row count.
- more_records value.
- Whether the result is simulated or observed.
Expected result
The query parser should accept valid API names and return a JSON response. A query can correctly return zero records without being a transport failure.
Practice B — Test Upsert replay
Send this payload twice:
{
  "data": [
    {
      "Account_Name": "NOVCH14-REPLAY-001",
      "Description": "Replay fixture"
    }
  ],
  "duplicate_check_fields": [
    "Account_Name"
  ],
  "trigger": []
}
Record:
attempt,action,record_id,description_after,observed
1,<insert or update>,<fill>,Replay fixture,NOT_YET_RUN
2,<insert or update>,<fill>,Replay fixture,NOT_YET_RUN
Expected logical behavior:
- First attempt: insert if no marker exists.
- Second attempt: update of the same record if the duplicate field is still present.
- The record ID should remain the same.
- This is API-level duplicate matching, not proof of a distributed idempotency ledger.
Practice C — Run a Bulk Read job
Use a bounded marker:
Account_Name starts with NOVCH14-
Request only:
Account_Name, Description, Modified_Time, id
Record:
job_id,initial_state,completed_state,count,download_url,downloaded,observed
<fill>,<fill>,<fill>,<fill>,<fill>,<yes/no>,NOT_YET_RUN
Do not repeatedly poll without a bound. Use a documented interval and maximum attempt count. If the job remains incomplete, record the state and stop.
Practice D — Run a two-row Bulk Write
Prepare:
Account_Name,Description
NOVCH14-BULK-001,CH14 bulk fixture one
NOVCH14-BULK-002,CH14 bulk fixture two
1. ZIP the CSV.
2. Upload it to the documented upload domain.
3. Capture file_id.
4. Create a Bulk Write upsert job.
5. Poll job status.
6. Download the result ZIP.
7. Inspect STATUS, RECORD_ID, and ERRORS.
8. Clean up only rows whose markers match.
Expected result:
Account_Name,STATUS,RECORD_ID,ERRORS
NOVCH14-BULK-001,ADDED or UPDATED,<id>,
NOVCH14-BULK-002,ADDED or UPDATED,<id>,
This is an expected result pattern, not a claim that the tenant job succeeded.
## Independent challenge

Design an advanced CRM retrieval and write plan for the following Nova request:
“Show completed service visits for Cedar Works, include the CRM Account name and owner, count the related customer contacts, and update a disposable CRM record with the resulting summary.”
Your design must answer:
Design question	Your answer
Source of completed visit facts
Source of CRM Account ID
COQL base module
Lookup path
Maximum join depth used
Aggregate used
External ID needed?
Upsert duplicate field
Normal read or Bulk Read?
Bulk Write needed?
Composite required?
Rollback setting
Replay behavior
Read-back target
Cleanup marker
GraphQL contract verified?
Create these failure fixtures:
Failure fixture 1 — Query joins exceed the limit
Attempt a COQL query with three lookup joins.
Expected analysis:
- Stop before sending a production request.
- Reduce the query to two joins or split the retrieval.
- Do not assume the server will optimize the third join.
Failure fixture 2 — Bulk Write partial result
Assume two rows are uploaded:
Account_Name,Description
NOVCH14-BULK-VALID,valid row
,missing Account_Name
Expected analysis:
- Inspect the result CSV.
- Keep the successful row’s record ID.
- Record the failed row’s error.
- Do not retry the entire file blindly.
- Clean up the successful marker deliberately.
Failure fixture 3 — Composite subrequest failure
Assume an Upsert succeeds but a dependent read fails.
Compare:
{
  "rollback_on_fail": true,
  "parallel_execution": false
}
with:
{
  "rollback_on_fail": false,
  "parallel_execution": false
}
Explain:
- Which CRM changes may remain.
- Which subrequest results must be inspected.
- Why a rollback does not affect an external email or webhook.
- Why the final state still requires a read-back.
## Common problems and recovery

Symptom	Likely cause	Recovery
COQL returns INVALID_QUERY	Display label or invalid field API name	Read Fields Metadata and replace labels with API names
COQL returns syntax error	Missing FROM, malformed criteria, or unbalanced parentheses	Simplify the query and add criteria incrementally
COQL returns too many joins	More than two lookup relationships	Split the query or retrieve a narrower path
Aggregate query fails	Missing GROUP BY with non-aggregate fields	Group every non-aggregate selected field
Aggregate query fails on text field	Unsupported aggregate data type	Use numeric, lookup, or supported picklist fields as documented
COQL result differs between pages	Unstable ordering or changing data	Add deterministic ordering and record retrieval time
COQL page token is rejected	Parameters changed or token belongs to another user	Reuse the exact bound parameters and original user
Bulk Read job remains IN PROGRESS	Asynchronous processing	Poll within a bounded policy and record the final known state
Bulk Read download fails after completion	Result window expired	Create a new job; do not claim the old file remains available
Bulk Read export lacks expected order	Bulk Read does not guarantee custom sorting	Sort the downloaded file locally only after recording source semantics
Bulk Write upload rejected	File is not a ZIP, is too large, or lacks organization header	Verify ZIP, size, X-CRM-ORG, and feature: bulk-write
Bulk Write rows are skipped	Invalid field, duplicate, mandatory field, or lookup mapping	Read the result CSV ERRORS column
Upsert inserts a duplicate	Wrong duplicate field or field not unique	Verify duplicate-check configuration and metadata
Upsert updates the wrong record	Duplicate field is not sufficiently unique	Stop, inspect matching records, and use a verified external ID
207 Multi-Status treated as failure of all rows	Outer status misunderstood	Map each response entry to its input position
Composite returns HTTP 200 with errors	Outer success means the composite was processed	Inspect every subrequest body and status
Composite reference invalid	Wrong JSONPath, parallel execution, or failed source request	Validate the source result and reference path
CRM rollback expected but target remains changed	Operation was outside the composite or rollback was disabled	Read all targets and classify actual state
GraphQL endpoint cannot be verified	Current tenant documentation does not publish a contract	Use COQL or Bulk Read; do not guess the endpoint
CRM ID loses digits in JavaScript	ID passed through Number	Keep it as an exact string
Token appears in evidence	Raw request or debug output captured	Redact and regenerate evidence without secrets
## Check your understanding

 1. What is COQL designed to do that a simple module read may not do conveniently?
 2. How many lookup joins does the current COQL documentation allow?
 3. What is the purpose of an external ID?
 4. What is the maximum number of records in one Upsert request?
 5. What does an Upsert response’s action value tell you?
 6. What does HTTP 207 mean for multi-record CRM writes?
 7. Is Bulk Read synchronous?
 8. What is the purpose of the Bulk Write result CSV?
 9. How many subrequests can Composite API contain?
10. When should Composite use rollback_on_fail: true?
11. Does Composite rollback external side effects?
12. Why should you avoid guessing a GraphQL endpoint?
13. Which value must remain an exact string in JavaScript?
14. What is the correct recovery after an uncertain CRM write?
15. What evidence distinguishes a simulated result from an actual tenant result?
## Solutions and explanations

 1. COQL supports SQL-like selection, criteria, lookup traversal, grouping, aggregates, and pagination in one retrieval contract.
 2. The documented COQL limit is two lookup joins.
 3. An external ID stores an identifier from another system so records can be found or upserted without depending only on CRM-generated IDs.
 4. Up to 100 records per Upsert request.
 5. It states whether the matching record was inserted or updated.
 6. It means that individual records in the request can have different outcomes. The response must be mapped by input order.
 7. No. Bulk Read creates an asynchronous job, which must be checked before the result is downloaded.
 8. It identifies row-level status, CRM record ID, and errors for skipped or unprocessed rows.
 9. Up to five.
10. Use it when the supported CRM subrequests form one dependent CRM operation and reverting CRM changes on failure is an intentional requirement.
11. No. It does not undo email, webhook, Creator, external service, or other side effects outside the composite CRM operation.
12. The current public v8 documentation reviewed for this chapter does not provide a verified GraphQL endpoint, schema, scope, or limits. An invented endpoint can send credentials to the wrong target or produce an invalid implementation.
13. CRM record IDs, external IDs, Request keys, Visit keys, and event keys must remain exact strings.
14. Preserve the original identity and facts, read the target by its exact ID, compare the stored result, and only then decide whether another write is necessary.
15. Actual evidence includes the tenant, environment, organization, request time, response status, safe response code, captured target ID, and read-back result. A local fixture or expected response must be labeled as simulated or expected.
## Chapter recap and next step

Advanced CRM APIs are different tools for different shapes of work:
- Use Records API for bounded module operations.
- Use COQL for joins, criteria, aliases, aggregates, and external-field retrieval.
- Use ordinary pagination for manageable result sets.
- Use Bulk Read for asynchronous large exports.
- Use Bulk Write for asynchronous large inserts, updates, or upserts.
- Use Upsert for small insert-or-update operations with a verified duplicate field.
- Use Composite for up to five CRM subrequests with explicit dependency and rollback decisions.
- Use GraphQL only after its endpoint, schema, scope, version, and limits are verified for the tenant.
Every advanced API needs a recovery plan:
1. Preserve the original input identity.
2. Classify the response at both outer and per-record or per-subrequest levels.
3. Read back uncertain writes.
4. Avoid blind retries.
5. Keep IDs and external keys as opaque strings.
6. Record actual tenant evidence separately from expected behavior.
7. Never expose tokens, client secrets, raw Authorization headers, or confidential CRM responses.
The next chapter is:
C02-CH15 — Reliable Event-Driven Integration
## Glossary and further reading

Glossary
Aggregate
A calculation such as COUNT, SUM, AVG, MIN, or MAX performed during a query.
COQL
CRM Object Query Language, a SQL-like read query language for Zoho CRM.
Composite API
An endpoint that combines up to five CRM subrequests in one request.
Duplicate-check field
A field used by CRM Upsert to decide whether a record already exists.
External ID
An organization-defined CRM field containing an identifier from another system.
Bulk Read
An asynchronous CRM export job that produces a downloadable CSV inside a ZIP file.
Bulk Write
An asynchronous CRM insert, update, or upsert job based on ZIP-compressed CSV input.
Lookup path
A COQL field path that traverses one or more CRM lookup relationships.
Page token
A user-specific continuation token for CRM record pagination.
Partial result
A response in which individual records or subrequests have different outcomes.
Read-back
A read performed after a write to verify the stored target state.
Upsert
An insert-or-update operation determined by duplicate-check fields.
Further reading
- CRM v8 Query API overview (https://www.zoho.com/crm/developer/docs/api/v8/COQL-Overview.html)
- Get Records through COQL (https://www.zoho.com/crm/developer/docs/api/v8/Get-Records-through-COQL-Query.html)
- CRM v8 Get Records (https://www.zoho.com/crm/developer/docs/api/v8/get-records.html)
- CRM v8 Field Metadata (https://www.zoho.com/crm/developer/docs/api/v8/field-meta.html)
- CRM v8 Upsert Records (https://www.zoho.com/crm/developer/docs/api/v8/upsert-records.html)
- CRM v8 Insert Records (https://www.zoho.com/crm/developer/docs/api/v8/insert-records.html)
- CRM v8 Update Records (https://www.zoho.com/crm/developer/docs/api/v8/update-records.html)
- CRM v8 Composite API (https://www.zoho.com/crm/developer/docs/api/v8/composite-api.html)
- CRM v8 Composite overview (https://www.zoho.com/crm/developer/docs/api/v8/composite-overview.html)
- CRM v8 Bulk Read overview (https://www.zoho.com/crm/developer/docs/api/v8/bulk-read/overview.html)
- CRM v8 Create Bulk Read Job (https://www.zoho.com/crm/developer/docs/api/v8/bulk-read/create-job.html)
- CRM v8 Bulk Read Job Details (https://www.zoho.com/crm/developer/docs/api/v8/bulk-read/job-details.html)
- CRM v8 Bulk Read limitations (https://www.zoho.com/crm/developer/docs/api/v8/bulk-read/limitations.html)
- CRM v8 Bulk Write overview (https://www.zoho.com/crm/developer/docs/api/v8/bulk-write/overview.html)
- CRM v8 Bulk Write file upload (https://www.zoho.com/crm/developer/docs/api/v8/bulk-write/upload-file.html)
- CRM v8 Create Bulk Write Job (https://www.zoho.com/crm/developer/docs/api/v8/bulk-write/create-job.html)
- CRM v8 Bulk Write Job Details (https://www.zoho.com/crm/developer/docs/api/v8/bulk-write/job-details.html)
- CRM v8 Download Bulk Write Result (https://www.zoho.com/crm/developer/docs/api/v8/bulk-write/download-result.html)
- CRM v8 Modules API (https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html)
