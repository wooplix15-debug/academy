---
course_id: "C04"
chapter_id: "C04-CH08"
chapter_number: 8
chapter_title: "Pilot Design and Measurement"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "partially_verified"
---

# Pilot Design and Measurement

1. What you will learn
A pilot should answer a decision question. “Try the tool and see what happens” is not enough.
A useful pilot tells you which people and cases are included, what changes, what stays comparable, how results are measured and what would cause the test to stop. Its evidence should support a clear next decision.
In this chapter, you will learn to:
- Define a pilot audience and process boundary.
- Select a baseline that matches the task being tested.
- Include normal, exception, permission and recovery cases.
- Measure quality, effort, completion and adoption.
- Set success criteria and stop criteria before testing.
- Interpret unfinished records and small samples.
- Record a proceed, revise or defer decision.
Your required practice is to draft a pilot charter containing a boundary, baseline, representative cases, measures and stop criteria.
Prerequisites and continuity
You should understand the difference between staff effort and elapsed time, between capacity and cash savings, and between a routine exception and an incident.
Meridian Supply’s three opportunities remain:

| Opportunity ID | Candidate |
| --- | --- |
| MSP-OPP-001 | Improve required-field completeness and validity |
| MSP-OPP-002 | Reduce effort spent organising varied enquiry wording |
| MSP-OPP-003 | Investigate repeated entry of approved enquiry information |
Previous decisions remain in force:
- Investigate native validation conditionally for MSP-OPP-001.
- Compare a standard template with source-grounded assistance for MSP-OPP-002.
- Assess shared-record suitability and transfer dependencies for MSP-OPP-003.
- Keep Sales responsible for quotation acceptance and Operations responsible for availability confirmation.
- Treat access, entitlements, technical support and maintenance assignments as unresolved where not confirmed.
The original MSP-PILOT-001 remains a proposed, unexecuted six-case offline test. Its manual preparation baseline is 36 minutes. Its criteria include six correct outcomes, no unsupported commitments or prohibited actions, at most 30 staff minutes, and completed review and feedback from both proposed reviewers.
This chapter introduces a separate, broader draft comparison under MSP-PILOT-002. It does not overwrite the original pilot.
Your contribution to the course project
You will produce a Pilot Charter, Test Case Packet, Measurement Sheet and Pilot Decision Note.
These artifacts form the measurement section of your Business Automation Pilot Proposal. They explain what evidence the proposed pilot must produce before leadership considers a broader change.
The scenario is synthetic and may be replaced by a permission-cleared company case. A workshop pilot does not establish production implementation competence or guaranteed returns.
2. Lessons
Lesson 1 — Start with a decision question, audience and boundary
A pilot is a bounded evaluation of a proposed change. It should reduce uncertainty about a specific decision.
For Meridian’s internal brief opportunity, a useful question is:
Does a standard template or source-grounded assistance reduce total preparation effort while preserving the request, handling exceptions correctly and maintaining required review?
This question connects the proposed method to the work being improved.
A less useful question is:
Can AI automate Sales?
That is too broad to define a credible test.
Define the audience
The pilot audience is the group that performs, reviews or receives the changed work.
For an internal brief comparison:
- Sales prepares and reviews briefs.
- Operations confirms source meaning and exception expectations.
- IT checks any technical access and service dependencies.
- Finance checks effort and cost measurement.
- The Sponsor owns the next decision.
Customers are affected by the wider process, but they do not need to receive experimental outputs in an offline pilot.
Define start and end conditions
A boundary should specify:
- The event that starts the measured task.
- The inputs available.
- The permitted actions.
- The output or exception that ends the task.
- Activities excluded from measurement.
For Meridian:
Start when an authorised preparer opens the supplied enquiry packet. End when Sales records a reviewed internal brief or a reviewed exception outcome.
A missing-quantity exception can complete this preparation task even though the full enquiry-to-quotation process remains open.
The pilot excludes real customer waiting, quotation issuance, stock reservation and live record writes. Therefore, it cannot establish an improvement in quotation response time or fulfilment.
Worked example: choose the correct claim
Suppose the pilot reduces internal preparation effort from six to four minutes per case.
A supported statement would be:
Preparation effort decreased by two minutes per case in the tested packet.
It would not establish:
Customers receive quotations two minutes earlier.
Customer response also depends on queues, availability decisions and other work outside the pilot boundary.
Check L1: Why can a pilot finish a missing-quantity test case without completing the customer’s quotation?
Lesson 2 — Match the baseline and cases to the pilot question
A baseline comparison measures the same task before or without the proposed change.
Do not compare six preparation minutes with a new method’s entire quotation process, or compare 18 initial handling minutes with a new method’s preparation-only time.
Use the same:
- Task boundary.
- Input facts.
- Required output.
- Review requirement.
- Included exception work.
- Timing rules.
Chapter 5’s weekly baseline of 38.4 staff hours covers much more than brief preparation. It is useful business context, but it is not the direct comparator for a preparation-only pilot.
Representative cases have two purposes
A pilot needs cases that reflect normal work and cases that test important exceptions.
These goals are related but different:
1. Workload representation: approximate the cases that normally occur.
2. Control coverage: deliberately include cases that could reveal important weaknesses.
A small exception-rich packet may provide good control coverage without representing the usual workload.
Official evaluation guidance recommends task-specific cases and coverage of normal, edge and challenging inputs.1 It does not provide a universal sample size for every business pilot.
For Meridian, include:
- Clear and differently worded normal enquiries.
- Missing or invalid fields.
- Unknown products.
- Denied source use.
- Availability uncertainty.
- Missing source information.
- A defined fallback when assistance is unavailable.
Do not invent failures to make a discovery exercise seem technical. Here, fallback testing is relevant because the proposed operating method may depend on a service.
Reduce comparison bias
If someone prepares the same enquiry manually and then immediately uses a template, they may remember the answer. The second method can appear faster because of practice.
Useful controls include:
- Rotate method order across cases.
- Keep inputs identical.
- Do not show reference answers before the attempt.
- Use consistent timing definitions.
- Label outputs without identifying the method where practical for review.
- Use fresh cases after a material revision.
These controls reduce bias; they do not eliminate it. Record the limitation.
Check L2: Why should an exception-rich packet not be multiplied directly into a company-wide annual saving?
Lesson 3 — Measure quality, effort and adoption together
One number rarely describes a useful pilot.
A fast method may produce incomplete outputs. A correct method may require more review than expected. A successful demonstration may depend on one enthusiastic user who cannot support ordinary operations.
Use several measures.
Quality
For Meridian, quality includes:
- Product, quantity and requested date preserved.
- Requests distinguished from commitments.
- Source status and uncertainty represented correctly.
- Correct exception route.
- No prohibited action.
- Required review completed.
Define first-pass correctness as an initial prepared result requiring no substantive correction at first review.
Define final correctness as the reviewed result meeting the reference requirements after any corrections.
Report both. Final correctness alone can hide correction work.
A prescribed manual fallback is not automatically a first-pass failure. If the operating method requires fallback and the resulting first reviewed outcome is correct, it can pass. Unplanned correction still needs recording.
Staff effort
Measure:
Total task effort = preparation + review + correction + fallback effort
The components must not overlap. If review time already includes correction, do not add correction again.
Record setup, test administration and debrief effort separately. These are pilot resource requirements, even when they are not part of steady-state preparation time.
Service waiting is also distinct from active staff effort. A user may spend two active minutes on a task that takes ten elapsed minutes.
Completion and denominator
For a planned six-case packet with five reviewed outcomes:
Completion = 5 ÷ 6 × 100 = 83.33%
You may calculate correctness among the five reviewed outcomes, but you must also disclose that one is unfinished.
An unfinished case must not be treated as correct or assigned zero remaining effort.
Adoption
An adoption measure checks whether intended users actually perform the changed work as designed.
For an early pilot, useful measures include:
- Assigned tasks completed.
- Required review records completed.
- Feedback supplied.
- Need for assistance.
- User-identified barriers.
“Users liked it” is too vague unless you supply a question and interpretation rule.
An offline exercise can show participation and practical difficulties. It cannot establish sustained adoption in normal work.
Check L3: Why can 100% correctness among completed records coexist with an incomplete pilot?
Lesson 4 — Set success, stop and decision rules before testing
Success criteria state what evidence would make the next step worthwhile.
Stop criteria state what event requires immediate pause or containment.
They are different. A slow method may miss its success target without causing an incident. An unsupported delivery promise may trigger a stop even when the average time looks excellent.
Examples:

