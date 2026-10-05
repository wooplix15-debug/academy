# Roles, Profiles and Record Access

## 1. What you will learn

A connected process requires people to share information without sharing every responsibility.
At Meridian Supply:
- Ava needs to prepare sales information.
- Leo needs to review the billing packet.
- Mia needs enough customer context to provide service.
- Noor needs to monitor the process.
- Isha needs to administer the configuration.
Giving all five people administrator access would make the records easy to open. It would also remove important boundaries.
Ava could record Finance acceptance. Mia could change commercial information unrelated to her service task. A routine user could alter the rules that determine access. Historical evidence could be deleted.
The opposite design is also ineffective. If every record is private and no appropriate sharing is configured, Finance cannot review Sales’ packets and Service cannot see the customer context it needs.
This chapter teaches you to establish appropriate access: enough information and authority to complete the task, with specific boundaries around other work.
By the end, you should be able to:
 1. Explain the different roles of a role hierarchy and a profile.
 2. Configure representative CRM roles and profiles.
 3. Distinguish record visibility from permission to change a field.
 4. Restrict Finance decision fields for ordinary Sales and Service users.
 5. Set organisation-wide record access and add targeted sharing.
 6. Explain how record ownership affects access.
 7. Use a CRM group for a defined collaboration purpose.
 8. Distinguish groups, Deal Teams, territories and Teamspaces.
 9. Inspect audit information within the user’s permitted visibility.
10. Demonstrate permitted and denied actions using separate user identities.
11. Diagnose unexpected access by tracing every applicable access route.
Prerequisites
You need the dedicated training organisation from Chapter 3 and the data model from Chapter 4.
The live exercise uses:
- Accounts.
- Contacts.
- Deals.
- Enquiries.
- Order Packets.
- Packet Versions.
- The Supporting References subform.
You need Isha’s administrative access and controlled training identities for Ava, Leo, Mia and Noor.
The complete exercise requires custom profiles, field permissions, sharing rules and individual record sharing. The accessed record-sharing help identifies Enterprise and Ultimate editions for that particular feature. If you use Zoho One, check the actual CRM entitlement associated with your organisation.
No coding is required.
Preserved case decisions
| Information or decision | Authority |
| --- | --- |
| Sales preparation and correction | Ava |
| Finance acceptance | Leo |
| Customer-service work | Mia |
| Process monitoring and improvement | Noor |
| Configuration administration | Isha |
| Current accounting facts | Books, maintained by Finance |
| Service-ticket status | Desk, maintained by Service |
| Employee and leave information | Separate People process |
| Packet revision history | CRM Packet Versions |

The historical records remain:
- Northbank order MER-ORD-001, accepted through MER-PVER-001-01.
- Redwood order MER-ORD-002, first returned through MER-PVER-002-01, then accepted through MER-PVER-002-02.
The September timestamps and Chapter 1 measurements remain historical case inputs. This chapter’s access tests do not replace them.
New training decisions
This chapter introduces:
- Four named non-administrator CRM profiles.
- A role hierarchy for the customer-process participants.
- A CRM group called Meridian Finance Reviewers.
- An Access Scope field on Order Packets and Packet Versions.
- Temporary records with LAB identifiers for permission tests.
Access Scope is an administrative classification for the training sharing rules. It is not a Finance decision or proof that the packet is complete.
Your contribution to the project
You will create the project’s first configured access matrix and demonstrations of permitted and denied actions.
Your evidence will explain:
- Who can open a record.
- Which fields they can see.
- Which fields they can change.
- Which access route provides visibility.
- Which business action remains reserved for another participant.
Later chapters will use this foundation for controlled transitions, integration identities and user acceptance testing.
## 2. Lessons

### Lesson 1 — Answer three different access questions

When someone says, “I cannot access the order,” ask what they mean.
There are at least three different questions:
1. Can the user access the module?
2. Can the user access this particular record?
3. Can the user perform this action or change this field?
A person can pass one question and fail another.
For example, Mia can have permission to view Packet Versions as a module but still be unable to open Redwood’s version because that record has not been shared with her.
Leo can open a shared Northbank version and edit its Finance review fields while being unable to change the billing-email snapshot.
The ordinary-user access model
For this chapter’s organisation modules, use this reasoning model:
A permitted action needs the relevant module permission, a valid record-access route, and the required field or action permission.
Record-access routes can include ownership, hierarchy and applicable sharing.
They are not all independent restrictions. Several routes can grant access to the same record.
A narrow sharing entry does not necessarily reduce access already granted by ownership, public settings or another sharing route.
Zoho’s sharing documentation explains that profile permissions remain a ceiling on actions, while overlapping sharing routes can provide the highest applicable record access.^sharing
Worked example
Leo has:
- View and Edit permission for Packet Versions.
- Read/Write sharing to a Northbank version.
- Read Only permission on Billing Email Snapshot.
- Read/Write permission on Accepted At.
The results differ by field:
| Attempt | Expected result | Reason |
| --- | --- | --- |
| Open the version | Permitted | Module and record access are present |
| Edit Accepted At | Permitted | Edit, record write access and field write permission are present |
| Edit Billing Email Snapshot | Denied or unavailable | Field is read-only for Finance |
| Delete the version | Denied or unavailable | Delete permission is not granted |

“Read/Write record access” does not mean every field becomes writable.
Administrator access
The official role documentation states that a user with the Administrator profile can access all data regardless of their assigned role.^roles
Therefore, Isha is unsuitable as the test identity for ordinary Sales or Finance restrictions.
Finance-only acceptance in this chapter refers to the configured ordinary business profiles. Isha retains administrative configuration and recovery privileges.
Check L1: Leo can open a version but cannot change its billing email. Which access layer should you inspect first?
### Lesson 2 — Use roles for hierarchy, profiles for actions

