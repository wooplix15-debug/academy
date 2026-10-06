# OAuth and Connection Security

C02-CH12 — OAuth, Connections and Integration Security
1. Chapter Orientation
1.1 Why this chapter matters
In C02-CH11, the Nova integration learned how to call Zoho CRM REST API V8. Those requests require authentication and authorization.
An API request is not secure merely because it uses HTTPS. A secure integration must also control:
- Which application is calling.
- Which user granted access.
- Which data and operations the token permits.
- Where client secrets are stored.
- How access tokens are refreshed.
- Which data centre serves the organization.
- What happens when a token expires or is revoked.
- How credentials are removed during an incident.
Zoho uses OAuth 2.0 for CRM API authentication. OAuth allows an application to receive delegated access without collecting the user’s Zoho password.
Nova will use an OAuth connection for Creator-to-CRM requests. The connection stores authorization configuration outside the Deluge source code. A Deluge function refers to the connection by name rather than embedding a token.
1.2 Learning outcomes
By the end of this chapter, you should be able to:
 1. Explain the roles in an OAuth 2.0 flow.
 2. Distinguish a client ID, client secret, authorization code, access token and refresh token.
 3. Describe the server-based authorization code flow.
 4. Explain why authorization codes and access tokens have different lifetimes.
 5. Request only the scopes required by a Nova integration.
 6. State the difference between CRM API domains and Accounts authorization-server domains.
 7. Design a secure Creator connection without placing tokens in Deluge source.
 8. Refresh an expired access token without asking the user to authorize again.
 9. Revoke a compromised or retired token.
10. Design a credential rotation and incident response procedure.
11. Diagnose common OAuth errors without logging secrets.
12. Create an OAuth security register and connection test plan.
1.3 Prerequisites
You should already understand:
- CRM API V8 endpoint structure.
- CRM module and field API names.
- API scopes from C02-CH11.
- Deluge invokeurl.
- Creator-to-CRM source-of-truth boundaries.
- Correlation keys and safe diagnostics from C02-CH10.
This chapter assumes a server-side or managed-platform integration. It does not teach how to build a browser application that stores OAuth tokens in JavaScript.
2. Nova’s Security Boundary
2.1 Authentication and authorization
These terms answer different questions:
Question	Concept
Who is the calling application?	Client registration
Who granted access?	Resource owner consent
Can the application call this CRM endpoint?	OAuth scope
Can the CRM user perform this operation?	CRM profile, role and sharing permissions
Is the token still valid?	Access-token lifetime
Can a new access token be issued?	Refresh token validity
Can the application safely keep using the credential?	Secret storage and rotation
A successful OAuth token exchange does not guarantee a successful CRM request. The token may lack the required scope, or the CRM user may lack module permission.
2.2 Nova security boundary
flowchart LR
    U[CRM Administrator or Owner] --> C[OAuth Consent]
    C --> A[Zoho Authorization Server]
    A --> T[Access and Refresh Tokens]
    T --> K[Managed Connection]
    K --> D[Creator Deluge Function]
    D --> R[CRM API V8]
    R --> P[CRM Profiles and Sharing]
