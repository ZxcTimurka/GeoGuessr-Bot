import telebot
from config import TOKEN
from check_coords import check

token = TOKEN
bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['location'])
def start_message(message):
    bot.send_message(message.chat.id, f"{message.location.latitude, message.location.longitude}")


@bot.message_handler(content_types=['text'])
def start_message(message):
    msg = [float(i) for i in message.text.split(', ')]
    print((56.475772, 84.949756,), msg)
    img1, img2 = check((56.475772, 84.949756,), (message.text))
    bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(img1), telebot.types.InputMediaPhoto(img2)])


bot.infinity_polling()
