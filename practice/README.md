# Run the practical exercises
Python 3.10 or newer. Standard library only. No keys, installs or network calls needed.
From the workspace folder:
```bash
python3 practice/practice_lab.py migration --out practice/results
python3 practice/practice_lab.py sync --out practice/results
python3 practice/practice_lab.py retrieval --out practice/results
python3 practice/practice_lab.py cost --out practice/results
python3 -m unittest discover -s practice -p 'test_*.py' -v
```
Migration: lab-policy validation yields 42 accepted, 5 rejected and 3 excluded. `accepted.csv` is a staging file, not proof of a successful Zoho import. Name/company/email rules are lab choices. Inspect actual layout and field metadata before configuring a real import.

Sync: this SQLite destination model shows stable keys, transactions, replay, a lost response after commit and version conflict. It does not call Zoho or implement a background retry worker. The two-connection test is sequential; concurrent load tests remain an extension.

Retrieval: lexical evidence lookup with status and permission filters. It is not an LLM, embedding index or production RAG system. The quarantined attack record checks source eligibility; it does not prove resistance to instructions inside an otherwise eligible document. Run the live-model evaluation cases separately.

Cost: synthetic rates are supplied to the formula for arithmetic practice; use current configured rates for actual estimation.

Try changes in a copy: alter company-required policy; add a conflicting same-version write; add an unsupported question. Predict before running, compare result, then explain the mismatch. Do not use real customer data.
