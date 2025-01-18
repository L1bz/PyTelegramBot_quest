import telebot
import sqlite3
from telebot import types
from config import BOT_TOKEN
from connectDB import DB



bot=telebot.TeleBot(BOT_TOKEN)


class meth():
	def __init__(self):

		self.counter = 0
		self.maxcounter = 0
		self.status = False
		self.quest = 1
		self.categ = ["Скорость ответов", "Качество", "Обращение с клиентом", "Впечатление от общения","Итог"]

	
	def start(self, message):

		DB.startDB(message)

		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("🖊 Написать отзыв")
		item2 = types.KeyboardButton("💬 Посмотреть отзывы")
		markup.add(item1, item2,)

		bot.send_message(message.chat.id, "Привет {0.first_name} Я бот TestBot, могу помоч когда напишешь! \033[1mЖирный текст\033".format(message.from_user),reply_markup=markup)

	
	def feedback(self, message):

		user_i=message.chat.id

		if message.text == '🖊 Написать отзыв' or message.text == '🖊 Изменить отзыв':
			self.status = True
			markup = types.InlineKeyboardMarkup()
			btm1 = types.InlineKeyboardButton("⭐", callback_data='⭐')
			btm2 = types.InlineKeyboardButton("⭐⭐", callback_data='⭐⭐')
			btm3 = types.InlineKeyboardButton("⭐⭐⭐", callback_data='⭐⭐⭐')
			btm4 = types.InlineKeyboardButton("⭐⭐⭐⭐", callback_data='⭐⭐⭐⭐')
			btm5 = types.InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data='⭐⭐⭐⭐⭐')
			markup.add(btm1, btm2, btm3,btm4,btm5)

			bot.send_message(message.chat.id, self.categ[self.quest-1], reply_markup=markup)

		if message.text == '💬 Посмотреть отзывы':

			self.status = False

			a = DB.GetLenFeedbackDB()
			b = DB.GetFeedbackDB()

			self.maxcounter = len(a)

			markup = types.InlineKeyboardMarkup()
			button1 = types.InlineKeyboardButton("Следуший отзыв =>", callback_data='12')
			markup.add(button1) 

			bot.send_message(message.chat.id, DB.GetStarFeedbackDB(self.counter, self.maxcounter, a), parse_mode = "markdown", reply_markup=markup)  

		if self.status==True and message.text != '💬 Посмотреть отзывы' and message.text !='🖊 Написать отзыв' and message.text != '🖊 Изменить отзыв':
			
			DB.SetFeedbackDB(message)

			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			item1 = types.KeyboardButton("🖊 Изменить отзыв")
			item2 = types.KeyboardButton("💬 Посмотреть отзывы")
			markup.add(item1, item2,)

			bot.send_message(message.chat.id, "Ваш отзыв вдохновляет нас продолжать совершенствоваться!".format(message.from_user),reply_markup=markup)
	
	
	def anws(self, call):

		markup = types.InlineKeyboardMarkup()
		btm1 = types.InlineKeyboardButton("⭐", callback_data='⭐')
		btm2 = types.InlineKeyboardButton("⭐⭐", callback_data='⭐⭐')
		btm3 = types.InlineKeyboardButton("⭐⭐⭐", callback_data='⭐⭐⭐')
		btm4 = types.InlineKeyboardButton("⭐⭐⭐⭐", callback_data='⭐⭐⭐⭐')
		btm5 = types.InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data='⭐⭐⭐⭐⭐')
		markup.add(btm1, btm2, btm3,btm4,btm5)

		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=self.categ[self.quest-1], reply_markup=markup)
	
	
	def callback_anws(self, call):

		a = DB.GetLenFeedbackDB()

		self.maxcounter = len(a)

		if call.message:
			if call.data == '12':
				self.counter+=1

				if self.counter == self.maxcounter-1:
					markup = types.InlineKeyboardMarkup()
					button2 = types.InlineKeyboardButton("<= Предыдущий отзыв", callback_data='13')
					markup.add(button2)

					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=DB.GetStarFeedbackDB(self.counter, self.maxcounter, a), parse_mode = "markdown", reply_markup=markup) 

				else:
					markup = types.InlineKeyboardMarkup()
					button1 = types.InlineKeyboardButton("Следуший отзыв =>", callback_data='12')
					button2 = types.InlineKeyboardButton("<= Предыдущий отзыв", callback_data='13')
					markup.add(button2, button1) 

					
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=DB.GetStarFeedbackDB(self.counter, self.maxcounter, a), parse_mode = "markdown", reply_markup=markup) 

			elif call.data == '13':
				self.counter-=1

				if self.counter == 0:
					markup = types.InlineKeyboardMarkup()
					button1 = types.InlineKeyboardButton("Следуший отзыв =>", callback_data='12')
					markup.add(button1) 

					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=DB.GetStarFeedbackDB(self.counter, self.maxcounter, a), parse_mode = "markdown", reply_markup=markup) 

				else:
					markup = types.InlineKeyboardMarkup()
					button1 = types.InlineKeyboardButton("Следуший отзыв =>", callback_data='12')
					button2 = types.InlineKeyboardButton("<= Предыдущий отзыв", callback_data='13')
					markup.add(button2, button1) 

					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=DB.GetStarFeedbackDB(self.counter, self.maxcounter, a), parse_mode = "markdown", reply_markup=markup) 

			elif "⭐" in call.data:
				DB.quest(call.data, self.quest,call.message.chat.id)
				if self.quest < 5:
					self.quest+=1
					meth.anws(self, call)
				else:
					self.quest = 1
					self.status = True
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="asdf")