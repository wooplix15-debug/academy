# Books and the Sales-to-Finance Handoff

1. What you will learn
A sales process is not complete when a quote is accepted. Finance must receive information that is accurate, complete, correctly mapped and usable in the finance system.
This chapter follows a commercial record from a CRM quote through finance records and payment. You will learn to distinguish a sales record from a finance record and to investigate differences rather than assuming that synchronisation succeeded.
You will learn to:
- distinguish customers, contact persons, items, quotes, orders, invoices and payments;
- understand receivables and outstanding balances;
- record adjustments without hiding the original transaction;
- define tax and currency assumptions;
- map CRM records and fields to Books records and fields;
- understand synchronisation direction, status and failure recovery;
- reconcile quote, order, invoice, payment and adjustment amounts;
- investigate a discrepancy using complete source records;
- document a finance handoff and its receiving evidence;
- test normal, missing-data, permission and failed-handoff scenarios.
This chapter continues the Meridian Supply commercial records from Chapter 12. The supplied continuity establishes:
- MER-QUOTE-101 is a USD quote for MER-CUST-101;
- the quote uses MER-PB-STD-2026;
- its three lines are 10 workstations, one installation service and one support plan;
- the subtotal is USD 6,800.00;
- the approved quote-level discount is 12%, or USD 816.00;
- the total before tax is USD 5,984.00;
- tax is excluded from the synthetic case;
- the quote has been accepted by the customer;
- finance acceptance has not previously been established.
This chapter introduces an explicit new case decision: finance accepts the complete handoff for MER-QUOTE-101. That is a new scenario event, not an earlier observation.
No product execution has been verified. Exact Zoho Books and CRM navigation, synchronisation behavior, tax features, currency settings and permission names depend on the current edition and organisation configuration.
2. Lessons
2.1 How commercial and finance records relate
Finance records have different meanings from sales records.
Record	Main question	Meridian example
Customer	Who is the organisation buying or owing money?	MER-CUST-101
Contact person	Which person communicates for the customer?	Aisha Green
Item	What product or service is being sold in the finance system?	Finance item for a workstation
Quote	What commercial offer was made?	MER-QUOTE-101
Sales order	What accepted commercial request is being fulfilled?	MER-ORDER-101
Invoice	What amount is recorded as owed?	MER-INVOICE-101
Payment	What money was received and applied?	MER-PAY-101
Receivable	What remains owed after payments and adjustments?	Open balance on an invoice
Adjustment	A controlled correction or credit/debit applied to a balance	MER-ADJ-101
A quote may be prepared in CRM, while the invoice and payment are recorded in Books. The two records must be linked without treating them as the same record.
Customer and contact person
A customer is the business relationship. A contact person is an individual associated with that customer.
A customer may have several contact persons:
- purchasing contact;
- finance contact;
- installation contact;
- service contact.
Do not create a new customer merely because a different contact person sends an enquiry. Search for the existing customer and add or associate the contact according to the approved duplicate rule.
Item
A finance item corresponds to a product or service that can appear on an order or invoice. It may map from a CRM product, but the two records can have different IDs and descriptions.
For example:
CRM product	Books item	Relationship
MER-PROD-WS-001	MER-ITEM-WS-001	Same business product, separate application records
MER-PROD-INST-001	MER-ITEM-INST-001	Same installation service
MER-PROD-SUP-001	MER-ITEM-SUP-001	Same support plan
The mapping should be explicit. Matching by product name alone is unsafe when names change or contain spelling variations.
Check your understanding
Why should a contact person record not automatically create a new customer?
Answer: Several people may represent the same customer. Creating a new customer for each contact creates duplicates and can split quotes, invoices, payments and receivables across incorrect records.
2.2 Quotes, orders and invoices
A quote is a proposal. An order is an accepted request to supply or fulfil something. An invoice records an amount owed to finance.
The exact relationship depends on the organisation’s design. A possible sequence is:
CRM quote
    ↓ customer acceptance
Sales order
    ↓ fulfilment or finance processing
Invoice
    ↓ payment
