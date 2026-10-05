# Data Preparation and Migration

## 1. What you will learn

A successful migration preserves the meaning of records, their relationships and their history.
In this chapter, you will extend Meridian Supply’s CRM reconstruction from two historical orders to the complete six-order baseline. You will work with deliberately untidy source files, prepare import-ready copies, import records in dependency order, investigate a rejected row and reconcile the result.
By the end, you should be able to:
- Profile source data before changing it.
- Distinguish formatting defects, missing information, duplicates and conflicting instructions.
- Map source columns to the correct CRM fields.
- Use business identifiers without confusing them with Zoho record IDs.
- Choose between adding records, updating records and doing both.
- Preserve Account, Contact, Deal, Order Packet and Packet Version relationships.
- Recover a rejected record without recreating successful records.
- Check counts, identifiers, values, relationships, access and historical measurements.
- Explain what import undo can recover and what requires a before-image.
- Prepare a practical backup and recovery record.
Your chapter output: a reconciled six-order historical dataset, supported by a source profile, cleansing log, field map, record crosswalk, import ledger and recovery plan.
All Meridian records and evidence references in this chapter are synthetic training inputs. Expected results are supplied for comparison; actual product results must come from your own laboratory observations.
## 2. Lessons

2.1 Start with a source profile
Data profiling means examining a dataset to understand its shape, quality and meaning before changing it.
Start with questions such as:
- How many rows are present?
- What does one row represent?
- Which fields are required?
- Which identifiers should be unique?
- Which rows refer to records in another file?
- What date, time and currency conventions are used?
- Which values are missing?
- Which records already exist in the destination?
- Do repeated identifiers carry identical or conflicting information?
A file can be technically readable and still be unsuitable for import.
For example, a Contact file might contain valid CSV syntax but associate Morgan Lee with MER-CUST-999, an Account that does not exist in the source or destination. That is a relationship defect, not a CSV defect.
Classify problems before fixing them
| Classification | Meaning | Example |
| --- | --- | --- |
| Formatting defect | Meaning is known, but representation is inconsistent | A trailing space in a business ID |
| Missing required information | A necessary value is absent | Contact Last Name is blank |
| Expected historical absence | A blank accurately describes an earlier event | Billing email missing in a returned packet version |
| Exact duplicate | The same business record or event is repeated without a changed instruction | Two copies of the same confirmation |
| Conflicting instruction | Repeated identity carries a materially different value | Same Contact ID, different unverified email |
| Invalid relationship | A reference cannot be resolved or points to the wrong parent | Contact references the wrong Account ID |
| Destination duplicate | The record already exists in CRM | Northbank Account appears in a new source extract |

Do not treat every blank as something to fill.
The missing billing email in Redwood’s first returned version is evidence of why Finance returned it. Replacing it with the later correction would erase the original failure.
Likewise, Elm’s draft version has no Submitted At value because Sales had not sent it at the observation cutoff. Filling that field would invent an event.
Preserve the original
Keep the source extract unchanged. Make a separate working copy for preparation.
Your source profile should record:
- Source filename and extraction reference.
- Number of data rows, excluding the header.
- Record grain.
- Identifier column.
- Required fields.
- Relationship columns.
- Known formatting conventions.
- Defects and unresolved questions.
- The prepared file produced from the source.
A useful distinction is:
The source is evidence. The prepared file is an instruction to the destination system.
Keep a connection between them.
2.2 Clean according to meaning
Cleansing makes data suitable for its intended use. It should not silently replace uncertain information with convenient guesses.
Identifiers
Meridian’s controlled business-ID format uses uppercase prefixes and fixed identifiers such as MER-CUST-004.
For this training registry:
- Remove leading and trailing spaces.
- Restore the registered uppercase spelling.
- Keep the identifier as text.
- Preserve leading zeroes.
- Do not generate a different ID because a display name changed.
This rule belongs to Meridian’s registry. An identifier supplied by another system could be case-sensitive and require different treatment.
Names
Correct spelling or capitalization only when you have an authoritative value.
CEDAR Office Co  becomes Cedar Office Co in this exercise because the reviewed registry supplies that name. The transformation is supported by evidence, not merely by a preference for title case.
Email addresses
Remove accidental surrounding spaces.
You may normalize the domain’s capitalization: example.COM becomes example.com. Do not assume that changing every character in an address is an appropriate cleansing rule.
An email address is also not a dependable substitute for a person’s identity:
- Two people might use a shared address.
- One person might change addresses.
- A source might contain an outdated address.
Use Meridian’s Contact Business ID for identity and retain email as a contact attribute.
Picklists
Map source vocabulary to the configured vocabulary.
For example:
| Source value | Reviewed destination value |
| --- | --- |
| WON | Closed Won |
| yes | Yes |
| No | No |

Do not import a new spelling simply because the importer accepts it. An unexpected picklist value can make filters and reports incomplete.
Dates and times
Keep two concepts separate:
1. The business event time, such as when a confirmation arrived.
2. The system record time, such as when today’s import created the CRM record.
This chapter uses UTC business events. For the prepared files, use:
- Date: 2026-09-14
- Date/Time: 2026-09-14 10:30:00
Select the corresponding format in the importer. Confirm that the organisation and importing user retain the Chapter 3 UTC settings, then inspect an imported timestamp.
Do not expect the module importer to backdate Created Time. The current new-import documentation lists Created Time, Modified Time, Created By and Modified By among unsupported fields. Historical events belong in Meridian’s explicit business Date/Time fields.
Numbers and currency
Meridian’s home currency remains GBP.
A source value such as £700.00 becomes the numeric value 700.00 for the Amount field. This removes a display symbol; it does not perform a currency conversion.
Keep decimal precision. Do not turn 700.00 into 70.00 or interpret a comma using an unverified regional convention.
Blank values during updates
A blank can mean:
- Unknown.
- Not applicable.
- Not yet occurred.
- Intentionally absent in a historical snapshot.
- An instruction to clear an existing value.
Those meanings are different.
For update imports, Zoho provides an option to skip updating empty values. When selected, a blank in the file retains the existing destination value. When not selected, a mapped blank can clear it.
Choose deliberately. Also remember that a nonblank wrong value is not protected by this option.
2.3 Choose the import operation before mapping
The documented module importer supports three operations.
| Operation | What it does | Appropriate use |
| --- | --- | --- |
| Add as new records | Creates new records; matching existing records can be skipped | A reviewed new-record batch |
| Update existing records only | Changes matching existing records; creates no new records | A controlled correction or enrichment |
| Both | Adds unmatched records and updates matched records | A deliberately approved mixed batch |

For the main Meridian exercise, choose Add as new records.
The four missing historical orders are new to the chapter’s base CRM reconstruction. Northbank and Redwood already exist, so their repeated source rows are withheld during preparation.
Choose a matching field that expresses identity
The relevant business keys are:
| Module | Meridian matching field |
| --- | --- |
| Accounts | Customer Business ID |
| Contacts | Contact Business ID |
| Deals | Opportunity Business ID |
| Order Packets | Order Business ID |
| Packet Versions | Version Business ID |

Verify the Chapter 4 required/unique configuration and that the intended matching field is available in your importer.
A display name is less dependable. A customer can be renamed while retaining the same Customer Business ID.
For an update to records exported from the same CRM organisation, the actual Zoho record ID is also a strong matching option. Preserve it exactly.
Repeatability needs a defined operation
Suppose a four-Account Add batch succeeds. You then submit the identical file again with the same business-ID matching policy.
The expected second result is:
- Added: 0.
- Updated: 0.
- Skipped: 4.
- Account count: unchanged.
That is useful repeatability.
Choosing Both would have different consequences: matching records could be updated. A repeatable migration is therefore more than a clean filename; it is a defined combination of keys, operation, mappings and effects.
2.4 Preserve relationships through identifiers and order
A lookup is a relationship to another record. A text snapshot is a stored value.
These are not interchangeable.
For Packet Versions:
- Order Packet is a lookup.
- Customer ID Snapshot is text.
- Quote Business ID Snapshot is text.
- Confirmation Reference Snapshot is text.
Putting MER-ORD-004 into an unrelated text field does not associate a version with Cedar’s parent packet.
Business IDs and Zoho IDs
| Identifier | Purpose |
| --- | --- |
| MER-CUST-004 | Meridian’s business identity for Cedar |
| An actual Zoho Account record ID | Identity of Cedar’s record in a particular CRM organisation |
| C02 | Source-row reference in the cleansing log |

