# User Experience and Release

C03-CH20 — User Experience and Release
1. What you will learn
A technically capable assistant still needs a safe and understandable user experience. Users need to know where an answer came from, when the system is uncertain, what an action will do and when a human must take over. Teams need a controlled way to move configuration from development to pilot, respond to provider changes, revert a release and learn from feedback.
This final chapter teaches you to:
- present citations beside the claims they support;
- communicate uncertainty and missing evidence without sounding falsely definitive;
- show action previews before consequential changes;
- define escalation triggers and useful handoff information;
- prepare pilot acceptance criteria and a user walkthrough;
- promote a versioned configuration through release gates;
- plan fallbacks for provider, model, knowledge and action-adapter changes;
- revert to a known-good release without losing evidence; and
- collect feedback as a controlled project input.
The Northstar release-pack fixture is NST-REL-001. It includes a candidate manifest, pilot acceptance table, feedback records, provider-change matrix and user walkthrough. The pack is intentionally blocked: held-out action safety is 0.75 instead of the required 1.0, and the monitoring fixture contains an unresolved tenant-boundary security incident. The correct release decision is to stop promotion, fix the blockers and repeat the gates.
2. Lessons
2.1 Citations should help users verify a claim
A citation is useful when the user can tell which claim it supports. Put source identity close to the claim rather than collecting unrelated links at the bottom of a long answer.
For Northstar, a policy response can use:
Do not promise a refund for the opened carton. Route the request to a Sales Manager for review. [NST-POLICY-001:v3#returns]
The citation should identify an approved source and version. The application should ensure that the cited source was permitted for the authenticated tenant and available when the answer was generated.
Do not use citations as decoration. A response fails groundedness when the source is present but does not support the claim, when a superseded version is cited or when the answer makes a stronger promise than the source allows.
In the user interface, make citations inspectable without overwhelming the answer. A source label can open a controlled excerpt, source title, version and freshness marker. Do not expose restricted source content merely because the assistant cited it.
2.2 Communicate uncertainty as a useful next step
Uncertainty should tell the user what is known, what is missing and what can happen next.
Situation	Weak wording	Better wording
Missing invoice date	“The date is probably 2026-09-30.”	“The invoice date is missing. Please provide the invoice or confirm the date before we continue.”
Conflicting policy versions	“The policy allows a refund.”	“The retrieved versions conflict. I found v2 and v3; v3 is current, so I will use v3 and cite it.”
No permitted record	“The customer does not exist.”	“I cannot provide that record in the current access scope.”
Provider unavailable	“The CRM update succeeded.”	“I prepared the change, but the action service is unavailable. No record change was confirmed.”
Stale action	“I retried the note.”	“The record changed after approval. The action stopped; a fresh preview is required.”
The assistant should not use vague confidence scores as a substitute for evidence. A useful uncertainty message is tied to a missing field, conflicting version, permission boundary or unavailable dependency.
2.3 Action previews make consequences visible
A user should see an action preview before a consequential operation. At minimum, show:
- operation;
- target and tenant scope;
- current record version;
- proposed change;
- expected side effects;
- approval requirement and reviewer role;
- expiration or freshness condition; and
- what will happen if the record changes.
Example:
Proposed action: append an internal note
Target: Alder Retail (NST-CUST-001)
Current record version: r7
Change: Follow up on invoice date and route opened-carton request to Sales Manager.
Side effect: one internal note; no public reply or refund promise
Approval: separate Sales Manager required
Status: preview only
The confirmation control should identify the exact preview, not just offer a generic “yes.” The server must revalidate the actor, reviewer, tenant, target and record version. A user-interface button is not a permission boundary.
2.4 Escalation is part of the product behavior
Escalation should be designed, not added as “contact support” after a failure. Define triggers, destination, evidence and user-visible expectation.
Trigger	Escalate to	Preserve	User message
Policy missing or conflicting	Knowledge Editor or Sales Manager	Source IDs, versions and question	“I need an approved policy decision before answering definitively.”
Cross-tenant or unauthorized request	Administrator/security owner	Principal, tenant and denial code	“I cannot provide that information in this access scope.”
High-risk action or stale record	Sales Manager	Preview hash, versions and action ID	“The change is paused; a reviewer must approve a fresh preview.”
Provider unavailable	Operations/action owner	Trace ID, adapter status and receipt state	“No provider change was confirmed. The preview is retained.”
Prompt injection or secret exposure	Security owner	Redacted trace and source/tool ID	“I stopped because the content attempted an unsafe instruction.”
The handoff must contain enough context for a human to act without requesting the user to repeat private information. Use trace IDs and controlled source references instead of copying full prompts into tickets.
2.5 Pilot acceptance tests the experience and the controls
A pilot is not a production launch with fewer users. It is a controlled evidence-gathering phase with explicit entry, acceptance and exit conditions.
Pilot acceptance should cover:
- citation visibility and source correctness;
- uncertainty and missing-data language;
- action preview and approval separation;
- cross-customer and cross-tenant permissions;
- prompt-injection and secret handling;
- escalation and handoff behavior;
- latency and availability expectations;
- trace and feedback collection; and
- known blockers and rollback ownership.
Use a table with target, observed result, status, owner and evidence. A failed high-risk gate must block promotion even if the average pilot rating is positive.
The Northstar acceptance table has four passing experience/control gates and two failed release gates. The two failures are not hidden in an average:
1. held-out action safety is 0.75, below the required 1.0; and
2. a critical tenant-boundary incident remains unresolved in monitoring evidence.
2.6 Promote a versioned configuration, not a collection of files
A release manifest should identify the complete behavior bundle:
Component	Candidate value
Prompt	p18.2
Model	hybrid_v2
Tool contract	tc14.1
Knowledge version	NST-POLICY-001:v3
Evaluator	eval-0.4
Application	app-2026-10-05.2
Environment	pilot
Promotion is a state transition such as:
draft → validated → pilot → approved → production → retired
The transition should require the release gates relevant to the risk. The manifest should point to test results, runbook, fallback behavior and previous release. Avoid changing a prompt, model, knowledge source and tool schema together without recording each change; otherwise a later regression cannot be diagnosed.
2.7 Provider changes require capability checks and fallbacks
Providers can change model availability, API versions, rate limits, tool schemas, structured-output behavior, pricing, regions or deprecation status. A provider change is a release input even when the application code is unchanged.
For each dependency, document:
- how change is detected;
- what capability the application requires;
- temporary behavior during uncertainty;
- whether actions are disabled or draft-only;
- which fallback is supported;
- which tests must pass before reopening; and
- who owns the decision.
A fallback should preserve the safety boundary. If the action adapter is unavailable, a safe fallback is a retained preview with no receipt, not a claim of success. If current knowledge is unavailable, a safe fallback is uncertainty and escalation, not a memorized policy promise.
2.8 Reversion is a supported operation
Reversion should be planned before release. Define:
1. trigger conditions;
2. the known-good target release;
3. the route or feature to disable;
4. how pending actions are handled;
5. what evidence must be preserved;
6. who approves the reversion; and
7. which tests verify the restored release.
For NST-REL-001, a critical security alert or failed release gate stops promotion and targets NST-REL-000. The reversion steps disable the changed route, restore the previous manifest, run security and smoke cases, then record the incident and owner.
Do not delete the failed release’s traces or feedback. A reversion restores service behavior; it does not erase the history needed to understand the failure.
2.9 Feedback is a controlled input to the next version
Pilot feedback should identify the scenario, role, issue, requested change and status. Avoid placing real customer data or secrets into an unstructured feedback field.
Classify feedback as:
- defect requiring correction;
- usability improvement;
- documentation or training need;
- policy or knowledge issue;
- accepted limitation; or
- release blocker.
Feedback should link to evaluation or trace evidence when possible. “Users disliked it” is less actionable than “three pilot users could not find the approval owner in the preview for action AC01.”
Prioritize feedback by risk and frequency, not only by the number of votes. One credible cross-tenant disclosure can outweigh many requests for cosmetic changes.
3. Visual explanation
flowchart TD
    A[Versioned release manifest] --> B[Validation gates]
    B --> C{Pilot accepted?}
    C -- no --> D[Block promotion and assign blockers]
    C -- yes --> E[Controlled promotion]
    E --> F[User walkthrough and feedback]
    F --> G[Monitoring and incident evidence]
    G --> H{Provider change or release failure?}
    H -- no --> I[Continue supported operation]
    H -- yes --> J[Fallback or revert to known-good release]
    J --> K[Verify tests and record follow-up]
The release manifest binds configuration to evidence. Pilot acceptance determines whether promotion is allowed. After promotion, feedback and monitoring remain part of the release lifecycle. Fallback and reversion are supported paths, not improvised emergency behavior.
4. Worked case
Candidate release
NST-REL-001 proposes:
{
  "environment": "pilot",
  "prompt_version": "p18.2",
  "model_id": "hybrid_v2",
  "tool_contract_version": "tc14.1",
  "knowledge_version": "NST-POLICY-001:v3",
  "promotion_allowed": false,
  "previous_release": "NST-REL-000"
}
The manifest includes citations, uncertainty, action-preview and security gates. It also includes explicit fallbacks for provider unavailability, missing knowledge, unavailable action adapters and model timeouts.
Acceptance result
Gate	Target	Observed	Status
Citations visible	pass	pass	pass
Uncertainty language	pass	pass	pass
Action preview	pass	pass	pass
Permission and security controls	pass	pass	pass
Held-out action safety	1.0	0.75	fail
Critical monitoring alerts	0	1	fail
The release cannot be promoted. The correct user experience is still usable in a pilot environment, but the release owner must communicate that the candidate is blocked and that no production promotion occurred.
User walkthrough result
The walkthrough checks:
1. a policy answer with a nearby citation;
2. a missing invoice date with uncertainty language;
3. an internal-note preview with version and approval details;
4. a cross-tenant request with minimal denial; and
5. escalation with a trace ID and next step.
The walkthrough itself passes because the experience controls are present. That does not override the failed held-out action and critical monitoring gates.
Reversion decision
If the pilot route were already receiving traffic and the security alert were confirmed, the supported response would be:
stop promotion
→ disable the changed route
→ restore NST-REL-000
→ verify security and smoke cases
→ preserve traces and feedback
→ record owner, impact and follow-up
5. Try it yourself — guided practice
Goal
Validate a release pack and explain why a blocked candidate must not be promoted.
Complete manifest excerpt
{
  "release_id": "NST-REL-001",
  "candidate_version": "0.1",
  "environment": "pilot",
  "status": "blocked",
  "promotion_allowed": false,
  "previous_release": "NST-REL-000",
  "components": {
    "prompt_version": "p18.2",
    "model_id": "hybrid_v2",
    "tool_contract_version": "tc14.1",
    "knowledge_version": "NST-POLICY-001:v3",
    "evaluator_version": "eval-0.4",
    "application_version": "app-2026-10-05.2"
  },
  "blockers": [
    "Held-out H03 still contains a committed-action regression.",
    "Monitoring fixture contains an unresolved tenant-boundary security incident."
  ]
}
Use the complete files:
- release_manifest.json;
- pilot_acceptance.csv;
- pilot_feedback.csv;
- provider_change_matrix.csv;
- user_walkthrough.md; and
- check_release_pack.py.
Steps
1. Compile the checker:
python3 -B -m py_compile check_release_pack.py
2. Validate the pack:
python3 -B check_release_pack.py \
  --manifest release_manifest.json \
  --acceptance pilot_acceptance.csv \
  --feedback pilot_feedback.csv \
  --changes provider_change_matrix.csv \
  --walkthrough user_walkthrough.md \
  --out release_results.json
3. Identify the failed gates and blocking feedback.
4. Explain what must change before promotion_allowed can become true.
5. For each provider-change row, identify the temporary user behavior and verification test.
6. Read the walkthrough as a pilot user and record whether each expected result is understandable.
Expected result
The checker reports:
{
  "release_id": "NST-REL-001",
  "promotion_allowed": false,
  "acceptance_rows": 6,
  "failed_gates": 2,
  "feedback_rows": 5,
  "blocking_feedback": 1,
  "provider_change_rows": 5,
  "walkthrough_verified": true,
  "result": "PASS_BLOCKED_RELEASE",
  "live_execution": "not_run"
}
PASS_BLOCKED_RELEASE means the release-pack checker worked. It does not mean the candidate is ready for promotion.
6. Independent challenge
Create a release pack for a corrected candidate called NST-REL-002. Use these requirements:
prompt_version: p18.3
model_id: hybrid_v2
tool_contract_version: tc14.2
knowledge_version: NST-POLICY-001:v3
previous_release: NST-REL-000
Your pack must include:
1. a release manifest with all component versions;
2. acceptance criteria for citations, uncertainty, previews, escalation, permissions, held-out action safety and monitoring alerts;
3. a user walkthrough with at least four scenarios;
4. a provider-change matrix with fallback behavior;
5. a reversion plan to NST-REL-000; and
6. three synthetic pilot-feedback rows, including one blocking issue.
The corrected candidate may claim promotion eligibility only if the held-out action regression has been fixed, the tenant-boundary incident has been resolved and the relevant tests have been rerun. If any gate remains unresolved, mark the release blocked and explain why.
7. Common problems and recovery
Symptom	Diagnosis	Recovery	Verification
Users cannot tell which source supports an answer	Citations are distant or opaque	Place source ID/version beside the claim and provide a controlled excerpt	Pilot user can identify the supporting source
The assistant sounds certain with missing data	Uncertainty was treated as a model style issue	Add explicit missing-data and escalation behaviors	Missing-data cases pass evaluation
A confirmation button commits the wrong target	UI confirmation was treated as authorization	Bind confirmation to a server-side preview hash and revalidate	Wrong target or stale version is rejected
Pilot feedback is too vague to action	Feedback lacks scenario and evidence	Require scenario, role, issue, requested change and status	Each row maps to a test or owner
A provider change silently alters behavior	Configuration was not versioned	Pin component versions and gate promotion	Manifest identifies every changed component
Provider outage causes false success	Fallback behavior was undefined	Return read-only, draft-only or escalation state	No receipt is claimed during outage
Reversion restores code but not knowledge	Release is more than application code	Restore the complete manifest and source versions	Smoke and citation tests use the restored bundle
A failed gate is hidden by positive pilot ratings	Acceptance was averaged	Treat critical gates as blockers	promotion_allowed remains false
Feedback contains customer secrets	Feedback form accepts unrestricted text	Use synthetic IDs, redaction and access control	Feedback checker contains no raw secrets
8. Check your understanding
 1. What makes a citation useful to a user?
 2. Why should uncertainty identify a next step?
 3. Which fields belong in an action preview?
 4. Why is a pilot not simply a smaller production launch?
 5. What should a release manifest version besides application code?
 6. Give one safe fallback for an unavailable action adapter.
 7. What is the difference between fallback and reversion?
 8. Why should a single critical security failure block promotion even if pilot ratings are positive?
 9. What information makes pilot feedback actionable?
10. What must be preserved when reverting a failed release?
9. Solutions and explanations
1. A citation is useful when it identifies an approved source and version close to the claim, supports that claim and can be inspected within the user’s access scope.
2. Uncertainty without a next step leaves the user unable to proceed. A good message identifies the missing or conflicting evidence and explains whether the user should provide information, wait, approve, or escalate.
3. Show operation, target, tenant scope, current version, proposed change, side effects, approval requirement, freshness/expiry and the behavior if the record changes.
4. A pilot is controlled evidence gathering with explicit acceptance and rollback conditions. It must test user experience and safety controls before promotion, and it should have limited scope and owners.
5. Version prompts, model/deployment, tool contracts, knowledge sources, evaluator, application release and environment. Any component that can change behavior belongs in the manifest.
6. Keep the action as a receipt-free preview, return a read-only result or escalate. Never claim that the provider change succeeded without a verified receipt.
7. A fallback handles a dependency or capability problem while the current release remains active. Reversion moves the system back to a known-good release after a release failure or serious risk.
8. A security failure can expose protected data or create unauthorized access. Aggregate satisfaction cannot compensate for a broken security boundary.
9. Include a synthetic pilot-user ID, role, scenario, rating, issue, requested change and status. Link to a trace, evaluation case or release gate when appropriate.
10. Preserve traces, feedback, incident records, failed manifest, impact assessment and ownership. Reversion changes service behavior; it does not erase evidence.
The guided release result is:
Area	Result	Decision
Citation and uncertainty UX	Pass	Retain in candidate
Action preview	Pass	Retain with server-side revalidation
Permission and injection controls	Pass in the security fixture	Continue monitoring
Held-out action safety	Fail at 0.75	Fix H03 and rerun evaluation
Critical monitoring alerts	Fail with tenant-boundary incident	Contain, diagnose and verify before promotion
Feedback	One blocking item	Assign owner and track to closure
The correct outcome is PASS_BLOCKED_RELEASE, not production approval.
10. Chapter recap and next step
Release is a controlled user and system transition:
explain evidence → preview consequences → escalate uncertainty
→ validate pilot behavior → promote a manifest → monitor
→ fallback or revert safely → learn from feedback
You should now be able to say:
- I can place citations where users can verify claims.
- I can communicate uncertainty with a useful next step.
- I can show an action preview before a consequential change.
- I can design escalation triggers and a human handoff.
- I can prepare pilot acceptance criteria and a walkthrough.
- I can promote versioned configuration only after release gates pass.
- I can specify provider-change fallbacks and supported reversion.
- I can use feedback as structured evidence for the next iteration.
The Northstar project now has a complete student-coursebook lifecycle from use-case definition through model choice, action control, evaluation, security, efficiency, observability and release planning. The release pack remains blocked until its explicit action-safety and security blockers are resolved.
11. Glossary and further reading
Glossary
- Action preview: A user-visible description of a proposed side effect before commit.
- Escalation: Transfer of a question, decision or incident to an authorized human or team.
- Fallback: Supported temporary behavior when a dependency or capability is unavailable.
- Pilot acceptance: Evidence-based criteria used to decide whether a limited candidate can proceed.
- Promotion: Moving a versioned configuration from one controlled environment or state to another.
- Release manifest: A versioned record of prompts, models, tools, knowledge, evaluator, application and environment.
- Reversion: Restoring a previous known-good release after a failure or unacceptable risk.
- Uncertainty language: User-facing explanation of missing, conflicting or unavailable evidence.
- User walkthrough: A scripted set of scenarios used to verify the experience and expected controls.
Further reading
- NIST AI Risk Management Framework (https://www.nist.gov/itl/ai-risk-management-framework) — risk management and trustworthy operation considerations.
- OWASP LLM01:2025 Prompt Injection (https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — source separation, output validation, least privilege and human approval.
- OpenAI Prompt Caching (https://developers.openai.com/api/docs/guides/prompt-caching) — operational monitoring and behavior changes that can affect a release.
- OpenAI Batch API (https://developers.openai.com/api/docs/guides/batch) — asynchronous processing and release-test workload considerations.
- Northstar Chapter 14 — Controlled Business-System Actions (C03_CH14_Controlled_Business-System_Actions_Student.md) — action previews, approval and revalidation.
- Northstar Chapter 19 — Observability and Reliability (C03_CH19_Observability_and_Reliability_Student.md) — traces, alerts, incidents and runbooks used in this release pack.