Receivable balance
A quote may be accepted without immediately creating an order. An order may be created without being fully invoiced. An invoice may be issued in stages. These distinctions must be defined rather than assumed.
Required links
A finance handoff should preserve:
- CRM customer ID;
- CRM contact reference;
- CRM quote ID;
- product or item mapping;
- price-book reference;
- currency;
- line quantities;
- applied unit prices;
- discounts;
- total;
- approval evidence;
- customer acceptance evidence.
The receiving finance record should have its own business ID or product-generated ID. Store it as a separate reference.
Meridian record relationships
Sales-side record	Finance-side record	Mapping requirement
MER-CUST-101	MER-BOOK-CUST-101	Customer business ID and finance customer code
Aisha Green	MER-BOOK-CONTACT-101	Contact email and customer association
MER-PROD-WS-001	MER-ITEM-WS-001	Product-to-item mapping
MER-QUOTE-101	MER-BOOK-QUOTE-101	Quote reference and source system
Accepted quote	MER-ORDER-101	Quote ID and order reference
Order	MER-INVOICE-101	Order reference and invoice reference
Invoice	MER-PAY-101	Invoice reference and payment allocation
Check your understanding
Why should the Books invoice store the CRM quote ID?
Answer: The CRM quote ID allows finance and sales to trace the invoice back to the commercial offer, products, discounts and approval evidence. It also supports discrepancy investigation.
2.3 Payments and receivables
A payment is not automatically applied to the correct invoice. A payment may be:
- fully applied;
- partially applied;
- unapplied;
- applied to the wrong invoice;
- recorded in the wrong currency;
- duplicated;
- reversed or refunded.
A basic open-balance formula is:
Open receivable
= invoice amount
− applied payments
− approved credit adjustments
+ approved debit adjustments
The sign of an adjustment must be defined. In this chapter, a credit adjustment reduces the receivable.
Example
Invoice amount = USD 6,800.00
Applied payment = USD 5,984.00
Credit adjustment = USD 816.00

Open receivable
= 6,800.00 − 5,984.00 − 816.00
= USD 0.00
A payment received does not prove that the invoice is settled until the payment is correctly allocated and any approved adjustment is recorded.
Payment allocation
When reconciling a payment, verify:
- payment reference;
- payer;
- currency;
- amount received;
- receipt date;
- invoice applied;
- amount applied;
- unapplied amount;
- reversal or refund status.
Do not infer that a payment belongs to the oldest invoice unless that is an explicit finance policy.
Adjustments
An adjustment should preserve the original amount and record:
- adjustment ID;
- reason;
- amount;
- linked invoice;
- authorised person;
- date;
- approval or evidence;
- effect on the receivable.
An adjustment is not a way to hide a mapping error. First identify the cause. Then apply an authorised correction if the business decision requires it.
Check your understanding
An invoice is USD 6,800 and payment is USD 5,984. What is the balance before any adjustment?
Answer:
6,800 − 5,984 = USD 816
The balance is USD 816. An approved credit adjustment of USD 816 would reduce the balance to zero.
2.4 Tax and currency settings
Tax and currency settings affect commercial records and reconciliation. They must be defined before synchronisation.
Currency
At minimum, document:
- quote currency;
- price-book currency;
- customer or finance currency;
- invoice currency;
- payment currency;
- exchange-rate source and date if currencies differ;
- rounding rule;
- handling of currency changes after quote approval.
The simplest Meridian learning case uses USD throughout. This avoids foreign-exchange calculations but does not demonstrate multi-currency behavior.
If a quote is in EUR and an invoice is in USD, reconciliation needs:
- original amount and currency;
- converted amount and currency;
- exchange rate;
- rate date;
- rounding;
- whether the payment was received in the invoice currency.
Do not convert currencies using an unexplained current rate after the fact.
Tax
The case in this chapter excludes tax. That means:
Tax amount = USD 0.00 for the synthetic calculation
This does not establish a tax treatment for a real business. A real configuration must confirm:
- tax registration and applicable rules;
- customer tax treatment;
- product or item tax category;
- tax region;
- tax-inclusive or tax-exclusive pricing;
- rounding;
- tax account mapping;
- invoice display requirements.
A blank tax field can mean:
- tax is intentionally excluded;
- tax was not configured;
- required tax data is missing;
- the synchronisation omitted the field.
The system should not silently treat all blank tax values as the same business meaning.
Check your understanding
Why is a USD quote and a EUR payment not automatically a zero-balance payment?
Answer: The currencies differ. The finance process needs an exchange rate, rate date, converted amount, rounding rule and payment allocation before the balance can be calculated.
2.5 Mappings and synchronisation
A mapping states how a source field or record becomes a target field or record.
A useful mapping table includes:
- source application;
- source record and field;
- target application;
- target record and field;
- transformation;
- required or optional status;
- owner;
- exception behavior.
Meridian mapping example
Source	Source field	Target	Target field	Transformation
CRM	Customer ID	Books customer	Customer code or reference	Preserve business ID
CRM	Contact email	Books contact person	Email	Validate format
CRM	Product ID	Books item	Item code	Use approved product map
CRM	Quote ID	Books quote/order	Reference number	Preserve source ID
CRM	Currency	Books transaction	Currency	Exact code match
CRM	Quantity	Books line item	Quantity	Numeric value, positive
CRM	Applied unit price	Books line item	Rate	Preserve approved price
CRM	Discount amount	Books transaction	Discount	Map quote or line basis explicitly
Books	Invoice ID	CRM finance reference	Finance reference	Store target business ID
Books	Payment status	CRM handoff	Finance status	Controlled value mapping
Synchronisation direction
Record which side is authoritative:
- CRM may be authoritative for enquiry, customer context, quote and sales ownership.
- Books may be authoritative for finance customer code, item accounting data, invoice, payment and receivable.
- A returned finance handoff should update the CRM process state without allowing an uncontrolled overwrite of finance records.
Synchronisation may be:
- one-way;
- two-way;
- scheduled;
- event-driven;
- manually initiated.
The design must define duplicate prevention and update behavior. A repeated synchronisation should not create a second customer, order or invoice for the same business event.
Sync status
Useful controlled statuses include:
Not started
Ready
Sent
Accepted
Returned
Failed
Reconciled
Sent does not mean Accepted. Failed requires an error or exception record. Reconciled requires comparison evidence.
Check your understanding
What is wrong with mapping a CRM quote discount to a finance field without stating whether it is a percentage or amount?
Answer: The target may interpret the value incorrectly. A value of 12 could mean 12%, USD 12 or another unit. The mapping must define field meaning, unit and transformation.
2.6 Reconciliation
Reconciliation compares records from different sources and explains differences.
A reconciliation should compare at least:
- source quote;
- source order or handoff;
- target order;
- target invoice;
- payments;
- adjustments;
- open receivable;
- IDs and currencies.
Reconciliation levels
1. Record-level: Does each source record have the correct target record?
2. Line-level: Do products, quantities, prices and discounts match?
3. Amount-level: Do subtotal, discount, tax, total, payment and balance match?
4. Status-level: Do acceptance, invoice and payment states match the evidence?
5. Timing-level: Are event timestamps available? Do not infer that targets were met without target and observed times.
Difference formula
Difference
= observed target amount − expected source amount
For Meridian:
Observed invoice = USD 6,800.00
Expected invoice = USD 5,984.00

