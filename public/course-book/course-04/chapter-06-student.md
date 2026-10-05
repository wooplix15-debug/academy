# Prioritisation and Solution Selection

## 1. What you will learn

The opportunity with the largest forecast benefit is not always the best next step. It may depend on unavailable data, unclear ownership or an expensive change that is difficult to reverse.

Likewise, the most capable technology is not necessarily the best solution. A native validation feature may handle a fixed rule more clearly than an AI assistant. An integration platform may handle cross-app work more economically than custom development. A simple template may outperform generative assistance after review and operating costs are included.

In this chapter, you will learn to:

- Distinguish opportunity prioritisation from solution selection.
- Compare native product features, Zoho Flow, custom development and AI options.
- Evaluate value, feasibility, complexity, data readiness, failure consequences, reversibility and ownership.
- Apply essential requirements before ranking options.
- Calculate a weighted comparison and test its sensitivity.
- Explain a conditional recommendation and its unresolved dependencies.

Your required practice is to compare native features, Flow, custom development and AI against value, feasibility and risk.

Prerequisites and continuity

Chapter 3 produced Meridian Supply’s use-case cards. Chapter 4 assessed readiness. Chapter 5 calculated provisional value and costs.

The existing candidates remain:

| Opportunity ID | Candidate |
| --- | --- |
| MSP-OPP-001 | Improve required-field completeness and validity |
| MSP-OPP-002 | Reduce effort spent organising varied enquiry wording |
| MSP-OPP-003 | Investigate repeated entry of approved enquiry information |

The established weekly baseline remains 120 completed enquiries, 18 initial staff minutes per enquiry, and 24 enquiries requiring six additional rework minutes.

Important previous findings remain open:

- The transfer scope under MSP-OPP-003 has a 45.00% readiness score, with unresolved access, interface, licensing and support dependencies.
- The Chapter 5 template and generative-assistance figures are forecasts, not observed results.
- No cash saving is established in the main case.
- Pilot MSP-PILOT-001 remains proposed and unexecuted.

This chapter adds synthetic comparison assumptions. It does not silently confirm product capabilities or resolve earlier dependencies.

### Your contribution to the course project

You will produce an Option Comparison, a Prioritisation Rationale and a Solution Recommendation.

These artifacts explain why one opportunity deserves the next investigation and why a particular mechanism is worth testing. They form part of your Business Automation Pilot Proposal.

The workshop supports assessment and proposal writing. It does not establish production implementation competence or guaranteed returns.

## 2. Lessons
### Lesson 1 — Prioritise an opportunity before selecting its mechanism

Prioritisation decides which opportunity should receive attention next.

Solution selection decides how to address a defined opportunity.

These are different decisions. “Use Flow first” names a mechanism. It does not explain which business problem should be addressed.

A useful sequence is:

1. Define the problem and expected result.
2. Check whether the process can be simplified.
3. Identify essential requirements.
4. Compare plausible mechanisms.
5. Record dependencies and choose the next bounded step.

Worked example: three different next steps

Meridian’s weekly correction log contains:

- 14 missing-quantity/date cases.
- Six copied-code errors.
- Four outdated-stock checks.

The missing-information category represents:

14 cases/week × 6 additional minutes/case = 84 staff minutes/week

That is evidence of correction effort associated with missing information. It is not proof that validation would remove all 84 minutes. Some clarification work may move earlier rather than disappear.

This evidence makes MSP-OPP-001 a useful candidate for a narrow rules investigation.

For MSP-OPP-002, Chapter 5 gives a different reason to investigate: compare the template and generative options because their costs and review requirements differ.

For MSP-OPP-003, the next useful step is to resolve the shared-record question and technical dependencies before estimating a reliable live-transfer result.

A prioritisation rationale can therefore be qualitative and evidence-based. You do not need to invent a numerical ranking across opportunities whose costs and benefits are not yet comparable.

Avoid the “easy means valuable” mistake

An easy change can be worthwhile, but ease alone does not establish value. Conversely, a high-value issue may justify difficult work.

The question is:

Is the next investment of effort justified by the problem evidence, likely benefit, dependencies and consequences?

Check L1: Why is “the tool is already available” insufficient as an opportunity-prioritisation argument?

### Lesson 2 — Compare four solution families against the same task

A native feature is a capability already provided within the application where the work occurs. Examples can include required fields, validation, workflow rules, templates and approvals.

An integration platform connects applications using configured triggers and actions. Zoho Flow is one example.

Custom development creates software or extensions for requirements that are not adequately met by existing features.

An AI option uses a model for tasks such as interpreting varied language, drafting, retrieval or model-directed investigation. AI may be one component of a larger workflow.

