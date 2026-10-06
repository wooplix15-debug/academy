schema_version: "1.1"
course_id: "C01"
chapter_id: "C01-CH17"
chapter_number: 17
chapter_title: "Reporting and Zoho Analytics"
filename: "C01_CH17_Reporting_and_Zoho_Analytics_Student.md"
audience_type: "student"
version: "0.1"
status: "draft"
research_status: "not_verified"
---
Reporting and Zoho Analytics
1. What you will learn
Reports and dashboards help you understand what is happening in a business process. They can also create false conclusions when records are joined at the wrong grain, unfinished records are excluded without explanation or totals are duplicated.
This chapter uses Zoho Analytics as the candidate reporting application for Meridian Supply. It teaches stable reporting concepts and a configuration method. Exact current connectors, user-interface labels, refresh behavior and sharing permissions must be verified before production use.
You will learn to:
- distinguish a report from a dashboard;
- connect CRM, Books, Desk and People data;
- define relationships between source tables;
- identify the grain of a dataset;
- create formulas with clear units and denominators;
- build pivots and summary reports;
- design dashboard cards, charts and filters;
- configure sharing and restricted audiences;
- understand refresh and connector failures;
- detect duplicated totals after joins;
- write reproducible metric definitions;
- build a dashboard and reconcile it to source records.
The chapter continues the Meridian project. The supplied continuity from Chapter 16 establishes:
- employee records are separate from sales, finance and service records;
- confidential employee fields require restricted access;
- customer, quote, finance and service records have separate system ownership;
- no live product execution has been verified.
The reporting data in this chapter is a synthetic reporting snapshot. It does not silently revise earlier chapter facts. Where a snapshot uses earlier business IDs, the values shown in the snapshot are the values to use for that reporting exercise.
2. Lessons
2.1 Reports, dashboards and source records
A report answers a defined question using a dataset.
Examples:
- How many enquiries were accepted this month?
- Which invoices have an open balance?
- Which service tickets missed the first-response target?
- Which department owns the largest backlog?
A dashboard presents several related reports and measures on one screen for a defined audience.
A dashboard should not replace the source records. It summarizes them. When a dashboard number is disputed, the source records and metric definition must be available.
Report types
Report type	Purpose	Example
Detail report	Show one row per defined record	One row per ticket
Summary report	Group and aggregate records	Ticket count by department
Pivot report	Compare dimensions across rows and columns	Ticket count by severity and department
Reconciliation report	Compare expected and observed values	Quote total versus invoice total
Exception report	Show records requiring action	Failed handoffs
Dashboard	Present several reports and controls together	Meridian operations dashboard
Source ownership
Data	Source of truth in the Meridian design
Enquiry, customer context and quote	CRM
Product and pricing context	CRM commercial records
Invoice, payment and receivable	Books
Ticket, assignment and resolution	Desk
Employee record, leave and onboarding	People
A connector can copy data into Analytics without transferring ownership. The report should identify the source and last refresh time.
Check your understanding
Why should a dashboard tile showing open receivables link back to invoice and payment records?
Answer: The tile is a summary. Users need source records to verify invoice amount, payment allocation, adjustments and the calculation used for the balance.
2.2 Connectors and relationships
A connector imports or synchronizes data from another application. It may bring in:
- tables;
- modules;
- fields;
- record IDs;
- timestamps;
- relationships;
- update or refresh information.
A connector does not automatically create a correct analytical model. You must decide which tables to use, how they relate and which records are included.
Relationships
A relationship explains how records in one table correspond to records in another.
Examples:
- one customer has many quotes;
- one quote has many line items;
- one invoice has many payments or adjustments;
- one customer has many tickets;
- one employee has many leave requests.
A relationship key should be stable and meaningful. Use business IDs or verified application IDs rather than display names.
Parent table	Child table	Relationship
Customer	Quote	One customer to many quotes
Quote	Quote line item	One quote to many lines
Invoice	Payment allocation	One invoice to many payment allocations
Customer	Ticket	One customer to many tickets
Employee	Leave request	One employee to many leave requests
Before creating a relationship, ask:
1. Is the parent key unique?
2. Can the child have multiple parents?
3. Are unmatched records expected?
4. What should happen to records with missing keys?
5. Will the relationship multiply rows?
Connector refresh
Document:
- source application;
- tables or modules;
- last successful refresh;
- refresh schedule;
- records added;
- records changed;
- records rejected;
- owner of connector failure.
A dashboard with a current-looking design may still display yesterday’s data.
Check your understanding
Why should a relationship between customers and quotes use a customer ID instead of customer name?
Answer: Names can be duplicated, abbreviated or changed. A stable customer ID provides a more reliable relationship.
2.3 Data grain
The grain of a dataset states what one row represents.
Examples:
- one row per enquiry;
- one row per quote;
- one row per quote line;
- one row per invoice;
- one row per payment allocation;
- one row per service ticket;
- one row per leave request.
Write the grain in a sentence before creating formulas.
This table has one row per approved quote.
This table has one row per quote line.
If you do not know the grain, you cannot safely sum amounts or count records.
One-to-many duplication
Suppose MER-QUOTE-101 has:
- quote total: USD 5,984.00;
- three quote lines.
If you join the quote table to the line table and retain the quote total on every joined row, the data may look like this:
Quote ID	Line	Quote total
MER-QUOTE-101	1	5,984.00
MER-QUOTE-101	2	5,984.00
MER-QUOTE-101	3	5,984.00
A simple sum produces:
5,984 + 5,984 + 5,984 = USD 17,952
That is incorrect. The quote total was repeated once per line.
Correct approaches include:
- sum the quote table before joining;
- calculate totals from line extensions at line grain;
- use a distinct quote-level measure;
- aggregate the child table before joining;
- keep quote and line reports separate.
Other duplication risks
- one invoice joined to several payments;
- one customer joined to several contacts;
- one ticket joined to several messages;
- one employee joined to several leave records.
A count of rows is not necessarily a count of business records.
Check your understanding
If one invoice has three payment allocations, what can happen when invoice amount is summed after joining?
Answer: The invoice amount may appear three times and be overstated. Invoice totals should be calculated at invoice grain, while payment totals should be calculated at payment-allocation grain.
2.4 Formulas and metric definitions
A formula is useful only when its inputs, units, denominator and exclusions are clear.
Example: quote acceptance rate
Definition:
Accepted quotes / quotes sent × 100
If four quotes were sent and three were accepted:
3 / 4 × 100 = 75%
Do not use all quote records as the denominator if some were never sent.
Example: first-response attainment
Definition:
Eligible tickets meeting target / eligible tickets × 100
If two of three eligible tickets met the target:
2 / 3 × 100 = 66.67%
An ineligible ticket with missing customer context should be reported separately, not silently counted as success or failure.
Example: open receivable
At invoice grain:
Open receivable
= invoice amount
− applied payment amount
− credit adjustments
+ debit adjustments
Do not calculate it from a joined table unless the payment and adjustment aggregation has already been controlled.
Metric-definition template
Definition item	Example
Metric name	First-response attainment
Business question	What proportion of eligible tickets received a timely human response?
Grain	One row per ticket
Numerator	Eligible tickets where first human response met target
Denominator	Eligible tickets with a valid service target
Formula	Numerator / denominator × 100
Exclusions	Missing customer context; invalid timestamps
Time zone	Meridian local service time
Source	Desk ticket table
Refresh	Daily synthetic snapshot
Owner	Service reporting owner
A report should display the metric definition or link to it.
Check your understanding
Why is “average response time” incomplete as a metric definition?
Answer: It does not state the time unit, start event, response event, exclusions, time zone, ticket population or treatment of unfinished tickets.
2.5 Pivots and dashboards
A pivot report groups measures by dimensions.
A pivot normally needs:
- row dimension;
- column dimension;
- measure;
- aggregation;
- filters;
- date range;
- grain.
Example:
Pivot component	Meridian choice
Rows	Service department
Columns	Severity
Measure	Distinct ticket count
Filter	Created date in reporting period
Exclusion	Missing-customer tickets shown separately
A dashboard should contain a small number of useful elements:
- KPI cards;
- trend chart;
- exception table;
- reconciliation table;
- filters;
- last-refresh indicator;
- metric-definition link.
Meridian dashboard design
Dashboard element	Measure
Quotes sent	Count of quotes with sent timestamp
Quote acceptance rate	Accepted sent quotes / sent quotes
Open receivables	Invoice-level balance
Service first-response attainment	Eligible tickets meeting target / eligible tickets
Failed handoffs	Count of distinct failed correlation IDs
Reconciliation exceptions	Count of unreconciled invoice or payment records
Do not place sales, finance, service and employee data in one broadly shared dashboard without considering access. An employee dashboard with confidential information should be restricted separately.
Filters
Useful filters include:
- reporting period;
- department;
- owner;
- customer tier;
- quote status;
- service severity;
- reconciliation status.
A filter should have a defined scope. If a date filter affects quotes but not payments, the dashboard should make that behavior clear.
Check your understanding
Why should a dashboard include a last-refresh timestamp?
Answer: It tells users how current the data is. A number without refresh information may be mistaken for a live operational result.
2.6 Sharing and confidentiality
Sharing must protect the source data and the derived report.
Define:
- who can view the dashboard;
- who can edit the dashboard;
- who can export data;
- whether filters restrict rows or only change the display;
- whether employee data is excluded or separately restricted;
- who can view raw source tables;
- who owns metric definitions.
A dashboard filter is not automatically a security control. A user may be able to remove a filter unless row-level access or equivalent restrictions are configured.
Meridian audiences
Audience	Suitable dashboard access
Sales leadership	Sales pipeline and quote measures
Finance	Orders, invoices, payments and receivables
Service management	Tickets, targets, escalations and article usage
Operations leadership	Approved cross-functional summary
HR	Restricted employee dashboard
Sales representative	Own or permitted sales records only
Do not include employee names, identity information, payroll information or confidential case notes in the shared operations dashboard.
Check your understanding
Why is hiding a column different from restricting access to the underlying employee data?
Answer: A hidden column may still be accessible through exports, source tables or changed report settings. Access restrictions must apply to the data and user role, not only the visible layout.
2.7 Refresh and reconciliation
A refresh updates the analytical dataset from its sources. A successful refresh does not guarantee correct data.
Check:
- refresh completion;
- source record count;
- new and changed records;
- rejected records;
- duplicate imports;
- missing relationships;
- time-zone conversion;
- changed field definitions;
- connector errors.
A reconciliation compares the report result with source records.
For example:
Dashboard open receivable = USD 936.50
Source invoice reconciliation total = USD 936.50
Difference = USD 936.50 − USD 936.50 = USD 0.00
If the dashboard shows USD 2,809.50, it may have repeated each invoice balance once per payment or adjustment row.
Reconciliation evidence
Field	Example
Report name	Meridian Operations Dashboard
Refresh timestamp	2026-12-01 08:00
Source population	Three invoices
Expected total	USD 936.50
Dashboard total	USD 936.50
Difference	USD 0.00
Reviewer	Finance reporting owner
Result	Reconciled
Check your understanding
What should you investigate if the source invoice total is correct but the dashboard total is three times higher?
Answer: Check for a one-to-many join, such as each invoice being repeated for three payment or adjustment rows. Recalculate at invoice grain or aggregate the child table first.
2.8 Configuring Zoho Analytics
This is an edition-neutral procedure. Exact connectors, import options, formula names, relationships, filters, sharing controls and refresh schedules must be verified.
Required access
You need:
- Analytics workspace access;
- permission to create or manage connections;
- source-system access to CRM, Books, Desk and People;
- permission to define relationships and formulas;
- permission to create reports, pivots and dashboards;
- permission to configure refresh;
- permission to share data with defined audiences;
- source owners who can verify results.
Procedure
1. Define dashboard questions and audiences.
Expected result: Every dashboard element has a business purpose and permitted audience.
2. Select source tables and connectors.
Expected result: Sources, owners and refresh responsibilities are recorded.
3. Record the grain of each table.
Expected result: A report designer can state what one row represents.
4. Define relationships.
Expected result: Parent and child keys are identified and unmatched records have a route.
5. Create formulas and metric definitions.
Expected result: Each formula has a numerator, denominator, unit and exclusion rule.
6. Build detail and reconciliation reports.
Expected result: Dashboard values can be traced to source records.
 7. Build pivots and dashboard components.
