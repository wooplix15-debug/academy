# Lead Capture and Customer Engagement

## 1. What you will learn

A capture form connects an incoming request to the people who will handle it. Its usefulness depends on what happens after submission: identifying the requester, preserving the request, assigning responsibility and communicating an appropriate next step.
In this chapter, you will build Meridian’s controlled enquiry intake and prospect-capture forms. You will distinguish existing customers from new prospects, handle a repeated submission, recover missing information and prepare customer messages using CRM templates.
By the end, you should be able to:
- Explain the difference between an enquiry, a Lead and an established customer.
- Design a form around information needed for the next decision.
- Configure and publish a native CRM webform.
- Understand required fields, hidden fields, ownership and awaiting-record queues.
- Link enquiries to reviewed customer or prospect records.
- Create module-specific email templates using supported merge fields.
- Configure a webform acknowledgement and its fallback.
- Distinguish sending a message from receiving and associating a reply.
- Record customer communication preferences without confusing them with every email-control feature.
- Test normal, duplicate, incomplete, denied-action and recovery cases.
- Measure capture and response outcomes using explicit denominators.
Your chapter output: four new canonical enquiries, one prospect Lead, four follow-up tasks, two configured capture forms and an engagement evidence package.
The Meridian examples are synthetic. Product configuration instructions are supported by official documentation; actual publication, delivery and capture results require your laboratory evidence.
## 2. Lessons

2.1 An incoming request is not automatically a new Lead
An enquiry represents a distinct request.
A Lead represents prospective qualification work.
An Account represents an established business relationship, while a Contact represents a person associated with that relationship.
These grains lead to different decisions.
Incoming situation
Taylor requests new pricing for Northbank
Taylor asks a separate question about toner
Devon requests pricing for Marlow, which has no established customer record
The same request is submitted again without a changed instruction
An incomplete form is corrected before any record was admitted
A requester supplies a company name resembling an existing Account
Creating one Lead for every form submission would mix:
- Existing-customer requests.
- New prospects.
- Repeated requests.
- Incomplete submissions.
It would also make Lead counts a poor measure of new business interest.
One person can make several valid requests
Taylor’s email address does not identify the request itself.
Taylor can submit:
- A replacement-printer request.
- A toner-pricing request.
Those are two enquiries from one person.
For Meridian’s Enquiries module, the request identifier is Enquiry Business ID. The reply email is an attribute and a communication route; it is not a unique enquiry key.
A webform targets one module
A native CRM webform is configured for a selected module.
An Enquiries form does not automatically create a Lead, Account, Contact and Deal as one connected transaction.
The chapter uses two explicit stages:
1. Capture the request in Enquiries.
2. For a reviewed new prospect, capture a Lead and associate it with the enquiry.
This preserves the distinction established in Chapter 4.
2.2 Design the form for the next useful decision
Start with the decision the receiving team must make.
For Meridian:
Can Sales identify the request, understand its subject and decide who should handle the next step?
That requires:
- A request reference.
- A short title.
- The requester’s name.
- An organisation name as supplied.
- A usable reply address.
- A request summary.
- A communication preference.
It does not yet require a confirmed order, accepted packet version or invoice.
Customer-supplied text and reviewed relationships
“Northbank Studio” entered in a form is supplied text.
A Customer lookup pointing to MER-CUST-001 is a reviewed relationship to a CRM record.
Keep those concepts separate:
| Field | Meaning |
| --- | --- |
| Organisation As Supplied | What the requester entered |
| Customer lookup | The Account selected after review |
| Requester names | Names supplied with this request |
| Sales Contact lookup | The reviewed existing Contact |
| Related Prospect lookup | Qualification record associated after triage |

Zoho’s webform FAQ states that lookup fields are not offered in the form’s field-selection list. Populate those relationships through staff review.
A supplied business reference is also not an authentication credential. Knowing an Account or enquiry ID does not grant access to its CRM records.
The chapter’s reference-allocation choice
Chapter 4 made Meridian’s business identifiers controlled fields.
For this chapter’s small, staff-issued pilot:
- Staff issue the request references in the exercise register.
- The form includes Issued request reference.
- The participant enters the issued value.
- A repeat of the same unchanged request retains that reference.
- A genuinely different request receives a different reference.
This is a controlled invitation design. It does not demonstrate automatic reference allocation for unrestricted public intake.
A hidden constant such as MER-ENQ-010 would not solve general reference allocation: every submission would carry the same value.
Keep required fields purposeful
Mark the fields needed for intake as required in the webform.
Do not make every newly added field globally required in the CRM layout. The existing historical enquiry predates these additions and may legitimately lack them.
Distinguish:
- Module-required fields: required by the record model.
- Form-required fields: required for this capture path.
- Staff-completed fields: populated during review.
Use hidden fields for source hints
A hidden Capture Source value can identify the configured form.
For example:
- C07-Enquiry-Link
- C07-Prospect-Link
It is useful for routing and reporting, but it is not a security boundary. Hidden values originate in a client-facing form and should not confer privileges or establish Finance acceptance.
2.3 Prepare the CRM fields and permissions
Use the existing Enquiries, Leads, Accounts, Contacts and Tasks modules.
In the tables below, Request Summary means the existing enquiry-summary field from Chapter 4. Use its actual configured label.
Additions to Enquiries
| Field | Type | Purpose |
| --- | --- | --- |
| Requester First Name | Text | Request-level supplied name |
| Requester Last Name | Text | Request-level supplied name |
| Organisation As Supplied | Text | Supplied organisation label |
| Reply Email | Email | Address used for the reply route |
| Supplied Email Snapshot | Text | Preserve the fictional source address in the laboratory |
| Capture Source | Picklist | C07-Enquiry-Link; Manual logged |
| Identity Review | Picklist | Unchecked; Existing customer; New prospect; Needs clarification |
| Intake Status | Picklist | New; Ready for Sales; Needs clarification |
| Engagement Preference | Picklist | Request reply only; Updates requested |
| Related Prospect | Lookup to Leads | Associate a prospect after review |
| First Personal Response At | Date/Time | First verified staff response for this request |

Continue using the existing:
- Enquiry Name.
- Enquiry Business ID.
- Received At.
- Customer lookup.
- Sales Contact lookup.
- Related Opportunity lookup.
- Request Summary.
Additions to Leads
| Field | Type | Purpose |
| --- | --- | --- |
| Enquiry Reference | Text | Originating enquiry business reference |
| Supplied Email Snapshot | Text | Fictional source email retained separately from live laboratory routing |
| Capture Source | Picklist | C07-Prospect-Link |
| Engagement Preference | Picklist | Request reply only; Updates requested |

