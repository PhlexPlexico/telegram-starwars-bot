#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Dice Rolling Bot, commands are defined in the readme.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
#from emoji import emojize
#emojize(":cake:", use_aliases=True) 
import logging
import die
from random import (randrange, uniform)
from functools import wraps
from quotes import getQuote
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Kevin
LIST_OF_ADMINS = [50589297]

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        # extract user_id from arbitrary update
        try:
            user_id = update.message.from_user.id
        except (NameError, AttributeError):
            try:
                user_id = update.inline_query.from_user.id
            except (NameError, AttributeError):
                try:
                    user_id = update.chosen_inline_result.from_user.id
                except (NameError, AttributeError):
                    try:
                        user_id = update.callback_query.from_user.id
                    except (NameError, AttributeError):
                        print("No user_id available in update.")
                        return
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(update.message.from_user.id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    bot.send_message(update.message.chat_id, "/d(4,6,10,20) to roll a die of your choice. \n/quote for a random quote! \n/time <days> <user> to time a user. \n/removetime <user> to remove the timer. \n/rollall Rolls all star wars RPG die. \n/rollboost Rolls the boost die. \n/rollsetback Rolls the setback die. \n/rollability Rolls the ability die. \n/rolldifficulty Rolls the difficulty die. \n/rollforce Rolls the force die. \n/rollproficiency Rolls the proficiency die. \n/rollchallenge Rolls the challenge die.")

def dicehelp(bot,update):
    strDiceMsg = "Positive Symbols:\n💥: Means success of whether a skill check succeeds or fails. Success is undermined by failure. One success symbol (💥) is canceled by one failure (🔽). Based on core mechanic, if at least one success remains in the pool after all cancellations have been made, the skill check succeeds. In force and destiny, success symbols can also influence the magnitude of the outcome. For example, in combat, each net Success is added to the damage inflicted on the target.\n♉️: Is advantage. It indicates an opportunity for a positive consequence or side effect, regardless of the task's success or failure. Examples of these postitive side effects include slicing a computer in far less time than anticipated, finding unexpected cover during a firefight, or recovering from strain during a stressful situation.\nIt's possible to fail a task while generating a number of Advantage symbols, allowing something good to come out of the failure. Likewise, advantage can cur alongside success, allowing for siginificantly positive outcomes. It's important to remember that Advantage sumbols do not have a direct impact on success or failure; they only affect their magnitude or potential side effects. Advantage is canceled by threat (☸️).\n⚔️: Means Triumph, a powerful result indicating a siginificant boon or beneficial outcome. Each triumph provides two effects: First, each triumph symbol also counts as one success, which means it could be canceled by a failure symbol. Second, each triumph can be used to trigger incredibly potent effects. Two common uses are to trigger a Critical Injury upon a successful attack and to activate a weapon's special quality. These effects also require advantages to activate too.\n\nNegative Symbols:\n🔽 is the failure symbol, as previously mentioned cancel out any success or possible triumphs.\n☸️  is the threat symbol, which cancels out any advantage symbols."
    bot.sendMessage(update.message.chat_id, strDiceMsg)
def randWiki(bot, update):
    cid = update.message.chat_id
    bot.send_message(cid, text="[Wookiepedia](http://starwars.wikia.com/wiki/Special:Random)", parse_mode="MARKDOWN")

def echo(bot, update):
    update.message.reply_text(update.message.text)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def r4(bot, update):
    intrand = randrange(1,4)
    update.message.reply_text(intrand)

def r6(bot, update):
    intrand = randrange(1,6)
    update.message.reply_text(intrand)

def r10(bot, update):
    intrand = randrange(1,10)
    update.message.reply_text(intrand)

def r20(bot, update):
    intrand = randrange(1,20)
    update.message.reply_text(intrand)

def quote(bot, update):
    bot.sendMessage(update.message.chat_id, getQuote())

def rollall(bot, update):
    bot.sendMessage(update.message.chat_id, die.rollAll())

def rollboost(bot, update):
    bot.sendMessage(update.message.chat_id, die.rollBoost())

def rollsetback(bot, update):
    bot.sendMessage(update.message.chat_id, die.rollSetBack())

def rollability(bot, update):
    bot.sendMessage(update.message.chat_id, die.rollAbility())

def rolldifficulty(bot, update):
    bot.sendMessage(update.message.chat_id, die.rollDifficulty())

def rollforce(bot, update):
    bot.sendMessage(update.message.chat_id, die.rollForce())

def rollproficiency(bot, update):
    bot.sendMessage(update.message.chat_id, die.rollProficiency())

def rollchallenge(bot, update):
    bot.sendMessage(update.message.chat_id, die.rollChallenge())

@restricted
def check(bot, update):
    bot.sendMessage(update.message.chat_id, str(update.message.from_user.name) + " is the current DM.")

@restricted
def set(bot, update, args, job_queue, chat_data):
    try:
        """Adds a job to the queue"""
        chat_id = update.message.chat_id
        user_id = str(update.message.from_user.id) + str(args[1])
        username = str(args[1])
        # args[0] should contain the time for the timer in seconds
        duetf = int(args[0]) * 86400
        duett = int(args[0]) * 79200
        if duetf < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return
        if user_id+'tt' in chat_data:
            update.message.reply_text('Sorry! We can\'t add another 22 hour timer for ' + username)
        else:
            twentytwo = job_queue.run_once(warning, duett, context=chat_id, name=username)
            chat_data[user_id+'tt'] = twentytwo 
        if user_id+'tf' in chat_data:
            update.message.reply_text('Sorry! We can\'t add another 24 hour timer for ' + username)
        else:
            # Add job to queue
            twentyfour = job_queue.run_once(alarm, duetf, context=chat_id, name=username)
            chat_data[user_id+'tf'] = twentyfour
        update.message.reply_text('Timer successfully set for ' + username + '!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /time <days> <user>')

@restricted
def unset(bot, update, args, chat_data):
    try:

        """Removes the job if the user changed their mind"""
        usernamett = str(update.message.from_user.id) + str(args[0]) + 'tt'
        usernametf = str(update.message.from_user.id) + str(args[0]) + 'tf'

        if usernametf not in chat_data:
            update.message.reply_text('You have no active timer')
            return
        job = chat_data[usernametf]
        job.schedule_removal()
        del chat_data[usernametf]

        if usernamett not in chat_data:
            update.message.reply_text('You have no active timer')
            return

        #if args[0] = chat_data['job'].name:
        job = chat_data[usernamett]
        job.schedule_removal()
        del chat_data[usernamett]

        update.message.reply_text('Timer successfully unset!')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /removetime <user>')

def alarm(bot, job):
    """Function to send the alarm message"""
    strReturnText = job.name + "'s turn is now over!"
    bot.send_message(job.context, text=strReturnText)

def warning(bot, job):
    strReturnText = job.name + " ONLY HAS TWO HOURS LEFT!!"
    """Function to send the alarm message"""
    bot.send_message(job.context, text=strReturnText)

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("d4", r4))
    dp.add_handler(CommandHandler("d6", r6))
    dp.add_handler(CommandHandler("link", randWiki))
    dp.add_handler(CommandHandler("d10", r10))
    dp.add_handler(CommandHandler("d20", r20))
    dp.add_handler(CommandHandler("admin", check))
    dp.add_handler(CommandHandler("quote", quote))
    dp.add_handler(CommandHandler("rollall", rollall))
    dp.add_handler(CommandHandler("rollboost", rollboost))
    dp.add_handler(CommandHandler("rollability", rollability))
    dp.add_handler(CommandHandler("rolldifficulty", rolldifficulty))
    dp.add_handler(CommandHandler("rollproficiency", rollproficiency))
    dp.add_handler(CommandHandler("rollforce", rollforce))
    dp.add_handler(CommandHandler("dicehelp", dicehelp))
    dp.add_handler(CommandHandler("rollsetback", rollsetback))
    dp.add_handler(CommandHandler("rollchallenge", rollchallenge))
    dp.add_handler(CommandHandler("time", set,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("removetime", unset, pass_chat_data=True, pass_args=True))
    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

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

