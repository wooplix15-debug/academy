# Controlled Business-System Actions

C03-CH14 — Controlled Business-System Actions
1. What you will learn
An assistant that only answers questions can usually be corrected by asking a better question. An assistant that changes a CRM record, updates a support ticket, creates an invoice, or sends a message can create a business event that is harder to reverse. This chapter shows how to put a controlled boundary around that kind of action.
You will learn to:
- distinguish a read, a proposed change, an approval and a committed change;
- design a narrow adapter for CRM, Desk, Books or Creator without pretending that all four products have the same API;
- create a change preview that names the target, identity, current version, proposed result and side effects;
- enforce tenant, role and owner checks in application code;
- require a separate human approval and re-read the record before committing;
- use record versions, conditional requests and conflict stops to reduce time-of-check/time-of-use errors;
- record an audit event and a receipt that can be correlated to the original action; and
- prevent a retry from applying the same logical action twice.
The Northstar project contribution is a human-reviewed CRM update with replay protection. In this chapter, Mira is allowed to propose a note for customer NST-CUST-001. Len, a Sales Manager, must approve it. The exercise uses an isolated local SQLite store. It does not call a live CRM or send a message.
You should already understand JSON, API requests, tool contracts, workflow state and permission boundaries. Chapters 9–13 supplied those foundations. The next chapter will use the evidence produced here in a reproducible evaluation dataset.
2. Lessons
2.1 A business-system action has a larger boundary than an API call
An API request is only one part of an action. A safe application must know who asked, which tenant and record are in scope, what exact operation is proposed, whether the operation is permitted, whether a person approved this exact proposal and whether the record is still current.
For Northstar, a controlled action envelope can look like this:
{
  "action_id": "NST-ACTION-LAB-AC01",
  "tenant_id": "NST-TENANT-001",
  "actor": {"user_id": "NST-USER-001", "role": "Sales Representative"},
  "operation": "append_internal_note",
  "target": {"logical_customer_id": "NST-CUST-001", "provider_record_id": null},
  "requested_change": "Follow up on invoice date and route opened-carton request to Sales Manager.",
  "mode": "preview",
  "expected_record_version": "r7",
  "approval_required": true
}
logical_customer_id is the business identifier used by Northstar. provider_record_id is the identifier required by a particular provider. Keep them separate: a CRM record ID, a Desk ticket ID and a Creator record ID are not interchangeable.
The four systems in this course have different business purposes:
System	Example target	Typical risk	Adapter question
CRM	Customer, contact, deal or note	Wrong customer or unintended workflow	Which permitted record ID and module field are being changed?
Desk	Ticket, comment or status	Customer-facing support commitment	Is this an internal note or a public reply?
Books	Invoice, bill or payment-related record	Financial or accounting consequence	Does this require a stronger approval and reconciliation step?
Creator	Custom form or application record	Organization-specific validation	Which app, report, form and field rules apply?
An adapter should expose a small, product-specific interface such as get_current, make_preview, commit_if_current and map_error. The policy layer calls that interface; it does not construct arbitrary provider requests from model-generated text.
2.2 Draft is not commit
Use separate states. A draft is a description of a possible change. A commit is an external side effect.
NEW
  │ authenticated request + authorization
  ▼
PREVIEW_READY ── reject ──► STOP_REJECTED
  │ approval of this exact preview
  │ fresh read + version check
  ├─ changed ─────────────► STOP_STALE
  ├─ hash differs ─────────► DRAFT_CHANGED
  └─ valid commit ─────────► COMMITTED
                                  │ same action and same hash
                                  └────────► REPLAYED
