---
course_id: "C04"
chapter_id: "C04-CH05"
chapter_number: 5
chapter_title: "Value, Costs and Business Case"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "partially_verified"
---

# Value, Costs and Business Case

1. What you will learn
A proposal can release staff time while increasing cash expenditure. It can also appear attractive because its calculation omits review, support or implementation work.
Your task is to build a business case that explains what the proposed change might deliver, what it would consume and which assumptions still need evidence.
In this chapter, you will learn to:
- Calculate baseline volume, staff effort and additional rework.
- Separate distinct activities so that effort is not counted twice.
- Estimate the effect of coverage, adoption and human review.
- Distinguish released capacity from actual cash savings.
- Include implementation, licences, model usage, support and maintenance.
- Compare plausible options using consistent boundaries.
- Test important assumptions and explain what the numbers mean.
Your required practice is to estimate volume, effort, errors and rework, then separate released capacity from cash savings.
Prerequisites and continuity
Chapter 2 taught you to distinguish staff effort from elapsed time. Chapter 3 showed that opportunities can overlap. Chapter 4 identified readiness dependencies that may affect costs.
Meridian Supply’s existing opportunities remain:

| Opportunity ID | Candidate |
| --- | --- |
| MSP-OPP-001 | Improve required-field completeness and validity |
| MSP-OPP-002 | Reduce effort spent organising varied enquiry wording |
| MSP-OPP-003 | Investigate repeated entry of approved enquiry information |
The established weekly baseline is 120 completed enquiries, 18 initial staff minutes per enquiry, and 24 enquiries requiring six additional rework minutes.
The six preparation minutes are already inside the 18 initial minutes.
MSP-OPP-003 received a 45.00% readiness score for its stated transfer scope. Access, interfaces, licensing and support gaps remain unresolved. A financial calculation does not close those gaps.
Pilot MSP-PILOT-001 remains proposed and unexecuted. No automated performance, savings or returns have been observed.
Your contribution to the course project
You will produce a Value/Cost Model and a Business Case Note for the Business Automation Pilot Proposal.
These artifacts explain:
What changes, how much work might be released, what additional resources are needed, and whether any expenditure can actually be avoided.
The Meridian scenario is synthetic and may be replaced with a permission-cleared company case. All new cost rates in this chapter are explicit teaching assumptions.
2. Lessons
Lesson 1 — Build the baseline from volume and non-overlapping effort
A baseline describes the current process before the proposed change. Its calculation needs a defined period, case population and activity boundary.
Start with:
Baseline staff effort = initial handling effort + additional rework effort
For Meridian:
Initial effort = 120 enquiries/week × 18 minutes/enquiry = 2,160 staff minutes/week
Additional rework = 24 reworked enquiries/week × 6 minutes/reworked enquiry = 144 staff minutes/week
Total = (2,160 + 144) ÷ 60 = 38.4 staff hours/week
The units explain the calculation. Enquiries cancel in the first multiplication, leaving minutes per week.
Count the right thing
The 24 figure counts enquiries requiring rework, not necessarily the number of errors or correction events. One enquiry could contain several errors. If multiple correction events are recorded, use their actual effort or an appropriate event-based model.
For this chapter’s established baseline, the supplied six-minute additional effort applies once to each of the 24 reworked enquiries.
The supplied rework categories are:

| Category | Reworked enquiries/week | Additional minutes per enquiry | Additional effort/week |
| --- | --- | --- | --- |
| Missing quantity or date | 14 | 6 | 84 minutes |
| Copied-code error | 6 | 6 | 36 minutes |
| Outdated-stock check | 4 | 6 | 24 minutes |
| Total | 24 |  | 144 minutes |
These categories partition the supplied 24 cases. Do not add the category total again to the overall rework figure.
The sample rework proportion is:
24 ÷ 120 × 100 = 20% of completed enquiries
That is a completed-case measure. It does not establish the rework rate among unfinished enquiries or incoming demand.
Avoid overlapping activities
Meridian’s preparation component contains organisation, source lookup and rekeying. It is part of initial handling:
18 initial minutes = 6 preparation minutes + 12 other initial minutes
A calculation of 18 + 6 would count preparation twice.
Similarly, an improvement that changes preparation cannot claim all 18 initial minutes as removable work. Availability checking, quotation acceptance and other activities may remain.
Check L1: Why does “24 reworked enquiries” not necessarily mean “24 errors”?
Lesson 2 — Estimate changed effort after coverage and review
A proposed tool rarely affects every case equally.
Coverage is the proportion of cases to which the proposed method is actually applied. It can depend on eligibility, permissions, available sources and user adoption.
For example:
Effective coverage = eligible proportion × adoption among eligible cases
If 80% of cases are eligible and 75% of those use the method:
80% × 75% = 60% effective coverage
Do not apply the proposed saving to all cases when your forecast assumes partial coverage.
For covered cases, include the work that remains:
Net minutes released per covered case = baseline task minutes − assisted task minutes − review/correction minutes
Suppose a six-minute task becomes two minutes of assisted handling plus 1.5 minutes of review:
6 − 2 − 1.5 = 2.5 minutes released per covered case
The forecast is not a four-minute saving. Review consumes part of the apparent reduction.
New rework and recovery
If assisted output needs correction, record that work. You may include it in a clearly defined review/correction allowance or model it separately.
Do not count the same correction in both places.
Also preserve unrelated baseline rework unless there is evidence that the proposal changes it. A drafting assistant does not automatically remove a copied-code error elsewhere in the process.
A useful conservative forecast can hold baseline rework unchanged while testing preparation effort. That makes the claim narrower and easier to evaluate.
Worked demonstration: permission changes coverage
Ten of 12 cases are eligible for assisted preparation. Two use the original manual route because one lacks required information and one lacks permission for the proposed service.
If eligible cases release 2.5 minutes each:
10 × 2.5 = 25 minutes released
Using 12 × 2.5 = 30 minutes would incorrectly include cases that did not use the method.
Check L2: Why should a permission-blocked case remain in the total workload even though it is excluded from assisted coverage?
Lesson 3 — Separate capacity, cash and business outcomes
Released capacity is staff time available for other work. It may help a team handle demand, reduce a queue or improve service.
Cash savings occur when expenditure actually decreases.
Examples of possible cash reductions include:
- Removing paid overtime that would otherwise occur.
- Avoiding an agreed contractor expense.
- Cancelling a redundant subscription.
- Avoiding a planned purchase where the dependency is genuinely removed.
A reduction in task effort does not automatically reduce salary expenditure. If the same employees receive the same pay, the benefit is capacity.
A capacity valuation attaches a planning rate to released hours:
Capacity-equivalent value = released hours × stated hourly planning rate
This helps compare resource use. It is not an invoice credit or a payroll reduction.
Worked demonstration: the same hours, different claims
A proposal releases ten staff hours per month. The planning rate is 30 currency units per staff hour.
10 hours/month × 30 CU/hour = 300 CU/month of capacity-equivalent value
If salaries remain unchanged, cash savings are 0 CU/month.
If Finance separately confirms that six of those hours can replace removable paid overtime at 40 CU/hour:
6 hours/month × 40 CU/hour = 240 CU/month of conditional cash savings
You cannot then claim all ten hours as additional capacity and add the six converted hours as another benefit. The same six hours would be counted twice.
Record:
- Six hours converted into avoided overtime.
- Four hours remaining as released capacity.
The conversion also depends on matching skills, timing and workload. Ten scattered minutes across several people may not remove an overtime shift.
Customer outcomes need their own evidence
Reduced staff effort does not prove faster customer response. Chapter 2 showed that waiting can dominate elapsed time.
Similarly, faster response does not automatically prove additional revenue. A revenue claim needs evidence about demand, conversion and the relationship between the change and sales outcomes.
For Meridian, lost-sales impact remains unknown. Do not add speculative revenue to the business case.
Check L3: What evidence is needed before released time can be described as cash savings?
Lesson 4 — Include the whole cost of the proposed change
Separate one-time and recurring costs.