These families can overlap. A custom service can use an AI model. Flow can connect to services used by a broader solution. Label the main mechanism and identify supporting components.

Native product features

Native features are often a strong starting point when the task occurs inside one application and the required rule is explicit.

For example:

Quantity must be present and be a positive whole number.

A native feature can be useful if it evaluates the relevant entry routes and produces a clear exception.

However, “the application has business rules” does not establish that the exact rule works for every form, import or API write. Microsoft’s Dataverse documentation lists validation and error-message actions, while also describing scope and app-type differences.1 This illustrates a native capability; it does not establish that Meridian uses Dataverse or has those features.

Zoho Flow

Flow is relevant when the task spans applications. Its official FAQ describes workflows in which an event triggers actions in other apps.2

For Meridian’s repeated-entry opportunity, a proposed integration could:

1. Receive a checked enquiry event.
2. Look up the business reference.
3. Create a matching request if none exists.
4. Record the destination-generated identifier.
5. Route mismatches or uncertain results to an owner.

Whether the specific trigger, lookup and create actions are supported remains an application-specific question.

Flow does not automatically make source data correct. It also introduces connection, mapping, usage and support dependencies.

Custom development

Custom development can provide tailored validation, interfaces, logging and recovery behaviour.

It may be justified when:

- Required entry routes cannot be controlled through native features.
- Existing connectors cannot meet a required interface.
- Recovery or transaction requirements are unusually demanding.
- A reusable service has a credible wider purpose.

The additional flexibility comes with development, testing, deployment and maintenance work. A custom solution still needs business ownership and permissions.

AI options

AI is useful when variation in language or investigation is part of the problem.

For a fixed quantity rule, generative judgement adds little. A model could help extract a quantity from a message, but an explicit rule should still validate the extracted value.

An agent is relevant when the model must choose steps or tools in response to results. A predefined sequence of lookups does not become an agent merely because it is long. Official architectural guidance distinguishes predefined workflows from agents that dynamically direct their process and tool use.3

Check L2: Which family is a plausible starting point for a fixed rule inside one application? Which becomes more relevant when checked data must move between applications?

### Lesson 3 — Apply essential requirements before weighted scoring

An essential requirement is a condition an option must satisfy to perform the stated task.

An evaluation criterion helps compare options that may satisfy the task.

Keep them separate. A high score for simplicity cannot compensate for an option that cannot produce the required output.

For example:

Required result: create a linked Operations request without rekeying.

A native CSV export may be useful, but it does not satisfy that result by itself. It should be recorded as an incomplete alternative rather than given a high overall score for an automatic transfer.

Use explicit gates

A gate is a requirement that must be resolved before a stated decision.

Useful gates include:

| Gate | Question |
| --- | --- |
| Task fit | Can the option produce the required output across the included entry routes? |
| Permitted use | Are the required data use and actions authorised? |
| Ownership | Is someone accountable for the result and exception handling? |
| Operating boundary | Can the proposed actions be limited and stopped? |
| Entitlement and resources | Are the required licences, capacity and support available for the next step? |

Use three statuses:

- Meets: supported for the stated decision.
- Fails: supplied evidence shows that it does not meet the requirement.
- Unknown: further evidence is required.

An unknown does not mean impossible. It also does not mean ready.

You may compare designs provisionally while gates remain unknown. State that the comparison supports investigation, not live use.

Worked example: denied write permission

An integration can read an enquiry and search the destination. It cannot create a request because write permission is absent.

The correct conclusion is:

The design may fit the task, but the current permission gate prevents the create action.

Do not raise its score because the data is easy to retrieve.

Check L3: What should happen when the highest-scoring option fails an essential output requirement?

### Lesson 4 — Evaluate seven criteria without hiding uncertainty

The following criteria address different questions:

| Criterion | Business question |
| --- | --- |
| Value | Does the option address an evidenced issue, and are its benefits and costs credible? |
| Feasibility | Can it be delivered within the actual systems, skills, permissions and resources? |
| Complexity | How many components, interfaces and operating dependencies does it introduce? |
| Data readiness | Are the required sources sufficiently defined, authoritative, accessible and complete? |
| Failure consequences and containment | What could go wrong, who would be affected, and can incorrect results be detected before impact? |
| Reversibility | Can the organisation stop the change and recover without leaving harmful or confusing effects? |
| Ownership | Are result acceptance, support and maintenance responsibilities clear? |

For complexity, the score must be directional: a higher score means lower or better-controlled complexity.

Failure consequences are not the same as failure probability. Even an infrequent error can matter if it creates a customer commitment or changes a financial record.

