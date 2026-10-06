# Multi-Agent Design

C03-CH13 — Multi-Agent Systems
What you will learn
By the end of this chapter, you will be able to:
 1. Explain when a multi-agent system is useful and when a single agent or workflow is better.
 2. Distinguish workflows, agents, supervisors, specialists, handoffs and agent-as-tool patterns.
 3. Decompose a business task into bounded specialist responsibilities.
 4. Design structured handoff contracts between agents.
 5. Control context, tools, scopes and permissions for each specialist.
 6. Combine sequential, parallel and evaluator-review patterns.
 7. Add stopping conditions, retries, escalation and human approval.
 8. Evaluate multi-agent quality using evidence, policy, cost and latency metrics.
 9. Design a Northstar renewal-research system that uses the read-only MCP boundary from C03-CH12.
10. Keep multi-agent coordination separate from direct CRM writes and outbound messaging.
Accuracy note: complexity is a design choice
A multi-agent system is not automatically better than a single agent.
Current guidance from Anthropic distinguishes:
- Workflows: predefined code paths that coordinate language-model calls and tools.
- Agents: systems where the model dynamically directs its own process and tool usage.
Anthropic recommends starting with the simplest system that can satisfy the task, then adding complexity when evaluation shows a meaningful benefit.
Current OpenAI Agents SDK guidance describes two common delegation patterns:
- Agents as tools: a manager keeps control of the conversation and calls specialists for bounded subtasks.
- Handoffs: a triage agent transfers control to a specialist, which becomes the active agent.
These are implementation patterns. They do not replace application-level authorization, data access rules, approval gates or audit controls.
Lesson 1 — Why use more than one agent?
1.1 Start with a simpler baseline
Before designing multiple agents, establish the simplest workable baseline.
A task might begin as:
User request
    |
    v
One model call
    |
    v
One grounded answer
Then add tools or retrieval only when required:
User request
    |
    v
One agent
    |
    +--> CRM read tool
    +--> Document resource
    |
    v
Grounded answer
This design may be enough when:
- The task has one clear objective.
- The available data is small.
- One tool policy is sufficient.
- A single output format is needed.
- There are no independent specialist concerns.
- The same agent can safely see all required context.
A multi-agent design becomes more attractive when:
- Different subtasks require different expertise.
- Each specialist should see only part of the data.
- The task has independent research branches.
- A reviewer must check another agent’s work.
- Routing depends on the request type.
- A single agent repeatedly confuses similar tools.
- Different subtasks have different risk levels or permissions.
1.2 The cost of adding agents
Each additional agent can introduce:
- More model calls.
- More latency.
- More token usage.
- More intermediate state.
- More failure modes.
- More ambiguous ownership.
- More opportunities for unsupported claims.
- More difficult debugging.
- More complex authorization.
A useful design question is:
What measurable problem does this additional agent solve?
Weak answer:
“The system should feel more autonomous.”
Stronger answers:
“A separate evidence reviewer reduces unsupported claims from 18% to below 5% on the held-out evaluation.”
“A CRM specialist has access to customer tools, while the writer sees only a redacted evidence packet.”
“Two independent research branches reduce missed-source errors without granting either branch write access.”
1.3 Common orchestration patterns
Pattern	Shape	Best use
Sequential chain	A → B → C	Fixed, dependent stages
Routing	Classifier → one specialist	Distinct task categories
Parallel sectioning	A → B and C in parallel → join	Independent subtasks
Parallel voting	Several agents answer → aggregate	Confidence through independent attempts
Orchestrator-workers	Supervisor → dynamically chosen workers → synthesis	Variable decomposition
Evaluator-optimizer	Draft → reviewer → revise	Clear quality criteria
Handoff	Triage → specialist takes over	A specialist should own the next conversation stage
Agents as tools	Manager → specialist result → manager remains owner	Manager should preserve final-answer control
Anthropic’s published guidance covers prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer and autonomous agents as composable patterns.
1.4 Workflow versus agent
A workflow has a known shape:
1. Identify customer.
2. Retrieve approved sources.
3. Build evidence packet.
4. Draft brief.
5. Review citations.
6. Return draft.
An agent has more freedom:
1. Decide what to investigate.
2. Choose tools.
3. Decide whether more research is needed.
4. Recover from errors.
5. Stop when it believes the task is complete.
For a Northstar renewal brief, the known sequence makes a code-controlled workflow a strong first design.
The language model can still perform flexible subtasks inside the workflow:
- Interpret the user’s request.
- Extract the customer identifier.
- Summarize evidence.
- Draft prose.
- Explain missing data.
The overall path remains controlled by application code.
Checkpoint 1
Answer these questions:
1. Why should a team establish a simple baseline before adding agents?
2. Which pattern is a good fit for two independent research branches?
3. Which pattern is a good fit when a reviewer should critique and improve a draft?
4. Does adding agents automatically improve accuracy?
Answers
1. A baseline shows whether additional complexity solves a real problem.
2. Parallel sectioning.
3. Evaluator-optimizer.
4. No. Additional agents can improve specialization or review, but they also add latency, cost and failure modes.
Lesson 2 — Agent roles and delegation patterns
2.1 A specialist has a narrow contract
A specialist agent should have:
- One primary responsibility.
- A small tool set.
- A defined input schema.
- A defined output schema.
- Clear completion criteria.
- Clear refusal and escalation behavior.
- No unnecessary access to other specialists’ context.
Example:
CRM Research Agent

Purpose:
  Retrieve authorized customer and deal facts.

May:
  Search contacts.
  Read customer snapshots.
  Read open-deal summaries.

