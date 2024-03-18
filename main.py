import telebot
from config import TOKEN
from get_distance import getDistance
from check_coords import check
from get_image import getImage, getImages

token = TOKEN
bot = telebot.TeleBot(token)
photo = ''


@bot.message_handler(commands=['start'])
def start_message(message):
    global photo
    photo = getImage()
    bot.send_photo(message.chat.id, photo, caption='Отправь мне координаты этого места')


@bot.message_handler(content_types=['location'])
def start_message(message):
    global photo
    if not photo:
        bot.send_message(message.chat.id, 'Cначала нажми кнопку /start')
        return
    msg = tuple([message.location.latitude, message.location.longitude])
    name = tuple([float(i) for i in photo.name.replace('images/', '').replace('.jpeg', '').split(', ')])
    img1 = check(name, msg)
    bot.send_photo(message.chat.id, img1, caption=getDistance(*name, *msg))


@bot.message_handler(content_types=['text'])
def start_message(message):
    if message.text.isdigit():
        try:
            imgs = getImages(int(message.text))
            bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(i) for i in imgs])
        except ValueError:
            bot.send_message(message.chat.id, 'Неверный ввод')


bot.infinity_polling()