Nova’s application code should know:
- The connection name.
- The API resource it intends to call.
- The expected response shape.
- The correlation key.
Nova’s application code should not know:
- The client secret.
- The refresh token.
- A long-lived access token.
- A user password.
- A secret copied from an administrator’s browser.
2.3 Responsibility matrix
Security responsibility	Owner
Register OAuth client	Nova technical owner
Approve requested scopes	CRM administrator and data owner
Configure redirect URI	OAuth client owner
Create Creator connection	Creator application administrator
Store connection secrets	Zoho-managed connection configuration
Control CRM profile permissions	CRM administrator
Review access logs	Integration owner
Rotate or revoke credentials	OAuth client owner
Approve production promotion	Nova service manager
Remove a compromised connection	Technical owner and administrator
2.4 Environment separation
Use separate OAuth clients or credentials for:
Environment	Recommended credential policy
Development	Synthetic CRM data and development client
UAT	UAT client and approved test data
Production	Production client, restricted owners and production scopes
Do not move a development refresh token into production. Do not use a production OAuth client in a developer’s personal collection.
3. OAuth 2.0 Concepts
3.1 Protected resource
The protected resource is the Zoho CRM data and metadata that the application wants to access.
Examples:
- Contacts.
- Accounts.
- Module metadata.
- Field metadata.
- Attachments.
3.2 Resource owner
The resource owner is the Zoho user or organization administrator who grants consent for the client to access authorized resources.
For Nova, consent should be granted by an approved CRM administrator or integration owner, not by a technician using a personal account.
3.3 Client
The client is the application requesting access.
Possible client types include:
- Server-based application.
- Client-based application.
- Mobile application.
- Non-browser application.
- Self client.
The Nova Creator integration uses a managed server-side connection. The OAuth client secret must remain outside student-facing browser code and source files.
3.4 Client ID and client secret
When an application is registered in the Zoho API Console, it receives:
client_id
client_secret
The client ID identifies the application. The client secret authenticates the confidential application during server-side token exchange.
The client secret is not a user password and must not be sent to the CRM resource endpoint.
3.5 Authorization code
The authorization code is:
- Returned after the user grants consent.
- Sent to the configured redirect URI.
- Temporary.
- Valid for two minutes according to the official server-based OAuth documentation.
- Usable only once.
The application exchanges it for an access token and, when requesting offline access, a refresh token.
3.6 Access token
The access token is sent with CRM API requests.
The official Zoho OAuth documentation states that:
- The access token is valid for one hour.
- The token is limited to the scopes requested.
- The token must be kept confidential.
- The token is used as a bearer credential.
CRM V8 endpoint examples use this header form:
Authorization: Zoho-oauthtoken {access_token}
The general Zoho OAuth response identifies the token type as Bearer. Follow the authorization-header format required by the specific Zoho API documentation and managed connection client being used. Do not invent a different header prefix.
3.7 Refresh token
A refresh token is used to request a new access token after the access token expires.
The refresh token:
- Is issued when the authorization request uses access_type=offline.
- Can be used without asking the user to consent each hour.
- Remains valid until revoked according to the CRM OAuth overview.
- Must be stored as a high-value secret.
- Must not be sent to the CRM records endpoint.
The refresh-token flow returns a new access token and the API domain. Store or use the returned API domain for later resource calls.
4. Authorization Code Flow
4.1 Flow overview
sequenceDiagram
    participant N as Nova/Connection Setup
    participant A as Zoho Accounts
    participant U as Authorizing User
    participant C as Zoho CRM API

    N->>A: Authorization request with client_id and scopes
    A->>U: Consent screen
    U-->>A: Approve
    A-->>N: One-time authorization code
    N->>A: Exchange code for tokens
    A-->>N: Access token, refresh token and api_domain
    N->>C: CRM request with access token
    C-->>N: CRM response
4.2 Step 1: Register the application
Register the client in the Zoho API Console.
For a server-based application, record:
client_type: "server-based"
application_name: "Nova Field Service CRM Integration"
homepage_url: "https://integration.example.com"
redirect_uri: "https://integration.example.com/oauth/callback"
environment: "development"
owner: "nova-integration-team"
The authorized redirect URI must match the URI registered in the API Console. A difference in:
- Scheme.
- Host.
- Path.
- Port.
- Trailing slash.
can cause an invalid redirect URI error.
Use HTTPS for real environments. A local development redirect may use an approved local URI if the client configuration permits it.
4.3 Step 2: Request authorization
The server-based authorization endpoint is:
GET {accounts-server-url}/oauth/v2/auth
The Accounts server URL is data-centre-specific.
Example with placeholders:
https://accounts.zoho.com/oauth/v2/auth
  ?response_type=code
  &client_id={{client_id}}
  &scope=ZohoCRM.modules.contacts.READ,ZohoCRM.settings.fields.READ
  &redirect_uri=https%3A%2F%2Fintegration.example.com%2Foauth%2Fcallback
  &access_type=offline
  &prompt=consent
Important parameters:
Parameter	Purpose
response_type=code	Requests an authorization code
client_id	Identifies the registered client
scope	Requests delegated permissions
redirect_uri	Must match the registered URI
access_type=offline	Requests a refresh token
prompt=consent	Requests consent again when needed
The user sees the requested permissions before approving.
4.4 Step 3: Receive the authorization code
After consent, Zoho redirects to the registered URI:
https://integration.example.com/oauth/callback
  ?code={{one_time_code}}
  &location=us
  &accounts-server=https%3A%2F%2Faccounts.zoho.com
