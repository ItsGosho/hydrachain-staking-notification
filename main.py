import logging
import datetime
from twilio.rest import Client

from arguments import ArgumentParser, Argument
from transaction_checker import TransactionChecker

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


def transaction_listener_sms(transaction):
    logging.info(f"SMS Event Listener notified about transaction {transaction}")

    date = datetime.datetime.fromtimestamp(transaction['timestamp'])
    amount = abs(float(transaction['fees'])) / 100000000
    address = transaction["inputs"][0]["address"]
    send_sms(amount, date, address)


def transaction_listener_webhook(transaction):
    logging.info(f"Webhook Event Listener notified about transaction {transaction}")


"""
The idea of behind that way of specifying the listeners and not just if X argument value is Y then
pass the listeners for calling to the transaction checker is to provider easier and more flexible way of doing it.
That way without modifying the code and centralized more arguments listeners can be specified, which is way easier.
"""
transaction_listener_configurations = {
    Argument.SMS_ENABLE.value: {
        'expected_argument_values': ['yes'],
        'listeners': [transaction_listener_sms]
    },
    Argument.WEBHOOK_ENABLE.value: {
        'expected_argument_values': ['yes'],
        'listeners': [transaction_listener_webhook]
    }
}


def get_listeners(transaction_listener_configurations, argument_values):
    listeners = []

    for argument, configuration in transaction_listener_configurations.items():
        expected_argument_values = configuration['expected_argument_values']

        argument_provided_value = argument_values[argument]

        if argument_provided_value in expected_argument_values:
            listeners.extend(configuration['listeners'])

    return listeners


if __name__ == '__main__':
    logging.info(f"Hydrachain Staking Notification {VERSION}")
    logging.info(f"Started the application with log level {argument_parser.get(Argument.LOG_LEVEL)}")
    logging.info(f"Listening for transactions on address {argument_parser.get(Argument.ADDRESS)}")
    logging.info(f"Transactions check interval is {argument_parser.get(Argument.TRANSACTIONS_CHECK_INTERVAL)} seconds")
    logging.info(f"SMS enabled - {argument_parser.get(Argument.SMS_ENABLE)}")
    logging.info(f"Webhook enabled {argument_parser.get(Argument.WEBHOOK_ENABLE)}")

    listeners = get_listeners(transaction_listener_configurations, argument_parser.get_all())

    transaction_checker = TransactionChecker(listeners,
                                             argument_parser.get(Argument.ADDRESS),
                                             argument_parser.get(Argument.TRANSACTIONS_CHECK_INTERVAL))

    transaction_checker.run()