Difference
= 6,800.00 − 5,984.00
= USD 816.00
The reconciliation result should identify whether the difference is caused by:
- missing discount mapping;
- wrong price book;
- quantity mismatch;
- product mapping;
- tax treatment;
- currency conversion;
- duplicate line;
- payment allocation;
- authorised adjustment;
- manual correction.
Do not fix a difference by changing the source quote unless the source quote itself is wrong and an authorised correction process exists.
Check your understanding
A source quote is USD 5,984, an invoice is USD 6,800 and a payment is USD 5,984. What should reconciliation investigate first?
Answer: It should compare the quote lines, discount and invoice mapping. The invoice is USD 816 higher than the approved quote, and the payment matches the quote rather than the invoice.
2.7 Configuring the sales-to-finance handoff
This procedure uses common CRM and Books concepts. Exact Zoho screens, synchronisation options, tax settings and permissions must be verified in the current edition.
Required access
You need suitable access to:
- view and update CRM customers, contacts, products and quotes;
- view the approved quote and its line items;
- create or update Books customers and contact persons;
- create or update Books items;
- configure or inspect quote, order, invoice and payment records;
- configure mappings or synchronisation connections;
- view sync history and errors;
- record adjustments or credit notes where authorised;
- reconcile records;
- test as sales, finance processor and finance manager.
Procedure
1. Confirm the source quote.
Verify customer, contact, quote ID, approval, acceptance, product lines, prices, discounts, currency and total.
Expected result: A complete source record exists.
2. Confirm customer mapping.
Match the customer by approved business ID and verify the contact person.
Expected result: One target customer and the correct contact association exist.
3. Confirm item mapping.
Match every CRM product to one finance item.
Expected result: No line item depends only on a product name.
4. Confirm currency and tax assumptions.
Verify currency code, tax basis and rounding.
Expected result: Source and target calculations use the same declared basis.
5. Create or inspect the target quote or order.
Preserve the CRM quote ID and applied prices.
Expected result: The target transaction can be traced to the source.
6. Create or inspect the invoice.
Compare quantities, prices, discounts, tax and total.
Expected result: Invoice amount agrees with the approved commercial record or has an explained difference.
7. Record or inspect payment.
Verify amount, currency, payer and invoice allocation.
Expected result: Payment status and open receivable are calculable.
8. Reconcile.
Compare source, target, payment and adjustment records.
Expected result: The difference is zero or has a documented explanation and authorised correction.
 9. Recover exceptions.
