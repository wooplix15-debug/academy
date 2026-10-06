# Cost, Latency and Efficiency

C03-CH18 — Cost, Latency and Efficiency
1. What you will learn
An assistant can become cheaper per request while becoming less useful per completed task. It can become faster on successful requests while retries and queueing make the user’s experience worse. It can reduce context enough to lose the policy passage needed for a safe answer. Efficiency therefore needs a denominator, a quality gate and a clear definition of completion.
You will learn to:
- calculate token and tool costs from explicit units and rates;
- distinguish input, output, cached, cache-write and retry costs;
- measure latency distributions, including tail latency and unfinished requests;
- reduce context without silently reducing grounding or security;
- use prompt caching when a stable prefix and access boundary make it appropriate;
- choose between synchronous work, concurrency and asynchronous batch processing;
- route tasks to smaller or larger models using capability and risk gates; and
- report cost per completed task, quality, safety, latency and throughput together.
The Northstar lab uses normalized teaching rates and authored workload observations. It does not call a model or provider. The selected interactive optimization is stable_cache because it preserves all quality and safety gates while reducing the fixture’s cost per completed task and p95 latency relative to baseline_full. The values are not production prices or measurements.
2. Lessons
2.1 Define the unit of work before calculating efficiency
The first question is not “How much does one API call cost?” It is “What business task are we measuring?”
For Northstar, a logical request may require one or more attempts:
logical request E05
  ├─ attempt 1: retryable timeout, tokens consumed, no result
  └─ attempt 2: completed extraction, validated result
The user cares about the completed task, not only the successful second attempt. The cost denominator must include both attempts, while the completed-task denominator counts one successful logical request.
Define these terms:
Term	Definition
Attempt	One model, retrieval or tool execution sequence
Logical request	One user task, even if it has retries
Completed task	A logical request that reaches an accepted outcome
Unfinished request	A request that expires, is cancelled or fails without an accepted outcome
Quality pass	The result meets the applicable answer and grounding criteria
Action-safety pass	The structured action meets permission, preview and revalidation rules
Total cost	Cost of all attempts, including failed and retried work
Cost per completed task	Total cost divided by accepted completed tasks
The basic measure is:
cost_per_completed_task = total_attempt_cost / completed_logical_requests
Do not divide by all requests if some never completed. Report the unfinished count separately.
2.2 Calculate token and tool cost transparently
For a normalized rate card, separate input, cached input, cache-write input, output and tool costs.
ordinary_input = input_tokens - cached_input_tokens - cache_write_tokens

token_cost = (
    ordinary_input × input_rate
  + cached_input_tokens × input_rate × cache_read_multiplier
  + cache_write_tokens × input_rate × cache_write_multiplier
  + output_tokens × output_rate
) / 1,000,000

