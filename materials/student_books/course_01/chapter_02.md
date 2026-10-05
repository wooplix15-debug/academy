# Zoho Ecosystem and Solution Selection

## 1. What you will learn

A connected business process needs more than a collection of applications. It needs clear answers to questions such as:
- Where should a new enquiry be recorded?
- Which application holds the customer’s approved billing information?
- Who is allowed to change an invoice?
- Where should a service agent update a ticket?
- How should information move between applications?
- Which application’s record should a report trust when two copies disagree?
Without these decisions, adding applications can create more work. Teams may enter the same information several times, maintain conflicting customer details, or assume that a record visible in one application is automatically synchronized with another.
In this chapter, you will learn how to select applications around a business process and define their responsibilities.
By the end, you should be able to:
1. Explain the different roles of Zoho CRM, Books, Desk, People, Flow, Creator and Analytics.
2. Explain what Zoho One administration contributes to a connected solution.
3. Translate process requirements into application-selection criteria.
4. Identify the authoritative application for each record or clearly defined part of a record.
5. Distinguish a business identifier from an application-generated identifier.
6. Choose between a controlled manual handoff, a native integration, a Flow workflow and an analytical connector.
7. Produce an application map, ownership matrix, integration decision sheet and initial access plan.
8. Trace a normal case, missing-data case, duplicate, denied action and mapping exception through your design.
Prerequisites
You need basic spreadsheet and web application skills. No coding or Zoho subscription is required for this chapter’s practice.
You should understand these discovery concepts:
- A trigger starts a process instance.
- An endpoint provides evidence that the process has finished.
- A handoff transfers work and responsibility.
- An exception prevents the normal route from continuing.
- A current-state map describes existing work.
- A future-state map describes proposed changes.
The chapter supplies the Meridian information needed for the exercises. You do not need to retrieve an earlier worksheet to answer them.
Continuity from Chapter 1
The Chapter 1 draft established the following synthetic case rules and starting measurements:
| Established item | Meridian position |
| --- | --- |
| Detailed process scope | Written order confirmation to Finance acceptance of the billing packet |
| Sales participant | Ava prepares, submits and corrects packets |
| Finance participant | Leo reviews packets and alone records Finance acceptance |
| Process owner | Noor coordinates process improvement and unresolved queue ownership |
| Required packet information | Order ID, customer ID, quote ID, confirmation reference, confirmed billing email and installation flag |
| Repeated confirmation | An unchanged repeat links to the existing order; it does not create another case |
| Correction | A corrected packet preserves the original order ID |
| Baseline cutoff | 14 September 2026, 17:00 UTC |
| Baseline position | Four accepted orders and two open orders |
| Completed-case measurements | Mean elapsed time: 195 minutes; first-pass acceptance: 50% |
| Proposed pilot | Ten consecutive unique confirmations received 09:00–15:00 on one training day |
| Proposed targets | Mean no more than 120 minutes; first-pass at least 90%; all ten accepted by 17:00 |

Those results came from supplied paper records. They are not evidence of a configured Zoho process or a completed product test.
Your contribution to the course project
The project is to configure Meridian’s connected enquiry-to-order and customer-service process, with a separate People exercise.
Chapter 1 described the work. This chapter decides where that work and its records should live.
Your application map becomes a foundation for the later data dictionary, access matrix, CRM configuration, Books handoff, Flow integration, Desk service process and reconciled dashboard.
The goal is a justified design. Application configuration begins in the relevant later chapters.
## 2. Lessons

### Lesson 1 — Translate process needs into application requirements

Application selection begins with the work people need to complete.
A statement such as “We need CRM” names a proposed solution. It does not explain the requirement. A better starting statement is:
Sales needs one place to record an enquiry, identify its customer, track the commercial opportunity and see the next follow-up activity.
That statement identifies the participant, work and required information. You can then compare applications against it.
A requirement is a condition the solution must satisfy. Useful requirements describe observable behavior rather than broad ambitions.
Consider these translations:
| Broad request | Usable requirement |
| --- | --- |
| Connect Sales and Finance | Finance must receive the six required packet elements and record its own acceptance decision |
| Give everyone customer visibility | Each participant must see the customer information needed for their work, within an agreed access boundary |
| Automate support | A service request must have a ticket owner, status and next action |
| Improve reporting | Reports must use identified source records and show when their data was last refreshed |
| Keep HR in the same ecosystem | Employee and leave records must have an HR owner and restricted access |
| Stop duplicates | Repeated events must be checked against the existing business record before creating more work |

The requirement should remain understandable even if you change the application choice.
Separate necessary behavior from convenience
A must-have requirement is necessary for the process to operate acceptably. A preference improves convenience but may be negotiable.
For Meridian, Finance-only acceptance is a must-have because it preserves the business decision established in Chapter 1. A particular screen arrangement is a preference unless a usability test shows that it is necessary.
A design with attractive screens but no reliable acceptance authority does not satisfy the must-have requirement.
Worked example: the billing handoff
Ava currently prepares a packet and sends it to Leo.
The requirements are:
1. Ava can prepare and correct the packet.
2. The order keeps the same business ID when corrected.
3. Missing confirmed information prevents the packet from being treated as complete.
4. Leo can review and record acceptance.
5. Ava can see whether Finance has accepted it.
6. The accepted packet can support later billing work.
7. Reporting can distinguish submitted, returned and accepted packets.
Notice that none of these statements requires every participant to edit every application. Visibility and editing are different requirements.
A useful design could let Sales see a Finance-owned result without giving Sales permission to create that result.
Check L1: Rewrite “Let Sales do everything from one screen” as two requirements: one about visibility and one about decision authority.
### Lesson 2 — Understand the seven application roles

