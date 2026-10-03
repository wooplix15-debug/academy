# Nova Services case brief
Nova is a fictional service business for teaching. Values, names, policies and examples are synthetic. The team may replace them with reviewed Wooplix experience.
## Business journey
Inquiry arrives, sales qualifies it, a quote is reviewed, a deal is won, a delivery request is created and service work is completed. Managers need evidence of routing, data quality, follow up and delivery status.
## Proposed requirements
- R01 Sales Operations owns region routing. West and East route to their sales queues; blank or unknown region routes to Review Queue.
- R02 Sales Manager owns qualification. A deal cannot progress to quote without a recorded service need and contact method.
- R03 Sales Manager owns quote review. Amount greater than INR 50000 requires approval. Exactly INR 50000 uses the normal route.
- R04 Data Steward owns import quality. Lab name, company and valid email are required; normalized email duplicates keep the first valid occurrence.
- R05 Administrator owns access. Sales reads and edits its assigned regional records; manager reviews both regions. Export and administrative permissions are separately decided and tested.
- R06 Delivery Lead owns handoff. Each won deal has one delivery request identified by NOVA plus stable deal ID. Replay must not create a second request.
- R07 Department owners agree field authority. CRM owns amount; the service app owns technician and completion status.
- R08 Sponsor owns release acceptance. Eight core UAT scenarios require evidence and no unresolved critical access or unintended-write defect.
## Interview cards
Sales Manager: I want faster response and fewer lost leads. Ask which clock, working days and ownership apply; do not assume a four-hour SLA is agreed.
Sales Representative: I edit contact details after creation and worry about repeated tasks. Ask which updates should retrigger follow up.
Data Steward: We have duplicate emails and incomplete files. Ask which matching rule and exception owner apply.
Delivery Lead: Retries create confusing handoffs. Ask which key, field owner and recovery rule apply.
## Unresolved decisions
Working-hours calendar, qualification minimums, quote modification after approval, export policy, actual Zoho edition and pilot date require sponsor or trainer confirmation.
## Portfolio structure
requirements/ design/ configuration/ migration/ integration/ tests/ handover/
Keep a requirement ID in each relevant artifact. Store synthetic IDs and redacted evidence. Name environment, product edition, API version, date, tester and observed result in live-product test records.
