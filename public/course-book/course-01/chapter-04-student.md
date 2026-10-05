# CRM Data Architecture

## 1. What you will learn

A CRM record should help someone perform work, understand a customer and find reliable evidence. It should not become a container into which everyone places unrelated information.
Imagine that Meridian keeps the following information in one spreadsheet cell:
Northbank Studio, Taylor Ross, two printers, installation required, quote accepted, finance returned email, corrected, accepted.
You can read the sentence, but you cannot reliably answer:
- Is Northbank the customer organisation or a contact person?
- Which enquiry led to the order?
- Which quote was confirmed?
- What information was missing from the first packet?
- Which version did Finance accept?
- Did the customer’s billing email change, or was a missing value corrected?
- Who must perform the next task?
- How many unique orders were completed?
Data architecture is the design of records, fields and relationships that makes these questions answerable.
In this chapter, you will learn to use Zoho CRM’s standard record categories and build a small custom structure for Meridian’s enquiry and order-handoff evidence.
By the end, you should be able to:
 1. Explain the roles of Leads, Accounts, Contacts, Deals and activities.
 2. Decide whether information belongs in a standard module, a custom module, a field or a subform.
 3. Define what one record represents.
 4. Choose appropriate field types.
 5. Create relationships using lookup fields.
 6. Organise fields into a usable layout.
 7. Configure required and unique fields.
 8. Create criteria-based validation rules.
 9. Build a data dictionary that explains meaning, ownership and correction.
10. Trace a customer, opportunity, confirmed order and packet revision without confusing their identities.
11. Test normal records, missing information, duplicates and incorrect relationships.
Prerequisites
You need the training administration skills from Chapter 3:
- Identify the correct CRM organisation.
- Sign in with the appropriate administrator permissions.
- Distinguish personal settings from organisation settings.
- Keep laboratory identities separate from synthetic customer contacts.
No coding is required.
The full live exercise requires access to custom modules, custom fields, criteria-based validation and a custom subform. The official subform help identifies Professional edition and above for subforms. Other feature availability and available capacity must be checked in your training entitlement.
Continuity from the earlier chapters
The following decisions remain in force:
| Item | Preserved decision |
| --- | --- |
| Customer identity | Northbank Studio is MER-CUST-001 |
| Enquiry | MER-ENQ-001 |
| Sales contact | Taylor Ross is MER-CON-001 |
| Contact email | taylor.ross@example.com (mailto:taylor.ross@example.com) |
| Commercial quote | MER-QUOTE-001 |
| Confirmed order | MER-ORD-001 |
| Written confirmation | CONF-001 |
| Billing email | northbank.billing@example.com (mailto:northbank.billing@example.com) |
| Installation requirement | Yes |
| Sales preparation | Ava |
| Finance acceptance | Leo alone establishes the business decision |
| Process ownership | Noor |
| CRM responsibility | Sales relationships, commercial records and handoff history |
| Books responsibility | Financial records and current billing information |
| Training timing | UTC |
| Training home currency | GBP |

Chapter 1’s baseline remains:
- Six unique confirmed orders.
- Four accepted and two open at the supplied cutoff.
- Mean completed elapsed time of 195 minutes.
- Completed-case first-pass acceptance of 50%.
This chapter reconstructs a small subset for data-model practice. It does not replace the six-order baseline or establish that earlier chapters executed a product configuration.
Your contribution to the course project
You will build and document the CRM structure that later chapters use for:
- Lead capture and qualification.
- Sales-management views.
- Follow-up automation.
- Controlled transitions.
- Commercial records.
- Finance handoff.
- Reporting and reconciliation.
Your evidence is a relationship map, field dictionary, configured layouts, small linked dataset and validation-test record.
The next chapter will configure representative record and field access. In this chapter, creating an acceptance field does not yet enforce Finance-only acceptance.
## 2. Lessons

### Lesson 1 — Define what one record represents

Before choosing a module, complete this sentence:
One record represents one ______.
This is the record’s grain: the level of detail represented by a row.
For Meridian:
- One Account represents one commercial customer organisation.
- One Contact represents one person.
- One Deal represents one commercial opportunity.
- One Enquiry represents one distinct incoming request.
- One Order Packet represents one unique confirmed order being handed to Finance.
- One Packet Version represents one preserved revision of that order’s packet.
The grain determines how you count records and where you place repeating information.
If one order has two packet versions, you have:
- One order.
- Two versions.
- Potentially one return and one acceptance.
You do not have two orders merely because two submissions occurred.
Separate identity from description
A business identifier answers, “Which object is this?”
A description answers, “What is this object about?”
For example:
| Information | Value |
| --- | --- |
| Order Business ID | MER-ORD-001 |
| Packet Name | Northbank printer order |
| Opportunity Name | Northbank — two printers and installation |

Descriptions may change as wording improves. The business identifier should remain stable.
The CRM-generated record ID is another identifier. It belongs to the product’s local record. Preserve it in an environment crosswalk when needed, but do not replace the supplied business ID with it.
Worked example: a customer with two requests
Northbank first requests printers and later requests a separate equipment addition.
The customer remains one Account, but the two requests are two Enquiries. They may lead to one or two Deals depending on the commercial work involved.
A common mistake is to create another Account because a new enquiry arrived. That duplicates the customer rather than representing the new work.
Another mistake is to overwrite the first enquiry with the second. That destroys the history of the requests.
Check L1: If an order is returned, corrected and resubmitted, which identity remains stable, and which record category should preserve the new revision?
### Lesson 2 — Use standard CRM modules for their intended business meaning

Zoho CRM provides standard modules, including Leads, Accounts, Contacts, Deals and activities.^modules
Use those categories when their meaning fits the work. A custom module is justified by a requirement that the standard category does not represent clearly.
Leads: prospective relationships requiring qualification
A Lead contains information about a prospective relationship that has not yet been qualified into the appropriate customer and commercial records.
For example, Rowan Clarke from Papertrail Workspaces asks whether Meridian can supply equipment for a new office. Sales has not yet confirmed the need, purchasing process or commercial opportunity.
A lead can hold:
- Rowan’s name.
- Papertrail’s company name.
- Contact details.
- Qualification status.
- Follow-up activities.
The existence of a lead does not prove that the person has placed an order.
Zoho CRM supports lead conversion into relevant records such as Accounts, Contacts and Deals. The conversion procedure and mapping belong in Chapter 7.
Leads are not a universal enquiry ledger
A known customer can send several enquiries. It is not necessary to create a new unqualified lead for every request from that customer.
Meridian therefore makes a new explicit architecture decision:
Use an Enquiries custom module to preserve distinct intake requests. Use Leads when the request requires prospective-relationship qualification.
This avoids forcing every enquiry into a person-oriented qualification record.
Accounts: commercial customer organisations
An Account represents an organisation with which you do business or plan to do business.
Northbank Studio belongs in Accounts.
Its commercial identity should not be repeated independently inside every Contact and Deal. Related records should refer to the Account.
For the course, add a custom Customer Business ID field to Accounts. This preserves MER-CUST-001 separately from the product’s generated ID.
Contacts: people associated with the relationship
A Contact represents a person.
Taylor Ross belongs in Contacts and is associated with Northbank through the standard Account relationship.
A customer may have several contacts:
- A purchasing contact.
- A technical contact.
- A billing contact.
Do not assume that one person fills all three roles.
Taylor’s enquiry email and Northbank’s billing email have different purposes. This remains true even if the same customer organisation owns both addresses.
Deals: commercial opportunities
A Deal represents a specific commercial opportunity.
Northbank’s proposed purchase of two printers with installation is one opportunity. A later purchase can be another.
Deals include standard information such as:
- Deal Name.
- Account relationship.
- Contact relationship where relevant.
- Stage.
- Closing Date.
- Amount.
An Account can have several Deals. A Deal should not be used as the permanent customer identity.
For this chapter, the supplied historical opportunities use an existing Closed Won stage. Detailed pipeline definitions and stage-management rules belong in Chapter 8.
A won deal does not prove that Finance accepted the packet, created an invoice or received payment.
Activities: work to perform or record
Activities represent tasks, meetings and calls.
A task answers:
What must someone do, by when, and in relation to which record?
An order answers:
What business object is being processed?
A task to inspect a packet is not a second packet. Completing the task does not independently establish Finance acceptance.
The official task help states that the system-defined Completed task status closes a task; creating another field with the same label does not substitute for it.^records
Worked example
For Northbank:
| Business meaning | CRM home |
| --- | --- |
| Distinct incoming request | Enquiries custom module |
| Customer organisation | Accounts |
| Person | Contacts |
| Commercial opportunity | Deals |
| Confirmed-order handoff | Order Packets custom module |
| Preparation or review work | Tasks |

