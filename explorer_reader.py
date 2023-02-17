import json
import datetime

import requests


def request_address_transaction_ids(address, page=0, pageSize=20):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    url = f"https://explorer.hydrachain.org/7001/address/{address}/txs?page={page}&pageSize={pageSize}"
    response = requests.get(url=url, headers=headers)
    return response.json()


def request_transactions(transaction_ids):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    url = f"https://explorer.hydrachain.org/7001/txs/{','.join(transaction_ids)}"
    response = requests.get(url=url, headers=headers)
    return response.json()


def request_transactions_created_after(address, datetime):
    transactions_created_after = []

    while True:
        address_transaction_ids = request_address_transaction_ids(address)["transactions"]
        transactions = request_transactions(address_transaction_ids)

        for transaction in transactions:
            if (transaction["timestamp"] >= datetime.timestamp()):
                transactions_created_after.append(transaction)
            else:
                return transactions_created_after

def request_mined_transactions_after(address, datetime):
    transactions_created_after = request_transactions_created_after(address, datetime)

    filteredTransactions = filter(lambda transaction: transaction["isCoinstake"] == True, transactions_created_after)
    return list(filteredTransactions)


# address = "XXX"
# mined_transactions_until = request_mined_transactions_after(address, datetime.datetime.now() - datetime.timedelta(days =10))
# print(json.dumps(mined_transactions_until, indent = 4))

# def requestAllAddressTransactions(address):
#
#     addressTransactionIds = requestAllAddressTransactionIds(address)["transactions"]
#     allAddressTransactions = []
#     atTime = 20
#     for j in range(0, len(addressTransactionIds), atTime):
#         transactionIds = addressTransactionIds[j: j + atTime]
#         transactions = requestTransactions(transactionIds)
#         allAddressTransactions.extend(transactions)
#
#     return allAddressTransactions