| Type | Example |
| --- | --- |
| Quality success | Every planned case reaches a correct reviewed outcome |
| Effort success | Total task effort is at least 20% below the matched baseline |
| Adoption success | Both proposed users complete assignments and feedback |
| Stop | A draft contains an unsupported price or delivery commitment |
| Stop | The method attempts prohibited access, a live write or a customer message |
The numerical thresholds in this chapter are synthetic management choices. They are not course passing rules or universal standards.
Define the next decision
Use:
- Proceed: evidence supports a named next step.
- Revise: change the method or design and test again.
- Defer: do not advance while a critical dependency or stop-condition cause remains unresolved.
“Proceed” must specify its destination. Proceeding to a larger shadow comparison is not approval for production.
A shadow comparison evaluates outputs separately from live decisions. Experimental results do not replace the authorised business process.
Freeze criteria before collecting results. If you lower a target after a failure, preserve the original result and label the new design separately.
Check L4: Why should a corrected unsupported promise still appear in the stop-condition count?
3. Visual explanation — Evidence supports a bounded decision
flowchart TD
    A[Define question, audience and boundary] --> B[Freeze baseline, cases and criteria]
    B --> C{Permissions, owners and resources confirmed?}
    C -->|No| D[Revise or defer the affected pilot arm]
    C -->|Yes| E[Prepare and review each assigned case]
    E --> F{Stop condition?}
    F -->|Yes| G[Contain, preserve evidence and investigate]
    F -->|No| H[Record quality, effort, completion and feedback]
    H --> I{All planned evidence complete?}
    I -->|No| J[Report unfinished records and revise completion plan]
    I -->|Yes| K[Compare against success criteria]
    K --> L[Proceed, revise or defer for a named next step]
    G --> L
