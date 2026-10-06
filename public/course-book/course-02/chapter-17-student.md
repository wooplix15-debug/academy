# CRM Client Script

## What you will learn

By the end of this chapter, you will be able to:
- Explain what CRM Client Script can and cannot protect.
- Choose a supported CRM page and event for a user-interface requirement.
- Use JavaScript and ZDK Client APIs to read and update fields.
- Use onChange, onType, onSave, onLoad, subform, detail-page, Canvas, wizard, and command contexts appropriately.
- Prevent a form save or Blueprint transition from the browser when a local validation fails.
- Use server-side validation for rules that must also apply to API, import, automation, and other non-browser paths.
- Use ZDK Web APIs carefully because they consume CRM API capacity.
- Configure trusted domains for browser calls.
- Use static resources without relying on unsupported browser globals.
- Control script order and avoid conflicting scripts on the same page.
- Debug Client Script using the IDE Run panel, log, console.log, the Terminal, and browser developer tools.
- Design a safe Nova training UI that improves data entry without changing CRM ownership or Creator workflow authority.
Client Script runs in the user’s browser. It is a user-interface layer, not a security boundary.
## Lessons

### Lesson 1 — Understand the Client Script boundary

A CRM Client Script is JavaScript that runs in the browser while a user interacts with CRM.
It can:
- Show messages.
- Set or clear field values.
- Make fields read-only or mandatory in supported contexts.
- Validate values before a save.
- Filter or populate lookup values.
- React to field, page, subform, Blueprint, button, or command events.
- Call supported ZDK Client and Web APIs.
- Invoke server-side CRM Functions through supported ZDK APIs.
It cannot be treated as the sole authority for:
- Record permissions.
- Ownership.
- Business authorization.
- API access.
- Import rules.
- Server-side lifecycle enforcement.
- Confidential secret storage.
A user can bypass browser logic by using:
- CRM APIs.
- Imports.
- Server-side Functions.
- Workflows.
- Other applications.
- Another browser or page that does not load the script.
Therefore:
Client Script = user experience and early feedback
Server-side rule = authoritative enforcement
For Nova, a Client Script can tell a dispatcher that a field is missing. The Creator validation, CRM server-side rule, or integration function must still enforce the rule when the operation comes through another path.
Supported pages
The current Client Script overview lists these pages:
- Create Page.
- Edit Page.
- Clone Page.
- Standard List Page.
- Standard Detail Page.
- Canvas Detail Page.
- Create Page in a Wizard.
- Edit Page in a Wizard.
The event documentation also contains sections for Canvas record pages, Canvas list pages, and Quick Create popups. Another official FAQ states that Client Script cannot run in Quick Create. Because these official pages are inconsistent, do not make Quick Create part of a production contract without testing the tenant’s current behavior.
This chapter uses the standard Accounts Create and Edit pages, which are the safest bounded lab context.
A separate Client Script is required for each CRM layout where the script must run. A script configured for one layout does not automatically cover every layout in the module.
Client Script timeout
The documented Client Script execution timeout is 10 seconds.
A script that performs several Web API calls, waits on a slow third-party service, or executes a large loop can exceed this limit.
Client-side visibility
Users can inspect browser code and browser requests. Do not place these in Client Script:
- Client secrets.
- Refresh tokens.
- API keys.
- Passwords.
- Long-lived bearer tokens.
- Confidential business rules that must not be exposed.
If a browser needs a sensitive operation, call a server-side Function or another controlled backend.
Lesson check
1. Is Client Script a security boundary?
2. Which system must enforce a rule that also applies to imports and APIs?
3. What is the documented Client Script timeout?
4. Does a script on one CRM layout automatically run on every layout?
5. Why should a client-side script not contain a client secret?
### Lesson 2 — Choose the right page event

