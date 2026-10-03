# Reliable Synchronization Worked Teaching Example

Module ZDV M09

## Learner scenario

A fictional service application sends request SR 104 to a destination system. The destination creates record D 900, but the response is lost. The source cannot tell whether the write succeeded. A retry must not create a second service request.

## Trainer walkthrough

Show why blindly retrying a create request can duplicate a business operation. Define a stable business key, such as the source request ID plus source system. Record that key at the destination if the destination supports a unique field or an idempotency contract. Before a retry, query or reconcile by that key. A search followed by create is not enough to guarantee uniqueness under concurrent writers; a destination enforced unique constraint or an equivalent atomic operation is needed.

Use pseudocode to teach the design. First validate the payload and business key. Then request an idempotent create or update if the destination supports it. Store the destination ID and completion state. On timeout, reconcile by key before replaying. Retry only transient failures within a bound; put invalid data into a review queue. Verify the selected Zoho API behavior and edition before translating this design into Deluge.

## Guided test fixture

Event E1 carries SR 104 with customer C 12. Event E2 repeats E1. Event E3 times out after the destination commit. Event E4 has no business key. Event E5 conflicts with a newer destination status. Use materials/sync_events.json. A deterministic mock can model these responses without credentials.

## Independent assignment

Design a synchronization state table and replay procedure. Demonstrate an initial create, duplicate event, lost response, invalid payload and conflicting update. Submit design, pseudocode, five test results and an operator recovery note. Time budget is two hours. A deeper code build belongs in the capstone if it cannot fit this module budget.

## Expected outcomes

The initial create yields one destination business record. The duplicate resolves to the same record. The lost response is reconciled before any new write. The missing key produces a validation failure, with no write. A conflict follows a documented ownership rule or goes to review. Correctness does not depend on assuming all retries are safe.

## Common mistakes

Generating a new key on each retry; treating every error as transient; logging access tokens; claiming that search then create prevents races; and silently overwriting newer data. Use documented API contracts and current quota information when implementing the design. Sources S02 S03 S04.