The seven applications in this course solve different kinds of problems. Some manage operational records. Others connect applications, provide custom solutions or analyze information.
Choose an application because its role fits the work.
Zoho CRM — Sales relationships and commercial progress
Customer relationship management, usually shortened to CRM, organizes information about prospective and existing customers and the work involved in developing those relationships.
Zoho CRM includes standard modules such as Leads, Accounts, Contacts, Deals and Activities, as documented in its module documentation.^crm
A module is a category of records. A record is one instance within that category: one contact, one account or one deal.
At this stage, you need the business meaning of these categories:
- A lead represents a prospective relationship that needs qualification.
- An account represents an organization with which you do business.
- A contact represents a person.
- A deal represents a commercial opportunity.
- An activity represents work such as a task, call or meeting.
The exact structure used for Meridian’s enquiries and confirmed-order packets will be designed in Chapter 4.
Meridian example
Taylor Ross sends an enquiry on behalf of Northbank Studio.
Sales needs to distinguish:
- The enquiry: MER-ENQ-001.
- The customer organization: MER-CUST-001.
- Taylor as a person.
- The commercial quote: MER-QUOTE-001.
- The confirmed order: MER-ORD-001.
These are related records, not interchangeable names for the same thing.
CRM is the proposed operational home for Meridian’s sales-side information and commercial progress. It is also the proposed home of the order’s handoff record, including a Finance-owned acceptance decision.
That does not make Sales the authority for every field stored there. A record can be held in CRM while a particular decision remains Finance-owned.
Common mistake: Treating “customer” as a single text field that contains a company name, contact person, billing email and order description. This makes it difficult to connect multiple people and orders to the same organization.
Zoho Books — Accounting and financial transactions
Zoho Books supports financial work involving customers, items and transactions such as invoices and payments. Its documented CRM integration also distinguishes customer synchronization from financial transaction access.^books
For Meridian, Books is the proposed authoritative home for billing customer information, invoices, payments and balances.
A quote, an invoice and a payment have different meanings:
- A quote presents a commercial offer.
- An invoice records an amount billed.
- A payment records money received and its application to financial obligations.
Winning a deal does not prove payment. Finance accepting a billing packet does not prove that an invoice exists.
Meridian example
Sales confirms MER-ORD-001, and Leo accepts its packet.
The later financial process may use that packet to prepare an invoice. However, the six discovery fields alone do not constitute a complete invoice. Item details, amounts and appropriate financial settings will be addressed in Chapters 12 and 13.
The proposed ownership decision is:
Sales owns the commercial opportunity; Finance owns the accounting transaction.
Finance information may be visible from CRM through a documented integration, but visibility does not transfer accounting authority to Sales.
Common mistake: Assuming that a record called “Invoice” in any application must be the accounting source of truth. The application, module and integration route matter.
Zoho Desk — Customer-service work
Zoho Desk organizes customer-service work around tickets. Its official feature documentation describes ticket management, assignment, knowledge-base functions, workflows and service-level features.^desk
A ticket is a service work record. It identifies the request, its status, responsible participant and conversation or resolution history.
A customer may have an open sales opportunity and an unrelated support ticket at the same time. The ticket should not replace the deal or become a new sales stage.
Meridian example
For future service planning, assume that Northbank Studio later asks for help with a printer connection problem. The proposed service business identifier is MER-TKT-001.
The service team needs:
- The customer and requester.
- A description of the problem.
- A ticket owner.
- Service status and next action.
- Relevant order or product context.
Desk is the proposed authority for the ticket’s service status. CRM may show selected service context so that Ava understands the customer’s situation.
If Mia closes the ticket in Desk, that does not mean the customer has paid an invoice in Books.
Common mistake: Recording a service problem only as an unstructured sales note. A note can provide context, but it does not necessarily establish service ownership, status or a response commitment.
Zoho People — Employee operations
Zoho People manages employee-related work. Its official welcome guide describes employee information, leave, attendance, timesheets, files, cases and approvals.^people
For Meridian, People is the proposed home for employee records and the separate leave-request exercise.
An employee record and a customer contact record may both contain a name and email address, but they serve different purposes and access boundaries.
The Chapter 1 HR exercise used:
- Employee identifiers such as MER-EMP-001.
- Leave-request identifiers such as MER-HR-001.
- Omar as HR coordinator.
- Ren as the leave decision owner.
Those responsibilities continue.
Meridian example
An employee submits a leave request. Omar checks the information; Ren approves or declines it; Omar records the outcome and notifies the employee.
People is the proposed operational system for that work. A sales user’s ability to view customers does not justify access to the employee’s leave details.
People access can also be limited by purpose. An employee may need self-service access to their own record without receiving HR administrator access to everyone’s records.
Common mistake: Copying employee details into the customer process simply because both processes are part of the same organization.
Zoho Flow — Cross-application orchestration
Zoho Flow is an integration platform for workflows across cloud applications. Its official FAQ describes triggers, actions, application connections and workflow execution.^flow
A trigger starts a workflow. An action performs work after the trigger, such as transferring information or creating a related task.
An integration connection is the authorization through which a workflow accesses an application. It is different from the business record being transferred.
Meridian example
Suppose an agreed service event should cause Sales to receive a follow-up task.
The business sequence is:
1. A relevant ticket event occurs in Desk.
2. The workflow checks whether the event meets the agreed conditions.
3. It identifies the correct customer or order.
4. It creates or updates the agreed follow-up work in CRM.
5. Someone monitors exceptions.
Flow is a candidate for this cross-application orchestration. The exact available trigger and action must be checked before configuration in Chapter 14.
Flow does not become the authority for the ticket or the customer merely because it moves their information.
The Flow FAQ distinguishes its workflows from a managed two-way synchronization service and warns about loops when opposite-direction flows are used.^flow Therefore, “create two opposite flows” is not a complete synchronization design.
Common mistake: Treating an integration workflow as the master customer database or assuming that a successful workflow action proves the whole business process has finished.
Zoho Creator — Custom applications for a demonstrated gap
Zoho Creator is a low-code platform for custom applications. Its official quickstart guide demonstrates forms, related records, reports, pages and approval workflows, alongside some capabilities that use scripting.^creator
A custom application is a solution designed around a particular business need rather than a predefined sales, accounting or service structure.
Creator can be useful when you discover a genuine requirement that needs its own records and user experience.
Meridian example
Suppose installation work later requires a reusable register of customer sites, rooms and repeated readiness inspections.
That is a different requirement from simply recording a service ticket.
A Creator application could be evaluated for those records. Alternatively, an appropriate CRM custom-module design might be sufficient. The decision depends on record relationships, access, usability and support effort.
Creator is therefore evaluated but deferred in Meridian’s base design. The existing requirements do not yet justify another operational application.
“No coding required” does not mean every possible Creator requirement can be implemented without coding. Keep this course’s selection exercise focused on forms, records, relationships and ownership. Advanced Deluge and API development are outside its scope.
Common mistake: Building a custom replacement for a standard process before checking whether a suitable application already meets the requirement.
Zoho Analytics — Cross-source analysis
Zoho Analytics supports importing data, combining sources, creating reports and building dashboards. Its official help describes datasets stored in tables, relationships, reports and dashboards.^analytics
An analytical copy is information brought into a reporting environment for analysis. Its refresh position may differ from the current operational record.
A dashboard answers questions such as:
- How many orders were accepted?
- How long did the handoff take?
- Which orders remain open?
- How many service tickets need attention?
- What balances does Finance report?
It does not become the authority for the operational events that answer those questions.
Meridian example
Noor wants to compare order handoff performance with service activity.
The proposed source responsibilities are:
- CRM supplies the order confirmation and Finance-acceptance timestamps.
- Desk supplies ticket status and service events.
- Books supplies invoice and payment facts.
Analytics combines the selected information for an operations dashboard.
The documented CRM connector includes administrative setup requirements and plan-dependent refresh options.^analyticscrm Consequently, the application map must include a freshness requirement. “Connected to Analytics” does not, by itself, prove that the dashboard is current enough for a decision.
Common mistake: Correcting a source-data problem only inside a reporting table, while leaving the operational record wrong.
Application-role comparison
| Application | Main role in this chapter | Meridian example |
| --- | --- | --- |
| CRM | Sales relationships and commercial process | Enquiry, customer relationship, quote and order handoff |
| Books | Financial records and transactions | Billing customer, invoice and payment |
| Desk | Customer-service work | Printer support ticket |
| People | Employee operations | Employee and leave request |
| Flow | Cross-application workflow | Service event to follow-up action |
| Creator | Custom operational application | Possible room-inspection register |
| Analytics | Analysis and reporting | Reconciled operations dashboard |

Check L2: Which proposed application should own each of these: an invoice payment, a printer support ticket, a leave decision and a cross-source performance dashboard? Explain why Flow is not the owner of all four.
### Lesson 3 — Understand Zoho One administration

Zoho One provides a suite context and centralized administration. Its official resource page describes an Admin Panel for managing applications across an organization from a central location.^one
This administrative layer helps answer:
- Who belongs to the organization?
- Which applications should a person be assigned?
- Who is responsible for administrative changes?
- Which access should be removed when someone leaves?
It does not replace the operational records held in CRM, Books, Desk or People.
Four concepts you must distinguish
| Concept | Question it answers |
| --- | --- |
| Identity | Who is signing in? |
| Organization membership | Which organization does this person belong to? |
| Application assignment | Which application may this person use? |
| In-application authorization | What may this person do with particular records or functions? |