These records are linked. They are not different names for one row.
Check L2: Why should a service follow-up task not replace the customer’s Account or the Deal to which the task relates?
### Lesson 3 — Choose fields that express the information correctly

A field stores one attribute of a record.
Choosing the field type is a business decision because it determines how information can be entered, compared and validated.
| Field type | Suitable use |
| --- | --- |
| Single-line text | Identifiers or short references |
| Email | An email address |
| Date | A calendar date without an event time |
| Date/Time | An event requiring a timestamp |
| Number | A whole-number quantity |
| Currency | A monetary amount |
| Picklist | One option from an agreed set |
| Checkbox | A clearly defined true/false fact |
| Multi-line text | A longer explanation |
| Lookup | Association with another record |

Identifiers should usually be text
MER-CUST-001 is text, not a quantity.
A numeric field cannot represent its prefix. Even an identifier made only of digits may need text if leading zeros matter.
For example:
- Identifier: 000127.
- Quantity: 127 units.
These have different meanings.
Distinguish false from unknown
A checkbox can be unsuitable when you need three meanings:
- Yes.
- No.
- Not yet known.
For Meridian’s supplied confirmed packets, Installation Snapshot must be explicitly Yes or No.
Do not default it to No merely to make the form save. That could turn missing information into a false business assertion.
Event timestamps differ from creation timestamps
CRM records have system information such as Created Time.
If you reconstruct a September order during an October laboratory session:
- Created Time describes the October data-entry event.
- Confirmation Received At describes the supplied September business event.
Use the business-event field for the handoff measure.
Otherwise, a historically slow order could appear to take a few seconds because its records were entered during one laboratory session.
Mutable values differ from snapshots
A snapshot preserves information as it stood in a specific version or event.
Northbank’s current billing email may change in the future. The accepted September packet should still preserve the email that Finance accepted at that time.
The architecture therefore separates:
- Current customer information.
- Packet preparation information.
- Preserved packet-version information.
Worked example: field-type correction
Suppose Isha creates Confirmation Received At as a Date field.
The form can capture 14 September but not distinguish 09:00 from 15:00. That is insufficient for an elapsed-minute measure.
The official custom-field help states that a field’s type cannot be changed after creation.^fields
The correct recovery is to create a properly typed Date/Time field, preserve and move any existing information through a controlled correction, and update the dictionary and dependent configuration.
Do not delete a populated field simply to make its label look correct.
Check L3: Which field type should hold MER-ORD-001, which should hold 2026-09-14T09:00:00Z, and why should neither be substituted with Created Time?
### Lesson 4 — Use lookups for relationships

A lookup associates one record with another record.
A text field containing Northbank Studio is a description. A lookup selecting Northbank’s Account establishes a CRM relationship.
With an Account lookup on Order Packets:
- One Order Packet selects one Account.
- One Account can have several Order Packets.
This is a one-to-many relationship.
Meridian’s proposed relationships
| Child record | Lookup |
| --- | --- |
| Contact | Account Name |
| Deal | Account Name |
| Enquiry | Customer |
| Enquiry | Sales Contact |
| Enquiry | Related Opportunity |
| Order Packet | Customer |
| Order Packet | Related Opportunity |
| Packet Version | Order Packet |
| Order Packet | Accepted Version |

The last relationship identifies which revision Finance accepted.
It does not create another version. It points to an existing version.
A lookup does not prove business consistency
Suppose an Order Packet belongs to Northbank but its Related Opportunity lookup selects Redwood’s deal.
Both selected records exist. The individual lookups can still be wrong as a combination.
A relationship test must therefore ask:
Does the selected opportunity belong to the same customer as the packet?
The core exercise checks this manually.
Do not assume that a lookup automatically enforces every cross-record business rule. Lookup filters and further controls require their own configuration and availability checks.
Lookup creation procedure
The documented procedure is:
1. Open Setup → Customization → Modules and Fields.
2. Select the module and layout.
3. Drag Lookup into the layout.
4. Set the field label.
5. Select the lookup module.
6. Name the related list.
7. Click Done.
8. Save the layout.^fieldtypes
For the Packet Versions module:
- Field label: Order Packet.
- Lookup module: Order Packets.
- Related list title: Packet Versions.
Expected result: a version can select an existing packet, and the packet’s detail page can show its related versions.
Recovery: if you selected the wrong parent record, correct the association using the supplied evidence. If the lookup was designed against the wrong module, correct the design before loading dependent records.
Quote references in this chapter
MER-QUOTE-001 remains a supplied business reference.
The exercise stores it as Quote Business ID Snapshot. It does not create a quote lookup yet because the commercial quote records and their product configuration are taught in Chapter 12.
A text reference preserves the supplied identifier. It does not prove that a quote record exists in CRM.
Check L4: Why is selecting an existing Deal insufficient evidence that it is the correct Deal for an Order Packet?
### Lesson 5 — Use custom modules and subforms for different needs

A custom module represents a business record category that needs its own identity, relationships and lifecycle.
A subform stores repeated rows inside a parent record.
These are not interchangeable design choices.
When a custom module is appropriate
Use a custom module when the object needs to be:
- Identified independently.
- Related to other records.
- Followed through its own status.
- Assigned or reported as a business object.
- Retained as a distinct historical item.
Meridian uses three custom organisation modules:
1. Enquiries.
2. Order Packets.
3. Packet Versions.
Packet Versions are separate because the first returned revision and the later accepted revision must remain distinguishable.
Putting only the latest values on the parent packet would erase the evidence needed to explain rework.
Creating the custom modules
The official module procedure uses:
1. Setup → Customization → Modules and Fields.
2. Create New Module.
3. Select Organization modules.
4. Enter the singular and plural names.
5. Save the module.
6. Select its Teamspace placement where the interface requests it.
7. Set module access for the intended profiles.
8. Save.^custommodules
For the build exercise, keep the new modules available to Isha’s Administrator profile while the design is tested.
Representative Sales and Finance access will be configured in Chapter 5.
Expected result: the three modules appear in the intended training CRM context and can be configured by Isha.
When a subform is appropriate
A packet version can cite several supporting references.
These references belong to that version. They do not require their own approval process in this exercise.
Use a standard subform called Supporting References, with:
- Evidence Reference.
- Evidence Kind.
- Evidence Note.
This is different from storing Packet Versions themselves as unstructured notes.
Creating the subform
The documented procedure is:
1. Open the Packet Versions layout.
2. Drag the Subform block into the layout.
3. Choose Standard.
4. Name it Supporting References.
5. Set a maximum of five rows for this training design.
6. Leave the subform optional.
7. Add the three specified columns.
8. Save.^subforms
Five rows is Meridian’s small training-design limit, not a universal product quota.
The subform type is chosen when it is created. The help states that its type cannot simply be changed afterward.
Expected result: a packet version can preserve several structured evidence-reference rows.
Required subform fields do not always require a subform
The official help distinguishes:
- An optional subform with no rows.
- An entered row whose required columns must be completed.
- A required subform that must contain information.
For this exercise:
- Supporting References is optional.
- Evidence Reference and Evidence Kind are required when a row is entered.
- Evidence Note is optional.
The main packet fields carry the required submission information. The subform is additional structured evidence.
A subform is not automatically an immutable audit trail
Rows can be edited according to the available permissions and configuration.
Keeping revision records and reference rows preserves structure, but that alone does not guarantee that users cannot rewrite accepted history.
Chapter 5 will restrict relevant field access. Chapter 10 will establish controlled process transitions.
Check L5: Why does Meridian use a separate Packet Versions module for revisions but a subform for their supporting references?
### Lesson 6 — Design layouts around a task

