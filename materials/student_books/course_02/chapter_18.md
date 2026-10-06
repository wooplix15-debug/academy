# Widgets and Contextual Data

## What you will learn

By the end of this chapter, you will be able to:
- Explain how CRM Widgets differ from Client Scripts, Functions, and Queries.
- Build the basic HTML, CSS, and JavaScript structure of a CRM Widget.
- Use the Zoho Widget CLI to create, run, validate, and package a widget.
- Register widget lifecycle listeners and inspect contextual data.
- Use the Widget SDK to access current-user and CRM context information.
- Distinguish internal hosting from external hosting.
- Use CRM Queries with Module, COQL, CRM REST API, REST API, database, and cloud database sources.
- Use query variables such as {{ACCOUNT_ID}}.
- Understand Query schemas, result paths, labels, field types, and serializers.
- Create safe serializer output for a contextual Nova panel.
- Protect database and external-service sources with least privilege, trusted domains, and read-only settings.
- Test null, missing-context, permission, source, schema, serializer, and package failures.
- Keep browser widgets as presentation and interaction layers rather than business-authority layers.
This chapter creates a contextual training widget for the CRM Account marker:
NOVCH18LAB901A
The widget does not implement a production Creator-to-CRM synchronization. Creator remains the authority for Nova intake, assignment, inspection, and completion. CRM remains the authority for CRM customer and service reference facts.
## Lessons

### Lesson 1 — Understand Widgets, context, and hosting

A Widget is an embeddable HTML, CSS, and JavaScript component that runs inside a CRM context.
Widgets can be used in:
- Dashboards.
- Web tabs.
- Custom buttons.
- Custom related lists.
- Wizards.
- Signals.
- Settings.
- Blueprints.
A Widget can display data from CRM or an external service and provide an interactive interface without requiring the user to leave CRM.
Widget versus Client Script
Capability	Client Script	Widget
Main purpose	Modify CRM page behavior	Provide a custom embedded interface
Primary technology	JavaScript in CRM page context	HTML, CSS, JavaScript application
UI size	Field and page interactions	Panels, forms, cards, tables, charts
Context	Page and field events	Widget lifecycle and contextual event payload
Hosting	Managed by CRM	Internal or external hosting
Reusable package	Static resources	ZET project and packaged widget
External integrations	Trusted-domain browser calls, ZDK	Widget SDK, ZRC, connections, external services
Best use	Immediate field guidance	Contextual dashboard or operational panel
A Widget can contain more structure than a Client Script, but it still runs in a browser. Do not put client secrets or permanent credentials into widget files.
Widget context
A Widget can subscribe to CRM events:
ZOHO.embeddedApp.on("PageLoad", function(data) {
    console.log("CRM page context", data);
});

ZOHO.embeddedApp.init();
The PageLoad callback receives context data from the CRM page. The exact keys depend on the place where the Widget is embedded.
Do not assume that every location sends the same context object. During setup:
1. Log the context keys.
2. Remove sensitive values from exported evidence.
3. Identify the current module.
4. Identify the current record ID, if supplied.
5. Identify the placement or button context.
6. Store only the fields that the widget requires.
A Widget that is opened from an Account detail page may receive an Account context. A dashboard Widget may have no current record. A button Widget may receive action-specific context. Treat missing context as a supported condition.
Internal hosting
With internal hosting:
- The widget files are uploaded to CRM.
- CRM hosts the static package.
- The package is created and tested with the Zoho CLI.
- The upload is a ZIP package.
External hosting
With external hosting:
- You host the Widget at your own URL.
- CRM embeds the external URL.
- You are responsible for hosting availability, TLS, content security, deployment, and access controls.
- The external host must be configured correctly for the CRM embedding context.
A local development server can be used for testing. The current Widget documentation describes:
zet run
and using the generated local URL as the external Widget Base URL for a production or Sandbox test.
Widget size and edition limits
The current Widget documentation states:
- Widgets require Developer Permissions.
- Widgets are available in Professional, Enterprise, and Ultimate editions.
- Enterprise and Ultimate editions allow up to 200 Widgets.
- The maximum uploaded Widget ZIP size is 25 MB.
Verify the current tenant edition and limits before deployment.
Lesson check
1. What is the main difference between a Client Script and a Widget?
2. Why should a Widget handle missing context?
3. What is the difference between internal and external hosting?
4. Where should a client secret be stored?
5. What must be recorded before relying on a Widget context key?
### Lesson 2 — Build, run, validate, and package a Widget