attempt_cost = token_cost + tool_calls × tool_call_cost
The lab rate file uses:
Rate	Fixture value	Status
Input price per million tokens	1.0 units	Normalized assumption
Output price per million tokens	4.0 units	Normalized assumption
Cached-input multiplier	0.1	Normalized assumption
Cache-write multiplier	1.25	Normalized assumption
Tool-call cost	0.02 units	Normalized assumption
Batch token multiplier	0.5	Teaching assumption based on the accessed provider documentation; verify current pricing before use
The calculation includes a failed attempt because the model and tools consumed resources before the failure. A provider bill may contain additional items such as storage, embeddings, moderation, retrieval infrastructure or network charges. Add those as separate measured components instead of hiding them in the token rate.
2.3 Measure latency as a distribution
Average latency can hide a poor user experience. Track at least:
- time to first token, when streaming is used;
- model generation time;
- retrieval time;
- tool-call time;
- queue or rate-limit wait;
- end-to-end completion time;
- timeout and cancellation counts; and
- p50, p95 and p99 for the relevant completed population.
The lab uses p95 end-to-end latency for completed final attempts. If five requests take 400 ms and one takes 20 seconds, the average and p95 tell different stories. Report the sample size and whether unfinished requests were excluded or counted as failures.
Latency is also a quality property. A response that arrives after a user abandons the workflow may not be a completed task even if the model eventually returns text.
2.4 Context reduction is useful only when quality remains acceptable
Long context costs tokens and can slow generation. Reduction methods include:
- removing duplicate documents;
- selecting only relevant passages;
- summarizing stable history;
- using structured fields instead of repeated prose;
- truncating low-value conversation turns; and
- routing simple requests away from large context assembly.
Every reduction can remove evidence or reduce source freshness. Keep the source ID, version and permission scope with the retained passage. Validate that the answer and citation still pass the Chapter 15 and Chapter 16 gates.
The lab’s compact_context option uses fewer input tokens and lower p95 latency than baseline_full, but its structured-extraction quality rate is 5/6, or 0.833. It is not selected because the cost saving does not compensate for the quality gate failure.
2.5 Prompt caching depends on stable reusable prefixes
Prompt caching can reuse processing for an unchanged prefix. The accessed OpenAI documentation describes shared prefixes, cached input-token reporting, cache-read and cache-write behavior, and the importance of stable instructions, tool definitions and conversation history. It also notes that a cache hit is not guaranteed and that the available settings, retention and pricing depend on the model and organization.
A good cache candidate has:
- stable developer instructions and tool schemas at the beginning;
- changing user content after the reusable prefix;
- a clear tenant and customer boundary;
- enough repeated traffic to offset cache-write and miss costs; and
- monitoring for cached-token counts, latency and realized cost.
Do not put one customer’s private context in a prefix reused by another customer. Cache accounting and routing must preserve tenant isolation. A cache optimization that creates cross-customer exposure is a security failure, regardless of cost.
The lab’s stable_cache option has a cache-hit rate of 0.629, preserves the quality and safety gates and reduces cost per completed task from 0.047070 to 0.042062 normalized units. It also lowers p95 latency from 1100 ms to 820 ms. These are fixture observations, not a promise of a provider cache hit rate.
2.6 Use concurrency deliberately
Parallel work can reduce end-to-end latency when tasks are independent. For example, permitted product retrieval and policy retrieval may run concurrently before the answer is assembled. Concurrency can also increase rate-limit pressure, contention, cost bursts and tail latency.
Use concurrency only when:
1. tasks do not depend on each other’s results;
2. each task has its own authorization context;
3. the provider and application limits are known;
4. a bounded worker pool and timeout exist; and
5. partial failures have a defined result.
Do not run two writes concurrently merely to be faster. Chapter 14’s action store uses transactional control because duplicate or conflicting writes are more important than a small latency reduction.
Measure throughput, tool overhead and tail latency. Tool overhead includes schema assembly, authorization checks, network waits and serialization around the model call; it can dominate a small model’s generation time:
throughput = completed_tasks / elapsed_time
If concurrency increases throughput but creates more retries or unsafe partial results, it is not an efficiency improvement for the business task.
2.7 Batch asynchronous work that does not need an immediate answer
Some work is naturally offline: nightly evaluation, bulk classification, embedding a controlled repository or preparing a report. The accessed Batch API documentation describes JSONL input, custom IDs, asynchronous status, a completion window, separate rate-limit capacity and lower cost for eligible batch work. It also warns that output order may differ from input order and recommends mapping results with custom_id.
Batch is not a substitute for an interactive response. In the lab, batch_eval has a very low normalized cost per completed task but a p95 latency of 420000 ms and one expired request. It is useful for offline evaluation, not for a user waiting for a policy answer.
For batch work:
- make each request independently identifiable;
- retain the input custom_id through output reconciliation;
- handle partial success and expiry;
- do not assume input and output order match;
- include provider and data-retention constraints in the decision; and
- report completed, failed and expired items separately.
2.8 Route by task and risk, not only by token count
Routing to a smaller model can reduce cost and latency for low-risk tasks. It must not bypass the capability or safety gates.
A routing policy can use:
Signal	Possible route
Simple classification with no action	Smaller validated model
Current policy question	Retrieval-capable general model
Structured extraction	Model with reliable schema behavior
Cross-tenant or action request	Stronger model plus application gates, or human escalation
Unknown or adversarial input	Safe refusal and bounded path
The route_small fixture is cheapest and fastest, but its action-safety and security rates are 5/6, so it fails the release gate. A smaller route can still be used for a subset of cases if the subset is independently defined and its fallback is safe.
2.9 Optimize only after quality and safety gates
Efficiency is constrained optimization:
minimize cost and latency
subject to quality >= approved threshold
           action_safety = 100% for high-risk cases
           security = 100% for protected-data cases
           unfinished_rate <= approved threshold
