import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.async_telebot import AsyncTeleBot

import asyncio
from datetime import time
import aioschedule as schedule
import time


from check_coords import check
from config import TOKEN
from get_distance import getDistance
from get_image import getImages, getImage
from online_db import add_player, print_curr_img, update_curr_img, update_time_bool, print_time_bool
from db import search_by_coords

token = TOKEN
bot = AsyncTeleBot(token)


@bot.message_handler(commands=['start'])
async def start_message(message):
    name = message.from_user.first_name
    add_player(message.chat.id, name, 0, 0, 0)
    text = f'Привет, {name}!'
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
    if call.data == 'classic_mode':
        await classic_mode(call.message)
        if call.message.content_type != 'photo':
            await bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == 'time_mode':
        await time_mod(call.message)
        if call.message.content_type != 'photo':
            await bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.message_handler(content_types=['location'])
async def fgh_message(message):
    print(print_curr_img(message.chat.id)[0])
    print('ok')

    if not print_curr_img(message.chat.id)[0]:
        await bot.send_message(message.chat.id, 'Cначала нажми кнопку /start')
        return
    # print(print_time_bool(message.chat.id))
    # if print_time_bool(message.chat.id):
    #     update_time_bool(message.chat.id, False)
    #     await bot.send_message(message.chat.id, 'Время вышло')
    #     await game_mods()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Назад', callback_data='play'),
                InlineKeyboardButton('Продолжить', callback_data='classic_mode'))
    msg = tuple([message.location.latitude, message.location.longitude])
    name = tuple([float(i) for i in
                    ''.join(print_curr_img(message.chat.id)).replace('images/', '').replace('.jpeg', '').split(
                        ', ')])
    await bot.send_photo(message.chat.id, check(name, msg), caption=f'{getDistance(*name, *msg)} - {search_by_coords(*name)[0]}', reply_markup=markup)
    update_curr_img(message.chat.id, None)


@bot.message_handler(content_types=['text'])
async def asd_message(message):
    if message.text.isdigit():
        try:
            imgs = getImages(int(message.text))
            await bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(i) for i in imgs])
        except ValueError:
            await bot.send_message(message.chat.id, 'Неверный ввод')


async def game_mods(message):
    text = 'Отлично! Выбери режим игры😉'
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton('Обычный', callback_data='classic_mode'),
               InlineKeyboardButton('На время', callback_data='time_mode'),
               InlineKeyboardButton('Онлайн', callback_data='online_mode'))
    markup.row(InlineKeyboardButton('Описание режимов', callback_data='des_game_mode'))
    await bot.send_message(message.chat.id, text, reply_markup=markup)


async def classic_mode(message):
    photo = getImage()
    update_curr_img(message.chat.id, photo.name)
    print(print_curr_img(message.chat.id))
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Верунться назад', callback_data='play'))
    await bot.send_photo(message.chat.id, photo, caption='Отправь мне координаты этого места', reply_markup=markup)



async def time_mod(message):
    photo = getImage()
    update_curr_img(message.chat.id, photo.name)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Верунться назад', callback_data='play'))
    markup_lose = InlineKeyboardMarkup()
    markup_lose.add(InlineKeyboardButton('Начать заново', callback_data='time_mode'),
                    InlineKeyboardButton('Выбрать режим', callback_data='play'))
    await bot.send_photo(message.chat.id, photo, caption='Отправь мне координаты этого места!!!', reply_markup=markup)
    schedule.every(3).seconds.do(stop_schedule, message=message)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(schedule.run_pending())
    time.sleep(0.1)


def stop_schedule(message):
    print(schedule.get_jobs())
    schedule.cancel_job(schedule.get_jobs()[0])
    update_time_bool(message.chat.id, True)






asyncio.run(bot.polling())