Continue using Prospect Business ID and the standard First Name, Last Name, Company, Email and Description fields.
Enquiry Reference is not unique. A prospect may eventually have several enquiries; this field identifies the origin of this particular qualification record.
Field-creation procedure
Using Isha’s administrator account:
1. Open Setup → Customization → Modules and Fields.
2. Select the module and its Standard layout.
3. Drag the required field type from the New Fields tray.
4. Set the field label and properties.
5. Add the specified picklist values.
6. For Related Prospect, choose Leads as the lookup module.
7. Save the layout.
8. Check the field permissions for the course profiles.
9. Reopen a record to verify the fields.
Create the fields in the specified module. The optional Lead-field copying facility should not create unplanned fields in other modules.
Verify the existing business-ID uniqueness settings. For custom text fields, the official procedure uses Edit Properties → Do not allow duplicate values, followed by saving the layout.
Do not mark Reply Email unique. Taylor’s two enquiries need the same reply route.
Permission changes for this chapter
Chapter 5 gave ordinary profiles no email-sending authority.
Apply these deliberate additions:
| Profile | Chapter addition |
| --- | --- |
| Meridian Sales | Leads View/Create/Edit; Send Email for Enquiries and Leads |
| Meridian Operations Read | Leads View |
| Meridian Sales, when performing mailbox integration | Email & Chat Settings for its controlled laboratory mailbox |

Use Setup → Security Control → Profiles to inspect and adjust the relevant permissions.
Keep Leads private. Ava owns the new Lead; Noor’s superior role and View permission support the Operations view.
Isha continues to manage fields, templates, webforms and awaiting-record approval. Sales uses shared templates rather than receiving template-administration authority.
Mass Email, Import, Export, deletion and developer privileges are not needed for these ordinary-user exercises.
Record access, permission to send, template-folder visibility and access to integrated email content are separate controls.
2.4 Build and publish the Enquiries webform
The current official guide supports webforms for custom organisation modules.
The user configuring the form needs Manage Webform permission. Publication formats and other features depend on the account’s entitlement.
Configure the form
Using Isha:
 1. Open Setup → Channels → Webforms.
 2. Select Enquiries.
 3. Choose New Form.
 4. Name it Meridian Enquiry Intake — Training.
 5. Select the Standard layout where offered.
 6. Drag the required fields into the builder.
 7. Set the field labels and help text.
 8. Use each field’s Settings control to mark form-required fields.
 9. Add Capture Source as a hidden field with value C07-Enquiry-Link.
10. Preview the form.
11. Continue to form details.
12. Choose Ava’s actual active CRM user as owner.
13. Select Request for Approval.
14. Leave visitor acknowledgement off for this first intake form.
15. Choose the built-in thank-you page where offered.
16. Save and open the publication options.
Use this field order:
1. Issued request reference — Enquiry Business ID.
2. Request title — Enquiry Name.
3. Requester First Name.
4. Requester Last Name.
5. Organisation As Supplied.
6. Reply Email.
7. Request Summary.
8. Engagement Preference.
9. Training intake time — Received At.
The last field supports this supervised exercise’s business-event timeline. It is not a demonstration of trusted automatic server-side receipt-time assignment.
For a live run, enter and retain the actual laboratory intake time. For the supplied reconstruction exercise, use the fictional scenario time. Keep actual execution timestamps separate.
Leave staff assessment and relationship fields off the visitor form.
Publish without writing code
The current setup guide documents a Link publication option for eligible paid accounts.
Where available:
1. Select Link.
2. Copy the generated URL.
3. Record it in the configuration worksheet.
4. Open it in a separate browser session.
5. Confirm that the form loads and shows the expected fields.
6. Submit the supplied cases.
The guide states that Form Location URL restrictions do not apply to Link publication.
If using an embedded form instead:
- Use the actual hosted page.
- Configure the correct Form Location URL.
- Use the generated publication output.
- Preserve Zoho’s required hidden elements.
- Test the published page.
A locally opened HTML file is not the documented supported hosting route. Previewing the builder is also not an end-to-end submission test.
A thank-you page proves only part of the journey
It does not establish that:
- The request is an active record.
- It passed review.
- It is a new unique enquiry.
- Its customer links are correct.
- A message was delivered.
- Finance accepted an order.
Check the destination and awaiting-record state.
2.5 Review captured records and resolve identity
The documented awaiting-record mechanism holds records before ordinary module access.
To inspect and approve:
1. Open the module.
2. Open the Actions menu.
3. Choose Approve Module or the equivalent awaiting-record action shown.
4. Inspect the submitted values.
5. Select the appropriate records.
6. Choose Approve.
7. Verify the admitted records in the module.
Use Isha’s approval authority for this exercise.
This is capture admission. It is distinct from:
- Prospect qualification.
- Deal progression.
- A formal business approval process.
- Finance acceptance of an order packet.
Review identity and request grain
For each submitted request:
1. Check the issued enquiry reference.
2. Compare the payload with the exercise register.
3. Check whether the reference already represents the same request.
4. Review the supplied person and organisation.
5. Select existing customer/contact lookups only when the supplied evidence supports them.
6. Identify a new prospect without prematurely creating an Account.
7. Record the next action.
For an exact duplicate, preserve one canonical enquiry and link the repeated attempt in the capture ledger.
The native system may reject, flag or hold a duplicate depending on the channel and configuration. Record the actual behavior. Do not assume that an import duplicate policy is also the webform policy.
If an extra duplicate is awaiting review, do not admit it as another business request. Use the available duplicate-resolution/rejection action and retain its disposition. A pending exception is not a completed resolution.
A missing field and a duplicate need different recovery
- Missing required summary: supply the missing request information.
- Exact repeat: retain the existing canonical request.
- Changed instruction under an old reference: inspect the change; do not automatically discard it or overwrite reviewed history.
2.6 Capture the new prospect separately
After reviewing Marlow’s enquiry, build a second form:
Meridian Prospect Capture — Training
Target: Leads.
Include:
| Field | Treatment |
| --- | --- |
| Prospect Business ID | Required; issued reference |
| First Name | Required for this form |
| Last Name | Required |
| Company | Required for this form |
| Email | Required; controlled laboratory recipient for live tests |
| Enquiry Reference | Required for this form |
| Description | Request details |
| Engagement Preference | Required |
| Capture Source | Hidden C07-Prospect-Link |