Authentication establishes identity. Authorization determines permitted actions.
A shared sign-in experience can simplify authentication without making every user an administrator of every application.
An application assignment also does not answer every record-access question. The product’s own roles, profiles, permissions and sharing settings still matter. Their names and behavior differ between applications.
Worked example: Ava can open CRM but cannot accept a packet
Assume Isha, the newly introduced central administrator, assigns Ava access to CRM.
Ava can sign in and open the application. Meridian still requires her acceptance attempt to be denied because Leo owns the Finance decision.
Two checks are therefore needed:
1. Can Ava enter the application?
2. Can Ava perform the particular action?
A successful first check does not imply a successful second check.
Chapter 3 will address organization and user administration. Chapter 5 will address representative CRM access controls and demonstrations.
Organization context is part of the design
An application organization is a particular organization or tenant within an application. A suite context does not mean that every application shares one database or one interchangeable organization identifier.
Before a later integration is configured, identify the intended source and destination organizations. Connecting the correct applications in the wrong organization context can send information to the wrong training dataset.
For this chapter, use the planning label MER-TRAIN-ORG. It is a human-readable design label, not a Zoho organization ID.
The actual organization identifiers, data-center choices and Books country edition remain undecided until administration and finance setup.
Provisioning and deprovisioning
Provisioning means establishing the access needed for a person’s work. Deprovisioning means removing access that is no longer needed.
A practical lifecycle includes:
1. Confirm the person and role.
2. Identify the correct organization.
3. Assign the necessary applications.
4. Establish the application-specific permissions.
5. Check one permitted action and one relevant denied action.
6. Record ownership of work and integrations that may need reassignment.
7. Remove access when the role ends.
Connections also need ownership. If a workflow depends on authorization from a departing employee, disabling the employee without planning connection ownership can affect the workflow.
The Flow FAQ documents that connections are accessible to organization owners and administrators and can be shared more broadly.^flow That makes connection-sharing an administrative decision, not simply a convenience setting.
Check L3: Isha assigns Mia CRM so that Mia can see selected customer context. Does this justify giving Mia permission to alter Finance acceptance? Which two kinds of access must be considered separately?
### Lesson 4 — Define data ownership before moving information

An application map should identify who owns the truth, not merely where copies appear.
A system of record is the authoritative application for a defined record or information domain.
A business data owner is the person or team responsible for its business meaning and correction.
A record owner inside an application may be an assigned user responsible for one particular record. That is a third concept.
For example:
- CRM can be the system of record for an enquiry.
- Sales can be its business data owner.
- Ava can be the assigned owner of one enquiry record.
These statements are related, but they are not identical.
Scope ownership precisely
A customer appears in several processes:
- Sales needs the commercial relationship.
- Finance needs billing information.
- Service needs the requester and relevant customer context.
You do not have to force every customer-related fact into one application. You do need clearly defined authority for each information domain.
For Meridian’s proposed design:
| Information domain | Authority |
| --- | --- |
| Commercial customer identity and relationship | CRM, maintained by Sales |
| Current approved billing profile | Books, maintained by Finance |
| Service-ticket status and resolution | Desk, maintained by Service |
| Employee and leave information | People, maintained by the authorized HR participants |
| Reporting definitions | Analytics artifacts, owned by Operations, using identified source facts |

The commercial customer profile and billing customer profile are related records with different responsibilities. They are not competing masters for the same undefined “customer details.”
Fields can have different authority
The proposed design introduces these distinctions:
| Information | Authoritative location |
| --- | --- |
| Sales enquiry contact email | CRM |
| Proposed billing email before handoff | CRM packet preparation |
| Accepted packet billing-email snapshot | CRM handoff history |
| Current billing email after adoption into billing work | Books |
| Invoice balance | Books |
| Ticket status | Desk |

A snapshot preserves information as it stood at a particular event.
If the current billing email changes later, the accepted packet should still show which email was accepted at the earlier handoff. Replacing history with the latest value makes investigation difficult.
Worked example: two different emails
Northbank’s enquiry contact is:
taylor.ross@example.com
Its supplied billing contact is:
northbank.billing@example.com
Both values can be correct. The problem is not that the strings differ. The problem would be using the enquiry address as the billing address without the required confirmation.
This is why mapping by field purpose is stronger than mapping by a similar label such as “Email.”
Preserve business identifiers
A business identifier is the stable reference used to follow the business object, such as MER-CUST-001.
An application-generated identifier is a local identifier assigned by a product to its own record.
The same customer can have different local identifiers in CRM, Books and Desk. A crosswalk records their relationship.
| Application | Business identifier | Local reference |
| --- | --- | --- |
| CRM | MER-CUST-001 | Not yet created |
| Books | MER-CUST-001 | Not yet created |
| Desk | MER-CUST-001 | Not yet created |

This is a completed planning crosswalk: it honestly identifies the business object while showing that no local records have been created.
Later exercises may use clearly labeled simulation references. They must not be mistaken for observed product-generated IDs.
Beware of names as matching keys
Names can change, be abbreviated or be shared by different customers.
The accessed Books integration documentation describes duplicate customer comparison using CRM Account Name and Books Customer Display Name.^books That is a documented behavior of that integration route. It does not prove that Meridian’s business identifier automatically controls native duplicate matching.
Therefore, the later configuration must check the documented matching behavior and verify the business association. Simply adding a custom business-ID field does not establish that every connector uses it as its duplicate key.
Check L4: Taylor’s enquiry email and Northbank’s billing email differ. Should the map automatically overwrite one with the other? Explain how authority and field purpose affect the decision.
### Lesson 5 — Choose the right integration pattern