Expected result: Users can see trends, categories and exceptions without losing the underlying detail.
 8. Add filters and refresh information.
Expected result: Filter scope and data freshness are visible.
 9. Configure sharing.
Expected result: Users see only the data permitted for their role.
10. Refresh and reconcile.
Expected result: Dashboard totals match independently calculated source totals or have documented differences.
3. Visual explanation
flowchart LR
    CRM[CRM tables] --> Model[Analytics data model]
    Books[Books tables] --> Model
    Desk[Desk tables] --> Model
    People[People tables] --> Restricted[Restricted HR model]
    Model --> Grain[Grain and relationship checks]
    Grain --> Formula[Metric formulas]
    Formula --> Reports[Detail, pivot and reconciliation reports]
    Reports --> Dashboard[Shared operations dashboard]
    Restricted --> HRDashboard[Restricted HR dashboard]
    Sources[Refresh history] --> Dashboard
    Dashboard --> Reconcile[Source reconciliation]
The diagram separates the shared operations model from the restricted HR model. It also shows that formulas and dashboards should be built after grain and relationships are checked.
4. Worked case: Meridian operations dashboard
4.1 Reporting snapshot
This is a synthetic snapshot for 2026-12-01. It does not revise the earlier process examples.
The shared operations dashboard uses:
- one row per quote in the quote table;
- one row per invoice in the invoice table;
- one row per service ticket in the ticket table;
- one row per quote line in the quote-line table.
4.2 Quote fact table
Quote ID	Enquiry ID	Status	Sent?	Accepted?	Total USD
MER-QUOTE-101	MER-ENQ-101	Customer Accepted	Yes	Yes	5,984.00
MER-QUOTE-202	MER-ENQ-202	Awaiting Customer	Yes	No	2,800.00
MER-QUOTE-301	MER-ENQ-301	Customer Accepted	Yes	Yes	4,153.60
MER-QUOTE-401	MER-ENQ-401	Customer Accepted	Yes	Yes	8,017.10
MER-QUOTE-404	MER-ENQ-404	Awaiting Approval	No	No	4,500.00
Quote acceptance rate:
Accepted sent quotes = 3
Sent quotes = 4

