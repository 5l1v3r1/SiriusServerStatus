# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from emoji import emojize

import logging

#Log in
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
#logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Edad' + emojize("yummy :cake:", use_aliases=True), 'Color favorito'], ['Número de hermanos', 'Algunas cosas...'], ['Completado']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):
    print('START')
    update.message.reply_text("Hola. Vamos a conversar, cuentame algo", reply_markup=markup)

    return CHOOSING


def regular_choice(bot, update, user_data):
    print('REGULAR')
    text = update.message.text
    user_data['choice'] = text
    update.message.reply_text('Tu {}? Si, me encantaría escuchar!'.format(text.lower()))

    return TYPING_REPLY


def custom_choice(bot, update):
    print('CUSTOM')
    update.message.reply_text('Bien, enviame la categoría primero, ' 
                                'por ejemplo, "Habilidad más impresionante"')

    return TYPING_CHOICE


def received_information(bot, update, user_data):
    print('RECEIVED')
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("Esto fue lo que dijiste: " 
                                "{}" 
                                "Puedes decirme más o cambiar tu opinión sobre algo.".format(facts_to_str(user_data)), reply_markup=markup)

    return CHOOSING


def done(bot, update, user_data):
    print('DONE')
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("Aprendí esto sobre ti: " 
                                "{}"
                                "Hasta la próxima.".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    logger.warning('La actualización "%s" provocó el error "%s"', update, error)


def main():
    with open('./token.txt') as file:
        token = file.read()

    updater = Updater(token)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],

        states = {
            CHOOSING: [RegexHandler('^(Edad|Color favorito|Numero de hermanos)$',
                                    regular_choice,
                                    pass_user_data=True),
                        RegexHandler('^Algunas cosas...$',
                                    custom_choice),
                    ],
            
            TYPING_CHOICE: [MessageHandler(Filters.text,
                                            regular_choice,
                                            pass_user_data=True)
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                            received_information,
                                            pass_user_data=True),
                        ],
        },

        fallbacks = [RegexHandler('^Completado$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()