The authorization code is temporary and single-use.
The callback handler should:
1. Confirm the request arrived at the expected redirect route.
2. Read the code without logging it.
3. Read the data-centre information.
4. Exchange the code immediately.
5. Delete the code from temporary storage after exchange.
6. Return a generic success or failure page to the user.
4.5 Step 4: Exchange the code for tokens
The token endpoint is:
POST {accounts-server-url}/oauth/v2/token
Example using form-encoded data:
curl --request POST \
  --url "https://accounts.zoho.com/oauth/v2/token" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "client_id=${CLIENT_ID}" \
  --data-urlencode "client_secret=${CLIENT_SECRET}" \
  --data-urlencode "grant_type=authorization_code" \
  --data-urlencode "redirect_uri=https://integration.example.com/oauth/callback" \
  --data-urlencode "code=${AUTHORIZATION_CODE}"
Never place the client secret or authorization code in a browser URL that can be copied into history or analytics logs.
A documented token response contains values similar to:
{
  "access_token": "redacted-access-token",
  "refresh_token": "redacted-refresh-token",
  "api_domain": "https://api.zoho.com",
  "token_type": "Bearer",
  "expires_in": 3600
}
The values above are placeholders. They are not usable credentials.
4.6 Step 5: Call CRM
Use the returned API domain for the resource request:
curl --request GET \
  --url "https://api.zoho.com/crm/v8/Contacts?fields=id,Last_Name,Email&per_page=10" \
  --header "Authorization: Zoho-oauthtoken ${ACCESS_TOKEN}"
The resource API domain and Accounts authorization-server domain serve different purposes:
Domain type	Purpose
Accounts server URL	Authorize, exchange, refresh or revoke OAuth tokens
CRM API domain	Access CRM modules, records and metadata
4.7 Step 6: Refresh when required
The refresh endpoint is also:
POST {accounts-server-url}/oauth/v2/token
The request uses:
grant_type=refresh_token
refresh_token={{refresh_token}}
client_id={{client_id}}
client_secret={{client_secret}}
Example:
curl --request POST \
  --url "https://accounts.zoho.com/oauth/v2/token" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "client_id=${CLIENT_ID}" \
  --data-urlencode "client_secret=${CLIENT_SECRET}" \
  --data-urlencode "grant_type=refresh_token" \
  --data-urlencode "refresh_token=${REFRESH_TOKEN}"
The response provides:
- A new access token.
- The API domain.
- Token type.
- Expiry duration.
The refresh token is not normally returned again. Preserve the existing refresh token until it is rotated or revoked.
5. Scopes and Least Privilege
5.1 Scope structure
Zoho OAuth scopes contain three parts:
service_name.scope_name.OPERATION_TYPE
Examples:
ZohoCRM.modules.contacts.READ
ZohoCRM.modules.contacts.CREATE
ZohoCRM.settings.fields.READ
Multiple scopes are comma-separated:
ZohoCRM.modules.contacts.READ,ZohoCRM.settings.fields.READ
A scope limits the application’s delegated access. It does not grant access to data that the CRM user cannot access.
5.2 Nova scope matrix
Connection	Required purpose	Suggested scopes
crm_metadata_read_dev	Discover modules and fields	ZohoCRM.settings.modules.READ, ZohoCRM.settings.fields.READ, ZohoCRM.settings.related_lists.READ
crm_customer_lookup_dev	Find Contacts	ZohoCRM.modules.contacts.READ, ZohoSearch.securesearch.READ
crm_customer_create_dev	Create test Contacts	ZohoCRM.modules.contacts.CREATE
crm_customer_update_dev	Update approved fields	ZohoCRM.modules.contacts.UPDATE
crm_attachment_read_dev	List Contact attachments	ZohoCRM.modules.contacts.READ, ZohoCRM.modules.attachments.READ
crm_production_service	Approved production workflow	Exact combination approved by CRM administrator
Avoid starting with:
ZohoCRM.ALL
or a broad all-modules permission unless the integration has a documented reason.
5.3 Scope approval record
Create a scope approval record before production:
Field	Example
Application	Nova Field Service CRM Integration
Environment	Production
Data owner	CRM Administrator
Requested scope	ZohoCRM.modules.contacts.READ
Business reason	Resolve customer identity before Creator dispatch
Data accessed	Contact ID, name, email, phone
Write access	No
Expiry/review date	2027-01-06
Approver	Name and date
Evidence	OAuth client and connection record
5.4 Incremental authorization
Zoho supports incremental authorization. This allows an application to request additional permission when a feature needs it rather than requesting every possible scope on the first consent screen.
For Nova:
1. Start with Contacts read and metadata read.
2. Add Contacts create only when customer creation is approved.
3. Add Contacts update only when update ownership is approved.
4. Add attachment scope only when attachment access is required.
5. Review whether the new scope is still needed after the feature is complete.
6. Managed Connections and Deluge
6.1 Why use a connection
A managed connection gives the Deluge function a named authorization configuration.
The function can refer to:
crm_oauth_connection
instead of embedding:
- Client ID.
- Client secret.
- Refresh token.
- Access token.
A connection also provides a central place to:
- Reauthorize.
- Review scopes.
- Change the owner.
- Revoke access.
- Separate development and production credentials.
6.2 Deluge request pattern
A CRM read using a named connection can follow this pattern:
crm_response = invokeurl
[
    url: "https://www.zohoapis.com/crm/v8/Contacts/search?email=maya.rivera%40example.com"
    type: GET
    connection: "crm_oauth_connection"
];

