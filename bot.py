import logging
import asyncio
import sqlite3
from sqlite3 import Error
import holy
import db
import shop
import time
import random
import house
import re
import json
from random import randrange


from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, admin_id, main_chat, TIMERS, STUFF, TEXTS, timevert

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, loop=loop)




#funcs

async def send_to_admin(dp):
	await bot.send_message(chat_id=admin_id, text="💖 Холи запущен! 💖")

#funcs

#handlers

def rate():
	items = db.post_sql(f"SELECT * FROM users ORDER BY holics DESC LIMIT 10")
	rate = "✨ Список красавчиков ✨\n\n"
	num = 1
	for item in items:
		if num == 1:
			rate += f"{num}\t\t🌈 {str(item[3])}\t\t<code>{str(item[1])}</code>\t\t <b>{timevert(int(item[2]))}</b> 💕\n"
			rate += f"┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n"	
			num += 1
			continue
		
		rate += f"{num}\t\t{str(item[3])}\t\t<code>{str(item[1])}</code>\t\t <b>{timevert(int(item[2]))}</b> 💕\n"
		num += 1
	return rate	

@dp.callback_query_handler(text="rate")
async def answer(callback_query: types.CallbackQuery):
	btn = InlineKeyboardButton(f"💫 обновить", callback_data=f"rate")
	inline = InlineKeyboardMarkup().add(btn)
	await bot.answer_callback_query(callback_query.id)
	try:
		await callback_query.message.edit_text(rate(), reply_markup=inline)
	except:
		pass

@dp.message_handler(commands=['rate'])
async def com_help(message: types.Message):
	
	btn = InlineKeyboardButton(f"💫 обновить", callback_data=f"rate")
	inline = InlineKeyboardMarkup().add(btn)

	await message.reply(rate(), reply_markup=inline)

def strip_emoji(text):
    RE_EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    return RE_EMOJI.sub(r'emj', text)

@dp.message_handler(regexp='^buyemoji')
async def com_help(message: types.Message):
	text_arr = message.text.split(" ")
	
	allow = True if len(text_arr) == 2 else False

	if allow == False:
		await message.reply("🥺 Что-то не так написал\n пример: <code>buyemoji 💩</code>")
		return

	if db.dbget("holics",message.from_user.id) < 1000:
		await message.reply("🥺 Недостаточно холиков, нужно 1000 💕")
		return

	emoj = text_arr[1]
	check = strip_emoji(emoj)
	if check == "emj":
		await message.reply(f"Поставил {emoj}")
		db.post_sql(f"UPDATE users SET emoj = '{emoj}' WHERE chat_id = '{message.from_user.id}' ")
		db.post_sql(f"UPDATE users SET holics = holics - 1000 WHERE chat_id = '{message.from_user.id}' ")
	else:
		await message.reply("🥺 Что-то не так написал\n пример: <code>buyemoji 💩</code>")

@dp.message_handler(commands=['buyholics'])
async def com_help(message: types.Message):
	text = f"😍  Купить холики  😍\n\
⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n\
💕 <b>{15*STUFF['holicsprice']}</b>  =   🇺🇦 <b>15 грн</b>\n\
⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n\
карта приват:   <b>4149 4991 4246 0706</b>\n\n\
<code>При донате выше 30🇺🇦 игроку даётся 🧿 holy-щит \
который защищает от ограблений на 2 дня</code>\n\
<i>По всем вопросам начисления и платежей @taftsky</i>"
	await message.reply(text)

@dp.message_handler(commands=['donaterate'])
async def com_help(message: types.Message):
	items = db.post_sql(f"SELECT * FROM donaters ORDER BY money DESC")
	rate = "💫  <b>Список денежных</b>  💫\n✦ 💰 <b>красавулей!</b> 💰 ✦\n┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄"
	num = 1
	for item in items:
		rate += f"\n💟  {num}\t\t💘\t\t<code>{str(item[0])}</code>\t\t <b>{timevert(int(item[1]))} <i>грн</i>  💵</b>\n"
				
		num += 1
	rate += "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n<i>огромное спасибо всем котикам кто покупает холики,\
	все денюжки идут на улучшение качества казино и качество еды владика, \
	а то я уже заебался овсянку есть блять ♡</i>"
	await message.reply(rate)

