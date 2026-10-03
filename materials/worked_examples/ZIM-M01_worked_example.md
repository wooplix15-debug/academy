# CRM Discovery and Scope Worked Teaching Example

Module ZIM M01

## Learner scenario

Nova Services is fictional. Its sales team receives website inquiries, qualifies leads, sends quotes and hands won deals to an implementation coordinator. The team currently uses spreadsheets. The sales manager asks for automatic lead assignment, cleaner pipeline reporting and a reliable handoff. No budget, deadline, product edition or success threshold has been agreed.

## Trainer walkthrough

Begin by asking what successful inquiry handling looks like. Separate observations from assumptions. Ask who owns assignment, which geography defines an owner, what makes a lead qualified, when a quote requires approval, which handoff fields the coordinator needs and who may see other teams’ records. Ask for a baseline sample before claiming that automation will save time.

Turn the statement “follow up leads quickly” into a requirement with an owner and an agreed threshold. Example requirement R01: when a new lead has region West and is not a duplicate, assign it to the West sales queue. The proposed queue membership must be confirmed by the sponsor. A lead with no region should go to an exception queue rather than being silently discarded.

Example acceptance tests: a new valid West lead enters the West queue; a lead without region enters the exception queue; a duplicate is flagged without creating an extra follow up; a sales user cannot read records outside the agreed sharing model. These are design examples, not assertions that every Zoho edition supports a particular configuration.

## Guided assignment

Write eight requirements for the scenario. Each must have an ID, business owner, trigger, desired behavior and test. Include assignment, qualification, quote review, handoff, duplicate handling, access, reporting and exceptions. Add assumptions, exclusions and five unanswered questions. Draw a process with owners at each stage.

## Independent assignment

Produce a one page discovery brief, eight requirement records, a process map, a scope statement and a priority list. Use synthetic input records from materials/synthetic_leads.csv to create at least four positive and four negative test examples. Time budget is two hours.

## Answer guidance

Strong work distinguishes record lifecycle from approval and handoff; does not assume an unlimited tool license; keeps missing sponsor decisions visible; and defines what happens when input is invalid. An answer may use different stages if it is consistent with the scenario and can be tested. Do not require an invented service level as the only correct answer.

## Sample exit questions

What is missing from “automate lead assignment”? Expected answer: assignment criteria, eligible record event, owner, exception path and measurable acceptance.

Why is the product edition an open question? Expected answer: feature availability may constrain the design, effort and practical exercise.

Who approves the discovery scope? Expected answer: the responsible business sponsor and delivery owner; the AI only drafts it.