Client Script events describe actions in the CRM browser.
Create, Clone, and Edit pages
The main page events are:
Event	When it runs	Typical use
onLoad	Page opens	Set initial UI state
onChange	A page field changes	Coordinate several fields
onSave	Save is clicked before the record is saved	Final browser-side validation
Field events include:
Event	When it runs
Field onChange	User leaves or commits the field value
Field onType	User types into the field
Use Field onChange when one field has a local rule. Use Page onChange when several fields interact.
Use onType carefully. It can execute many times while the user types and can produce unnecessary work or API calls.
Preventing a save
An onSave script can display an error and return false:
const accountNameField = ZDK.Page.getField("Account_Name");
const descriptionField = ZDK.Page.getField("Description");

const accountName = accountNameField.getValue();
const description = descriptionField.getValue();

if (accountName === "NOVCH17LAB901A" &&
    (!description || description.trim() === "")) {
    descriptionField.showError(
        "The CH17 scratch Account requires a Description."
    );
    return false;
}
This prevents the browser save for that Client Script execution.
It does not prove that:
- An API call cannot save the record.
- An import cannot save the record.
- A server-side Function cannot save the record.
- Another layout has the same rule.
- A user cannot disable or bypass the script.
The corresponding server-side rule must exist if the requirement is authoritative.
Detail pages
Standard and Canvas detail pages support different events from Create and Edit pages.
Examples include:
- Detail page onLoad.
- Field onBeforeUpdate.
- Blueprint beforeTransition.
- Tag changes.
- Subform row actions.
- Canvas button, text, and icon clicks.
- Mandatory-fields form events.
Some detail-page field operations have different support from form-page operations. Do not copy a Create Page script into a Detail Page and assume that setValue() has the same effect.
Subforms
The event documentation includes:
- onRowAdd.
- onCellChange.
- onRowDelete.
- BeforeRowDelete.
- BeforeRowUpdate in supported contexts.
For example, a Client Script can stop a subform row deletion:
if (value && value.Result === "Rework_Required") {
    ZDK.Client.showMessage(
        "Review the rework item before deleting this row.",
        { type: "warning" }
    );
    return false;
}
The exact event arguments depend on the configured page and event. Use the IDE event dictionary rather than assuming that value always contains the complete subform row.
Wizards
Wizard pages support events such as:
- onLoad.
- onChange.
- onTransition.
- onBeforeTransition.
- onBeforeSave.
A wizard transition can be stopped with return false in a supported before-transition event.
Commands
Client Script Commands run outside a single module page through:
- The CRM command palette.
- A user-configured keyboard shortcut.
Use a Command for a reusable user action that does not belong to one form event. The current documentation states that up to 30 Client Script Commands can be created.
Do not use a Command to bypass server-side authorization.
Lesson check
1. Which event is appropriate for final browser-side validation before a form save?
2. What is the difference between Page onChange and Field onChange?
3. Which event can stop a supported Blueprint transition?
4. Why should onType avoid expensive API calls?
5. Does return false create a server-side guarantee?
### Lesson 3 — Use JavaScript and ZDK safely

Client Script supports JavaScript. The current FAQ documents core JavaScript support through ES7 and permits var, let, and const.
Read and set a field
A common pattern is:
const summaryField = ZDK.Page.getField("Description");
const summary = summaryField.getValue();

if (!summary || summary.trim() === "") {
    summaryField.setValue("CH17 scratch Account");
}
For a lookup field, set the record ID and name together:
ZDK.Page.getField("Parent_Account").setValue({
    id: "5725767000001000001",
    name: "NOVCH11LAB901A"
});
The ID above is a synthetic example. Do not send it to a live organization unless the tenant captured the same ID.
CRM IDs must remain strings in JavaScript. Do not use:
Number(crmId)
or:
parseInt(crmId, 10)
Large CRM IDs can lose precision when converted to JavaScript numbers.
Display messages
Use supported ZDK Client APIs:
ZDK.Client.showMessage(
    "CH17 client-side check completed.",
    { type: "info" }
);
ZDK.Client.showAlert(
    "Review the required fields before continuing."
);
Use field-level errors when the problem belongs to one field:
ZDK.Page.getField("Description").showError(
    "Description is required for the CH17 scratch Account."
);
Read the current form
The current form can be inspected through the Page API:
const form = ZDK.Page.getForm();
const values = form.getValues();