Maintain a crosswalk connecting business IDs to observed Zoho record IDs.
Never invent Zoho IDs. Never assume a record ID from another organisation identifies the corresponding record in this organisation.
The new importer documents lookup association using supported identifiers including record ID and unique-field value. At field mapping, select both:
1. The destination lookup field.
2. The field in the parent module used to find the referenced record.
If CustomerKey contains MER-CUST-004, select Customer Business ID as the association field. Do not select Record ID for that column.
The classic importer’s lookup instructions emphasize record names or record IDs. Where your interface does not offer the intended unique-field association, replace the lookup column’s business keys with actual destination record IDs from the checked crosswalk and select record-ID association.
Keep one identifier type throughout each lookup column.
Import parents first
Use this dependency order:
1. Accounts.
2. Contacts, linked to Accounts.
3. Deals, linked to Accounts and Contacts.
4. Order Packets, linked to Accounts and Deals.
5. Packet Versions, linked to Order Packets.
6. Supporting References.
7. Accepted Version selections and final packet state.
Check each parent batch before starting its children.
Resolve the accepted-version cycle
An Order Packet points to its Accepted Version. A Packet Version points back to its Order Packet.
You cannot select a destination version that does not exist yet.
For this exercise:
- Create the new Order Packets in Draft with Internal draft access scope.
- Import the versions against those parents.
- Resolve the rejected version.
- Add the evidence rows.
- Select the appropriate Accepted Version.
- Reconcile the record set.
- Apply the historical final status and access scope.
This is controlled staging. The source’s intended historical status remains in the release worksheet throughout preparation.
2.5 Configure the actual import carefully
Official documentation currently distinguishes a new importer and a classic importer. Identify which interface your organisation presents.
Both require appropriate import permission. Custom modules, subforms and other inherited course features also depend on your CRM entitlement.
Allocate migration authority
Chapter 5 gave ordinary Meridian profiles no Import or Export permission.
For this exercise:
| Participant | Migration responsibility |
| --- | --- |
| Isha | Executes imports, exports, historical reconstruction and technical recovery using the Administrator profile |
| Ava | Prepares source copies and owns the reconstructed business records |
| Leo | Checks Finance history and the final permitted Finance view |
| Noor | Reviews reconciliation and unresolved source exceptions |
| Mia | Checks the restricted Service view |

Isha can populate the historical review fields that are read-only for Sales. Ava’s ordinary profile is not an appropriate importer for this complete reconstruction.
To inspect a profile’s permissions, use Setup → Security Control → Profiles, open the profile and examine:
- Module-level View/Create/Edit permissions.
- Import/Export permissions.
- Field permissions.
- Data Administration permissions, including Import History where applicable.
The profile documentation states that Import Records is configured per organisation module and depends on Create permission. Permission changes apply immediately.
New-importer procedure
For each prepared main-module file:
 1. Open the destination module.
 2. Near Create Record, open the dropdown and select Import Records.
 3. Upload the CSV.
 4. Check the character set. The chapter’s files use UTF-8.
 5. Select Next.
 6. Choose the Standard layout where the interface offers layout selection.
 7. Choose Add as new Records.
 8. Select the intended unique matching field.
 9. Map the file to the main module if a file-to-module page appears.
10. Map each required column to its reviewed destination field.
11. Configure lookup association explicitly.
12. Select the Date, Date/Time and numeric formats offered for the mapped fields.
13. Assign the record owner to Ava’s actual active laboratory user account.
14. Apply the chapter’s staging defaults.
15. Inspect the complete mapping, including unmapped columns.
16. Continue to post-import actions.
17. Submit and wait for completion.
18. Refresh the module and inspect the results.
The documented default-value facility can assign a single field value to a batch. Use the actual Ava user selected in CRM; MER-USR-002 is a business reference, not a Zoho user ID.
If you map an owner column instead, use the actual supported user identifier. The troubleshooting guide explains that unrecognized names or inactive owners can cause records to be assigned to the importer.
Classic-importer procedure
The classic guide starts from the module’s Create dropdown and similarly provides:
- File upload and character encoding.
- Layout selection where applicable.
- Add, Update or Both.
- Existing-record matching.
- Field mapping and format selection.
- Default values.
- Post-import options.
- Finish.
The classic and new tools have different supported-module lists and limits. Use the documentation for the interface you are actually using; the chapter’s small files do not justify assuming that both tools have identical capabilities.
Post-import actions for this reconstruction
Configure the historical batch as follows:
| Option | Chapter choice |
| --- | --- |
| Assignment rules | Not selected; owner is deliberately assigned to Ava |
| Manual record approval | Not selected |
| Trigger automation/process management | Not selected |
| Assign follow-up tasks | Not selected |
| Business-record email actions | None required |

Manual import approval is a product queue. It is not Meridian’s Finance acceptance process.
Also, an unchecked automation option is not proof that every possible effect is suppressed. The classic guide explicitly notes that date-based workflows can still run. Inspect the laboratory for active date workflows and connected applications before importing historical dates.
Import acceptance is not full business validation
Zoho’s validation-rule documentation explains that updates through channels including imports can take precedence over criteria-based validation rules.
Therefore:
- A successful manual Save test from Chapter 4 does not establish import enforcement.
- A row imported successfully is not automatically business-correct.
- Required fields, types and matching controls do not establish every cross-record condition.
Check the complete source and destination invariants yourself.
2.6 Investigate rejected records with a ledger
After completion, navigate to:
Setup → Data Administration → Import → Import History
Open the job. In the new interface, you may first select View Imported Modules, then the module.
Inspect:
- Added.
- Updated.
- Skipped.
- Error or warning details.
- Source row numbers.
- Importing user.
- File and execution time.
Download the skipped-record/error list when available.
Row-level detail has a limited availability window. Capture it in the same working session rather than relying on a later visit.
Do not equate “skipped” with one cause
Skipped records can include:
- Existing-record matches deliberately not added.
- Missing mandatory values.
- Invalid formats.
- Relationship errors.
- Other reported import failures.
Separate these reasons in your ledger.
For a completed main-module job:
\[
\text{Submitted rows}
=
\text{Added}
+
\text{Updated}
+
\text{Skipped}
\]
Verify the categories shown by your actual tool. A file blocked before submission is a preflight failure, not a completed import containing skipped records.
Retry only the unresolved instruction
Suppose four version rows import and one fails.
Correct the failed row, retain its business ID and submit a one-row repair file using Add as new with the same matching policy.
Do not infer success from a notification alone. Confirm that the repaired version exists once, belongs to the intended packet and has the expected fields.
2.7 Reconcile in layers
Reconciliation compares what should exist with what actually exists and explains differences.
Use several controls.
| Control | Question |
| --- | --- |
| Source disposition | Is every source row accounted for? |
| Import accounting | Do job totals balance? |
| Record count | Did each intended record appear exactly once? |
| Identity | Are the correct business IDs present? |
| Relationship | Does each child point to the correct parent? |
| Value | Are important values preserved? |
| Historical state | Are return, submission and acceptance events represented correctly? |
| Access | Can the intended users see and act on the result? |
| Measurement | Does the reconstructed history reproduce the original baseline? |