The assistant response and the action receipt should use different fields. In the Northstar response contract, execution_status: "draft_only" means the assistant has not performed a live provider write. The local action receipt can separately contain action_status: "committed" because the offline fixture committed to its own test store. This distinction prevents a local test result from being presented as a CRM update.
A prompt instruction such as “ask for approval before writing” is useful guidance, but it is not an enforcement mechanism. The commit function must reject a request with no valid approval, even if the model says that approval happened.
2.3 Integrations need provider-specific evidence
The Zoho CRM v8 Update Records documentation describes PUT endpoints for a module or a specific record, requires the record ID for a specific update, and lists module-specific UPDATE or WRITE scopes. It also documents If-Unmodified-Since and a 412 ALREADY_MODIFIED response when the record has changed since the supplied time. The application still has to map its logical customer to the correct CRM module and record ID, and it has to verify the actual field and permission configuration.
The safe sequence is therefore:
1. Read the permitted record and its provider version or modification marker.
2. Construct a narrow, typed change using provider field API names.
3. Obtain approval for that exact change.
4. Read again immediately before the write.
5. Use the provider’s documented conditional mechanism when available.
6. Treat a conflict, permission error or ambiguous response as a stop requiring diagnosis.
The CRM Update Records documentation also distinguishes operation scopes such as UPDATE and WRITE, and documents provider errors including NO_PERMISSION, OAUTH_SCOPE_MISMATCH and ALREADY_MODIFIED.
Do not substitute an upsert merely because it is convenient. An upsert can create a record when no duplicate is found, while an exact note action normally intends to affect one existing record. Use an explicit update when the target must already exist. If a product has no documented conditional write or idempotency facility, maintain an application-side action ledger and use a conservative reconciliation process; do not claim that a normal HTTP retry is safe.
Desk, Books and Creator need the same boundary but different adapters. For example, a Desk adapter must distinguish an internal ticket note from a public response. A Books adapter should treat invoice or payment changes as financially consequential and apply the organization’s approval policy. A Creator adapter must identify the correct application, form or report and honor its field validation. The exact endpoint, OAuth scope and side-effect behavior must be checked against the current product documentation and tenant configuration before deployment.
2.4 Human approval is an identity and policy decision
Approval is not merely a second model response. The application should obtain the reviewer identity from the authenticated session or trusted gateway context. It should not accept a user ID supplied as ordinary model arguments.
For this chapter, the approval policy is:
- the actor and reviewer belong to the same tenant;
- the actor is authorized for the target record;
- the reviewer has the Sales Manager role;
- the reviewer is not the actor;
- the reviewer approves the stored preview hash, not a paraphrase of it; and
- the approval is within the preview’s expiry period.
These rules implement separation of duties for the example. A real organization may allow self-approval for low-risk operations, but that must be an explicit policy decision enforced in code. A role label from an untrusted request is not proof of a role; resolve it from the application’s authorization source.
2.5 A preview makes the proposed effect inspectable
A useful preview answers six questions:
1. Who requested this action, and in which tenant?
2. What exact record will be affected?
3. What operation and fields will change?
4. What are the before and after values or versions?
5. What side effects could occur?
6. What must the reviewer approve?
Example:
{
  "action_id": "NST-ACTION-LAB-AC01",
  "target": {"customer_id": "NST-CUST-001", "tenant_id": "NST-TENANT-001"},
  "change": {
    "operation": "append_internal_note",
    "note_text": "Follow up on invoice date and route opened-carton request to Sales Manager.",
    "record_version_before": "r7",
    "record_version_after": "r8"
  },
  "before": {"record_version": "r7", "notes_count": 0},
  "after": {"record_version": "r8", "notes_count": 1},
  "approval_required": true,
  "action_status": "preview_only",
  "preview_sha256": "ffcd177d0ed91fdbb7a64836c9ab513946ebd8204fd5d7f724466354454a676a"
}
The hash is a compact integrity check over the canonical preview. It is not a substitute for authorization, a record version or a signature. It ensures that the approval refers to the stored proposal rather than a later or altered proposal.
A preview can expire. It does not reserve the provider record. Another user may update the customer after the preview, so the commit path must revalidate.
2.6 Revalidation prevents stale writes, but only if the check is real
The time between the preview read and the commit is a time-of-check/time-of-use window. Suppose the preview saw r7, but another user changed the customer to r8. Appending the note based on the old assumptions may overwrite a field, attach a note to the wrong context or violate a business rule.
At commit time, compare the fresh provider value with the value captured in the preview. If they differ, stop with STOP_STALE, show the new context to an authorized user and require a new preview. Do not silently merge a changed note or retry the old write.
Provider controls vary:
- an HTTP conditional header such as If-Unmodified-Since can cause a documented provider rejection;
- an ETag or provider revision can support an If-Match-style check when the provider documents it;
- a database adapter may use a version predicate in an atomic transaction; and
- a system may provide neither, in which case the application must be honest about the weaker guarantee.
RFC 9110 defines HTTP semantics, but the RFC does not make every provider endpoint atomic or idempotent. Read the endpoint documentation and test conflict behavior in the actual tenant.
2.7 Receipts and audit events make outcomes observable
An audit event should be append-oriented and queryable. Useful fields include:
Field	Example	Why it matters
action_id	NST-ACTION-LAB-AC01	Correlates the request, preview and receipt
actor_id	NST-USER-001	Identifies who proposed the change
reviewer_id	NST-USER-002	Identifies who approved or rejected it
tenant_id	NST-TENANT-001	Prevents cross-tenant ambiguity
preview_sha256	ffcd...	Binds approval to exact content
record_version_before/after	r7 / r8	Shows the state transition
outcome	COMMITTED, STOP_STALE	Makes success and stops measurable
receipt_id	NST-RECEIPT-LAB-350dd24bcea0	Supports reconciliation
provider_record_id	null in the lab	Separates local testing from live execution
error_code	DRAFT_CHANGED	Supports diagnosis without guessing
Replay protection starts with a unique action ID and a stored preview hash. If the same approved action is submitted again, return the original receipt as REPLAYED. If the action ID is paired with a different hash, stop with DRAFT_CHANGED. A database transaction or equivalent concurrency control must ensure that two simultaneous approval callbacks cannot both apply the effect.
3. Visual explanation
flowchart TD
    A[Authenticated request] --> B{Tenant and target authorization}
    B -- no --> X[STOP_ACCESS_DENIED]
    B -- yes --> C[Fresh read and typed preview]
    C --> D[Store preview hash and expiry]
    D --> E{Separate authorized human approval?}
    E -- reject --> R[STOP_REJECTED]
    E -- no or expired --> Q[WAIT or STOP_EXPIRED]
    E -- approve --> F[Fresh read immediately before commit]
    F --> G{Expected version still matches?}
    G -- no --> S[STOP_STALE]
    G -- yes --> H[Conditional narrow provider write]
    H -- conflict/error --> T[STOP and reconcile]
    H -- success --> I[Write receipt and audit event]
    I --> J{Same action and preview hash seen again?}
    J -- yes --> K[REPLAYED: return same receipt]
    J -- no --> L[COMMITTED]
