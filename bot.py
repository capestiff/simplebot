#!/usr/local/bin/python
# coding: utf-8

import logging, re, ephem
from datetime import date
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO,
                    handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')]
                    )

def start_bot(bot, update):
    welcome = "Hi, {}! I understand the commands: {}, {}, {}".format(update.message.chat.first_name,'/start','/wordcount', '/planet')
    logging.info('Пользователь {} нажал /start'.format(update.message.chat.username))
    update.message.reply_text(welcome)

def wordcount_bot(bot, update, args):
    # regex pattern
    p = re.compile(r'\W+')
    if args == [] or not(args[0].startswith('\"') and args[-1].endswith('\"')):
        update.message.reply_text('Enter a phrase in quotes and I write how much words it has.')
    elif not len(p.split(str(args))) - 2 == 1:
        # words counting by regex pattern separator minus 2 'cause of quotes
        update.message.reply_text('{} words'.format(len(p.split(str(args))) - 2))
    else:
        update.message.reply_text('1 word')

def planet_bot(bot, update, args):
    if args == []:
        update.message.reply_text('Enter the name of any planet in the English language, and I\'ll tell you which constellation it is today.')
    else:
        planet_name = ''.join(args)
        today = date.__str__(date.today())
        try:
            planet = getattr(ephem, planet_name)()
        except (AttributeError, NameError):
            update.message.reply_text('Please, enter the correct name of the planet. Ex.: Moon, Earth, Mars etc.')
        planet.compute(today)
        planet_constellation = ''.join(ephem.constellation(planet)[1])
        update.message.reply_text('Today {} is in {}.'.format(planet_name, planet_constellation))

def main():
    upd = Updater(settings.TELEGRAM_API_KEY)

    upd.dispatcher.add_handler(CommandHandler("start", start_bot))
    upd.dispatcher.add_handler(CommandHandler("wordcount", wordcount_bot, pass_args=True))
    upd.dispatcher.add_handler(CommandHandler("planet", planet_bot, pass_args=True))

    upd.start_polling()
    upd.idle()

if __name__ == "__main__":
    logging.info('Bot started.')
    main()

