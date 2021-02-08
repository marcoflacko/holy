from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

i = {
  "бургерок": {"type": "food", "price": 40, "value": 50, "emoji": "🍔"},
  "сочок": {"type": "food", "price": 40, "value": 30, "emoji": "🧃"},
  "пестик": {"type": "tool", "price": 1500, "emoji": "🔫"},
  "отрава": {"type": "tool", "price": 60, "value": 50, "emoji": "🏴‍☠️"}


}

def shop(page):
	if page == "shop_main":
		btn_1 = InlineKeyboardButton("Еда 🍔", callback_data="shop_food")
		btn_2 = InlineKeyboardButton("Штуки 🔫", callback_data="shop_tools")
		btn_3 = InlineKeyboardButton("Активы 🏡", callback_data="shop_assets")
		btn_4 = InlineKeyboardButton("Эмодзи 💖", callback_data="shop_emoji")

		inline = InlineKeyboardMarkup().add(btn_1).add(btn_2).add(btn_3).add(btn_4)
		
	if page == "shop_food":
		btn_1 = InlineKeyboardButton("🍔\t\tбургерок\t\t💕40", callback_data="buy_бургерок")
		btn_2 = InlineKeyboardButton("🧃\t\tсочок\t\t💕40", callback_data="buy_сочок")
		btn_3 = InlineKeyboardButton("🙅‍♂️\t\tназад", callback_data="shop_back")

		inline = InlineKeyboardMarkup().add(btn_1).add(btn_2).add(btn_3)

	if page == "shop_tools":
		btn_1 = InlineKeyboardButton("🔫\t\tпестик\t\t💕1500", callback_data="buy_пестик")
		btn_2 = InlineKeyboardButton("🏴‍☠️\t\tотрава\t\t💕40", callback_data="buy_отрава")
		btn_3 = InlineKeyboardButton("🧨\t\tдинамит\t\t💕40", callback_data="buy_динамит")
		btn_4 = InlineKeyboardButton("🙅‍♂️\t\tназад", callback_data="shop_back")

		inline = InlineKeyboardMarkup().add(btn_1).add(btn_2).add(btn_3).add(btn_4)

	if page == "shop_assets":
		btn_1 = InlineKeyboardButton("🏠\t\tдомик\t\t💕1500", callback_data="buy_домик")
		btn_2 = InlineKeyboardButton("💒\t\tхолизавод\t\t💕40", callback_data="buy_холизавод")
		btn_3 = InlineKeyboardButton("🏩\t\tотель\t\t💕40", callback_data="buy_отель")
		btn_4 = InlineKeyboardButton("🙅‍♂️\t\tназад", callback_data="shop_back")

		inline = InlineKeyboardMarkup().add(btn_1).add(btn_2).add(btn_3).add(btn_4)	

	if page == "shop_emoji":
		btn_1 = InlineKeyboardButton("🏠\t\t💕1500", callback_data="yo")
		btn_2 = InlineKeyboardButton("💒\t\t💕40", callback_data="yo")
		btn_3 = InlineKeyboardButton("🏩\t\t💕40", callback_data="yo")
		btn_4 = InlineKeyboardButton("🙅‍♂️\t\tназад", callback_data="shop_back")

		inline = InlineKeyboardMarkup().add(btn_1).add(btn_2).add(btn_3).add(btn_4)	

	return inline