Acceptance rate
= 3 / 4 × 100
= 75%
MER-QUOTE-404 is excluded from the denominator because it was not sent.
4.3 Invoice fact table
Invoice ID	Quote ID	Invoice amount	Payment applied	Credit adjustment	Open balance
MER-INVOICE-101	MER-QUOTE-101	6,800.00	5,984.00	816.00	0.00
MER-INVOICE-301	MER-QUOTE-301	4,153.60	4,000.00	100.00	53.60
MER-INVOICE-401	MER-QUOTE-401	8,900.00	8,017.10	0.00	882.90
Open-receivable total:
0.00 + 53.60 + 882.90
= USD 936.50
4.4 Service ticket fact table
Ticket ID	Department	Severity	Eligible for SLA?	Met first-response target?
MER-TKT-301	Installation Support	Standard	Yes	Yes
MER-TKT-302	Technical Support	High	Yes	No
MER-TKT-304	Installation Support	Standard	Yes	Yes
MER-TKT-303	Service Data Review	Standard	No	—
First-response attainment:
Eligible tickets = 3
Eligible tickets meeting target = 2

Attainment
= 2 / 3 × 100
= 66.67%
4.5 Duplicate-total example
Suppose the quote table is joined to the quote-line table. MER-QUOTE-101 has three lines, so its USD 5,984 quote total appears three times.
Incorrect joined sum:
5,984 × 3 = USD 17,952
Correct quote-level total:
MER-QUOTE-101 = USD 5,984
The report should either:
- calculate quote totals from the quote fact table;
- calculate line totals from the quote-line table;
- aggregate lines by quote before joining;
- use a distinct quote-level measure.
Do not sum a quote-level amount across a quote-line join.
4.6 Completed dashboard design
Dashboard element	Source grain	Formula or measure
Quotes sent	One row per quote	Count where Sent = Yes
Quote acceptance rate	One row per quote	Accepted sent / sent
Open receivables	One row per invoice	Sum open balance
SLA attainment	One row per ticket	Met eligible / eligible
Reconciliation exceptions	One row per invoice	Count Reconciled = No
Escalated service tickets	One row per ticket	Count Status = Escalated
4.7 Mistake and correction
Mistake: The dashboard joins quotes, quote lines, invoices and payments into one wide table, then sums every amount.
Why it is wrong: Each one-to-many relationship multiplies rows. Quote amounts, invoice amounts and payment amounts can all be repeated.
Correction: Keep fact tables at their original grain. Aggregate child records before joining or use separate reports for quote, invoice and payment measures. Reconcile each dashboard tile to its source grain.
5. Try it yourself — guided practice
Learning goal
Build a Meridian dashboard and reconcile it to source records.
Required access
You need:
- Analytics workspace access;
- CRM, Books and Desk source access;
- permission to create relationships, formulas, reports, pivots and dashboards;
- permission to refresh and share a test dashboard;
- a finance and service owner who can verify totals.
Complete practice data
Quote table: one row per quote
Quote ID	Status	Sent?	Accepted?	Total USD
MER-QUOTE-501	Customer Accepted	Yes	Yes	6,400.00
MER-QUOTE-502	Awaiting Customer	Yes	No	2,800.00
MER-QUOTE-503	Customer Accepted	Yes	Yes	3,900.00
MER-QUOTE-504	Draft	No	No	5,100.00
Invoice table: one row per invoice
Invoice ID	Quote ID	Invoice amount	Payment applied	Credit adjustment
MER-INVOICE-501	MER-QUOTE-501	6,400.00	6,400.00	0.00
MER-INVOICE-503	MER-QUOTE-503	3,900.00	3,800.00	0.00
Ticket table: one row per ticket
Ticket ID	Department	Severity	Eligible?	Met target?
MER-TKT-601	Installation Support	Standard	Yes	Yes
MER-TKT-602	Technical Support	High	Yes	No
MER-TKT-603	Billing Questions	Standard	Yes	Yes
MER-TKT-604	Service Data Review	Standard	No	—
Guided steps and expected results
Step 1: Record table grain
Create a source register.
Expected result:
Quote table: one row per quote
Invoice table: one row per invoice
Ticket table: one row per ticket
Step 2: Create relationships
Relate quote to invoice using Quote ID. Keep the ticket table separate from quote and invoice amounts unless a controlled customer or case relationship is needed.
Expected result: The invoice totals remain at invoice grain.
Step 3: Build quote reports
Create a detail report and a summary report.
Calculate:
Sent quotes = 3
Accepted sent quotes = 2

