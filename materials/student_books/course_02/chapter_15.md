# Reliable Event-Driven Integration

## What you will learn

By the end of this chapter, you will be able to:
- Explain the difference between webhooks, CRM Notification APIs, polling, and reconciliation.
- Configure a bounded Zoho CRM v8 notification channel.
- Verify notification source context using the configured channel ID and token.
- Design an HTTP receiver that acknowledges quickly and defers business processing.
- Create stable idempotency keys for Nova service-summary delivery.
- Handle duplicate, missing, delayed, and out-of-order events.
- Use bounded backoff for known no-write failures.
- Distinguish a known failed write from an uncertain write.
- Renew and verify expiring notification channels.
- Use polling and deleted-record APIs to repair notification gaps.
- Design queue states: Pending, Retryable, Blocked, and Delivered.
- Reconcile a possible CRM write before attempting another write.
- Understand what Composite rollback does and does not protect.
- Record evidence without exposing access tokens, refresh tokens, client secrets, or confidential payloads.
This chapter introduces the reliability design for the Nova integration. It does not implement the future production queue, summary module, or distributed worker system.
The earlier chapters established this event identity:
Event_Key = Request_Key + ":completed:v1"
For example:
NOV-REQ-801:completed:v1
The event payload is based on accepted Creator completion facts:
{
  "Request_Key": "NOV-REQ-801",
  "Visit_Key": "NOV-VISIT-801",
  "CRM_Account_ID": "<exact CRM Account ID>",
  "CRM_Product_ID": "<exact CRM Product ID>",
  "Summary": "Inspect data-operations training unit A",
  "Status": "Completed",
  "Completed_At": "<accepted UTC completion time>",
  "Event_Key": "NOV-REQ-801:completed:v1"
}
## Lessons

### Lesson 1 — Choose an event source and define its limits

An event-driven integration usually has four parts:
1. A source system produces a change.
2. A delivery mechanism sends a notification or makes the change discoverable.
3. A receiver records and processes the event.
4. A reconciliation process repairs gaps or uncertainty.
These terms describe different mechanisms:
Mechanism	What it does	Main reliability concern
Webhook	Sends an HTTP request to a receiver	Duplicate, missing, delayed, or malformed requests
CRM Notification API	Creates and manages CRM action-watch subscriptions	Channel expiry, configuration drift, and incomplete event payloads
Polling	Periodically reads records changed since a checkpoint	Overlap, missed boundaries, API limits, and stale checkpoints
Queue	Stores work until a worker can process it	Duplicate jobs, stuck jobs, visibility, and retry policy
Reconciliation	Compares source and target state	Uncertain writes, missing events, duplicate targets, and stale mappings
A reliable design does not assume that an event notification is a complete business record.
A Zoho CRM v8 notification callback can contain:
- server_time
- query_params
- module
- resource_uri
- ids
- affected_fields
- operation
- channel_id
- token
If return_affected_field_values is enabled, the callback can also contain changed values. These values are useful hints. They are not a replacement for reading the authoritative record when the business operation depends on the complete record.
For Nova, a CRM notification that says an Account changed does not prove that the corresponding Creator Request was completed. Creator remains the authority for the service visit lifecycle.
Event-driven does not mean exactly once
The provider documentation describes notifications as near-real-time alerts. It does not establish an exactly-once delivery guarantee, a global ordering guarantee, or a permanent event history for every callback.
Design the receiver as if delivery can be:
- At least once.
- Delayed.
- Duplicated.
- Out of order.
- Temporarily unavailable.
- Missing for a period.
The receiver must make repeated processing safe.
CRM Notification API
The CRM Notification API uses:
POST {api_domain}/crm/v8/actions/watch
The notification scope uses the form:
ZohoCRM.notifications.{operation_type}
For enabling notifications, the operation is CREATE. For reading details, use READ. For updating or disabling notification details, use the appropriate documented write or delete operation.
A minimal subscription shape is:
{
  "watch": [
    {
      "channel_id": "9000000000001501",
      "events": [
        "Accounts.edit"
      ],
      "channel_expiry": "<ISO timestamp within one week>",
      "token": "NOV-CH15-VERIFY-901",
      "notify_url": "https://<controlled-host>/nova/crm/notifications"
    }
  ]
}
The following values are lab placeholders:
- 9000000000001501 is a synthetic channel ID.
- NOV-CH15-VERIFY-901 is a synthetic verification token.
- The receiver URL must be replaced with a real HTTPS endpoint for tenant execution.
Documented notification details include:
- channel_id is returned in callbacks.
- token is returned in callbacks.
- channel_expiry can be at most one week from the time notifications are enabled.
- If expiry is absent or exceeds one week, the documented default is one hour.
- Events can be module-specific, such as Accounts.create, Accounts.edit, Accounts.delete, or Accounts.all.
- Field-specific conditions can contain up to 10 fields.
- A field-selection condition can contain up to two grouped objects.
- Related-record notifications can be controlled with notify_on_related_action.
Lesson check
1. Does a CRM callback prove that the full changed record is present in the callback?
2. What delivery guarantee should your receiver assume?
3. What is the purpose of channel_id?
4. What is the documented maximum notification expiry?
5. Which system owns Nova completion facts?
### Lesson 2 — Verify and acknowledge notifications safely