info crm_response;
The connection name is configuration. It is not a secret.
A production function should not log the full response if it may contain customer data. Instead, classify and record a safe summary:
safe_summary = Map();
safe_summary.put("http_status", "not_available_in_this_example");
safe_summary.put("response_type", crm_response.get("status"));
safe_summary.put("correlation_key", "C02-CH12-NOV-REQ-001");
info safe_summary;
The exact response-inspection code depends on the host context and the response returned by the connection invocation.
6.3 Connection naming convention
Use names that expose purpose and environment:
crm_oauth_customer_lookup_dev
crm_oauth_customer_write_uat
crm_oauth_customer_prod
Avoid vague names:
my_connection
test
zoho
new_connection
A clear name reduces the risk of using a production credential from a development function.
6.4 Connection configuration record
connection_name: "crm_oauth_customer_lookup_dev"
service: "Zoho CRM"
environment: "development"
oauth_client: "Nova Field Service Development"
accounts_server_dc: "organization-specific"
api_domain: "organization-specific"
crm_api_version: "v8"
scopes:
  - "ZohoCRM.modules.contacts.READ"
  - "ZohoSearch.securesearch.READ"
owner: "Nova integration team"
secret_storage: "managed connection configuration"
token_logging: false
rotation_owner: "Nova technical owner"
review_frequency: "quarterly"
6.5 Never pass tokens through application records
Do not store access or refresh tokens in:
- Creator form fields.
- CRM Contact fields.
- A configuration form visible to end users.
- A report.
- A public page.
- A URL parameter.
- A debug message.
Application records may store:
connection_name
environment
scope_summary
last_successful_call_at
last_refresh_at
credential_review_at
They should not store the token value.
7. Secret Handling, Rotation and Data Protection
7.1 Secret classification
Credential	Classification	Storage
Client ID	Sensitive configuration	Managed configuration
Client secret	High-value secret	Secret manager or managed OAuth client
Authorization code	Temporary secret	Memory or short-lived protected storage
Access token	Short-lived secret	Managed connection or protected runtime
Refresh token	Long-lived high-value secret	Managed connection or secret manager
CRM record ID	Business integration data	Creator integration fields
Customer email	Customer data	Approved application records
7.2 Secret handling rules
 1. Do not commit secrets.
 2. Do not print secrets in info statements.
 3. Do not include tokens in screenshots.
 4. Do not paste tokens into support tickets.
 5. Do not send refresh tokens to a browser.
 6. Do not store client secrets in client-side JavaScript.
 7. Do not share one production connection across unrelated applications.
 8. Do not use a production credential to test an unreviewed collection.
 9. Remove expired credentials from local environments.