Acceptance rate
= 2 / 3 × 100
= 66.67%
Expected result: The Draft quote is excluded from the denominator.
Step 4: Build the receivable report
Calculate:
Invoice total = 6,400 + 3,900 = 10,300
Payment total = 6,400 + 3,800 = 10,200
Credit total = 0
Open receivable = 10,300 − 10,200 = USD 100
Expected result: Open receivable is USD 100.
Step 5: Build a service pivot
Use:
- rows: department;
- columns: met target;
- measure: distinct ticket count.
Expected result:
- two eligible tickets met target;
- one eligible ticket missed target;
- one ticket is excluded for missing context.
Step 6: Build dashboard cards
Create cards for:
- sent quotes;
- quote acceptance rate;
- open receivables;
- service first-response attainment;
- unresolved reconciliation exceptions.
Expected result: The dashboard displays source-linked measures, not manually typed numbers.
Step 7: Add filters
Add filters for:
- owner;
- department;
- quote status;
- service severity;
- reporting date.
Expected result: Filter scope is documented.
Step 8: Configure sharing
Share a sales view with sales users, a finance view with finance users and a service view with service managers. Do not include People data in the shared dashboard.
Expected result: Each role sees only its permitted subject area.
Step 9: Refresh and reconcile
Record refresh time and compare every KPI with the source tables.
Expected result: The reconciliation difference is zero.
Final artifact
Your dashboard submission should contain:
Artifact	Minimum content
Source register	Application, table, grain, owner and refresh
Relationship design	Keys, cardinality and unmatched-record treatment
Metric dictionary	Formula, numerator, denominator and exclusions
Pivot report	Dimensions, measure and filters
Dashboard	Cards, charts, exception table and refresh timestamp
Sharing matrix	Role, dashboard and export permission
Reconciliation sheet	Source total, dashboard total and difference
User guide	How a manager reads and filters the dashboard
Safe cleanup
Use a test Analytics workspace where possible. Remove only test connections, reports and dashboards after recording results. Do not alter shared source connectors without confirming ownership.
Offline alternative
Use spreadsheets to model grain, relationships, formulas, pivots and reconciliation. This cannot demonstrate actual connector refresh, Analytics sharing, row-level access or production dashboard performance.
6. Independent challenge
Quarterly Meridian dashboard and duplicate-total investigation
Create a dashboard using the following changed data.
Quote table: one row per quote
Quote ID	Customer tier	Sent?	Accepted?	Total USD
MER-QUOTE-601	Standard	Yes	Yes	3,000.00
MER-QUOTE-602	Standard	Yes	No	1,000.00
MER-QUOTE-603	Partner	Yes	Yes	5,500.00
MER-QUOTE-604	Standard	No	No	2,000.00
Quote-line table: one row per quote line
Quote ID	Line number	Product	Extension USD
MER-QUOTE-601	1	Workstation	2,000.00
MER-QUOTE-601	2	Installation	1,000.00
MER-QUOTE-602	1	Support plan	1,000.00
MER-QUOTE-603	1	Monitor	2,000.00
MER-QUOTE-603	2	Docking station	1,500.00
MER-QUOTE-603	3	Installation	2,000.00
MER-QUOTE-604	1	Workstation	2,000.00
Invoice table
Invoice ID	Quote ID	Invoice amount	Payment applied	Credit adjustment
MER-INVOICE-601	MER-QUOTE-601	3,000.00	3,000.00	0.00
MER-INVOICE-603	MER-QUOTE-603	5,600.00	5,500.00	0.00
Service table
Ticket ID	Department	Eligible?	Met target?
MER-TKT-701	Installation Support	Yes	Yes
MER-TKT-702	Technical Support	Yes	No
MER-TKT-703	Technical Support	Yes	Yes
MER-TKT-704	Service Data Review	No	—
Deliverables
Create:
1. a dashboard with sales, finance and service cards;
2. a quote acceptance metric;
3. a service attainment metric;
4. an invoice reconciliation metric;
5. a demonstration of the duplicated-total problem after joining quotes to lines;
6. a corrected report design;
7. a sharing matrix;
8. a refresh and reconciliation record.
Success criteria
Your design should:
- calculate acceptance using sent quotes only;
- calculate open receivables at invoice grain;
- identify the USD 100 open balance on MER-INVOICE-603;
- show why MER-QUOTE-601 is overstated if quote total is summed after joining to two lines;
- exclude MER-QUOTE-604 from the sent-quote denominator;
- exclude MER-TKT-704 from SLA attainment but report it as a data exception;
- keep employee information outside the shared dashboard.
7. Common problems and recovery
Symptom	Diagnosis	Correction	Verification
Dashboard totals are higher than source totals	One-to-many join duplicated parent amounts	Aggregate child rows or use grain-specific measures	Reconcile at parent grain
Quote acceptance rate changes when line items are imported	Denominator is line rows instead of quote rows	Count distinct sent quote IDs	Recalculate from quote table
Open receivable is multiplied by payment count	Invoice amount was summed after payment join	Aggregate payments first, then join to invoice	Compare invoice-level balances
A report includes stale records	Connector refresh failed or schedule is unknown	Inspect refresh history and rerun safely	Record last successful refresh
An unmatched record disappears	Inner relationship or filter excluded it	Use an exception report or controlled unmatched branch	Count source versus model records
A filter appears to secure data	Filter changes display but not access	Configure role or row-level access	Test export and source-table access
HR data appears in an operations dashboard	Restricted and shared datasets were combined	Separate HR workspace or restricted dashboard	Test non-HR viewer
Formula has no denominator definition	Metric was named without a measurement rule	Add numerator, denominator and exclusions	Reproduce with source records
Dashboard shows average response time without units	Formula lacks time unit and start event	Define business hours, timestamps and pauses	Recalculate one ticket manually
Pivot counts updates instead of tickets	Grain is event or message, not ticket	Count distinct ticket IDs	Compare to source ticket list
Refresh creates duplicate records	Incremental key or merge logic is missing	Use stable source IDs and update strategy	Refresh twice and compare counts
Invoice discrepancy is hidden by a dashboard adjustment	Report hides source difference	Show expected, observed and adjustment separately	Reconcile before and after adjustment
Users export more data than needed	Sharing and export permissions are broad	Restrict export and source-table access	Test each role
Source field changes break formulas	Connector schema changed	Review failed fields and update mappings	Reconcile after refresh
A dashboard number is manually typed	Report is not connected to source data	Replace manual value with formula or source report	Trace the value to a record
8. Check your understanding
 1. What is the difference between a report and a dashboard?
 2. What does data grain mean?
 3. What is the grain of a quote-line table?
 4. Why can a quote total be duplicated after joining to quote lines?
 5. What is the formula for quote acceptance rate?
 6. Why must a metric define its denominator?
 7. What is the purpose of a connector?
 8. Why should HR data be placed in a restricted model or dashboard?
 9. What should a refresh record contain?