A layout determines the fields and sections presented for a record.
A layout can make good data easier to enter by grouping information in the order the user needs it.
For Packet Versions, use:
1. Identity and Parent.
2. Packet Snapshot.
3. Review Evidence.
4. Supporting References.
This sequence answers:
- Which version am I entering?
- Which order does it belong to?
- What information does this version contain?
- What happened during review?
- Which references support it?
One layout is enough for the base exercise
Do not create separate layouts merely because two people use the record.
Ava and Leo may work with the same packet version while having different field permissions and transition authority.
Layout design and authorization are related but separate.
The exercise uses each custom module’s Standard layout, reorganised into the specified sections.
Editing a layout
Use Setup → Customization → Modules and Fields, select the module and its layout, then drag fields and sections into the required order.
Save and preview the layout.^custommodules
The documented preview can show the layout for a selected profile. Use it to inspect presentation, but still perform live user-access tests when permissions are configured.
Creating an additional layout
If a genuine variation requires different fields or mandatory information, the documented procedure is:
1. Select the module.
2. Choose Create New Layout.
3. Name it.
4. Add or organise fields and sections.
5. Select Save Layout.
6. Assign the permitted profiles.^layouts
Validation rules are layout-specific. Adding another layout therefore creates another configuration surface to inspect.
For example, a later specialised order type might have additional information requirements. That would justify considering another layout. Simply hiding Finance fields in a Sales layout is not a complete security design.
Check L6: If you create a second layout, why should you review its validation rules and profile assignment?
### Lesson 7 — Combine required fields, uniqueness and validation

These controls solve different problems.
| Control | Question it answers |
| --- | --- |
| Required field | Must a value be present? |
| Field type | Is the value represented in the appropriate form? |
| Unique field | Has this identity value already been used in the module? |
| Validation rule | Does the value satisfy the specified condition? |
| Permission | Is this user allowed to establish or change it? |
| Relationship check | Do the associated records agree with the business case? |

No single control proves all six.
Required fields
Make identity and essential relationship fields required.
For a Packet Version, Version Business ID, parent Order Packet, revision number and the supplied snapshot references are required.
Billing Email Snapshot is conditionally required for Submitted or Accepted versions.
Why not require it for every record?
Because the historical returned first version of MER-ORD-002 genuinely lacked the email. The architecture must preserve that exception rather than falsifying it.
Unique fields
Mark the supplied business-ID fields unique using the documented Do not allow duplicate values option.^fields
For example, Order Business ID is unique in Order Packets.
This blocks a second manually created order packet carrying MER-ORD-001 once the configured uniqueness check is effective.
Uniqueness is scoped to a module. It does not prove global identity across every application.
The official help also describes indexing delay and channel-specific behavior. Test the actual entry routes used later; do not treat a manual duplicate test as proof for every migration or synchronization path.
Criteria-based validation
Use criteria-based rules for the core exercise. Functions and external checks are outside this course’s scope.
The documented procedure is:
 1. Open Setup → Customization → Modules and Fields.
 2. Select Packet Versions.
 3. Open Validation Rules.
 4. Select Create New Validation Rule.
 5. Choose the Standard layout and primary field.
 6. Select Based on Criteria.
 7. Select Save Only.
 8. Define the primary condition.
 9. Select whether the rule executes when the criterion is met.
10. Define the secondary record condition.
11. Set the error message and Stop with error behavior where presented.
12. Save.^validation
For the email rule:
- Primary field: Billing Email Snapshot.
- Primary condition: is empty.
- Secondary condition: Review Outcome is Submitted or Accepted.
- Execute when criteria is met.
- Message: Enter the confirmed billing email before submitting or accepting this version.
Expected result: a manually saved Submitted version with a blank email is blocked. A Returned historical version with the supplied blank email can be retained.
Presence is not truth
A syntactically valid email is not necessarily the confirmed billing email.
taylor.ross@example.com could be valid email syntax but still be wrong for the billing field.
Likewise, an acceptance timestamp proves only that a timestamp was entered unless the process also establishes who may enter it and when.
Validation and permission must work together.
The accessed validation documentation describes supported interfaces and interactions with other entry or update routes. The chapter’s tests establish manual web-form behavior only. Imports, webforms, workflow updates and controlled transitions need their own tests in the relevant chapters.
Check L7: Why should the email rule allow a historical Returned version to remain blank but block a Submitted version with the same blank value?
### Lesson 8 — Write a data dictionary that someone else can use

A data dictionary records what each field means, how it is stored and how it should be used.
A useful dictionary includes:
- Module and field label.
- Meaning.
- Type.
- Requiredness.
- Allowed values.
- Relationship target.
- Business authority.
- Correction or historical treatment.
It should distinguish current facts from snapshots and identifiers from descriptions.
Labels and technical names
A field label is the name users see.
An API name is the product’s technical field reference. Zoho’s developer documentation distinguishes API names from visible labels.^metadata
This chapter does not require an API call.
Record actual technical names in an environment companion sheet when needed. Do not assume that a label such as “Customer Business ID” guarantees a particular generated API name.
Worked dictionary entry
| Attribute | Completed definition |
| --- | --- |
| Module | Packet Versions |
| Field | Billing Email Snapshot |
| Meaning | Customer-confirmed billing email contained in this particular packet revision |
| Type | Email |
| Requiredness | Required when Review Outcome is Submitted or Accepted |
| Authority | Sales supplies confirmed evidence; Finance establishes acceptance of the version |
| Historical treatment | Preserve earlier missing or different values in their original versions |
| Correction | Create or use the next version with the permitted correction |
| Not equivalent to | Sales contact email or current Books billing master |

This definition explains more than a field name. It tells a future administrator why a current email should not overwrite the historical snapshot.
Check L8: What important meaning would be lost if the dictionary described this field only as “Customer email”?
## 3. Visual explanation — Meridian’s record relationships