| Cost category | Typical contents | Important distinction |
| --- | --- | --- |
| Implementation | Configuration, development, mapping, testing and handover | External invoices and internal staff effort affect different budgets |
| Data preparation | Source cleanup, field definitions and document organisation | May be required before the tool can be evaluated |
| Adoption | User practice, instructions and process updates | Staff time still has a resource cost |
| Licences | Users, applications, connectors or environments | Existing licences are not automatically incremental costs |
| Model usage | Input, output, tool calls and other billed usage | Include repeated calls and relevant service charges |
| Human review | Checking, correction and acceptance | Count within process effort or separately, but not twice |
| Support | Monitoring, questions, incidents and fallback work | A successful demonstration does not eliminate support |
| Maintenance | Rule, mapping, source, prompt and template updates | Assign an owner and a realistic allowance |
An incremental cost is an additional cost caused by the proposal. Keep unchanged existing costs in the baseline, but do not present them as new purchases.
Internal staff time has an economic cost even when it causes no additional cash payment. State both views.
Model usage
A token is a unit of text processing used by many language-model services. It is not a fixed number of words.
A simple text-usage estimate is:
Usage cost = input tokens ÷ billing unit × input rate + output tokens ÷ billing unit × output rate
OpenAI’s official pricing documentation distinguishes input and output rates and lists additional tool-related charges.1 Exact rates depend on the chosen model and service configuration.
The worked case uses fictional rates. It assumes no cached-token discounts or separately billed retrieval/storage tools. A real design using those features must add their charges.
For automation platforms, an enquiry is not necessarily a billable task. Zoho Flow’s FAQ states that executions depend on plan task allowances and may also be affected by third-party API limits.2 Identify the platform’s current charging unit before translating business volume into purchased capacity.
Compare options consistently
Use the same:
- Workload and period.
- Process boundary.
- Coverage definition.
- Quality requirements.
- Treatment of review.
- Cash and internal-effort categories.
Then test sensitive assumptions. A small change in review time can matter more than a large percentage change in model cost.
Check L4: Why is “the model call is cheap” insufficient as a business-case argument?
3. Visual explanation — Two benefit views and one cost boundary

| View | Calculation | What it answers |
| --- | --- | --- |
| Process capacity | Baseline effort − changed process effort | How much task effort might be released? |
| Net organisational capacity | Process capacity released − additional support/maintenance hours | How much time remains after operating the change? |
| Cash budget | Avoided expenditure − new cash expenditure | Does the organisation spend less money? |
| Capacity-equivalent comparison | Valued process time released − recurring cash and internal resource costs | Is the resource trade-off attractive under the stated rates? |
These views answer different questions.
If new support work uses a different staff group, its hours may not be interchangeable with Sales hours. Report the gross release and new support requirement separately as well as the aggregate.
The capacity-equivalent comparison subtracts support valued at its own rate. It should not be relabelled as cash profit.
4. Worked case — Meridian’s provisional value/cost model
Explicit new assumptions
This model examines MSP-OPP-002: preparing a source-grounded internal enquiry brief. It does not include automatic quotation issuance, live record writes or availability decisions.
All rates are fictional currency units, CU. They are not vendor prices or accounting requirements.

| Record ID | Input or assumption |
| --- | --- |
| MSP-VAL-001 | Repeats the established weekly baseline |
| MSP-VAL-002 | Assumes a four-week planning period and 80% effective assisted coverage |
| MSP-VAL-003 | Supplies forecast handling, review and operating effort |
| MSP-VAL-004 | Supplies fictional cost rates and implementation allowances |
| MSP-VAL-005 | Supplies a template alternative and sensitivity variants |
The planning period is called a four-week planning month. Twelve such periods contain 48 weeks, not a full 52-week calendar year. Do not reuse these totals as a calendar-year budget without adjusting the period.
Further assumptions:
- The weekly volume repeats for planning; it is not an observed monthly volume.
- Full forecast usage begins in the first operating period.
- Additional baseline rework remains unchanged.
- Salaries remain fixed; no overtime, contractor or subscription saving is identified.
- Internal support and upkeep fit within existing paid hours.
- Taxes, financing and discounting are outside this teaching model.
- Readiness, entitlements and actual performance remain unconfirmed.
Step 1: calculate the planning baseline
Volume = 120 enquiries/week × 4 weeks/period = 480 enquiries/period

| Baseline component | Calculation | Staff hours/period |
| --- | --- | --- |
| Preparation | 480 × 6 minutes ÷ 60 | 48.0 |
| Other initial handling | 480 × 12 minutes ÷ 60 | 96.0 |
| Additional rework | 24 × 4 × 6 minutes ÷ 60 | 9.6 |
| Total | 48.0 + 96.0 + 9.6 | 153.6 |
This also reconciles with:
38.4 hours/week × 4 weeks = 153.6 hours/period
Step 2: calculate forecast changed preparation
Supplied forecasts:
- Effective coverage: 80%.
- Assisted handling: two minutes per covered case.
- Review and correction: 1.5 minutes per covered case.
- Uncovered cases retain six manual preparation minutes.
- Review covers every assisted case.
Covered cases = 480 × 80% = 384 cases/period
Uncovered cases = 480 − 384 = 96 cases/period