Reversibility is also more than turning off a workflow. Stopping new writes does not remove records already created. Zoho Flow’s FAQ states that deleting a flow stops future updates while previously updated data in other apps remains.2 For any write-based option, consider reconciliation as well as stopping.

Keep scores interpretable

This chapter uses a 0–3 comparison scale:

| Score | Meaning |
| --- | --- |
| 0 | No support, a major mismatch or insufficient information to assess |
| 1 | Weak fit or material unresolved dependency |
| 2 | Plausible fit with defined work still required |
| 3 | Strong fit supported by the supplied design or evidence |

A score of 3 is not proof of production readiness. A design may be strong while its implementation remains untested.

A weighted result is:

Weighted points = criterion score ÷ 3 × criterion weight

If value has weight 20 and an option scores 2:

2 ÷ 3 × 20 = 13.33 points

The total is a comparison index. It is not a percentage probability of success.

Check L4: Why should a score of 80 out of 100 not be described as an 80% chance of successful implementation?

### Lesson 5 — Use sensitivity to improve the recommendation

Sensitivity analysis asks whether the recommendation changes when reasonable assumptions or priorities change.

Test:

- A different weighting of failure consequences.
- A lower feasibility score when a capability is unconfirmed.
- A higher review burden.
- Reduced data coverage.
- Unresolved ownership.
- Higher implementation or operating cost.

A stable ranking can increase confidence in the direction of the recommendation. It does not repair poor evidence.

A changing ranking is useful information. It identifies the decision-driving criterion.

For example:

Native validation ranks first under the base priorities, but a custom validator ranks first when failure containment receives much greater weight. Verify entry-route coverage and containment before choosing.

This is more informative than hiding the alternate result.

Check L5: If two options are close and their order changes under reasonable weights, what should the recommendation explain?

## 3. Visual explanation — Gates, comparison and the next decision

flowchart TD
    A[Defined opportunity and required output] --> B[Consider process simplification]
    B --> C[Identify plausible solution options]
    C --> D{Essential task requirement met?}
    D -->|Fails| E[Exclude or redesign the incomplete option]
    D -->|Unknown| F[Record assumption and seek evidence]
    D -->|Meets or conditionally plausible| G[Compare value, feasibility and risk]
    F --> G
    G --> H[Test sensitivity and critical dependencies]
    H --> I[Recommend proceed, revise or defer for a defined next step]
The diagram explains why scoring follows task definition.

An option with an unknown capability can receive a provisional design comparison, but it retains the unknown gate. An option known to fail the required output must be excluded or redesigned.

The final decision names the next step. Proceeding with an offline comparison, technical verification or pilot design is different from proceeding with live implementation.

## 4. Worked case — Select the next mechanism to investigate

Scope and new synthetic inputs

This comparison concerns MSP-OPP-001:

When an enquiry is recorded, check product recognition, positive whole-number quantity and the presence of a requested date. Produce a checked-intake status or a specific exception. Do not decide availability or send a quotation.

The proposed check must ultimately cover form entry and imported records. Whether native features cover both is unconfirmed.

The following new records contain paper design assessments, not product tests:

| Record ID | Supplied content |
| --- | --- |
| MSP-SEL-001 | Validation requirements and eight-case packet |
| MSP-SEL-002 | Four candidate designs and assessment judgements |
| MSP-SEL-003 | Base weights and scoring assumptions |
| MSP-SEL-004 | Failure-focused sensitivity weights |

Meridian’s actual application, edition and native capabilities remain unspecified.

Complete case packet

For these independent cases, the only recognised catalogue code is BF-10. Requested dates shown are valid dates. No default quantity or automatic product correction is authorised.

| Enquiry ID | Product | Quantity | Requested date | Source use permitted? |
| --- | --- | --- | --- | --- |
| MSP-ENQ-701 | BF-10 | 25 | 2026-10-20 | Yes |
| MSP-ENQ-702 | BF-10 | Missing | 2026-10-20 | Yes |
| MSP-ENQ-703 | BF-10 | 0 | 2026-10-20 | Yes |
| MSP-ENQ-704 | BF-10 | 2.5 | 2026-10-20 | Yes |
| MSP-ENQ-705 | XX-99 | 8 | 2026-10-20 | Yes |
| MSP-ENQ-706 | BF-10 | 10 | Missing | Yes |
| MSP-ENQ-707 | BF-10 | 4 | 2026-10-20 | No |
| MSP-ENQ-708 | BF-10 | 60 | 2026-10-20 | Yes |

Case 708 is a valid intake request. The separate supplied stock snapshot lists 40 units, so Operations still needs to investigate availability. Intake validity is not availability approval.

