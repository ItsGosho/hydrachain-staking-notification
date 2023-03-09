import datetime
import json
import time
import logging
from explorer import explorer_reader
from explorer.explorer_reader import ExplorerReader

logger = logging.getLogger(__name__)


class MinedTransaction:

    def __init__(self, date, amount, address):
        self.date = date
        self.amount = amount
        self.address = address

    def __str__(self):
        return f"date: {self.date}, amount: {self.amount}, address: {self.address}"


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

    def __init__(self, listeners, address, check_interval_seconds, explorer_reader: ExplorerReader = ExplorerReader()):
        self.listeners = listeners
        self.address = address
        self.check_interval_seconds = check_interval_seconds
        self.running = False
        self.last_check = datetime.datetime.now()

        #date_str = '01/03/2023'
        #self.last_check = datetime.datetime.strptime(date_str, '%d/%m/%Y')

        self.explorer_reader = explorer_reader

    def start(self):
        self.running = True

        while self.running:
            time.sleep(self.check_interval_seconds)

            mined_transactions_after = self._checkForRewards(self.address, self.last_check)

            if not len(mined_transactions_after) > 0:
                continue

            for mined_transaction_after in mined_transactions_after:
                mined_transaction = self._mapExplorerTransactionToMinedTransaction(mined_transaction_after)
                self._callListeners(self.listeners, mined_transaction)

    def stop(self):
        self.running = False

    def _callListeners(self, listeners, mined_transaction):
        for listener in listeners:
            listener.onReward(mined_transaction)

    def _checkForRewards(self, address, last_check):
        mined_transactions_after = self.explorer_reader.request_mined_transactions_created_after(address, last_check)

        logger.debug(
            f"Checked for reward transaction of address {address} after {last_check}. Found: {mined_transactions_after}")
        logger.info(
            f"Checked for reward transaction of address {address} after {last_check}. Total: {len(mined_transactions_after)}")

        self.last_check = datetime.datetime.now()
        return mined_transactions_after

    def _mapExplorerTransactionToMinedTransaction(self, explorer_transaction):
        date = datetime.datetime.fromtimestamp(explorer_transaction['timestamp'])
        amount = abs(float(explorer_transaction['fees'])) / 100000000
        address = explorer_transaction["inputs"][0]["address"]

        return MinedTransaction(date, amount, address)
