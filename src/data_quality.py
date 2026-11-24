from ingest import (ingest_bank_transactions, ingest_payment_transactions)
from validate import validate_transaction


def validate_dataset(transactions):
    count_pass = 0
    count_fail= 0
    invalid_records=[]

    
    for transaction in transactions:
        valid = validate_transaction(transaction)
        if valid:
            count_pass+=1
        else:
            count_fail+=1
            invalid_records.append(transaction)


    output = {'total_records':len(transactions),
              'valid_count':count_pass,
              'invalid_count':count_fail,
              'invalid_records':invalid_records
              }
    return output


def find_duplicate_transactions(transactions):
    count_dict = {}
    duplicate_dict = {}

    for transaction in transactions:

        if not isinstance(transaction, dict):
            continue

        transaction_id = transaction.get('transaction_id')

        if not isinstance(transaction_id, str):
            continue

        if not transaction_id.strip():
            continue


        if(transaction_id in count_dict):
            count_dict[transaction_id]+=1
        else:
            count_dict[transaction_id]=1

    for key in count_dict:
        if count_dict[key]>1:
            duplicate_dict[key]=count_dict[key]
            
    return(duplicate_dict)


def analyse_data_quality(transactions,source_name):
    

    validation = validate_dataset(transactions)
    duplicates = find_duplicate_transactions(transactions)

    output = {
        "source": source_name,
        "total_records": validation['total_records'],
        "valid_count": validation['valid_count'],
        "invalid_count": validation['invalid_count'],
        'invalid_records':validation['invalid_records'],
        "duplicate_ids": duplicates
    }
    return output




if __name__ == "__main__":
    print('Validate_dateset for payment_transactions:')
    payment_transactions = ingest_payment_transactions("data/raw/payment_transactions.json")
    print(validate_dataset(payment_transactions))
    print('\n')

    print('Validate_dateset for bank_transactions:')
    bank_transactions = ingest_bank_transactions("data/raw/bank_transactions.csv")
    print(validate_dataset(bank_transactions))
    print('\n')

    print('analyse_data_quality for payment_transactions')
    print(analyse_data_quality(payment_transactions,'payment'))
    print('\n')

    print('analyse_data_quality for bank_transactions')
    print(analyse_data_quality(bank_transactions,'bank'))

    print('\n\n\n\n')
    test_transactions = [
        {'transaction_id': 'TX00001'},
        {'transaction_id': 'TX00001'},
        {'account_id': 'ACC1001'},
        {'transaction_id': None},
        {'transaction_id': ['TX00002']},
        None
    ]

    print(find_duplicate_transactions(test_transactions))


    


