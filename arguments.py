import argparse
from enum import Enum


class Argument(Enum):
    ADDRESS = 'address'
    LOG_LEVEL = 'log-level'
    TWILIO_ACCOUNT_SID = 'twilio-account-sid'
    TWILIO_AUTH_TOKEN = 'twilio-auth-token'
    TWILIO_FROM_NUMBER = 'twilio-from-number'
    SMS_TO_NUMBER = 'sms-to-number'
    TRANSACTIONS_CHECK_INTERVAL = 'transactions-check-interval'
    SMS_TRANSACTION_DATE_FORMAT = 'sms-transaction-date-format'
    LOG_FORMAT = 'log-format'
    SMS_ENABLE = 'sms-enable'
    WEBHOOK_ENABLE = 'webhook-enable'
    WEBHOOK_URL = 'webhook-url'
    WEBHOOK_SECRET_KEY = 'webhook-secret-key'


arguments = {
    Argument.ADDRESS.value: {
        'type': str,
        'help': 'Hydra address',
        'required': True
    },
    Argument.LOG_LEVEL.value: {
        'type': str,
        'help': 'Level of logging',
        'choices': ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        'default': 'INFO'
    },
    Argument.TWILIO_ACCOUNT_SID.value: {
        'type': str,
        'help': 'Twilio account SID'
    },
    Argument.TWILIO_AUTH_TOKEN.value: {
        'type': str,
        'help': 'Twilio auth token'
    },
    Argument.TWILIO_FROM_NUMBER.value: {
        'type': str,
        'help': 'Twilio sms sending phone number'
    },
    Argument.SMS_TO_NUMBER.value: {
        'type': str,
        'help': 'Number to receive sms notifications'
    },
    Argument.TRANSACTIONS_CHECK_INTERVAL.value: {
        'type': int,
        'help': 'How often to check for transactions in seconds',
        'default': 3600  # 1 Hour
    },
    Argument.SMS_TRANSACTION_DATE_FORMAT.value: {
        'type': str,
        'help': 'Datetime format for the transaction date sms. Refer to https://strftime.org/ for available formatting',
        'default': '%d-%b-%Y %H:%M:%S'
    },
    Argument.LOG_FORMAT.value: {
        'type': str,
        'help': 'Format of the logs. Refer to https://docs.python.org/3/library/logging.html#logrecord-attributes for available formatting',
        'default': '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'
    },
    Argument.SMS_ENABLE.value: {
        'type': str,
        'help': 'To enable sms sending',
        'choices': ['yes', 'no'],
        'default': 'no'
    },
    Argument.WEBHOOK_ENABLE.value: {
        'type': str,
        'help': 'To enable webhook sending',
        'choices': ['yes', 'no'],
        'default': 'no'
    },
    Argument.WEBHOOK_URL.value: {
        'type': str,
        'help': 'URL for sending the webhook',
        'default': 'http://localhost:5555'
    },
    Argument.WEBHOOK_SECRET_KEY.value: {
        'type': str,
        'help': 'Secret key, generated by you. Used to hash the content and make secure way to check the validity of the webhook at the receiver side.'
    }
}


class ArgumentParser:

    def __init__(self):
        parser = argparse.ArgumentParser(description='Hydrachain Staking Notification',
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        for arg_name, arg_attrs in arguments.items():
            parser.add_argument(f'--{arg_name}', dest=arg_name, **arg_attrs)

        self.parser = parser
        self.arguments = self.parser.parse_args()
        self._validate_sms_arguments_are_provided()
        self._validate_webhook_arguments_are_provided()

    def get_argument(self, argument):
        return self.arguments.__getattribute__(argument.value)

    def _validate_webhook_arguments_are_provided(self):

        if self.get_argument(Argument.WEBHOOK_ENABLE) == 'no':
            return

        required_arguments = [Argument.WEBHOOK_SECRET_KEY]

        self._validate_arguments_present(Argument.WEBHOOK_ENABLE, required_arguments)

    def _validate_sms_arguments_are_provided(self):

        if self.get_argument(Argument.SMS_ENABLE) == 'no':
            return

        required_arguments = [Argument.TWILIO_ACCOUNT_SID, Argument.TWILIO_AUTH_TOKEN, Argument.TWILIO_FROM_NUMBER,
                              Argument.SMS_TO_NUMBER]
        self._validate_arguments_present(Argument.SMS_ENABLE, required_arguments)

    def _validate_arguments_present(self, argument, required_arguments):
        missing_required_arguments = self.get_arguments_with_none_value(required_arguments)
        missing_required_arguments_with_prefix = self.prefix_arguments('--', missing_required_arguments)

        if len(missing_required_arguments_with_prefix) > 0:
            error_message = f"Argument --{argument.value} requires additional arguments: {', '.join(missing_required_arguments_with_prefix)}"
            self.parser.error(error_message)

    def get_arguments(self):
        return self.arguments

    def check_not_none_values(*values):
        return all(value is not None for value in values)

    def get_arguments_with_none_value(self, arguments):
        arguments_with_none_value = []

        for argument in arguments:
            argument_value = self.get_argument(argument)
            arguments_with_none_value.append(argument) if argument_value == None else None

        return arguments_with_none_value

    def prefix_arguments(self, prefix, arguments):
        return [prefix + a.value for a in arguments]