A receiver has two responsibilities:
1. Verify that the request belongs to the configured notification channel.
2. Acknowledge the request quickly after durable intake.
These responsibilities should be separated from business processing.
Verification data
The receiver should validate:
- HTTPS was used.
- The request body is valid JSON.
- channel_id matches an active subscription record.
- token matches the configured channel token.
- module is an allowed module.
- operation is an allowed operation.
- resource_uri matches the expected CRM API domain and module.
- ids is present and contains valid-looking opaque strings.
- The body is within a configured size limit.
- The event is not obviously malformed.
The current CRM notification documentation describes the callback token and channel ID. It does not provide a signed request or HMAC verification contract in the material used for this chapter.
Therefore:
- Do not claim that the token is a cryptographic signature.
- Do not invent a Zoho webhook signature header.
- Do not treat the callback as authenticated merely because it arrived at your URL.
- Use HTTPS, channel and token checks, restricted endpoint behavior, safe logging, and reconciliation.
The token should not be placed in a public source repository or ordinary debug log. Store it with the notification configuration.
Acknowledge before doing slow work
A receiver should not perform all of these operations before responding:
- Read the entire CRM record.
- Call Creator.
- Call CRM again.
- Send email.
- Upload files.
- Wait for a worker.
- Retry a failed delivery.
Instead:
receive request
  -> parse and verify
  -> create durable inbox entry
  -> return success acknowledgement
  -> process asynchronously
The durable inbox entry should contain safe metadata such as:
{
  "inbox_key": "CH15-INGRESS-901",
  "channel_id": "9000000000001501",
  "module": "Accounts",
  "operation": "edit",
  "record_ids": [
    "<opaque CRM ID>"
  ],
  "received_at": "<UTC timestamp>",
  "verification": "CHANNEL_AND_TOKEN_MATCH",
  "processing_state": "Pending"
}
Do not store the raw Authorization header, access token, refresh token, client secret, or complete confidential callback body in a normal evidence file.
Multiple IDs in one callback
A callback can contain multiple record IDs. Treat the callback envelope and each record-level work item as separate objects:
one callback envelope
  -> record ID A -> work item A
  -> record ID B -> work item B
The envelope may be acknowledged once. Each work item needs its own idempotency and processing result.
Verification failures
A verification failure must not create a normal delivery job.
Examples:
Failure	Action
Unknown channel	Reject and alert
Wrong token	Reject and alert
Missing module	Reject and record safe diagnostic
Empty IDs	Reject as malformed
Unexpected module	Reject or quarantine
Invalid JSON	Reject and preserve only safe request metadata
Expired channel	Mark subscription for renewal or recreation
Valid channel but unknown event	Quarantine for review
Do not silently treat an invalid callback as a valid event.
Lesson check
1. Why should acknowledgment be separate from business processing?
2. Is the notification token a cryptographic signature?
3. Why does a callback with two IDs produce two work items?
4. What should happen when the channel ID is unknown?
5. Which secrets must not appear in receiver logs?
### Lesson 3 — Design idempotency and ordering

Idempotency means that processing the same logical event more than once produces the same intended result without creating another business effect.
Business idempotency
For Nova, the business identity is:
Request_Key
The event identity includes the event version:
Event_Key = Request_Key + ":completed:v1"
The target summary identity is also intended to be based on Request_Key.
This produces a stable relationship:
Identity	Purpose
Request_Key	One service request
Visit_Key	One service visit
Event_Key	One versioned completion event
CRM summary identity	One summary for the Request
A retry must reuse the same Event_Key. It must not create:
NOV-REQ-801:completed:v2
unless the business contract deliberately introduces a new version.
Source idempotency versus business idempotency
A CRM notification does not provide a documented universal event ID in the callback shape. A local source fingerprint can help detect repeated delivery:
Source_Fingerprint =
  channel_id + "|" +
  module + "|" +
  operation + "|" +
  record_id + "|" +
  server_time