Return missing or invalid mappings to the responsible owner. Do not create a duplicate record to bypass an error.
Expected result: The correction can be retried without losing the original evidence.
10. Document support ownership.
Record who owns CRM data, Books data, mappings, tax settings, payments and reconciliation.
Expected result: A future discrepancy has a named resolver.
3. Visual explanation
flowchart LR
    CRMCustomer[CRM customer and contact] --> MapCustomer[Customer mapping]
    CRMQuote[Approved CRM quote] --> MapQuote[Quote and line mapping]
    CRMProducts[CRM products] --> MapItems[Product to finance item mapping]
    MapCustomer --> BooksCustomer[Books customer and contact]
    MapItems --> BooksItems[Books items]
    MapQuote --> BooksOrder[Books order or finance transaction]
    BooksOrder --> BooksInvoice[Books invoice]
    BooksInvoice --> Payment[Payment allocation]
    Payment --> Receivable[Open receivable]
    BooksInvoice --> Reconcile[Reconciliation]
    Payment --> Reconcile
    CRMQuote --> Reconcile
    Reconcile -->|Difference found| Adjustment[Approved adjustment or correction]
    Adjustment --> Receivable
The diagram shows that reconciliation compares multiple records. A payment cannot be interpreted without the invoice it was applied to. An invoice cannot be evaluated without the approved quote and line-item mapping.
4. Worked case: Meridian quote to payment
4.1 New scenario decision
For this chapter, Meridian finance accepts the complete handoff for MER-QUOTE-101 at 2026-10-16 09:00. This is an explicit new scenario event.
The finance handoff contains:
- customer ID MER-CUST-101;
- quote ID MER-QUOTE-101;
- three item mappings;
- USD currency;
- subtotal USD 6,800.00;
- approved quote discount USD 816.00;
- expected total USD 5,984.00.
4.2 Source and target records
Record type	Business ID	Amount or value	Status
CRM quote	MER-QUOTE-101	USD 5,984.00	Customer Accepted
Finance customer	MER-BOOK-CUST-101	—	Active
Finance contact	MER-BOOK-CONTACT-101	—	Active
Finance order	MER-ORDER-101	USD 5,984.00	Accepted
Finance invoice	MER-INVOICE-101	USD 6,800.00	Open
Payment	MER-PAY-101	USD 5,984.00	Applied
Adjustment	MER-ADJ-101	USD 816.00 credit	Proposed for correction
The invoice amount is intentionally inconsistent with the approved quote. It omits the USD 816 discount.
4.3 Mapping evidence
Source record or field	Target record or field	Supplied mapping result
MER-CUST-101	MER-BOOK-CUST-101	Mapped
Aisha Green	MER-BOOK-CONTACT-101	Mapped
MER-PROD-WS-001	MER-ITEM-WS-001	Mapped
MER-PROD-INST-001	MER-ITEM-INST-001	Mapped
MER-PROD-SUP-001	MER-ITEM-SUP-001	Mapped
MER-QUOTE-101	MER-ORDER-101	Mapped
Quote discount amount USD 816	Invoice discount	Not mapped
CRM currency USD	Finance currency USD	Mapped
The missing discount mapping explains the amount difference.
4.4 Reconciliation calculation
Expected invoice:
Approved quote total = USD 5,984.00
Expected invoice = USD 5,984.00
Observed invoice:
Invoice amount = USD 6,800.00
Difference:
Difference
= observed invoice − expected invoice
= 6,800.00 − 5,984.00
= USD 816.00
Receivable before adjustment:
Invoice = USD 6,800.00
Payment applied = USD 5,984.00

