import hmac
import hashlib

import datetime as datetime
import json
import logging

import requests

logging.basicConfig(level='INFO')


def send_webhook(secret_key, url, body):
    timestamp = datetime.datetime.now().timestamp()

    hashable = body + str(timestamp)
    hashed = hmac.new(secret_key.encode(), hashable.encode(), hashlib.sha256).hexdigest()

    signature_header = "{},{}".format(hashed, timestamp)
    headers = {'X-Webhook-Signature': signature_header}
    response = requests.post(url, data=body, headers=headers)
    print(response)


def validate_webhook(secret_key, signature, body, tolerance_seconds):
    received_hash = get_signature_secret_key_body_hash(signature)

    if received_hash is None:
        logging.info('Hash is not present in the signature.')
        return False

    received_timestamp = get_signature_timestamp(signature)

    if received_timestamp is None:
        logging.info('Timestamp is not present in the signature.')
        return False

    hashable = body + str(received_timestamp)
    expected_hash = hmac.new(secret_key.encode(), hashable.encode(), hashlib.sha256).hexdigest()

    if received_hash != expected_hash:
        logging.info('Hash is not valid.')
        return False

    sent_datetime = datetime.datetime.fromtimestamp(float(received_timestamp))
    received_datetime = datetime.datetime.now()
    delta_datetime = received_datetime - sent_datetime

    if delta_datetime >= datetime.timedelta(seconds=tolerance_seconds):
        logging.info('Webhook is expired. Receiving difference %s is more than the given tolerance %s in seconds.',
                     delta_datetime.seconds, tolerance_seconds)
        return False

    return True


def get_signature_secret_key_body_hash(signature):
    items = signature.split(',')
    return items[0] if len(signature) != 0 else None


def get_signature_timestamp(signature):
    items = signature.split(',')
    return items[1] if 1 in range(len(items)) else None


secret = 'asd123'
tolerance_seconds = 60  # 300

# Send
url = 'https://webhook.site/7a1b0dad-b8ff-4da4-a642-806f2503adfa'
body = {'name': 'joro'}
# send_webhook(secret, url, json.dumps(body))

# Check
received_signature = '2d65924bf6fea448866cc3cf391788ce1e77fb4caa491a7721457e82cd368ee1,1676727682.667726'
received_body = '{"name": "joro"}'

validate_webhook(secret, received_signature, received_body, tolerance_seconds)