| Changed preparation component | Calculation | Staff hours/period |
| --- | --- | --- |
| Assisted handling | 384 × 2 ÷ 60 | 12.8 |
| Review/correction | 384 × 1.5 ÷ 60 | 9.6 |
| Manual preparation for uncovered cases | 96 × 6 ÷ 60 | 9.6 |
| Total preparation |  | 32.0 |
Process capacity released = 48 − 32 = 16 hours/period
Changed process effort:
32 preparation + 96 other initial + 9.6 rework = 137.6 hours/period
Step 3: include support and maintenance
Forecast operating effort:
- Support: two internal hours per period at 40 CU/hour.
- Source/template maintenance: one internal hour per period at 30 CU/hour.
Additional operating effort = 2 + 1 = 3 hours/period
Net aggregate capacity released = 16 − 3 = 13 hours/period
The completed artifact should still show that 16 process hours are released while three operating hours are required. The aggregate does not establish that all hours are interchangeable across roles.
Step 4: calculate model usage
Fictional usage inputs:

| Input | Supplied assumption |
| --- | --- |
| Normal calls | One per covered case |
| Additional calls | 10% of covered cases require one extra call |
| Input per call | 2,000 tokens |
| Output per call | 500 tokens |
| Input rate | 2 CU per 1,000,000 tokens |
| Output rate | 8 CU per 1,000,000 tokens |
| Other tool/storage charges | Zero under this specific model assumption |
Cost per call:
(2,000 ÷ 1,000,000 × 2) + (500 ÷ 1,000,000 × 8)
= 0.004 + 0.004 = 0.008 CU/call
Expected calls:
384 × 1.10 = 422.4 calls/period
The fractional figure is an expected planning value. Actual call counts will be whole numbers.
Usage cost:
422.4 × 0.008 = 3.3792 CU/period, displayed as 3.38 CU.
Step 5: calculate implementation and recurring costs
One-time implementation

| Item | Calculation | Cash cost | Internal effort value |
| --- | --- | --- | --- |
| External setup/configuration | 14 hours × 50 CU/hour | 700 CU | 0 CU |
| External testing/recovery design | 6 hours × 50 CU/hour | 300 CU | 0 CU |
| External handover/documentation | 4 hours × 50 CU/hour | 200 CU | 0 CU |
| Internal source preparation | 8 hours × 30 CU/hour | 0 CU | 240 CU |
| Internal user practice/process updates | 8 hours × 30 CU/hour | 0 CU | 240 CU |
| Total |  | 1,200 CU | 480 CU |
One-time economic resource cost = 1,200 + 480 = 1,680 CU
These are estimating allowances, not supplier quotations.
Recurring costs

| Item | Calculation | Cash cost/period | Internal effort value/period |
| --- | --- | --- | --- |
| Incremental licences | 3 users × 20 CU/user/period | 60.00 CU | 0 CU |
| Model usage | 422.4 calls × 0.008 CU/call | 3.3792 CU | 0 CU |
| Support | 2 hours × 40 CU/hour | 0 CU | 80 CU |
| Maintenance | 1 hour × 30 CU/hour | 0 CU | 30 CU |
| Total |  | 63.3792 CU | 110 CU |
Recurring economic resource cost = 63.3792 + 110 = 173.3792 CU/period
Human review is already included in changed preparation. Its planning value is:
9.6 review hours × 30 CU/hour = 288 CU/period
Do not add that 288 CU again to a benefit calculation that already deducted review time.
Step 6: separate the benefit statements
At 30 CU per released process hour:
Gross capacity-equivalent value = 16 × 30 = 480 CU/period
Recurring capacity-equivalent balance = 480 − 173.3792 = 306.6208 CU/period
For 12 planning periods:
12 × 306.6208 − 1,680 = 1,999.4496 CU
This is a positive resource-equivalent balance under the assumptions, not cash profit.
Cash savings are zero. New cash expenditure is:
1,200 + 12 × 63.3792 = 1,960.5504 CU
Therefore the proposal has a forecast cash increase of 1,960.55 CU over the 12-period horizon.
There is no cash-savings payback in this base case because no avoided expenditure has been identified.
Step 7: compare the template alternative
The supplied template forecast uses the same 480 cases and 80% coverage:
- Three preparation minutes plus one review minute per covered case.
- Six manual minutes for uncovered cases.
- Baseline rework unchanged.
- One support hour at 40 CU and half a maintenance hour at 30 CU per period.
- Eight internal setup hours at 30 CU.
- No incremental licence, model or external implementation charge under this option’s assumptions.
Process release:
384 × (6 − 3 − 1) ÷ 60 = 12.8 hours/period
Net aggregate capacity:
12.8 − 1 − 0.5 = 11.3 hours/period
Recurring equivalent balance:
12.8 × 30 − (40 + 15) = 329 CU/period
Twelve-period balance:
12 × 329 − 8 × 30 = 3,708 CU

