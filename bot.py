import telegram
import random
from telegram.ext import Updater, CommandHandler


with open('./token.txt') as file:
    token = file.read()

sirius_bot_updater = Updater(token)


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hola")


start_handler = CommandHandler('start', start)

dispatcher = sirius_bot_updater.dispatcher

dispatcher.add_handler(start_handler)

sirius_bot_updater.start_polling()


while True:
    pass