import logging
import asyncio
import sqlite3
from sqlite3 import Error
import holy
import db
import shop

from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, admin_id

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, loop=loop)






#funcs

async def send_to_admin(dp):
	await bot.send_message(chat_id=admin_id, text="Bot is activated 💫")

#funcs

#handlers

@dp.message_handler(commands=['rate'])
async def com_help(message: types.Message):
	items = db.post_sql(f"SELECT * FROM users ORDER BY holics DESC LIMIT 10")
	rate = "💫 Красавчики 💫\n\n";
	num = 1
	for item in items:
		rate += f"{str(item[3])}\t\t{num}\t\t<code>{str(item[1])}</code>\t\t <b>{str(item[2])}</b> 💕\n"
		num += 1
	await message.reply(rate)

@dp.message_handler(commands=['items'])
async def com_help(message: types.Message):
	items = db.post_sql(f"SELECT * FROM items WHERE chat_id = {message.from_user.id} ORDER BY type")
	rate = f"<b>{message.from_user.first_name}</b>\n<i>твои предметы</i> 🧤\n┄┄┄┄┄┄┄┄┄\n";
	num = 1
	inline = InlineKeyboardMarkup()
	for item in items:
		if(item[3] == "food"):
			btn = InlineKeyboardButton(f"{shop.i[item[1]]['emoji']}\t\t({str(item[2])})", callback_data=f"use_{item[1]}_{message.from_user.id}")
			inline.insert(btn)
		else:	
			rate += f" <code>({str(item[2])})</code>\t\t{shop.i[item[1]]['emoji']}\t\t{str(item[1])}\n"

		num += 1
	# btn_1 = InlineKeyboardButton("использовать 🧤", callback_data="shop_food")
	# inline = InlineKeyboardMarkup().add(btn_1)
	await message.reply(rate, reply_markup=inline)

@dp.message_handler(commands=['help'])
async def com_help(message: types.Message):
	await message.reply("Привет, это обновлённый HolyGame!")

@dp.message_handler(commands=['start'])
async def com_help(message: types.Message):
	db.user_reg(message.from_user.id,message.from_user.username)
	await message.reply(f"Привет {message.from_user.username}")

@dp.message_handler(commands=['remove'])
async def com_help(message: types.Message):
	db.post_sql(f"UPDATE users SET holics = holics - 5 WHERE chat_id = {message.chat.id}")
	await message.reply("минусанул")

@dp.message_handler(commands=['balance'])
async def com_help(message: types.Message):
	# query = f'SELECT holics FROM users WHERE chat_id = {message.chat.id};'
	holics = db.dbget("holics", message.from_user.id)
	name = message.from_user.first_name
	user = db.post_sql(f"SELECT * FROM users WHERE chat_id = {message.from_user.id}")

	await message.reply(f"{name}\n💕 <b>{holics}</b> холиков \n\n{user[0][3]} 1 уровень")
	

                              
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

@dp.message_handler(text="/shop")
async def send(message: types.Message):

	await message.reply(f"Добро пожаловать\nв холишоп", reply_markup=shop.shop("shop_main"))





@dp.callback_query_handler( regexp="(^shop)")
async def answer(callback_query: types.CallbackQuery):
	if callback_query.data == "shop_food":
		await callback_query.message.edit_text(f'еда', 
			reply_markup=shop.shop(callback_query.data))

	if callback_query.data == "shop_tools":
		await callback_query.message.edit_text(f'еда', 
			reply_markup=shop.shop(callback_query.data))

	if callback_query.data == "shop_assets":
		await callback_query.message.edit_text(f'еда', 
			reply_markup=shop.shop(callback_query.data))

	if callback_query.data == "shop_emoji":
		await callback_query.message.edit_text(f'еда', 
			reply_markup=shop.shop(callback_query.data))

	if callback_query.data == "shop_back":
		await callback_query.message.edit_text(f'Добро пожаловать\nв холишоп', 
		reply_markup=shop.shop("shop_main"))		


	await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler( regexp="(^buy)")
async def answer(callback_query: types.CallbackQuery):
	items = callback_query.data.split("_")
	res = await db.shop_buy(callback_query.from_user.id,items[1])
	if res is True:
		await bot.send_message(callback_query.message.chat.id,
			f"{callback_query.from_user.first_name} купил {shop.i[items[1]]['emoji']} -{shop.i[items[1]]['price']} 💕")


	await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler( regexp="(^use)")
async def answer(callback_query: types.CallbackQuery):
	items = callback_query.data.split("_")
	if callback_query.from_user.id != int(items[2]):
		await bot.answer_callback_query(callback_query.id, text="Нельзя брать чужое 😈")
		return;
	res = await db.item_use(callback_query.from_user.id,items[1])
	if res is True:
		await bot.send_message(callback_query.message.chat.id,
			f"Юзнул")


	await bot.answer_callback_query(callback_query.id)
	


#pooling

if __name__ == "__main__":
	executor.start_polling(dp, on_startup=send_to_admin)