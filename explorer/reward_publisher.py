import datetime
import json
import time
import logging
from explorer import explorer_reader

logger = logging.getLogger(__name__)

class MinedTransaction:

    def __init__(self, date, amount, address):
        self.date = date
        self.amount = amount
        self.address = address

    def __str__(self):
        return f"{self.date}, {self.amount}, {self.address}"

class MinedTransactionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MinedTransaction):
            return {
                'date': obj.date.strftime('%d-%b-%Y %H:%M:%S'),
                'amount': obj.amount,
                'address': obj.address
            }
        return json.JSONEncoder.default(self, obj)


class RewardChecker:

    def __init__(self, listeners, address, check_interval_seconds):
        self.listeners = listeners
        self.address = address
        self.check_interval_seconds = check_interval_seconds
        # self.last_fetch = datetime.datetime.now()

        date_str = '20/02/2023'
        self.last_check = datetime.datetime.strptime(date_str, '%d/%m/%Y')

    def run(self):

        while True:
            time.sleep(self.check_interval_seconds)

            mined_transactions_after = self._checkForRewards(self.address, self.last_check)


            if len(mined_transactions_after) > 0:
                for mined_transaction_after in mined_transactions_after:
                    for listener in self.listeners:

                        mined_transaction = self._mapExplorerTransactionToMinedTransaction(mined_transaction_after)

                        listener.onReward(mined_transaction)

        pass

    def _checkForRewards(self, address, last_check):
        mined_transactions_after = explorer_reader.request_mined_transactions_after(address, last_check)

        total_mined_transactions_after = len(mined_transactions_after)
        logger.info(
            f"Checked for rewards after {last_check}. Found: {total_mined_transactions_after}")
        self.last_check = datetime.datetime.now()
        return mined_transactions_after

    def _mapExplorerTransactionToMinedTransaction(self, explorer_transaction):
        date = datetime.datetime.fromtimestamp(explorer_transaction['timestamp'])
        amount = abs(float(explorer_transaction['fees'])) / 100000000
        address = explorer_transaction["inputs"][0]["address"]

        return MinedTransaction(date, amount, address)

    def _