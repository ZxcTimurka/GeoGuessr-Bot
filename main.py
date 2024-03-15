import telebot
from config import TOKEN
token = TOKEN
bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['location'])
def start_message(message):
    bot.send_message(message.chat.id, f"{message.location.latitude, message.location.longitude}")


bot.infinity_polling()