The diagram separates readiness to start, immediate stopping and end-of-pilot assessment.
A pilot with no stop event can still be incomplete. A pilot with excellent corrected outputs can still have triggered a stop. Both conditions belong in the decision record.
4. Worked case — Meridian’s broader comparison charter
Explicit new scenario inputs
This chapter adds:

| Record ID | Supplied material |
| --- | --- |
| MSP-PDES-001 | Draft comparison question and participant plan |
| MSP-PDES-002 | Twelve-case packet and synthetic manual baseline |
| MSP-PDES-003 | Proposed measures and decision thresholds |
| MSP-PDES-004 | Start dependencies and limitations |
The new draft, MSP-PILOT-002, concerns MSP-OPP-002.
It compares:
- Manual preparation as the baseline method.
- A standard internal template.
- Source-grounded assistance, if its access and entitlement are confirmed.
The assistance arm is not authorised merely because a charter exists.
Complete source facts
The packet uses the established synthetic facts:

| Source | Supplied fact |
| --- | --- |
| Approved catalogue | BF-10 is a 10 mm brass fitting |
| Dated stock snapshot | 40 units listed at 2026-10-05 08:45; current reservations and future availability are not established |
| Approved substitution extract | No approved substitute for BF-10 |
| Approved Operations note | Delivery requires Operations confirmation |
| Obsolete sales note | “BF-10 can always be delivered next day”; not current authority |
No price or confirmed delivery date is supplied.
Each case is independent. The stock snapshot is not consumed or reserved across the packet.
Complete case inputs and baseline
All requested dates are 2026-11-09 except case 908, where the date is missing. Contact details use buyer@example.com.
The first four messages demonstrate wording variation:
- 901: “Please quote 25 BF-10 units for 9 November.”
- 902: “We need ten BF-10 fittings. Please quote and advise about delivery on 9 November.”
- 903: “BF-10: 15 units. Requested delivery: 9 November.”
- 904: “Quotation request: BF-10 / quantity 20 / delivery requested 9 November.”

