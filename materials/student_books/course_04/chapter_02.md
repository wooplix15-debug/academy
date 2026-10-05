---
course_id: "C04"
chapter_id: "C04-CH02"
chapter_number: 2
chapter_title: "Process Discovery and Problem Framing"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "partially_verified"
---

# Process Discovery and Problem Framing

1. What you will learn
Before you can improve a process, you need to understand what actually happens. A description such as “Sales receives an enquiry, Operations checks it, and Sales sends a quotation” is a useful starting point. It does not yet explain where work waits, why it returns or what happens when information is missing.
In this chapter, you will learn to:
- Define a process trigger, boundary and end condition.
- Identify the people involved and the information passed between them.
- Map decisions, queues, rework and exceptions.
- Separate staff effort from elapsed time.
- Distinguish supplied facts, assumptions and unknowns.
- Write a problem statement that describes an evidenced business issue.
Your required practice is to map a familiar process, including its trigger, roles, handoffs and exceptions, and mark facts separately from assumptions. A complete Meridian Supply practice packet is supplied if you do not have a permission-cleared company process.
Prerequisites and continuity
Chapter 1 introduced rules, integrations, generative assistance and agents. You should now recognise that different tasks may need different capabilities.
Meridian’s established discovery candidates remain:

| Opportunity ID | Existing candidate |
| --- | --- |
| MSP-OPP-001 | Improve required-field completeness and validity |
| MSP-OPP-002 | Reduce effort spent organising varied enquiry wording |
| MSP-OPP-003 | Investigate repeated entry of approved enquiry information |
The supplied weekly baseline remains 120 completed enquiries, 18 initial staff minutes per enquiry and 24 enquiries requiring six additional rework minutes: 38.4 staff hours in total.
The Chapter 1 pilot reference packet remains a separate six-case packet with 36 manual preparation minutes. Pilot MSP-PILOT-001 is proposed, not executed.
This chapter introduces new, explicitly labelled synthetic discovery records. They do not replace the earlier enquiry records or establish pilot results.
Your contribution to the course project
You will produce a Current-State Process Map, a Discovery Evidence Register and an Evidence-Based Problem Statement.
These artifacts support your Business Automation Pilot Proposal. They help you choose a process boundary, explain where the problem occurs and avoid building a solution around an untested assumption.
2. Lessons
Lesson 1 — Define where the process starts, ends and changes hands
A process is a connected set of activities that turns an input into a result. A department is not a process. “Sales” names a team; “receive an enquiry and issue a quotation” describes work with a possible boundary.
The trigger starts a particular instance of the process. Receiving a customer enquiry is a trigger. “Every Monday” can also be a trigger for scheduled work. Official automation documentation uses the same basic idea: a trigger is the event that starts a flow.1
A boundary states what you include. It should identify a start condition and an end condition.
For Meridian:
Start when a customer enquiry becomes available in the Sales inbox. End when Sales sends a quotation or records an authorised closure.
Order acceptance, stock reservation, fulfilment and invoicing are outside this discovery boundary. They may influence it, but they are different processes.
A case can remain inside the boundary without reaching an end condition. An enquiry waiting for availability confirmation is still open.
Identify people by their work
A process map should show who performs an activity and who receives its output.

| Participant | Role in Meridian’s discovery |
| --- | --- |
| Customer | Supplies the enquiry, clarification or withdrawal |
| Sales Lead and Sales staff | Own intake, customer clarification, quotation preparation and customer-facing acceptance |
| Operations Lead and Operations staff | Check product and availability information; resolve availability exceptions |
| IT Lead | Investigates access exceptions and later assesses technical connections |
| Finance Lead | Checks effort and cost evidence; does not perform every enquiry step |
| Sponsor | Owns the later investment decision; does not approve every quotation in this scenario |
Do not insert a participant into every case simply because that person belongs to the management team.
Worked example: make a handoff visible
“Sales asks Operations to check the enquiry” hides several questions.
A clearer handoff description is:

