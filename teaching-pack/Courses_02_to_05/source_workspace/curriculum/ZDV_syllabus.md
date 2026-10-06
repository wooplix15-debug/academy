# Zoho Creator Deluge and Integration Developer

Program ZDV | Developer | 12 weeks | 72 total hours

Audience: Existing Zoho developers and technically confident implementation specialists.

Prerequisites: Demonstrate CRM proficiency, basic variables and conditions, JSON and HTTP concepts in the programming diagnostic.

Completion outcome: Build a Creator application and a resilient Deluge integration using documented API contracts and tests.

Environment: Creator and CRM training organizations, enabled connections, API client, version control and synthetic datasets; verify licensing and call budgets.

Time allocation: 48 facilitated hours and 24 independent practical hours. Quiz and review time are included in those hours.

## Module syllabus

### Week 1 Application requirements and model

Module ZDV-M01 | 4 facilitated hours | 2 practice hours

Learners will design entities for a service workflow; identify data ownership.

Syllabus: User stories; Entity relationships; Unique business keys.

Practical: Model customers, service requests and work items with a unique request key.

Submission: Entity diagram and six user stories.

Assessment checks: Relationships match requirements; Uniqueness rule is defined; Ownership of shared fields is explicit.

### Week 2 Creator forms and reports

Module ZDV-M02 | 4 facilitated hours | 2 practice hours

Learners will build related forms; create appropriate views for users.

Syllabus: Field types and lookups; Reports; Validation and navigation.

Practical: Build request and work item forms with a filtered open work report.

Submission: App screenshots and data dictionary.

Assessment checks: Lookups connect intended records; Validation catches bad input; Report filters match user tasks.

### Week 3 Deluge language essentials

Module ZDV-M03 | 4 facilitated hours | 2 practice hours

Learners will use variables lists maps and conditions; trace a script with sample values.

Syllabus: Data types; Collections and loops; Null handling.

Practical: Transform five synthetic request payloads into normalized maps.

Submission: Commented script and expected outputs.

Assessment checks: Null values are handled; Each output matches the input rule; Learner explains the control flow.

### Week 4 Deluge functions and debugging

Module ZDV-M04 | 4 facilitated hours | 2 practice hours

Learners will write reusable functions; diagnose failure from controlled logs.

Syllabus: Function inputs and outputs; Error handling; Redacted diagnostics.

Practical: Build a reusable request validation function and diagnose three seeded defects.

Submission: Function and debugging notes.

Assessment checks: Inputs have a contract; Logs omit tokens and personal data; Each defect has a reproducible test.

### Week 5 Form events and workflow behavior

Module ZDV-M05 | 4 facilitated hours | 2 practice hours

Learners will choose the correct form event; test validation before persistence.

Syllabus: Load input and submission events; Workflow ordering; Event specific limitations.

Practical: Implement request validation and post submission action in appropriate events.

Submission: Event matrix and four case log.

Assessment checks: Invalid requests are rejected; Actions occur at the intended stage; Edition and event limitations are documented.

### Week 6 REST and JSON contracts

Module ZDV-M06 | 4 facilitated hours | 2 practice hours

Learners will read an API request and response; map payloads to application fields.

Syllabus: HTTP methods and statuses; JSON; API metadata and pagination.

Practical: Map a CRM record response to the service request model using a mock response first.

Submission: Contract and mapping table.

Assessment checks: Required fields are explicit; Pagination is considered; Malformed JSON has a handled failure path.

### Week 7 OAuth and connections

Module ZDV-M07 | 4 facilitated hours | 2 practice hours

Learners will explain delegated authorization; configure minimum required access.

Syllabus: Authorization grant; Scopes and environments; Connections and token handling.

Practical: Document connection setup and test an allowed read and a denied operation.

Submission: Setup guide with redacted evidence.

Assessment checks: No secret is submitted; Scopes match the lab; Test and production environments are distinguished.

### Week 8 Deluge integrations

Module ZDV-M08 | 4 facilitated hours | 2 practice hours

Learners will use documented integration tasks; handle external call limits deliberately.

Syllabus: Integration task wrappers; invoke URL concepts; Response handling and quotas.

Practical: Create a reviewed test record through a connection or a mock equivalent.

Submission: Integration code and response log.

Assessment checks: API version is recorded; Response success is checked; External call consumption is estimated.

### Week 9 Reliable synchronization

Module ZDV-M09 | 4 facilitated hours | 2 practice hours

Learners will prevent duplicate business operations; design recoverable synchronization.

Syllabus: Idempotency; Timeouts retries and backoff; Reconciliation and conflict rules.

Practical: Simulate duplicate events and a timeout after the destination committed a record.

Submission: Sync design and replay evidence.

Assessment checks: Replay does not create a second business record; Retry has a bound; Conflict ownership is documented.

### Week 10 Testing and release

Module ZDV-M10 | 4 facilitated hours | 2 practice hours

Learners will create meaningful positive and failure tests; plan versioned deployment.

Syllabus: Test fixtures; Change records; Release and rollback.

Practical: Run the developer scenario suite and prepare a deployment checklist.

Submission: Test log and deployment notes.

Assessment checks: Ten scenarios have expected outcomes; Known defects are recorded; Rollback includes data impact.

### Week 11 Capstone build and review

Module ZDV-M11 | 4 facilitated hours | 2 practice hours

Learners will assemble the service application; improve code through review.

Syllabus: Build integration; Peer review; Support documentation.

Practical: Complete the service request application and resolve reviewer defects.

Submission: Working training app and review log.

Assessment checks: Core journey works end to end; Failure paths are demonstrated; Another developer can inspect the code.

### Week 12 Developer defense and handover

Module ZDV-M12 | 4 facilitated hours | 2 practice hours

Learners will explain implementation tradeoffs; transfer support knowledge.

Syllabus: Practical defense; Code explanation; Operations handover.

Practical: Demonstrate the capstone, answer scenario questions and repeat a repair task.

Submission: Portfolio bundle and final practical.

Assessment checks: Learner explains code independently; All required tests pass; Handover includes limitations and maintenance.

## Capstone and assessment

Build a service request application with a reviewed CRM handoff and status reconciliation.

Required evidence: Requirements, forms and reports, Deluge code, connection setup guide without secrets, API contract, test log, failure queue design and deployment notes.

Scenario tests: Missing required field; invalid lookup; unauthorized action; token or connection failure; duplicate request; retry after timeout; malformed payload; quota exhaustion simulation; conflicting update; data reconciliation.

Assessment weighting: quizzes 15 percent, module labs 35 percent, capstone 40 percent, practical defense 10 percent.

Proposed version 0.2 pass rules: overall score, module-lab average and capstone each at least 70 percent; at least 80 percent attendance with approved makeups; every required submission; all critical permission and data integrity checks passed; and acceptance by a named human reviewer. Practical defense contributes 10 percent to the overall score. Use materials/Practical_Assessment_Rubric.md and confirm the policy before enrollment.

Reference identifiers: S02, S03, S04, S05. Verify the actual product edition and feature access before delivery.
