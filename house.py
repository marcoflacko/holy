import bot
import db
import asyncio
import math
import holy
import time
import shop

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

def housecheck(user,text_arr,type):

		asset = db.post_sql(f"SELECT * FROM assets WHERE rowid = {text_arr[3]}")
		owneremoji = db.post_sql(f"SELECT emoj FROM users WHERE chat_id = {asset[0][0]}")[0][0]
		

		if asset[0][0] == user.id:
			visitor = "owner"
		else:
			visitor = "guest"

		if type == "text":
			if not asset[0][5]:
				dweller = "нихто;".split(";")
				dwelleremoji = "🙅‍♂️"
				timepassed = ""
			else:
				dweller = asset[0][5].split(";")
				dwelleremoji = db.post_sql(f"SELECT emoj FROM users WHERE chat_id = {dweller[2]}")[0][0]
				if int(dweller[2]) != int(asset[0][0]):
					timepassed = f"\n<i>осталось жить ( {holy.since(int(dweller[4]) - int(time.time()))} )</i>"
				else:
					timepassed = ""

			owner = asset[0][4].split(";")

			text = f'{shop.i[asset[0][1]]["emoji"]} {asset[0][1]}  <code>({text_arr[3]})</code> | {owneremoji} <b>{owner[0]}</b>\n'
			text += f'┄┄┄┄┄┄┄┄┄┄┄\n'
			text += f'🚪 <i>Живёт:</i> {dwelleremoji} <b>{dweller[0]}</b> {timepassed}\n'
			text += f'💜 <i>Состояние:</i> <b>{asset[0][2]} %</b>\n'
			text += f'🛋️ <i>Аренда (час):</i> <b>{asset[0][3]}</b> 💕\n'
			return text
		
		elif type == "keyboard":

			back = text_arr[4]
			if not asset[0][5]:
				dweller = "нихто;🙅‍♂️".split(";")
				if visitor == "guest":
					btn = InlineKeyboardButton(f"🏡 заселиться", callback_data=f"assets {user.id} housedwell {text_arr[3]} {back}")
				elif visitor == "owner":
					btn = InlineKeyboardButton(f"🏡 заселиться", callback_data=f"assets {user.id} housedwellowner {text_arr[3]} {back}")
				timepassed = ""
			else:
				dweller = asset[0][5].split(";")
				timepassed = f"<i>( {holy.since(int(time.time()) - int(dweller[3]))} )</i>"
				if visitor == "owner":
					if int(dweller[2]) != int(asset[0][0]):
						btn = InlineKeyboardButton(f"❌ выселить {dweller[0]}", callback_data=f"assets {user.id} houseundwell {text_arr[3]} {back} fuckyou")
					else:
						btn = InlineKeyboardButton(f"🏡 сдать в аренду", callback_data=f"assets {user.id} houseundwellowner {text_arr[3]} {back}")
				else:
					btn = InlineKeyboardButton(f"❌ выселиться", callback_data=f"assets {user.id} houseundwell {text_arr[3]} {back}")

			if visitor == "owner" and asset[0][2] == 0:
				btn = InlineKeyboardButton(f"🏚 починить дом 💕500", callback_data=f"assets {user.id} repair {text_arr[3]} {back}")
			inline = InlineKeyboardMarkup()
			btn2 = InlineKeyboardButton(f"🙅‍♂️ назад", callback_data=f"assets {user.id} {back}")
			inline.add(btn).add(btn2)	
			return inline

def houseundwell(text_arr,type):
	if type == "guest":

		asset = db.post_sql(f"SELECT * FROM assets WHERE rowid = {text_arr[3]}")
		user = asset[0][5].split(";")[2]
		price = int(asset[0][2]) / 3600
		holics = int(asset[0][5].split(";")[5])
		timepassed = int(time.time()) - int(asset[0][5].split(";")[3])
		holicstoowner = int(timepassed * price)
		holicsback = int(holics - holicstoowner)

		db.post_sql(f"UPDATE assets SET dwellerinfo = '' WHERE rowid = {text_arr[3]}")
		db.post_sql(f"UPDATE users SET home = 0 WHERE chat_id = {user}")
		db.post_sql(f"UPDATE users SET holics = holics + {holicsback} WHERE chat_id = {user}")
		db.post_sql(f"UPDATE users SET holics = holics + {holicstoowner} WHERE chat_id = {asset[0][0]}")

	if type == "owner":

		asset = db.post_sql(f"SELECT * FROM assets WHERE rowid = {text_arr[3]}")
		user = asset[0][5].split(";")[2]
		db.post_sql(f"UPDATE assets SET dwellerinfo = '' WHERE rowid = {text_arr[3]}")
		db.post_sql(f"UPDATE users SET home = 0 WHERE chat_id = {user}")

