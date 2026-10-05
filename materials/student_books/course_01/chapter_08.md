# Sales Operations and Management

## 1. What you will learn

Sales operations turns captured interest into organised, evidence-based work.
A useful sales record tells you more than the customer’s name. It identifies the opportunity, explains its current stage, records who owns the next action and supports a realistic management view.
In this chapter, you will qualify Meridian’s new prospect, convert the Lead with controlled field mappings, create two opportunities and organise their progress in a sales pipeline.
By the end, you should be able to:
- Distinguish intake readiness, prospect qualification, opportunity progress and order acceptance.
- Qualify an opportunity using documented facts rather than enthusiasm alone.
- Prepare and execute an individual Lead conversion.
- Preserve business identifiers across Accounts, Contacts and Deals.
- Create a pipeline with meaningful stages and planning probabilities.
- Understand the relationship between Stage, Deal Category and Forecast Category.
- Configure assignment rules for supported entry channels.
- Maintain next actions and related tasks.
- Build list and Kanban views for sales review.
- Calculate raw pipeline, weighted pipeline, coverage and achievement.
- Reconcile new sales records with the existing historical dataset.
- Explain why a CRM sales forecast is different from invoiced revenue or cash received.
Your chapter output: one converted prospect, two open opportunities, an evidence-based sales pipeline, updated follow-up work and a reconciled sales-review package.
All Meridian commercial values and qualification evidence remain synthetic. Actual configuration, conversion and record results require laboratory observation.
## 2. Lessons

2.1 Qualification answers whether an opportunity is worth pursuing
Chapter 7 established that a request exists and can be handled.
Qualification asks a different question:
Is there enough evidence of a relevant buying requirement and a practical next step to pursue this as an opportunity?
A qualification discussion should establish:
| Area | Useful question |
| --- | --- |
| Need | What problem or requirement is the organisation trying to address? |
| Fit | Can Meridian reasonably provide the requested solution? |
| Scope | What quantity, installation or delivery requirements are known? |
| Commercial expectation | Is there an indicative budget or pricing expectation? |
| Decision path | Who evaluates the proposal, and who makes the final decision? |
| Timing | When is the decision expected? |
| Next step | What specific action has been agreed, and who owns it? |

These are discovery questions, not a universal mandatory framework.
A missing budget may require another conversation. A known budget does not prove a customer will buy. A person who explains requirements may not have purchasing authority.
Keep the decisions separate
| Decision | Meaning |
| --- | --- |
| Intake ready for Sales | The request has sufficient reviewed information for a sales discussion |
| Prospect qualified for pursuit | Evidence supports further commercial work |
| Lead converted | CRM has moved the prospect into Account/Contact records, with an optional Deal |
| Opportunity at Proposal Preparation | Work is being organised to prepare a proposal |
| Closed Won | Meridian has the commercial confirmation required by its sales-stage definition |
| Finance accepted | Finance has accepted a complete order-packet version |
| Invoice issued or paid | A separate financial event in Books |

These states are related, but one does not automatically establish the next.
The historical dataset already illustrates this distinction: all six reconstructed Deals are Closed Won, but only four corresponding orders were Finance accepted at the Chapter 1 cutoff.
Write evidence, not impressions
Weak qualification note:
Good prospect. Looks promising.
Useful qualification note:
Devon confirmed three office printers with installation. The indicative budget is GBP 1800. Devon coordinates requirements; Jordan Blake makes the purchasing decision. The intended decision date is 23 October. Next action: confirm the approval-meeting date with Devon.
The second note supports a decision and exposes the remaining work.
2.2 Lead conversion changes the record model
Zoho CRM supports converting a Lead into an Account and Contact, with an optional Deal.
An Account can represent an organisation with which you plan business dealings. Creating one does not prove that the organisation has already placed an order.
Prepare the conversion before selecting Convert
Check:
- Correct Lead and business identity.
- Qualification evidence.
- Existing Account and Contact matches.
- Required destination fields.
- Field-conversion mappings.
- New-record ownership.
- Whether a Deal should be created during conversion.
- Existing notes, emails and activities.
- The source-to-destination crosswalk.
The official conversion guide states that a converted Lead cannot be reverted to its original Lead state.
Therefore, a missing-data test should be performed in a preflight worksheet or controlled test record, not by deliberately converting the main prospect incorrectly.
Do not reuse the Lead ID as every destination ID
Meridian’s identities remain distinct:
| Record | Business identifier |
| --- | --- |
| Source prospect | MER-LEAD-002 |
| New Marlow Account | MER-CUST-007 |
| New Devon Contact | MER-CON-010 |
| Marlow opportunity | MER-DEAL-008 |

Mapping Prospect Business ID directly into Customer Business ID would store the wrong kind of identity.
A value can be unique and still be semantically wrong.
Conversion helper fields
Add these optional text fields to Leads:
- Conversion Customer Business ID
- Conversion Contact Business ID
Use the same field type and a compatible length as the destination business-ID fields. The conversion guide requires compatible types and lengths.
For Lead 002, populate:
- Conversion Customer Business ID: MER-CUST-007
- Conversion Contact Business ID: MER-CON-010
These values belong to this Lead. They are not global defaults for future prospects.
Add these optional fields to Contacts:
| Field | Type |
| --- | --- |
| Source Prospect Reference | Text |
| Supplied Email Snapshot | Text |
| Engagement Preference | Picklist |

Also add Origin Prospect Reference, text, to Enquiries. Populate enquiry 011 with MER-LEAD-002 before conversion.
This preserves the business origin independently of what happens to the existing Related Prospect lookup.
Configure Lead Conversion Mapping
Using Isha:
1. Open Setup → Customization → Modules and Fields.
2. Select Leads.
3. Open Module Settings → Lead Conversion Mapping.
4. Select the Standard source and destination layouts where offered.
5. Inspect standard mappings.
6. Configure the custom mappings.
7. Save.
8. Record the mapping evidence.
Use:
| Lead source field | Destination field |
| --- | --- |
| Conversion Customer Business ID | Accounts → Customer Business ID |
| Conversion Contact Business ID | Contacts → Contact Business ID |
| Prospect Business ID | Contacts → Source Prospect Reference |
| Supplied Email Snapshot | Contacts → Supplied Email Snapshot |
| Engagement Preference | Contacts → Engagement Preference |

Standard mappings transfer Company to the Account name and person/email information to the Contact.
For a live laboratory, the Lead’s primary Email contains the controlled address from Chapter 7. Its Supplied Email Snapshot preserves devon.ellis@example.com.
Do not replace the controlled primary Email during conversion merely to make it resemble the printed dataset.
Inspect existing-record suggestions
The conversion guide describes matching through mapped unique fields and standard information such as email and company name.
If the conversion screen suggests an unexpected existing record:
1. Inspect its actual business ID.
2. Compare the supplied organisation and person.
3. Check the controlled-email mapping.
4. Resolve the match before continuing.
An apparent name or email match is not a reason to merge unrelated business identities.
Convert without creating the Deal
For this chapter’s main path:
 1. Open Lead MER-LEAD-002.
 2. Select Convert.
 3. Verify the expected new Account and Contact choices.
 4. Choose the option that does not create a Deal during conversion.
 5. Select Ava as the owner of new records.
 6. Inspect the conversion details.
 7. Convert.
 8. Verify the Account and Contact.
 9. Record their actual CRM record IDs.