Must not:
  Change CRM records.
  Send messages.
  Read held-out evaluations.
  Draft unsupported commercial claims.
This is stronger than:
You are a smart sales agent. Do whatever is needed.
2.2 Manager and specialist
In a manager pattern:
flowchart LR
    U[User] --> M[Manager agent]

    M -->|bounded subtask| C[CRM specialist]
    M -->|bounded subtask| K[Knowledge specialist]
    M -->|bounded subtask| R[Review specialist]

    C --> M
    K --> M
    R --> M

    M --> O[Final response]
The manager remains responsible for:
- Interpreting the user request.
- Choosing specialists.
- Combining results.
- Deciding whether the task is complete.
- Producing the final answer.
- Escalating when a policy gate fails.
The specialists return subtask results rather than taking over the entire conversation.
This resembles the “agents as tools” pattern.
2.3 Handoff
In a handoff pattern:
flowchart LR
    U[User] --> T[Triage agent]
    T -->|handoff| S[Specialist agent]
    S --> O[Specialist response]
The specialist becomes the active owner of the next stage.
A handoff is appropriate when:
- The specialist should speak directly to the user.
- The triage agent should stop making decisions.
- The next conversation needs different instructions.
- The active agent should own follow-up questions.
A handoff should still carry structured information:
{
  "destination": "crm_specialist",
  "reason": "customer_record_lookup",
  "customer_identifier": "contact@example.com",
  "allowed_scope": "crm:read",
  "writes_enabled": false
}
The receiving agent should not infer critical permissions from prose alone.
2.4 Manager versus handoff
Question	Manager with agents as tools	Handoff
Who owns the final response?	Manager	Receiving specialist
Are specialists bounded subtask providers?	Usually	Not necessarily
Does control remain with the original agent?	Yes	No
Good for	Synthesis, shared policy, multiple outputs	Routing, specialist-led conversations
Main risk	Manager may miscombine results	Specialist may receive excessive history or permissions
2.5 Context passed between agents
Do not automatically pass the entire conversation to every agent.
Possible context strategies:
1. Full history.
2. A compact summary.
3. A structured task object.
4. A filtered evidence packet.
5. A redacted subset.
6. A reference to shared state that the receiving agent is authorized to read.
For Northstar, prefer a structured handoff:
{
  "task_id": "NST-TASK-001",
  "tenant": "northstar-demo",
  "customer_id": "NST-CUST-001",
  "user_goal": "Prepare a renewal research brief",
  "required_output": "draft_with_citations",
  "allowed_sources": [
    "NST-PROD-001:v1.2",
    "NST-POLICY-001:v3.0"
  ],
  "excluded_sources": [
    "NST-POLICY-001:v2.0",
    "NST-EVAL-001"
  ],
  "writes_enabled": false,
  "messages_enabled": false
}
The document specialist does not need the user’s private conversational history. The writer does not need raw CRM credentials. The reviewer does not need a CRM tool.
2.6 Handoff contracts
A handoff contract should answer:
- Who is sending the work?
- Who is receiving the work?
- What task is being delegated?
- What facts are already verified?
- What remains unknown?
- Which tools may be used?
- Which sources are allowed?
- What output schema is required?
- What should happen if the task cannot be completed?
- What correlation ID links the work to the parent run?
Example:
handoff_id: NST-HANDOFF-001
parent_task_id: NST-TASK-001
from_agent: NST-MA-SUPERVISOR-001
to_agent: NST-MA-CRM-001
purpose: retrieve_authorized_customer_facts
input:
  customer_lookup:
    email: contact@example.com
  tenant: northstar-demo
  requested_fields:
    - customer_id
    - account_name
    - active_status
    - open_deal_summary
permissions:
  scopes:
    - crm:read
  writes_enabled: false
  messages_enabled: false
output_contract:
  required:
    - match_count
    - customer_id
    - source_ids
    - missing_fields
  forbidden:
    - unsupported_recommendation
    - CRM mutation
    - outbound message
stop_conditions:
  - multiple_exact_matches
  - no_authorized_match
  - tool_permission_denied
  - timeout_after_retry_budget
