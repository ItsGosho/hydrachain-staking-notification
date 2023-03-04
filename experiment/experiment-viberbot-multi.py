from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from argument.arguments import ArgumentParser, Argument

hydrachain_arguments = ArgumentParser('1.0.0')
viber_bot_name = hydrachain_arguments.get(Argument.VIBER_BOT_NAME)
viber_bot_avatar = hydrachain_arguments.get(Argument.VIBER_BOT_AVATAR)
viber_bot_token = hydrachain_arguments.get(Argument.VIBER_BOT_TOKEN)
viber_user = hydrachain_arguments.get(Argument.VIBER_USER)

bot_configuration1 = BotConfiguration(
    name='Bot 1',
    avatar=viber_bot_avatar,
    auth_token=viber_bot_token,
)

bot_configuration2 = BotConfiguration(
    name='Bot 2',
    avatar='',
    auth_token=viber_bot_token,
)

viber1 = Api(bot_configuration1)
viber2 = Api(bot_configuration2)

viber1.send_messages(viber_user, [
    TextMessage(text="Bot 1")
])

viber2.send_messages(viber_user, [
    TextMessage(text="Bot 2")
])