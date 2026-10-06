# Products, Pricing and Commercial Records

1. What you will learn
A commercial process must connect the customer, the quote, the products, the prices, the discounts and the approval decision. If these relationships are unclear, users may quote the wrong price, apply a discount twice or send a quote that was never approved.
In this chapter, you will learn to:
- define products and distinguish them from quote line items;
- use price books to select controlled prices;
- understand the relationships among customers, contacts, quotes, products and line items;
- calculate line extensions, discounts and quote totals;
- distinguish line-level and quote-level discounts;
- design approval controls for discounts and pricing exceptions;
- understand configure-price-quote concepts;
- preserve the price and product information used in a historical quote;
- configure and test a commercial quotation process;
- recover from missing products, invalid price books, incorrect discounts and incomplete approvals.
This chapter continues the Meridian Supply process. The supplied continuity from Chapter 11 establishes:
- guided actions must respect the Blueprint and approval controls;
- Submit for Finance is different from Finance Accepted;
- MER-QUOTE-101 contains a synthetic quote calculation of 10 workstations, installation and a support plan;
- that quote has a 12% discount and an approved state for the guided finance-handoff example;
- the exact current Zoho product, price-book, quote and approval behavior has not been verified in a live environment.
The detailed product and price records in this chapter are new synthetic records or explicit additions to the learning case. They are not universal pricing, tax, accounting or commercial policies.
No coding is required. Product configuration requires suitable CRM administration, catalog, commercial-record and approval permissions. Exact Zoho CRM screens, feature availability, price-book behavior and permission names must be checked in the current product edition.
2. Lessons
2.1 How commercial records relate to each other
Commercial records answer different questions:
- Customer: Who is buying?
- Contact: Which person communicates for the customer?
- Product: What does Meridian sell or provide?
- Price book: Which approved price applies in a defined pricing context?
- Quote: What commercial offer was made to a customer?
- Quote line item: Which products, quantities, prices and discounts make up the quote?
- Order: What the customer agreed to receive, subject to the organisation’s process.
- Invoice: What finance records for payment, subject to the finance system’s process.
A quote is not simply a list of product names. It is a commercial snapshot connected to a customer, a price context, line items, terms and an approval state.
Relationship model
Record	Relationship	Meridian example
Customer	Owns or is associated with contacts and commercial records	MER-CUST-101
Contact	Person associated with a customer	Aisha Green
Product	Catalog item or service that can be quoted	MER-PROD-WS-001
Price book	Named set of prices for products	MER-PB-STD-2026
Quote	Commercial proposal for a customer	MER-QUOTE-101
Quote line item	Product, quantity, price and discount within a quote	10 workstations at USD 520
Order	Commercial record created after acceptance where supported	Future finance or order record
Invoice	Finance request for payment	Future finance record
A product is reusable catalog information. A quote line item is a specific use of that product in a particular quote. The same product can appear on many quotes with different quantities, price books or permitted discounts.
Business IDs and product-generated IDs
Meridian business identifiers are stable case references:
- MER-PROD-WS-001
- MER-PB-STD-2026
- MER-QUOTE-101
A product may also generate an internal record ID. Keep the business ID and product-generated ID separate. The business ID helps learners and business users refer to the record; the generated ID may be needed for product relationships or integrations.
Check your understanding
Why is a quote line item not the same thing as a product?
Answer: A product is a reusable catalog definition. A quote line item is a specific product used on one quote with a quantity, applied price, discount and line total.
2.2 Products and price books
A product record should contain information that is stable enough to reuse:
- product name;
- business product ID;
- product type;
- unit of measure;
- description;
- active or inactive status;
- standard price or price-book relationship;
- eligibility or configuration information.
A product may be physical equipment, a service, installation work or a support plan. Use a clear product type so users do not quote a service as if it were a physical item.
A price book is a named pricing context. It may be used for:
- standard customers;
- approved partners;
- a particular region;
- a currency;
- a contract;
- a valid period;
- a customer segment.
The price book design must specify:
- which customers may use it;
- which currency it uses;
- the effective period;
- which products are included;
- the price for each product;
- whether a user may override the price;
- the approval needed for an override.
These are design decisions, not assumptions about a universal Zoho configuration.
Example product catalog
Product ID	Product name	Type	Unit	Standard price
MER-PROD-WS-001	Office workstation	Equipment	Each	USD 520.00
MER-PROD-INST-001	Installation service	Service	Job	USD 1,200.00
MER-PROD-SUP-001	Twelve-month support plan	Service	Plan	USD 400.00
MER-PROD-DOCK-001	Docking station	Equipment	Each	USD 180.00
Example price books
Price book ID	Name	Currency	Customer eligibility
MER-PB-STD-2026	Meridian Standard 2026	USD	Standard customers
MER-PB-PARTNER-2026	Meridian Partner 2026	USD	Approved Partner customers
For this learning case, MER-CUST-101 is a standard customer and must use MER-PB-STD-2026. It must not use the partner price book merely because the partner price is lower.
Check your understanding
What should happen if a standard customer is assigned the partner price book?
Answer: The quote should be blocked or returned for correction. The customer’s eligibility and the price-book rules must be checked before the quote is sent.
2.3 Quote line items and price calculations
A quote line item normally contains:
- product reference;
- product name;
- quantity;
- unit of measure;
- list or price-book unit price;
- line-level discount, if permitted;
- applied unit price;
- line extension;
- description;
- tax or charge fields where required by the approved design.
A basic line-extension formula is:
Line extension
= quantity × unit price × (1 − line discount percentage)
For a product with quantity 10, unit price USD 520 and no line discount:
Line extension
= 10 × 520 × (1 − 0)
= USD 5,200
For a product with quantity 10, unit price USD 225 and a 2% line discount:
Line extension
= 10 × 225 × (1 − 0.02)
= 2,250 × 0.98
= USD 2,205
The quote must state whether it uses:
- line-level discounts;
- quote-level discounts;
- both;
- neither.
Do not silently apply both types.
Quote-level discount
If the quote-level discount is applied after line extensions:
Quote subtotal
= sum of line extensions