10. Inspect the Converted Leads view.
Creating the Deal separately makes its pipeline, stage and Opportunity Business ID explicit.
The official documentation supports conversion without a Deal. Where the interface shows “Create a new Deal,” leave it unselected; where it shows “Do not create a new Deal,” select that option.
Inspect related information after conversion
The Lead-management FAQ explains that open activities are associated with the corresponding converted records and Lead emails map to the Contact.
Check actual record IDs and related lists. Do not create replacement activities merely because a view changed.
Custom enquiry relationships also require inspection. Do not assume an arbitrary Lead lookup automatically becomes a Contact lookup.
For enquiry 011:
- Preserve Origin Prospect Reference.
- Select the new Customer and Sales Contact.
- Later select the new Related Opportunity.
- Record the observed outcome of the old Related Prospect lookup.
2.3 A pipeline represents a commercial process
A pipeline groups Deals that follow a particular sales process.
A stage records where an opportunity currently sits in that process.
Stage definitions should tell the salesperson:
- What is known.
- What evidence supports the position.
- What work comes next.
- What would justify moving forward or closing the opportunity.
A stage name without entry evidence becomes a subjective label.
Meridian Equipment Sales
Use the following synthetic planning model:
| Stage | Probability | Deal Category | Forecast Category | Evidence for the stage |
| --- | --- | --- | --- | --- |
| Meridian Qualification | 10% | Open | Pipeline/Open | A relevant opportunity is being assessed |
| Meridian Needs Confirmed | 25% | Open | Pipeline/Open | Requirements, decision path and timing are documented |
| Meridian Proposal Preparation | 50% | Open | Best Case | Requirements support preparing a proposal; the next preparation action is assigned |
| Meridian Decision Review | 75% | Open | Best Case | A proposal is under a documented customer decision process |
| Closed Won | 100% | Closed Won | Closed | The commercial confirmation required by Meridian’s sales definition exists |
| Closed Lost | 0% | Closed Lost | Omitted | The opportunity has been declined, withdrawn or otherwise closed unsuccessfully |

The first four stage names are distinct from existing standard stages so their probability settings do not silently redefine an unrelated process.
The probabilities are training planning assumptions. They are not statistically estimated from Meridian’s small dataset.
The builder may label the early open forecast bucket Open; the Forecasts guide describes Pipeline. Record the actual label shown.
Stage, category and probability are different
- Stage: commercial position.
- Deal Category: Open, Closed Won or Closed Lost.
- Forecast Category: how the opportunity contributes to forecast views.
- Probability: planning weight used for Expected Revenue.
A 75% opportunity remains open.
A forecast category such as Committed is also not Finance acceptance.
Shared stages share settings
The pipeline guide states that a stage used in different pipelines shares its probability value.
Before changing an existing stage, inspect where it is used.
For this exercise, verify the existing Closed Won and Closed Lost mappings. Retain the historical stage values and evidence rather than redefining them to improve the new pipeline’s appearance.
Configure the pipeline
Using Isha:
 1. Open Setup → Customization → Pipelines.
 2. Select New Pipeline.
 3. Name it Meridian Equipment Sales.
 4. Associate it with the Standard Deals layout.
 5. Add the four new stages through Create New Stages.
 6. Enter their probabilities and categories.
 7. Include the existing Closed Won and Closed Lost stages.
 8. Arrange the stages in order.
 9. Leave the new pipeline unselected as the default for this exercise.
10. Save.
If this is the first pipeline configuration, the guide explains that CRM creates a system-defined Standard pipeline for existing Deals.
Record the actual historical pipeline name and verify the six existing Deals’ assignments.
Select Meridian Equipment Sales explicitly for the two new opportunities.
A pipeline does not enforce every transition
A user with editing authority can change Stage, including through supported Kanban operations.
The stage definitions in this chapter are manually applied business criteria. Enforced transition controls are developed in Chapter 10.
2.4 Create an opportunity with a clear grain
A Deal represents one commercial opportunity.
For Meridian:
- Northbank’s replacement-printer request becomes Deal 007.
- Marlow’s three-printer request becomes Deal 008.
- Northbank’s toner request remains intake work until the printer model is known.
- Redwood’s additional-printer request remains intake work until the delivery requirement is clarified.
This does not imply that the last two requests are unimportant. It means their next decision has not yet justified the opportunity record used in this exercise.
Reuse established relationships
For Northbank:
- Reuse Account MER-CUST-001.
- Reuse Contact MER-CON-001.
- Create a new Deal.
Do not reopen the completed historical Deal 001 merely because Taylor is the same person.
Add sales-management fields
Add these optional fields to Deals:
| Field | Type |
| --- | --- |
| Originating Enquiry | Lookup to Enquiries |
| Next Sales Action | Text |
| Next Sales Action Due | Date/Time |
| Stage Evidence Reference | Text |

These are optional at the layout level so the historical Deals are not given invented values.
For new open opportunities, the chapter’s quality check requires a usable next action and due time.
Create the Deal
Using Ava:
 1. Open Deals.
 2. Select New/Create Deal.
 3. Enter Opportunity Business ID.
 4. Enter a descriptive Deal Name.
 5. Select the correct Account and Contact.
 6. Select Standard layout and Meridian Equipment Sales.
 7. Select the initial stage.
 8. Enter Amount and planned Closing Date.
 9. Select the originating Enquiry.
10. Enter the next-action fields.
11. Verify owner Ava.
12. Save and reopen.
The Amount is an opportunity estimate.
The official Deals guide also explains that products associated with a Deal do not automatically sum into its Amount. Formal product/pricing records are developed in Chapter 12.
Planned Closing Date is not an acceptance timestamp
It represents the expected sales decision/closure date.
It is not:
- Confirmation Received At.
- Packet Submitted At.
- Finance Accepted At.
- Invoice date.
- Payment date.
Keep the event boundaries explicit.
2.5 Ownership rules need a supported entry channel
An owner identifies the person responsible for managing the record.
A role, group membership or visible record does not automatically make every user responsible for the next sales action.
Assignment rules
Zoho documents assignment rules for records entering through:
- Import.
- Webforms.
- Supported API entry.
The assignment-rule guide states that ordinary manual record creation does not trigger them.
Likewise, changing a field on an existing record is not a general-purpose assignment-rule trigger.
Configure Meridian’s Lead assignment
Using Isha:
 1. Open Setup → Automation → Assignment.
 2. Select Create Assignment Rule.
 3. Choose Leads.
 4. Name the rule Meridian Prospect Ownership.
 5. Add a rule entry.
 6. Set Capture Source equal to C07-Prospect-Link.
 7. Assign matching records to Ava’s actual active user.
 8. Use no online-status or shift-availability condition for this static laboratory allocation.
 9. Select Isha as the explicit default user.