Open receivable
= 6,800.00 − 5,984.00
= USD 816.00
Synthetic recovery choice:
Credit adjustment = USD 816.00
Open receivable after adjustment
= 6,800.00 − 5,984.00 − 816.00
= USD 0.00
The adjustment should be authorised by the finance owner and linked to the approved quote and invoice. This is a case recovery choice, not a universal accounting instruction.
4.5 Completed reconciliation artifact
Check	Expected	Observed	Difference	Finding
Customer mapping	MER-CUST-101	MER-BOOK-CUST-101	None	Correct
Contact mapping	Aisha Green	Aisha Green	None	Correct
Workstation lines	10 at USD 520	10 at USD 520	None	Correct
Installation line	1 at USD 1,200	1 at USD 1,200	None	Correct
Support line	1 at USD 400	1 at USD 400	None	Correct
Quote discount	USD 816	USD 0	USD 816	Missing discount mapping
Invoice total	USD 5,984	USD 6,800	USD 816	Incorrect target total
Payment	USD 5,984	USD 5,984	None	Matches approved quote
Balance after proposed credit	USD 0	USD 816 before credit	USD 816	Credit adjustment required if authorised
4.6 Mistake and correction
Mistake: A learner concludes that the customer underpaid USD 816 because the invoice shows an open balance.
Why it is wrong: The payment matches the approved quote. The invoice is higher because the discount was omitted during the handoff.
Correction:
1. preserve the source quote and payment;
2. identify the missing discount mapping;
3. notify the finance owner;
4. correct the mapping for future transactions;
5. apply an authorised credit adjustment or other approved correction to the affected invoice;
6. reconcile again;
7. record the final balance.
Do not alter the approved CRM quote to match the incorrect invoice.
5. Try it yourself — guided practice
Learning goal
Trace a quote through customer mapping, item mapping, order, invoice, payment and receivable. Investigate one discrepancy.
Required access
You need:
- read access to the CRM quote and line items;
- access to the finance customer, item, order, invoice and payment records;
- access to mapping and synchronisation history;
- permission to prepare, but not necessarily approve, an adjustment;
- sales and finance test roles.
Complete source data
Field	Value
CRM quote	MER-QUOTE-301
CRM customer	MER-CUST-301
Contact	Ava Ross
Email	ava@ridgeway.example.com
Currency	USD
Approved quote total	USD 4,153.60
Approval	Approved
Customer acceptance	Recorded
Tax	Excluded
Quote lines:
Product ID	Quantity	Unit price	Line extension
MER-PROD-WS-001	6	520.00	3,120.00
MER-PROD-INST-001	1	1,200.00	1,200.00
MER-PROD-SUP-001	1	400.00	400.00
Quote calculation:
Subtotal = 3,120 + 1,200 + 400
         = USD 4,720.00

Discount = 4,720 × 0.12
         = USD 566.40

Approved total = 4,720 − 566.40
               = USD 4,153.60
Finance records:
Record	Business ID	Amount	Status
Finance customer	MER-BOOK-CUST-301	—	Active
Finance contact	MER-BOOK-CONTACT-301	—	Active
Finance order	MER-ORDER-301	4,153.60	Accepted
Finance invoice	MER-INVOICE-301	4,153.60	Open
Payment	MER-PAY-301	4,000.00	Applied
Credit adjustment	MER-ADJ-301	100.00	Approved
Payment allocation:
Payment applied to MER-INVOICE-301 = USD 4,000.00
Mapping data
CRM product	Books item	Mapping status
MER-PROD-WS-001	MER-ITEM-WS-001	Mapped
MER-PROD-INST-001	MER-ITEM-INST-001	Mapped
MER-PROD-SUP-001	MER-ITEM-SUP-001	Mapped
MER-PROD-DOCK-001	Blank	Missing mapping
Guided steps and expected results
Step 1: Verify the source quote
Confirm customer, contact, quote ID, currency, products, discount and approved total.
Expected result: The source total is USD 4,153.60.
Step 2: Verify customer and contact mapping
Confirm that MER-CUST-301 maps to MER-BOOK-CUST-301 and that Ava Ross is associated with that customer.
Expected result: No duplicate customer or unassociated contact is found.
Step 3: Verify item mappings
Compare each quote product with its Books item.
Expected result: All three products on MER-QUOTE-301 are mapped. The missing docking-station mapping is an exception for another potential quote.
Step 4: Trace order and invoice
Compare MER-ORDER-301 and MER-INVOICE-301 to the approved quote.
Expected result: Order and invoice totals agree with the approved quote.
Step 5: Reconcile payment
Calculate:
Invoice = USD 4,153.60
Payment = USD 4,000.00
Credit adjustment = USD 100.00

Open receivable
= 4,153.60 − 4,000.00 − 100.00
= USD 53.60
Expected result: USD 53.60 remains open.
Step 6: Investigate the discrepancy
The source quote and invoice agree. The difference is caused by a payment of USD 4,000 and a credit adjustment of USD 100, which together are USD 53.60 short of the invoice.
Expected result: The discrepancy is a remaining receivable, not a quote-to-invoice mapping error.
Step 7: Test permission handling
Use a sales role to attempt to edit the invoice amount.
Expected result: The sales user cannot alter the finance invoice. The issue is routed to finance.
Step 8: Test a failed handoff
Create a synthetic quote containing MER-PROD-DOCK-001, which has no Books item mapping.
Expected result: The handoff is held or reported as failed; a finance item mapping must be supplied before retry.
Final artifact
Your submission should contain:
Artifact	Minimum content
Handoff trace	Source quote, customer, contact, item, order and invoice references
Mapping table	Source fields, target fields, transformation and owner
Reconciliation table	Expected, observed, difference and finding
Payment allocation	Amount, invoice and applied balance
Adjustment register	ID, amount, reason, authority and linked invoice
Exception record	Missing item mapping and recovery
Permission test	User role, attempted action and result
Safe cleanup
Use synthetic finance records and test mappings. Do not delete real invoices, payments or customer records. Record any test adjustment clearly as training data and reverse it only through an authorised finance process.
Offline alternative
A spreadsheet can trace mappings and calculate receivables. It cannot demonstrate actual synchronisation, Books permissions, invoice creation, payment allocation or adjustment history.
6. Independent challenge
Partner quote-to-payment reconciliation
Use the Partner quotation from Chapter 12.
Complete source data
Field	Value
CRM quote	MER-QUOTE-401
Customer	MER-CUST-401
Contact	Elena Cruz
Email	elena@oakridge.example.com
Price book	MER-PB-PARTNER-2026
Currency	USD
Approved quote total	USD 8,017.10
Tax	Excluded
Approval	Sales manager approved
The approved calculation is:
Monitor lines after 2% line discount = USD 4,410.00
Docking-station lines = USD 3,300.00
Installation = USD 1,100.00

