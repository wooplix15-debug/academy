# Extensions, Testing and Release Readiness

## What you will learn

By the end of this chapter, you will be able to:
- Explain what a Zoho CRM extension is and how it differs from a one-off customization.
- Distinguish native extensions from third-party integration extensions.
- Select extension components for a reusable solution.
- Use namespaces to prevent collisions between extension components.
- Design tenant-specific configuration without embedding organization assumptions in code.
- Distinguish custom variables from OAuth connectors.
- Use metadata to discover installation-specific module and field API names.
- Design install, authorization, revocation, and upgrade actions deliberately.
- Package a reusable Nova extension boundary without making live tenant changes.
- Test field mappings, organization isolation, environment isolation, and safe projection locally.
- Plan private distribution, Marketplace submission, and version upgrades.
- Recognize which extension changes are additive, mutable, or difficult to remove.
This chapter builds on Chapter 19. The previous chapter produced a reusable serverless CRM context component. Here, that component becomes part of a broader extension design that can be installed, configured, tested, upgraded, and reused across multiple organizations.
## Lessons

### Lesson 1 — An extension is a product boundary

A custom Function solves a problem inside one organization. An extension packages a repeatable solution for other organizations.
The difference is not only packaging. A reusable extension must answer additional questions:
- Which components are installed?
- Which names are globally unique?
- Which values are tenant-specific?
- Which credentials require user authorization?
- Which organization owns the data?
- What happens during installation?
- What happens during authorization?
- What happens when a user uninstalls or upgrades?
- Which components can be edited later?
- Which components can be deleted?
- How is the extension tested without changing production data?
- How is the extension distributed?
A useful extension boundary has three layers:
Reusable product contract
    |
    +-- Extension components
    |      - fields
    |      - modules
    |      - functions
    |      - widgets
    |      - connectors
    |      - variables
    |
    +-- Installation contract
    |      - namespace
    |      - organization
    |      - environment
    |      - defaults
    |
    +-- Runtime contract
           - record context
           - API calls
           - authorization
           - output schema
The extension should not assume that every customer has:
- The same field labels.
- The same custom modules.
- The same CRM edition.
- The same user profiles.
- The same regional data center.
- The same third-party account.
- The same existing workflows.
- The same API permissions.
### Lesson 2 — Understand the extension categories

The current Zoho Developer documentation describes two broad extension types.
Native extensions
Native extensions add functionality inside a Zoho application.
Examples include:
- Custom modules.
- Custom fields.
- Custom related lists.
- Custom buttons.
- Web tabs.
- Workflow automations.
- Custom Functions.
- Email templates.
- Inventory templates.
A native Nova extension could add:
Accounts
    |
    +-- Nova Service Segment
    +-- Nova Context Status
    +-- Nova Last Context Refresh
It could also add a custom Function that uses the installed fields.
Third-party integration extensions
Third-party extensions connect Zoho CRM to an outside service.
Typical components include:
- A Connector.
- Connector APIs.
- Custom variables.
- Connected Apps.
- Custom Functions.
- Optional CRM fields or modules.
Use a Connector when the customer must authorize an external service through OAuth 2.0 or another supported connector flow.
Use a custom variable for tenant-specific, non-secret configuration such as:
External service region
External tenant label
Feature mode
Default synchronization window
Do not use a custom variable as a substitute for secure secret storage. Client secrets, access tokens, refresh tokens, and API keys must remain in the appropriate platform-managed authorization mechanism.
### Lesson 3 — Plan the extension before creating components

An extension starts with a component inventory.
For Nova’s reusable CRM context extension, the inventory is:
Component	Purpose	Ownership
Namespace	Avoid naming collisions	Extension developer
Custom field	Store optional CRM context	Installing organization
Custom Function	Read and normalize context	Extension
Custom variable	Enable or disable optional behavior	Installing organization
Connector	Optional external service authorization	Installing user or organization
Connected App or Widget	Optional user-facing presentation	Extension
Install action	Seed safe defaults	Extension
Sandbox test	Verify installation and behavior	Developer
Release notes	Explain version changes	Extension developer
Do not add every possible component. Every component increases:
- Installation complexity.
- Upgrade responsibility.
- Permission surface.
- Support burden.
- Testing requirements.
- Potential naming conflicts.
A minimal first release is easier to support than a feature bundle with undocumented dependencies.
### Lesson 4 — Namespaces are part of the data contract

When an extension is created, it receives a unique namespace. The current Developer Console documentation states that the namespace is used in the extension link and cannot be changed after creation.
A namespace should be:
- Globally unique within the Developer Console.
- Short enough to use in API names.
- Stable for the life of the extension.
- Independent of a customer name.
- Free from ambiguous environment labels.
- Documented before components are created.
For this chapter, use the synthetic namespace:
nova_field_service
This is a teaching value, not a claimed registered namespace.
Illustrative generated API names may look like:
nova_field_service__Service_Segment
nova_field_service__Context_Status
nova_field_service__Enable_Context_Read
The exact API name generated by the platform must be verified after creation. Do not assume that a display label maps directly to a field API name.
A label can change for user experience reasons. An API name is part of the integration contract.
### Lesson 5 — Use API names, not display labels

A CRM extension should store and use API names.
Display labels can change because of:
- Renaming.
- Translation.
- Customer terminology.
- Product changes.
- User interface preferences.
The CRM Fields Metadata API provides field information such as:
- API name.
- Display label.
- JSON type.
- Read-only status.
- Visibility.
- Custom-field status.
- Operation support.
- Picklist values.
- Field source.
The metadata endpoint is:
GET /settings/fields?module={module_api_name}
A record request should use field API names:
GET /crm/v8/Accounts/{record_id}?fields=Account_Name,nova_field_service__Service_Segment
Do not build an extension around a label such as:
"Service Segment"
Use the verified API name instead:
"nova_field_service__Service_Segment"
The API name may be generated or prefixed by the platform. Treat the actual installed metadata as authoritative.
### Lesson 6 — Configuration belongs to the installation

An extension is designed once but installed into multiple organizations.
Therefore, configuration must be resolved per installation.
A safe installation context contains at least:
org_id: "000900000000002001"
environment: "sandbox"
extension_namespace: "nova_field_service"
schema_version: "1"
enabled: true
The runtime should verify:
1. The configuration belongs to the current organization.
2. The configuration belongs to the current environment.
3. The configuration schema is supported.
4. The requested feature is enabled.
5. The configured API fields exist in the current organization.
6. The field types are compatible.
7. The record being read belongs to the expected module.
8. The response contains only approved fields.
The request body should not be allowed to override:
- Organization ID.
- Extension namespace.
- Environment.
- Connector name.
- Selected security policy.
- Allowed field list.
Those values belong to installed configuration or controlled server-side code.
### Lesson 7 — Custom variables are configuration, not secrets

Custom variables allow an extension to store values that can be reused across its components.
Suitable examples:
Enable context read: true
Default service segment: Training
Context contract version: 1
External region: eu
A custom variable can be:
- Read-write.
- Read-only.
- Hidden.
The exact behavior and visibility must be verified in the target Developer Console. A hidden variable should not be treated as a cryptographic secret. It is still part of the extension’s configuration surface.
Do not store these in custom variables:
client_secret
refresh_token
access_token
authorization_header
api_key
Use a Connector or another platform-approved credential mechanism for authorization.
A good configuration variable has:
- A clear API name.
- A documented data type.
- A default value or an explicit required-installation value.
- A defined owner.
- A defined effect on runtime behavior.
- A validation rule.
- A safe failure path.
### Lesson 8 — Connectors provide reusable authorization

A Connector describes how the extension communicates with a third-party OAuth 2.0 service.
Connector setup generally includes:
- Authorization URL.
- Access-token URL.
- Refresh-token URL where required.
- Client ID.
- Client secret.
- Scopes and additional parameters.
- One or more API definitions.
- Dynamic path or request parameters.
A Connector API definition should specify:
- Method.
- URL.
- Headers.
- Query parameters.
- Request body.
- Dynamic values.
- Expected response handling.
The Connector API must be tested before it is published. Current Developer Console documentation describes publishing the API as the action that makes the Connector available for association with an extension.
A custom Function can invoke a published Connector using the Connector API identifier:
arguments = Map();
arguments.put("request_key", requestKey);
arguments.put("external_id", externalId);

response = zoho.crm.invokeConnector(
    "nova_field_service.external.context.read",
    arguments
);
The exact identifier is generated by the platform and must be copied from the extension’s Connector details. The string above is illustrative only.
A Connector does not eliminate integration design. You still need to define:
- Authorization ownership.
- Reauthorization behavior.
- Revocation behavior.
- Scope minimization.
- Timeout handling.
- Error mapping.
- Rate-limit handling.
- Duplicate-event behavior.
- Data retention.
### Lesson 9 — Install actions must be small and repeatable

The Developer Console supports install actions such as:
- On installation.
- On uninstallation.
- On connector authorization.
- On connector revocation.
- On purchase.
- On plan downgrade.
A post-install script can use installation context such as:
- Organization ID.
- Installer ID.
- Whether the operation is a first installation or upgrade.
- Previous version.
Use install actions for bounded setup work:
- Seed a safe default.
- Validate required configuration.
- Record an installation marker.
- Create a small configuration record.
- Register a controlled external resource when authorization is available.
Do not use installation actions for an unbounded data migration.
Avoid a post-install script that:
- Updates every CRM record.
- Sends an email to every user.
- Creates an uncontrolled webhook fan-out.
- Stores a token in a visible field.
- Assumes a specific custom field already exists.
- Runs without a version guard.
- Cannot be safely retried.
A safe install action should be:
- Short.
- Observable.
- Idempotent or guarded.
- Limited in scope.
- Safe to run in a sandbox.
- Explicit about partial failure.
The current documentation states that an extension has one post-install script. Keep that script as an orchestrator and move complex work into separately testable functions where possible.
### Lesson 10 — Design upgrades as schema evolution