| Handoff element | Completed description |
| --- | --- |
| Sender | Sales |
| Receiver | Operations |
| Item transferred | Enquiry reference, product code, quantity and requested delivery date |
| Receiver’s task | Check the product and availability information |
| Completion evidence | Operations records checked facts or a specific exception |
| Return owner | Sales, if customer information needs correction; Operations, if availability remains unresolved |
A handoff transfers work or information between participants. Sending an item does not prove that the receiver has started it. That gap may be a queue.
Check L1: Why is “Sales → Operations” insufficient as a complete handoff description?
Lesson 2 — Show decisions, exceptions and rework instead of drawing only the normal path
A decision selects a route according to a condition. Useful decision labels are questions with clear answers:
- Are required fields complete and valid?
- Is source access permitted?
- Is the product code recognised?
- Can Operations complete the availability check?
“Check enquiry” is an activity. “Is the enquiry complete?” is a decision. Keeping them separate helps you identify the rule or judgement behind the route.
An exception is a condition requiring a different path from routine processing. Missing information, an unknown product and denied source access are examples.
An exception is not necessarily an error. A customer may legitimately request more units than a stock snapshot shows. The process must handle that condition even when everyone has performed their task correctly.
Rework means repeating or correcting work because an earlier result was incomplete or incorrect. A wrong copied product code is rework. Waiting for a legitimate availability decision is not automatically rework.
Worked example: two superficially similar returns
Consider these supplied situations:

| Situation | Classification | Reason |
| --- | --- | --- |
| Sales notices missing quantity before sending the request to Operations | Intake exception | The request needs clarification before the handoff |
| Sales forwards a request without quantity; Operations returns it | Rework after handoff | The receiving team could not use the earlier output |
| Operations finds a request for 60 units against a 40-unit snapshot | Availability exception | The customer request may be valid, but availability needs investigation |
| Sales copies BF-10 as BF-1O, using the letter O instead of zero | Data-entry error requiring rework | The source value was changed incorrectly |
These distinctions matter when measuring improvement. A better intake check might reduce Operations returns. It would not necessarily remove genuine stock shortages.
An exception path needs a destination and an owner. “Reject” is incomplete unless you explain who receives the issue, what happens next and whether the case closes or stays open.
For denied source access, the safe path is to stop source enrichment and refer the access issue to IT. Sales tracks the enquiry. The map must not silently replace this with “use another person’s account”.
Check L2: Why should a valid stock-shortage request and an incorrectly copied product code appear as different exception paths?
Lesson 3 — Find waiting without confusing it with staff effort
Staff effort is time spent actively working. Elapsed time is the interval between two events. A customer experiences elapsed time, including waiting.
A queue contains work ready for an activity but not yet started. A request may wait in an Operations queue even though no one is actively working on it.
Other waits should be named accurately. Waiting for a customer reply is different from waiting for an internal team to start work. Both affect elapsed time, but they have different owners and possible remedies.
For a serial case with complete, non-overlapping records:
Elapsed time = active processing intervals + waiting intervals
For the simple examples in this chapter, staff work does not overlap. In a real process, two people may work simultaneously. Their combined staff effort can then exceed the elapsed processing interval. Do not apply the serial formula without checking that assumption.
Worked example: a short task inside a long process
A supplied enquiry trace shows:

| Event | Time on 2026-10-05 |
| --- | --- |
| Enquiry received; Sales starts | 09:00 |
| Sales finishes intake; Operations queue begins | 09:06 |
| Operations starts | 10:00 |
| Operations finishes; Sales quotation queue begins | 10:08 |
| Sales resumes | 10:30 |
| Sales finishes review and sends quotation | 10:34 |
All times use the same synthetic local clock, UTC+00:00. There are no breaks or overlapping activities in this trace.
Staff effort:
6 Sales intake minutes + 8 Operations minutes + 4 Sales quotation minutes = 18 staff minutes
Waiting:
54 Operations queue minutes + 22 Sales queue minutes = 76 minutes
Elapsed time:
10:34 − 09:00 = 94 minutes
Reconciliation:
18 + 76 = 94 minutes
Automating two minutes of intake would affect only part of this case. It would not automatically remove the 76 minutes of waiting.
The same evidence also does not prove that Operations is understaffed. The queue could reflect batching, competing priorities, working patterns or another cause. Queue duration is evidence of waiting; its cause still requires investigation.
Check L3: In this trace, which is larger: active effort or waiting? What should you investigate before claiming a staffing problem?
Lesson 4 — Separate facts, assumptions and customer impact
A process map is useful only if you know which parts are supported.
Use this chapter’s simple legend:

| Label | Meaning | Example |
| --- | --- | --- |
| F — Fact | Explicitly supported by a supplied record or scenario description | “Case 101 waited 54 minutes before Operations started” |
| A — Assumption | A proposition being used or considered without sufficient evidence | “The same queue pattern occurs every week” |
| U — Unknown | Information intentionally absent or not yet established | “Why Operations started at 10:00” |
In this synthetic case, “fact” means a fact within the supplied scenario. It does not mean evidence collected from a real company.
The content of an interview statement may also be uncertain. It can be a fact that the Sponsor said “Operations causes every delay”. That does not make the underlying claim true.
Ask three questions:
1. What exactly does the source establish?
2. How broad is the claim?
3. What remains unexplained?
Worked example: from complaint to problem statement
Complaint:
Quotations take too long because Sales writes slowly.
Evidence:
In one supplied case, total elapsed time was 94 minutes, including 76 waiting minutes and 18 active staff minutes.
Better problem statement:
The supplied case contains substantial waiting between Sales and Operations activities. Investigate the handoff queues and intake quality before selecting a drafting solution.
The improved statement identifies an evidenced condition without inventing its cause.
Customer impact should also be separated into measured and hypothesised effects.
- A late quotation timestamp establishes a longer response interval.
- A customer asking twice for an update establishes an additional contact.
- “The customer was frustrated” needs customer evidence.
- “The business lost the order” needs outcome evidence.
Process discovery helps you frame the problem. Chapter 3 turns recurring issues into use-case cards. Chapters 5 and 6 assess value and compare solutions.
Check L4: What evidence would distinguish “customers wait longer” from “longer waits cause lost sales”?
3. Visual explanation — Meridian’s current-state routes
The following is a simplified current-state discovery map. It uses ordinary flowchart conventions, not full Business Process Model and Notation, or BPMN. BPMN is a formal, implementation-independent process notation maintained by the Object Management Group.2
flowchart TD
    A[Customer enquiry available] --> B[Sales intake queue]
    B --> C[Sales records and checks request]
    C --> D{Required fields usable?}
    D -->|No| E[Sales requests customer clarification]
    E --> F[Wait for customer reply]
    F --> C
    D -->|Yes| G{Source access permitted?}
    G -->|No| H[IT access exception; Sales tracks open case]
    H -->|If access is resolved| C
    G -->|Yes| I[Operations queue]
    I --> J[Operations checks product and availability]
    J --> K{Information usable?}
    K -->|No: missed or copied field| L[Return to Sales for correction]
    L --> C
    K -->|Yes| M{Availability issue unresolved?}
    M -->|Yes| N[Operations owns availability exception; case waits]
    N -->|When resolved| J
    M -->|No| O[Sales quotation queue]
    O --> P[Sales prepares, checks and sends quotation]
    P --> Q[Quotation sent: end]
The map makes three learning points visible.
First, handoffs create possible queues. The arrows do not mean work starts immediately.
Second, rework returns to an earlier activity. Sales may perform an intake check again after Operations returns a missed or incorrectly copied field.
Third, an exception can leave a case open. The arrows labelled “if” and “when” describe permitted recovery routes, not evidence that recovery has occurred in every case.
A customer withdrawal can end the process through an authorised closure. No withdrawal appears in the main six-case packet below, so that route is examined in the independent challenge.
4. Worked case — Discover what the sample actually supports
New scenario inputs
This chapter adds a separate discovery packet under these source IDs:

| Source ID | Supplied material |
| --- | --- |
| MSP-DISC-001 | Process description and role responsibilities used in the lessons |
| MSP-DISC-002 | Six-case input and timing packet below |
| MSP-DISC-003 | Detailed event trace for MSP-ENQ-101, shown in Lesson 3 |
| MSP-DISC-004 | Stakeholder statements below |
The following extensions are explicit synthetic scenario assumptions:
- Current intake checking is manual and can miss required-field problems.
- Operations returns unusable handoffs to Sales.
- Operations owns unresolved availability issues.
- Sales tracks enquiries blocked by an access issue while IT investigates.
- No supplied source confirms a delivery commitment. A requested date must remain distinct from a promise.
- All recorded activities in this packet are serial and use non-overlapping time categories.
These describe the case being studied. They are not Wooplix policies or universal business requirements.
Case conditions
The catalogue still recognises BF-10 as a 10 mm brass fitting. The stock snapshot lists 40 units, and no approved substitute is supplied.