The Zoho Widget CLI is called zet.
Prerequisites
- Node.js and npm.
- Access to the CRM Developer Hub.
- A CRM Sandbox or dedicated training organization.
- Developer Permissions.
- A controlled Widget name.
- A local development directory.
Create a Widget project:
npm install -g zoho-extension-toolkit
zet
zet init
During zet init:
1. Select Zoho CRM.
2. Enter a Widget project name.
3. Open the generated project directory.
A typical project contains:
nova-ch18-context-widget/
├── app/
│   ├── widget.html
│   ├── widget.js
│   └── widget.css
└── plugin-manifest.json
The exact generated files may vary by current CLI version. Treat the generated manifest and project structure as the source of truth for that CLI version.
HTML
A minimal widget.html:
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Nova Context</title>
  <link rel="stylesheet" href="widget.css">
</head>
<body>
  <main id="app" aria-live="polite">
    <h1>Nova CRM Context</h1>
    <p id="status">Loading context…</p>
    <dl>
      <dt>Module</dt>
      <dd id="module">Unknown</dd>
      <dt>Record</dt>
      <dd id="record">Unknown</dd>
      <dt>Account marker</dt>
      <dd id="marker">Not checked</dd>
    </dl>
  </main>

  <script src="https://static.zohocdn.com/crm/widgets/v1.5/js/ZohoEmbededAppSDK.min.js"></script>
  <script src="widget.js"></script>
</body>
</html>
Use the current Widget SDK URL supplied by the tenant documentation or generated project. Do not copy a versioned SDK URL from an old project without checking compatibility.
CSS
:root {
  color-scheme: light;
  font-family: system-ui, sans-serif;
}

body {
  margin: 0;
  padding: 1rem;
  color: #1f2937;
  background: #ffffff;
}

main {
  max-width: 42rem;
}

dl {
  display: grid;
  grid-template-columns: 10rem 1fr;
  gap: 0.5rem 1rem;
}

dt {
  font-weight: 700;
}

dd {
  margin: 0;
  overflow-wrap: anywhere;
}

#status {
  padding: 0.5rem;
  background: #eef2ff;
}
JavaScript lifecycle
const state = {
  context: null,
  module: null,
  recordId: null
};

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) {
    element.textContent = value == null ? "Unknown" : String(value);
  }
}

function renderContext(context) {
  state.context = context || {};
  state.module = state.context.Module || state.context.module || null;
  state.recordId =
    state.context.EntityId ||
    state.context.entityId ||
    state.context.recordId ||
    null;

  setText("module", state.module);
  setText("record", state.recordId);
  setText(
    "status",
    state.recordId
      ? "Context received. Waiting for a verified query result."
      : "No record context was supplied."
  );
}

ZOHO.embeddedApp.on("PageLoad", function(context) {
  renderContext(context);
  console.log("Widget context received", context);
});

ZOHO.embeddedApp.init();
The fallback key names in this teaching example are intentionally defensive. The learner must inspect the actual context object in the tenant and then replace the fallback logic with the supported context contract for the selected Widget placement.
Never use an arbitrary query parameter as proof of record identity. The Widget must validate context against the CRM or Query response before displaying record-specific information.
Local run
Start the development server:
zet run
The CLI serves the Widget locally, commonly on port 5000.
Use the generated local URL as the Base URL for an external-hosted Widget in a Sandbox or training organization. Local hosting is machine-specific.
Validate and package
Validate the project:
zet validate
Package the project:
zet pack
The CLI creates an uploadable ZIP in the project’s distribution directory.
The validation result proves package structure and CLI rules. It does not prove:
- CRM context mapping.
- User permissions.
- Query results.
- External source access.
- Production availability.
- Correct handling of missing data.
Lesson check
1. Which command starts the local Widget server?
2. Which command validates the Widget package?
3. Which command creates the uploadable package?
4. Why does a valid package not prove that the Widget works in CRM?
5. Why should the Widget inspect context before making a record-specific query?
### Lesson 3 — Use the Widget SDK and contextual data safely

Register before initializing
The usual lifecycle pattern is:
ZOHO.embeddedApp.on("PageLoad", function(data) {
  // Use the context only after this event.
});