Choose Ava as owner.
For this reviewed, staff-assisted capture step, leave Request for Approval off. The Lead is still unqualified business work; admission to Leads does not make Marlow an established customer.
Use the existing configured open Lead Status and record its actual label.
After capture:
1. Verify Prospect Business ID.
2. Verify the originating Enquiry Reference.
3. Populate the Lead’s Supplied Email Snapshot from the source register.
4. Open the originating Enquiry.
5. Select the new Lead in Related Prospect.
6. Verify the link.
The two records represent different things:
- Enquiry: Devon’s request.
- Lead: Devon/Marlow’s qualification work.
2.7 Create customer messages with email templates
An email template is reusable message content. A merge field inserts values from the selected module or supported related fields.
Templates are module-specific. An Enquiries template should use Enquiries fields; a Leads template should use Leads fields.
Create a template
Using Isha:
 1. Open Setup → Customization → Templates → Email.
 2. Select New Template.
 3. Choose the target module.
 4. Select a Blank template.
 5. Add a Text component.
 6. Enter the name and subject.
 7. Insert merge fields using the builder’s picker.
 8. Save to Meridian Intake.
 9. Share that folder with the intended users, including Ava.
10. Preview desktop and mobile output.
11. Test the template using the available test-email facility.
The builder documentation describes typing # to open the merge-field list. Select the actual field rather than guessing a technical token.
Its test-email guidance restricts test delivery to the current user’s inbox. This checks rendering and that test route; it does not prove delivery to the intended requester or correct record association.
Template content must match the event
An acknowledgement may say:
We have received your request.
It should not say:
Your order has been approved.
A pricing enquiry has not established:
- An agreed price.
- A confirmed order.
- An installation booking.
- Finance acceptance.
Design the next question
A useful follow-up asks for information that advances the decision.
For Devon, installation is undecided. Ask whether installation should be included.
For Taylor’s replacement-printer request, confirm the installation location.
For a repeat submission, avoid creating another parallel conversation unless the earlier response needs to be recovered.
Communication preference is a separate decision
The synthetic preference values are:
- Request reply only.
- Updates requested.
“Request reply only” means the request can be handled without treating the person as a promotional subscriber.
Do not use this preference as a blanket substitute for native suppression, unsubscribe or confirmation features. Nor should a captured preference automatically produce an unrelated marketing send.
2.8 Configure acknowledgements and understand email channels
Webform auto-response rule
For the Leads form:
 1. Open Setup → Channels → Webforms.
 2. Select Auto-Response Rules.
 3. Choose Create Rule.
 4. Name it Meridian Prospect Receipt.
 5. Select Leads.
 6. Add a criterion:
- Capture Source equals C07-Prospect-Link.
- Engagement Preference equals Request reply only.
 7. Select the request-only acknowledgement template.
 8. Choose the available laboratory From address.
 9. Set the actual controlled Sales Reply To address.
10. Save and activate the rule.
11. Open the Leads webform’s details.
12. Enable Acknowledge Visitor.
13. Select the rule.
14. Select the generic default acknowledgement for unmatched submissions.
15. Save and retain the current publication output.
The official guide explains that the selected default template is used when no rule criterion matches.
Do not leave the fallback ambiguous.
A webform auto-response rule is an immediate capture response. It is not a scheduled nurturing sequence.
Double opt-in
Double opt-in adds email confirmation before the record is pushed into CRM.
The documented feature requires the primary Email field in the form. Configuration includes:
- Enabling Double Opt-in in form details.
- Customizing the confirmation email/page where needed.
- Choosing the supported action after confirmation.
- Saving and publishing the updated form.
An unconfirmed submission is not an admitted active Lead.
The main exercise leaves double opt-in off so you can distinguish its capture path from the awaiting-record path. An optional test appears later.
Email confirmation is not proof that the prospect is commercially qualified.
Native sending and reply synchronization
Zoho documents two main sending arrangements:
| Arrangement | What it supports |
| --- | --- |
| Native CRM email without an integrated inbox | Sending from CRM; does not provide the same inbound reply synchronization |
| Integrated mailbox | Two-way email association according to configuration and matching |

To send from a record:
1. Open the record.
2. Select Send Email, or Compose Email in the Emails related list.
3. Check the actual From and To addresses.
4. Select the correct module template.
5. Inspect the merged content.
6. Complete the specific next question.
7. Send.
8. Inspect the Emails related list.
9. Retain the observed status and evidence.
For this chapter, new Enquiries use Reply Email for the controlled route. Existing Contact email values remain their fictional source values.
Connect a laboratory inbox when testing replies
Where enabled for Ava:
1. Open Setup → Channels → Email → Email Configuration.
2. Choose the actual supported email service.
3. Select the offered IMAP route.
4. Complete the provider’s authorization.
5. Select the synchronization period.
6. Set email sharing according to the laboratory’s intended access.
7. Finish the configuration.
8. Send and receive a controlled reply.
Use the provider’s current authorization flow. Do not copy credentials or app passwords into your course artifacts.
The documentation describes OAuth for supported popular services and provider-specific configuration for others. Record the route actually offered rather than inventing server settings.
For custom Reply Email addresses, the communication guide explains that received-email synchronization depends on Custom Email Preference and its current configuration prerequisites. Check that setting with Isha before claiming that Enquiries replies are synchronized.
Email association does not establish request association
Taylor’s two enquiries use the same reply address.
An email associated through an address is not automatically proof that it belongs to both requests. Use:
- Enquiry reference in the subject/body.
- Conversation context.
- The actual question answered.
- The engagement ledger.
Record First Personal Response At only for the request the staff response actually addresses.
2.9 Measure capture and engagement carefully
Use separate measures for separate stages.
Capture
\[
\text{Form submission conversion}
=
\frac{\text{Submitted visits}}{\text{Form visits}}
\times 100
\]
This measures form behavior, not sales conversion.
\[
\text{Canonical enquiry yield}
=
\frac{\text{Unique admitted enquiries}}{\text{Server submissions}}
\times 100
\]
A yield below 100% can be appropriate when duplicates are resolved.
Response
\[
\text{Personal-response coverage}
=
\frac{\text{Unique enquiries with a verified personal response}}{\text{Unique enquiries in the cohort}}
\times 100
\]
\[
\text{Mean completed personal-response time}
=
\frac{\text{Total elapsed minutes for personally answered enquiries}}{\text{Number personally answered}}
\]
Report unanswered request ages separately.
An automatic acknowledgement is not a personal response. A preview is not a sent message.
Product analytics
The official guide documents:
Setup → Channels → Webforms → More Stats, and individual View Analytics actions.
Available detail depends on edition, tracking, publication mode, time filters and cookie/measurement coverage.
Record those conditions. Do not invent native visit or submission counters from your manual ledger.
Also distinguish:
- Form submission.
- Active Lead creation.
- Business qualification.
- Lead conversion.
- Deal creation.
- Finance acceptance.
A product panel’s “qualified” or created-record label does not replace Meridian’s commercial qualification decision.
## 3. Visual explanation

