# Observability and Reliability

C03-CH19 — Observability and Reliability
1. What you will learn
An assistant can fail in many places before the user sees a response. Retrieval may return a stale source, a tool may time out, a model version may change, an action may stop safely or an authorization boundary may be crossed. A final chat message is not enough evidence to distinguish these cases.
This chapter teaches you to:
- define a trace that connects a session, turn, model call, retrieval operation, tool call and outcome;
- record prompt, model, tool-contract and knowledge versions;
- measure latency distributions, token and cache usage, failures, retries and tool errors;
- sample answer quality and action safety without logging unnecessary sensitive content;
- design alerts with thresholds, denominators and trace correlation;
- distinguish a normal safety stop from an operational incident;
- diagnose incidents with a structured runbook; and
- verify recovery with regression, security and quality checks.
The Northstar artifact is an offline monitoring view over five authored traces. It raises alerts for high p95 latency, high error rate, quality regression, a security incident and knowledge-version drift. It includes four incident cases and a six-stage runbook. It does not call a model, provider or live tenant.
2. Lessons
2.1 Observability is evidence about a system path
Monitoring a final response alone cannot answer:
- Which prompt and model version produced it?
- Which knowledge source and version were retrieved?
- Which tools were called, with what duration and result?
- Did a retry consume more tokens?
- Was an action committed, stopped or never attempted?
- Did quality or security checks run?
Use a trace as the correlation boundary for one session turn or logical request. A trace contains spans for meaningful operations, such as retrieval, model generation, authorization, approval and provider calls.
{
  "trace_id": "T002",
  "session_id": "S002",
  "turn_id": "turn-04",
  "tenant_id": "NST-TENANT-001",
  "actor_id": "NST-USER-001",
  "prompt_version": "p18.2",
  "model_id": "hybrid_v2",
  "tool_contract_version": "tc14.1",
  "knowledge_version": "NST-POLICY-001:v3",
  "outcome": "STOP_STALE",
  "error_code": "STOP_STALE"
}
The trace metadata identifies the path. Spans explain where time was spent and what failed. Keep identifiers stable enough to correlate evidence, but do not put raw secrets or full private prompts in ordinary logs.
2.2 Version every behavior that can change
A production trace should record the versions that influence behavior:
Version	Examples	Diagnosis supported
Prompt/instruction	p18.2	Did a prompt change cause the regression?
Model/deployment	hybrid_v2	Did the selected model or snapshot change?
Tool contract	tc14.1	Did a schema, permission or tool description change?
Knowledge source	NST-POLICY-001:v3	Was the answer based on the current policy?
Evaluator	eval-0.4	Did scoring logic change?
Application release	app-2026-10-05.2	Which code was running?
Do not log only a human-friendly name such as “sales assistant.” Two deployments can share that name while using different prompts, tools and knowledge. Version records turn a vague regression into a comparison.
Versioning also supports rollback. A known-good prompt and tool-contract bundle is more useful than an instruction to “restore yesterday’s behavior” without identifiers.
2.3 Trace spans should explain latency and failure boundaries
A span represents one operation within a trace. Useful span fields include:
- span_id and parent_span_id;
- operation and component name;
- start time and duration;
- status and error code;
- tool name, when relevant;
- input/output token counts or cache counts where permitted;
- retry attempt number; and
- redacted correlation data.
For example, T003 has two failed retrieval spans with TOOL_TIMEOUT. The trace makes it possible to distinguish retrieval delay from model generation delay. A retry without a new trace or attempt number would make the cost and failure pattern difficult to interpret.
Do not assume every failure is a model failure. A timeout can occur in DNS, a provider queue, a retrieval index, an authorization service, a tool connector or the application’s own worker pool. The component and error code should identify the boundary without exposing sensitive payloads.
2.4 Measure reliability with named denominators
Useful rates include:
error_rate = failed_or_incident_traces / total_traces

quality_sample_pass_rate = quality_passes / quality_sampled_traces

action_safety_pass_rate = safe_action_outcomes / total_action_traces