10. Calculate quote acceptance when 3 of 4 sent quotes were accepted.
11. Calculate open receivable when invoice amounts total USD 10,300 and payments total USD 10,200 with no adjustments.
12. Why should service attainment exclude a ticket with missing customer context?
13. What is a pivot report useful for?
14. Why is a dashboard filter not necessarily a security control?
15. What should you do when a dashboard value does not reconcile to source records?
9. Solutions and explanations
9.1 Answers to the checks
 1. A report answers a defined question using a dataset. A dashboard presents several related reports and measures for a defined audience.
 2. Grain states what one row represents.
 3. One row per quote line.
 4. The parent quote total appears once for each child line. Summing the repeated parent value overstates the total.
 5. Accepted sent quotes / sent quotes × 100.
 6. Without a denominator, the percentage cannot be reproduced or interpreted.
 7. A connector imports or synchronizes source data into the analytical environment.
 8. Employee data may contain confidential information and should not be exposed to users who only need sales, finance or service summaries.
 9. Source, refresh time, success or failure, records added or changed, rejected records and owner.
10. 3 / 4 × 100 = 75%.
11. 10,300 − 10,200 = USD 100.
12. The ticket is not eligible under the stated metric definition. It should be reported separately as a data-quality exception.
13. A pivot compares grouped dimensions, such as ticket counts by department and severity.
14. A user may remove or change a display filter unless row-level access or equivalent restrictions are configured.
15. Check grain, joins, filters, refresh, source population and formulas. Reconcile at the relevant source-record grain before changing the dashboard.
9.2 Guided practice sample solution
Grain register
Table	Grain
Quote table	One row per quote
Invoice table	One row per invoice
Ticket table	One row per service ticket
Quote metrics
Sent quotes = MER-QUOTE-501, MER-QUOTE-502, MER-QUOTE-503
            = 3