flowchart TD
    A[Incoming request] --> B[Enquiries webform]
    B --> C{Required fields complete?}
    C -->|No| D[Correct information and retry]
    D --> B
    C -->|Yes| E[Awaiting-record review]
    E --> F{Same unchanged request?}
    F -->|Yes| G[Link repeat to canonical enquiry]
    F -->|No| H[Admit one distinct enquiry]
    H --> I{Reviewed relationship}
    I -->|Existing customer| J[Select existing Account and Contact]
    I -->|New prospect| K[Capture one qualification Lead]
    K --> L[Link Lead to enquiry]
    J --> M[Assign next action]
    L --> M
    M --> N[Personal response and follow-up task]
    N --> O[Check delivery, replies and request context]
The form captures supplied facts. Review establishes request grain and relationships.
The existing-customer branch reuses customer records. The new-prospect branch creates qualification work.
A repeated submission returns to the canonical enquiry rather than becoming another Lead, Deal or order.
flowchart LR
    A[Template preview] --> B[Test email]
    B --> C[Actual requester send]
    C --> D[Observed delivery status]
    D --> E[Reply received]
    E --> F[Reply associated with the correct request]
These are separate checkpoints. Success at an earlier checkpoint does not establish the later ones.
## 4. Worked case

Taylor has an existing relationship
Northbank already has:
- Account MER-CUST-001.
- Contact MER-CON-001, Taylor Ross.
- Historical enquiry MER-ENQ-001.
- Historical order MER-ORD-001.
Taylor now asks for replacement-printer pricing.
That creates a new enquiry, MER-ENQ-010, because it is a distinct request. It does not replace the earlier enquiry or confirmed order.
Review result
| Item | Decision |
| --- | --- |
| Organisation supplied | Northbank Studio |
| Reviewed Account | MER-CUST-001 |
| Reviewed Contact | MER-CON-001 |
| New enquiry | MER-ENQ-010 |
| New Lead | Not needed |
| Related Opportunity | Not selected yet |
| Next action | Confirm installation location before progressing the sales discussion |

Taylor submits the same request again
The repeated payload contains:
- Same issued enquiry reference.
- Same person and organisation.
- Same request summary.
- Same communication preference.
- No changed customer instruction.
Treat it as a repeat of MER-ENQ-010.
Record the attempt and observed product disposition. Keep one canonical enquiry.
Taylor submits another request
The toner-pricing request has:
- Different enquiry reference MER-ENQ-012.
- Different request summary.
- The same Contact and Account.
It is a valid second enquiry.
This is why Reply Email must not be the Enquiries module’s unique request key.
Devon is a new prospect
Devon Ellis asks for indicative pricing for Marlow Workspace.
The reviewed exercise register contains no established Marlow Account.
Create:
- Enquiry MER-ENQ-011.
- Prospect Lead MER-LEAD-002.
Link the Lead through Related Prospect. Leave Customer and Sales Contact unset until the appropriate commercial process establishes those records.
Marlow’s installation choice remains undecided, so the next communication asks for that information.
Interpret the first response correctly
In the supplied timeline:
- Marlow enquiry received: 09:10.
- Prospect-form acknowledgement: 09:25.
- Ava’s personal response: 09:50.
Personal-response elapsed time:
\[
09{:}50 - 09{:}10 = 40\text{ minutes}
\]
The 09:25 acknowledgement belongs to the second capture step. It does not demonstrate that Ava personally handled the request at that time.
## 5. Try it yourself — guided practice

5.1 Confirm the starting base
Use the cleaned Chapter 6 base:
Structure
Accounts
Contacts
Deals
Enquiries
Leads
Tasks
Order Packets
Packet Versions
Supporting References rows
Identify optional earlier challenge records separately.
Keep the historical six-order set available for comparison. The new capture cohort is specifically enquiries 010–013.
5.2 Prepare the laboratory recipient map
The book’s example.com addresses preserve fictional business identities. For live delivery, map each recipient key to an actual controlled mailbox.
| Recipient key | Fictional identity |
| --- | --- |
| LAB-TAYLOR | Taylor Ross |
| LAB-DEVON | Devon Ellis |
| LAB-ALEX | Alex Rivera |

Use:
- Reply Email: actual controlled address in a live run.
- Supplied Email Snapshot: fictional source address.
- Lead Email: actual controlled Devon address for the acknowledgement test.
The same LAB-TAYLOR address supports both Northbank enquiries. Keep their request contexts distinct.
Record the actual Sales sender and Reply To address as well.
5.3 Use the reviewed identity register
AUTH-CAP-07 supplies these synthetic review facts:
| Requester | Reviewed relationship |
| --- | --- |
| Taylor Ross | Northbank MER-CUST-001; Taylor MER-CON-001 |
| Alex Rivera | Redwood MER-CUST-002; Alex MER-CON-002 |
| Devon Ellis | Marlow Workspace; no established Account/Contact in the base |

The register authorizes the exercise’s record associations. A name entered in an uncontrolled public form would need its own review evidence.
5.4 Run these six intake attempts
All supplied scenario times are UTC on 6 October 2026.
For the reconstruction/paper branch, use these business times. For a live performance run, record the actual times and calculate actual results separately.
AttemptID,AttemptAtUTC,TrainingReceivedAtUTC,EnquiryBusinessID,EnquiryName,FirstName,LastName,OrganisationAsSupplied,SuppliedEmailSnapshot,RecipientKey,RequestSummary,EngagementPreference
S01,2026-10-06T09:00:00Z,2026-10-06T09:00:00Z,MER-ENQ-010,Replacement printer,Taylor,Ross,Northbank Studio,taylor.ross@example.com,LAB-TAYLOR,Request pricing for one replacement printer with installation,Request reply only
S02,2026-10-06T09:10:00Z,2026-10-06T09:10:00Z,MER-ENQ-011,Three printers,Devon,Ellis,Marlow Workspace,devon.ellis@example.com,LAB-DEVON,Request indicative pricing for three printers; installation choice not yet decided,Request reply only
S03,2026-10-06T09:12:00Z,2026-10-06T09:00:00Z,MER-ENQ-010,Replacement printer,Taylor,Ross,Northbank Studio,taylor.ross@example.com,LAB-TAYLOR,Request pricing for one replacement printer with installation,Request reply only
S04,2026-10-06T09:20:00Z,2026-10-06T09:20:00Z,MER-ENQ-012,Toner pricing,Taylor,Ross,Northbank Studio,taylor.ross@example.com,LAB-TAYLOR,Request pricing for five toner cartridges,Request reply only
S05,2026-10-06T09:30:00Z,2026-10-06T09:30:00Z,MER-ENQ-013,Additional printer,Alex,Rivera,Redwood Office Co,alex.rivera@example.com,LAB-ALEX,,Request reply only
S06,2026-10-06T09:40:00Z,2026-10-06T09:40:00Z,MER-ENQ-013,Additional printer,Alex,Rivera,Redwood Office Co,alex.rivera@example.com,LAB-ALEX,Request pricing for one additional office printer; installation not required,Request reply only
S03 repeats S01’s unchanged request payload. Its attempt occurs later, but the canonical business receipt remains S01’s time.
S05 deliberately omits the required summary. S06 supplies the missing information.
Capture tasks
 1. Configure the fields and permissions.
 2. Build and publish the Enquiries form.
 3. Run the six attempts before completing staff triage.
 4. Observe the missing-summary behavior.
 5. Inspect awaiting records and duplicate outcomes.
 6. Admit one canonical record per distinct valid request.
 7. Populate Supplied Email Snapshot.
 8. Complete reviewed customer/contact relationships.
 9. Record the duplicate disposition.