Checkpoint 2
1. What should a specialist’s tool set look like?
2. Why might a document writer not need CRM credentials?
3. What is the key difference between a manager pattern and a handoff?
4. Why use a structured handoff instead of passing only natural-language instructions?
Answers
1. Small and purpose-specific.
2. The writer can work from a filtered evidence packet, reducing unnecessary access.
3. In a manager pattern, the manager retains control; in a handoff, the receiving specialist becomes the active owner.
4. A schema makes permissions, required fields, exclusions, stopping conditions and output requirements explicit and testable.
Lesson 3 — The Northstar multi-agent design
3.1 Business task
Northstar wants a renewal research brief.
The request is:
“Find the customer associated with contact@example.com, read the current approved product and policy sources, prepare a renewal brief, and identify missing facts. Do not change CRM and do not send a message.”
This task contains several distinct responsibilities:
1. Validate the request.
2. Identify the customer.
3. Read authorized CRM facts.
4. Read approved documents.
5. Assemble evidence.
6. Draft the brief.
7. Review citations and policy compliance.
8. Return the draft to the user.
3.2 Proposed agents
Agent	Identifier	Responsibility
Supervisor	NST-MA-SUPERVISOR-001	Own the workflow and final response
CRM researcher	NST-MA-CRM-001	Retrieve authorized CRM facts
Knowledge researcher	NST-MA-KNOWLEDGE-001	Retrieve approved product and policy evidence
Evidence assembler	NST-MA-EVIDENCE-001	Normalize and combine evidence
Draft writer	NST-MA-DRAFT-001	Produce a cited draft
Evidence reviewer	NST-MA-REVIEW-001	Check evidence coverage and unsupported claims
These are synthetic Northstar identifiers.
3.3 Agent permissions
Agent	CRM tools	Document resources	Writes
Supervisor	No direct CRM tools	No direct raw documents	No
CRM researcher	Read-only CRM tools	No	No
Knowledge researcher	No CRM tools	Approved current resources	No
Evidence assembler	No	Receives filtered evidence	No
Draft writer	No	Receives evidence packet	No
Evidence reviewer	No	Receives draft and evidence packet	No
The supervisor may invoke specialist agents, but it should not bypass their access boundaries by attaching every tool directly to itself.
3.4 Tool assignment
The CRM researcher may use:
crm.search_contacts
crm.get_customer_snapshot
crm.list_open_deals
crm.get_related_activity_summary
The knowledge researcher may read:
northstar://product/NST-PROD-001:v1.2
northstar://policy/NST-POLICY-001:v3.0
northstar://knowledge/NST-KNOWLEDGE-001
No agent may access:
northstar://policy/NST-POLICY-001:v2.0
northstar://evaluation/NST-EVAL-001
crm.update_customer
crm.delete_record
messages.send
3.5 Workflow shape
Because the stages are known, use code-controlled orchestration:
flowchart TD
    A[Receive request] --> B[Validate task and permissions]
    B --> C[CRM research]
    B --> D[Knowledge research]

    C --> E[Evidence join]
    D --> E

    E --> F[Draft writer]
    F --> G[Evidence reviewer]

    G -->|pass| H[Supervisor prepares user response]
    G -->|repairable issue| F
    G -->|missing evidence or policy issue| I[Escalate to user]
CRM and knowledge research can run in parallel because they are independent.
The join must wait for both branches.
3.6 Why not let the supervisor do everything?
A single supervisor with every tool could be simpler to build, but it would have more responsibilities:
- Customer lookup.
- Document selection.
- Writing.
- Evidence checking.
- Tool permissions.
- Policy enforcement.
- Final response.
That broad surface increases the chance that the supervisor:
- Selects an archived source.
- Uses a write tool accidentally.
- Mixes customer facts with unsupported inferences.
- Hides a failed research branch.
- Treats a draft as an executed action.
Specialists do not guarantee correctness, but they make access and responsibility easier to inspect.
Lesson 4 — State, joins and stopping conditions
4.1 State machine
A multi-agent system needs explicit state.
RECEIVED
   |
   v
VALIDATED
   |
   +--> CRM_RESEARCH_RUNNING
   |
   +--> KNOWLEDGE_RESEARCH_RUNNING
   |
   v
EVIDENCE_JOINED
   |
   v
DRAFTED
   |
   v
REVIEWED
   |
   +--> READY_FOR_USER
   |
   +--> REPAIR_REQUIRED
   |
   +--> ESCALATION_REQUIRED
A state transition should be caused by an observable result, not by a vague model statement such as:
“I think this is complete.”
4.2 Parallel branches
Parallel work is safe only when the branches are independent.
Good parallel branches:
CRM researcher:
  retrieve customer facts

Knowledge researcher:
  retrieve approved product and policy evidence
Poor parallel branches:
Two agents both update the same CRM record.
Two agents both send messages.
Two agents both change the same workflow state.
Parallel branches need:
- Separate ownership.
- Separate identifiers.
- A join condition.
- A timeout.
- A failure policy.
- A conflict policy.
4.3 Join contract
The evidence join can require:
join_id: NST-JOIN-001
required_branches:
  - crm_research
  - knowledge_research
success_conditions:
  - crm_research.status == "complete"
  - knowledge_research.status == "complete"
  - each branch has source_ids
  - each branch has missing_fields
failure_conditions:
  - branch_timeout
  - unauthorized_access
  - source_version_conflict
  - malformed_output
join_behavior:
  - create_evidence_packet
  - preserve_branch_status
  - mark_missing_evidence
If the CRM branch fails but the document branch succeeds, the workflow should not silently present a complete customer brief.
4.4 Retry budgets
Each agent should have a bounded retry policy.
Example:
retry_policy:
  transient_timeout:
    max_attempts: 2
    backoff: exponential
  invalid_arguments:
    max_attempts: 1
    action: repair_arguments
  permission_denied:
    max_attempts: 0
    action: escalate
  no_match:
    max_attempts: 0
    action: report_no_match
A retry is appropriate for a transient network timeout.
A retry is usually not appropriate for:
- Permission denial.
- A missing source.
- A held-out record.
- A policy prohibition.
- A request to use a forbidden tool.
4.5 Stopping conditions
Stop when:
- Required branches complete.
- The reviewer passes.
- The user must approve the next action.
- The task cannot be completed with available evidence.
- The retry budget is exhausted.
- A permission boundary is reached.
- A maximum-turn limit is reached.
- A conflicting source requires human resolution.
Without stopping conditions, agents may continue searching and increase:
- Cost.
- Latency.
- API-credit consumption.
- Data exposure.
- Chance of irrelevant evidence.
4.6 Explicit state handles
MCP itself does not make a multi-agent workflow stateful. The application must manage state.
A state record may include:
task_id: NST-TASK-001
run_id: NST-RUN-001
state: EVIDENCE_JOINED
tenant: northstar-demo
customer_id: NST-CUST-001
branch_status:
  crm_research: complete
  knowledge_research: complete
