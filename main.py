import telebot

import aiohttp
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.async_telebot import AsyncTeleBot
import asyncio

from check_coords import check
from config import TOKEN
from get_distance import getDistance
from get_image import getImages, getImage


token = TOKEN
bot = AsyncTeleBot(token)
photo = ''


@bot.message_handler(commands=['start'])
async def start_message(message):
    text = 'Привет!'
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Играть', callback_data='play'),
               InlineKeyboardButton('Рейтинг', callback_data='rate'))
    markup.row(InlineKeyboardButton('Добавить локацию', callback_data='add'))
    await bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    if call.data == "back":
        await game_mods(call.message)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'play':
        await game_mods(call.message)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'classic_mode':
        await game_message(call.message)
        print(call.message)
        if call.message.content_type != 'photo':
            await bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.message_handler(content_types=['location'])
async def fgh_message(message):
    global photo
    if not photo:
        await bot.send_message(message.chat.id, 'Cначала нажми кнопку /start')
        return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Назад', callback_data='play'),
               InlineKeyboardButton('Продолжить', callback_data='classic_mode'))
    msg = tuple([message.location.latitude, message.location.longitude])
    name = tuple([float(i) for i in photo.name.replace('images/', '').replace('.jpeg', '').split(', ')])
    await bot.send_photo(message.chat.id, check(name, msg), caption=getDistance(*name, *msg), reply_markup=markup)


@bot.message_handler(content_types=['text'])
async def asd_message(message):
    if message.text.isdigit():
        try:
            imgs = getImages(int(message.text))
            await bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(i) for i in imgs])
        except ValueError:
            await bot.send_message(message.chat.id, 'Неверный ввод')


async def game_message(message):
    global photo
    photo = getImage()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Верунться назад', callback_data='back'))
    await bot.send_photo(message.chat.id, photo, caption='Отправь мне координаты этого места', reply_markup=markup)


async def game_mods(message):
    text = 'Отлично! Выбери режим игры😉'
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Обычный', callback_data='classic_mode'),
               InlineKeyboardButton('На время', callback_data='time_mode'),
               InlineKeyboardButton('Онлайн', callback_data='online_mode'))
    markup.row(InlineKeyboardButton('Описание режимов', callback_data='des_game_mode'))
    await bot.send_message(message.chat.id, text, reply_markup=markup)



asyncio.run(bot.polling())