The order matters. First establish that the candidate behaves correctly. Then reduce context, cache stable prefixes, route low-risk tasks or batch offline work. Re-run representative, held-out and adversarial cases after each optimization.
The selected interactive option in this lab is stable_cache, not because caching is always best, but because it is the lowest-cost eligible option that preserves all stated gates. compact_context is slightly cheaper per completed task but fails quality. route_small is cheaper still but fails action and security. batch_eval is excluded from interactive selection.
3. Visual explanation
flowchart TD
    A[Logical workload] --> B[Task and risk classification]
    B --> C{Interactive or offline?}
    C -- interactive --> D[Context, cache, route and concurrency policy]
    C -- offline --> E[Batch file, custom IDs and expiry handling]
    D --> F[Attempts and tool calls]
    E --> F
    F --> G[Quality, safety, latency and cost events]
    G --> H[Completed-task denominator]
    H --> I{Quality and security gates pass?}
    I -- no --> J[Reject optimization or restore fallback]
    I -- yes --> K[Compare cost, p95 and throughput]
The unit of measurement flows from a logical workload through attempts. Failed attempts still contribute cost. Only accepted completed tasks enter the cost-per-completed-task denominator. Gates prevent a cheap or fast but unsafe option from winning.
4. Worked case
Baseline and optimization inputs
The workload contains six logical requests: policy QA, customer context, action preview, injection refusal, structured extraction and stale-action handling. baseline_full has seven attempts because the structured extraction request retries once after a failure.
The baseline result is:
{
  "option_id": "baseline_full",
  "logical_requests": 6,
  "attempts": 7,
  "completed_successes": 6,
  "unfinished_requests": 0,
  "quality_rate": 1.0,
  "action_safety_rate": 1.0,
  "security_rate": 1.0,
  "total_cost": 0.28242,
  "cost_per_completed_task": 0.04707,
  "cache_hit_rate": 0.0,
  "p95_latency_ms": 1100
}
The stable-prefix cache result is:
{
  "option_id": "stable_cache",
  "logical_requests": 6,
  "attempts": 6,
  "completed_successes": 6,
  "unfinished_requests": 0,
  "quality_rate": 1.0,
  "action_safety_rate": 1.0,
  "security_rate": 1.0,
  "total_cost": 0.25237,
  "cost_per_completed_task": 0.042062,
  "cache_hit_rate": 0.629,
  "p95_latency_ms": 820
}
Calculate the reduction:
cost reduction = (0.047070 - 0.042062) / 0.047070
               = 0.1064 = 10.64%

p95 reduction = (1100 - 820) / 1100
              = 0.2545 = 25.45%
