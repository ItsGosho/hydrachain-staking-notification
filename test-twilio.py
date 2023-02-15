from twilio.rest import Client
from arguments import HydraChainArguments

hydrachain_arguments = HydraChainArguments()

client = Client(hydrachain_arguments.get_twilio_account_sid(), hydrachain_arguments.get_twilio_auth_token())

"""
1. Option to format the decimal places of the SMS.
"""

format_1 = "Hydra Mined:\n5.88123415.\n10-February-2023 21:22\nH8Rw6bdg8zYgQ8YYm5K7zkK6EytetYsAuY"

def sendMessage():
  message = client.messages.create(
    body=format_1,
    from_=hydrachain_arguments.get_twilio_from_number(),
    to=hydrachain_arguments.get_sms_to_number()
  )
  print(message.sid)

#sendMessage()