10. Revoke credentials that may have been exposed.
7.3 Rotation procedure
A planned rotation should follow this order:
create or register replacement credential
→ configure replacement connection
→ test read-only operation
→ test approved write in UAT
→ promote replacement connection
→ monitor successful calls
→ revoke old credential
→ remove old secret from local stores
→ update security register
Do not revoke the old token before the replacement connection has been tested unless an incident requires immediate revocation.
7.4 Incident response
If a refresh token or client secret may be exposed:
 1. Stop using the affected connection.
 2. Record the incident time and affected environment.
 3. Revoke the refresh token or connected application access.
 4. Rotate the client secret if the client credentials may be exposed.
 5. Inspect recent CRM activity and integration logs.
 6. Identify data and operations permitted by the scopes.
 7. Create a replacement connection with the minimum scope set.
 8. Test the replacement in a non-production environment.
 9. Restore production traffic under monitoring.
10. Record the incident and remediation evidence.
Do not include the exposed token in the incident record.
7.5 Revocation
A user can revoke access through Connected Apps in Zoho Accounts.
A token can also be revoked programmatically:
POST {accounts-server-url}/oauth/v2/revoke/token
The request uses the app credentials and the token to revoke:
curl --request POST \
  --url "https://accounts.zoho.com/oauth/v2/revoke/token" \
  --user "${CLIENT_ID}:${CLIENT_SECRET}" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "token=${REFRESH_TOKEN}" \
  --data-urlencode "token_type=refresh_token"
The exact authorization encoding must follow the current Zoho OAuth documentation. A refresh-token revocation invalidates access tokens generated from that refresh token.
7.6 Safe diagnostic record
correlation_key: "C02-CH12-NOV-REQ-001"
environment: "development"
connection_name: "crm_oauth_customer_lookup_dev"
request_name: "search_customer_by_email"
crm_api_version: "v8"
scope_class: "contacts-read"
token_value_logged: false
refresh_token_logged: false
http_status: 401
response_code: "OAUTH_SCOPE_MISMATCH"
retryable: false
next_action: "Repair connection scope and reauthorize"
This record supports troubleshooting without exposing credentials.
8. Data Centres and OAuth Errors
8.1 Data-centre routing
Zoho maintains multiple data centres. The authorization server URL is specific to the organization or user location.
The authorization response can include:
location
accounts-server
The token response includes:
{
  "api_domain": "https://api.zoho.com"
}
Treat the returned api_domain as configuration associated with the token.
Do not assume that an Accounts URL from one data centre can be used for every organization.
8.2 Common data-centre failure
A token request can fail with invalid_client when:
- The Accounts server URL does not match the user’s data centre.
- The client ID is invalid.
- The grant type is wrong.
A resource request can fail when the caller uses an API domain that does not serve the organization.
Recovery:
1. Inspect the location returned during authorization.
2. Use the corresponding Accounts server URL for token exchange.
3. Store the returned CRM API domain.
4. Reauthorize if the client is not enabled for the required data centre.
5. Do not try random regional domains.
8.3 OAuth error table
Error	Likely cause	Recovery
access_denied	User rejected consent	Explain required access and retry only with approval
Invalid client	Wrong client ID or Accounts server	Verify client registration and data centre
Invalid client secret	Wrong or rotated secret	Retrieve the current secret securely
Invalid OAuth scope	Scope missing or misspelled	Compare with official API scope
Invalid redirect URI	URI differs from registration	Make the URI identical
Invalid code	Code expired or already used	Start a new authorization request
OAUTH_SCOPE_MISMATCH	CRM token lacks endpoint scope	Reauthorize with required scope
AUTHENTICATION_FAILURE	Access token invalid or expired	Refresh through the connection
NO_PERMISSION	CRM user cannot access data	Repair CRM role/profile/sharing
Invalid token	Refresh token revoked or malformed	Reauthorize and replace connection
TOO_MANY_REQUESTS	Resource concurrency limit reached	Backoff and reduce concurrency
8.4 Token lifecycle state machine
stateDiagram-v2
    [*] --> NotAuthorized
    NotAuthorized --> Authorized: user grants consent
    Authorized --> AccessTokenActive: exchange code
    AccessTokenActive --> AccessTokenActive: CRM request
    AccessTokenActive --> RefreshRequired: access token expires
    RefreshRequired --> AccessTokenActive: refresh succeeds
    RefreshRequired --> ReauthorizationRequired: refresh revoked or invalid
    AccessTokenActive --> ReauthorizationRequired: token revoked
    ReauthorizationRequired --> Authorized: consent again
    Authorized --> Revoked: administrator revokes
    Revoked --> NotAuthorized