ZOHO.embeddedApp.init();
Register listeners before calling init().
A Widget may also use the CRM configuration API:
ZOHO.CRM.CONFIG.getCurrentUser().then(function(user) {
  console.log("Current user context", user);
});
Use the current-user result for presentation or server-side request routing. Do not treat a browser-provided user object as proof of business authorization.
Context is not authorization
A Widget may receive:
{
  "Module": "Accounts",
  "EntityId": "<opaque CRM ID>",
  "Placement": "record_detail"
}
This tells the Widget what the CRM page intends to display. It does not prove that:
- The record still exists.
- The user can read every field.
- The record belongs to the expected customer.
- A write is authorized.
- A CRM connection can update the record.
- The Widget should expose confidential fields.
Before displaying or updating a record:
1. Validate the module.
2. Validate the record ID format.
3. Use a bounded CRM Query or server-side Function.
4. Confirm the marker or record identity.
5. Render only approved fields.
Contextual rendering
A safe rendering function should handle nulls:
function renderAccountSummary(record) {
  const accountName = record?.Account_Name || "Unknown Account";
  const description = record?.Description || "No description";
  const ownerName = record?.Owner?.name || "Owner unavailable";

  setText("marker", accountName);
  setText("status", `${ownerName}: ${description}`);
}
Do not render raw HTML from CRM fields unless the content is intentionally sanitized and the Widget’s output contract allows it.
Use textContent, not innerHTML, for ordinary CRM values.
Widget to server-side Function
For a sensitive action:
Widget context
  -> server-side Function
  -> CRM or external Connection
  -> safe response
  -> Widget rendering
The server-side Function should re-read the record and enforce the marker, ownership, and business rules. The Widget must not send a secret or claim that the user is authorized merely because the Widget is visible.
Widget placement
The Widget type affects its context:
Placement	Typical context
Dashboard	Organization or dashboard context
Web tab	Page-level context, possibly no record
Custom Button	Current record or action context
Custom Related List	Parent record context
Wizard	Wizard and screen context
Signal	Signal notification context
Settings	Configuration context
Blueprint	Transition context
Test every placement that the Widget supports. Do not assume that a record detail Widget and dashboard Widget receive the same context.
Lesson check
1. Why must listeners be registered before ZOHO.embeddedApp.init()?
2. Does Widget context prove authorization?
3. Why should ordinary CRM values be rendered with textContent?
4. Which Widget placement is most likely to have a parent record context?
5. Where should sensitive CRM writes occur?
### Lesson 4 — Use CRM Queries for contextual data

CRM Queries provide a managed way to retrieve and shape data for CRM components such as:
- Canvas record detail views.
- Canvas list views.
- Kiosk screens.
- Kiosk decision components.
- Custom related lists.
Queries can use:
- CRM Module sources.
- COQL.
- Zoho CRM REST API.
- External REST API sources.
- Database sources.
- Cloud database sources.
Module query
A Module query retrieves structured records from one CRM module.
Current documented limits include:
- Up to 50 selected fields.
- Up to two related lookup fields in the Module query configuration.
- Criteria can use static or dynamic values.
- A record ID can be passed as a dynamic variable.
- Results can be sorted.
For the Nova Account context panel, define:
Query name: Nova CH18 Account Context
API name: nova_ch18_account_context
Source: Zoho CRM Module
Module: Accounts
Fields:
  - Account_Name
  - Description
  - Owner
  - Modified_Time
Criteria:
  Account ID equals {{ACCOUNT_ID}}
The variable is declared using:
{{ACCOUNT_ID}}
When the Query is associated with a Canvas or custom related list, map ACCOUNT_ID to the current Account record ID.
COQL query
Use a COQL Query when you need joins, aggregates, or more complex criteria.
Example:
select Account_Name,
       Description,
       Owner,
       Modified_Time,
       id
