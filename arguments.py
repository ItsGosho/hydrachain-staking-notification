import argparse

LOG_LEVEL_DEFAULT = 'INFO'
TRANSACTION_CHECK_INTERVAL_DEFAULT = 60 * 60  # 1 Hour

ADDRESS_NAME = 'address'
LOG_LEVEL_NAME = 'log-level'
TWILIO_ACCOUNT_SID_NAME = 'twilio-account-sid'
TWILIO_AUTH_TOKEN_NAME = 'twilio-auth-token'
TWILIO_FROM_NUMBER_NAME = 'twilio-from-number'
SMS_TO_NUMBER_NAME = 'sms-to-number'
TRANSACTIONS_CHECK_INTERVAL_NAME = 'transactions-check-interval'

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
                            help="How often to check for transactions.",
                            default=TRANSACTION_CHECK_INTERVAL_DEFAULT)

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

    def get_argument(self, argument_name):
        return self.arguments.__getattribute__(argument_name)

    def get_arguments(self):
        return self.arguments
