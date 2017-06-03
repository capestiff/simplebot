#!/usr/local/bin/python
# coding: utf-8

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO,
                    handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')]
                    )

def start_bot(bot, update):
    welcome = "Привет, {}! Я непростой бот, но понимаю только команду {}".format(update.message.chat.first_name,'/start')
    logging.info('Пользователь {} нажал /start'.format(update.message.chat.username))
    update.message.reply_text(welcome)

def chat(bot, update):
    text = update.message.text
    logging.info(text)
    update.message.reply_text(text)

def main():
    upd = Updater(settings.TELEGRAM_API_KEY)

    upd.dispatcher.add_handler(CommandHandler("start", start_bot))
    upd.dispatcher.add_handler(MessageHandler(Filters.text, chat))

    upd.start_polling()
    upd.idle()

if __name__ == "__main__":
    logging.info('Bot started.')
    main()

