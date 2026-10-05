# Integration and Quality Management


## 1. What you will learn

An integration connects responsibilities as well as applications. You need to know who owns the source information, what the receiving system promises, how failures are handled and what evidence shows the interface behaves correctly.

A successful request is not necessarily a completed business outcome. A receiver may accept a completion handoff while Finance review remains pending. A timeout may occur after the receiver has already committed the work.

By the end of this chapter, you should be able to:

- Define interface ownership and a bounded integration specification.
- Map fields without confusing business names with product API names.
- Specify duplicate, retry and conflict behaviour.
- Build a test strategy covering normal, invalid, permission and failure cases.
- Record defects with reproducible evidence.
- Distinguish severity from priority.
- Explain root cause rather than restating the symptom.
- Retest a correction and run relevant regression checks.
- Produce an integration specification, test pack and defect record.

Prerequisites and continuity

You need the requirements, access plan, migration controls and reference prototype from Chapters 4–10.


| Carried-forward item | Current state |
| --- | --- |
| Finance rule | Service completion does not release an invoice |
| Existing boundary | EVG-BOUNDARY-001 is a proposed manual Finance-review demonstration |
| Live integration | Outside the proposed pilot scope |
| Local prototype | Exercises business rules; does not prove Zoho behaviour |
| Native design | Conditional; entry-path and related-record proof pending |
| EVG-CHANGE-004 | Automatic customer notification requested, not approved |
| EVG-DEFECT-001 | Reserved before this chapter; no prior observed product failure |
| Product authority | No Zoho configuration, tokens, API calls or tenant inspection authorised |
| Migration exceptions | C04 unresolved; cancellation group held |
| Estimates | Conditional proposals; not an approved delivery baseline |

EVG-SRC-097 authorises a local interface simulator and quality artifacts. EVG-SRC-104 requests assessment of an automated handoff as EVG-CHANGE-005. Neither authorises a live interface.

Your project contribution

You will add:

1. A logical interface specification.
2. A mapping and ownership table.
3. A retry and reconciliation policy.
4. A test strategy and evidence register.
5. A reproduced reference-model defect and correction.
6. A release-boundary recommendation.

All business facts and messages are synthetic. Local reference execution is distinct from Zoho execution, client UAT and acceptance. The worked defect in this chapter concerns the supplied local receiver, not a Zoho product defect.


## 2. Lessons


### 2.1 Define the interface promise and its owners

Skill: state what crosses the boundary and what the receiver guarantees.

An interface contract defines the information, behaviour and responsibilities at a boundary.

It should answer:

- What business event causes a message?
- Which system owns each value?
- Who may send and receive it?
- What makes the message valid?
- What does acknowledgement mean?
- How are duplicates, conflicts and failures handled?
- Who investigates unresolved delivery?

For Evergreen, the proposed event is:

A qualified service-completion handoff is available for Finance.

The receiver’s promise is narrower:

Record the handoff and make one review item available for that event.

It does not promise:

Finance has approved the job or released an invoice.

Separate transport acknowledgement, receipt and business completion:


| Stage | Meaning |
| --- | --- |
| Request accepted for processing | The receiving service has accepted the request, possibly asynchronously |
| Handoff recorded | Receipt evidence exists for the business event |
| Finance review complete | Finance has made the review decision |
| Invoice release | Separate Finance action outside this simulator |

Zoho’s common status documentation describes HTTP 202 as accepted while processing may take time.2 Do not interpret it as a completed business review.

Ownership should include both business and technical roles. Operations owns the source job/customer relationship; Technician Lead owns completion facts; Finance owns review decisions. The Developer owns the local adapter implementation, while the Implementation Lead coordinates interface issues.

Lesson check LC1: Why should a handoff receipt not be displayed as “Finance approved”?


### 2.2 Map meaning, identifiers and allowed information

Skill: specify an interface payload that preserves business meaning.

A message should contain the information the receiver needs, not an unrestricted copy of the source record.

For Evergreen, that includes job/customer references, completion information and an event identifier. It excludes cost, margin and private Finance reasons.

A message identifier identifies one immutable business event. A job identifier identifies the job. One job can produce multiple events, such as an initial completion handoff and a later correction.

A source revision orders the relevant source changes. It is not automatically a Zoho record version or Modified_Time.

Keep these distinctions explicit:


| Identifier | Purpose |
| --- | --- |
| EVG-JOB-2001 | Business job |
| EVG-EVENT-001 | One interface event |
| Source revision 1 | Business revision represented by the event |
| SIM-RECEIPT-001 | Local simulator receipt |
| Product record ID | Actual product identifier; unallocated here |

The interface fields below are logical contract names. They are not invented Zoho API field names.

If a future adapter uses CRM upsert, it must use actual module/field API names and verified duplicate-check fields.1 Upsert matching can update a record, but it does not by itself define the complete business duplicate policy.

Lesson check LC2: Why should a corrected handoff have a new event identity rather than reuse an accepted event with changed content?


### 2.3 Specify duplicate and retry behaviour

Skill: distinguish repeated delivery from repeated business work.

A duplicate delivery repeats the same event and payload. An idempotent operation produces the same intended effect when repeated.

For this contract:

- Same event ID and same payload: acknowledge the existing receipt.
- Same event ID and different payload: collision; do not overwrite.
- New event with an older or equal source revision: hold as stale.
- New valid event with a later revision: record it and create its review item.

A unique receipt record is not enough. If a duplicate request creates another review item, the integration still repeats business work.

A timeout introduces uncertainty:

- The receiver may not have committed.
- It may have committed but lost the acknowledgement.
- The sender may not know which occurred.

Use receipt lookup where available. If lookup is unavailable and retry is permitted, resend the same immutable event—not a new event ID and not a payload with a refreshed event timestamp.

In a production design, durable event tracking and coordinated side effects must survive process restarts and concurrency. The in-memory simulator does not establish those guarantees.

Lesson check LC3: Why is “one stored record” insufficient evidence that duplicate handling is correct?


### 2.4 Treat errors and partial results by category

Skill: choose correction, retry or escalation from the actual outcome.

Do not retry every error automatically.


| Condition | Appropriate treatment |
| --- | --- |
| Missing or invalid business data | Hold; obtain authorised correction |
| Permission or scope problem | Block; route to the identity owner |
| Same ID with different payload | Hold collision; inspect immutable-event handling |
| Stale revision | Preserve current data; obtain an owner decision if needed |
| Timeout or uncertain server outcome | Investigate receipt; use bounded immutable retry |
| Exhausted retry budget | Manual hold and escalation |
| Partial batch success | Account for each row; do not resend the accepted subset blindly |

Zoho CRM upsert documents per-record results and HTTP 207 for partial success. Results retain input order, allowing correlation to submitted records.1 A batch-level status does not replace row-level accounting.

The same documentation distinguishes scope, permission, validation and modified-record errors. Use the endpoint’s actual response, not a generic assumption that every 4xx or 5xx means the same thing.

For authorised readback, CRM Get Records supports retrieving a specific record by actual module API name and product record ID.3 The simulator’s event lookup is a separate logical operation, not a claimed Zoho endpoint.

Lesson check LC4: What should happen when two of three batch rows succeed?


### 2.5 Build a layered quality strategy

Skill: link tests to risks and requirements.

A test strategy explains what will be tested, at which level, with which data and evidence.

Evergreen needs several layers:


| Layer | Main question |
| --- | --- |
| Mapping/contract checks | Are required values, identities and relationships valid? |
| Receiver component checks | Are duplicate, collision and revision rules enforced? |
| Adapter integration checks | Are requests/results translated and correlated correctly? |
| End-to-end checks | Does qualified completion reach review without invoice release? |
| Access and information checks | Are permitted identities and projections respected? |
| Recovery checks | What happens before commit, after commit and after retry exhaustion? |

Use requirement links. A test should explain which condition it demonstrates.

Test evidence needs the build/version, input, expected result, observed result and relevant environment. Label paper-derived results separately.

Business-led UAT comes in Chapter 13. Supplier checks should make that activity possible, not pretend to replace it.

Lesson check LC5: Which checks would a happy-path handoff test miss?


### 2.6 Record defects, root cause and retest

Skill: make a failure reproducible and its correction accountable.

A defect is observed nonconformance against the applicable requirement or contract.

Record:

- Stable defect ID.
- Requirement and test links.
- Version/environment.
- Reproduction steps and input.
- Expected and observed behaviour.
- Impact, severity and priority.
- Owner.
- Root cause and correction.
- Retest/regression evidence.