Counts alone are weak evidence.
Six Contacts could exist, but one could belong to the wrong Account. Six Deals could exist, but an Amount could be wrong. A packet could say Accepted while selecting a version belonging to another order.
Use control totals appropriately
For opportunity amounts:
\[
\text{Expected final opportunity total}
=
\text{Existing opportunity total}
+
\text{Eligible new opportunity total}
\]
This is a CRM opportunity control. It is not invoiced revenue, payment collection or a Books reconciliation.
For each accepted packet, also check:
- Selected version belongs to that packet.
- Version outcome is Accepted.
- Accepted At is present.
- Accepted At is not earlier than Submitted At.
- Submitted At is not earlier than confirmation receipt.
- Historical reviewer reference is present.
- Required billing snapshot and evidence are present.
A returned earlier version can legitimately preserve a missing billing email.
Reconcile using a suitable view
A user may see fewer records because of permissions, ownership, sharing or a filtered list.
Isha’s administrator reconciliation and Leo’s Finance-view test answer different questions:
- Isha checks whether the complete reconstruction exists.
- Leo checks whether Finance sees precisely its permitted subset.
Keep both results.
2.8 Plan backup and recovery before submitting
A before-image is a retained copy of relevant values before a change.
An import history entry is not a before-image for every field.
Export affected modules
The current export documentation gives this procedure:
1. Open Setup → Data Administration → Export.
2. Select Start an Export.
3. Choose the module or subform.
4. Select the appropriate custom view or criteria.
5. Choose all required fields, including Record ID and relationship fields.
6. Select CSV and the appropriate character set.
7. Start the export.
8. Wait for Completed status.
9. Download and inspect the archive.
You can also start an export from the module’s Actions menu.
For this exercise, preserve the base records in the five affected main modules and the Supporting References subform. Preserve Enquiries and Tasks for the unchanged-record check.
Keep:
- Record IDs.
- Business IDs.
- Lookup references.
- Historical snapshots.
- Event timestamps.
- Status and access-scope fields.
- Accepted Version selections.
- Subform parent identifiers.
Record configuration separately where necessary: roles, profiles, sharing rules, field properties and validation settings. Do not assume a module CSV can recreate configuration.
Native data backup
An administrator can use:
Setup → Data Administration → Data Backup
The official guide documents immediate and scheduled backup options. Where the feature is available within the laboratory’s entitlement:
1. Select the immediate-download option.
2. Confirm the displayed request.
3. Wait until the backup is ready.
4. Download the offered data and attachment archives.
5. Inspect their contents and retain the original identifiers.
Availability and charging depend on the account. If you use module exports for this small exercise, describe them accurately as module/subform before-images, not as a completed native full backup.
The backup guide identifies exclusions including email content and attachments, Documents, and data obtained through integration. A CRM backup is not a backup of the separate Books, Desk or People applications.
Choose recovery according to the change
| Problem | Suitable recovery approach |
| --- | --- |
| A row was rejected and never created | Correct and retry that row |
| New records were added incorrectly | Inspect the affected batch and relationships; use available added-record recovery carefully |
| Existing fields were overwritten | Restore from before-images using a narrow update |
| Related records were deleted | Investigate related-record recovery, recycle-bin availability and backup/migration requirements |
| An external message or transaction occurred | Handle that effect in the receiving application; CRM undo is insufficient |

Import undo removes added records; it does not reverse updates to existing records.
The official import-history guidance also warns about associated Accounts and Contacts when undoing/deleting imported data. Inspect the affected relationship set before using undo.
The help pages describe limited undo/detail windows, with some differences between importer documentation. Use the action actually available for the job and capture evidence immediately.
Supporting References at larger scale
The new importer supports dependent-module files, including subforms, alongside a main-module file. The dependent file needs a parent-identification column mapped against a unique column in the parent file.
The classic guide documents Import Subforms with a required parent identifier.
For this chapter’s six new evidence rows, use the small, explicit manual-entry procedure in Section 5. At larger scale, use the documented subform facility for your interface and reconcile subform rows separately from parent records.
A parent-record count does not tell you how many evidence rows were preserved.
## 3. Visual explanation

flowchart TD
    A[Retain original extracts] --> B[Profile source rows]
    B --> C[Classify defects and duplicates]
    C --> D[Prepare reviewed import copies]
    D --> E[Capture before-images]
    E --> F[Import Accounts]
    F --> G[Import Contacts]
    G --> H[Import Deals]
    H --> I[Create staged Order Packets]
    I --> J[Import Packet Versions]
    J --> K{Unresolved rows?}
    K -->|Yes| L[Read errors and prepare narrow repair]
    L --> J
    K -->|No| M[Add supporting evidence]
    M --> N[Select accepted versions]
    N --> O[Reconcile IDs, links, values and history]
    O --> P[Apply final historical status and scope]
    P --> Q[Test permitted and denied access]
    Q --> R[Retain evidence and recovery package]
The sequence follows dependencies.
Accounts exist before Contacts and Deals refer to them. Order Packets exist before their versions. Accepted Version selection comes after the selected version exists.
The repair loop returns only unresolved instructions to import. It does not restart the entire migration automatically.
Reconciliation checks business meaning as well as import totals. Final Finance visibility is applied after the reconstructed packets and versions have been checked.
## 4. Worked case

Northbank appears in another extract
Northbank already exists:
| Item | Existing value |
| --- | --- |
| Customer Business ID | MER-CUST-001 |
| Account Name | Northbank Studio |
| Confirmed order | MER-ORD-001 |
| Accepted version | MER-PVER-001-01 |
| Confirmation received | 2026-09-14T09:00:00Z |
| Finance accepted | 2026-09-14T10:00:00Z |

A new source extract contains:
SourceRow,CustomerBusinessID,AccountName
A06,MER-CUST-001,Northbank Studio
There is no changed customer instruction.
Decision
Classify A06 as an existing destination record. Link the source row to the existing Account and withhold it from the new-Account batch.
If it were submitted using Add as new and Customer Business ID matching, the expected result would be a skip, not another Northbank Account.
Why not use Both automatically?
Both permits updates to matching records.
If a later source file included stale mapped values, it could overwrite existing information. The fact that one row is harmless does not make a mixed add/update policy suitable for every source extract.
Preserve Northbank’s historical measurement
The confirmation-to-acceptance elapsed time is:
\[
10{:}00 - 09{:}00 = 60\text{ minutes}
\]
Today’s import date must not replace either business timestamp.
A record created today can still describe a confirmation accepted on 14 September 2026. The reporting field determines which event you are measuring.
Cedar needs two versions
Cedar’s historical order is MER-ORD-004.
Its first submission lacked billing email. The later correction used:
- cedar.billing@example.com
- Evidence reference BILL-004
A faithful reconstruction requires two versions:
| Version | Meaning |
| --- | --- |
| MER-PVER-004-01 | Returned first submission; missing billing email remains blank |
| MER-PVER-004-02 | Corrected submission accepted by Finance |

Do not overwrite version 1 with version 2’s email.
The parent packet eventually selects version 2 as Accepted Version. Version 1 remains part of the evidence explaining first-pass failure.
A useful recovery distinction
Suppose version 2 is rejected because Version Name is blank.
No version 2 exists yet. Its recovery is a corrected one-row Add import.
That is different from recovering an existing version whose billing email was overwritten. The latter requires a before-image and a controlled update.
## 5. Try it yourself — guided practice

5.1 Establish your starting point
Use the cleaned Chapter 5 base reconstruction.
| Module or structure | Expected starting count |
| --- | --- |
| Accounts | 2 |
| Contacts | 2 |
| Deals | 2 |
| Enquiries | 1 |
| Order Packets | 2 |
| Packet Versions | 3 |
| Tasks | 1 |
| Leads | 0 |
| Supporting References rows | 4 |

