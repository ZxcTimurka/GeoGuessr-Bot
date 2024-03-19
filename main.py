import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from check_coords import check
from config import TOKEN
from get_distance import getDistance
from get_image import getImage, getImages

token = TOKEN
bot = telebot.TeleBot(token)
photo = ''


@bot.message_handler(commands=['start'])
def start_message(message):
    text = 'Привет!'
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Играть', callback_data='play'),
               InlineKeyboardButton('Рейтинг', callback_data='rate'))
    markup.row(InlineKeyboardButton('Добавить локацию', callback_data='add'))
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'play':
        game_message(call.message)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == "back":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start_message(call.message)


def game_message(message):
    global photo
    photo = getImage()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Верунться назад', callback_data='back'),
               InlineKeyboardButton('Рейтинг', callback_data='rate'))
    bot.send_photo(message.chat.id, photo, caption='Отправь мне координаты этого места', reply_markup=markup)


@bot.message_handler(content_types=['location'])
def fgh_message(message):
    global photo
    if not photo:
        bot.send_message(message.chat.id, 'Cначала нажми кнопку /start')
        return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Верунться назад', callback_data='back'),
               InlineKeyboardButton('Рейтинг', callback_data='rate'))
    msg = tuple([message.location.latitude, message.location.longitude])
    name = tuple([float(i) for i in photo.name.replace('images/', '').replace('.jpeg', '').split(', ')])
    img1 = check(name, msg)
    bot.send_photo(message.chat.id, img1, caption=getDistance(*name, *msg), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def asd_message(message):
    if message.text.isdigit():
        try:
            imgs = getImages(int(message.text))
            bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(i) for i in imgs])
        except ValueError:
            bot.send_message(message.chat.id, 'Неверный ввод')


bot.infinity_polling()
