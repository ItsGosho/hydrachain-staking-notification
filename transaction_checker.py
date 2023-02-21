import datetime
import time
import logging
import explorer_reader

class TransactionChecker:

    def __init__(self, listeners, address, check_interval_seconds):
        self.listeners = listeners
        self.address = address
        self.check_interval_seconds = check_interval_seconds
        self.last_fetch = datetime.datetime.now()

        #date_str = '10/02/2023'
        #self.last_fetch = datetime.datetime.strptime(date_str, '%d/%m/%Y')


    def run(self):

        while True:

            time.sleep(self.check_interval_seconds)

            mined_transactions_after = explorer_reader.request_mined_transactions_after(self.address, self.last_fetch)

            total_mined_transactions_after = len(mined_transactions_after)
            logging.info(f"Checked for mined transactions after {self.last_fetch}. Found: {total_mined_transactions_after}")
            self.last_fetch = datetime.datetime.now()

            if total_mined_transactions_after > 0:
                for mined_transaction in mined_transactions_after:
                    for listener in self.listeners:
                        listener(mined_transaction)


        pass