Northbank and Redwood are the existing customers. Their orders and versions remain historical reconstruction fixtures.
If you completed an optional earlier challenge, identify those records separately. Use the stated base subset for this exercise’s comparison rather than treating additional challenge records as migration errors.
Remove any remaining Chapter 5 temporary LAB records using that chapter’s cleanup instructions before recording the starting counts.
5.2 Use these reviewed authority notes
AUTH-MIG-06 is the synthetic reviewed registry for this exercise.
| Question | Authoritative training value |
| --- | --- |
| Customer 003 display name | Harbor Works |
| Customer 004 display name | Cedar Office Co |
| Customer 005 display name | Oak Services |
| Customer 006 display name | Elm Design |
| Contact 007 full name | Sam Reed |
| Contact 008 customer | MER-CUST-005 |
| Contact 009 email | riley.stone@example.com |
| Contact 007 approved email | sam.reed@example.com |
| Different email in C06 | Unverified; hold the proposed change |
| Source WON | Configured Deal stage Closed Won |
| Blank V03 Version Name | Correct name is Cedar packet v2 |
| Source event-time convention | All supplied business times are UTC |
| Cedar corrected resubmission | 2026-09-14T16:00:00Z |
| Cedar first-return evidence | RETURN-004 |
| New Deal Amounts | GBP opportunity estimates, not invoice amounts |

The new customer labels, contacts, opportunity estimates and Cedar resubmission detail are additional synthetic migration inputs. The original six-order confirmation, acceptance and cutoff measurements remain the same.
Contact identifiers 006–009 are used so that optional earlier challenge identifiers remain separate.
5.3 Profile the raw source files
Retain these extracts unchanged. SourceRow supports lineage in your worksheet; it is not a Zoho record ID.
Accounts source
SourceRow,CustomerBusinessID,AccountName
A01,MER-CUST-003,Harbor Works
A02," mer-cust-004 ","CEDAR Office Co "
A03,MER-CUST-005,Oak Services
A04,MER-CUST-006,Elm Design
A05,MER-CUST-004,Cedar Office Co
A06,MER-CUST-001,Northbank Studio
Contacts source
SourceRow,ContactBusinessID,FirstName,LastName,Email,CustomerBusinessID
C01,MER-CON-006,Jordan,Vale,jordan.vale@example.com,MER-CUST-003
C02,MER-CON-007,Sam,,sam.reed@example.com,MER-CUST-004
C03,MER-CON-008,Morgan,Lee,morgan.lee@example.com,MER-CUST-999
C04,MER-CON-009,Riley,Stone,riley.stone@example.COM,MER-CUST-006
C05," MER-CON-006 ",Jordan,Vale,"jordan.vale@example.com ",MER-CUST-003
C06,MER-CON-007,Sam,Reed,sam.changed@example.com,MER-CUST-004
Deals source
SourceRow,OpportunityBusinessID,DealName,CustomerBusinessID,ContactBusinessID,ClosingDate,Stage,Amount
D01,MER-DEAL-003,Harbor historical opportunity,MER-CUST-003,MER-CON-006,2026-09-14,Closed Won,600.00
D02,MER-DEAL-004,Cedar historical opportunity,MER-CUST-004,MER-CON-007,2026-09-14,WON,950.00
D03,MER-DEAL-005,Oak historical opportunity,MER-CUST-005,MER-CON-008,2026-09-14,Closed Won,£700.00
D04,MER-DEAL-006,Elm historical opportunity,MER-CUST-006,MER-CON-009,14/09/2026,Closed Won,500.00
D05,MER-DEAL-002,Redwood — office equipment,MER-CUST-002,MER-CON-002,2026-09-14,Closed Won,800.00
Order Packets source
SourceRow,PacketName,OrderBusinessID,CustomerBusinessID,OpportunityBusinessID,ConfirmationReceivedAt,DesiredPacketStatus,ConfirmationReference
P01,Harbor packet,MER-ORD-003,MER-CUST-003,MER-DEAL-003,2026-09-14T10:00:00Z,Accepted,CONF-003
P02,Cedar packet,MER-ORD-004,MER-CUST-004,MER-DEAL-004,14/09/2026 10:30 UTC,Accepted,CONF-004
P03,Oak packet,MER-ORD-005,MER-CUST-005,MER-DEAL-005,2026-09-14T13:00:00Z,Awaiting Finance review,CONF-005
P04,Elm packet,MER-ORD-006,MER-CUST-006,MER-DEAL-006,2026-09-14T14:00:00Z,Draft,CONF-006
P05,Harbor packet,MER-ORD-003,MER-CUST-003,MER-DEAL-003,2026-09-14T10:00:00Z,Accepted,CONF-003
Packet Versions source
SourceRow,VersionName,VersionBusinessID,OrderBusinessID,RevisionNumber,CustomerIDSnapshot,QuoteIDSnapshot,ConfirmationReferenceSnapshot,InstallationSnapshot,BillingEmailSnapshot,BillingEvidenceReference,SubmittedAt,ReviewOutcome,ReturnReason,AcceptedAt,ReviewerReference
V01,Harbor packet v1,MER-PVER-003-01,MER-ORD-003,1,MER-CUST-003,MER-QUOTE-003,CONF-003,yes,harbor.billing@example.com,CONF-003,14/09/2026 10:30 UTC,Accepted,,2026-09-14T11:00:00Z,MER-USR-003
V02,Cedar packet v1,MER-PVER-004-01,MER-ORD-004,1,MER-CUST-004,MER-QUOTE-004,CONF-004,No,,,2026-09-14T12:00:00Z,Returned,Billing email missing,,MER-USR-003
V03,,MER-PVER-004-02,MER-ORD-004,2,MER-CUST-004,MER-QUOTE-004,CONF-004,No,cedar.billing@example.com,BILL-004,2026-09-14T16:00:00Z,Accepted,,2026-09-14T16:30:00Z,MER-USR-003
V04,Oak packet v1,MER-PVER-005-01,MER-ORD-005,1,MER-CUST-005,MER-QUOTE-005,CONF-005,Yes,oak.billing@example.com,CONF-005,14/09/2026 14:00 UTC,Submitted,,,
V05,Elm packet v1,MER-PVER-006-01,MER-ORD-006,1,MER-CUST-006,MER-QUOTE-006,CONF-006,No,elm.billing@example.com,CONF-006,,Draft,,,
V06,Harbor packet v1,MER-PVER-003-01,MER-ORD-003,1,MER-CUST-003,MER-QUOTE-003,CONF-003,Yes,harbor.billing@example.com,CONF-003,2026-09-14T10:30:00Z,Accepted,,2026-09-14T11:00:00Z,MER-USR-003
5.4 Prepare the source profile and cleansing log
For each file:
1. Count its data rows.
2. Identify its record grain and business key.
3. Find repeated identifiers.
4. Classify blanks.
5. Find unresolved or wrong relationships.
6. Identify required transformations.
7. Assign every row a disposition.
Use this worksheet:
| Source file | Raw rows | Grain | Key | Eligible records |
| --- | --- | --- | --- | --- |
| Accounts |  |  |  |  |
| Contacts |  |  |  |  |
| Deals |  |  |  |  |
| Order Packets |  |  |  |  |
| Packet Versions |  |  |  |  |

Use these cleansing-log columns:
SourceFile,SourceRow,BusinessID,Issue,Disposition,PreparedValue,EvidenceReference,DestinationRecordID
Controlled rejection exercise: retain V03’s blank Version Name in the first version-import file. Correct the other known defects and withhold duplicates/conflicting instructions before importing.
This one deliberate defect lets you observe mandatory-field rejection and perform a narrow repair. Do not replace it with a default name during first-pass mapping.
5.5 Capture before-images and prepare the field map
Record the actual starting counts and export the affected base records using Lesson 2.8.
Inspect the downloads. Confirm that the historical returned versions still contain their original blanks and that accepted-version selections are retained.
Create your field map using this structure:
| Prepared column | Destination module/field | Type |
| --- | --- | --- |
|  |  |  |