@dp.message_handler(regexp="^houseprice")
async def set(message: types.Message):
	text_arr = message.text.split(" ")

	if len(text_arr) == 3:
		home = text_arr[1]
		price = text_arr[2]
		if not price.isnumeric():
			await message.reply(f"🥺 чё-то ты не то написал \n<code>houseprice (номер_дома) (цена)</code>\nпример:   <code>houseprice 5 200</code>")
			return
		check = db.post_sql(f"SELECT chat_id FROM assets WHERE rowid = {home} AND chat_id = '{message.from_user.id}'")
		if check:
			check = db.post_sql(f"SELECT dwellerinfo FROM assets WHERE rowid = {home} AND chat_id = '{message.from_user.id}'")
			if check[0][0] != "":
				await message.reply(f"🏠 В домике кто-то живёт. Цену можно изменить когда домик пустой")
				return

			await message.reply(f"🏠Да! Ты успешно изменил \nцену аренды на <b>{price}</b> 💕")
			db.post_sql(f"UPDATE assets SET value = {price} WHERE rowid = {home}")
		else:
			await message.reply("🥺 ты ввёл номер не своего дома")
	else:
		await message.reply("🥺 чё-то ты не то написал \n<code>houseprice (номер_дома) (цена)</code>\nпример:   <code>houseprice 5 200</code>")



def itemskeyboard(chat_id):
	items = db.post_sql(f"SELECT * FROM items WHERE chat_id = {chat_id} ORDER BY type")

	num = 1
	inline = InlineKeyboardMarkup()
	for item in items:
		if(item[3] == "food"):
			btn = InlineKeyboardButton(f"{shop.i[item[1]]['emoji']}\t\t({str(item[2])})", callback_data=f"use_{item[1]}_{chat_id}")
			inline.insert(btn)
		else:	
			continue

		num += 1	
	return inline

def assetskeyboard(chat_id, type):
	if type == "myassets":
		items = db.post_sql(f"SELECT rowid, * FROM assets WHERE chat_id = {chat_id} ORDER BY asset")
		num = 1
		inline = InlineKeyboardMarkup()
		btn2 = InlineKeyboardButton(f"🙅‍♂️ назад", callback_data=f"assets {chat_id} balance")
		for item in items:

			btn = InlineKeyboardButton(f"{shop.i[item[2]]['emoji']}\t\t{str(item[2])}", callback_data=f"assets {chat_id} check {item[0]} main")
			inline.add(btn)
			num += 1	
		inline.add(btn2)
	if type == "hometodwell":
		items = db.post_sql(f"SELECT rowid, * FROM assets WHERE asset = 'домик' AND dwellerinfo = '' ")
	
		num = 1
		inline = InlineKeyboardMarkup()
		for item in items:
			asset = item[2]
			owner = item[5].split(";")[0]
			price = item[4]
			btn = InlineKeyboardButton(f"{shop.i[item[2]]['emoji']}\t\t{asset}\t\t{owner}\t\t{price} 💕", callback_data=f"assets {chat_id} check {item[0]} hometodwell")
			inline.add(btn)
			num += 1			

	return inline


# -------------------------------------------------------------------#
# -------       A S S E T S    C A L L B A C K S            ---------#


