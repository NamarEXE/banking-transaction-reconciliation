import random
from decimal import Decimal
from datetime import date, timedelta
import csv
import json


##generate a list of dictionaries to represent bank transactions
def generate_bank_transactions(count):
    transactions =[]

    ##generate a start date for transactions to be within the last 90 days
    start_date = date.today() - timedelta(days=90)

    ##loop to generate x amount of transactions
    for i in range(count):

        ##generate transaction_ids
        transaction_id = f"TX{i+1:05d}"
        account_id = f"ACC{random.randint(1001, 9999)}"

        ##generate amount using randint get amount for pennies then convert to currency amount using Decimal
        pennies = random.randint(1000,500000)
        amount = Decimal(pennies) / Decimal(100)

        ##generate date for transaction 
        transaction_date = start_date + timedelta(days=random.randint(0, 90))
        
        ##create transaction as a dictionary
        transaction = {
            'transaction_id': transaction_id,
            'account_id': account_id,
            'transaction_date':transaction_date.strftime('%Y-%m-%d'),
            'amount': f"{amount:.2f}",
            'currency': 'GBP',
            'transaction_type': 'PAYMENT',
            'status':'COMPLETED'
        }

        ##add transaction to the list of transactions
        transactions.append(transaction)

    ##after loop return the list of transactions    
    return transactions


##save bank transactions to CSV
def save_to_csv(transactions,filepath):

    fieldnames = [
        'transaction_id',
        'account_id',
        'transaction_date',
        'amount',
        'currency',
        'transaction_type',
        'status'
        ] 

    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        ##initiate csv.DictWriter with the file and fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(transactions)


##generate matching payment transactions from bank transactions
def generate_payment_transactions(bank_transactions):
    payment_transactions = []

    for transaction in bank_transactions:
        payment_transactions.append(transaction.copy())
    return payment_transactions

##save payment transactions to JSON
def save_to_json(transactions, filepath):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(transactions, file, indent=4)




##Exception generator
def introduce_exceptions(bank_transactions, payment_transactions):
    ##for loop to to iterate every transaction and create exceptions of duplicates and mismatches by removing records. 
    for transaction in bank_transactions.copy():

        ##TX00001: create a mismatch from bank_transactions by removing it from the bank_transactions
        if transaction['transaction_id'] == 'TX00001':
            bank_transactions[:] = [t for t in bank_transactions if t['transaction_id'] != 'TX00001']

        ##TX00002: create a mismatch from payments_transaction by removing it from the payment_transactions list
        if transaction['transaction_id'] == 'TX00002':
            payment_transactions[:] = [t for t in payment_transactions if t['transaction_id'] != 'TX00002']

        ##TX00005: create duplicate record in bank_transactions by appending a copy of the transaction to the list
        if transaction['transaction_id'] == 'TX00005':
            duplicate_transaction = transaction.copy()
            bank_transactions.append(duplicate_transaction)

    ##for loop to iterate payment_transactions and create exceptions/mismatches for specific transaction_ids
    for transaction in payment_transactions.copy():
        ##TX00003: create amount mismatch by adding £10 to the bank transaction amount
        if transaction['transaction_id']== 'TX00003':
            original_amount = Decimal(transaction['amount'])
            updated_amount = original_amount + Decimal('10.00')
            transaction['amount'] = f"{updated_amount:.2f}"

        ##TX00004: create Currency Mismatch - change currency from GBP to EUR
        if transaction['transaction_id'] == 'TX00004':
            transaction['currency'] = 'EUR'

        ##TX00006: create invalid records exception by setting payment amount to INVALID
        if transaction['transaction_id'] == 'TX00006':
            transaction['amount'] = 'INVALID'




##main code run 
if __name__ == "__main__":
    transactions = generate_bank_transactions(100)
    payment_transactions = generate_payment_transactions(transactions)
    print('transactions and payments generated successfully')

    introduce_exceptions(transactions, payment_transactions)
    print('exceptions introduced successfully')


    save_to_csv(transactions, 'data/raw/bank_transactions.csv')
    print('bank transactions saved to CSV successfully')

    save_to_json(payment_transactions, 'data/raw/payment_transactions.json')
    print('payment transactions saved to JSON successfully')