Your mapping must explicitly distinguish:
- Matching business-ID fields.
- Parent lookup fields.
- Text snapshot fields.
- Business Date/Time fields.
- Staging defaults.
- Source-only columns retained in the ledger.
Do not map DesiredPacketStatus directly into the first packet import. Retain it for final release.
Create a record crosswalk:
Module,BusinessID,ZohoRecordID,VerificationResult
Fill actual record IDs after observation. Use the Chapter 4 crosswalk and fresh exports where appropriate.
5.6 Test the normal permission boundary
Using Ava’s ordinary Sales account:
1. Open Accounts.
2. Inspect the Create dropdown.
3. Record whether Import is unavailable.
4. Repeat in Packet Versions.
Then use Isha’s administrator account for the imports.
Do not record a successful denied-action test merely because a permission matrix says Import is off. Record the observed interface result. Do not assume the audit log contains a denied click.
5.7 Import in dependency order
Prepare and import:
1. Accounts.
2. Contacts.
3. Deals.
4. Staged Order Packets.
5. First-pass Packet Versions.
For the new Order Packets, explicitly use:
- Owner: Ava’s actual active CRM user.
- Packet Status: Draft.
- Access Scope: Internal draft.
- Accepted Version: not yet selected.
For new Packet Versions, use:
- Owner: Ava.
- Access Scope: Internal draft.
- Historical Review Outcome and event fields from the prepared file.
After each job:
- Save its result details.
- Balance submitted rows against the displayed result categories.
- Inspect the business IDs.
- Check the parent relationships.
- Add the observed record IDs to the crosswalk.
Use this import-ledger structure:
BatchReference,Filename,Module,Operation,MatchingField,SubmittedRows,Added,Updated,Skipped,ObservedReason,EvidenceReference
5.8 Investigate and repair V03
For the first version import:
1. Open Import History.
2. Locate the Packet Versions job.
3. Open the skipped-record detail.
4. Capture the actual reason.
5. Locate source V03.
6. Prepare a one-row repair with Version Name Cedar packet v2.
7. Keep business ID MER-PVER-004-02.
8. Import it using Add as new and Version Business ID matching.
9. Confirm one corrected version exists under MER-ORD-004.
If the interface blocks the file before submission, record that as a preflight rejection. Correct the row and use the actual subsequent submission counts. Do not invent a completed skipped-record result.
5.9 Add six Supporting References
After all five new versions exist, use these evidence rows:
ParentVersionBusinessID,EvidenceReference,EvidenceKind,EvidenceNote
MER-PVER-003-01,CONF-003,Customer confirmation,Confirmation includes the supplied billing email
MER-PVER-004-01,RETURN-004,Finance return,Billing email missing in the first submission
MER-PVER-004-02,CONF-004,Customer confirmation,Original confirmation reference retained
MER-PVER-004-02,BILL-004,Billing correction,Corrected billing email supplied
MER-PVER-005-01,CONF-005,Customer confirmation,Submitted packet awaiting Finance review
MER-PVER-006-01,CONF-006,Customer confirmation,Confirmation received but packet not submitted
For this small batch:
1. Open the version identified by ParentVersionBusinessID.
2. Verify its Order Packet.
3. Select Edit.
4. Add the supplied row or rows to Supporting References.
5. Use the exact configured Evidence Kind value.
6. Save.
7. Reopen and verify the rows.
The subform training maximum is five rows per version. No version here exceeds two new rows.
The four existing evidence rows remain part of the base reconstruction.
5.10 Reconcile and release the historical states
Prepare the final-state worksheet.
Determine:
- Which packets need Accepted Version selections.
- Which new versions should be Finance review.
- Which packet and version remain Internal draft.
- Which original missing values must remain blank.
Select the accepted versions while the new packets are still staged. Reconcile identifiers, links, values and event chronology.
Then apply the historical final packet status and scope from the reviewed source.
Isha is reconstructing supplied history. Typed Reviewer Reference: MER-USR-003 is not evidence that Leo performed a new authenticated acceptance action during this migration.
5.11 Test access and repeated import
Check:
- Ava’s ownership of the new records.
- Leo’s permitted Finance records.
- Leo’s lack of access to Elm’s Internal draft packet/version.
- Mia’s existing Northbank-only Service context.
- Noor’s read-only hierarchical view.
Use Chapter 5’s sharing execution/recalculation procedure where required, then test the actual user views.
Finally, resubmit the same prepared four-Account file using Add as new and Customer Business ID matching.
Record the result and confirm that the Account count did not increase.
5.12 Complete the historical reconciliation
Use this fixed observation boundary:
14 September 2026, 17:00 UTC
| Order | Confirmation received | First submission | Finance accepted |
| --- | --- | --- | --- |
| MER-ORD-001 | 09:00 | 09:30 | 10:00 |
| MER-ORD-002 | 09:15 | 10:15 | 14:15 |
| MER-ORD-003 | 10:00 | 10:30 | 11:00 |
| MER-ORD-004 | 10:30 | 12:00 | 16:30 |
| MER-ORD-005 | 13:00 | 14:00 | Not accepted |
| MER-ORD-006 | 14:00 | Not submitted | Not accepted |

Calculate:
1. Completed-order elapsed minutes.
2. Mean completed-order elapsed time.
3. Completed first-pass percentage.
4. Accepted proportion of the six-order set.
5. Age of each open order at the fixed cutoff.
6. New and final opportunity Amount totals.
7. Final counts for the base modules and subform.
Use these artifact names:
- C01_CH06_Meridian_Source_Profile.md
- C01_CH06_Meridian_Cleansing_Log.csv
- C01_CH06_Meridian_Field_Map.md
- C01_CH06_Meridian_Migration_Crosswalk.csv
- C01_CH06_Meridian_Import_Ledger.csv
- C01_CH06_Meridian_Reconciliation.md
- C01_CH06_Meridian_Backup_and_Recovery.md
## 6. Independent challenge

Challenge A — Counts match, but values do not
After the main exercise, a proposed update-only enrichment file accidentally changes Oak’s Deal Amount.
The following observations are supplied for analysis:
| Item | Value |
| --- | --- |
| Deal count before update | 6 |
| Deal count after update | 6 |
| Intended Oak Amount | GBP 700.00 |
| Imported Oak Amount | GBP 70.00 |
| Correct six-Deal total | GBP 4750.00 |
| Observed six-Deal total | GBP 4120.00 |
| Import result | 1 updated; 0 added; 0 skipped |
| Before-image | Contains Oak’s actual CRM record ID and Amount 700.00 |

Answer:
1. Why does the count check pass?
2. What control reveals the defect?
3. What is the monetary difference?
4. Can Undo Import restore the Amount?
5. What should the narrow repair file contain?
6. Which fields should remain outside its mapping?
7. What must be checked after recovery?
Analyze the scenario without changing the main project’s historical records.
Challenge B — A renamed Account is resubmitted
A source row contains:
CustomerBusinessID,AccountName
MER-CUST-004,Cedar Workplace Services
The existing CRM Account is:
- Customer Business ID: MER-CUST-004
- Account Name: Cedar Office Co
No approved rename instruction is supplied.
Explain the expected behavior under:
1. Add as new with Customer Business ID matching.
2. Both with Customer Business ID matching and Account Name mapped.
3. Matching only on Account Name.
Recommend a preparation decision.
Challenge C — A summary is not row evidence
A migration note says:
“All 21 prepared records imported successfully.”
The actual first-pass job totals are:
- 20 added.
- 0 updated.
- 1 skipped.
The author has not opened the skipped-record detail.
Write a corrected status statement and list the evidence needed to close the migration.
## 7. Common problems and recovery

| Problem | Likely explanation |
| --- | --- |
| Import is missing from the menu | Import permission is absent for that profile/module, or access prerequisites are unmet |
| A business ID is treated as a Zoho record ID | Wrong lookup association type |
| Contact imports but has the wrong Account | Source reference or mapping is wrong |
| Records belong to Isha instead of Ava | Owner was omitted, unrecognized or inactive |
| First version’s missing billing email is “cleaned” | Historical absence was mistaken for a defect |
| A version has no accepted parent selection | Accepted Version was deferred but never completed |
| Imported timestamps shift | Source format or importing-user time convention was not verified |
| A repeated file adds another record | Matching key was not selected or configured as intended |
| Skipped records are called failures indiscriminately | Deliberate duplicate skips and true errors were combined |
| A file fails before submission | Preflight validation blocked it |
| Finance cannot see all reconstructed orders | One order is intentionally Internal draft, or sharing/ownership is wrong |
| Finance sees Elm’s draft | An overlapping sharing or ownership route grants access |
| Business automations run despite an unchecked option | A date workflow or other active route still applies |
| Undo is unavailable for an update | Updates are not reversible through import undo |
| Undo could affect related records | The batch includes linked Accounts/Contacts or dependent records |
| Subform row count is wrong | Parent association failed, rows were repeated or evidence was omitted |
| Opportunity total is correct but individual values are wrong | Two errors may cancel each other |