Subtotal after line discounts = USD 8,810.00
Quote discount at 9% = USD 792.90
Approved total = USD 8,017.10
Finance records
Record	Business ID	Amount	Status
Finance customer	MER-BOOK-CUST-401	—	Active
Finance order	MER-ORDER-401	8,900.00	Accepted
Finance invoice	MER-INVOICE-401	8,900.00	Open
Payment	MER-PAY-401	8,017.10	Applied
Adjustment	None	0.00	None
Mapping evidence
Source field	Target field	Supplied result
Customer ID	Books customer code	Mapped
Partner item IDs	Books item codes	Mapped
Line discount 2%	Finance line discount	Not mapped
Quote discount 9%	Finance quote discount	Not mapped
Currency USD	Finance currency	Mapped
Quote total	Order total	Source says 8,017.10; target says 8,900.00
Deliverables
Create:
1. a source-to-target trace;
2. a line-level reconciliation;
3. an amount discrepancy calculation;
4. a root-cause finding;
5. a recovery recommendation;
6. a mapping correction;
7. a payment and receivable calculation;
8. a permission and failed-handoff test.
Success criteria
Your work should:
- calculate the expected total as USD 8,017.10;
- identify the target amount as USD 8,900.00;
- calculate the USD 882.90 difference;
- explain that both discounts were omitted from the finance transaction;
- calculate the open receivable after the payment;
- keep the approved CRM quote unchanged;
- distinguish a mapping correction from an authorised financial adjustment.
7. Common problems and recovery
Symptom	Diagnosis	Correction	Verification
A duplicate customer exists in Books	Matching used name only or failed to use the business ID	Review the customer match and consolidate through an authorised process	Trace both records and their transactions
A contact is not associated with the customer	Contact mapping omitted the customer relationship	Correct the association and preserve the contact email	Open the customer and verify the contact
A CRM product has no finance item	Item mapping is incomplete	Create or map the finance item before retrying	Reprocess a synthetic handoff
Invoice total differs from approved quote	Discount, price, quantity, tax or currency mapping differs	Compare line by line and identify the first difference	Reconcile after correction
Payment is received but receivable remains open	Payment is unapplied, partially applied or applied to another invoice	Review allocation and correct through finance process	Recalculate the balance
Payment amount is in another currency	Currency conversion was not recorded	Capture currency, rate, date and converted value	Reconcile in both original and invoice currency
Tax is missing	Tax was intentionally excluded, not configured or omitted	Confirm the case rule and finance tax settings	Compare expected and observed tax basis
Finance user changes the original quote to match invoice	Source and target ownership are confused	Preserve the approved quote and correct the target or issue an authorised adjustment	Compare source history and target history
A handoff is marked Accepted when sync only says Sent	Synchronisation stages were conflated	Separate Sent, Accepted, Failed and Reconciled states	Inspect receiving evidence
A failed item mapping creates a partial invoice	Error handling allowed incomplete creation	Hold the handoff until all required mappings exist	Test an unmapped product
A credit adjustment is used without a reason	Adjustment is hiding a discrepancy	Record reason, authority, invoice and source evidence	Reconcile adjustment to invoice
Sales can edit a finance invoice	Permissions cross the system boundary	Restrict finance records and route corrections to finance	Test sales and finance roles
A price book changes after invoicing	Historical applied price was not preserved	Store transaction-level applied values	Compare original quote and invoice
A payment is counted twice	Duplicate payment or duplicate allocation exists	Compare payment IDs and bank references	Reconcile at payment-record grain
Receivable report does not equal invoice balance	Report includes adjustments, credits or other documents	Define report population and signs	Reproduce the balance from source records
8. Check your understanding
 1. What is the difference between a quote and an invoice?
 2. Why must CRM product IDs and Books item IDs be mapped explicitly?
 3. What is the formula for an open receivable?
 4. A USD 5,984 invoice has a USD 5,000 payment and a USD 500 credit adjustment. What remains open?
 5. Why is Sent different from Accepted in synchronisation?
 6. What information is needed to reconcile a payment?
 7. Why should a quote’s applied price be preserved after a price-book change?
 8. What should happen when a product has no target finance item?
 9. Which system should normally own invoice and payment status in the Meridian design?
