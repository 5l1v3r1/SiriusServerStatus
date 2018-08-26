from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler
from emoji import emojize

import logging
import json
import requests
import time, threading

import os, json

with open('./config.json') as f:
    data = json.load(f)

config = data['config']

user = ''
last = ''

# Token
token = config['token']

sirius_bot_updater = Updater(token)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Status', ''], ['', ''], ['Completado']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


# Emojies
sun_glasses = emojize(":sunglasses:", use_aliases=True)
fire = emojize(":fire:", use_aliases=True)
good = emojize(":+1:", use_aliases=True)
skull = emojize(":skull:", use_aliases=True)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def check():
    source = config['server']

    try:
        r = requests.get(source, timeout=5)
    except Exception:
        return False

    res = r.json()
    print(res)
    global last
    last = time.ctime()
    return True


def cron_status(bot, job):
    print('AUXILIO', time.ctime())
    text = ''

    if check():
        text = 'Todo anda bien ' + good
    else:
        global last
        text = fire + ' Auxilio  ' + fire + '\n Parece que el servidor está muerto ' + skull + '\n Última conexión: ' + last

    bot.send_message(job.context, text=text)


def start(bot, update, job_queue, chat_data):
    chat_id = update.message.chat_id
    global user
    user = update.message.chat.first_name + " " + update.message.chat.last_name
    job = job_queue.run_repeating(cron_status, 900, context=chat_id)
    chat_data['job'] = job

    text = sun_glasses + ' Hola ' + user

    update.message.reply_text(text)
    # update.message.reply_text('Hi! Use /set <seconds> to set a timer')


# def alarm(bot, job):
#     """Send the alarm message."""
#     bot.send_message(job.context, text='Beep! ' + user)


# def set_timer(bot, update, args, job_queue, chat_data):
#     """Add a job to the queue."""
#     chat_id = update.message.chat_id
#     try:
#         # args[0] should contain the time for the timer in seconds
#         due = int(args[0])
#         if due < 0:
#             update.message.reply_text('Sorry we can not go back to future!')
#             return

#         # Add job to queue
#         job = job_queue.run_repeating(alarm, due, context=chat_id)
#         chat_data['job'] = job

#         update.message.reply_text('Timer successfully set!')

#     except (IndexError, ValueError):
#         update.message.reply_text('Usage: /set <seconds>')

#     job = job_queue.run_repeating(alarm, due, context=chat_id)


def status(bot, update):
    print('AUXILIO', time.ctime())
    chack = emojize(":check:", use_aliases=True)
    fire = emojize(":fire:", use_aliases=True)
    good = emojize(":+1:", use_aliases=True)
    skull = emojize(":skull:", use_aliases=True)
    text = ''

    if check():
        text = 'Todo anda bien ' + good
    else:
        text = fire + ' Auxilio ' + fire + '\n Parece que el servidor está muerto ' + skull

    bot.sendMessage(chat_id=update.message.chat_id, text=text)


def help(bot, update):
    print('HELP', time.ctime())
    arrow = emojize(":arrow_forward:", use_aliases=True)
    arrow_right = emojize(":arrow_right:", use_aliases=True)    

    text = " /start    " + arrow_right + " Inicia el bot \n/status    " + arrow_right + " Estado actual del servidor"

    bot.sendMessage(chat_id=update.message.chat_id, text=text)


def stop(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    if 'job' not in chat_data:
        update.message.reply_text('No existen tareas')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Revisión desactivada')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Run bot."""
    print('STARTING ... ', time.ctime())
    global last
    last = time.ctime()
    updater = sirius_bot_updater

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("help", help))
    # dp.add_handler(CommandHandler("set", set_timer,
    #                               pass_args=True,
    #                               pass_job_queue=True,
    #                               pass_chat_data=True))
    dp.add_handler(CommandHandler("stop", stop, pass_chat_data=True))
    dp.add_handler(CommandHandler("status", status))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()