## 8. Check your understanding

 1. Why should the original source extract remain unchanged?
 2. What distinguishes a duplicate from a conflicting instruction?
 3. Why is a blank billing email correct in a returned historical version?
 4. What is the difference between a business ID and a Zoho record ID?
 5. Why do Accounts need to precede Contacts in this exercise?
 6. Why is Accepted Version selection deferred?
 7. What can import undo recover, and what can it not reverse?
 8. Why can a successful import still contain business-invalid data?
 9. What does “skip updating empty values” protect against?
10. Why is a six-record count insufficient evidence of correct migration?
11. Which time fields reproduce the historical baseline?
12. Why are the migrated historical orders not automatically new pilot observations?
## 9. Solutions and explanations

9.1 Source profile and row disposition
| Source | Raw rows | Eligible records | Withheld rows | Explanation |
| --- | --- | --- | --- | --- |
| Accounts | 6 | 4 | 2 | One source duplicate; one existing Account |
| Contacts | 6 | 4 | 2 | One source duplicate; one unverified conflicting email instruction |
| Deals | 5 | 4 | 1 | Redwood Deal already exists |
| Order Packets | 5 | 4 | 1 | Repeated Harbor confirmation |
| Packet Versions | 6 | 5 | 1 | Repeated Harbor version |
| Total | 28 | 21 | 7 | Every source row is accounted for |

The seven withheld rows comprise:
- Six duplicate/existing-record rows.
- One conflicting instruction held for evidence.
The five eligible versions include V03, which deliberately retains a missing mandatory name for first-pass rejection.
Eligibility here means “belongs in the reviewed reconstruction.” It does not mean every eligible row is already technically import-ready.
Cleansing decisions
| Source row | Decision |
| --- | --- |
| A01 | Import |
| A02 | Normalize ID and approved display name; import |
| A03 | Import |
| A04 | Import |
| A05 | Withhold; link to A02’s retained record |
| A06 | Withhold; link to existing Northbank |
| C01 | Import |
| C02 | Supply Last Name Reed; import |
| C03 | Replace parent reference with MER-CUST-005; import |
| C04 | Normalize email domain; import |
| C05 | Withhold; link to C01 |
| C06 | Hold conflicting email change |
| D01 | Import |
| D02 | Map WON to Closed Won; import |
| D03 | Remove currency symbol; retain numeric 700.00 |
| D04 | Normalize closing date; import |
| D05 | Withhold; link to existing Redwood Deal |
| P01–P04 | Import as staged packets |
| P05 | Withhold; link to P01 |
| V01 | Normalize Installation and Date/Time; import |
| V02 | Preserve missing billing values; import |
| V03 | Retain blank name for first pass; repair afterward |
| V04 | Normalize submission time; import |
| V05 | Preserve absent submission/acceptance; import |
| V06 | Withhold; link to V01 |

A useful source-disposition check is:
\[
28 = 21 + 6 + 1
\]
That is:
- 21 eligible records.
- 6 duplicate/existing rows withheld.
- 1 conflicting instruction held.
9.2 Prepared files
These files use business keys for lookup association in the new importer. For a classic interface requiring destination record IDs, substitute the verified lookup IDs from your crosswalk.
C01_CH06_Accounts_Ready.csv
CustomerBusinessID,AccountName
MER-CUST-003,Harbor Works
MER-CUST-004,Cedar Office Co
MER-CUST-005,Oak Services
MER-CUST-006,Elm Design
C01_CH06_Contacts_Ready.csv
ContactBusinessID,FirstName,LastName,Email,CustomerKey
MER-CON-006,Jordan,Vale,jordan.vale@example.com,MER-CUST-003
MER-CON-007,Sam,Reed,sam.reed@example.com,MER-CUST-004
MER-CON-008,Morgan,Lee,morgan.lee@example.com,MER-CUST-005
MER-CON-009,Riley,Stone,riley.stone@example.com,MER-CUST-006
C01_CH06_Deals_Ready.csv
OpportunityBusinessID,DealName,CustomerKey,ContactKey,ClosingDate,Stage,Amount
MER-DEAL-003,Harbor historical opportunity,MER-CUST-003,MER-CON-006,2026-09-14,Closed Won,600.00
MER-DEAL-004,Cedar historical opportunity,MER-CUST-004,MER-CON-007,2026-09-14,Closed Won,950.00
MER-DEAL-005,Oak historical opportunity,MER-CUST-005,MER-CON-008,2026-09-14,Closed Won,700.00
MER-DEAL-006,Elm historical opportunity,MER-CUST-006,MER-CON-009,2026-09-14,Closed Won,500.00
C01_CH06_OrderPackets_Stage.csv
PacketName,OrderBusinessID,CustomerKey,OpportunityKey,ConfirmationReceivedAt
Harbor packet,MER-ORD-003,MER-CUST-003,MER-DEAL-003,2026-09-14 10:00:00
Cedar packet,MER-ORD-004,MER-CUST-004,MER-DEAL-004,2026-09-14 10:30:00
Oak packet,MER-ORD-005,MER-CUST-005,MER-DEAL-005,2026-09-14 13:00:00
Elm packet,MER-ORD-006,MER-CUST-006,MER-DEAL-006,2026-09-14 14:00:00
Assign Draft and Internal draft as explicit staging defaults. The intended final status is retained separately.
C01_CH06_PacketVersions_FirstPass.csv
VersionName,VersionBusinessID,OrderKey,RevisionNumber,CustomerIDSnapshot,QuoteIDSnapshot,ConfirmationReferenceSnapshot,InstallationSnapshot,BillingEmailSnapshot,BillingEvidenceReference,SubmittedAt,ReviewOutcome,ReturnReason,AcceptedAt,ReviewerReference
Harbor packet v1,MER-PVER-003-01,MER-ORD-003,1,MER-CUST-003,MER-QUOTE-003,CONF-003,Yes,harbor.billing@example.com,CONF-003,2026-09-14 10:30:00,Accepted,,2026-09-14 11:00:00,MER-USR-003
Cedar packet v1,MER-PVER-004-01,MER-ORD-004,1,MER-CUST-004,MER-QUOTE-004,CONF-004,No,,,2026-09-14 12:00:00,Returned,Billing email missing,,MER-USR-003
,MER-PVER-004-02,MER-ORD-004,2,MER-CUST-004,MER-QUOTE-004,CONF-004,No,cedar.billing@example.com,BILL-004,2026-09-14 16:00:00,Accepted,,2026-09-14 16:30:00,MER-USR-003
Oak packet v1,MER-PVER-005-01,MER-ORD-005,1,MER-CUST-005,MER-QUOTE-005,CONF-005,Yes,oak.billing@example.com,CONF-005,2026-09-14 14:00:00,Submitted,,,
Elm packet v1,MER-PVER-006-01,MER-ORD-006,1,MER-CUST-006,MER-QUOTE-006,CONF-006,No,elm.billing@example.com,CONF-006,,Draft,,,
Assign Internal draft access scope during staging.
C01_CH06_PacketVersion_Repair.csv
VersionName,VersionBusinessID,OrderKey,RevisionNumber,CustomerIDSnapshot,QuoteIDSnapshot,ConfirmationReferenceSnapshot,InstallationSnapshot,BillingEmailSnapshot,BillingEvidenceReference,SubmittedAt,ReviewOutcome,ReturnReason,AcceptedAt,ReviewerReference
Cedar packet v2,MER-PVER-004-02,MER-ORD-004,2,MER-CUST-004,MER-QUOTE-004,CONF-004,No,cedar.billing@example.com,BILL-004,2026-09-14 16:00:00,Accepted,,2026-09-14 16:30:00,MER-USR-003
The repair retains the intended business identity. It supplies the missing mandatory name without altering the historical event.
9.3 Field map
Use the labels actually configured in your organisation. These are the course’s logical destination fields, not guessed API names.
| Prepared column | Destination |
| --- | --- |
| CustomerBusinessID | Accounts → Customer Business ID |
| AccountName | Accounts → Account Name |
| ContactBusinessID | Contacts → Contact Business ID |
| FirstName / LastName / Email | Contacts → corresponding standard fields |
| CustomerKey in Contacts | Contacts → Account Name lookup |
| OpportunityBusinessID | Deals → Opportunity Business ID |
| DealName | Deals → Deal Name |
| CustomerKey in Deals | Deals → Account Name lookup |
| ContactKey | Deals → Contact Name lookup |
| ClosingDate | Deals → Closing Date |
| Stage | Deals → Stage |
| Amount | Deals → Amount |
| PacketName | Order Packets → Packet Name |
| OrderBusinessID | Order Packets → Order Business ID |
| CustomerKey in packets | Order Packets → Customer lookup |
| OpportunityKey | Order Packets → Related Opportunity lookup |
| ConfirmationReceivedAt | Order Packets → Confirmation Received At |
| VersionName | Packet Versions → Version Name |
| VersionBusinessID | Packet Versions → Version Business ID |
| OrderKey | Packet Versions → Order Packet lookup |
| RevisionNumber | Packet Versions → Revision Number |
| CustomerIDSnapshot | Packet Versions → Customer ID Snapshot |
| QuoteIDSnapshot | Packet Versions → Quote Business ID Snapshot |
| ConfirmationReferenceSnapshot | Same-named version field |
| InstallationSnapshot | Installation Snapshot |
| BillingEmailSnapshot | Billing Email Snapshot |
| BillingEvidenceReference | Billing Evidence Reference |
| SubmittedAt | Submitted At |
| ReviewOutcome | Review Outcome |
| ReturnReason | Return Reason |
| AcceptedAt | Accepted At |
| ReviewerReference | Reviewer Reference |