### Step 1: compare the proposed designs

The option IDs below are business comparison identifiers, not product-generated IDs.

| Option ID | Family | Proposed design | Important dependency |
| --- | --- | --- | --- |
| MSP-OPT-001 | Native feature | Validate fields inside the existing intake application | Exact rules and import-route coverage are unconfirmed |
| MSP-OPT-002 | Zoho Flow | Run checks after an intake event and return an exception/status | Required trigger, actions, permissions and latency need assessment |
| MSP-OPT-003 | Custom development | Central validator designed to reject unusable input and record a trace before handoff | Build, integration, hosting and maintenance ownership remain open |
| MSP-OPT-004 | AI-assisted | Model identifies candidate issues, followed by explicit validation and Sales review | Adds model access, review and operating dependencies without a demonstrated language need |

All four are proposed designs. No capability has been executed.

The custom design’s trace and reject-before-handoff behaviour justify a stronger proposed containment assessment. They remain features to verify, not observed results.

### Step 2: record the gate status

| Requirement | Current status | Consequence |
| --- | --- | --- |
| Exact validation across form and imports | Unknown for native; proposed for other designs | Verification required |
| Authorised access and configuration changes | Unknown | No live change authorised by this comparison |
| Confirmed entitlement and operating resources | Unknown | Cost and licence check required |
| Business result owner | Sales Lead identified | Ownership partly established |
| Availability/customer-commitment boundary | Defined | All options must preserve it |
| Technical support and maintenance owner | Not assigned | Operating dependency remains |

The score supports choosing the next investigation. It does not authorise implementation.

### Step 3: apply the base weights

| Criterion | Weight |
| --- | --- |
| Value | 20 |
| Feasibility | 20 |
| Controlled complexity | 15 |
| Data readiness | 15 |
| Failure consequences and containment | 15 |
| Reversibility | 5 |
| Ownership | 10 |
| Total | 100 |

The supplied provisional scores are:

| Criterion | Native | Flow | Custom | AI-assisted |
| --- | --- | --- | --- | --- |
| Value | 2 | 2 | 2 | 1 |
| Feasibility | 2 | 1 | 2 | 1 |
| Controlled complexity | 3 | 2 | 1 | 1 |
| Data readiness | 2 | 2 | 2 | 1 |
| Failure consequences and containment | 2 | 2 | 3 | 1 |
| Reversibility | 3 | 2 | 2 | 2 |
| Ownership | 2 | 1 | 1 | 1 |

Why these scores?

- Value remains provisional: the issue recurs, but exact costs and realised reductions are untested.
- Native validation has fewer proposed components, but entry-route coverage is unresolved.
- Flow introduces connection and event dependencies for a task that begins inside one application.
- Custom development introduces more build and maintenance work, with a stronger specified containment design.
- AI-assisted validation adds dependencies without an evidenced need to interpret varied language in this scope.
- The shared source evidence is partial; a different technology does not make it complete.
- Technical maintenance ownership is unresolved, particularly for the additional services.

### Step 4: calculate the weighted result

| Criterion | Native points | Flow points | Custom points | AI-assisted points |
| --- | --- | --- | --- | --- |
| Value | 13.33 | 13.33 | 13.33 | 6.67 |
| Feasibility | 13.33 | 6.67 | 13.33 | 6.67 |
| Controlled complexity | 15.00 | 10.00 | 5.00 | 5.00 |
| Data readiness | 10.00 | 10.00 | 10.00 | 5.00 |
| Failure consequences and containment | 10.00 | 10.00 | 15.00 | 5.00 |
| Reversibility | 5.00 | 3.33 | 3.33 | 3.33 |
| Ownership | 6.67 | 3.33 | 3.33 | 3.33 |
| Total, using unrounded values | 73.33 | 56.67 | 63.33 | 35.00 |

For native validation:

(2×20 + 2×20 + 3×15 + 2×15 + 2×15 + 3×5 + 2×10) ÷ 3

= 220 ÷ 3 = 73.33 points

Use unrounded values for totals. Display rounding can make the visible cells differ slightly from the total.

### Step 5: test failure-focused priorities

Use these alternate weights, leaving scores unchanged:

| Criterion | Base weight | Failure-focused weight |
| --- | --- | --- |
| Value | 20 | 10 |
| Feasibility | 20 | 20 |
| Controlled complexity | 15 | 5 |
| Data readiness | 15 | 15 |
| Failure consequences and containment | 15 | 35 |
| Reversibility | 5 | 5 |
| Ownership | 10 | 10 |
| Total | 100 | 100 |
| Option | Base total | Failure-focused total |
| Native | 73.33 | 70.00 |
| Flow | 56.67 | 56.67 |
| Custom | 63.33 | 73.33 |
| AI-assisted | 35.00 | 35.00 |