10. Save the entry and rule.
11. Open the Chapter 7 Leads form.
12. Replace its fixed-owner choice with this assignment rule.
13. Save and retain the current publication configuration.
No automatic follow-up task is added by this rule in the chapter’s base configuration. Follow-up tasks are managed explicitly.
Define the unmatched route
The assignment FAQ explains that records not matching criteria go to the default user.
The default user is therefore operationally important.
Isha’s fallback ownership means:
A record that did not match the intended route needs administrative triage.
It does not mean Isha is now the ordinary sales representative.
If multiple eligible users are selected, the documented assignment mechanism can distribute records in round-robin fashion. Meridian’s base exercise has one Sales owner, so equal multi-representative distribution is not demonstrated.
Test ownership through the actual channel
A criterion matching on paper does not establish that the rule ran.
Record:
- Entry channel.
- Selected rule.
- Source value.
- Actual owner.
- Default-route result.
- Any availability conditions.
2.6 Activities turn “follow up” into accountable work
A useful next action has:
- A specific verb and outcome.
- An owner.
- A due date or time.
- A related record.
- A completion condition.
Weak:
Follow up.
Useful:
Confirm the approval-meeting date with Devon by 13 October at 11:00 UTC; record the agreed date in the Marlow opportunity note.
Deal next action and Task are related controls
The Deal fields summarize what should happen next.
The Task represents assigned work.
They should agree, but they are not automatically synchronized by the fields created in this chapter.
Avoid marking a task Completed merely because:
- A receipt acknowledgement was sent.
- The Deal stage changed.
- A new note was added.
The official Tasks guide identifies Completed as the system status that closes the task.
Respect the working calendar
Meridian’s training calendar remains:
- Monday–Friday.
- 09:00–17:00 UTC.
- Closure on Monday, 12 October 2026.
A planned follow-up on that closure date requires review.
The Marlow action is therefore placed on Tuesday, 13 October. Do not assume every manually entered due date is automatically adjusted for the holiday.
System activity is not always customer progress
Zoho’s Last Activity Time can include record edits, note changes and other administrative actions.
A recently edited record may still lack customer contact.
For sales review, inspect the underlying evidence:
- Customer discussion.
- Requirements clarification.
- Proposal work.
- Decision meeting.
- Completed next action.
Do not equate an active-looking timestamp with commercial progress.
2.7 Use list and Kanban views for different questions
A list view is useful for detailed review across fields.
A Kanban view is useful for seeing the distribution of opportunities by stage.
Neither view grants access beyond the user’s record and field permissions.
Create a custom list view
Using Isha:
1. Open Deals.
2. Open the list-view dropdown.
3. Select New Custom View.
4. Enter the name.
5. Add criteria.
6. Choose columns.
7. Share with the intended users.
8. Save.
9. Verify the result as those users.
Create Meridian Open Equipment Opportunities.
Use these criteria:
1. Pipeline is Meridian Equipment Sales.
2. Stage is Meridian Qualification.
3. Stage is Meridian Needs Confirmed.
4. Stage is Meridian Proposal Preparation.
5. Stage is Meridian Decision Review.
Pattern:
1 and (2 or 3 or 4 or 5)
This includes the defined open stages and excludes both terminal stages.
Choose useful columns:
- Opportunity Business ID.
- Deal Name.
- Account.
- Stage.
- Amount.
- Expected Revenue.
- Closing Date.
- Next Sales Action.
- Next Sales Action Due.
Missing-next-action view
Create a second view using the same pipeline/open-stage scope, plus:
- Next Sales Action is empty; or
- Next Sales Action Due is empty.
Use explicit parentheses.
A record can save successfully while still appearing in this quality view because these fields are not globally mandatory.
Fixed review-point view
For the supplied management exercise, use:
2026-10-09T12:00:00Z
Create a snapshot view for open equipment opportunities with a nonblank Next Sales Action Due before that time.
Name the view clearly, such as Meridian Action Review — 09 Oct 12 UTC.
Do not call a fixed historical/simulated snapshot a live “overdue now” view.
Configure Kanban
Using Isha:
1. Open Deals.
2. Select the Kanban view icon.
3. Set the view name.
4. Categorize by Stage.
5. Aggregate by Amount.
6. Select identifying fields.
7. Save.
8. Select Standard layout and Meridian Equipment Sales.
9. Verify the two cards.
The official guide documents drag-and-drop stage changes. Those changes update the underlying record.
Noor’s read-only view should not become an editing route.
Stage age
Use the actual Stage History for a live run.
The supplied case separately contains scenario stage-entry times for paper calculations.
Do not backdate system stage history or treat rapid laboratory updates as proof that an opportunity genuinely spent days in a stage.
2.8 Understand raw pipeline, weighted pipeline and targets
Raw open pipeline sums the Amount of open opportunities.
Weighted open pipeline multiplies each Amount by its planning probability.
\[
\text{Weighted opportunity}
=
\text{Amount}
\times
\frac{\text{Probability}}{100}
\]
For a GBP 650 opportunity at 50%:
\[
650 \times 0.50 = 325\text{ GBP}
\]
That is a planning value, not an invoice amount or guaranteed result.
Target, achievement and pipeline differ
| Measure | Meaning |
| --- | --- |
| Target | Desired outcome for a defined period |
| Achievement | Qualifying completed sales under the forecast definition |
| Open pipeline | Opportunities still being pursued |
| Weighted pipeline | Probability-weighted planning value |
| Gap to target | Target minus achievement |
| Forecast-category amount | Amount assigned to a category such as Pipeline or Best Case |

Forecast category totals are not automatically the same as weighted totals.
Coverage
\[
\text{Raw coverage}
=
\frac{\text{Open pipeline amount}}{\text{Target}}
\]
\[
\text{Weighted coverage}
=
\frac{\text{Weighted open pipeline}}{\text{Target}}
\]
Coverage above 1 does not establish that the target will be achieved.
The probabilities and opportunity dates still need credible evidence.
Keep populations separate
Meridian has:
- Six historical Closed Won Deals.
- Two new open opportunities.
The historical GBP 4750 total is not current open pipeline.
A broad total can be mathematically correct and operationally misleading.
2.9 Configure and inspect native forecasts
The official Forecasts guide supports amount-based and quantity-based forecasts, hierarchy-based targets and selected-Deal criteria.
Only administrators configure the global forecast foundation. Other forecast actions depend on role and forecast-manager authority.
For this exercise, Isha performs native configuration and reconciliation.
Inspect the existing foundation first
The guide states that changing forecast configuration can delete current/future forecasts, and changing fiscal-year configuration can delete forecast history.
Inspect the organisation’s actual existing configuration before altering it.
Use a compatible existing foundation where available. If the laboratory cannot support the intended configuration, complete the supplied forecast worksheet and record the native feature as not executed rather than claiming a product result.
Intended foundation
| Setting | Chapter choice |
| --- | --- |
| Model | Top-down |
| Hierarchy | Existing role hierarchy |
| Amount field | Deals Amount |
| Fiscal settings | Existing organisation configuration |
| Forecast adjustments | Not required |
| Ordinary forecast-manager appointment | Not required |