A role places a user in the CRM hierarchy.
A profile defines the actions and features that a user may use.
A job title, role and profile may have related names, but they solve different problems.
Role hierarchy
For organisation modules, users higher in a role hierarchy can access records owned below them, subject to the required module permissions.
The official role help also explains:
- Same-level or peer access is not automatically granted.
- Share Data with Peers is a separate setting.
- Managers still need the relevant module Read or Edit permission.
- The Administrator profile has wider access irrespective of role.^roles
Meridian’s target hierarchy is:
- Existing top organisation role.
- Meridian Process Lead: Noor.
- Meridian Sales: Ava.
- Meridian Finance: Leo.
- Meridian Service: Mia.
Isha remains in the appropriate existing administrative position with the Administrator profile.
Do not place Finance above Sales merely to make Sales’ records visible. That would give the hierarchy a broader meaning than the handoff requires.
Finance review is cross-functional collaboration. Targeted sharing is the better route.
Profile permissions
Meridian uses:
- Meridian Sales.
- Meridian Finance.
- Meridian Service Context.
- Meridian Operations Read.
The profile determines whether its users may view, create, edit or delete records in each module. It also controls functions such as import, export, sharing, owner changes and customization.^profiles
Noor’s hierarchy position provides a record-visibility route. His read-only profile prevents that visibility from becoming general editing authority.
Worked example: Noor above Ava
Noor sits above Ava.
Ava owns the Northbank Account.
Noor’s profile permits viewing Accounts but not editing them.
Expected result:
- Noor can view Northbank through the hierarchy.
- Noor cannot edit its fields.
If Noor’s profile did not permit viewing Accounts at all, the hierarchy would not supply the missing module permission.
Documented role configuration
Users need Manage Roles permission.
1. Open Setup → Security Control → Roles and Sharing.
2. In Roles, select New Role.
3. Enter the role name.
4. Select its immediate superior in Reports To.
5. Leave Share Data with Peers unselected for this exercise.
6. Add a useful description.
7. Click Save.^roles
Assign the role through:
Setup → General → Users → selected user → Edit → Role → Save.
Check the organisation’s hierarchy preference at:
Setup → General → Company Settings → Hierarchy Preference.^hierarchy
The exercise uses Role Hierarchy.
Do not change a populated shared organisation’s hierarchy preference as an incidental step. Use the dedicated training context and record the setting before configuring roles.
Documented profile configuration
Users need Manage Profiles permission.
1. Open Setup → Security Control → Profiles.
2. Select New Profile.
3. Name the profile.
4. Choose the existing profile to clone.
5. Add a description.
6. Click Create.
7. Configure the resulting permissions.^createprofiles
Clone Standard rather than Administrator for the four ordinary business profiles.
The current profile-permission help states that permission changes apply immediately.^profiles
Expected result: each representative user has the intended role and custom profile.
Recovery: if the user has the wrong profile, correct the assignment and repeat the affected checks under that user’s fresh session.
Check L2: Why does moving Leo above Ava solve the wrong problem when the requirement is only to review selected Sales packets?
### Lesson 3 — Restrict fields according to business authority

A field restriction controls whether a profile may read or write a field.
For Meridian, some people need to see the outcome without establishing it.
Ava should see that Finance accepted a packet. She should not be able to enter that acceptance herself.
Separate preparation from review
The Packet Versions module contains two main information groups:
Preparation and snapshot information
- Version identity.
- Parent packet.
- Revision number.
- Customer and quote references.
- Confirmation reference.
- Installation requirement.
- Billing email and evidence.
- Submission timestamp.
Finance review information
- Review Outcome.
- Return Reason.
- Accepted At.
- Reviewer Reference.
The Order Packets module also contains:
- Packet Status.
- Accepted Version.
For ordinary profiles, the target is:
- Sales writes preparation information.
- Finance reads the supplied preparation and writes review information.
- Service reads selected context.
- Operations reads the process.
- Isha configures and administers.
Read Only differs from hidden
Use Read Only when the value is needed for the user’s work but must not be edited.
Use Don’t Show when the value itself is not needed.
For Mia:
- Installation Snapshot is useful context.
- Review Outcome is useful context.
- Billing Email Snapshot is not required for her service task.
- Billing Evidence Reference is not required.
- Reviewer Reference is not required.
The Supporting References notes can also contain a billing email. Hiding the principal email field while leaving the same address in a visible note would not meet the information boundary.
Therefore, hide the subform’s Evidence Note column for the Service profile.
Documented field-permission procedure
The custom-field help describes:
1. Open Setup → Customization → Modules and Fields.
2. Select the module and layout.
3. Open the field’s settings.
4. Select Set Permission.
5. Set each profile’s permission.
6. Save the permission and layout changes.^fields
For subform columns, use the column’s More → Set Permissions control and the documented Read and Write, Read Only or Don’t Show options.^subforms
The field-permission help identifies edition dependencies. Confirm that the required controls are available.
Expected result: the user can read or change only the fields allowed by the field matrix.
Recovery: correct the specific field/profile setting, then reopen the record as the affected user. A layout preview alone is insufficient evidence of the live result.
Static permissions and lifecycle controls
Profile field permissions apply according to the profile. They do not, by themselves, change because a version moved from Draft to Accepted.
This chapter establishes who may write Finance fields. State-dependent protection of accepted snapshots requires additional lifecycle configuration in Chapter 10.
Use the temporary laboratory records for editing tests. Preserve the historical September records.
Worked example
Ava opens a version she owns.
She can edit its Version Name and billing preparation fields.
She sees Accepted At as read-only.
Ownership does not give Ava Finance field-write permission when her profile denies it.
Likewise, Leo’s Finance profile cannot edit a read-only snapshot merely because he has Read/Write sharing.
Check L3: Why should Mia’s Evidence Note column be hidden if the main Billing Email Snapshot is hidden?
### Lesson 4 — Start with a suitable sharing baseline

Organisation-wide permissions establish the default record-access model for a module.
The documented choices include:
- Private.
- Public Read Only.
- Public Read/Write.
- Public Read/Write/Delete.^rules
For Meridian’s customer-process modules, begin with Private.
Private does not mean “only the owner under every circumstance.” Hierarchy, administration and additional sharing can still provide access.
Sharing rules extend access
A sharing rule grants additional access to records that meet a defined source or criterion.
The official help states that a sharing rule cannot restrict broader access already supplied by the organisation’s default permissions.^rules
Therefore:
Public Read/Write plus a narrow read-only rule does not create a narrow access boundary.
Start with the intended baseline, then add the access needed by the process.
Owner-based and criteria-based rules
An owner-based rule can share records owned by users in a role or group.
A criteria-based rule selects records using their values.
Meridian uses both:
- Owner-based sharing gives Finance read-only customer and opportunity context from Sales.
- Criteria-based sharing gives Finance editing access to selected packets and versions.
Access Scope
Add this field to Order Packets and Packet Versions:
| Attribute | Decision |
| --- | --- |
| Label | Access Scope |
| Type | Picklist |
| Values | Internal draft; Finance review |
| Default | Internal draft |
| Required | Yes |
| Write authority | Isha’s administrative profile |
| Ordinary profiles | Read Only |
| Purpose | Select the records included in the training Finance-sharing rules |

