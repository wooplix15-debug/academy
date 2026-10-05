# Organisation and User Administration

## 1. What you will learn

An application can be correctly selected and still be difficult to use because its organisation settings or user administration are wrong.
Consider these situations:
- Sales creates an activity for 09:00, but another user sees a different local time.
- An administrator assumes that a date written as 10/11/2026 means 11 October, while the user intended 10 November.
- A new Finance user receives an invitation but never joins the intended organisation.
- A service user receives administrator access because it was the quickest way to make an application open.
- A departing employee is deactivated before their application or integration ownership is transferred.
- A reminder is expected during working hours, but its timing uses elapsed hours rather than a business calendar.
These problems are not primarily about coding. They are about establishing a reliable operating environment.
In this chapter, you will learn how to configure the organisational foundation and manage the lifecycle of users who work within it.
By the end, you should be able to:
 1. Identify the correct training organisation and application account before changing settings.
 2. Configure organisation information and distinguish organisational settings from personal preferences.
 3. Explain locale, date formats, time zones and currency settings.
 4. Configure CRM business hours and a synthetic holiday calendar.
 5. Add users, check their joining status and assign the intended applications.
 6. Organise participants into a cross-functional team without confusing team membership with business authority.
 7. Configure an allowed multi-factor authentication method and its recovery.
 8. Follow a documented user-deactivation procedure.
 9. Prepare onboarding, role-change and offboarding checklists.
10. Record actual configuration evidence without treating an expected result as an observation.
Prerequisites
You should understand Chapter 2’s application map:
- CRM is the proposed home for sales relationships and confirmed-order packet history.
- Books owns financial records.
- Desk owns service tickets.
- People holds separate employee and HR work.
- Flow supports defined cross-application actions.
- Analytics supports reporting.
- Zoho One provides organisation and application-access administration.
You need basic web application skills. No coding is required.
For the live practice, you need a dedicated training environment and the permissions described in Section 5. A supplied training organisation is sufficient: this chapter teaches its configuration, rather than requiring you to purchase a subscription or create a production organisation.
Continuity and new training assumptions
Chapter 2 introduced Isha as the central administrator, while preserving these business authorities:
- Ava prepares and corrects Sales packets.
- Leo alone establishes Finance acceptance.
- Mia manages Service work.
- Noor owns process improvement.
- Omar coordinates the separate HR exercise.
- Ren makes its leave decisions.
The application design remains proposed. The earlier chapters do not establish that any case record has been created in a live application.
This chapter adds the following explicit training configuration decisions:
| Setting | Meridian training decision |
| --- | --- |
| Human-readable environment label | MER-TRAIN-ORG |
| Organisation display name | Meridian Supply — Training |
| Language | English |
| Country locale for the training examples | United Kingdom |
| CRM organisation time zone | UTC, using the available equivalent zero-offset time-zone option |
| Main working week | Monday–Friday |
| Main working hours | 09:00–17:00 UTC |
| Week starts | Monday |
| Home currency | GBP |
| Additional currencies | None required for the base exercise |
| Synthetic business closure | 12 October 2026: Meridian training maintenance closure |
| Pilot team | Meridian Handoff Pilot |
| Pilot application | CRM |
| Pilot users | Ava and Leo, administered by Isha |
| Invitation route | Controlled training email addresses, without assuming a verified corporate domain |
| MFA exercise | OTP Authenticator, where permitted by the organisation’s policy |

The United Kingdom locale and GBP are synthetic course-case choices. They do not establish Meridian’s legal jurisdiction, tax treatment or a required Books country edition.
MER-TRAIN-ORG remains a planning label. It is not a product-generated organisation ID.
Your contribution to the project
You will produce:
- An organisation-settings record.
- An identity and application-assignment register.
- A team-membership record.
- A user-lifecycle checklist.
- Configuration and access evidence.
These make the later CRM data model and access controls usable. They also establish who should administer the connected process when users join, change jobs or leave.
## 2. Lessons

### Lesson 1 — Establish the correct organisation before configuring it

An organisation is the account context in which a group of users and its application configuration operate.
In a connected solution, there are several related contexts:
1. The Zoho One organisation.
2. The CRM organisation associated with that solution.
3. Other application organisations, such as a Books organisation.
4. Each individual user’s Zoho identity.
Do not assume that the display name is a sufficient identifier. Two environments can have similar names, and one user may belong to more than one account context.
An organisation register records the relationship between the human-readable training label and the actual account information you observe.
| Context | Planning label | Information to record during live work |
| --- | --- | --- |
| Suite administration | MER-TRAIN-ORG | Actual Zoho One organisation identification and regional sign-in context |
| CRM | Meridian Supply — Training CRM | Actual CRM organisation identification and associated account |
| Books | Later finance environment | Not connected or configured by this exercise |
| Pilot identities | Ava, Leo and Isha | Actual controlled login identities used for their laboratory roles |

The register is useful before imports, integrations or user invitations. A correct configuration applied to the wrong organisation is still an incorrect result.
What you configure first
The organisation profile provides basic identity information such as the company name, primary location and contact information.
In Zoho One’s documented One Experience UI, an Organisation Owner or Organisation Admin can:
1. Sign in to the intended Zoho One organisation.
2. Open the Admin Panel.
3. Select Organization.
4. Click Edit under Organization Info.
5. Modify the required information.
6. Click Update.^org
For this exercise, change the display name to Meridian Supply — Training. Preserve an existing training portal URL unless there is a specific reason to change it.
Expected result: reopening Organisation Info shows the saved training name.
Recovery: if you edited the wrong display value in the correct dedicated training organisation, restore the recorded previous value. If you are in the wrong organisation, leave that editing session and establish the correct context before continuing.
Adding an application is an account-association decision
In the documented One Experience UI:
1. Open Admin Panel → App Management.
2. In Applications, select + Add Application → Add Zoho Apps.
3. Select Add beside the required application.
4. If offered existing accounts or Create a New Account, identify the intended training account before proceeding.
5. Assign the required users through the documented application-assignment process.^addapp
The official help states that the selected application account cannot simply be changed later without support.
This is an important distinction from editing a display name. A display-name correction and an application-account association are different changes with different recovery paths.
For Meridian, begin with CRM. Do not attach an existing operational CRM account merely because it appears first in the list.
Worked example
Isha sees two CRM choices:
- An existing operating-business account.
- A dedicated Meridian training account.
The correct choice is the dedicated training account, even if both are accessible to Isha.
Ava and Leo’s laboratory work should not create training users or sample configuration in the operating-business account.
Check L1: Why should you record both the training display name and the actual application-account association?
### Lesson 2 — Separate organisation settings from personal locale

A locale is a set of regional presentation conventions. It can influence language, date formatting, number formatting and other displayed values.
A time zone determines how a timestamp is represented as local time. It is not the same as a date format.
Compare:
- 2026-10-13T09:00:00Z: an explicitly identified UTC timestamp.
- 13/10/2026: a date displayed day-first.
- 10/13/2026: the same date displayed month-first.
Changing the display format does not change which calendar date the record represents.
Organisation-level settings
CRM’s documented company-settings procedure is:
1. Sign in with an Administrator profile.
2. Open Setup → General → Company Settings.
3. Use the appropriate edit control for the company information.
4. Save the changes.^crmcompany
For the organisation time zone:
1. In Company Settings, locate Locale Information.
2. Click its edit control.
3. Select the intended Time Zone.
4. Click Save.^crmcompany
The official documentation states that the organisation time zone is used in calculating a day for workflow rules. This is why it is more than a visual preference.
Expected result: the saved organisation time zone represents UTC for Meridian’s base exercise.
Recovery: if the selected zone is wrong, correct it before creating timing-dependent automation. Record what changed so that later tests use the correct basis.
Personal settings
Users also have personal locale preferences. CRM documents the following route:
Setup → General → Personal Settings → Locale Information → Edit
The user can select:
- Language.
- Country Locale.
- Date Format.
- Time Format.
- Time Zone.
- Number grouping and decimal options.
Then select Save.^personal
For the base pilot, Ava and Leo use:
| Personal preference | Target |
| --- | --- |
| Language | English |
| Country locale | United Kingdom |
| Date format | Day/month/year |
| Time format | 24-hour |
| Time zone | UTC |
| Number grouping | Comma |
| Decimal separator | Full stop |