An extension is not finished when version 1 is published.
Existing installations may contain:
- Data in extension fields.
- Workflow associations.
- Connector authorizations.
- Custom buttons.
- User expectations.
- Local configuration values.
- External webhook registrations.
Current upgrade guidance indicates that component editability differs:
- Custom fields can be edited, but the field type cannot be changed.
- Custom modules cannot be deleted through the listed upgrade mechanism.
- Custom Functions can be edited and deleted.
- Connectors and custom variables can be edited.
- Workflow rules have restrictions on changing the associated module and trigger option.
- Web tabs, custom links, buttons, and related lists have their own update behavior.
Treat every published component as a compatibility commitment.
Prefer additive upgrades:
Version 1:
  nova__Service_Segment

Version 2:
  nova__Service_Segment
  nova__Context_Status
Avoid destructive upgrades such as:
Version 1:
  Service_Segment is a text field

Version 2:
  Change Service_Segment into a picklist field
Instead:
Version 2:
  Keep Service_Segment
  Add Service_Segment_Status
  Migrate deliberately if required
Record the migration plan in release notes.
### Lesson 11 — Test in a sandbox before publication

The Developer Console provides a sandbox testing workflow for extensions.
A sandbox is useful because it lets you test:
- Component installation.
- Custom module creation.
- Custom field availability.
- Workflow behavior.
- Custom Functions.
- Connector authorization.
- Widget rendering.
- Upgrade behavior.
- Uninstall behavior.
- Error handling.
A sandbox result is evidence of sandbox behavior. It is not evidence that all customer organizations will behave identically.
Before publishing, verify:
- The extension installs into a clean sandbox.
- The namespace appears as expected.
- API names are recorded.
- Required fields exist.
- Optional fields fail safely.
- Configuration is organization-specific.
- A disabled feature does not execute.
- An unauthorized Connector fails safely.
- A Connector revocation path exists.
- The extension does not expose secrets.
- Upgrade behavior is documented.
- Release notes describe changed components.
### Lesson 12 — Choose distribution deliberately

The current publishing documentation describes two main distribution paths:
1. Private publication.
2. Public listing in Zoho Marketplace.
A private extension is available through an installation URL. This can support controlled distribution to named customers or internal organizations.
A public Marketplace listing requires additional review and submission information, such as:
- Logo.
- Screenshots.
- Documentation.
- Support information.
- Pricing information where applicable.
- Release notes.
- Functional testing.
Do not describe a private installation URL as a Marketplace listing.
Do not call an extension “published to the Marketplace” until there is actual Marketplace approval evidence.
## Visual explanation

Reusable extension boundary
+--------------------------------------------------+
| Nova Field Service Extension                     |
| Namespace: nova_field_service                    |
+--------------------------------------------------+
| CRM components                                   |
|  - Account fields                                |
|  - Optional custom module                        |
|  - Custom Function                               |
|  - Workflow or button association                |
+--------------------------------------------------+
| Configuration                                    |
|  - Organization ID                               |
|  - Environment                                   |
|  - Schema version                                |
|  - Feature flag                                  |
|  - API field mapping                             |
+--------------------------------------------------+
| Authorization                                    |
|  - Connector                                     |
|  - OAuth scopes                                  |
|  - Authorization and revocation actions          |
+--------------------------------------------------+
| Presentation                                     |
|  - Widget or Web Tab, if required                |
+--------------------------------------------------+
| Lifecycle                                        |
|  - Install                                       |
|  - Sandbox test                                 |
|  - Private or Marketplace publication            |
|  - Upgrade                                      |
|  - Uninstall                                    |
+--------------------------------------------------+
Per-installation runtime
Request
  |
  v
Read current organization and environment
  |
  v
Load extension configuration
  |
  v
Load current field metadata
  |
  v
Validate namespace, org, environment, and schema
  |
  v
Build a bounded API request
  |
  v
Project only approved response fields
  |
  v
Return a stable contract
Native extension versus third-party integration
Native extension
  CRM fields
  CRM modules
  Custom Functions
  Workflow actions
  Widgets
  Templates

Third-party integration extension
  CRM components
  Connector
  OAuth authorization
  Connector APIs
  Custom variables
  Authorization/revocation actions
A single extension can contain both types of components.
## Worked case

Scenario
Nova wants to distribute the Chapter 19 CRM context logic to multiple customer organizations.
The original serverless Function assumed a known field mapping:
Account_Name
Segment
That assumption is unsafe for an extension because each installation may have:
- A different custom field API name.
- A different environment.
- A different organization.
- No optional segment field.
- A field with an incompatible type.
- A disabled feature.
- A field hidden or unavailable to the current runtime.
The extension will therefore use an installation configuration and a metadata catalog.
Extension design
extension:
  display_name: "Nova Field Service Context"
  namespace: "nova_field_service"
  type: "native-plus-integration-ready"

components:
  custom_fields:
    - label: "Nova Service Segment"
      intended_type: "text"
    - label: "Nova Context Status"
      intended_type: "picklist"
  custom_function:
    name: "nova_context_read"
    purpose: "Return approved Account context"
  custom_variables:
    - name: "Enable Context Read"
      type: "checkbox"
      default: true
    - name: "Contract Version"
      type: "text"
      default: "1"

installation:
  configuration_scope: "per organization and environment"
  live_execution: false
The actual generated field API names must be recorded after installation. Do not hardcode a guessed prefix.
Installation contract
{
  "schema_version": "1",
  "org_id": "000900000000002001",
  "environment": "sandbox",
  "enabled": true,
  "fields": {
    "name": "Account_Name",
    "segment": "Segment"
  }
}
For another synthetic installation, the segment field is different:
{
  "schema_version": "1",
  "org_id": "000900000000002002",
  "environment": "sandbox",
  "enabled": true,
  "fields": {
    "name": "Account_Name",
    "segment": "Service_Segment"
  }
}
The business contract is the same, but the installation-specific API mapping is different.
Metadata catalog
The extension reads or receives a verified metadata catalog:
{
  "org_id": "000900000000002001",
  "environment": "sandbox",
  "module": "Accounts",
  "fields": [
    {
      "api_name": "Account_Name",
      "json_type": "string",
      "visible": true
    },
    {
      "api_name": "Segment",
      "json_type": "string",
      "visible": true
    }
  ]
}
The catalog is not trusted merely because it exists. The runtime checks:
- Organization match.
- Environment match.
- Module match.
- Field uniqueness.
- JSON type.
- Visibility.
- Approved field name.
Portable planning function
The portable core determines whether a read is allowed:
"use strict";

function fail(code) {
  return { ok: false, code: code };
}

function object(value) {
  return value !== null &&
    typeof value === "object" &&
    !Array.isArray(value);
}

function text(value) {
  return typeof value === "string" &&
    value.length > 0 &&
    value.length <= 256 &&
    value.trim() === value &&
    !(/[\u0000-\u001f\u007f]/).test(value);
}

function hasExactKeys(value, keys) {
  if (!object(value)) {
    return false;
  }

  var actual = Object.keys(value).sort();
  var expected = keys.slice().sort();

  return actual.length === expected.length &&
    actual.every(function(key, index) {
      return key === expected[index];
    });
}