The owner and staging defaults are additional batch instructions.
SourceRow, DesiredPacketStatus and the packet source’s ConfirmationReference remain in the preparation/release evidence. They are not mapped to unrelated destination fields.
9.4 Expected import ledger
For the documented row-skip path:
| Batch | Module | Submitted | Added | Updated |
| --- | --- | --- | --- | --- |
| B01 | Accounts | 4 | 4 | 0 |
| B02 | Contacts | 4 | 4 | 0 |
| B03 | Deals | 4 | 4 | 0 |
| B04 | Order Packets | 4 | 4 | 0 |
| B05 | Packet Versions | 5 | 4 | 0 |
| B06 | Packet Versions repair | 1 | 1 | 0 |
| B07 | Accounts repeat | 4 | 0 | 0 |
| Total |  | 26 | 21 | 0 |

These are expected results, not supplied observation evidence.
The first main passes balance as:
\[
21 = 20 + 0 + 1
\]
Including repair and the duplicate probe:
\[
26 = 21 + 0 + 5
\]
Physical submissions are not the same as unique intended records.
The retry submits one record a second time. The probe submits four records again. That explains why 26 submitted rows produce 21 new records.
Manual evidence entry, accepted-version selection and final-state edits are recorded separately; they are not import additions or updates in this table.
If the importer blocks V03 before execution
Record the original file as preflight blocked.
After correcting V03, the completed main jobs should instead account for:
- 21 submitted.
- 21 added.
- 0 updated.
- 0 skipped.
The later four-row Account repeat adds four deliberate skips.
Use the actual branch observed in your laboratory.
9.5 Final packet and version state
New parent packets
| Order | Final Packet Status | Accepted Version |
| --- | --- | --- |
| MER-ORD-003 | Accepted | MER-PVER-003-01 |
| MER-ORD-004 | Accepted | MER-PVER-004-02 |
| MER-ORD-005 | Awaiting Finance review | None |
| MER-ORD-006 | Draft | None |

New versions
| Version | Review Outcome | Submitted At, UTC |
| --- | --- | --- |
| MER-PVER-003-01 | Accepted | 10:30 |
| MER-PVER-004-01 | Returned | 12:00 |
| MER-PVER-004-02 | Accepted | 16:00 |
| MER-PVER-005-01 | Submitted | 14:00 |
| MER-PVER-006-01 | Draft | None |

All listed event times are on 14 September 2026.
The existing accepted-version selections remain:
- Order 001 → MER-PVER-001-01.
- Order 002 → MER-PVER-002-02.
Cedar version 1 retains blank Billing Email Snapshot and Billing Evidence Reference. Elm retains blank Submitted At, Accepted At and Reviewer Reference.
9.6 Final counts and relationship checks
| Module or structure | Starting |
| --- | --- |
| Accounts | 2 |
| Contacts | 2 |
| Deals | 2 |
| Enquiries | 1 |
| Order Packets | 2 |
| Packet Versions | 3 |
| Tasks | 1 |
| Leads | 0 |
| Supporting References rows | 4 |

No historical Enquiries are invented to fill missing upstream history. The six-order reconstruction does not require six Leads.
New relationship cross-check
| Account | Contact | Deal |
| --- | --- | --- |
| MER-CUST-003 | MER-CON-006 | MER-DEAL-003 |
| MER-CUST-004 | MER-CON-007 | MER-DEAL-004 |
| MER-CUST-005 | MER-CON-008 | MER-DEAL-005 |
| MER-CUST-006 | MER-CON-009 | MER-DEAL-006 |

For each row:
- Contact belongs to the listed Account.
- Deal references that Account and Contact.
- Packet references that Account and Deal.
- Every version belongs to that packet.
- Snapshot customer ID agrees with the intended customer.
- Selected accepted version, if any, belongs to the same packet.
The displayed short version suffixes refer to full MER-PVER-* identifiers.
9.7 Opportunity control total
Existing opportunity total:
\[
1200.00 + 800.00 = 2000.00\text{ GBP}
\]
New opportunity total:
\[
600.00 + 950.00 + 700.00 + 500.00
=
2750.00\text{ GBP}
\]
Expected final total:
\[
2000.00 + 2750.00 = 4750.00\text{ GBP}
\]
Inspect each Deal as well as the aggregate.
These figures remain synthetic opportunity estimates. They do not establish quote lines, invoices, payments or revenue recognition.
9.8 Historical measurement reconciliation
Completed orders:
| Order | Calculation |
| --- | --- |
| 001 | 10:00 − 09:00 |
| 002 | 14:15 − 09:15 |
| 003 | 11:00 − 10:00 |
| 004 | 16:30 − 10:30 |

Completed elapsed total:
\[
60 + 300 + 60 + 360 = 780\text{ minutes}
\]
Mean completed elapsed:
\[
\frac{780}{4} = 195\text{ minutes}
\]
Orders 005 and 006 have no acceptance event and are excluded from the completed-time mean.
Completed first-pass:
\[
\frac{2\text{ accepted without return}}{4\text{ completed orders}}
\times 100
=
50\%
\]
Accepted proportion:
\[
\frac{4}{6}\times 100 \approx 66.7\%
\]
Open age at 17:00 UTC:
| Order | Calculation |
| --- | --- |
| 005 | 17:00 − 13:00 |
| 006 | 17:00 − 14:00 |

The open orders’ eventual first-pass outcomes remain unknown.
Reconstructing the missing history reproduces the original baseline. It does not demonstrate that the proposed pilot improved performance.
9.9 Access reconciliation
Under the Chapter 5 base access design, with no additional sharing routes:
| User | Expected packet/version view | Expected authority |
| --- | --- | --- |
| Ava | Six packets and eight versions as owner | Preparation-field authority; no Finance review-field editing |
| Leo | Orders 001–005 and their seven versions | Finance review-field authority; no import permission |
| Mia | Northbank’s shared packet 001 and version 001-01 | Read-only Service context |
| Noor | Six packets and eight versions through hierarchy | Read-only Operations profile |
| Isha | Complete administrator view | Technical administration and reconstruction |