Do not select Expected Revenue as the amount basis and then also apply the planning probabilities a second time.
Native procedure
Using Isha:
 1. Open Forecasts.
 2. Select Configure Forecast where no foundation exists.
 3. Choose Top-down.
 4. Choose Role hierarchy.
 5. Select the revenue/amount forecast using Deals Amount.
 6. Review the existing fiscal settings.
 7. Save the compatible configuration.
 8. Select Create Forecast.
 9. Choose Revenue-based.
10. Select the supported period covering the October exercise window.
11. Name it Meridian Equipment — October Planning.
12. Choose Selected Deals.
13. Filter to Meridian Equipment Sales.
14. Restrict Closing Date to 1–31 October 2026.
15. Continue to target setting.
16. Allocate the illustrative target.
17. Save.
18. Open View Full Hierarchy and inspect contributing Deals.
19. Refresh where available and record the last-synced time.
Monthly selection depends on the fiscal-year pattern. If the tool uses a fiscal period instead, record its actual boundaries and the October date criteria.
Illustrative target allocation
For this exercise only:
- Company target: GBP 2000.
- Process Lead branch total: GBP 2000.
- Sales branch total: GBP 2000.
- Ava individual target: GBP 2000.
- Other individual sales targets in this exercise: zero.
Branch totals are rollups. Do not add them together and report GBP 6000 as the target.
This is a synthetic planning target, not a course passing rule or a forecast inferred from historical performance.
Reconcile freshness
The guide documents periodic synchronization and manual refresh.
Record the actual synchronization time before comparing native forecast values with your worksheet. A stale native view is not proof that a record update failed.
## 3. Visual explanation

flowchart TD
    A[Reviewed enquiry] --> B{Existing relationship?}
    B -->|Yes| C[Reuse Account and Contact]
    B -->|New prospect| D[Qualification discussion]
    D --> E{Evidence supports pursuit?}
    E -->|Not yet| F[Clarify and retain Lead]
    E -->|Yes| G[Verify conversion mappings and identities]
    G --> H[Convert to Account and Contact]
    C --> I[Create distinct opportunity]
    H --> I
    I --> J[Select pipeline and stage]
    J --> K[Assign next action and task]
    K --> L[Review evidence and progress]
The existing-customer branch does not need another Lead conversion.
The new-prospect branch creates a formal relationship only after the supplied qualification decision. Deal creation is explicit on both branches.
flowchart LR
    A[Open Deal Amount] --> B[Raw pipeline]
    A --> C[Multiply by planning probability]
    C --> D[Weighted pipeline]
    E[Closed Won in forecast scope] --> F[Achievement]
    G[Period target] --> H[Gap and coverage]
    B --> H
    D --> H
    F --> H
Raw pipeline, weighted pipeline and achievement answer different questions.
None of these boxes represents payment received in Books.
## 4. Worked case

Northbank is a new opportunity within an existing relationship
Enquiry MER-ENQ-010 concerns one replacement printer with installation.
The reviewed customer and Contact already exist:
- MER-CUST-001
- MER-CON-001
Create Deal MER-DEAL-007.
Do not create another Northbank Account, another Taylor Contact or another Lead.
Why not reuse Deal 001?
Deal 001 belongs to the completed historical order process.
The replacement-printer request is a separate commercial opportunity with its own:
- Scope.
- Amount estimate.
- Planned closing date.
- Stage.
- Next action.
Reusing the old Deal would mix completed history with new work.
Marlow’s prospect can now be pursued
The new evidence establishes:
- Three printers with installation.
- Indicative budget GBP 1800.
- Devon coordinates requirements.
- Jordan Blake makes the purchasing decision.
- Intended decision date: 23 October 2026.
The decision path is known even though the purchase is not approved.
Convert Lead 002 to:
- Account MER-CUST-007, Marlow Workspace.
- Contact MER-CON-010, Devon Ellis.
Create Deal MER-DEAL-008 separately.
Calculate the management values
Final Northbank position:
- Amount: GBP 650.
- Stage: Meridian Proposal Preparation.
- Probability: 50%.
\[
650 \times 0.50 = 325\text{ GBP}
\]
Final Marlow position:
- Amount: GBP 1800.
- Stage: Meridian Needs Confirmed.
- Probability: 25%.
\[
1800 \times 0.25 = 450\text{ GBP}
\]
Combined raw pipeline:
\[
650 + 1800 = 2450\text{ GBP}
\]
Combined weighted pipeline:
\[
325 + 450 = 775\text{ GBP}
\]
Neither opportunity is Closed Won.
Choose the next action by evidence
At the supplied review point:
- Northbank’s next action is one hour late.
- Marlow’s next action is scheduled for 13 October.
The larger Marlow Amount does not automatically make it the first action.
Northbank has a specific due commitment requiring attention. The manager should inspect that commitment rather than prioritising solely by Amount.
## 5. Try it yourself — guided practice

5.1 Confirm the starting base
Structure
Accounts
Contacts
Deals
Enquiries
Active base Leads
Tasks
Order Packets
Packet Versions
Supporting References rows
The active base Lead is MER-LEAD-002.
Identify optional earlier challenge records separately.
Capture the actual starting record IDs and retained before-images using the Chapter 6 method.
5.2 Use the new qualification evidence
These are additional synthetic case inputs.
NEEDS-007-01 — Northbank
Recorded scenario time: 2026-10-07T09:30:00Z
| Item | Reviewed fact |
| --- | --- |
| Request | One replacement printer with installation |
| Account/Contact | Northbank/Taylor |
| Installation postcode | AB2 3CD |
| Indicative opportunity estimate | GBP 650 |
| Intended decision date | 2026-10-16 |
| Decision path | Taylor coordinates the requirement and obtains purchasing confirmation |
| Current commercial confirmation | No order confirmation |
| Next preparation work | Prepare draft pricing scope |

QUAL-008-01 — Marlow
Recorded scenario time: 2026-10-07T10:00:00Z
| Item | Reviewed fact |
| --- | --- |
| Request | Three printers |
| Installation | Include installation |
| Installation postcode | AB1 2CD |
| Indicative budget/estimate | GBP 1800 |
| Requirements contact | Devon Ellis |
| Final decision-maker | Jordan Blake |
| Intended decision date | 2026-10-23 |
| Current commercial confirmation | No order confirmation |
| Qualification decision | Pursue the opportunity |
| Next work | Confirm the approval-meeting date with Devon |

Jordan Blake is a documented decision-path participant. The exercise does not create another Contact without contact-record inputs.
For the other enquiries:
| Enquiry | Remaining question |
| --- | --- |
| 012 | Printer model needed for toner compatibility |
| 013 | Delivery postcode not yet supplied |

