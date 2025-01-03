import telebot
import sqlite3
import BotFun
from telebot import types
from config import BOT_TOKEN


bot=telebot.TeleBot(BOT_TOKEN)

newbot = BotFun.meth()



@bot.message_handler(commands= ['start'])
def Bot_start(message):
	newbot.start(message)

@bot.message_handler(content_types='text')
def reply(message):
	newbot.feedback(message)
@bot.callback_query_handler(func=lambda call:True)
def callback(call):
	newbot.callback_anws(call)

bot.polling()