from config import timevert
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

i = {
  "бургерок": {"type": "food", "price": 95, "value": 50, "emoji": "🍔"},
  "сочок": {"type": "food", "price": 40, "value": 30, "emoji": "🧃"},
  "пестик": {"type": "tool", "price": 10500, "emoji": "🔫"},
  "отрава": {"type": "tool", "price": 500, "value": 50, "emoji": "🏴‍☠️"},
  "динамит": {"type": "tool", "price": 1200, "value": 50, "emoji": "🧨"},
  "домик": {"type": "asset", "price": 100000, "emoji": "🏠"},
  "холизавод": {"type": "asset", "price": 1000000, "emoji": "🏭"}


}

def shop(page):
	if page == "shop_main":
		btn_1 = InlineKeyboardButton(f"Еда 🍔", callback_data="shop_food")
		btn_2 = InlineKeyboardButton(f"Штуки 🔫", callback_data="shop_tools")
		btn_3 = InlineKeyboardButton(f"Активы 🏡", callback_data="shop_assets")
		btn_4 = InlineKeyboardButton(f"Эмодзи 💖", callback_data="shop_emoji")

		inline = InlineKeyboardMarkup().add(btn_1).add(btn_2).add(btn_3).add(btn_4)
		
	if page == "shop_food":
		btn_1 = InlineKeyboardButton(f"🍔\t\tбургерок\t\t💕{i['бургерок']['price']}", callback_data="buy_бургерок")
		btn_2 = InlineKeyboardButton(f"🧃\t\tсочок\t\t💕{i['сочок']['price']}", callback_data="buy_сочок")
		btn_3 = InlineKeyboardButton(f"🙅‍♂️\t\tназад", callback_data="shop_back")

		inline = InlineKeyboardMarkup().add(btn_1).add(btn_2).add(btn_3)

	if page == "shop_tools":
		btn_1 = InlineKeyboardButton(f"🔫\t\tпестик\t\t💕{timevert(i['пестик']['price'])}", callback_data="buy_пестик")
		btn_2 = InlineKeyboardButton(f"🏴‍☠️\t\tотрава\t\t💕{timevert(i['отрава']['price'])}", callback_data="buy_отрава")
		btn_3 = InlineKeyboardButton(f"🧨\t\tдинамит\t\t💕{timevert(i['динамит']['price'])}", callback_data="buy_динамит")
		btn_4 = InlineKeyboardButton(f"🙅‍♂️\t\tназад", callback_data="shop_back")

		inline = InlineKeyboardMarkup().add(btn_1).add(btn_2).add(btn_3).add(btn_4)

	if page == "shop_assets":
		btn_1 = InlineKeyboardButton(f"🏠\t\tдомик\t\t💕{timevert(i['домик']['price'])}", callback_data="buy_домик")
		btn_2 = InlineKeyboardButton(f"💒\t\tхолизавод\t\t💕{timevert(i['холизавод']['price'])}", callback_data="buy_холизавод")
		btn_3 = InlineKeyboardButton(f"🏩\t\tотель\t\t💕(скоро)", callback_data="buy_отель")
		btn_4 = InlineKeyboardButton(f"🙅‍♂️\t\tназад", callback_data="shop_back")

		inline = InlineKeyboardMarkup().add(btn_1).add(btn_2).add(btn_3).add(btn_4)	

	if page == "shop_emoji":

		btn_4 = InlineKeyboardButton(f"🙅‍♂️\t\tназад", callback_data="shop_back")

		inline = InlineKeyboardMarkup().add(btn_4)	

	return inline