erDiagram
    ACCOUNT ||--o{ CONTACT : has
    ACCOUNT ||--o{ DEAL : has
    ACCOUNT o|--o{ ENQUIRY : identified_for
    CONTACT o|--o{ ENQUIRY : sent_by
    DEAL o|--o{ ENQUIRY : develops_into
    ACCOUNT ||--o{ ORDER_PACKET : customer_for
    DEAL ||--o{ ORDER_PACKET : opportunity_for
    ORDER_PACKET ||--o{ PACKET_VERSION : has
    ORDER_PACKET o|--o| PACKET_VERSION : selects_accepted_version
    PACKET_VERSION ||--o{ SUPPORTING_REFERENCE : contains
The diagram shows the intended business relationships.
An Enquiry can initially have no identified Account, Contact or Deal. This permits prospective or incomplete intake without creating false customer records.
An Order Packet in this confirmed-order exercise has one customer and one related opportunity.
A Packet Version belongs to one Order Packet. Several versions can belong to the same order.
Accepted Version is a selection of one existing related revision. The diagram’s cardinality does not prove that the selected version belongs to the same order; the exercise includes that consistency check.
Supporting References are parent-dependent subform rows.
Leads and activities are not shown in this diagram because they serve additional qualification and work-tracking purposes. A prospect can be qualified through Leads, and a task can be associated with the relevant person or business record.
## 4. Worked case — Build the record model and dictionary

Explicit additions to the case
This chapter introduces:
- MER-DEAL-001: Northbank’s commercial opportunity.
- MER-DEAL-002: a second opportunity for MER-CUST-002.
- Redwood Office Co as the supplied name for MER-CUST-002.
- Alex Rivera as Contact MER-CON-002.
- Three packet-version business IDs.
- One laboratory task.
The opportunity amounts are synthetic exercise estimates. They are not invoice amounts, payment evidence or an established quote-line calculation.
Complete standard-record inputs
Accounts
customer_business_id,account_name
MER-CUST-001,Northbank Studio
MER-CUST-002,Redwood Office Co
Contacts
contact_business_id,first_name,last_name,email,customer_business_id
MER-CON-001,Taylor,Ross,taylor.ross@example.com,MER-CUST-001
MER-CON-002,Alex,Rivera,alex.rivera@example.com,MER-CUST-002
Deals
opportunity_business_id,deal_name,customer_business_id,contact_business_id,closing_date,stage,amount_gbp
MER-DEAL-001,Northbank - two printers and installation,MER-CUST-001,MER-CON-001,2026-09-14,Closed Won,1200.00
MER-DEAL-002,Redwood - office equipment,MER-CUST-002,MER-CON-002,2026-09-14,Closed Won,800.00
The linked Account, Contact and Deal must agree. Northbank’s Deal must not point to Alex’s Redwood Contact.
Complete custom-record inputs
Enquiry
The received timestamp is a new synthetic reconstruction input.
enquiry_business_id,enquiry_name,received_at,sender_name,sender_email,intake_type,summary,customer_business_id,contact_business_id,opportunity_business_id
MER-ENQ-001,Northbank printer enquiry,2026-09-11T08:30:00Z,Taylor Ross,taylor.ross@example.com,Existing customer,Two office printers with installation,MER-CUST-001,MER-CON-001,MER-DEAL-001
Order Packets
order_business_id,packet_name,customer_business_id,opportunity_business_id,confirmation_received_at,packet_status,accepted_version_business_id
MER-ORD-001,Northbank printer order,MER-CUST-001,MER-DEAL-001,2026-09-14T09:00:00Z,Accepted,MER-PVER-001-01
MER-ORD-002,Redwood equipment order,MER-CUST-002,MER-DEAL-002,2026-09-14T09:15:00Z,Accepted,MER-PVER-002-02
Packet Versions
The first submission and final acceptance timestamps preserve Chapter 1.
The return at 11:00 and corrected resubmission at 14:00 for MER-ORD-002 are explicit additional synthetic trace details.
version_business_id,version_name,order_business_id,revision_number,customer_id_snapshot,quote_id_snapshot,confirmation_ref_snapshot,installation_snapshot,billing_email_snapshot,billing_evidence_ref,submitted_at,review_outcome,return_reason,accepted_at,reviewer_reference
MER-PVER-001-01,Northbank revision 1,MER-ORD-001,1,MER-CUST-001,MER-QUOTE-001,CONF-001,Yes,northbank.billing@example.com,CONF-001,2026-09-14T09:30:00Z,Accepted,,2026-09-14T10:00:00Z,MER-USR-003
MER-PVER-002-01,Redwood revision 1,MER-ORD-002,1,MER-CUST-002,MER-QUOTE-002,CONF-002,No,,,2026-09-14T10:15:00Z,Returned,Billing email missing,,MER-USR-003
MER-PVER-002-02,Redwood revision 2,MER-ORD-002,2,MER-CUST-002,MER-QUOTE-002,CONF-002,No,redwood.billing@example.com,BILL-002,2026-09-14T14:00:00Z,Accepted,,2026-09-14T14:15:00Z,MER-USR-003
For historical review evidence, MER-USR-003 identifies Leo. It is a business reference, not a claim that the currently signed-in administrator is Leo.
The separately supplied return event is:
| Version | Return timestamp |
| --- | --- |
| MER-PVER-002-01 | 2026-09-14T11:00:00Z |

Use the timestamp in the supporting note. The base model does not add a separate Returned At field.
Supporting References
version_business_id,evidence_reference,evidence_kind,evidence_note
MER-PVER-001-01,CONF-001,Customer confirmation,Confirms order and supplied billing address
MER-PVER-002-01,RETURN-002,Finance return,Returned at 2026-09-14T11:00:00Z because billing email was missing
MER-PVER-002-02,CONF-002,Customer confirmation,Original order confirmation
MER-PVER-002-02,BILL-002,Billing correction,Customer-confirmed correction to redwood.billing@example.com
Task
| Task attribute | Supplied value |
| --- | --- |
| Subject | MER-TASK-001 — Inspect Redwood packet relationships |
| Owner | Ava’s controlled training identity |
| Due date | 2026-10-15 |
| Contact | Alex Rivera, MER-CON-002 |
| Related business record | Redwood’s Deal, MER-DEAL-002 |
| Status | Existing open status, such as Not Started |
| Description | Laboratory data-model verification only. Check the customer, opportunity and packet links. Do not contact the customer. |
| Reminder | None |
| Recurrence | None |

Completed field dictionary
Use R for required at record creation, C for conditionally required and O for optional.
System-required fields remain in place. The tables identify the fields used or added for this exercise.
Standard modules
| Module | Field | Type | Requirement |
| --- | --- | --- | --- |
| Leads | Prospect Business ID | Single-line text, unique | R when used in the challenge |
| Leads | First Name | Standard text | O |
| Leads | Last Name | Standard text | System requirement |
| Leads | Company | Standard text | Supply for this B2B exercise |
| Leads | Email | Standard email | Supply in challenge |
| Accounts | Account Name | Standard text | System requirement |
| Accounts | Customer Business ID | Single-line text, unique | R |
| Contacts | First Name | Standard text | O |
| Contacts | Last Name | Standard text | System requirement |
| Contacts | Email | Standard email | Supply in sample |
| Contacts | Account Name | Standard lookup to Accounts | R for sample |
| Contacts | Contact Business ID | Single-line text, unique | R |
| Deals | Deal Name | Standard text | System requirement |
| Deals | Account Name | Standard lookup to Accounts | Required in sample |
| Deals | Contact Name | Standard lookup to Contacts | Supply in sample |
| Deals | Closing Date | Standard date | Required in sample |
| Deals | Stage | Standard picklist | Required in sample |
| Deals | Amount | Standard currency | Supply in sample |
| Deals | Opportunity Business ID | Single-line text, unique | R |
| Tasks | Subject | Standard text | System requirement |
| Tasks | Owner, Due Date and Status | Standard fields | Supply in sample |
| Tasks | Contact and related record | Standard associations | Supply in sample |
| Tasks | Description | Standard multi-line text | Supply in sample |

Enquiries
| Field | Type | Requirement |
| --- | --- | --- |
| Enquiry Name | Default name field, text | R |
| Enquiry Business ID | Single-line text, unique | R |
| Received At | Date/Time | R |
| Sender Name | Single-line text | R |
| Sender Email | Email | R for exercise |
| Intake Type | Picklist | R |
| Enquiry Summary | Multi-line text, small | R |
| Customer | Lookup to Accounts | O |
| Sales Contact | Lookup to Contacts | O |
| Related Opportunity | Lookup to Deals | O |

Order Packets
| Field | Type | Requirement |
| --- | --- | --- |
| Packet Name | Default name field, text | R |
| Order Business ID | Single-line text, unique | R |
| Customer | Lookup to Accounts | R |
| Related Opportunity | Lookup to Deals | R |
| Confirmation Received At | Date/Time | R |
| Packet Status | Picklist | R |
| Accepted Version | Lookup to Packet Versions | C |

Packet Versions
| Field | Type | Requirement | Meaning or rule |
| --- | --- | --- | --- |
| Version Name | Default name field, text | R | Readable revision description |
| Version Business ID | Single-line text, unique | R | Stable identity of this revision |
| Order Packet | Lookup to Order Packets | R | Parent confirmed order |
| Revision Number | Number | R | Whole number of at least 1 |
| Customer ID Snapshot | Single-line text | R | Customer business ID preserved in this revision |
| Quote Business ID Snapshot | Single-line text | R | Supplied commercial quote reference |
| Confirmation Reference Snapshot | Single-line text | R | Written confirmation reference |
| Installation Snapshot | Picklist | R | Yes or No; no assumed default |
| Billing Email Snapshot | Email | C | Required for Submitted or Accepted; preserves this revision’s supplied value |
| Billing Evidence Reference | Single-line text | C | Required for Submitted or Accepted |
| Submitted At | Date/Time | C | Submission event; entered for the supplied Submitted, Returned and Accepted records |
| Review Outcome | Picklist | R | Draft; Submitted; Returned; Accepted |
| Return Reason | Single-line text | C | Required when Returned |
| Accepted At | Date/Time | C | Required when Accepted |
| Reviewer Reference | Single-line text | C | Required for Returned or Accepted; supplied historical business user reference |
| Supporting References | Standard subform | O | Repeated references belonging to this version |

Supporting References subform
| Column | Type | Requirement |
| --- | --- | --- |
| Evidence Reference | Single-line text | Required when a row is entered |
| Evidence Kind | Picklist | Required when a row is entered |
| Evidence Note | Multi-line text, small | O |

For historical reconstruction, Isha enters the records as the administrator. System Created By and Modified By identify that laboratory entry. Reviewer Reference preserves the supplied historical participant assertion.
Do not present that assertion field as an authenticated approval control.
Completed validation specification
Configure these rules on Packet Versions’ Standard layout.
For each rule, the primary condition identifies an invalid value, so use When criteria is met.
| Rule | Primary field and invalid condition | Secondary record condition |
| --- | --- | --- |
| V01 | Billing Email Snapshot is empty | Outcome is Submitted or Accepted |
| V02 | Billing Evidence Reference is empty | Outcome is Submitted or Accepted |
| V03 | Revision Number is less than 1 | All records |
| V04 | Accepted At is empty | Outcome is Accepted |
| V05 | Reviewer Reference is empty | Outcome is Returned or Accepted |
| V06 | Return Reason is empty | Outcome is Returned |
| V07 | Submitted At is empty | Outcome is Submitted, Returned or Accepted |

Use Save Only and Stop with error for the exercise.
The core model also requires these manual consistency checks:
- Version customer snapshot matches its parent customer.
- Parent opportunity belongs to the parent customer.
- Accepted Version belongs to the parent packet.
- Accepted timestamp is not before confirmation or submission.
- Parent Accepted status has an Accepted Version.
- Accepted historical values are not overwritten by correction.
These checks are part of the artifact requirements. They are not claimed to be automatically enforced by V01–V07.
Worked creation sequence
 1. Create the standard-module business-ID fields.
 2. Create Enquiries, Order Packets and Packet Versions.
 3. Add fields and forward lookups.
 4. Add Accepted Version after Packet Versions exists.
 5. Add Supporting References.
 6. Configure V01–V07.
 7. Create Accounts, Contacts and Deals.
 8. Create the Enquiry.
 9. Create the two parent Order Packets initially as Draft, with Accepted Version blank.
10. Create the three historical versions.
11. Select the supplied accepted versions on the parents and set their statuses to Accepted.
12. Create the supplied task.
13. Verify every relationship.
The temporary Draft state is a loading sequence. It does not change the supplied historical end state.
Completed reasoning
Northbank has one packet and one accepted version.
Redwood has one packet and two versions:
- Revision 1 preserves the missing billing email and Finance return.
- Revision 2 preserves the permitted correction and acceptance.
The corrected email is redwood.billing@example.com, supported by BILL-002. The earlier missing value remains visible in revision 1.
Counting correctly
There are two completed orders in this subset.
First-pass completed orders:
- Northbank: Yes.
- Redwood: No.
First-pass rate = 1 ÷ 2 × 100% = 50%
Counting two Accepted versions among three version records would produce:
2 ÷ 3 × 100% = 66.7%
That answers a different version-level question. It is not the completed-order first-pass rate.
Mistake and correction
Mistake: Replace Redwood revision 1’s blank email with the corrected email, then mark that same version Accepted.
Correction: Preserve revision 1 as Returned. Create revision 2 with the supplied correction and select revision 2 as the accepted version.
The correction protects the evidence explaining why the order was not first-pass.
## 5. Try it yourself — Guided practice

Learning goal
Build Meridian’s CRM data model, create the supplied linked records and demonstrate that the architecture preserves both normal work and correction history.
Required access
Use the dedicated training CRM organisation.
Isha needs the relevant module and field customization permissions, validation-rule permissions and record-creation access.
The training entitlement must expose the required custom modules, fields and subform block.
Use only synthetic case data. No customer email is sent in this exercise.
Complete task inputs
Use every dataset and rule in Section 4.
For the negative tests, use these additional inputs:
| Test | Supplied attempt |
| --- | --- |
| T01: normal reconstruction | Create Northbank’s accepted revision with all supplied values |
| T02: historical missing data | Create Redwood revision 1 as Returned with blank email and evidence reference, supplied reason, submission time and reviewer |
| T03: invalid submission | New scratch version MER-PVER-TEST-001; parent MER-ORD-002; revision 3; Redwood snapshot references; Submitted; submitted at 2026-10-15T10:00:00Z; billing email blank; evidence BILL-002 |
| T04: invalid revision | Change scratch version revision number to 0 |
| T05: duplicate order | Attempt a second Order Packet using MER-ORD-001 and the same customer/opportunity |
| T06: wrong relationship | Scratch version selects parent MER-ORD-001 but Customer ID Snapshot is MER-CUST-002 |
| T07: missing acceptance timestamp | Change scratch outcome to Accepted; set reviewer MER-USR-003; leave Accepted At blank |
| T08: denied customization | Ava is a non-administrator without customization permission and attempts to alter the module |

For T03, the complete scratch snapshot is:
| Field | Value |
| --- | --- |
| Version Name | Scratch Redwood validation test |
| Version Business ID | MER-PVER-TEST-001 |
| Order Packet | MER-ORD-002 |
| Revision Number | 3 |
| Customer ID Snapshot | MER-CUST-002 |
| Quote Business ID Snapshot | MER-QUOTE-002 |
| Confirmation Reference Snapshot | CONF-002 |
| Installation Snapshot | No |
| Billing Email Snapshot | Initially blank |
| Billing Evidence Reference | BILL-002 |
| Submitted At | 2026-10-15T10:00:00Z |
| Review Outcome | Submitted |
| Return Reason | Blank |
| Accepted At | Blank |
| Reviewer Reference | Blank while Submitted |

T07’s accepted timestamp is only a scratch-test input. It does not change Redwood’s historical acceptance.
Learner worksheets
Module decisions
| Business object | One record represents | Standard or custom home |
| --- | --- | --- |
| Customer |  |  |
| Person |  |  |
| Opportunity |  |  |
| Enquiry |  |  |
| Order packet |  |  |
| Packet version |  |  |
| Supporting reference |  |  |

Field dictionary extension
Use this worksheet for actual technical names and any environment-specific mandatory fields.
| Module | Visible field label | Actual technical name, if recorded |
| --- | --- | --- |
|  |  |  |

Do not fill the technical-name column by guessing.
Test evidence
| Test | Expected result | Actual result | Correction performed |
| --- | --- | --- | --- |
| T01 |  |  |  |
| T02 |  |  |  |
| T03 |  |  |  |
| T04 |  |  |  |
| T05 |  |  |  |
| T06 |  |  |  |
| T07 |  |  |  |
| T08 |  |  |  |

Guided steps and expected intermediate results
Step 1 — Inspect the existing configuration
Open the intended CRM organisation and inspect Accounts, Contacts, Deals and Leads.
Check whether the supplied fields or case records already exist.
Expected result: you know which additions are necessary. Existing case records are reused when their identifiers and relationships match.
Step 2 — Add standard-module business identifiers
Add:
- Customer Business ID to Accounts.
- Contact Business ID to Contacts.
- Opportunity Business ID to Deals.
- Prospect Business ID to Leads.
Use single-line text and the unique setting. Make them required for the training design.
The documented field procedure is to open the module layout, drag the field type from the tray, set properties and save.^fields
Expected result: each relevant standard module has a separate business-ID field.
Step 3 — Create custom modules and fields
Create the three custom organisation modules and all dictionary fields.
Keep their default name fields as text, renamed to the descriptive labels in the dictionary. Business IDs remain separate unique text fields.
Expected result: every field has the intended type; there is no attempt to use a numeric field for a business identifier.
Step 4 — Create and inspect lookups
Add the relationships from Lesson 4.
Set useful related-list titles, such as Enquiries, Order Packets and Packet Versions.
Expected result: each lookup selects records from the intended module, and related lists show the reverse association.
Step 5 — Organise layouts and the subform
Use the supplied sections. Add Supporting References to Packet Versions.
Expected result: the version form separates identity, snapshot, review information and reference rows.
Step 6 — Configure and test validation
Create V01–V07.
Run T03 and T04 before entering the full reconstruction if that helps confirm the criteria.
Expected result: the invalid submission and revision are blocked; the supplied corrections permit a valid scratch save.
Step 7 — Create standard records
Use the documented creation forms:
- Accounts: add the Account and save.
- Contacts: create the Contact, select its Account and save.
- Deals: create the Deal, select the supplied relationships and values, then save.^records
Expected result: two Accounts, two Contacts and two Deals exist with consistent links.
Retain any additional system-required fields shown by the actual layout. If the supplied case does not provide a genuinely required value, record the blocker rather than inventing it.
Step 8 — Create the custom reconstruction
Use each custom module’s new-record form.
Follow Section 4’s parent-first sequence, then enter the reference rows and select the accepted revisions.
Expected result: one Enquiry, two Order Packets and three historical Packet Versions are linked correctly.
Step 9 — Create the task
Use Tasks → Create Task, enter the supplied task details and save.^records
Expected result: the task is related to Alex and Redwood’s opportunity. It remains an open laboratory inspection task until deliberately completed.
Step 10 — Run the remaining tests
Complete T01–T08.
T06 is a manual relationship-consistency test. A record that can be saved is not automatically a record that passes the business check.
Expected result: the evidence distinguishes system validation, duplicate detection, manual relationship checking and denied customization.
Step 11 — Reconcile the final artifact
After removing the scratch test record, the intended persistent dataset is:
| Module | Expected records |
| --- | --- |
| Accounts | 2 |
| Contacts | 2 |
| Deals | 2 |
| Enquiries | 1 |
| Order Packets | 2 |
| Packet Versions | 3 |
| Tasks | 1 |
| Leads | 0 in the base dataset |

Supporting-reference rows:
- Northbank revision 1: one.
- Redwood revision 1: one.
- Redwood revision 2: two.
Total: four subform rows.
Final artifacts
Create:
- C01_CH04_Meridian_CRM_Data_Model.md
- C01_CH04_Meridian_Field_Dictionary.md
- C01_CH04_Meridian_Layout_and_Validation.md
- C01_CH04_Meridian_Record_Crosswalk.csv
- C01_CH04_Meridian_Data_Model_Tests.md
The crosswalk records actual CRM IDs only after creation or observation. Preserve business IDs in their own columns.
Cleanup and recovery
Remove only the clearly identified scratch version MER-PVER-TEST-001 after the tests. It must not remain selected as an accepted version.
Keep the historical dataset and model for later chapters.
If a field was placed incorrectly, move it or correct the layout. The official help distinguishes removing a field to Unused Fields from permanently deleting it.^fields
If a validation rule was configured incorrectly, edit or temporarily deactivate that rule, correct it and retest. Do not delete historical records to make the rule appear successful.
Offline alternative
Without the required training entitlement, complete the model, dictionary, sample-record tables and expected test traces on paper.
The offline artifact cannot demonstrate actual field creation, saved validation, duplicate blocking, subform behavior or product access denial.
Mark those results as expected or blocked.
## 6. Independent challenge — Represent repeated customer requests and a new prospect

Meridian receives three additional requests.
These are new synthetic inputs, separate from the September reconstruction.
Complete incoming-request dataset
enquiry_business_id,received_at,sender_name,sender_email,company_name,customer_business_id,contact_business_id,intake_type,summary
MER-ENQ-003,2026-10-16T09:00:00Z,Taylor Ross,taylor.ross@example.com,Northbank Studio,MER-CUST-001,MER-CON-001,Existing customer,Additional equipment for a meeting room
MER-ENQ-004,2026-10-16T09:15:00Z,Casey Morgan,casey.morgan@example.com,Northbank Studio,MER-CUST-001,MER-CON-003,Existing customer,Separate request for reception equipment
MER-ENQ-005,2026-10-16T09:30:00Z,Rowan Clarke,rowan.clarke@example.com,Papertrail Workspaces,,,Prospective,Advice on equipment for a planned office
Additional facts:
- Casey Morgan is a new person at the existing Northbank customer.
- MER-CON-003 is the supplied new contact business ID.
- Rowan has not been qualified.
- MER-LEAD-001 is Rowan’s supplied prospect business ID.
- No Account business ID has been assigned to Papertrail.
- No opportunity has been established for any of these three new enquiries.
- No order or quote has been confirmed.
- A qualification task is needed for Rowan.
Qualification task inputs
| Attribute | Value |
| --- | --- |
| Subject | MER-TASK-002 — Qualify Papertrail request |
| Owner | Ava |
| Due date | 2026-10-19 |
| Associated person | Rowan’s Lead |
| Status | Existing open task status |
| Description | Confirm the requirement and purchasing process. No order is established by this request. |
| Reminder | None |
| Recurrence | None |

Deliverables
Create C01_CH04_Enquiry_Architecture_Challenge.md containing:
1. The proposed new Enquiry records and their relationships.
2. Any new Contact or Lead records required.
3. The qualification task’s association.
4. Fields that must remain intentionally unfilled.
5. An explanation of why no new Northbank Account is required.
6. An explanation of why the prospective request does not establish an order.
7. One duplicate test and its expected recovery.
8. The final record counts if the challenge is added to the cleaned base dataset.
You may propose an additional lookup from the Lead to its originating Enquiry. If you do, define its purpose and record it in the dictionary. It must not be presented as a relationship automatically created by the base model.
Success criteria
Your answer must preserve:
- One Northbank customer identity.
- Separate enquiry identities.
- Casey’s separate person identity.
- Rowan’s unqualified status.
- The difference between a missing association and permission to invent a record.
- The base September order and version history.
## 7. Common problems and recovery

| Symptom | Diagnosis | Correction |
| --- | --- | --- |
| One “customer” field contains company and person | Two entities were combined | Separate Account and Contact; associate them |
| Another enquiry creates another Northbank Account | Intake was confused with customer identity | Reuse MER-CUST-001; create a new Enquiry |
| Corrected packet destroys the missing-value history | Current values replaced the historical revision | Preserve Returned revision; create corrected revision |
| Business IDs lose prefixes or leading zeros | Wrong field type | Use text identifiers |
| Confirmation time cannot be entered | Date field used instead of Date/Time | Create correctly typed field and move data carefully |
| Deal lookup points to another customer | Existing record mistaken for correct record | Select the supplied matching Deal |
| Version snapshot customer differs from parent | Cross-record consistency was not checked | Correct the supplied association or snapshot using evidence |
| Email rule blocks the historical Returned record | Rule applies to the wrong outcomes | Restrict its secondary condition to Submitted or Accepted |
| Invalid submission saves after a rule was created | Wrong layout, criterion or execution option | Inspect the selected layout and criteria direction |
| Duplicate order appears immediately after uniqueness setup | Configuration may not yet be indexed, or wrong field was tested | Confirm the unique property and allow indexing; investigate existing duplicate safely |
| Required subform columns do not force any rows | Subform itself is optional | Decide whether rows are genuinely required; preserve base design |
| Accepted timestamp is entered by Sales | Data field exists without decision control | Apply later access and transition controls |
| Report counts three orders | Version grain used instead of order grain | Count Order Packets for unique orders |
| Created Time is used as confirmation time | Laboratory entry event confused with business event | Use Confirmation Received At |
| Field disappears after layout editing | Field may be in Unused Fields | Restore it through the documented layout procedure |

A failed test should lead to a specific correction and repeated verification.
Do not respond by deleting the entire custom module. The official module help explains that deleting a custom module also deletes its associated records and configuration.^custommodules
## 8. Check your understanding

 1. Explain the difference between Account, Contact and Deal using Northbank.
 2. Why does Meridian retain an Enquiry module even when Leads is available?
 3. What does one Packet Version represent?
 4. Which fields preserve business identity, and which identify the actual local CRM records?
 5. Why should Billing Email Snapshot be separate from a current billing master?
 6. Calculate confirmation-to-acceptance elapsed time for the two supplied orders.
 7. Explain why two Accepted versions out of three versions is not a 66.7% order first-pass rate.
 8. Why can a lookup be structurally valid but commercially wrong?
 9. Which controls detect a blank email, a repeated order ID and an unauthorized acceptance action?
10. Why is Reviewer Reference not an authenticated approval control?
11. What should happen if you discover that a populated custom field has the wrong type?
12. Which information should remain blank for Rowan’s prospective request?
## 9. Solutions and explanations

Lesson checks
| Check | Explained answer |
| --- | --- |
| L1 | The Order Business ID remains stable. A new Packet Version preserves the corrected revision. |
| L2 | A task represents work, not the customer or opportunity. It should be associated with those records rather than replacing them. |
| L3 | MER-ORD-001 belongs in a text identifier field. The supplied UTC event belongs in Date/Time. Created Time describes the actual CRM-entry event, which may occur later. |
| L4 | The selected Deal can exist while belonging to another customer. A correct relationship must also satisfy the customer/opportunity consistency check. |
| L5 | Revisions need independent identity and review history. Supporting references are small parent-dependent rows without a separate lifecycle in this exercise. |
| L6 | Validation is layout-specific, and access to the layout is assigned to profiles. A second layout can change both data-entry behavior and who encounters it. |
| L7 | Returned history must preserve the actual missing information. Submitted or Accepted versions must meet the completeness condition before the manual save succeeds. |
| L8 | “Customer email” does not state its purpose, confirmation evidence, revision scope, authority or distinction from the current master. |

Guided practice — Completed architecture artifact
| Business object | Grain | Home |
| --- | --- | --- |
| Customer | One commercial organisation | Accounts |
| Person | One person | Contacts |
| Opportunity | One commercial opportunity | Deals |
| Enquiry | One distinct request | Enquiries |
| Order packet | One confirmed order | Order Packets |
| Packet version | One revision | Packet Versions |
| Supporting reference | One reference row within a version | Subform |

The field dictionary and validation specification in Section 4 are the completed reference artifacts.
Completed expected tests
| Test | Expected result | Explanation and recovery |
| --- | --- | --- |
| T01 | Valid record saves | All accepted-version requirements are supplied |
| T02 | Returned historical record saves | Missing email is preserved; required return and reviewer evidence are present |
| T03 | Initial save blocked by V01 | Enter redwood.billing@example.com (mailto:redwood.billing@example.com) using BILL-002, then save |
| T04 | Save blocked by V03 | Restore Revision Number to 3 |
| T05 | Duplicate manually created order blocked once uniqueness is effective | Use the existing MER-ORD-001 record |
| T06 | Manual consistency check fails | Change the parent from MER-ORD-001 to MER-ORD-002 for the supplied Redwood scratch case |
| T07 | Save blocked by V04 | Keep Submitted or use the supplied scratch acceptance time; do not alter historical acceptance |
| T08 | Customization unavailable or denied | Isha performs approved changes; Ava remains non-administrator |

T06 may not be blocked by V01–V07. Its expected failure is a business verification failure, not an invented product error.
T08 tests customization authority. It does not claim that the Finance acceptance transition has already been secured.
Completed historical relationships
| Record | Required relationship |
| --- | --- |
| MER-CON-001 | Account MER-CUST-001 |
| MER-CON-002 | Account MER-CUST-002 |
| MER-DEAL-001 | Account MER-CUST-001; Contact MER-CON-001 |
| MER-DEAL-002 | Account MER-CUST-002; Contact MER-CON-002 |
| MER-ENQ-001 | MER-CUST-001; MER-CON-001; MER-DEAL-001 |
| MER-ORD-001 | Customer MER-CUST-001; Deal MER-DEAL-001; Accepted Version MER-PVER-001-01 |
| MER-ORD-002 | Customer MER-CUST-002; Deal MER-DEAL-002; Accepted Version MER-PVER-002-02 |
| MER-PVER-001-01 | Parent MER-ORD-001 |
| MER-PVER-002-01 | Parent MER-ORD-002 |
| MER-PVER-002-02 | Parent MER-ORD-002 |

A completed environment crosswalk adds the actual observed CRM ID for each row. The chapter does not invent those IDs.
Independent challenge — Complete sample answer
New enquiry records
| Enquiry | Customer lookup | Contact lookup | Opportunity lookup | Reason |
| --- | --- | --- | --- | --- |
| MER-ENQ-003 | Existing MER-CUST-001 | Existing MER-CON-001 | Blank | New request from existing customer; no opportunity established |
| MER-ENQ-004 | Existing MER-CUST-001 | New MER-CON-003 | Blank | Different person and distinct request |
| MER-ENQ-005 | Blank | Blank | Blank | Prospective organisation and person are not yet established as Account/Contact/Deal |

Enquiry names can be:
- Northbank meeting-room equipment enquiry.
- Northbank reception equipment enquiry.
- Papertrail planned-office enquiry.
Each retains its supplied timestamp, sender email and summary.
New Contact
| Field | Value |
| --- | --- |
| Contact Business ID | MER-CON-003 |
| First Name | Casey |
| Last Name | Morgan |
| Email | casey.morgan@example.com (mailto:casey.morgan@example.com) |
| Account | MER-CUST-001 |

Casey is not Taylor. They share an Account but have separate person identities.
New Lead
| Field | Value |
| --- | --- |
| Prospect Business ID | MER-LEAD-001 |
| First Name | Rowan |
| Last Name | Clarke |
| Company | Papertrail Workspaces |
| Email | rowan.clarke@example.com (mailto:rowan.clarke@example.com) |
| Qualification position | Not yet qualified |

Use an existing appropriate lead-status value in the live environment and record its meaning. Do not mark the lead converted or create an opportunity without supplied qualification evidence.
An additional Originating Enquiry lookup can link the Lead to MER-ENQ-005, if deliberately added. The alternative is a documented origin reference in the qualification record’s description.
The lookup offers a stronger explicit relationship, but neither should be described as automatically created by the base model.
Qualification task
Associate MER-TASK-002 — Qualify Papertrail request with Rowan’s Lead.
Use Ava as owner, 19 October 2026 as due date and the supplied open status and description.
Do not associate it with a nonexistent Papertrail Account.
Intentionally unfilled information
The following remain blank:
- Papertrail Account association.
- Papertrail Contact association.
- Opportunity relationships for all three new enquiries.
- Quote and order records for these requests.
These blanks mean the corresponding business work has not been established. They do not justify placeholder identities.
Duplicate test
Attempt a second Enquiry with MER-ENQ-003.
Expected result: the configured unique business-ID check blocks the duplicate manual creation once effective.
Recovery: use the existing enquiry, retaining the new request’s distinct identity. Do not replace its ID with a random new value simply to make the save succeed.
Final counts
After adding the challenge to the cleaned base dataset:
| Module | Base count |
| --- | --- |
| Accounts | 2 |
| Contacts | 2 |
| Deals | 2 |
| Enquiries | 1 |
| Order Packets | 2 |
| Packet Versions | 3 |
| Tasks | 1 |
| Leads | 0 |

The challenge adds intake and qualification work. It does not add confirmed orders.
Understanding questions
1. Account: Northbank Studio. Contact: Taylor Ross. Deal: Northbank’s specific printer-and-installation opportunity. They represent organisation, person and commercial work respectively.
2. An enquiry is a distinct intake event; a Lead is a qualification record. Existing customers can make new requests without becoming unqualified prospects again.
3. One preserved revision of a confirmed order’s packet. It can be returned or accepted independently of another revision.
4. Business identity is held in the supplied text-ID fields. Local CRM record IDs are generated by the product and recorded separately after observation.
5. The snapshot explains the historical event. Current billing information may change without changing what a previous version contained.
6. Northbank:  
10:00 − 09:00 = 60 minutes.  
Redwood:  
14:15 − 09:15 = 5 hours = 300 minutes.
7. The denominators differ. There are three versions but two completed orders. One of those orders passed first time: 1 ÷ 2 × 100% = 50%.
8. Existence is not business agreement. A lookup can select a real Deal belonging to the wrong customer.
9. Blank email: requiredness or the supplied conditional validation. Repeated order ID: uniqueness. Unauthorized acceptance: permissions and controlled transitions, configured later.
10. It is entered historical information. It does not authenticate the person who performed a live action or prevent someone else from entering the reference.
11. Preserve the data and create a correctly typed replacement. Update dependent configuration and verify the controlled move. The documented field type is not editable after creation.
12. Account, Contact and Deal associations remain unestablished. No quote or confirmed-order identity is supplied for Rowan.
## 10. Chapter recap and next step

Good CRM architecture makes different business objects distinguishable and connects them without copying every value everywhere.
Meridian’s design now separates:
- Customer organisation.
- Contact person.
- Commercial opportunity.
- Incoming enquiry.
- Confirmed-order handoff.
- Packet revision.
- Supporting reference.
- Work activity.
The returned Redwood revision remains visible beside the corrected accepted revision. That structure makes rework explainable and prevents version counts from becoming order counts.
The field dictionary explains meaning and authority. Required fields, uniqueness and validation support data quality, while manual consistency checks address the relationships not yet enforced automatically.
“I can…” completion checklist
- I can state what one record represents.
- I can distinguish Leads, Accounts, Contacts, Deals and activities.
- I can justify a custom module or subform.
- I can choose appropriate field types.
- I can create and verify lookup relationships.
- I can organise fields into a useful layout.
- I can configure required, unique and criteria-validated fields.
- I can preserve missing-data and correction history.
- I can reproduce record counts and measures using the correct grain.
- I can distinguish structural data from authenticated business decisions.
Your model and dictionary become part of the project’s application map, data dictionary and access matrix.
The next chapter, Roles, Profiles and Record Access, establishes who may view, create, change and share these records. It will build on the distinction between Sales preparation, Finance acceptance and administrator configuration.
## 11. Glossary and further reading

Glossary
| Term | Meaning |
| --- | --- |
| Account | A commercial organisation record |
| Activity | A task, meeting or call representing work or an interaction |
| Business identifier | A stable reference used by the business case |
| Contact | A person record |
| Custom module | A user-defined category of CRM records |
| Data architecture | The design of records, fields and relationships |
| Data dictionary | Documented meaning, structure and use of fields |
| Deal | A commercial opportunity |
| Grain | What one record or row represents |
| Layout | The fields and sections presented for a record |
| Lead | A prospective relationship requiring qualification |
| Lookup | Association with another existing record |
| One-to-many | A relationship in which one parent can have several children |
| Packet version | A preserved revision of a confirmed order’s handoff information |
| Required field | A field whose value must be present under the applicable condition |
| Snapshot | Information preserved as it stood in a particular revision or event |
| Subform | Repeated rows held within a parent record |
| System timestamp | A timestamp generated for a product event such as record creation |
| Unique field | A field configured to detect repeated values within its supported scope |
| Validation rule | A condition used to check whether entered information is acceptable |

Further reading
The official sources below were accessed for the configuration procedures and product distinctions taught in this chapter. They do not establish that the chapter’s proposed Meridian configuration has been executed.
Feature availability depends on the training edition and permissions. Some subform and layout-related capabilities are released in phases. The core practice uses documented basic field, relationship, subform and criteria-validation behavior rather than assuming every optional feature is present.
^modules: Zoho CRM, Standard Modules & Fields (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/standard-modules-fields).
^custommodules: Zoho CRM, Customizing Organization Modules (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-modules/articles/customize-modules), including custom-module creation, layout design, profile access and deletion behavior.
^fields: Zoho CRM, Working with Custom Fields (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/use-custom-fields), including requiredness, uniqueness, field-type permanence and Unused Fields.
^fieldtypes: Zoho CRM, Types of Custom Fields (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/types-of-fields), particularly lookup creation and field-type choices.
^layouts: Zoho CRM, Working with Page Layouts (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-page-layouts/articles/create-page-layouts).
^subforms: Zoho CRM, Building a Subform (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/managing-subforms/articles/build-subforms), particularly standard subforms, requiredness, reference rows and edition availability.
^validation: Zoho CRM, Working with Validation Rules (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/validation-rules/articles/create-validation-rules), including criteria direction, layout scope and supported entry/update behavior.
^records: Zoho CRM, Creating Accounts (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/accounts/articles/create-accounts), Creating Contacts (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/contacts/articles/create-contacts), Creating Deals (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/create-deals), Creating Leads (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/leads/articles/create-leads), and Working with Tasks (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/activities/articles/working-with-tasks-and-meetings).
^metadata: Zoho CRM Developer Documentation, Fields Metadata, V8 (https://www.zoho.com/crm/developer/docs/api/v8/field-meta.html). Used here to distinguish technical field names from labels. No API execution is required.