function planRead(config, context, catalog, input) {
  if (!object(context) ||
      !text(context.org_id) ||
      ["sandbox", "production"].indexOf(context.environment) === -1) {
    return fail("CONTEXT_INVALID");
  }

  if (!hasExactKeys(config, [
        "schema_version",
        "org_id",
        "environment",
        "enabled",
        "fields"
      ]) ||
      !hasExactKeys(config.fields, ["name", "segment"]) ||
      !text(config.org_id) ||
      typeof config.enabled !== "boolean") {
    return fail("CONFIG_INVALID");
  }

  if (config.schema_version !== "1") {
    return fail("CONFIG_VERSION_UNSUPPORTED");
  }

  if (config.org_id !== context.org_id) {
    return fail("ORG_MISMATCH");
  }

  if (config.environment !== context.environment) {
    return fail("ENV_MISMATCH");
  }

  if (!config.enabled) {
    return fail("DISABLED");
  }

  var approvedSegments = [
    "Segment",
    "Service_Segment",
    "nova_field_service__Service_Segment"
  ];

  if (config.fields.name !== "Account_Name" ||
      (config.fields.segment !== null &&
       approvedSegments.indexOf(config.fields.segment) === -1)) {
    return fail("FIELD_NOT_APPROVED");
  }

  if (!object(catalog) ||
      catalog.org_id !== context.org_id ||
      catalog.environment !== context.environment ||
      catalog.module !== "Accounts" ||
      !Array.isArray(catalog.fields)) {
    return fail("CATALOG_MISMATCH");
  }

  var selectedFields = [config.fields.name];

  if (config.fields.segment !== null) {
    selectedFields.push(config.fields.segment);
  }

  var fieldsAvailable = selectedFields.every(function(apiName) {
    var matches = catalog.fields.filter(function(field) {
      return object(field) &&
        field.api_name === apiName;
    });

    return matches.length === 1 &&
      matches[0].json_type === "string" &&
      matches[0].visible === true;
  });

  if (!fieldsAvailable) {
    return fail("FIELD_UNAVAILABLE");
  }

  if (!hasExactKeys(input, [
        "request_key",
        "crm_account_id"
      ]) ||
      !text(input.request_key) ||
      !text(input.crm_account_id)) {
    return fail("INPUT_INVALID");
  }

  return {
    ok: true,
    method: "GET",
    path: "/crm/v8/Accounts/" +
      encodeURIComponent(input.crm_account_id),
    request_key: input.request_key,
    crm_account_id: input.crm_account_id,
    fields: {
      name: config.fields.name,
      segment: config.fields.segment
    }
  };
}
The function returns a plan rather than immediately calling CRM.
This allows the caller to:
- Inspect the planned path.
- Verify the selected fields.
- Record a safe audit event.
- Test without a tenant.
- Reject unsafe configuration before a request is made.
Response projection
After the CRM response is received, project only the approved values:
function projectAccount(plan, row) {
  if (!plan ||
      plan.ok !== true ||
      !row ||
      typeof row.id !== "string" ||
      row.id !== plan.crm_account_id) {
    return {
      ok: false,
      code: "RECORD_MISMATCH"
    };
  }

  var nameField = plan.fields.name;

  if (typeof row[nameField] !== "string" ||
      row[nameField] === "") {
    return {
      ok: false,
      code: "NAME_UNAVAILABLE"
    };
  }

  var segment = null;

  if (plan.fields.segment !== null) {
    var segmentField = plan.fields.segment;

    if (row[segmentField] !== null &&
        typeof row[segmentField] !== "string") {
      return {
        ok: false,
        code: "SEGMENT_UNAVAILABLE"
      };
    }

    segment = row[segmentField];
  }

  return {
    ok: true,
    body: {
      contract_version: "1",
      source: "CRM",
      request_key: plan.request_key,
      crm_account_id: row.id,
      account: {
        id: row.id,
        name: row[nameField],
        segment: segment
      }
    }
  };
}
If the CRM record contains:
{
  "id": "000900000000002901",
  "Account_Name": "Nova Training Account",
  "Segment": "Training",
  "Internal_Notes": "Do not return this field."
}
The extension returns:
{
  "contract_version": "1",
  "source": "CRM",
  "request_key": "NOV-REQ-801",
  "crm_account_id": "000900000000002901",
  "account": {
    "id": "000900000000002901",
    "name": "Nova Training Account",
    "segment": "Training"
  }
}
The response does not contain Internal_Notes.
Install action design
The installation action should create or validate only safe defaults.
Illustrative logic:
orgId = input.installParamMap.get("organizationId");
isInstall = input.installParamMap.get("isInstall");
previousVersion = input.installParamMap.get("previousVersion");

info "Nova extension install action started";

if(isInstall == true)
{
    // Seed non-secret defaults only.
    // Do not write access tokens or client secrets.
    info "Nova extension first-install configuration requested";
}
else
{
    info "Nova extension upgrade detected from version " + previousVersion;
}
This is a design sketch. It does not claim that the script was installed or executed in a live organization.
A production implementation should also:
- Validate the actual field API names.
- Avoid repeated creation of duplicate records.
- Guard upgrade-only behavior.
- Handle partial failure.
- Record a safe status.
- Avoid logging raw installation context if it contains unnecessary identifiers.
Connector design
If Nova later integrates with an external dispatch service, the extension could add a Connector:
connector:
  display_name: "Nova Dispatch"
  auth: "OAuth 2.0"
  operations:
    - name: "read_service_context"
      method: "GET"
      path: "/v1/service-context/{external_id}"
  dynamic_parameters:
    - external_id
  credentials:
    stored_in: "platform-managed connector authorization"
  live_authorization: false
The Connector API would be tested independently before association with the extension.
The extension should not place the external service client secret in:
- Deluge source.
- A custom field.
- A visible custom variable.
- A Widget.
- A public repository.
- A release note.
- A test fixture.
## Try it yourself — guided practice

Goal
Create a reusable, installation-aware configuration boundary for Nova’s CRM context extension.
The exercise uses local synthetic data and does not require a Zoho tenant.
Part 1 — Create the extension manifest
Create a manifest with:
display_name: "Nova Field Service Context"
namespace: "nova_field_service"
extension_type: "native"
schema_version: "1"
Record the namespace as immutable in your design notes.
Add these intended components:
components:
  custom_fields:
    - label: "Nova Service Segment"
      type: "text"
    - label: "Nova Context Status"
      type: "picklist"
  custom_function:
    name: "nova_context_read"
  custom_variables:
    - name: "Enable Context Read"
      type: "checkbox"
      default: true
Do not claim that these components exist in a live CRM.
Part 2 — Create two installations
Installation A:
{
  "schema_version": "1",
  "org_id": "000900000000002001",
  "environment": "sandbox",
  "enabled": true,
  "fields": {
    "name": "Account_Name",
    "segment": "Segment"
  }
}
Installation B:
{
  "schema_version": "1",
  "org_id": "000900000000002002",
  "environment": "sandbox",
  "enabled": true,
  "fields": {
    "name": "Account_Name",
    "segment": "Service_Segment"
  }
}
Verify that the business logic remains the same while the field mapping differs.
Part 3 — Create metadata catalogs
Catalog A:
{
  "org_id": "000900000000002001",
  "environment": "sandbox",
  "module": "Accounts",
  "fields": [
    {
      "api_name": "Account_Name",
      "json_type": "string",
      "visible": true
    },
    {
      "api_name": "Segment",
      "json_type": "string",
      "visible": true
    }
  ]
}
Catalog B:
{
  "org_id": "000900000000002002",
  "environment": "sandbox",
  "module": "Accounts",
  "fields": [
    {
      "api_name": "Account_Name",
      "json_type": "string",
      "visible": true
    },
    {
      "api_name": "Service_Segment",
      "json_type": "string",
      "visible": true
    }
  ]
}
Part 4 — Plan requests locally
Use:
{
  "request_key": "NOV-REQ-801",
  "crm_account_id": "000900000000002901"
}
Expected plan:
{
  "ok": true,
  "method": "GET",
  "path": "/crm/v8/Accounts/000900000000002901",
  "request_key": "NOV-REQ-801",
  "crm_account_id": "000900000000002901",
  "fields": {
    "name": "Account_Name",
    "segment": "Segment"
  }
}
Verify that the path preserves the exact identifier.
Part 5 — Test rejection cases
Add tests for:
 1. Missing configuration.
 2. Configuration with an unexpected key.
 3. Unsupported schema version.
 4. Organization mismatch.
 5. Environment mismatch.
 6. Disabled feature.
 7. Metadata from another organization.
 8. Metadata for the wrong module.
 9. Unapproved field mapping.
10. Missing metadata.
11. Hidden field.
12. Wrong JSON field type.
13. Numeric Account ID.
14. Whitespace in the Account ID.
15. A request body attempting to override org_id.
16. A CRM response with a different record ID.
17. A CRM response containing an extra confidential field.
Each rejection should return a stable code and should not produce a request path.
Part 6 — Run the local verification
The Chapter 20 lab artifacts are:
c02_ch20_portable.cjs
c02_ch20_verify.cjs
Run:
node c02_ch20_verify.cjs
The local verification result for the prepared lab is:
34 local portability cases passed. No Zoho requests made.
This verifies the portable configuration and projection logic only.
Part 7 — Write the installation checklist
Your checklist should include:
installation_checklist:
  - namespace recorded
  - actual field API names recorded
  - field types verified
  - organization context verified
  - sandbox tested
  - install action reviewed
  - connector not required for native-only release
  - secrets absent from source and variables
  - private publication decision recorded
  - upgrade constraints documented
  - uninstall behavior documented
## Independent challenge

Design a reusable Nova extension that supports both:
1. A native CRM context feature.
2. An optional external dispatch integration.
Your design must include:
Extension identity
- Display name.
- Immutable namespace.
- Version.
- Extension type.
- Supported CRM product.
- Minimum edition assumptions, if any.
Native components
- One custom field.
- One custom Function.
- One optional custom variable.
- One workflow or button association.
- One response contract.
Third-party components
- One Connector.
- Two Connector API operations.
- OAuth authorization ownership.
- Required scopes.
- Authorization and revocation behavior.
- Error categories.
- Rate-limit behavior.
Installation behavior
- First-install action.
- Upgrade action.
- Disabled-feature behavior.
- Missing-field behavior.
- Missing-authorization behavior.
- Uninstall behavior.
Upgrade design
Document how you will handle:
- A renamed display label.
- A changed custom field type requirement.
- A new required field.
- A removed optional field.
- A Connector API change.
- A workflow condition change.
- A change from private distribution to Marketplace submission.
Evidence
Provide:
- Local configuration tests.
- Field metadata fixture.
- Connector request fixture with secrets removed.
- Expected successful response.
- Expected authorization failure.
- Expected organization mismatch.
- Expected upgrade warning.
- Statement of whether any live tenant was used.
## Common problems and recovery

