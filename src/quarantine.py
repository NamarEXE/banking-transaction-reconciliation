from data_quality import find_duplicate_transactions
from validate import validate_transaction
from ingest import ingest_bank_transactions, ingest_payment_transactions

import json

def partition_transactions(transactions, source_name):
    accepted_records=[]
    quarantined_records=[]

    duplicateskeys = find_duplicate_transactions(transactions).keys()
    
    for transaction in transactions:
        reasons = []
        if isinstance(transaction, dict):
            transaction_id = transaction.get('transaction_id')
        else:
            transaction_id = None

        if (
        isinstance(transaction_id, str)
        and transaction_id.strip()
        ):
            
            if(validate_transaction(transaction)):
                if transaction_id in duplicateskeys:
                    quarantined_records.append({
                    'source':source_name,
                    'record':transaction,
                    'reasons':['DUPLICATE_TRANSACTION_ID']
                })
                else:
                    accepted_records.append(transaction)
            else:
                ##change insert format here later
                reasons.append('SCHEMA_INVALID')
                if transaction_id in duplicateskeys:
                    reasons.append('DUPLICATE_TRANSACTION_ID')

                quarantine_format = {
                                'source':source_name,
                                'record':transaction,
                                'reasons':reasons
                            }
                quarantined_records.append(quarantine_format)
        else:
            quarantine_format = {
            'source':source_name,
            'record':transaction,
            'reasons':['SCHEMA_INVALID']
            }
            quarantined_records.append(quarantine_format)


    output = {'source':source_name,
              'accepted_records':accepted_records,
              'quarantined_records':quarantined_records
              }


    assert (
    len(accepted_records) + len(quarantined_records)
    == len(transactions)
    ), "Record counts do not reconcile"
    
    return output

def export_results(partion_result,path_accept,path_quarantine):
    with open(file=path_accept,mode='w',encoding='utf-8') as file:
        json.dump(partion_result['accepted_records'],file,indent=4)

    with open(file=path_quarantine,mode='w',encoding='utf-8') as file:
        json.dump(partion_result['quarantined_records'],file,indent=4)



if __name__ == "__main__":
    payment_transactions = ingest_payment_transactions('data/raw/payment_transactions.json')
    partioned_data = partition_transactions(payment_transactions,'payment_transactions')
    export_results(partioned_data,'data/processed/payment_accepted.json','data/processed/payment_quarantine.json')

    bank_transactions = ingest_bank_transactions('data/raw/bank_transactions.csv')
    partioned_data = partition_transactions(bank_transactions,'bank_transactions')
    export_results(partioned_data,'data/processed/bank_accepted.json','data/processed/bank_quarantine.json')



    transaction1 = {
    'transaction_id': 'TX00010',
    'account_id': 'ACC1001',
    'transaction_date': '2026-11-21',
    'amount': '100.00',
    'currency': 'GBP',
    'transaction_type': 'PAYMENT',
    'status': 'COMPLETED'
    }

    transaction2 = transaction1.copy()
    transaction2['amount'] = 'INVALID'


    result = partition_transactions(
        [transaction1, transaction2],
        "bank"
    )

    for record in result['quarantined_records']:
        print(record['reasons'])


    test_transactions = [
        {'account_id': 'ACC1001'},
        {'transaction_id': ['TX00001']},
        None
    ]

    result = partition_transactions(
        test_transactions,
        "bank"
    )

    print(len(result['accepted_records']))
    print(len(result['quarantined_records']))





    

# payment_transactions = ingest_payment_transactions('data/raw/payment_transactions.json')
# partition_transactions(payment_transactions,'payment_transactions.json')


# banking_transactions = ingest_bank_transactions('data/raw/bank_transactions.csv')
# partition_transactions(banking_transactions,'bank_transactions.csv')
    