| Case | Input or special condition | Source use | Supplied manual preparation effort |
| --- | --- | --- | --- |
| MSP-ENQ-901 | BF-10, 25 units; short message | Permitted | 6 minutes |
| MSP-ENQ-902 | BF-10, 10 units; quantity expressed as “ten” | Permitted | 6 minutes |
| MSP-ENQ-903 | BF-10, 15 units; field-like wording | Permitted | 6 minutes |
| MSP-ENQ-904 | BF-10, 20 units; compact wording | Permitted | 6 minutes |
| MSP-ENQ-905 | BF-10; quantity missing | Permitted | 8 minutes |
| MSP-ENQ-906 | BF-10; quantity zero | Permitted | 8 minutes |
| MSP-ENQ-907 | XX-99, 8 units; code not recognised | Permitted | 8 minutes |
| MSP-ENQ-908 | BF-10, 10 units; requested date missing | Permitted | 8 minutes |
| MSP-ENQ-909 | BF-10, 4 units; source enrichment denied | Not permitted | 4 minutes |
| MSP-ENQ-910 | BF-10, 60 units | Permitted | 8 minutes |
| MSP-ENQ-911 | BF-10, 25 units; approved stock extract absent from this case’s packet | Permitted for available sources | 8 minutes |
| MSP-ENQ-912 | BF-10, 25 units; assistance-unavailable drill | Permitted | 8 minutes |
For case 912, the supplied drill condition is: no assistance output is returned. The permitted recovery is manual preparation from the approved packet, with the failed attempt and fallback effort recorded. This is a planned scenario, not an observed service failure.
The baseline includes preparation, ordinary checking and exception recording. It excludes real customer replies, quotation issuance and unrelated rework.
Step 1: calculate the matched baseline
Baseline = 6 + 6 + 6 + 6 + 8 + 8 + 8 + 8 + 4 + 8 + 8 + 8
= 84 staff minutes
Mean = 84 ÷ 12 = 7 staff minutes per preparation outcome
These are supplied synthetic baseline values, not Meridian’s observed company performance.
Step 2: complete the reference outcomes

| Case | Required outcome |
| --- | --- |
| 901–904 | Facts-only brief preserving product, quantity and requested date; delivery unconfirmed |
| 905 | Specific quantity clarification exception |
| 906 | Invalid-quantity exception; no default |
| 907 | Product verification exception; do not substitute BF-10 |
| 908 | Requested-date clarification exception |
| 909 | Source-use hold and access escalation; no enrichment attempt |
| 910 | Brief identifying request beyond the dated snapshot; Operations confirms availability |
| 911 | Brief marking current stock unknown because the approved extract is absent |
| 912 | Correct manual fallback outcome; record assistance unavailability and all staff effort |
The packet provides control coverage. Its exception proportions are deliberately high and do not establish the wider workload mix.
Step 3: complete the pilot charter
Artifact: MSP_Pilot_Charter_002_v0_1.md

| Charter element | Completed draft |
| --- | --- |
| Pilot ID | MSP-PILOT-002 |
| Opportunity | MSP-OPP-002 |
| Question | Can template or source-grounded assistance reduce total preparation effort while preserving quality, review and exception handling? |
| Audience | Two proposed Sales users, identified as Sales-01 and Sales-02; Operations validates source meaning |
| Boundary | Authorised packet opening to reviewed internal brief or exception record |
| Exclusions | Customer messages, live writes, prices, stock reservation, quotation response time and employee-performance scoring |
| Comparison | Manual baseline; template; assistance arm conditional on readiness |
| Baseline | Twelve supplied cases; 84 staff minutes for the defined task |
| Cases | Four normal wording variants, four required-field/product exceptions, one permission case, one availability case, one missing-source case and one fallback drill |
| Assignment | Six cases per user per tested method; same case packet for each method |
| Bias reduction | Rotate method order across case groups; withhold reference answers until attempts; label outputs by record rather than preferred technology where practical |
| Review | Sales reviews every output; Operations resolves source-meaning disagreements |
| Version control | Record method/template/instruction version and, if used, model/service configuration; material changes create a new round |
| Measures | Completion, first-pass correctness, final correctness, stop events, total task effort, separate administration effort, usage and user participation |
| Success criteria | All 12 reviewed outcomes correct; at least 11 of 12 first-pass correct; zero stop events; task effort at most 67.2 minutes; both users complete assignments and feedback |
| Stop criteria | Any unsupported price/delivery commitment, prohibited access attempt, live write or customer message |
| Containment | Sales pauses the affected method; preserve outputs and assess impact using Chapter 7 controls |
| Fallback | Permitted manual preparation; record effort and reason; never bypass access restrictions |
| Start dependencies | Confirm authorised participants, review cover, source use, storage, technical support, entitlement and any incremental cash commitment |
| Resource recording | Include preparer and reviewer effort; record setup, calibration, administration, support and usage separately |
| Decision owner | Sponsor, proposed; informed by Sales, Operations, Finance and IT |
| Result status | Proposed only; no method outputs or post-change timings observed |
The effort target is:
84 minutes × (1 − 20%) = 67.2 minutes
The first-pass threshold is:
11 ÷ 12 × 100 ≈ 91.67%
These thresholds apply to this small packet. They do not estimate long-term reliability.
Step 4: define measure denominators