evidence_packet_id: NST-EVIDENCE-001
draft_id: NST-DRAFT-001
review_id: null
writes_enabled: false
messages_enabled: false
If state is stored outside the current request:
- Use opaque identifiers.
- Bind state to the authenticated principal.
- Validate ownership on every access.
- Set expiration where appropriate.
- Never treat possession of a state ID as authentication.
Checkpoint 3
1. Why is a join needed after parallel research?
2. Name one situation where retrying is inappropriate.
3. What should happen when one research branch fails?
4. Who should own workflow state?
Answers
1. The join verifies that required branches completed and combines their results in a controlled way.
2. Permission denial, held-out data, an archived source or a policy prohibition.
3. Preserve the branch failure, mark the result incomplete and either repair or escalate.
4. The application or orchestration layer should own workflow state, with authorization checks on every access.
Lesson 5 — Evidence contracts between agents
5.1 Do not pass unsupported prose as state
This is weak:
The CRM agent says the customer is ready to renew and the product is a good fit.
It does not identify:
- Which source supports the claim.
- Whether the claim is a fact or inference.
- Which customer it describes.
- Whether it is current.
- Whether the result was observed or simulated.
Use a structured evidence item instead.
5.2 Evidence-item schema
{
  "evidence_id": "NST-EVID-001",
  "task_id": "NST-TASK-001",
  "claim": "The matched customer is Acme Manufacturing.",
  "claim_type": "observed_fact",
  "value": "Acme Manufacturing",
  "source": {
    "source_id": "NST-CUST-001",
    "source_uri": "crm://customer/NST-CUST-001",
    "source_version": "current",
    "status": "authorized"
  },
  "retrieval": {
    "agent_id": "NST-MA-CRM-001",
    "retrieval_status": "simulated_fixture",
    "retrieved_at": "2026-10-06T00:00:00Z"
  },
  "allowed_use": "customer_research",
  "confidence": "high"
}
5.3 Claim types
Use different labels for different kinds of statements:
Claim type	Meaning	Example
observed_fact	Returned by an authorized source	Customer status is active
documented_fact	Stated in an approved document	Policy requires approval
derived_value	Calculated from supplied facts	Renewal window is 30 days
inference	Reasoned interpretation	Customer may need follow-up
recommendation	Proposed next step	Ask the account owner
unknown	Not present or not verified	Renewal amount unavailable
Do not convert an inference into an observed fact during handoff.
5.4 Evidence packet
evidence_packet_id: NST-EVIDENCE-PACKET-001
task_id: NST-TASK-001
customer_id: NST-CUST-001
items:
  - evidence_id: NST-EVID-001
    claim_type: observed_fact
    claim: "The exact email matched one active customer."
    value: "NST-CUST-001"
    source_id: NST-CUST-001
    source_status: authorized
    observed_status: simulated_fixture

  - evidence_id: NST-EVID-002
    claim_type: documented_fact
    claim: "The product reference is Northstar Analytics v1.2."
    value: "NST-PROD-001:v1.2"
    source_id: NST-PROD-001:v1.2
    source_status: approved
    observed_status: simulated_fixture

  - evidence_id: NST-EVID-003
    claim_type: documented_fact
    claim: "The current policy source is approved."
    value: "NST-POLICY-001:v3.0"
    source_id: NST-POLICY-001:v3.0
    source_status: approved
    observed_status: simulated_fixture

missing:
  - renewal_amount
  - confirmed_decision_maker
excluded:
  - NST-POLICY-001:v2.0
  - NST-EVAL-001
5.5 Evidence reviewer
The reviewer checks:
- Every factual claim has a source.
- Every source is allowed.
- Archived sources are excluded.
- Held-out sources are excluded.
- Inferences are labeled.
- Missing fields are preserved.
- No write or message was executed.
- The draft does not claim live execution.
- The customer identity is consistent.
- Citations point to the evidence packet.
A reviewer should return structured results:
{
  "review_id": "NST-REVIEW-001",
  "status": "needs_repair",
  "checks": [
    {
      "name": "source_coverage",
      "status": "pass"
    },
    {
      "name": "archived_source_exclusion",
      "status": "pass"
    },
    {
      "name": "unsupported_renewal_claim",
      "status": "fail",
      "detail": "The draft says the renewal is likely to close, but no source supports that inference."
    }
  ],
  "required_repairs": [
    "Remove or label the unsupported renewal prediction."
  ]
}
Lesson 6 — Guardrails, permissions and observability
6.1 Guardrails operate at different boundaries
Agent systems often have checks at several layers:
User input guardrail
    |
    v
Supervisor
    |
    +--> Handoff guardrail
    |
    +--> Specialist tool-input guardrail
    |
    +--> Specialist tool-output guardrail
    |
    v
Draft writer
    |
    v
Final output guardrail
A check attached only to the first agent may not protect every later specialist or tool call.
Current OpenAI Agents SDK guidance distinguishes:
- Input guardrails.
- Output guardrails.
- Tool guardrails.
The exact implementation depends on the framework, but the architectural lesson is general:
Put a check at the boundary where the risk occurs.
Examples:
- Validate the user request before expensive execution.
- Validate CRM tool arguments immediately before the CRM call.
- Validate tool output before passing it to another agent.
- Validate the final answer before returning it to the user.
6.2 Permission by agent
Use least privilege.
agents:
  - agent_id: NST-MA-CRM-001
    scopes:
      - crm:read
    tools:
      - crm.search_contacts
      - crm.get_customer_snapshot
    writes_enabled: false

  - agent_id: NST-MA-KNOWLEDGE-001
    scopes:
      - documents:read
    resources:
      - northstar://product/NST-PROD-001:v1.2
      - northstar://policy/NST-POLICY-001:v3.0
    writes_enabled: false

  - agent_id: NST-MA-DRAFT-001
    scopes: []
    tools: []
    resources: []
    input: NST-EVIDENCE-PACKET-001