@dp.callback_query_handler( regexp="(^assets)")
async def answer(callback_query: types.CallbackQuery):

	text_arr = callback_query.data.split(" ")


	if callback_query.from_user.id != int(text_arr[1]):
		await bot.answer_callback_query(callback_query.id, text="не трогай 😈")
		return;
	

	# -------------------------------------------------------------------#
	# --------------------------- H O U S E -----------------------------#


	if text_arr[2] == "check":
		await callback_query.message.edit_text(house.housecheck(callback_query.from_user,text_arr,'text'), reply_markup=house.housecheck(callback_query.from_user,text_arr,'keyboard'))

	if text_arr[2] == "housedwell":
		isempty = db.post_sql(f"SELECT dwellerinfo FROM assets WHERE rowid = '{text_arr[3]}' ")
		if isempty[0][0] != '':
			await bot.answer_callback_query(callback_query.id, text="домик уже занят 😈")
			return

		price = db.post_sql(f"SELECT value FROM assets WHERE rowid = '{text_arr[3]}' ")
		text = f"🏡 На сколько арендуем?\n<i> Владелец установил <b>{price[0][0]}</b> 💕 (за час)</i>"
		inline = house.housedwell(text_arr)
		await callback_query.message.edit_text(text, reply_markup=inline)

	if text_arr[2] == "housedwellfinal":
		isempty = db.post_sql(f"SELECT dwellerinfo FROM assets WHERE rowid = '{text_arr[3]}' ")
		if isempty[0][0] != '':
			await bot.answer_callback_query(callback_query.id, text="домик уже занят 😈")
			return
		if db.dbget("holics", callback_query.from_user.id) < int(text_arr[6]):
			await bot.answer_callback_query(callback_query.id, text="мало холиков 😈")
			return
		house.housedwellfinal(text_arr,callback_query,"guest")
		await callback_query.message.edit_text(house.housecheck(callback_query.from_user,text_arr,'text'), reply_markup=house.housecheck(callback_query.from_user,text_arr,'keyboard'))
		h = db.post_sql(f"SELECT * FROM assets WHERE rowid = '{text_arr[3]}'")
		owner = h[0][4].split(";")[0]

		await callback_query.message.answer(f"🏡 {callback_query.from_user.first_name} арендовал домик у @{owner}")

	if text_arr[2] == "houseundwell":
		isdweller = db.post_sql(f"SELECT dwellerinfo FROM assets WHERE rowid = '{text_arr[3]}' ")[0][0].split(";")[2]

		if int(isdweller) != int(callback_query.from_user.id):
			await bot.answer_callback_query(callback_query.id, text="что-то не так 😳")
			return
		if len(text_arr) == 6:
			f = True
		else:
			f = False
		asset = db.post_sql(f"SELECT * FROM assets WHERE rowid = {text_arr[3]}")
		asset = asset[0][5].split(";")
		if (time.time() - int(asset[3])) < 5 and f == False:
			await bot.answer_callback_query(callback_query.id, text="Покинуть квартиру можно минимум через 30 минут")
			return
		h = db.post_sql(f"SELECT * FROM assets WHERE rowid = '{text_arr[3]}'")
		if f == True:
			dweller = h[0][5].split(";")[0]
			await callback_query.message.answer(f"🏡 {callback_query.from_user.first_name} выселил @{dweller} со своего домика")
		else:
			owner = h[0][4].split(";")[0]
			await callback_query.message.answer(f"🏡 {callback_query.from_user.first_name} выселился c домика @{owner}")
		house.houseundwell(text_arr, "guest")
		await callback_query.message.edit_text(house.housecheck(callback_query.from_user,text_arr,'text'), reply_markup=house.housecheck(callback_query.from_user,text_arr,'keyboard'))

	if text_arr[2] == "housedwellowner":
		await bot.answer_callback_query(callback_query.id)
		house.housedwellfinal(text_arr,callback_query,"owner")
		await callback_query.message.edit_text(house.housecheck(callback_query.from_user,text_arr,'text'), reply_markup=house.housecheck(callback_query.from_user,text_arr,'keyboard'))	

	if text_arr[2] == "houseundwellowner":
		await bot.answer_callback_query(callback_query.id)
		house.houseundwell(text_arr, "owner")
		await callback_query.message.edit_text(house.housecheck(callback_query.from_user,text_arr,'text'), reply_markup=house.housecheck(callback_query.from_user,text_arr,'keyboard'))
	
	if text_arr[2] == "repair":
		if db.dbget("holics",callback_query.from_user.id) < 500:
			await bot.answer_callback_query(callback_query.id,text="Недостаточно холиков 😢")
			return
		await bot.answer_callback_query(callback_query.id,text="👍 Ты отремонтировал домик!")
		db.post_sql(f"UPDATE assets SET state = 100 WHERE rowid = {text_arr[3]}")
		asset = db.post_sql(f"SELECT * FROM assets WHERE rowid = {text_arr[3]}")
		dweller = asset[0][5].split(";")[2]
		db.post_sql(f"UPDATE users SET home = {text_arr[3]} WHERE chat_id = '{dweller}' ")

		await callback_query.message.edit_text(house.housecheck(callback_query.from_user,text_arr,'text'), reply_markup=house.housecheck(callback_query.from_user,text_arr,'keyboard'))

	# --------------------------- H O U S E -----------------------------#
	# -------------------------------------------------------------------#

	if text_arr[2] == "main":
		try:
			await callback_query.message.edit_text(assets(callback_query.from_user), reply_markup=assetskeyboard(callback_query.from_user.id, "myassets"))
		except:
			pass

	if text_arr[2] == "balance":
		await callback_query.message.edit_text(balance(callback_query.from_user,"text"),reply_markup=balance(callback_query.from_user,"keyboards"))

	if text_arr[2] == "hometodwell":
		m = "🏡 Снять квартиру\n<i>список доступных к аренде домов</i>"
		r = assetskeyboard(callback_query.from_user.id, "hometodwell")
		if not r['inline_keyboard']:
			m += f"\n┄┄┄┄┄┄┄┄┄┄┄\nК сожалению никто сейчас \nне сдаёт квартиру 🐶"
		await callback_query.message.edit_text(m,reply_markup=r)

	await bot.answer_callback_query(callback_query.id)