from Accounts
where id = '{{ACCOUNT_ID}}'
limit 0, 1
The exact variable substitution and quoting behavior must be tested in the Query Workbench. Keep CRM IDs as strings and do not place unescaped user text directly into a COQL statement.
CRM REST API source
The built-in Zoho CRM REST API source can access CRM metadata and other supported REST endpoints.
The current Query documentation recommends using Module or COQL Query types for CRM record retrieval. Use the CRM REST API source for cases such as:
- Module metadata.
- Field metadata.
- Layout metadata.
- User or configuration metadata.
It is not the preferred record retrieval source for this lab.
External REST API source
An external REST API source can:
- Define a base URL.
- Define default parameters and headers.
- Use a Connection.
- Use GET, POST, PUT, PATCH, or DELETE.
- Map response data to a Query schema.
Use an external REST source only after:
- The domain is approved.
- The Connection is configured.
- The response contract is documented.
- The request and response fields are minimized.
- The source has appropriate read-only settings where possible.
Database and cloud database sources
Queries can connect to database and cloud database sources such as:
- MySQL.
- Microsoft SQL.
- PostgreSQL.
- Amazon RDS.
- Microsoft Azure.
- Other supported cloud database platforms.
Use:
- SSL.
- Least-privilege database credentials.
- Read-only sources for dashboards and contextual views.
- A configured database time zone.
- A connection timeout.
- Database-side access controls.
The current documentation warns that Developer users may access configured sources. Do not connect a source using a superuser credential unless that exposure is intentionally approved.
Query limits
The current SQL Query Limits documentation lists:
Limit	Documented value
Professional edition queries	100
Enterprise edition queries	250
Ultimate edition queries	500
REST API sources, Enterprise/Ultimate	200
SQL sources, Enterprise/Ultimate	5
Selected columns	50
Required SELECT limit	Yes
Default SELECT limit	100
Maximum SELECT limit	100
Joins	5
WHERE items or conditions	50
GROUP BY items	50
ORDER BY items	50
HAVING items	50
Subqueries	Not supported
These limits apply to the Query feature and should be verified against the current tenant.
Lesson check
1. What is the purpose of {{ACCOUNT_ID}}?
2. When should a Module Query be preferred over a REST API Query?
3. Why should a database source use a read-only credential for contextual display?
4. What is the maximum documented SELECT limit for SQL Query sources?
5. What is the risk of using a broad database credential?
### Lesson 5 — Manage schemas and serializers

Query schema
After a Query executes, CRM generates a schema containing:
- Result path.
- CRM field type.
- Label.
Example response:
{
  "data": [
    {
      "Account_Name": "NOVCH18LAB901A",
      "Description": "CH18 widget fixture",
      "Owner": {
        "name": "Training User",
        "id": "<opaque user ID>"
      },
      "Modified_Time": "<ISO timestamp>",
      "id": "<opaque account ID>"
    }
  ]
}
A schema might describe:
path,crm_field_type,label
data[].Account_Name,string,Account Name
data[].Description,multi_line,Description
data[].Owner,lookup,Owner
data[].Modified_Time,date_time,Modified Time
data[].id,long_integer,Record ID
The schema is a consumer contract. If a serializer changes:
Owner -> Owner_Name
the Widget, Canvas, or related list consuming Owner must be updated.
Treat schema changes as versioned integration changes.
Serializer
A Serializer is JavaScript that transforms a Query response.
Example:
return result.map(function(record) {
    const owner = record.Owner || {};

    return {
        Account_Name: record.Account_Name || "Unknown",
        Description: record.Description || "",
        Owner_Name: owner.name || "Unavailable",
        Account_Id: String(record.id || ""),
        Has_Description:
            typeof record.Description === "string" &&
            record.Description.trim().length > 0
    };
});
A serializer should:
- Handle nulls.
- Preserve exact IDs as strings.
- Return only approved fields.
- Avoid adding secrets.
- Avoid creating arbitrary links from untrusted values.
- Keep output stable for its consuming component.
Lookup and URL enhancement
Query serializers can produce structured lookup values and links for custom related lists.
Example:
return result.map(function(record) {
    return {
        Account: {
            id: String(record.id),
            name: record.Account_Name || "Unknown",
            module: "Accounts"
        },
        Link: {
            label: "Open Account",
            href: "/crm/tab/Accounts/" + encodeURIComponent(record.id)
        }
    };
});
The actual CRM URL pattern must be confirmed for the tenant and placement. Do not build a link using an untrusted arbitrary host.
Schema and serializer testing
Test:
- Normal record.
- Missing Description.
- Null Owner.
- Missing ID.
- Duplicate records.
- Unexpected response shape.
- Empty array.
- Query error.
- Serializer exception.
- Long text.
- Exact ID preservation.
A serializer error should fail visibly in the Query or component. Do not silently render an empty panel and claim that the source returned no data.
Lesson check
1. What does the Query schema describe?
2. Why must a serializer preserve CRM IDs as strings?
3. What should happen when Owner is null?
4. Why should a schema change be treated as an integration change?
5. What should a serializer do with an unexpected response shape?
## Visual explanation