The draft writer cannot call the CRM merely because another agent could.
6.3 Human approval
The Northstar workflow ends with a draft.
If a future process wants to:
- Update a CRM record.
- Create a task.
- Send an email.
- Change ownership.
- Close a deal.
Then it must introduce a new boundary:
Draft proposal
    |
    v
Human approval
    |
    v
Revalidate current record
    |
    v
Execute permitted write
    |
    v
Audit result
The multi-agent system should not bypass this boundary by allowing the supervisor to hand a draft directly to a write-capable agent.
6.4 Tracing
A useful trace records:
- One parent run.
- Agent spans.
- Handoff spans.
- Tool-call spans.
- Guardrail results.
- Retry attempts.
- Join status.
- Final review status.
Example:
Trace: NST-TRACE-001
  Supervisor run
    Handoff: CRM researcher
      Tool: crm.search_contacts
      Tool: crm.get_customer_snapshot
    Handoff: Knowledge researcher
      Resource: NST-PROD-001:v1.2
      Resource: NST-POLICY-001:v3.0
    Evidence join
    Draft writer
    Evidence reviewer
    Final response
Trace data may contain sensitive information. Apply:
- Redaction.
- Access controls.
- Retention limits.
- Safe correlation IDs.
- Exclusion of tokens and secrets.
- PII minimization.
OpenAI Agents SDK documentation describes traces and spans for generations, tool calls, handoffs, guardrails and custom events. The same concepts can be implemented with another observability system.
6.5 Metrics
Track more than “the agent answered.”
Metric	Definition
Task completion	Percentage of tasks reaching an acceptable final state
Evidence coverage	Percentage of factual claims linked to allowed sources
Unsupported claim rate	Claims lacking adequate evidence
Tool selection accuracy	Percentage of calls using the correct tool
Handoff validity	Percentage of handoffs passing schema and policy checks
Reviewer pass rate	Drafts passing on the first review
Repair rate	Drafts requiring revision
Escalation rate	Tasks requiring a human or user decision
Latency	End-to-end elapsed time
Model cost	Tokens or model-call cost
CRM credit estimate	Expected upstream CRM consumption
Write-block rate	Attempts to invoke unavailable write tools
Data exposure	Amount of context passed to each specialist
6.6 Evaluation fixtures
Use synthetic tests that include:
- Exact single match.
- No match.
- Multiple matches.
- Archived policy conflict.
- Held-out evaluation request.
- CRM permission denial.
- Document read timeout.
- Unsupported renewal amount.
- Prompt injection inside a document.
- Tool schema error.
- Reviewer rejection.
- User requests a write.
A multi-agent system should be evaluated at:
1. Individual agent level.
2. Handoff level.
3. Join level.
4. End-to-end workflow level.
5. Human escalation level.
Checkpoint 4
1. Why is an evidence packet preferable to an unstructured summary?
2. Where should CRM tool-input validation occur?
3. What should a trace connect?
4. Name two metrics beyond final-answer quality.
Answers
1. It preserves source, claim type, status, missing fields and authorization information.
2. Immediately before the CRM call, in addition to earlier request validation.
3. The parent run, agent steps, handoffs, tools, guardrails, retries, joins and final review.
4. Examples include evidence coverage, unsupported claim rate, latency, CRM-credit estimate, repair rate and escalation rate.
Worked case — Renewal Research Team
User request
Find the customer associated with contact@example.com.
Prepare a renewal research brief using only current approved product and policy sources.
Do not update CRM and do not send a message.
Synthetic run identifiers
Task: NST-TASK-001
Run: NST-RUN-001
Supervisor: NST-MA-SUPERVISOR-001
Evidence packet: NST-EVIDENCE-PACKET-001
Draft: NST-DRAFT-001
Review: NST-REVIEW-001
Trace: NST-TRACE-001
Step 1: Supervisor validates the request
The supervisor extracts:
tenant: northstar-demo
customer_lookup:
  email: contact@example.com
requested_output: renewal_research_brief
writes_enabled: false
messages_enabled: false
allowed_sources:
  - NST-PROD-001:v1.2
  - NST-POLICY-001:v3.0
excluded_sources:
  - NST-POLICY-001:v2.0
  - NST-EVAL-001
The supervisor does not attach CRM tools directly.
Step 2: Parallel delegation
sequenceDiagram
    participant S as Supervisor
    participant C as CRM researcher
    participant K as Knowledge researcher
    participant E as Evidence assembler
    participant W as Draft writer
    participant R as Evidence reviewer

    S->>C: Retrieve authorized customer facts
    S->>K: Retrieve approved product and policy evidence

    C-->>E: Customer evidence packet
    K-->>E: Document evidence packet

    E->>W: Structured evidence packet
    W-->>R: Draft with citations

    R-->>S: Pass or repair instructions
    S-->>S: Prepare final user response