Quote discount
= quote subtotal × quote discount percentage

Quote total before tax
= quote subtotal − quote discount
The rounding rule must be defined. In this chapter’s synthetic examples, currency is rounded to two decimal places and tax is excluded.
Historical price preservation
A price-book price may change after a quote is created. A historical quote should retain the applied price used when the quote was prepared or approved. Otherwise, a later catalog change could silently change a customer-facing commercial record.
This should be treated as a business requirement to test. Do not assume that a current product price automatically preserves or rewrites old quote line items.
Check your understanding
A quote contains three line items totaling USD 6,800 and a quote-level discount of 12%. What is the discount amount and total before tax?
Answer:
Discount = 6,800 × 0.12 = USD 816.00
Total before tax = 6,800 − 816 = USD 5,984.00
2.4 Discounts and approval controls
A discount is a commercial decision, not merely a number field. The process should define:
- who may apply a discount;
- the maximum amount or percentage;
- whether it is a line or quote discount;
- whether discounts may be combined;
- which role approves the discount;
- what evidence is recorded;
- whether the discount affects commissions, margin or finance processing.
For the Meridian learning case:
- a quote-level discount of 10% or less does not require the synthetic sales-manager approval;
- a quote-level discount greater than 10% requires sales-manager approval;
- the sales representative cannot approve their own quote;
- a quote with an unapproved discount cannot be sent;
- line-level discounts are not allowed for the standard guided quote unless explicitly approved.
These rules are synthetic.
Approval thresholds
Discount condition	Required route
No discount	Standard route
Greater than 0% and up to 10%	Standard route under this case rule
Greater than 10%	Sales manager approval
Missing discount value	Correction before submission
Price override without an approved reason	Correction or approval route
If an organisation introduces a second threshold, such as director approval above 15%, define whether the threshold uses:
- quote-level discount percentage;
- total discount amount;
- effective discount after line discounts;
- margin impact;
- price override amount.
A percentage threshold is not reproducible until its denominator is defined.
Discount calculation example
For the Meridian quote:
Subtotal = USD 6,800.00
Discount percentage = 12%
Discount amount = 6,800 × 0.12 = USD 816.00
Total before tax = 6,800 − 816 = USD 5,984.00
The approval condition is based on the stated quote-level discount percentage of 12%, so manager approval is required.
Check your understanding
Why should an approval rule state whether it uses the line discount or the quote-level discount?
Answer: The two discounts can produce different outcomes. Without defining the calculation basis, two users may apply different approval decisions to the same quote.
2.5 Configure-price-quote concepts
Configure-price-quote, often shortened to CPQ, describes a connected commercial method:
1. Configure: Select valid products, bundles, options and dependencies.
2. Price: Apply a permitted price book, quantity rule, discount and pricing exception.
3. Quote: Produce a commercial proposal with line items, terms and customer context.
4. Approve: Obtain required approval before the quote is sent or accepted.
A simple catalog does not automatically require a full CPQ implementation. CPQ becomes more useful when:
- products have compatible and incompatible options;
- bundles have required components;
- quantities affect price;
- customers have contract-specific pricing;
- discounts require multiple approval tiers;
- quote generation must be consistent;
- configuration errors are costly.
CPQ decision table
Question	Example answer
What can be configured?	Workstations, docking stations and installation
What combinations are valid?	Installation is required when the customer selects on-site setup
Which price applies?	Standard USD price book for standard customers
What discount is permitted?	Up to 10% without manager approval under this case rule
What requires approval?	Quote-level discount above 10%
What is quoted?	Customer, products, quantities, applied prices, discount and total
What proves approval?	Approver, decision, timestamp and quote version
Advanced CPQ development, custom scripts and complex product-configuration code are outside this course. The important skill here is to define the commercial rules and test their relationships.
Check your understanding
Which activity is configuration rather than pricing?
A. Choosing a workstation and compatible docking station  
B. Applying a 12% discount  
C. Selecting the standard price book
Answer: A. Choosing valid product components is configuration. Applying a discount and selecting a price book are pricing decisions.
2.6 Commercial record lifecycle
A typical commercial lifecycle may be:
Product catalog
    ↓