tool_failure_rate = failed_tool_spans / total_tool_spans

unfinished_rate = unfinished_logical_requests / total_logical_requests
Every rate needs a population and time window. A 100% quality rate over two manually selected examples does not establish production quality. A 2% error rate over one million requests may require more urgent attention than 20% over five exploratory tests, depending on the impact.
Keep business outcomes separate from infrastructure outcomes. A STOP_STALE action is a safe business control, not automatically an application outage. A response that succeeds technically but cites stale policy may be a quality incident.
2.5 Sample quality without copying sensitive content
Quality sampling can inspect a bounded proportion of traces or use risk-based sampling. Sample cases involving:
- current and outdated knowledge;
- missing or ambiguous context;
- high-risk actions;
- permission denials;
- prompt injection;
- tool failures and retries; and
- user feedback or escalation.
Store quality labels, source IDs and reason codes rather than full private content whenever possible. A sampled record can contain groundedness_pass: false, source_version: v2, reviewer_id and trace_id without copying the customer’s entire conversation into a general log.
Action safety should be sampled separately from answer quality. A response can be fluent and grounded while returning an unsafe action object. Chapter 15’s dimension scorecard and Chapter 16’s security cases are inputs to reliability monitoring.
2.6 Alerts should identify a decision, not create noise
An alert should have:
1. a measured signal;
2. a named denominator and time window;
3. a threshold or comparison baseline;
4. severity and owner;
5. a link to correlated traces; and
6. a runbook action.
The fixture thresholds are illustrative:
Alert	Threshold	Owner question
P95_LATENCY_HIGH	p95 above 1200 ms	Which component or queue is slow?
ERROR_RATE_HIGH	error rate above 15%	Is there a common failing dependency?
QUALITY_REGRESSION	sampled quality below 95%	Did a version or knowledge source change?
SECURITY_INCIDENT	any tenant disclosure	Which access path must be contained now?
KNOWLEDGE_VERSION_DRIFT	trace source differs from current v3	Why was an outdated source eligible?
Avoid alerting on every safe stop. A stale action may be expected behavior, while a sudden increase in stale stops may indicate a concurrency or integration problem. Use a count, rate or trend alert appropriate to the event.
2.7 Reliability is controlled degradation, not “never fail”
Reliable behavior defines what happens when a dependency fails:
- bounded retry for transient retrieval failure;
- no blind retry for a write or stale action;
- safe fallback only when it preserves grounding and permissions;
- explicit refusal when required context is unavailable;
- circuit breaking when a dependency repeatedly fails;
- rate limiting and backpressure under load; and
- a trace outcome that explains the stop.
T003 demonstrates a poor recovery result: two retrieval timeouts lead to a failed trace. The runbook should determine whether the retry budget, fallback and alerting are appropriate. T002 demonstrates a correct safety stop: the stale action does not retry the commit. Reliability is not achieved by converting every stop into a success message.
2.8 Diagnose incidents by comparing traces and versions
Use a fixed diagnosis sequence:
1. Confirm the alert and time window.
2. Identify affected tenants, sessions, traces and logical requests.
3. Compare prompt, model, tool-contract, knowledge and application versions with a known-good period.
4. Inspect span duration, retries, error codes and partial results.
5. Determine whether data was disclosed or a side effect occurred.
6. Contain the affected route or tool if necessary.
7. Restore a known-good configuration or apply a reviewed fix.
8. Run representative, held-out, action and security checks before reopening.
9. Record root cause, impact, owner and follow-up work.
Do not delete traces to make an alert disappear. Redact sensitive values, restrict access and retain the evidence needed to understand impact.
2.9 A runbook connects metrics to action
A monitoring view without a runbook tells someone that a problem exists but not what to do. The Northstar runbook has six stages:
Stage	Output
Detect	Alert, time and correlated trace IDs
Contain	Owner, affected route and safe containment action
Diagnose	Version comparison, spans, errors and scope
Recover	Reviewed rollback or fix
Verify	Regression, quality and security checks
Close	Impact, root cause, owner and follow-up
The runbook must distinguish incidents from expected controls. STOP_STALE is usually a safe action outcome that may become an incident only if its rate increases or indicates a broken version mapping. TENANT_BOUNDARY_BREACH is a security incident even if no live provider was called in the fixture.
3. Visual explanation
flowchart TD
    A[Request] --> B[Trace context]
    B --> C[Versioned prompt/model/knowledge/tools]
    C --> D[Retrieval and tool spans]
    D --> E[Validated response or action]
    E --> F[Outcome, quality sample and audit event]
    F --> G[Metrics and alerts]
    G --> H{Incident or expected stop?}
    H -- expected --> I[Measure trend and continue]
    H -- incident --> J[Contain, diagnose, recover]
    J --> K[Run regression and security checks]
    K --> L[Close with evidence and follow-up]