| Enquiry ID | Supplied condition |
| --- | --- |
| MSP-ENQ-101 | BF-10, 25 units; normal handoff |
| MSP-ENQ-102 | BF-10, 10 units; normal handoff |
| MSP-ENQ-103 | Quantity missing at first Operations handoff; customer later supplies 12 units |
| MSP-ENQ-104 | Source code BF-10 copied as BF-1O; corrected to BF-10 using the original enquiry |
| MSP-ENQ-105 | BF-10, 4 units; source access denied; no resolution supplied |
| MSP-ENQ-106 | BF-10, 60 units; unresolved availability exception |
All six request delivery on 2026-10-12. That is a customer request, not confirmed delivery.
Complete timing dataset
Dates are 2026-10-05, using UTC+00:00. For open cases, end_or_cutoff is the snapshot cutoff, not a completion time.
operations_returns counts returns to Sales caused by missing or incorrectly copied information. It does not count an availability hold.
enquiry_id,received,end_or_cutoff,status,initial_staff_min,correction_staff_min,intake_queue_min,operations_queue_min,sales_quote_queue_min,customer_wait_min,access_wait_min,availability_wait_min,operations_returns
MSP-ENQ-101,09:00,10:34,quotation_sent,18,0,0,54,22,0,0,0,0
MSP-ENQ-102,09:10,10:10,quotation_sent,18,0,0,30,12,0,0,0,0
MSP-ENQ-103,09:20,12:20,quotation_sent,18,6,0,30,6,120,0,0,1
MSP-ENQ-104,09:30,11:00,quotation_sent,18,6,0,42,24,0,0,0,1
MSP-ENQ-105,09:40,13:00,open_access,4,0,0,0,0,0,196,0,0
MSP-ENQ-106,09:50,13:00,open_availability,14,0,0,46,0,0,0,130,0
The correction minutes are additional to initial effort. Queue values for returned cases include all visits to that queue.
Stakeholder statements

| Speaker | Supplied statement |
| --- | --- |
| Sales Lead | “Operations returned two cases in this packet for information correction.” |
| Operations Lead | “Case 106 remains with us because the requested quantity exceeds the stock snapshot.” |
| Sponsor | “I suspect slow drafting is the main cause of delay.” |
| IT Lead | “We have not established why source access was denied for case 105.” |
| Finance Lead | “We need to keep staff effort and customer elapsed time separate.” |
The first two statements are supported by the case packet. The Sponsor’s causal explanation remains a hypothesis.
Step 1: reconcile individual cases
For case 103:
Elapsed time = 12:20 − 09:20 = 180 minutes
Staff effort = 18 + 6 = 24 minutes
Waiting = 30 + 6 + 120 = 156 minutes
24 + 156 = 180 minutes
The case reconciles. Most of its waiting is for customer clarification, although an unusable handoff caused the clarification cycle.
For case 106:
Elapsed time to cutoff = 13:00 − 09:50 = 190 minutes
Recorded effort = 14 minutes
Waiting = 46 + 130 = 176 minutes
14 + 176 = 190 minutes
This is an open-case age, not quotation response time.
Step 2: define a reproducible completed-case measure
Use only cases with status quotation_sent: 101, 102, 103 and 104.
Mean quotation response interval
(94 + 60 + 180 + 90) minutes ÷ 4 completed quotations = 106 minutes/quotation
Mean staff effort
(18 + 18 + 24 + 24) staff minutes ÷ 4 = 21 staff minutes/quotation
Mean waiting
(76 + 42 + 156 + 66) minutes ÷ 4 = 85 minutes/quotation
The two open cases are excluded from these completion measures. They must still be reported: one is awaiting access resolution and one is awaiting availability resolution.
A completed-case average can understate the experience of the whole cohort when long-running cases remain unfinished.
Step 3: measure returns using the supplied flags
Define first-pass handoff completion for this example as:
A quotation-completed case with no Operations return for information correction.
Two of four completed cases have zero returns.
First-pass handoff completion = 2 ÷ 4 × 100 = 50%
This is a sample measure with a defined denominator. It is not Meridian’s company-wide rate.
Case 105 had no Operations assessment. Case 106 is unfinished. Neither belongs in this completed-quotation denominator. Zero recorded returns in an unfinished record does not automatically mean successful completion.
Step 4: complete the process artifact
Completed artifact: MSP_Current_State_Process_Map_v0_1.md