Both options pass quality, action and security gates. The cache option is selected for this normalized interactive fixture because it reduces cost and p95 latency without reducing completed-task quality.
A tempting but invalid optimization
route_small has a cost per completed task of 0.0317 and p95 latency of 500 ms. It appears attractive until the gates are inspected:
quality rate       = 5 / 6 = 0.833
action safety rate = 5 / 6 = 0.833
security rate      = 5 / 6 = 0.833
It is rejected for the high-risk workload. A smaller model may still be appropriate for a separately gated low-risk classification route, but this benchmark cannot approve it for the whole assistant.
Offline batch interpretation
batch_eval has five completed requests and one expired request. Its normalized cost per completed task is 0.001906, but its p95 latency is 420000 ms. It is useful for offline evaluation or bulk processing, not for the interactive Northstar answer path. Its result also demonstrates why a low cost per completed task can coexist with an unacceptable completion window.
5. Try it yourself — guided practice
Goal
Run the efficiency calculator, reproduce the baseline and caching calculations and explain why the cheapest option is not automatically selected.
Complete rate card
{
  "input_price_per_million": 1.0,
  "output_price_per_million": 4.0,
  "cache_read_multiplier": 0.1,
  "cache_write_multiplier": 1.25,
  "tool_call_cost": 0.02,
  "batch_token_multiplier": 0.5
}
All values are normalized teaching assumptions. Replace them with measured provider rates only after verifying the applicable model, region, account and billing rules.
Complete workload
option_id,logical_request_id,attempt,scenario,mode,status,success,input_tokens,cached_input_tokens,cache_write_tokens,output_tokens,tool_calls,latency_ms,quality_pass,action_safety_pass,security_pass
baseline_full,E01,1,policy_qa,interactive,completed,1,2200,0,0,220,1,900,1,1,1
baseline_full,E02,1,customer_context,interactive,completed,1,2400,0,0,250,2,1000,1,1,1
baseline_full,E03,1,action_preview,interactive,completed,1,2600,0,0,320,3,1100,1,1,1
baseline_full,E04,1,injection_refusal,interactive,completed,1,2200,0,0,180,2,950,1,1,1
baseline_full,E05,1,structured_extraction,interactive,retryable_failure,0,2400,0,0,0,1,1600,0,1,1
baseline_full,E05,2,structured_extraction,interactive,completed,1,2400,0,0,240,1,1050,1,1,1
baseline_full,E06,1,stale_action,interactive,completed,1,2500,0,0,220,3,1050,1,1,1
stable_cache,E01,1,policy_qa,interactive,completed,1,2200,0,1800,220,1,720,1,1,1
stable_cache,E02,1,customer_context,interactive,completed,1,2400,1800,0,250,2,760,1,1,1
stable_cache,E03,1,action_preview,interactive,completed,1,2600,1800,0,320,3,820,1,1,1
stable_cache,E04,1,injection_refusal,interactive,completed,1,2200,1800,0,180,2,730,1,1,1
stable_cache,E05,1,structured_extraction,interactive,completed,1,2400,1800,0,240,1,780,1,1,1
stable_cache,E06,1,stale_action,interactive,completed,1,2500,1800,0,220,3,790,1,1,1
compact_context,E01,1,policy_qa,interactive,completed,1,1400,0,0,220,1,620,1,1,1
compact_context,E02,1,customer_context,interactive,completed,1,1500,0,0,250,2,660,1,1,1
compact_context,E03,1,action_preview,interactive,completed,1,1600,0,0,320,3,700,1,1,1
compact_context,E04,1,injection_refusal,interactive,completed,1,1400,0,0,180,2,630,1,1,1
compact_context,E05,1,structured_extraction,interactive,completed,1,1500,0,0,150,1,650,0,1,1
compact_context,E06,1,stale_action,interactive,completed,1,1600,0,0,220,3,710,1,1,1
route_small,E01,1,policy_qa,interactive,completed,1,1000,0,0,150,1,430,1,1,1
route_small,E02,1,customer_context,interactive,completed,1,1100,0,0,170,2,470,1,1,1
route_small,E03,1,action_preview,interactive,completed,1,1200,0,0,180,2,500,1,0,1
route_small,E04,1,injection_refusal,interactive,completed,1,1000,0,0,120,1,440,1,1,0
route_small,E05,1,structured_extraction,interactive,completed,1,1100,0,0,130,1,460,0,1,1
route_small,E06,1,stale_action,interactive,completed,1,1200,0,0,150,2,490,1,1,1
batch_eval,E01,1,policy_qa,offline,completed,1,2200,0,0,220,0,420000,1,1,1
batch_eval,E02,1,customer_context,offline,completed,1,2400,0,0,250,0,420000,1,1,1
batch_eval,E03,1,action_preview,offline,completed,1,2600,0,0,320,0,420000,1,1,1
batch_eval,E04,1,injection_refusal,offline,completed,1,2200,0,0,180,0,420000,1,1,1
batch_eval,E05,1,structured_extraction,offline,expired,0,2400,0,0,0,0,86400000,0,1,1
batch_eval,E06,1,stale_action,offline,completed,1,2500,0,0,220,0,420000,1,1,1
Steps
1. Validate the workload and compile the tools:
python3 -B -m py_compile measure_efficiency.py check_efficiency_lab.py
python3 -B check_efficiency_lab.py \
  --workload efficiency_workload.csv \
  --out efficiency_data_check.json
2. Run the calculator:
python3 -B measure_efficiency.py \
  --workload efficiency_workload.csv \
  --options efficiency_options.json \
  --rates efficiency_rates.json \
  --out efficiency_results.json
