import csv
import json
import tempfile
import unittest
from pathlib import Path
from practice_lab import classify_leads, SyncStore, retrieve, eligible_sources, synthetic_cost, sync_demo

ROOT=Path(__file__).resolve().parents[1]
class PracticalTests(unittest.TestCase):
    def rows(self):
        with (ROOT/'materials/datasets/leads_50.csv').open(newline='') as f: return list(csv.DictReader(f))
    def test_reconciliation(self):
        result=classify_leads(self.rows()); self.assertEqual(result['counts'],{'source':50,'accepted':42,'rejected':5,'excluded':3})
    def test_invalid_reasons(self):
        result=classify_leads(self.rows()); self.assertEqual(len(result['rejected']),5)
        self.assertTrue(all(x['reason'] for x in result['rejected']))
    def test_email_normalization(self):
        r=self.rows()[0]; r['email']='  PERSON001@EXAMPLE.TEST  '
        result=classify_leads([r]); self.assertEqual(result['accepted'][0]['email'],'person001@example.test')
    def test_duplicate_case(self):
        rows=self.rows()[:2]; rows[1]['email']=rows[0]['email'].upper()
        self.assertEqual(classify_leads(rows)['counts']['excluded'],1)
    def test_missing_region_routes_review(self):
        row=self.rows()[0]; row['region']=''; self.assertEqual(classify_leads([row])['accepted'][0]['owner_queue'],'Review Queue')
    def test_policy_change(self):
        self.assertEqual(classify_leads(self.rows(),require_company=False)['counts']['accepted'],43)
    def test_zero_amount(self):
        s=SyncStore(); self.addCleanup(s.close); self.assertEqual(s.write('K',1,0)['status'],'created')
    def test_duplicate_does_not_create(self):
        s=SyncStore(); self.addCleanup(s.close); s.write('K',1,2); self.assertEqual(s.write('K',1,2)['status'],'replayed')
        self.assertEqual(s.db.execute('SELECT count(*) FROM requests').fetchone()[0],1)
    def test_timeout_committed(self):
        s=SyncStore(); self.addCleanup(s.close)
        with self.assertRaises(TimeoutError): s.write('K',1,2,'timeout_after_commit')
        self.assertEqual(s.get('K')['amount'],2); self.assertEqual(s.write('K',1,2)['status'],'replayed')
    def test_stale_update(self):
        s=SyncStore(); self.addCleanup(s.close); s.write('K',2,10)
        self.assertEqual(s.write('K',1,9)['status'],'stale_rejected'); self.assertEqual(s.get('K')['amount'],10)
    def test_same_version_conflict(self):
        s=SyncStore(); self.addCleanup(s.close); s.write('K',1,10)
        self.assertEqual(s.write('K',1,99)['status'],'conflict_rejected'); self.assertEqual(s.get('K')['amount'],10)
    def test_authorization_no_write(self):
        s=SyncStore(); self.addCleanup(s.close)
        with self.assertRaises(PermissionError): s.write('K',1,2,'unauthorized')
        self.assertIsNone(s.get('K'))
    def test_quota_no_write(self):
        s=SyncStore(); self.addCleanup(s.close); self.assertEqual(s.write('K',1,2,'quota')['status'],'paused_quota'); self.assertIsNone(s.get('K'))
    def test_invalid_amount(self):
        s=SyncStore(); self.addCleanup(s.close)
        for amount in (-1,True,'10',1.5):
            with self.assertRaises(ValueError): s.write('K',1,amount)
    def test_two_connections_unique(self):
        with tempfile.TemporaryDirectory() as d:
            a=SyncStore(str(Path(d)/'store.db')); b=SyncStore(str(Path(d)/'store.db'))
            try:
                a.write('K',1,1); self.assertEqual(b.write('K',1,1)['status'],'replayed')
                self.assertEqual(b.db.execute('SELECT count(*) FROM requests').fetchone()[0],1)
            finally: a.close(); b.close()
    def records(self): return json.loads((ROOT/'materials/datasets/knowledge_records.json').read_text())
    def test_eligibility(self): self.assertEqual([r['id'] for r in eligible_sources(self.records())],['K1','K5','K6'])
    def test_restricted_abstention(self): self.assertEqual(retrieve('client secret',self.records())['status'],'abstain')
    def test_supported_evidence(self): self.assertEqual(retrieve('certificate issuer',self.records())['source_ids'],['K1'])
    def test_conflicting_evidence(self): self.assertEqual(retrieve('attendance threshold',self.records())['status'],'conflict_review')
    def test_unknown_abstention(self): self.assertEqual(retrieve('job guarantee',self.records())['status'],'abstain')
    def test_synthetic_cost(self): self.assertAlmostEqual(synthetic_cost(10000,2000,1,4),0.018)
    def test_negative_usage(self):
        with self.assertRaises(ValueError): synthetic_cost(-1,0,1,4)
    def test_demo_final_state(self):
        r=sync_demo(); self.assertEqual(r['destination_rows'],2); self.assertEqual(r['latest_D001']['version'],2); self.assertEqual(r['latest_D001']['amount'],1500)

if __name__=='__main__': unittest.main()