Read the diagram from left to right. Authorization occurs before the preview, approval is bound to a stored preview, and revalidation occurs after approval. The receipt is written only after the controlled commit outcome is known. The REPLAYED path is not a second business effect; it is a safe response to a repeated callback.
4. Worked case
Scenario inputs and rules
The current customer projection is:
{
  "customer_id": "NST-CUST-001",
  "tenant_id": "NST-TENANT-001",
  "record_version": "r7",
  "customer_name": "Alder Retail",
  "last_enquiry": "Asked whether an opened carton can be returned.",
  "refund_promise_recorded": false,
  "notes_count": 0
}
Mira (NST-USER-001) is the Sales Representative who owns this customer. Len (NST-USER-002) is a Sales Manager in the same tenant. Noor is a Knowledge Editor and is not an authorized owner or reviewer for this operation. The note is valid only when it is one to 500 non-whitespace characters.
Step-by-step result
1. The application obtains Mira’s identity from its trusted session and creates NST-ACTION-LAB-AC01. It does not accept owner=mira as proof of identity from model text.
2. The policy layer confirms the tenant and customer ownership, then reads version r7.
3. The application stores the preview shown in Lesson 2.5. The state becomes PREVIEW_READY; no customer note has been added.
4. Len approves the exact preview hash. Mira cannot approve her own action because the exercise policy requires separation.
5. The commit path reads the customer again. It still has version r7, so the local transaction appends the note and advances the local projection to r8.
6. The action store records COMMITTED, a receipt and audit events. The global CRM fixture remains unchanged, and provider_record_id remains null.
The observed offline result is:
{
  "mode": "offline_action_replay",
  "crm_unchanged": true,
  "outcome": "COMMITTED",
  "action_status": "committed",
  "record_version_before": "r7",
  "record_version_after": "r8",
  "provider_record_id": null,
  "receipt_id": "NST-RECEIPT-LAB-350dd24bcea0"
}
Submitting the same action and matching preview hash again returns REPLAYED with the same receipt. It does not add a second note.
A mistake and its correction
Mistake: The model calls an update tool immediately after composing the note and reports “the CRM was updated.” There is no stored preview, no separate reviewer, no fresh version check and no provider receipt.
Correction: The model can request a proposal. Application code authenticates Mira, authorizes the target, stores the preview, obtains Len’s approval, re-reads the record and performs a narrow conditional commit. The response states whether the result is a local simulated receipt or a verified provider receipt. In this chapter’s lab it is local only.
5. Try it yourself — guided practice
Goal
Run a complete preview → approval → commit → replay cycle and inspect the evidence. Then run the negative cases to see why a safe action stops.
Lab files and complete inputs
Use the supplied offline files:
- northstar_action_lab.py — isolated SQLite action store and state transitions;
- run_action_lab.py — start, review, replay and inspect commands;
- check_action_lab.py — fixture checker for outcomes, replay, concurrency, audit events and CRM immutability; and
- action_cases.csv — the complete guided dataset below.
case_id,owner,reviewer,customer_id,note_text,decision,approval_hash,crm_before_review,review_at,expected
AC01,mira,len,NST-CUST-001,Follow up on invoice date and route opened-carton request to Sales Manager.,approve,match,ok,2026-10-05T09:05:00Z,COMMITTED
AC02,mira,len,NST-CUST-001,Follow up on invoice date and route opened-carton request to Sales Manager.,reject,match,ok,2026-10-05T09:05:00Z,STOP_REJECTED
AC03,mira,len,NST-CUST-001,Follow up on invoice date and route opened-carton request to Sales Manager.,approve,mismatch,ok,2026-10-05T09:05:00Z,DRAFT_CHANGED
AC04,mira,len,NST-CUST-001,Follow up on invoice date and route opened-carton request to Sales Manager.,approve,match,new_version,2026-10-05T09:05:00Z,STOP_STALE
AC05,mira,mira,NST-CUST-001,Follow up on invoice date and route opened-carton request to Sales Manager.,approve,match,ok,2026-10-05T09:05:00Z,SEPARATION_REQUIRED
AC06,noor,len,NST-CUST-001,Follow up on invoice date and route opened-carton request to Sales Manager.,approve,match,ok,2026-10-05T09:05:00Z,ACCESS_DENIED
AC07,mira,len,NST-CUST-001,Follow up on invoice date and route opened-carton request to Sales Manager.,approve,match,ok,2026-10-05T09:31:00Z,PREVIEW_EXPIRED
AC08,mira,len,NST-CUST-001,Follow up on invoice date and route opened-carton request to Sales Manager.,approve,match,ok,2026-10-05T09:05:00Z,COMMITTED
AC09,mira,len,NST-CUST-001,Different note content for the same action.,approve,mismatch,ok,2026-10-05T09:05:00Z,DRAFT_CHANGED
AC10,mira,len,NST-CUST-002,Follow up on invoice date.,approve,match,ok,2026-10-05T09:05:00Z,ACCESS_DENIED
AC11,mira,len,NST-CUST-001,,approve,match,ok,2026-10-05T09:05:00Z,INVALID_NOTE
The action_cases.csv file in the lab bundle contains the same rows and values. Use it directly when comparing hashes.
Steps
1. Start AC01 at 2026-10-05T09:00:00Z:
python3 -B run_action_lab.py start --case AC01 --db action_guided.sqlite
Expected intermediate result: action_status is preview_only, the before version is r7, and crm_unchanged is true.
2. Review AC01 with the matching hash:
python3 -B run_action_lab.py review --case AC01 --db action_guided.sqlite
Expected intermediate result: outcome is COMMITTED, the receipt has action_status: "committed", and the local customer becomes r8.
3. Replay the same approval:
python3 -B run_action_lab.py replay --case AC01 --db action_guided.sqlite
Expected result: outcome is REPLAYED, the receipt ID and idempotency key are unchanged, and the local note count has not increased again.
4. Run the full fixture checker in a new output directory:
python3 -B check_action_lab.py --out action_checks_guided
Record the summary. It should report 11 fixture cases passed, replay passed, concurrent approval passed, audit events passed, crm_unchanged: true and live_provider_execution: "not_run".
5. Inspect the saved state for AC01 and explain each event:
python3 -B run_action_lab.py inspect --case AC01 --db action_guided.sqlite
6. Before reading the solutions, write a one-sentence reason for each stop case: AC02, AC03, AC04, AC05, AC06, AC07, AC10 and AC11.
6. Independent challenge
Create a separate database for each case. Do not modify the global CRM fixture. The challenge dataset is:
case_id,owner,reviewer,customer_id,note_text,decision,approval_hash,crm_before_review,review_at,expected
ACC1,mira,len,NST-CUST-001,Request missing invoice date before manager review.,approve,match,ok,2026-10-05T09:05:00Z,COMMITTED
ACC2,mira,len,NST-CUST-001,Request missing invoice date before manager review.,approve,match,new_version,2026-10-05T09:05:00Z,STOP_STALE
ACC3,mira,len,NST-CUST-001,Request missing invoice date before manager review.,reject,match,ok,2026-10-05T09:05:00Z,STOP_REJECTED
For each case, deliver:
1. the observed callback outcome and final action phase;
2. the expected before and after record versions;
3. the reviewer and authorization decision;
4. the audit event count and whether a receipt exists; and
5. a short explanation of why the action must not be retried blindly.
Then add one new case of your own in which the reviewer belongs to another tenant. State the expected stop code before running it. A successful challenge has a receipt only for ACC1, no receipt for ACC2 or ACC3, and no change to the global CRM fixture.
7. Common problems and recovery
Symptom	Diagnosis	Safe correction	Verification
A preview says r7, but review returns STOP_STALE	The customer changed after preview	Fetch current context and create a new preview	New preview names the new version; old action remains stopped
Review returns DRAFT_CHANGED	The approval hash does not match the stored proposal	Do not edit the stored draft in place; create a new action	New action has a new ID and hash
Owner receives SEPARATION_REQUIRED	The policy requires a separate reviewer	Route to an authorized manager	Reviewer identity comes from trusted context
ACCESS_DENIED occurs before preview	Tenant, ownership or role check failed	Ask an authorized user or correct the application mapping	No action row or provider write is created
A retry creates a second note	There is no durable action ledger or idempotency key	Store the action ID, preview hash and receipt before accepting replay	Same approved request returns the original receipt
The update API returns 412 ALREADY_MODIFIED	The documented conditional timestamp is stale	Stop, re-read and create a new preview	No blind retry; audit contains the conflict
A model says “updated” but the receipt has provider_record_id: null	The test store was mistaken for the provider	Report the result as offline or simulated	Response keeps execution_status: "draft_only"
A public Desk reply was made instead of an internal note	The adapter did not distinguish side-effect classes	Split operations and require a separate permission for public replies	Preview explicitly says internal or public
Upsert creates a new record	Upsert was used for an exact existing-record action	Resolve the record ID and use a narrow update	A missing target stops instead of creating data
8. Check your understanding
 1. Why should a model-generated approved_by field not be accepted as proof of approval?
 2. A preview captured customer version r7; the fresh read at commit shows r8. What should the application do, and why?
 3. Name three fields that must appear in a useful change preview.
 4. What is the difference between COMMITTED and REPLAYED?
 5. Why is provider_record_id separate from logical_customer_id?
 6. When can If-Unmodified-Since help, and what does it not prove by itself?
 7. Why is an explicit update safer than an upsert for the exact existing customer in this lesson?
 8. A reviewer changes the note text in a browser after seeing the preview and clicks Approve. What should the system bind the approval to?
 9. Which evidence would let a support engineer determine whether a note was committed, rejected or stopped as stale?
