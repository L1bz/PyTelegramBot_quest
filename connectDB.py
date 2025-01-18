import sqlite3
from telebot import types


class DB():
	def startDB(message):

		connect=sqlite3.connect('user.db')
		cursor = connect.cursor()

		cursor.execute("""CREATE TABLE IF NOT EXISTS user(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_id INTEGER,
			q1 VARCHAR(15),
			q2 VARCHAR(15),
			q3 VARCHAR(15),
			q4 VARCHAR(15),
			q5 VARCHAR(15),
			status BOOL,
			feedback VARCHAR(120)
		)""");

		connect.commit()

		user_i=message.chat.id
		cursor.execute("""SELECT user_id FROM user WHERE user_id = ?""", [user_i])

		if cursor.fetchone()is None:
			cursor.execute("""INSERT INTO user(user_id, status) VALUES(?, ?);""", (user_i, False))

		connect.commit()

	def quest(anws, quest, user_i):
		connect=sqlite3.connect('user.db')
		cursor = connect.cursor()
		for i in range(1,6):
			if i == quest:
				quest = "q" + str(i)
				break
		cursor.execute(f"UPDATE user SET {quest} = '{anws}' WHERE user_id={user_i}")
		connect.commit()

	def GetFeedbackDB():
		connect=sqlite3.connect('user.db')
		cursor = connect.cursor()
		cursor.execute("""SELECT feedback FROM user""")
		feedback = cursor.fetchall()
		
		return feedback

	def SetFeedbackDB(message):
		connect=sqlite3.connect('user.db')
		cursor = connect.cursor()
		user_i=message.chat.id
		text=[str(message.text)]
		cursor.execute(f"UPDATE user SET feedback = '{text[0]}' WHERE user_id={user_i}")
		cursor.execute(f"UPDATE user SET status = false WHERE user_id={user_i}")
		connect.commit()

	def GetLenFeedbackDB():
		a = [] 
		b = DB.GetFeedbackDB()
		for i in b:
			a.append(i)
		return a
	def GetStarFeedbackDB(count, maxcount, a):
		connect=sqlite3.connect('user.db')
		cursor = connect.cursor()
		cursor.execute("""SELECT q1 FROM user""")
		q1 = cursor.fetchall()
		cursor.execute("""SELECT q2 FROM user""")
		q2 = cursor.fetchall()
		cursor.execute("""SELECT q3 FROM user""")
		q3 = cursor.fetchall()
		cursor.execute("""SELECT q4 FROM user""")
		q4 = cursor.fetchall()
		cursor.execute("""SELECT q5 FROM user""")
		q5 = cursor.fetchall()
		text = f'**Jnpsd - ** **{count+1}/{maxcount}** \n\n%s'%f'**Впечатление от общения** : **{q1[count]}**\n**Скорость ответов** : **{q2[count]}**\n**Качество** : **{q3[count]}**\n**Обращение с клиентом** : **{q4[count]}**\n**Итог** : **{q5[count]}**\n\n**Rjvtynfhbq** : \n%s'%a[count]
		return text