This is a useful duplicate hint, but it is not a guaranteed global event identity.
Business idempotency is stronger:
Event_Key = NOV-REQ-801:completed:v1
If a worker receives the same completion event twice, it should look up the delivery intent by Event_Key.
Possible outcomes:
Existing intent	Action
No intent	Create one Pending intent
Pending	Do not create another intent
Retryable	Resume according to retry policy
Delivered	Return duplicate/already delivered
Blocked	Do not retry automatically
More than one intent	Block and reconcile duplicate records
A database or Creator field with a unique constraint is necessary. A search-before-create check alone is not sufficient under concurrency.
Ordering
Events can arrive in an order different from the order in which changes occurred.
Example:
1. Request completed
2. CRM update notification arrives
3. Earlier Account edit notification arrives
Do not process event order from arrival time alone.
For each business key:
1. Read the authoritative source.
2. Confirm the current lifecycle facts.
3. Compare the event version or source revision if available.
4. Ignore an older event if a newer terminal event is already delivered.
5. Reconcile when the sequence cannot be established.
Nova completion is easier than a general CRM change stream because:
- Completion is a terminal baseline state.
- Ordinary edits after completion are not allowed.
- Event_Key is stable.
- The completion payload is built from accepted Creator facts.
The system must still read the Creator Job and Request before attempting the CRM summary write.
Out-of-order fixture
arrival_order,event_key,source_state,expected_action
1,NOV-REQ-801:completed:v1,Completed,process or create Pending
2,NOV-REQ-801:completed:v1,Completed,duplicate; do not create a second intent
3,NOV-REQ-801:reopened:v1,not supported by baseline,Block
The third row is outside the baseline. Do not invent reopening behavior in this chapter.
Lesson check
1. What is the Nova business idempotency key?
2. Why is a source fingerprint not always a complete event identity?
3. What should happen when a Delivered event is received again?
4. Why should a worker read the authoritative source before delivery?
5. Does callback arrival time establish business ordering?
### Lesson 4 — Use bounded queues and backoff

A queue separates intake from processing. It also makes failure visible.
Queue states
Use these conceptual states:
State	Meaning
Pending	Accepted work has not completed its first delivery attempt
Retryable	A known temporary failure occurred and another attempt is allowed
Blocked	Automatic processing must stop until a human or controlled reconciliation resolves the issue
Delivered	Target state was verified according to the delivery contract
The state is not the same as an HTTP status.
Examples:
Condition	Queue state
Valid new completion event	Pending
CRM service returns 503 before any write is proven	Retryable
OAuth scope mismatch	Blocked
CRM response is lost after a write may have happened	Blocked or reconciliation hold
Exact target summary found during read-back	Delivered
Duplicate of an already delivered event	Remains Delivered
Missing CRM Account mapping	Blocked
Missing active CRM owner mapping	Blocked
Known failure versus uncertain failure
These two outcomes must not be treated alike.
Known no-write failure
Examples:
- DNS failure before a request reaches the provider.
- Connection refused.
- Provider returns 503 before accepting the request.
- Provider explicitly returns a validation error before processing.
- Request is rejected for insufficient scope before the write operation.
The system has evidence that the business write did not happen, subject to the provider’s contract.
For the Nova lab, use this bounded policy:
attempt 1 -> wait 1 minute
attempt 2 -> wait 5 minutes
attempt 3 -> wait 15 minutes
after attempt 3 -> Blocked
These are lab/application policy values. They are not universal CRM retry quotas.
Uncertain write
Examples:
- Network connection closes after the request is sent.
- The client times out after submitting the body.
- A proxy returns an incomplete response.
- A worker crashes after the provider accepts the write.
The system does not know whether the write happened.
Do not immediately send another create request. First:
1. Preserve the original Event_Key.
2. Read the target by its known identity if available.
3. Query by the verified external identity if available.
4. Compare required facts.
5. If exactly one matching target exists, mark Delivered.
6. If no target exists and the provider contract proves no write, perform a controlled retry.
7. If multiple targets exist, mark Blocked.
Backoff with jitter
A worker can add small random jitter to avoid many workers retrying simultaneously:
delay = policy_delay + random_jitter
For example:
policy delay: 5 minutes
jitter: 0 to 30 seconds
This is a worker policy, not a provider guarantee. Never use jitter to hide unlimited retries.
Pure Deluge planning helper
Host: Zoho Creator custom function or test function
Function: nova_ch15_plan_delivery
Inputs: event Map, current UTC text, existing-intent facts, attempt count
Connection: none
Supported task: Validate event identity and return a delivery decision
Dependencies: none; no writes; no network calls
Return contract: Map with code, state, dedupe_key, delay_minutes, requires_reconciliation, and safe reason
map nova_ch15_plan_delivery(map event_map, boolean intent_exists, string existing_state, long attempt_count)
{
	result = Map();
	result.put("code","BLOCKED");
	result.put("state","Blocked");
	result.put("delay_minutes",0);
	result.put("requires_reconciliation",false);

	if(event_map == null)
	{
		result.put("code","BLOCKED_INPUT");
		result.put("reason","event_missing");
		return result;
	}

	request_key = event_map.get("Request_Key");
	visit_key = event_map.get("Visit_Key");
	event_key = event_map.get("Event_Key");
	status_value = event_map.get("Status");

	if(request_key == null || visit_key == null || event_key == null ||
	   status_value == null)
	{
		result.put("code","BLOCKED_INPUT");
		result.put("reason","required_identity_missing");
		return result;
	}

	expected_event_key = request_key.toString() + ":completed:v1";
	if(event_key.toString() != expected_event_key)
	{
		result.put("code","BLOCKED_EVENT_VERSION");
		result.put("reason","unexpected_event_key");
		return result;
	}

	if(status_value.toString() != "Completed")
	{
		result.put("code","BLOCKED_SOURCE_STATE");
		result.put("reason","source_not_completed");
		return result;
	}

	result.put("dedupe_key",event_key.toString());

	if(intent_exists && existing_state == "Delivered")
	{
		result.put("code","ALREADY_DELIVERED");
		result.put("state","Delivered");
		result.put("reason","same_event_key_already_verified");
		return result;
	}

	if(intent_exists && existing_state == "Blocked")
	{
		result.put("code","ALREADY_BLOCKED");
		result.put("state","Blocked");
		result.put("reason","manual_reconciliation_required");
		return result;
	}

	if(intent_exists && existing_state == "Pending")
	{
		result.put("code","ALREADY_PENDING");
		result.put("state","Pending");
		result.put("reason","another_worker_owns_first_attempt");
		return result;
	}

	if(attempt_count == null || attempt_count < 0)
	{
		result.put("code","BLOCKED_ATTEMPT_COUNT");
		result.put("reason","invalid_attempt_count");
		return result;
	}

	if(attempt_count == 0)
	{
		result.put("code","READY_FIRST_ATTEMPT");
		result.put("state","Pending");
		result.put("reason","new_verified_event");
		return result;
	}

	if(attempt_count == 1)
	{
		result.put("code","RETRYABLE_DELAY");
		result.put("state","Retryable");
		result.put("delay_minutes",1);
		result.put("reason","known_no_write_failure");
		return result;
	}

	if(attempt_count == 2)
	{
		result.put("code","RETRYABLE_DELAY");
		result.put("state","Retryable");
		result.put("delay_minutes",5);
		result.put("reason","known_no_write_failure");
		return result;
	}

	if(attempt_count == 3)
	{
		result.put("code","RETRYABLE_DELAY");
		result.put("state","Retryable");
		result.put("delay_minutes",15);
		result.put("reason","known_no_write_failure");
		return result;
	}

	result.put("code","BLOCKED_RETRY_LIMIT");
	result.put("state","Blocked");
	result.put("requires_reconciliation",true);
	result.put("reason","bounded_retry_limit_reached");
	return result;
}
This helper is deliberately incomplete:
- It does not create a queue record.
- It does not lock a worker lease.
- It does not perform a CRM call.
- It does not calculate authentication state.
- It does not prove that a retry is safe.
- It does not replace a unique database constraint.
- It does not implement a distributed lock.
Lesson check
1. What is the difference between Retryable and Blocked?
2. Why is a lost response not automatically a known no-write failure?
3. What is the purpose of bounded backoff?
4. What does Event_Key prevent?
5. Does the Deluge helper implement a queue?
### Lesson 5 — Renew subscriptions and repair gaps with polling