Severity describes impact. Priority describes when the issue should be addressed.

Use this synthetic classification for the exercises:


| Severity | Exercise meaning |
| --- | --- |
| S1 Critical | Protected-information exposure or unintended live financial action |
| S2 High | Essential workflow blocked or duplicated business work |
| S3 Moderate | Nonessential behaviour impaired with a controlled workaround |
| S4 Low | Presentation issue without workflow/control impact |

These are educational definitions, not a Wooplix incident policy.

“Timeout caused a duplicate” is a symptom description. A root cause explains why the implementation repeated the effect.

Retesting reruns the original failing case against the correction. Regression testing checks related behaviours that the change could affect.

Do not close a defect merely because code changed.

Lesson check LC6: Why are retest and regression both needed after changing the duplicate branch?


## 3. Visual explanation: uncertain delivery


```mermaid
sequenceDiagram
    participant S as Sender
    participant R as Receiver
    participant J as Event journal
    participant F as Review work
    S->>R: Immutable event
    R->>J: Record event and payload fingerprint
    R->>F: Create one review item
    R--xS: Acknowledgement lost
    S->>R: Same event, same payload
    R->>J: Find existing event
    R-->>S: Existing receipt; no new review item
```

The lost acknowledgement does not undo the receiver’s work.

The retry must find the existing event and suppress another review item. A production implementation needs durable coordination between event recording and side effects. The local example tests only the supplied in-memory behaviour.


## 4. Worked case: specify and reproduce the interface defect


### 4.1 Completed ownership and boundary

EVG-SRC-098 supplies these responsibilities.


| Responsibility | Owner |
| --- | --- |
| Source job/customer relationship | Operations Manager |
| Completion facts | Technician Lead |
| Receiving review process | Finance Lead |
| Local adapter/receiver | Developer, Riley Park |
| Test evidence and retest | Quality Lead, Sam Torres |
| Coordination and escalation | Implementation Lead, Jordan Ellis |
| Future connection authority | Client Administrator |
| Scope decision | Client Sponsor |

EVG-IF-001 v0.1 — proposed logical interface


| Specification field | Completed definition |
| --- | --- |
| Purpose | Record qualified completion events for Finance review |
| Current transport | Local Receiver.receive() call |
| Future endpoint | Not selected; live Finance system remains unidentified |
| Sender identity | Local label handoff_writer; not real authentication |
| Business acknowledgement | Received, not reviewed or invoice-approved |
| Allowed content | Eight contract fields listed below |
| Restricted content | Cost, margin and private Finance reason |
| Event handling | Immutable key plus payload comparison |
| Ordering | New accepted source revision must exceed the current revision |
| Retry budget | Initial attempt plus at most two retries |
| Retry delays | 30 seconds, then 120 seconds, measured after failed-attempt completion |
| Timeout | Five seconds per attempt in the supplied timing exercise |
| Exhaustion | Manual hold; Implementation Lead coordinates escalation |
| Retention | Lifetime of the local fixture; production retention unresolved |
| Scope status | Assessment only, EVG-CHANGE-005 not approved |

These retry values are synthetic contract inputs, not Zoho limits.


### 4.2 Complete mapping and message

EVG-SRC-099 supplies the schema and recognised relationships:

- EVG-JOB-2001 → EVG-CUST-0101.
- EVG-JOB-2002 → EVG-CUST-0102.
- EVG-JOB-2003 → EVG-CUST-0103.

| Contract field | Meaning/validation |
| --- | --- |
| schema_version | Exactly "1.0" |
| event_id | Nonblank immutable event reference |
| job_ref | Recognised business job reference |
| customer_ref | Must agree with the job relationship |
| source_revision | Positive integer; not a product version |
| completed_on | ISO date, not after event date |
| summary | Nonblank completion summary |
| occurred_at | UTC business-event timestamp; unchanged on retry |

Unexpected fields are rejected rather than silently copied.

Message A:

{

  "schema_version": "1.0",
  "event_id": "EVG-EVENT-001",
  "job_ref": "EVG-JOB-2001",
  "customer_ref": "EVG-CUST-0101",
  "source_revision": 1,
  "completed_on": "2027-01-28",
  "summary": "Replaced filter",
  "occurred_at": "2027-01-28T09:00:00Z"
}


### 4.3 Runnable local receiver