An integration enables applications to exchange or use information. Different integration patterns solve different problems.
Before choosing a mechanism, describe the business handoff:
- What event makes information eligible to move?
- Which information is transferred?
- Which application is authoritative?
- What identifies the destination record?
- What result proves the transfer was usable?
- Who handles a mismatch or rejection?
Controlled manual handoff
A controlled manual handoff uses a person and an agreed checklist to transfer or verify information.
It is useful when the process is still being validated, the volume is manageable, or a connector’s suitability has not yet been established.
For Meridian’s first finance mapping exercise, Leo can inspect the accepted packet, verify the customer association and prepare the later financial record through a supervised procedure.
“Manual” should not mean “copy whatever seems useful.” The handoff still needs named source fields, checks, stable references and completion evidence.
Native integration
A native integration is a documented connection supplied for the applications involved.
It can reduce custom maintenance, but you must check its scope:
- Which modules does it handle?
- Which direction is supported?
- What matching rules does it use?
- Which fields can be mapped?
- What permissions are required?
- What happens to updates, duplicates and exceptions?
The Books documentation provides a useful example. It distinguishes CRM Accounts, Contacts, customer synchronization and financial transaction modules.^books
For the documented Accounts-and-Contacts option:
- CRM Accounts are fetched as business customers.
- Associated Contacts are fetched as contact persons.
That option is relevant when Meridian needs to represent Northbank Studio separately from Taylor Ross.
However, that documented customer option does not prove that every commercial transaction in CRM is automatically copied to Books.
A critical distinction: native CRM records and Zoho Finance records
The accessed Books documentation states that native CRM transaction modules—including Quotes, Invoices, Sales Orders and Purchase Orders—do not have direct synchronization with the corresponding Books transaction modules through that standard route. It separately describes transactions accessed through CRM’s Zoho Finance area.^books
For selection purposes, the lesson is:
The record’s module and integration route matter as much as its label.
A CRM-native quote and a Books financial quote visible through CRM are not automatically the same operational object.
Meridian’s base proposal keeps MER-QUOTE-001 as the sales commercial quote. Finance’s later billing work must use a deliberately verified handoff. This chapter does not assume that the native quote’s line items will automatically appear in Books.
A different design could use Books-owned quotes accessed through an appropriate Finance integration. That is a legitimate alternative, but it changes the commercial record’s authoritative home and user procedure. It must be chosen explicitly.
Flow orchestration
Flow is useful when a defined event must cause work in another application, particularly when conditions and branches are needed.
A proposed Desk-to-CRM follow-up is a suitable candidate to evaluate. It needs a trigger, matching rule, action and exception owner.
Do not configure a Flow workflow and a native integration to create the same destination object without assigning clear responsibilities. Two independent creators can produce duplicate work.
Opposite-direction workflows also need rules that prevent repeated updates from triggering each other.
Analytical connector
An analytical connector imports information for reporting.
Its success criteria differ from operational handoff criteria. It may need:
- The right source organization.
- Selected modules and fields.
- Suitable refresh frequency.
- Correct relationships.
- Authorized sharing.
- Reconciliation with source records.
An analytical refresh should not be treated as evidence that Finance accepted a packet. It can report an acceptance event only if that event exists in the authoritative source.
Integration contract
An integration contract is a plain-language agreement about a particular information exchange.
Here is a completed contract for Meridian’s proposed packet handoff:
| Contract element | Decision |
| --- | --- |
| Source | CRM confirmed-order packet |
| Eligibility | The six required fields are complete and Finance has recorded acceptance |
| Business key | Existing order ID plus its linked customer and quote IDs |
| Destination purpose | Finance’s later Books billing preparation |
| Initial method | Controlled manual mapping |
| Field authority | Finance preserves the accepted packet and controls accounting facts |
| Success evidence | Verified customer association and traceable destination reference when the later record is created |
| Missing or ambiguous mapping | Hold; Finance verifies the association |
| Repeat behavior | Reuse the existing business case; do not create another order or billing record merely because the packet is resent |
| Monitoring owner | Leo for finance mapping; Noor for unresolved process ownership |
| Later verification | Chapter 13 confirms the actual mappings and product procedure |

This contract does not claim that an invoice can be created from the six fields alone. It defines the route into later financial preparation.
Check L5: Why is “CRM and Books are connected” insufficient evidence that MER-QUOTE-001 will synchronize as the intended financial transaction?
### Lesson 6 — Compare proposals using gates and weighted criteria

A selection gate is a requirement that a proposal must satisfy before you consider it acceptable.
A weighted score helps compare eligible proposals. It should not allow a serious requirement failure to disappear inside a high average.
For Meridian, use these synthetic gates:
- G1: Finance retains sole authority for packet acceptance.
- G2: HR request details remain restricted to the supplied HR access boundary.
- G3: Every operational area has a named support owner.
Consider three specific proposals:
| Proposal | Description |
| --- | --- |
| A | Keep all work in one broadly shared CRM design; let Sales close finance handoffs; include HR request details in the shared customer workspace |
| B | Use CRM for sales, Books for accounting, Desk for service and People for HR; stage Flow and Analytics; name support owners |
| C | Build a custom replacement for sales, finance, service and HR; no person is assigned to maintain the custom applications |

These are assessments of the described proposals, not claims that CRM or Creator inherently cannot support appropriate controls.
The supplied scoring scale is 1–5: 1 means poor fit against the stated criterion; 5 means strong fit. The ratings are synthetic judgments for this comparison.
| Criterion | Weight | A rating |
| --- | --- | --- |
| Business fit | 4 | 3 |
| Ownership clarity | 3 | 2 |
| Supportability | 2 | 4 |
| User convenience | 1 | 5 |

Calculate:
Weighted score = sum of each weight × its rating
The maximum is:
(4 + 3 + 2 + 1) × 5 = 50 points
For Proposal B:
(4 × 5) + (3 × 5) + (2 × 4) + (1 × 3)
= 20 + 15 + 8 + 3 = 46 points
Normalized score = 46 ÷ 50 × 100% = 92%
Proposal B is the selected base design because it passes the gates and has the strongest score among the supplied proposals.
Its score does not prove successful configuration. It expresses the selection reasoning that later testing must examine.
Check L6: Could a proposal that fails Finance-only acceptance still be selected simply because its weighted score is higher? Explain the purpose of a gate.
## 3. Visual explanation — Meridian’s proposed application architecture

flowchart LR
    ONE["Zoho One: identity and application administration"]

    subgraph CUSTOMER["Customer operations"]
        CRM["CRM: sales and order handoff"]
        BOOKS["Books: billing and accounting"]
        DESK["Desk: service tickets"]
        FLOW["Flow: proposed cross-app actions"]
        ANALYTICS["Analytics: reconciled reporting"]
    end

    PEOPLE["People: separate employee and HR process"]

    ONE -. "application access" .-> CRM
    ONE -. "application access" .-> BOOKS
    ONE -. "application access" .-> DESK
    ONE -. "application access" .-> PEOPLE

    CRM -->|"controlled identity and accepted-packet handoff"| BOOKS
    BOOKS -->|"selected finance context"| CRM
    CRM -->|"selected customer context"| DESK
    DESK -->|"eligible service event"| FLOW
    FLOW -->|"agreed follow-up work"| CRM

    CRM -->|"reporting copy"| ANALYTICS
    BOOKS -->|"reporting copy"| ANALYTICS
    DESK -->|"reporting copy"| ANALYTICS
This is a proposed architecture, not a diagram of tested connections.
The solid arrows describe business information exchanges. Each needs its own contract and verification. They do not mean that every field travels in both directions.
The dotted arrows describe application-access administration. They do not transfer customer or employee records.
People is separate from the customer-operation data flows. The same organization can administer access to both areas while keeping their operational records and readers separate.
Flow sits between an eligible event and a defined action. It does not replace the ticket or customer record.
Analytics receives reporting copies from operational sources. It should retain enough identifiers and freshness information to reconcile its results.
Creator is deferred in the base architecture. The independent challenge introduces a specific requirement that could justify evaluating it again.
## 4. Worked case — Select Meridian’s base solution

Case inputs
Use the established identifiers and the following explicit additions:
- Northbank Studio remains MER-CUST-001.
- Taylor Ross remains the enquiry contact at taylor.ross@example.com.
- Introduce MER-CON-001 as Taylor’s business contact identifier.
- MER-QUOTE-001 remains the commercial quote.
- MER-ORD-001 remains the confirmed order.
- CONF-001 remains its written confirmation reference.
- The supplied billing email remains northbank.billing@example.com.
- Installation required remains Yes.
- Introduce Mia as the Service participant.
- Introduce Isha as the central administrator.
- MER-TKT-001, MER-INV-001 and MER-PAY-001 are planned identifiers for later service and financial examples. They are not evidence that those records already exist.
- MER-DASH-001 identifies the planned operations dashboard definition.
All application assignments below are target-design decisions. No case records have been imported or configured by this chapter.
Step 1 — Select the application responsibilities
The completed application map is the content of C01_CH02_Meridian_Application_Map.md.
| Application or layer | Meridian responsibility | Selection position |
| --- | --- | --- |
| CRM | Enquiries, commercial customer relationship, contacts, quotes and confirmed-order packet history | Selected for sales process |
| Books | Billing customer profile, invoices, payments and financial balances | Selected for finance process |
| Desk | Service tickets, service status and resolution history | Selected for service process |
| People | Employee records and separate leave-request process | Selected for HR exercise |
| Flow | Defined cross-application follow-up actions and workflow monitoring | Selected for later integration work |
| Analytics | Cross-source operations reporting and reconciled metric definitions | Selected for later reporting work |
| Creator | Custom application only if a demonstrated record or user-experience gap remains | Deferred in base design |
| Zoho One | Organization identity and application-access administration | Administrative foundation |