The accepted historical packet records and versions use Finance review.
The laboratory contains both Finance review and Internal draft examples.
Access Scope does not establish completeness, submission or acceptance. The validation and review fields retain their separate meanings.
Documented default-sharing procedure
Users need Manage Data Sharing permission.
1. Open Setup → Security Control → Roles and Sharing → Data Sharing Settings.
2. Open Default Organization Permissions.
3. Select the intended Default Access for each module.^rules
The current help documents rule execution and also describes recalculation in the group-sharing guidance. Complete the execution or recalculation action presented in your environment before testing.
Expected result: the applicable module baseline is Private, and the target rules have finished applying.
Documented sharing-rule procedure
 1. Open Data Sharing Settings.
 2. Select the Sharing Rules tab.
 3. Choose Create Sharing Rule.
 4. Select the module.
 5. Enter the rule name.
 6. Choose owner-based or criteria-based sharing.
 7. Define the source or criteria.
 8. Select the destination role or group.
 9. Choose the permission.
10. Set Superiors Allowed according to the requirement.
11. Save and complete the applicable execution.^rules
For the Finance rules, leave Superiors Allowed unselected.
Noor already has a hierarchy route to Ava-owned records. The rule does not need to add another superior-sharing route.
Worked example
Two versions are owned by Ava:
| Version | Access Scope |
| --- | --- |
| MER-PVER-LAB-001-01 | Finance review |
| MER-PVER-LAB-002-01 | Internal draft |

The Finance rule matches only Finance review.
Expected result:
- Leo can open the first version.
- Leo cannot open the second through that rule.
- Ava can open both as owner.
- Noor can view both through hierarchy and his View permission.
Check L4: Why would Public Read/Write invalidate the intended “Internal draft is not visible to Leo” test?
### Lesson 5 — Use ownership and individual sharing deliberately

A record owner is the assigned CRM user responsible for the record.
A business data owner is responsible for the information’s business meaning.
They can be different.
Ava can own an Order Packet in CRM while Leo remains the authority for Finance acceptance.
Reassigning the Chapter 4 reconstruction
Chapter 4 entered the dataset under Isha’s build access.
For this exercise, assign its Accounts, Contacts, Deals, Enquiry, Order Packets and Packet Versions to Ava.
This establishes a consistent Sales ownership route for testing.
Changing the assigned owner does not change the supplied historical confirmation, submission or acceptance events.
Documented owner-change procedure
A user needs Change Owner permission.
1. Open the intended module and record.
2. Select the Record Owner control.
3. Choose the new user.
4. Inspect any offered associated-record transfer options.
5. Save.^ownership
The official help describes different associated-record behavior across modules and circumstances.
For the small exercise, transfer the listed records explicitly and verify their owners. Do not assume every child record transferred exactly as intended.
Expected result: each listed base record shows Ava as its assigned owner.
Sharing one record
Individual sharing is useful when the requirement is record-specific.
Mia needs Northbank context but not every Sales customer.
Use targeted sharing of:
- Northbank Account.
- Taylor’s Contact.
- Northbank Order Packet.
- Northbank accepted Packet Version.
Share each as Read Only and leave With Related List unselected.
This prevents the exercise from treating a broad related-list share as equivalent to carefully selected context.
Documented individual-sharing procedure
1. Open the record.
2. Select More Actions → Share.
3. Choose Private sharing.
4. Add the intended user, role or group.
5. Choose Read Only, Read/Write or Full Access.
6. Choose whether related lists are included.
7. Click Share.^sharing
The official help distinguishes those levels:
- Read Only allows viewing.
- Read/Write allows viewing and editing, without owner change or deletion through that grant.
- Full Access includes broader record operations, subject to profile permission.
For Mia, Read Only is sufficient.
Revoking one route may leave another
Suppose Northbank is shared with Mia:
- Directly to Mia.
- Through a group containing Mia.
Removing the direct entry does not remove the group route.
When access remains after a change, inspect all routes:
- Ownership.
- Hierarchy.
- Default access.
- Sharing rules.
- Direct sharing.
- Related-list sharing.
- Group membership.
- Deal Team or territory access, if configured.
Worked example
Mia can open Northbank through a direct Read Only share.
She cannot open Redwood because:
- She does not own it.
- She is not above Ava.
- Accounts is Private.
- No applicable Finance group membership includes her.
- No Redwood direct share exists.
Her Account module View permission makes Northbank access possible. It does not expose every Account.
Check L5: If you remove Mia’s direct share but she still belongs to a group with access, should you expect the record to disappear?
### Lesson 6 — Distinguish teams, groups and territories

The word “team” can refer to several different product structures.
Choose the structure that fits the access requirement.
| Structure | Main purpose |
| --- | --- |
| Zoho One collaboration group | Suite-level coordination and administration |
| CRM group | Destination or source for CRM sharing and user grouping |
| Deal Team | Contributors associated with a particular Deal |
| Territory | Rule-based customer coverage structure |
| Teamspace | Organisation of the CRM workspace and modules |
| Team module | A separate CRM module model with its own team-profile controls |

Membership in one structure does not prove membership or permission in another.
CRM group
Create Meridian Finance Reviewers with Leo as its only member.
Do not assume the Zoho One Handoff Pilot group automatically supplies this CRM group or its sharing permissions.
The documented CRM group procedure is:
1. Open Setup → General → Users → Groups.
2. Select Create Group.
3. Enter its name and description.
4. Select the members.
5. Save.
6. Use View Users to inspect the effective membership.^groups
Groups can include users and other supported member structures. The effective-members view is important when membership is indirect.
The official group help states that CRM records are owned by users rather than groups. A group is a collaboration and sharing mechanism.
Deal Teams
A Deal Team can give multiple contributors access to a particular commercial opportunity.
The accessed Team Selling help documents edition and rollout dependencies.
Its configuration route is:
Setup → Customization → Modules and Fields → Deal Management → Team Selling
An administrator selects the layout and team roles, then saves. A permitted user can add members through the Deal’s Deal Team related list.^dealteam
For example, a technical adviser could receive access to Northbank’s opportunity without becoming the Deal owner.
That does not make the adviser the Finance decision owner.
The base exercise does not require Deal Team configuration because its access needs are already met by the specified rules and direct shares.
Territories
A territory groups customer coverage using criteria such as region, industry or product line.
A role hierarchy follows managerial structure. A territory follows customer coverage.
A salesperson can need accounts across reporting lines. Territory management is useful when that requirement becomes systematic.
For a separate planning example, assume:
| Customer | Supplied Sales Region |
| --- | --- |
| MER-CUST-001 | North |
| MER-CUST-002 | South |

