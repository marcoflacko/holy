from bot import bot
import db
import asyncio

async def roll(game,message):
	text_arr = message.text.split(" ")
	
	try:
		bet = int(text_arr[1])
	except (ValueError, IndexError):
		await message.reply("Не ввёл сумму")
		return
	# if type(bet) != int:
	# 	await message.reply("Ставка должна состоять из чисел")
	# 	return

	if bet < 1:
		return;
	if db.enoughholy(message.from_user.id,bet) is False:
		await message.reply("Недостаточно холиков")
		return

	profit = bet
	# DICE
	if game == "dice":
		dice = await bot.send_dice(chat_id=message.chat.id,emoji="🎲")
		result = ""
		game = "🎲"

		await asyncio.sleep(3.5)
		dice = dice.dice.value
		if (text_arr[0].lower() == "бб" and dice < 4) or (text_arr[0].lower() == "кк" and dice > 3):
			result = "win"
			act = "+"

		else: 
			result = "lose"
			act = "-"

	elif game == "ball":
		dice = await bot.send_dice(chat_id=message.chat.id,emoji="🏀")
		result = ""
		game = "🏀"

		await asyncio.sleep(3.5)
		dice = dice.dice.value
		if str(dice) in ("5","4") :
			result = "win"
			act = "+"
			profit = bet * 2

		else: 
			result = "lose"
			act = "-"


	db.post_sql(f"UPDATE users SET holics = holics {act} {bet} WHERE chat_id = {message.from_user.id}")	
	holics = db.dbget("holics", message.from_user.id)
	await message.reply(f"{game} — <i>{result}</i>\n💕 {holics} ({act}{profit})")

	# await asyncio.sleep(1)
	# text = f"{text_arr[0]}-шнул и поставил {bet}, выпало {dice.dice.value}"
	# await message.reply(text)

