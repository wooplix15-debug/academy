"""Standard-library teaching simulator; no network calls or Zoho credentials."""
import argparse
import csv
import json
import re
import sqlite3
from pathlib import Path

EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

def classify_leads(rows, require_company=True):
    accepted, rejected, excluded, seen = [], [], [], set()
    for source in rows:
        row = dict(source)
        row['email'] = row.get('email', '').strip().lower()
        reasons = []
        if not row.get('last_name', '').strip(): reasons.append('missing_lab_required_name')
        if require_company and not row.get('company', '').strip(): reasons.append('missing_lab_required_company')
        if not EMAIL.fullmatch(row['email']): reasons.append('invalid_lab_email_format')
        if reasons:
            rejected.append({**row, 'reason': ';'.join(reasons)})
        elif row['email'] in seen:
            excluded.append({**row, 'reason': 'duplicate_normalized_email_keep_first'})
        else:
            seen.add(row['email'])
            row['owner_queue'] = {'West':'West Sales', 'East':'East Sales'}.get(row.get('region'), 'Review Queue')
            accepted.append(row)
    assert len(rows) == len(accepted) + len(rejected) + len(excluded)
    return {'accepted': accepted, 'rejected': rejected, 'excluded': excluded,
            'counts': {'source': len(rows), 'accepted': len(accepted), 'rejected': len(rejected), 'excluded': len(excluded)}}

class SyncStore:
    """SQLite uniqueness and transactions simulate destination controls.
    This is not a Zoho API adapter, and does not claim all side effects run once.
    Never call real external APIs inside this transaction.
    """
    def __init__(self, path=':memory:'):
        self.db = sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS requests (business_key TEXT PRIMARY KEY, version INTEGER NOT NULL, amount INTEGER NOT NULL)')

    def get(self, key):
        r = self.db.execute('SELECT business_key,version,amount FROM requests WHERE business_key=?', (key,)).fetchone()
        return dict(zip(('business_key','version','amount'), r)) if r else None

    def write(self, key, version, amount, failure=None):
        if not isinstance(key, str) or not key.strip(): raise ValueError('missing_key')
        if type(version) is not int or version < 1: raise ValueError('invalid_version')
        if type(amount) is not int or amount < 0: raise ValueError('invalid_integer_amount')
        if failure == 'unauthorized': raise PermissionError('authorization_denied')
        if failure == 'quota': return {'status':'paused_quota', 'key':key}
        # A database transaction serializes local competing writers.
        try:
            self.db.execute('BEGIN IMMEDIATE')
            existing = self.get(key)
            if existing and version < existing['version']:
                status = 'stale_rejected'
            elif existing and version == existing['version']:
                status = 'replayed' if amount == existing['amount'] else 'conflict_rejected'
            elif existing:
                self.db.execute('UPDATE requests SET version=?, amount=? WHERE business_key=?', (version,amount,key))
                status = 'updated'
            else:
                self.db.execute('INSERT INTO requests VALUES (?,?,?)', (key,version,amount))
                status = 'created'
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        if failure == 'timeout_after_commit': raise TimeoutError('response_lost_outcome_unknown')
        return {'status':status, 'record': self.get(key)}

    def close(self): self.db.close()

def eligible_sources(records, permission='public'):
    return [r for r in records if r['status']=='approved' and r['permission']==permission and r.get('current') is True]

def retrieve(query, records, permission='public'):
    """Lexical search for evidence only. No embeddings or model generation.
    Attack resistance beyond this toy fixture requires live model evaluations.
    """
    words=set(re.findall(r'[a-z0-9]+', query.lower()))
    candidates=[]
    for record in eligible_sources(records, permission):
        score=len(words & set(re.findall(r'[a-z0-9]+', record['text'].lower())))
        if score: candidates.append((score,record['id'],record))
    if not candidates: return {'status':'abstain', 'source_ids':[], 'evidence':[]}
    candidates.sort(key=lambda x:(-x[0],x[1]))
    top=candidates[:2]
    if any(r.get('conflict_group') for _,_,r in top) and len(top)>1 and top[0][2].get('conflict_group') == top[1][2].get('conflict_group'):
        return {'status':'conflict_review', 'source_ids':[r['id'] for _,_,r in top], 'evidence':[r['text'] for _,_,r in top]}
    return {'status':'evidence_found', 'source_ids':[top[0][2]['id']], 'evidence':[top[0][2]['text']]}

def synthetic_cost(input_tokens, output_tokens, input_per_million, output_per_million):
    if any(v < 0 for v in (input_tokens,output_tokens,input_per_million,output_per_million)): raise ValueError('negative_usage')
    return (input_tokens * input_per_million + output_tokens * output_per_million)/1_000_000

def sync_demo():
    store=SyncStore(); trace=[]
    try:
        trace.append(store.write('NOVA-D001',1,1250))
        trace.append(store.write('NOVA-D001',1,1250))
        try: store.write('NOVA-D002',1,800,failure='timeout_after_commit')
        except TimeoutError:
            trace.append({'status':'timeout_reconciled', 'record':store.get('NOVA-D002')})
        trace.append(store.write('NOVA-D001',2,1500))
        trace.append(store.write('NOVA-D001',1,1250))
        trace.append(store.write('NOVA-D001',2,9999))
        count=store.db.execute('SELECT COUNT(*) FROM requests').fetchone()[0]
        return {'trace':trace,'destination_rows':count,'latest_D001':store.get('NOVA-D001')}
    finally: store.close()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('exercise', choices=['migration','sync','retrieval','cost'])
    parser.add_argument('--out',type=Path, help='Optional directory for local results')
    args=parser.parse_args(); root=Path(__file__).resolve().parents[1]
    if args.exercise=='migration':
        with (root/'materials/datasets/leads_50.csv').open(newline='') as f: rows=list(csv.DictReader(f))
        result=classify_leads(rows)
    elif args.exercise=='sync': result=sync_demo()
    elif args.exercise=='retrieval':
        records=json.loads((root/'materials/datasets/knowledge_records.json').read_text())
        result={q:retrieve(q,records) for q in ['certificate issuer','job guarantee','client secret','attendance threshold']}
    else: result={'cost_usd':synthetic_cost(10000,2000,1,4),'rates':'Synthetic teaching inputs; not current vendor prices'}
    if args.out:
        args.out.mkdir(parents=True,exist_ok=True)
        (args.out/(args.exercise+'_result.json')).write_text(json.dumps(result,indent=2)+'\n')
        if args.exercise=='migration':
            for kind in ('accepted','rejected','excluded'):
                values=result[kind]
                with (args.out/(kind+'.csv')).open('w',newline='') as f:
                    writer=csv.DictWriter(f,fieldnames=list(values[0]) if values else list(rows[0])); writer.writeheader(); writer.writerows(values)
    print(json.dumps(result if args.exercise!='migration' else result['counts'],indent=2))

if __name__=='__main__': main()
