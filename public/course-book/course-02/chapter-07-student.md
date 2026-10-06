# Deluge Language Foundations

1. What you will learn
Deluge is Zoho’s scripting language for adding logic to Zoho services. It is used when configuration alone cannot express a calculation, validation rule, reusable operation or integration step.
This chapter teaches the language foundations needed to implement the Nova Field Service rules from Chapters 1–6.
You will learn to:
- assign and inspect variables;
- use operators and conditions;
- work with lists, maps and record collections;
- loop through values and records;
- manipulate strings;
- work with dates and date-time values;
- distinguish null, blank and empty values;
- write reusable functions;
- return predictable result shapes;
- test priority and validation functions.
The required practice is to write tested priority-calculation and validation functions.
Contribution to the course project
The functions in this chapter support:
- Request priority calculation;
- required-field validation;
- duplicate-key checks;
- Technician assignment validation;
- inspection completion checks;
- reusable workflow logic;
- consistent error result shapes.
Later chapters will add Creator record operations, Deluge data tasks, external services and CRM APIs. This chapter keeps the examples focused on language behavior.
Continuity from previous chapters
Item	Carried-forward decision
Customer ownership	CRM owns customer identity and service information
Creator forms	Customer_Reference, Service_Requests, Technicians and Jobs
Business identifiers	NOV-CUST-001, NOV-REQ-001 and NOV-VISIT-001 remain stable
Request lifecycle	New, Validated, Ready for Dispatch, Assigned, In Progress, Awaiting Inspection, Completed, Cancelled, Exception
Sync lifecycle	Not Required, Pending, Succeeded, Error, Retry Pending
Access	Technician sees assigned Jobs; Service Manager handles exceptions
Workflow protection	Duplicate actions and recursion must be prevented
Testing	Functions must have normal, invalid, null and boundary cases
Integration	CRM API version, data centre, field API names and OAuth details remain later-chapter dependencies
Deluge execution contexts
Deluge syntax is shared across Zoho services, but available variables, record tasks and permissions depend on the host.
Host	Example context	Important input or return detail
Creator	Form On Validate	input refers to form fields; cancel submit; can prevent saving
Creator	Form On Success	The record has been saved; use approved follow-up actions
Creator	Custom Function	Arguments are defined by the function; return type must be documented
Creator	Scheduled workflow	Query eligible records; no interactive user input should be assumed
CRM	Custom function	Arguments come from the CRM action or trigger; CRM record tasks differ from Creator tasks
Flow	Custom function or action	Inputs come from trigger and prior steps; connections are selected separately
External call	Creator, CRM or Flow	Use an approved connection placeholder; document response and failure shape
The executable examples in this chapter are labelled by host. A Creator example must not be pasted into a CRM function or Flow action without adapting its inputs, tasks and return behavior.
2. Lessons
Lesson 1: Variables and values
A variable is a name associated with a value.
Deluge assignments use the variable name, an equals sign and the value:
priority = "High";
retryCount = 0;
isEmergency = true;
Deluge is dynamically typed. The value determines the type during execution.
Common values include:
Value type	Example	Nova use
Text	"NOV-REQ-001"	Business ID or description
Number	3	Retry count or item count
Decimal	12.5	Duration or measurement
Boolean	true	Whether a risk is present
Date	'10-Oct-2026'	Service date
Date-time	'10-Oct-2026 10:00:00'	Scheduled start
List	{"Low", "Medium", "High"}	Ordered values
Map	{"priority":"High"}	Named values
Record collection	Jobs[Job_Status == "Scheduled"]	Matching Creator records
Variable names should describe the business meaning:
requestPriority = "High";
assignedTechnicianId = "TECH-001";
Avoid names that hide type or meaning:
x = "High";
data = "TECH-001";
A variable can be changed:
retryCount = 0;
retryCount = retryCount + 1;
A value can also be derived from another value:
requestLabel = requestBusinessId + " - " + requestPriority;
Assignment is not comparison
Use = to assign:
requestStatus = "Validated";
Use == to compare:
if(requestStatus == "Validated")
{
    info "Request may continue";
}
Confusing assignment and comparison changes data or causes an invalid condition.
Operators
Category	Operators	Example
Arithmetic	+, -, *, /, %	attempts = attempts + 1;
Comparison	==, !=, >, <, >=, <=	priority == "High"
Logical	&&, `	 
Text concatenation	+	id + " - " + status
Use parentheses when a rule has several conditions:
if((priority == "High" || isEmergency == true) && customerFound == true)
{
    approvalRequired = true;
}
Quick check
1. What does = do, and what does == do?
2. Which type should hold NOV-REQ-001?
3. What does this condition require?
if(priority == "High" && customerFound == true)
Lesson 2: Conditions and decisions
A condition evaluates to true or false. Deluge supports if, else if and else.
if(priority == "High")
{
    approvalRequired = true;
}
else if(priority == "Medium")
{
    approvalRequired = false;
}
else
{
    approvalRequired = false;
}
The first matching branch runs. Arrange conditions from the most specific or important rule to the general fallback.
Example: priority decision
This function is an illustrative Deluge custom function. It accepts a map and returns text. It does not query a form, call an API or use a connection.
string calculatePriority(map request)
{
    incidentLevel = request.get("incident_level");
    safetyRisk = request.get("safety_risk");

    if(incidentLevel == "Emergency" || safetyRisk == true)
    {
        return "High";
    }
    else if(incidentLevel == "Urgent")
    {
        return "Medium";
    }
    else
    {
        return "Low";
    }
}
The function has one responsibility: calculate a priority. It does not save a Request or send a notification.
Conditional values
Deluge also supports a conditional expression:
queueName = if(priority == "High", "Urgent Queue", "Standard Queue");
Use a conditional expression for a simple value choice. Use a full if block when several actions or validations are needed.
Null fallback
ifNull returns a fallback when the first expression is null:
displayName = ifNull(customerName, "Customer not mapped");
A fallback should not hide an important exception. For a CRM customer lookup, "Customer not mapped" may be a useful display value, but it must not be used as proof that a valid Customer Reference exists.
Quick check
What is the problem with this rule?
if(priority == "High")
{
    approvalRequired = true;
}
else
{
    approvalRequired = false;
}
if(isEmergency == true)
{
    priority = "High";
}
The emergency rule changes priority after the approval decision. The calculation and decision should occur in a deliberate order, or the priority should be calculated first.
Lesson 3: Lists, maps and collections
Lists
A list is an ordered group of values.
allowedPriorities = {"Low", "Medium", "High"};
You can also create a list and add values:
errors = List();
errors.add("Customer is required");
errors.add("Description is required");
Useful list operations include:
hasHigh = allowedPriorities.contains("High");
numberOfErrors = errors.size();
A list can contain text, numbers, maps or other lists. Use a consistent element shape when the list will be processed by a loop.
checks = List();

check = Map();
check.put("name", "Pump pressure");
check.put("required", true);
check.put("result", "Pass");

checks.add(check);
Maps
A map stores key-value pairs.
request = Map();
request.put("request_business_id", "NOV-REQ-001");
request.put("priority", "High");
request.put("request_status", "New");
Read a value with get:
requestPriority = request.get("priority");
If the key is not found, get returns null. That makes a missing key an important exception condition.
A map literal can also be used:
request = {
    "request_business_id" : "NOV-REQ-001",
    "priority" : "High",
    "request_status" : "New"
};
If put is called with an existing key, the new value replaces the old value:
request.put("request_status", "Validated");
This is useful for building a result map, but dangerous if a later assignment silently overwrites a validated value.
Record collections in Creator
A Creator form criteria query returns a collection of matching records. This is different from a simple list of text values.
Creator context: Form workflow or Creator custom function
scheduledJobs = Jobs[Job_Status == "Scheduled"];

for each job in scheduledJobs
{
    info job.Job_Business_ID;
}
Jobs and Job_Status are proposed form and field link names from Chapter 3. Confirm the actual names in the target Creator application before using the query.
A record collection can be empty. Check its count before assuming that a match exists:
scheduledJobs = Jobs[Job_Status == "Scheduled"];

if(scheduledJobs.count() == 0)
{
    info "No scheduled Jobs found";
}
Do not confuse:
errors = List();
with:
scheduledJobs = Jobs[Job_Status == "Scheduled"];
The first is an in-memory list. The second is a Creator record collection obtained from a form query.
Quick check
1. Which structure is best for priority -> queue name?
2. What happens when request.get("missing_key") is used?
3. Why should a Creator record collection be checked before processing?
Lesson 4: Loops and repeated work
A loop repeats an operation for each value or record.
Loop through a list
priorities = {"Low", "Medium", "High"};

for each priority in priorities
{
    info priority;
}
The loop variable contains one element at a time.
Loop through a list of maps
checks = List();

checkOne = Map();
checkOne.put("name", "Pump pressure");
checkOne.put("result", "Pass");
checks.add(checkOne);

checkTwo = Map();
checkTwo.put("name", "Electrical enclosure");
checkTwo.put("result", null);
checks.add(checkTwo);

failedOrMissing = List();

for each check in checks
{
    result = check.get("result");

    if(isNull(result) || result == "Fail")
    {
        failedOrMissing.add(check.get("name"));
    }
}
The result is a list containing Electrical enclosure.
Loop through Creator records
Creator context: scheduled workflow or custom function
errorRequests = Service_Requests[Sync_Status == "Error"];

for each request in errorRequests
{
    request.Sync_Status = "Retry Pending";
}
This is a record update example. It is not executed here. In a real workflow, add a claim state, access design, error handling and recursion guard before updating records.
Avoid modifying the collection unpredictably
If a loop removes records from the same collection it is processing, the result may be difficult to reason about. Prefer:
1. collect IDs to change;
2. finish the scan;
3. apply controlled updates;
4. record successes and failures.
Quick check
Why is it safer to collect the business IDs of failed inspection rows before applying a separate correction step?
Lesson 5: Strings and normalization
Strings represent text, but text often contains formatting differences.
These values may represent the same business key to a human:
"EXT-REQ-1001"
" EXT-REQ-1001 "
"ext-req-1001"
The business rule must define whether case and spaces matter.
Deluge’s trim removes leading and trailing spaces:
cleanKey = externalKey.trim();
replaceAll replaces matching text:
cleanDescription = description.replaceAll("\n", " ", true);
The third argument controls regular-expression behavior. Confirm the desired behavior before using special characters.
Use normalization before duplicate comparison:
normalizedKey = externalKey.trim().toUpperCase();
If a method or function is not available in the target host, use the corresponding documented Deluge function and test it in that host. Product-specific support can differ.
Do not normalize away meaningful data. For example, changing a customer’s display name to uppercase may make a comparison easier but should not change the stored display value.
String validation
A safe text check considers:
- null;
- empty string;
- spaces only;
- maximum length;
- allowed format;
- whether the value is a business key or free text.
if(isNull(description) || isBlank(description))
{
    errors.add("Description is required");
}
Deluge’s null, blank and empty functions have different behavior across value types and services. In Creator, test the exact form field behavior rather than assuming that an empty form field is identical to a missing map key.
Quick check
Why should the validation function trim an external key before duplicate comparison but preserve the original description formatting for display?
Lesson 6: Dates and date-time values
Dates are not ordinary strings. They support comparison and date-time functions.
Use date-time fields from Creator records rather than manually parsing display text whenever possible.
daysOpen = daysBetween(request.Created_At, zoho.currenttime);
The daysBetween function returns the number of days between two date or date-time values. Confirm whether the business requires calendar days, elapsed hours or business hours before using the result.
Format a date-time for display:
displayStart = request.Scheduled_Start.toString(
    "yyyy-MM-dd HH:mm",
    "UTC"
);
The format and timezone must match the application’s timezone rules.
Null dates
A missing date cannot be safely compared:
if(isNull(request.Due_At))
{
    measurementStatus = "Not Measured";
}
else
{
    measurementStatus = "Due time supplied";
}
Do not treat a missing Due_At as “on time.”
Date calculation example
Creator context: reusable function receiving date-time arguments
map responseWindowStatus(datetime createdAt, datetime firstResponseAt, number targetMinutes)
{
    result = Map();

    if(isNull(createdAt) || isNull(firstResponseAt))
    {
        result.put("measured", false);
        result.put("status", "Not Measured");
        return result;
    }

    elapsedMinutes = createdAt.minutesBetween(firstResponseAt);

    result.put("measured", true);
    result.put("elapsed_minutes", elapsedMinutes);

    if(elapsedMinutes <= targetMinutes)
    {
        result.put("status", "Met");
    }
    else
    {
        result.put("status", "Missed");
    }

    return result;
}
This example is illustrative and must be verified in the target Deluge host before use. It does not infer a target for a record that lacks timestamps.
Quick check
A Request has Created_At but no First_Response_At. What should responseWindowStatus return?
Lesson 7: Handle null, blank and empty values deliberately
Null behavior is a common source of bugs.
Deluge provides functions such as:
- isNull;
- isBlank;
- isEmpty;
- ifNull.
They do not always return the same result for every input type or service. The official Deluge documentation specifically distinguishes their behavior and notes differences for Creator.
Conceptual distinctions:
Value	Meaning
null	No value or missing value
""	Empty text
" "	Text containing spaces
empty list	A list with no elements
missing map key	get returns null
empty form subform	No child rows
false	A deliberate Boolean value
0	A deliberate numeric value
Use explicit checks:
value = request.get("description");

if(isNull(value) || isBlank(value))
{
    errors.add("Description is required");
}
Do not use a generic comparison that could confuse false or 0 with missing data.
Form object caution
The official isNull documentation notes that the method form is not supported for form objects. Use the supported function form and validate the field expression in the actual Creator event.
For example, this is a Creator validation context:
if(isNull(input.Customer))
{
    alert "Customer is required";
    cancel submit;
}
cancel submit; is a Creator-only task for an On Validate event. It prevents the form submission. It is not a general Deluge statement for CRM or Flow.
Quick check
Why should this condition not be used to detect a missing Boolean field?
if(!request.get("safety_risk"))
It treats false as if it were missing. Use a null check and then evaluate the Boolean value.
Lesson 8: Write reusable functions with predictable returns
A reusable function should have:
- a clear name;
- explicit arguments;
- one coherent responsibility;
- predictable return type or shape;
- documented null behavior;
- no hidden dependency on a global record;
- an identified host context.
A function that validates a map can return a map:
map validateRequest(map request)
{
    errors = List();
    allowedPriorities = {"Low", "Medium", "High"};

    externalKey = request.get("external_request_key");
    customerId = request.get("customer_business_id");
    description = request.get("description");
    priority = request.get("priority");

    if(isNull(externalKey) || isBlank(externalKey))
    {
        errors.add("external_request_key is required");
    }

    if(isNull(customerId) || isBlank(customerId))
    {
        errors.add("customer_business_id is required");
    }

    if(isNull(description) || isBlank(description))
    {
        errors.add("description is required");
    }

    if(isNull(priority) || !allowedPriorities.contains(priority))
    {
        errors.add("priority must be Low, Medium, or High");
    }

    result = Map();
    result.put("valid", errors.size() == 0);
    result.put("errors", errors);
    return result;
}
This function is designed for a Creator custom function with a map argument and map return. It does not perform Creator record operations, CRM operations or external calls. That makes it easier to test.
A caller can use the result:
validation = validateRequest(requestMap);

if(validation.get("valid") == false)
{
    info validation.get("errors");
}
Do not return different shapes for different branches:
// Unsafe design
return "valid";
return {"error":"missing customer"};
Use one shape:
{
    "valid": true or false,
    "errors": list
}
Quick check
What should a reusable validation function return when the input is missing: an alert, a Boolean, a map of errors or a new record? Choose the best primary return and explain why.
3. Visual explanation
Data movement through a reusable function
flowchart LR
    E[Host event] --> I[Input map or form fields]
    I --> N[Normalize strings and nulls]
    N --> V[Validate values]
    V -->|invalid| R[Return valid=false and errors]
    V -->|valid| C[Calculate or classify]
    C --> O[Return predictable result map]
    O --> H[Host-specific next action]
    H -->|Creator| CF[Save, alert or cancel submit]
    H -->|CRM| CRM[CRM operation]
    H -->|Flow| FL[Mapped Flow output]
Plain-text explanation:
1. A host event supplies input.
2. The function normalizes and checks values.
3. Invalid data returns a structured error result.
4. Valid data is calculated or classified.
5. The reusable function returns a predictable map.
6. The host decides whether to save, block, update, call CRM or pass data to Flow.
The reusable function should not assume that every host provides input, supports cancel submit, or has the same record operations.
Function boundary	Good responsibility
Normalizer	Trim and standardize values
Priority calculator	Return Low, Medium or High
Validator	Return valid flag and errors
Date calculator	Return measured status and duration
Creator form event	Adapt input and block or allow submit
Flow step	Map trigger input and handle output
CRM function	Adapt CRM arguments and perform CRM-specific work
4. Worked case
Case inputs
Priority inputs:
case_id,incident_level,safety_risk,expected_priority
P-001,Emergency,true,High
P-002,Urgent,false,Medium
P-003,Normal,false,Low
P-004,Normal,true,High
P-005,,false,Low
Validation inputs:
case_id,external_request_key,customer_business_id,description,priority,expected_valid
V-001,EXT-REQ-4001,NOV-CUST-001,Pump pressure low,High,true
V-002,,NOV-CUST-001,Pump pressure low,High,false
V-003,EXT-REQ-4003,,Pump pressure low,High,false
V-004,EXT-REQ-4004,NOV-CUST-001,,High,false
V-005,EXT-REQ-4005,NOV-CUST-001,Door access failure,Urgent,false
V-006,EXT-REQ-4006,NOV-CUST-001,Generator alarm,Medium,true
The validation rule allows only Low, Medium and High. Urgent is an incident level, not a stored Request priority.
Step 1: Calculate priority
string calculatePriority(map request)
{
    incidentLevel = request.get("incident_level");
    safetyRisk = request.get("safety_risk");

    if(incidentLevel == "Emergency" || safetyRisk == true)
    {
        return "High";
    }
    else if(incidentLevel == "Urgent")
    {
        return "Medium";
    }
    else
    {
        return "Low";
    }
}
Expected output:
Case	Reason
P-001	Emergency incident
P-002	Urgent incident
P-003	Normal, no safety risk
P-004	Safety risk
P-005	Missing incident level and no safety risk
P-005 returns Low because this function calculates a fallback priority. A separate validation function may still require incident_level. Calculation and validation answer different questions.
Step 2: Validate the Request
map validateRequest(map request)
{
    errors = List();
    allowedPriorities = {"Low", "Medium", "High"};

    externalKey = request.get("external_request_key");
    customerId = request.get("customer_business_id");
    description = request.get("description");
    priority = request.get("priority");

    if(isNull(externalKey) || isBlank(externalKey))
    {
        errors.add("external_request_key is required");
    }

    if(isNull(customerId) || isBlank(customerId))
    {
        errors.add("customer_business_id is required");
    }

    if(isNull(description) || isBlank(description))
    {
        errors.add("description is required");
    }

    if(isNull(priority) || !allowedPriorities.contains(priority))
    {
        errors.add("priority must be Low, Medium, or High");
    }

    result = Map();
    result.put("valid", errors.size() == 0);
    result.put("errors", errors);
    return result;
}
Expected validation results:
Case	Result	Error
V-001	Valid	None
V-002	Invalid	External request key is required
V-003	Invalid	Customer business ID is required
V-004	Invalid	Description is required
V-005	Invalid	Priority must be Low, Medium, or High
V-006	Valid	None
Step 3: Adapt the function to a Creator form
Host: Zoho Creator  
Context: Service Requests form, On Validate event  
Inputs: input.External_Request_Key, input.Customer, input.Description, input.Priority  
Supported tasks: map creation, list operations, alert, cancel submit  
Connection: none  
Return shape: no function return; the event either allows submission or cancels it
Illustrative adapter:
requestMap = Map();
requestMap.put("external_request_key", input.External_Request_Key);
requestMap.put("customer_business_id", input.Customer.Customer_Business_ID);
requestMap.put("description", input.Description);
requestMap.put("priority", input.Priority);

validation = validateRequest(requestMap);

if(validation.get("valid") == false)
{
    alert validation.get("errors").toString();
    cancel submit;
}
The input.Customer.Customer_Business_ID expression depends on the actual lookup structure and field link names. Confirm it in the target Creator application. If the Customer lookup is null, the adapter itself must guard the lookup before dereferencing its field.
A safer adapter separates the lookup check:
if(isNull(input.Customer))
{
    alert "Customer is required";
    cancel submit;
}
Step 4: Run the tests
A custom test function can pass maps to the reusable functions. This is an illustrative Creator custom function with no connection and a map return.
map runPriorityTests()
{
    tests = List();
    passedCount = 0;

    testOne = Map();
    inputOne = Map();
    inputOne.put("incident_level", "Emergency");
    inputOne.put("safety_risk", true);
    testOne.put("name", "Emergency becomes High");
    testOne.put("input", inputOne);
    testOne.put("expected", "High");
    tests.add(testOne);

    testTwo = Map();
    inputTwo = Map();
    inputTwo.put("incident_level", "Urgent");
    inputTwo.put("safety_risk", false);
    testTwo.put("name", "Urgent becomes Medium");
    testTwo.put("input", inputTwo);
    testTwo.put("expected", "Medium");
    tests.add(testTwo);

    results = List();

    for each testCase in tests
    {
        actual = calculatePriority(testCase.get("input"));
        passed = actual == testCase.get("expected");

        row = Map();
        row.put("name", testCase.get("name"));
        row.put("expected", testCase.get("expected"));
        row.put("actual", actual);
        row.put("passed", passed);
        results.add(row);

        if(passed)
        {
            passedCount = passedCount + 1;
        }
    }

    summary = Map();
    summary.put("total", tests.size());
    summary.put("passed", passedCount);
    summary.put("results", results);
    return summary;
}
Expected mocked output:
{
  "total": 2,
  "passed": 2,
  "results": [
    {
      "name": "Emergency becomes High",
      "expected": "High",
      "actual": "High",
      "passed": true
    },
    {
      "name": "Urgent becomes Medium",
      "expected": "Medium",
      "actual": "Medium",
      "passed": true
    }
  ]
}
This output is expected, not an observed execution result.
Mistake and correction
Mistake: The developer writes one large Creator workflow that reads input, calculates priority, queries CRM, creates a Job, sends email and updates Sync Status.
Why it is wrong: The logic cannot be tested without Creator records, CRM access and notifications. It also mixes host-specific tasks and makes failures difficult to classify.
Correction:
1. Keep calculatePriority as a pure map-to-text function.
2. Keep validateRequest as a map-to-result function.
3. Use a Creator adapter to convert input fields into a map.
4. Perform Creator record operations in the host workflow.
5. Move CRM and external operations to later integration functions with explicit connections and failure shapes.
5. Try it yourself — guided practice
Learning goal
Write and test two reusable Deluge functions:
1. calculatePriority;
2. validateRequest.
Then adapt the validation function to a Creator form validation context.
Host and access requirements
Use a Creator development or sandbox environment if available. The reusable functions should be created as Creator custom functions with:
- explicit map input;
- no external connection;
- predictable map or text return;
- no production record updates.
If you cannot create custom functions, use the offline alternative.
Sample inputs
Priority cases:
case_id,incident_level,safety_risk,expected_priority
T-001,Emergency,false,High
T-002,Urgent,false,Medium
T-003,Normal,false,Low
T-004,Normal,true,High
T-005,,false,Low
Validation cases:
case_id,external_request_key,customer_business_id,description,priority,expected_valid
T-101,EXT-T-101,NOV-CUST-001,Pump pressure low,High,true
T-102,,NOV-CUST-001,Pump pressure low,High,false
T-103,EXT-T-103,,Pump pressure low,High,false
T-104,EXT-T-104,NOV-CUST-001,,High,false
T-105,EXT-T-105,NOV-CUST-001,Door access failure,Urgent,false
T-106,EXT-T-106,NOV-CUST-001,Generator alarm,Low,true
Null and boundary inputs:
case_id,field,value,expected_behavior
N-001,description,null,reject
N-002,description,"",reject
N-003,description,"   ",reject
N-004,safety_risk,false,do not treat as missing
N-005,priority,0,reject as invalid priority
Steps and expected intermediate results
1. Create calculatePriority with a map input and text return.  
Expected result: the function has no Creator record query and no connection.
2. Run the five priority cases.  
Expected result: T-001 and T-004 return High; T-002 returns Medium; T-003 and T-005 return Low.
3. Create validateRequest with a map input and map return.  
Expected result: every branch returns valid and errors.
4. Run the six validation cases.  
Expected result: T-101 and T-106 are valid; T-102 through T-105 are invalid.
5. Add null, empty and spaces-only tests.  
Expected result: descriptions that are null, empty or spaces only are rejected; false safety risk is treated as a valid Boolean value.
6. Create a Creator Service Requests On Validate adapter.  
Expected result: the adapter maps input fields and uses alert and cancel submit only in the Creator context.
7. Test the form adapter with:
- valid Request;
- missing Customer;
- missing Description;
- invalid Priority;
- duplicate External Request Key.
Expected result: invalid values do not create a valid operational Request.
8. Record the test results with:
- function name;
- host;
- input;
- expected result;
- actual result;
- pass/fail;
- notes.
Final artifact
Create:
- C02-CH07_Nova_Field_Service_Deluge_Functions_v0.1.md;
- calculatePriority;
- validateRequest;
- test harness or test table;
- Creator form adapter;
- null-handling notes;
- host-context notes;
- mocked expected output.
Cleanup
Remove or disable test custom functions and validation adapters created in a shared development environment if they are not needed for later chapters. Delete only synthetic test records.
Offline alternative
Write the functions and test cases in a Markdown file and evaluate the expected results by inspection or a separate Deluge practice environment. This demonstrates language reasoning but cannot prove Creator editor compatibility or form-event behavior.
6. Independent challenge
Changed rules
Nova introduces emergency classification:
1. incident_level = "Emergency" produces High.
2. safety_risk = true produces High.
3. incident_level = "Urgent" produces Medium unless safety risk is true.
4. All other valid incident levels produce Low.
5. Valid incident levels are Emergency, Urgent and Normal.
6. A valid Request requires:
- external request key;
- customer business ID;
- non-blank description;
- valid incident level;
- calculated priority matching the supplied priority.
7. If the calculated priority and supplied priority differ, validation fails.
8. A missing or null safety risk is invalid because the classification rule requires an explicit Boolean.
9. The function must return every validation error, not only the first one.
Challenge input
case_id,external_request_key,customer_business_id,description,incident_level,safety_risk,supplied_priority,expected_valid
C-001,EXT-C-001,NOV-CUST-001,Water entering electrical room,Emergency,false,High,true
C-002,EXT-C-002,NOV-CUST-002,Door access failure,Urgent,false,Medium,true
C-003,EXT-C-003,NOV-CUST-001,Generator alarm,Normal,true,High,true
C-004,EXT-C-004,NOV-CUST-001,Filter replacement,Normal,false,High,false
C-005,EXT-C-005,NOV-CUST-001,,Emergency,true,High,false
C-006,,NOV-CUST-001,Alarm active,Emergency,true,High,false
C-007,EXT-C-007,NOV-CUST-001,Alarm active,,false,High,false
C-008,EXT-C-008,NOV-CUST-001,Alarm active,Emergency,,High,false
Deliverables
Produce:
- updated priority-calculation function;
- updated validation function;
- a test harness or complete test table;
- a Creator On Validate adapter;
- expected result for every supplied row;
- an explanation of null, blank, false and mismatched-priority behavior;
- a note identifying which code is Creator-specific and which code is reusable.
Success criteria
Your solution succeeds when:
- C-001, C-002 and C-003 are valid;
- C-004 fails because supplied priority does not match calculated priority;
- C-005 fails because description is blank;
- C-006 fails because external key is missing;
- C-007 fails because incident level is missing;
- C-008 fails because safety risk is null;
- a single invalid case may contain multiple errors;
- false safety risk is not treated as missing;
- the Creator adapter blocks invalid form submission only in the Creator On Validate context.
7. Common problems and recovery
Symptom	Diagnosis	Correction
= is used in a condition	Assignment and comparison were confused	Use == for comparison
Missing map key causes an unexpected result	get returned null	Check null before using the value
false is treated as missing	Truthiness was used	Distinguish null from Boolean false
Empty and spaces-only descriptions pass	String normalization is missing	Use null and blank checks
Function returns text on success and map on failure	Return shape is unstable	Always return one documented shape
Creator input is pasted into a CRM function	Host context was ignored	Define explicit CRM function arguments
cancel submit is used in Flow	Creator-only task was used in another host	Move blocking behavior to Creator On Validate
Date strings are compared lexically	Date-time values were treated as text	Use date-time fields and date functions
A form object is passed to a map function	Reusable function depends on host object	Adapt form fields into a map
A list is modified while being processed	Loop state becomes unpredictable	Collect IDs first, then update
An invalid priority is silently replaced	Validation and defaulting were mixed	Return an explicit error or approved fallback
A function queries and updates records during calculation	Pure logic has hidden side effects	Separate calculation from record operations
A test checks only valid input	Negative behavior is untested	Add null, blank, false, duplicate and mismatch cases
Field link names do not resolve	Proposed names were assumed to be final	Verify names in target environment
8. Check your understanding
 1. What is the difference between a Deluge list, map and Creator record collection?
 2. What does request.get("unknown_key") return when the key is absent?
 3. Why should false not be treated as a missing safety-risk value?
 4. What does this expression do?
queueName = if(priority == "High", "Urgent Queue", "Standard Queue");
 5. Which host supports cancel submit;?
 6. Why should a reusable validation function return a map rather than display an alert itself?
 7. What should happen when Due_At is null?
 8. Why should a priority calculation function not also create a Job record?
 9. Which input cases must a date-duration function test?
10. What is the expected result for a Request with a valid customer, description and external key but priority "Urgent"?
11. Why must a Creator form adapter check a lookup before reading one of its fields?
12. What is the purpose of a test harness that returns total, passed and results?
9. Solutions and explanations
Lesson quick checks
1. = assigns a value; == compares values.
2. NOV-REQ-001 should be stored as text because its prefix and formatting are meaningful.
3. The condition requires both a High priority and a found customer.
4. List() creates a list; Map() creates a map; Jobs[criteria] returns a Creator record collection.
5. An absent map key returns null, so the caller must handle the missing value before using it.
6. A Creator record collection may contain zero, one or many records. Checking its count prevents empty-result errors and incomplete processing.
For conditions, the emergency priority must be calculated before approval routing. Otherwise a record can be routed as Low or Medium before the Emergency rule changes its priority to High.
For null handling, false is a meaningful Boolean value. A null check should establish whether the value exists; a separate Boolean comparison should evaluate whether it is true or false.
For reusable functions, a map return gives the caller structured errors without tying the function to a user interface. The Creator adapter can display an alert, while a CRM function or Flow step can log or map the errors differently.
For date values, test:
- both dates present;
- start before end;
- equal timestamps;
- end before start;
- null start;
- null end;
- timezone rule;
- unfinished record.
For the "Urgent" priority case, validation should reject it because the allowed stored priorities are Low, Medium and High. If "Urgent" is an input classification, calculate its stored priority as Medium before validation.
Worked-case results
Priority outputs:
Case	Output
P-001	High
P-002	Medium
P-003	Low
P-004	High
P-005	Low fallback
Validation outputs:
Case	Valid	Error
V-001	Yes	None
V-002	No	External request key is required
V-003	No	Customer business ID is required
V-004	No	Description is required
V-005	No	Priority must be Low, Medium, or High
V-006	Yes	None
The Creator adapter must check:
if(isNull(input.Customer))
{
    alert "Customer is required";
    cancel submit;
}
before reading:
input.Customer.Customer_Business_ID
Otherwise a missing lookup may cause a runtime error instead of a controlled validation result.
Guided-practice sample solution
The two reusable functions are:
string calculatePriority(map request)
{
    incidentLevel = request.get("incident_level");
    safetyRisk = request.get("safety_risk");

    if(incidentLevel == "Emergency" || safetyRisk == true)
    {
        return "High";
    }
    else if(incidentLevel == "Urgent")
    {
        return "Medium";
    }
    else
    {
        return "Low";
    }
}
map validateRequest(map request)
{
    errors = List();
    allowedPriorities = {"Low", "Medium", "High"};

    externalKey = request.get("external_request_key");
    customerId = request.get("customer_business_id");
    description = request.get("description");
    priority = request.get("priority");

    if(isNull(externalKey) || isBlank(externalKey))
    {
        errors.add("external_request_key is required");
    }

    if(isNull(customerId) || isBlank(customerId))
    {
        errors.add("customer_business_id is required");
    }

    if(isNull(description) || isBlank(description))
    {
        errors.add("description is required");
    }

    if(isNull(priority) || !allowedPriorities.contains(priority))
    {
        errors.add("priority must be Low, Medium, or High");
    }

    result = Map();
    result.put("valid", errors.size() == 0);
    result.put("errors", errors);
    return result;
}
The Creator adapter is:
if(isNull(input.Customer))
{
    alert "Customer is required";
    cancel submit;
}

requestMap = Map();
requestMap.put("external_request_key", input.External_Request_Key);
requestMap.put("customer_business_id", input.Customer.Customer_Business_ID);
requestMap.put("description", input.Description);
requestMap.put("priority", input.Priority);

validation = validateRequest(requestMap);

if(validation.get("valid") == false)
{
    alert validation.get("errors").toString();
    cancel submit;
}
Expected guided results:
Case	Expected
T-001	High
T-002	Medium
T-003	Low
T-004	High
T-005	Low
T-101	Valid
T-102	Invalid, missing external key
T-103	Invalid, missing customer
T-104	Invalid, missing description
T-105	Invalid priority
T-106	Valid
Null and boundary results:
Case	Expected
N-001	Reject null description
N-002	Reject empty description
N-003	Reject spaces-only description
N-004	Treat false safety risk as a supplied Boolean
N-005	Reject numeric zero as an invalid priority
Independent-challenge sample solution
Updated priority function:
string calculateEmergencyPriority(map request)
{
    incidentLevel = request.get("incident_level");
    safetyRisk = request.get("safety_risk");

    if(incidentLevel == "Emergency" || safetyRisk == true)
    {
        return "High";
    }
    else if(incidentLevel == "Urgent")
    {
        return "Medium";
    }
    else
    {
        return "Low";
    }
}
Updated validation function:
map validateEmergencyRequest(map request)
{
    errors = List();
    validIncidentLevels = {"Emergency", "Urgent", "Normal"};
    allowedPriorities = {"Low", "Medium", "High"};

    externalKey = request.get("external_request_key");
    customerId = request.get("customer_business_id");
    description = request.get("description");
    incidentLevel = request.get("incident_level");
    safetyRisk = request.get("safety_risk");
    suppliedPriority = request.get("supplied_priority");

    if(isNull(externalKey) || isBlank(externalKey))
    {
        errors.add("external_request_key is required");
    }

    if(isNull(customerId) || isBlank(customerId))
    {
        errors.add("customer_business_id is required");
    }

    if(isNull(description) || isBlank(description))
    {
        errors.add("description is required");
    }

    if(isNull(incidentLevel) || !validIncidentLevels.contains(incidentLevel))
    {
        errors.add("incident_level must be Emergency, Urgent, or Normal");
    }

    if(isNull(safetyRisk))
    {
        errors.add("safety_risk must be true or false");
    }

    if(isNull(suppliedPriority) || !allowedPriorities.contains(suppliedPriority))
    {
        errors.add("supplied_priority is invalid");
    }

    if(errors.size() == 0)
    {
        calculatedPriority = calculateEmergencyPriority(request);

        if(calculatedPriority != suppliedPriority)
        {
            errors.add("supplied_priority does not match calculated priority");
        }
    }

    result = Map();
    result.put("valid", errors.size() == 0);
    result.put("errors", errors);
    return result;
}
Expected challenge results:
Case	Valid	Explanation
C-001	Yes	Emergency calculates High; all fields valid
C-002	Yes	Urgent calculates Medium; all fields valid
C-003	Yes	Safety risk calculates High
C-004	No	Normal with no safety risk calculates Low, not supplied High
C-005	No	Description is blank
C-006	No	External key is missing
C-007	No	Incident level is missing
C-008	No	Safety risk is null
Multiple missing values	No	All applicable errors are returned
The functions are reusable because they accept maps and return data. The Creator adapter is host-specific because it reads input, displays an alert and uses cancel submit.
10. Chapter recap and next step
You should now be able to:
- assign and compare Deluge values correctly;
- use operators and conditions;
- create and process lists;
- create, read and update maps;
- distinguish in-memory collections from Creator record collections;
- loop through values, maps and records;
- normalize strings;
- handle null, blank, empty, false and zero deliberately;
- compare and format dates safely;
- write reusable functions with predictable return shapes;
- adapt reusable functions to a Creator form context;
- test normal, invalid, null and boundary cases.
Your project artifacts from this chapter are:
- C02-CH07_Nova_Field_Service_Deluge_Functions_v0.1.md;
- calculatePriority;
- validateRequest;
- test harness or test table;
- Creator On Validate adapter;
- null and date-handling notes;
- host-context documentation.
Chapter 8 applies Deluge to Creator record operations. It will distinguish Creator record tasks from integration tasks, use criteria and search, create and update related records, map values and handle partial failures.
11. Glossary and further reading
Glossary
Boolean  
A value that is true or false.
Collection  
A group of records or values processed together. In Creator, a form criteria query returns a collection of records.
Date-time  
A value containing a date and time that can be compared or formatted.
Function  
A reusable block of logic that accepts inputs and returns a result.
List  
An ordered group of values.
Map  
A key-value data structure.
Null  
The absence of a value.
Record object  
A host-specific representation of a stored record, such as a Creator form record.
Return shape  
The documented structure and meaning of a function’s returned value.
String or text  
A sequence of characters.
Type  
The category of a value, such as text, number, Boolean, list or map.
Further reading
- Introduction to Deluge (https://www.zoho.com/deluge/help/) — official overview of Deluge, supported Zoho services and scripting use cases.
- Deluge Conditional Statements (https://www.zoho.com/deluge/help/conditional-statements/condition.html) — official if, else if, else, conditional and ifNull reference.
- Deluge List Functions (https://www.zoho.com/deluge/help/functions/list.html) — official list operations such as add, contains, size and get.
- Deluge put() Function (https://www.zoho.com/deluge/help/functions/map/put.html) — official map insertion and overwrite behavior.
- Deluge get() Function (https://www.zoho.com/deluge/help/functions/map/get.html) — official map lookup and missing-key behavior.
- Deluge Null, Blank and Empty Values (https://www.zoho.com/deluge/help/functions/common/isnull-isblank-isempty-difference.html) — official comparison of null, blank and empty functions.
- Deluge Date-Time Functions (https://www.zoho.com/deluge/help/functions/datetime.html) — official date and time operations.
- Deluge daysBetween() (https://www.zoho.com/deluge/help/functions/datetime/daysbetween.html) — official date-duration reference.
- Creator cancel submit (https://www.zoho.com/deluge/help/misc-statements/cancel-submit.html) — official Creator-only validation task.
- Deluge trim() (https://www.zoho.com/deluge/help/functions/string/trim.html) — official string normalization reference.
- Deluge replaceAll() (https://www.zoho.com/deluge/help/functions/string/replaceall.html) — official string replacement reference.