flowchart LR
    A[CRM Account context] --> B[Widget PageLoad]
    A --> C[Query variable mapping]
    C --> D[CRM Module or COQL Query]
    D --> E[Raw response]
    E --> F[Schema]
    F --> G[Serializer]
    G --> H[Widget or Canvas presentation]
    H --> I[User action]
    I --> J[Server-side Function or approved ZDK operation]
Plain-text explanation:
- The Widget receives a CRM context.
- A Query can receive the current record ID as a variable.
- The Query retrieves only approved data.
- The schema describes the response.
- The serializer creates a stable presentation shape.
- A user action requiring authority goes to a server-side Function.
- The Widget does not become the system of record.
## Worked case

Nova Context Panel
Create an isolated CRM Account:
Account_Name: NOVCH18LAB901A
Description: CH18 widget fixture
Capture the actual CRM ID:
artifact,module,marker,record_id,observed
CH18 widget Account,Accounts,NOVCH18LAB901A,<captured ID>,NOT_YET_RUN
Query configuration
Create a CRM Module Query:
Query name: Nova CH18 Account Context
API name: nova_ch18_account_context
Source: Zoho CRM Module
Module: Accounts
Select:
Account_Name
Description
Owner
Modified_Time
id
Configure a dynamic record ID criterion:
ID equals {{ACCOUNT_ID}}
Map ACCOUNT_ID to the current Account record when associating the Query with:
- A Canvas Record Detail component.
- A custom related list.
- Another supported contextual component.
Expected logical result:
{
  "Account_Name": "NOVCH18LAB901A",
  "Description": "CH18 widget fixture",
  "Owner": {
    "name": "<tenant user>",
    "id": "<opaque user ID>"
  },
  "Modified_Time": "<tenant timestamp>",
  "id": "<captured CRM ID>"
}
No live tenant result is claimed.
Serializer
Use:
return result.map(function(record) {
    const owner = record.Owner || {};
    const id = record.id == null ? "" : String(record.id);

    return {
        Marker: record.Account_Name || "Unknown",
        Description: record.Description || "No description",
        Owner_Name: owner.name || "Unavailable",
        Account_Id: id,
        Record_Link: {
            label: "Open Account",
            href: "/crm/tab/Accounts/" + encodeURIComponent(id)
        }
    };
});
If the consuming component expects a schema, update the schema to include:
path,type,label
data[].Marker,string,Marker
data[].Description,string,Description
data[].Owner_Name,string,Owner
data[].Account_Id,string,Account ID
data[].Record_Link,object,Account Link
Do not change Account_Id to a numeric type.
Widget
Create a Widget project:
zet init
cd nova-ch18-context-widget
zet run
app/widget.html:
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Nova Context Panel</title>
  <link rel="stylesheet" href="widget.css">
</head>
<body>
  <main>
    <h1>Nova Context Panel</h1>
    <p id="status">Waiting for CRM context…</p>

    <section aria-labelledby="context-heading">
      <h2 id="context-heading">Context</h2>
      <dl>
        <dt>Module</dt>
        <dd id="module">Unknown</dd>
        <dt>Record</dt>
        <dd id="record">Unknown</dd>
      </dl>
    </section>

    <section aria-labelledby="result-heading">
      <h2 id="result-heading">Safe result</h2>
      <pre id="result">No query result.</pre>
    </section>
  </main>

  <script src="https://static.zohocdn.com/crm/widgets/v1.5/js/ZohoEmbededAppSDK.min.js"></script>
  <script src="widget.js"></script>
</body>
</html>
app/widget.js:
const state = {
  context: null,
  safeContext: {
    module: null,
    recordId: null
  }
};

function write(id, value) {
  const element = document.getElementById(id);
  if (element) {
    element.textContent = value == null ? "Unknown" : String(value);
  }
}

function safeContext(context) {
  const data = context || {};
  const moduleName = data.Module || data.module || null;
  const recordId =
    data.EntityId ||
    data.entityId ||
    data.recordId ||
    null;

  return {
    module: moduleName,
    recordId: recordId == null ? null : String(recordId)
  };
}