The exact date-format label may use different capitalization. Select the option that displays a known date such as 13 October 2026 in day-first order.
Expected result: a known October date is displayed consistently with the selected format, and time is shown using the chosen personal zone.
Worked example: one instant, two local displays
Suppose an event occurs at:
2026-10-13T09:00:00Z
For this paper example, a second user has a supplied fixed offset of UTC+02:00.
Local time = UTC time + offset
09:00 + 2 hours = 11:00
Both displays refer to the same instant.
It would be wrong to “correct” the source event to 11:00 UTC merely because the second user sees 11:00 locally.
Real regional time zones may change offset seasonally. This example uses a fixed supplied offset, so it requires no daylight-saving assumption.
Ambiguous dates need an agreed interpretation
10/11/2026 is ambiguous without a known format.
Under Meridian’s day-first rule:
- Day = 10.
- Month = 11.
- Year = 2026.
- Meaning = 10 November 2026.
Use ISO-style dates such as 2026-11-10 in the course’s CSV datasets and configuration records where possible. This reduces ambiguity when data crosses applications.
Common mistake: changing the organisation time zone to satisfy one user’s display preference. Change the user’s personal preference when that is the actual problem.
Check L2: A UTC+02:00 user sees a 09:00 UTC event at 11:00. Has the event moved two hours later?
### Lesson 3 — Configure currencies deliberately

A home currency is the primary currency used by the organisation. A record currency is the currency associated with a particular record.
An exchange rate defines how an amount in one currency relates to another.
Currency labels are not interchangeable decorations. An amount of 1,000 GBP is not the same financial statement as 1,000 USD.
Meridian’s decision
The base training organisation uses GBP.
No earlier Meridian dataset supplied commercial amounts or an approved home currency. Therefore, this is a new explicit case decision, not a reinterpretation of an established financial record.
Before confirming it, check that the dedicated CRM training organisation is suitable for this decision.
Documented CRM procedure
Users need the Manage Currencies permission to administer the Currencies settings.
The documented route is:
Setup → General → Company Settings → Currencies
The accessed documentation describes confirming the suggested home currency or changing it before confirmation. It also describes currency-format options such as code or symbol, digit separator and decimal places.^currency
For the exercise:
1. Open Currencies.
2. Identify the current home-currency state.
3. If GBP is already confirmed, record that state.
4. If it is not yet confirmed, select or confirm GBP using the documented home-currency controls.
5. Use a readable format with two decimal places.
6. Save the applicable settings.
Expected result: the organisation’s confirmed home currency is GBP.
Why this step needs more care than changing a name
The official help states that home-currency confirmation is not an ordinary reversible edit. Its documented change warning also explains that currency codes can change while existing numeric values remain unchanged.
Suppose a record contains:
1,000 USD
Changing its label to GBP without converting the value would yield:
1,000 GBP
That is relabeling, not exchange-rate conversion.
Therefore, if an existing training account already has a different confirmed home currency, do not treat the exercise as permission to relabel populated records. Use a correctly prepared empty training environment or resolve the account choice with its administrator.
This recovery follows from the documented behavior of the currency feature.
Multiple currencies
The accessed CRM help describes multiple-currency support for paid editions and notes that adding additional currencies activates a feature that cannot simply be switched off afterward.^currency
Meridian’s base exercise does not need an additional currency. You should still understand when one would be useful: for example, when a commercial opportunity must be expressed in a customer’s currency while reporting uses the organisation’s home currency.
Consider this complete paper example:
- Home currency: GBP.
- Record currency: EUR.
- Record amount: EUR 1,000.
- Supplied synthetic rate: GBP 0.85 for EUR 1.
Home amount = record amount × home-currency units per record-currency unit
EUR 1,000 × GBP 0.85/EUR = GBP 850
The EUR units cancel, leaving GBP.
The exchange rate is synthetic. It is not a current market rate, and this chapter does not configure automatic rate updates.
Common mistake: adding amounts from different currencies before defining how they are converted.
Check L3: Why would changing 1,000 USD to 1,000 GBP without changing the number not demonstrate currency conversion?
### Lesson 4 — Configure business hours, shifts and holidays

Business hours define the working periods used by supported application features.
A shift identifies a particular working schedule and, where applicable, its time zone.
A holiday list identifies dates excluded from normal working availability for the relevant organisation or shift.
These settings describe availability. They do not automatically rewrite every due date, report formula or reminder to use working time.
You must still choose a feature’s business-time option when its documented procedure requires one.
Main CRM business hours
CRM’s documented procedure requires an Administrator profile:
1. Open Setup → General → Company Settings → Business hours.
2. Select Create Business Hour.
3. Select Custom hours.
4. Choose Same hours every day.
5. Set 09:00–17:00.
6. Select Monday–Friday.
7. Set Monday as the beginning of the work week where that control is available.
8. Click Save.^hours
Expected result: the saved main schedule shows five working days, each from 09:00 to 17:00.
For this configuration, the organisation time zone is UTC. It aligns the schedule with the UTC timestamps already used in Meridian’s discovery datasets.
Recovery: if Saturday was selected accidentally, edit the schedule and remove Saturday. Reopen the saved schedule to verify the correction.
Holiday configuration
The synthetic closure is:
| Holiday name | Date |
| --- | --- |
| Meridian training maintenance closure | 2026-10-12 |

This is not a national-holiday claim.
The documented holiday-list procedure is:
1. Open Setup → Company Settings → Holidays.
2. Select Create Holiday List.
3. Choose 2026.
4. If shifts exist, use Apply To to identify the intended shift scope.
5. Enter the holiday name and date.
6. Click Save.^hours
The help explains that a holiday list created before shifts can apply to shifts created later. This makes creation order and scope worth recording.
Expected result: the saved list contains 12 October 2026, and its scope is understood.
Recovery: edit the holiday list if the date, year or scope is wrong. Confirm the saved result rather than relying on what was typed before saving.
Shifts
CRM’s documented shift procedure uses:
Business Hours → + New Shift Hours
You enter a shift name, choose its time zone and working hours, add the relevant users and save.^hours
A shift can be useful when a service group works different hours from the main team.
However, the documentation notes that inconsistent organisation and shift hours can produce an alert. Do not assume that any proposed shift can be added independently of the organisation’s schedule.
Meridian’s base pilot uses one schedule. An additional shift is unnecessary unless a supplied requirement establishes different availability.
Worked example: elapsed time versus working time
Use these supplied inputs:
- Start: Friday, 9 October 2026, 16:30 UTC.
- Working schedule: Monday–Friday, 09:00–17:00 UTC.
- Saturday and Sunday are non-working.
- Monday, 12 October, is the supplied closure.
- Required interval: two working hours.
- No other holiday applies.
- No break interval is excluded.
Two working hours equal:
2 × 60 = 120 working minutes
Friday contributes:
17:00 − 16:30 = 30 working minutes
Remaining:
120 − 30 = 90 working minutes
The next working opening is Tuesday, 13 October, 09:00 UTC.
09:00 + 90 minutes = 10:30 UTC
Therefore, the paper due time is:
Tuesday, 13 October 2026, 10:30 UTC.
Elapsed clock time is different:
90 hours × 60 = 5,400 elapsed minutes
The working interval is 120 minutes, while the elapsed interval is 5,400 minutes.
This calculation establishes the expected business-calendar result. It is not evidence that an automation has been configured to use it. Chapter 9 will configure and test scheduled actions.
Check L4: Why would a simple “add two elapsed hours” operation produce a different result from this working-time calculation?
### Lesson 5 — Add users, assign applications and organise teams