A North territory based on Sales Region = North should select Northbank, not Redwood.
These are paper-planning values. They are not added to the base customer records.
The documented enabling route is:
Setup → Security Control → Territory Management → Get Started
The administrator chooses whether to start from scratch or extend the role hierarchy.
The help explains that this initial choice cannot simply be switched to the other approach later.^territories
Creating a territory uses:
Territory Management → Territories → Create New Territory
The administrator defines:
- Name and description.
- Parent territory.
- Territory manager.
- Members and permissions.
- Selection criteria.
Territory access still depends on profile module permissions. The feature adds another record-access route; it does not remove field restrictions.
Do not enable territories merely to demonstrate a menu. Meridian’s small base process does not establish a territory-management requirement.
Check L6: Why would a North territory be based on customer coverage rather than placing Northbank “under” a manager’s user role?
### Lesson 7 — Use audit visibility as evidence, not as a substitute for access testing

An audit log records supported actions performed in CRM.
It helps answer:
- Which user performed an update?
- Which record or configuration was affected?
- When did it happen?
- What action category was recorded?
The official help describes record changes and supported configuration changes, including roles, profiles and groups.^audit
Audit visibility differs from record visibility
A user may be able to read an Account without being able to inspect another user’s audit activity.
The accessed help states that ordinary users can view their own and subordinate audit logs. Administrative visibility is broader.^audit
Therefore:
- Leo’s shared read access to Northbank does not automatically give him Ava’s audit-log visibility.
- Noor can inspect applicable subordinate activity because Ava is below Noor.
- Isha can inspect administrative audit information.
Documented audit procedure
1. Open Setup → Security Control → Audit Log.
2. Filter by the relevant entity.
3. Select the user.
4. Select the action.
5. Use the actual test date or date range.^audit
For a Sales update performed today, filter for:
- Entity: Accounts.
- User: Ava.
- Action: Updated.
- Time: Today or the actual test range.
Do not filter on September’s historical confirmation date merely because the record contains a September business event. The audit event concerns the current laboratory update.
A denied action needs direct test evidence
Do not assume that every denied click produces an audit entry.
For a denied acceptance-field change, record:
- Tested identity.
- Profile and role.
- Record.
- Attempted field or action.
- Expected result.
- Observed interface or save result.
- Confirmation that the stored value did not change.
Successful updates and configuration changes can be investigated in the audit log. Permission-denial evidence comes from the controlled test itself.
Worked example
Ava updates a supplied laboratory description on Northbank’s Account.
Noor opens Audit Log and filters for Ava’s Account update during the actual test period.
Leo tries to inspect Ava’s audit activity.
Expected result:
- Noor can see applicable subordinate activity.
- Leo does not gain peer audit visibility merely from a shared Account.
Check L7: Why should the test use the actual update date rather than the record’s historical confirmation timestamp?
## 3. Visual explanation — Separate hierarchy and handoff sharing

flowchart TD
    TOP["Existing top role / administrative context"]
    NOOR["Noor: Meridian Process Lead / Operations Read"]
    AVA["Ava: Meridian Sales role / Sales profile"]
    LEO["Leo: Meridian Finance role / Finance profile"]
    MIA["Mia: Meridian Service role / Service Context profile"]

    TOP --> NOOR
    NOOR --> AVA
    NOOR --> LEO
    NOOR --> MIA

    AVA -. "selected packet records through sharing rules" .-> LEO
    AVA -. "selected Northbank context through direct Read Only sharing" .-> MIA
The solid lines represent the role hierarchy.
The dotted lines represent additional record access.
Leo and Mia do not sit above Ava. Their access comes from the intended collaboration route.
Noor can view Ava-owned records through the hierarchy, but the Operations Read profile prevents general editing.
The diagram does not show Isha as an ordinary business reviewer. Isha retains administrative access for configuration and recovery.
## 4. Worked case — Meridian’s access design

Complete user assignments
| User | Business reference | CRM role |
| --- | --- | --- |
| Isha | MER-USR-001 | Appropriate existing administrative position |
| Ava | MER-USR-002 | Meridian Sales |
| Leo | MER-USR-003 | Meridian Finance |
| Mia | MER-USR-004 | Meridian Service |
| Noor | MER-USR-005 | Meridian Process Lead |

Omar and Ren retain the separate People exercise. This chapter does not grant them CRM access.
Module permissions
V means View, C Create and E Edit. Delete is off for every ordinary profile in this exercise.
| Module | Sales | Finance |
| --- | --- | --- |
| Accounts | V, C, E | V |
| Contacts | V, C, E | V |
| Deals | V, C, E | V |
| Enquiries | V, C, E | None |
| Order Packets | V, C, E | V, E |
| Packet Versions | V, C, E | V, E |
| Tasks | V, C, E | V, C, E |

For all ordinary profiles, turn off the exercise’s unneeded administrative and bulk powers:
- Module customization.
- Roles, profiles, groups and data-sharing administration.
- Manage Automation.
- Import and export.
- Mass update and mass delete.
- Change Owner and mass transfer.
- Record Share.
- Developer API access and extensibility administration.
- Send Email and Mass Email for this synthetic laboratory.
Later chapters will deliberately revise relevant permissions, such as controlled import access. Do not grant them now merely because the cloned profile included them.
Field permissions
RW means Read/Write, RO Read Only and Hidden Don’t Show.
Module and field group
Order Packets: Packet Name, Customer, Related Opportunity, Confirmation Received At
Order Packets: Order Business ID
Order Packets: Packet Status, Accepted Version
Order Packets: Access Scope
Packet Versions: name, identity, parent, revision and non-billing snapshot references
Packet Versions: Installation Snapshot and Submitted At
Packet Versions: Billing Email Snapshot
Packet Versions: Billing Evidence Reference
Packet Versions: Review Outcome, Return Reason, Accepted At
Packet Versions: Reviewer Reference
Packet Versions: Access Scope
Supporting References: Evidence Reference and Evidence Kind
Supporting References: Evidence Note
Isha retains administrative field access.
For new Sales preparation records:
- Packet Status defaults to Draft.
- Review Outcome defaults to Draft.
- Access Scope defaults to Internal draft.
These defaults let a preparation record exist without allowing Sales to assert Finance acceptance.
Request-to-submission actions and state-dependent snapshot protection will be configured in later chapters.
Record ownership and scope
Assign the base reconstruction’s business records to Ava.
| Record family | Base ownership |
| --- | --- |
| Accounts, Contacts and Deals | Ava |
| MER-ENQ-001 | Ava |
| MER-ORD-001 and MER-ORD-002 | Ava |
| Three historical Packet Versions | Ava |
| MER-TASK-001 | Ava |

Parent and version scopes are entered explicitly in this exercise. Setting a parent field does not automatically establish its children’s scope.
Completed sharing rules
| Rule | Module | Selection |
| --- | --- | --- |
| S01 | Accounts | Owner in Meridian Sales role |
| S02 | Contacts | Owner in Meridian Sales role |
| S03 | Deals | Owner in Meridian Sales role |
| S04 | Order Packets | Access Scope = Finance review |
| S05 | Packet Versions | Access Scope = Finance review |