The trace begins before model execution and ends after validation. Versions travel with the trace. Metrics aggregate many traces, while the runbook returns from an alert to individual evidence. Recovery is incomplete until the relevant evaluation and security checks pass.
4. Worked case
Monitoring result
The local view contains five traces:
Metric	Result
Traces	5
Outcomes	2 success, 1 STOP_STALE, 1 failed, 1 security incident
Error rate	0.400
Quality sample pass rate	0.400
Action-safety pass rate	0.800
Security pass rate	0.800
P95 end-to-end latency	3200 ms
Tool calls	7
Tool failures	2
Tool failure rate	0.286
Cached input tokens	3200
The thresholds are p95 below 1200 ms, error rate at or below 0.15, quality sample pass rate at or above 0.95 and current knowledge version NST-POLICY-001:v3. The view raises five alerts:
[
  {"code":"P95_LATENCY_HIGH","value":3200},
  {"code":"ERROR_RATE_HIGH","value":0.4},
  {"code":"QUALITY_REGRESSION","value":0.4},
  {"code":"SECURITY_INCIDENT","value":"tenant_disclosure"},
  {"code":"KNOWLEDGE_VERSION_DRIFT","traces":["T004"]}
]
Diagnosis
- T003 / INC01: Two retrieval attempts timed out. The trace shows tool-level failure rather than a model-generation failure. The owner should inspect the retrieval dependency, stop unbounded retries and verify fallback behavior.
- T002 / INC02: The action stopped as STOP_STALE after revalidation. This is a safe controlled result and has no receipt. The operator should not retry the old commit; create a new preview if the user still wants the change.
- T004 / INC04: The trace used policy v2 while the current version is v3. The answer succeeded technically but failed quality. Pin the current source and rerun version and citation tests.
- T005 / INC03: The security boundary failed. This is the highest-severity condition. Contain the affected data path, preserve trace evidence, inspect authorization and tool-contract versions and run cross-tenant security cases before reopening.
The key lesson is that one monitoring window can contain a safe stop, a dependency failure, a knowledge regression and a security incident. Treating every event as “the model was wrong” would misdirect recovery.
5. Try it yourself — guided practice
Goal
Build the monitoring view, identify all alerts and use the runbook to assign diagnosis and verification steps.
Complete trace metadata
Use trace_metadata.jsonl:
{"trace_id":"T001","session_id":"S001","tenant_id":"NST-TENANT-001","actor_id":"NST-USER-001","started_ms":1000,"end_to_end_ms":680,"outcome":"SUCCESS","prompt_version":"p18.2","model_id":"hybrid_v2","tool_contract_version":"tc14.1","knowledge_version":"NST-POLICY-001:v3","quality_sampled":true,"quality_pass":true,"action_safety_pass":true,"security_pass":true,"incident_id":null,"error_code":null,"tenant_disclosure":false}
{"trace_id":"T002","session_id":"S002","tenant_id":"NST-TENANT-001","actor_id":"NST-USER-001","started_ms":2000,"end_to_end_ms":1500,"outcome":"STOP_STALE","prompt_version":"p18.2","model_id":"hybrid_v2","tool_contract_version":"tc14.1","knowledge_version":"NST-POLICY-001:v3","quality_sampled":true,"quality_pass":true,"action_safety_pass":true,"security_pass":true,"incident_id":"INC02","error_code":"STOP_STALE","tenant_disclosure":false}
{"trace_id":"T003","session_id":"S003","tenant_id":"NST-TENANT-001","actor_id":"NST-USER-001","started_ms":3000,"end_to_end_ms":3200,"outcome":"FAILED","prompt_version":"p18.2","model_id":"hybrid_v2","tool_contract_version":"tc14.1","knowledge_version":"NST-POLICY-001:v3","quality_sampled":true,"quality_pass":false,"action_safety_pass":true,"security_pass":true,"incident_id":"INC01","error_code":"TOOL_TIMEOUT","tenant_disclosure":false}
{"trace_id":"T004","session_id":"S004","tenant_id":"NST-TENANT-001","actor_id":"NST-USER-001","started_ms":4000,"end_to_end_ms":950,"outcome":"SUCCESS","prompt_version":"p18.2","model_id":"hybrid_v2","tool_contract_version":"tc14.1","knowledge_version":"NST-POLICY-001:v2","quality_sampled":true,"quality_pass":false,"action_safety_pass":true,"security_pass":true,"incident_id":"INC04","error_code":"KNOWLEDGE_VERSION_DRIFT","tenant_disclosure":false}
{"trace_id":"T005","session_id":"S005","tenant_id":"NST-TENANT-001","actor_id":"NST-USER-003","started_ms":5000,"end_to_end_ms":850,"outcome":"SECURITY_INCIDENT","prompt_version":"p18.1","model_id":"hybrid_v2","tool_contract_version":"tc13.9","knowledge_version":"NST-POLICY-001:v3","quality_sampled":true,"quality_pass":false,"action_safety_pass":false,"security_pass":false,"incident_id":"INC03","error_code":"TENANT_BOUNDARY_BREACH","tenant_disclosure":true}
The complete trace_spans.csv file contains request, model, retrieval, authorization, approval, action and response spans for these traces. The runbook is:
{
  "runbook_id": "NST-RUNBOOK-001",
  "version": "0.1",
  "steps": [
    {"stage":"detect","required_fields":["incident_id","trace_id","alert","time"]},
    {"stage":"contain","required_fields":["owner","containment","scope"]},
    {"stage":"diagnose","required_fields":["prompt_version","model_id","tool_contract_version","knowledge_version","error_code"]},
    {"stage":"recover","required_fields":["rollback_or_fix","approval"]},
    {"stage":"verify","required_fields":["regression_cases","security_cases","quality_check"]},
    {"stage":"close","required_fields":["root_cause","impact","owner","follow_up"]}
  ]
}
Steps
1. Compile the monitoring tools:
python3 -B -m py_compile build_monitoring_view.py check_incident_runbook.py
2. Build the monitoring view:
python3 -B build_monitoring_view.py \
  --metadata trace_metadata.jsonl \
  --spans trace_spans.csv \
  --thresholds monitor_thresholds.json \
  --out monitoring_view.json