| Step | Owner | Input or trigger | Output and next route | Evidence label |
| --- | --- | --- | --- | --- |
| Receive and queue enquiry | Sales | Customer message available | Enquiry waits for intake | F: DISC-001 |
| Record and check request | Sales | Enquiry and required fields | Usable request, clarification or access exception | F: DISC-001 |
| Obtain clarification | Sales and Customer | Missing or unknown required information | Customer reply returns to Sales checking | F: DISC-001; DISC-002 case 103 |
| Investigate access block | IT; Sales tracks case | Source use denied | Case stays open until authorised resolution | F: DISC-002 case 105 |
| Queue for Operations | Operations | Usable handoff | Work waits for Operations start | F: DISC-002; DISC-003 |
| Check product and availability | Operations | Request and approved sources | Checked facts, correction return or availability hold | F: DISC-001; DISC-002 |
| Correct unusable handoff | Sales | Specific return reason | Corrected information sent back through checking | F: DISC-002 cases 103–104 |
| Resolve availability issue | Operations | Unresolved availability | Open case until issue is resolved | F: DISC-002 case 106 |
| Queue, prepare and check quotation | Sales | Operations result | Checked quotation ready to send | F: DISC-001; DISC-003 |
| Send quotation | Sales | Accepted customer-facing quotation | Quotation-sent end condition | F: DISC-002 |
These labels support the described route. They do not establish why every queue occurred.
Step 5: write the problem statement
Completed artifact: MSP_Problem_Statement_v0_1.md
In the supplied six-case discovery packet, four enquiries reached quotation sent. Their mean response interval was 106 minutes, comprising 21 staff minutes and 85 waiting minutes. Two completed cases were returned by Operations for information correction. Two additional cases remained open at cutoff: one access block and one availability issue. Investigate intake quality and handoff waiting, while treating access and availability as distinct exceptions. The packet does not establish that drafting is the main delay cause or that these figures represent a typical week.
A common mistake would be to write:
An AI drafting assistant will solve Meridian’s quotation delays.
The corrected statement describes the problem before deciding the solution.
5. Try it yourself — Guided practice
Learning goal and access
Map the enquiry intake subprocess, from message receipt to a usable Operations handoff or an unresolved intake exception.
Use the supplied afternoon packet. No product account is needed. You can work on paper or in a local document. This practice demonstrates process reasoning, not live system behaviour.
In a group, use the Sponsor, Sales, Finance, Operations and IT perspectives. Individually, ask what each role would need to know before accepting your map.
Complete practice inputs
This packet is separate from the morning discovery packet.
The required intake fields are product code, positive whole-number quantity and requested delivery date. Source access must be permitted before source enrichment. The only recognised product is BF-10.

| Record ID | Customer input and permitted correction |
| --- | --- |
| MSP-ENQ-201 | BF-10, 20 units, requested date 2026-10-14; access permitted |
| MSP-ENQ-202 | BF-10, quantity missing, requested date 2026-10-14; customer supplies 12 units after clarification |
| MSP-ENQ-203 | BF-1O, 8 units, requested date 2026-10-14; customer explicitly corrects the code to BF-10 |
| MSP-ENQ-204 | BF-10, 4 units, requested date 2026-10-14; source access denied; no resolution supplied |
Messages use the synthetic contact buyer@example.com.
The supplied intake method is:
1. Wait for Sales to start.
2. Check required fields.
3. Ask the customer to resolve missing or unknown values.
4. Recheck the reply.
5. Check source permission.
6. Send a usable request to Operations, or refer the access exception to IT while Sales tracks the open case.
For cases 202 and 203, Sales performs three minutes before the clarification wait and three minutes after it.
enquiry_id,received,sales_start,reply_received,handoff_or_cutoff,status,staff_effort_min,intake_queue_min,customer_wait_min,access_wait_min
MSP-ENQ-201,14:00,14:10,not_applicable,14:16,operations_handoff,6,10,0,0
MSP-ENQ-202,14:05,14:15,14:48,14:51,operations_handoff,6,10,30,0
MSP-ENQ-203,14:10,14:20,14:43,14:46,operations_handoff,6,10,20,0
MSP-ENQ-204,14:15,14:25,not_applicable,15:00,open_access,4,10,0,31
All times are on 2026-10-05, UTC+00:00.
Two additional claims are supplied:
- “These four cases represent a typical month.” No supporting sample evidence is supplied.
- “An automated field check would eliminate all intake delay.” This has not been tested.
Blank learner worksheets