EVG-SRC-100 supplies two reference versions. V1 deliberately contains a duplicate-side-effect defect. V2 corrects it.

Save as evergreen_interface.py and run with Python 3.7 or later:


```bash
python3 evergreen_interface.py
```

No packages, credentials, network calls or files beyond the script are required.


```python
from copy import deepcopy
from datetime import date, datetime
import hashlib
import json

FIELDS = {
    "schema_version", "event_id", "job_ref", "customer_ref",
    "source_revision", "completed_on", "summary", "occurred_at"
}
JOBS = {
    "EVG-JOB-2001": "EVG-CUST-0101",
    "EVG-JOB-2002": "EVG-CUST-0102",
    "EVG-JOB-2003": "EVG-CUST-0103"
}
A = {
    "schema_version": "1.0", "event_id": "EVG-EVENT-001",
    "job_ref": "EVG-JOB-2001", "customer_ref": "EVG-CUST-0101",
    "source_revision": 1, "completed_on": "2027-01-28",
    "summary": "Replaced filter", "occurred_at": "2027-01-28T09:00:00Z"
}


def fingerprint(message):
    text = json.dumps(message, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Receiver:
    def __init__(self, version="V2"):
        self.version = version
        self.receipts, self.latest, self.review_items = {}, {}, []
        self.invoice_releases = 0

    def receive(self, message, identity="handoff_writer", fault=None):
        if identity != "handoff_writer":
            return {"outcome": "DENIED"}
        if not isinstance(message, dict) or set(message) != FIELDS:
            return {"outcome": "INVALID"}

        strings = FIELDS - {"source_revision"}
        if any(not isinstance(message[k], str) or not message[k].strip()
               for k in strings):
            return {"outcome": "INVALID"}
        if (message["schema_version"] != "1.0"
                or type(message["source_revision"]) is not int
                or message["source_revision"] < 1):
            return {"outcome": "INVALID"}
        if JOBS.get(message["job_ref"]) != message["customer_ref"]:
            return {"outcome": "INVALID"}

        try:
            occurred = datetime.fromisoformat(
                message["occurred_at"].replace("Z", "+00:00")
            )
            if (occurred.utcoffset() is None
                    or occurred.utcoffset().total_seconds() != 0
                    or date.fromisoformat(message["completed_on"])
                    > occurred.date()):
                return {"outcome": "INVALID"}
        except (TypeError, ValueError):
            return {"outcome": "INVALID"}

        key, digest = message["event_id"], fingerprint(message)
        existing = self.receipts.get(key)
        if existing:
            if existing["fingerprint"] != digest:
                return {"outcome": "COLLISION"}
            if self.version == "V1":
                self.review_items.append(key)  # Deliberate model defect
            return {
                "outcome": "DUPLICATE",
                "receipt_ref": existing["receipt_ref"],
                "finance_status": "Received"
            }

        current = self.latest.get(
            message["job_ref"], {}
        ).get("source_revision", 0)
        if message["source_revision"] <= current:
            return {"outcome": "STALE"}
        if fault == "before_commit":
            raise TimeoutError("Simulated timeout before commit")

        receipt = "SIM-RECEIPT-{:03d}".format(len(self.receipts) + 1)
        self.receipts[key] = {
            "fingerprint": digest, "receipt_ref": receipt,
            "job_ref": message["job_ref"]
        }
        self.latest[message["job_ref"]] = {
            "source_revision": message["source_revision"],
            "summary": message["summary"]
        }
        self.review_items.append(key)

        if fault == "after_commit":
            raise TimeoutError("Simulated acknowledgement loss after commit")
        return {
            "outcome": "ACCEPTED",
            "receipt_ref": receipt, "finance_status": "Received"
        }

    def lookup(self, event_id):
        receipt = self.receipts.get(event_id)
        return deepcopy(receipt) if receipt else None

    def public(self, event_id):
        receipt = self.receipts[event_id]
        return {
            "job_ref": receipt["job_ref"],
            "handoff_status": "Received",
            "finance_contact": "finance@evergreen.example.com"
        }


def replay_probe(version):
    receiver = Receiver(version)
    try:
        receiver.receive(A, fault="after_commit")
    except TimeoutError:
        pass
    # The fixture assumes receipt lookup is unavailable to the sender.
    retry = receiver.receive(A)
    return {
        "version": version, "retry": retry["outcome"],
        "stored_events": len(receiver.receipts),
        "review_items": len(receiver.review_items),
        "invoice_releases": receiver.invoice_releases
    }


if __name__ == "__main__":
    for version in ("V1", "V2"):
        print(json.dumps(replay_probe(version), sort_keys=True))
```