A user identity establishes who signs in. An application assignment establishes which application that identity may use.
A business responsibility establishes what the person is accountable for.
These should be related, but they are not interchangeable.
Ava needs CRM for Sales work. That does not make her an organisation administrator or the Finance decision owner.
New-user information
Use enough information to identify and place the user correctly:
- Name and display name.
- Correct login email.
- Business or workforce reference where applicable.
- Department and reporting information where supplied.
- Locale and time zone.
- Required applications.
- Joining and access-check status.
Do not fabricate optional personal data merely to fill a form.
The following surnames and user references are explicit additions for the training roster. They do not rename existing business records or replace the separate HR employee IDs.
user_ref,first_name,last_name,synthetic_email,function,base_time_zone,planned_business_apps
MER-USR-001,Isha,Lin,isha.lin@example.com,Central administration,UTC,Zoho One administration;CRM administration;later Flow and Analytics administration
MER-USR-002,Ava,Patel,ava.patel@example.com,Sales,UTC,CRM;own People self-service when implemented
MER-USR-003,Leo,Chen,leo.chen@example.com,Finance,UTC,CRM Finance review;Books when implemented;own People self-service
MER-USR-004,Mia,Reed,mia.reed@example.com,Service,UTC,Desk when implemented;restricted CRM context;own People self-service
MER-USR-005,Noor,Khan,noor.khan@example.com,Operations,UTC,CRM operations visibility;Analytics when implemented;own People self-service
MER-USR-006,Omar,Malik,omar.malik@example.com,HR coordination,UTC,People HR scope when implemented
MER-USR-007,Ren,Park,ren.park@example.com,HR decision owner,UTC,People manager scope when implemented
For live invitations, map the synthetic addresses to individually controlled training mailboxes. Keep the case reference and the real laboratory login in separate columns.
Do not send invitations to example.com, attempt to verify that domain, or include passwords in the mapping file.
Add a user
An Organisation Owner, Organisation Admin or a custom role with Add Users permission can perform the documented task.
In One Experience UI:
 1. Open Admin Panel → User Management → Users.
 2. Click Add User.
 3. Enter the first name, last name, display name and controlled email address.
 4. Complete supplied company information.
 5. Select Language, Country and Time Zone.
 6. Complete any genuinely required custom fields.
 7. Click Continue where presented.
 8. Choose the applicable existing user-license option.
 9. Retain the intended notification route.
10. Click Add.^users
Expected result: a user record appears with a joining status appropriate to the route used.
For the pilot’s invitation route, an existing-email user may remain Pending until they accept and sign in. A verified-domain route has different joining behavior. Do not assume that “record added” means “user has successfully joined.”
Recover a pending invitation
For a pending user, the documented One Experience route is:
1. Open User Management → Users.
2. Locate the pending user.
3. Open the user.
4. Click Resend.
5. Confirm with Yes, Confirm.^reinvite
Before resending, confirm the intended email and mailbox access. Repeatedly resending to an incorrect address does not resolve the problem.
The official help documents a limit on reinvitation attempts. Use the current account guidance if that limit is reached; do not create another identity simply to bypass the unresolved invitation.
Assign CRM
Organisation Owners, Organisation Admins and Application Admins can use the documented individual-assignment route:
1. Open Admin Panel → App Management → Applications.
2. Select CRM and its action menu.
3. Choose Assign Users.
4. Open the Individual tab.
5. Select the intended user.
6. Set the application-specific options presented.
7. Click Assign.^assign
For Ava and Leo’s pilot access, use an available non-administrator CRM profile suitable for the basic access test, such as the predefined Standard profile. Record the actual role and profile selected.
The detailed Finance acceptance restriction will be configured in later chapters. A generic Standard assignment does not, by itself, implement that business transition.
Expected result: Ava and Leo can enter the intended CRM organisation without receiving company-settings administrator authority.
Teams and groups
A department describes an organisational placement. A collaboration group supports a cross-functional purpose.
Meridian’s handoff team includes Sales and Finance, so a collaboration group is suitable.
The proposed pilot group is:
| Group attribute | Input |
| --- | --- |
| Name | Meridian Handoff Pilot |
| Type | Collaboration Group |
| Description | Coordinates the training order-to-finance handoff |
| Moderator | Isha |
| Members | Ava and Leo |
| Email alias in paper records | meridian.handoff@example.com (mailto:meridian.handoff@example.com) |
| Live alias | An approved training alias available in the controlled environment |

Zoho One documents:
1. Admin Panel → User Management → Groups → Add Group.
2. Enter the name, description and required group email.
3. Select Collaboration Group.
4. Assign moderators and members.
5. Click Create Group.^groups
Expected result: the group has the intended moderator and two ordinary members.
Group membership can support administration and application assignment. It does not prove that the user has a particular CRM record-sharing permission or business approval authority.
In this pilot, assign CRM individually so that the assignment source is clear. Do not use membership in the handoff group to give Ava Finance acceptance authority.
Check L5: If Ava and Leo are both members of the handoff group, why does Leo still retain the Finance decision?
### Lesson 6 — Configure identity controls and recovery

Multi-factor authentication, or MFA, adds another factor to identity verification beyond a password.
An OTP Authenticator generates a time-based one-time password through an authenticator application.
MFA helps establish that the person signing in controls the enrolled factor. It does not decide whether that user may approve a packet or view a financial record.
Configure the user’s factor
The documented Zoho Accounts procedure is:
1. Sign in to the user’s regional Zoho Accounts service.
2. Open Multi-Factor Authentication.
3. Under OTP Authenticator, select Set up Now.
4. Scan the displayed QR code in an approved authenticator application, or enter its setup key using the documented alternative.
5. Click Next.
6. Enter the authenticator’s current OTP.
7. Click Verify.^otp
An organisation policy may restrict which factors can be configured. If OTP Authenticator is not permitted, use the permitted method and its documentation rather than attempting to circumvent the policy.
Expected result: the account shows the factor as configured, and a fresh sign-in uses the applicable MFA challenge.
Keep the QR code and setup key private. They are credentials for enrolling the factor, not student-book evidence.
Generate recovery codes
The documented recovery-code route is:
Zoho Accounts → Multi-factor Authentication → MFA Recovery Options → Generate new codes
Save the generated codes privately.^backup
The documentation establishes that:
- Each recovery code can be used once.
- Newly generated codes invalidate the old unused set.
- Organisation policy can restrict generation or use.
Your course artifact should record only:
Recovery method established and tested.
Do not paste actual codes into project files.
Test recovery without destroying the working factor
For a controlled OTP test account:
1. Keep the normal authenticator configured.
2. Start a separate, fresh sign-in.
3. Use the documented Can’t access your device? route, or the Problem signing in? route followed by that option.
4. Select Use backup verification codes.
5. Enter one unused code.
6. Verify access.
7. Record that the recovery sign-in succeeded.
8. Preserve the remaining recovery arrangement.^backup
This demonstrates an alternate recovery route. It does not require deleting the authenticator or losing a device.
Administrator reset is a different recovery
Zoho One’s documented Reset MFA clears the existing MFA configuration and requires reconfiguration at the next sign-in.
The accessed help lists eligible administrative roles and specific limitations, including restrictions for external users.^reset
For an eligible organisation user in One Experience UI:
1. Open Admin Panel → User Management → Users.
2. Select the intended user and the documented Reset MFA action.
3. Confirm the selected identity.
4. Complete the required administrator reauthentication.
5. Confirm the reset.
6. Have the user re-enrol the permitted factor.^reset
Do not reset the administrator’s own factor simply to demonstrate the menu. The guided exercise uses the user’s backup-code recovery instead.
Organisation policies
Zoho One’s current documentation distinguishes password/session security policies from conditional-access policies.
For a documented conditional-access policy, an administrator can select actions such as Deny access, Allow access or Allow with MFA, define MFA options, conditions, scope and exclusions.^policy
Policy design must consider:
- Which users are included.
- Which application types are covered.
- Which conditions must match.
- How existing policies interact.
- Which recovery options remain available.
Meridian’s base exercise configures the pilot users’ allowed factor and recovery. It does not require deploying a new organisation-wide conditional-access policy.
A later organisation may already enforce one. Record the relevant policy context when interpreting the pilot’s sign-in result.
Check L6: Why is a successful MFA sign-in insufficient evidence that a user should be allowed to record Finance acceptance?
### Lesson 7 — Manage onboarding, role changes and offboarding

