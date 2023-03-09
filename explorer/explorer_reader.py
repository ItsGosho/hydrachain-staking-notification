import logging
from hydrachain_explorer_requester.explorer_requester import ExplorerRequester
from hydrachain_explorer_requester.query_parameters import TransactionsQueryParameters

logger = logging.getLogger(__name__)


class ExplorerReader:

    def __init__(self, explorer_requester: ExplorerRequester = ExplorerRequester()):
        self.explorer_requester = explorer_requester

    def request_transactions_created_after(self, address, created_after):

        transactions_created_after = []

        for transaction in self.get_address_transactions_iterator(address):

            if (transaction["timestamp"] >= created_after.timestamp()):
                transactions_created_after.append(transaction)
            else:
                return transactions_created_after

    def request_mined_transactions_created_after(self, address, created_after):
        transactions_created_after = self.request_transactions_created_after(address, created_after)
        logger.debug(
            f"Transactions of address {address} created after {created_after} are {transactions_created_after}")

        filteredTransactions = list(
            filter(lambda transaction: transaction["isCoinstake"] == True, transactions_created_after))
        return filteredTransactions

    def get_address_transactions_iterator(self, address):

        query_parameters = TransactionsQueryParameters()
        query_parameters.set_page(0)
        query_parameters.set_page_size(20)

        while True:
           address_transactions_response = self.explorer_requester.get_address_transactions(address, query_parameters)
           transaction_ids = address_transactions_response["transactions"]

           if len(transaction_ids) == 0:
               break

           transactions = self.explorer_requester.get_transactions(transaction_ids)

           for transaction in transactions:
               yield transaction

           query_parameters.set_page(query_parameters.page.value + 1)