Notification renewal
There is no separate renewal endpoint in the verified CRM v8 Notification API material. Renewal is performed by updating notification details.
The current channel should first be read:
GET {api_domain}/crm/v8/actions/watch?channel_id=<channel_id>
Authorization: Zoho-oauthtoken <access_token>
Before expiry:
1. Read the current channel configuration.
2. Confirm the channel ID, module, events, receiver URL, and token.
3. Select a new expiry no more than one week from the renewal request.
4. Update the channel.
5. Read the channel again.
6. Compare the stored configuration.
7. Record the new expiry.
A PATCH request updates specific notification details, but the documented request still requires key configuration fields such as notify_url, channel_id, and events. Send the complete known configuration to reduce accidental drift.
A PUT request persists the provided details and removes the rest. Use PUT only when you intentionally want to replace the full configuration.
If renewal is uncertain:
- Do not create a second channel immediately.
- Read the existing channel by ID.
- Compare its expiry and configuration.
- If the channel is gone or unusable, create a new channel with a new controlled channel ID.
- Record the old channel as disabled, expired, or unknown.
Polling as gap recovery
Polling should not normally compete with notifications. Use it to:
- Repair a receiver outage.
- Detect expired channels.
- Cover a deployment window.
- Reconcile events that may have been lost.
- Detect deletions.
For ordinary records, use a checkpoint containing:
{
  "module": "Accounts",
  "last_seen_modified_time": "<UTC or CRM ISO timestamp>",
  "last_seen_id": "<opaque CRM ID>",
  "overlap_start": "<earlier safe time>",
  "poll_run_key": "CH15-POLL-901"
}
Use an overlap window rather than starting exactly at the last timestamp. The overlap protects against equal timestamps and clock differences. Dedupe the overlapping records using the record ID and an observed revision such as Modified_Time.
For a query-based poll, use a deterministic order:
{
  "select_query":
    "select Account_Name, Modified_Time, id
     from Accounts
     where Modified_Time >= '<overlap timestamp>'
       and Account_Name like 'NOVCH15%'
     order by Modified_Time asc, id asc
     limit 0, 200"
}
The exact date-time syntax must match the CRM API contract and tenant time zone.
For deleted records:
GET {api_domain}/crm/v8/Accounts/deleted?type=all
Authorization: Zoho-oauthtoken <access_token>
The deleted-record API documents:
- all, recycle, and permanent types.
- Up to 200 records per page.
- Recycle-bin records available for up to 60 days.
- Permanently deleted records available for up to 120 days.
These windows are not a permanent event archive. A reconciliation process must run within the available retention window.
Polling checkpoint safety
Never advance the checkpoint before processing the retrieved page.
Use this sequence:
read page
  -> validate response
  -> record IDs and safe revision values
  -> enqueue or reconcile work
  -> persist next checkpoint