| Step or decision | Owner | Input | Output or branch | Handoff/queue/exception | F, A or U and source |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
| Case | End status | Elapsed to handoff/cutoff | Effort | Waiting | Interpretation |
| MSP-ENQ-201 |  |  |  |  |  |
| MSP-ENQ-202 |  |  |  |  |  |
| MSP-ENQ-203 |  |  |  |  |  |
| MSP-ENQ-204 |  |  |  |  |  |
Steps and expected intermediate results
1. Write the boundary.
- Expected result: receipt is the trigger; Operations handoff is the successful end; unresolved access remains open.
2. Draw the normal path.
- Expected result: receipt, queue, Sales check, permission decision and Operations handoff.
3. Add clarification and access branches.
- Expected result: a customer-reply loop and a separately owned access exception.
4. Annotate evidence.
- Expected result: supplied routes and records marked F; both broad claims marked A; access-denial cause marked U.
5. Reconcile each case.
- Expected result: elapsed time equals supplied effort plus non-overlapping waits.
6. Write a short problem statement.
- Expected result: a statement reporting actual packet conditions without claiming monthly representativeness or guaranteed automation effects.
Your final artifact is MSP_Intake_Subprocess_Map_Practice.md, containing the map, timing table, evidence annotations and problem statement.
An optional company alternative is acceptable if you can supply equivalent permission-cleared facts. Missing company timestamps should remain unknown rather than being estimated silently.
Retain your synthetic final artifact. No system cleanup is required.
6. Independent challenge
A new packet adds a customer withdrawal and an incomplete record. These are exercise variants, not amendments to the main discovery packet.

| Record ID | Complete supplied input |
| --- | --- |
| MSP-ENQ-301 | Received 2026-10-06 at 09:00; quotation sent at 10:00. Staff effort 18 minutes; Operations queue 10 minutes; Sales queue 2 minutes; customer clarification wait 30 minutes. |
| MSP-ENQ-302 | Received at 09:10; customer sends an authorised withdrawal at 10:10. Sales records closure immediately. Staff effort 6 minutes; intake queue 4 minutes; customer wait 50 minutes. No Operations handoff occurred. |
| MSP-ENQ-303 | Received at 09:20; snapshot cutoff 11:00. Last confirmed event is Operations queue entry at 09:26. Operations start timestamp is missing. Six staff minutes are recorded, but effort-log completeness is unconfirmed. Status is open; whether Operations started is unknown. |
Times use UTC+00:00. A customer withdrawal before quotation may close the enquiry when Sales records it.
The Sponsor states:
Operations causes every delay, so we should automate Operations first.
You may request permission-cleared event records from Sales and Operations. Private employee messages are outside the permitted evidence set.
Deliverables
1. Extend the current-state map to include authorised withdrawal and closure.
2. Annotate the missing event without inventing a process failure.
3. Calculate quotation response time using an explicit denominator and exclusions.
4. Explain what the packet supports and does not support about the Sponsor’s claim.
5. Identify two specific evidence requests.
Success criteria
Your map must show who closes a withdrawn case. Your calculation must exclude non-quotation outcomes. Your explanation must distinguish known waiting from missing evidence and avoid attributing unrecorded time to a team.
7. Common problems and recovery

| Symptom | Diagnosis | Correction | Verification |
| --- | --- | --- | --- |
| The map starts with “Sales” | A team name has replaced the trigger | Write the event that starts a case | A reader can identify when a new case exists |
| All arrows go directly to the next activity | Waiting and handoff acceptance are hidden | Add named queues and receiving owners | Trace the interval between ready and started |
| Every unusual case is called an error | Legitimate exceptions are mixed with rework | Separate correction, clarification, access and availability routes | Each route has a reason and owner |
| A missing timestamp is treated as a system failure | Absence of evidence has become a technical diagnosis | Mark the event unknown and request permitted records | The map does not invent an outage |
| Completed cases look fast while open cases disappear | The denominator hides unfinished work | Report completion measures and open-case ages separately | Every supplied case appears in the cohort summary |
| Interview opinions become map facts | A statement has been confused with confirmation | Record the statement and label its underlying claim appropriately | Each factual route has a supporting source |
| A map contains the proposed automation | Current and future states have been mixed | Keep observed/supplied routes separate from change hypotheses | The current-state artifact can be explained without assuming implementation |
8. Check your understanding
1. What are Meridian’s trigger and quotation-sent end condition? Why is a stock-shortage case still open?
2. What information makes a handoff more useful than an arrow between two departments?
3. Why is customer clarification waiting different from an Operations queue?
4. In the morning packet, why are cases 105 and 106 excluded from mean quotation response time but still reported?
5. What is the difference between “the Sponsor said drafting is the problem” and “drafting is the problem”?
6. Which evidence would you request before claiming that reducing rekeying will reduce customer waiting?
9. Solutions and explanations
Lesson checks
L1: The arrow does not specify the item transferred, the receiver’s task, acceptance conditions or return owner. A complete handoff makes these visible.
L2: The copied-code error requires correction of earlier work. A valid stock-shortage request requires an availability decision. Their causes, owners and possible remedies differ.
L3: Waiting is larger: 76 minutes compared with 18 active staff minutes. Investigate queue arrival, workload, priorities, batching and start-time evidence before diagnosing a staffing problem.
L4: Receipt and quotation timestamps can establish waiting or response intervals. Lost-sales claims also need order outcomes and evidence connecting those outcomes to delay. Timing alone does not establish the commercial cause.
Guided practice — Completed map
A correct text map is:
Enquiry received → Sales intake queue → Sales checks fields → if missing or unknown, request clarification and wait for customer reply → recheck → permission decision → if permitted, hand off to Operations; if denied, refer to IT and keep the case open under Sales tracking.