5.3 Prepare the conversion mapping and permissions
1. Add the conversion helper and destination trace fields.
2. Configure the mappings from Lesson 2.2.
3. Add Origin Prospect Reference to Enquiries.
4. Populate enquiry 011 with MER-LEAD-002.
5. Give Meridian Sales the individual Convert Leads permission.
6. Keep mass conversion outside the ordinary exercise.
7. Verify that Noor’s read-only account cannot convert the Lead.
8. Verify Ava’s conversion authority.
Complete this worksheet:
| Check | Expected value |
| --- | --- |
| Source prospect | MER-LEAD-002 |
| Target customer identity | MER-CUST-007 |
| Target contact identity | MER-CON-010 |
| Company | Marlow Workspace |
| Owner | Ava |
| Required mappings | Reviewed and compatible |
| Existing matches | None expected for this base case |
| Deal during conversion | Not created |

For the missing-data test, use a worksheet copy with Conversion Contact Business ID blank. Record the readiness failure, then restore the correct value before conversion.
5.4 Convert and reconcile Marlow
Populate Lead 002:
- Conversion Customer Business ID: MER-CUST-007
- Conversion Contact Business ID: MER-CON-010
Execute the individual conversion without a Deal.
Verify:
- Account name and Customer Business ID.
- Contact name and Contact Business ID.
- Contact-to-Account association.
- Source Prospect Reference.
- Supplied Email Snapshot.
- Engagement Preference.
- Controlled primary Email.
- Owner Ava.
- Converted Leads representation.
- Related activities and correspondence.
Update enquiry 011:
- Customer → Marlow Account.
- Sales Contact → Devon Contact.
- Intake Status → Ready for Sales.
- Origin Prospect Reference remains MER-LEAD-002.
Identity Review remains the intake-time assessment New prospect. Do not rewrite it to imply that Marlow was an existing customer at initial capture.
Record the observed old Related Prospect lookup behavior.
5.5 Create the pipeline and two opportunities
Create Meridian Equipment Sales with the stage definitions in Lesson 2.3.
Then create:
OpportunityBusinessID,DealName,CustomerBusinessID,ContactBusinessID,OriginatingEnquiry,AmountGBP,ClosingDate,InitialStage,OwnerReference
MER-DEAL-007,Northbank replacement printer and installation,MER-CUST-001,MER-CON-001,MER-ENQ-010,650.00,2026-10-16,Meridian Qualification,MER-USR-002
MER-DEAL-008,Marlow three printers and installation,MER-CUST-007,MER-CON-010,MER-ENQ-011,1800.00,2026-10-23,Meridian Qualification,MER-USR-002
Use the actual record lookups and owner account, not the printed business references as Zoho IDs.
Required-field test
When preparing Northbank’s new Deal, attempt Save with Closing Date blank.
Record the actual required-field result. Supply 2026-10-16, then save the valid record.
Next-action quality test
Initially leave Marlow’s Next Sales Action and Next Sales Action Due blank.
The fields are optional at layout level. Inspect whether the record saves and appears in the missing-next-action view.
Repair it using the supplied action below. Record the same Deal ID before and after the repair.
5.6 Apply the stage evidence
Use these scenario events:
| Opportunity | Scenario event |
| --- | --- |
| 007 | Requirements confirmed |
| 007 | Ready for proposal preparation |
| 008 | Requirements and decision path confirmed |

PREP-007-01 means draft-pricing preparation is assigned. It is not a customer-approved quote.
NEEDS-008-01 confirms the supplied Marlow requirements and decision path.
Set the final records:
| Field | Deal 007 |
| --- | --- |
| Stage | Meridian Proposal Preparation |
| Stage Evidence Reference | PREP-007-01 |
| Next Sales Action | Prepare draft pricing scope |
| Next Sales Action Due | 2026-10-09 11:00 UTC |

Link:
- Enquiry 010 → Related Opportunity 007.
- Enquiry 011 → Related Opportunity 008.
- Each Deal → its Originating Enquiry.
Record actual stage-history timestamps separately from the scenario ledger.
5.7 Update the follow-up tasks
Close these existing tasks after checking the supplied work and record associations:
| Task | Completion basis |
| --- | --- |
| MER-TASK-003 | Northbank installation scope clarified |
| MER-TASK-004 | Marlow qualification facts collected and converted relationship checked |

Use the actual system Status Completed.
Inspect Task 004’s associations after conversion rather than creating a duplicate task.
Keep:
- Task 005 open: toner compatibility unresolved.
- Task 006 open: delivery requirement unresolved.
Create:
| Reference | Subject |
| --- | --- |
| MER-TASK-007 | Prepare draft pricing scope — MER-ENQ-010 |
| MER-TASK-008 | Confirm approval-meeting date — MER-ENQ-011 |

Owner: Ava.
Use an existing open Status.
The Deal’s Next Sales Action Due contains a time. The standard Task Due Date is a date. Retain this distinction in the management review.
5.8 Configure and test assignment
Configure Meridian Prospect Ownership.
Add C08-Fallback-Test as a Lead Capture Source picklist value.
Use these temporary tests:
| Test | Business ID | Entry channel |
| --- | --- | --- |
| AS01 | MER-LEAD-LAB-008-01 | Leads webform with rule selected |
| AS02 | MER-LEAD-LAB-008-02 | Cloned test webform with same rule |
| AS03 | MER-LEAD-LAB-008-03 | Manual creation by Isha |

Use:
- First Name: Rae.
- Last Name: Assignment.
- Company: Meridian Assignment Laboratory.
- Enquiry Reference: corresponding LAB-ENQ-008-01, -02 or -03.
- Engagement Preference: Request reply only.
- Email: a controlled laboratory address.
- Supplied Email Snapshot: rae.assignment@example.com.
The test references are not canonical customer enquiries.
For AS02, clone the Leads form within the same module and change its hidden source value.
For AS03, explicitly choose Isha as owner during manual creation.
Capture actual owners and channel/configuration evidence.
Afterward, Isha removes the three unconverted temporary Leads and deactivates the cloned test form. Retain the main form’s assignment-rule configuration.
5.9 Build the management views
Create and share:
1. Meridian Open Equipment Opportunities.
2. Meridian Missing Next Action.
3. Meridian Action Review — 09 Oct 12 UTC.
4. Meridian Equipment Kanban.
5. A Sales task view for tasks whose subjects contain MER-ENQ-.
Test:
- Ava can update her opportunity.
- Noor can inspect but cannot edit or drag it to another stage.
- Leo’s permitted Deal access remains read-only.
- Mia’s Northbank customer context does not grant Deals-module access.
Continue customer messages through the Enquiries route permitted in Chapter 7. Lead conversion does not itself grant Contacts or Deals email-sending permission.
5.10 Produce the sales review and forecast
Review point:
2026-10-09T12:00:00Z
Calculate:
- Raw open pipeline.
- Weighted open pipeline.
- Total Amount across historical and new Deals.
- Coverage against the illustrative GBP 2000 target.
- Achievement and gap in the selected October pipeline.
- Scenario current-stage age.
- Due next actions.
- Sales-task completion and overdue counts.
The sales-task cohort is tasks 003–008. The Chapter 4 inspection Task 001 remains outside that operational cohort.
Configure and inspect the native forecast where available. Record the actual period, criteria, contributing Deal IDs and synchronization time.
Use these artifacts:
- C01_CH08_Meridian_Qualification.md
- C01_CH08_Meridian_Conversion_Map.md
- C01_CH08_Meridian_Conversion_Crosswalk.csv
- C01_CH08_Meridian_Pipeline_and_Stages.md
- C01_CH08_Meridian_Opportunity_Register.csv
- C01_CH08_Meridian_Assignment_Tests.md
- C01_CH08_Meridian_Sales_Review.md
- C01_CH08_Meridian_Forecast_Reconciliation.md
## 6. Independent challenge