Problem 1 — The extension namespace is already taken
Cause:
- Namespace uniqueness is global to the Developer Console context.
- A previous extension already uses the requested namespace.
Recovery:
- Choose a new namespace before creating the extension.
- Do not create a second extension with a temporary namespace and assume it can be renamed later.
- Record the chosen namespace in the design contract.
- Treat the namespace as immutable.
Problem 2 — The label exists but the expected API name does not
Cause:
- The platform generated a prefixed API name.
- The extension was installed into a different organization.
- A previous component already used a similar name.
- The label and API name were confused.
Recovery:
- Read the actual field metadata.
- Store the verified API name in installation configuration.
- Use API names in API requests.
- Keep display labels only for user-facing text.
Problem 3 — A custom field type cannot be changed during an upgrade
Cause:
- The original field type is part of the installed schema.
- The new version requires different semantics.
Recovery:
- Keep the original field.
- Add a new field with a new API name.
- Add a migration or compatibility layer.
- Mark the old field as deprecated.
- Update documentation and release notes.
- Do not silently reinterpret existing values.
Problem 4 — A Connector is not available for association
Possible causes:
- The Connector API has not been published.
- The Connector belongs to another Developer Console context.
- The Connector was not added to the extension.
- Client credentials have not been configured.
- The Connector contains an invalid API definition.
Recovery:
1. Test the Connector API independently.
2. Publish the Connector API if appropriate.
3. Associate the Connector with the extension.
4. Configure client credentials through the console.
5. Verify the generated redirect URL with the third-party provider.
6. Do not put client credentials in source code.
7. Test authorization in a sandbox.
Problem 5 — A custom variable is visible when it should not be
Cause:
- The variable type or visibility was configured incorrectly.
- A hidden variable was treated as a secure secret store.
- The value is being surfaced through a response or log.
Recovery:
- Remove secrets from the variable.
- Use a Connector or secure platform credential mechanism.
- Review variable visibility.
- Redact the value from logs and responses.
- Rotate any credential that may have been exposed.
Problem 6 — Install action runs more than expected
Cause:
- Installation and upgrade behavior were not distinguished.
- The script lacks a version guard.
- A side effect is not idempotent.
- A retry occurs after partial completion.
Recovery:
- Read the installation context.
- Branch explicitly between first installation and upgrade.
- Use an installation marker.
- Make creation operations idempotent.
- Avoid sending irreversible notifications during a retry.
- Keep the action bounded.
Problem 7 — A field appears in metadata but is not safe to return
Cause:
- Field visibility was mistaken for data approval.
- Sensitive or private fields were included in a broad query.
- The projection copied all fields from the CRM response.
Recovery:
- Maintain an explicit response allowlist.
- Select only required fields.
- Check field permissions and compliance settings.
- Never return the raw CRM object.
- Add a test containing a synthetic confidential field and verify exclusion.
Problem 8 — A private extension is described as a public product
Cause:
- The extension has a private installation URL but has not completed Marketplace review.
- Publication and listing were treated as the same action.
Recovery:
- Label the extension status precisely:
- Draft.
- Sandbox tested.
- Privately published.
- Submitted to Marketplace.
- Marketplace approved.
- Keep installation evidence separate from Marketplace evidence.
- Do not claim customer availability without installation evidence.
Problem 9 — A workflow association breaks during upgrade
Cause:
- The upgrade changed a restricted workflow property.
- The associated module or trigger option is not editable in the current upgrade model.
- The extension assumes that existing customer workflow configuration matches the developer sandbox.
Recovery:
- Preserve the existing workflow association.
- Add a new rule when an additive change is required.
- Document the migration steps.
- Validate the upgraded extension in a sandbox.
- Test both clean installation and upgrade installation.
## Check your understanding

 1. What is the difference between a native extension and a third-party integration extension?
 2. Why should an extension namespace be selected before adding components?
 3. Why should runtime code use API names rather than display labels?
 4. What is a safe use for a custom variable?
 5. Why should a custom variable not be used for an OAuth client secret?
 6. What must happen before a Connector can be associated with an extension?
 7. What information can an install action receive?
 8. Why should post-install scripts be bounded and version-aware?
 9. What is the purpose of a sandbox extension test?
10. Why can a custom field type not simply be changed during an upgrade?
11. What is the difference between private publication and Marketplace listing?
12. Why does the runtime validate organization and environment before making a CRM request?
13. What should happen when metadata identifies a hidden or incompatible field?
14. Why is a raw CRM record response unsuitable as an extension response?
15. Does a reusable extension automatically provide a durable queue or delivery ledger?
## Solutions and explanations

Guided practice solution
A sound solution has these characteristics:
- The namespace is recorded as immutable.
- Installation configuration includes organization and environment.
- The field mapping is installation-specific.
- The metadata catalog is associated with the same organization and environment.
- The module is explicitly verified as Accounts.
- The selected fields are checked for uniqueness, type, and visibility.
- The request body cannot override installation context.
- Identifiers remain strings.
- URL path values are encoded.
- A failed validation produces no request path.
- The CRM response is projected through an allowlist.
- Extra fields are excluded.
- The local verification uses fake data and makes no Zoho requests.
The prepared lab passed:
34 local portability cases passed. No Zoho requests made.
That result is local evidence for the portable core. It is not tenant evidence.
Independent challenge solution
A suitable extension architecture is:
Native layer
  - Accounts custom field for service segment
  - Custom Function for context read
  - Optional feature flag
  - Optional CRM button

Integration layer
  - OAuth 2.0 Connector
  - Read-context API
  - Update-context API
  - Authorization action
  - Revocation action

Lifecycle layer
  - Install defaults
  - Sandbox test
  - Private publication
  - Upgrade notes
  - Uninstall behavior
The Connector should be published and tested before being associated with the extension. Client credentials belong in the Developer Console and the third-party provider configuration, not in Deluge or Widget source.
The extension should return stable error categories such as:
CONFIG_INVALID
ORG_MISMATCH
FIELD_UNAVAILABLE
CONNECTOR_NOT_AUTHORIZED
EXTERNAL_RATE_LIMIT
EXTERNAL_TIMEOUT
UPGRADE_REQUIRES_MIGRATION
The extension should not return a raw external response or raw exception.
Check-your-understanding answers
 1. A native extension adds components inside a Zoho application; a third-party integration extension connects the application to an external service, typically through integration components such as Connectors.
 2. The namespace is used to identify and isolate extension components and cannot be changed after creation according to the current Developer Console documentation.
 3. Labels can change or vary by language. API names are the stable integration identifiers.
 4. A custom variable can store non-secret organization-specific configuration such as a feature flag, mode, region, or contract version.
 5. Custom variables are configuration values, not a secure token vault. Client secrets and tokens belong in platform-managed authorization mechanisms.
 6. Its API definitions must be created and tested, and the Connector/API must be published before it becomes available for association.
 7. Organization ID, installer ID, installation-versus-upgrade status, and previous version information can be available through the installation context.
 8. Installation may be retried or followed by an upgrade. Version guards and bounded side effects prevent duplicate or unsafe changes.
 9. A sandbox permits extension behavior to be tested without changing the real production organization.
10. The existing field’s type is part of the installed schema. Add a new field or migration path instead.
11. Private publication provides controlled access through an installation URL. Marketplace listing requires submission and review for public availability.
12. Without those checks, configuration from one installation or environment could be used against another.
13. Reject the configuration or omit the optional field according to the documented contract. Do not silently use an unapproved field.
14. It can expose fields that were not approved for the extension’s contract and may contain sensitive information.
15. No. An extension can package reusable components, but durable queues, retry state, worker leases, and delivery ledgers still require explicit design and storage.
## Chapter recap and next step

This chapter introduced extensions as reusable, installable product boundaries.
You learned that:
- Native extensions add reusable CRM functionality.
- Third-party integrations combine CRM components with Connectors and authorization.
- Namespaces are stable identifiers and should be selected before component creation.
- API names are safer integration contracts than display labels.
- Metadata must be inspected per installation.
- Custom variables are appropriate for non-secret configuration.
- OAuth credentials belong in Connectors or other managed authorization mechanisms.
- Install actions should be short, bounded, and version-aware.
- Upgrades must respect component mutability and schema constraints.
- Sandbox testing provides controlled extension evidence.
- Private publication and Marketplace listing are different states.
- Reusable packaging does not eliminate organization-specific configuration.
- An extension does not automatically provide durable delivery or queue semantics.
In the next chapter, you will test extensions, SDK components, and integration boundaries systematically, then evaluate performance and failure behavior before release.
## Glossary and further reading