3. Check the incident runbook:
python3 -B check_incident_runbook.py \
  --cases incident_cases.jsonl \
  --runbook incident_runbook.json \
  --monitoring monitoring_view.json \
  --out incident_runbook_results.json
4. List all five alert codes.
5. For each incident, write the trace ID, affected component, version comparison, containment action and verification test.
Expected result
The monitoring view contains five traces and five alerts:
P95_LATENCY_HIGH
ERROR_RATE_HIGH
QUALITY_REGRESSION
SECURITY_INCIDENT
KNOWLEDGE_VERSION_DRIFT
The runbook checker reports four incident cases, six required stages and PASS. Model and provider execution remain not_run.
6. Independent challenge
Use observability_challenge.jsonl:
{"case_id":"CH01","kind":"version_drift","trace_id":"T006","symptom":"A response cites policy v2 after the current manifest moved to v3.","expected_alert":"KNOWLEDGE_VERSION_DRIFT","required_evidence":["trace_id","knowledge_version","current_version","prompt_version","model_id"]}
{"case_id":"CH02","kind":"latency_spike","trace_id":"T007","symptom":"P95 latency rises above the interactive threshold while tool retries increase.","expected_alert":"P95_LATENCY_HIGH","required_evidence":["trace_id","tool_name","error_code","attempt","duration_ms"]}
For each challenge, produce:
1. a trace metadata record;
2. at least two correlated spans;
3. the alert condition and denominator;
4. a containment step that preserves evidence;
5. a diagnosis hypothesis; and
6. a verification test and closure condition.
Then decide whether CH01 is primarily a quality incident, a reliability incident or both. For CH02, distinguish a single slow request from a systemic latency alert. A successful challenge includes enough version and span evidence that another engineer can reproduce the diagnosis without reading the full user conversation.
7. Common problems and recovery
Symptom	Diagnosis	Recovery	Verification
Traces cannot be joined to tool calls	Correlation IDs were generated independently	Propagate trace and parent span IDs through each adapter	One trace shows the complete request path
A regression cannot be reproduced	Prompt, model or knowledge version was omitted	Record all behavior-affecting versions	A trace can be compared with a known-good trace
Error rate looks low despite many failed retries	Denominator counts attempts or only final successes incorrectly	Define logical-request and attempt metrics separately	Retry and unfinished counts are reported
P95 latency is normal but users report slowness	Queue time, abandoned requests or a small affected segment was excluded	Measure end-to-end latency and segment by route/tenant	User-facing population is represented
Quality sampling stores full private prompts	Sampling copied sensitive content unnecessarily	Store labels, source IDs and hashes or references	Review data contains no unnecessary secrets or PII
Every STOP_STALE raises a critical outage alert	Safe controls were confused with incidents	Alert on abnormal rates or security impact	Normal stops are measured separately
A security alert has no containment owner	Alert contains a code but not an operational route	Add severity, owner, containment and runbook link	Incident case has accountable owner
Logs are edited after an incident	Evidence was not protected	Restrict access, append corrections and preserve originals	Trace history remains auditable
Recovery is declared after a rollback only	No regression or security verification ran	Execute the relevant test suite before reopening	Runbook has verification evidence
8. Check your understanding
 1. Why should a trace record prompt, model, tool-contract and knowledge versions?
 2. What is the difference between a trace and a span?
 3. Why should STOP_STALE not automatically count as an application failure?
 4. How can a technically successful response still create a quality alert?
 5. What denominator is used for tool failure rate?
 6. Why should quality sampling avoid copying complete private conversations?
 7. Name three fields an alert needs before an operator can act on it.
 8. What does T003 tell you that a final “service unavailable” message does not?
 9. Why is tenant disclosure a higher-severity signal than an ordinary timeout?