Accepted sent quotes = MER-QUOTE-501 and MER-QUOTE-503
                     = 2

Acceptance rate
= 2 / 3 × 100
= 66.67%
MER-QUOTE-504 is not sent and is excluded from the denominator.
Receivable metric
Invoice total
= 6,400 + 3,900
= USD 10,300

Payment total
= 6,400 + 3,800
= USD 10,200

Credit adjustments = USD 0

Open receivable
= 10,300 − 10,200
= USD 100
Service metric
Eligible tickets:
- MER-TKT-601;
- MER-TKT-602;
- MER-TKT-603.
Tickets meeting target:
- MER-TKT-601;
- MER-TKT-603.
First-response attainment
= 2 / 3 × 100
= 66.67%
MER-TKT-604 is excluded from the denominator and shown in the data-exception report.
Dashboard artifact
Card	Expected result
Sent quotes	3
Quote acceptance rate	66.67%
Open receivables	USD 100
Eligible tickets	3
SLA attainment	66.67%
Reconciliation exceptions	1
A valid alternative is to show eligible and ineligible ticket counts together, provided the attainment denominator remains clear.
9.3 Independent challenge sample solution
Quote acceptance
Sent quotes:
- MER-QUOTE-601;
- MER-QUOTE-602;
- MER-QUOTE-603.
Accepted sent quotes:
- MER-QUOTE-601;
- MER-QUOTE-603.
Acceptance rate
= 2 / 3 × 100
= 66.67%
MER-QUOTE-604 is Draft and excluded.
Finance reconciliation
Invoice total
= 3,000 + 5,600
= USD 8,600

Payment total
= 3,000 + 5,500
= USD 8,500

Credit adjustments = USD 0

