from decimal import Decimal, InvalidOperation
from datetime import datetime

def validate_transaction(transaction):

    ##check input is correct type
    if not isinstance(transaction, dict):
        return False

    required_fields = [
    'transaction_id',
    'account_id',
    'transaction_date',
    'amount',
    'currency',
    'transaction_type',
    'status'
    ]


    ## validate all required keys are present
    for field in required_fields:
        if field not in transaction:
            return False

    ##validate account id is of string type and account_id is not null or empty
    if isinstance(transaction['account_id'], str):
        if transaction['account_id'].strip() == '':
            return False
    else:
        return False

    ##validate transaction_id is of string type and transaction_id is not null or empty
    if isinstance(transaction['transaction_id'], str):
        if transaction['transaction_id'].strip() == '':
            return False
    else:
        return False

    ##validate amount value is valid
    try: 
        amount = Decimal(transaction['amount'])

        if not amount.is_finite():
            return False
        if (amount <= 0) or amount.as_tuple().exponent != -2:
            return False
    except (InvalidOperation, ValueError, TypeError):
        return False


    ##validate dates
    try:
        parsed_date = datetime.strptime(transaction['transaction_date'],'%Y-%m-%d')
        formatted_date = parsed_date.strftime('%Y-%m-%d')
        if (formatted_date!=transaction['transaction_date']):
            return False
    except (ValueError,TypeError):
        return False

    ##validate currency
    if not isinstance(transaction['currency'], str):
        return False
    
    if transaction['currency'].isalpha() == False or transaction['currency'].isupper() == False or len(transaction['currency']) !=3:
        return False
    # if transaction['currency'] not in ['GBP','USD','EUR']:
    #     return False

    ##validate status
    if transaction['status'] != 'COMPLETED':
        return False

    ##validate transaction_type
    if transaction['transaction_type'] != 'PAYMENT':
            return False



    return True

    








if __name__ == "__main__":

    valid_transaction = {
        'transaction_id': 'TX00001',
        'account_id': 'ACC1001',
        'transaction_date': '2026-11-11',
        'amount': '11.11',
        'currency': 'GBP',
        'transaction_type': 'PAYMENT',
        'status': 'COMPLETED'
    }


    print(validate_transaction(valid_transaction))

    test_cases = [
    ("Valid transaction", "amount", "125.50", True),
    ("Invalid amount", "amount", "INVALID", False),
    ("Negative amount", "amount", "-50.00", False),
    ("Zero amount", "amount", "0.00", False),
    ("One decimal", "amount", "125.5", False),
    ("Three decimals", "amount", "125.456", False),
    ("NaN amount", "amount", "NaN", False),
    ("Valid EUR", "currency", "EUR", True),
    ("Null currency", "currency", None, False),
    ("Numeric currency", "currency", 123, False),
    ("Invalid date", "transaction_date", "2026-02-30", False),
    ("Wrong date format", "transaction_date", "21-11-2026", False),
    ("Empty account", "account_id", "", False),
    ("Whitespace account", "account_id", "   ", False)
    ]

    for name, field, value, expected in test_cases:
        transaction = valid_transaction.copy()
        transaction[field] = value

        actual = validate_transaction(transaction)

        if actual == expected:
            print(f"PASS: {name}")
        else:
            print(f"FAIL: {name} — Expected {expected}, got {actual}")

