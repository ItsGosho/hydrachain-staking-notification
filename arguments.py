import argparse

LOG_LEVEL_CHOICES = ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
SMS_ENABLE_CHOICES = ['yes', 'no']
WEBHOOK_ENABLE_CHOICES = ['yes', 'no']

LOG_LEVEL_DEFAULT = 'INFO'
LOG_FORMAT_DEFAULT = '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'
TRANSACTION_CHECK_INTERVAL_DEFAULT = 60 * 60  # 1 Hour
SMS_TRANSACTION_DATE_FORMAT_DEFAULT = '%d-%b-%Y %H:%M:%S'

SMS_ENABLE_DEFAULT = 'no'
WEBHOOK_ENABLE_DEFAULT = 'no'
WEBHOOK_URL_DEFAULT = 'http://localhost:5555'

# General

ADDRESS_NAME = 'address'
TRANSACTIONS_CHECK_INTERVAL_NAME = 'transactions-check-interval'
LOG_LEVEL_NAME = 'log-level'
LOG_FORMAT_NAME = 'log-format'

SMS_ENABLE_NAME = 'sms-enable'
WEBHOOK_ENABLE_NAME = 'webhook-enable'

# Sms

TWILIO_ACCOUNT_SID_NAME = 'twilio-account-sid'
TWILIO_AUTH_TOKEN_NAME = 'twilio-auth-token'
TWILIO_FROM_NUMBER_NAME = 'twilio-from-number'
SMS_TO_NUMBER_NAME = 'sms-to-number'
SMS_TRANSACTION_DATE_FORMAT_NAME = 'sms-transaction-date-format'

# Webhook

WEBHOOK_URL_NAME = 'webhook-url'
WEBHOOK_SECRET_KEY_NAME = 'webhook-secret-key'