Open receivable
= 8,600 − 8,500
= USD 100
MER-INVOICE-603 is the discrepancy because the invoice is USD 5,600 and payment is USD 5,500. The expected source quote total is USD 5,500, so the invoice is USD 100 higher than the source and also has a USD 100 open balance.
The dashboard should show:
- invoice amount;
- expected quote amount;
- payment;
- adjustment;
- open balance;
- reconciliation status.
Service attainment
Eligible tickets:
- MER-TKT-701;
- MER-TKT-702;
- MER-TKT-703.
Tickets meeting target:
- MER-TKT-701;
- MER-TKT-703.
Service attainment
= 2 / 3 × 100
= 66.67%
MER-TKT-704 is shown as a data exception because customer context is missing.
Duplicate-total demonstration
MER-QUOTE-601 has two lines, but the quote total is USD 3,000.
Incorrect join result:
3,000 + 3,000 = USD 6,000
Correct result:
Quote total at quote grain = USD 3,000
Line total at line grain = 2,000 + 1,000 = USD 3,000
A corrected design keeps quote totals and line extensions in separate measures or aggregates the line table before joining.
Sharing matrix
Audience	Access
Sales	Quote report and acceptance dashboard
Finance	Invoice reconciliation and receivable dashboard
Service	Ticket and SLA dashboard
Operations leadership	Combined summary without confidential employee data
HR	Separate restricted employee dashboard
Sales representative	No access to raw employee or finance-payment tables
10. Chapter recap and next step
Reporting is reliable when its data grain, relationships, formulas, access and refresh behavior are explicit.
You should now be able to:
- distinguish reports, pivots and dashboards;
- connect source applications through controlled connectors;
- state the grain of every reporting table;
- define relationships using stable keys;
- prevent duplicated totals after one-to-many joins;
- write formulas with units, denominators and exclusions;
- create dashboard cards, filters and exception reports;
- configure sharing for different audiences;
- record refresh and connector status;
- reconcile dashboard totals to source records;
- keep employee data separate from shared operational dashboards.
For the Meridian Supply project, this chapter produces:
C01_CH17_Meridian_Analytics_Source_and_Grain_Register
C01_CH17_Meridian_Analytics_Relationship_and_Metric_Dictionary
C01_CH17_Meridian_Operations_Dashboard
C01_CH17_Meridian_Source_Reconciliation
C01_CH17_Meridian_Dashboard_Sharing_and_Refresh_Record
The next chapter covers testing, rollout and administration. It builds on the need to test reports, permissions, refresh, configuration records, user instructions and controlled improvements.
11. Glossary and further reading
Glossary
Term	Definition
Connector	Mechanism that imports or synchronizes source data into an analytical system
Dashboard	Collection of related reports, measures and filters for an audience
Data grain	Statement describing what one row represents
Formula	Calculation based on defined fields, units and conditions
Metric definition	Specification of a metric’s purpose, grain, formula, denominator, exclusions and source
Pivot report	Report that groups measures across row and column dimensions
Refresh	Update of analytical data from source systems
Relationship	Defined connection between records in two tables
Reconciliation	Comparison between report values and independently calculated source values
Report	Structured answer to a defined business question
Row-level access	Permission that restricts which records a user may see
Source of truth	Application or record type treated as authoritative for a data element
One-to-many join	Relationship where one parent record connects to several child records
Further reading
Check the current Zoho Analytics edition, connectors, relationships, formulas, refresh behavior, dashboards, filters and sharing controls before implementation:
- Zoho Analytics Help (https://help.zoho.com/portal/en/kb/analytics)
- Zoho Analytics documentation (https://www.zoho.com/analytics/help/)
- Zoho CRM Help (https://help.zoho.com/portal/en/kb/crm)
- Zoho Books Help (https://help.zoho.com/portal/en/kb/books)
- Zoho Desk Help (https://help.zoho.com/portal/en/kb/desk)
- Zoho People Help (https://help.zoho.com/portal/en/kb/people)
This chapter has not verified current Zoho Analytics connectors, relationship behavior, formula features, refresh schedules, filter scope, sharing permissions or row-level security in a live environment. Synthetic dashboard results are expected learning outputs, not product execution observations.
continuity:
  previous_continuity:
    supplied: "C01-CH16"
    source_artifacts:
      - "C01_CH16_Meridian_Employee_Record_and_Access_Design"
      - "C01_CH16_Meridian_Onboarding_State_and_Checklist"
      - "C01_CH16_Meridian_Employee_Document_and_Case_Register"
      - "C01_CH16_Meridian_Leave_Approval_and_Exception_Design"
      - "C01_CH16_Meridian_People_Test_and_Confidentiality_Evidence"
    note: "Continuity from C01-CH02 through C01-CH08 was not supplied; no decisions from those chapters are assumed."
  record_ids:
    inherited:
      - MER-ENQ-001
      - MER-CUST-001
      - MER-QUOTE-001
      - MER-ENQ-002
      - MER-ENQ-003
      - MER-ENQ-004
      - MER-CUST-002
      - MER-QUOTE-002
      - MER-ENQ-101
      - MER-ENQ-102
      - MER-ENQ-103
      - MER-ENQ-104
      - MER-ENQ-105
      - MER-ENQ-201
      - MER-ENQ-202
      - MER-ENQ-203
      - MER-ENQ-204
      - MER-ENQ-205
      - MER-QUOTE-003
      - MER-QUOTE-004
      - MER-QUOTE-101
      - MER-QUOTE-102
      - MER-QUOTE-103
      - MER-QUOTE-104
      - MER-QUOTE-105
      - MER-CUST-101
      - MER-QUOTE-201
      - MER-QUOTE-202
      - MER-QUOTE-203
      - MER-QUOTE-204
      - MER-SVC-301
      - MER-SVC-302
      - MER-SVC-303
      - MER-SVC-304
      - MER-PROD-WS-001
      - MER-PROD-INST-001
      - MER-PROD-SUP-001
      - MER-PROD-DOCK-001
      - MER-PROD-MON-001
      - MER-PB-STD-2026
      - MER-PB-PARTNER-2026
      - MER-QUOTE-301
      - MER-QUOTE-302
      - MER-QUOTE-303
      - MER-QUOTE-304
      - MER-CUST-301
      - MER-CUST-302
      - MER-CUST-303
      - MER-CUST-304
      - MER-QUOTE-401
      - MER-QUOTE-402
      - MER-QUOTE-403
      - MER-QUOTE-404
      - MER-CUST-401
      - MER-CUST-402
      - MER-CUST-403
      - MER-CUST-404
      - MER-BOOK-CUST-101
      - MER-BOOK-CONTACT-101
      - MER-BOOK-QUOTE-101
      - MER-ITEM-WS-001
      - MER-ITEM-INST-001
      - MER-ITEM-SUP-001
      - MER-ORDER-101
      - MER-INVOICE-101
      - MER-PAY-101
      - MER-ADJ-101
      - MER-BOOK-CUST-301
      - MER-BOOK-CONTACT-301
      - MER-ORDER-301
      - MER-INVOICE-301
      - MER-PAY-301
      - MER-ADJ-301
      - MER-BOOK-CUST-401
      - MER-ORDER-401
      - MER-INVOICE-401
      - MER-PAY-401
      - MER-HO-101
      - MER-HO-102
      - MER-QUOTE-FLOW-102
      - MER-HO-201
      - MER-HO-202
      - MER-HO-203
      - MER-HO-204
      - MER-ORDER-203
      - MER-ITEM-DOCK-001
      - MER-PAY-402
      - MER-PAY-403
      - MER-PAY-404
      - MER-INVOICE-402
      - MER-INVOICE-403
      - MER-INVOICE-404
      - MER-TKT-301
      - MER-TKT-302
      - MER-TKT-303
      - MER-TKT-304
      - MER-TKT-401
      - MER-TKT-402
      - MER-TKT-403
      - MER-TKT-404
      - MER-TKT-405
      - MER-TKT-501
      - MER-TKT-502
      - MER-TKT-503
      - MER-TKT-504
      - MER-TKT-505
      - MER-KB-001
      - MER-KB-101
      - MER-KB-201
      - MER-EMP-001
      - MER-EMP-002
      - MER-EMP-003
      - MER-MGR-001
      - MER-MGR-002
      - MER-MGR-003
      - MER-DOC-001
      - MER-DOC-002
      - MER-DOC-003
      - MER-DOC-004
      - MER-DOC-005
      - MER-TASK-001
      - MER-TASK-002
      - MER-TASK-003
      - MER-TASK-004
      - MER-TRAIN-002
      - MER-EMP-101
      - MER-EMP-102
      - MER-EMP-103
      - MER-MGR-OPS
      - MER-MGR-SALES
      - MER-MGR-TECH
      - MER-LEAVE-201
      - MER-LEAVE-202
      - MER-LEAVE-203
      - MER-LEAVE-204
      - MER-LEAVE-205
      - MER-EMP-201
      - MER-EMP-202
      - MER-EMP-203
      - MER-EMP-204
      - MER-EMP-205
    added_for_reporting_practice:
      - MER-QUOTE-202
      - MER-ENQ-301
      - MER-ENQ-401
      - MER-ENQ-404
      - MER-QUOTE-501
      - MER-QUOTE-502
      - MER-QUOTE-503
      - MER-QUOTE-504
      - MER-INVOICE-501
      - MER-INVOICE-503
      - MER-TKT-601
      - MER-TKT-602
      - MER-TKT-603
      - MER-TKT-604
      - MER-QUOTE-601
      - MER-QUOTE-602
      - MER-QUOTE-603
      - MER-QUOTE-604
      - MER-INVOICE-601
      - MER-INVOICE-603
      - MER-TKT-701
      - MER-TKT-702
      - MER-TKT-703
      - MER-TKT-704
  case_decisions:
    - "The shared operations dashboard uses separate quote, invoice and ticket fact tables with declared grain."
    - "Quote acceptance rate uses accepted sent quotes divided by sent quotes."
    - "Open receivables are calculated at invoice grain before any one-to-many joins."
    - "Service first-response attainment excludes tickets without valid eligibility evidence and reports them separately."
    - "Quote, invoice and payment amounts must not be summed after uncontrolled one-to-many joins."
    - "Employee data is excluded from the shared operations dashboard and belongs in a restricted reporting model."
    - "Every metric includes a source, formula, denominator, exclusions, time zone and refresh definition."
    - "No live Zoho Analytics connector, refresh, sharing or dashboard behavior has been verified."
  artifacts:
    - "C01_CH17_Meridian_Analytics_Source_and_Grain_Register"
    - "C01_CH17_Meridian_Analytics_Relationship_and_Metric_Dictionary"
    - "C01_CH17_Meridian_Operations_Dashboard"
    - "C01_CH17_Meridian_Source_Reconciliation"
    - "C01_CH17_Meridian_Dashboard_Sharing_and_Refresh_Record"
  open_case_assumptions_next_chapter:
    - "The exact current Zoho Analytics connectors, formulas, refresh behavior and sharing controls must be verified."
    - "The next chapter should use dashboard reconciliation and source ownership when preparing testing and rollout evidence."
    - "Any combined CRM, Books, Desk and People report must preserve grain, confidentiality and record-level traceability."
    - "Metric definitions must be approved before a dashboard is used for operational decisions."
END OF C01-CH17