The fingerprint compares payload content. It is not a signature, credential or authentication mechanism.

The local identity string and in-memory journal also do not provide real authentication, durability or concurrency guarantees.


### 4.4 Reproduced reference result

The supplied reference fixture produces:

{"invoice_releases": 0, "retry": "DUPLICATE", "review_items": 2, "stored_events": 1, "version": "V1"}

{"invoice_releases": 0, "retry": "DUPLICATE", "review_items": 1, "stored_events": 1, "version": "V2"}

These outcomes were reproduced in a local Python reference check. They are not tenant, client or financial-system observations.

For each version:


> 2 deliveries=1 initial attempt+1 retry

V1 records one event but creates two review items. V2 records one event and creates one review item.

The receipt count alone would conceal V1’s defect.


### 4.5 Completed defect record

EVG-DEFECT-001 — duplicate review work in reference receiver V1


| Field | Completed content |
| --- | --- |
| Requirement | Candidate EVG-REQ-016: reliable event handoff without repeated work or uncontrolled overwrite |
| Test | EVG-TEST-029 |
| Environment/version | Local in-memory receiver V1 |
| Input | Message A; timeout after commit; immutable retry |
| Expected | One receipt and one review item |
| Observed reference result | One receipt and two review items |
| Severity | S2 High: duplicated essential review work |
| Priority | Correct before treating the reference duplicate path as valid |
| Owner | Developer |
| Root cause | V1 appends review work in the existing-event branch |
| Correction | Return existing receipt without appending another review item |
| Retest | Original after-commit timeout/retry fixture in V2 |
| Retest result | One receipt and one review item |
| Product status | No Zoho defect or product retest claimed |

The timeout is the trigger, not the root cause. The duplicate branch causes the repeated work.

The local correction is not enough to claim a production guarantee. Durable journal and side-effect coordination still need design and verification.

Record EVG-DEC-031: acknowledgement means Received only; Finance review remains separate.

Record EVG-DEC-032: use immutable event identity and verify both receipt and side-effect counts.

A mistake and its correction

Mistake: “Upsert prevents duplicate records, so retries are safe.”

Correction: “Record matching is one part of the design. Verify repeated requests, side effects, changed payloads, revision order and configured automation.”


## 5. Try it yourself — guided practice

Learning goal and access

Complete the interface test pack and assess partial results.

Use the code, an editor and Python. Without a runtime, label outcomes paper-derived. No Zoho access is required.

Complete test inputs

Use a fresh Receiver("V2") for each isolated case.


| Test | Input and action |
| --- | --- |
| EVG-TEST-026 | Submit A normally |
| EVG-TEST-027 | Submit dict(A, summary="") |
| EVG-TEST-028 | Submit A with identity metadata_reader |
| EVG-TEST-029 | Submit A with after_commit, catch timeout, resend unchanged A |
| EVG-TEST-030 | Accept A, then resend same ID with summary “Different summary” |
| EVG-TEST-031 | Accept event 003 for job 2001, revision 2, summary “Replaced filter and checked airflow”; then submit event 004 with A’s revision 1 values |
| EVG-TEST-032 | Submit A with before_commit, catch timeout, resend A |
| EVG-TEST-033 | Submit dict(A, finance_reason="Private") |

For events 003 and 004, all fields not specified above are copied from A.

A separate valid Message B is supplied:

{

  "schema_version": "1.0",
  "event_id": "EVG-EVENT-005",
  "job_ref": "EVG-JOB-2002",
  "customer_ref": "EVG-CUST-0102",
  "source_revision": 1,
  "completed_on": "2027-01-28",
  "summary": "Reset controller",
  "occurred_at": "2027-01-28T09:05:00Z"
}

EVG-SRC-101 supplies a synthetic future-adapter response-correlation exercise. It is not a captured API result.


