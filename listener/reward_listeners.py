import hashlib
import hmac
import json
import logging
import datetime
import requests
import twilio.rest
from viberbot import BotConfiguration, Api
from viberbot.api.messages import TextMessage

from explorer import reward_publisher

logger = logging.getLogger(__name__)


class TwilioSMSListener:

    def __init__(self, account_sid, auth_token, from_, to, transaction_date_format):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_ = from_
        self.to = to
        self.transaction_date_format = transaction_date_format
        self.twilioClient = twilio.rest.Client(self.account_sid, self.auth_token)

    def onReward(self, transaction):
        logger.info(f"SMS Event Listener notified about transaction {transaction}")

        datetime_formatted = transaction.date.strftime(self.transaction_date_format)
        body = f"Hydra Mined:\n{transaction.amount}\n{datetime_formatted} UTC\n{transaction.address}"

        self.send_sms(body)

    def send_sms(self, body):
        message = self.twilioClient.messages.create(
            body=body,
            from_=self.from_,
            to=self.to
        )
        logger.info(f"Sent SMS ({message.sid}) from {self.from_} to {self.to} with content {body}")

    def __str__(self):
        return f"name: {self.account_sid}, auth_token: {self.auth_token}, from_: {self.from_}, to: {self.to}"


class WebhookListener:

    def __init__(self, secret_key, url):
        self.secret_key = secret_key
        self.url = url

    def onReward(self, transaction):
        logger.info(f"Webhook Event Listener notified about transaction {transaction}")

        self.send_webhook(self.secret_key,
                          self.url,
                          json.dumps(transaction, cls=reward_publisher.MinedTransactionEncoder))

    def send_webhook(self, secret_key, url, body):
        timestamp = datetime.datetime.now().timestamp()

        hashable = body + str(timestamp)
        hashed = hmac.new(secret_key.encode(), hashable.encode(), hashlib.sha256).hexdigest()

        signature_header = f"{hashed},{timestamp}"
        headers = {'X-Webhook-Signature': signature_header}
        response = requests.post(url, data=body, headers=headers)
        logger.info(f"Sent Webhook to {url} with body {body} and signature {signature_header}")

    def __str__(self):
        return f"secret_key: {self.secret_key}, url: {self.url}"


class ViberBotListener:

    def __init__(self, bot_name, bot_avatar_url, bot_auth_token, receiving_user_id, transaction_date_format):
        self.bot_name = bot_name
        self.bot_avatar_url = bot_avatar_url
        self.bot_auth_token = bot_auth_token
        self.receiving_user_id = receiving_user_id
        self.transaction_date_format = transaction_date_format

        self.bot_configuration = BotConfiguration(
            name=self.bot_name,
            avatar=self.bot_avatar_url,
            auth_token=self.bot_auth_token,
        )
        self.viber_api  = Api(self.bot_configuration)

    def onReward(self, transaction):
        logger.info(f"Viber Bot Event Listener notified about transaction {transaction}")

        datetime_formatted = transaction.date.strftime(self.transaction_date_format)
        message = f"Hydra Mined:\n{transaction.amount}\n{datetime_formatted} UTC\n{transaction.address}"

        self.send_message(message)

    def send_message(self, message):
        self.viber_api.send_messages(self.receiving_user_id, [
            TextMessage(
                text=message
            )
        ])
        logger.info(f"Sent Viber Message to user {self.receiving_user_id} with content {message}")

    def __str__(self):
        return f"bot_name: {self.bot_name}, bot_avatar_url: {self.bot_avatar_url}, bot_auth_token: {self.bot_auth_token}, receiving_user_id: {self.receiving_user_id}"