log(JSON.stringify(values));
Use getValues() for diagnostics and cross-field checks. Avoid logging the entire form in a production environment if it contains personal or confidential data.
ZDK Web APIs
Client Script provides Web APIs that invoke CRM APIs internally. Every ZDK Web API call consumes CRM API capacity.
Use a Web API only when the browser genuinely needs server data that is not already present in the page.
Examples of appropriate uses:
- Read a small, safe lookup result.
- Fetch the current user profile.
- Check a non-sensitive status for user guidance.
- Populate a field from a verified CRM record.
Examples of inappropriate uses:
- Fetching thousands of records on page load.
- Replacing a server-side authorization check.
- Returning confidential fields to the browser.
- Repeatedly calling the API on every keystroke.
- Calling the API when a local field comparison is sufficient.
The current FAQ shows a pattern similar to:
const user = ZDK.Apps.CRM.Users.fetchById($Crm.user.id);
log(JSON.stringify(user));
Use the Client Script IDE Library documentation to confirm the exact method signature for the current tenant and page context.
Invoke a server-side Function
Client Script can invoke supported CRM Functions through ZDK. A documented example uses:
ZDK.Apps.CRM.Functions.execute("Send_Quote");
Use a server-side Function when the operation requires:
- CRM-side authorization.
- Sensitive credentials.
- A connection.
- Cross-module business logic.
- An audit-controlled write.
- A rule that must not be visible in browser source.
A client call to a server-side Function is still subject to:
- Function permissions.
- Function category.
- Function execution limits.
- Server-side validation.
- Connection scopes.
- CRM record permissions and business rules.
Show a loader for a call that may take time:
ZDK.Client.showLoader({
    type: "page",
    template: "spinner",
    message: "Checking the training Account..."
});

ZDK.Apps.CRM.Functions.execute("nova_ch17_server_preview")
    .then(function(response) {
        ZDK.Client.hideLoader();
        ZDK.Client.showMessage(
            "Server check completed.",
            { type: "success" }
        );
    })
    .catch(function(error) {
        ZDK.Client.hideLoader();
        log("server_preview_failed");
        ZDK.Client.showMessage(
            "The server check could not be completed.",
            { type: "error" }
        );
    });
Confirm the Promise and response shape in the IDE Library before using it in a tenant. Do not claim success based only on the browser Promise resolving; read back the target state when a write occurred.
Unsupported browser globals
The current Client Script documentation and FAQ state that browser globals and APIs such as these are not supported:
- window
- document
- WebSocket
- setTimeout
- setInterval
- Worker
- MessageChannel
- postMessage
- importScripts
- localStorage
Do not import a library that depends on these objects unless the tenant documentation explicitly confirms compatibility.
Lesson check
1. Why must CRM IDs remain strings in Client Script?
2. When should a ZDK Web API call be avoided?
3. Why should sensitive operations use a server-side Function?
4. What should happen if a server-side Function call times out?
5. Which browser globals are unavailable in the documented Client Script environment?
### Lesson 4 — Use static resources, trusted domains, and script order

Static resources
Static Resources let you upload reusable JavaScript files and include them in Client Scripts.
Current documented limits include:
- JavaScript files only.
- Up to 5 MB per file.
- Up to 200 files.
- Up to 5 resources imported per page.
- Resources are available to scripts on the page where they are added.
- DOM- and window-dependent libraries are unsuitable.
Example static resource:
// nova_ch17_rules_v1.js
function nova_ch17_isScratchAccount(name) {
    return name === "NOVCH17LAB901A";
}

function nova_ch17_hasDescription(value) {
    return typeof value === "string" && value.trim().length > 0;
}
Client Script:
if (field_name === "Account_Name") {
    const name = ZDK.Page.getField("Account_Name").getValue();
    const description = ZDK.Page.getField("Description");

    if (nova_ch17_isScratchAccount(name) &&
        !nova_ch17_hasDescription(description.getValue())) {
        description.showError(
            "Enter a Description for the CH17 scratch Account."
        );
    }
}
Use a namespace prefix such as nova_ch17_ to reduce collisions between resources.
Do not assume that two resources with the same global function name will resolve in a safe order.
Trusted domains
A Client Script can call a third-party domain only when that domain is added under:
Setup
  -> Security Control
  -> Trusted Domain