10. The action checker reports crm_unchanged: true and live_provider_execution: "not_run". What may you claim, and what may you not claim?
9. Solutions and explanations
 1. Approval must come from a trusted authenticated principal and an authorization decision. A model can propose a reviewer name, but it cannot prove that the person authenticated, belongs to the tenant or has the required role. Accepting the field would allow a prompt or tool output to self-authorize a write.
 2. Stop with STOP_STALE. The proposed change was based on r7, so silently applying it to r8 could use obsolete context. Re-read the record, explain the conflict to an authorized user and create a new preview.
 3. A strong answer includes the exact target, operation and fields, before/after values or versions, actor/tenant, side-effect description, approval requirement, expiry and a content hash. Three are the minimum requested; in production, omitting identity or version information weakens the control.
 4. COMMITTED means this action caused one controlled effect in the action store or provider path. REPLAYED means the same action and preview hash were submitted again and the system returned the original receipt without performing another effect.
 5. The logical ID belongs to Northstar’s business model. The provider ID belongs to the selected CRM, Desk, Books or Creator tenant. Keeping both prevents a record from one system or tenant being accidentally used in another system’s endpoint.
 6. If-Unmodified-Since can cause a documented provider rejection if the record was modified after the supplied time. It does not, by itself, establish that the application chose the correct record, has the correct business permission, made an idempotent operation or safely handled all provider-side workflows.
 7. Upsert has create-or-update semantics. If the duplicate matching rule is different from the application’s target rule, it can create or change an unintended record. An explicit update requires the resolved existing record ID and can stop when that target is unavailable.
 8. Approval should bind to the stored canonical preview hash. Changing the note creates a different proposed effect, so the old approval must not authorize it. The application should return DRAFT_CHANGED and require a new preview and approval.
 9. The action ID, actor, reviewer, tenant, preview hash, operation, target IDs, before/after versions, outcome, error code, receipt ID, idempotency key and timestamps provide the necessary evidence. A final chat sentence alone does not.
