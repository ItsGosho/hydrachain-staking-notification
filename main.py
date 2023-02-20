import logging
import multiprocessing
import time
import explorer_reader
import datetime
from twilio.rest import Client

from arguments import ArgumentParser, Argument

argument_parser = ArgumentParser()

# TODO: Which one of these two is better and what are their cons and pros
argument_parser.get_sms_enable()
argument_parser.get_argument(Argument.ADDRESS)

logging.basicConfig(level=argument_parser.get_log_level(), format=argument_parser.get_log_format())

logging.basicConfig(level=argument_parser.get_argument(Argument.LOG_LEVEL),
                    format=argument_parser.get_argument(Argument.LOG_FORMAT))

client = Client(argument_parser.get_twilio_account_sid(), argument_parser.get_twilio_auth_token())


def send_sms(amount, datetime, address):
    datetime_formatted = datetime.strftime(argument_parser.get_sms_transaction_date_format())
    messageBody = "Hydra Mined:\n{}\n{} UTC\n{}".format(amount, datetime_formatted, address)
    sentFrom = argument_parser.get_twilio_from_number()
    sentTo = argument_parser.get_sms_to_number()

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
        time.sleep(argument_parser.get_transactions_check_interval())
        mined_transactions_after = explorer_reader.request_mined_transactions_after(argument_parser.get_address(),
                                                                                    last_fetch)
        total_mined_transactions_after = len(mined_transactions_after)
        logging.info("Checked for mined transactions after %s. Found: %s", last_fetch,
                     total_mined_transactions_after)
        last_fetch = datetime.datetime.now()

        if total_mined_transactions_after > 0:
            for listener in listeners:
                listener(mined_transactions_after)


if __name__ == '__main__':
    logging.info("Hydrachain Staking Notification")
    logging.info("Started the application with log level %s", argument_parser.get_log_level())
    logging.info("Listening for transactions on address %s", argument_parser.get_address())
    logging.info("Transactions check interval is %s seconds", argument_parser.get_transactions_check_interval())

    # TODO: If SMS/Webhook is enable, log more configurations without secret ones.

    p1 = multiprocessing.Process(target=transaction_checker, args=(event_listener_test,))
    p1.start()
    p1.join()