Custom development now ranks first because its proposed containment score receives more weight.

This does not establish that custom development is necessary. It identifies a deciding question:

Can native validation cover every included entry route with suitable exception visibility, or does the process require a central validator?

A second sensitivity test lowers native feasibility from 2 to 0:

73.33 − (2 ÷ 3 × 20) = 60.00 points

More importantly, a confirmed inability to cover a required route would fail task fit. The team must redesign or exclude that option rather than rely on its remaining score.

### Step 6: connect selection to the existing business case

For MSP-OPP-002, Chapter 5 supplied these forecasts:

| Twelve four-week planning periods | Template | Generative assistance |
| --- | --- | --- |
| Capacity-equivalent balance | 3,708 CU | 1,999.45 CU |
| Incremental cash expenditure | 0 CU | 1,960.55 CU |
| Net aggregate capacity per period | 11.3 hours | 13.0 hours |

The template releases less forecast capacity but has a stronger equivalent balance under those assumptions.

Those figures belong to brief preparation. Do not reuse them as the value of MSP-OPP-001 validation or MSP-OPP-003 transfer.

For the validation comparison, estimates still need to include:

| Family | Cost evidence to obtain |
| --- | --- |
| Native | Configuration, entry-route testing, entitlement and rule maintenance |
| Flow | Mapping, connectors, usage allowance, monitoring and exception support |
| Custom | Development, testing, hosting, deployment, recovery and maintenance |
| AI-assisted | Model/service access, usage, explicit validation, review, source upkeep and support |

### Step 7: record the recommendation

Completed artifact: MSP_Solution_Recommendation_v0_1.md

Recommendation: investigate native validation first for MSP-OPP-001, conditionally.

It ranks highest under the base priorities and introduces fewer proposed components. Verify the exact checks, form/import coverage, permissions, entitlement and support ownership. If native coverage is inadequate, reassess the custom validator and integration designs. Failure-focused weighting changes the leading option, so containment must be checked explicitly. Continue the template comparison for MSP-OPP-002 and resolve the shared-record question for MSP-OPP-003. No live implementation or pilot result is established.

Completed reference outcomes

| Case | Correct outcome |
| --- | --- |
| 701 | Intake valid; continue the human-owned process |
| 702 | Clarify missing quantity |
| 703 | Clarify invalid zero quantity |
| 704 | Clarify non-whole-number quantity |
| 705 | Verify unknown product code |
| 706 | Clarify missing requested date |
| 707 | Stop affected source use; refer access exception |
| 708 | Intake valid; Operations handles the separate availability issue |

These are reference outcomes, not test observations.

Mistake and correction

Mistake: “Native scored 73.33, so it is approved and will remove the weekly rework.”

Correction: The score compares provisional designs. Capabilities and costs remain unconfirmed, and clarification may move earlier rather than disappear. The recommendation is to verify a bounded candidate.

## 5. Try it yourself — Guided practice

Learning goal and access

Compare four mechanisms for a cross-app handoff.

Use the supplied paper packet. No product access is required. This practice cannot demonstrate live connectors, permissions or reliability.

The exercise is separate from the main readiness assessment.

Required output

When a checked enquiry is ready, make one linked Operations request available without rekeying.

Preserve business reference, product, quantity and requested date. Do not send a quotation or decide availability.

Option packet

| Exercise option | Supplied proposed capability | Assessment condition |
| --- | --- | --- |
| EX-OPT-NATIVE | Existing application exports a CSV; it cannot create the Operations request by itself | Incomplete for the required output |
| EX-OPT-FLOW | Proposed lookup/create workflow using business reference and an exception route | Paper design; exact connector and permissions unverified |
| EX-OPT-CUSTOM | Proposed service with explicit validation, record trace and reconciliation | Paper design; development and maintenance dependencies remain |
| EX-OPT-AI | Proposed model-assisted transfer followed by explicit checks | No language interpretation need is supplied; additional dependencies remain |

For provisionally task-fitting designs, use these supplied scores and the worked case’s base weights:

| Criterion | Flow | Custom | AI |
| --- | --- | --- | --- |
| Value | 2 | 2 | 1 |
| Feasibility | 2 | 2 | 1 |
| Controlled complexity | 2 | 1 | 1 |
| Data readiness | 2 | 2 | 1 |
| Failure consequences and containment | 2 | 3 | 1 |
| Reversibility | 2 | 2 | 2 |
| Ownership | 2 | 1 | 1 |