Challenge A — A unique value can still be wrong
A proposed conversion map sends:
- Prospect Business ID → Customer Business ID.
- Prospect Business ID → Contact Business ID.
The value is MER-LEAD-002, and no destination record currently uses it.
Explain:
1. Why uniqueness does not make this mapping correct.
2. Which identities should be used instead.
3. Where the source prospect reference should be retained.
4. What recovery can and cannot do after a mistaken conversion.
Challenge B — Pipeline coverage is not achievement
A manager sees GBP 2450 of open pipeline against a GBP 2000 target and writes:
Target achieved: 122.5%.
Correct the statement using the supplied main-case data.
Distinguish:
- Raw coverage.
- Weighted coverage.
- Actual achievement.
- Gap to target.
Challenge C — Calculate a separate sales cohort
Use this paper-only simulation at 15 October 2026:
| Simulation | Amount GBP | Opened | Outcome |
| --- | --- | --- | --- |
| SIM-01 | 800 | 2026-10-01 | Closed Won |
| SIM-02 | 400 | 2026-10-02 | Closed Lost |
| SIM-03 | 950 | 2026-10-03 | Open |
| SIM-04 | 650 | 2026-10-02 | Closed Won |
| SIM-05 | 500 | 2026-10-04 | Open |

Target: GBP 2000.
Calculate:
1. Win rate among closed opportunities.
2. Won proportion of the complete five-opportunity cohort.
3. Won Amount.
4. Target attainment.
5. Actual gap.
6. Weighted open pipeline.
7. Mean won sales-cycle length in elapsed calendar days.
Do not import or apply these simulation outcomes to the main Meridian records.
Challenge D — A recent edit looks like progress
Northbank’s record was edited five minutes before review to correct a spelling mistake.
Its next sales action is still late, and no new customer discussion occurred.
Explain why Last Activity Time alone is insufficient for deciding that the opportunity is progressing.
Challenge E — The wrong stage filter
A proposed “Open Deals” view uses only:
Stage is not Closed Won.
Explain which records could still enter the view and provide a better definition for Meridian Equipment Sales.
## 7. Common problems and recovery

| Problem | Likely explanation |
| --- | --- |
| Convert is unavailable | Convert Leads permission, record access or record state does not permit it |
| Destination mapping is absent | Types or field lengths are incompatible |
| Source Lead ID becomes Customer ID | Different entity identities were mapped together |
| An unexpected existing Contact is suggested | Unique-field or standard email/name matching found a candidate |
| A converted Lead disappears from the active view | Conversion moved it to Converted Leads |
| A new Deal appears unexpectedly | Deal creation was selected during conversion |
| Custom enquiry links are wrong after conversion | They were assumed to update automatically |
| Pipeline creation changes old Deal assignments | First-time setup created the Standard pipeline |
| New Deal lands in the historical pipeline | Default pipeline was used |
| Probability change affects other Deals | A shared stage’s mapping was edited |
| Deal saves without a next action | Layout fields are optional |
| Assignment rule does not run for manual creation | The channel is unsupported for that trigger |
| A record goes to Isha | No criterion matched or the intended route fell back |
| A task is called complete but remains open | The actual system Status is not Completed |
| Marlow action is due on 12 October | The training closure was overlooked |
| Kanban total differs from the worksheet | Layout, pipeline, view, access or aggregation differs |
| Noor can see a card but cannot move it | Read-only authority is working |
| Forecast shows old values | Synchronization has not refreshed |
| Forecast achievement includes unrelated Deals | Period or selected-Deal criteria are too broad |
| Stage-age figure differs from the supplied case | Actual stage history and scenario times were mixed |
| Target is counted several times | Branch rollups were added as separate allocations |

## 8. Check your understanding

 1. What is the difference between intake readiness and qualification?
 2. Why can a converted Account still represent an organisation that has not bought?
 3. Why does conversion require separate destination business IDs?
 4. What should be checked when the converter suggests an existing Contact?
 5. Why does the main exercise create the Deal separately?
 6. How do Stage, Deal Category and Forecast Category differ?
 7. Why are planning probabilities not guaranteed outcomes?
 8. Which entry channels trigger assignment rules?
 9. Why is a recent Last Activity Time not always customer progress?
10. What is the difference between a Task Due Date and Next Sales Action Due?
11. Why does GBP 2450 pipeline not mean the GBP 2000 target is achieved?
12. Why should native forecast synchronization time be recorded?
## 9. Solutions and explanations

9.1 Qualification decisions
| Enquiry | Decision | Reason |
| --- | --- | --- |
| 010 | Create Northbank opportunity | Scope, installation requirement and next preparation work are documented |
| 011 | Qualify and convert Marlow prospect; create opportunity | Need, estimate, decision path and timing support pursuit |
| 012 | Continue intake follow-up | Toner compatibility cannot yet be established |
| 013 | Continue intake follow-up | Delivery requirement remains unresolved |

The last two remain valid enquiries. They are not counted as lost opportunities merely because no Deal was created in this exercise.
Marlow’s known decision-maker does not mean the purchase is approved.
9.2 Conversion crosswalk
| Source | Destination |
| --- | --- |
| MER-LEAD-002 | Account |
| MER-LEAD-002 | Contact |
| MER-ENQ-011 | Separately created Deal |

Fill actual CRM IDs from observation.
Expected destination values:
| Field | Expected value |
| --- | --- |
| Account Name | Marlow Workspace |
| Account Customer Business ID | MER-CUST-007 |
| Contact name | Devon Ellis |
| Contact Business ID | MER-CON-010 |
| Contact Account | Marlow Workspace |
| Source Prospect Reference | MER-LEAD-002 |
| Supplied Email Snapshot | devon.ellis@example.com (mailto:devon.ellis@example.com) |
| Engagement Preference | Request reply only |
| Primary Email | Controlled address inherited from the live laboratory Lead |
| Owner | Ava |

The source Lead remains represented through Converted Leads and the crosswalk. It is not an active unconverted prospect.
9.3 Opportunity register
| Item | Deal 007 |
| --- | --- |
| Name | Northbank replacement printer and installation |
| Account | MER-CUST-001 |
| Contact | MER-CON-001 |
| Enquiry | MER-ENQ-010 |
| Pipeline | Meridian Equipment Sales |
| Final Stage | Meridian Proposal Preparation |
| Amount | GBP 650.00 |
| Probability | 50% |
| Expected Revenue | GBP 325.00 |
| Closing Date | 2026-10-16 |
| Next action | Prepare draft pricing scope |
| Next action due | 2026-10-09 11:00 UTC |
| Owner | Ava |