Use the specific role for S01–S03, rather than including the wider organisation hierarchy.
For all five rules, Superiors Allowed is not required.
Completed direct sharing
Share these records directly with Mia as Read Only, without related lists:
Record
Northbank Account
Taylor’s Contact
Northbank Order Packet
Northbank accepted version
No Redwood record is directly shared with Mia.
No Deal is shared with Mia because her profile has no Deal module permission.
Expected base-record access
| User | Northbank packet | Redwood packet | Finance fields |
| --- | --- | --- | --- |
| Ava | Owner access | Owner access | Read Only |
| Leo | Shared access | Shared access | Read/Write |
| Mia | Direct Read Only | No applicable route | Read Only on visible Northbank record |
| Noor | Hierarchy Read | Hierarchy Read | Read Only |
| Isha | Administrative access | Administrative access | Administrative access |

The matrix describes expected configuration. Live results must be recorded separately.
Laboratory records
Use these temporary parent records:
order_business_id,packet_name,customer_business_id,opportunity_business_id,confirmation_received_at,packet_status,access_scope,owner
MER-ORD-LAB-001,Northbank permission test,MER-CUST-001,MER-DEAL-001,2026-10-16T09:00:00Z,Awaiting Finance review,Finance review,Ava
MER-ORD-LAB-002,Northbank internal draft test,MER-CUST-001,MER-DEAL-001,2026-10-16T09:05:00Z,Draft,Internal draft,Ava
Use these temporary versions:
version_business_id,version_name,order_business_id,revision_number,customer_id_snapshot,quote_id_snapshot,confirmation_ref_snapshot,installation_snapshot,billing_email_snapshot,billing_evidence_ref,submitted_at,review_outcome,return_reason,accepted_at,reviewer_reference,access_scope,owner
MER-PVER-LAB-001-01,Northbank access test version,MER-ORD-LAB-001,1,MER-CUST-001,MER-QUOTE-001,CONF-LAB-001,Yes,northbank.billing@example.com,CONF-LAB-001,2026-10-16T09:15:00Z,Submitted,,,,Finance review,Ava
MER-PVER-LAB-002-01,Northbank private draft version,MER-ORD-LAB-002,1,MER-CUST-001,MER-QUOTE-001,CONF-LAB-002,Yes,,,,Draft,,,,Internal draft,Ava
These are permission-test copies, not additional observed sales orders. Their simulated October business times are not the actual execution times of the access test.
The supplied successful Finance acceptance input for the first version is:
| Field | Value |
| --- | --- |
| Review Outcome | Accepted |
| Accepted At | 2026-10-16T09:30:00Z |
| Reviewer Reference | MER-USR-003 |
| Parent Packet Status | Accepted |
| Parent Accepted Version | MER-PVER-LAB-001-01 |

The parent’s accepted-version association must be checked separately.
Step-by-step reasoning
Step 1 — Establish the action ceilings
Profiles define which modules and actions are available.
Finance can edit packet modules but only view commercial identity modules.
Service can view selected packet context but cannot edit the modules.
Step 2 — Establish record routes
Private defaults prevent peer access from appearing automatically.
The Finance group and rules provide the intended cross-functional route.
Mia receives only selected Northbank records.
Step 3 — Establish field authority
Sales preparation access does not include Finance-field write access.
Finance record-write access does not include snapshot correction.
Step 4 — Test with the actual business identities
Ava edits the temporary version’s name to:
Northbank access test — checked by Sales
She cannot edit Accepted At.
Leo can enter the supplied acceptance values on the temporary version, then update its parent.
Noor can view but not edit.
Mia cannot open the private laboratory version, because it has not been directly shared and she is not a Finance-group member.
Step 5 — Verify stored values
A denied action is successful evidence only when the attempted value has not been stored.
For example, after Ava’s acceptance attempt, the temporary version remains without Ava-established acceptance.
After Leo’s permitted acceptance, the supplied fields and parent association can be verified.
Mistake and correction
Mistake: Put Leo in a role above Ava so that Finance can see her records.
Correction: Keep Finance parallel to Sales and use S01–S05 for the defined handoff access.
This preserves Noor’s monitoring hierarchy without using managerial access as a substitute for cross-functional sharing.
## 5. Try it yourself — Guided practice

Learning goal
Configure the role, profile, field and sharing model, then demonstrate permitted and denied actions for the representative users.
Access and materials
You need:
- The training CRM organisation.
- Isha’s administrative permissions.
- Five controlled user identities.
- The Chapter 4 base records or the supplied reconstruction.
- Entitlement for the required sharing and field controls.
- Separate browser sessions for the tested users.
If Mia or Noor is not yet provisioned, use Chapter 3’s onboarding procedure and controlled-login mapping.
Do not test a business restriction while signed in as Isha.
Additional audit-test input
Northbank’s Account Description may already contain laboratory information.
Preserve its exact existing value before the test.
Ava appends this supplied line:
Training access check: Ava verified Northbank context.
After evidence is captured, restore the original Description.
This produces a documented Account update without changing the supplied customer name or business ID.
Blank access-test worksheet
| Test | Identity | Record or feature | Attempt | Expected result |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Use Observed, Expected or Blocked for evidence status.
Required tests
| Test | Identity | Attempt |
| --- | --- | --- |
| A01 | Ava | Open and edit Version Name on MER-PVER-LAB-001-01 |
| A02 | Ava | Attempt to edit Accepted At on that version |
| A03 | Leo | Open MER-PVER-LAB-001-01 and enter the supplied acceptance values |
| A04 | Leo | Attempt to edit Billing Email Snapshot on that version |
| A05 | Leo | Attempt to open MER-PVER-LAB-002-01 |
| A06 | Mia | Open MER-PVER-001-01; inspect visible context and hidden billing fields |
| A07 | Mia | Attempt to open MER-PVER-002-02 |
| A08 | Noor | Open MER-ORD-LAB-002; attempt to change Packet Name |
| A09 | Ava | Attempt to delete MER-PVER-LAB-001-01 |
| A10 | Ava | Attempt to open profile or sharing administration |
| A11 | Ava | Append the supplied Northbank Account Description line |
| A12 | Noor | Inspect Ava’s applicable Account-update audit entry |
| A13 | Leo | Attempt to inspect Ava’s peer audit activity |
| A14 | Isha | Change the draft laboratory version’s owner from Ava to Leo, inspect access, then restore Ava |