Price book selection
    ↓
Quote preparation
    ↓
Quote line-item validation
    ↓
Discount approval where required
    ↓
Quote sent
    ↓
Customer acceptance
    ↓
Order or finance handoff
Each stage has different evidence.
Stage	Evidence
Product selection	Product ID, active status and selected unit
Price selection	Price-book ID, currency and applied unit price
Quote preparation	Customer, contact, quote ID and owner
Line-item validation	Quantity, unit price, extension and total
Discount approval	Approver, decision and version
Customer acceptance	Acceptance evidence and timestamp
Finance handoff	Complete references and handoff state
Finance acceptance	Finance reference and receiving decision
A quote should not be sent merely because its total can be calculated. It also needs the correct customer, currency, product eligibility and approval state.
Check your understanding
What evidence should be preserved if a product price changes after a quote is approved?
Answer: Preserve the product reference, price-book reference, applied unit price, quantity, discount, quote version and approval evidence used for the approved quote.
2.7 Configuring products, pricing and quote records
This procedure uses common commercial-record concepts and Zoho CRM terminology. Exact navigation, fields, price-book behavior and approval options must be verified in the current product edition.
Required access
You need suitable access to:
- create and edit products;
- create and edit price books and product-price entries;
- create and edit quotes;
- add and change quote line items;
- configure discount and price-override controls;
- configure commercial approval rules;
- view record history;
- test as sales representative, manager and finance user;
- activate or deactivate the configuration.
Configuration sequence
1. Define the commercial rules.
Document products, units, currencies, price books, discounts, approval thresholds and rounding.
Expected result: A learner can calculate a quote without guessing.
2. Create or confirm product records.
Add product IDs, names, types, units, descriptions and active status.
Expected result: Each quoteable item has one identifiable catalog record.
3. Create or confirm price books.
Add currency, eligibility, effective period and product prices.
Expected result: A customer can be matched to an eligible price book.
4. Create product-price entries.
Link each product to its price-book price.
Expected result: The selected price can be traced to a product and price book.
5. Create the quote.
Link it to the customer, contact, currency, owner and price book.
Expected result: The quote has commercial context before line items are added.
6. Add line items.
Add product, quantity, unit price, permitted discount and line extension.
Expected result: The subtotal can be recalculated from the supplied inputs.
7. Configure discount approval.
Define the threshold, approver, requester, rejection or return route and evidence.
Expected result: A quote above the threshold cannot be sent without approval.
 8. Test record relationships.
Change a product price in a test copy or create a new price-book version.
Expected result: The effect on existing and new quotes is known and documented.
 9. Test exceptions.
Test missing customer, inactive product, ineligible price book, missing currency, invalid quantity and unapproved discount.
Expected result: Each exception has a correction route.
10. Activate and document.
Record catalog owner, price-book owner, approval owner and support route.
Expected result: A user can identify who maintains each commercial rule.
This chapter does not claim that these steps were executed in a live Zoho environment.
3. Visual explanation
flowchart LR
    C[Customer and contact] --> Q[Quote]
    P[Product catalog] --> PB[Price book]
    PB --> Q
    P --> L[Quote line item]
    Q --> L
    L --> S[Subtotal and total]
    S --> D[Discount decision]
    D --> A{Approval required?}
    A -- No --> T[Send quote]
    A -- Yes --> R[Manager approval]
    R -- Approved --> T
    R -- Returned or rejected --> X[Correct or close]
    T --> U[Customer acceptance]
    U --> F[Finance handoff]
    F --> O[Order or finance record]