| Forecast measure | Template | Generative assistance |
| --- | --- | --- |
| Gross process hours released/period | 12.8 | 16.0 |
| Additional operating hours/period | 1.5 | 3.0 |
| Net aggregate hours released/period | 11.3 | 13.0 |
| New cash cost/period | 0 CU | 63.38 CU |
| One-time economic resource cost | 240 CU | 1,680 CU |
| Twelve-period equivalent balance | 3,708 CU | 1,999.45 CU |
The generative option releases more forecast time but has a lower equivalent balance. This makes the template a credible comparator. Neither forecast establishes actual performance.
Step 8: test sensitivity
Change one assumption at a time; keep the other base inputs unchanged.

| Variant | Gross hours released/period | Recurring equivalent balance/period |
| --- | --- | --- |
| Base: 80% coverage, 1.5-minute review | 16.0 | 306.62 CU |
| Coverage falls to 50% | 10.0 | 127.89 CU |
| Review rises to 2.5 minutes | 9.6 | 114.62 CU |
| Review rises to 4 minutes | 0.0 | −173.38 CU |
For 50% coverage:
Covered cases = 480 × 50% = 240
Usage = 240 × 1.10 × 0.008 = 2.112 CU
Balance = 240 × 2.5 ÷ 60 × 30 − 110 − 60 − 2.112 = 127.888 CU
At four review minutes, assisted handling plus review equals the original six-minute task. Support and cash costs remain, so the proposal consumes additional resources.
The recurring equivalent break-even review time, \(r\), satisfies:
384 × (6 − 2 − r) ÷ 60 × 30 = 173.3792
192 × (4 − r) = 173.3792
r = 4 − 173.3792 ÷ 192 ≈ 3.097 minutes/case
This threshold concerns the recurring resource-equivalent balance. It excludes one-time setup and is not a cash break-even point.
Completed business case note
Artifact: MSP_Business_Case_Note_v0_1.md
Compare the standard template with source-grounded assistance before choosing a solution. The assistance forecast releases 16 process hours per four-week period, requiring three additional operating hours. Its 12-period resource-equivalent balance is 1,999.45 CU, but its cash expenditure increases by 1,960.55 CU. The template has a higher forecast equivalent balance under the supplied assumptions. Revise the estimates using measured coverage, review effort, quality and confirmed costs. Existing readiness gaps remain open.
For the proposed pilot, record preparation, review, correction and fallback effort separately. Preserve its existing boundary and stop criteria. Chapter 8 develops the measurement design.
Mistake and correction
Mistake: “Add 16 hours of capacity value, 288 CU of avoided review and a payroll saving.”
Correction: Review is performed, not avoided. The 16-hour release already deducts review. Fixed payroll does not decrease. The base model supports capacity and expenditure statements only.
5. Try it yourself — Guided practice
Learning goal and access
Build a small baseline and forecast from case-level inputs. Calculate rework, changed effort, model usage and released capacity.
Use paper or a local worksheet. No product account is needed.
The following packet is synthetic and separate from all earlier packets. The proposed timings and calls are supplied simulation inputs, not observed model results.
Complete inputs
For each of 12 completed baseline cases:
- Preparation takes six minutes.
- Other initial handling takes 12 minutes.
- A yes rework flag adds six further minutes.
- That baseline rework remains unchanged in the forecast.
- All staff are salaried; no paid expense is removed.
- Packet-level support/setup costs are not supplied. Do not invent them or call this a complete deployment budget.
For forecast eligible cases, review minutes include all assisted-output corrections. Cases 606 and 610 use an additional draft call; its review effort is already included.
Case 603 needs quantity clarification. Case 605 lacks permission to use the proposed drafting service. Their six-minute manual fallback includes permitted enquiry handling and exception recording; it does not authorise prohibited source access.
enquiry_id,baseline_rework_flag,eligible,assisted_min,review_correction_min,manual_fallback_min,model_calls,scenario
MSP-ENQ-601,no,yes,2,1,0,1,normal
MSP-ENQ-602,yes,yes,2,2,0,1,normal
MSP-ENQ-603,no,no,0,0,6,0,missing_quantity
MSP-ENQ-604,no,yes,2,1,0,1,normal
MSP-ENQ-605,no,no,0,0,6,0,service_permission_denied
MSP-ENQ-606,no,yes,2,2,0,2,additional_draft_after_source_check
MSP-ENQ-607,yes,yes,2,1,0,1,normal
MSP-ENQ-608,no,yes,2,2,0,1,normal
MSP-ENQ-609,no,yes,2,1,0,1,normal
MSP-ENQ-610,yes,yes,2,2,0,2,additional_draft_after_source_check
MSP-ENQ-611,no,yes,2,1,0,1,normal
MSP-ENQ-612,no,yes,2,2,0,1,normal
Each call uses the worked-case fictional allowance: 2,000 input tokens and 500 output tokens, at 2 and 8 CU per million respectively.
Learner worksheet