Step 3: CRM researcher result
Simulated result:
{
  "agent_id": "NST-MA-CRM-001",
  "status": "complete",
  "customer": {
    "customer_id": "NST-CUST-001",
    "account_name": "Acme Manufacturing",
    "status": "active"
  },
  "sources": [
    "NST-CUST-001"
  ],
  "missing_fields": [
    "renewal_amount",
    "confirmed_decision_maker"
  ],
  "writes_performed": false,
  "messages_sent": false,
  "observed_status": "simulated_fixture"
}
Step 4: Knowledge researcher result
Simulated result:
{
  "agent_id": "NST-MA-KNOWLEDGE-001",
  "status": "complete",
  "sources": [
    {
      "source_id": "NST-PROD-001:v1.2",
      "status": "approved",
      "claim": "Current Northstar product reference is v1.2."
    },
    {
      "source_id": "NST-POLICY-001:v3.0",
      "status": "approved",
      "claim": "Current approved policy source is v3.0."
    }
  ],
  "excluded_sources": [
    {
      "source_id": "NST-POLICY-001:v2.0",
      "reason": "archived"
    },
    {
      "source_id": "NST-EVAL-001",
      "reason": "held_out"
    }
  ],
  "observed_status": "simulated_fixture"
}
Step 5: Evidence join
The evidence assembler rejects this claim:
The customer is highly likely to renew.
Reason:
No supplied source establishes renewal likelihood.
It preserves this claim:
The customer is active and associated with the supplied email.
Reason:
Supported by the simulated CRM result.
Step 6: Draft
## Renewal research draft

### Customer

Acme Manufacturing (`NST-CUST-001`) was matched to the supplied email address.
Source: `NST-CUST-001` — simulated CRM fixture result.

### Approved context

The current product reference is Northstar Analytics v1.2.
Source: `NST-PROD-001:v1.2`.

The current approved policy source is version 3.0.
Source: `NST-POLICY-001:v3.0`.

### Unknowns

The supplied evidence does not include a verified renewal amount or confirmed
decision-maker.

### Exclusions

Archived policy `NST-POLICY-001:v2.0` and held-out evaluation `NST-EVAL-001`
were excluded.

### Action status

This run did not update CRM records and did not send a message.
The results shown here are simulated training fixtures, not observed live account results.
Step 7: Review
{
  "review_id": "NST-REVIEW-001",
  "status": "pass",
  "checks": {
    "all_claims_cited": true,
    "only_approved_sources_used": true,
    "archived_source_excluded": true,
    "held_out_source_excluded": true,
    "missing_fields_preserved": true,
    "writes_performed": false,
    "messages_sent": false,
    "live_execution_claimed": false
  }
}
Step 8: Supervisor response
The supervisor returns the draft and clearly labels:
- The evidence sources.
- The unknown fields.
- The excluded sources.
- The simulated status.
- The absence of CRM writes and messages.
Guided practice — Build an agent contract
Objective
Create a multi-agent design for the Northstar renewal task using the fixture below.
Fixture
item_type,item_id,status,allowed_use
tenant,northstar-demo,active,trusted request context
customer,NST-CUST-001,active,read CRM facts
customer,NST-CUST-002,active,read CRM facts
product,NST-PROD-001:v1.2,approved,approved product evidence
policy,NST-POLICY-001:v3.0,approved,approved current policy evidence
policy,NST-POLICY-001:v2.0,archived,exclude
evaluation,NST-EVAL-001,held_out,exclude
brief,NST-BRIEF-001,draft,output target only
Tasks
1. Define three specialists.
2. Assign each specialist only the tools or resources it needs.
3. Decide which tasks may run in parallel.
4. Write a handoff contract for the CRM researcher.
5. Define the join condition.
6. Define two stopping conditions.
7. Define three review checks.
8. State whether the design claims live execution.
Guided-practice solution
1. Specialists
agents:
  - agent_id: NST-MA-CRM-001
    purpose: retrieve_authorized_customer_facts

  - agent_id: NST-MA-KNOWLEDGE-001
    purpose: retrieve_approved_product_and_policy_evidence

  - agent_id: NST-MA-REVIEW-001
    purpose: review_draft_against_evidence_and_policy
2. Permissions
permissions:
  NST-MA-CRM-001:
    scopes:
      - crm:read
    tools:
      - crm.search_contacts
      - crm.get_customer_snapshot
      - crm.list_open_deals
    writes_enabled: false
    messages_enabled: false

  NST-MA-KNOWLEDGE-001:
    scopes:
      - documents:read
    resources:
      - northstar://product/NST-PROD-001:v1.2
      - northstar://policy/NST-POLICY-001:v3.0
    writes_enabled: false
    messages_enabled: false

  NST-MA-REVIEW-001:
    scopes: []
    tools: []
    resources: []
    input:
      - evidence_packet
      - draft
3. Parallel tasks
These may run in parallel:
CRM researcher
Knowledge researcher
These must wait:
Evidence join waits for both research branches.
Draft writer waits for the evidence packet.
Reviewer waits for the draft.
4. CRM handoff
handoff_id: NST-HANDOFF-CRM-001
from_agent: NST-MA-SUPERVISOR-001
to_agent: NST-MA-CRM-001
task_id: NST-TASK-001
input:
  tenant: northstar-demo
  lookup:
    email: contact@example.com
  requested_fields:
    - customer_id
    - account_name
    - active_status
    - open_deal_summary
permissions:
  scope: crm:read
  writes_enabled: false
  messages_enabled: false
required_output:
  - match_count
  - customer_id
  - source_ids
  - missing_fields
stop_conditions:
  - multiple_exact_matches
  - no_authorized_match
  - permission_denied