For A14, transfer only MER-PVER-LAB-002-01.
Do not change its parent owner, Access Scope, timestamps or historical records.
Guided configuration sequence
Step 1 — Record the before state
Capture:
- Existing hierarchy preference.
- User role/profile assignments.
- Default sharing settings.
- Existing record owners.
- Any existing direct shares or relevant rules.
Expected result: you can explain which change produced each later test result.
Step 2 — Create and assign the roles
Create Meridian Process Lead, Sales, Finance and Service in the supplied hierarchy.
Leave peer sharing off.
Expected result: Sales, Finance and Service are parallel roles below Noor’s process role.
Step 3 — Create the profiles
Clone Standard into the four named profiles.
Apply the module and tool-permission matrix.
Update the user assignments through the documented user editor.
Expected result: ordinary users have the intended action ceilings.
Step 4 — Enable module and layout access
Chapter 4 initially limited the custom build modules to administrator access.
Use each custom module’s Module Permission control to include the appropriate custom profiles.^fields
Check Standard-layout assignment where the interface presents layout permissions.
Expected result: the module can be used by the intended profiles; record sharing still determines which records appear.
Step 5 — Configure field restrictions
Apply the field matrix, including the Supporting References Evidence Note restriction for Service.
Set Draft defaults and the Access Scope default.
Expected result: preparation and Finance fields have different write authorities.
Step 6 — Set Private defaults and create the Finance group
Set the listed customer-process modules to Private.
Create Meridian Finance Reviewers with Leo as its only member.
Inspect effective membership.
Expected result: no unintended ordinary user receives Finance-group access.
Step 7 — Assign owners and scopes
Transfer the listed base records to Ava.
Set Finance review on the historical Order Packets and Versions.
Create the two laboratory packets and versions using the supplied inputs.
Expected result: each record has the intended owner, scope and relationships.
Step 8 — Configure S01–S05
Create the completed sharing rules.
Complete the execution or recalculation action required by the environment.
Expected result: Leo receives the intended records but not the Internal draft laboratory version.
Step 9 — Share the four Northbank records with Mia
Use direct Read Only sharing without related lists.
Expected result: Mia can open the specified Northbank context while Redwood remains outside her record scope.
Step 10 — Run A01–A13
Use separate identities and fresh record views.
Record denied controls as unavailable, read-only or rejected according to what the interface actually presents.
Do not invent an error message.
Expected result: permitted edits succeed and denied edits leave the stored values unchanged.
Step 11 — Demonstrate ownership as a separate route
For A14, Isha changes the private laboratory version’s owner to Leo.
Have Leo reopen it.
Expected result: Leo can now open the record through ownership despite its Internal draft classification.
His Finance snapshot restrictions still apply.
Restore Ava as owner and recheck. Once access changes have applied, Leo should again lack a route to that private version.
Step 12 — Inspect audit evidence and reconcile
Inspect the actual test-period Account update.
Restore Northbank’s original Description.
Compare the final roles, profiles, owners, scopes and shares with the target artifacts.
Expected result: the evidence distinguishes hierarchy, ownership, sharing, profile and field behavior.
Final artifacts
Create:
- C01_CH05_Meridian_Access_Matrix.md
- C01_CH05_Meridian_Roles_and_Profiles.md
- C01_CH05_Meridian_Sharing_Register.md
- C01_CH05_Meridian_Access_Tests.md
- C01_CH05_Meridian_Audit_Evidence.md
Cleanup
Restore the private laboratory version’s owner to Ava.
Restore Northbank’s Description.
After capturing evidence, remove the clearly identified laboratory versions and packets using Isha’s access. Clear the laboratory parent’s Accepted Version selection before removing its referenced version.
Keep the base case records and the configured role/profile/sharing design.
Offline alternative
Use the complete matrices and records to work through the expected access decisions on paper.
This demonstrates your reasoning but cannot demonstrate saved permissions, sharing execution, actual field hiding, denied actions or audit visibility.
Mark those results Expected or Blocked.
## 6. Independent challenge — Temporary review and overlapping access

A temporary observer, Quinn, must inspect Northbank’s packet without editing it.
Use a paper copy of the access design.
Complete inputs
| Item | Supplied value |
| --- | --- |
| User | Quinn Vale |
| Business user reference | MER-USR-010 |
| Synthetic email | quinn.vale@example.com (mailto:quinn.vale@example.com) |
| Organisation/app status | Active in the intended training CRM |
| Role | Meridian Finance, parallel to Sales |
| Profile | Meridian Finance Observer |
| Module permissions | View only for Accounts, Contacts, Order Packets and Packet Versions |
| Edit/Create/Delete | Off for those modules |
| Field permissions | Read Only for visible review fields; no field-write authority |
| Ownership | Quinn owns no case records |
| Territory or Deal Team route | None |
| Public defaults | Private |

The proposed temporary access is:
- Northbank Account.
- Taylor’s Contact.
- Northbank Order Packet.
- Northbank accepted Packet Version.
- No Redwood records.
Quinn is not added to Meridian Finance Reviewers, because that group’s rules include both customer cases.
Instead, a CRM group Northbank Review Observers contains Quinn and has Read Only direct sharing to the four specified Northbank records.
An accidental second share gives Quinn Read/Write access directly to MER-ORD-001.
Changed conditions
1. Quinn attempts to edit Packet Status.
2. Isha removes the accidental direct Read/Write share.
3. Quinn still opens the packet through Northbank Review Observers.
4. At the end of the review, Quinn is removed from that group.
5. No other record-access route exists.
Deliverables
Create C01_CH05_Temporary_Observer_Challenge.md containing:
1. A corrected access plan.
2. The expected result of Quinn’s edit attempt.
3. An explanation of why removing the accidental share does not immediately remove all read access.
4. The final action that removes the remaining route.
5. A verification checklist for Northbank and Redwood.
6. An explanation of why adding Quinn to the existing Finance group would grant the wrong record scope.
7. A statement distinguishing the actual actor from a typed Reviewer Reference.
Success criteria
The observer must have the supplied read-only action ceiling and Northbank-only record scope.
The departure check must account for every supplied access route.
## 7. Common problems and recovery

