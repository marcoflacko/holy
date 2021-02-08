import sqlite3
from sqlite3 import Error
from shop import i




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
		insert_to_db_query = f'INSERT INTO users (chat_id, username, emoj) VALUES ({chat_id}, "{username}", "🐸");'
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
		await add_item("+", chat_id, item)
		return True

async def item_use(chat_id,item):
	check = post_sql(f'SELECT * FROM items WHERE chat_id = {chat_id} AND item = "{item}" ')
	if check:
		if i[item]["type"] == "food":
			await add_item("-", chat_id, item)
			# await post_sql(f'UPDATE items SET amount = amount {act} 1 WHERE chat_id = {chat_id} AND item = "{item}" ')

		return True
	else:
		
		return False



def enoughholy(chat_id, amount):

	holics = dbget("holics", chat_id)
	if int(holics) < int(amount):
		return False
	else:
		return True
# DATABASE