10. What must happen before an incident is closed?
9. Solutions and explanations
 1. These versions identify the behavior and dependencies that produced the result. Without them, an engineer cannot tell whether a regression came from a prompt, model, tool schema, source version or application release.
 2. A trace correlates one logical request or interaction. A span is one operation inside that trace, such as retrieval, model generation or authorization. Spans expose timing and failure boundaries.
 3. STOP_STALE is a deliberate fail-closed action outcome. It may indicate normal concurrent-record behavior. It becomes an operational concern if its rate changes sharply, but one safe stop is not equivalent to a crash or unsafe write.
 4. The system can return a response using an outdated policy, unsupported citation or unsafe structured action while the HTTP and model calls both succeed. Quality and action checks therefore belong in monitoring.
 5. tool_failure_rate = failed_tool_spans / total_tool_spans. Count the tool span population, not all user requests, when measuring this signal.
 6. Full conversations may contain secrets, personal data and business-sensitive context. Store the minimum evidence needed to score and diagnose, such as trace ID, source version, labels and controlled references.
 7. An alert needs a signal, denominator/time window, threshold, severity, owner and trace correlation. A runbook link or containment instruction makes it actionable.
 8. T003 shows that retrieval timed out twice, which component failed, how long the trace took and which incident owns it. That evidence distinguishes a dependency timeout from model-generation or policy logic failure.
 9. A tenant disclosure can expose protected customer data and indicates a boundary failure. A timeout usually affects availability without necessarily exposing data. Both matter, but their containment and severity differ.