10. What is the difference between a credit adjustment and changing the original quote?
11. Why must tax settings be stated even when tax is excluded from the learning case?
12. What is the first calculation in the MER-QUOTE-401 discrepancy?
13. Why should a sales representative be denied permission to edit a finance invoice?
14. What evidence proves that a handoff was reconciled?
15. If an invoice is higher than the quote but the payment matches the quote, what are two likely investigation areas?
9. Solutions and explanations
9.1 Answers to the checks
 1. A quote is a commercial proposal. An invoice is a finance record of an amount owed.
 2. Names can change or be duplicated. Explicit IDs and mappings provide traceability and prevent the wrong finance item from being used.
 3. Open receivable = invoice amount − applied payments − credit adjustments + debit adjustments.
 4. 5,984 − 5,000 − 500 = USD 484 remains open.
 5. Sent means information was transmitted or a request was made. Accepted means the receiving process accepted the record or handoff.
 6. Payment ID, payer, amount, currency, date, invoice allocation, applied amount, unapplied amount and any reversal or refund status.
 7. Otherwise a later catalog change could silently alter the commercial value of an approved quote.
 8. Hold or fail the handoff, identify the missing mapping and create the finance item or approved mapping before retrying.
 9. Books or the selected finance application should own invoice, payment and receivable status.
10. A credit adjustment corrects the balance while preserving the original transaction. Changing the quote changes the commercial source record and may destroy evidence.
11. Tax affects totals, mappings and finance interpretation. Excluding tax in the synthetic case is an explicit assumption, not a real tax decision.
12. Compare the approved source total USD 8,017.10 with the observed target amount USD 8,900.00.
13. Finance records require controlled financial access. Sales may submit or investigate a handoff but should not alter invoice or payment records without authority.
14. Source and target records, amounts, mappings, payment and adjustment evidence have been compared and the result is zero difference or a documented authorised difference.
15. Investigate missing discount or price mapping, and verify whether the invoice used the wrong price book, quantity, currency or tax basis.
9.2 Guided practice sample solution
Handoff trace
Stage	Source or target record	Result
CRM quote	MER-QUOTE-301	Approved total USD 4,153.60
Customer mapping	MER-CUST-301 → MER-BOOK-CUST-301	Correct
Contact mapping	Ava Ross → MER-BOOK-CONTACT-301	Correct
Item mappings	Workstation, installation and support	All mapped
Finance order	MER-ORDER-301	USD 4,153.60
Finance invoice	MER-INVOICE-301	USD 4,153.60
Payment	MER-PAY-301	USD 4,000 applied
Adjustment	MER-ADJ-301	USD 100 credit
Receivable	Invoice less payment and credit	USD 53.60 open
Reconciliation calculation
Invoice = USD 4,153.60
Payment = USD 4,000.00
Credit adjustment = USD 100.00

Open receivable
= 4,153.60 − 4,000.00 − 100.00
= USD 53.60
The invoice agrees with the quote. The discrepancy is not a quote-to-invoice price error. It is a remaining receivable after a partial payment and a USD 100 credit.
Recovery
The finance owner should investigate why the customer paid USD 4,000 rather than USD 4,153.60. Since no authorised waiver for the remaining USD 53.60 is supplied, the expected case result is:
- retain the approved USD 100 adjustment;
- keep the invoice and payment evidence;
- request or record the remaining USD 53.60 according to the organisation’s finance process;
- do not change the CRM quote to USD 4,000.
Permission test
A sales user attempting to edit MER-INVOICE-301 should be denied. The user can report the discrepancy, but finance owns the correction.
Failed handoff
A quote containing MER-PROD-DOCK-001 cannot complete the finance handoff because its Books item mapping is blank. The correct recovery is to create or approve the mapping, verify the item and retry the handoff. Do not create a second customer or quote to avoid the missing mapping.
9.3 Independent challenge sample solution
Expected source calculation
Monitor lines after 2% discount = USD 4,410.00
Docking stations = USD 3,300.00
Installation = USD 1,100.00

Subtotal after line discounts = 4,410 + 3,300 + 1,100
                              = USD 8,810.00