The diagram shows why a quote cannot be calculated from the product catalog alone. The quote needs a customer, price context, line items, discount decision and approval route.
It also shows that the product catalog and price book are inputs to the quote. They are not substitutes for the quote’s historical applied prices and approval evidence.
4. Worked case: Meridian quotation
4.1 Scenario assumptions
The following assumptions are new for this chapter:
- All worked amounts are in USD.
- Tax is excluded from the calculations.
- Currency amounts are rounded to two decimal places.
- The quote uses one price book.
- The standard price book is used for standard customers.
- Line-level discounts are not used in the worked quote.
- The quote-level discount is applied after line extensions.
- A quote-level discount greater than 10% requires sales-manager approval.
- Product and price-book business IDs are distinct from any product-generated IDs.
- Existing quote MER-QUOTE-101 from Chapter 11 receives the detailed product and line-item records below.
- No live catalog, price book or quote configuration has been executed.
4.2 Product catalog
Product ID	Name	Type	Unit	Standard price USD
MER-PROD-WS-001	Office workstation	Equipment	Each	520.00
MER-PROD-INST-001	Installation service	Service	Job	1,200.00
MER-PROD-SUP-001	Twelve-month support plan	Service	Plan	400.00
MER-PROD-DOCK-001	Docking station	Equipment	Each	180.00
4.3 Price books
Price book ID	Name	Currency	Eligibility
MER-PB-STD-2026	Meridian Standard 2026	USD	Standard customers
MER-PB-PARTNER-2026	Meridian Partner 2026	USD	Approved Partner customers
For this quote, MER-CUST-101 is a standard customer. The quote uses MER-PB-STD-2026.
4.4 Quote and line items
Field	Value
Quote ID	MER-QUOTE-101
Enquiry ID	MER-ENQ-101
Customer ID	MER-CUST-101
Contact	Aisha Green
Email	aisha@greenfield.example.com
Price book	MER-PB-STD-2026
Currency	USD
Quote state	Customer Accepted
Approval	Approved
Quote-level discount	12%
Tax	Excluded
Line	Product ID	Quantity	Unit price	Line discount
1	MER-PROD-WS-001	10	520.00	0%
2	MER-PROD-INST-001	1	1,200.00	0%
3	MER-PROD-SUP-001	1	400.00	0%
Calculation:
Subtotal
= 5,200.00 + 1,200.00 + 400.00
= USD 6,800.00

Discount amount
= 6,800.00 × 0.12
= USD 816.00