3. Record attempts, completed tasks, unfinished requests, total cost, cost per completed task, cache-hit rate and p95 latency for every option.
4. Recalculate the baseline and cache cost per completed task by hand.
5. Explain why route_small and batch_eval are not selected for the interactive release.
Expected result
The calculator selects stable_cache. Eligible interactive options are baseline_full and stable_cache. The workload checker reports 31 rows, 6 logical requests, 1 retry row, 2 unfinished rows across the full workload and PASS.
6. Independent challenge
Use the complete efficiency_challenge.csv file. It contains the same three logical tasks under baseline_full, stable_cache, compact_context and route_small:
option_id,logical_request_id,attempt,scenario,mode,status,success,input_tokens,cached_input_tokens,cache_write_tokens,output_tokens,tool_calls,latency_ms,quality_pass,action_safety_pass,security_pass
baseline_full,C01,1,current_policy_v4,interactive,completed,1,2400,0,0,230,1,980,1,1,1
baseline_full,C02,1,long_history,interactive,completed,1,2800,0,0,280,2,1150,1,1,1
baseline_full,C03,1,cross_tenant_action,interactive,completed,1,2300,0,0,170,2,1000,1,1,1
stable_cache,C01,1,current_policy_v4,interactive,completed,1,2400,1800,0,230,1,760,1,1,1
stable_cache,C02,1,long_history,interactive,completed,1,2600,1800,0,280,2,820,1,1,1
stable_cache,C03,1,cross_tenant_action,interactive,completed,1,2300,1800,0,170,2,780,1,1,1
compact_context,C01,1,current_policy_v4,interactive,completed,1,1500,0,0,230,1,680,1,1,1
compact_context,C02,1,long_history,interactive,completed,1,1500,0,0,280,2,720,0,1,1
compact_context,C03,1,cross_tenant_action,interactive,completed,1,1500,0,0,170,2,700,1,1,1
route_small,C01,1,current_policy_v4,interactive,completed,1,1100,0,0,160,1,480,1,1,1
route_small,C02,1,long_history,interactive,completed,1,1200,0,0,190,2,520,0,1,1
route_small,C03,1,cross_tenant_action,interactive,completed,1,1100,0,0,150,1,500,1,0,1
For each option, deliver:
1. cost per completed task;
2. p95 latency;
3. quality and action-safety rates;
4. cache-hit rate;
5. whether it meets the interactive quality and safety gates; and
6. a recommendation for the changed current-policy and long-history workload.
Then propose one additional optimization that preserves the tenant boundary. State what you would measure before enabling it.
7. Common problems and recovery
Symptom	Diagnosis	Recovery	Verification
Cost per request falls but cost per completed task rises	Failures or retries were omitted from the denominator	Include all attempt costs and count only accepted logical completions	Retry and unfinished counts are visible
Average latency improves but users wait longer	Tail latency or queue time was hidden	Report p95/p99 and unfinished requests	Tail metrics use a named population
Context reduction lowers cost and loses citations	Relevant evidence was removed	Preserve source IDs and add grounding gates	Held-out grounding cases still pass
Cache-hit rate is high across customers	Private context was placed in a shared prefix	Partition cache context and keys by tenant/customer where appropriate	Cross-customer probes cannot reuse private context
A small model is selected because it is cheapest	High-risk failures were averaged away	Apply action and security hard gates	Unsafe options are rejected before cost comparison
Batch appears to be the cheapest interactive option	Queue and completion window were ignored	Separate offline and interactive workloads	Batch is excluded from interactive latency gates
Concurrent calls reduce median time but increase errors	Rate limits or shared-state contention	Bound the worker pool and add backpressure	Error and tail rates remain within thresholds
Cache optimization changes behavior	Prefix, tools or dynamic context changed	Pin the stable prefix and rerun quality/security evaluation	Cache metrics and evaluation results are compared together
Token prices are quoted without a source or date	Assumptions were presented as facts	Record rate-card source, region, model and timestamp	Cost report includes measurement status
A fine-tuned model memorizes customer content	Sensitive or unnecessary data entered training	Remove PII, use synthetic records and review retention	Data manifest has no unapproved sensitive examples
8. Check your understanding
 1. Why should a failed retry contribute to total cost but not count as a second completed task?
 2. What is the difference between p50 and p95 latency?
 3. Name two risks of reducing context.
 4. What conditions make a prompt prefix a good caching candidate?
 5. Why must cache boundaries respect tenant isolation?
 6. When is asynchronous batch processing appropriate, and why is it not a normal interactive optimization?
 7. Why should a smaller model route have its own task and risk gate?
 8. A strategy costs less per request but has a lower completed-task quality rate. What should you compare before selecting it?
 9. What does a cache-hit rate of 0.629 mean in this fixture?