The selection is staged because the application map defines the destination design; it does not require every connection to be activated immediately.
Step 2 — Assign an authoritative home to every record family
The completed ownership matrix is the content of C01_CH02_Meridian_Record_Ownership.md.
“Record family” means one defined category of information. The inventory contains twelve families, including the derived dashboard definition.
| Family | Record or information scope | Example business ID | Authoritative application |
| --- | --- | --- | --- |
| R01 | Enquiry | MER-ENQ-001 | CRM |
| R02 | Commercial customer profile | MER-CUST-001 | CRM |
| R03 | Sales contact | MER-CON-001 | CRM |
| R04 | Commercial quote | MER-QUOTE-001 | CRM |
| R05 | Confirmed order and packet history | MER-ORD-001 | CRM |
| R06 | Current billing customer profile | MER-CUST-001 | Books |
| R07 | Invoice | MER-INV-001, planned | Books |
| R08 | Payment | MER-PAY-001, planned | Books |
| R09 | Service ticket | MER-TKT-001, planned | Desk |
| R10 | Employee | MER-EMP-001 | People |
| R11 | Leave request | MER-HR-001 | People |
| R12 | Operations dashboard definition | MER-DASH-001, planned | Analytics |

The same customer ID appears in R02 and R06 because the records represent different information domains. The map does not authorize two independent masters for the same billing field.
Step 3 — Record integration decisions
The completed decision sheet is the content of C01_CH02_Meridian_Integration_Decisions.md.
| Contract | Source to destination | Purpose and eligibility | Initial pattern |
| --- | --- | --- | --- |
| I01 | CRM customer identity to Books billing customer | Establish the correct customer association before financial work | Controlled manual association; evaluate native customer mapping |
| I02 | CRM accepted packet to Books preparation | Use a Finance-accepted packet to support later billing preparation | Controlled manual mapping for the first verified exercise |
| I03 | Books to CRM | Show selected invoice, payment or balance context | Evaluate documented Finance integration |
| I04 | CRM to Desk | Provide selected customer and contact context | Evaluate documented application integration |
| I05 | Desk event through Flow to CRM | Create agreed service-related follow-up work | Evaluate Flow trigger, conditions and action |
| I06 | CRM to Analytics | Supply sales and handoff facts | Analytical connector |
| I07 | Books to Analytics | Supply invoice and payment facts | Analytical connector |
| I08 | Desk to Analytics | Supply service facts | Analytical connector |

There are eight logical contracts. None has execution evidence in this chapter.
A native customer integration and a Flow workflow should not both create the same billing customer without an explicit coordination rule. In this base design, I01 controls the customer association; I05 has a different purpose.
Step 4 — Build an initial access plan
This plan states business needs. It does not claim that the corresponding product permissions are already configured.
| Person | Planned application needs | Permitted business work |
| --- | --- | --- |
| Ava | CRM; People self-service if assigned | Prepare and correct sales packets; view selected finance/service context |
| Leo | Books; CRM Finance-review access; own People self-service | Maintain finance records and accept packets |
| Mia | Desk; restricted CRM customer context; own People self-service | Manage service work |
| Noor | CRM operations visibility; operations Analytics views; own People self-service | Monitor process work and measures |
| Omar | People with the required HR scope | Maintain employee/request information and coordinate corrections |
| Ren | People with appropriate manager scope | Make the supplied leave decisions |
| Isha | Zoho One administration; separately authorized Flow and Analytics administration | Manage assignments and approved technical setup |
| Employee MER-EMP-001 | People self-service | Access own permitted information and request status |

This is the completed starting content of C01_CH02_Meridian_Access_Plan.md.
Step 5 — Check design coverage
Define:
Ownership coverage = families with a defined authoritative application ÷ required families × 100%
For the completed map:
12 ÷ 12 × 100% = 100%
This proves inventory coverage, not correct configuration.
Define separately:
Executed integration verification = contracts with supplied execution evidence ÷ defined contracts × 100%
For this chapter:
0 ÷ 8 × 100% = 0%
The second result is appropriate at selection stage. The eight contracts are planned, not tested.
Mistake and correction
Mistake: The map says, “CRM quote → Books quote automatically,” because both applications have a quote concept.
Correction: Identify the source as Meridian’s commercial CRM quote and select a controlled, later-verified finance handoff. The documented native CRM transaction-module distinction must be respected.
If you instead choose a Books-owned quote accessible through a supported Finance route, change the ownership matrix and user procedure explicitly. Do not leave both applications as independent commercial quote masters.
## 5. Try it yourself — Guided practice

Learning goal
Create an application map that identifies the authoritative application for every required record family and remains usable when the normal route encounters an exception.
Requirements and materials
Use a spreadsheet, Markdown editor or paper.
You need:
- The twelve-family inventory R01–R12.
- The eight integration contracts I01–I08.
- The participant and access rules in Section 4.
- The complete simulation inputs below.
No account, application license or product administrator access is required. This planning exercise cannot prove live synchronization, configured permissions or connector execution.
Additional simulation inputs
These are architecture replays. They do not replace Chapter 1’s historical packet records or change its accepted/open counts.
For customer association, use this paper candidate list:
| Paper reference | Application and organization label | Business customer ID | Display name |
| --- | --- | --- | --- |
| SIM-CRM-001 | CRM, MER-TRAIN-ORG | MER-CUST-001 | Northbank Studio |
| SIM-BOOKS-A | Books, MER-TRAIN-ORG | MER-CUST-001 | Northbank Studio |
| SIM-BOOKS-B | Books, MER-TRAIN-ORG | MER-CUST-001 | Northbank Studio |

These references are simulation labels, not product-generated IDs. Nothing in the inputs authorizes deletion or merging of either candidate.
Use these six scenario cards:
| Scenario | Complete input |
| --- | --- |
| AP-01: normal | MER-ORD-001 links MER-CUST-001, MER-QUOTE-001 and CONF-001; billing email is northbank.billing@example.com; installation = Yes; Finance accepts in the replay |
| AP-02: missing data | Replay the original first packet of MER-ORD-002: customer MER-CUST-002, quote MER-QUOTE-002, confirmation CONF-002, installation = No, billing email blank |
| AP-03: denied action | Ava can open CRM and edit preparation information; the replay packet awaits Finance; Ava attempts to record Finance acceptance |
| AP-04: repeat | AP-01 is already accepted; an unchanged repeat carries MER-ORD-001, MER-CUST-001, MER-QUOTE-001 and CONF-001 |
| AP-05: ambiguous association | I01 initially finds SIM-BOOKS-A and SIM-BOOKS-B by the same name; MAP-001 is the supplied Finance verification |
| AP-06: wrong field purpose | A proposed mapping sends taylor.ross@example.com from enquiry-contact email into the billing-contact destination; the supplied accepted packet contains northbank.billing@example.com |

