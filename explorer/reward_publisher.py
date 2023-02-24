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
        self.last_fetch = datetime.datetime.strptime(date_str, '%d/%m/%Y')

    def run(self):

        while True:
            test = __name__
            logger.info(test)

            time.sleep(self.check_interval_seconds)

            mined_transactions_after = explorer_reader.request_mined_transactions_after(self.address, self.last_fetch)

            total_mined_transactions_after = len(mined_transactions_after)
            logger.info(
                f"Checked for mined transactions after {self.last_fetch}. Found: {total_mined_transactions_after}")
            self.last_fetch = datetime.datetime.now()

            if total_mined_transactions_after > 0:
                for mined_transaction_after in mined_transactions_after:
                    for listener in self.listeners:
                        date = datetime.datetime.fromtimestamp(mined_transaction_after['timestamp'])
                        amount = abs(float(mined_transaction_after['fees'])) / 100000000
                        address = mined_transaction_after["inputs"][0]["address"]

                        mined_transaction = MinedTransaction(date, amount, address)

                        listener.onReward(mined_transaction)

        pass