8.5 No blind retry for authorization errors
A 401 or invalid refresh-token response is not a network failure.
Do not:
retry the same request indefinitely
Instead:
classify
→ stop protected requests
→ notify connection owner
→ reauthorize or repair scopes
→ test with a non-destructive request
→ resume queued work
9. Guided Practice — Create a Secure OAuth Connection Plan
9.1 Scenario
The Nova development team needs to resolve Contacts before creating Creator Jobs.
The first release requires:
- Read Contacts.
- Search Contacts by email.
- Read module and field metadata.
- No CRM writes.
- No attachment access.
- No access to Deals, Invoices or other modules.
The team must create a secure connection plan without exposing a token.
9.2 Connection plan artifact
Create this file:
C02-CH12_Nova_OAuth_Connection_Register_v0.1.md
Use this table:
Field	Required value
Application name	Nova Field Service CRM Integration
Client type	Server-based or managed platform connection
Environment	Development
OAuth version	OAuth 2.0
CRM API version	V8
Accounts server	Data-centre-specific
CRM API domain	Returned by token response or approved environment configuration
Redirect URI	Exact registered URI
Scopes	Contacts read, secure search read, required metadata read
Client secret storage	Managed OAuth configuration
Access-token logging	Prohibited
Refresh-token logging	Prohibited
CRM writes	Not requested
Attachments	Not requested
Owner	Nova technical owner
Review date	90 days from approval
Revocation owner	Nova technical owner and CRM administrator
9.3 Authorization checklist
Before requesting consent:
- The application is registered in the correct API Console.
- The client type matches the integration.
- The redirect URI exactly matches the registered URI.
- The requested scope list contains only required permissions.
- The Accounts server matches the organization’s data centre.
- The authorization request uses response_type=code.
- Offline access is requested only when refresh is required.
- The authorization code will be exchanged immediately.
- Tokens will not be written to logs.
- The CRM user has the required module permissions.
9.4 Connection smoke-test sequence
The connection owner should run these tests in order:
1. Read module metadata.
2. Read field metadata for Contacts.
3. Search for nova-api-test@example.com.
4. Confirm that a write request is rejected or unavailable because write scope was not granted.
5. Wait for or simulate access-token expiry using the managed connection’s refresh behavior.
6. Confirm that a refreshed access token can perform the same read.
7. Revoke the development credential.
8. Confirm that protected calls stop working.
9. Create a replacement connection only after the revocation test is recorded.
9.5 Expected observations
Test	Expected observation
Module metadata	Successful response if metadata read scope and CRM permission exist
Field metadata	Successful response for Contacts
Customer search	Successful response or documented no-match response
Create request	Scope mismatch or unavailable operation because create scope was not requested
Token refresh	New access token with expiry information
Revoked token	Authentication or invalid-token failure
Replacement connection	Read succeeds after reauthorization
9.6 Practice questions
1. Why is a refresh token more sensitive than a short-lived access token?
2. Why should the API domain be stored with the token configuration?
3. Why does a token with Contacts read scope fail when used for Contacts create?
4. Why should the application request metadata read scope separately from Contacts read scope?
5. Why should production and development use different connections?
6. Which value must match exactly during code exchange?
7. What should the application do when a refresh token has been revoked?
10. Independent Practice — Security Design and Solutions
10.1 Independent challenge
The Nova team proposes this design:
- Put the refresh token in a Creator form called Integration_Settings.
- Let Dispatchers view the form.
- Use ZohoCRM.ALL for every environment.
- Print the access token when a CRM call fails.
- Use the .com Accounts server for every customer organization.
- Store the CRM API domain as a hardcoded constant.
- Use one OAuth client for development and production.
Identify each security problem and write a replacement design.
10.2 Solution table
Proposed design	Problem	Replacement
Refresh token in Creator form	End users may view or export it	Store it in a managed connection or approved secret store
Dispatchers can view token configuration	Operational users do not need credential access	Restrict configuration administration
ZohoCRM.ALL everywhere	Excessive delegated permission	Request module and operation-specific scopes
Print access token on failure	Logs become credential exposure	Log status, code, correlation key and sanitized details
.com Accounts server for every organization	Data centre may differ	Use organization-specific Accounts server and returned location
Hardcoded API domain	Token may return a different resource domain	Store or use the api_domain returned by OAuth
One client for all environments	Test compromise can affect production	Separate clients and connections
Immediate blind retry after token failure	Can create loops and hide credential incidents	Stop, classify, repair or reauthorize
10.3 Completed Nova security design
application:
  name: "Nova Field Service CRM Integration"
  environments:
    development:
      oauth_client: "Nova CRM Development"
      connection: "crm_oauth_customer_lookup_dev"
      data: "synthetic example.com records"
      scopes:
        - "ZohoCRM.settings.modules.READ"
        - "ZohoCRM.settings.fields.READ"
        - "ZohoCRM.modules.contacts.READ"
        - "ZohoSearch.securesearch.READ"
    production:
      oauth_client: "Nova CRM Production"
      connection: "crm_oauth_customer_prod"
      data: "approved production customer data"
      scopes:
        - "ZohoCRM.modules.contacts.READ"
        - "ZohoSearch.securesearch.READ"
      approval: "CRM administrator and service owner"