| Symptom | Likely cause | Correction |
| --- | --- | --- |
| Finance sees every private Sales draft | Public defaults, hierarchy placement or a broad rule grants access | Inspect and correct the broad route |
| Finance sees no packets | Missing module/layout access, group membership or rule execution | Check those layers in order |
| Sales can enter Accepted At | Wrong profile or field permission | Restore Sales Read Only on Finance fields |
| Finance can alter the billing snapshot | Finance field permission is too broad | Set snapshot fields Read Only |
| Service sees a billing email in evidence text | Main field was hidden but alternate text remained visible | Hide the Evidence Note column and inspect other representations |
| Service sees Redwood | Another share, group or broad default applies | Trace all routes and remove the unintended grant |
| Noor can edit a subordinate record | Operations profile has Edit permission | Remove the unintended action permission |
| User loses access after owner transfer | Ownership was the only record route | Establish the intended sharing or restore the correct owner |
| Removing a direct share does not remove access | Group, hierarchy, territory or indirect sharing remains | Inspect every route |
| Profile test passes only in preview | Preview was treated as execution evidence | Test with the actual user session |
| A02 fails because a required field is missing | Validation failure is being confused with permission denial | Use the complete test inputs and inspect field editability |
| Audit filter finds no test update | Wrong entity, actor or date range | Use the actual laboratory update period |
| No audit entry appears for a denied click | Denied attempts are not assumed to be logged | Use direct test evidence |
| An administrator passes every denied test | Wrong test identity | Use the intended ordinary user |
| Service cannot open a linked Deal | Deal module permission is intentionally absent | Use the selected customer/packet context |

Correct the specific layer that is wrong.
For example, changing Finance’s profile to Administrator might make the packet open, but it does not repair the intended sharing rule.
## 8. Check your understanding

 1. What is the difference between a role and a profile?
 2. Why can Noor see Ava’s records without being permitted to edit them?
 3. Which access routes let Leo see Finance review packets?
 4. Why does Access Scope not prove that a packet is complete?
 5. Ava owns a version. Can ownership override her read-only Accepted At field?
 6. Why should the Northbank direct share omit related lists in this exercise?
 7. A record has one Read Only share and another Read/Write share. What must you inspect before expecting read-only behavior?
 8. Why is a CRM group not the assigned owner of the packet?
 9. What changes when the private laboratory version is assigned to Leo?
10. Does shared Account access automatically provide another user’s audit-log visibility?
11. Why is a territory not simply another name for a role?
12. What evidence is needed to demonstrate a denied acceptance action?
## 9. Solutions and explanations

Lesson checks
| Check | Explained answer |
| --- | --- |
| L1 | Inspect the field permission for Finance first. Opening the record already demonstrates module View and a record route. Module Edit and record write access should also be confirmed, but the supplied design deliberately makes the billing snapshot Read Only. |
| L2 | A superior role supplies broad hierarchical visibility. The requirement is a selected cross-functional handoff, so sharing should establish that route without redefining managerial access. |
| L3 | The same address can appear in the note. Hiding one field does not satisfy the information boundary if another visible field repeats it. |
| L4 | Public Read/Write supplies broader access to other users’ records. A narrow rule does not remove that default grant. |
| L5 | No. The group route remains. Remove or revise the applicable group access and verify all other routes. |
| L6 | A territory selects customer coverage using business criteria. A role places a user in a hierarchy. Northbank is a customer record, not a subordinate employee role. |
| L7 | The audit entry records the current update event. The September field value is historical business data, not the date the laboratory user edited the Account. |

Guided practice — Completed expected test results
| Test | Expected result |
| --- | --- |
| A01 | Permitted |
| A02 | Denied or read-only |
| A03 | Permitted with complete values |
| A04 | Denied or read-only |
| A05 | No record access |
| A06 | Selected context visible; billing and reviewer fields hidden |
| A07 | No record access |
| A08 | View permitted; edit denied |
| A09 | Delete denied or unavailable |
| A10 | Administration denied or unavailable |
| A11 | Permitted |
| A12 | Applicable subordinate audit entry visible |
| A13 | Peer activity not made visible by Account sharing |
| A14 | Leo gains owner access; snapshot remains read-only; restored owner removes that route |

These are expected results. A completed live evidence file records the learner’s actual observations.
Completed ordinary-user action matrix
Action
Edit permitted preparation fields on an accessible version
Read Finance outcome on an accessible version
Establish supplied Finance outcome on an accessible test version
Read billing email on an accessible version
Edit billing-email snapshot under the preparation profile
Delete case versions
Change record owners
Administer profiles and sharing
“Accessible” matters. A field permission does not give a user access to a record that has no valid record route.
Completed sharing register
| Record category | Route | Recipient |
| --- | --- | --- |
| Sales-owned customer context | S01–S03 | Finance Reviewers |
| Finance review Order Packets | S04 | Finance Reviewers |
| Finance review Packet Versions | S05 | Finance Reviewers |
| Four specified Northbank records | Direct sharing | Mia |
| Ava-owned process records | Role hierarchy | Noor |
| Any record administered for the exercise | Administrator profile | Isha |

A complete denied-action evidence example
| Evidence element | What the learner records |
| --- | --- |
| Test | A02 |
| Identity | Ava, MER-USR-002 |
| Role/profile | Meridian Sales / Meridian Sales |
| Record | MER-PVER-LAB-001-01 |
| Attempt | Change Accepted At |
| Expected | Field is read-only or change is denied |
| Observation | Actual interface or save behavior |
| Stored-value check | Accepted At remains unchanged after the attempt |
| Evidence reference | Learner’s redacted capture or precise written observation |
| Status | Observed only after the live check |

The actual wording of a product message must come from the observation.
Independent challenge — Completed solution
Corrected observer design
Keep Quinn:
- Active in the intended CRM.
- In the parallel Finance role.
- On the Finance Observer profile with View only.
- In Northbank Review Observers.
- Outside Meridian Finance Reviewers.
Share only the four supplied Northbank records with the observer group.
Quinn’s edit attempt
The attempted Packet Status edit is denied or unavailable.
Although an accidental direct share supplies Read/Write record access, Quinn’s profile has no module Edit permission.
The record grant does not override the profile action ceiling.
Removing the accidental share
After removing the direct Read/Write entry, Quinn still has Read Only access through Northbank Review Observers.
This is expected. The record remains reachable through another route.
Ending the review
Remove Quinn from Northbank Review Observers and verify its effective membership.
The inputs establish:
- Quinn owns no records.
- Quinn is not above Ava.
- Defaults are Private.
- No territory or Deal Team route exists.
- The accidental direct share has been removed.
Therefore, after the remaining group route is removed and the change applies, Quinn should no longer open the Northbank records.
Verification checklist
Check
Before review ends: open Northbank Account
Before review ends: edit packet status
Before review ends: open Redwood
After direct-share removal: read Northbank
After group removal: open Northbank
Inspect effective group membership
Why the existing Finance group is wrong
S01–S05 provide Finance access covering both Northbank and Redwood.
Quinn’s requirement is Northbank-only observation. Adding Quinn to the broader group would violate the supplied record scope even if the observer profile prevented editing.
Action scope and record scope must both fit.
Actor versus assertion
A typed Reviewer Reference such as MER-USR-003 is record content.
The actual signed-in actor is established by the identity performing the action and the available system evidence.
Quinn’s ability to read Leo’s reference does not make Quinn the reviewer. A manually typed reference does not substitute for actor evidence.
Understanding questions
1. Role: hierarchy and associated record reach. Profile: permitted actions, modules and features.
2. The hierarchy supplies visibility; the read-only profile limits actions. Both settings contribute to the result.
3. Leo has matching S04/S05 sharing through Meridian Finance Reviewers, along with the required profile permissions.
4. It is a sharing classification. Completeness depends on the packet information and validation; acceptance depends on the permitted Finance action.
5. No. The ordinary profile’s field restriction remains applicable.
6. The requirement is selected context. Including related lists can expose additional records and create another access route that must be justified.
7. Inspect all grants and the profile/field ceilings. A broader route can remain effective even when one entry is Read Only.
8. CRM groups extend access to user-owned records. The documented model retains a user as the record owner.
9. Leo gains an ownership route. His Finance snapshot fields remain read-only. Restoring Ava removes that owner route.
10. No. Audit visibility has its own documented user/subordinate scope.
11. A territory follows customer coverage criteria. A role follows the user hierarchy.
12. Test as the intended ordinary identity, attempt the action, record the observed result and verify the stored value did not change. An administrator screenshot or a layout preview is insufficient.
## 10. Chapter recap and next step