Onboarding establishes that a user can join and perform the required work.
A role change updates access when responsibilities change.
Offboarding removes access while preserving ownership and continuity of business work.
A user-lifecycle checklist should track both access and responsibilities.
Onboarding readiness
For Meridian’s pilot, a user is ready only when all five conditions are satisfied:
| Condition | Evidence |
| --- | --- |
| Identity | The intended user has joined the correct organisation |
| Locale | The required personal locale and time zone are saved |
| Application | The intended CRM account can be opened |
| Authentication | The permitted MFA factor and recovery are established |
| Access boundary | A permitted personal-settings action succeeds and a company-settings modification is unavailable or denied |

This readiness rule is synthetic. It is a case acceptance criterion, not a universal Zoho onboarding rule.
Role changes
Suppose Mia needs selected CRM customer context.
The appropriate sequence is:
1. Identify the changed business task.
2. Add the required application or visibility.
3. Establish the relevant application permission.
4. Remove obsolete access if necessary.
5. Verify a permitted action.
6. Verify a relevant denied action.
Adding access is not the same as making Mia an administrator. Her Service responsibility does not transfer Finance authority.
Offboarding requires ownership preparation
Before deactivation, identify:
- Owned applications.
- Administrator roles.
- Owned integrations or connections.
- Open business work.
- Any independently managed external application accounts.
The official Zoho One deactivation guidance explicitly calls out administrative roles, application ownership, integrations and SAML applications.^deactivate
For planned departures, prepare ownership transfers before the access cutoff. If immediate revocation is required, do not leave access active while waiting for a business-work transfer; record and resolve that work separately.
Documented deactivation
An Organisation Owner, Organisation Admin or a permitted custom role can deactivate users.
In One Experience UI:
1. Open Admin Panel → User Management → Users.
2. Locate the intended user.
3. Open the user’s action menu.
4. Select Deactivate.
5. Complete any confirmation presented.^deactivate
The documentation describes deactivation as revoking access without deleting the account and retaining its data.
Expected result: the user is inactive and cannot establish the relevant new organisation/application sign-in.
Deactivation is not evidence that every external application account or integration token has been dealt with. The documented guidance specifically states that certain SAML-connected applications require their own deactivation.
Sessions
A session is an authenticated instance of access, such as a browser sign-in.
Zoho One’s Account Activity documentation describes login history and session clearing, including a possible delay in ending sessions.^sessions
Where the administrator has View and clear sessions permission, use the relevant user’s Account Activity to inspect and clear the required session.
Do not claim immediate termination merely because a button was clicked. Verify the relevant access result.
Reactivation
The documented user activation route uses Users → selected user → Activate, subject to available user capacity.
The help notes that prior assignments, roles or groups can be restored.^activate
This makes reactivation useful for laboratory recovery but also important to inspect. A reactivated identity may regain more access than a new job requires.
Check L7: Why should an administrator review application and integration ownership before a planned departure, and review restored access after reactivation?
## 3. Visual explanation — A user’s lifecycle

flowchart TD
    A["Requested: identity and business need supplied"] --> B{"Required inputs complete?"}
    B -- No --> C["Hold request; obtain permitted correction"]
    C --> B
    B -- Yes --> D["Add intended identity in training organisation"]
    D --> E["Pending join or first sign-in"]
    E --> F["Assign intended application and permissions"]
    F --> G["Configure locale, MFA and recovery"]
    G --> H{"Readiness checks satisfied?"}
    H -- No --> I["Correct the specific failed check"]
    I --> H
    H -- Yes --> J["Ready for intended work"]
    J --> K{"Responsibility changes?"}
    K -- Yes --> L["Revise access; verify allowed and denied actions"]
    L --> J
    J --> M["Departure: inventory and transfer responsibilities"]
    M --> N["Deactivate; verify access removal"]
    N --> O{"Authorised reactivation needed?"}
    O -- Yes --> P["Activate; inspect restored access"]
    P --> H
This diagram shows the business lifecycle, not a claim that Zoho uses these exact status labels.
A user can exist in the directory and still be unready because they have not joined, configured their personal settings or passed the access checks.
A correction loop returns to the failed check rather than creating a second identity.
Offboarding includes both continuity of work and access removal. Reactivation returns to readiness checking because restored access must still fit the current purpose.
## 4. Worked case — Prepare the Meridian pilot

Complete inputs
Use these supplied conditions:
- A dedicated training Zoho One organisation is available.
- Isha is its authorised administrator and has CRM Administrator access.
- The correct training CRM account is identified.
- Ava and Leo will be invited through distinct, controlled mailboxes.
- The existing policy permits OTP Authenticator and backup recovery codes.
- A suitable non-administrator CRM profile is available.
- User capacity is available for the two pilot users.
- Leo’s pilot account owns no applications, integrations or business records before the temporary deactivation exercise.
- No production application is involved.
If your actual environment does not satisfy a condition, record the difference. These inputs describe the worked case, not facts discovered about your own account.
Step 1 — Record the organisation target
The completed target record is:
| Configuration item | Target |
| --- | --- |
| Display name | Meridian Supply — Training |
| Environment label | MER-TRAIN-ORG |
| Organisation time zone | UTC |
| Pilot personal locale | English; United Kingdom; day-first date; 24-hour time; UTC |
| Home currency | GBP |
| Working schedule | Monday–Friday, 09:00–17:00 |
| Closure | 12 October 2026 |
| Team | Meridian Handoff Pilot |
| Pilot app | Correct training CRM |