oauth:
  flow: "authorization_code"
  access_type: "offline"
  access_token_lifetime: "3600 seconds"
  authorization_code_lifetime: "2 minutes"
  refresh_token_storage: "managed connection"
  client_secret_storage: "managed OAuth configuration"
  token_logging: false
  code_logging: false
routing:
  accounts_server: "resolve from organization data centre"
  crm_api_domain: "use returned api_domain"
  crm_api_version: "v8"
operations:
  write_scope: "not granted to lookup-only connection"
  attachment_scope: "not granted unless feature is approved"
  retry_authentication_errors: false
  reconcile_unknown_writes: true
monitoring:
  log:
    - "connection name"
    - "environment"
    - "scope class"
    - "correlation key"
    - "sanitized error code"
    - "timestamp"
  never_log:
    - "client_secret"
    - "authorization_code"
    - "access_token"
    - "refresh_token"
10.4 Secure failure-handling pseudocode
function callCrmWithConnection(request, connectionName):
    correlationKey = createCorrelationKey()
    response = invokeUsingManagedConnection(request, connectionName)

    if response indicates success:
        writeSafeAudit(correlationKey, "success")
        return response

    if response indicates authentication failure:
        pause protected work
        writeSafeAudit(correlationKey, "authentication_failure")
        notify connection owner
        return "REAUTHORIZATION_REQUIRED"

    if response indicates scope mismatch:
        do not retry
        writeSafeAudit(correlationKey, "scope_mismatch")
        return "CONFIGURATION_ERROR"

    if response indicates permission failure:
        do not retry
        writeSafeAudit(correlationKey, "crm_permission_failure")
        return "ACCESS_REVIEW_REQUIRED"

    if response indicates transient server or concurrency failure:
        retry with bounded backoff
        if retry limit reached:
            queue for reconciliation
        return result

    if response indicates invalid data:
        do not retry unchanged
        return "MAPPING_ERROR"