10. Record any unresolved queue exception.
Use this ledger:
AttemptID,EnquiryBusinessID,ObservedSubmissionResult,QueueResult,CanonicalRecordID,Disposition,EvidenceReference,ActualExecutionTime
5.5 Capture Marlow’s prospect Lead
Use the Leads form with:
| Field | Input |
| --- | --- |
| Prospect Business ID | MER-LEAD-002 |
| First Name | Devon |
| Last Name | Ellis |
| Company | Marlow Workspace |
| Email | Controlled LAB-DEVON address for live testing |
| Enquiry Reference | MER-ENQ-011 |
| Description | Request indicative pricing for three printers; installation choice not yet decided |
| Engagement Preference | Request reply only |
| Capture Source | Hidden C07-Prospect-Link |
| Owner | Ava’s actual active CRM user |

After capture:
- Verify the Lead.
- Set Supplied Email Snapshot to devon.ellis@example.com.
- Link it from enquiry 011.
- Record the actual open Lead Status.
- Confirm that no Account, Contact or Deal was created by this step.
5.6 Create these templates
Create three complete templates.
A. Enquiries personal follow-up
Name: MER-ET-007-01 — Request follow-up
Subject: Meridian request — followed by the Enquiry Business ID merge field.
Include:
- Requester First Name.
- Enquiry Business ID.
- Request Summary.
- A sentence introducing the next question.
- A receipt-versus-order statement.
- Meridian Supply signature.
B. Leads request-only acknowledgement
Name: MER-ET-007-02 — Prospect receipt
Subject: Meridian received your prospect details
Include:
- First Name.
- Company.
- Enquiry Reference.
- Receipt acknowledgement.
- Statement that the message concerns the submitted request.
- No claim of an agreed order or installation booking.
C. Leads fallback acknowledgement
Name: MER-ET-007-03 — Generic prospect receipt
Subject: Meridian received your details
Include:
- First Name.
- Enquiry Reference.
- A generic acknowledgement.
- A statement that the next step will be reviewed.
Share the template folder with Ava. Preview every template and record the test-rendering result.
Configure the Leads auto-response rule and fallback from Lesson 2.8.
5.7 Prepare these personal responses
Use the Enquiries template and tailor the next question.
| Enquiry | Specific next question |
| --- | --- |
| 010 | Please confirm the postcode of the installation location. |
| 011 | Should installation be included in the indicative pricing? |
| 012 | Please confirm the printer model so we can identify the toner cartridges. |
| 013 | Please confirm the delivery postcode for the additional printer. |

For the supplied measurement exercise, use:
Event
Lead 002 automatic acknowledgement
Enquiry 010 first personal response
Enquiry 011 first personal response
Enquiry 012 first personal response
Enquiry 013 first personal response
These are fictional measurement inputs, not proof of sends.
In a live run, retain actual delivery/related-list evidence and enter actual verified personal-response times. If you only previewed a message, record Previewed rather than Sent.
5.8 Create four follow-up tasks
Use these task references and inputs:
| Reference | Subject | Contact/Lead |
| --- | --- | --- |
| MER-TASK-003 | Review installation scope — MER-ENQ-010 | Taylor, MER-CON-001 |
| MER-TASK-004 | Clarify prospect requirements — MER-ENQ-011 | Devon, MER-LEAD-002 |
| MER-TASK-005 | Review toner compatibility — MER-ENQ-012 | Taylor, MER-CON-001 |
| MER-TASK-006 | Review delivery requirements — MER-ENQ-013 | Alex, MER-CON-002 |

Owner: Ava.
Use an existing open task status and record its exact label. No recurrence is required.
Procedure:
1. Open Tasks.
2. Select Create Task.
3. Enter the subject, owner, due date and supported associations.
4. Add the enquiry reference and requested next action to Description.
5. Save.
6. Verify the task and retain its actual CRM record ID.
Task references belong in the course crosswalk. Do not confuse them with system-generated task IDs. If there is no dedicated Task Business ID field, include the reference in the task’s subject or description.
These tasks represent continuing review work. A sent acknowledgement does not complete that work.
5.9 Test access, reply handling and counts
Test:
- Ava can view the admitted enquiries and Lead.
- Ava can use the shared Enquiries and Leads templates.
- Ava cannot administer webforms.
- Mia can view her permitted Northbank Contact context but cannot send email from it.
- Leo gains no Enquiries or Leads visibility through this chapter.
- Noor can view the new records through the intended read-only design.
- Integrated-email visibility matches the actual email-sharing configuration.
For a live reply test, send the following from the controlled Devon mailbox to the actual Sales Reply To address:
Subject: Re: Meridian request — MER-ENQ-011  
Please include installation in the indicative pricing. The installation postcode for this laboratory request is AB1 2CD.
The postcode is synthetic.
Verify:
1. The reply reaches the Sales mailbox.
2. The applicable CRM synchronization route captures it.
3. The record association is observed.
4. Its enquiry context is 011.
5. The clarification is recorded without claiming a confirmed order.
5.10 Complete the evidence package
Use:
- C01_CH07_Meridian_Capture_Design.md
- C01_CH07_Meridian_Field_and_Access_Changes.md
- C01_CH07_Meridian_Form_Configuration.md
- C01_CH07_Meridian_Capture_Ledger.csv
- C01_CH07_Meridian_Identity_and_Record_Links.csv
- C01_CH07_Meridian_Templates.md
- C01_CH07_Meridian_Engagement_Evidence.md
- C01_CH07_Meridian_Capture_and_Response_Measures.md
Record actual URLs, IDs and execution results only after observation.
## 6. Independent challenge