The actual product IDs and controlled login addresses belong in the learner’s environment register after observation.
Step 2 — Configure and verify settings
Isha follows the documented procedures in Lessons 1–4.
After each save, she reopens the relevant page and compares it with the target.
The important intermediate result is not merely “Save clicked.” It is:
The saved value was reopened and matched the supplied target.
For home currency, she first checks the account’s current state. If it is already confirmed as GBP, she records that rather than attempting an unnecessary change.
Step 3 — Add and assign the pilot users
Ava and Leo are added as two distinct identities.
Their case references remain:
- Ava: MER-USR-002.
- Leo: MER-USR-003.
The controlled laboratory addresses are mapped separately from the synthetic emails.
They accept their invitations and open the intended training CRM account. Isha records their actual non-administrator profiles.
Step 4 — Establish authentication and recovery
Each user configures the permitted factor and saves recovery codes privately.
Each then performs a fresh sign-in and a controlled backup-code recovery test.
The evidence records success or failure, the identity reference and the date of the check. It contains no OTP, setup key or backup code.
Step 5 — Apply the readiness rule
This supplied paper snapshot describes readiness before Leo corrects his locale:
| User | Joined correct organisation | Locale correct | CRM opens |
| --- | --- | --- | --- |
| Ava | Yes | Yes | Yes |
| Leo | Yes | No | Yes |

Leo’s observed paper value is a month-first date format. The permitted correction is the supplied day-first format.
Readiness requires all five conditions.
Ready proportion = ready pilot users ÷ all pilot users × 100%
= 1 ÷ 2 × 100% = 50%
After Leo saves the correct format and the locale check passes:
Expected ready proportion = 2 ÷ 2 × 100% = 100%
The second value is an expected result of the supplied correction. A learner must perform and record the live check before calling it an actual result.
Step 6 — Test temporary deactivation
Leo’s pilot account has the supplied empty ownership inventory.
Isha:
1. Records that inventory.
2. Deactivates Leo.
3. Verifies inactive status and the relevant new-sign-in denial.
4. Inspects relevant session activity where permitted.
5. Reactivates Leo for continued course work.
6. Rechecks his profile, group membership and application assignment.
7. Rechecks readiness.
Leo is the temporary test subject because the inputs establish that the account has no owned applications or integrations. Isha’s administrator identity remains available to perform recovery.
Completed lifecycle checklist
| Lifecycle stage | Required action | Completion evidence |
| --- | --- | --- |
| Request | Confirm identity, business purpose and mailbox | Approved roster and address mapping |
| Add | Create one intended user record | Correct case reference and joining status |
| Join | User accepts and signs in | Confirmed identity in intended organisation |
| Assign | Give intended application access | Correct CRM account opens |
| Personalise | Save locale and time zone | Known date/time displayed as expected |
| Authenticate | Configure factor and recovery | Fresh sign-in and recovery check |
| Boundary test | Verify permitted and denied administration actions | Personal settings succeed; company modification denied or unavailable |
| Ready | Apply all five readiness conditions | Complete checklist |
| Departure preparation | Inventory responsibilities | Named destinations for applicable transfers |
| Deactivate | Remove relevant access | Inactive status and access check |
| Reactivate | Restore only for authorised training purpose | Restored access reviewed and readiness repeated |

Mistake and correction
Mistake: Isha records “Leo ready” immediately after clicking Add User.
Correction: Record the joining status first. Then verify CRM access, locale, authentication and the non-administrator boundary.
Adding the identity is one step in onboarding. It is not the endpoint.
## 5. Try it yourself — Guided practice

Learning goal
Configure the dedicated Meridian training organisation and demonstrate a complete user-lifecycle exercise using two controlled pilot identities.
Access and environment requirements
You need:
- A dedicated training Zoho One organisation.
- Organisation Owner/Admin access, or the documented permissions required for the selected tasks.
- CRM Administrator access for company information, business hours and holidays.
- Manage Currencies permission for the currency task.
- Available capacity for Ava and Leo’s training identities.
- Two distinct mailboxes you control or are authorised to use.
- An allowed authenticator and recovery method.
- An approved group alias where the group-creation form requires one.
- A browser session for Isha and separate sessions for the pilot users.
For the required denied-action test, Ava and Leo must be non-administrator CRM users. The later Sales-to-Finance transition restriction is outside this chapter’s configuration.
Identity mapping worksheet
Populate the live-login column privately before sending invitations.
| Case reference | Synthetic identity | Controlled laboratory login |
| --- | --- | --- |
| MER-USR-001 | isha.lin@example.com (mailto:isha.lin@example.com) |  |
| MER-USR-002 | ava.patel@example.com (mailto:ava.patel@example.com) |  |
| MER-USR-003 | leo.chen@example.com (mailto:leo.chen@example.com) |  |

The live-login values are environment inputs you supply. They are not business customer contact addresses.
Configuration worksheet
Record the before value, saved value and verification.
| Item | Before value | Target |
| --- | --- | --- |
| Organisation display name |  | Meridian Supply — Training |
| CRM organisation time zone |  | UTC |
| Home currency |  | GBP |
| Main schedule |  | Mon–Fri, 09:00–17:00 UTC |
| Week start |  | Monday |
| Closure |  | 2026-10-12 |
| Ava personal locale |  | English, UK, day-first, 24-hour, UTC |
| Leo personal locale |  | English, UK, day-first, 24-hour, UTC |
| Pilot group |  | Isha moderator; Ava and Leo members |

Scenario inputs
Use these paper scenarios to supplement live observations. They do not require deliberately creating invalid production records.
| Scenario | Supplied condition |
| --- | --- |
| ADM-01: normal join | Ava’s request is complete; the intended mailbox is controlled; capacity is available |
| ADM-02: invalid email input | Leo’s preparation worksheet contains leo.chen.example.com, with no @ |
| ADM-03: repeated request | Ava already exists under MER-USR-002 with the intended login |
| ADM-04: pending join | Leo’s existing invitation has not been accepted; his mapped mailbox is correct |
| ADM-05: denied administration | Ava is a Standard CRM user and attempts to modify Company Settings |
| ADM-06: factor recovery | Leo has an enrolled OTP factor and one unused backup code stored privately |
| ADM-07: temporary departure | Leo owns no app, integration, administrator role or business record in this pilot |
| ADM-08: external-user limitation | A separate paper identity is an external user; Isha is asked to reset its MFA through Meridian administration |

