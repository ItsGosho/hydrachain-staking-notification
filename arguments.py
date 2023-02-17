import argparse

LOG_LEVEL_DEFAULT = 'INFO'
TRANSACTION_CHECK_INTERVAL_DEFAULT = 60 * 60  # 1 Hour
SMS_TRANSACTION_DATE_FORMAT_DEFAULT = '%d-%b-%Y %H:%M:%S'

ADDRESS_NAME = 'address'
LOG_LEVEL_NAME = 'log-level'
TWILIO_ACCOUNT_SID_NAME = 'twilio-account-sid'
TWILIO_AUTH_TOKEN_NAME = 'twilio-auth-token'
TWILIO_FROM_NUMBER_NAME = 'twilio-from-number'
SMS_TO_NUMBER_NAME = 'sms-to-number'
TRANSACTIONS_CHECK_INTERVAL_NAME = 'transactions-check-interval'
SMS_TRANSACTION_DATE_FORMAT_NAME = 'sms-transaction-date-format'

LOG_LEVEL_ALLOWED = ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


class LogLevelAction(argparse.Action):
    def __call__(self, parser, namespace, log_level, option_string=None):
        if log_level not in LOG_LEVEL_ALLOWED:
            raise ValueError(
                'Log level {} is not supported. Supported ones: {}'.format(log_level, ', '.join(LOG_LEVEL_ALLOWED)))

        setattr(namespace, self.dest, log_level)


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
                            help='Level of logging. Default is {}'.format(LOG_LEVEL_DEFAULT),
                            default=LOG_LEVEL_DEFAULT,
                            action=LogLevelAction)

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
                            help="How often to check for transactions. Default is {} seconds".format(TRANSACTION_CHECK_INTERVAL_DEFAULT),
                            default=TRANSACTION_CHECK_INTERVAL_DEFAULT)

        parser.add_argument('--{}'.format(SMS_TRANSACTION_DATE_FORMAT_NAME),
                            dest=SMS_TRANSACTION_DATE_FORMAT_NAME,
                            type=str,
                            help="Datetime format for the transaction date sms. Refer to https://strftime.org/ for available formatting. Default is %%d-%%b-%%Y %%H:%%M:%%S",
                            default=SMS_TRANSACTION_DATE_FORMAT_DEFAULT)

        self.parser = parser
        self.arguments = self.parser.parse_args()

    def get_address(self):
        return self.get_argument(ADDRESS_NAME)

    def get_log_level(self):
        return self.get_argument(LOG_LEVEL_NAME)

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

    def get_argument(self, argument_name):
        return self.arguments.__getattribute__(argument_name)

    def get_arguments(self):
        return self.arguments
