import logging
from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

logger = logging.getLogger(__name__)


def request_transactions_created_after(address, created_after):
    explorer_requester = ExplorerRequester()

    transactions_created_after = []
    for transactionId in explorer_requester.get_address_transactions_iterator(address):
        transaction = explorer_requester.get_transaction(transactionId)

        if (transaction["timestamp"] >= created_after.timestamp()):
            transactions_created_after.append(transaction)
        else:
            return transactions_created_after


def request_mined_transactions_created_after(address, created_after):
    transactions_created_after = request_transactions_created_after(address, created_after)
    logger.debug(f"Transactions of address {address} created after {created_after} are {transactions_created_after}")

    filteredTransactions = list(
        filter(lambda transaction: transaction["isCoinstake"] == True, transactions_created_after))
    return filteredTransactions