Guided steps
Step 1 — Establish context
Complete the organisation register and identify the associated CRM training account.
Expected intermediate result: you can distinguish the training account from every other account offered. The register contains actual observed identification, not invented IDs.
Step 2 — Configure the organisational foundation
Follow Lessons 1–4 to save:
- The training name.
- UTC organisation time zone.
- GBP home currency, subject to its current confirmation state.
- Monday–Friday, 09:00–17:00 business hours.
- Monday week start.
- The supplied October closure.
Expected intermediate result: reopened settings match the target table.
Step 3 — Onboard Ava and Leo
Follow Lesson 5. Check the address mapping before adding either user.
Expected intermediate result: two distinct users have joined the correct organisation. A repeated request does not create another identity.
Step 4 — Assign CRM and create the pilot group
Use individual CRM assignment and the documented collaboration-group procedure.
Expected intermediate result: the two users can open the intended CRM account; the pilot group contains the stated participants.
Step 5 — Configure personal settings
Each user saves the supplied locale and UTC time zone.
Expected intermediate result: a known date such as 13 October 2026 is interpreted and displayed consistently with the day-first selection.
Step 6 — Configure authentication and recovery
Each user follows the permitted MFA enrollment procedure and recovery setup.
Use one controlled backup-code recovery test.
Expected intermediate result: normal and recovery sign-ins work for the tested identity. Evidence contains outcomes, not credentials.
Step 7 — Demonstrate the administration boundary
As a non-administrator pilot user:
- Change a permitted personal preference.
- Attempt to access the Company Settings modification route.
Expected intermediate result: personal settings can be managed, while organisation modification is unavailable or denied.
If the user can modify company settings, investigate the actual profile before proceeding.
Step 8 — Demonstrate Leo’s lifecycle recovery
Use the supplied empty ownership inventory and Lesson 7’s deactivation/reactivation procedures.
Expected intermediate result: deactivation is verified; reactivation is followed by a fresh access review.
Step 9 — Complete readiness and exception evidence
Apply the five-condition readiness rule to each pilot user. Complete the ADM-01–ADM-08 paper traces.
Expected final result: every completed user has evidence for all five conditions, and every exception has an owner and a defined recovery route.
Final artifacts
Create:
- C01_CH03_Meridian_Organisation_Settings.md
- C01_CH03_Meridian_User_Register.csv
- C01_CH03_Meridian_Team_Membership.md
- C01_CH03_Meridian_User_Lifecycle_Checklist.md
- C01_CH03_Meridian_Administration_Evidence.md
Label evidence entries as:
- Observed: you performed the check.
- Expected: the supplied scenario predicts the result.
- Blocked: the environment lacks the necessary access or capability.
Safe cleanup
Retain the organisation settings and continuing pilot identities for later chapters.
After the temporary deactivation test, verify whether Leo is active again. If the pilot identity is no longer needed, leave it deactivated according to the laboratory’s intended lifecycle.
Sign out of temporary browser sessions. Keep authentication secrets outside project files.
Offline alternative
If you lack the required environment, complete the settings target, roster, lifecycle checklist, calendar calculations and scenario traces on paper.
This can demonstrate your administration reasoning. It cannot demonstrate:
- Saved product settings.
- Invitation acceptance.
- Application provisioning.
- MFA enrollment.
- Access denial.
- Deactivation or session behavior.
Record those items as expected or blocked, not observed.
## 6. Independent challenge — Handle a role change and a departure

Use a paper copy of the Meridian administration design. These changes do not automatically modify the continuing base-case roster.
Changed inputs
| Identity | Supplied situation |
| --- | --- |
| Mia, MER-USR-004 | Needs CRM customer context in addition to Service work; remains a non-administrator |
| Eli, MER-USR-008 | New Sales participant; email eli.stone@example.com; correct mailbox mapping exists; time zone missing from request |
| Tara, MER-USR-009 | Temporary Service participant leaving at 17:00 UTC on 16 October 2026 |

For Eli, the only authorised missing-value correction is:
Time zone = UTC, supplied by onboarding request JOIN-008.
For Tara, the complete ownership inventory is:
| Item | Current holder | Required destination or action |
| --- | --- | --- |
| Application owner role | None | No transfer needed |
| Organisation administrator role | None | No transfer needed |
| Integration connection | SIM-CONN-009 | Transfer or replace authorisation under Isha’s approved administration |
| Open service work | SIM-TASK-009 | Mia |
| Browser session | SIM-SESSION-009 | Clear through the permitted session procedure and verify |
| Separately managed external app | SIM-EXT-009 | Deactivate in that application as well |

All SIM- references are paper labels. They are not actual connector IDs, product records or observed sessions.
Tara’s access must be removed at the supplied cutoff even if a non-access work item remains unresolved. Planned ownership preparation should occur before that cutoff.
Calendar input
For a separate timing check:
- Start: Thursday, 8 October 2026, 16:00 UTC.
- Interval: 150 working minutes.
- Main schedule: Monday–Friday, 09:00–17:00 UTC.
- No break exclusion.
- No closure on 8 or 9 October.
- The known 12 October closure remains in the calendar.
Deliverables
Create C01_CH03_User_Change_Challenge.md containing:
1. Mia’s application-entry, visibility and decision-authority requirements.
2. Eli’s missing-data recovery and onboarding checklist.
3. Tara’s ordered departure plan, including integration, session and external-app work.
4. The expected working-time due timestamp and elapsed-time comparison.
5. At least one permitted and one denied action for Mia.
6. A distinction between expected outcomes and actual evidence.
Success criteria
Your plan must:
- Preserve Finance-only acceptance.
- Avoid granting administrator access merely to provide customer context.
- Use JOIN-008 for Eli’s missing time zone.
- Identify all unfinished departure items.
- Remove Tara’s access at the stated cutoff.
- Retain the explicit external-app deactivation task.
- Produce the calendar result from the supplied working periods.
## 7. Common problems and recovery

| Symptom | Diagnosis | Correction |
| --- | --- | --- |
| The wrong account appears when adding CRM | Application association was chosen without checking context | Stop account association; identify the dedicated training account |
| A user sees a date differently | Personal locale differs from the supplied convention | Edit Personal Settings rather than changing the source date |
| Times differ by a consistent offset | Different personal time zones may be displaying the same instant | Compare explicit timestamps and offsets |
| Home currency is already confirmed differently | The environment was prepared with another currency | Use a suitable training account or resolve the account decision with its administrator |
| Saturday appears as working | Wrong day selected in Custom hours | Edit and save the working-day selection |
| The closure does not affect the expected calendar | Wrong date, year or holiday scope | Edit the holiday list and inspect Apply To where relevant |
| A user remains Pending | Invitation acceptance has not completed | Check the mapped mailbox; use the documented reinvitation route |
| Repeated onboarding creates another identity | The existing identity was not checked | Reconcile the repeated request to the existing user |
| A pilot user can modify Company Settings | Administrator authority was assigned | Inspect the actual CRM profile and correct the assignment |
| MFA code is rejected | Wrong enrolled account, stale code or device timing may be involved | Use the correct current factor; check the authenticator’s time; use the approved recovery route if needed |
| Recovery code fails after regenerating codes | The earlier unused set was invalidated | Use the currently valid private recovery set |
| Reset MFA is unavailable for an external user | The documented account-management limitation applies | Use an appropriate account/organisation route rather than claiming local reset |
| Deactivation is blocked by ownership | User remains an application/admin/integration owner | Transfer or resolve the specific ownership using its documented procedure |
| Deactivated user still has separately managed external access | Suite deactivation did not cover that account | Complete the external-app task |
| Reactivated user has obsolete privileges | Previous assignments were restored | Review the restored roles, groups and app access |

Recover the specific failed condition. Do not respond to every problem by granting administrator access, creating another user or changing organisation-wide settings.
## 8. Check your understanding

 1. Explain the difference between a training environment label and a product-generated organisation ID.
 2. Why should a user’s personal time-zone preference not automatically become the organisation’s time zone?
 3. Interpret 10/11/2026 under Meridian’s supplied date convention.
 4. Calculate the GBP value of EUR 2,000 using the supplied rate GBP 0.85 per EUR.
 5. Why should you not add a second currency merely to demonstrate a dropdown?
 6. What remains unfinished when a user record exists but its invitation is Pending?
 7. Ava can change her personal date format. Should this imply that she can modify company business hours?
 8. Why are a collaboration-group moderator and a Finance decision owner different responsibilities?
 9. What does a successful backup-code sign-in demonstrate?
10. What changes when an administrator resets an eligible user’s MFA?
11. Tara’s external application is connected through SSO. Why should its independent deactivation remain on the checklist?
12. Two pilot users are in the onboarding population. Only Ava meets all five readiness conditions. What is the readiness percentage, and should Leo be excluded?
## 9. Solutions and explanations

