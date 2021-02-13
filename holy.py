import bot
import db
import asyncio
import math

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
		return
	if db.enoughholy(message.from_user.id,bet) is False:
		await message.reply("Недостаточно холиков")
		return

	profit = bet
	# DICE
	if game == "dice":
		dice = await bot.bot.send_dice(chat_id=message.chat.id, emoji="🎲")
		result = ""
		game = "🎲"

	
		await asyncio.sleep(3)
		dice = dice.dice.value
		if (text_arr[0].lower() == "бб" and dice < 4) or (text_arr[0].lower() == "кк" and dice > 3):
			result = "win"
			act = "+"

		else: 
			result = "lose"
			act = "-"

	elif game == "ball":
		dice = await bot.bot.send_dice(chat_id=message.chat.id,emoji="🏀")
		result = ""
		game = "🏀"

		await asyncio.sleep(3.3)
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
	await addxp(message.from_user.id, bet)

	# await asyncio.sleep(1)
	# text = f"{text_arr[0]}-шнул и поставил {bet}, выпало {dice.dice.value}"
	# await message.reply(text)




def since(since):
    if since < 1:
        return 0
        
    chunks = [[60*60*24*365, 'year'],[60*60*24*30, 'month'],[60*60*24*7, 'week'],[60*60*24, 'день'],[60*60, 'час'],[60, 'минут'],[1,'секунд']]
    i = 0
    j = len(chunks)

    while i < j:
        i += 1
        seconds = chunks[i][0]
        name = chunks[i][1]
        count = (math.floor(since / seconds))
        if count != 0:
            
            break
    if count == 1 and name in ("секунд","минут"):
        name = name + "а"
    elif count > 1 and count < 5 and name in ("секунд","минут"):
        name = name + "ы"
    elif count > 1 and count < 5 and name in ("час"):
        name = name + "а"
    elif count > 4 and name in ("час"):
        name = name + "ов"
    elif count > 1 and count < 5 and name in ("день"):
        name = "дня"
    elif count > 4 and name in ("день"):
        name = "дней"
    p = f"{count} {name}"
    return p






async def addxp(chat_id, bet):
	user = db.post_sql(f"SELECT * FROM users WHERE chat_id = {chat_id}")
	holics = user[0][2]
	lvl = user[0][5]
	oldxp = user[0][6]

	if holics < 500:
		holics = 1
	elif holics >= 500 and holics < 100:
		holics = 1.5
	elif holics >= 1000 and holics < 10000:
		holics = 1.7
	elif holics >= 10000:
		holics = 2

	xp = round((bet / holics) / (lvl * 50),2)

	db.post_sql(f"UPDATE users SET xp = xp + {round(xp,1)} WHERE chat_id = {chat_id}")

	if (oldxp + xp) >= (100*lvl):
		hol_am = ((lvl+1)*200)
		await bot.bot.send_message(chat_id, f"💫 Крутяк! Ты апнул новый уровень!\n И получил {hol_am} 💕")
		db.post_sql(f"UPDATE users SET xp = 0 WHERE chat_id = {chat_id}")
		db.post_sql(f"UPDATE users SET lvl = {lvl+1} WHERE chat_id = {chat_id}")
		db.post_sql(f"UPDATE users SET holics = holics + {int(hol_am)} WHERE chat_id = {chat_id}")