Total before tax
= 6,800.00 − 816.00
= USD 5,984.00
The 12% quote discount is above the synthetic 10% threshold, so sales-manager approval is required. Chapter 11 states that the approval outcome is Approved.
4.5 Completed commercial artifact
Commercial element	Completed value
Customer	MER-CUST-101
Contact	Aisha Green
Price book	MER-PB-STD-2026
Currency	USD
Product references	Three active product records
Quantity validation	All quantities are positive
Subtotal	USD 6,800.00
Discount	12%, approved
Discount amount	USD 816.00
Total before tax	USD 5,984.00
Quote state	Customer Accepted
Finance state	Not yet Finance Accepted
Historical price evidence	Price book, applied unit prices and quote version
4.6 Test cases
These are expected simulated results, not actual product observations.
Test ID	Scenario	Expected result
P-01	Add 10 workstations, one installation and one support plan	Subtotal is USD 6,800.00
P-02	Apply 12% quote discount	Discount is USD 816.00; total before tax is USD 5,984.00
P-03	Submit 12% discount quote	Manager approval is required
P-04	Attempt to send before approval	Send action is denied
P-05	Select partner price book for a standard customer	Selection is denied or returned for correction
P-06	Set quantity to zero	Line item is rejected
P-07	Change the current product price after quote approval	Approved quote retains its applied price, or the difference is identified for correction according to verified behavior
P-08	Remove customer ID	Quote cannot be submitted or sent
4.7 Mistake and correction
Mistake: A learner selects the partner price book because its workstation price is lower.
Why it is wrong: The customer is not an approved Partner customer under the case rules. The lower price is not available merely because it exists.
Correction: Use MER-PB-STD-2026, record the standard price, and follow the permitted discount approval route if a lower commercial offer is needed.
A second mistake is applying a 12% line discount and a 12% quote discount without declaring that discounts stack. This would produce a different total and potentially bypass the approval calculation.
The correction is to define one permitted discount method or explicitly calculate both in a controlled rule.
5. Try it yourself — guided practice
Learning goal
Create and test a quotation containing products, a price book, quote line items, a discount and an approval route.
Required access
You need access to:
- products;
- price books or equivalent commercial pricing records;
- quotes;
- quote line items;
- discount fields;
- approval configuration;
- at least a sales representative and sales manager test role;
- synthetic records and recipients.
Complete product and price-book inputs
Product ID	Name	Type	Unit	Standard USD price
MER-PROD-WS-001	Office workstation	Equipment	Each	520.00
MER-PROD-INST-001	Installation service	Service	Job	1,200.00
MER-PROD-SUP-001	Twelve-month support plan	Service	Plan	400.00
MER-PROD-DOCK-001	Docking station	Equipment	Each	180.00
Price book ID	Currency	Eligibility	Workstation	Installation	Support plan
MER-PB-STD-2026	USD	Standard	520.00	1,200.00	400.00
MER-PB-PARTNER-2026	USD	Partner only	500.00	1,100.00	360.00
Complete quote inputs
Quote ID	Customer ID	Customer tier	Contact	Email	Price book	Currency
MER-QUOTE-301	MER-CUST-301	Standard	Ava Ross	ava@ridgeway.example.com (mailto:ava@ridgeway.example.com)	MER-PB-STD-2026	USD
MER-QUOTE-302	MER-CUST-302	Standard	Leo Martin	leo@quietlake.example.com (mailto:leo@quietlake.example.com)	MER-PB-PARTNER-2026	USD
MER-QUOTE-303	Blank	Standard	Sam Rivera	sam@riverbend.example.com (mailto:sam@riverbend.example.com)	MER-PB-STD-2026	USD
MER-QUOTE-304	MER-CUST-304	Standard	Priya Shah	priya@northstar.example.com (mailto:priya@northstar.example.com)	MER-PB-STD-2026	USD
Line items for MER-QUOTE-301:
Line	Product ID	Quantity	Expected unit price
1	MER-PROD-WS-001	6	520.00
2	MER-PROD-INST-001	1	1,200.00
3	MER-PROD-SUP-001	1	400.00
Practice rules
- Standard customers must use the standard price book.
- A quote-level discount above 10% requires sales-manager approval.
- A customer, price book, currency, product, quantity and unit price are required before submission.
- Quantities must be greater than zero.
- Tax is excluded from this practice.
- A sales representative cannot approve their own quote.
- A price-book mismatch is a correction exception.
Guided steps and expected results
Step 1: Create or confirm products
Add the four product records and confirm their units and active states.
Expected result: Each product can be identified by a unique business ID.
Step 2: Create or confirm price books
Add the two price books and their customer eligibility.
Expected result: The standard and Partner pricing contexts are distinct.
Step 3: Create the quote
Create MER-QUOTE-301 and link it to MER-CUST-301, the standard price book and USD.
Expected result: The quote has a customer, currency and price context before line items are added.
Step 4: Add line items
Add the three supplied lines.
Calculate:
6 × 520 = 3,120
1 × 1,200 = 1,200
1 × 400 = 400

Subtotal = 3,120 + 1,200 + 400
         = USD 4,720.00
Expected result: The subtotal is USD 4,720.00.
Step 5: Apply the discount
Apply the 12% quote-level discount.
Discount = 4,720 × 0.12
         = USD 566.40

Total before tax = 4,720 − 566.40
                 = USD 4,153.60