function renderContext(context) {
  state.context = context;
  state.safeContext = safeContext(context);

  write("module", state.safeContext.module);
  write("record", state.safeContext.recordId);

  if (state.safeContext.module !== "Accounts") {
    write("status", "This panel is configured for Accounts.");
    return;
  }

  if (!state.safeContext.recordId) {
    write("status", "No Account record context was supplied.");
    return;
  }

  write("status", "Account context received.");
}

ZOHO.embeddedApp.on("PageLoad", function(context) {
  renderContext(context);
  console.log("CH18 context keys", Object.keys(context || {}));
});

ZOHO.embeddedApp.init();
The Widget displays context only. It does not directly trust the context to authorize a CRM write.
Cleanup
After evidence is recorded:
1. Remove the Query association.
2. Disable or delete the Widget.
3. Remove the CH18 Account.
4. Remove any external source or Connection created only for the lab.
5. Keep the package and evidence labeled as training artifacts.
## Try it yourself — guided practice

Practice A — Build and run the Widget
1. Install the CLI.
2. Run zet init.
3. Create the HTML, CSS, and JavaScript files.
4. Run zet run.
5. Configure an external-hosted Widget in a Sandbox with the local URL.
6. Open the Widget in its intended placement.
7. Capture the context keys without exporting confidential values.
8. Run zet validate.
9. Run zet pack.
Record:
step,command_or_action,expected_result,observed,status
1,zet init,project created,<fill>,NOT_YET_RUN
2,zet run,local server starts,<fill>,NOT_YET_RUN
3,CRM external hosting,Widget loads,<fill>,NOT_YET_RUN
4,PageLoad,context callback runs,<fill>,NOT_YET_RUN
5,zet validate,package passes validation,<fill>,NOT_YET_RUN
6,zet pack,ZIP created,<fill>,NOT_YET_RUN
Practice B — Test missing context
Open the Widget in a dashboard or other context that may not have an Account record.
Expected behavior:
Module: Unknown or dashboard context
Record: Unknown
Status: No Account record context was supplied
The Widget must not query an Account with a null ID.
Practice C — Configure the CRM Query
Create the Module Query from the worked case.
Test:
1. Valid Account ID.
2. Null Account ID.
3. Account ID from another module.
4. Account that does not exist.
5. Account with a null Owner.
6. Account with an empty Description.
Record:
case,variable_value,expected_query_result,expected_rendering,observed
valid,<CH18 Account ID>,one record,marker displayed,NOT_YET_RUN
missing,null,no query or blocked query,no record claim,NOT_YET_RUN
wrong module,<Contact ID>,blocked or no Account match,no Account claim,NOT_YET_RUN
unknown,<unknown ID>,empty or not found,no record claim,NOT_YET_RUN
null owner,<valid ID>,one record,Owner unavailable,NOT_YET_RUN
empty description,<valid ID>,one record,No description,NOT_YET_RUN
Practice D — Test the serializer
Use synthetic response fixtures:
[
  {
    "Account_Name": "NOVCH18LAB901A",
    "Description": "CH18 widget fixture",
    "Owner": {
      "name": "Training User",
      "id": "5725767000001190199"
    },
    "id": "5725767000001000001"
  }
]
[
  {
    "Account_Name": "NOVCH18LAB902A",
    "Description": null,
    "Owner": null,
    "id": "5725767000001000002"
  }
]
[]
Expected serializer behavior:
- Preserve IDs as strings.
- Render null Description as No description.
- Render null Owner as Unavailable.
- Return an empty array for an empty result.
- Never throw because Owner is null.
Practice E — Test a server-side boundary
Add a Widget button or action that invokes a server-side Function only after the current context is valid.
The Function must:
1. Receive the record ID.
2. Re-read the CRM Account.
3. Check Account_Name == "NOVCH18LAB901A".
4. Return a safe result.
5. Perform no write in the first exercise.
Expected result:
{
  "code": "READY",
  "marker_match": true,
  "write_performed": false
}
This is an expected contract, not a live tenant result.
## Independent challenge