If the worker fails after enqueueing but before saving the checkpoint, the next poll will overlap. Idempotency must make that safe.
If the worker saves the checkpoint before enqueueing, a crash can permanently skip records.
Lesson check
1. How is a CRM notification channel renewed?
2. Why should the current channel be read before renewal?
3. Why should polling use an overlap window?
4. When should a polling checkpoint advance?
5. How long does the deleted-record API document for recycle-bin records?
## Visual explanation

flowchart LR
    A[CRM change] --> B[Notification channel]
    B --> C[HTTPS receiver]
    C --> D[Verify channel and token]
    D --> E[Durable inbox]
    E --> F[Queue intent by Event_Key]
    F --> G[Worker]
    G --> H[Read Creator source]
    H --> I[Read or reconcile CRM target]
    I --> J[Write target if safe]
    J --> K[Read back]
    K --> L[Delivered]
    G --> M[Retryable]
    G --> N[Blocked]
    O[Polling checkpoint] --> E
    P[Channel renewal] --> B
    Q[Deleted-record scan] --> E
Plain-text explanation:
- Notifications provide speed.
- The receiver provides verification and durable intake.
- The queue provides controlled processing.
- The worker reads authoritative source facts.
- Read-back establishes target state.
- Polling repairs notification gaps.
- Renewal keeps the source subscription alive.
- Reconciliation resolves uncertainty rather than guessing.
## Worked case

Nova completion delivery
The baseline target is a future CRM service-summary record owned by the actual active Morgan CRM user. That module and its fields have not yet been implemented.
The lab therefore models the intent without claiming production delivery.
Source facts
Use the established Chapter 8 completed fixture:
Request_Key: NOV-REQ-801
Visit_Key: NOV-VISIT-801
Request status: Completed
Job Work_State: Completed
Inspection_Result: Pass
Completion notes: Filter checked; ventilation operating normally
CRM Account ID: exact mapped string
CRM Product ID: exact mapped string
Completed_At: actual accepted Creator UTC time
The exact Chapter 8 completion timestamp must be read from the tenant. Do not substitute the mock timestamp when recording live evidence.
Event
{
  "Event_Key": "NOV-REQ-801:completed:v1",
  "Request_Key": "NOV-REQ-801",
  "Visit_Key": "NOV-VISIT-801",
  "CRM_Account_ID": "<exact Cedar Account ID>",
  "CRM_Product_ID": "<exact Ventilation Product ID>",
  "Summary": "Inspect data-operations training unit A",
  "Status": "Completed",
  "Completed_At": "<accepted Creator UTC time>",
  "Completion_Notes": "Filter checked; ventilation operating normally"
}
Intent record
The proposed intent record is conceptual:
{
  "Event_Key": "NOV-REQ-801:completed:v1",
  "Request_Key": "NOV-REQ-801",
  "Visit_Key": "NOV-VISIT-801",
  "State": "Pending",
  "Attempt_Count": 0,
  "Next_Attempt_At": null,
  "Last_Code": "RECEIVED",
  "Target_Identity": "Request_Key=NOV-REQ-801",
  "Owner_Identity": "<actual Morgan CRM user ID>",
  "Source": "Creator completion",
  "Created_At": "<UTC time>"
}
The actual persistent module is not built in this chapter.
Processing sequence
1. Receive completion event.
2. Validate Event_Key and required fields.
3. Check whether Event_Key already exists.
4. If Delivered, stop with duplicate-safe result.
5. If Pending under another worker, do not create another intent.
6. Read Creator Request and Job.
7. Confirm Completed / Completed / Pass facts.
8. Confirm exact CRM Account and Product IDs.
9. Confirm actual active Morgan CRM user mapping.
10. Read target summary by Request_Key.
11. If exact target exists and facts match, mark Delivered.
12. If no target exists, submit one controlled write.
13. If response is accepted, read the target back.
14. If read-back matches, mark Delivered.
15. If a known no-write failure occurs, schedule bounded retry.
16. If the write result is uncertain, reconcile before another write.
Expected decision fixtures
fixture,event_key,existing_state,source_state,delivery_result,expected_state
1,NOV-REQ-801:completed:v1,none,Completed,ready for first attempt,Pending
2,NOV-REQ-801:completed:v1,Delivered,Completed,duplicate-safe no write,Delivered
3,NOV-REQ-801:completed:v1,Pending,Completed,another worker owns intent,Pending
4,NOV-REQ-801:completed:v1,none,In Progress,source validation blocked,Blocked
5,NOV-REQ-801:completed:v1,none,Completed with missing CRM ID,identity blocked,Blocked
6,NOV-REQ-801:completed:v1,none,Completed with known 503,wait 1 minute,Retryable
7,NOV-REQ-801:completed:v1,none,Completed with uncertain timeout,reconcile first,Blocked
8,NOV-REQ-801:completed:v1,Blocked,Completed,manual review required,Blocked
Reconciliation outcomes
Read-back result	Meaning	State
One target, exact Request_Key, exact facts	Delivery verified	Delivered
No target, provider proved no write	Controlled retry may be allowed	Retryable
No target, response was uncertain	Write state unknown	Blocked pending reconciliation
Two targets with same Request_Key	Duplicate target	Blocked
Target exists but wrong Account or Product	Data conflict	Blocked
Target exists with old facts	Stale or partial target	Blocked or deliberate update policy
Do not delete one of two duplicate targets automatically. A human or approved repair process must determine which record is authoritative.
## Try it yourself — guided practice