Both remain Open.
The current stage evidence is PREP-007-01 and NEEDS-008-01.
9.4 Field and quality tests
Missing Closing Date
Expected manual-save behavior is a required-field error.
After supplying 16 October, the valid Northbank record is saved.
Record the actual interface result rather than a presumed screenshot outcome.
Missing next action
Marlow can be technically saved with optional next-action fields blank.
The quality view should expose it.
After repair:
- Same Opportunity Business ID.
- Same actual Deal record ID.
- Next Sales Action populated.
- Next Sales Action Due populated.
- Missing-next-action view no longer includes it.
This demonstrates the difference between record-save acceptance and business readiness.
Permission tests
- Ava can use her permitted conversion/editing actions.
- Noor’s read-only access does not allow conversion or stage editing.
- Leo’s Deal access does not grant editing.
- Mia’s customer-context share does not override absent Deals-module permission.
9.5 Assignment results
| Test | Expected result | Explanation |
| --- | --- | --- |
| AS01 | Ava owns the record | Webform selects the rule and source matches |
| AS02 | Isha owns the record | Rule selected, criterion unmatched, default user applies |
| AS03 | Isha owns the record | Manual creation does not trigger assignment rules |

Actual results and rule/channel evidence are required.
All three temporary Leads are removed after testing. They are not converted or counted as new business prospects.
The main Leads form retains the rule choice for future controlled capture.
9.6 Task reconciliation
At the fixed review point:
| Task | Status in the supplied case | Due date |
| --- | --- | --- |
| 003 | Completed | 2026-10-07 |
| 004 | Completed | 2026-10-07 |
| 005 | Open | 2026-10-07 |
| 006 | Open | 2026-10-07 |
| 007 | Open | 2026-10-09 |
| 008 | Open | 2026-10-13 |

Sales-task cohort:
- Total: 6.
- Completed: 2.
- Open: 4.
- Open and overdue by date: 2.
Completion proportion:
\[
\frac{2}{6}\times 100 \approx 33.3\%
\]
Overdue proportion among open sales tasks:
\[
\frac{2}{4}\times 100 = 50\%
\]
The Northbank Deal’s timed next action is one hour late at noon. Task 007’s date-only due value still means due today.
Do not label both controls identically without explaining the time precision.
Task 001 remains an open inspection task due 15 October and is excluded from this sales-task cohort.
9.7 Stage age and next-action review
Scenario review point:
2026-10-09T12:00:00Z
Northbank current stage entered:
2026-10-07T10:00:00Z
\[
48\text{ hours} + 2\text{ hours} = 50\text{ hours}
\]
Marlow current stage entered:
2026-10-08T10:00:00Z
\[
24\text{ hours} + 2\text{ hours} = 26\text{ hours}
\]
Northbank next action due:
2026-10-09T11:00:00Z
\[
12{:}00 - 11{:}00 = 1\text{ hour late}
\]
Marlow’s action is scheduled after the 12 October closure.
These are scenario calculations. Actual stage-history aging uses actual observed timestamps.
The final management views should show:
| View | Expected base result |
| --- | --- |
| Open equipment opportunities | Two Deals |
| Missing next action, after repair | Zero |
| Fixed due-action snapshot | Deal 007 |
| Equipment Kanban | One Proposal Preparation card; one Needs Confirmed card |

9.8 Pipeline and forecast calculations
Raw open pipeline:
\[
650 + 1800 = 2450\text{ GBP}
\]
Weighted open pipeline:
\[
650(0.50) + 1800(0.25)
=
325 + 450
=
775\text{ GBP}
\]
Combined historical and new Deal Amount:
\[
4750 + 2450 = 7200\text{ GBP}
\]
The GBP 7200 figure is not open pipeline.
Against the illustrative GBP 2000 target:
\[
\text{Raw coverage}
=
\frac{2450}{2000}
=
1.225
\approx 1.23\times
\]
Expressed as a percentage:
\[
1.225 \times 100 = 122.5\%
\]
Weighted coverage:
\[
\frac{775}{2000}
=
0.3875
\approx 0.39\times
\]
Or:
\[
38.75\%
\]
New-pipeline Closed Won achievement:
\[
0\text{ GBP}
\]
Target attainment:
\[
\frac{0}{2000}\times100 = 0\%
\]
Actual gap:
\[
2000 - 0 = 2000\text{ GBP}
\]
Forecast-category reconciliation
Under the specified category mappings:
| Category | Contributing Deal |
| --- | --- |
| Pipeline/Open | 008 |
| Best Case | 007 |
| Committed | None |
| Closed in new forecast scope | None |

These category amounts are not probability-weighted amounts.
The native view should be reconciled using its actual period, filters, categories and synchronization time.
9.9 Final base counts
| Structure | Starting | Change |
| --- | --- | --- |
| Accounts | 6 | +1 |
| Contacts | 6 | +1 |
| Deals | 6 | +2 |
| Enquiries | 5 | 0 |
| Active base Leads | 1 | −1 through conversion |
| Converted base Leads | 0 | +1 |
| Tasks | 5 | +2 |
| Order Packets | 6 | 0 |
| Packet Versions | 8 | 0 |
| Supporting References rows | 10 | 0 |

The source prospect is represented as converted, not treated as an unexplained deletion.
The new opportunities have no order confirmations. The historical Finance baseline therefore remains:
- Four completed orders.
- Two open orders.
- Mean completed elapsed time: 195 minutes.
- Completed first-pass: 50%.
9.10 Management review example
Review: Meridian Equipment Sales  
Scenario point: 9 October 2026, 12:00 UTC  
Operational reviewer: Noor
| Review area | Finding |
| --- | --- |
| Open opportunities | Two, raw Amount GBP 2450 |
| Weighted planning value | GBP 775 |
| Northbank | Proposal Preparation; timed action one hour late |
| Marlow | Needs Confirmed; decision-path follow-up due 13 October |
| Toner enquiry | Model missing; task overdue |
| Redwood enquiry | Delivery postcode missing; task overdue |
| Next-action quality | Both open Deals have action and due time after repair |
| New forecast achievement | GBP 0 |
| Historical reconciliation | Six historical Deals remain distinct |
| Access | Noor reviews; Ava executes permitted changes |