Expected result: The quote requires sales-manager approval and has a total before tax of USD 4,153.60.
Step 6: Submit for approval
Submit the quote as the sales representative.
Expected result: The quote enters the approval route. It cannot be sent while approval is pending.
Step 7: Test the exceptions
- MER-QUOTE-302: partner price book with a Standard customer.
- MER-QUOTE-303: missing customer.
- MER-QUOTE-304: approval already pending.
Expected result: Each record follows a different correction or controlled path.
Step 8: Test approval and price preservation
Approve MER-QUOTE-301 as the sales manager. Then change the catalog price in a test copy.
Expected result: The approved quote retains or clearly records its applied price according to the verified product behavior. No historical quote should silently change without a controlled event.
Final artifact
Your completed artifact should contain:
Artifact	Minimum content
Product catalog	IDs, names, types, units and active status
Price-book register	Currency, eligibility, product prices and status
Quote	Customer, contact, price book, currency and state
Quote line items	Product, quantity, unit price, discount and extension
Calculation sheet	Subtotal, discount amount and total
Approval register	Threshold, approver, decision and evidence
Exception matrix	Invalid price book, missing customer, missing currency and invalid quantity
Test evidence	Expected result and actual observation
Safe cleanup
Use synthetic products, customers and quotes. Deactivate practice approval rules and remove only practice records after recording the results. Do not delete a shared product or price book used by another learner.
Offline alternative
A spreadsheet can calculate line extensions, discounts, price-book eligibility and approval routes. It cannot demonstrate actual product relationships, quote line-item persistence, price-book selection behavior or approval history.
6. Independent challenge
Partner quotation with line and quote discounts
Design a quotation for an approved Partner customer. This challenge changes the pricing rules so that you must distinguish line-level discounts from quote-level discounts.
Scenario rules
- Partner customers may use MER-PB-PARTNER-2026.
- Standard customers may not use the Partner price book.
- One price book must be used for the whole quote.
- Hardware line discounts may be up to 3%.
- Service line discounts are not allowed.
- Quote-level discounts above 8% require sales-manager approval.
- Effective total discounts above 15% require director approval.
- The quote-level discount is applied after line-level discounts.
- The customer, currency, price book, products and quantities must be complete before approval.
- Tax is excluded.
- All prices are in USD.
Product and price-book data
Product ID	Product name	Type	Standard price
MER-PROD-MON-001	24-inch monitor	Equipment	240.00
MER-PROD-DOCK-001	Docking station	Equipment	180.00
MER-PROD-INST-001	Installation service	Service	1,200.00
Customer and quote data
Quote ID	Customer ID	Customer tier	Contact	Email	Price book
MER-QUOTE-401	MER-CUST-401	Partner	Elena Cruz	elena@oakridge.example.com (mailto:elena@oakridge.example.com)	MER-PB-PARTNER-2026
MER-QUOTE-402	MER-CUST-402	Standard	Daniel Wu	daniel@brightline.example.com (mailto:daniel@brightline.example.com)	MER-PB-PARTNER-2026
MER-QUOTE-403	MER-CUST-403	Partner	Noor Ali	noor@westfield.example.com (mailto:noor@westfield.example.com)	MER-PB-PARTNER-2026
MER-QUOTE-404	MER-CUST-404	Partner	Grace Kim	grace@harborview.example.com (mailto:grace@harborview.example.com)	MER-PB-PARTNER-2026
Line items:
Quote	Product	Quantity	Line discount
MER-QUOTE-401	MER-PROD-MON-001	20	2%
MER-QUOTE-401	MER-PROD-DOCK-001	20	0%
MER-QUOTE-401	MER-PROD-INST-001	1	0%
MER-QUOTE-402	MER-PROD-MON-001	10	0%
MER-QUOTE-403	MER-PROD-INST-001	1	5%
MER-QUOTE-404	MER-PROD-MON-001	5	0%
Deliverables
Create:
1. a product and price-book eligibility matrix;
2. a quote line-item table;
3. calculations for MER-QUOTE-401;
4. approval decisions for all four quotes;
5. correction routes for invalid records;
6. a test plan for line discounts, quote discounts, customer tier, service discounts and missing discount values;
7. a completed expected-results table.
Success criteria
Your solution should:
- calculate MER-QUOTE-401 using Partner prices;
- apply the 2% hardware line discount before the 9% quote-level discount;
- require sales-manager approval but not director approval for MER-QUOTE-401;
- reject or correct MER-QUOTE-402 because the customer is Standard;
- reject or correct MER-QUOTE-403 because a service line cannot receive a discount;
- prevent MER-QUOTE-404 from approval submission until the discount value is defined.
7. Common problems and recovery
Symptom	Diagnosis	Correction	Verification
A quote uses a lower price from the wrong price book	Customer eligibility was not checked	Select the eligible price book and record the correction	Test Standard and Partner customers
A product appears twice in the catalog	Product identity and naming rules are unclear	Preserve one business product ID and retire or merge the duplicate through a controlled process	Search by product ID and name
A quote total cannot be reproduced	Quantity, unit price or discount basis is missing	Store line calculations and quote-level discount separately	Recalculate from the saved inputs
Line and quote discounts are both applied unexpectedly	Stacking rules were not defined	Permit one method or document the calculation order	Test with a discount-bearing quote
A discontinued product can be added	Active-state control is absent	Prevent selection or route the quote for product-owner review	Attempt to add an inactive product
A service line receives a hardware discount	Product type was not used in discount validation	Apply type-specific discount criteria	Test equipment and service lines
An approved quote changes after a catalog price update	Historical applied price was not preserved or behavior is unknown	Store the applied price and test price-change behavior	Compare quote version before and after price update
A sales user can send an unapproved discount	Approval is informational rather than blocking	Connect send action to approval outcome	Attempt to send a pending quote
Currency is blank or inconsistent	Quote and price-book currency rules are missing	Require currency and match the price book	Test a blank or mismatched currency
Quantity is zero or negative	Numeric validation is absent	Require a positive quantity	Submit invalid line items
A price override has no reason	Override permissions are too broad	Require reason, approval and audit evidence	Test an override with and without reason
Product and quote IDs are mixed	Business and product-generated IDs are confused	Store them in separate fields	Trace one product from catalog to quote
A rejected quote is resubmitted without correction	Rejection and return routes are unclear	Require a new version or authorised correction route	Reject, correct and resubmit a test quote
Approval is calculated from the wrong discount basis	Threshold denominator is undefined	Document whether it uses line, quote or effective discount	Recalculate an example manually
8. Check your understanding
 1. What is the difference between a product and a quote line item?
 2. What information should a price book define?
 3. Why should a quote use one declared currency?
 4. Calculate the extension for 4 workstations at USD 520 with no line discount.
 5. Calculate the extension for 4 workstations at USD 520 with a 2% line discount.
 6. What is the difference between a line-level discount and a quote-level discount?
 7. Why should a customer’s eligibility be checked before selecting a price book?
 8. Under the Meridian synthetic rule, does a 12% quote discount require approval?
 9. What evidence should be preserved after a quote is approved?