# -------       A S S E T S    C A L L B A C K S            ---------#
# -------------------------------------------------------------------#



def assets(user):
	items = db.post_sql(f"SELECT * FROM assets WHERE chat_id = {user.id} ORDER BY asset")	
	rate = f"🏩 <b>{user.first_name}</b>\n<i>твои активы</i>\n";
	return rate

@dp.message_handler(commands=['assets'])
async def com_help(message: types.Message):
	m = assets(message.from_user)
	r = assetskeyboard(message.from_user.id, "myassets")
	await message.reply(m,reply_markup=r)

@dp.message_handler(commands=['rent'])
async def com_help(message: types.Message):
	m = "🏡 Снять квартиру\n<i>список доступных к аренде домов</i>"
	r = assetskeyboard(message.from_user.id, "hometodwell")

	if not r['inline_keyboard']:
		m += f"\n┄┄┄┄┄┄┄┄┄┄┄\nК сожалению никто сейчас \nне сдаёт квартиру 🐶"
	await message.reply(m,reply_markup=r)

@dp.message_handler(commands=['items'])
async def com_help(message: types.Message):
	items = db.post_sql(f"SELECT * FROM items WHERE chat_id = {message.from_user.id} ORDER BY type")
	if items:
		rate = f"<b>{message.from_user.first_name}</b>\n<i>твои предметы</i> 🧤\n┄┄┄┄┄┄┄┄┄\n";
	else:
		rate = f"<b>{message.from_user.first_name}</b>\nу тебя ничего нету 🙉";
	num = 1
	# inline = InlineKeyboardMarkup()
	for item in items:
		if(item[3] == "food"):
			continue
		else:	
			rate += f" <code>({str(item[2])})</code>\t\t{shop.i[item[1]]['emoji']}\t\t{str(item[1])}\n"

		num += 1
	# btn_1 = InlineKeyboardButton("использовать 🧤", callback_data="shop_food")
	# inline = InlineKeyboardMarkup().add(btn_1)
	await message.reply(rate, reply_markup=itemskeyboard(message.from_user.id))

@dp.message_handler(commands=['help'])
async def com_help(message: types.Message):
	text = f"<b>{message.from_user.first_name}</b>, круто что ты решил разобраться! Сейчас я введу тебя в краткий курс дела ✨\n\n"
	text += TEXTS['help_message']
	btn1 = InlineKeyboardButton(f"🎲 кости", callback_data=f"1")
	btn2 = InlineKeyboardButton(f"🏀 мяч", callback_data=f"1")
	btn3 = InlineKeyboardButton(f"🎰 слот", callback_data=f"1")
	btn4 = InlineKeyboardButton(f"🧤 команды", callback_data=f"1")
	btn5 = InlineKeyboardButton(f"🧨 предметы", callback_data=f"1")
	inline = InlineKeyboardMarkup().add(btn1,btn2,btn3).add(btn4,btn5)
	await message.reply(text,reply_markup=inline)


# -------------------------------------------------------------------#
# --------------------------- D A I L Y -----------------------------#

@dp.message_handler(commands=['daily'])
async def com_help(message: types.Message):
	
	d_timer = db.post_sql(f"SELECT time FROM timers WHERE chat_id = {message.from_user.id} AND timer = 'daily' ")
	if time.time() > d_timer[0][0]:

		amount = randrange(95, 200)

		await message.reply(f"💫┄┄┄┄┄┄┄💫\n💕 +  {amount}  холиков\n    за дэйли-бонус 🎁\n💫┄┄┄┄┄┄┄💫")
		await message.answer_animation("CgACAgEAAxkBAAIukWAjj4UmQmqgOWi2MQyVgy6fEEtpAAJHAAPyqYhGP9kT-1kcAUoeBA")
		db.post_sql(f"UPDATE timers SET time = {time.time()+TIMERS['daily']} WHERE chat_id = {message.from_user.id} AND timer = 'daily' ")	
		db.post_sql(f"UPDATE users SET holics = holics + {amount} WHERE chat_id = {message.from_user.id}")

	else:
		t = holy.since(d_timer[0][0] - time.time())
		await message.reply(f"До дэйли-бонуса\nосталось: <b>{t}</b>\nЖди 🦖")	