A trusted-domain entry should contain:
- A clear name.
- A purpose.
- The exact approved domain.
- The business owner.
- The environment or use case.
Do not add a broad wildcard domain when one host is sufficient.
Example:
Name: CH17 training echo
Description: Disposable client-side validation lab
Domain: training-api.example.test
A browser call to an untrusted domain should fail. This is expected protection, not an application defect.
Never embed secrets in Client Script
Even a trusted domain does not make a browser-held API key secret.
Use this pattern:
Client Script
  -> server-side Function
  -> Connection
  -> external API
Do not use this pattern:
Client Script
  -> hardcoded API key
  -> external API
The Client Script source and browser network traffic can be inspected by users.
Script order
The current best-practice documentation provides a Reorder option for Client Scripts. The order applies within a particular page and event.
Use ordering only when the dependency is deliberate:
1. normalize input
2. apply local field rule
3. display summary
Avoid hidden ordering dependencies. Prefer one page-level script with a switch or clear functions when several fields share logic.
The documentation states that up to 30 Client Scripts can be created per page. Too many scripts increase:
- Execution-order ambiguity.
- Duplicate messages.
- Repeated API calls.
- Debugging cost.
- Risk of one script undoing another script’s field change.
Lesson check
1. What is the maximum documented static resource size?
2. How many static resources can be imported per page?
3. Why does a trusted domain not protect an API key embedded in JavaScript?
4. When does Reorder apply?
5. Why should reusable functions have a namespace prefix?
### Lesson 5 — Debug in the IDE and browser without claiming tenant outcomes

The Client Script IDE provides:
- Syntax highlighting.
- ZDK suggestions.
- Code review.
- Conflict management.
- Revision history.
- Run mode.
- Messages panel.
- Terminal.
- Static Resource management.
log() and console.log()
Use safe diagnostic messages:
log("code=CH17_STARTED");
log("field_name=" + field_name);
For a structured object:
log("form_keys=" + Object.keys(values).join(","));
console.log("safe_event", {
    event: "onChange",
    field: field_name
});
Use JSON.stringify() when the Messages panel does not render an object clearly:
log("response=" + JSON.stringify(response));
Do not log:
- Authorization headers.
- Access tokens.
- Refresh tokens.
- Client secrets.
- Full customer records.
- Full API responses containing confidential fields.
Run mode changes real CRM data
The Client Script IDE documentation warns that CRM operations executed in Run mode are reflected in the CRM organization.
Therefore:
- Use a training organization or Sandbox.
- Use NOVCH17LAB901A.
- Test reads before writes.
- Keep a cleanup plan.
- Do not use live customer records.
- Treat Run mode as execution, not a mock simulator.
Terminal
The Terminal can be used to try supported ZDK APIs:
ZDK.Client.showMessage(
    "Terminal test",
    { type: "info" }
);
A Terminal response proves that the local ZDK expression ran in that IDE context. It does not prove that a particular production layout, user profile, button, or browser receives the same result.
Browser console
The Client Script FAQ states that console.log() can be used with the browser console.
Use browser developer tools to inspect:
- JavaScript exceptions.
- Failed network requests.
- Trusted-domain failures.
- Response status.
- Timing.
- Promise rejection.
- Which script ran before another script.
Redact request and response values before exporting browser evidence.
Revision history
Client Script IDE revisions provide a recovery point. Use a commit message such as:
CH17 add scratch Account onSave guard
Before changing a script that is already active:
1. Read the current script.
2. Record the current revision.
3. Make one bounded change.
4. Test the target layout and event.
5. Verify the negative path.
6. Confirm no other script was reordered unintentionally.
7. Keep the prior revision available.
Lesson check
1. Where do log() results appear in the IDE?
2. Does Run mode guarantee that CRM operations are simulated?
3. What should browser network evidence exclude?
4. What does the Client Script revision history provide?
5. Why must the target layout be included in test evidence?
## Visual explanation