def housedwell(text_arr):
	asset = db.post_sql(f"SELECT * FROM assets WHERE rowid = {text_arr[3]}")
	price = int(asset[0][3]) / 3600
	back = text_arr[4]

	# user = db.post_sql(f"SELECT * FROM users WHERE chat_id = {callback_query.from_user.id}")
	# db.post_sql(f"UPDATE assets SET dwellerinfo = '{callback_query.from_user.username};{user[0][3]};{callback_query.from_user.id};{int(time.time())}' WHERE rowid = {text_arr[2]}")
	# db.post_sql(f"UPDATE users SET home = {text_arr[2]} WHERE chat_id = {callback_query.from_user.id}")
	# await callback_query.message.edit_text(housecheck(callback_query.from_user,text_arr,'text'), reply_markup=housecheck(callback_query.from_user,text_arr,'keyboard'))

	inline = InlineKeyboardMarkup()
	btn1 = InlineKeyboardButton(f"1 час", callback_data=f"assets {text_arr[1]} housedwellfinal {text_arr[3]} {text_arr[4]} {int(time.time()) + 3620} {int(3600*price)}")
	btn2 = InlineKeyboardButton(f"2 часа", callback_data=f"assets {text_arr[1]} housedwellfinal {text_arr[3]} {text_arr[4]} {int(time.time()) + 7220} {int(7200*price)}")
	btn3 = InlineKeyboardButton(f"4 часа", callback_data=f"assets {text_arr[1]} housedwellfinal {text_arr[3]} {text_arr[4]} {int(time.time()) + 14420} {int(14400*price)}")
	btn4 = InlineKeyboardButton(f"8 часов", callback_data=f"assets {text_arr[1]} housedwellfinal {text_arr[3]} {text_arr[4]} {int(time.time()) + 28820} {int(28800*price)}")
	btn5 = InlineKeyboardButton(f"12 часов", callback_data=f"assets {text_arr[1]} housedwellfinal {text_arr[3]} {text_arr[4]} {int(time.time()) + 43220} {int(43200*price)}")
	btn6 = InlineKeyboardButton(f"16 часов", callback_data=f"assets {text_arr[1]} housedwellfinal {text_arr[3]} {text_arr[4]} {int(time.time()) + 57620} {int(57600*price)}")
	btn7 = InlineKeyboardButton(f"1 день", callback_data=f"assets {text_arr[1]} housedwellfinal {text_arr[3]} {text_arr[4]} {int(time.time()) + 86420} {int(86400*price)}")
	btn8 = InlineKeyboardButton(f"2 дня", callback_data=f"assets {text_arr[1]} housedwellfinal {text_arr[3]} {text_arr[4]} {int(time.time()) + 172820} {int(172800*price)}")
	btn9 = InlineKeyboardButton(f"3 дня", callback_data=f"assets {text_arr[1]} housedwellfinal {text_arr[3]} {text_arr[4]} {int(time.time()) + 259220} {int(259200*price)}")
	btn10 = InlineKeyboardButton(f"🙅‍♂️ назад", callback_data=f"assets {text_arr[1]} check {text_arr[3]} {text_arr[4]}")
	inline.add(btn1, btn2, btn3).add(btn4, btn5, btn6).add(btn7,btn8,btn9).add(btn10)
	return inline


def housedwellfinal(text_arr,callback_query,type):
	if type == "guest":
		user = db.post_sql(f"SELECT * FROM users WHERE chat_id = {callback_query.from_user.id}")
		db.post_sql(f"UPDATE assets SET dwellerinfo = '{callback_query.from_user.username};{user[0][3]};{callback_query.from_user.id};{int(time.time())};{text_arr[5]};{text_arr[6]}' WHERE rowid = {text_arr[3]}")
		db.post_sql(f"UPDATE users SET home = {text_arr[3]} WHERE chat_id = {callback_query.from_user.id}")
		db.post_sql(f"UPDATE users SET holics = holics - {text_arr[6]} WHERE chat_id = {callback_query.from_user.id}")

	if type == "owner":
		asset = db.post_sql(f"SELECT * FROM assets WHERE rowid = {text_arr[3]}")
		price = int(asset[0][3]) / 3600
		user = db.post_sql(f"SELECT * FROM users WHERE chat_id = {callback_query.from_user.id}")
		db.post_sql(f"UPDATE assets SET dwellerinfo = '{callback_query.from_user.username};{user[0][3]};{callback_query.from_user.id};{int(time.time())}' WHERE rowid = {text_arr[3]}")
		db.post_sql(f"UPDATE users SET home = {text_arr[3]} WHERE chat_id = {callback_query.from_user.id}")