10. You may claim that the offline fixture preserved the global CRM object, exercised the stated local cases and did not invoke a live provider. You may not claim that Zoho CRM, Desk, Books or Creator was updated, that a provider receipt exists or that production authorization is complete.
The guided practice should produce this decision table:
Case	Expected result	Reason
AC01	COMMITTED	Matching hash, authorized separate reviewer and current r7
AC02	STOP_REJECTED	Len rejected the exact preview
AC03	DRAFT_CHANGED	Supplied approval hash differs
AC04	STOP_STALE	Fresh customer version is r8, not expected r7
AC05	SEPARATION_REQUIRED	Mira cannot approve her own action
AC06	ACCESS_DENIED	Noor cannot act as the customer owner
AC07	PREVIEW_EXPIRED	Review occurs after the 30-minute preview TTL
AC08	COMMITTED	Independent normal commit with matching approval
AC09	DRAFT_CHANGED	The test supplies a mismatched hash; a different content proposal also requires a new action ID
AC10	ACCESS_DENIED	Mira is not the owner of NST-CUST-002
AC11	INVALID_NOTE	The note is empty
The independent challenge has the following solution:
- ACC1 commits from r7 to r8 and creates one receipt.
- ACC2 stops as STOP_STALE after the fixture changes the customer to r8; it has no receipt.
- ACC3 stops as STOP_REJECTED; it has no receipt.
- A reviewer from another tenant should receive ACTION_UNAVAILABLE or an equivalent tenant-isolation stop before commit. The precise public error can be less revealing than the internal audit code, but the result must not disclose or alter the other tenant’s record.
10. Chapter recap and next step
The central control is a sequence, not a single prompt:
authenticate → authorize → preview → approve exact preview → revalidate → commit narrowly → receipt and audit
You should now be able to say:
- I can keep draft generation separate from commit.
- I can identify the authenticated actor and tenant without trusting model arguments.
- I can require a separate human approval for a specified risk class.
- I can show before/after values, versions, target IDs and side effects in a preview.
- I can stop on a stale record or changed proposal instead of overwriting silently.
- I can distinguish a logical business ID from a provider record ID.
- I can return the same receipt for a safe replay.
- I can show the difference between an offline action result and a live provider execution.
The Northstar project artifact is a tested, human-reviewed CRM update fixture with preview hashes, approval checks, stale-record handling, replay protection, audit events and a scoreable outcome table. Chapter 15, Evaluation-Driven Development, will turn these cases into representative and held-out evaluation data with explicit checks for answer quality and action correctness.
11. Glossary and further reading
Glossary
- Action envelope: Structured data describing an actor, tenant, operation, target, proposed change and control metadata.
- Conditional write: A write accepted only when a documented condition, such as a version or modification time, still matches.
- Draft: A proposed change that has not caused a business-system side effect.
- Idempotency: The property that repeating the same logical request does not create another effect.
- Logical ID: A business identifier used by the application, independent of a provider’s record ID.
- Preview hash: A digest of the canonical proposed change used to bind approval to exact content.
- Provider record ID: The identifier required by a specific CRM, Desk, Books or Creator tenant.
- Revalidation: A fresh read and policy check immediately before commit.
- Receipt: Durable evidence of an action outcome, target, versions, identity and correlation identifiers.
- Replay: A repeated submission of a previously handled action.
- Separation of duties: A policy that requires different people or roles to propose and approve a consequential action.
- Stale action: A proposal whose assumptions no longer match the current record.
Further reading
- Zoho CRM API v8 — Update Records (https://www.zoho.com/crm/developer/docs/api/v8/update-records.html) — specific record updates, field API names, scopes, conditional header behavior and documented errors.
- Zoho CRM API v8 — Get Records (https://www.zoho.com/crm/developer/docs/api/v8/get-records.html) — obtaining permitted records and provider IDs before an update.
- Zoho CRM API v8 — Upsert Records (https://www.zoho.com/crm/developer/docs/api/v8/upsert-records.html) — compare create-or-update semantics with an exact update.
- Zoho Creator API v2 overview (https://www.zoho.com/creator/help/api/v2/) — OAuth, data APIs, status codes and application-specific records.
- RFC 9110 — HTTP Semantics (https://www.rfc-editor.org/rfc/rfc9110.html) — HTTP methods, conditional requests and status-code semantics.
- MCP Security Best Practices (https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices) — confused-deputy risks, token handling and authorization boundaries relevant to tool-mediated actions.
