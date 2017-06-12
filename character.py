
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Bot to create a character.
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Creates and stores a character based on the user
data supplied from chat using a ConversationHandler.
Send /start to initiate the setup.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Brawn', 'Agility'],
                  ['Intellect', 'Cunning'],
                  ['Willpower', 'Presence'],
                  ['Health', 'Name'],
                  ['Done']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
      #Ignore the command stored to show what was set.
      if key != "character":
        facts.append('%s - %s' % (key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):
    update.message.reply_text(
        "Hello there! It's time to create your character! Tell me a little about yourself with the choices below.",
        reply_markup=markup)

    return CHOOSING


def regular_choice(bot, update, user_data):
    text = update.message.text
    user_data['character'] = text
    update.message.reply_text('Your %s? Well, hurry and tell me.' % text.lower())

    return TYPING_REPLY

def received_information(bot, update, user_data):
    text = update.message.text
    category = user_data['character']
    user_data[category] = text
    #del user_data['character']

    update.message.reply_text("Alright cool, so here's what I got so far:"
                              "%s"
                              "You adjust your values if you'd like, or finish up here."
                              % facts_to_str(user_data),
                              reply_markup=markup)

    return CHOOSING


def done(bot, update, user_data):
    #if 'choice' in user_data:
     #   del user_data['choice']

    update.message.reply_text("Alright so here's what you're looking like so far:"
                              "%s"
                              "This is what we're going with!" % facts_to_str(user_data))
    #Since we store in user data, we can always come back and adjust values later.
    return ConversationHandler.END

def returnStoredCharacter(bot, update, user_data):
  bot.sendMessage(update.message.chat_id, facts_to_str(user_data))

def changeValues(bot, update, args, user_data):
  try:
    storedName = str(args[0])
    setValue = str(args[1])
    for key, value in user_data.items():
      #Ignore the command stored to show what was set.
      if key == storedName:
        user_data[key] = setValue
        bot.sendMessage(update.message.chat_id, "Successfully updated %s to %s" % (storedName, setValue))
        return
    bot.sendMessage(update.message.chat_id, "Sorry, %s doesn't exist for a character trait." % storedName)
  except (IndexError, ValueError):
    update.message.reply_text('Usage: /statSet <stat> <value>')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^(Brawn|Agility|Intellect|Cunning|Willpower|Presence|Health|Name)$',
                                    regular_choice,
                                    pass_user_data=True)
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice,
                                           pass_user_data=True),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )
    dp.add_handler(conv_handler)
    #Returns the character.
    dp.add_handler(CommandHandler("character", returnStoredCharacter, pass_user_data=True))
    dp.add_handler(CommandHandler("statset", changeValues,  pass_args=True, pass_user_data=True))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()