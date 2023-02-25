import logging

from argument.arguments import ArgumentParser, Argument
from explorer.reward_publisher import RewardChecker
from listener.reward_listeners import TwilioSMSListener, WebhookListener

VERSION = "2.0.0"

argument_parser = ArgumentParser(VERSION)

logging.basicConfig(level=argument_parser.get(Argument.LOG_LEVEL),
                    format=argument_parser.get(Argument.LOG_FORMAT))

logger = logging.getLogger(__name__)


def get_listeners(argument_values):
    listeners = []

    if argument_values[Argument.SMS_ENABLE.value] == 'yes':
        listeners.append(
            TwilioSMSListener(
                account_sid=argument_values[Argument.TWILIO_ACCOUNT_SID.value],
                auth_token=argument_values[Argument.TWILIO_AUTH_TOKEN.value],
                from_=argument_values[Argument.TWILIO_FROM_NUMBER.value],
                to=argument_values[Argument.SMS_TO_NUMBER.value],
                transaction_date_format=argument_values[Argument.SMS_TRANSACTION_DATE_FORMAT.value]
            ))

    if argument_values[Argument.WEBHOOK_ENABLE.value] == 'yes':
        listeners.append(
            WebhookListener(
                secret_key=argument_values[Argument.WEBHOOK_SECRET_KEY.value],
                url=argument_values[Argument.WEBHOOK_URL.value]
            ))

    return listeners

if __name__ == '__main__':
    logger.info(f"Hydrachain Staking Notification {VERSION}")
    logger.info(f"Started the application with log level {argument_parser.get(Argument.LOG_LEVEL)}")
    logger.info(f"Listening for transactions on address {argument_parser.get(Argument.ADDRESS)}")
    logger.info(f"Transactions check interval is {argument_parser.get(Argument.TRANSACTIONS_CHECK_INTERVAL)} seconds")
    logger.info(f"SMS enabled - {argument_parser.get(Argument.SMS_ENABLE)}")
    logger.info(f"Webhook enabled {argument_parser.get(Argument.WEBHOOK_ENABLE)}")

    listeners = get_listeners(argument_parser.get_all())

    reward_checker = RewardChecker(listeners,
                                   argument_parser.get(Argument.ADDRESS),
                                   argument_parser.get(Argument.TRANSACTIONS_CHECK_INTERVAL))

    reward_checker.start()