| Input position | Business event | Submitted summary |
| --- | --- | --- |
| 1 | EVG-EVENT-011, job 2001/customer 0101, revision 1 | Replaced filter |
| 2 | EVG-EVENT-012, job 2002/customer 0102, revision 1 | Blank |
| 3 | EVG-EVENT-013, job 2003/customer 0103, revision 1 | Checked pump |

All three have schema 1.0, completion date 28 January and event time 09:10 UTC. The illustrative batch status is HTTP 207. The exercise assumes the future adapter’s approved validation requires the summary.

Guided steps

1. Run and record the eight local cases.  

Capture version, input, outcome and both counts.

2. Inspect public output.  

Confirm that public() returns only the allowed projection.

3. Retest the original defect.  

Compare V1 and V2 with the same fault placement and payload.

4. Assess regression.  

Ensure the correction did not weaken invalid, permission, collision or stale handling.

5. Correlate the batch rows.  

Expected: two accepted rows and one correction hold, not a whole-batch retry.

6. Complete the evidence and recommendation.  

Distinguish local execution from the paper adapter exercise and unperformed product tests.

Blank test-evidence worksheet


| Test ID | Requirement | Version/environment | Input | Expected | Observed or paper result |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

Blank defect worksheet


| Field | Your entry | Guidance |
| --- | --- | --- |
| ID and requirement/test links |  | Stable records |
| Version and reproduction |  | Exact input, identity and fault |
| Expected/observed |  | Separate the two |
| Impact/severity/priority |  | Explain business consequence |
| Root cause/correction |  | Mechanism, not symptom |
| Retest/regression |  | Same failing case and relevant neighbours |
| Closure boundary |  | Local, product or client evidence |

Final artifacts: EVG-IF-001 v0.2, a test pack and EVG-DEFECT-001’s reference retest record.

Cleanup: new receiver instances reset all state. Retain code and evidence versions. No external record cleanup is needed.


## 6. Independent challenge

Changed sender behaviour

EVG-SRC-102 supplies Message K:

{

  "schema_version": "1.0",
  "event_id": "EVG-EVENT-007",
  "job_ref": "EVG-JOB-2003",
  "customer_ref": "EVG-CUST-0103",
  "source_revision": 1,
  "completed_on": "2027-01-28",
  "summary": "Inspected valve",
  "occurred_at": "2027-01-28T09:20:00Z"
}

Use a fresh V2 receiver.

- Initial attempt starts at 09:20:00 and times out at 09:20:05 after commit.
- Receipt lookup is unavailable at that point.
- The sender wrapper incorrectly creates its retry with:
retry_payload = dict(K, occurred_at="2027-01-28T09:20:35Z")

- No other value changes.
- At 09:20:40, authorised lookup becomes available and returns the original event’s receipt and fingerprint.
- No business correction to K is authorised.

Retry-exhaustion inputs

A separate fresh receiver is used for event 008:

- Job EVG-JOB-2002, customer EVG-CUST-0102, revision 1.
- Schema 1.0; completed date 28 January.
- Summary “Checked pump.”
- occurred_at remains 2027-01-28T09:30:00Z.
- Initial attempt starts 09:30:00.
- Every attempt lasts five seconds and fails before commit.
- All receipt lookups remain unavailable.
- Apply the specified 30-second and 120-second delays after failed-attempt completion.
- No further retries are permitted.

EVG-SRC-103 confirms that Received is not Finance review complete. No live financial action or new support service is authorised.

Deliverables

Produce:

1. Expected outcome and counts for K’s altered retry.
2. Sender diagnosis and safe correction.
3. A proposed EVG-DEFECT-002 entry for the sender wrapper, marked pending recorded reproduction if you do not run it.
4. Exact retry start/finish times for event 008.
5. Final sender/receiver states and ownership.
6. A release recommendation.

Success criteria

Do not classify correct collision rejection as a receiver defect. Preserve the original event content and do not create another review item.

Stop after the stated retry budget. Do not call an unresolved delivery Finance-approved or invent a recovery result.


## 7. Common problems and recovery