For AP-02, the only supplied correction is:
redwood.billing@example.com, supported by BILL-002.
For AP-06, the exercise supplies no customer authorization to replace the billing email with Taylor’s enquiry address.
Learner worksheets
Application selection
Record one responsibility for each application and explain whether it is selected, staged or deferred.
| Application | Business requirement | Selected, staged or deferred? |
| --- | --- | --- |
| CRM |  |  |
| Books |  |  |
| Desk |  |  |
| People |  |  |
| Flow |  |  |
| Creator |  |  |
| Analytics |  |  |
| Zoho One administration |  |  |

Ownership
Use R01–R12 as the required inventory. Enter one authoritative application for each defined family.
| Family | Authoritative application | Business authority |
| --- | --- | --- |
| R01 |  |  |
| R02 |  |  |
| R03 |  |  |
| R04 |  |  |
| R05 |  |  |
| R06 |  |  |
| R07 |  |  |
| R08 |  |  |
| R09 |  |  |
| R10 |  |  |
| R11 |  |  |
| R12 |  |  |

Scenario traces
Show the state before the decision, the responsible participant and the resulting route.
| Scenario | Starting condition | Decision and reason | Owner |
| --- | --- | --- | --- |
| AP-01 |  |  |  |
| AP-02 |  |  |  |
| AP-03 |  |  |  |
| AP-04 |  |  |  |
| AP-05 |  |  |  |
| AP-06 |  |  |  |

Guided steps and expected intermediate results
1. Identify application responsibilities.  
Expected result: all seven applications are considered; Zoho One administration is identified separately; Creator has an explicit selection position.
2. Complete the twelve-family ownership inventory.  
Expected result: no required family has a blank or competing authoritative application. Shared customer information is scoped by purpose.
3. Describe each integration contract.  
Expected result: I01–I08 each has a purpose, direction, method and exception owner. Candidate integrations are labeled as requiring verification.
4. Complete the participant access plan.  
Expected result: app entry, record visibility and decision authority are distinguished. HR details remain outside the customer dashboard.
5. Trace AP-01–AP-06.  
Expected result: each scenario has a justified owner and route; permitted corrections use only the supplied values and evidence.
6. Calculate ownership coverage and execution-verification coverage.  
Expected result: denominators are twelve families and eight contracts respectively. Planned architecture is distinguished from execution evidence.
Final artifact
Your final submission for this chapter consists of:
- C01_CH02_Meridian_Application_Map.md
- C01_CH02_Meridian_Record_Ownership.md
- C01_CH02_Meridian_Integration_Decisions.md
- C01_CH02_Meridian_Access_Plan.md
- C01_CH02_Meridian_Scenario_Traces.md
Another student should be able to identify the correct home and authority for a record, then follow an exception without guessing.
No live-system cleanup is necessary. Preserve simulation labels and original inputs when revising your design.
## 6. Independent challenge — Add installation-readiness records

Meridian has a new proposed requirement: installation teams must record readiness separately for each room at a customer site and retain successive inspection results.
This is an explicit extension to the base case, not a requirement established in Chapter 1.
New requirements
- A customer can have several sites.
- A site can have several rooms.
- A room can have several inspections over time.
- Each inspection records power, network and access observations.
- Noor owns the readiness process.
- Mia records inspection observations.
- Sales can read a readiness summary but cannot edit inspection results.
- HR request information must not enter this process.
- Noor is assumed to be able to maintain simple forms and reports in either of the two custom-record proposals below.
- Detailed feasibility and permissions must still be verified before implementation.
Candidate proposals
| Proposal | Supplied design |
| --- | --- |
| D | Store one free-text “site ready” note on a Desk ticket; define no separate room or inspection records |
| E | Use Creator for related Site, Room and Inspection records; share a derived readiness summary with customer operations |
| F | Use suitable CRM custom modules for Site, Room and Inspection records; share a restricted readiness summary |

These are candidate designs. Proposal D’s limitation is its supplied record structure, not a universal claim that Desk cannot be extended.
Input records and readiness rule
The site is MER-SITE-001, linked to MER-CUST-001.
Use the following inspections:
| Inspection | Room | Site | Power available |
| --- | --- | --- | --- |
| MER-INSP-001 | MER-ROOM-001 | MER-SITE-001 | Yes |
| MER-INSP-002 | MER-ROOM-002 | MER-SITE-001 | Yes |
| MER-INSP-003 | MER-ROOM-003 | MER-SITE-001 | Yes |

Apply this synthetic rule:
1. If any supplied observation is No, classify the inspection Not ready.
2. Otherwise, if any observation is missing, classify it Needs clarification.
3. Otherwise, if all three are Yes, classify it Ready.
For the missing value in MER-INSP-003, the permitted later correction is Yes, supported by customer evidence ACCESS-003. Preserve the original missing observation and correction history.
Deliverables
Create C01_CH02_Installation_Extension.md containing:
1. Your selected proposal and reasoning.
2. Authoritative homes for Site, Room, Inspection and readiness-summary information.
3. The relationship path from inspection to customer.
4. Initial readiness classifications for all three inspections.
5. The permitted recovery for the missing observation and the resulting classification.
6. A statement of Sales’ permitted and denied actions.
7. An explanation of how your choice changes the base application map.
8. At least two implementation checks needed before configuration.
Success criteria
Your design must preserve room-level records and inspection history, identify business and application ownership, retain the customer link, apply the supplied rule reproducibly and protect editing authority.
Either E or F can be valid if the reasoning and resulting ownership map are consistent. A single unstructured site note does not satisfy the supplied record-history requirement.
## 7. Common problems and recovery

| Symptom | Diagnosis | Correction |
| --- | --- | --- |
| The map contains app names but no record ownership | Responsibilities were not defined | Add record families and authoritative homes |
| CRM and Books both claim the current billing-email master | The information domain is ambiguous | Define Finance-owned current billing information separately from Sales proposals and historical snapshots |
| Every customer field is copied to every application | Information transfer has no business purpose | Select only the data needed for each handoff |
| A native quote is assumed to synchronize because Books also has quotes | Labels were confused with integration scope | Check the exact source module and documented route |
| Two matching customer names are accepted automatically | Name matching was treated as identity proof | Hold the association and consult approved business evidence |
| A repeated event creates another financial case | Attempts were counted as new business objects | Reuse the existing order and verify destination references before further creation |
| Sales can open CRM and therefore assumes all actions are permitted | App assignment was confused with authorization | Retain Finance-only acceptance |
| The dashboard is treated as live operational truth | Refresh and source authority were ignored | Identify source facts and last refresh position |
| People records appear in the customer dashboard | Separate HR access scope was lost | Remove the inappropriate data path and restrict the HR artifact |
| Flow and a native connector create the same object | Integration responsibilities overlap | Assign one creator and define any other route as lookup, context or update |
| A correction overwrites accepted history | A current master value was confused with an event snapshot | Preserve the accepted version and add the correction/change record |

In this selection chapter, recovery means correcting the design, mapping decision or paper route. It does not require inventing a technical outage.
For an ambiguous association, do not delete records merely to make the map look tidy. Establish the correct relationship first; investigate duplicate cleanup separately with appropriate evidence.
## 8. Check your understanding