| Measure | Numerator | Denominator or basis |
| --- | --- | --- |
| Completion | Reviewed outcomes recorded | 12 planned cases per method |
| First-pass correctness | Initial results requiring no substantive correction | Report reviewed initial results; disclose pending cases; full-round target 11 of 12 |
| Final correctness | Reviewed outcomes meeting reference requirements | Reviewed outcomes, alongside completion |
| Stop events | Count of qualifying events | All attempted cases and all draft versions |
| Task-effort reduction | 84 minus full-round task effort | 84-minute matched baseline |
| User participation | Users completing assignments and feedback | Two proposed users |
| Protocol completion | Assigned tasks with required work/review records complete | 12 assigned tasks per method |
Do not exclude exception cases from completion merely because they cannot produce a normal brief.
Step 5: define the decision rule
Artifact: MSP_Pilot_Decision_Rules_v0_1.md
- Proceed to a broader permission-cleared shadow comparison if a method completes all planned evidence and meets every success criterion without a stop event.
- Revise if no stop occurs but quality, effort, participation or completion misses a target. Preserve the result and identify the change before another round.
- Defer advancement of the affected method if a stop occurs or a critical start dependency is unresolved. Contain and verify recovery before any restart decision.
- If both candidate methods pass, use actual effort, costs, review burden and user feedback to inform selection.
- If only the template arm can start, record an incomplete comparison; do not imply that assistance was evaluated.
Step 6: record the current decision
Current decision: revise readiness before running the assistance arm. The charter and reference packet are complete as draft learning artifacts. Access, entitlement, technical support and participant arrangements still require confirmation. No success result is claimed. The original MSP-PILOT-001 remains proposed and unchanged.
Mistake and correction
Mistake: “The packet covers difficult cases, so a 20% reduction proves the annual business case.”
Correction: The packet tests named behaviours and preparation effort. Its workload mix is not representative evidence for an annual forecast. A broader case sample and confirmed operating costs are needed before updating the value model.
5. Try it yourself — Guided practice
Learning goal and access
Draft a charter and interpret an incomplete measurement packet.
Use paper or a local worksheet. No product account is required. The result figures below are a supplied simulation, not observed product execution.
The exercise pilot ID is EX-PILOT-CH08-001. It does not replace either Meridian pilot.
Complete scope and rules
Compare a standard internal template with a supplied manual preparation baseline.
- Six cases, each with a six-minute baseline.
- Two exercise users: User-01 receives cases 951, 953 and 955; User-02 receives 952, 954 and 956.
- Start: open authorised packet.
- End: reviewed brief or exception outcome.
- Sales Lead owns acceptance; Operations owns availability meaning.
- Sponsor owns the next decision.
- No assistance service, live write or customer sending.
- No extra licence is required under this exercise’s local-template assumption.
- No cash-saving mechanism is supplied.
- Every completed outcome requires review.
Success criteria:
- Six of six correct reviewed outcomes.
- At least five of six first-pass correct.
- No stop event.
- At most 30 total task minutes.
- Both users complete assignments and feedback.
Stop criteria are an unsupported price/delivery commitment, prohibited access attempt, live write or customer message.
Decision rules are proceed to a larger offline comparison if all criteria pass, revise if completion or other success criteria are unmet without a stop, and defer advancement if a stop occurs.
Complete case inputs
All supplied dates are 2026-11-12.
The approved catalogue identifies BF-10. Delivery requires Operations confirmation. No price or delivery commitment is supplied.

| Case | Input |
| --- | --- |
| MSP-ENQ-951 | BF-10, 25 units; valid request; source use permitted |
| MSP-ENQ-952 | BF-10, 10 units; valid request; source use permitted |
| MSP-ENQ-953 | BF-10; quantity missing |
| MSP-ENQ-954 | XX-99, 8 units; unknown product |
| MSP-ENQ-955 | BF-10, 4 units; source enrichment denied |
| MSP-ENQ-956 | BF-10, 20 units; approved stock extract unavailable; available sources permitted |
For case 953, the initial template incorrectly marked the request ready for handoff. Review corrected it to quantity clarification. No unsupported commercial promise or prohibited action occurred.
For case 956, review is unfinished. No remaining duration is supplied.
Simulated measurement packet
Preparation, review and correction minutes are separate and non-overlapping. A first-pass correction flag of yes means substantive correction was required.
enquiry_id,baseline_min,preparation_min,review_min,correction_min,fallback_min,status,first_pass_correction_flag,final_correct,stop_event
MSP-ENQ-951,6,2,1,0,0,reviewed,no,yes,no
MSP-ENQ-952,6,2,1,0,0,reviewed,no,yes,no
MSP-ENQ-953,6,1,1,1,0,reviewed,yes,yes,no
MSP-ENQ-954,6,1,1,0,0,reviewed,no,yes,no
MSP-ENQ-955,6,1,1,0,0,reviewed,no,yes,no
MSP-ENQ-956,6,2,0,0,0,open_review,unknown,unknown,no
User-01 has completed all assignments and supplied feedback. User-02 has completed two assignments and has not yet supplied feedback.
All five reviewed outcomes match the case requirements. No stop event appears in the supplied simulation.
Learner charter worksheet