| Measure | Formula and inputs | Result | Interpretation |
| --- | --- | --- | --- |
| Completed baseline volume |  |  |  |
| Reworked cases and proportion |  |  |  |
| Baseline preparation effort |  |  |  |
| Baseline total effort |  |  |  |
| Forecast preparation effort |  |  |  |
| Forecast total effort |  |  |  |
| Process capacity released |  |  |  |
| Model usage cost |  |  |  |
| Cash savings |  |  |  |
Steps and expected intermediate results
1. Count cases and rework flags.
- Expected result: a reproducible denominator and a separate reworked-case count.
2. Calculate baseline effort.
- Expected result: preparation, other initial work and additional rework shown separately.
3. Sum forecast preparation components.
- Expected result: assisted handling, review/correction and manual fallback all included.
4. Preserve unchanged activities.
- Expected result: other initial effort and baseline rework remain in the forecast.
5. Count calls and price usage.
- Expected result: additional calls included; no call charged to ineligible cases.
6. Write benefit statements.
- Expected result: released minutes reported as capacity; cash savings reported separately; deployment costs identified as incomplete.
Your final artifact is C04_CH05_Value_Cost_Model_Practice.md.
In a group, Finance can check units, Sales can check review/fallback effort, Operations can check unchanged work and IT can check cost dependencies. Individually, perform those checks in the same order.
Retain the final synthetic worksheet. No system cleanup is required.
6. Independent challenge
Use this changed planning scenario for MSP-OPP-002. It does not overwrite the main case.
Supplied changes and retained inputs
- Volume remains 480 cases per four-week period.
- Effective coverage remains 80%.
- Assisted handling remains two minutes.
- Review/correction rises to 2.5 minutes per covered case.
- Support remains two hours and maintenance one hour per period.
- Licence cost remains 60 CU per period.
- Usage remains one call plus a 10% extra-call allowance, at 0.008 CU per call.
- External setup remains 1,200 CU.
- Internal setup remains 16 hours, performed within existing paid hours.
- Finance confirms the exercise condition: if the forecast net capacity is attained and matches the work schedule, up to six paid overtime hours per period can be removed at 40 CU/hour.
- Those overtime hours are part of the existing workload, not extra volume.
- No other expense is removed.
Deliverables
1. Calculate gross and net capacity released.
2. Calculate conditional avoided overtime expenditure.
3. Calculate recurring net cash benefit and the 12-period cash balance after external setup.
4. Identify capacity remaining after overtime conversion.
5. State what must be measured before the forecast becomes an actual cash-saving claim.
Success criteria
Include review, support and maintenance. Respect the six-hour conversion limit. Count converted hours once. Keep internal setup effort visible even though it creates no additional cash payment.
7. Common problems and recovery