flowchart TD
    A[User opens CRM page] --> B[Client Script event]
    B --> C[JavaScript and ZDK Client API]
    C --> D{Local UI rule?}
    D -->|Yes| E[Show error, set field, or return false]
    D -->|No| F{Needs CRM or external data?}
    F -->|CRM data| G[ZDK Web API]
    F -->|Sensitive operation| H[Server-side Function]
    F -->|Third-party browser call| I[Trusted Domain check]
    H --> J[Connection and server-side rule]
    G --> K[API credit and timeout]
    E --> L[Server-side rule still validates]
    J --> L
Plain-text explanation:
- The browser is the first feedback layer.
- ZDK Client APIs change the user interface.
- ZDK Web APIs consume CRM API capacity.
- Sensitive work belongs on the server.
- Trusted Domains restrict browser destinations, but they do not make browser code confidential.
- Server-side enforcement remains necessary.
## Worked case

CH17 scratch Account UI
Create a disposable CRM Account:
Account_Name: NOVCH17LAB901A
Description: CH17 scratch Account
The CRM record ID is generated by the tenant.
Record it as:
artifact,module,marker,record_id,layout,event,observed
CH17 scratch Account,Accounts,NOVCH17LAB901A,<captured ID>,Standard Create,Page onChange,NOT_YET_RUN
CH17 scratch Account,Accounts,NOVCH17LAB901A,<captured ID>,Standard Create,Page onSave,NOT_YET_RUN
This Account is a UI fixture. It is not a Nova production customer.
Client Script A — Page onChange
Host: Accounts Create Page, Standard layout
Event: Page onChange
Argument: field_name
Dependencies: ZDK Client API
Connection: none
Supported task: Display a training marker and populate a safe Description default
Return contract: No return required
if (field_name === "Account_Name") {
    const accountNameField = ZDK.Page.getField("Account_Name");
    const descriptionField = ZDK.Page.getField("Description");
    const accountName = accountNameField.getValue();

    if (accountName === "NOVCH17LAB901A") {
        if (!descriptionField.getValue()) {
            descriptionField.setValue("CH17 scratch Account");
        }

        ZDK.Client.showMessage(
            "CH17 training marker detected.",
            { type: "info" }
        );

        log("code=SCRATCH_MARKER_DETECTED");
    }
}
This is a convenience behavior. It does not authorize a CRM Account and does not prove that the name is unique in every path.
Client Script B — Page onSave
Host: Accounts Create Page, Standard layout
Event: Page onSave
Dependencies: ZDK Client API
Connection: none
Supported task: Prevent an incomplete scratch record from being saved through this browser page
Return contract: false when the browser save must be stopped
const accountNameField = ZDK.Page.getField("Account_Name");
const descriptionField = ZDK.Page.getField("Description");

const accountName = accountNameField.getValue();
const description = descriptionField.getValue();

if (accountName === "NOVCH17LAB901A" &&
    (!description || description.trim() === "")) {
    descriptionField.showError(
        "Description is required for the CH17 scratch Account."
    );

    log("code=CLIENT_SAVE_BLOCKED");
    return false;
}

log("code=CLIENT_SAVE_ALLOWED");
This prevents a browser save only for the configured page and event. The equivalent server-side validation is still required if this rule is important.
Client Script C — Detail-page information
Host: Accounts Standard Detail Page
Event: Page onLoad
Dependencies: ZDK Client API
Connection: none
Supported task: Display safe training context
Return contract: none
const nameField = ZDK.Page.getField("Account_Name");
const name = nameField.getValue();

