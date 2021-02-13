import sqlite3
from sqlite3 import Error
from shop import i
import time
from config import STUFF, TIMERS




#  DATABASE
def dbget(item, chat_id):
	with sqlite3.connect('holygame.db') as connection:
		cursor = connection.cursor()
		cursor.execute(f"SELECT {item} FROM users WHERE chat_id = {chat_id}")
		result = cursor.fetchall()

		return result[0][0]


def post_sql(sql_query):
	with sqlite3.connect('holygame.db') as connection:
		cursor = connection.cursor()
		try:
			cursor.execute(sql_query)
		except Error:
			pass

		result = cursor.fetchall()
		return result

def user_reg(chat_id,username):
	user_check_query = f'SELECT * FROM users WHERE chat_id = {chat_id};'
	user_check_data = post_sql(user_check_query)
	if not user_check_data:
		dic = {"holyshit": "False"}
		insert_to_db_query = f'INSERT INTO users (chat_id, username, emoj, dic) VALUES ({chat_id}, "{username}", "🐸", "{dic}");'
		post_sql(insert_to_db_query)
		print(f'user {username} added')

async def add_item(act, chat_id, item):
	# post_sql(f'INSERT INTO users (chat_id, username, emoj) VALUES ({chat_id}, "{username}", "🐸");')
		i_type = i[item]["type"]
		check = post_sql(f'SELECT * FROM items WHERE chat_id = {chat_id} AND item = "{item}" ')

		if not check:
			post_sql(f'INSERT INTO items (chat_id, item, type) VALUES ("{chat_id}", "{item}", "{i_type}") ')

		else:
			post_sql(f'UPDATE items SET amount = amount {act} 1 WHERE chat_id = {chat_id} AND item = "{item}" ')
			if act == "-" and (int(check[0][2])-1) == 0 :
				post_sql(f'DELETE FROM items WHERE chat_id = {chat_id} AND item = "{item}" ')

async def shop_buy(chat_id,item):
	if i[item]['price'] > dbget("holics", chat_id):
		return False
	else:
		if i[item]['type'] == "asset":
			user = post_sql(f"SELECT * FROM users WHERE chat_id = {chat_id}")
			post_sql(f'INSERT INTO assets (chat_id, asset, ownerinfo, dwellerinfo) VALUES ("{chat_id}", "{item}", "{user[0][1]};{user[0][3]}", "{user[0][1]};{user[0][3]};{user[0][0]};0") ')
			if item == 'домик':
				rowid = post_sql(f"SELECT rowid FROM assets WHERE chat_id = {chat_id} and asset = 'домик' ")
				post_sql(f'UPDATE users SET home = {rowid[-1][0]} WHERE chat_id = {chat_id}')
			return True
		await add_item("+", chat_id, item)
		post_sql(f"UPDATE users SET holics = holics - {int(i[item]['price'])} WHERE chat_id = {chat_id}")	
		return True

def holyshit(chat_id,act):
	if act == "add":
		print("added")
		post_sql(f"INSERT INTO timers (chat_id, timer, time) VALUES ('{chat_id}','holyshit','{int(time.time()+TIMERS['holyshit'])}')")
	elif act == "check":
		check = post_sql(f"SELECT * FROM timers WHERE chat_id = '{chat_id}' AND timer = 'holyshit' ")
		if check:
			if time.time() > int(check[0][2]):
				post_sql(f"DELETE FROM timers WHERE chat_id = '{chat_id}' AND timer = 'holyshit'") 
				return False
			return int(check[0][2] - time.time())
			print("checked")

def check_item(chat_id, item):
	check = post_sql(f'SELECT * FROM items WHERE chat_id = {chat_id} AND item = "{item}" ')
	if check:
		return True
	else:
		return False

async def item_use(chat_id,item):
	check = post_sql(f'SELECT * FROM items WHERE chat_id = {chat_id} AND item = "{item}" ')
	if check:
		if i[item]["type"] == "food":
			await add_item("-", chat_id, item)
			post_sql(f'UPDATE users SET hunger = hunger + {i[item]["value"]} WHERE chat_id = {chat_id}" ')

		return True
	else:
		
		return False

async def hunger_check(chat_id):
	check = post_sql(f'SELECT time FROM timers WHERE chat_id = {chat_id} AND timer = "hunger" ')
	decrease = round((int(time.time()) - check[0][0]) / STUFF['hungerdec'],2)
	post_sql(f"UPDATE users SET hunger = hunger - {decrease} WHERE chat_id = {chat_id};")
	post_sql(f" UPDATE timers SET time = {int(time.time())} WHERE chat_id = {chat_id} AND timer = 'hunger'")

def timer_check(chat_id, timer):
	check = post_sql(f'SELECT * FROM timers WHERE chat_id = {chat_id} AND timer = "{timer}" ')
	if not check:
		post_sql(f'INSERT INTO timers (chat_id, timer, time) VALUES ({chat_id}, "{timer}", {int(time.time())}) ')

	d_timer = post_sql(f"SELECT time FROM timers WHERE chat_id = {chat_id} AND timer = '{timer}' ")
	return d_timer

def enoughholy(chat_id, amount):

	holics = dbget("holics", chat_id)
	if int(holics) < int(amount):
		return False
	else:
		return True
# DATABASE