| Symptom | Diagnosis | Correction | Verification |
| --- | --- | --- | --- |
| Claimed saving exceeds baseline task time | Scope or overlap error | Map each saving to a distinct baseline activity | Claimed removable minutes do not exceed that activity |
| Review appears both in changed effort and as another deducted cost | Double counting | Choose one consistent treatment | Review is counted once |
| All cases receive the assisted saving | Coverage ignored | Separate covered and fallback cases | Counts reconcile to total volume |
| Rework disappears without evidence | Optimistic assumption | Hold it unchanged or supply a supported reduction | Every reduction has a stated basis |
| Salaried time becomes payroll savings | Capacity confused with expenditure | Identify a removable expense | Finance can name the budget line and conversion mechanism |
| A missing price is entered as zero | Unknown treated as free | Mark the dependency unresolved | Zero appears only where the scenario supports no incremental charge |
| Usage excludes additional calls | Recovery consumption omitted | Count all forecast or recorded calls | Call total reconciles to the case packet |
| Four-week totals are called a calendar-year budget | Period mismatch | State weeks and adjust the horizon | Annual volume matches the chosen calendar basis |
When costs are incomplete, keep the model provisional. The specific recovery is to obtain the missing entitlement, implementation or operating estimate.
8. Check your understanding
1. Why is Meridian’s weekly total 38.4 hours rather than 48 hours?
2. Why must review effort be included even if the output usually looks correct?
3. What is the cash-saving claim in the main worked case?
4. Why can the template have a better equivalent balance while releasing fewer hours?
5. Which guided-practice cases are excluded from model usage, and why?
6. What would you need before adding a revenue benefit for faster quotations?
9. Solutions and explanations
Lesson checks
L1: A reworked enquiry may contain several errors or correction events. The supplied baseline counts affected enquiries and assigns six additional minutes to each.
L2: The case still consumes permitted manual handling and exception effort. Excluding it from assisted coverage must not remove it from workload.
L3: Identify an expense that can be removed, confirm the hours match the work and schedule, and obtain Finance’s agreement about the budget effect. Actual savings require observed reductions.
L4: Model charges are only one component. Implementation, licences, review, data upkeep and support may dominate total cost.
Guided practice — Completed worksheet

| Measure | Formula and inputs | Result | Interpretation |
| --- | --- | --- | --- |
| Completed baseline volume | Count all records | 12 cases | Separate sample |
| Reworked cases | Cases 602, 607 and 610 | 3 cases | Count from supplied flags |
| Rework proportion | 3 ÷ 12 × 100 | 25% | Sample proportion, not the weekly 20% rate |
| Baseline preparation | 12 × 6 | 72 minutes | Inside initial handling |
| Other initial effort | 12 × 12 | 144 minutes | Unchanged |
| Additional rework | 3 × 6 | 18 minutes | Additional and unchanged |
| Baseline total | 72 + 144 + 18 | 234 minutes | 3.9 staff hours |
| Assisted handling | 10 × 2 | 20 minutes | Ten eligible cases |
| Review/correction | Five × 1 + five × 2 | 15 minutes | Includes assisted corrections |
| Manual fallback | 2 × 6 | 12 minutes | Cases 603 and 605 |
| Forecast preparation | 20 + 15 + 12 | 47 minutes | Includes all preparation routes |
| Forecast total | 47 + 144 + 18 | 209 minutes | Approximately 3.483 staff hours |
| Process capacity released | 234 − 209 | 25 minutes | Approximately 0.417 staff hours |
| Model usage | 12 calls × 0.008 | 0.096 CU | Display as 0.10 CU |
| Cash savings | No removable expense supplied | 0 CU | Capacity is not payroll saving |
Call reconciliation:
10 first calls + 2 additional calls = 12 calls
Token reconciliation:
12 × 2,000 = 24,000 input tokens
12 × 500 = 6,000 output tokens
Cost:
24,000 ÷ 1,000,000 × 2 + 6,000 ÷ 1,000,000 × 8
= 0.048 + 0.048 = 0.096 CU
An acceptable conclusion is:
The supplied forecast releases 25 process minutes across 12 cases and adds 0.096 CU of model usage. No cash saving is established. Setup, licensing and packet-level support costs are incomplete, so this is a task-effort comparison rather than a full deployment business case.
Do not extrapolate the packet’s 25% rework proportion to the established weekly baseline. They are different samples.
Independent challenge — Explained solution
Covered cases:
480 × 80% = 384
Release per covered case:
6 − 2 − 2.5 = 1.5 minutes
Gross process release:
384 × 1.5 ÷ 60 = 9.6 hours/period
Net aggregate release:
9.6 − 2 − 1 = 6.6 hours/period
Under the supplied work-matching condition, convertible overtime is:
Minimum of 6.6 released hours and 6 removable overtime hours = 6 hours
Conditional avoided expenditure:
6 × 40 = 240 CU/period
Recurring new cash cost remains:
60 + 384 × 1.10 × 0.008 = 63.3792 CU/period
Recurring net cash benefit:
240 − 63.3792 = 176.6208 CU/period
Twelve-period balance after external setup:
12 × 176.6208 − 1,200 = 919.4496 CU, displayed as 919.45 CU.
Remaining capacity:
6.6 − 6 = 0.6 hours/period
Do not add the converted six hours again as additional capacity value.
The 16 internal setup hours remain a resource requirement. They create no new cash payment under the supplied exercise conditions, so they are not included in this cash balance.
Before claiming actual cash savings, measure:
- Covered case volume and achieved effort, including correction.
- Operating support and maintenance effort.
- Whether released time matches the overtime work.
- Actual overtime hours and payments removed.
- Actual licences, usage and implementation payments.
Existing readiness gaps still require resolution before live use.
Understanding questions
1. Correct effort is 120 × 18 + 24 × 6 = 2,304 minutes, or 38.4 hours. Adding the six preparation minutes to the 18 initial minutes would count them twice.
2. Review is real work and is necessary for acceptance. Omitting it overstates release and can conceal correction effort.
3. Zero cash savings. The forecast adds 1,960.55 CU of cash expenditure over 12 four-week periods.
4. Its lower setup and operating requirements can outweigh its smaller time reduction. Benefits and costs must be compared together.
5. Cases 603 and 605: missing quantity and denied drafting-service permission. Their manual fallback remains in total effort.
6. You need response-time evidence, customer/order outcomes and a justified relationship between faster quotations and additional business. Staff-effort reductions alone are insufficient.
10. Chapter recap and next step
A useful business case reconciles baseline work, changed work and operating requirements. It makes clear which figures are evidence, forecasts or unresolved inputs.
The strongest benefit statement may be released capacity rather than cash savings. That can still matter, provided you explain what the team will do with the time and how the result will be measured.
“I can…” checklist
- I can calculate volume, effort and additional rework with units.
- I can avoid overlapping activity counts.
- I can apply coverage and include review/fallback effort.
- I can distinguish capacity value from avoided expenditure.
- I can include one-time and recurring costs.
- I can price supplied usage inputs without inventing vendor rates.
- I can compare options and test sensitive assumptions.
- I can explain a provisional business case without claiming observed returns.
Your project artifacts are:
- MSP_Value_Cost_Model_v0_1.md
- MSP_Business_Case_Note_v0_1.md
- MSP_Case_Assumptions_v0_5.md
Retain assumptions MSP-A-001 through MSP-A-014 and add:

| Assumption ID | New assumption | Status |
| --- | --- | --- |
| MSP-A-015 | Weekly workload repeats across four-week planning periods | Planning assumption |
| MSP-A-016 | Assistance reaches 80% coverage with two-minute handling and 1.5-minute review | Untested forecast |
| MSP-A-017 | Supplied fictional implementation, licence and usage rates approximate future resource needs | Replace with confirmed estimates |
| MSP-A-018 | Full usage begins immediately and baseline rework stays unchanged | Modelling assumption |
| MSP-A-019 | Main-case salaries remain fixed and no avoidable expenditure is identified | Base-case condition; overtime challenge is separate |
| MSP-A-020 | Support takes two hours and maintenance one hour per period | Untested operating allowance |
Chapter 6, Prioritisation and Solution Selection, compares plausible options against value, feasibility, complexity, data readiness, failure consequences, reversibility and ownership.
11. Glossary and further reading
Glossary

| Term | Meaning |
| --- | --- |
| Capacity-equivalent value | Planning value assigned to staff time, without implying expenditure reduction |
| Cash saving | An actual decrease in expenditure |
| Coverage | Proportion of cases actually handled by the proposed method |
| Incremental cost | Additional cost caused by a change |
| Maintenance | Work to keep rules, mappings, sources or assistance current |
| Net capacity | Released process effort after additional operating effort |
| Recurring cost | Cost repeated during operation |
| Released capacity | Staff time made available for other work |
| Sensitivity analysis | Testing how results change when assumptions change |
| Token | A text-processing unit used by many model services |
| Usage cost | Charge associated with measured service consumption |
Further reading
Official sources were accessed for charging concepts. The worked rates are fictional, and no product usage was executed. Actual pricing depends on the chosen product, model, plan, edition, region, service configuration and contract.
1. OpenAI — API pricing. Distinguishes input/output token rates and additional tool-related charges. Use the applicable configuration when replacing the fictional rates.  
https://developers.openai.com/api/docs/pricing
2. Zoho Flow — FAQ. Explains plan task allowances and notes that third-party API limits can affect execution. Use current product help to establish the charging unit for the proposed workflow.  
https://www.zoho.com/flow/help/faq.html
[1]: https://developers.openai.com/api/docs/pricing
[2]: https://www.zoho.com/flow/help/faq.html