class HydraChainArguments:

    def __init__(self):
        self.initiailize()

    def initiailize(self):
        parser = argparse.ArgumentParser(description='Hydrachain Staking Notification')

        parser.add_argument('--{}'.format(ADDRESS_NAME),
                            dest=ADDRESS_NAME,
                            type=str,
                            help='Hydra address',
                            required=True)

        parser.add_argument('--{}'.format(LOG_LEVEL_NAME),
                            dest=LOG_LEVEL_NAME,
                            type=str,
                            help='Level of logging. Default: {}'.format(LOG_LEVEL_DEFAULT),
                            choices=LOG_LEVEL_CHOICES,
                            default=LOG_LEVEL_DEFAULT)

        parser.add_argument('--{}'.format(TWILIO_ACCOUNT_SID_NAME),
                            dest=TWILIO_ACCOUNT_SID_NAME,
                            type=str,
                            help="Twilio account SID.")

        parser.add_argument('--{}'.format(TWILIO_AUTH_TOKEN_NAME),
                            dest=TWILIO_AUTH_TOKEN_NAME,
                            type=str,
                            help="Twilio auth token.")

        parser.add_argument('--{}'.format(TWILIO_FROM_NUMBER_NAME),
                            dest=TWILIO_FROM_NUMBER_NAME,
                            type=str,
                            help="Twilio sms sending phone number.")

        parser.add_argument('--{}'.format(SMS_TO_NUMBER_NAME),
                            dest=SMS_TO_NUMBER_NAME,
                            type=str,
                            help="Number to receive sms notifications.")

        parser.add_argument('--{}'.format(TRANSACTIONS_CHECK_INTERVAL_NAME),
                            dest=TRANSACTIONS_CHECK_INTERVAL_NAME,
                            type=int,
                            help="How often to check for transactions. Default: {} seconds".format(
                                TRANSACTION_CHECK_INTERVAL_DEFAULT),
                            default=TRANSACTION_CHECK_INTERVAL_DEFAULT)

        parser.add_argument('--{}'.format(SMS_TRANSACTION_DATE_FORMAT_NAME),
                            dest=SMS_TRANSACTION_DATE_FORMAT_NAME,
                            type=str,
                            help="Datetime format for the transaction date sms. Refer to https://strftime.org/ for available formatting. Default: {}".format(
                                SMS_TRANSACTION_DATE_FORMAT_DEFAULT.replace('%', '%%')),
                            default=SMS_TRANSACTION_DATE_FORMAT_DEFAULT)

        parser.add_argument('--{}'.format(LOG_FORMAT_NAME),
                            dest=LOG_FORMAT_NAME,
                            type=str,
                            help="Format of the logs. Refer to https://docs.python.org/3/library/logging.html#logrecord-attributes for available formatting. Default: {}".format(
                                LOG_FORMAT_DEFAULT.replace('%', '%%')),
                            default=LOG_FORMAT_DEFAULT)

        parser.add_argument('--{}'.format(SMS_ENABLE_NAME),
                            dest=SMS_ENABLE_NAME,
                            type=str,
                            help="To enable sms sending. Default: {}".format(SMS_ENABLE_DEFAULT),
                            choices=SMS_ENABLE_CHOICES,
                            default=SMS_ENABLE_DEFAULT)

        parser.add_argument('--{}'.format(WEBHOOK_ENABLE_NAME),
                            dest=WEBHOOK_ENABLE_NAME,
                            type=str,
                            help="To enable webhook sending. Default: {}".format(WEBHOOK_ENABLE_DEFAULT),
                            choices=WEBHOOK_ENABLE_CHOICES,
                            default=WEBHOOK_ENABLE_DEFAULT)

        parser.add_argument('--{}'.format(WEBHOOK_URL_NAME),
                            dest=WEBHOOK_URL_NAME,
                            type=str,
                            help="URL for sending the webhook. Default: {}".format(WEBHOOK_URL_DEFAULT),
                            default=WEBHOOK_URL_DEFAULT)

        parser.add_argument('--{}'.format(WEBHOOK_SECRET_KEY_NAME),
                            dest=WEBHOOK_SECRET_KEY_NAME,
                            type=str,
                            help="Secret key, generated by you. Used to hash the content and make secure way to check the validity of the webhook at the receiver side.")

        self.parser = parser
        self.arguments = self.parser.parse_args()
        self._validate_sms_arguments_are_provided()
        self._validate_webhook_arguments_are_provided()

    def get_address(self):
        return self.get_argument(ADDRESS_NAME)

    def get_log_level(self):
        return self.get_argument(LOG_LEVEL_NAME)

    def get_log_format(self):
        return self.get_argument(LOG_FORMAT_NAME)

    def get_twilio_account_sid(self):
        return self.get_argument(TWILIO_ACCOUNT_SID_NAME)

    def get_twilio_auth_token(self):
        return self.get_argument(TWILIO_AUTH_TOKEN_NAME)

    def get_twilio_from_number(self):
        return self.get_argument(TWILIO_FROM_NUMBER_NAME)

    def get_sms_to_number(self):
        return self.get_argument(SMS_TO_NUMBER_NAME)

    def get_transactions_check_interval(self):
        return self.get_argument(TRANSACTIONS_CHECK_INTERVAL_NAME)

    def get_sms_transaction_date_format(self):
        return self.get_argument(SMS_TRANSACTION_DATE_FORMAT_NAME)

    def get_sms_enable(self):
        smsEnableArgumentValue = self.get_argument(SMS_ENABLE_NAME)

        return True if smsEnableArgumentValue == 'yes' else False

    def get_webhook_enable(self):
        webhookEnableArgument = self.get_argument(WEBHOOK_ENABLE_NAME)

        return True if webhookEnableArgument == 'yes' else False

    def get_webhook_url(self):
        return self.get_argument(WEBHOOK_URL_NAME)

    def get_webhook_secret(self):
        return self.get_argument(WEBHOOK_SECRET_KEY_NAME)

    def get_argument(self, argument_name):
        return self.arguments.__getattribute__(argument_name)

    def _validate_webhook_arguments_are_provided(self):

        if not self.get_webhook_enable():
            return

        required_argument_names = [WEBHOOK_SECRET_KEY_NAME]

        self._validate_arguments_present(WEBHOOK_ENABLE_NAME, required_argument_names)
    def _validate_sms_arguments_are_provided(self):

        if not self.get_sms_enable():
            return

        required_argument_names = [TWILIO_ACCOUNT_SID_NAME, TWILIO_AUTH_TOKEN_NAME, TWILIO_FROM_NUMBER_NAME,
                                   SMS_TO_NUMBER_NAME]
        self._validate_arguments_present(SMS_ENABLE_NAME, required_argument_names)

    def _validate_arguments_present(self, argument_name, required_argument_names):
        missing_required_argument_names = self.get_argument_names_with_none_value(required_argument_names)
        missing_required_arguments = self.prefix_strings('--', missing_required_argument_names)

        if len(missing_required_arguments) > 0:
            error_message = 'Argument --{} requires additional arguments: {}'.format(
                argument_name, ', '.join(missing_required_arguments))
            self.parser.error(error_message)

    def get_arguments(self):
        return self.arguments

    def check_not_none_values(*values):
        return all(value is not None for value in values)

    def get_argument_names_with_none_value(self, argument_names):
        argument_names_with_none_value = []

        for argument_name in argument_names:
            argument_value = self.get_argument(argument_name)
            argument_names_with_none_value.append(argument_name) if argument_value == None else None

        return argument_names_with_none_value

    def prefix_strings(self, prefix, strings):
        return [prefix + s for s in strings]