| Symptom | Diagnosis | Correction |
| --- | --- | --- |
| One receipt but two review tasks | Side effect not deduplicated | Suppress work for an existing identical event |
| Retry becomes a collision | Sender changed immutable content | Preserve original payload; inspect wrapper |
| Validation error retried repeatedly | Error category ignored | Hold for business correction |
| Permission failure treated as outage | Identity issue misclassified | Route to Administrator/connection owner |
| Older revision overwrites current | Ordering rule absent | Hold stale event |
| Whole batch resent after 207 | Per-row evidence ignored | Correlate results and recover only affected rows |
| Defect closed after code change | Retest missing | Repeat original fixture and relevant regression |
| Retry budget exhausted silently | Ownership incomplete | Manual hold and escalation |
| Received displayed as approved | Transport/business states conflated | Separate receipt and Finance outcome |

A source correction creates an authorised new event or revision according to the contract. It is not a reason to mutate an accepted event.

Local reset recreates a simulator. It does not reverse a financial transaction, recover a persistent journal or recall an external notification.


## 8. Check your understanding

1. What must an interface specification say about acknowledgement?
2. Why is event identity different from job identity?
3. What is the difference between a duplicate and a collision?
4. Why can a timeout be consistent with successful receipt?
5. What makes a defect record reproducible?
6. How do severity and priority differ?
7. Why is “network timeout” not the root cause of V1’s duplicated work?
8. Which evidence is still needed before a live Evergreen handoff can be approved?

## 9. Solutions and explanations


### 9.1 Lesson checks

LC1: Receipt shows that handoff information was recorded. Finance has not necessarily reviewed it or made an invoice decision.

LC2: An accepted event represents immutable content. A correction is a different business event; changing accepted content under the same ID causes ambiguity.

LC3: Side effects such as review tasks can repeat even when a unique receipt prevents duplicate records.

LC4: Preserve the two accepted results, hold/correct the failed row and correlate its recovery separately.

LC5: Missing data, wrong identity, repeated delivery, altered payload, revision order, partial outcome and recovery.

LC6: Retest proves the original failure is corrected. Regression checks whether the changed branch damaged related controls.


### 9.2 Guided practice solution

The eight V2 receiver cases were reproduced in a local reference verification. Their result categories are:


| Test | Result | Receipt/work state |
| --- | --- | --- |
| 026 | ACCEPTED | 1 / 1 |
| 027 | INVALID | 0 / 0 |
| 028 | DENIED | 0 / 0 |
| 029 | DUPLICATE after lost acknowledgement | 1 / 1 |
| 030 | COLLISION | Original 1 / 1 unchanged |
| 031 | STALE | Revision 2 retained; 1 / 1 |
| 032 | Timeout before commit, then ACCEPTED | 0 / 0 before retry; 1 / 1 after |
| 033 | INVALID | 0 / 0 |

These are local component results. Product and client checks remain unperformed.

The public projection for A is:


| Job reference | Handoff status | Finance contact |
| --- | --- | --- |
| EVG-JOB-2001 | Received | finance@evergreen.example.com |

Batch correlation


> 3 rows=2 accepted+1 rejected


> Accepted-row proportion=(2) ÷ (3)×100≈66.67%

This describes the supplied batch only, not overall quality or release readiness.

Positions 1 and 3 remain accepted. Position 2 requires an authorised summary correction and appropriate new-event treatment. Do not replay the complete batch blindly.

Retest conclusion

EVG-DEFECT-001 is corrected and retested within the local reference receiver. The V2 duplicate branch preserves one review item.

Record EVG-DEC-033: retain per-row and side-effect evidence; local regression does not close product-readiness gaps.


### 9.3 Independent challenge solution

Altered retry

K’s initial attempt records one event and review item before acknowledgement loss.

Changing occurred_at changes the payload fingerprint. V2 returns COLLISION. Counts remain one receipt and one review item.

The receiver is enforcing the contract correctly. The sender wrapper is defective because it replaces business-event time with retry-attempt time.

Use separate fields in the sender’s attempt log for attempt timestamps. Keep K unchanged.

When lookup becomes available, compare its original receipt/fingerprint with the original K. If they agree, record Received and stop delivery retries. No new event or review item is required.

Proposed EVG-DEFECT-002


| Field | Entry |
| --- | --- |
| Component | Local sender retry wrapper |
| Contract | Immutable event payload |
| Test | Altered-timestamp retry of K |
| Expected | Retry uses original occurred_at; existing receipt recognised |
| Supplied behaviour | Wrapper changes timestamp, causing collision |
| Severity | S2 High: recovery path blocked |
| Owner | Developer |
| Correction | Preserve original message; record attempt time separately |
| Status | Proposed pending recorded reproduction, or opened as a local defect after reproduction |
| Boundary | Not a Zoho or receiver defect |

