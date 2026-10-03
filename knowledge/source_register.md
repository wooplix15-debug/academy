# Source Register and Owner Decisions

Technical links were checked on 2 October 2026. They support specific technical references, not the proposed durations, policies or business outcomes. The source plan’s CoGrad and NVIDIA examples were not used as evidence for this curriculum.

## S01 User supplied Wooplix Academy Business Automation Plan

Wooplix_Academy_Business_Automation_Plan.docx

Strategic input only; internal experience and commercial claims have not been independently verified.

## S02 Zoho CRM V8 API documentation

https://www.zoho.com/crm/developer/docs/api/v8/

API families and integration reference; recheck version, edition and quotas before labs.

## S03 Zoho CRM OAuth authorization

https://www.zoho.com/crm/developer/docs/api/v8/auth-request.html

Organization and environment scoped authorization.

## S04 Zoho Deluge integration tasks

https://www.zoho.com/deluge/help/integration-tasks.html

Integration task wrappers and external call consumption.

## S05 Zoho Creator form workflows

https://help.zoho.com/portal/en/kb/creator/developer-guide/workflows/create-and-manage-form-workflows/articles/understanding-form-workflows

Form events and workflow behavior.

## S06 Zoho CRM Blueprint overview

https://www.zoho.com/crm/tutorials/blueprint/summary.html

States, transitions and business process design.

## S07 OpenAI structured outputs

https://developers.openai.com/api/docs/guides/structured-outputs

Structured response contract for the optional agent runner.

## S08 OpenAI agent evaluations

https://developers.openai.com/api/docs/guides/agent-evals

Evaluation of agent workflow quality.

## Decisions needed before enrollment

Confirm the primary learner group, teaching language, live delivery mode, program durations, trainer and reviewer names, pilot capacity, actual Zoho editions and environments, budget and prices, cohort dates and timezones, refund and retake terms, credential wording, recording consent, data retention and source permissions. These decisions refine the starter package; they do not prevent work on the first synthetic lessons.

## Next practical action

Choose Implementation Practitioner as the first technical pilot and the corporate workshop as the short business offer. Have a Zoho trainer rehearse the first lesson and all practitioner labs. Confirm actual tool access, then publish the approved syllabus and enrollment terms. Use the website copy with your own verified trainer profiles and experience. Generate remaining teaching detail from the catalog and review it one module at a time with your team.

## Practical teaching additions
- S09: [CRM upsert](https://www.zoho.com/crm/developer/docs/api/v8/upsert-records.html). Upsert selects insert or update using duplicate-check fields. Teach record uniqueness separately from exactly-once downstream effects. Verify supported matching fields and current conditional-write behavior before a connected lab.
- S10: [CRM API limits](https://www.zoho.com/crm/developer/docs/api/v8/api-limits.html). Credits, concurrency and operation behavior depend on the documented API and organization. Teach observation and explicit run budgets rather than hardcoded universal limits.
- S11: [Planned mandatory-field change](https://help.zoho.com/portal/pt/community/topic/crm-developer-update-mandatory-field-behavior-changes-in-zoho-crm-apis). Checked 2 October 2026: this official notice says a change is planned for the end of October 2026 and is not live yet. Do not teach it as deployed. Refresh before the next cohort and inspect actual layout and field metadata. Name, company and email requirements in the migration simulator are lab rules.
- S12: [Deluge connections](https://www.zoho.com/deluge/help/connections.html). Connections provide authorized access for supported service tasks. Record the connection name, needed operations and environment without copying credential values.

- S13 Deluge lab references checked 3 October 2026. See knowledge/S13_reference.md and materials/code_examples/README.md for the official links and rehearsal limits.
