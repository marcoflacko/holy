BOT_TOKEN = "1342370248:AAG49A39deLD32_7wGj_O8Z_cs72_3-aKBc"
admin_id = "389539950"
main_chat = "-1001406084077"

TIMERS = {
    'daily': 28800,
    'rob': 3600,
    'rob_attempt': 1200,
    'otrava': 3600,
    'holyshit': 172850
}


STUFF = {
	'holicsprice': 200,
	'hungerdec': 450
}


TEXTS = {

	"help_message": "В основе всего тут лежат азартные игры, кости 🎲, слот 🎰 и даже баскетбол 🏀. \
Все ставки делаются на ХОЛИКИ 💕, это наша виртуальная валюта. Чем больше холиков тем ты выше в \
рейтинге, чем их больше тем больше власти и возможностей. За холики можно купить пистолет и \
грабить людей, или можно купить дом и обезопасить себя от ограбления, или же можно сдавать дом \
в аренду получая от этого холики 💕, а если ты супер богач то можно приобрести завод и люди \
будут на нём батрачить на тебя. Если ты конечно всё не сольёшь в один миг, или тебя не ограбят ночью."

}

def timevert(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'k', 'm', 'b', 't'][magnitude])