10. What happens if a service product receives a hardware-only discount?
11. Calculate the total before tax for a USD 10,000 subtotal with a 15% quote discount.
12. Why should a quote not be sent while its required approval is pending?
13. Which CPQ stage validates that products can be combined correctly?
14. Which CPQ stage applies price books and discounts?
15. What should happen when a product price changes after an approved quote is created?
16. In the independent challenge, why is MER-QUOTE-402 invalid?
9. Solutions and explanations
9.1 Answers to the checks
 1. A product is a reusable catalog definition. A quote line item is a particular product, quantity, price and discount used on one quote.
 2. A price book should define name, currency, eligibility, effective period, included products, prices and permitted overrides.
 3. Currency affects price selection, calculation and finance interpretation. A quote should not combine incompatible currency values.
 4. 4 × 520 = USD 2,080.00.
 5. 4 × 520 × 0.98 = USD 2,038.40.
 6. A line-level discount applies to one product line. A quote-level discount applies to the subtotal or another declared quote basis.
 7. A lower price may be restricted to a customer segment or contract. Selecting it for an ineligible customer creates an invalid commercial offer.
 8. Yes. It is greater than the synthetic 10% approval threshold.
 9. Preserve quote version, products, quantities, price book, applied unit prices, discounts, total, approver, approval decision and timestamp.
10. The quote should be blocked or returned because the discount is not permitted for that product type.
11. Discount = 10,000 × 0.15 = USD 1,500.00. Total = 10,000 − 1,500 = USD 8,500.00.
12. Sending it before approval allows an unauthorised commercial offer to reach the customer.
13. Configure validates valid products, options, dependencies and combinations.
14. Price applies the eligible price book, quantities, discounts and price rules.
15. The approved quote should preserve or clearly record its applied historical price. A later catalog change should not silently alter the approved commercial offer.
16. MER-QUOTE-402 uses a Partner price book for a Standard customer, which violates the stated eligibility rule.
9.2 Guided practice sample solution
Price-book eligibility
Customer	Tier	Permitted price book	Result
MER-CUST-301	Standard	MER-PB-STD-2026	Valid
MER-CUST-302	Standard	MER-PB-PARTNER-2026	Invalid
MER-CUST-303	Standard	MER-PB-STD-2026	Valid, but customer ID is missing
MER-CUST-304	Standard	MER-PB-STD-2026	Valid
MER-QUOTE-301 calculation
Line	Calculation	Extension
Workstations	6 × 520	3,120.00
Installation	1 × 1,200	1,200.00
Support plan	1 × 400	400.00
Subtotal = 3,120 + 1,200 + 400
         = USD 4,720.00

Discount = 4,720 × 0.12
         = USD 566.40

Total before tax = 4,720 − 566.40
                 = USD 4,153.60
Because the discount is 12%, the quote requires sales-manager approval.
Expected practice results
Quote	Expected result	Reason
MER-QUOTE-301	Approval required	Discount is 12%; customer and pricing context are complete
MER-QUOTE-302	Returned or blocked	Partner price book is not valid for a Standard customer
MER-QUOTE-303	Returned or blocked	Customer ID is missing
MER-QUOTE-304	Approval remains pending	Discount is 16%; it cannot be sent without approval
Approval evidence
For MER-QUOTE-301, the completed approval artifact should include:
Quote ID: MER-QUOTE-301
Discount: 12%
Requester: Sales representative
Approver: Sales manager
Decision: Approved
Decision timestamp: Recorded during test
Quote version: Recorded during test
A valid alternative is to require a return for correction if the total, currency or line-item validation is incomplete before approval submission.
9.3 Independent challenge sample solution
MER-QUOTE-401 calculation
Partner prices:
Product	Quantity	Partner unit price	Line discount	Calculation
24-inch monitor	20	225.00	2%	20 × 225 × 0.98
Docking station	20	165.00	0%	20 × 165
Installation service	1	1,100.00	0%	1 × 1,100
Subtotal after line discounts
= 4,410.00 + 3,300.00 + 1,100.00
= USD 8,810.00