if (name === "NOVCH17LAB901A") {
    ZDK.Client.showMessage(
        "This is an isolated CH17 training Account.",
        { type: "warning" }
    );
    log("code=TRAINING_CONTEXT_SHOWN");
}
The exact field behavior on Detail Page can differ by page type. Verify this script in the current tenant before using it.
Server-side boundary
If the Account Description rule is authoritative, use the CH16 server-side Function or another CRM validation mechanism.
The client script should not be considered proof that:
Account_Name is unique
Description is valid
Caller is authorized
Record was saved
The server must re-read the record and enforce those conditions.
## Try it yourself — guided practice

Practice A — Create and configure the scripts
 1. Create the scratch Account.
 2. Navigate to Client Script setup.
 3. Create a Module Client Script for Accounts.
 4. Select the Standard layout.
 5. Configure Page onChange.
 6. Add Script A.
 7. Configure Page onSave.
 8. Add Script B.
 9. Save with a descriptive revision message.
10. Enable the scripts.
11. Open the Create Page and test the marker.
Expected test matrix:
case,event,input,expected_ui_result,expected_server_claim,observed
1,onChange,NOVCH17LAB901A,info message and default description,none,NOT_YET_RUN
2,onSave,scratch name with blank description,error and save blocked,none,NOT_YET_RUN
3,onSave,scratch name with description,save allowed by client,server still validates,NOT_YET_RUN
4,onChange,other Account name,no training message,none,NOT_YET_RUN
5,onSave,blank Account name,client rule does not claim authority,server handles rule,NOT_YET_RUN
Practice B — Test a missing value
Test:
- Account_Name empty.
- Description empty.
- Account_Name = NOVCH17LAB901A.
- Description containing spaces only.
Expected local result for the marker and blank description:
Client error shown.
Save prevented in the configured browser event.
No claim made about API or import behavior.
Practice C — Test a ZDK Web API read
Use the IDE Library to select a supported current-user or record-read API. Confirm the generated method for the current tenant before saving.
Record:
operation,api_version,record_or_user_scope,api_calls_expected,response_redacted,observed
ZDK read,<v2 or v8>,one record or current user,1,<safe code only>,NOT_YET_RUN
The Web API call must be limited to one small read. Record that it consumes CRM API capacity.
Practice D — Test a trusted domain
Use a controlled test endpoint only if the exercise has one.
1. Add the exact host under Trusted Domains.
2. Make one browser request.
3. Remove or disable the trusted domain.
4. Repeat the request.
5. Record the difference.
Expected result:
domain_status,request_result,expected_reason,observed
trusted,request may proceed,domain approved,NOT_YET_RUN
not trusted,request blocked,domain not allowlisted,NOT_YET_RUN
Do not use an API key in the browser request.
Practice E — Test script order
Create two tiny scripts on the same page and event:
// Script A
log("CH17_ORDER_A");
// Script B
log("CH17_ORDER_B");
Use the Reorder control to reverse their order.
Record:
page,event,first_log_before,first_log_after,reorder_scope,observed
Accounts Create,Page onLoad,CH17_ORDER_A,CH17_ORDER_B,same page and event only,NOT_YET_RUN
Do not create production logic that depends on an undocumented order between unrelated scripts.
## Independent challenge

Design a Client Script package for the following requirement:
On the Nova CRM training Account Create Page, guide the user when the scratch marker is entered, require a Description before browser save, and provide a read-only detail-page indicator.
Complete this design sheet:
Design item	Your answer
Module
Layout
Page
Page event
Field event
Server-side equivalent
Client-only behavior
ZDK Client APIs
ZDK Web APIs
Trusted domains
Static resources
Script order
Timeout risk
Browser evidence
Cleanup
Create these failure fixtures.
Failure fixture 1 — Client-only validation bypass
A user creates a valid-looking record through the CRM API without running the browser.
Expected analysis:
- Client Script does not execute.
- The server-side rule must validate the record.
- The Client Script is useful for user feedback but not sufficient enforcement.
- Evidence must distinguish browser behavior from API behavior.
Failure fixture 2 — Third-party API key in JavaScript
A developer places a map-service API key in Client Script.
Expected analysis:
- Remove the key from the browser.
- Move the call to a server-side Function and Connection.
- Add only the server endpoint or required browser domain to Trusted Domains.
- Rotate the exposed key if it was real.
- Do not include the key in evidence.
Failure fixture 3 — Untrusted domain
The Client Script calls a domain that is not configured under Trusted Domains.
Expected analysis:
- The browser call should be blocked.
- Add the exact approved domain only after security review.
- Do not broaden the domain unnecessarily.
- Test both allowed and blocked cases.
Failure fixture 4 — API call on every keystroke
An onType field event calls a CRM Web API for every character typed.
Expected analysis:
- Remove the Web API call from onType.
- Use local validation while typing.
- Use Field onChange or an explicit Button for one bounded lookup.
- Keep the server-side Function available for sensitive work.
- Measure API calls before and after the change.
Failure fixture 5 — Conflicting scripts
One script sets Description to a default while another clears it.
Expected analysis:
- Consolidate related logic into one script or define an explicit order.
- Use Reorder only within the same page and event.
- Test all layouts where the scripts are enabled.
- Record the final behavior rather than assuming source-file order.
## Common problems and recovery