# --------------------------- D A I L Y -----------------------------#
# -------------------------------------------------------------------#

@dp.message_handler(commands=['start'])
async def com_help(message: types.Message):
	# if message.from_user.id
	check = db.post_sql(f"SELECT * FROM users WHERE chat_id = {message.from_user.id}")
	if check:
		await message.reply("Йоу! У тебя уже есть аккаунт чувак 😛")
		return

	db.user_reg(message.from_user.id,message.from_user.username)
	await message.reply(f"🐸💖 {message.from_user.first_name},\n\
добро пожаловать в Holygame!\n\
┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n\
<b>+ 200</b> 💕холиков тебе для старта\n\
И будь добр, чекни это /help")

@dp.message_handler(commands=['remove'])
async def com_help(message: types.Message):
	db.post_sql(f"UPDATE users SET holics = holics - 5 WHERE chat_id = {message.chat.id}")
	await message.reply("минусанул")

 #  _           _                      
 # | |__   __ _| | __ _ _ __   ___ ___ 
 # | '_ \ / _` | |/ _` | '_ \ / __/ _ \
 # | |_) | (_| | | (_| | | | | (_|  __/
 # |_.__/ \__,_|_|\__,_|_| |_|\___\___|

def balance(u,type):
	# query = f'SELECT holics FROM users WHERE chat_id = {message.chat.id};'
	inline = InlineKeyboardMarkup()
	holics = db.dbget("holics", u.id)
	user = db.post_sql(f"SELECT * FROM users WHERE chat_id = {u.id}")
	isassets = db.post_sql(f"SELECT * FROM assets WHERE chat_id = {u.id}")
	name = u.first_name
	hunger = user[0][4]
	home = "🐶 бездомный\n"

	if user[0][4] > 0.1:
		h_timer = db.post_sql(f"SELECT time FROM timers WHERE chat_id = {u.id} AND timer = 'hunger' ")
		hung = int(user[0][4] - (int(time.time()) - h_timer[0][0]) / STUFF['hungerdec'])
		hung = hung if hung >= 0.1 else 0
		hunger = f"🍉 сытость: {hung} %"
	else:
		hunger = "🍉 голоден 😭"
	if user[0][7] != 0:
		# home = "🏠 живёт в домике"
		btn = InlineKeyboardButton(f"🏠 мой домик", callback_data=f"assets {u.id} check {user[0][7]} balance")
		# inline = InlineKeyboardMarkup()
		inline.add(btn)
		home = ""
	if isassets:
		assbtn = InlineKeyboardButton(f"🏩 активы", callback_data=f"assets {u.id} main")
		inline.add(assbtn)

	text = f"{name}\n💕 <b>{holics}</b> холиков \n\n{user[0][3]} {user[0][5]} уровень\n<i>({round(user[0][6],1)} XP из {user[0][5] * 100})</i>\n\n{hunger}\n{home}"
	holyshit = db.holyshit(u.id,"check")
	if holyshit:
		text += f"<b>Холи-щит</b> 🧿 {holy.since(holyshit)}"
	if type == "text":
		return text
	else:
		return inline


@dp.message_handler(commands=['balance'])
async def com_help(message: types.Message):
	# query = f'SELECT holics FROM users WHERE chat_id = {message.chat.id};'
	# inline = InlineKeyboardMarkup()
	# holics = db.dbget("holics", message.from_user.id)
	# user = db.post_sql(f"SELECT * FROM users WHERE chat_id = {message.from_user.id}")
	# name = message.from_user.first_name
	# hunger = user[0][4]
	# home = "🐶 бездомный "
	# if user[0][4] > 0.1:
	# 	h_timer = db.post_sql(f"SELECT time FROM timers WHERE chat_id = {message.from_user.id} AND timer = 'hunger' ")
	# 	hunger = f"🍉 сытость: {round(user[0][4] - (int(time.time()) - h_timer[0][0]) / 50, 1)} %"
	# else:
	# 	hunger = "🍉 голоден 😭"
	# if user[0][7] != 0:
	# 	# home = "🏠 живёт в домике"
	# 	btn = InlineKeyboardButton(f"🏠 мой домик", callback_data=f"assets check {user[0][7]}")
	# 	# inline = InlineKeyboardMarkup()
	# 	inline.add(btn)
	# 	home = ""

	# assbtn = InlineKeyboardButton(f"🏩 активы", callback_data=f"assets main")
	# inline.add(assbtn)


	await message.reply(balance(message.from_user,"text"),reply_markup=balance(message.from_user,"keyboards"))
	await db.hunger_check(message.from_user.id)


                              
