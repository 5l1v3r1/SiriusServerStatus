from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from emoji import emojize

import json
import requests
import time, threading


with open('./token.txt') as file:
    token = file.read()

sirius_bot_updater = Updater(token)


CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Status', ''], ['', ''], ['Completado']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def check():
    source = 'http://sirius.utp.edu.co/status/'
    
    try:
        r = requests.get(source, timeout=5)
    except Exception:
        return False

    res = r.json()
    print(res)
    return True


def start(bot, update):
    print('START', time.ctime())
    sun_glasses = emojize(":sunglasses:", use_aliases=True)
    text = sun_glasses + ' Hola ' + update.message.chat.first_name + " " + update.message.chat.last_name
    bot.sendMessage(chat_id=update.message.chat_id, text=text, reply_markup=markup)


def status(bot, update):
    print('AUXILIO', time.ctime())
    fire = emojize(":fire:", use_aliases=True)
    good = emojize(":+1:", use_aliases=True)
    skull = emojize(":skull:", use_aliases=True)
    text = ''

    if check():
        text = 'Todo anda bien ' + good
    else:
        text = fire + ' Auxilio ' + update.message.chat.first_name + " " + update.message.chat.last_name + ' ' + fire + '\n Parece que el servidor está muerto ' + skull

    bot.sendMessage(chat_id=update.message.chat_id, text=text)


def help(bot, update):
    print('HELP', time.ctime())
    arrow = emojize(":arrow_forward:", use_aliases=True)
    arrow_right = emojize(":arrow_right:", use_aliases=True)    

    text = " /start    " + arrow_right + " Inicia el bot \n/status    " + arrow_right + " Estado actual del servidor"

    bot.sendMessage(chat_id=update.message.chat_id, text=text)


def main():
    print('STARTING ... ')
    start_handler = CommandHandler('start', start)
    status_handler = CommandHandler('status', status)
    help_handler = CommandHandler('help', help)
    dispatcher = sirius_bot_updater.dispatcher
    # dispatcher.add_handler(MessageHandler(Filters.text , time, pass_job_queue=True))
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(status_handler)
    dispatcher.add_handler(help_handler)
    sirius_bot_updater.start_polling()
        

    #while True:    
    #    pass


if __name__ == '__main__':
    main()