Symptom	Likely cause	Recovery
Script does not run	Wrong module, layout, page, or event	Compare configuration with the actual page and layout
Script runs on one layout only	Client Scripts are layout-specific	Create and test a separate script for each required layout
onSave validation does not stop save	Missing return false or wrong event	Use Page onSave and return false after displaying the reason
Field rule runs too often	onType selected instead of onChange	Use Field onChange for committed values
Field value is null	Field not available on that page or value absent	Check field API name and null handling
Lookup value is rejected	Lookup requires ID and name structure	Set {id, name} using exact CRM values
Web API call consumes too much quota	Call runs on page load or every keystroke	Reduce calls, cache only within supported context, or move to server
External call is blocked	Domain is not Trusted	Add the exact approved domain or use a server-side Function
External call exposes a secret	API key embedded in browser code	Rotate the key and move authentication server-side
Static resource does not load	Resource not added to the page or file is invalid	Add it through the IDE and check the resource limit
Static library throws window error	Library depends on unsupported browser globals	Remove it or use a Client Script-compatible library
Two scripts conflict	Duplicate event logic or order dependency	Consolidate, namespace, or reorder within the same event
Browser behavior differs from IDE Run	Different layout, user, event, or page state	Reproduce in the actual page and record the context
Run mode changed CRM data	ZDK write or Web API operation was executed	Use training data and read back the target
Messages panel hides object details	Object serialization is unclear	Use JSON.stringify() with redacted fields
Browser console shows a Promise rejection	Async ZDK or fetch failure	Add explicit success and failure handlers
Detail page field does not change	Detail-page field editing has different support	Use a supported event or server-side update
Client Script appears secure because button is hidden	UI visibility mistaken for authorization	Add server-side authorization and target guards
Quick Create behavior is inconsistent	Official documentation differs by page/version	Exclude Quick Create from the contract until tenant-tested
Script exceeds 10 seconds	Long loop or slow API call	Reduce work, show a loader, or move work server-side
Client Script cannot access stored browser state	localStorage unsupported	Use CRM fields, server-side state, or a supported Function
## Check your understanding

 1. Where does CRM Client Script execute?
 2. What is the difference between Page onSave and server-side validation?
 3. Which event runs when a user types into a field?
 4. What happens when return false is used in a supported onSave event?
 5. Do ZDK Web API calls consume CRM API capacity?
 6. Why should a browser not hold an API key?
 7. What is the purpose of Trusted Domains?
 8. How many static resources can be imported per page?
 9. What is the maximum documented Client Script timeout?
10. Does script order change globally across all pages?
11. What does the IDE Run mode warning mean?
12. Which data structure is required to set a lookup field?
13. What should happen when a user bypasses Client Script through an API?
14. Why should a Client Script use a server-side Function for sensitive work?
15. What evidence is needed before claiming that the script works in a tenant?
## Solutions and explanations

 1. It executes in the user’s browser.
 2. onSave improves browser feedback and can stop the configured browser save. Server-side validation is required for APIs, imports, automation, and other non-browser paths.
 3. Field onType.
 4. It prevents the browser action when the event supports cancellation, such as a supported Page onSave or beforeTransition.
 5. Yes. The current documentation states that ZDK Web API calls consume CRM API capacity.
 6. Browser source and network requests can be inspected by users. A key in JavaScript is not secret.
 7. Trusted Domains allow Client Script browser calls only to approved third-party domains.
 8. Up to five resources per page.
 9. Ten seconds.