Practice A — Configure a notification channel
Dependencies
- Dedicated CRM training organization.
- Current CRM v8 OAuth access token.
- Notification create and read scopes.
- Controlled HTTPS receiver.
- A safe test module such as Accounts.
- A unique synthetic channel ID.
- A channel verification token no longer than 50 characters.
Configuration worksheet
field,value,observed
api_domain,<token api_domain>,NOT_YET_RUN
module,Accounts,EXPECTED
event,Accounts.edit,EXPECTED
channel_id,<synthetic long value>,NOT_YET_RUN
channel_expiry,<within one week>,NOT_YET_RUN
token,NOV-CH15-VERIFY-901,EXPECTED
notify_url,<controlled HTTPS URL>,NOT_YET_RUN
return_affected_field_values,true,EXPECTED
Enable the channel with a marker Account edit. Do not use a production customer record.
Expected subscription response:
- A success result.
- Resource URI for Accounts.
- Resource ID for Accounts.
- Channel ID.
- Channel expiry.
This is an expected response shape, not a live result.
Practice B — Receive and verify a callback
Edit one disposable Account.
Capture only safe callback evidence:
received_at,channel_id,module,operation,record_count,token_match,resource_match,verification,observed
<UTC>,<fill>,Accounts,edit,<fill>,<true/false>,<true/false>,<fill>,NOT_YET_RUN
Do not export the complete token or confidential CRM values.
The receiver should:
1. Parse the JSON.
2. Compare channel_id.
3. Compare the configured token.
4. Validate module and operation.
5. Validate the record ID shape.
6. Create an inbox entry.
7. Return the receiver’s normal acknowledgement.
8. Process the ID asynchronously.
Practice C — Test duplicates and out-of-order events
Use these synthetic callback bodies:
{
  "server_time": 1791200000000,
  "module": "Accounts",
  "resource_uri": "https://www.zohoapis.eu/crm/v8/Accounts",
  "ids": [
    "5725767000001000001"
  ],
  "affected_fields": [
    {
      "5725767000001000001": [
        "Description"
      ]
    }
  ],
  "operation": "update",
  "channel_id": "9000000000001501",
  "token": "NOV-CH15-VERIFY-901"
}
Send the same body twice.
Expected local behavior:
attempt,inbox_result,queue_result,target_writes
1,accepted,new intent,at most one
2,accepted duplicate,same intent,zero additional writes
Then send an older synthetic callback after a newer one.
Expected behavior:
- The receiver can accept it as a valid source callback.
- The worker must not overwrite a newer verified business state without checking the authoritative record.
- The event should be marked duplicate, stale, or reconciliation-required according to the local intent state.
These are local simulation expectations. They do not prove provider retry behavior.
Practice D — Test renewal
1. Read current notification details.
2. Record channel_expiry.
3. Calculate a renewal expiry no more than one week from the renewal request.
4. Update the notification with the full known configuration.
5. Read it again.
6. Compare channel ID, module, events, receiver URL, token match, and expiry.
Evidence:
operation,channel_id,old_expiry,new_expiry,events_preserved,notify_url_preserved,verification,observed
renew,<fill>,<fill>,<fill>,<true/false>,<true/false>,<fill>,NOT_YET_RUN
Practice E — Simulate polling recovery
Use a checkpoint:
{
  "module": "Accounts",
  "overlap_minutes": 5,
  "last_seen_modified_time": "2026-10-05T13:00:00Z",
  "last_seen_id": "5725767000001000001"
}
Create a synthetic result containing:
Account_Name,Modified_Time,id
NOVCH15-A,2026-10-05T12:58:00Z,5725767000001000000
NOVCH15-B,2026-10-05T13:02:00Z,5725767000001000001
NOVCH15-C,2026-10-05T13:03:00Z,5725767000001000002
Expected behavior:
- NOVCH15-A is inside the overlap and may be a duplicate.
- NOVCH15-B matches the checkpoint ID and must be deduplicated.
- NOVCH15-C is new work.
- The checkpoint advances only after the page is safely enqueued or reconciled.
## Independent challenge