Challenge A — Read the capture measures
A supplied, closed observation sample for the Enquiries form contains:
Measure
Form visits
Visits with a started form
Visits completing a server submission
Unique admitted enquiries
New prospect Leads
Leads converted
New Deals
The sample uses the same publication mode, time window and counting units. It is separate from proof of your live native counters.
Calculate:
1. Submission conversion.
2. Abandonment among started visits.
3. Canonical enquiry yield.
4. Share of admitted enquiries requiring a new prospect Lead.
Explain why one Lead does not mean three enquiries were lost.
Challenge B — The old reference contains a changed request
After enquiry 010 is reviewed, another submission uses MER-ENQ-010 but says:
Please remove installation from the replacement-printer pricing request.
Explain:
1. Why this is not an exact duplicate.
2. What must be compared before updating the canonical request.
3. What should be retained as evidence.
4. Why the old receipt and first-response timestamps should not be overwritten automatically.
Challenge C — “Sent” does not mean “ignored”
One message sent through an integrated mailbox shows Sent. It has no Opened or Clicked result.
A colleague concludes:
The prospect ignored the message.
Explain why the available evidence does not support that conclusion. Identify the next checks.
Challenge D — Test the fallback
Optional live extension:
- Prospect Business ID: MER-LEAD-LAB-007
- First Name: Blair
- Last Name: Test
- Company: Meridian Form Laboratory
- Enquiry Reference: LAB-ENQ-007
- Engagement Preference: Updates requested
- Email: a separately controlled laboratory address
Submit through the Leads form.
Determine which acknowledgement should be selected. Inspect the actual result.
After retaining evidence, Isha removes the temporary Lead. This record is not part of the base count.
Challenge E — Double opt-in
Optional live extension:
Use a separate temporary prospect, MER-LEAD-LAB-008, and a controlled address. Enable double opt-in on a separate test form or controlled test configuration.
Observe:
1. State before email confirmation.
2. State after confirmation.
3. Whether awaiting review is also enabled.
4. Actual acknowledgement messages and timing.
Record the configured path. Do not assume that confirmation and manual approval are the same event.
Remove the temporary record and restore the main form’s defined configuration after retaining evidence.
## 7. Common problems and recovery

| Problem | Likely explanation |
| --- | --- |
| Custom field is absent from the builder | It was not created/saved, is not in the selected layout, or is an unsupported form type |
| Customer lookup is not available in the form | Native webforms do not offer lookup fields in the documented field list |
| Every submission has the same business reference | A fixed hidden value was used for a record identifier |
| Two Taylor enquiries conflict on email uniqueness | Reply Email was made the request key |
| Thank-you page appears but Ava sees no record | It may be awaiting approval, flagged, assigned elsewhere or outside Ava’s access |
| Record is assigned to Isha | Default ownership or the selected form owner is wrong |
| Missing summary is admitted unexpectedly | The field was not required on the published version |
| A duplicate is counted as another request | Product submission count was treated as canonical enquiry count |
| A changed request is discarded | Same identifier was treated as proof of identical instruction |
| Template is unavailable | Wrong module or folder visibility |
| Merge content is blank or unsupported | Missing values, deleted fields or wrong-module merge fields |
| Acknowledgement uses the wrong template | Rule criterion or fallback selection differs from the intended design |
| No active Lead appears after submission | Double opt-in, manual approval or another capture exception is holding it |
| Message preview is recorded as delivery | Rendering and sending were conflated |
| Native send succeeds but reply is absent | No inbox integration, custom-email preference or association issue |
| A Taylor message appears in another request context | Email-address matching does not uniquely identify the enquiry |
| Noor sees the record but not the email | Record access and integrated-email sharing differ |
| No Opened result appears | Transport/tracking does not support that status, or no event is available |
| Lead creation is called qualification | Product admission was confused with the business decision |

## 8. Check your understanding

 1. Why does Taylor’s toner request need another enquiry but not another Contact?
 2. Why is Reply Email unsuitable as the Enquiries module’s unique key?
 3. What is the purpose of Organisation As Supplied?
 4. Why are customer lookups completed by staff?
 5. What can a hidden Capture Source value establish?
 6. What does Request for Approval do?
 7. Why is a created Lead not automatically an established customer?
 8. What does the auto-response fallback do?
 9. What must happen before a double-opt-in record is admitted?
10. Why might a reply reach the mailbox but not appear against the expected CRM record?
11. Why should automatic acknowledgements be excluded from personal-response time?
12. Why can the new 25-minute response example not be compared directly with the 195-minute historical order measure?
## 9. Solutions and explanations

9.1 Intake disposition
| Attempt | Expected business disposition |
| --- | --- |
| S01 | Admit distinct replacement-printer request |
| S02 | Admit new-prospect request |
| S03 | Link exact repeat; no additional canonical request |
| S04 | Admit distinct toner request |
| S05 | Required-summary failure; retain attempt evidence |
| S06 | Admit corrected additional-printer request |

Expected attempt accounting:
\[
6 = 4\text{ admitted distinct requests}
- 1\text{ repeat}
- 1\text{ incomplete attempt}
\]
This is business-ledger accounting. Native counters and queue categories must be recorded as observed.
Expected server-submission path:
- Five completed submissions.
- One browser/form-required-field failure.
If your observed path differs, explain the actual branch. Do not manufacture a browser rejection or native duplicate classification.
9.2 Reviewed relationships and statuses
| Enquiry | Customer | Sales Contact | Related Prospect |
| --- | --- | --- | --- |
| 010 | MER-CUST-001 | MER-CON-001 | None |
| 011 | None | None | MER-LEAD-002 |
| 012 | MER-CUST-001 | MER-CON-001 | None |
| 013 | MER-CUST-002 | MER-CON-002 | None |

“Ready for Sales” means the reviewed intake can proceed to the sales discussion. It does not mean Closed Won or Finance accepted.
All four new enquiries and the Lead are owned by Ava.
Related Opportunity remains unset for these new requests until the sales process establishes the appropriate opportunity.
9.3 Lead result
Expected new prospect record:
| Item | Value |
| --- | --- |
| Prospect Business ID | MER-LEAD-002 |
| First Name | Devon |
| Last Name | Ellis |
| Company | Marlow Workspace |
| Enquiry Reference | MER-ENQ-011 |
| Supplied Email Snapshot | devon.ellis@example.com |
| Primary Email for live laboratory | Actual controlled LAB-DEVON address |
| Capture Source | C07-Prospect-Link |
| Engagement Preference | Request reply only |
| Owner | Ava |
| Business qualification | Not completed |

