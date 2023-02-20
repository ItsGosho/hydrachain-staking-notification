import logging
import multiprocessing
import time
import explorer_reader
import datetime
from twilio.rest import Client

from arguments import ArgumentParser, Argument

VERSION = "1.0.0"

argument_parser = ArgumentParser(VERSION)

logging.basicConfig(level=argument_parser.get(Argument.LOG_LEVEL),
                    format=argument_parser.get(Argument.LOG_FORMAT))

client = Client(argument_parser.get(Argument.TWILIO_ACCOUNT_SID),
                argument_parser.get(Argument.TWILIO_AUTH_TOKEN))

def send_sms(amount, datetime, address):
    datetime_formatted = datetime.strftime(argument_parser.get(Argument.SMS_TRANSACTION_DATE_FORMAT))
    messageBody = f"Hydra Mined:\n{amount}\n{datetime_formatted} UTC\n{address}"
    sentFrom = argument_parser.get(Argument.TWILIO_FROM_NUMBER)
    sentTo = argument_parser.get(Argument.SMS_TO_NUMBER)

    message = client.messages.create(
        body=messageBody,
        from_=sentFrom,
        to=sentTo
    )
    logging.info(f"Sent SMS ({message.sid}) from {sentFrom} to {sentTo} with content {messageBody}")


def event_listener_test(transactions):
    logging.info(f"Event listener received transactions {transactions}")

    for transaction in transactions:
        date = datetime.datetime.fromtimestamp(transaction['timestamp'])
        amount = abs(float(transaction['fees'])) / 100000000
        address = transaction["inputs"][0]["address"]
        send_sms(amount, date, address)


def transaction_checker(*listeners):
    # Test:
    #date_str = '10/02/2023'
    #last_fetch = datetime.datetime.strptime(date_str, '%d/%m/%Y')

    last_fetch = datetime.datetime.now()

    while True:
        time.sleep(argument_parser.get(Argument.TRANSACTIONS_CHECK_INTERVAL))
        mined_transactions_after = explorer_reader.request_mined_transactions_after(argument_parser.get(Argument.ADDRESS),
                                                                                    last_fetch)
        total_mined_transactions_after = len(mined_transactions_after)
        logging.info(f"Checked for mined transactions after {last_fetch}. Found: {total_mined_transactions_after}")
        last_fetch = datetime.datetime.now()

        if total_mined_transactions_after > 0:
            for listener in listeners:
                listener(mined_transactions_after)


if __name__ == '__main__':
    logging.info(f"Hydrachain Staking Notification {VERSION}")
    logging.info(f"Started the application with log level {argument_parser.get(Argument.LOG_LEVEL)}")
    logging.info(f"Listening for transactions on address {argument_parser.get(Argument.ADDRESS)}")
    logging.info(f"Transactions check interval is {argument_parser.get(Argument.TRANSACTIONS_CHECK_INTERVAL)} seconds")

    # TODO: If SMS/Webhook is enable, log more configurations without secret ones.

    p1 = multiprocessing.Process(target=transaction_checker, args=(event_listener_test,))
    p1.start()
    p1.join()
