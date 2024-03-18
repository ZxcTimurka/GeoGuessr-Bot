import telebot
from config import TOKEN
from get_distance import getDistance
from check_coords import check

token = TOKEN
bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['location'])
def start_message(message):
    msg = tuple([message.location.longitude, message.location.latitude])
    print(56.475772, 84.949756, *msg)
    img1 = check((84.949756, 56.475772,), msg)
    bot.send_photo(message.chat.id, img1, caption=getDistance(56.475772, 84.949756, msg[1], msg[0]))


@bot.message_handler(content_types=['text'])
def start_message(message):
   bot.send_message('ss')


bot.infinity_polling()