10. No. Reorder applies within a particular page and event.
11. CRM operations executed in Run mode can affect the actual CRM organization.
12. An object containing the lookup record’s ID and name.
13. The server-side rule must validate it because the Client Script did not run.
14. Server-side Functions can use controlled permissions, Connections, audit logs, and protected implementation details.
15. Evidence should include module, layout, page, event, user context, script revision, safe input, observed UI result, server-side result where applicable, and confirmation that no secrets were exported.
## Chapter recap and next step

CRM Client Script is a powerful browser-side customization layer.
Use it to:
- Give immediate feedback.
- Reduce data-entry mistakes.
- Populate fields.
- Guide users through forms.
- Display contextual messages.
- Control supported UI transitions.
- Trigger bounded server-side operations.
Do not use it as the only protection for:
- Permissions.
- Confidential data.
- Business authorization.
- API enforcement.
- Imports.
- Server-side workflows.
- External credentials.
The most reliable pattern is:
Client Script:
  guide and validate early

Server-side Function or rule:
  authorize and enforce

CRM record:
  store the final state

Read-back:
  verify important writes
The Nova CRM training example uses the NOVCH17LAB901A marker and standard Accounts pages. It does not alter the Creator-owned field-service lifecycle or introduce production CRM schema.
The next chapter is:
C02-CH18 — Widgets and Contextual Data
## Glossary and further reading

Glossary
Client Script
JavaScript executed in the CRM browser in response to configured pages and events.
Event
A user or page action that triggers Client Script, such as onLoad, onChange, onSave, or beforeTransition.
Layout
A CRM module layout to which a Client Script is attached. Scripts are layout-specific.
Page API
ZDK Client API used to access fields and forms in the current CRM page.
Trusted Domain
An explicitly approved third-party domain that Client Script may call from the browser.
Static Resource
An uploaded JavaScript file reused by one or more Client Scripts on a page.
ZDK Client API
Client-side APIs for user-interface operations such as field access and messages.
ZDK Web API
Client-side APIs that invoke CRM operations and consume CRM API capacity.
onSave
A form event that runs after the user clicks Save but before the record is saved.
onType
A field event that runs while a user types.
Server-side Function
CRM-hosted code executed outside the browser with server-side permissions and limits.
Further reading
- Client Script overview (https://www.zoho.com/crm/developer/docs/client-script/overview.html)
- Client Script events (https://www.zoho.com/crm/developer/docs/client-script/client-script-events.html)
- Creating a Client Script (https://www.zoho.com/crm/developer/docs/client-script/creation.html)
- Client Script IDE (https://www.zoho.com/crm/developer/docs/client-script/ide-components.html)
- Client Script best practices (https://www.zoho.com/crm/developer/docs/client-script/client-script-best-practices.html)
- Client Script static resources (https://www.zoho.com/crm/developer/docs/client-script/static-resources.html)
- Trusted Domains (https://www.zoho.com/crm/developer/docs/client-script/trusted-domains.html)
- Client Script Commands (https://www.zoho.com/crm/developer/docs/client-script/commands.html)
- Client Script FAQs (https://www.zoho.com/crm/developer/docs/client-script/FAQs.html)
- CRM Functions overview (https://www.zoho.com/crm/developer/docs/functions/)
- CRM Functions security (https://www.zoho.com/crm/developer/docs/functions/security.html)
- CRM Functions limits and quotas (https://www.zoho.com/crm/developer/docs/functions/limits-quotas.html)
- CRM Functions and Deluge guide (https://www.zoho.com/crm/developer/docs/functions/language-guide/deluge.html)