#    ____ _____ _____ ___  ___  _____
#   / __ `/ __ `/ __ `__ \/ _ \/ ___/
#  / /_/ / /_/ / / / / / /  __(__  ) 
#  \__, /\__,_/_/ /_/ /_/\___/____/  
# /____/                             


@dp.message_handler(regexp="(^кк|бб)")
async def send(message: types.Message):

	await holy.roll("dice",message)

@dp.message_handler(regexp="(^мяч)")
async def send(message: types.Message):

	await holy.roll("ball",message)

@dp.message_handler(commands=['shop'])
async def send(message: types.Message):

	await message.reply(f"🎁 <b>Добро пожаловать 🎁\n               в холишоп</b>", reply_markup=shop.shop("shop_main"))

@dp.message_handler(text="!ttt")
async def send(message: types.Message):
	db.holyshit(message.from_user.id,"add")
	await message.reply(f"added")


@dp.message_handler(lambda message: message.reply_to_message and message.text == "!getjson")
async def send(message: types.Message):
	if str(message.from_user.id) == admin_id:
		await message.reply(message)

@dp.message_handler(regexp="^!donate")
async def send(message: types.Message):
	if str(message.from_user.id) == admin_id:
		text_arr = message.text.split(" ")
		user = text_arr[1]
		money = text_arr[2]
		holics = int(money) * STUFF['holicsprice']

		if int(money) >= 30:
			u_id = db.post_sql(f"SELECT chat_id FROM users WHERE username = '{user}' ")
			db.holyshit(int(u_id[0][0]),"add")

		check = db.post_sql(f"SELECT * FROM donaters WHERE username = '{user}'")
		if check:
			db.post_sql(f"UPDATE donaters SET money = money + {money} WHERE username = '{user}' ")
		else:
			db.post_sql(f"INSERT INTO donaters (username, money) VALUES ('{user}', {int(money)})")

		text = f"╔═══════════════════╗\n\n\
		     💖💫  <b>ОМАГАД!</b>  💫💖\n\n\
		          @{user}, задонатил\n\
		         и получил   <b>💕{holics}</b>\n\n\
╚═══════════════════╝"
		db.post_sql(f"UPDATE users SET holics = holics + {int(holics)} WHERE username = '{user}' ")
		await message.reply(f"Есть! Донат для {user} добавлен в базу 👍💕")
		await bot.send_message(chat_id=main_chat,text=text)

@dp.message_handler(regexp="^!addsome")
async def send(message: types.Message):
	if str(message.from_user.id) == admin_id:
		text_arr = message.text.split(" ")
		await message.reply(f"added {text_arr[1]}💕")
		db.post_sql(f"UPDATE users SET holics = holics + {text_arr[1]} WHERE chat_id = {admin_id}")


@dp.message_handler(lambda message: message.reply_to_message, regexp="(^отправить)")
async def send(message: types.Message):
	text_arr = message.text.split(" ")
	target = message.reply_to_message.from_user
	holics = db.dbget("holics", message.from_user.id)
	if text_arr[1].isnumeric():
		if holics >= int(text_arr[1]):
			await message.reply(f"💖 <i>{message.from_user.first_name}</i> отправил <i>\n@{target.username}</i> — <b>{text_arr[1]} холиков</b> 💕")
			db.post_sql(f"UPDATE users SET holics = holics - {text_arr[1]} WHERE chat_id = {message.from_user.id}")
			db.post_sql(f"UPDATE users SET holics = holics + {text_arr[1]} WHERE chat_id = {target.id}")
		else:
			await message.reply(f"🥺 недостаточно холиков, чувак")
	else:
		check = db.post_sql(f'SELECT * FROM items WHERE chat_id = {message.from_user.id} AND item = "{text_arr[1]}" ')
		if check:
			await message.reply(f"💖 <i>{message.from_user.first_name}</i> отправил <i>\n@{target.username}</i> — <b>{shop.i[text_arr[1]]['emoji']}{text_arr[1]}</b>")
			await db.add_item("-", message.from_user.id, text_arr[1])
			await db.add_item("+", target.id, text_arr[1])
		else:
			await message.reply(f"🥺 нельзя отправить то, чего нету")





