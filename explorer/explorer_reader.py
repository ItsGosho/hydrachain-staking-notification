import logging
import requests

logger = logging.getLogger(__name__)

def request_address_transaction_ids(address, page=0, page_size=20):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    url = f"https://explorer.hydrachain.org/7001/address/{address}/txs?page={page}&pageSize={page_size}"
    response = requests.get(url=url, headers=headers)
    logger.debug(f"GET {url} responded with status code {response.status_code}, body {response.content}")
    return response.json()


def request_transactions(transaction_ids):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    url = f"https://explorer.hydrachain.org/7001/txs/{','.join(transaction_ids)}"
    response = requests.get(url=url, headers=headers)
    logger.debug(response.content)
    return response.json()


def request_transactions_created_after(address, created_after):
    transactions_created_after = []

    while True:
        address_transaction_ids = request_address_transaction_ids(address)["transactions"]
        logger.debug(address_transaction_ids)
        transactions = request_transactions(address_transaction_ids)
        logger.debug(transactions)

        for transaction in transactions:
            if (transaction["timestamp"] >= created_after.timestamp()):
                transactions_created_after.append(transaction)
            else:
                return transactions_created_after


def request_mined_transactions_after(address, after):
    transactions_created_after = request_transactions_created_after(address, after)
    logger.debug(transactions_created_after)

    filteredTransactions = list(
        filter(lambda transaction: transaction["isCoinstake"] == True, transactions_created_after))
    logger.debug(filteredTransactions)
    return filteredTransactions

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