Quote-level discount
= 8,810.00 × 0.09
= USD 792.90

Total before tax
= 8,810.00 − 792.90
= USD 8,017.10
The undiscounted Partner-price subtotal is:
20 × 225 = 4,500.00
20 × 165 = 3,300.00
1 × 1,100 = 1,100.00

Undiscounted subtotal = USD 8,900.00
The effective total discount is:
Total discount amount
= 8,900.00 − 8,017.10
= USD 882.90

Effective discount percentage
= 882.90 / 8,900.00 × 100
≈ 9.92%
Under the challenge rules:
- the 9% quote-level discount is above 8%, so sales-manager approval is required;
- the effective total discount is below 15%, so director approval is not required;
- the 2% hardware line discount is within the 3% limit;
- the service line has no discount.
Expected challenge results
Quote	Expected result	Reason
MER-QUOTE-401	Valid after manager approval	Partner customer, eligible price book, valid hardware discount and 9% quote discount
MER-QUOTE-402	Return or block	Standard customer cannot use Partner price book
MER-QUOTE-403	Return or block	Service line has a prohibited 5% line discount
MER-QUOTE-404	Return or block	Discount value is missing before approval evaluation
Correction routes
- MER-QUOTE-402: change to the standard price book or confirm an authorised customer-tier correction.
- MER-QUOTE-403: remove the service-line discount and recalculate the quote.
- MER-QUOTE-404: record the intended quote discount, then reevaluate whether approval is required.
- MER-QUOTE-401: submit to the sales manager and preserve the line-level and quote-level calculations.
10. Chapter recap and next step
A reliable commercial record connects product identity, price context, quote lines, discounts, approvals and customer records.
You should now be able to:
- distinguish products, price books, quotes and quote line items;
- define product type, unit and active status;
- select an eligible price book;
- calculate line extensions and quote totals;
- distinguish line-level and quote-level discounts;
- define a reproducible discount approval threshold;
- preserve applied prices and quote versions;
- explain configure, price, quote and approve concepts;
- test invalid customers, products, price books, quantities and discounts;
- separate a finance handoff from finance acceptance;
- document commercial ownership and recovery routes.
For the Meridian Supply project, this chapter produces:
C01_CH12_Meridian_Product_Catalog
C01_CH12_Meridian_Price_Book_Register
C01_CH12_Meridian_Quote_and_Line_Item_Calculation
C01_CH12_Meridian_Discount_Approval_Register
C01_CH12_Meridian_Commercial_Test_Evidence
The next chapter traces the sales-to-finance handoff through Books. It builds on the quote, product, line-item, discount and approval artifacts created here.
11. Glossary and further reading
Glossary
Term	Definition
Applied price	The price actually used on a specific quote line
Catalog	Collection of products and services available for commercial use
Configure-price-quote	Connected method for selecting valid products, applying prices, preparing quotes and obtaining approval
Extension	Quantity multiplied by the applicable unit price after permitted line discount
Line item	One product or service entry within a commercial record
List price	A reference price before a quote-specific discount or override
Price book	Named set of product prices for a customer, currency, contract or segment
Product	Reusable catalog item or service
Quote	Commercial proposal containing customer, products, prices, discounts and terms
Quote-level discount	Discount applied to the quote subtotal or another defined quote basis
Line-level discount	Discount applied to one quote line
Price override	Change from the selected price-book price
Quote version	Identifiable version of a commercial proposal used for approval or customer acceptance
Further reading
Check the current Zoho CRM edition, product relationships, price-book behavior, quote features and approval permissions before implementation:
- Zoho CRM Help (https://help.zoho.com/portal/en/kb/crm)
- Zoho CRM customization help (https://help.zoho.com/portal/en/kb/crm/customize-crm-account)
- Zoho CRM products and price books help (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/products)
- Zoho CRM quotes help (https://help.zoho.com/portal/en/kb/crm/sales-force-automation/quotes)
- Zoho CRM automation help (https://help.zoho.com/portal/en/kb/crm/automate-business-processes)
- Zoho CRM developer documentation (https://www.zoho.com/crm/developer/docs/)
This chapter has not verified current product screens, price-book behavior, quote-line persistence, CPQ support, approval limits or permission names in a live Zoho environment. Synthetic calculations and test results are expected learning outputs, not product execution observations.