10. The owner must document impact and root cause, restore or fix the affected path, run relevant regression and security checks, record evidence and assign follow-up work. A rollback alone is not proof of recovery.
The guided fixture’s alert and incident mapping is:
Alert	Evidence	Incident or response
P95_LATENCY_HIGH	T003 has 3200 ms end-to-end time	INC01 retrieval timeout diagnosis
ERROR_RATE_HIGH	2 of 5 traces are failed/incident	Inspect T003 and T005 separately
QUALITY_REGRESSION	2 of 5 quality samples pass	INC04 version drift and INC03 security failure
SECURITY_INCIDENT	T005 has tenant disclosure	INC03 immediate containment
KNOWLEDGE_VERSION_DRIFT	T004 uses policy v2 instead of v3	INC04 pin and verify source version
The runbook must keep INC02 distinct: its stale stop has no receipt and is a controlled action result. The operator should create a new preview rather than retrying the old commit.
10. Chapter recap and next step
Reliable AI systems leave evidence across the full path:
trace request → preserve versions → record spans and outcomes
→ measure quality and reliability → alert with thresholds
→ contain and diagnose → verify recovery → close with evidence
You should now be able to say:
- I can correlate model, retrieval, tool and action events in one trace.
- I can record the versions needed to reproduce a behavior.
- I can calculate latency, failure, quality and tool-error rates with denominators.
- I can monitor quality and security without copying unnecessary private content.
- I can distinguish expected safety stops from operational incidents.
- I can create alerts with owners, thresholds and trace evidence.
- I can use a runbook to contain, diagnose, recover, verify and close an incident.
The Northstar project artifact is a monitoring view over versioned trace metadata and spans, five alert conditions, four incident cases and a six-stage runbook. Chapter 20, User Experience and Release, will connect reliability evidence to citations, uncertainty, action previews, pilot acceptance, configuration promotion, fallbacks and release walkthroughs.
11. Glossary and further reading
Glossary
- Alert: A threshold or rule indicating that an operator should investigate or act.
- Incident: An event requiring containment, diagnosis, recovery or formal follow-up.
- Observability: Evidence that allows a system’s internal behavior to be understood from its outputs, traces and measurements.
- P95 latency: A tail-latency value below which approximately 95% of measured observations fall.
- Quality sampling: Reviewing a selected subset of outputs against grounding, completeness or action criteria.
- Reliability: The ability to provide acceptable outcomes or safe, explainable degradation under normal and failure conditions.
- Runbook: A structured set of detection, containment, diagnosis, recovery, verification and closure steps.
- Span: A timed operation within a trace.
- Trace: A correlated record of one logical request or interaction across system components.
- Version drift: A trace using a prompt, model, tool or knowledge version different from the approved current version.
Further reading
- OpenAI Prompt Caching — Observability and usage (https://developers.openai.com/api/docs/guides/prompt-caching) — cached-token usage, latency and cache monitoring fields.
- OpenAI Agents API observability (https://developers.openai.com/api/docs/guides/agents-api/observability) — provider-specific observability concepts; verify current availability and fields for the deployment.
- OpenAI Rate Limits (https://developers.openai.com/api/docs/guides/rate-limits) — limits and capacity considerations for retries and concurrency.
- NIST AI Risk Management Framework (https://www.nist.gov/itl/ai-risk-management-framework) — risk management practices relevant to monitoring and trustworthy operation.
- Northstar Chapter 16 — Prompt Injection and Data Protection (C03_CH16_Prompt_Injection_and_Data_Protection_Student.md) — sensitive logging, application boundaries and security controls.
- Northstar Chapter 18 — Cost, Latency and Efficiency (C03_CH18_Cost_Latency_and_Efficiency_Student.md) — the efficiency events and metrics consumed by this chapter.