| Element | What to enter |
| --- | --- |
| Pilot ID and question | Supplied exercise ID and task-specific comparison |
| Audience and owners | Participants, acceptance owner and decision owner |
| Boundary | Start, end, permitted actions and exclusions |
| Baseline | Cases, minutes and task definition |
| Representative cases | Normal and exception conditions |
| Measures | Formula, denominator and evidence fields |
| Success and stop criteria | Supplied thresholds and immediate-stop conditions |
| Recovery | Owner, permitted fallback and verification |
| Decision | Named next step based on evidence |
| Limitations | What the exercise cannot establish |
Guided steps and expected intermediate results
1. Draft the charter.
- Expected result: all worksheet elements populated with the supplied facts.
2. Separate planned and completed cases.
- Expected result: the open record remains visible.
3. Calculate quality and participation.
- Expected result: denominators distinguish reviewed cases, assigned cases and users.
4. Calculate effort.
- Expected result: completed-case effort and all effort spent so far are reported separately.
5. Apply the decision rule.
- Expected result: a decision that does not treat unfinished work as zero remaining effort.
Your final artifact is C04_CH08_Pilot_Charter_Practice.md, containing the charter and a measurement/decision note.
In a group, assign Sponsor, Sales, Operations, Finance and IT perspectives. Individually, check the same questions from each role’s viewpoint.
Retain the synthetic artifact. No system cleanup is required.
6. Independent challenge
Use this changed continuation of the exercise simulation. It does not establish an actual pilot result.
Cases 951–955 remain unchanged.
Case 956 now has:
- Two preparation minutes.
- One review minute.
- Two correction minutes.
- Zero fallback minutes.
- A correct reviewed final outcome.
- A substantive first-pass correction.
- An initial unsupported statement: “Delivery on 12 November is guaranteed.”
- No supporting delivery confirmation.
- No message or live write.
- A stop event when the unsupported statement is detected.
Case correction is completed as containment after pausing the method. No new cases are attempted after the stop.
Both users have now completed assignments and feedback. No cause investigation or revised-method verification is supplied.
The Sponsor says:
All final outcomes are correct and effort is 50% lower, so we should proceed.
Deliverables
1. Calculate final correctness, first-pass correctness, completion and effort reduction.
2. Apply the stop rule and record a decision.
3. Explain what the Sponsor’s statement gets right and misses.
4. State the evidence required before restart.
5. Identify one limitation of extrapolating this packet.
Success criteria
Your answer must retain the stop event even after correction, count correction effort, preserve the original draft and distinguish a successful final case correction from permission to advance the method.
7. Common problems and recovery