Glossary
API name
The stable identifier used by APIs for a CRM module or field.
Connector
A reusable integration component that defines authentication and API operations for a third-party service.
Custom variable
An extension-level configuration value that can be reused by extension components.
Extension
A packaged set of components that adds functionality to a Zoho application or integrates it with a third-party service.
Install action
A script associated with installation, uninstallation, authorization, revocation, purchase, or plan changes.
Marketplace listing
Public distribution of an extension after submission and review.
Native extension
An extension that primarily adds functionality inside a Zoho application.
Namespace
A unique extension identifier used to distinguish extension components.
Private publication
Distribution through a controlled installation URL rather than a public Marketplace listing.
Projection
Selecting and reshaping only approved fields from a larger API response.
Sandbox
An isolated environment used to test extension components without changing the real production organization.
Schema evolution
Managing changes to installed data structures and contracts across extension versions.
Third-party integration extension
An extension that connects a Zoho application to an external service.
Further reading
- Zoho Developer — Build an Extension (https://www.zoho.com/developer/extensions.html)
- Extensions Overview (https://www.zoho.com/developer/help/extensions/overview.html)
- Quickstart Guide for Extensions (https://www.zoho.com/developer/help/extensions/quick-start.html)
- Extension Creation and Components (https://www.zoho.com/developer/help/extensions/build-extension/create-extension.html)
- Setting Up a Plugin and Namespace (https://www.zoho.com/developer/help/extensions/build-extension/create-a-new-plugin.html)
- Custom Variables (https://www.zoho.com/developer/help/extensions/custom-variables.html)
- Connectors (https://www.zoho.com/developer/help/extensions/connectors.html)
- Install Actions (https://www.zoho.com/developer/help/extensions/post-install-script.html)
- Testing an Extension (https://www.zoho.com/developer/help/extensions/test-extension.html)
- Publishing an Extension (https://www.zoho.com/developer/help/extensions/publish-extension.html)
- Updating an Extension (https://www.zoho.com/developer/help/extensions/upgrade-index.html)
- Building a Client-Side Application (https://www.zoho.com/developer/help/extensions/buildingwidgets.html)
- Installing and Using Zet CLI (https://www.zoho.com/developer/help/extensions/zappscli.html)
- CRM Fields Metadata API (https://www.zoho.com/crm/developer/docs/api/v8/field-meta.html)
- CRM Get Records API (https://www.zoho.com/crm/developer/docs/api/v8/get-records.html)
- Zoho CRM JavaScript SDK and Embedded Apps (https://help.zwidgets.com/help/latest/index.html)

### Testing, performance and release readiness

### Testing module — What you will learn
By the end of this chapter, you will be able to:
- Design tests for Creator, CRM, Functions, Widgets, SDKs, and extensions.
- Separate unit, contract, integration, sandbox, and production evidence.
- Build a scenario matrix for successful and failed integration paths.
- Test duplicate events, malformed payloads, authentication failures, quotas, conflicts, and uncertain outcomes.
- Create performance budgets without confusing them with platform limits.
- Estimate API credit usage for common CRM operations.
- Account for API concurrency and sub-concurrency.
- Account for Function execution time, response size, and execution credits.
- Choose between single-record APIs, COQL, Composite, Bulk Read, and Bulk Write.
- Use synthetic latency and failure injection to test recovery behavior.
- Interpret Function revisions, logs, failures, analytics, and credit information.
- Decide whether an implementation is ready for sandbox testing, controlled release, or further development.
- Preserve Nova’s rule that accepted Creator completion remains valid when CRM delivery fails.
This testing module extends the extension design you have just completed. It verifies reusable components under normal load, invalid input, API failure, quota pressure, duplicate delivery and version changes.
### Testing module — Lessons
### Testing module — Lesson 1 — Testing is an evidence model
A test is not only a command that returns “pass.”
A useful test records:
- The scenario.
- The input.
- The expected result.
- The observed result.
- The execution environment.
- The version under test.
- The data source.
- The timestamp.
- The evidence location.
- Any unresolved limitation.
For Nova, distinguish these evidence classes:
Evidence class	Example	What it proves
Pure local test	Validate an event-key function	Local code behavior
Fake-client test	Simulate CRM 404	Error mapping behavior
Contract test	Validate a synthetic CRM response shape	Parser and projection behavior
Sandbox test	Run a Function in CRM Sandbox	Behavior in a controlled Zoho environment
Tenant test	Call a configured CRM organization	Current tenant behavior
Production observation	Review deployed logs and outcomes	Behavior in the live release
A local test must not be reported as a live CRM result.
A sandbox result must not automatically be reported as a production result.
A successful HTTP status must not automatically be reported as a successful business operation.
### Testing module — Lesson 2 — Use test layers
A practical test pyramid for the Nova integration is:
                 +----------------------+
                 | Production evidence |
                 +----------------------+
                 | Sandbox scenarios   |
                 +----------------------+
                 | Contract/API tests  |
                 +----------------------+
                 | Component tests     |
                 +----------------------+
                 | Pure logic tests    |
                 +----------------------+
Pure logic tests
Test functions without Zoho access:
- Validate event keys.
- Validate opaque identifiers.
- Validate configuration.
- Build query paths.
- Select allowed fields.
- Classify errors.
- Calculate retry decisions.
- Calculate API budgets.
Component tests
Test a function with fake dependencies:
- Fake CRM client.
- Fake Connector.
- Fake clock.
- Fake destination.
- Fake quota response.
- Fake timeout.
Contract tests
Test that the code understands expected request and response shapes:
- CRM record response.
- COQL response.
- Composite response.
- Bulk job response.
- Connector response.
- Function REST response.
Sandbox tests
Use the extension or Function sandbox to verify:
- Installation.
- Permissions.
- Field API names.
- Workflow association.
- Function execution.
- Connector authorization.
- Widget or extension behavior.
- Upgrade behavior.
Controlled production tests
Use only when the release process permits them:
- Small synthetic or approved records.
- Narrow scope.
- Monitoring in place.
- Rollback or disablement available.
- No unbounded writes.
### Testing module — Lesson 3 — Test the business scenarios, not only the happy path
Nova’s minimum scenario suite includes:
Scenario	Expected classification
Missing required field	Blocked
Invalid lookup	Blocked
Unauthorized action	Blocked
Token or Connection failure	Blocked until reauthorized
Duplicate completion event	Suppressed or already delivered
Timeout before destination commit	Retryable
Timeout after destination commit	Uncertain; reconcile
Malformed payload	Blocked
Quota exhaustion	Retryable after a bounded delay
Conflicting update	Blocked or reconciliation-required
Successful delivery	Delivered
Missing destination record	Retryable or Blocked according to contract
CRM accepted, external response lost	Uncertain
Partial batch result	Retry only failed items
Unsupported schema version	Blocked
A scenario should be specific enough that another engineer can reproduce it.
Weak scenario:
Test failure handling.
Useful scenario:
Given Event_Key NOV-REQ-801:completed:v1 has not been delivered,
when the destination commits the upsert but the response times out,
then the delivery state is Uncertain,
no blind duplicate write is issued,
and reconciliation is required before another write.
### Testing module — Lesson 4 — Model failure states explicitly
A useful delivery state model is:
Pending
  |
  v
InFlight
  |
  +--> Delivered
  |
  +--> Retryable
  |       |
  |       +--> InFlight
  |
  +--> Blocked
  |
  +--> Uncertain
          |
          +--> Reconcile
                    |
                    +--> Delivered
                    +--> Retryable
                    +--> Blocked
The Uncertain state matters.
If a request times out, you do not know whether:
- The destination rejected it before processing.
- The destination accepted it but the response was lost.
- The destination committed it and the caller timed out.
- The destination committed it partially.
- The network failed after the remote system changed state.
Do not treat every timeout as a safe retry.
Nova’s future reliable delivery ledger does not yet exist in production. The state model in this chapter is a local design and testing model.
### Testing module — Lesson 5 — Define performance budgets separately from platform limits
A platform limit is imposed by Zoho or another service.
A performance budget is an engineering target chosen for a specific workflow.
Examples:
Item	Platform limit or documented behavior	Example lab budget
REST Function timeout	10 seconds	Complete under 8 seconds
REST response size	10 MB	Keep response under 1 MB
API concurrency	Edition-dependent	Keep test peak below 15
Sub-concurrency	10 for listed heavy APIs	Keep test peak below 8
Widget initial load	Tenant/application dependent	Render core state under 2 seconds
Retry attempts	No universal business rule	Maximum 3 automatic attempts
Batch size	API-specific	Use the smallest batch that meets throughput
The lab budget is not a claim about Zoho’s universal product limit.
A good budget includes:
- Target.
- Measurement method.
- Environment.
- Sample size.
- Failure threshold.
- Action when exceeded.
Example:
performance_budget:
  component: "nova_context_read"
  environment: "sandbox"
  request_type: "REST API Function"
  target_execution_seconds: 8
  hard_platform_timeout_seconds: 10
  target_response_bytes: 1048576
  max_api_calls_per_request: 2
  peak_org_concurrency_target: 15
  sample_count: 30
  action_on_breach: "block release and investigate"
### Testing module — Lesson 6 — Understand CRM API credits
The current CRM API limits documentation describes a rolling 24-hour credit system. Credit usage varies by operation.
Examples documented for CRM v8 include:
Operation	Documented credit behavior
Most standard APIs	1 credit
Composite request	1 credit
COQL with limit 1–200	1 credit
COQL with limit 201–1000	2 credits
COQL with limit 1001–2000	3 credits
Insert, update, or upsert	1 credit per 10 records
Send Mail	20 credits
Bulk Read initialize	50 credits
Bulk Write initialize	500 credits
Create custom field	10 credits per field
Create custom module	500 credits
Credit and concurrency constraints are separate.
An implementation can have enough daily credits but still fail because:
- Too many calls are active at once.
- A heavy API reaches sub-concurrency.
- A Function reaches its execution timeout.
- A Function exhausts its Function credit allowance.
- A Connector or external service imposes its own limit.
Estimate cost before writing a loop.
Example:
1,000 individual record updates
= approximately 1,000 API calls
= approximately 1,000 credits

10 update calls with 100 records each
= approximately 10 API calls
= approximately 100 credits
The second design may be more efficient, but it still needs tests for:
- Partial batch failure.
- Record-level error results.
- Retry selection.
- Request-size limits.
- Ordering.
- Idempotency.
### Testing module — Lesson 7 — Understand API concurrency
Current CRM API documentation describes edition-dependent concurrency limits.
The documentation lists these example organization/application concurrency limits:
Edition	Concurrency
Free	5
Standard/Starter	10
Professional	15
Enterprise/Zoho One	20
Ultimate/CRM Plus	25
The same documentation describes a sub-concurrency limit of 10 for selected resource-intensive API operations, including:
- Get Records with certain parameters.
- Convert Lead.
- Insert, Update, or Upsert for more than 10 records.
- Send Mail.
- Search Records invoked from a Function.
- Query API.
- Composite API.
Concurrency is not a license to launch unlimited parallel requests.
If a worker launches 100 calls in parallel:
Desired concurrency: 100
Available concurrency: 20
Result: throttling, errors, retries, and more pressure
Use bounded concurrency:
async function mapWithLimit(items, limit, worker) {
  var next = 0;
  var results = new Array(items.length);

  async function run() {
    while (true) {
      var index = next;
      next += 1;

      if (index >= items.length) {
        return;
      }

      results[index] = await worker(items[index], index);
    }
  }

  var workers = [];
  var count = Math.min(limit, items.length);

  for (var i = 0; i < count; i += 1) {
    workers.push(run());
  }

  await Promise.all(workers);
  return results;
}
The limit must be chosen from the actual organization, API type, and workload. The value 5 or 10 in a code sample is not a universal Zoho recommendation.
### Testing module — Lesson 8 — Choose the correct data API
Different APIs have different cost and performance characteristics.
Get Records
Use when:
- You need records from one module.
- You can paginate.
- You know the required fields.
- You need a relatively direct record read.
The current API documentation states that:
- Up to 50 field API names can be specified in the fields parameter.
- A request returns up to 200 records.
- Page-based pagination can reach the first 2,000 records.
- A page token is required for larger retrievals.
- Page tokens are user-specific and expire.
- Up to 100,000 records can be retrieved through the documented pagination path.
Search Records
Use when:
- You need module-specific search.
- The search criteria are well-defined.
- You can handle special-character encoding.
- A search result is bounded.
The current documentation states:
- Up to 10 criteria can be used.
- A single call can return up to 200 records.
- Search is limited to 2,000 records.
- Search can behave differently for special characters and equals.
- Immediately searching after a create or edit can encounter indexing delay.
Do not use Search Records as a universal exact-match database query without testing the criteria semantics.
COQL
Use when:
- You need joins across lookup-linked modules.
- You need aggregates.
- You need a structured query.
- You need controlled field selection.
The current COQL documentation states:
- Up to 500 field API names can be selected.
- Up to 25 criteria can be used.
- LIMIT has credit implications.
- The documented maximum per query is 2,000 records.
- Pagination and ordering must be designed deliberately.
- API names, not labels, belong in the query.
Composite
Use when:
- You have up to five related sub-requests.
- You need to reduce round trips.
- You need controlled sequencing.
- You may need rollback behavior.
Composite requests can use:
- Sequential execution.
- Parallel execution for independent sub-requests.
- rollback_on_fail for a transaction-like request behavior.
Parallel execution is inappropriate when a sub-request depends on the result of another sub-request.
Bulk Read
Use when:
- You need a large export.
- The result can be asynchronous.
- CSV or ICS output is acceptable.
- Polling or a callback can be supported.
Bulk Read is not an immediate record lookup API.
Bulk Write
Use when:
- You need large insert, update, or upsert operations.
- You can prepare a CSV ZIP.
- You can process an asynchronous job.
- You can consume a result file containing status and errors.
The current documentation states that Bulk Write supports up to 25,000 records in one API call, subject to documented CSV limitations.
### Testing module — Lesson 9 — Measure the whole request path
A request’s latency is not only the CRM API latency.
For a Nova Function:
Caller
  |
  +-- Network to Function
  |
  +-- Function startup
  |
  +-- Input parsing
  |
  +-- Configuration lookup
  |
  +-- Metadata lookup, if not cached
  |
  +-- CRM request
  |
  +-- Response validation
  |
  +-- Projection
  |
  +-- Response serialization
  |
  +-- Network to caller
Record at least:
- Total elapsed time.
- Number of CRM calls.
- Number of external calls.
- Function execution time.
- Response size.
- Retry count.
- Concurrency.
- API credits consumed or estimated.
- Outcome classification.
Do not optimize only the slowest single API call. A design with five fast sequential calls may be slower and more expensive than one carefully designed query.
### Testing module — Lesson 10 — Use controlled failure injection
Failure injection changes one dependency at a time.
Examples:
CRM returns 401
CRM returns 403
CRM returns 404
CRM returns 429
CRM returns 500
Connection throws
Destination times out before commit
Destination times out after commit
Destination returns a conflict
Payload contains an unknown field
Payload contains a numeric ID
Configuration belongs to another organization
A failure injection test should answer:
- Is the error classified?
- Is it safe to retry?
- Is the event state preserved?
- Is an operator action required?
- Is the response redacted?
- Is the error observable?
- Does the test avoid making another live call?
Use deterministic fixtures rather than random failures for core tests.
Randomized or load testing can be added later after deterministic behavior is correct.
### Testing module — Lesson 11 — Use Function management evidence
The current Function management documentation describes several operational views:
- Functions list.
- Analytics.
- Revisions.
- Logs.
- Failures.
- Credits.
Use these views as separate evidence sources.
Revisions
Use revisions to answer:
- Which version was deployed?
- Who deployed it?
- What changed?
- Which version should be compared with the failure?
Java, Node.js, and Python Functions use draft and deployment behavior. Deluge has different save behavior.
Logs
Use logs for:
- Safe correlation IDs.
- Outcome classes.
- Duration categories.
- External operation names.
- Retry state.
Do not log tokens, raw payloads, or complete records.
Failures
The Function management documentation describes a Failures view and rerun actions.
A rerun is not automatically safe.
Before rerunning:
1. Determine whether the Function performs a read or write.
2. Identify the business key.
3. Check whether the destination may have committed.
4. Confirm idempotency behavior.
5. Verify the current Connection.
6. Record the operator decision.
Analytics
Use Analytics to inspect:
- Execution by category.
- Execution by source.
- Execution by language.
- Execution by module.
- Most executed Functions.
- Most credit-consuming Functions.
Analytics are useful for identifying trends. They are not a substitute for request-level tracing.
Credits
Use the Credits view to inspect:
- Available credits.
- Unused credits.
- Additional credits.
- Current charge.
- Billing period.
- High-consumption Functions.
### Testing module — Visual explanation
Test evidence flow
Requirement
    |
    v
Scenario
    |
    +--> Pure local test
    |
    +--> Fake dependency test
    |
    +--> Contract test
    |
    +--> Sandbox test
    |
    +--> Controlled tenant test
    |
    v
Evidence record
    |
    +-- expected
    +-- observed
    +-- environment
    +-- version
    +-- limitations
Performance budget
Request budget
+------------------------------------------------+
| Function time                                  |
|   parse + validate + CRM calls + projection    |
+------------------------------------------------+
| API budget                                     |
|   credits + concurrency + sub-concurrency      |
+------------------------------------------------+
| Payload budget                                 |
|   request bytes + response bytes               |
+------------------------------------------------+
| Retry budget                                   |
|   attempts + delay + reconciliation            |
+------------------------------------------------+
| Operational budget                             |
|   logs + audit + support effort                |
+------------------------------------------------+
Failure classification
Malformed input
    |
    +--> Blocked

Invalid permission or expired authorization
    |
    +--> Blocked until operator action

Quota or temporary service failure
    |
    +--> Retryable with bounded backoff

Timeout before known commit
    |
    +--> Retryable after policy delay

Timeout after possible commit
    |
    +--> Uncertain; reconcile first

Duplicate event with delivered ledger state
    |
    +--> Suppressed
### Testing module — Worked case
Scenario
Creator has accepted a Nova service request completion.
The integration event is:
request_key: "NOV-REQ-801"
event_key: "NOV-REQ-801:completed:v1"
crm_account_id: "000900000000002901"
event_type: "completion"
payload_version: "1"
lab_marker: "NOVCH20LAB901A"
The intended future flow is:
Creator completion accepted
        |
        v
Delivery boundary
        |
        +--> CRM summary or external destination
The delivery boundary does not yet have a production queue or persistent ledger. This chapter uses an in-memory test ledger to validate the intended state transitions.
Scenario matrix
ID	Setup	Expected result
S01	Valid completion event	Delivered
S02	Missing event_key	Blocked
S03	Numeric CRM ID	Blocked
S04	Wrong event-key format	Blocked
S05	Destination success	Delivered
S06	Same event replayed after delivery	Duplicate suppressed
S07	Timeout before commit	Retryable
S08	Timeout after possible commit	Uncertain
S09	Destination quota	Retryable
S10	Destination authorization failure	Blocked
S11	Destination conflict	Blocked
S12	Destination client exception	Retryable
S13	Unknown destination result	Blocked
S14	REST Function completes in 9 seconds	Within platform timeout
S15	REST Function takes 11 seconds	Timeout breach
S16	Response is over 10 MB	Response-size breach
S17	Organization concurrency reaches 21 on a 20-call budget	Concurrency breach
S18	Heavy API sub-concurrency reaches 11	Sub-concurrency breach
Event envelope
The event-key rule remains:
Event_Key = Request_Key + ":completed:v1"
A validator should reject:
{
  "event_key": "NOV-OTHER:completed:v1",
  "request_key": "NOV-REQ-801",
  "event_type": "completion",
  "crm_account_id": "000900000000002901",
  "payload_version": "1"
}
because the event key does not correspond to the request key.
A CRM ID must remain a string:
{
  "crm_account_id": "000900000000002901"
}
Do not use:
Number("000900000000002901");
parseInt("000900000000002901", 10);
Delivery simulator
The local simulator uses an injected destination:
async function deliver(input, dependencies) {
  var parsed = validateEnvelope(input);

  if (!parsed.ok) {
    return parsed;
  }

  var value = parsed.value;
  var previous = dependencies.ledger.get(value.event_key);

  if (previous && previous.state === "Delivered") {
    return {
      ok: true,
      state: "Delivered",
      code: "DUPLICATE_SUPPRESSED",
      destination_id: previous.destination_id,
      api_calls: 0
    };
  }

  var response;

  try {
    response = await dependencies.destination.upsert({
      event_key: value.event_key,
      request_key: value.request_key,
      crm_account_id: value.crm_account_id
    });
  } catch (error) {
    return {
      ok: false,
      state: "Retryable",
      code: "DESTINATION_CLIENT_ERROR",
      retryable: true
    };
  }

  if (response.kind === "success") {
    dependencies.ledger.put(value.event_key, {
      state: "Delivered",
      destination_id: response.destination_id
    });

    return {
      ok: true,
      state: "Delivered",
      code: "DELIVERED",
      destination_id: response.destination_id,
      api_calls: 1
    };
  }

  if (response.kind === "timeout_before_commit") {
    dependencies.ledger.put(value.event_key, {
      state: "Retryable"
    });

    return {
      ok: false,
      state: "Retryable",
      code: "TIMEOUT_BEFORE_COMMIT",
      retryable: true
    };
  }

  if (response.kind === "timeout_after_commit") {
    dependencies.ledger.put(value.event_key, {
      state: "Uncertain"
    });

    return {
      ok: false,
      state: "Uncertain",
      code: "TIMEOUT_AFTER_COMMIT",
      retryable: false
    };
  }

  return {
    ok: false,
    state: "Blocked",
    code: "DESTINATION_UNEXPECTED",
    retryable: false
  };
}
This is a teaching simulator.
It does not claim that Nova has a production ledger. It demonstrates the state transitions that a future durable implementation must preserve.
Performance budget
For the REST context Function, use this instructional budget:
component: "nova_context_read"
category: "rest_api"
target_execution_seconds: 8
documented_category_timeout_seconds: 10
target_response_bytes: 1048576
organization_concurrency_target: 15
organization_concurrency_test_limit: 20
sub_concurrency_target: 8
sub_concurrency_test_limit: 10
automatic_retry_attempts: 3
The values 8, 1 MB, 15, and 8 are lab targets.
The values 10 and 10 correspond to documented Function/API limits used by the test fixture. Actual availability and behavior must be verified in the target organization.
API planning example
Suppose a nightly reconciliation needs:
Read 100 Accounts
Read 100 Service Requests
Update 100 CRM summary records
A naïve design could issue:
100 Account reads
100 Service Request reads
100 individual updates
= approximately 300 API calls
A more deliberate design could use:
1 COQL query for related reads
10 update calls with 10 records each
= approximately 11 API calls
The second design still requires:
- Query field validation.
- Criteria validation.
- Update payload validation.
- Partial-result handling.
- Conflict handling.
- Idempotency.
- Concurrency control.
- Response verification.
A Composite request may reduce round trips for up to five sub-requests, but it should only use parallel execution when the sub-requests are independent. Dependent requests should be sequenced.
A Bulk Write job may be appropriate for a large asynchronous migration, but it is not appropriate for a user waiting for an immediate Button response.
### Testing module — Try it yourself — guided practice
Goal
Build a local scenario and performance harness for the Nova completion event.
The exercise uses synthetic dependencies and makes no Zoho requests.
Part 1 — Create the baseline event
Use:
{
  "event_key": "NOV-REQ-801:completed:v1",
  "request_key": "NOV-REQ-801",
  "event_type": "completion",
  "crm_account_id": "000900000000002901",
  "payload_version": "1"
}
Verify:
- All required keys exist.
- No unexpected keys exist.
- All identifiers are strings.
- The event key matches the request key.
- The payload version is supported.
- The event type is supported.
Part 2 — Create a fake destination
Create a destination with an upsert method that can return:
{ kind: "success", destination_id: "NOV-DEST-901" }
Also implement fixtures for:
{ kind: "timeout_before_commit" }
{ kind: "timeout_after_commit" }
{ kind: "quota" }
{ kind: "auth" }
{ kind: "conflict" }
Do not contact a real external system.
Part 3 — Implement duplicate suppression
Run the same valid event twice.
Expected behavior:
First run:
  state = Delivered
  api_calls = 1

Second run:
  state = Delivered
  code = DUPLICATE_SUPPRESSED
  api_calls = 0
The second run must not invoke the destination again.
Part 4 — Test uncertain outcomes
Simulate:
Destination commits the record.
Response is lost.
Caller receives a timeout.
Expected result:
state: "Uncertain"
retryable: false
next_action: "reconcile before another write"
Do not convert the result directly to Retryable.
Part 5 — Create a performance evaluator
Evaluate:
{
  "category": "rest_api",
  "execution_seconds": 9,
  "response_bytes": 1024,
  "api_calls": 2,
  "concurrent_calls": 1,
  "sub_concurrent_calls": 1,
  "org_concurrency_limit": 20,
  "sub_concurrency_limit": 10
}
Expected result:
Within the documented category timeout and concurrency fixture.
Then change execution_seconds to 11.
Expected result:
FUNCTION_TIMEOUT
Part 6 — Add API cost estimation
Use these local cost rules:
read: 1
update_10_records: 1
coql_200: 1
coql_1000: 2
coql_2000: 3
composite: 1
bulk_read_initialize: 50
bulk_write_initialize: 500
send_mail: 20
Explain that these are documented examples and that the actual API plan must be checked against the current official limits and tenant edition.
Part 7 — Record the evidence
Create an evidence table:
Item	Expected	Observed	Environment
Valid envelope	Accepted	 	Local
Duplicate event	Suppressed	 	Local
Timeout before commit	Retryable	 	Local
Timeout after commit	Uncertain	 	Local
Auth failure	Blocked	 	Local
REST timeout breach	Detected	 	Local
Response-size breach	Detected	 	Local
Live Zoho request	Not attempted	 	None
The prepared local verification artifacts are:
c02_ch20_harness.cjs
c02_ch20_verify.cjs
Run:
node c02_ch20_verify.cjs
Prepared local result:
26 local scenario and budget cases for this chapter passed. No Zoho requests made.
### Testing module — Independent challenge
Design a complete test plan for Nova’s extension and CRM delivery boundary.
Your plan must include:
Functional scenarios
- Successful Account context read.
- Missing Account.
- Invalid Account ID.
- Unsupported configuration version.
- Organization mismatch.
- Environment mismatch.
- Hidden or incompatible field.
- Accepted Creator completion.
- Duplicate completion.
- CRM authorization failure.
- External destination authorization failure.
- Quota exhaustion.
- Destination conflict.
- Timeout before commit.
- Timeout after possible commit.
- Reconciliation success.
- Reconciliation failure.
- Partial batch result.
Performance scenarios
- One-record context read.
- Ten-record bounded batch.
- One hundred-record batch.
- Composite request with independent sub-requests.
- Composite request with dependent sub-requests.
- COQL with a small limit.
- COQL with a larger limit.
- Bulk Read job initialization.
- Bulk Write job initialization.
- Function response near the instructional response budget.
- Function execution near the documented timeout.
- Concurrency at one below the configured limit.
- Concurrency at one above the configured limit.
Test evidence
For every scenario, record:
scenario_id:
description:
input_fixture:
expected_state:
expected_code:
retryable:
expected_api_calls:
expected_credit_class:
expected_log_category:
environment:
observed_result:
evidence_location:
live_tenant_used: false
Release decision
Define:
- Conditions for passing local tests.
- Conditions for entering Sandbox.
- Conditions for private extension publication.
- Conditions for a controlled tenant pilot.
- Conditions for blocking release.
- Conditions that require reconciliation rather than retry.
- Conditions that require reauthorization.
- Conditions that require a schema migration.
### Testing module — Common problems and recovery
Problem 1 — A test passes locally but fails in Sandbox
Possible causes:
- Tenant field API name differs.
- Sandbox metadata is stale.
- Connection authorization differs.
- Edition or permission differs.
- Function runtime differs.
- The Function is using admin-level access in one context and Connection-level access in another.
Recovery:
1. Record the exact environment.
2. Retrieve current metadata.
3. Verify the Function revision.
4. Verify the Connection owner and scopes.
5. Compare the request and response contract.
6. Do not change the local fixture to imitate an undocumented tenant response without recording the difference.
Problem 2 — A search immediately after a write returns no record
Cause:
- Search indexing delay.
Recovery:
- Do not assume the write failed.
- Use the response from the write operation where possible.
- Use a documented read or Query path if immediate retrieval is required.
- Add a bounded reconciliation check.
- Avoid unbounded polling.
Problem 3 — Parallel calls trigger throttling
Cause:
- The worker exceeds organization concurrency.
- A resource-intensive API reaches sub-concurrency.
- Multiple Functions share the same organization limits.
Recovery:
- Bound concurrency.
- Use a queue or scheduler for larger work.
- Reduce unnecessary calls.
- Use Composite, COQL, or bulk APIs when appropriate.
- Add jittered backoff for retryable throttling.
- Do not retry all failed requests simultaneously.
Problem 4 — A Function exceeds its timeout
Cause:
- Too much work in an interactive category.
- Sequential external calls.
- Large response construction.
- Unbounded loops.
- Metadata fetched on every request.
- A slow external Connection.
Recovery:
- Reduce fields and records.
- Use one query instead of multiple reads.
- Move batch work to a Schedule Function or external worker.
- Cache only where the data lifecycle permits it.
- Separate interactive acknowledgement from asynchronous processing.
- Measure each stage of the request path.
Problem 5 — A Composite request is faster but produces unsafe results
Cause:
- Dependent operations were incorrectly marked for parallel execution.
- Rollback behavior was not selected deliberately.
- A response from one sub-request was used before it existed.
- The implementation assumed all sub-requests succeeded.
Recovery:
- Classify sub-requests as independent or dependent.
- Use sequential execution for dependencies.
- Decide whether rollback is required.
- Parse every sub-response.
- Test partial and rollback outcomes.
Problem 6 — A Bulk job is treated like a synchronous API
Cause:
- The implementation expects records in the job-creation response.
- The callback or polling path was not designed.
- Downloaded result files are not parsed.
Recovery:
- Store the synthetic or real job ID.
- Poll or receive the documented callback.
- Download the result only after completion.
- Parse per-record statuses.
- Retry only failed records where safe.
- Preserve the original business key.
Problem 7 — Rerunning a failed Function creates a duplicate
Cause:
- The Function performs a write.
- No idempotency key is used.
- The failure occurred after the destination committed.
- The operator assumed failure meant no side effect.
Recovery:
- Check the destination using the business key.
- Reconcile before rerunning.
- Use upsert or a unique external ID where supported.
- Record the operator decision.
- Do not use the Function Failure rerun control as a substitute for idempotency.
Problem 8 — API credit consumption is unexpectedly high
Possible causes:
- A loop makes one call per record.
- COQL limit increases credit cost.
- Bulk initialization has a high fixed credit cost.
- Metadata is fetched repeatedly.
- An integration task is calling CRM APIs behind the scenes.
- Multiple Functions respond to the same event.
Recovery:
- Inspect the API Dashboard or Function Credits view.
- Compare estimated and observed calls.
- Remove redundant metadata calls.
- Use field selection.
- Batch operations where safe.
- Add a credit budget to the release plan.
Problem 9 — A test logs confidential data
Cause:
- The full response was printed.
- The failure fixture contains realistic personal data.
- Raw exceptions include request details.
Recovery:
- Replace fixture data with synthetic values.
- Log categories and stable test identifiers.
- Redact body and headers.
- Check serialized logs in the test output.
- Add a test that fails if a forbidden marker appears in the output.
Problem 10 — A scenario suite has no clear release decision
Cause:
- Tests were collected without acceptance criteria.
- Failures are not classified.
- Expected results are ambiguous.
- Live and local evidence are mixed.
Recovery:
- Add a release gate.
- Define blocking failures.
- Separate observed from expected.
- Record environment and version.
- Require a reviewer to approve unresolved limitations.
### Testing module — Check your understanding
 1. What does a local fake-client test prove?
 2. Why should a sandbox result not automatically be reported as a production result?
 3. What is the difference between a retryable and an uncertain timeout?
 4. Why is an API credit budget separate from a concurrency budget?
 5. What is the purpose of a performance budget?
 6. When is COQL preferable to Search Records?
 7. When is Bulk Read preferable to Get Records?
 8. Why should dependent Composite sub-requests not run in parallel?
 9. What does the Function Failures view provide?
10. Why is rerunning a failed Function not automatically safe?
11. What should an implementation do after a possible destination commit followed by a timeout?
12. What does the CRM Search API limit imply for large search results?
13. Why should a Function fetch only required fields?
14. What evidence should accompany a release decision?
15. What does the local lab claim about live Zoho requests?
### Testing module — Solutions and explanations
Guided practice solution
A valid solution:
- Validates the event envelope before making any request.
- Rejects numeric IDs.
- Preserves Event_Key exactly.
- Suppresses a duplicate after a recorded delivery.
- Marks a timeout before commit as retryable.
- Marks a timeout after possible commit as uncertain.
- Blocks authorization failures until an operator reauthorizes.
- Treats quota exhaustion as retryable with bounded delay.
- Measures Function execution against the category timeout.
- Measures response size against the platform limit.
- Keeps concurrency below the selected test budget.
- Uses explicit API credit estimates.
- Records local evidence separately from tenant evidence.
The prepared harness passed:
26 local scenario and budget cases for this chapter passed. No Zoho requests made.
This result covers the local scenario simulator and performance-budget checks only.
Independent challenge solution
A strong test plan contains:
 1. Pure validation tests.
 2. Fake dependency tests.
 3. Response-shape contract tests.
 4. Failure classification tests.
 5. Duplicate and idempotency tests.
 6. Performance-budget tests.
 7. Sandbox installation and Function tests.
 8. Connector authorization tests.
 9. Upgrade tests.
10. Evidence review and release gates.
A release should be blocked when:
- The event key is not deterministic.
- A timeout after possible commit is blindly retried.
- A raw CRM response is exposed.
- A secret appears in source or logs.
- Required fields are not available.
- The Function exceeds its interactive timeout.
- The organization or environment is not verified.
- A critical failure has no recovery owner.
- The extension upgrade changes data semantics without migration.
- The observed result cannot be tied to a tested version.
Check-your-understanding answers
 1. It proves local code behavior against the supplied fixtures and fake dependencies.
 2. Sandbox data, permissions, configuration, and deployment state can differ from production.
 3. A retryable timeout is believed to have occurred before the destination committed; an uncertain timeout may have occurred after the destination committed, so reconciliation is required.
 4. Credits measure consumption; concurrency measures simultaneous active work. Either can fail independently.
 5. It defines a measurable engineering target for a specific component and release.
 6. COQL is preferable for structured queries, joins, aggregates, and controlled field selection across linked modules.
 7. Bulk Read is preferable for large asynchronous exports where immediate results are unnecessary.
 8. A dependent request needs the result of an earlier request; parallel execution can run it before the required data exists.
 9. It provides failed Function executions and diagnostic context, and may provide rerun actions.
10. A failed execution may have committed a side effect before failing or timing out.
11. Mark it uncertain and reconcile using the business key before issuing another write.
12. A Search API call returns at most 200 records and the documented search result is limited to 2,000 records.
13. It reduces response size, data exposure, processing time, and unnecessary API cost.
14. It should include scenario results, version, environment, expected and observed values, unresolved limitations, and reviewer ownership.
15. The local lab made no Zoho requests.
### Testing module — Chapter recap and next step
This chapter established testing and performance as part of integration design.
You learned that:
- Tests are evidence records, not merely pass/fail commands.
- Local, sandbox, tenant, and production evidence must remain distinct.
- Nova requires scenarios for both successful and failed behavior.
- Duplicate events require deterministic identity and suppression.
- Timeouts after a possible commit require reconciliation.
- API credits, concurrency, sub-concurrency, Function limits, and external service limits are different constraints.
- Get Records, Search Records, COQL, Composite, Bulk Read, and Bulk Write serve different workloads.
- Performance budgets are engineering targets, not universal platform guarantees.
- Function Analytics, Revisions, Logs, Failures, and Credits support operational diagnosis.
- A rerun control is not a replacement for idempotency.
- Release decisions should be tied to explicit evidence and blocking conditions.
- The local harness passed 26 synthetic cases without making live Zoho requests.
Use the evidence in this module to decide whether an extension is ready for controlled release and operational handover.
### Testing module — Glossary and further reading
Glossary
API credit
A unit consumed by a CRM API operation according to the operation’s documented credit behavior.
API concurrency
The number of API calls active simultaneously for an organization and application.
Contract test
A test that verifies the structure and meaning of a request or response exchanged between components.
Failure injection
A deliberate simulated failure used to verify error classification and recovery behavior.
Performance budget
An engineering target for latency, size, concurrency, credits, retries, or other operational resources.
Retryable
A result that may be attempted again according to a bounded retry policy.
Sub-concurrency
A narrower concurrency limit applied to selected resource-intensive APIs.
Test evidence
The record connecting a scenario, expected result, observed result, version, environment, and limitations.
Uncertain
A state where the result of a remote side effect cannot be determined safely from the response.
Unit test
A test of a small piece of logic in isolation.
Further reading
- CRM API Limits — V8 (https://www.zoho.com/crm/developer/docs/api/v8/api-limits.html)
- CRM Get Records API — V8 (https://www.zoho.com/crm/developer/docs/api/v8/get-records.html)
- CRM Search Records API — V8 (https://www.zoho.com/crm/developer/docs/api/v8/search-records.html)
- CRM Query API / COQL — V8 (https://www.zoho.com/crm/developer/docs/api/v8/COQL-Overview.html)
- CRM Composite API (https://www.zoho.com/crm/developer/docs/api/v8/composite-overview.html)
- CRM Bulk Read API (https://www.zoho.com/crm/developer/docs/api/v8/bulk-read/overview.html)
- CRM Bulk Write API (https://www.zoho.com/crm/developer/docs/api/v8/bulk-write/overview.html)
- CRM Notification APIs (https://www.zoho.com/crm/developer/docs/api/v8/notifications/overview.html)
- CRM Function Platform Limits and Quotas (https://www.zoho.com/crm/developer/docs/functions/limits-quotas.html)
- CRM Function Security (https://www.zoho.com/crm/developer/docs/functions/security.html)
- Managing CRM Functions (https://www.zoho.com/crm/developer/docs/functions/management.html)
- Testing a Zoho CRM Extension (https://www.zoho.com/developer/help/extensions/test-extension.html)
- Publishing a Zoho CRM Extension (https://www.zoho.com/developer/help/extensions/publish-extension.html)
- Zoho CRM Field Metadata API (https://www.zoho.com/crm/developer/docs/api/v8/field-meta.html)