The existing configured open Lead Status is recorded from the actual organisation.
No new Account, Contact or Deal is required yet.
9.4 Completed template content
The bracketed labels below identify merge-field positions. Replace each entire label through the builder’s field picker; do not send the bracketed notation as literal text.
Enquiries template
Name: MER-ET-007-01 — Request follow-up
Subject: Meridian request — ⟦Enquiry Business ID⟧
Hello ⟦Requester First Name⟧,

We have received request ⟦Enquiry Business ID⟧.

Your request:
⟦Request Summary⟧

To help us prepare the next step, please answer the question below.

This message acknowledges your enquiry. It does not confirm a price,
an order, an installation booking or Finance acceptance.

Meridian Supply
Before sending, add the request-specific question after the question-introduction sentence.
Leads request-only acknowledgement
Name: MER-ET-007-02 — Prospect receipt
Subject: Meridian received your prospect details
Hello ⟦First Name⟧,

Thank you for providing the prospect details for ⟦Company⟧.

We have recorded the details associated with enquiry
⟦Enquiry Reference⟧.

This message concerns your submitted request. Sales will review the
information and contact you about the next step.

Receipt of these details does not confirm a price, an order,
an installation booking or Finance acceptance.

Meridian Supply
Leads fallback acknowledgement
Name: MER-ET-007-03 — Generic prospect receipt
Subject: Meridian received your details
Hello ⟦First Name⟧,

We have received your details associated with enquiry
⟦Enquiry Reference⟧.

Sales will review the request and the recorded communication preference
before deciding the next step.

This is a receipt acknowledgement, not an order confirmation.

Meridian Supply
The fallback acknowledges receipt without inventing a matched rule or a qualification outcome.
Completed personal response for Marlow
Subject: Meridian request — MER-ENQ-011
Hello Devon,

We have received request MER-ENQ-011.

Your request:
Request indicative pricing for three printers; installation choice
not yet decided.

To help us prepare the next step, should installation be included
in the indicative pricing?

This message acknowledges your enquiry. It does not confirm a price,
an order, an installation booking or Finance acceptance.

Meridian Supply
The same template produces different questions for Northbank and Redwood. Its core meaning remains stable.
9.5 Auto-response selection
Submission
Main Devon Lead, source C07-Prospect-Link, preference Request reply only
Optional Blair test, preference Updates requested
Verify actual From, Reply To, recipient, rendered values and observed message result.
A shared template and an active rule are configuration evidence. They are not delivery evidence by themselves.
9.6 Follow-up tasks
The four tasks retain the original enquiry references and appropriate person/account associations.
For Marlow:
- Person association: Devon’s Lead.
- Account association: none.
- Description: enquiry 011 and unresolved installation choice.
For Northbank and Redwood:
- Reuse the established Contacts and Accounts.
- Keep the new request reference in the task context.
- Do not attach the new request to a completed historical Deal merely because that Deal exists.
The task work remains open after a receipt acknowledgement. Closing a CRM task uses its actual system Status, not a separate similarly named custom field.
9.7 Expected final base counts
| Structure | Starting |
| --- | --- |
| Accounts | 6 |
| Contacts | 6 |
| Deals | 6 |
| Enquiries | 1 |
| Leads | 0 |
| Tasks | 1 |
| Order Packets | 6 |
| Packet Versions | 8 |
| Supporting References rows | 10 |

Optional temporary Leads are excluded after cleanup.
The six-Deal opportunity control remains GBP 4750.00. The new enquiries have not established additional opportunity amounts or orders.
9.8 Personal-response measures
Cohort: enquiries 010–013.
Cutoff: 2026-10-06T10:00:00Z.
| Enquiry | Received | First personal response |
| --- | --- | --- |
| 010 | 09:00 | 09:20 |
| 011 | 09:10 | 09:50 |
| 012 | 09:20 | Not sent by cutoff |
| 013 | 09:40 | 09:55 |

The incomplete 09:30 attempt does not replace enquiry 013’s valid 09:40 receipt.
Completed response total:
\[
20 + 40 + 15 = 75\text{ minutes}
\]
Mean completed personal-response time:
\[
\frac{75}{3} = 25\text{ minutes}
\]
Personal-response coverage:
\[
\frac{3}{4}\times 100 = 75\%
\]
Unanswered enquiry 012 age:
\[
10{:}00 - 09{:}20 = 40\text{ minutes}
\]
Exclude:
- The old enquiry 001.
- Duplicate attempt S03.
- Incomplete attempt S05.
- The Lead-form acknowledgement.
- Template previews.
Report actual live-run measures separately.
9.9 Access and communication checks
| Check | Expected result |
| --- | --- |
| Ava sees five base enquiries | Allowed |
| Ava sees Lead 002 | Allowed |
| Ava sends from Enquiries/Leads using shared templates | Allowed after chapter permissions |
| Ava manages webforms | Denied |
| Ava imports or exports | Denied |
| Mia sends from her read-only Northbank Contact context | Denied |
| Leo accesses Enquiries/Leads | Not granted |
| Noor views the new records | Allowed through intended read-only profile/hierarchy |
| Noor views Ava’s integrated mailbox content | Depends on actual email sharing; not established by record access |

