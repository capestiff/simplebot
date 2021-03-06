#!/usr/local/bin/python
# coding: utf-8

import logging, re, ephem, parser, settings, csv
from city_list import city_list
from datetime import date, datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from w2n_ru import word_to_num, russian_number_system

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO,
                    handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')]
                    )
upd = Updater(settings.TELEGRAM_API_KEY)
pieces_list = []
custom_keyboard = [[KeyboardButton('7'), KeyboardButton('8'), KeyboardButton('9'), KeyboardButton('+')],
                   [KeyboardButton('4'), KeyboardButton('5'), KeyboardButton('6'), KeyboardButton('-')],
                   [KeyboardButton('1'), KeyboardButton('2'), KeyboardButton('3'), KeyboardButton('*')],
                   [KeyboardButton('.'), KeyboardButton('0'), KeyboardButton('/'), KeyboardButton('=')]]

def goroda_bot(bot, update, args):
    city_name = ' '.join(args)
    if args == []:
        update.message.reply_text('Введите /goroda название города')
    elif city_name in city_list:
        for city in city_list:
            if city_name[-1].lower() == city[0].lower():
                bot_city = city_list.pop(city_list.index(city))
                update.message.reply_text('{}, ваш ход.'.format(bot_city))
                city_list.remove(city)
            elif city_name[-2].lower() == city[0].lower():
                bot_city = city_list.pop(city_list.index(city))
                update.message.reply_text('{}, ваш ход.'.format(bot_city))
                city_list.remove(city)
    else:
        update.message.reply_text('Ошибка! Введите название города, который еще не называли и который существует.')

def start_bot(bot, update):
    welcome = '''Hi, {}! I understand the commands: {}, {}, {}. Also I can work like a calculator ({}) with integers 
and float numbers (enter for example 3.0+3=). Если введешь запрос в формате: сколько будет три целых пять десятых плюс 
сто миллиардов триста семьдесят миллионов восемьсот семьдесят три целых шестьсот 
восемьдесят три тысячных'''.format(update.message.chat.first_name, 
        '/start','/wordcount', '/planet', '/showcalc')
    logging.info('User {} selected /start'.format(update.message.chat.username))
    update.message.reply_text(welcome)

def wordcount_bot(bot, update, args):
    # regex pattern
    p = re.compile(r'\W+')
    args_quantity = len(p.split(str(args)))
    if not args or not(args[0].startswith('\"') and args[-1].endswith('\"')):
        update.message.reply_text('Enter a phrase in double quotes and I\'ll write how much words it has.')
    elif args_quantity - 2 != 1:
        word_form = 'words'
    else:
        word_form = 'word'
    # words counting by regex pattern separator minus 2 'cause of quotes
    word_quantity = len(p.split(str(args))) - 2
    update.message.reply_text('{} {}'.format(word_quantity, word_form))

def planet_bot(bot, update, args):
    if args == []:
        update.message.reply_text('Enter the name of any planet in the English language, and I\'ll tell you which constellation it is today.')
    else:
        planet_name = ''.join(args)
        today = str(date.today())
        try:
            planet = getattr(ephem, planet_name)()
            planet.compute(today)
            planet_constellation = ''.join(ephem.constellation(planet)[1])
            update.message.reply_text('Today {} is in {}.'.format(planet_name, planet_constellation))
        except (AttributeError, NameError):
            update.message.reply_text('Please, enter the correct name of the planet. Ex.: Moon, Jupiter, Mars etc.')

def fullmoon_bot(bot, update):
    user_expression = update.message.text
    date_str = user_expression.split()[4].strip('?')
    date_fullmoon = str(ephem.next_full_moon(date_str))
    update.message.reply_text(date_fullmoon)

def calc(bot, update):
    user_expression = update.message.text
    calc_reply(bot, update, user_expression)