Answer before reading the solutions.
 1. Explain the difference between an application’s system-of-record responsibility and a user’s assigned record ownership.
 2. Why can MER-CUST-001 legitimately appear in both CRM and Books?
 3. Which application should establish an invoice payment fact, and which application may report it?
 4. If a Finance-owned transaction is visible from CRM, does CRM visibility alone make Sales its business authority?
 5. Why is a crosswalk stronger than assuming equal display names prove equal customers?
 6. What should happen when a completeness check fails before a packet is submitted?
 7. The supplied Proposal A has a weighted score of 31 points. Show how that result is calculated and why the proposal still fails selection.
 8. Why should a Desk-to-CRM workflow have a named exception owner?
 9. A dashboard displays “accepted orders,” but its source field is “Sales sent packet.” What is wrong with the design?
10. What evidence would justify selecting Creator for the installation extension?
11. Why does 100% ownership coverage not mean that the integration work is finished?
12. Name two facts you must check before relying on a native integration for an operational handoff.
## 9. Solutions and explanations

Answers to lesson checks
| Check | Explained answer |
| --- | --- |
| L1 | Visibility requirement: Sales can see the order’s Finance-review status and selected financial context from its working environment. Authority requirement: only Finance can establish acceptance and accounting outcomes. One-screen convenience does not require shared authority. |
| L2 | Books owns invoice payment facts; Desk owns the service ticket; People holds the leave request and Ren’s decision; Analytics owns the dashboard definition and reporting presentation. Flow moves or acts on information but does not acquire the business authority of every source record. |
| L3 | No. Mia’s app entry and selected record visibility are separate from action authorization. Customer-context access does not justify altering Finance acceptance. |
| L4 | No automatic overwrite is justified. The enquiry email identifies Taylor for Sales communication; the billing email serves a different purpose and has supplied confirmation evidence. The ownership map must preserve that distinction. |
| L5 | The connection’s exact module scope and route determine behavior. The accessed documentation distinguishes native CRM transaction modules from Zoho Finance transaction access. A generic connection statement does not establish the intended quote mapping. |
| L6 | No. A gate represents a required condition. A higher weighted score cannot compensate for violating Finance-only acceptance. Revise the proposal so it passes the gate before treating it as eligible. |

Guided practice — Completed scenario traces
Use the completed maps in Section 4 as the reference artifacts. The additional scenario evidence below completes C01_CH02_Meridian_Scenario_Traces.md.
| Scenario | Decision and explanation | Owner |
| --- | --- | --- |
| AP-01 | Keep the confirmed-order packet in CRM; Finance establishes acceptance; use I02 for later Books preparation | Sales prepares; Finance accepts and maps |
| AP-02 | Blank confirmed billing information prevents normal submission; preserve the first-version exception | Sales correction owner |
| AP-03 | CRM entry does not authorize Ava to establish Finance acceptance | Finance remains decision owner |
| AP-04 | Exact unchanged repeat belongs to the already accepted case | Sales identifies repeat |
| AP-05 | Equal names do not resolve the initial ambiguity; use supplied Finance verification | Finance |
| AP-06 | Enquiry-contact purpose differs from billing-contact purpose | Finance owns billing mapping; Sales supplies packet evidence |

Why AP-02 does not alter the baseline
Chapter 1 showed MER-ORD-002 eventually accepted after correction. AP-02 replays its original first-version condition to test the proposed gate.
The replay does not change the historical acceptance timestamp, first-pass result or baseline count.
Why AP-04 is not a blanket “never create another invoice” rule
The supplied repeat contains no changed instruction and represents no new business event. It therefore provides no basis for another case.
A later, separately authorized transaction or billing arrangement would require its own requirements and evidence. The duplicate rule applies to this unchanged repeat.
Why AP-05 does not authorize deletion
MAP-001 approves an association to SIM-BOOKS-A. It does not supply transaction history or a cleanup procedure for SIM-BOOKS-B.
Correct association and safe duplicate cleanup are separate decisions.
Completed ownership checks
The authoritative application sequence for R01–R12 is:
| Family | Application |
| --- | --- |
| R01 | CRM |
| R02 | CRM |
| R03 | CRM |
| R04 | CRM |
| R05 | CRM |
| R06 | Books |
| R07 | Books |
| R08 | Books |
| R09 | Desk |
| R10 | People |
| R11 | People |
| R12 | Analytics |

A valid worksheet must also retain the business authorities and copy rules from Section 4. Merely listing these application names does not complete the reasoning.
For correction routes:
- Sales corrects sales preparation and commercial identity problems.
- Finance resolves billing associations and accounting information.
- Service corrects ticket information.
- Authorized HR participants correct employee/request information.
- Reporting problems are diagnosed in Analytics, but incorrect source facts are corrected by the relevant operational owner.
Completed coverage calculations
Ownership:
12 defined families ÷ 12 required families × 100% = 100%
Integration execution evidence:
0 executed contracts ÷ 8 defined contracts × 100% = 0%
The first result describes completeness of the planning inventory. The second describes the absence of product execution evidence at this stage.
Both can be correct simultaneously.
Independent challenge — One complete solution
Select Proposal E, a Creator application for the installation-readiness extension.
The reason is the newly supplied need for independent Site, Room and repeated Inspection records. This is a demonstrated gap in Proposal D’s one-note design.
The choice adds an operational application, so it must also add a support responsibility and integration decision.
Completed extension ownership map
| Record or information | Authoritative application | Business authority |
| --- | --- | --- |
| Commercial customer MER-CUST-001 | CRM | Sales |
| Site MER-SITE-001 | Creator | Operations, Noor |
| Rooms MER-ROOM-001 to MER-ROOM-003 | Creator | Operations, Noor |
| Inspections MER-INSP-001 to MER-INSP-003 | Creator | Operations; Mia records observations |
| Readiness summary | Derived from Creator inspections | Operations defines the rule |
| Service ticket, if separately required | Desk | Service |
| HR records | People | Authorized HR participants |

The relationship path is:
Inspection → Room → Site → Customer business reference
For example:
MER-INSP-002 → MER-ROOM-002 → MER-SITE-001 → MER-CUST-001
The customer reference preserves the CRM relationship. It does not make Creator the commercial customer master.
Completed classifications
| Inspection | Substitution into the rule |
| --- | --- |
| MER-INSP-001 | Power Yes; network Yes; access Yes; no No or missing observations |
| MER-INSP-002 | Network = No, so rule 1 applies |
| MER-INSP-003 | No observation is No, but access is missing, so rule 2 applies |