Check actual email-sharing results independently.
For the reply test, distinguish:
1. Message received by Sales mailbox.
2. Message synchronized to CRM.
3. Message associated with a record.
4. Message interpreted as the response to enquiry 011.
Only the complete evidence chain supports updating that enquiry’s clarification.
9.10 Independent challenge solutions
Challenge A
Submission conversion:
\[
\frac{5}{12}\times 100 \approx 41.7\%
\]
Abandonment among started visits:
\[
\frac{9-5}{9}\times 100
=
\frac{4}{9}\times 100
\approx 44.4\%
\]
Canonical enquiry yield:
\[
\frac{4}{5}\times 100 = 80\%
\]
Share requiring a new prospect Lead:
\[
\frac{1}{4}\times 100 = 25\%
\]
The other three enquiries belong to established customer relationships. They remain valid enquiries without creating new Leads.
Lead conversion and new Deal creation are zero in this sample. Form conversion is a different measure.
Challenge B
The installation instruction changed, so this is not an exact repeat.
Compare:
- Requester and review evidence.
- Existing canonical request.
- Changed instruction.
- Whether the change concerns the same request or a genuinely separate request.
Retain the new submission and its time in the ledger. Apply the reviewed change through an appropriate correction process.
Preserve the original receipt and first-response events. A later instruction does not make those earlier events disappear.
Challenge C
The evidence supports a sent-message status, not a conclusion about attention or intent.
The official email FAQ explains that integrated-mailbox transport does not provide the same Opened/Clicked statuses as CRM-server transport.
Check:
- Actual sending route.
- Recipient address.
- Delivery/bounce evidence available for that route.
- The recipient’s controlled mailbox in the laboratory.
- Replies.
- Correct conversation association.
“No tracked open” is not equivalent to “ignored.”
Challenge D
Blair’s preference is Updates requested, so the request-only rule does not match.
The configured generic fallback should be selected.
Capture the observed result, then remove the temporary test Lead and verify the base count returns to one Lead.
Challenge E
Before confirmation, the submission is held in the double-opt-in path and is not an admitted active Lead.
After confirmation, inspect the next configured state:
- With manual review also enabled, further admission review may remain.
- Without it, successful confirmation permits the documented record-push step, subject to other capture outcomes.
Observe acknowledgement timing instead of assuming it.
Remove the temporary record and restore the main capture configuration after collecting evidence.
9.11 Knowledge-check answers
 1. Separate enquiry, same Contact: the request changed; Taylor’s person identity did not.
 2. Email is not the request key: the same address can make several valid requests.
 3. Supplied organisation: preserves what the requester entered before a reviewed CRM association exists.
 4. Staff lookups: native form support and relationship-review requirements are separate from supplied text.
 5. Hidden source: a source hint; it does not authorize access or prove business approval.
 6. Awaiting review: holds captured records before ordinary module admission.
 7. Lead versus customer: a Lead represents qualification work; an Account relationship has not necessarily been established.
 8. Fallback: selects the default acknowledgement when no configured rule condition matches.
 9. Double opt-in: the recipient must complete the email-confirmation step before the documented push into CRM.
10. Reply association: mailbox integration, address matching, custom-email preferences, sharing and request context affect the result.
11. Personal-response boundary: an automated receipt is a different event from staff handling.
12. Different measurements: 25 minutes measures enquiry-to-personal-response; 195 minutes measures confirmation-to-Finance-acceptance. Their boundaries and cohorts differ.
## 10. Chapter recap and next step

You have built a capture path that preserves both request identity and customer identity.
The expected base now contains:
- Five enquiries.
- One new prospect Lead.
- Five tasks.
- The existing six-customer, six-Deal and six-order historical reconstruction.
The chapter distinguishes configuration, admission, message rendering, delivery, replies and business qualification. Each requires its own evidence.
Next: Chapter 8 — Sales Operations and Management. You will use the reviewed enquiries and prospect record to organise qualification, opportunities, ownership and sales progress.
## 11. Glossary and further reading

Glossary
| Term | Meaning |
| --- | --- |
| Acknowledgement | Message confirming receipt of information |
| Active record | Record admitted to the ordinary module view, subject to permissions |
| Auto-response rule | Webform response selection based on configured criteria |
| Awaiting-record queue | Capture-review state before admission |
| Canonical enquiry | Retained business record for one distinct request |
| Capture source | Recorded origin of submitted information |
| Conversion rate | A ratio whose meaning depends on the defined stages and denominator |
| Double opt-in | Email-confirmation mechanism before documented record admission |
| Enquiry | One distinct request |
| Fallback | Default response when rule criteria do not match |
| Hidden field | Form field submitted without ordinary visitor display |
| Identity review | Staff assessment linking supplied facts to a business/person record |
| Lead | Prospective qualification work |
| Merge field | Template element populated from a supported record field |
| Personal response | Staff response addressing the specific request |
| Reply synchronization | Association of received mailbox messages with CRM |
| Request grain | Meaning of one enquiry record |
| Submission | A form-send event, which may not become a unique admitted record |
| Template folder | Grouping used to organise and share templates |
| Webform | Published form that captures data into a selected CRM module |

Official product references
Documentation accessed for this chapter: 5 October 2026. Verify the interface, entitlement and publication options shown in your account.
1. Zoho CRM — Webforms: An Introduction (https://help.zoho.com/portal/en/kb/crm/connect-with-customers/webforms/articles/web-forms-introduction)  
Supported modules, permissions and preparation.
2. Zoho CRM — Setting up Webforms (https://help.zoho.com/portal/en/kb/crm/connect-with-customers/webforms/articles/set-up-web-forms)  
Builder controls, required/hidden fields, ownership, publication formats, acknowledgement and double opt-in.
3. Zoho CRM — FAQs: Webforms (https://help.zoho.com/portal/en/kb/crm/faqs/channels/articles/faqs-webforms)  
Supported field types, lookup limitations, approval visibility and publication troubleshooting.
4. Zoho CRM — Awaiting Records (https://help.zoho.com/portal/en/kb/crm/manage-crm-data/record-management/articles/approve-records)  
Capture admission and approval procedure.
5. Zoho CRM — Auto-response rules for webforms (https://help.zoho.com/portal/en/kb/crm/connect-with-customers/webforms/articles/web-form-auto-response-rule)  
Criteria, template selection, activation and fallback behavior.
6. Zoho CRM — Creating Email Templates (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-templates/articles/email-templates)  
Module-specific templates, folders, sharing and preview.
7. Zoho CRM — Understanding Email Template Builder (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-templates/articles/template-builder)  
Text components, merge-field selection and test rendering.
 8. Zoho CRM — Email Communication: Send and receive mails (https://help.zoho.com/portal/en/kb/crm/connect-with-customers/email/user-functions/articles/email-communication-send-and-receive-mails)  
Native sending, integrated mailboxes, custom email fields and reply synchronization.
 9. Zoho CRM — Email Configuration for IMAP and POP3 (https://help.zoho.com/portal/en/kb/crm/connect-with-customers/email/user-functions/articles/email-configuration-for-imap-and-pop3)  
Mailbox integration, authorization, synchronization and email sharing.
10. Zoho CRM — Frequently asked questions on Emails (https://help.zoho.com/portal/en/kb/crm/faqs/emails/articles/frequently-asked-questions-emails-in-zoho-crm)  
Status meanings and transport-dependent tracking.
11. Zoho CRM — Webform Analytics (https://help.zoho.com/portal/en/kb/crm/connect-with-customers/webforms/articles/webform-analytics)  
Visits, starters, submissions, admitted records and analytics access.
12. Zoho CRM — Working with Tasks (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/activities/articles/working-with-tasks-and-meetings)  
Task creation, associations and completion status.
13. Zoho CRM — Working with Custom Fields (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/use-custom-fields)  
Field creation, permissions, required fields and uniqueness.
14. Zoho CRM — Managing Profile Permissions (https://help.zoho.com/portal/en/kb/crm/security-control/profile-management/articles/manage-profile-permissions)  
Sending, templates, webforms and email configuration permissions.