Appropriate access is built from several complementary controls:
- Roles determine hierarchical record reach.
- Profiles define action ceilings.
- Field permissions distinguish reading from writing.
- Ownership supplies responsibility and a record-access route.
- Private defaults establish the starting boundary.
- Sharing rules and direct shares provide deliberate collaboration.
- Groups, Deal Teams and territories can add further routes.
- Audit visibility helps investigate supported events.
Meridian’s design lets Sales prepare, Finance review, Service see selected Northbank context and Operations monitor.
It also provides meaningful denied actions: Sales cannot write Finance fields, Service cannot edit packet records, Finance cannot correct the billing snapshot, and ordinary users cannot administer the access model.
“I can…” completion checklist
- I can explain role and profile differences.
- I can configure ordinary business profiles.
- I can separate record scope from action scope.
- I can apply field restrictions for preparation and review.
- I can configure Private defaults and targeted sharing.
- I can inspect ownership and effective group membership.
- I can explain how overlapping access routes affect a result.
- I can demonstrate a permitted action and a denied action.
- I can distinguish audit evidence from a typed historical reference.
Your access matrix and test evidence become part of the course project’s configuration and user-acceptance evidence.
The next chapter, Data Preparation and Migration, uses the data model and access design to prepare, import and reconcile deliberately messy records. It will also distinguish ordinary manual-entry validation from import behavior.
## 11. Glossary and further reading

Glossary
| Term | Meaning |
| --- | --- |
| Access route | A reason a user can reach a record, such as ownership, hierarchy or sharing |
| Action ceiling | The maximum actions permitted by the applicable profile and field controls |
| Audit log | Recorded supported CRM actions, viewed within the permitted scope |
| Criteria-based sharing | Sharing records selected by field conditions |
| Deal Team | Contributors associated with a particular commercial opportunity |
| Direct sharing | Sharing a specific record with identified users, roles or groups |
| Field permission | Whether a profile may read, write or see a field |
| Group | A defined collection of users or supported membership structures |
| Indirect sharing | Access supplied through a related-record sharing route |
| Organisation-wide permission | A module’s default record-access model |
| Owner-based sharing | Sharing selected by the record owner’s role or group |
| Private | A starting record-access model that can be extended by permitted routes |
| Profile | A collection of module, action and feature permissions |
| Read Only | Permission to view without the corresponding edit grant |
| Record owner | The assigned CRM user responsible for a record |
| Role | A position in the CRM hierarchy |
| Territory | A customer-coverage structure defined using business criteria |
| Teamspace | A workspace arrangement for modules and work areas |
| Verification | Checking the actual stored or accessible result against the requirement |

Further reading
The official sources were accessed for the procedures and distinctions in this chapter. No Meridian product execution is claimed.
The role and sharing procedures here apply to organisation modules. The official documentation distinguishes team modules, which have a different team-profile access model.
Direct sharing, field permissions, territories and Deal Team features have edition or rollout dependencies. Verify the actual training entitlement before configuring them.
^roles: Zoho CRM, Managing Roles (https://help.zoho.com/portal/en/kb/crm/security-control/role-management/articles/role-management-introduction), including hierarchy behavior, peer sharing, profile dependencies and Administrator access.
^hierarchy: Zoho CRM, Manage Hierarchy Preference (https://help.zoho.com/portal/en/kb/crm/organization-settings/company-settings/articles/crm-setup-hierarchy-preference).
^createprofiles: Zoho CRM, Creating Profiles (https://help.zoho.com/portal/en/kb/crm/security-control/profile-management/articles/create-profile).
^profiles: Zoho CRM, Managing Profile Permissions (https://help.zoho.com/portal/en/kb/crm/security-control/profile-management/articles/manage-profile-permissions), including basic actions, tools, administration and immediate permission changes.
^fields: Zoho CRM, Working with Custom Fields (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-fields/articles/use-custom-fields) and Customizing Organization Modules (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/customizing-modules/articles/customize-modules).
^subforms: Zoho CRM, Building a Subform (https://help.zoho.com/portal/en/kb/crm/customize-crm-account/managing-subforms/articles/build-subforms), particularly column permissions and supporting information.
^rules: Zoho CRM, Setting up Data Sharing Rules (https://help.zoho.com/portal/en/kb/crm/security-control/manage-data-sharing/articles/data-sharing-rules).
^sharing: Zoho CRM, Sharing Records (https://help.zoho.com/portal/en/kb/crm/security-control/manage-data-sharing/articles/share-records), including grant levels, related-list sharing, overlapping routes and revocation.
^ownership: Zoho CRM, Common Operations with Records (https://help.zoho.com/portal/en/kb/crm/manage-crm-data/record-management/articles/common-operations-with-records), particularly Change Record’s Owner.
^groups: Zoho CRM, Create and Manage Groups (https://help.zoho.com/portal/en/kb/crm/security-control/group-management/articles/create-groups).
^dealteam: Zoho CRM, Enhance Sales Collaboration with Team Selling and Deal Split (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/deal-management/articles/team-selling-and-deal-split). Only the Team Selling access concepts are used here.
^territories: Zoho CRM, Territory Management — An Overview (https://help.zoho.com/portal/en/kb/crm/security-control/territory-management/articles/territory-management) and Using Territories (https://help.zoho.com/portal/en/kb/crm/security-control/territory-management/articles/use-territories).
^audit: Zoho CRM, Monitoring Audit Log (https://help.zoho.com/portal/en/kb/crm/security-control/audit-log/articles/monitor-audit-log).