Elm’s packet and version remain Internal draft. Leo still has the separately shared customer/deal context; that does not automatically grant access to Elm’s custom packet records.
Actual results must be recorded. If a user sees a different subset, investigate ownership, hierarchy, direct shares, groups, criteria rules and other overlapping routes.
Static permissions still do not provide state-dependent freezing of all accepted-history preparation fields. That control remains part of Chapter 10.
9.10 Backup and recovery record
A completed plan should identify:
| Item | Required entry |
| --- | --- |
| Recovery scope | Base records in affected modules and supporting subform |
| Before-image location | Actual retained exports/archive |
| Identity preservation | Business IDs, actual Record IDs and parent references retained |
| Configuration evidence | Actual roles/profiles/sharing/field-rule evidence |
| Added-record recovery | Inspect batch and dependencies before using available undo |
| Updated-value recovery | Narrow update from verified before-image |
| Rejection recovery | Correct and retry unresolved row |
| External effects | Investigate and recover separately in receiving application |
| Post-recovery checks | Counts, keys, values, links, historical states and access |
| Completion evidence | Actual comparison results and unresolved exceptions |

A backup is useful when you can identify the required record, field and relationship in it. “A ZIP was downloaded” is not a complete recovery demonstration.
9.11 Independent challenge solutions
Challenge A
The count check passes because the update changed a value without adding or deleting a Deal.
The Amount control reveals the defect:
\[
4750.00 - 4120.00 = 630.00\text{ GBP}
\]
This agrees with Oak’s individual error:
\[
700.00 - 70.00 = 630.00\text{ GBP}
\]
Undo Import cannot reverse the update.
Prepare a narrow update-only file containing:
- Oak’s actual record ID from the same organisation.
- Correct Amount 700.00.
Map the record-ID matcher and Amount. Leave unrelated fields outside the mapping.
After recovery, check:
- Oak Amount is 700.00.
- Six-Deal total is 4750.00.
- Deal count remains six.
- Account and Contact lookups are unchanged.
- No unexpected process or external effect occurred.
- Recovery execution is recorded.
Challenge B
1. Add as new, business-ID matching: expected skip because MER-CUST-004 already exists.
2. Both, business-ID matching with Account Name mapped: the existing record can be renamed to Cedar Workplace Services.
3. Account Name matching only: the different name might not match the existing Account. Other uniqueness controls may still reject it, but name matching alone does not express the intended identity.
Hold the unverified rename instruction. Link it to the existing customer identity and obtain approved evidence before applying a name change.
Challenge C
A corrected statement is:
“The first-pass jobs added 20 of the 21 submitted records. One record was skipped and remains unresolved. Migration completion has not yet been established.”
To close the migration, obtain:
- Actual skipped-row reason.
- Source-row identity.
- Reviewed correction.
- Repair-job result.
- Destination record and parent verification.
- Final count, value and historical-state reconciliation.
- Access-test evidence.
- Disposition for every withheld source row.
9.12 Knowledge-check answers
 1. Preserve the original: it provides evidence and allows preparation decisions to be traced or revisited.
 2. Duplicate versus conflict: a duplicate repeats the same identity/instruction; a conflict introduces a materially different value or instruction requiring evidence.
 3. Historical billing blank: it explains the returned submission. The later correction belongs in a later version.
 4. Business versus Zoho ID: one identifies the business entity; the other identifies its record in a particular CRM organisation.
 5. Accounts first: Contact lookups need resolvable parent Accounts.
 6. Deferred accepted selection: the selected version must exist before the packet can reference it.
 7. Undo limits: it removes eligible imported additions, not updates to existing records or external effects.
 8. Import versus business validation: import channels do not prove every validation rule, relationship or business invariant was enforced.
 9. Skip empty updates: it retains existing values where mapped source values are blank; it does not prevent nonblank errors.
10. Count insufficiency: the right number of records can still contain wrong identities, values or links.
11. Historical time fields: Confirmation Received At, Submitted At and Accepted At reproduce business events; Created Time does not.
12. Pilot boundary: these are reconstructed historical records, not newly observed pilot confirmations under the pilot’s receipt and cutoff conditions.
## 10. Chapter recap and next step

You have learned to treat migration as a controlled reconstruction:
- Profile first.
- Clean according to evidence.
- Match on identity.
- Import in dependency order.
- Separate rejected rows from deliberate duplicate skips.
- Repair narrowly.
- Reconcile meaning as well as counts.
- Retain before-images and a usable recovery path.
The expected Meridian base now contains six historical orders and eight preserved versions. Its completed-order mean remains 195 minutes, with two orders open at the original cutoff.
Next: Chapter 7 — Lead Capture and Customer Engagement. You will build new intake paths against this prepared customer dataset and distinguish a new enquiry, a known customer and a repeated submission.
## 11. Glossary and further reading

Glossary
| Term | Meaning |
| --- | --- |
| Add import | Creates new records under the selected duplicate-matching policy |
| Before-image | Retained values from before a change |
| Business identifier | Stable identity assigned by the business |
| Cleansing | Evidence-based preparation of data for its intended use |
| Conflict | Materially different instructions attached to the same identity |
| Control total | Aggregate used to detect missing or incorrect values |
| Crosswalk | Mapping between source/business identities and destination record identities |
| Data profiling | Examination of source structure, values and quality |
| Dependency order | Sequence in which referenced records exist before their children |
| Destination duplicate | Source record already represented in the destination |
| Grain | Meaning of one record or row |
| Idempotent behavior | Repetition produces the intended stable result rather than additional unintended effects |
| Lookup association | Selection of the field used to resolve a referenced record |
| Preflight failure | Failure before an import job is submitted |
| Reconciliation | Comparison of expected and actual records, values and relationships |
| Rejected row | Submitted instruction that was not accepted for the reported reason |
| Snapshot | Preserved value representing a particular historical state |
| Staging | Controlled intermediate state before final release |
| Update import | Changes matching existing records |
| Upsert | Adds unmatched records and updates matched records |

Official product references
Documentation accessed for this chapter: 5 October 2026. Procedures and capabilities should be checked against the importer version and entitlement shown in your organisation.
1. Zoho CRM — Import data into a CRM module (https://help.zoho.com/portal/en/kb/crm/data-administration/import-data/articles/import-data-into-a-crm-module)  
New-importer procedure, supported fields, lookup association, dependent files, import modes and error investigation.
2. Zoho CRM — Importing Data to Zoho CRM (https://help.zoho.com/portal/en/kb/crm/data-administration/import-data/articles/import-data)  
Classic-importer procedure, matching, formats, defaults, subform import and automation qualifications.
3. Zoho CRM — Viewing Import History (https://help.zoho.com/portal/en/kb/crm/data-administration/import-data/articles/view-import-history)  
Added/updated/skipped details, error downloads, history visibility and added-record undo.
4. Zoho CRM — Working with Validation Rules (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/validation-rules/articles/create-validation-rules)  
Supported validation contexts and import/update exceptions.
5. Zoho CRM — Export CRM Data (https://help.zoho.com/portal/en/kb/crm/data-administration/export-data/articles/export-crm-data)  
Module and subform exports, criteria, field selection, Record IDs and export history.
6. Zoho CRM — Requesting Data Backup (https://help.zoho.com/portal/en/kb/crm/data-administration/data-backup/articles/requesting-data-backup)  
Administrative backup requests, archives, exclusions and restoration approaches.
7. Zoho CRM — Managing Profile Permissions (https://help.zoho.com/portal/en/kb/crm/security-control/profile-management/articles/manage-profile-permissions)  
Module Import/Export permissions, prerequisites and Data Administration permissions.
8. Zoho CRM — Troubleshooting Data Import and Export (https://help.zoho.com/portal/en/kb/crm/troubleshooting/articles/troubleshooting-data-import-export)  
Owner matching, encoding, undo behavior and import troubleshooting.