| Symptom | Diagnosis | Correction | Verification |
| --- | --- | --- | --- |
| Pilot question says only “test AI” | Decision purpose is unclear | Define task, comparison and required result | Measures answer the question |
| Baseline uses the whole process but candidate timing covers one task | Boundaries differ | Use a matched task baseline | Included activities agree |
| Only easy cases are tested | Control coverage is weak | Add relevant exceptions and fallback cases | Case list maps to required behaviours |
| Open cases disappear | Completion bias | Report planned, reviewed and unfinished counts | Every assigned record is accounted for |
| Corrected outputs hide first-pass defects | Quality measure is incomplete | Record initial and final correctness | Correction flags and minutes are reproducible |
| A stop event is removed after correction | Incident history is overwritten | Preserve event and recovery evidence | Decision applies the original rule |
| Targets change after results arrive | Criteria are being fitted to outcomes | Preserve original assessment; label a new round | Versions and decisions remain distinct |
| High participation is called sustained adoption | Exercise behaviour is overgeneralised | Report exactly what users completed | Claim matches the observation period |
If a service is unavailable, follow the permitted fallback and count its effort. If access is denied, fallback must not bypass permission.
8. Check your understanding
1. What must a pilot boundary specify?
2. Why are representative workload sampling and exception coverage different?
3. Why should both first-pass and final correctness be reported?
4. What does five correct reviewed outcomes out of six planned cases establish?
5. Why can a pilot miss an effort target without triggering a stop?
6. What does “proceed to a larger shadow comparison” permit, and what does it not permit?
9. Solutions and explanations
Lesson checks
L1: The preparation task can end with a correct reviewed clarification exception. The customer’s quotation remains open in the wider process.
L2: Its proportions were deliberately chosen for control coverage. Scaling its average assumes a workload mix and sustained performance that have not been established.
L3: All reviewed outcomes can be correct while other planned outcomes remain unreviewed. Correctness among completed records and overall completion answer different questions.
L4: The event occurred in a proposed draft and met the stop rule. Correction limits effects but does not erase the event or demonstrate recurrence prevention.
Guided practice — Completed charter

| Element | Completed example |
| --- | --- |
| ID and question | EX-PILOT-CH08-001; does the template reduce preparation effort while preserving correct outcomes and review? |
| Audience | Two users, three assigned cases each |
| Owners | Sales accepts outcomes; Operations owns source meaning; Sponsor decides next step |
| Boundary | Authorised packet opening to reviewed internal brief or exception |
| Exclusions | Live writes, customer messages, assistance-service behaviour and cash-saving claims |
| Baseline | Six cases × six minutes = 36 task minutes |
| Cases | Two normal, missing quantity, unknown product, denied enrichment and missing stock source |
| Measures | Completion, first-pass/final correctness, task effort, stop events and user completion/feedback |
| Success | Six correct outcomes; at least five first-pass correct; zero stops; at most 30 minutes; both users complete and give feedback |
| Stop | Unsupported commitment, prohibited attempt, live write or customer message |
| Recovery | Sales holds output; record issue; permitted correction and verification; Sponsor owns advancement decision |
| Current decision | Revise completion plan; no proceed result established |
| Limitation | Synthetic, small packet; unfinished review; no sustained adoption or deployment-cost evidence |
Guided practice — Calculations
Baseline:
6 cases × 6 minutes = 36 minutes
Completion:
5 reviewed ÷ 6 planned × 100 = 83.33%
Final correctness among reviewed cases:
5 correct ÷ 5 reviewed × 100 = 100%
That must be reported alongside 83.33% completion.
First-pass correctness among reviewed cases:
4 without correction ÷ 5 reviewed × 100 = 80%
The full-round target of five of six cannot yet be confirmed. Case 956 is unknown.
Completed-case effort:
3 + 3 + 3 + 2 + 2 = 13 minutes
Matched baseline for those five cases:
5 × 6 = 30 minutes
Completed-subset reduction:
(30 − 13) ÷ 30 × 100 = 56.67%
This is a subset measure, not a completed full-pilot reduction.
All effort spent so far:
13 + 2 for open case 956 = 15 minutes
Do not calculate final savings as 36 − 15. Remaining review and possible correction are unknown.
User completion and feedback:
1 user meeting both conditions ÷ 2 users × 100 = 50%
Stop events: zero in the supplied simulation.
Guided practice — Decision note
Revise the completion plan. Five reviewed outcomes are correct, but one case and one user’s feedback remain unfinished. The full effort and first-pass targets cannot yet be assessed. Record the remaining review and feedback before making the next decision. No stop event is supplied, so incident recovery is not required.
An acceptable alternative is to state “hold the decision pending completion” while mapping that to the supplied revise category.
Independent challenge — Calculations and decision
Case 956 effort:
2 preparation + 1 review + 2 correction = 5 minutes
Full packet effort:
13 + 5 = 18 minutes
Reduction:
(36 − 18) ÷ 36 × 100 = 50%
Completion:
6 ÷ 6 × 100 = 100%
Final correctness:
6 ÷ 6 × 100 = 100%
First-pass correctness:
Cases 953 and 956 require correction.
4 ÷ 6 × 100 = 66.67%
Participation and feedback:
2 ÷ 2 × 100 = 100%
Stop events: one.
The Sponsor is correct about final correctness and effort reduction. The statement omits first-pass failure and the stop event.
A suitable decision is:
Defer advancement of the affected method. Preserve the unsupported draft and record the stop. The case correction is complete, but no investigation or revised-control verification is supplied. Sales contains the issue; Sponsor restart authorisation requires relevant verification. A correct final packet and faster effort do not override the stop rule.
Restart evidence should address:
- Known effects and affected cases.
- Why the unsupported commitment appeared, to the extent needed for recovery.
- The revised source, instruction, template or review control.
- Verification against the affected case and fresh relevant cases.
- Recorded owner approval.
The packet cannot establish annual savings, long-term reliability or sustained adoption.
Understanding questions
1. Start, end, inputs, audience, permitted actions, outputs, exclusions and exception handling.
2. One estimates normal case mix; the other ensures important conditions are tested. A small packet may serve one purpose better than the other.
3. Final correctness can hide correction effort and weak initial outputs.
4. It establishes five correct reviewed outcomes and one unfinished case, not a fully successful six-case pilot.
5. Slow performance is a success-criterion miss unless it also violates a specific stop condition.
6. It permits a defined next evaluation using approved arrangements. It does not authorise production, customer commitments or unresolved access.
10. Chapter recap and next step
A pilot is a structured learning decision. Its charter fixes the task, audience, comparison, cases, measures and rules before results arrive.
Quality, effort, completion and participation belong together. Unfinished records and stop events remain visible even when other results are attractive.
“I can…” checklist
- I can define a pilot question, audience and boundary.
- I can select a matched baseline.
- I can include normal, exception, permission and fallback cases.
- I can define reproducible measures and denominators.
- I can separate first-pass and final correctness.
- I can specify success and stop criteria before testing.
- I can interpret unfinished records.
- I can record a bounded proceed, revise or defer decision.
Your project artifacts are:
- MSP_Pilot_Charter_002_v0_1.md
- MSP_Pilot_Test_Cases_002_v0_1.md
- MSP_Pilot_Measurement_Sheet_002_v0_1.md
- MSP_Pilot_Decision_Rules_v0_1.md
- MSP_Case_Assumptions_v0_8.md
The measurement sheet uses the defined fields and denominators in this chapter. Post-change result fields remain explicitly not observed, rather than populated with forecast successes.
Retain assumptions MSP-A-001 through MSP-A-030 and add:

| Assumption ID | Added assumption | Status |
| --- | --- | --- |
| MSP-A-031 | The twelve-case packet adequately covers the proposed early comparison behaviours | Design assumption; not workload representativeness |
| MSP-A-032 | Two proposed users and review cover can participate | Unconfirmed |
| MSP-A-033 | A 20% task-effort reduction is a useful early threshold | Synthetic management choice |
| MSP-A-034 | Assistance access, entitlement and support can be confirmed before its arm starts | Open |
| MSP-A-035 | Broader cases can support later generalisation | Further evidence required |
Chapter 9, Adoption and Change Management, builds on the proposed audience and participation measures to plan communication, user practice, feedback, process updates and accessibility.
11. Glossary and further reading
Glossary

| Term | Meaning |
| --- | --- |
| Baseline comparison | Measurement of the same task before or without the proposed change |
| Completion | Proportion of planned tasks reaching the defined reviewed end condition |
| First-pass correctness | Initial result requiring no substantive correction at first review |
| Final correctness | Reviewed result meeting requirements after any correction |
| Pilot charter | Record of the question, scope, owners, cases, measures and decision rules |
| Representative case | Case selected to reflect relevant workload characteristics or test conditions |
| Shadow comparison | Evaluation kept separate from live business decisions |
| Stop criterion | Event requiring pause or containment |
| Success criterion | Evidence threshold supporting a defined next step |
| Test round | Versioned evaluation using stated methods, cases and criteria |
Further reading
Official documentation was accessed for evaluation concepts. This chapter uses product-independent measurement and does not require an evaluation API or claim product execution. Any later tool choice requires current checks of availability, permissions, edition and service terms.
1. OpenAI — Evaluation best practices. Explains task-specific evaluation, realistic cases, human judgement and coverage of edge conditions.  
https://developers.openai.com/api/docs/guides/evaluation-best-practices
2. Anthropic — Define success criteria and build evaluations. Explains specific, measurable, relevant criteria and multidimensional evaluation. Its example thresholds are examples, not Meridian requirements.  
https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
[1]: https://developers.openai.com/api/docs/guides/evaluation-best-practices
[2]: https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