Exhaustion schedule

Initial attempt:


> 09{:}30{:}00+5 seconds=09{:}30{:}05

First retry:


> 09{:}30{:}05+30 seconds=09{:}30{:}35

It finishes at 09:30:40.

Second retry:


> 09{:}30{:}40+120 seconds=09{:}32{:}40

It finishes at 09:32:45.


| Attempt | Start | Finish |
| --- | --- | --- |
| Initial | 09:30:00 | 09:30:05 |
| Retry 1 | 09:30:35 | 09:30:40 |
| Retry 2 | 09:32:40 | 09:32:45 |

Three attempts exhaust the budget. The receiver has zero receipts and zero review items in the supplied fixture.

The sender enters Manual hold. The Implementation Lead coordinates technical investigation with the Developer and relevant client support owner. Finance review has not begun.

A suitable recommendation is:

The local receiver correction passes its reference checks, but the sender retry wrapper needs correction and reproduction evidence. Exhausted delivery remains visible as Manual hold. A live interface still requires scope approval, identified systems, authorised identities, durable recovery and actual end-to-end evidence.

Record EVG-DEC-034: stop at retry exhaustion and preserve unresolved work under named ownership.


### 9.4 Understanding check answers

1. Whether acknowledgement means request acceptance, recorded receipt or completed business action.
2. One job can produce several immutable events.
3. A duplicate has the same ID/content. A collision has the same ID but different content.
4. The receiver may commit before its acknowledgement is lost.
5. Exact version, environment, identity, inputs, steps, expected and observed results.
6. Severity measures impact; priority determines treatment order.
7. Timeout exposes the path. V1’s duplicate branch creates the second review item.
8. Approved scope, actual mappings/endpoints, identities, permissions, durable duplicate/recovery design, product checks and appropriate business acceptance.

## 10. Chapter recap and next step

Integration quality depends on a clear promise and evidence that survives exceptions.

You should be able to explain what an acknowledgement means, how one event is recognised across retries, who owns correction and how unresolved work remains visible.

Completion checklist

- I can define interface ownership and allowed information.
- I can distinguish event, job and product identifiers.
- I can specify duplicate, collision and stale behaviour.
- I can handle partial and uncertain results.
- I can produce traceable test evidence.
- I can distinguish severity, priority and root cause.
- I can retest a defect and check related behaviour.
- I can state local verification and production limits honestly.

Your project pack now contains an interface specification, test pack and reference defect evidence.

Chapter 12, Scope Change and Communication, uses the notification, reporting, multi-site and proposed integration requests to practise impact analysis, approvals, risk/issue communication and steering decisions.


## 11. Glossary and further reading

Glossary


| Term | Meaning |
| --- | --- |
| Collision | Same event ID received with different content |
| Contract test | Check of agreed interface structure and behaviour |
| Duplicate delivery | Repetition of an identical event |
| Fingerprint | Derived value used to compare payload content |
| Idempotency | Repetition without additional unintended effect |
| Interface contract | Defined information, behaviour and responsibilities at a boundary |
| Regression | Checking related behaviour after a change |
| Retest | Repeating the original failing case after correction |
| Root cause | Mechanism that explains the failure |
| Severity | Impact classification |
| Stale event | Event representing a revision that should not replace current data |
| Unresolved outcome | Delivery whose effect is not yet known |

Further reading

1. Zoho CRM API v8 — Upsert Records  
[Open official reference](https://www.zoho.com/crm/developer/docs/api/v8/upsert-records.html)

Matching, validation/feature conditions, per-record results and partial success.

2. Zoho CRM API v8 — Common Status Codes  
[Open official reference](https://www.zoho.com/crm/developer/docs/api/v8/status-codes.html)

Accepted processing, multi-status and error categories.

3. Zoho CRM API v8 — Get Records  
[Open official reference](https://www.zoho.com/crm/developer/docs/api/v8/get-records.html)

Authorised readback using actual module and product record identifiers.

Consult the official references above for current product details. Confirm the applicable edition, permissions and environment before using product-specific procedures. The local reference checks do not establish Evergreen’s Zoho adapter, actual financial endpoint, authentication or production behaviour. No Zoho execution or client acceptance is claimed.