@dp.callback_query_handler( regexp="(^shop)")
async def answer(callback_query: types.CallbackQuery):

	if callback_query.data == "shop_food":

		await callback_query.message.edit_text(f'🍌 <b>Еда</b>', 
			reply_markup=shop.shop(callback_query.data))

	if callback_query.data == "shop_tools":
		await callback_query.message.edit_text(f'🧸 <b>Штуки</b>', 
			reply_markup=shop.shop(callback_query.data))

	if callback_query.data == "shop_assets":
		await callback_query.message.edit_text(f'🏡 <b>Активы</b>', 
			reply_markup=shop.shop(callback_query.data))

	if callback_query.data == "shop_emoji":
		await callback_query.message.edit_text(f'Чтоб купить эмодзи, пропиши в чате\n<code>buyemoji 💩</code>\n<i>(вместо говна, само собой ваш эмодзи)\n</i>Цена: <b>1к</b> 💕', 
			reply_markup=shop.shop(callback_query.data))

	if callback_query.data == "shop_back":
		await callback_query.message.edit_text(f"🎁 <b>Добро пожаловать 🎁\n               в холишоп</b>", 
		reply_markup=shop.shop("shop_main"))		


	await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler( regexp="(^buy)")
async def answer(callback_query: types.CallbackQuery):
	items = callback_query.data.split("_")
	res = await db.shop_buy(callback_query.from_user.id,items[1])
	if res is True:
		await bot.answer_callback_query(callback_query.id)
		await bot.send_message(callback_query.message.chat.id,
			f"{callback_query.from_user.first_name} купил {shop.i[items[1]]['emoji']} -{shop.i[items[1]]['price']} 💕")
	else:
		await bot.answer_callback_query(callback_query.id, text="😭 недостаточно холи")




@dp.callback_query_handler( regexp="(^use)")
async def answer(callback_query: types.CallbackQuery):
	items = callback_query.data.split("_")
	if callback_query.from_user.id != int(items[2]):
		await bot.answer_callback_query(callback_query.id, text="Нельзя брать чужое 😈")
		return;
	chat_id = int(callback_query.from_user.id)
	item = items[1]
	check = db.post_sql(f'SELECT * FROM items WHERE chat_id = {chat_id} AND item = "{item}" ')
	if check:
		if shop.i[item]["type"] == "food":

			await bot.answer_callback_query(callback_query.id, text=f"+ 🍉 {int(shop.i[item]['value'])} %")
			await db.add_item("-", chat_id, item)
			await bot.edit_message_reply_markup(callback_query.message.chat.id,callback_query.message.message_id,reply_markup=itemskeyboard(chat_id))
			db.post_sql(f'UPDATE users SET hunger = hunger + {float(shop.i[item]["value"])} WHERE chat_id = {chat_id}')
			db.post_sql(f" UPDATE timers SET time = {int(time.time())} WHERE chat_id = {chat_id} AND timer = 'hunger'")
			# edit_message_reply_markup
# 	
	else:
		await bot.send_message(callback_query.message.chat.id,
			f"У тебя нету {shop.i[items[1]]['emoji']}")
		
		
		


	await bot.answer_callback_query(callback_query.id)

# ГРАБЕЖИ И ОТРАВЛЕНИЯ

@dp.message_handler(lambda message: message.reply_to_message, regexp="(^отравить|^травануть)")
async def send(message: types.Message):
	item = db.check_item(message.from_user.id,"отрава")
	if not item:
		await message.reply(f"Купи отраву для начала")
		return
	d_timer = db.timer_check(message.from_user.id, "otrava")
	if time.time() < d_timer[0][0]:
		t = holy.since(d_timer[0][0] - time.time())
		await message.reply(f"До следующего отравления\nосталось: <b>{t}</b>\nЖди 🦖")
		return
	target = message.reply_to_message.from_user
	await message.reply(f"Отравил!")
	await db.add_item("-", message.from_user.id, "отрава")
	db.post_sql(f"UPDATE users SET hunger = hunger - 50 WHERE chat_id = {target.id}")	
	db.post_sql(f"UPDATE timers SET time = {time.time()+ TIMERS['otrava']} WHERE chat_id = {message.from_user.id} AND timer = 'otrava' ")