These are exercise judgements, not measurements.

Complete exception packet

| Enquiry | Supplied condition | Permitted recovery |
| --- | --- | --- |
| MSP-ENQ-751 | BF-10, 20 units, requested date 2026-10-21; checked; create permission available; no destination match | Create one linked request in the hypothetical design |
| MSP-ENQ-752 | BF-10, quantity missing, requested date 2026-10-21 | Clarify quantity; no normal create |
| MSP-ENQ-753 | BF-10, 4 units, requested date 2026-10-21; checked; destination read permitted but create denied | Hold create and refer permission issue |
| MSP-ENQ-754 | BF-10, 10 units, requested date 2026-10-21; acknowledgement lost; authorised lookup finds REQ-7402 linked to this business enquiry with all fields matching | Reconcile the matching record; do not create another |

REQ-7402 is an illustrative destination-generated ID, not an opportunity or enquiry ID.

Learner worksheets

| Option | Task-fit status | Score or reason not scored | Main dependency | Recommended next step |
| --- | --- | --- | --- | --- |
| Native |  |  |  |  |
| Flow |  |  |  |  |
| Custom |  |  |  |  |
| AI |  |  |  |  |

| Case | Permitted action | What must not happen |
| --- | --- | --- |
| 751 |  |  |
| 752 |  |  |
| 753 |  |  |
| 754 |  |  |

Guided steps and expected intermediate results

1. Apply the task-fit requirement.
- Expected result: distinguish a complete proposed transfer from an export-only alternative.
2. Calculate base totals.
- Expected result: three reproducible weighted scores.
3. Apply failure-focused weights.
- Expected result: show whether the leading design changes.
4. Resolve the four cases.
- Expected result: normal creation, clarification, permission hold and reconciliation handled separately.
5. Write a recommendation.
- Expected result: identify the leading base option, sensitivity and evidence required before live use.

Your final artifact is C04_CH06_Option_Comparison_Practice.md.

In a group, use Sponsor, Sales, Operations, Finance and IT perspectives. Individually, explain what each role needs from the recommendation.

No system cleanup is required.

## 6. Independent challenge

Use this changed version of the worked validation scope. It does not overwrite the main case.

New facts

- Both form entry and bulk import must be validated before Operations handoff.
- The supplied capability assessment now confirms that the native option checks forms only and cannot evaluate imported records.
- The Flow design proposes checks for both routes, but it has no verified connector or latency evidence.
- The custom design proposes both routes, reject-before-handoff behaviour and a record trace.
- The custom maintenance owner remains unassigned.
- AI-assisted validation still has no demonstrated language need.
- Use the worked base scores for the remaining designs.
- No option has confirmed live permissions or entitlement.
- Sales Lead owns business acceptance; IT must assess technical delivery and support.

A representative imported record is:

MSP-ENQ-781: product BF-10, quantity missing, requested date 2026-10-22.

An attached private staff note is not authorised for use and contains no permitted correction value.

Deliverables

1. Identify which option fails the essential requirement.
2. Rank the remaining designs under the base weights.
3. State the correct reference outcome for case 781.
4. Recommend proceed, revise or defer for a clearly named next step.
5. Identify two evidence requests and one scorecard limitation.

Success criteria

Your answer must cover both entry routes, preserve missing quantity, exclude the private note and distinguish a preferred design from a live-ready implementation.

## 7. Common problems and recovery

| Symptom | Diagnosis | Correction | Verification |
| --- | --- | --- | --- |
| The highest score wins despite missing output | A requirement was treated as a preference | Apply task-fit gates first | Every scored candidate can plausibly produce the required result |
| Native is assumed to mean free | Existing product presence was confused with entitlement and effort | Check configuration, testing, licensing and maintenance | Cost assumptions are explicit |
| Flow receives credit for fixing source errors | Data movement was confused with data quality | Add validation and exception requirements | Incorrect input cannot silently become accepted output |
| Custom development receives a high feasibility score because “anything can be built” | Delivery resources were ignored | Include skills, interfaces, budget and maintenance | Feasibility refers to this organisation and scope |
| AI receives credit for an unrelated capability | Broader features were compared against a narrow task | Score only the required work | Extra language ability is relevant only when the task needs it |
| Reversibility means only “switch it off” | Existing effects were ignored | Define record reconciliation and manual fallback | Created records remain identifiable |
| Weights are changed after seeing the winner | Scoring is being used to justify a preference | State base priorities, then report sensitivity separately | Both results and reasons remain visible |
| A 45% readiness score is compared with a 73.33-point selection score | Different matrices and scopes were mixed | Label purpose, weights and boundary | Each figure answers its own question |