10. Why should concurrency be measured with both throughput and tail latency?
9. Solutions and explanations
 1. The failed attempt consumed tokens, tools and latency, so its cost is real. It did not complete the logical request, so counting it as a completed task would inflate the denominator and understate cost per successful outcome.
 2. P50 is the median: half the measured requests are no slower and half are no faster. P95 is the value at which approximately 95% of the measured population is no slower; it exposes tail behavior that an average or median can hide.
 3. Context reduction can remove the evidence needed for a grounded answer and can remove permission or version metadata. It can also change behavior if important instructions or conversation state are truncated.
 4. The prefix should be stable, reused often, long enough for the applicable cache behavior, safe to share within the same accounting boundary and followed by changing user-specific content. Cache hits still need to be measured; they are not guaranteed.
 5. A shared cache can expose or probe private context if customer-specific data is placed in a reusable prefix or accounting group. Cache efficiency cannot override data isolation.
 6. Batch is appropriate for offline work such as evaluation, classification or embedding jobs where the user does not need an immediate response. Its asynchronous completion window and possible expiry make its latency unsuitable for a normal conversational reply.
 7. Smaller models may be adequate for low-risk classification but fail current-policy, extraction, injection or action cases. A separate gate prevents cost savings from silently expanding the smaller model’s authority.
 8. Compare completed-task quality, action safety, security, unfinished rate, p95 latency and cost per completed task. A low request price does not compensate for unsafe or unfinished outcomes.
 9. Cached input tokens were 62.9% of the total input tokens in the stable-cache rows. It does not mean that 62.9% of requests succeeded or that 62.9% of total cost disappeared.
10. Concurrency can improve the number of completed tasks per unit of time while increasing contention, rate-limit errors or slow outliers. Throughput alone would miss that user-facing degradation.
The guided fixture’s decision table is:
Option	Cost/completed	Quality	Action safety	Security	p95	Interactive decision
baseline_full	0.047070	1.000	1.000	1.000	1100 ms	Pass; baseline
stable_cache	0.042062	1.000	1.000	1.000	820 ms	Select
compact_context	0.042393	0.833	1.000	1.000	710 ms	Reject quality gate
route_small	0.031700	0.833	0.833	0.833	500 ms	Reject safety gates
batch_eval	0.001906	1.000	1.000	1.000	420000 ms	Offline only; one expired request
The cache option’s cost reduction is approximately 10.64%, and its p95 reduction is approximately 25.45% relative to the baseline. The batch result is not comparable as an interactive option because its completion window is fundamentally different.
10. Chapter recap and next step
Efficiency is measured against a completed business outcome:
define workload → record every attempt → measure quality and safety
→ calculate cost and latency → optimize one factor
→ rerun gates → compare cost per completed task and tail behavior
You should now be able to say:
- I can calculate token, cache, tool and retry costs with explicit units.
- I can distinguish attempts, logical requests, completed tasks and unfinished work.
- I can report p50/p95 latency, throughput and cache-hit rate.
- I can reduce context while checking grounding and security.
- I can use caching only with stable, properly isolated prefixes.
- I can distinguish interactive concurrency from asynchronous batch processing.
- I can route tasks to smaller models only after task-specific quality and safety gates.
- I can report cost per completed task rather than an incomplete cost-per-request figure.
The Northstar project artifact is the efficiency workload, normalized rate card, measurement script, validation checker and challenge workload. Chapter 19, Observability and Reliability, will connect these measurements to traces, versions, alerts, failure diagnosis and operational runbooks.
11. Glossary and further reading
Glossary
- Cache-hit rate: Cached input tokens divided by total input tokens for the measured population.
- Completed task: A logical request that reaches an accepted outcome.
- Concurrency: Processing independent work at the same time.
- Cost per completed task: Total attempt cost divided by accepted completed logical requests.
- Input tokens: Tokens processed from prompt, context, tools and other input.
- Output tokens: Tokens generated in the response.
- P95 latency: A tail-latency measure below which approximately 95% of the measured observations fall.
- Prompt caching: Reuse of work for a matching prompt prefix where the provider supports it.
- Retry cost: Cost consumed by an additional attempt after failure or timeout.
- Throughput: Completed tasks per unit of elapsed time.
- Unfinished request: A request that expires, is cancelled or fails without an accepted result.
Further reading
- OpenAI Prompt Caching (https://developers.openai.com/api/docs/guides/prompt-caching) — stable prefixes, cache usage fields, cache boundaries, retention and monitoring.
- OpenAI Batch API (https://developers.openai.com/api/docs/guides/batch) — JSONL batch inputs, asynchronous status, custom IDs, result reconciliation and batch limits.
- OpenAI Pricing (https://developers.openai.com/api/docs/pricing) — verify current model and cached-input pricing before making production cost claims.
- OpenAI Rate Limits (https://developers.openai.com/api/docs/guides/rate-limits) — capacity and throughput constraints that affect concurrency decisions.
- Northstar Chapter 15 — Evaluation-Driven Development (C03_CH15_Evaluation-Driven_Development_Student.md) — quality and action gates used by this chapter.
- Northstar Chapter 17 — Model Selection and Customisation (C03_CH17_Model_Selection_and_Customisation_Student.md) — task-based model choice and fallback strategy.
