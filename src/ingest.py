import csv
import json

##ingest bank transactions file data from csv file
def ingest_bank_transactions(filepath):
    transactions_list = []
    try:
        with open(filepath, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions_list.append(row)
        return transactions_list
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        raise
        

##ingest payments file data from json file
def ingest_payment_transactions(filepath):
    try:

        with open(filepath,mode='r',encoding='utf-8') as file:
            transactions = json.load(file)
        return transactions
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        raise








if __name__ == "__main__":

    bank_transactions = ingest_bank_transactions(
        "data/raw/bank_transactions.csv"
    )

    payment_transactions = ingest_payment_transactions(
        "data/raw/payment_transactions.json"
    )

    print(f"Bank records ingested: {len(bank_transactions)}")
    print(f"Payment records ingested: {len(payment_transactions)}")

    print("\nFirst bank transaction:")
    print(bank_transactions[0])

    print("\nFirst payment transaction:")
    print(payment_transactions[0])