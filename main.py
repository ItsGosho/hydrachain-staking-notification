import logging
import multiprocessing
import time
import explorer_reader
import datetime
from twilio.rest import Client

from arguments import HydraChainArguments

hydrachain_arguments = HydraChainArguments()
logging.basicConfig(level=hydrachain_arguments.get_log_level(), format=hydrachain_arguments.get_log_format())
client = Client(hydrachain_arguments.get_twilio_account_sid(), hydrachain_arguments.get_twilio_auth_token())

def send_sms(amount, datetime, address):
    datetime_formatted = datetime.strftime(hydrachain_arguments.get_sms_transaction_date_format())
    messageBody = "Hydra Mined:\n{}\n{} UTC\n{}".format(amount, datetime_formatted, address)
    sentFrom = hydrachain_arguments.get_twilio_from_number()
    sentTo = hydrachain_arguments.get_sms_to_number()

    message = client.messages.create(
        body=messageBody,
        from_=sentFrom,
        to=sentTo
    )
    logging.info("Sent SMS (%s) from %s to %s with content %s", message.sid, sentFrom, sentTo, messageBody)


def event_listener_test(transactions):
    logging.info("Event listener received transactions %s", transactions)

    for transaction in transactions:
        date = datetime.datetime.fromtimestamp(transaction['timestamp'])
        amount = abs(float(transaction['fees'])) / 100000000
        address = transaction["inputs"][0]["address"]
        send_sms(amount, date, address)


def transaction_checker(*listeners):
    # Test:
    # date_str = '10/02/2023'
    # date = datetime.datetime.strptime(date_str, '%d/%m/%Y')

    last_fetch = datetime.datetime.now()

    while True:
        time.sleep(hydrachain_arguments.get_transactions_check_interval())
        mined_transactions_after = explorer_reader.request_mined_transactions_after(hydrachain_arguments.get_address(),
                                                                                    last_fetch)
        total_mined_transactions_after = len(mined_transactions_after)
        logging.info("Checked for mined transactions after %s. Found: %s", last_fetch,
                     total_mined_transactions_after)
        last_fetch = datetime.datetime.now()

        if total_mined_transactions_after > 0:
            for listener in listeners:
                listener(mined_transactions_after)


if __name__ == '__main__':
    logging.info("Hydrachain Staking Notification.")
    logging.info("Check Interval: %s seconds.", hydrachain_arguments.get_transactions_check_interval())

    p1 = multiprocessing.Process(target=transaction_checker, args=(event_listener_test,))
    p1.start()
    p1.join()