Lesson checks
| Check | Explained answer |
| --- | --- |
| L1 | The display name helps people recognise the environment; the actual account association establishes where configuration and data will live. Similar names do not prove the correct account was selected. |
| L2 | No. 09:00 UTC and 11:00 at the supplied UTC+02:00 offset represent the same instant. The display changed, not the event. |
| L3 | The currency label changed but no exchange-rate calculation occurred. Conversion requires a defined rate and a changed amount where the currencies differ. |
| L4 | Elapsed addition counts every clock minute. The working-time calculation excludes the remainder of non-working periods, the weekend and the supplied Monday closure. |
| L5 | Membership supports coordination. It does not transfer the business decision established for Finance. Leo retains acceptance authority; Ava remains preparation and correction owner. |
| L6 | MFA verifies identity using the configured factor. Business authorization is a separate decision about what the verified identity may do. |
| L7 | Transfers preserve application and process continuity. Reactivation can restore prior access, so its suitability must be checked against the current role. |

Guided practice — Completed reference artifacts
Organisation settings artifact
The completed target portion of C01_CH03_Meridian_Organisation_Settings.md is:
| Item | Completed target record |
| --- | --- |
| Environment | MER-TRAIN-ORG, dedicated training context |
| Organisation name | Meridian Supply — Training |
| CRM organisation zone | UTC |
| Home currency | GBP |
| Main hours | Mon–Fri, 09:00–17:00 |
| Week begins | Monday |
| Closure | 2026-10-12, training maintenance |
| Pilot users | Ava and Leo |
| Group | Meridian Handoff Pilot |

This is a complete reference target. Actual saved values belong in the evidence columns only after the learner’s live work.
User-register example
This completed sample register records design decisions without inventing observed product IDs:
user_ref,synthetic_email,training_scope,crm_access_target,joining_evidence,mfa_evidence,readiness_evidence
MER-USR-001,isha.lin@example.com,Existing pilot administrator,Administrator,Required environment input,Existing approved authentication required,Administrator prerequisite
MER-USR-002,ava.patel@example.com,Pilot Sales user,Non-administrator profile,To record from live check,To record without secrets,Five conditions required
MER-USR-003,leo.chen@example.com,Pilot Finance user,Non-administrator profile;Finance transition control later,To record from live check,To record without secrets,Five conditions required
MER-USR-004,mia.reed@example.com,Later Service access,Restricted CRM context planned,Not part of two-user live pilot,Not observed in this chapter,Staged
MER-USR-005,noor.khan@example.com,Later Operations access,Operations visibility planned,Not part of two-user live pilot,Not observed in this chapter,Staged
MER-USR-006,omar.malik@example.com,Separate HR process,No customer-process access implied,Not part of two-user live pilot,Not observed in this chapter,Staged
MER-USR-007,ren.park@example.com,Separate HR decisions,No customer-process access implied,Not part of two-user live pilot,Not observed in this chapter,Staged
The laboratory login mapping is maintained separately. User references are business identifiers, not Zoho-generated IDs.
Team-membership artifact
| Team | Participant | Group responsibility |
| --- | --- | --- |
| Meridian Handoff Pilot | Isha | Moderator |
| Meridian Handoff Pilot | Ava | Member |
| Meridian Handoff Pilot | Leo | Member |
| Wider handoff process | Noor | Planned later participation |

The pilot does not remove Noor’s established process ownership. It simply limits this chapter’s live onboarding population.
Completed administration scenarios
| Scenario | Correct reasoning and route |
| --- | --- |
| ADM-01 | Add the complete intended identity once; complete joining, settings, authentication and access checks |
| ADM-02 | The prepared address lacks @; correct the case address using the supplied value and use its controlled-login mapping |
| ADM-03 | The identity already exists; investigate its current state rather than creating another |
| ADM-04 | Correct mailbox but incomplete join; use Resend for the pending user |
| ADM-05 | Standard user authority does not include company administration |
| ADM-06 | An unused current backup code provides the documented alternate recovery |
| ADM-07 | Empty ownership inventory permits the temporary pilot test |
| ADM-08 | The external-user limitation prevents assuming a Meridian-admin reset |

Readiness calculations
Before Leo’s correction:
1 ready user ÷ 2 pilot users × 100% = 50%
Leo remains in the population because he is a requested pilot user whose onboarding is unfinished.
After the supplied locale correction, if every live verification passes:
2 ready users ÷ 2 pilot users × 100% = 100%
If the correction was planned but not performed, the second value remains expected.
Evidence example
A suitable observed evidence entry would contain:
| Field | Example content |
| --- | --- |
| Check | Ava company-settings modification |
| Identity | MER-USR-002 |
| Organisation | Actual training organisation reference |
| Expected | Modification unavailable or denied |
| Observation | Learner records the actual result |
| Evidence reference | Learner’s redacted screenshot or written observation reference |
| Result | Pass, fail or blocked according to the observation |

Do not supply a fictional observation simply to make the artifact appear finished.
Independent challenge — Completed solution
Mia’s role change
| Access layer | Requirement |
| --- | --- |
| Identity | Existing MER-USR-004; no second identity |
| Application | Intended CRM account in addition to Service application |
| Visibility | Selected customer context needed for Service work |
| Editing | No general commercial or financial editing implied |
| Administration | No Company Settings modification |
| Business decision | No Finance acceptance |

A permitted action is reading the approved customer context.
A denied action is modifying Company Settings. Finance acceptance must also remain denied once that transition is configured.
The specific record-visibility configuration is completed in the access-control chapter rather than assumed from assigning CRM.
Eli’s onboarding
 1. Hold the incomplete request.
 2. Obtain UTC from JOIN-008.
 3. Record MER-USR-008 and eli.stone@example.com.
 4. Use the controlled laboratory-login mapping.
 5. Add Eli once.
 6. Complete joining.
 7. Assign the intended non-administrator CRM access.
 8. Save the supplied locale and UTC zone.
 9. Establish permitted MFA and recovery.
10. Verify the permitted personal action and denied company modification.
11. Apply the five-condition readiness rule.
The missing time zone is not permission to choose the administrator’s local zone by guess.
Tara’s departure
The incomplete items are:
- SIM-CONN-009 authorisation transfer or replacement.
- SIM-SESSION-009 clearing and verification.
- SIM-EXT-009 deactivation.
The service-work transfer is already acknowledged. There are no application-owner or organisation-admin roles to transfer.
A correct planned sequence is:
1. Identify Tara and the 17:00 UTC cutoff.
2. Complete the integration-authorisation preparation under Isha.
3. Verify Mia’s acknowledged service-work responsibility.
4. At the cutoff, deactivate Tara’s relevant organisation access.
5. Clear and verify applicable sessions through the permitted procedure.
6. Deactivate SIM-EXT-009 through its independently managed application route.
7. Record each result and any remaining blocker.
8. Reconcile the checklist so that unfinished work is not mistaken for completed offboarding.
If integration preparation remains unfinished at the cutoff, access removal still proceeds. Record the affected integration and its recovery owner rather than leaving Tara active.
Calendar calculation
Start:
Thursday, 8 October 2026, 16:00 UTC
Required interval:
150 working minutes
Thursday contribution:
17:00 − 16:00 = 60 minutes
Remaining:
150 − 60 = 90 minutes
Friday opens at 09:00:
09:00 + 90 minutes = 10:30
Expected due time:
Friday, 9 October 2026, 10:30 UTC
Elapsed time:
18 hours 30 minutes = (18 × 60) + 30 = 1,110 elapsed minutes
Working time:
150 minutes
The 12 October closure is not encountered because the interval finishes on 9 October.
Understanding questions
1. A planning label is human-readable. A product-generated ID identifies an actual application organisation. Record both where useful; do not invent the latter.
2. They serve different purposes. Personal settings represent the user’s display preferences. Organisation time-zone settings affect shared calculations such as documented workflow day boundaries.
3. 10 November 2026. Meridian’s convention is day/month/year.
4. GBP 1,700.  
EUR 2,000 × GBP 0.85/EUR = GBP 1,700.
5. It changes organisation capability and can have persistent consequences. The base exercise has no second-currency requirement, and the documented multi-currency activation is not an ordinary reversible demonstration.
6. The user has not completed the joining process. Readiness and actual application access are still unverified.
7. No. Personal preferences and company administration are separate permission scopes.
8. One administers group membership; the other establishes a business outcome. Moderating the handoff group does not make Isha or Ava the Finance decision owner.
9. It demonstrates that the supplied alternate recovery method works for the tested identity. It does not prove business authorization or every possible recovery situation.
10. The existing MFA configuration is cleared. The eligible user must configure MFA again at the next sign-in under the applicable process.
11. SSO and account lifecycle are different controls. The documented deactivation guidance states that certain SAML applications do not automatically deactivate their own accounts when the suite user is deactivated.
12. 50%.  
1 ÷ 2 × 100% = 50%.  
Leo remains in the onboarding population. Excluding unfinished users would hide incomplete work.
## 10. Chapter recap and next step