Design a Nova contextual Widget and Query package that displays safe CRM context for a customer Account.
Complete this design sheet:
Design item	Your answer
Widget placement
Hosting mode
Current module
Context key for record ID
Query type
Query source
Query variable
Selected fields
Maximum result size
Serializer output
Schema paths
Null behavior
Permission failure behavior
Server-side operation
Trusted domains
Static resources
Package validation command
Cleanup plan
Create these failure fixtures.
Failure fixture 1 — Widget opened without record context
Expected analysis:
- Render a no-context state.
- Do not issue a Query with an empty record ID.
- Do not display a previous record’s data.
- Do not assume the dashboard user is viewing a specific Account.
Failure fixture 2 — Query variable maps to the wrong module
Expected analysis:
- Validate the expected module before using the record ID.
- Query the correct module only.
- Return an empty or blocked state.
- Record the configuration error safely.
Failure fixture 3 — Serializer receives null Owner
Expected analysis:
- Use a null-safe fallback.
- Preserve the Account ID as a string.
- Render Owner unavailable.
- Do not throw an exception or expose the raw response.
Failure fixture 4 — External database source uses an elevated credential
Expected analysis:
- Replace it with a least-privilege credential.
- Enable read-only mode when the Widget only displays data.
- Enable SSL.
- Review Developer user access to the source.
- Remove the source if it is not needed.
Failure fixture 5 — Widget package exceeds 25 MB
Expected analysis:
- Remove unused assets.
- Compress images.
- Avoid bundling unnecessary libraries.
- Validate the reduced package.
- Do not claim that a package was deployed until CRM accepts it.
Failure fixture 6 — Context ID is converted to a number
Expected analysis:
- Keep the context ID as a string.
- Do not pass it through JavaScript numeric conversion.
- Compare exact strings.
- Verify the Query variable receives the same exact identifier.
## Common problems and recovery

Symptom	Likely cause	Recovery
Widget page is blank	Broken HTML, missing SDK, or JavaScript exception	Open browser tools and inspect the first error
PageLoad never runs	Listener registered after init() or wrong SDK package	Register before initialization and verify the generated SDK
Widget works locally but not in CRM	Incorrect Base URL, hosting type, or package path	Verify hosting configuration and index URL
Context is empty	Placement does not provide record context	Render no-context state or choose a record-aware placement
Widget displays a previous record	State was not cleared on new context	Reset state on every PageLoad
Query returns all Accounts	Missing or unmapped {{ACCOUNT_ID}} variable	Require a mapped record ID and bounded criteria
Query variable is not replaced	Incorrect curly-brace name or association mapping	Use the exact declared variable and inspect the association
Query response fields are missing	Field not selected or schema path changed	Re-run the Query and update the schema contract
Serializer fails on null data	No null handling	Use defaults and validate arrays before mapping
Schema type is wrong	Generated schema or manual type does not match response	Correct the schema and retest null and normal values
Serializer exposes raw fields	Output shape was not allowlisted	Return only fields required by the Widget
External REST source fails	Connection, endpoint, or trusted domain problem	Test source validation and inspect safe status codes
Database source cannot connect	Host, port, SSL, credential, or relay configuration error	Validate source and check database-side allowlisting
Database source exposes too much data	Broad user or writable source	Use least-privilege credentials and read-only configuration
Widget ZIP rejected	Package too large or invalid	Run zet validate, reduce package, and run zet pack again
Widget deletion is blocked	Widget still associated with a component	Remove related list, button, web tab, wizard, or Blueprint associations
CRM API key appears in Widget source	Secret was placed in browser code	Rotate the key and move the operation to a server-side Function
User can see records they should not	Widget or Query exposes fields without server-side filtering	Restrict Query fields and enforce CRM permissions/server rules
Link opens the wrong place	Tenant-specific CRM URL was guessed	Use a supported link pattern or render plain text
Widget uses stale data	Context changed but state was not refreshed	Re-run context handling and Query on each PageLoad
Query exceeds limits	Too many fields, joins, or rows	Narrow the Query and use a bounded result limit
Widget uses unsupported browser APIs	Library depends on window, document, timers, or WebSockets	Replace the library with a supported implementation
Query result is not ordered	No explicit sort configured	Configure Query ordering or sort in a controlled serializer
Context record ID loses digits	JavaScript numeric conversion	Preserve the ID as a string
## Check your understanding

 1. What is the purpose of a CRM Widget?
 2. Which command starts the local Widget server?
 3. What event should a Widget listen to for initial CRM context?
 4. Does a dashboard Widget necessarily receive a record ID?
 5. What is the purpose of a Query variable?
 6. Which Query sources are built into CRM?
 7. What does a Query schema describe?
 8. What does a serializer do?
 9. Why should a serializer allow for null values?