def button_calc(bot, update):
    if update.message.text == '=':
        pieces_list.append(update.message.text)
        user_expression = ''.join(pieces_list)
        update.message.reply_text(user_expression)
        calc_reply(bot, update, user_expression)
        pieces_list.clear()
    else:
        pieces_list.append(update.message.text)

def text_calc(bot, update):
    user_expression = update.message.text
    pattern = re.compile(r'^сколько будет (?P<num_sentence>.+)')
    match = pattern.match(user_expression)
    num_sentence = match.group('num_sentence')
    for num in num_sentence.split():
        if num not in russian_number_system:
            update.message.reply_text('Ошибка! Введите правильно запрос (например: сколько будет ноль целых пять десятых плюс семь целых сто пятьдесят тысячных)')
            break
    else:
        sum_sentence = num_sentence.strip().split('плюс')
        diff_sentence = num_sentence.strip().split('минус')
        product_sentence = num_sentence.strip().split('умножить на')
        quotient_sentence = num_sentence.strip().split('разделить на')
        if 'плюс' in num_sentence:
            update.message.reply_text(word_to_num(sum_sentence[0]) + word_to_num(sum_sentence[1]))
        elif 'минус' in num_sentence:
            update.message.reply_text(word_to_num(diff_sentence[0]) - word_to_num(diff_sentence[1]))
        elif 'умножить на' in num_sentence:
            update.message.reply_text(word_to_num(product_sentence[0]) * word_to_num(product_sentence[1]))
        elif 'разделить на' in num_sentence:
            update.message.reply_text(word_to_num(quotient_sentence[0]) / word_to_num(quotient_sentence[1]))

def calc_reply(bot, update, user_expression):
    pattern = re.compile(r'(?P<first_num>\d+\.?\d*?)(?P<operator_sign>\D)(?P<second_num>\d+\.?\d*?)=')
    match = pattern.match(user_expression)
    if match:
        first_number = float(match.group('first_num'))
        second_number = float(match.group('second_num'))
        operator = str(match.group('operator_sign'))
        if operator == '+':
            update.message.reply_text(first_number + second_number)
        elif operator == '-':
            update.message.reply_text(first_number - second_number)
        elif operator == '*':
            update.message.reply_text(first_number * second_number)
        elif operator == '/':
            if second_number == 0:
                update.message.reply_text('I cannot divide by zero. Try another number.')
            else:
                update.message.reply_text(first_number / second_number)

def keyboard(bot, update):

    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    calc_bot_welcome = 'Calculator. Press the buttons one by one and you will get a result. To hide the keyboard enter /hidecalc'
    bot.send_message(update.message.chat_id, calc_bot_welcome, reply_markup = reply_markup)

def kb_hide(bot, update):

    reply_markup = ReplyKeyboardRemove(custom_keyboard)
    bot.sendMessage(update.message.chat_id, 'To open the keyboard again enter /showcalc',reply_markup = reply_markup)

def main():
    upd.dispatcher.add_handler(CommandHandler('start', start_bot))
    upd.dispatcher.add_handler(CommandHandler('wordcount', wordcount_bot, pass_args=True))
    upd.dispatcher.add_handler(CommandHandler('planet', planet_bot, pass_args=True))
    upd.dispatcher.add_handler(CommandHandler('showcalc', keyboard))
    upd.dispatcher.add_handler(CommandHandler('hidecalc', kb_hide))
    upd.dispatcher.add_handler(CommandHandler('goroda', goroda_bot, pass_args=True))
    upd.dispatcher.add_handler(RegexHandler(r'\d+\.?\d*\D\d+\.?\d*=', calc))
    upd.dispatcher.add_handler(RegexHandler(r'/|\d|\+|\*|-|=|\.', button_calc))
    upd.dispatcher.add_handler(RegexHandler(r'^сколько будет .+', text_calc))
    upd.dispatcher.add_handler(RegexHandler(r'^когда ближайшее полнолуние после.+\?', fullmoon_bot))

    upd.start_polling()
    upd.idle()

if __name__ == "__main__":
    logging.info('Bot started.')
    main()