Design a reliable completion event pipeline for NOV-REQ-802, whose current state is:
Request: In Progress
Job: In Progress
Inspection_Result: Rework_Required
Completed_At: empty
Your design must answer:
Question	Your answer
Should a completion event be created?
Which source is authoritative?
What happens to a callback claiming Completed?
What is the dedupe key?
What is the queue state?
Which fields must be read before delivery?
What is a known no-write failure?
What is an uncertain-write failure?
What is the first retry delay?
What happens after three retryable attempts?
What proves Delivered?
What evidence is safe to export?
Create these failure fixtures.
Failure fixture 1 — Duplicate notification
Two callbacks contain the same:
channel_id
module
operation
record ID
token
Expected solution:
- Verify both callbacks.
- Accept the duplicate at ingress if it is structurally valid.
- Use the same source fingerprint or business key.
- Create only one delivery intent.
- Perform no second business write.
Failure fixture 2 — Expired channel
The channel read shows that channel_expiry is in the past.
Expected solution:
- Mark the subscription as expired.
- Start a polling recovery window.
- Attempt a controlled update or create a new channel according to the current configuration.
- Do not assume that events during the expired interval were delivered.
- Reconcile source records changed during the gap.
Failure fixture 3 — Lost delivery response
The CRM write request was sent, but the worker received a timeout.
Expected solution:
- Do not create a second target immediately.
- Read the target by exact identity or verified external key.
- If one exact target exists, compare all required facts.
- If zero targets exist, determine whether the provider contract proves no write.
- If the result remains uncertain, mark the intent for reconciliation.
- If duplicates exist, block automatic processing.
Failure fixture 4 — Out-of-order completion
A callback for an older state arrives after a callback for a newer state.
Expected solution:
- Compare the event version and source state.
- Read the authoritative Creator Request and Job.
- Do not regress the Nova lifecycle.
- Ignore or quarantine the older event.
- Preserve the newest verified state.
## Common problems and recovery

Symptom	Likely cause	Recovery
Callback has an unknown channel ID	Wrong subscription, stale receiver, or spoofed request	Reject and alert; inspect active channel configuration
Callback token does not match	Wrong environment, stale channel, or untrusted request	Reject; do not enqueue normal work
Callback contains a valid ID but no full record	Notification is an event hint	Read the authoritative record before delivery
Receiver performs slow CRM work before responding	Ingress and processing are coupled	Persist a safe inbox entry and acknowledge quickly
Same callback arrives twice	At-least-once delivery or source retry	Deduplicate by source fingerprint and business key
Events arrive out of order	Distributed delivery timing	Read current source state and apply monotonic business rules
Notification channel expires	No renewal process or renewal failed	Read details, renew with full configuration, verify, and poll the gap
PUT removes notification settings	PUT replaces provided configuration	Use complete configuration or use PATCH deliberately
Renewal creates a second channel	Existing channel state was not checked	Read by channel ID before creating another channel
Callback has multiple IDs	One notification covers several records	Fan out to record-level work items with separate dedupe
Worker retries after timeout and creates duplicate	Uncertain write treated as known failure	Reconcile target before retry
Queue retries forever	No attempt ceiling	Apply bounded delays and move to Blocked
Queue says Delivered after HTTP 200 only	Response not verified	Read back required identity and facts
Polling misses a record	Checkpoint advanced before processing	Advance checkpoint only after enqueue or reconciliation
Polling creates repeated work	Overlap window not deduplicated	Use record ID and revision-aware idempotency
Deleted record is not found	Retention window expired or permission missing	Record the gap; use another source or controlled manual recovery
Notification field condition is rejected	Invalid field API name or module ID mismatch	Read module and field metadata first
Notifications fire for unexpected related records	notify_on_related_action remains enabled	Set and verify the intended related-action behavior
Verification logs expose token	Raw callback was logged	Remove secret-bearing evidence and log only a safe match result
Provider retry behavior is assumed	No documented delivery contract	Design for duplicates and use polling/reconciliation
## Check your understanding

 1. What is the difference between a webhook and a notification subscription?
 2. What should happen before an HTTP receiver acknowledges a valid notification?
 3. Is a notification token a signed request?
 4. What is the Nova event key for a completed Request?
 5. Why is a unique constraint required for delivery intents?
 6. What should happen after a duplicate Delivered event?
 7. What is the difference between a known no-write failure and an uncertain write?
 8. What is the retry sequence used by this lab?
 9. Why must polling use an overlap window?
