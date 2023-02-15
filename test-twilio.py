from twilio.rest import Client
from arguments import HydraChainArguments

hydrachain_arguments = HydraChainArguments()

client = Client(hydrachain_arguments.get_twilio_account_sid(), hydrachain_arguments.get_twilio_auth_token())

"""
1. Option to format the decimal places of the SMS.
"""

format_1 = "5.88 Hydra Mined."

message = client.messages.create(
  body="5.88123415 Hydra Mined",
  from_="+16233043804",
  to="+359896997166"
)

print(message.sid)