| Step or decision | Owner | Input | Output or branch | Type | Evidence |
| --- | --- | --- | --- | --- | --- |
| Receive and queue | Sales | Customer message | Ready for Sales checking | Trigger and queue | F: practice method and times |
| Check fields | Sales | Product, quantity, date | Usable or clarification needed | Activity and decision | F: supplied requirements |
| Clarify missing/unknown value | Sales and Customer | Specific missing or unknown value | Authorised reply | Exception and external wait | F: cases 202–203 |
| Recheck reply | Sales | Customer correction | Valid request | Loop | F: supplied method |
| Check permission | Sales; IT for exceptions | Source-use permission | Continue or stop enrichment | Decision | F: supplied method |
| Send usable request | Sales → Operations | Checked fields | Operations handoff | Handoff and subprocess end | F: cases 201–203 |
| Investigate access | IT; Sales tracks | Denied source use | Open case pending resolution | Exception | F: case 204 |
The cause of case 204’s access denial is U. The monthly-representativeness claim and the claim that validation removes all delay are A.
Guided practice — Timing solution

| Case | End status | Elapsed to handoff/cutoff | Effort | Waiting | Interpretation |
| --- | --- | --- | --- | --- | --- |
| MSP-ENQ-201 | Operations handoff | 16 minutes | 6 minutes | 10 minutes | Completed intake |
| MSP-ENQ-202 | Operations handoff | 46 minutes | 6 minutes | 40 minutes | Includes 30-minute customer clarification wait |
| MSP-ENQ-203 | Operations handoff | 36 minutes | 6 minutes | 30 minutes | Customer authorised the product correction |
| MSP-ENQ-204 | Open access | 45 minutes | 4 minutes | 41 minutes | Age to cutoff, not completed intake time |
For case 202:
14:51 − 14:05 = 46 minutes
6 effort + 10 intake queue + 30 customer wait = 46 minutes
For case 204:
15:00 − 14:15 = 45 minutes
4 effort + 10 intake queue + 31 access wait = 45 minutes
If you report mean time to successful intake handoff:
(16 + 46 + 36) ÷ 3 = 32⅔ minutes, approximately 32.7 minutes per handoff.
Case 204 is excluded because it did not reach handoff. Report it separately as an open 45-minute-old case.
Guided practice — Completed problem statement
Three of four supplied afternoon enquiries reached Operations handoff. Two needed customer clarification, and one additional case remained open because source access was denied. Successful handoffs averaged approximately 32.7 elapsed minutes. Investigate required-field quality, intake waiting and access-exception handling separately. The packet does not establish a typical monthly pattern or prove that automated validation would eliminate customer or access waiting.
Independent challenge — Explained solution
Map extension:
Before quotation is sent, an authorised customer withdrawal → Sales records closure → end: withdrawn.
This end condition is different from quotation sent.
Missing event:
Annotate case 303’s Operations start as unknown. Its last confirmed state was queue entry at 09:26. Do not conclude that Operations never started or that a technical failure occurred.
Quotation response measure:
Only case 301 reached quotation sent.
10:00 − 09:00 = 60 minutes
Mean = 60 minutes ÷ 1 completed quotation = 60 minutes/quotation
Exclude case 302 because it was withdrawn, and case 303 because it was open. Disclose the cohort: one quotation, one withdrawal and one open case.
Case 301 reconciles:
18 effort + 10 Operations queue + 2 Sales queue + 30 customer wait = 60 minutes
Case 302 also reconciles:
6 effort + 4 intake queue + 50 customer wait = 60 minutes
For case 303, you can calculate age:
11:00 − 09:20 = 100 minutes
You cannot reliably allocate that interval into processing and waiting. The effort log is incomplete and the Operations start event is absent.
Sponsor’s claim:
The packet does not support “Operations causes every delay”. Case 301 includes more customer clarification waiting than Operations queue time. Case 302 never reached Operations. Case 303 contains insufficient evidence to assign its elapsed time.
This does not prove that Operations has no problems. It shows that the proposed universal explanation is unsupported.
Two suitable evidence requests:
1. Request the permission-cleared Operations receipt/start/completion records for case 303.
2. Request a complete activity log for case 303 and a broader sample of handoff timings before treating this packet as typical.
Understanding questions
1. Trigger: enquiry available in the Sales inbox. Quotation end: Sales sends the accepted quotation. A shortage case is still open because its availability issue remains unresolved.
2. Include sender, receiver, transferred information, receiving task, completion evidence and return ownership.
3. Customer clarification waits for an external reply. An Operations queue contains work ready for internal processing. Faster internal processing does not guarantee a faster customer reply.
4. Neither reached quotation sent. Excluding them makes the completion calculation valid; reporting them prevents the summary from hiding unfinished work.
5. The first is a supported statement about what was said. The second is a causal claim requiring process evidence.
6. Request rekeying effort, error/rework records, handoff timing and the location of rekeying within the elapsed-time path. A reduction in active effort may release capacity without changing the dominant wait.
10. Chapter recap and next step
A useful current-state map shows more than activity names. It explains what starts a case, who receives each handoff, which decisions change the route, where work waits and how exceptions return or remain open.
Evidence labels keep the map honest. A timestamp supports an interval; it does not automatically explain its cause. A completed-case average describes its denominator; it does not describe unfinished cases.
“I can…” checklist
- I can define a trigger, boundary and end condition.
- I can show roles and handoff information.
- I can distinguish queues, external waits, rework and legitimate exceptions.
- I can reconcile simple serial effort and elapsed-time records.
- I can state a denominator and report excluded open cases.
- I can label facts, assumptions and unknowns.
- I can write an evidenced problem statement without assuming a solution.
Your project artifacts are:
- MSP_Current_State_Process_Map_v0_1.md
- MSP_Discovery_Evidence_Register_v0_1.md
- MSP_Problem_Statement_v0_1.md
- MSP_Case_Assumptions_v0_2.md
For the evidence register, retain the four source IDs, the completed-case calculations and the explicit exclusions from this chapter.
For assumptions version 0.2, retain Chapter 1 assumptions MSP-A-001 to MSP-A-004 and add:

| Assumption ID | Added assumption | Status |
| --- | --- | --- |
| MSP-A-005 | Discovery queue patterns represent a typical week | Unconfirmed |
| MSP-A-006 | Drafting is the main cause of quotation delay | Unsupported by the packet |
| MSP-A-007 | Longer quotation waits cause lost sales | No customer-outcome evidence supplied |
Chapter 3, Opportunity Identification, will turn recurring, evidenced issues into use-case cards showing the affected team, task, trigger and expected result.
11. Glossary and further reading
Glossary

| Term | Meaning |
| --- | --- |
| Boundary | The start, end and included scope of a process |
| Current state | The process as described by present evidence |
| Decision | A condition that selects a process route |
| Elapsed time | Time between defined events, including waiting |
| Exception | A condition requiring a different route from routine processing |
| Fact | A statement supported by the supplied evidence |
| Handoff | Transfer of work or information between participants |
| Open-case age | Time from receipt to a stated cutoff for an unfinished case |
| Problem statement | A concise description of an evidenced issue and its scope |
| Queue | Work ready for an activity but not yet started |
| Rework | Repetition or correction caused by an earlier incomplete or incorrect result |
| Staff effort | Time people actively spend working |
| Unknown | Information not supplied or not established |
Further reading
The references support the concepts identified below. The exercises are product-independent; no product execution or company process verification is claimed.
1. Microsoft Learn — Triggers in Power Automate. Explains the event that starts a flow, including automated, manual and scheduled examples.  
https://learn.microsoft.com/en-us/power-automate/triggers-introduction
2. Object Management Group — About BPMN 2.0.2. Introduces the formal Business Process Model and Notation standard and its implementation-independent purpose. This chapter uses simplified flowcharts rather than teaching the full standard.  
https://www.omg.org/spec/BPMN/2.0.2/About-BPMN
[1]: https://learn.microsoft.com/en-us/power-automate/triggers-introduction
[2]: https://www.omg.org/spec/BPMN/2.0.2/About-BPMN