Noor’s review does not itself approve a price or accept an order packet.
9.11 Independent challenge solutions
Challenge A
The mapping stores a prospect identity in customer/contact identity fields.
Correct:
- Customer ID: MER-CUST-007.
- Contact ID: MER-CON-010.
- Source Prospect Reference: MER-LEAD-002.
After mistaken conversion, the source cannot be reverted to an unconverted Lead.
Inspect destination records, dependencies and before-images. Repair incorrect destination identities through controlled edits where appropriate, and preserve the conversion crosswalk. Deleting records does not undo every consequence of conversion.
Challenge B
Correct statement:
Raw open pipeline is GBP 2450, giving 1.225× coverage against the illustrative GBP 2000 target. Weighted open pipeline is GBP 775, or 0.3875× coverage. Achievement in the selected new pipeline is GBP 0, so the actual gap remains GBP 2000.
Coverage is not attainment.
Challenge C
Closed opportunities:
- Two Won.
- One Lost.
Win rate:
\[
\frac{2}{2+1}\times100 \approx 66.7\%
\]
Won proportion of complete cohort:
\[
\frac{2}{5}\times100 = 40\%
\]
Won Amount:
\[
800 + 650 = 1450\text{ GBP}
\]
Target attainment:
\[
\frac{1450}{2000}\times100 = 72.5\%
\]
Actual gap:
\[
2000 - 1450 = 550\text{ GBP}
\]
Weighted open pipeline:
\[
950(0.25) + 500(0.50)
=
237.50 + 250
=
487.50\text{ GBP}
\]
Won sales cycles:
- SIM-01: 6 October − 1 October = 5 elapsed calendar days.
- SIM-04: 12 October − 2 October = 10 elapsed calendar days.
Mean:
\[
\frac{5+10}{2} = 7.5\text{ days}
\]
The lost opportunity and two open opportunities are excluded from the mean won cycle. Their exclusion must be stated.
Challenge D
The spelling correction is system activity, not customer progress.
Inspect the due action, actual discussion and stage evidence. A recent Last Activity Time does not resolve the overdue commitment.
Challenge E
“Not Closed Won” can still include Closed Lost and other stages outside the intended pipeline.
Use:
- The intended pipeline.
- Its defined open stages or a correctly interpreted Open Deal Category filter.
- Explicit criteria grouping.
The chapter’s five-row criterion pattern includes the four named open stages and excludes both terminals.
9.12 Knowledge-check answers
 1. Intake versus qualification: one establishes a handleable request; the other establishes evidence supporting commercial pursuit.
 2. Converted Account: Accounts can represent organisations with which business dealings are planned, not only those that already bought.
 3. Distinct IDs: Leads, Accounts, Contacts and Deals are different entities and need their own business identities.
 4. Existing suggestions: inspect business identity, mapped keys, email use and organisation/person facts before merging.
 5. Separate Deal creation: it makes opportunity identity, pipeline, stage and ownership explicit.
 6. Stage/categories: Stage records position; Deal Category records open/won/lost state; Forecast Category groups planning contribution.
 7. Probability: it is an assumption or estimate, not a completed outcome.
 8. Assignment channels: supported import, webform and API entry; ordinary manual creation does not trigger the rule.
 9. Activity timestamp: administrative edits can make a record look active without advancing the customer discussion.
10. Due precision: Task Due Date is date-based; the custom next-action field contains a specific time.
11. Coverage versus achievement: open opportunities are still uncertain; the new scope has no Closed Won Amount.
12. Freshness: a forecast can lag Deal changes, so reconciliation needs the actual last-synced time.
## 10. Chapter recap and next step

You have moved from captured requests to organised sales work:
- Qualified Marlow using supplied evidence.
- Converted the prospect with distinct destination identities.
- Created two opportunities in a defined pipeline.
- Connected stage evidence, next actions and tasks.
- Tested assignment by entry channel.
- Reconciled raw pipeline, weighted planning values and forecast achievement.
The expected base contains seven Accounts, seven Contacts, eight Deals and one converted prospect.
Next: Chapter 9 — Workflow Automation. You will use the prepared records and follow-up conditions to automate repeatable actions and test their triggers, outcomes and duplicate controls.
## 11. Glossary and further reading

Glossary
| Term | Meaning |
| --- | --- |
| Achievement | Completed sales counted within a defined forecast scope |
| Assignment rule | Supported-channel ownership allocation based on configured criteria |
| Closing Date | Planned sales closure date for an open opportunity |
| Conversion | Movement of a Lead into destination sales records |
| Conversion mapping | Field-transfer definition used during conversion |
| Coverage | Pipeline amount divided by a defined target |
| Deal Category | Open, Closed Won or Closed Lost classification |
| Forecast Category | Planning grouping such as Pipeline, Best Case or Closed |
| Gap | Difference between target and achievement |
| Kanban | Card-based view grouped by a selected field |
| Next action | Specific work intended to advance the opportunity |
| Opportunity | One commercial pursuit represented by a Deal |
| Pipeline | Sales process grouping and its available stages |
| Planning probability | Weight assigned to an opportunity or stage |
| Qualification | Evidence-based decision about commercial pursuit |
| Rollup | Aggregation from lower hierarchy levels |
| Stage evidence | Facts supporting the opportunity’s current position |
| Stage history | Recorded changes in the opportunity stage |
| Target | Desired outcome for a defined population and period |
| Weighted pipeline | Open Amount multiplied by probability |

Official product references
Documentation accessed for this chapter: 5 October 2026. Match procedures to the edition, interface and configuration available in your laboratory.
1. Zoho CRM — Converting Leads (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/leads/articles/convert-leads)  
Individual conversion, existing-record matching, optional Deal creation and field mapping.
2. Zoho CRM — Working With Leads (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/leads/articles/leads-26-4-2026)  
Lead management and Converted Leads views.
3. Zoho CRM — FAQs: Leads Management (https://help.zoho.com/portal/en/kb/crm/faqs/sales-force-automation/lead-management/articles/faqs-on-leads-management)  
Conversion behavior, Accounts, activities and correspondence.
4. Zoho CRM — Creating Deals (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/create-deals)  
Deal creation, stage/category mappings, related information and sales-stage history.
5. Zoho CRM — Multiple Sales Pipeline (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/pipelines/articles/multiple-sales-pipeline)  
Layout-specific pipelines, first-time Standard pipeline creation and stage probabilities.
6. Zoho CRM — FAQs: Deals (https://help.zoho.com/portal/en/kb/crm/faqs/sales-force-automation/deals-management/articles/faqs-deals)  
Expected Revenue and stage-probability mapping.
7. Zoho CRM — Setting Assignment Rules (https://help.zoho.com/portal/en/kb/crm/automate-business-processes/assignment-rules/articles/set-assignment-rules)  
Criteria, ownership, supported channels and default users.
8. Zoho CRM — FAQs: Assignment (https://help.zoho.com/portal/en/kb/crm/faqs/automation/assignment-rules/articles/faqs-assignment)  
Manual-creation exclusions and unmatched/default assignment behavior.
 9. Zoho CRM — Managing List Views (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/managing-module-views/articles/list-view)  
Criteria patterns, sharing, columns and Last Activity Time.
10. Zoho CRM — Creating Kanban Views (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/managing-module-views/articles/kanban-views)  
Stage grouping, aggregation, layout/pipeline selection and drag-and-drop updates.
11. Zoho CRM — Working with Tasks (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/activities/articles/working-with-tasks-and-meetings)  
Task creation, associations and system completion status.
12. Zoho CRM — Creating and working with forecasts (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/forecasts/articles/creating-and-working-with-forecasts)  
Forecast foundation, selected-Deal criteria, hierarchy targets, categories and synchronization.