5. Join condition
CRM branch is complete.
Knowledge branch is complete.
Both branches provide source IDs.
Both branches report missing fields.
No branch reports an unhandled policy violation.
6. Stopping conditions
Examples:
Stop after two transient retries for one tool.
Stop immediately on permission denial.
Stop and escalate if customer identity is ambiguous.
Stop and escalate if required evidence is unavailable.
7. Review checks
Every factual claim has an allowed source.
Archived and held-out records are absent.
The draft does not claim writes, messages or live execution.
8. Execution status
Live execution claimed: false
Independent challenge — Choose the right orchestration pattern
Scenario A
A user asks for a simple product explanation from one approved document.
Scenario B
A support request must be classified as billing, technical support or account access, then handled by one specialist.
Scenario C
A renewal brief requires independent CRM research and policy research, followed by a combined draft.
Scenario D
A draft must be checked against a clear citation checklist and revised when it fails.
Scenario E
A coding task may require an unpredictable number of files and specialized subtasks.
Tasks
For each scenario:
1. Choose the most suitable starting pattern.
2. State whether the task should begin as a single agent, workflow or multi-agent design.
3. Identify one risk.
4. Define one evaluation metric.
Independent-challenge solution
Scenario	Pattern	Starting design	Main risk	Example metric
A	Single augmented model	Single agent or direct RAG workflow	Unsupported document interpretation	Citation coverage
B	Routing	Workflow with classifier and one specialist	Misclassification	Routing accuracy
C	Parallel sectioning plus join	Code-controlled multi-agent workflow	Conflicting or incomplete branches	Evidence coverage
D	Evaluator-optimizer	Sequential workflow	Endless revision loop	First-pass reviewer rate
E	Orchestrator-workers	Agentic multi-agent workflow	Unbounded delegation and cost	Task completion within budget
A good design does not select “multi-agent” merely because the task is interesting. It selects the smallest pattern that addresses the task’s actual structure.
Common problems and recovery
Problem 1: Every agent has every tool
Why it happens
The team attaches all tools to a shared supervisor for convenience.
Why it is harmful
- Increases tool-selection errors.
- Increases data exposure.
- Makes audit attribution difficult.
- Allows a writer or reviewer to mutate data.
- Weakens least privilege.
Recovery
- Create an explicit agent-to-tool matrix.
- Remove unused tools.
- Test that unauthorized tools are absent.
- Attach permissions to the agent role and application context.
Problem 2: A handoff transfers too much history
Why it happens
The entire conversation is forwarded to every specialist.
Risks
- Unnecessary personal data exposure.
- Prompt injection propagation.
- Larger context and cost.
- Confusion about which instructions are authoritative.
- Accidental disclosure of credentials or internal notes.
Recovery
- Use a structured handoff.
- Filter history.
- Pass only task-relevant facts.
- Preserve source identifiers.
- Redact secrets and unrelated personal data.
Problem 3: The supervisor accepts a specialist’s unsupported conclusion
Why it happens
The specialist returns fluent prose without evidence fields.
Recovery
Require:
claim
claim_type
source_id
source_status
observed_status
missing_fields
The supervisor should reject a conclusion that lacks required evidence.
Problem 4: Parallel agents write to the same record
Why it happens
Parallelization is applied to operations with shared side effects.
Recovery
- Keep parallel branches read-only.
- Serialize writes.
- Use a proposal and approval stage.
- Revalidate the record immediately before execution.
- Make writes idempotent.
- Record the owner and correlation ID.
Problem 5: A handoff loops forever
Why it happens
Agent A sends to B, B sends to C, and C sends back to A without a limit.
Recovery
Add:
max_handoffs: 4
max_turns: 12
max_repairs: 2
visited_agents:
  - ...
Stop when the budget is exceeded and return an escalation.
Problem 6: The reviewer becomes a second writer
Why it happens
The reviewer is asked to “fix anything necessary” and has broad tools.
Recovery
Make the reviewer return findings and repair instructions. Keep writing with the draft agent or controlled application code. Remove CRM and messaging tools from the reviewer.
Problem 7: The branches disagree
Example
CRM researcher: customer is active.
Knowledge researcher: policy source is archived.
Recovery
- Preserve both claims and sources.
- Apply source-status rules.
- Ask a reviewer or human to resolve a true conflict.
- Do not average the disagreement.
- Do not choose the most fluent answer.
Problem 8: Agent cost grows unexpectedly
Possible causes
- Repeated handoffs.
- Long history passed to every specialist.
- Unbounded retries.
- Overly broad research.
- Repeated reviewer loops.
- Duplicate parallel work.
Recovery
Track:
model calls per agent
tokens per handoff
tool calls per branch
retry count
review cycles
elapsed time
upstream API calls
Set budgets before production execution.
Problem 9: A reviewer passes because it sees the draft but not the source
Cause
The reviewer lacks the evidence packet.
Recovery
Pass the draft and the structured evidence packet together. The reviewer should not judge citations from prose alone.
Problem 10: Multi-agent architecture is used where a workflow is enough
Symptom
Several agents perform fixed steps with no real specialization.
Recovery
Collapse the system into:
- One agent.
- A deterministic chain.
- A single model call with retrieval.
- A code-controlled workflow.
Reintroduce specialists only when evaluation demonstrates the benefit.
Knowledge check
Question 1
Which design should be tested first for a simple question answered by one approved document?
A. Unbounded agent swarm  
B. Single grounded agent or direct retrieval workflow  
C. Five parallel writers  
D. Supervisor with every enterprise tool
Question 2
What does an “agents as tools” pattern preserve?
A. The specialist’s direct control of the user conversation  
B. The manager’s control of the overall answer  
C. Automatic CRM write permission  
D. A shared global credential
Question 3
What does a handoff do?
A. Deletes the prior agent  
B. Transfers the next stage of work to a specialist  
C. Grants all scopes to the specialist  
D. Guarantees correctness
Question 4
Why should CRM and document research run in parallel in the Northstar case?
Question 5
What must happen before the writer receives research results?
A. The CRM must be updated  
B. The evidence branches should be joined into a structured packet  
C. The reviewer should send an email  
D. The held-out evaluation should be added
Question 6
Which claim type should be used for “The customer may need follow-up”?
A. observed_fact  
B. documented_fact  
C. inference  
D. source_id
Question 7
Name two stopping conditions for a multi-agent workflow.
Question 8
Why should the reviewer receive both the draft and the evidence packet?
Question 9
Which operation should remain unavailable in the initial Northstar multi-agent design?
A. crm.search_contacts  
B. crm.get_customer_snapshot  
C. crm.update_customer  
D. Reading NST-POLICY-001:v3.0
Question 10
What should the system do when there is no source for a requested renewal amount?
A. Invent an estimate  
B. Copy the value from a different customer  
C. Mark the field unknown and report the missing evidence  
D. Read the held-out evaluation
Answers
 1. B. Begin with the simplest grounded design.
 2. B. The manager retains control and uses the specialist for a bounded subtask.
 3. B. It transfers the next stage to a specialist.
 4. They are independent read-only research branches.
 5. B. The join creates a structured evidence packet.
 6. C. It is an inference.
 7. Examples include permission denial, retry-budget exhaustion, ambiguous customer identity, missing required evidence or maximum-turn exhaustion.
 8. The reviewer must verify the draft against actual source evidence rather than trusting prose.
 9. C. CRM updates remain unavailable.