Organisation administration establishes the environment in which the business process operates.
The most important distinctions are:
- Training label versus actual organisation identification.
- Organisation settings versus personal preferences.
- Date formatting versus time-zone interpretation.
- Currency conversion versus currency relabeling.
- Business hours versus elapsed time.
- Application entry versus business authorization.
- User creation versus onboarding readiness.
- Deactivation versus deletion and independent external-account cleanup.
For Meridian, the configuration target is a dedicated training organisation with UTC timing, GBP home currency, Monday–Friday working hours and one explicit synthetic closure.
The pilot establishes Ava and Leo as identifiable, authenticated, non-administrator users. It does not yet configure the detailed Sales-to-Finance transition.
“I can…” completion checklist
- I can identify the correct organisation and application account.
- I can configure and verify organisation information.
- I can set personal locale without changing source dates or timestamps.
- I can explain and check the home currency.
- I can configure business hours and holiday scope.
- I can add users and distinguish joining status from readiness.
- I can assign applications and create a cross-functional group.
- I can establish permitted MFA and recovery.
- I can follow a user-deactivation procedure and review restored access.
- I can record observed, expected and blocked results accurately.
Your administration artifacts join the process maps and application map in the course project.
The next chapter, CRM Data Architecture, builds the record structure for the process. You will work with modules, fields, relationships, layouts, validation and a data dictionary. That structure will make Meridian’s enquiries, customers, commercial records and handoff evidence traceable.
## 11. Glossary and further reading

Glossary
| Term | Meaning |
| --- | --- |
| Application assignment | Establishing that an identity may use a particular application |
| Authentication | Verifying the identity that is signing in |
| Authorization | Determining the actions that identity may perform |
| Business hours | Configured working periods used by supported application features |
| Collaboration group | A cross-functional group created for a shared purpose |
| Deactivation | Revoking relevant user access while retaining the account and its data under the documented behavior |
| Department | Organisational placement used for administration and relevant application structures |
| Exchange rate | The relationship used to convert an amount between currencies |
| Home currency | The organisation’s primary currency |
| Locale | Regional presentation conventions such as language, date and number formatting |
| MFA | Multi-factor authentication |
| Offboarding | Removing access and arranging continuity when a user’s role ends |
| Onboarding | Establishing identity, access, settings and readiness for work |
| OTP Authenticator | An application that generates time-based one-time passwords |
| Pending user | An invited identity that has not completed the relevant joining process |
| Recovery code | A privately stored, single-use code used through the documented MFA recovery route |
| Session | An authenticated instance of access |
| Shift | A defined working schedule for particular users |
| Time zone | A rule for representing timestamps as local times |
| User readiness | The supplied conditions that establish a user can perform the intended work |

Further reading
The referenced official help articles were accessed for the procedures and product behavior described here. No product execution is claimed.
The Zoho One documentation distinguishes One Experience, Spaces and Unified interfaces. This chapter gives the One Experience path; use the corresponding tab in the linked help if your environment uses another interface.
CRM access depends on the documented profile or permission for the task. Currency availability depends on edition, and identity behavior depends on user classification, domain state and existing organisation policies.
^org: Zoho One, Edit Organization Info (https://help.zoho.com/portal/en/kb/one/admin-guide/organization/managing-organization-info/articles/zohoone-edit-company-details).
^addapp: Zoho One, Add a Zoho app (https://help.zoho.com/portal/en/kb/one/admin-guide/applications/adding-applications/articles/zohoone-add-zoho-app), including the existing-account association statement.
^crmcompany: Zoho CRM, Manage Company Settings (https://help.zoho.com/portal/en/kb/crm/organization-settings/company-settings/articles/manage-company-details), particularly company information and organisation time zone.
^personal: Zoho CRM, Managing CRM Account Settings (https://help.zoho.com/portal/en/kb/crm/organization-settings/personal-settings/articles/manage-account-settings), particularly locale and number formats.
^currency: Zoho CRM, Manage Multiple Currencies (https://help.zoho.com/portal/en/kb/crm/organization-settings/company-settings/articles/multiple-currencies), particularly home-currency confirmation, permissions and activation behavior.
^hours: Zoho CRM, Manage Business Hours (https://help.zoho.com/portal/en/kb/crm/organization-settings/company-settings/articles/business-hours), including custom schedules, shifts and holiday lists.
^users: Zoho One, Add user (https://help.zoho.com/portal/en/kb/one/admin-guide/users/managing-users/articles/zohoone-adding-a-user).
^reinvite: Zoho One, Reinvite a pending user (https://help.zoho.com/portal/en/kb/one/admin-guide/users/managing-users/articles/reinvite-pending-user).
^assign: Zoho One, Assign app to individual user (https://help.zoho.com/portal/en/kb/one/admin-guide/applications/managing-applications/articles/zohoone-assign-app-individually).
^groups: Zoho One, Groups — Overview (https://help.zoho.com/portal/en/kb/one/admin-guide/groups/articles/zohoone-groups-overview) and Add collaboration group (https://help.zoho.com/portal/en/kb/one/admin-guide/groups/articles/zohoone-add-collaboration-group).
^otp: Zoho Accounts, Set up an authenticator for your Zoho account (https://help.zoho.com/portal/en/kb/accounts/faqs-troubleshooting/faqs/multi-factor-authentication/articles/how-do-i-set-up-authenticator-for-my-zoho-account).
^backup: Zoho Accounts, Backup Verification Codes (https://help.zoho.com/portal/en/kb/accounts/multi-factor-authentication/articles/mfa-backup-verification-codes).
^reset: Zoho One, Reset MFA for users (https://help.zoho.com/portal/en/kb/one/admin-guide/users/managing-users/articles/reset-mfa-for-users).
^policy: Zoho One, Add conditional access policy (https://help.zoho.com/portal/en/kb/one/admin-guide/security/security-2-0/articles/add-conditional-access-policy-zo).
^deactivate: Zoho One, Deactivate users (https://help.zoho.com/portal/en/kb/one/admin-guide/users/managing-users/articles/zohoone-deactivate-users), including ownership checks and separately managed SAML applications.
^sessions: Zoho One, Account activity (https://help.zoho.com/portal/en/kb/one/admin-guide/users/managing-users/articles/zohoone-account-activity).
^activate: Zoho One, Activate users (https://help.zoho.com/portal/en/kb/one/admin-guide/users/managing-users/articles/activate-users).
