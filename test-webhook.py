import hmac
import hashlib

import datetime as datetime
import json
import logging

import requests

logging.basicConfig(level='INFO')

def send_webhook(secret_key, url, body):
    secret_key_body_hash = hmac.new(secret_key.encode(), body.encode(), hashlib.sha256).hexdigest()
    timestamp = datetime.datetime.now().timestamp()

    signature = "{},{}".format(secret_key_body_hash, timestamp)
    headers = {'X-Webhook-Signature': signature}
    response = requests.post(url, data=body, headers=headers)
    print(response)

def validate_webhook(secret_key, signature, body, tolerance_seconds):

    received_secret_key_body_hash = get_signature_secret_key_body_hash(signature)

    if received_secret_key_body_hash is None:
        logging.info('Secret key body hash is not present in the signature.')
        return False

    expected_secret_key_body_hash = hmac.new(secret_key.encode(), body.encode(), hashlib.sha256).hexdigest()

    if received_secret_key_body_hash != expected_secret_key_body_hash:
        logging.info('Secret key body hash is not valid.')
        return False

    received_timestamp = get_signature_timestamp(signature)

    if received_timestamp is None:
        logging.info('Timestamp is not present in the signature.')
        return False

    sent_datetime = datetime.datetime.fromtimestamp(float(received_timestamp))
    received_datetime = datetime.datetime.now()
    delta_datetime = received_datetime - sent_datetime

    if delta_datetime >= datetime.timedelta(seconds = tolerance_seconds):
        logging.info('Webhook is expired. Receiving difference is more than the given tolerance %s in seconds.', tolerance_seconds)
        return False

    return True

def get_signature_secret_key_body_hash(signature):
    items = signature.split(',')
    return items[0] if len(signature) != 0 else None

def get_signature_timestamp(signature):
    items = signature.split(',')
    return items[1] if 1 in range(len(items)) else None

secret = 'asd123'
tolerance_seconds = 60#300

#Send
url = 'https://webhook.site/7a1b0dad-b8ff-4da4-a642-806f2503adfa'
body = {'name': 'joro'}
send_webhook(secret, url, json.dumps(body))

#Check
received_signature = '67fec9d6874aca42385bb853da81eb0cef75475356e007e1df510580493c3435,1676725231.286176'
received_body = '{"name": "joro"}'

validate_webhook(secret, received_signature, received_body, tolerance_seconds)