10. C. Preserve the unknown and report the missing evidence.
Recap
A multi-agent system is a coordination design, not a badge of sophistication.
Start with:
simple prompt
    |
    v
grounded single-agent workflow
Add specialists when the task benefits from:
- Clear separation of responsibilities.
- Narrower data access.
- Independent research.
- Specialized prompts.
- Evaluation and review.
- Different risk or permission boundaries.
Useful patterns include:
Sequential chain
Routing
Parallel sectioning
Parallel voting
Orchestrator-workers
Evaluator-optimizer
Manager with agents as tools
Handoff to a specialist
For Northstar, the selected initial design is:
Supervisor
  |
  +--> CRM researcher
  |
  +--> Knowledge researcher
          |
          v
    Evidence join
          |
          v
      Draft writer
          |
          v
    Evidence reviewer
          |
          v
   User-facing draft
The design preserves the boundaries from C03-CH12:
- CRM tools are read-only.
- Documents are current and approved.
- Archived and held-out sources are excluded.
- The tenant comes from trusted context.
- Writes and messages are unavailable.
- No live execution is claimed.
- API consumption is measured at the upstream operation level.
- The final answer contains evidence and uncertainty.
The next chapter continues with deployment and operational concerns: how to move agent workflows from design and testing into controlled environments.
Glossary
Agent  
A model-driven system that can determine steps, use tools and continue toward a goal.
Agent-as-tool  
A pattern in which a manager calls a specialist as a bounded subtask while retaining overall control.
Branch  
An independent path within a workflow, such as CRM research or document research.
Code-controlled orchestration  
Application code determines the order, routing, joins and limits of agent execution.
Evidence packet  
A structured collection of source-backed claims, source status, missing fields and exclusions.
Evaluator-optimizer  
A pattern in which one component produces a draft and another evaluates it, potentially causing revision.
Handoff  
A transfer of active work from one agent to another specialist.
Join  
The controlled step that combines results from multiple workflow branches.
Manager agent  
An agent that retains responsibility for coordinating specialists and producing the final response.
Multi-agent system  
A system containing multiple specialized agents that coordinate through an explicit workflow or delegation mechanism.
Orchestrator-workers  
A pattern in which an orchestrator dynamically assigns subtasks to worker agents and synthesizes their outputs.
Parallel sectioning  
A pattern that splits independent subtasks and runs them concurrently.
Retry budget  
The maximum number of retries allowed for a given failure class.
Scope  
A permission boundary assigned to an agent, tool or access token.
Specialist agent  
An agent with a narrow task, tool set, context boundary and output contract.
Stopping condition  
An explicit rule that ends work, escalates or prevents unlimited execution.
Supervisor  
The coordinating component responsible for the overall task and policy decisions.
Workflow  
A predefined sequence of model calls, tools, checks and state transitions.
Further reading
Agent design
- Anthropic — Building Effective Agents (https://www.anthropic.com/research/building-effective-agents)
- OpenAI Agents SDK — Agent orchestration (https://openai.github.io/openai-agents-python/multi_agent/)
- OpenAI Agents SDK — Handoffs (https://openai.github.io/openai-agents-python/handoffs/)
- OpenAI Agents SDK — Guardrails (https://openai.github.io/openai-agents-python/guardrails/)
- OpenAI Agents SDK — Tracing (https://openai.github.io/openai-agents-python/tracing/)
Related Northstar chapters
- C03_CH09_Tool_and_API_Contract_Design_Student.md
- C03_CH10_Workflow_Orchestration_and_State_Student.md
- C03_CH11_Zia_Agent_Studio_Implementation_Student.md
- C03_CH12_Model_Context_Protocol_Student.md
Current Northstar continuity
- NST-ZIA-AGENT-001: read-and-draft Zia agent design.
- NST-ZIA-TOOLS-001: Zia tool group.
- NST-MCP-CATALOG-001: read-only MCP catalog.
- NST-MCP-ACCESS-001: MCP scope and access policy.
- NST-EVAL-001: held-out evaluation fixture.
- NST-BRIEF-001: draft output record.
No live multi-agent run, CRM write, message send or production deployment was observed.