10. When should a notification channel be renewed?
11. What does a CRM callback’s affected_fields list represent?
12. Does notification renewal guarantee that events during a previous outage can be recovered?
13. What proves that a target is Delivered?
14. Does a CRM Composite rollback undo a Creator write?
15. Which event processing behavior protects Nova from out-of-order callbacks?
## Solutions and explanations

 1. A webhook is the HTTP delivery mechanism. A CRM Notification API subscription configures which CRM actions are sent to the webhook receiver.
 2. The receiver should validate the request and persist a safe inbox entry before acknowledging it. Slow business processing belongs in a worker.
 3. No. The documented notification token is returned in the callback for verification. The reviewed contract does not define it as a cryptographic signature.
 4. NOV-REQ-801:completed:v1 for Request NOV-REQ-801.
 5. Search-before-create can race under concurrency. A unique constraint makes duplicate intent creation fail safely.
 6. Treat it as duplicate-safe and perform no additional business write.
 7. A known no-write failure provides evidence that the provider did not accept the write. An uncertain write means the client cannot determine whether the provider accepted it.
 8. First attempt immediately, then known no-write delays of 1 minute, 5 minutes, and 15 minutes, followed by Blocked.
 9. Equal timestamps, clock differences, and overlapping pages can otherwise cause records to be skipped. The overlap must be deduplicated.
10. Read the current channel before expiry, update it with a new expiry no more than one week from the renewal request, and read it again to verify.
11. It identifies fields affected by the notification. It is not automatically a complete record snapshot.
12. No. Expired-channel intervals require polling and reconciliation.
13. The target must be read and match the required identity and facts. An HTTP success response alone is insufficient for this chapter’s evidence contract.
14. No. Composite rollback applies to supported CRM subrequests in that composite. It does not roll back Creator, email, webhooks, or other external effects.
15. The worker reads the authoritative Creator state and applies the stable Event_Key and state rules instead of trusting callback arrival order.
## Chapter recap and next step

Reliable event-driven integration is built from several controls:
- Notifications provide near-real-time hints.
- Webhooks provide transport.
- Verification rejects malformed or untrusted callbacks.
- A durable inbox prevents acknowledged work from disappearing.
- Idempotency prevents duplicate business effects.
- Ordering rules prevent stale events from regressing state.
- Queues make work and failures visible.
- Bounded backoff prevents uncontrolled retry.
- Reconciliation resolves uncertain writes.
- Polling repairs gaps caused by outages or expired channels.
- Renewal keeps notification subscriptions active.
- Read-back proves target state.
For Nova, the most important identity is:
Event_Key = Request_Key + ":completed:v1"
A reliable worker must never create a second service-summary target merely because it received a duplicate callback or lost a response.
The production queue, delivery ledger, worker lease, retry scheduler, durable summary module, and receiver deployment remain outside this chapter. The next chapter will address server-side customization within CRM.
The next chapter is:
C02-CH16 — CRM Server-Side Customisation
## Glossary and further reading

Glossary
Acknowledgement
The receiver response indicating that a notification was accepted after safe intake.
At-least-once delivery
A delivery model in which the same event may be delivered more than once.
Backoff
A delay policy between retry attempts.
Blocked
A queue state requiring controlled reconciliation or human action before processing continues.
Channel
A CRM Notification API subscription identified by a channel ID.
Checkpoint
A stored polling position used to determine where the next poll begins.
Deduplication
The process of recognizing repeated delivery of the same logical work.
Event key
A stable business identity for one event, such as Request_Key:completed:v1.
Inbox
A durable intake record for a received notification before asynchronous processing.
Idempotency
The property that repeating the same logical operation does not create another business effect.
Notification condition
A CRM subscription filter that limits notifications to selected fields or operations.
Polling
Periodically reading source records to discover changes or repair event gaps.
Reconciliation
Comparing authoritative source facts and target state to resolve uncertainty.
Retryable
A queue state indicating that a bounded future attempt is allowed.
Webhook
An HTTP endpoint that receives a source system’s callback.
Further reading
- Zoho CRM v8 Notification APIs overview (https://www.zoho.com/crm/developer/docs/api/v8/notifications/overview.html)
- Enable Notifications (https://www.zoho.com/crm/developer/docs/api/v8/notifications/enable.html)
- Get Notification Details (https://www.zoho.com/crm/developer/docs/api/v8/notifications/get-details.html)
- Update Notification Details (https://www.zoho.com/crm/developer/docs/api/v8/notifications/update-details.html)
- Update Specific Notification Information (https://www.zoho.com/crm/developer/docs/api/v8/notifications/update-info.html)
- Disable Notifications (https://www.zoho.com/crm/developer/docs/api/v8/notifications/disable.html)
- Disable Specific Notifications (https://www.zoho.com/crm/developer/docs/api/v8/notifications/specific-disable.html)
- Zoho CRM v8 Get Records (https://www.zoho.com/crm/developer/docs/api/v8/get-records.html)
- Zoho CRM v8 List of Deleted Records (https://www.zoho.com/crm/developer/docs/api/v8/get-deleted-records.html)
- Zoho CRM v8 COQL overview (https://www.zoho.com/crm/developer/docs/api/v8/COQL-Overview.html)
- Zoho CRM v8 COQL query API (https://www.zoho.com/crm/developer/docs/api/v8/Get-Records-through-COQL-Query.html)
- Zoho CRM v8 Composite API (https://www.zoho.com/crm/developer/docs/api/v8/composite-api.html)