10.5 Security review rubric
Area	Meets expectation when
OAuth flow	Authorization code and token exchange are distinguished
Client registration	Redirect URI and environment are recorded
Scopes	Least-privilege permissions are explicit
Token storage	No token is placed in application data or source code
Data centres	Accounts server and CRM API domain are not assumed globally
Refresh	Access-token expiry is handled through the connection
Revocation	A revocation procedure exists
Rotation	Replacement credential can be deployed before old credential removal
Diagnostics	Logs exclude secrets
Environment isolation	Development and production credentials are separate
Failure response	Authentication errors stop protected work rather than retrying forever
11. Checks, Recap and Glossary
11.1 Knowledge check
Question 1
Which OAuth value identifies the registered application?
Question 2
Which OAuth value is exchanged for an access token and is valid for only a short period?
Question 3
What does access_type=offline request?
Question 4
How long is a Zoho OAuth access token documented as valid?
Question 5
Why should the application use the api_domain returned in the token response?
Question 6
A developer receives invalid_redirect_uri. What should be checked first?
Question 7
Should the refresh token be stored in a Creator form visible to Dispatchers?
Question 8
What should happen after a refresh token is revoked?
Question 9
A CRM request returns OAUTH_SCOPE_MISMATCH. Is retrying the same request likely to fix it?
Question 10
Which system owns Job_Status in the Nova baseline?
11.2 Answers
Answer 1
The client_id.
Answer 2
The authorization code. It is exchanged at the OAuth token endpoint and is valid for two minutes according to the official server-based OAuth documentation.
Answer 3
It requests a refresh token so the application can obtain new access tokens without requiring the user to authorize every hour.
Answer 4
One hour, or 3,600 seconds.
Answer 5
The API domain can depend on the user’s data centre. Using the returned domain avoids routing a token to the wrong regional resource server.
Answer 6
Check that the redirect_uri in the authorization request and token exchange exactly matches the URI registered in the API Console.
Answer 7
No. It should be stored in a managed connection or approved secret store with restricted administrative access.
Answer 8
Stop protected requests, notify the connection owner and complete a new authorization flow. Do not repeatedly retry the revoked token.
Answer 9
No. The connection must be reauthorized with the required scope, and CRM user permissions must also be checked.
Answer 10
Creator owns Job_Status. It is an operational workflow state.
11.3 Chapter recap
A secure Nova OAuth integration follows this sequence:
register separate client
→ configure exact redirect URI
→ request minimum scopes
→ receive one-time authorization code
→ exchange code server-side
→ store refresh token in managed connection
→ use returned API domain
→ call CRM with short-lived access token
→ refresh through the connection
→ classify authentication and permission failures
→ rotate or revoke credentials when required
Remember:
 1. OAuth is delegated access, not password sharing.
 2. Client secrets and refresh tokens are high-value secrets.
 3. Authorization codes are temporary and single-use.
 4. Access tokens expire and are scope-limited.
 5. A refresh token must never be sent to a CRM record endpoint.
 6. The redirect URI must match exactly.
 7. Scopes should be narrow and feature-specific.
 8. CRM permissions still apply after OAuth consent.
 9. Data-centre routing must be explicit.
10. Managed connections keep credentials out of Deluge source.
11. Authentication errors require repair or reauthorization, not infinite retries.
12. Revocation and rotation are normal lifecycle operations.
11.4 Glossary
Term	Meaning
Access token	Short-lived token used to call protected APIs
Accounts server	Zoho authorization server for a data centre
Authorization code	Temporary one-time value exchanged for tokens
Client	Application requesting delegated access
Client ID	Identifier for a registered OAuth application
Client secret	Confidential credential for a server-based client
Consent	User approval of requested OAuth scopes
Data centre	Regional location that serves an organization’s data
Delegated access	Access granted by a user to an application
Grant type	OAuth exchange type such as authorization_code or refresh_token
Managed connection	Platform configuration that stores and applies authorization for a service call
OAuth	Protocol for delegated access to protected resources
PKCE	Proof Key for Code Exchange, used to protect public-client authorization flows
Refresh token	Long-lived token used to obtain new access tokens
Redirect URI	Registered callback URI receiving the authorization response
Resource owner	User who grants access to protected resources
Scope	Permission describing allowed service, resource and operation
Token revocation	Action that invalidates a token
api_domain	Resource API domain returned with the OAuth token
access_type=offline	Authorization parameter used to request refresh capability
11.5 Further reading
Official documentation used for this chapter:
- Zoho CRM API V8 — OAuth 2.0 Overview (https://www.zoho.com/crm/developer/docs/api/v8/oauth-overview.html)
- Zoho OAuth 2.0 Introduction (https://www.zoho.com/accounts/protocol/oauth.html)
- Zoho OAuth Client Registration (https://www.zoho.com/accounts/protocol/oauth-setup.html)
- Server-Based OAuth Applications (https://www.zoho.com/accounts/protocol/oauth/web-server-applications.html)
- Get Authorization Code (https://www.zoho.com/accounts/protocol/oauth/web-apps/authorization.html)
- Get Access Token (https://www.zoho.com/accounts/protocol/oauth/web-apps/access-token.html)
- Refresh Access Token (https://www.zoho.com/accounts/protocol/oauth/web-apps/access-token-expiry.html)
- OAuth Scopes (https://www.zoho.com/accounts/protocol/oauth/scope.html)
- OAuth Multi-DC Support (https://www.zoho.com/accounts/protocol/oauth/multi-dc.html)
- Revoke OAuth Tokens (https://www.zoho.com/accounts/protocol/oauth/revoke-refresh-token.html)
- Mobile and Desktop OAuth with PKCE (https://www.zoho.com/accounts/protocol/oauth/mobile-applications.html#pkce)
