"""ZDV-M04 intentionally defective teaching code. Run, predict, then repair a copy.
Expected policy: customer ID required, zero permitted, numerical strings normalized.
This file is not used by the working migration or sync exercises.
"""
def defective_validate(payload):
    amount=payload.get('amount')
    if not amount:  # Seeded defect: rejects zero.
        return {'ok':False, 'error':'missing_amount'}
    if amount=='10':  # Seeded defect: string comparison skips numeric normalization.
        return {'ok':False, 'error':'special_case_ten'}
    return {'ok':True, 'amount':amount}  # Seeded defect: never checks customer ID.

if __name__=='__main__':
    cases=[({'customer_id':'C1','amount':0},True),
           ({'customer_id':'C1','amount':'10'},True),
           ({'customer_id':'','amount':20},False)]
    for payload,expected in cases:
        actual=defective_validate(payload)
        print({'input':payload,'expected_ok':expected,'actual':actual,'matches':actual['ok']==expected})