Missing information is not equivalent to an observed No, and it is not permission to assume Yes.
For MER-INSP-003, the supplied later correction is access Yes, with evidence ACCESS-003.
After the correction:
Power Yes + network Yes + access Yes → Ready
Preserve the original missing observation and record the correction evidence. Do not rewrite the history so that the first version appears complete.
Completed access decision
Sales may read the readiness summary and its customer/site reference.
Sales may not change Mia’s observations or establish readiness by editing the summary directly.
Noor owns the rule and process. Mia records the observations. The implementation must test these authorities separately.
Effect on the base map
Creator changes from deferred to selected for the installation extension only.
CRM remains the commercial customer master. Books remains the accounting authority. Desk remains the service-ticket authority. People remains separate.
Add a contract for the customer reference into Creator and a contract for restricted readiness-summary visibility. Their mechanisms require later verification.
Implementation checks
Before configuration, verify at least:
1. The proposed Site–Room–Inspection relationships can be represented as intended.
2. Inspection history and corrections can be retained without replacing earlier events.
3. Sales can read the required summary while being denied observation editing.
4. The customer reference is mapped to the correct organization and record.
5. The chosen summary-sharing method does not disclose unrelated information.
6. The design can be maintained within the agreed no-code scope.
Acceptable alternative: Proposal F
A CRM custom-module design can also be valid if it satisfies the relationships, history, authority and user-experience requirements.
Its advantage may be fewer cross-application links. Its tradeoff may be added complexity within the CRM data model.
Selecting F requires changing the ownership table to CRM for Site, Room and Inspection, while preserving restricted editing and historical observations. Creator would remain deferred.
Neither alternative is proven by a paper design alone. The choice establishes what must be configured and tested.
Answers to the understanding questions
1. System-of-record responsibility belongs to an application for a defined information scope. Assigned record ownership belongs to a user or team for a particular record. CRM can hold an enquiry while Ava is responsible for that enquiry.
2. The records serve different domains. CRM owns the commercial relationship; Books owns the billing profile. A shared business identifier connects them while field authority remains defined.
3. Books establishes the payment fact. Analytics may report it, and CRM may display selected financial context. A report or sales note does not independently establish payment.
4. No. The interface through which a person sees a record does not automatically change its business authority. The authorized financial process remains responsible.
5. A crosswalk documents a verified association. Equal names can be duplicates, abbreviations or unrelated records. The association must include the correct business object and application context.
 6. Hold with the preparation owner. Obtain the permitted correction, preserve the original exception and submit the corrected existing packet. Do not manufacture a value or an acceptance.
 7. Proposal A’s calculation is:  
(4 × 3) + (3 × 2) + (2 × 4) + (1 × 5)  
= 12 + 6 + 8 + 5 = 31 points  
31 ÷ 50 × 100% = 62%.  
It fails G1 and G2 because the described proposal lets Sales close finance handoffs and exposes HR details in the shared customer workspace.
 8. Someone must resolve business mismatches and unfinished work. A workflow cannot be considered operationally owned merely because an action is automated. The owner investigates wrong associations, incomplete information or unmet business conditions.
 9. The source event does not match the measure. “Sent” describes a Sales action. “Accepted” requires Finance’s decision. The dashboard would label one event as another.
10. A specific custom-record requirement can justify evaluation. Independent sites, rooms, repeated inspections, historical observations and a tailored readiness experience provide that evidence in the extension. The choice still needs support and feasibility checks.
11. Coverage is a planning measure. It establishes that every required family has a designated home. It does not prove fields, permissions, connections or execution.
12. Valid checks include module scope, direction, matching behavior, field mapping, organization context, permissions, edition availability and timing. State the particular checks relevant to the proposed handoff rather than writing only “verify integration.”
## 10. Chapter recap and next step

A connected solution needs clear responsibilities at three levels:
- Application responsibility: where each kind of work belongs.
- Data authority: which record or field provides the trusted fact.
- Participant authority: who may establish or change that fact.
Meridian’s base design uses CRM for sales and handoff history, Books for financial records, Desk for service and People for separate employee work. Flow supports defined cross-application actions; Analytics supports reconciled reporting. Creator remains deferred until a demonstrated gap justifies it.
The important selection decisions are not merely the application names. They include the distinction between commercial and financial records, protected Finance acceptance, scoped customer information, verified record associations and named exception owners.
“I can…” completion checklist
- I can explain the roles of the seven applications.
- I can explain Zoho One administration without confusing it with record ownership.
- I can turn a broad business request into observable requirements.
- I can identify an authoritative home for every required record family.
- I can distinguish a business identifier from a local application identifier.
- I can choose and justify an integration pattern.
- I can trace missing data, a repeat, a denied action and an ambiguous association.
- I can distinguish a completed design from a configured and tested solution.
Your five Meridian artifacts form the application-selection contribution to the course project. The installation extension is an additional challenge artifact, not an automatic change to every learner’s base design.
The next chapter, Organisation and User Administration, builds on the access plan. You will work with organization settings, locale, users, teams, identity controls and user-lifecycle requirements.
## 11. Glossary and further reading

Glossary
| Term | Meaning |
| --- | --- |
| Analytical connector | A mechanism that imports source information for reporting and analysis |
| Analytical copy | Information held for analysis rather than as the authoritative operational record |
| Application assignment | Permission or provisioning that enables a person to use an application in the intended organization |
| Authentication | Establishing who is signing in |
| Authorization | Determining what that identity may do |
| Business data owner | The participant accountable for a record’s business meaning and correction |
| Business identifier | A stable reference used to follow a business object across processes |
| Connection | An authorization used by an integration to access an application |
| Crosswalk | A documented relationship between a business identifier and application-local references |
| Deprovisioning | Removing access that is no longer required |
| Integration contract | The agreed purpose, eligibility, mapping, authority and recovery rules for an exchange |
| Module | A category of records within an application |
| Native integration | A documented connection supplied for the applications involved |
| Operational record | A record used to perform or establish business work |
| Provisioning | Establishing the access needed for a person’s work |
| Record family | A defined category of records or information in an ownership inventory |
| Selection gate | A required condition that a proposal must satisfy |
| Snapshot | A preserved version of information at a particular event |
| System of record | The authoritative application for a defined information scope |
| Weighted score | A comparison result calculated from ratings and criterion weights |

Further reading
The sources below were accessed for the application roles and documented distinctions used in this chapter. They do not establish that Meridian’s proposed configuration has been executed.
The Books integration source is the India-edition help page. Confirm the appropriate Books country edition and organization settings before applying its procedure. The Analytics CRM connector documents administrative setup and plan-dependent refresh options. The People resource catalog identifies its current administrator guide as version 5.0; this chapter uses conceptual roles rather than asserting a particular People navigation path.
Selected connector fields, actual entitlements, organization identifiers and configuration permissions remain implementation dependencies for the relevant later chapters.
^crm: Zoho CRM, Modules API, V8 (https://www.zoho.com/crm/developer/docs/api/v8/modules-api.html). Used here to establish standard module categories. No API call is required for this chapter.
^books: Zoho Books, Integrate Zoho Books with Zoho CRM (https://www.zoho.com/in/books/help/integrations/crm-integration.html). Read Sync Customers, Sync Transaction Modules and Manage Users and Roles to understand why module, matching and permission choices matter.
^desk: Zoho Desk, Features (https://www.zoho.com/desk/features.html). The ticket-management, assignment, knowledge-base and automation sections support the service role described here.
^people: Zoho People, Welcome Guide (https://www.zoho.com/people/welcome-guide.html), for employee and administrator concepts; Resource Center (https://www.zoho.com/people/resources.html), for the version-specific administrator and employee guides.
^flow: Zoho Flow, Frequently Asked Questions (https://www.zoho.com/flow/help/faq.html). Read the workflow, trigger/action, synchronization and connection-access explanations.
^creator: Zoho Creator, A Quickstart Guide to Zoho Creator (https://www.zoho.com/creator/help/new-quickstart-guide.html). The forms, relationships, reports and approval examples illustrate custom-application concepts. Advanced scripting examples are outside this chapter’s practice.
^analytics: Zoho Analytics, Online Help Overview (https://www.zoho.com/analytics/help/overview.html). Relevant sections cover tables, imported sources, relationships, reports and dashboards.
^analyticscrm: Zoho Analytics, Zoho CRM Advanced Analytics (https://www.zoho.com/analytics/help/connectors/zoho-crm.html). Relevant sections cover setup permissions, refresh options, source management and combining data.
^one: Zoho One, Product Resources (https://www.zoho.com/one/resources.html), especially the Admin Guides description and links to organization administration. It supports the centralized administration role; detailed configuration belongs in Chapter 3.
