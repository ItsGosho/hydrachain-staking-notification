import json
import logging
import datetime
import hmac
import hashlib

import requests
from twilio.rest import Client

from arguments import ArgumentParser, Argument
from reward_checker import RewardChecker, MinedTransactionEncoder

VERSION = "1.0.0"

argument_parser = ArgumentParser(VERSION)

logging.basicConfig(level=argument_parser.get(Argument.LOG_LEVEL),
                    format=argument_parser.get(Argument.LOG_FORMAT))

client = Client(argument_parser.get(Argument.TWILIO_ACCOUNT_SID),
                argument_parser.get(Argument.TWILIO_AUTH_TOKEN))


def send_sms(body, from_, to):

    message = client.messages.create(
        body=body,
        from_=from_,
        to=to
    )
    logging.info(f"Sent SMS ({message.sid}) from {from_} to {to} with content {body}")

def send_webhook(secret_key, url, body):
    timestamp = datetime.datetime.now().timestamp()

    hashable = body + str(timestamp)
    hashed = hmac.new(secret_key.encode(), hashable.encode(), hashlib.sha256).hexdigest()

    signature_header = f"{hashed},{timestamp}"
    headers = {'X-Webhook-Signature': signature_header}
    response = requests.post(url, data=body, headers=headers)
    logging.info(f"Sent Webhook to {url} with body {body} and signature {signature_header}")


def transaction_listener_sms(transaction):
    logging.info(f"SMS Event Listener notified about transaction {transaction}")

    datetime_formatted = transaction['date'].strftime(argument_parser.get(Argument.SMS_TRANSACTION_DATE_FORMAT))
    body = f"Hydra Mined:\n{transaction['amount']}\n{datetime_formatted} UTC\n{transaction['address']}"
    from_ = argument_parser.get(Argument.TWILIO_FROM_NUMBER)
    to = argument_parser.get(Argument.SMS_TO_NUMBER)

    send_sms(body, from_, to)


def transaction_listener_webhook(transaction):
    logging.info(f"Webhook Event Listener notified about transaction {transaction}")

    send_webhook(argument_parser.get(Argument.WEBHOOK_SECRET_KEY),
                 argument_parser.get(Argument.WEBHOOK_URL),
                 json.dumps(transaction, cls=MinedTransactionEncoder))

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

    reward_checker = RewardChecker(listeners,
                                   argument_parser.get(Argument.ADDRESS),
                                   argument_parser.get(Argument.TRANSACTIONS_CHECK_INTERVAL))

    reward_checker.run()