Quote discount = 8,810 × 0.09
               = USD 792.90

Expected approved total
= 8,810 − 792.90
= USD 8,017.10
Difference calculation
Observed invoice = USD 8,900.00
Expected invoice = USD 8,017.10

Difference
= 8,900.00 − 8,017.10
= USD 882.90
The difference equals the total discount that was omitted:
Line discount amount
= 4,500.00 − 4,410.00
= USD 90.00

Quote discount amount
= USD 792.90

Total omitted discounts
= 90.00 + 792.90
= USD 882.90
Receivable calculation
Invoice = USD 8,900.00
Payment = USD 8,017.10
Credit adjustment = USD 0.00

Open receivable
= 8,900.00 − 8,017.10
= USD 882.90
Root cause
The source quote includes:
- a 2% line discount on monitors;
- a 9% quote-level discount after line discounts.
The finance transaction includes neither discount. The target amount equals the undiscounted Partner-price subtotal of USD 8,900.00.
Recovery
1. Preserve the approved CRM quote and its calculation.
2. Correct the mapping for line discounts and quote-level discounts.
3. Confirm how the target application represents both discount types.
4. Ask the finance owner whether the invoice should be corrected through an authorised adjustment or reissued.
5. Apply the approved correction.
6. Reconcile the corrected invoice, payment and receivable.
7. Record the mapping correction so future Partner quotes are not affected.
A valid alternative is to reject the handoff correction and require a new finance transaction if the current invoice cannot be amended, provided the original invoice, payment and correction evidence remain traceable.
10. Chapter recap and next step
The sales-to-finance handoff is a chain of linked records, mappings and decisions. A complete quote is not enough; finance must receive data that can be identified, calculated, accepted and reconciled.
You should now be able to:
- distinguish customers, contact persons, items, quotes, orders, invoices and payments;
- map CRM products to finance items;
- preserve business IDs separately from target-system IDs;
- calculate invoice totals, payments, adjustments and receivables;
- state currency and tax assumptions;
- define source and target ownership;
- distinguish synchronisation states;
- reconcile records at customer, line, amount and payment level;
- identify missing discounts, wrong price books and payment allocation errors;
- recover through an authorised correction without changing source evidence;
- test missing mappings, permission denial and failed handoffs.
For the Meridian Supply project, this chapter produces:
C01_CH13_Meridian_Sales_to_Finance_Mapping
C01_CH13_Meridian_Customer_Contact_and_Item_Crosswalk
C01_CH13_Meridian_Quote_Order_Invoice_Payment_Trace
C01_CH13_Meridian_Reconciliation_and_Discrepancy_Record
C01_CH13_Meridian_Handoff_Exception_and_Recovery_Evidence
The next chapter examines cross-application automation with Flow. It builds on the mappings, handoff states, failure routes and reconciliation evidence created here.
11. Glossary and further reading
Glossary
Term	Definition
Adjustment	Controlled debit or credit applied to a finance balance
Applied payment	Payment amount allocated to a particular invoice
Contact person	Individual associated with a customer
Customer	Business relationship that may have commercial and finance records
Finance item	Product or service record used by the finance application
Invoice	Finance record of an amount owed
Mapping	Definition of how a source record or field corresponds to a target record or field
Open receivable	Amount still owed after applied payments and adjustments
Payment	Money received and recorded for allocation
Price-book mapping	Relationship between a sales pricing context and the commercial record used by finance
Reconciliation	Comparison of related records and amounts to identify and explain differences
Sales order	Record of an accepted commercial request to supply or fulfil
Synchronisation	Transfer or coordinated update of records between applications
Tax basis	Declared treatment of tax in a calculation, such as included, excluded or not supplied
Quote	Commercial proposal containing customer, products, prices, discounts and terms
Further reading
Check current product documentation, edition support, tax and currency features, permissions and synchronisation behavior before configuring a production handoff:
- Zoho Books Help (https://help.zoho.com/portal/en/kb/books)
- Zoho Books sales help (https://help.zoho.com/portal/en/kb/books/sales)
- Zoho Books customer and contact help (https://help.zoho.com/portal/en/kb/books/contacts)
- Zoho Books items help (https://help.zoho.com/portal/en/kb/books/items)
- Zoho Books payments and receivables help (https://help.zoho.com/portal/en/kb/books/sales)
- Zoho CRM Help (https://help.zoho.com/portal/en/kb/crm)
- Zoho CRM developer documentation (https://www.zoho.com/crm/developer/docs/)
This chapter has not verified current Zoho Books screens, CRM-to-Books synchronisation behavior, tax settings, currency handling, payment allocation or permission names in a live environment. Synthetic records and reconciliation results are expected learning outputs, not product execution observations.