@dp.message_handler(lambda message: message.reply_to_message, regexp="(^взорвать|^подорвать)")
async def send(message: types.Message):

	item = db.check_item(message.from_user.id,"динамит")
	if not item:
		await message.reply(f"Купи динамит для начала")
		return
	d_timer = db.timer_check(message.from_user.id, "dynamite")
	if time.time() < d_timer[0][0]:
		t = holy.since(d_timer[0][0] - time.time())
		await message.reply(f"До следующего подрыва\nосталось: <b>{t}</b>\nЖди 🦖")
		return
	target = message.reply_to_message.from_user
	home = db.dbget("home", target.id)
	if int(home) == 0:
		await message.reply(f"🙉 Что ты подрывать собрался? Он на улице живёт")
		return

	await message.reply(f"🧨 {message.from_user.first_name} подорвал домик {target.first_name}!")
	await db.add_item("-", message.from_user.id, "динамит")
	# db.post_sql(f"UPDATE users SET hunger = hunger - 50 WHERE chat_id = {target.id}")	
	db.post_sql(f"UPDATE timers SET time = {time.time()+20} WHERE chat_id = {message.from_user.id} AND timer = 'otrava' ")
	db.post_sql(f"UPDATE assets SET state = state - 50 WHERE chat_id = {message.from_user.id} AND rowid = {home} ")
	check = db.post_sql(f"SELECT state FROM assets WHERE rowid = {home}")
	if int(check[0][0]) <= 0:
		db.post_sql(f"UPDATE users SET home = 0 WHERE chat_id = {message.from_user.id}")
		db.post_sql(f"UPDATE assets SET state = 0 WHERE chat_id = {message.from_user.id} AND rowid = {home} ")



@dp.message_handler(lambda message: message.reply_to_message, regexp="(^ограбить|^грабануть)")
async def send(message: types.Message):
	d_timer = db.post_sql(f"SELECT time FROM timers WHERE chat_id = {message.from_user.id} AND timer = 'rob' ")
	if time.time() < d_timer[0][0]:
		t = holy.since(d_timer[0][0] - time.time())
		await message.reply(f"До следующего ограбления\nосталось: <b>{t}</b>\nЖди 🔫🦖")
		return

	target = message.reply_to_message.from_user
	await db.hunger_check(target.id)
	target_hunger = db.dbget("hunger", target.id)
	home = db.dbget("home", target.id)

	holyshit = db.holyshit(target.id,"check")
	if holyshit:
		await message.reply(f"<b>{target.first_name}</b> под защитой 🧿\n<code>Выбери другую жертву</code>")
		return

	if int(home) != 0:
		await message.reply(f"{target.first_name} в домике 🏠\nпососи")
		return

	if target_hunger == 0:
		gun = db.check_item(message.from_user.id,"пестик")
		if gun:
			chance = [1]
			amount_rand = [3,3,3,2.5,2.5,2.5,2,1.5]

		else:
			chance = [0,0,0,1]
			amount_rand = [7,7,6,6,5,5,5,5,4,4,4,3]
			
			
		if random.choice(chance) == 0:
			await message.reply(f"‼️ {message.from_user.first_name} попытался ограбить {target.first_name} но не получилось ...")
			db.post_sql(f"UPDATE timers SET time = {time.time()+TIMERS['rob_attempt']} WHERE chat_id = {message.from_user.id} AND timer = 'rob' ")	
			return

		amount = db.dbget("holics", target.id)
		amount = int(amount / int(random.choice(amount_rand)))
		await message.answer_animation("CgACAgQAAxkBAAIvoWAjo96LFMGOLNYgsEQXtwmjpE5aAAJiAgAC84o0Un_UeBSZfoYGHgQ")
		await asyncio.sleep(0.2)
		await message.reply(f"{message.from_user.first_name} 🔫 ограбил {target.first_name} на {amount} 💕")
		db.post_sql(f"UPDATE timers SET time = {time.time()+TIMERS['rob']} WHERE chat_id = {message.from_user.id} AND timer = 'rob' ")	
		db.post_sql(f"UPDATE users SET holics = holics - {amount} WHERE chat_id = {target.id}")	
		db.post_sql(f"UPDATE users SET holics = holics + {amount} WHERE chat_id = {message.from_user.id}")	
	else:
		await message.reply(f"🥺 низя, жертва сыта")

# ГРАБЕЖИ И ОТРАВЛЕНИЯ	


#pooling

if __name__ == "__main__":
	executor.start_polling(dp, on_startup=send_to_admin)