10. What is the maximum documented number of Module Query fields?
11. What is the maximum documented Query SELECT limit for SQL sources?
12. Why should a database source use least-privilege credentials?
13. What does zet validate prove?
14. Why must a Widget not perform sensitive business writes directly from browser code?
15. What is the difference between expected Query output and actual tenant evidence?
## Solutions and explanations

 1. A Widget is an embeddable HTML, CSS, and JavaScript interface that runs inside CRM and can work with CRM or external data.
 2. zet run.
 3. Register a PageLoad listener before calling ZOHO.embeddedApp.init().
 4. No. Dashboard and other placements may not have a current record.
 5. It allows dynamic values such as a current Account ID to be mapped when a Query executes.
 6. Module, COQL, Zoho CRM REST API, external REST API, database, and cloud database sources are documented Query options.
 7. It describes response paths, field types, and labels.
 8. It transforms the Query response with JavaScript into a shape suitable for a UI or related list.
 9. Real records can have empty Description, null Owner, missing lookup values, or no result rows.
10. Up to 50 fields in a Module Query.
11. The current SQL Query Limits documentation lists a maximum SELECT limit of 100.
12. Developer users may be able to access configured sources, so elevated credentials can expose restricted data through Query features.
13. It checks the local Widget package against CLI validation rules. It does not prove CRM context, permissions, Query behavior, or production availability.
14. Browser code and network calls can be inspected. Sensitive writes need server-side validation, authorization, audit, and protected credentials.
15. Expected output is a designed response shape or local fixture. Actual tenant evidence includes the organization, environment, placement, captured context, Query execution, response code, read-back, and safe exported results.
## Chapter recap and next step

Widgets provide a richer interface than Client Scripts:
- HTML structures the interface.
- CSS controls presentation.
- JavaScript manages interaction.
- The Widget SDK connects the component to CRM context.
- CRM Queries provide reusable contextual data.
- Variables pass record-specific values.
- Schemas describe response paths and types.
- Serializers shape output for UI components.
- Trusted domains and Connections control external access.
- Server-side Functions handle sensitive or authoritative operations.
A reliable contextual Widget follows this sequence:
receive context
  -> validate module and record ID
  -> run bounded Query
  -> validate response
  -> serialize approved fields
  -> render null-safe UI
  -> delegate sensitive actions to the server
Do not treat:
- A Widget context as authorization.
- A Query response as a complete business record.
- A serializer as a security boundary.
- A valid package as proof of production behavior.
- A browser-side write as proof of server-side authorization.
The next chapter is:
C02-CH19 — SDKs and Serverless Components
## Glossary and further reading

Glossary
Context
Information supplied to a Widget about the CRM placement, page, module, or current record.
CRM Query
A configurable CRM data retrieval feature that can use modules, COQL, REST APIs, databases, or cloud databases.
Internal hosting
Hosting a Widget package through CRM or Zoho’s Widget infrastructure.
External hosting
Hosting a Widget at an external URL and embedding it into CRM.
PageLoad
A Widget lifecycle event raised when the CRM entity page loads.
Query variable
A dynamic placeholder such as {{ACCOUNT_ID}} mapped to a value at runtime.
Schema
The Query response contract containing result paths, types, and labels.
Serializer
JavaScript that transforms Query output.
Static resource
A reusable file or package used by a Widget or related CRM customization.
Widget SDK
The JavaScript library used to initialize Widgets, register events, and interact with CRM context.
ZET
The Zoho CLI toolkit used to initialize, run, validate, and package Widgets.
Further reading
- Widgets overview (https://www.zoho.com/crm/developer/docs/widgets/)
- Create a Widget (https://www.zoho.com/crm/developer/docs/widgets/create-widget.html)
- Work with Widgets (https://www.zoho.com/crm/developer/docs/widgets/usage.html)
- Install the Widget CLI (https://www.zoho.com/crm/developer/docs/widgets/install-cli.html)
- CRM Queries overview (https://www.zoho.com/crm/developer/docs/queries/)
- CRM Query types (https://www.zoho.com/crm/developer/docs/queries/query-types.html)
- CRM Query SQL limits (https://www.zoho.com/crm/developer/docs/queries/sql-limits.html)
- Client Script Trusted Domains (https://www.zoho.com/crm/developer/docs/client-script/trusted-domains.html)
- CRM v8 COQL (https://www.zoho.com/crm/developer/docs/api/v8/Get-Records-through-COQL-Query.html)
- CRM v8 Field Metadata (https://www.zoho.com/crm/developer/docs/api/v8/field-meta.html)