## 8. Check your understanding

1. Why does MSP-OPP-001 have a different comparison boundary from MSP-OPP-002?
2. Why is quantity 60 valid at intake even when the supplied stock snapshot lists 40?
3. What does the worked sensitivity analysis reveal?
4. Why must an export-only option be separated from an automatic-create option?
5. What remains after a write-based workflow is stopped?
6. Why should the recommendation name both a business owner and a technical support owner?

## 9. Solutions and explanations

Lesson checks

L1: Availability establishes neither a recurring problem nor a useful expected result. You need issue evidence, task fit, costs and consequences.

L2: Native validation is a plausible starting point for a fixed in-application rule. An integration platform becomes more relevant when checked information must cross applications. Actual capabilities still require confirmation.

L3: Exclude or redesign it. A weighted total cannot compensate for failure to produce the essential output.

L4: The score combines ordinal judgements with selected weights. It is not based on a statistical model of implementation outcomes.

L5: Explain the criterion driving the change, the evidence uncertainty and what must be verified before choosing. Do not present a fragile lead as decisive.

### Guided practice — Completed option comparison

| Option | Task-fit status | Base result | Main dependency | Next step |
| --- | --- | --- | --- | --- |
| Native | Fails as a complete standalone solution | Not scored | Cannot create the required request | Retain as a manual/export comparator or redesign |
| Flow | Provisionally fits | 66.67 | Connector, permissions and operating evidence | Verify the bounded transfer design |
| Custom | Provisionally fits | 63.33 | Build effort and maintenance owner | Retain as a containment-focused alternative |
| AI | Provisionally fits through supporting checks | 35.00 | Additional model and review dependencies | Do not prioritise without an evidenced language need |

Flow calculation:

(2×20 + 2×20 + 2×15 + 2×15 + 2×15 + 2×5 + 2×10) ÷ 3

= 200 ÷ 3 = 66.67

Custom calculation:

(2×20 + 2×20 + 1×15 + 2×15 + 3×15 + 2×5 + 1×10) ÷ 3

= 190 ÷ 3 = 63.33

AI calculation:

(1×20 + 1×20 + 1×15 + 1×15 + 1×15 + 2×5 + 1×10) ÷ 3

= 105 ÷ 3 = 35.00

Under failure-focused weights:

| Option | Base total | Failure-focused total |
| --- | --- | --- |
| Flow | 66.67 | 66.67 |
| Custom | 63.33 | 73.33 |
| AI | 35.00 | 35.00 |

The leading design changes from Flow to custom. The base difference is only 3.33 points, so the recommendation should not treat it as decisive evidence.

### Guided practice — Completed exception outcomes

| Case | Permitted action | What must not happen |
| --- | --- | --- |
| 751 | Create one linked request in the hypothetical design | Do not promise delivery or replace the business ID |
| 752 | Clarify quantity | Do not guess a quantity or create a normal request |
| 753 | Hold create; refer permission issue | Do not infer write permission from read access |
| 754 | Reconcile REQ-7402 against the matching business reference and fields | Do not retry by creating a duplicate |

An acceptable recommendation is:

Investigate the Flow design first under the base priorities, retaining custom development as a containment-focused alternative. Verify the lookup/create actions, permissions, reconciliation behaviour and support ownership. The failure-focused ranking changes the leader, so check whether Flow can meet the required containment before choosing. The export-only native option is incomplete, and AI adds no demonstrated benefit for the stated transfer.

A hybrid alternative is acceptable if you define its additional components, costs and ownership. Do not treat an export plus an unspecified automation as a complete design.

### Independent challenge — Explained solution

The native option fails because the required scope includes imports and the supplied assessment confirms that it cannot evaluate them.

The remaining base ranking is:

1. Custom: 63.33
2. Flow: 56.67
3. AI-assisted: 35.00

Case 781 must receive a missing-quantity exception before normal handoff. The private note is excluded. It supplies no authorised correction.

A suitable decision is:

Proceed with technical verification of the custom validator design; revise the proposal before any live use. Confirm both entry routes, reject-before-handoff behaviour, permissions, entitlement and a maintenance owner. Keep Flow as an alternative if its interface and containment can meet the requirement. Sales owns business acceptance; IT must establish technical delivery and support.

This is also acceptable:

Defer live implementation while continuing bounded design assessment.

The next step must be explicit. A bare “proceed” would be misleading.

Two useful evidence requests are:

1. Demonstrate both form and import validation against permitted normal and invalid cases in an authorised test environment.
2. Confirm the support owner, required permissions and entitlement for the preferred design.

A suitable limitation is:

The scores assess proposed designs, not observed reliability or total cost. The ranking cannot establish that the preferred design is affordable or live-ready.

Understanding questions

1. Opportunity 001 concerns fixed intake validity. Opportunity 002 concerns organisation of wording and approved source facts. Their required outputs, costs and mechanisms differ.
2. Intake validity asks whether the request is usable. Availability asks whether Meridian can meet it. A valid request can still require an Operations exception.
3. The choice depends on how strongly failure containment is prioritised and whether the proposed controls are actually achievable.
4. They produce different results. Export may assist manual work but does not by itself remove rekeying or create the linked request.
5. Existing created or changed records may remain. They need traceability, reconciliation and a defined owner.
6. The business owner accepts the result and consequences. The technical owner supports configuration, operation and maintenance. Neither responsibility automatically replaces the other.

## 10. Chapter recap and next step

Good selection begins with a defined task and essential requirements. It compares mechanisms against the same output and makes uncertainty visible.

A weighted matrix can organise judgement, but it cannot repair missing evidence, grant permission or turn a provisional forecast into an observed result. Sensitivity helps identify what matters most before you invest further.

“I can…” checklist

- I can distinguish prioritisation from solution selection.
- I can compare native features, Flow, custom development and AI.
- I can apply essential requirements before ranking.
- I can evaluate all seven comparison criteria.
- I can calculate a weighted index and explain its limits.
- I can test whether priorities change the leading option.
- I can name a conditional next step and its owners.

Your project artifacts are:

- MSP_Option_Comparison_v0_1.md
- MSP_Prioritisation_Rationale_v0_1.md
- MSP_Solution_Recommendation_v0_1.md
- MSP_Case_Assumptions_v0_6.md

Completed prioritisation rationale:

Investigate native validation for MSP-OPP-001 because required-field issues recur and the bounded task may require few new components. Compare the template with generative assistance for MSP-OPP-002 using measured review and operating effort. Resolve shared-record suitability and transfer dependencies for MSP-OPP-003. This sequence prioritises evidence collection rather than approving implementation.

Retain assumptions MSP-A-001 through MSP-A-020 and add:

| Assumption ID | Added assumption | Status |
| --- | --- | --- |
| MSP-A-021 | Native features can perform the exact checks across included entry routes | Unconfirmed |
| MSP-A-022 | Required Flow triggers and actions can support the proposed scope | Unconfirmed |
| MSP-A-023 | Custom containment and traceability can be delivered within acceptable resources | Proposed design only |
| MSP-A-024 | Base comparison weights reflect leadership priorities | Workshop assumption; sensitivity supplied |
| MSP-A-025 | Technical support and maintenance can be assigned for the selected mechanism | Unresolved |

Chapter 7, Human Responsibility and Operating Controls, builds on the preferred designs by defining review points, decision ownership, data handling, escalation and incident responsibility.

## 11. Glossary and further reading

Glossary

| Term | Meaning |
| --- | --- |
| Essential requirement | A condition an option must satisfy to perform the stated task |
| Feasibility | Ability to deliver a defined change within actual constraints |
| Gate | A requirement that must be resolved before a specified decision |
| Native feature | Capability provided inside the application where work occurs |
| Prioritisation | Choosing which opportunity receives attention next |
| Reversibility | Ability to stop a change and recover from its effects |
| Solution selection | Choosing a mechanism for a defined opportunity |
| Task fit | Whether an option can produce the required output within the boundary |
| Weighted index | Combined comparison result using stated criteria and weights |

Further reading

Official sources were accessed for the product and architectural concepts cited here. No product was executed. Meridian’s application, native capability, connectors, editions, entitlements, permissions and regional dependencies remain unverified.

1. Microsoft Learn — Create a business rule in Microsoft Dataverse. Describes validation and other business-rule actions, with scope and app-type dependencies. It is a capability example, not confirmation of Meridian’s application.

https://learn.microsoft.com/en-us/power-apps/maker/data-platform/data-platform-create-business-rule

2. Zoho Flow — FAQ. Describes cross-app trigger/action workflows and explains that deleting a flow does not remove earlier updates in other applications.

https://www.zoho.com/flow/help/faq.html

3. Anthropic — Building effective agents. Explains predefined workflows, dynamically directed agents and the trade-off between added capability and complexity. Use it for architectural reasoning rather than current configuration procedures.

https://www.anthropic.com/engineering/building-effective-agents

[1]: https://learn.microsoft.com/en-us/power-apps/maker/data-platform/data-platform-create-business-rule

[2]: https://www.zoho.com/flow/help/faq.html

[3]: https://www.anthropic.com/engineering/building-effective-agents
