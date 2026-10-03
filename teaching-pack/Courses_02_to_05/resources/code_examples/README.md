# Deluge teaching examples
These authored starters have been checked against official syntax references. They have not been compiled or executed in a connected Zoho editor. Trainers must rehearse the selected product context and record actual results before teaching live steps.

## Normalize requests for ZDV M03
Open normalize_requests.deluge in a training script editor. Trace before running.

| Input | Expected teaching result |
| --- | --- |
| T01 amount 0 | valid, numeric zero retained |
| T02 amount text 1250 | valid, numeric 1250 |
| T03 absent amount | missing_amount |
| T04 amount twelve | invalid_amount_format |
| T05 email with spaces and capitals | valid, email a@example.test |

Number formatting in info output can vary; compare numeric values rather than display formatting. This starter normalizes email but does not validate deliverability or enforce a complete request schema. Extend it with customer ID validation in ZDV-M04.

## Training record creation for ZDV M08
The second example defaults to disabled external writes. Before enabling, verify the training account, chosen connection, field API names and required layout fields. The documented V8 wrapper returns a direct id on success and error information on failure. The empty trigger list requests suppression of the documented CRM automations; verify actual behavior in the training organization. It does not establish idempotent creation.

Observe one approved training create, then a deliberately invalid input. Do not run the same create repeatedly to test recovery: repeated creation requires a reviewed duplicate-key strategy. Remove only the synthetic record created by the exercise after recording evidence.

## Sources checked 3 October 2026
- [V8 createRecord wrapper](https://www.zoho.com/deluge/help/crm/create-record-V8.html)
- [Null checks](https://www.zoho.com/deluge/help/functions/common/isnull.html)
- [Decimal conversion](https://www.zoho.com/deluge/help/functions/common/todecimal.html)
- [List iteration](https://www.zoho.com/deluge/help/list-manipulations/for-each-element.html)
- [Deluge data types](https://www.zoho.com/deluge/help/datatypes.html)

Source ID S13 groups these references. Keep a separate observed test log. Do not treat these drafts as evidence of a working business integration.
